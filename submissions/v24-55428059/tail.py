# ---------------------------------------------------------------------------
# v24 layer on the C94 base.
#
# 1. Clone escalation: the base front-runs a detected mirror by one turn.  A
#    C94 copy does the same, which ties the exchange.  At high clone
#    confidence we extend our horizon to two turns, landing one step before
#    the copy's own front-run.
# 2. Boatlee-family layer: detect opponents replaying the public Boatlee V16
#    route (signature tracks from self-play) and sell our stock of a premium
#    line just before their scheduled batches, their adaptive 713 wool dump,
#    and their staged 713-718 terminal liquidation.
# ---------------------------------------------------------------------------
_V24_CLONE_ESCALATE_AT = 4   # confidence (max 8) needed for horizon 2
_V24_BOAT_TRACKS = json.loads(zlib.decompress(base64.b85decode(
    "__TRACKS_B85__"
)).decode("utf-8"))
_V24_BOAT_ACTIONS = json.loads(zlib.decompress(base64.b85decode(
    (
__BOAT_ROUTE_B85__
    )
)).decode("utf-8"))
_V24_C94_TRACK = json.loads(zlib.decompress(base64.b85decode(
    "__C94_TRACK_B85__"
)).decode("utf-8"))
_V24_BOAT_THRESHOLD = 4.0   # true copies measure <=3.3; nearest non-copies >=7.3
# The public meta's opening is fully converged: rival routes are identical to
# ours until ~step 240, so family detection only counts from there and only
# acts once the builds have demonstrably separated.
_V24_WARMUP_STEP = 240
_V24_MIN_STEP = 360
_V24_MIN_RATIO = 0.9
_V24_MAX_ACTORS = 13
_V24_CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
_V24_ANIMALS = ("COW", "SHEEP", "GOOSE")
_V24_KINDS = ("PASTURE", "COOP")
_V24_QUADRANTS = ("NW", "NE", "SW", "SE")
_V24_PREMIUM = ("MELON", "STRAWBERRY", "MILK", "WOOL", "FERTILIZER")
_V24_STATE = {"last_step": -1, "hits": 0, "total": 0, "yarn": None}
_V24_C94_STATE = {"last_step": -1, "hits": 0, "total": 0}

# Boatlee's scheduled sells per step, with its RC2 relay shift applied
# (a locked copy sells hour-17 fertilizer batches three steps early).
_V24_BOAT_SELLS = []
for _v24_entry in _V24_BOAT_ACTIONS:
    _v24_bucket = {}
    for _v24_order in (_v24_entry.get("market") or []):
        if (
            isinstance(_v24_order, list) and len(_v24_order) >= 3
            and _v24_order[0] == "SELL"
        ):
            try:
                _v24_bucket[_v24_order[1]] = (
                    _v24_bucket.get(_v24_order[1], 0) + max(0, int(_v24_order[2]))
                )
            except (TypeError, ValueError):
                pass
    _V24_BOAT_SELLS.append(_v24_bucket)
for _v24_s in range(len(_V24_BOAT_SELLS)):
    if _v24_s % 24 == 17 and 281 <= _v24_s <= 665:
        _v24_q = _V24_BOAT_SELLS[_v24_s].pop("FERTILIZER", 0)
        if _v24_q and _v24_s >= 3:
            _V24_BOAT_SELLS[_v24_s - 3]["FERTILIZER"] = (
                _V24_BOAT_SELLS[_v24_s - 3].get("FERTILIZER", 0) + _v24_q
            )


def _v24_position(value):
    try:
        return (int(value[0]), int(value[1]))
    except (IndexError, TypeError, ValueError):
        return (-1, -1)


def _v24_signature(farm):
    hands = list(farm.get("hands", []) or [])
    unlocks = set(farm.get("unlocked_quadrants", []) or [])
    positions = [_v24_position(farm.get("farmer", (-1, -1)))]
    positions.extend(_v24_position(item) for item in hands)
    positions = (positions + [(-1, -1)] * _V24_MAX_ACTORS)[:_V24_MAX_ACTORS]
    counts = {key: 0 for key in (*_V24_CROPS, *_V24_ANIMALS, *_V24_KINDS, "WEED")}
    yields = {key: 0 for key in (*_V24_CROPS, *_V24_ANIMALS)}
    for row in (farm.get("tiles", []) or []):
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
            if kind in _V24_KINDS:
                counts[kind] += 1
            if kind == "WEED":
                counts["WEED"] += 1
    return {
        "workers": len(hands),
        "unlocks": sum(1 << i for i, name in enumerate(_V24_QUADRANTS) if name in unlocks),
        "positions": [coordinate for point in positions for coordinate in point],
        "counts": [counts[key] for key in (*_V24_CROPS, *_V24_ANIMALS, *_V24_KINDS, "WEED")],
        "yields": [yields[key] for key in (*_V24_CROPS, *_V24_ANIMALS)],
    }


def _v24_distance(left, right):
    total = 12.0 * abs(int(left["workers"]) - int(right["workers"]))
    total += 7.0 * (int(left["unlocks"]) ^ int(right["unlocks"])).bit_count()
    for actor in range(_V24_MAX_ACTORS):
        offset = 2 * actor
        left_point = left["positions"][offset:offset + 2]
        right_point = right["positions"][offset:offset + 2]
        if left_point == [-1, -1] and right_point == [-1, -1]:
            continue
        weight = 0.8 if actor == 0 else 0.25
        total += weight * sum(abs(a - b) for a, b in zip(left_point, right_point))
    counts_left = left["counts"]
    counts_right = right["counts"]
    for index, (a, b) in enumerate(zip(counts_left, counts_right)):
        total += (0.25 if index == len(counts_left) - 1 else 3.0) * abs(a - b)
    total += 0.15 * sum(abs(a - b) for a, b in zip(left["yields"], right["yields"]))
    return total


def _v24_boat_track(obs, step):
    state = _V24_STATE
    if state.get("yarn") is None and step >= 168:
        shops = tuple((obs.get("town") or {}).get("unlocked_shops") or ())
        state["yarn"] = (
            "YARN_STORE" in shops
            and not any(shop in ("SMOOTHIE_SHOP", "PIZZA_SHOP") for shop in shops)
        )
    yarn = bool(state.get("yarn"))
    track = _V24_BOAT_TRACKS["yarn_on" if yarn else "yarn_off"] or _V24_BOAT_TRACKS["yarn_off"]
    return track[step] if track and step < len(track) else None


def _v24_boat_detected(obs, step):
    state = _V24_STATE
    if step == 0 or step < state.get("last_step", -1):
        state.update({"last_step": step, "hits": 0, "total": 0, "yarn": None})
    state["last_step"] = step
    farms = obs.get("farms", []) or []
    if len(farms) < 2:
        return False
    expected = _v24_boat_track(obs, step)
    if expected is None:
        return False
    player = int(obs.get("player", 0) or 0)
    distance = _v24_distance(_v24_signature(farms[1 - player]), expected)
    if step >= _V24_WARMUP_STEP:
        state["total"] += 1
        if distance <= _V24_BOAT_THRESHOLD:
            state["hits"] += 1
    return (
        step >= _V24_MIN_STEP
        and distance <= _V24_BOAT_THRESHOLD
        and state["total"] > 0
        and state["hits"] / state["total"] >= _V24_MIN_RATIO
    )


def _v24_c94_copy_detected(obs, step):
    """Exact-family check: is the opponent replaying our own C94 route?"""
    state = _V24_C94_STATE
    if step == 0 or step < state.get("last_step", -1):
        state.update({"last_step": step, "hits": 0, "total": 0})
    state["last_step"] = step
    farms = obs.get("farms", []) or []
    if len(farms) < 2 or step >= len(_V24_C94_TRACK):
        return False
    player = int(obs.get("player", 0) or 0)
    distance = _v24_distance(
        _v24_signature(farms[1 - player]), _V24_C94_TRACK[step]
    )
    if step >= _V24_WARMUP_STEP:
        state["total"] += 1
        if distance <= _V24_BOAT_THRESHOLD:
            state["hits"] += 1
    return (
        step >= _V24_MIN_STEP
        and distance <= _V24_BOAT_THRESHOLD
        and state["total"] > 0
        and state["hits"] / state["total"] >= _V24_MIN_RATIO
    )


def _v24_boat_frontrun(action, obs, step):
    """Sell our stock of a premium line just before a Boatlee copy's batch."""
    orders = list(action.get("market", []) or [])
    if len(orders) >= 10:
        return
    already = {}
    for order in orders:
        if isinstance(order, list) and len(order) >= 3 and order[0] == "SELL":
            already[order[1]] = already.get(order[1], 0) + max(0, int(order[2] or 0))
    shed = (obs.get("private") or {}).get("shed") or {}
    upcoming = {}
    for future in range(step + 1, min(step + 3, len(_V24_BOAT_SELLS))):
        for item, quantity in _V24_BOAT_SELLS[future].items():
            if item in _V24_PREMIUM:
                upcoming[item] = upcoming.get(item, 0) + quantity
    if step in (711, 712):
        # Their wool controller dumps everything at 713 and staged terminal
        # batches follow: flush our premium stock ahead of it.
        for item in _V24_PREMIUM:
            upcoming[item] = max(upcoming.get(item, 0), 999)
    for item, quantity in sorted(
        upcoming.items(),
        key=lambda pair: -_GLUT_WEIGHT.get(pair[0], 1.0) * _BASE_PRICE.get(pair[0], 100),
    ):
        if len(orders) >= 10:
            break
        if quantity < 3 and quantity < 999:
            continue
        available = max(0, int(shed.get(item, 0) or 0) - already.get(item, 0))
        take = min(available, max(quantity, 4))
        if take <= 0:
            continue
        orders.append(["SELL", item, take])
    action["market"] = orders[:10]


_v24_host_agent = agent


def agent(obs, config=None):
    global _C94_SPLIT_HORIZON
    try:
        step = int(obs.get("step", 0) or 0)
    except (TypeError, ValueError):
        step = 0
    try:
        # The base's operative front-run is the debt-accounted fertilizer
        # split at horizon 1.  A C94 copy runs the same split, tying the
        # exchange; against a track-confirmed copy of our exact route we
        # deepen the horizon to 2 and land one step before the copy's own
        # split.  Near-mirrors that are NOT our route (Kaito, Boatlee) keep
        # horizon 1 — advancing two turns against them measurably loses.
        _C94_SPLIT_HORIZON = (
            2 if (
                _CLONE_CONFIDENCE >= _V24_CLONE_ESCALATE_AT
                and _v24_c94_copy_detected(obs, step)
            ) else 1
        )
    except Exception:
        _C94_SPLIT_HORIZON = 1
    action = _v24_host_agent(obs, config)
    try:
        if _v24_boat_detected(obs, step):
            _v24_boat_frontrun(action, obs, step)
    except Exception:
        pass
    return action
