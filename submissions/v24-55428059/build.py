"""Build main.py (v24) = Rayk C94 base + v24 layer (clone escalation +
Boatlee-family front-running).

Usage: python build_v24.py
"""
import base64
import importlib.util
import json
import zlib
from pathlib import Path

HERE = Path(__file__).parent

base = (HERE / "rayk_c94.py").read_text(encoding="utf-8")
tail = (HERE / "v24_tail.py").read_text(encoding="utf-8")
tracks = (HERE / "boatlee_tracks.b85").read_text(encoding="utf-8").strip()

# Re-encode the Boatlee route actions for embedding.
spec = importlib.util.spec_from_file_location("boat_src", HERE / "boatlee_v16.py")
boat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(boat)
blob = base64.b85encode(zlib.compress(
    json.dumps(boat._LEGACY_ACTIONS).encode(), 9)).decode()
chunks = [blob[i:i + 100] for i in range(0, len(blob), 100)]
route_lines = "\n".join(f'        "{chunk}"' for chunk in chunks)

tail = tail.replace("__TRACKS_B85__", tracks)
tail = tail.replace("__C94_TRACK_B85__", (HERE / "c94_track.b85").read_text(encoding="utf-8").strip())
tail = tail.replace("__BOAT_ROUTE_B85__", route_lines)

out_text = base.rstrip() + "\n\n\n" + tail
out = HERE / "main.py"
out.write_text(out_text, encoding="utf-8", newline="\n")
compile(out_text, "main.py", "exec")
print(f"wrote {out} ({out.stat().st_size} bytes)")
