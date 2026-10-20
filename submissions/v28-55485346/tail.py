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
# Late conversion (289/433 cows and their 514/519 placements) fires only when
# a SECOND yarn store is visible at step 288+ (with-replacement unlocks can
# double it) and still no smoothie/pizza: double-yarn wool demand is the one
# regime where trading the late milk line is measured-safe.
_V25_LATE_BUY_STEPS = (289, 433)
_V25_LATE_WINDOW = (289, 540)
_V25_STATE = {
    0: {"yarn": None, "yarn2": None, "last_step": -1},
    1: {"yarn": None, "yarn2": None, "last_step": -1},
}


def _v25_yarn(obs, step, seat):
    state = _V25_STATE[seat]
    if step == 0 or step < state["last_step"]:
        state["yarn"] = None
        state["yarn2"] = None
    state["last_step"] = step
    shops = None
    if state["yarn"] is None and step >= 161:
        shops = tuple((obs.get("town") or {}).get("unlocked_shops") or ())
        state["yarn"] = (
            "YARN_STORE" in shops
            and not any(shop in ("SMOOTHIE_SHOP", "PIZZA_SHOP") for shop in shops)
        )
    if state["yarn2"] is None and step >= 288:
        if shops is None:
            shops = tuple((obs.get("town") or {}).get("unlocked_shops") or ())
        state["yarn2"] = (
            bool(state["yarn"])
            and list(shops).count("YARN_STORE") >= 2
            and not any(shop in ("SMOOTHIE_SHOP", "PIZZA_SHOP") for shop in shops)
        )
    return bool(state["yarn"])


def _v25_yarn2(seat):
    return bool(_V25_STATE[seat]["yarn2"])


def _v25_swap_unit(unit_action, step, late):
    in_window = _V25_SWAP_WINDOW[0] <= step <= _V25_SWAP_WINDOW[1] or (
        late and _V25_LATE_WINDOW[0] <= step <= _V25_LATE_WINDOW[1]
    )
    if (
        isinstance(unit_action, list)
        and len(unit_action) >= 2
        and unit_action[0] in ("PLACE", "PICKUP")
        and unit_action[1] == "COW"
        and in_window
    ):
        unit_action = list(unit_action)
        unit_action[1] = "SHEEP"
    return unit_action


def _v25_livestock_swap(action, step, late):
    action = dict(action)
    buy_steps = _V25_SWAP_BUY_STEPS + (_V25_LATE_BUY_STEPS if late else ())
    if step in buy_steps:
        market = []
        for order in (action.get("market") or []):
            order = list(order)
            if len(order) >= 2 and order[0] == "BUY_ANIMAL" and order[1] == "COW":
                order[1] = "SHEEP"
            market.append(order)
        action["market"] = market
    action["farmer"] = _v25_swap_unit(action.get("farmer") or ["PASS"], step, late)
    action["hands"] = [
        _v25_swap_unit(hand, step, late) for hand in (action.get("hands") or [])
    ]
    return action


# Yarn-gate the v24 Boatlee-frontrun: against wool-hoarding Boatlee copies on
# yarn draws the premium pre-dump is worth up to +7k, but on normal draws it
# dumps goods the C94 planner had priced better (measured -2.8k/game).  The
# yarn latch is set on a prior step's outer pass; boat detection cannot fire
# before step 360, long after the latch, so the ordering is safe.
_v25_boat_frontrun_unconditional = _v24_boat_frontrun


def _v24_boat_frontrun(action, obs, step):
    try:
        seat = 1 if int(obs.get("player", 0) or 0) == 1 else 0
    except (TypeError, ValueError, AttributeError):
        seat = 0
    if bool(_V25_STATE[seat].get("yarn")):
        _v25_boat_frontrun_unconditional(action, obs, step)


_v25_host_agent = agent


def agent(obs, config=None):
    action = _v25_host_agent(obs, config)
    try:
        step = int(obs.get("step", 0) or 0)
        seat = 1 if int(obs.get("player", 0) or 0) == 1 else 0
        if _v25_yarn(obs, step, seat):
            late = _v25_yarn2(seat)
            if step <= _V25_SWAP_WINDOW[1] + 24 or (
                late and step <= _V25_LATE_WINDOW[1] + 24
            ):
                action = _v25_livestock_swap(action, step, late)
    except Exception:
        pass
    return action


def kaggriculture_entrypoint(obs, config=None):
    """Submission entrypoint: MUST be the last newly-named callable in this
    file.  Kaggle's loader picks the last callable by namespace insertion
    order, and rebinding an existing name (like `agent`) keeps its original
    position - which silently selected an inner host agent in earlier
    submissions."""
    return agent(obs, config)
