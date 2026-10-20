"""Wrapper loading the X036 multi-file agent (stevenleehans) freshly per import."""
import importlib.util
import sys
import uuid
from pathlib import Path

_X = Path(__file__).resolve().parent / "x036"

for _name in ("community_v1_1_base", "community_v1_base", "x036_supply_model"):
    sys.modules.pop(_name, None)
if str(_X) not in sys.path:
    sys.path.insert(0, str(_X))

_tag = "_x036_main_" + uuid.uuid4().hex[:8]
_spec = importlib.util.spec_from_file_location(_tag, _X / "main.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

agent = _mod.agent
