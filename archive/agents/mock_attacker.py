"""Mock of the live loss pattern: C94 fork that front-runs the public C94
trace's premium sells by one step (debt-accounted), like Kaggs/Utkarsh/NatBel.
Built by importing the stock C94 module and overriding its split knobs.
"""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "c94_attacker_core", Path(__file__).parent / "rayk_c94.py"
)
_core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_core)

# Widen the debt-accounted split from fertilizer-only to all premium lines.
_core._C94_SPLIT_ITEMS = ("FERTILIZER", "MELON", "STRAWBERRY", "MILK", "WOOL")
_core._C94_SPLIT_CAPS = {"FERTILIZER": 10}
_core._C94_CLONE_THRESHOLD = 0
_core._C94_SPLIT_HORIZON = 1


def agent(obs, config=None):
    return _core.agent(obs, config)
