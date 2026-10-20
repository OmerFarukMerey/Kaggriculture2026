"""X036: frozen low-predicted-milk gate plus confirmed one-turn sale delay."""

from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path


try:
    import community_v1_1_base as _BASE
    import x036_supply_model as _MODEL
except ImportError:
    _HERE = Path(__file__).resolve().parent
    _BASE_PATH = _HERE.parents[0] / "v1_1_action_retry" / "main.py"
    _BASE_SPEC = importlib.util.spec_from_file_location("_x036_v1_1_base", _BASE_PATH)
    _BASE = importlib.util.module_from_spec(_BASE_SPEC)
    _BASE_SPEC.loader.exec_module(_BASE)
    _MODEL_SPEC = importlib.util.spec_from_file_location(
        "_x036_supply_model", _HERE / "x036_supply_model.py"
    )
    _MODEL = importlib.util.module_from_spec(_MODEL_SPEC)
    _MODEL_SPEC.loader.exec_module(_MODEL)


THRESHOLD = 28.86780869330488
DECISION_DAY = 10
ORIGINAL_STEP = 264
DELAY_STEP = 265
VERIFY_STEP = 266
QUANTITY = 3
_STATE = {
    0: {"last_step": -1, "activate": False, "prediction": None, "pending": False, "before_milk": None},
    1: {"last_step": -1, "activate": False, "prediction": None, "pending": False, "before_milk": None},
}
_TELEMETRY = Counter()


def _fresh_state():
    return {"last_step": -1, "activate": False, "prediction": None, "pending": False, "before_milk": None}


def _transform(action, obs):
    result = _BASE._copy_action(action)
    seat = _BASE._seat(obs) if hasattr(_BASE, "_seat") else (1 if int(_BASE._get(obs, "player", 0) or 0) == 1 else 0)
    step = int(_BASE._get(obs, "step", 0) or 0)
    day = int(_BASE._get(obs, "day", step // 24) or 0)
    hour = int(_BASE._get(obs, "hour", step % 24) or 0)
    state = _STATE[seat]
    if step == 0 or step <= int(state.get("last_step", -1)):
        state = _fresh_state()
        _STATE[seat] = state

    farms = list(_BASE._get(obs, "farms", []) or [])
    if day == DECISION_DAY and hour == 0 and state.get("prediction") is None and len(farms) > 1 - seat:
        prediction = float(_MODEL.predict_public_milk(farms[1 - seat]))
        state["prediction"] = prediction
        state["activate"] = prediction <= THRESHOLD
        _TELEMETRY["forecast_evaluated"] += 1
        _TELEMETRY["forecast_activated"] += int(state["activate"])

    private = _BASE._get(obs, "private", {}) or {}
    shed = _BASE._get(private, "shed", {}) or {}
    milk = int(_BASE._get(shed, "MILK", 0) or 0)

    if state.get("activate") and step == ORIGINAL_STEP and milk >= QUANTITY:
        for index, order in enumerate(result["market"]):
            if order == ["SELL", "MILK", QUANTITY]:
                del result["market"][index]
                state["pending"] = True
                _TELEMETRY["original_sale_removed"] += 1
                break

    if (
        state.get("activate") and step == DELAY_STEP and state.get("pending")
        and milk >= QUANTITY and len(result["market"]) < 10
    ):
        result["market"].append(["SELL", "MILK", QUANTITY])
        state["before_milk"] = milk
        state["pending"] = False
        _TELEMETRY["delayed_sale_submitted"] += 1

    if step == VERIFY_STEP and state.get("before_milk") is not None:
        if int(state["before_milk"]) - milk >= QUANTITY:
            _TELEMETRY["delayed_sale_confirmed"] += 1
        else:
            _TELEMETRY["delayed_sale_unconfirmed"] += 1
        state["before_milk"] = None

    state["last_step"] = step
    return result


def agent(obs, configuration=None):
    return _transform(_BASE.agent(obs, configuration), obs)


def get_telemetry():
    result = dict(_TELEMETRY)
    result["predictions"] = [state["prediction"] for state in _STATE.values()]
    return result


def _kaggle_submission_entrypoint(obs, configuration=None):
    return agent(obs, configuration)
