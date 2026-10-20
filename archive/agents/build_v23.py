"""Build main.py (v23) = Boatlee base + v22 detection/terminal + v23 controller.

Usage: python build_v23.py [threshold]
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
threshold = sys.argv[1] if len(sys.argv) > 1 else "8.0"

base = (HERE / "boatlee_v16.py").read_text(encoding="utf-8")
v22 = (HERE / "v22_tail.py").read_text(encoding="utf-8")
v23 = (HERE / "v23_tail.py").read_text(encoding="utf-8")
tracks = (HERE / "boatlee_tracks.b85").read_text(encoding="utf-8").strip()

base = base.replace(
    "Boatlee V16-RC2-MarketRelay for Kaggriculture.",
    "v23 for Kaggriculture: Boatlee V16-RC2 production core plus a closed-loop\n"
    "market controller (absorption-paced, copy-aware, cash/feed-safe) and\n"
    "terminal liquidation.",
    1,
)
v22 = v22.replace("__TRACKS_B85__", tracks)
v22 = v22.replace("__V22_THRESHOLD__", threshold)

out_text = base.rstrip() + "\n\n\n" + v22.rstrip() + "\n\n\n" + v23
out = HERE / "main.py"
out.write_text(out_text, encoding="utf-8", newline="\n")
compile(out_text, "main.py", "exec")
print(f"wrote {out} ({out.stat().st_size} bytes), threshold={threshold}")
