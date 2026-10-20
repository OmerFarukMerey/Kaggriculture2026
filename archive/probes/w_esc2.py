"""Experiment b: fire clone escalation earlier (confidence 2 instead of 4).
Wrapper over v24_agent.py; does not modify the base file.
"""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "w_esc2_core", Path(__file__).parent / "v24_agent.py"
)
_core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_core)

_core._V24_CLONE_ESCALATE_AT = 2


def agent(obs, config=None):
    return _core.agent(obs, config)
