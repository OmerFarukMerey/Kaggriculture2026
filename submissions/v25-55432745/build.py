"""Build main.py (v25) = v24 build + yarn-adaptive livestock swap tail."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
subprocess.run([sys.executable, str(HERE / "build_v24.py")], check=True)
base = (HERE / "main.py").read_text(encoding="utf-8")
tail = (HERE / "v25_tail.py").read_text(encoding="utf-8")
out_text = base.rstrip() + "\n\n\n" + tail
(HERE / "main.py").write_text(out_text, encoding="utf-8", newline="\n")
compile(out_text, "main.py", "exec")
print(f"wrote main.py ({len(out_text)} chars) with v25 tail")
