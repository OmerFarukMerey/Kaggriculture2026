"""Build main.py (v22) = Boatlee V16-RC2 base + v22 anti-copy/terminal layer.

Usage: python build_v22.py [threshold]
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
threshold = sys.argv[1] if len(sys.argv) > 1 else "8.0"

base = (HERE / "boatlee_v16.py").read_text(encoding="utf-8")
tail = (HERE / "v22_tail.py").read_text(encoding="utf-8")
tracks = (HERE / "boatlee_tracks.b85").read_text(encoding="utf-8").strip()

base = base.replace(
    "Boatlee V16-RC2-MarketRelay for Kaggriculture.",
    "v22 for Kaggriculture: Boatlee V16-RC2 production core plus a\n"
    "copy-detection/front-running layer and step-717 terminal liquidation.",
    1,
)
tail = tail.replace("__TRACKS_B85__", tracks)
tail = tail.replace("__V22_THRESHOLD__", threshold)

out_text = base.rstrip() + "\n\n\n" + tail
out = HERE / "main.py"
out.write_text(out_text, encoding="utf-8", newline="\n")
compile(out_text, "main.py", "exec")
print(f"wrote {out} ({out.stat().st_size} bytes), threshold={threshold}")
