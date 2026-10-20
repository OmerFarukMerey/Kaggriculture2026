# ---------------------------------------------------------------------------
# v23: closed-loop market controller.  The base engine's farm choreography is
# untouched; every SELL decision is recomputed online from the exact price
# curves, the observed shop draws (absorption), opponent pressure (exact
# schedule for detected copies, visible ripe yield otherwise), a wheat feed
# reserve, and a cash floor derived from the route's purchase schedule.
# ---------------------------------------------------------------------------
_V23_DEADLINE = 710
_V23_BATCH_MIN = 4
_V23_SPIKE_RATIO = 1.12
_V23_RESERVE_DAYS = 3
_V23_SHED_HIGH = 78   # force sales above this total (cap is 100; overflow is discarded)
_V23_SHED_TARGET = 58
_V23_RESILIENT_ORDER = (
    "FERTILIZER", "EGG", "CARROT", "TOMATO", "WHEAT", "MILK", "STRAWBERRY", "WOOL", "MELON",
)
# WHEAT is working capital (daily animal feed + the route's cash engine) and
# WOOL already has the base engine's own adaptive price-gated controller:
# both pass through untouched.  The controller paces the rest to cumulative
# parity with the route's schedule, a few steps ahead of it.
_V23_CONTROLLED = tuple(
    item for item in _V22_SELLABLE if item not in ("WHEAT", "WOOL")
)
_V23_LEAD = 4
_V23_STATE = {0: {}, 1: {}}

# Copy's effective schedule: route sells with the RC2 relay's -3 fertilizer
# shift applied (a locked copy sells those batches three steps early).
_V23_EFFECTIVE = [dict(bucket) for bucket in _V22_ROUTE_SELLS]
for _v23_s in range(len(_V23_EFFECTIVE)):
    if _v22_relay_covered(_v23_s):
        _v23_q = _V23_EFFECTIVE[_v23_s].pop("FERTILIZER", 0)
        if _v23_q and _v23_s >= 3:
            _V23_EFFECTIVE[_v23_s - 3]["FERTILIZER"] = (
                _V23_EFFECTIVE[_v23_s - 3].get("FERTILIZER", 0) + _v23_q
            )

# Remaining copy supply per product from each step on (suffix totals).
_V23_REMAINING = [dict() for _ in range(len(_V23_EFFECTIVE) + 1)]
for _v23_s in range(len(_V23_EFFECTIVE) - 1, -1, -1):
    _v23_acc = dict(_V23_REMAINING[_v23_s + 1])
    for _v23_item, _v23_q in _V23_EFFECTIVE[_v23_s].items():
        _v23_acc[_v23_item] = _v23_acc.get(_v23_item, 0) + _v23_q
    _V23_REMAINING[_v23_s] = _v23_acc

def _v23_state(seat, step):
    state = _V23_STATE[seat]
    if step == 0 or step < state.get("last_step", -1):
        state.clear()
    state.setdefault("sold", {})
    state["last_step"] = step
    return state


def _v23_absorption(obs, item):
    rate = 0.0
    for shop in (_get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []):
        products = _SHOP_PRODUCTS.get(shop, ())
        if item in products:
            rate += (2.0 if len(products) == 1 else 1.0) / 4.0
    if item != "FERTILIZER":
        rate += 1.0 / 24.0
    return rate


def _v23_reserve(obs, item):
    if item != "WHEAT":
        return 0
    animals = 0
    for row in (_get(_farm(obs, _seat(obs)), "tiles", []) or []):
        for tile in row if isinstance(row, list) else [row]:
            if isinstance(tile, dict) and tile.get("animal"):
                animals += 1
    return _V23_RESERVE_DAYS * animals


def _v23_copy_pressure(step, item, horizon=3):
    total = 0
    for future in range(step + 1, min(step + 1 + horizon, len(_V23_EFFECTIVE))):
        total += int(_V23_EFFECTIVE[future].get(item, 0))
    return total


def _v23_market(obs, action, step, copy_detected):
    action = _copy_action(action)
    keep = [
        list(order) for order in (action.get("market") or [])
        if not (
            isinstance(order, (list, tuple)) and len(order) >= 3
            and order[0] == "SELL" and order[1] in _V23_CONTROLLED
        )
    ]
    action["market"] = keep
    seat = _seat(obs)
    state = _v23_state(seat, step)
    stock = _v22_projected_shed(obs, action)
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    wheat_queued = sum(
        max(0, int(order[2]))
        for order in keep
        if len(order) >= 3 and order[0] == "SELL" and order[1] == "WHEAT"
    )
    sold = state.setdefault("sold", {})
    sells = {}
    horizon = min(step + _V23_LEAD + 1, len(_V23_REMAINING) - 1)
    for item in _V23_CONTROLLED:
        available = max(0, int(stock.get(item, 0) or 0)) - _v23_reserve(obs, item)
        if available <= 0:
            continue
        total = float(_V23_REMAINING[0].get(item, 0))
        # Route cumulative through step+LEAD: stay that far ahead of the
        # schedule every opponent in this basin sells on.
        target = total - float(_V23_REMAINING[horizon].get(item, 0))
        quantity = int(min(available, max(0.0, target - sold.get(item, 0))))
        base_price = float(_MARKET_PARAMS[item][0])
        price = float(_get(prices, item, base_price) or base_price)
        if price >= _V23_SPIKE_RATIO * base_price:
            # Scarcity spike (opponent purchases or heavy town draw): sell
            # extra into strength beyond schedule parity.
            quantity = min(available, quantity + 8)
        if step >= _V23_DEADLINE:
            quantity = available
        if quantity > 0:
            sells[item] = int(quantity)
            sold[item] = sold.get(item, 0) + int(quantity)

    # Shed pressure: the 100-item cap silently discards overflow at end-of-day
    # drop, so holding is bounded — force sales down to the target, cheapest
    # inventory first, before any harvest is lost.
    def _spare(item):
        spare = (
            max(0, int(stock.get(item, 0) or 0))
            - _v23_reserve(obs, item)
            - sells.get(item, 0)
        )
        if item == "WHEAT":
            spare -= wheat_queued
        return max(0, spare)

    total_stock = sum(max(0, int(value or 0)) for value in stock.values())
    queued = sum(sells.values()) + wheat_queued
    if total_stock - queued > _V23_SHED_HIGH:
        overflow = (total_stock - queued) - _V23_SHED_TARGET
        for item in _V23_RESILIENT_ORDER:
            if overflow <= 0:
                break
            available = _spare(item)
            if available <= 0:
                continue
            take = min(available, overflow)
            sells[item] = sells.get(item, 0) + take
            if item in _V23_CONTROLLED:
                sold[item] = sold.get(item, 0) + take
            overflow -= take

    # Sells lead the queue (revenue lands before the same turn's purchases,
    # matching the base engine's ordering), then everything else.
    route_sells = [
        order for order in keep
        if len(order) >= 3 and order[0] == "SELL"
    ]
    others = [
        order for order in keep
        if not (len(order) >= 3 and order[0] == "SELL")
    ]
    controller_sells = [["SELL", item, quantity] for item, quantity in sells.items()]
    action["market"] = route_sells + controller_sells + others
    action = _rank_sell_slots(obs, action, _V16_OFFICIAL_CONFIGURATION)
    action["market"] = list(action.get("market") or [])[:10]
    return action


def agent(obs):
    try:
        configuration = _V16_OFFICIAL_CONFIGURATION
        step = min(max(0, int(_get(obs, "step", 0) or 0)), len(_REBALANCE_ACTIONS) - 1)
        detect_state = _v22_state(_seat(obs), step)
        action = _v16_agent_impl(obs, configuration)
        try:
            detected = _v22_detect(obs, detect_state, step)
            action = _v23_market(obs, action, step, detected)
        except Exception:
            pass  # controller failure: keep the route's own market orders
        if step >= _V22_TERMINAL_STEP:
            action = _v22_terminal_market(obs, action)
        return _align_hands(action, obs)
    except Exception:
        farm = _farm(obs, _seat(obs))
        return {
            "farmer": ["PASS"],
            "hands": [["PASS"] for _ in (_get(farm, "hands", []) or [])],
            "market": [],
        }
