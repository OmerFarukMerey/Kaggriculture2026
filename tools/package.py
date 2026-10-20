"""Package a submission's main.py into the submission.tar.gz Kaggle expects.

    py -3.12 tools/package.py <main.py-path-or-submission-alias> [--check]

Kaggle wants a gzipped tar containing a single top-level main.py. This copies
the submission's main.py into a clean staging directory (so nothing else in the
repo can leak into the archive), tars it, and writes submission.tar.gz next to
the source main.py.

--check additionally plays one self-play game from the staging directory, which
is the only reliable way to catch an agent that depends on a file living beside
it in the repo but absent from the tarball.
"""
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "harness"))
from paths import ROOT, resolve_agent  # noqa: E402

CHECK = """
import sys, os
os.chdir(sys.argv[1]); sys.path.insert(0, sys.argv[1])
from kaggle_environments import make
env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 5000}, debug=True)
env.run(["main.py", "main.py"])
print("SELFPLAY", [s.reward for s in env.steps[-1]])
print("FILES_AFTER", sorted(os.listdir(".")))
"""


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return 2
    main_py = resolve_agent(sys.argv[1])
    out = main_py.parent / "submission.tar.gz"
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp) / "main.py"
        shutil.copy2(main_py, staged)
        with tarfile.open(out, "w:gz") as tar:
            tar.add(staged, arcname="main.py")
        print(f"packaged {main_py.relative_to(ROOT)} -> {out.relative_to(ROOT)} "
              f"({out.stat().st_size:,} bytes)")
        if "--check" in sys.argv:
            script = Path(tmp) / "_check.py"
            script.write_text(CHECK, encoding="utf-8")
            r = subprocess.run([sys.executable, str(script), tmp],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            for line in (r.stdout or "").splitlines():
                if line.startswith(("SELFPLAY", "FILES_AFTER")):
                    print("  " + line)
            if r.returncode != 0:
                print("  CHECK FAILED — the agent does not run from a directory holding only main.py")
                print((r.stderr or "")[-800:])
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
