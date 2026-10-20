"""v25 Kaggriculture portfolio agent.

Two engines, one dispatcher: the C94 stack (v24) by default, the wool-
exploiting Boatlee stack (v22) on yarn-favorable shop draws.  The two
lineages share a byte-identical farm choreography until ~step 240, so the
branch decision at step 161 (Boatlee's own yarn rule, latched once) hands
off cleanly.  Every one of v24's 12 live losses had YARN_STORE drawn.
"""
import importlib.util
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))


def _load(name):
    try:
        return __import__(name)
    except Exception:
        spec = importlib.util.spec_from_file_location(name, _HERE / f"{name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


_v22 = _load("v22_agent")
_v24 = _load("v24_agent")

_SWITCH_STEP = 161
_STATE = {
    0: {"branch": None, "last_step": -1},
    1: {"branch": None, "last_step": -1},
}


def _yarn_favorable(obs):
    town = obs.get("town", {}) if isinstance(obs, dict) else getattr(obs, "town", {})
    shops = tuple((town or {}).get("unlocked_shops", []) or ())
    return (
        "YARN_STORE" in shops
        and not any(shop in ("SMOOTHIE_SHOP", "PIZZA_SHOP") for shop in shops)
    )


def agent(obs, config=None):
    try:
        step = int(obs.get("step", 0) or 0)
    except (TypeError, ValueError, AttributeError):
        step = 0
    try:
        seat = 1 if int(obs.get("player", 0) or 0) == 1 else 0
    except (TypeError, ValueError, AttributeError):
        seat = 0
    state = _STATE[seat]
    if step == 0 or step < state["last_step"]:
        state["branch"] = None
    state["last_step"] = step
    if state["branch"] is None and step >= _SWITCH_STEP:
        try:
            state["branch"] = "yarn" if _yarn_favorable(obs) else "c94"
        except Exception:
            state["branch"] = "c94"
    if state["branch"] == "yarn":
        return _v22.agent(obs)
    return _v24.agent(obs, config)
