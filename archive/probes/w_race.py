"""Experiment c: race-aware sell slot ordering (_RACE_WEIGHT=1.0).
Only reorders our own already-planned sells within a turn; quantities and
steps unchanged (conservation-safe). Wrapper over v24_agent.py.
"""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "w_race_core", Path(__file__).parent / "v24_agent.py"
)
_core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_core)

_core._RACE_WEIGHT = 1.0


def agent(obs, config=None):
    return _core.agent(obs, config)
