"""Community V1.1: bounded observation-driven worker action retry.

The upstream economic plan, market orders, farm layout, and normal worker route
come unchanged from the frozen Kaito v25 community baseline. This experiment
only retries a FEED/WATER action when the following observation proves that the
action did not execute and the actor is still on the affected tile.
"""

from __future__ import annotations

import copy
import importlib.util
from collections import Counter
from pathlib import Path


try:
    # Kaggle extracts multi-file submissions together and executes main.py
    # without defining __file__. A normal sibling import is the portable path.
    import community_v1_base as _BASE
except ImportError:
    # Local repository layout used by benchmark.py and unit tests.
    _LOCAL_BASE_PATH = (
        Path(__file__).resolve().parents[2]
        / "community"
        / "kaito_v25"
        / "main.py"
    )
    _SPEC = importlib.util.spec_from_file_location(
        "_kaggriculture_community_v1", _LOCAL_BASE_PATH
    )
    _BASE = importlib.util.module_from_spec(_SPEC)
    _SPEC.loader.exec_module(_BASE)

_REPLAY_STEPS = 8
_MOVEMENT_OPS = {"NORTH", "SOUTH", "EAST", "WEST"}
_STATE = {0: {}, 1: {}}
_TELEMETRY = Counter()


def _get(value, key, default=None):
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _copy_action(action):
    action = copy.deepcopy(action or {})
    return {
        "farmer": list(action.get("farmer") or ["PASS"]),
        "hands": [list(order or ["PASS"]) for order in (action.get("hands") or [])],
        "market": [list(order) for order in (action.get("market") or [])],
    }


def _actors(action, expected_hands):
    hands = list(action.get("hands") or [])
    if len(hands) < expected_hands:
        hands.extend([["PASS"] for _ in range(expected_hands - len(hands))])
    return [list(action.get("farmer") or ["PASS"]), *hands[:expected_hands]]


def _tile_at(farm, position):
    try:
        x, y = int(position[0]), int(position[1])
        return (_get(farm, "tiles", []) or [])[y][x]
    except (IndexError, TypeError, ValueError):
        return "LOCKED"


def _retry_action(previous, previous_day, day, previous_position, position, tile, inventory):
    if previous_day != day or previous_position != position or not previous:
        return None
    op = previous[0]
    if (
        op == "FEED"
        and isinstance(tile, dict)
        and tile.get("animal")
        and not tile.get("fed_today", False)
        and int((inventory or {}).get("WHEAT", 0) or 0) > 0
    ):
        return ["FEED"]
    if (
        op == "WATER"
        and isinstance(tile, dict)
        and tile.get("kind") == "PLANT"
        and not tile.get("watered_today", False)
    ):
        return ["WATER"]
    return None


def _repair(obs, configuration, base_action):
    seat = 1 if int(_get(obs, "player", 0) or 0) == 1 else 0
    step = int(_get(obs, "step", 0) or 0)
    day = int(_get(obs, "day", step // 24) or 0)
    farms = list(_get(obs, "farms", []) or [])
    farm = farms[seat] if seat < len(farms) else {}
    positions = [list(_get(farm, "farmer", []) or []), *[
        list(position) for position in (_get(farm, "hands", []) or [])
    ]]
    private = _get(obs, "private", {}) or {}
    inventories = list(_get(private, "inventories", []) or [])
    if len(inventories) < len(positions):
        inventories.extend({} for _ in range(len(positions) - len(inventories)))

    game = _STATE[seat]
    if step == 0 or step <= int(game.get("last_step", -1)) or game.get("day") != day:
        game = {"active": {}, "history": {}}
        _STATE[seat] = game

    actions = _actors(base_action, max(0, len(positions) - 1))
    game["history"][step] = copy.deepcopy(actions)
    active = game["active"]

    # Continue a bounded one-step-delayed replay after inserting a repair.
    for actor, transaction in list(active.items()):
        if actor >= len(actions):
            active.pop(actor, None)
            continue
        age = step - transaction["start"]
        if age == 1:
            actions[actor] = list(transaction["intended"])
        elif 2 <= age <= 1 + _REPLAY_STEPS:
            prior = game["history"].get(step - 1, [])
            actions[actor] = list(prior[actor]) if actor < len(prior) else ["PASS"]
        else:
            active.pop(actor, None)

    previous_actions = game.get("returned", [])
    previous_positions = game.get("positions", [])
    previous_day = game.get("day")
    for actor, (position, inventory) in enumerate(zip(positions, inventories)):
        if actor in active:
            continue
        tile = _tile_at(farm, position)
        previous = previous_actions[actor] if actor < len(previous_actions) else None
        previous_position = (
            previous_positions[actor] if actor < len(previous_positions) else None
        )
        repair = _retry_action(
            previous,
            previous_day,
            day,
            previous_position,
            position,
            tile,
            inventory,
        )
        if repair is None or repair == actions[actor]:
            continue
        # A stationary displaced action does not change the actor's expected
        # route position, so resume the base tape next turn. Movement needs a
        # bounded delayed replay before resynchronizing.
        if actions[actor] and actions[actor][0] in _MOVEMENT_OPS:
            active[actor] = {
                "start": step,
                "intended": list(actions[actor]),
            }
        actions[actor] = repair
        _TELEMETRY[f"retry_{repair[0].lower()}"] += 1

    result = _copy_action(base_action)
    result["farmer"] = actions[0] if actions else ["PASS"]
    result["hands"] = actions[1:]
    game["returned"] = copy.deepcopy(actions)
    game["positions"] = copy.deepcopy(positions)
    game["day"] = day
    game["last_step"] = step
    # Only a short history is needed for bounded replay.
    for old_step in [key for key in game["history"] if key < step - _REPLAY_STEPS - 2]:
        game["history"].pop(old_step, None)
    return result


def agent(obs, configuration=None):
    base_action = _BASE.agent(obs, configuration)
    return _repair(obs, configuration, base_action)


def get_telemetry():
    return dict(_TELEMETRY)


def _kaggle_submission_entrypoint(obs, configuration=None):
    """Keep the actual agent as the final callable selected by Kaggle."""
    return agent(obs, configuration)
