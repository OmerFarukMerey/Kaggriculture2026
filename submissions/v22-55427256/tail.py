# ---------------------------------------------------------------------------
# v22 layer: Boatlee-copy detection and systematic front-running, plus a
# step-717 terminal liquidation.  The base production engine above is the
# public Boatlee V16-RC2 artifact; this layer targets the copies of it (and
# its near-mirrors) that populate the ladder.
# ---------------------------------------------------------------------------
_V22_TRACKS = json.loads(zlib.decompress(base64.b85decode(
    "__TRACKS_B85__"
)).decode("utf-8"))
_V22_CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
_V22_ANIMALS = ("COW", "SHEEP", "GOOSE")
_V22_KINDS = ("PASTURE", "COOP")
_V22_QUADRANTS = ("NW", "NE", "SW", "SE")
_V22_MAX_ACTORS = 13
_V22_THRESHOLD = __V22_THRESHOLD__
_V22_WARMUP_STEP = 48
_V22_MIN_STEP = 96
_V22_MIN_RATIO = 0.9
_V22_TERMINAL_STEP = 717
_V22_SELLABLE = (
    "STRAWBERRY", "MELON", "MILK", "WOOL", "EGG",
    "TOMATO", "CARROT", "WHEAT", "FERTILIZER",
)
_V22_PRODUCT_BY_ANIMAL = {"COW": "MILK", "SHEEP": "WOOL", "GOOSE": "EGG"}
_V22_GLUT_WEIGHT = {
    "STRAWBERRY": 2.0, "MELON": 3.6, "MILK": 2.0, "WOOL": 3.2,
    "EGG": 1.5, "TOMATO": 1.3, "CARROT": 1.0, "WHEAT": 1.0,
    "FERTILIZER": 1.0,
}
_V22_STATE = {0: {}, 1: {}}


def _v22_position(value):
    try:
        return (int(value[0]), int(value[1]))
    except (IndexError, TypeError, ValueError):
        return (-1, -1)


def _v22_signature(farm):
    hands = list(_get(farm, "hands", []) or [])
    unlocks = set(_get(farm, "unlocked_quadrants", []) or [])
    positions = [_v22_position(_get(farm, "farmer", (-1, -1)))]
    positions.extend(_v22_position(item) for item in hands)
    positions = (positions + [(-1, -1)] * _V22_MAX_ACTORS)[:_V22_MAX_ACTORS]
    counts = {key: 0 for key in (*_V22_CROPS, *_V22_ANIMALS, *_V22_KINDS, "WEED")}
    yields = {key: 0 for key in (*_V22_CROPS, *_V22_ANIMALS)}
    for row in (_get(farm, "tiles", []) or []):
        for tile in row if isinstance(row, list) else [row]:
            if not isinstance(tile, dict):
                continue
            crop = str(tile.get("crop", "")).upper()
            animal = str(tile.get("animal", "")).upper()
            kind = str(tile.get("kind", "")).upper()
            if crop in counts:
                counts[crop] += 1
                yields[crop] += max(0, int(tile.get("yield_units", 0) or 0))
            if animal in counts:
                counts[animal] += 1
                yields[animal] += max(0, int(tile.get("yield_units", 0) or 0))
            if kind in _V22_KINDS:
                counts[kind] += 1
            if kind == "WEED":
                counts["WEED"] += 1
    return {
        "workers": len(hands),
        "unlocks": sum(1 << i for i, name in enumerate(_V22_QUADRANTS) if name in unlocks),
        "positions": [coordinate for point in positions for coordinate in point],
        "counts": [counts[key] for key in (*_V22_CROPS, *_V22_ANIMALS, *_V22_KINDS, "WEED")],
        "yields": [yields[key] for key in (*_V22_CROPS, *_V22_ANIMALS)],
    }


def _v22_distance(left, right):
    total = 12.0 * abs(int(left["workers"]) - int(right["workers"]))
    total += 7.0 * (int(left["unlocks"]) ^ int(right["unlocks"])).bit_count()
    left_positions = list(left["positions"])
    right_positions = list(right["positions"])
    for actor in range(_V22_MAX_ACTORS):
        offset = 2 * actor
        left_point = left_positions[offset:offset + 2]
        right_point = right_positions[offset:offset + 2]
        if left_point == [-1, -1] and right_point == [-1, -1]:
            continue
        weight = 0.8 if actor == 0 else 0.25
        total += weight * sum(abs(a - b) for a, b in zip(left_point, right_point))
    left_counts = list(left["counts"])
    right_counts = list(right["counts"])
    for index, (a, b) in enumerate(zip(left_counts, right_counts)):
        total += (0.25 if index == len(left_counts) - 1 else 3.0) * abs(a - b)
    total += 0.15 * sum(abs(a - b) for a, b in zip(left["yields"], right["yields"]))
    return total


def _v22_state(seat, step):
    state = _V22_STATE[seat]
    if step == 0 or step < state.get("last_step", -1):
        state.clear()
    state.setdefault("hits", 0)
    state.setdefault("total", 0)
    state.setdefault("early", {})
    state["last_step"] = step
    return state


def _v22_track(seat, step):
    yarn = bool(_V16_ROUTE_STATE[seat].get("yarn"))
    track = _V22_TRACKS["yarn_on" if yarn else "yarn_off"] or _V22_TRACKS["yarn_off"]
    return track[step] if track and step < len(track) else None


def _v22_detect(obs, state, step):
    farms = list(_get(obs, "farms", []) or [])
    if len(farms) < 2:
        return False
    expected = _v22_track(_seat(obs), step)
    if expected is None:
        return False
    opponent = farms[1 - _seat(obs)]
    distance = _v22_distance(_v22_signature(opponent), expected)
    if step >= _V22_WARMUP_STEP:
        state["total"] += 1
        if distance <= _V22_THRESHOLD:
            state["hits"] += 1
    return (
        step >= _V22_MIN_STEP
        and distance <= _V22_THRESHOLD
        and state["total"] > 0
        and state["hits"] / state["total"] >= _V22_MIN_RATIO
    )


def _v22_consume_early(action, state, step):
    """Remove quantities already sold early from this step's sells so the
    per-product totals stay equal to the base engine's plan."""
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


def _v22_shed_access(size):
    half = size // 2
    return {
        (half - 1, half - 1), (half, half - 1),
        (half - 1, half), (half, half),
    }


def _v22_projected_shed(obs, action):
    seat = _seat(obs)
    farm = _farm(obs, seat)
    private = _get(obs, "private", {}) or {}
    projected = {
        key: max(0, int(value or 0))
        for key, value in dict(_get(private, "shed", {}) or {}).items()
    }
    inventories = list(_get(private, "inventories", []) or [])
    positions = [_get(farm, "farmer", [0, 0]), *list(_get(farm, "hands", []) or [])]
    actions = [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]
    tiles = list(_get(farm, "tiles", []) or [])
    access = _v22_shed_access(len(tiles) or 10)
    for index, unit_action in enumerate(actions):
        if index >= len(positions) or index >= len(inventories):
            continue
        position = positions[index]
        if not isinstance(position, (list, tuple)) or len(position) < 2:
            continue
        x, y = int(position[0]), int(position[1])
        if (x, y) not in access or not (0 <= y < len(tiles) and 0 <= x < len(tiles[y])):
            continue
        if tiles[y][x] == "LOCKED" or not isinstance(unit_action, list) or not unit_action:
            continue
        inventory = {
            key: max(0, int(value or 0))
            for key, value in dict(inventories[index] or {}).items()
        }
        if unit_action[0] == "DROP":
            deposits = inventory.items()
        elif unit_action[0] == "PLACE" and len(unit_action) >= 2:
            item = unit_action[1]
            tile = tiles[y][x]
            structure = {"COW": "PASTURE", "SHEEP": "PASTURE", "GOOSE": "COOP"}.get(item)
            if (
                structure is not None and isinstance(tile, dict)
                and tile.get("kind") == structure and "animal" not in tile
            ):
                continue
            try:
                requested = int(unit_action[2]) if len(unit_action) >= 3 else 1
            except (TypeError, ValueError):
                continue
            deposits = ((item, min(max(0, requested), inventory.get(item, 0))),)
        else:
            continue
        for item, quantity in deposits:
            room = max(0, 100 - sum(projected.values()))
            amount = min(max(0, int(quantity or 0)), room)
            if amount:
                projected[item] = projected.get(item, 0) + amount
    return projected


def _v22_remaining_after(obs, action):
    remaining = _v22_projected_shed(obs, action)
    for order in (action.get("market") or []):
        if len(order) >= 3 and order[0] == "SELL":
            try:
                quantity = max(0, int(order[2]))
            except (TypeError, ValueError):
                quantity = 0
            remaining[order[1]] = max(0, int(remaining.get(order[1], 0) or 0) - quantity)
    return remaining


def _v22_relay_covered(step):
    """True when the base engine's RC2 relay would move this route step's
    FERTILIZER sale three steps earlier (so a copy sells it at step-3)."""
    return step % 24 == 17 and 281 <= step <= 665


_V22_SENSITIVE = ("MILK", "STRAWBERRY", "MELON", "WOOL")
_V22_QUIET_HORIZON = 4
_V22_PREDUMP_STEP = 712
_V22_ROUTE_SELLS = []
for _v22_step_action in _LEGACY_ACTIONS:
    _v22_bucket = {}
    for _v22_order in (_v22_step_action.get("market") or []):
        if isinstance(_v22_order, (list, tuple)) and len(_v22_order) >= 3 and _v22_order[0] == "SELL":
            try:
                _v22_bucket[_v22_order[1]] = _v22_bucket.get(_v22_order[1], 0) + max(0, int(_v22_order[2]))
            except (TypeError, ValueError):
                pass
    _V22_ROUTE_SELLS.append(_v22_bucket)


def _v22_frontrun(obs, action, state, step):
    """Against a detected copy: fertilizer four steps ahead (beating its
    3-step relay by one), everything else one step ahead, wool the step
    before its 713 terminal wool dump.  All route quantities are debt-
    accounted; adaptive wool needs no debt (the base controller self-clamps
    on the emptied shed)."""
    action = _copy_action(action)
    market = [list(order) for order in (action.get("market") or [])]
    remaining = _v22_remaining_after(obs, action)
    moved = {}

    def queue(item, requested, debt_step):
        if len(market) >= 10 or requested <= 0:
            return
        quantity = min(requested, max(0, int(remaining.get(item, 0) or 0)))
        if quantity <= 0:
            return
        remaining[item] = max(0, int(remaining.get(item, 0) or 0) - quantity)
        market.append(["SELL", item, quantity])
        if debt_step is not None:
            bucket = moved.setdefault(debt_step, {})
            bucket[item] = bucket.get(item, 0) + quantity

    # Endgame: dump the whole shed at 712, one step before the copy's staged
    # 713-718 liquidation (and its wool controller's 713 full dump).  Later
    # route sells then no-op on the emptied shed; the 717/718 terminal pass
    # catches anything harvested afterwards.
    if step == _V22_PREDUMP_STEP:
        prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
        order_by_value = sorted(
            _V22_SELLABLE,
            key=lambda item: -_V22_GLUT_WEIGHT.get(item, 1.0)
            * max(1.0, float(prices.get(item, 1) or 1)),
        )
        for item in order_by_value:
            queue(item, int(remaining.get(item, 0) or 0), None)
        action["market"] = market[:10]
        return action

    # Lead-4 fertilizer: beat the copy's own 3-step relay.
    future = step + 4
    if _v22_relay_covered(future) and future < len(_LEGACY_ACTIONS):
        queue("FERTILIZER", int(_V22_ROUTE_SELLS[future].get("FERTILIZER", 0)), future)

    # Glut-sensitive products: sell only into turns where the copy is quiet on
    # that product, pre-empting its next scheduled batch within the horizon.
    # Solo turns capture the top of the price curve; the copy's batch then
    # lands on the crashed price.
    for item in _V22_SENSITIVE:
        if _V22_ROUTE_SELLS[step].get(item):
            continue  # the copy sells this product this turn: not a quiet turn
        for future in range(step + 1, min(step + 1 + _V22_QUIET_HORIZON, len(_LEGACY_ACTIONS))):
            target = int(_V22_ROUTE_SELLS[future].get(item, 0))
            if target > 0:
                already = int(state["early"].get(future, {}).get(item, 0) or 0)
                if target > already:
                    queue(item, target - already, future)
                break

    # Lead-1 for the remaining staples (wheat and friends): small but free.
    upcoming = step + 1
    if upcoming < len(_LEGACY_ACTIONS):
        for item, requested in _V22_ROUTE_SELLS[upcoming].items():
            if item in _V22_SENSITIVE:
                continue
            if item == "FERTILIZER" and _v22_relay_covered(upcoming):
                continue
            queue(item, int(requested), upcoming)

    for debt_step, bucket in moved.items():
        merged = state["early"].setdefault(debt_step, {})
        for item, quantity in bucket.items():
            merged[item] = merged.get(item, 0) + quantity
    action["market"] = market[:10]
    return action


def _v22_opponent_exposure(obs):
    seat = _seat(obs)
    farms = list(_get(obs, "farms", []) or [])
    opponent = farms[1 - seat] if len(farms) >= 2 else {}
    exposure = {item: 0.0 for item in _V22_SELLABLE}
    for row in (_get(opponent, "tiles", []) or []):
        for tile in row if isinstance(row, list) else [row]:
            if not isinstance(tile, dict):
                continue
            crop = str(tile.get("crop", "")).upper()
            if crop in exposure:
                exposure[crop] += max(1.0, float(tile.get("yield_units", 0) or 0))
            product = _V22_PRODUCT_BY_ANIMAL.get(str(tile.get("animal", "")).upper())
            if product:
                exposure[product] += 1.0 + max(0.0, float(tile.get("yield_units", 0) or 0))
            if tile.get("fertilizer_available", False):
                exposure["FERTILIZER"] += 1.0
    return exposure


def _v22_terminal_market(obs, action):
    action = _align_hands(action, obs)
    shed = _v22_projected_shed(obs, action)
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    exposure = _v22_opponent_exposure(obs)
    rows = []
    for index, item in enumerate(_V22_SELLABLE):
        quantity = max(0, int(shed.get(item, 0) or 0))
        if quantity <= 0:
            continue
        score = (
            (1.0 + exposure.get(item, 0.0))
            * _V22_GLUT_WEIGHT.get(item, 1.0)
            * max(1.0, float(prices.get(item, 1) or 1))
            * math.log1p(quantity)
        )
        rows.append((score, -index, item, quantity))
    rows.sort(reverse=True)
    action["market"] = [
        ["SELL", item, quantity] for _score, _index, item, quantity in rows[:10]
    ]
    return action


def agent(obs):
    try:
        configuration = _V16_OFFICIAL_CONFIGURATION
        step = min(max(0, int(_get(obs, "step", 0) or 0)), len(_REBALANCE_ACTIONS) - 1)
        state = _v22_state(_seat(obs), step)
        action = _v16_agent_impl(obs, configuration)
        action = _v22_consume_early(action, state, step)
        if _v22_detect(obs, state, step):
            action = _v22_frontrun(obs, action, state, step)
        else:
            action = _rc2_market_relay(obs, action, step, configuration)
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
