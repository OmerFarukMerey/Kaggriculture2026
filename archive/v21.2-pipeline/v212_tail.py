# ---------------------------------------------------------------------------
# v21.2 additions: public-copy detection, one-step sell front-running, and a
# step-717 terminal pre-dump.  Ordinary-turn totals per product are preserved:
# every unit sold early is subtracted from the exact route step it came from.
# ---------------------------------------------------------------------------
_BASE_PROTO_INDEX = __BASE_PROTO_INDEX__
_MIRROR_THRESHOLD = __MIRROR_THRESHOLD__
_MIRROR_WARMUP_STEP = 48
_MIRROR_MIN_STEP = 96
_MIRROR_MIN_RATIO = 0.9
_TERMINAL_PREDUMP_STEP = 717
_TERMINAL_STEP = 718
_MIRROR_STATE = {0: {}, 1: {}}


def _mirror_state(seat, step):
    state = _MIRROR_STATE[seat]
    if step == 0 or step < state.get("last_step", -1):
        state.clear()
    state.setdefault("hits", 0)
    state.setdefault("total", 0)
    state.setdefault("early", {})
    state["last_step"] = step
    return state


def _consume_early(action, state, step):
    """Subtract quantities already sold one step early from this step's route
    sells.  Runs on nominal route quantities, before any shed clamping, so the
    per-product season totals stay exactly equal to the route's."""
    owed = state["early"].pop(step, None)
    for stale in [key for key in state["early"] if key <= step]:
        state["early"].pop(stale, None)
    if not owed:
        return action
    market = []
    for order in (action.get("market") or []):
        order = list(order)
        if len(order) >= 3 and order[0] == "SELL" and order[1] in owed:
            try:
                quantity = max(0, int(order[2]))
            except (TypeError, ValueError):
                quantity = 0
            used = min(int(owed.get(order[1], 0) or 0), quantity)
            owed[order[1]] = int(owed.get(order[1], 0) or 0) - used
            if quantity - used <= 0:
                continue
            order[2] = quantity - used
        market.append(order)
    action["market"] = market
    return action


def _mirror_detect(obs, state, step):
    """True when the opponent's public farm has been tracking the deployed
    route's own signature closely enough, for long enough, that they are
    almost certainly replaying the same public artifact."""
    if _BASE_PROTO_INDEX is None:
        return False
    farms = list(_get(obs, "farms", []) or [])
    if len(farms) < 2:
        return False
    signatures = _PROTOTYPES[_BASE_PROTO_INDEX].get("signatures", [])
    if step >= len(signatures):
        return False
    opponent = farms[1 - _seat(obs)]
    distance = _signature_distance(_public_route_signature(opponent), signatures[step])
    if step >= _MIRROR_WARMUP_STEP:
        state["total"] += 1
        if distance <= _MIRROR_THRESHOLD:
            state["hits"] += 1
    return (
        step >= _MIRROR_MIN_STEP
        and distance <= _MIRROR_THRESHOLD
        and state["total"] > 0
        and state["hits"] / state["total"] >= _MIRROR_MIN_RATIO
    )


def _mirror_frontrun(obs, action, state, step):
    """Against a detected copy, place the route's next-step SELLs now, one step
    before the copy sells the same products.  Only quantities that fit the
    projected shed and the order cap are moved; the moved amount is recorded so
    _consume_early removes it from the next step."""
    if step + 1 >= len(_ACTIONS) or step + 1 >= _TERMINAL_PREDUMP_STEP:
        return action
    upcoming = [
        order for order in (_ACTIONS[step + 1].get("market") or [])
        if len(order) >= 3 and order[0] == "SELL"
    ]
    if not upcoming:
        return action
    market = [list(order) for order in (action.get("market") or [])]
    remaining = _projected_shed(obs, action)
    for order in market:
        if len(order) >= 3 and order[0] == "SELL":
            try:
                quantity = max(0, int(order[2]))
            except (TypeError, ValueError):
                quantity = 0
            remaining[order[1]] = max(0, int(remaining.get(order[1], 0) or 0) - quantity)
    moved = {}
    for order in upcoming:
        if len(market) >= 10:
            break
        item = order[1]
        try:
            requested = max(0, int(order[2]))
        except (TypeError, ValueError):
            continue
        quantity = min(requested, max(0, int(remaining.get(item, 0) or 0)))
        if quantity <= 0:
            continue
        remaining[item] = max(0, int(remaining.get(item, 0) or 0) - quantity)
        moved[item] = moved.get(item, 0) + quantity
        market.append(["SELL", item, quantity])
    if moved:
        state["early"][step + 1] = moved
        action["market"] = market
    return action


def agent(obs):
    try:
        step = min(max(0, int(_get(obs, "step", 0) or 0)), len(_ACTIONS) - 1)
        state = _mirror_state(_seat(obs), step)
        action = _consume_early(_copy_action(_ACTIONS[step]), state, step)
        action = _weed_repair_action(obs, action, _ACTIONS, step)
        action = _safe_market(obs, action)
        action = _conditional_reorder(obs, action, step)
        if _mirror_detect(obs, state, step):
            action = _mirror_frontrun(obs, action, state, step)
        if step >= _TERMINAL_PREDUMP_STEP:
            action = _terminal_market(obs, action)
        return _align_hands(action, obs)
    except Exception:
        farm = _farm(obs, _seat(obs))
        return {
            "farmer": ["PASS"],
            "hands": [["PASS"] for _ in (_get(farm, "hands", []) or [])],
            "market": [],
        }


def _kaggle_submission_entrypoint(obs):
    return agent(obs)
