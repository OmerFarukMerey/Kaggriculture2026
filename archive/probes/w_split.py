"""Experiment a: widen the debt-accounted split to wheat+fertilizer.
Wrapper over v24_agent.py; does not modify the base file.
"""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "w_split_core", Path(__file__).parent / "v24_agent.py"
)
_core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_core)

_core._C94_SPLIT_ITEMS = ("FERTILIZER", "WHEAT")
_core._C94_SPLIT_CAPS = {"FERTILIZER": 10, "WHEAT": 10}


def agent(obs, config=None):
    return _core.agent(obs, config)
