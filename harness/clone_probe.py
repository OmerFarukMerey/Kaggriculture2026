"""Behavioural clone test: replay the OPPONENT's own observation stream into a fresh
stock kaito_v43 and measure how often v43 emits exactly the opponent's action."""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS

SRC = (ROOT / "agents" / "public" / "kaito_v43.py").read_text(encoding="utf-8")
CODE = compile(SRC, "<v43>", "exec")

MODNAMES = None

def fresh_v43():
    """Exec kaito_v43 in a clean namespace, purging its bundled sys.modules."""
    global MODNAMES
    before = set(sys.modules)
    ns = {"__name__": "v43probe"}
    exec(CODE, ns)
    if MODNAMES is None:
        MODNAMES = set(sys.modules) - before
    for m in MODNAMES:
        sys.modules.pop(m, None)
    return ns["_kaggle_submission_entrypoint"]

def norm(a):
    return json.dumps(a, sort_keys=True, default=str)

def probe(replay, seat, kmax=60):
    """Return (matches, compared) over the first kmax steps for `seat`."""
    fn = fresh_v43()
    cfg = replay.get("configuration") or {}
    steps = replay["steps"]
    m = c = 0
    per = []
    for t in range(min(kmax, len(steps) - 1)):
        cell = steps[t][seat]
        obs = cell.get("observation")
        act = steps[t + 1][seat].get("action")
        if obs is None:
            continue
        obs = dict(obs)
        if "step" not in obs:
            obs["step"] = steps[t][0]["observation"].get("step", t)
        obs.setdefault("player", seat)
        try:
            pred = fn(obs, cfg)
        except Exception:
            pred = None
        if act is None:
            continue
        c += 1
        ok = pred is not None and norm(pred) == norm(act)
        m += ok
        per.append(ok)
    return m, c, per

if __name__ == "__main__":
    ep = sys.argv[1]
    r = json.load(open(REPLAYS / f"episode-{ep}-replay.json", encoding="utf-8"))
    t0 = time.time()
    for seat in (0, 1):
        m, c, per = probe(r, seat, int(sys.argv[2]) if len(sys.argv) > 2 else 60)
        print(f"seat {seat} ({(r['info']['TeamNames'])[seat]}): {m}/{c} = {m/max(c,1):.3f}  {''.join('1' if x else '0' for x in per)}")
    print(f"{time.time()-t0:.1f}s")
