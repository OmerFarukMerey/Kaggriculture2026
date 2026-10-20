"""v25 with the Boatlee-frontrun layer disabled (diagnostic wrapper)."""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("noboat_core", Path(__file__).parent / "main_v25_orig.py")
_core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_core)
_core._v24_boat_frontrun = lambda action, obs, step: None


def agent(obs, config=None):
    return _core.agent(obs, config)
