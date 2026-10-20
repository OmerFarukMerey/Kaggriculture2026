"""Build main.py (v21.2) from the decoded public v21.1 artifact + new tail.

Usage: python build_v212.py <base_proto_index> <mirror_threshold>
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
base_index = sys.argv[1] if len(sys.argv) > 1 else "None"
threshold = sys.argv[2] if len(sys.argv) > 2 else "8.0"

source = (HERE / "public_v211.py").read_text(encoding="utf-8")
tail = (HERE / "v212_tail.py").read_text(encoding="utf-8")

cut = source.index("def agent(obs):")
head = source[:cut].rstrip() + "\n\n\n"
head = head.replace(
    "v21.1 conditional Top-30 memory Kaggriculture agent.",
    "v21.2 conditional Top-30 memory Kaggriculture agent.\n\n"
    "Extends the public v21.1 artifact with public-copy detection, one-step\n"
    "sell front-running against detected copies, and a step-717 terminal\n"
    "pre-dump ahead of the meta's standard step-718 liquidation.",
    1,
)
tail = tail.replace("__BASE_PROTO_INDEX__", base_index)
tail = tail.replace("__MIRROR_THRESHOLD__", threshold)

out = HERE / "main.py"
out.write_text(head + tail, encoding="utf-8")
compile(head + tail, "main.py", "exec")
print(f"wrote {out} ({out.stat().st_size} bytes), base_proto_index={base_index}, threshold={threshold}")
