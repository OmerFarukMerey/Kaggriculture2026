"""Clone share of the field: what fraction of the opponents we met in a period are
behavioural clones of a given chassis. Works off slim replays (first 62 steps).
Usage: py -3.12 harness/clone_share.py <tag> <chassis> [kmax] [maxeps]
"""
import json, sys, random, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, DATA_ROOT, REPLAYS, resolve_agent

SLIM = DATA_ROOT / "slim"
tag, chassis = sys.argv[1], sys.argv[2]
KMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 40
MAXEPS = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9

SRC = resolve_agent(chassis).read_text(encoding="utf-8")
CODE = compile(SRC, "<chassis>", "exec")
MODNAMES = None

def fresh():
    global MODNAMES
    before = set(sys.modules)
    ns = {"__name__": "chassisprobe"}
    exec(CODE, ns)
    if MODNAMES is None:
        MODNAMES = set(sys.modules) - before
    for m in MODNAMES:
        sys.modules.pop(m, None)
    fn = None
    for k, v in ns.items():
        if k.startswith("__"):
            continue
        if callable(v) and getattr(v, "__module__", None) == "chassisprobe":
            fn = v          # last callable by INSERTION order = what the Kaggle loader picks
    return fn

def norm(a): return json.dumps(a, sort_keys=True, default=str)

def probe(rep, seat, kmax):
    fn = fresh(); cfg = rep.get("configuration") or {}; steps = rep["steps"]
    m = c = 0
    for t in range(min(kmax, len(steps) - 1)):
        cell = steps[t][seat]; obs = cell.get("observation")
        act = steps[t + 1][seat].get("action")
        if obs is None or act is None: continue
        obs = dict(obs)
        if "step" not in obs: obs["step"] = steps[t][0]["observation"].get("step", t)
        obs.setdefault("player", seat)
        try:
            pred = fn(obs, cfg)
        except TypeError:
            try: pred = fn(obs)
            except Exception: pred = None
        except Exception:
            pred = None
        c += 1
        m += (pred is not None and norm(pred) == norm(act))
    return m, c

rows = [json.loads(l) for l in open(ROOT / "analysis" / "summ" / f"{tag}.jsonl", encoding="utf-8")]
seen = set(); rows = [r for r in rows if not (r["episode"] in seen or seen.add(r["episode"]))]
import os
D0, D1 = os.environ.get("CS_D0"), os.environ.get("CS_D1")
if D0: rows = [r for r in rows if D0 <= r["createTime"][:10] <= D1]
random.Random(3).shuffle(rows)
rows = rows[:MAXEPS]
hits = []; byopp = collections.Counter(); tot = collections.Counter()
n = 0
for r in rows:
    p = SLIM / f"episode-{r['episode']}-slim.json"
    if not p.exists():
        p = REPLAYS / f"episode-{r['episode']}-replay.json"
        if not p.exists(): continue
    try: rep = json.load(open(p, encoding="utf-8"))
    except Exception: continue
    oseat = 1 - r["seat"]
    m, c = probe(rep, oseat, KMAX)
    if c == 0: continue
    frac = m / c
    n += 1
    tot[r["opponent"]] += 1
    if frac >= 0.85: byopp[r["opponent"]] += 1
    hits.append((frac, r["opponent"], r["episode"], r["outcome"]))
cl = sum(1 for f, *_ in hits if f >= 0.85)
print(f"{tag} vs {chassis}: probed {n} episodes, clone(>=0.85)={cl} share={cl/max(n,1):.3f}")
print("  frac distribution:", collections.Counter(round(f, 1) for f, *_ in hits).most_common())
w = sum(1 for f, o, e, oc in hits if f >= 0.85 and oc == "WIN")
t_ = sum(1 for f, o, e, oc in hits if f >= 0.85 and oc == "TIE")
print(f"  vs clones: {w}-{cl-w-t_}-{t_}")
w2 = sum(1 for f, o, e, oc in hits if f < 0.85 and oc == "WIN")
t2 = sum(1 for f, o, e, oc in hits if f < 0.85 and oc == "TIE")
nn = n - cl
print(f"  vs non-clones: {w2}-{nn-w2-t2}-{t2}")
json.dump([{"frac": f, "opponent": o, "episode": e, "outcome": oc} for f, o, e, oc in hits],
          open(ROOT / "analysis" / f"cloneshare_{tag}{os.environ.get('CS_SUF','')}_{Path(chassis).stem}.json", "w"), indent=1)
