"""Multi-chassis field composition probe.

For each of our live episodes, take the OPPONENT's seat, replay their own recorded
observation stream into every candidate chassis we hold, and count exact action
matches.  Observation streams are parsed ONCE per episode and scored against all
chassis (the expensive part is agent CPU, not JSON).

Indexing follows harness/clone_probe.py exactly:
  action at steps[t+1][seat] was computed from observation at steps[t][seat],
  and agent state is built from t=0 forward.
"""
import json, sys, os, time, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, DATA_ROOT, REPLAYS, resolve_agent

SLIM = DATA_ROOT / "slim"
KMAX = int(os.environ.get("FP_KMAX", "40"))

CHASSIS = [
    "kaito_v43", "kaito_v48", "kaito_v27",
    "tetsu", "tetsu_v2",
    "readmarket",
    "boatlee_v16", "boatlee_v20",           # boatlee_v20 == multiroute == multiroute_v2 (md5)
    "rayk_c94", "rayk_c92",
    "breaking_tie", "salem3000",            # salem3000 == salem2900 (md5)
    "rc5", "frontier_moon", "frontier_soil", "public_v211",
    "opp_yy", "opp_bohannn",
    "v31", "v32", "v33",
]

_CODE, _MODS = {}, {}

def load(name):
    if name not in _CODE:
        _CODE[name] = compile(resolve_agent(name).read_text(encoding="utf-8"), f"<{name}>", "exec")
    return _CODE[name]

def fresh(name):
    before = set(sys.modules)
    ns = {"__name__": "chassisprobe"}
    exec(load(name), ns)
    if name not in _MODS:
        _MODS[name] = set(sys.modules) - before
    for m in _MODS[name]:
        sys.modules.pop(m, None)
    fn = None
    for k, v in ns.items():
        if k.startswith("__"):
            continue
        if callable(v) and getattr(v, "__module__", None) == "chassisprobe":
            fn = v      # last callable by INSERTION order == what the Kaggle loader picks
    return fn

def norm(a):
    return json.dumps(a, sort_keys=True, default=str)


def stream(rep, seat, kmax=KMAX):
    """Cache-able (cfg, [(obs, normalised_action), ...]) for one seat."""
    cfg = rep.get("configuration") or {}
    steps = rep["steps"]
    out = []
    for t in range(min(kmax, len(steps) - 1)):
        obs = steps[t][seat].get("observation")
        act = steps[t + 1][seat].get("action")
        if obs is None or act is None:
            continue
        obs = dict(obs)
        if "step" not in obs:
            obs["step"] = steps[t][0]["observation"].get("step", t)
        obs.setdefault("player", seat)
        out.append((obs, norm(act)))
    return cfg, out


def score(name, cfg, pairs):
    """Fraction of the recorded actions this chassis reproduces exactly."""
    fn = fresh(name)
    if fn is None:
        return None
    m = 0
    for obs, act in pairs:
        try:
            pred = fn(obs, cfg)
        except TypeError:
            try:
                pred = fn(obs)
            except Exception:
                pred = None
        except Exception:
            pred = None
        m += (pred is not None and norm(pred) == act)
    return m / len(pairs) if pairs else None


def load_replay(ep):
    for p in (REPLAYS / f"episode-{ep}-replay.json", SLIM / f"episode-{ep}-slim.json"):
        if p.exists():
            try:
                return json.load(open(p, encoding="utf-8"))
            except Exception:
                return None
    return None


if __name__ == "__main__":
    rows = json.load(open(ROOT / "analysis" / sys.argv[1], encoding="utf-8"))
    outp = ROOT / "analysis" / sys.argv[2]
    only = sys.argv[3].split(",") if len(sys.argv) > 3 and sys.argv[3] != "-" else CHASSIS
    if len(sys.argv) > 4:
        si, sn = (int(x) for x in sys.argv[4].split("/"))
        rows = rows[si::sn]
    done = {}
    if outp.exists():
        done = {r["episode"]: r for r in json.load(open(outp, encoding="utf-8"))}
    res = []
    t0 = time.time()
    for i, r in enumerate(rows):
        prev = done.get(r["episode"])
        if prev and all(c in prev.get("m", {}) for c in only):
            res.append(prev); continue
        rep = load_replay(r["episode"])
        if rep is None:
            print("NOREPLAY", r["episode"], flush=True); continue
        cfg, pairs = stream(rep, 1 - r["seat"])
        if not pairs:
            print("NOSTREAM", r["episode"], flush=True); continue
        rec = dict(r); rec["n"] = len(pairs); rec["m"] = dict((prev or {}).get("m", {}))
        for c in only:
            try:
                rec["m"][c] = score(c, cfg, pairs)
            except Exception as e:
                rec["m"][c] = None
                print("ERR", c, r["episode"], type(e).__name__, e, flush=True)
        res.append(rec)
        if i % 10 == 0:
            best = max((v for v in rec["m"].values() if v is not None), default=0)
            print(f"{i}/{len(rows)} {time.time()-t0:.0f}s ep{r['episode']} best={best:.2f}", flush=True)
            json.dump(res, open(outp, "w"))
    json.dump(res, open(outp, "w"))
    print("wrote", outp, len(res), f"{time.time()-t0:.0f}s")
