# ---------------------------------------------------------------------------
# v25 layer: yarn-adaptive livestock swap on the C94 chassis.
#
# Every one of v24's live losses happened on YARN_STORE shop draws (often
# doubled/tripled under with-replacement unlocks), where wool-heavy builds
# out-earn C94's cow-heavy mix.  Boatlee's validated fix on its own route is
# a COW->SHEEP swap at its purchase step; we apply the same surgery to the
# C94 trace: on a yarn-favorable draw (latched at step 161, Boatlee's rule)
# the post-161 cow purchases, pickups and placements become sheep.  Tiles,
# labor, and feeding are unchanged — pastures and wheat serve both species —
# and the sell planner already works off the actual shed.
# ---------------------------------------------------------------------------
_V25_SWAP_BUY_STEPS = (161, 168, 192)
_V25_SWAP_WINDOW = (161, 212)
_V25_STATE = {
    0: {"yarn": None, "last_step": -1},
    1: {"yarn": None, "last_step": -1},
}


def _v25_yarn(obs, step, seat):
    state = _V25_STATE[seat]
    if step == 0 or step < state["last_step"]:
        state["yarn"] = None
    state["last_step"] = step
    if state["yarn"] is None and step >= 161:
        shops = tuple((obs.get("town") or {}).get("unlocked_shops") or ())
        state["yarn"] = (
            "YARN_STORE" in shops
            and not any(shop in ("SMOOTHIE_SHOP", "PIZZA_SHOP") for shop in shops)
        )
    return bool(state["yarn"])


def _v25_swap_unit(unit_action, step):
    if (
        isinstance(unit_action, list)
        and len(unit_action) >= 2
        and unit_action[0] in ("PLACE", "PICKUP")
        and unit_action[1] == "COW"
        and _V25_SWAP_WINDOW[0] <= step <= _V25_SWAP_WINDOW[1]
    ):
        unit_action = list(unit_action)
        unit_action[1] = "SHEEP"
    return unit_action


def _v25_livestock_swap(action, step):
    action = dict(action)
    if step in _V25_SWAP_BUY_STEPS:
        market = []
        for order in (action.get("market") or []):
            order = list(order)
            if len(order) >= 2 and order[0] == "BUY_ANIMAL" and order[1] == "COW":
                order[1] = "SHEEP"
            market.append(order)
        action["market"] = market
    action["farmer"] = _v25_swap_unit(action.get("farmer") or ["PASS"], step)
    action["hands"] = [
        _v25_swap_unit(hand, step) for hand in (action.get("hands") or [])
    ]
    return action


_v25_host_agent = agent


def agent(obs, config=None):
    action = _v25_host_agent(obs, config)
    try:
        step = int(obs.get("step", 0) or 0)
        seat = 1 if int(obs.get("player", 0) or 0) == 1 else 0
        if _v25_yarn(obs, step, seat) and step <= _V25_SWAP_WINDOW[1] + 24:
            action = _v25_livestock_swap(action, step)
    except Exception:
        pass
    return action
