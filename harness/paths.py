"""Path resolution for the repo layout.

Agent files live in several places (submissions/, candidates/, agents/public/, archive/agents/),
so the harness resolves a reference rather than assuming a flat directory. Bulk
replay data lives OUTSIDE the repo because it is ~23 GB; point KAGGRICULTURE_DATA
at it if you keep it somewhere other than ../kaggriculture-data.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = Path(os.environ.get("KAGGRICULTURE_DATA", ROOT.parent / "kaggriculture-data"))
REPLAYS = DATA_ROOT / "replays"
REPLAYS_TOP = DATA_ROOT / "replays_top"

_SEARCH = (
    Path.cwd(),
    ROOT,
    ROOT / "agents" / "public",
    ROOT / "archive" / "agents",
)


def resolve_agent(name):
    """Resolve an agent reference to a concrete .py file.

    Accepts, in order of precedence:
      * a path, relative to the current directory or absolute
      * a bare filename in agents/public/ or archive/agents/ ("kaito_v43.py", or "kaito_v43")
      * a submission alias -- "v30" finds submissions/v30-55597536/main.py
      * an unsubmitted build -- "cand-v48-mq" finds candidates/cand-v48-mq/main.py
    """
    p = Path(name)
    if p.is_file():
        return p.resolve()
    for base in _SEARCH:
        for cand in (base / name, base / f"{name}.py"):
            if cand.is_file():
                return cand.resolve()
    hits = []
    for subs in (ROOT / "submissions", ROOT / "candidates"):
        hits += sorted(subs.glob(f"{name}/main.py")) + sorted(subs.glob(f"{name}-*/main.py"))
    if hits:
        return hits[0].resolve()
    raise FileNotFoundError(
        f"could not resolve agent {name!r}. Tried the working directory, "
        f"agents/public/, archive/agents/, submissions/*/main.py and candidates/*/main.py"
    )


def submissions():
    """Every submission directory, oldest-numbered first."""
    return sorted((ROOT / "submissions").iterdir())
