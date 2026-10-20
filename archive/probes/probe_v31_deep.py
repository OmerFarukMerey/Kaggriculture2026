"""Deep probe: monkeypatch v31's own helpers to record (a) clone_distance at
every step, (b) whether _v31_repay actually found the full borrowed quantity
(conservation), (c) each borrow.

usage: py -3.12 probe_v31_deep.py <opponent.py> <seed> <seat>
"""
import importlib.util, sys, json, collections
from pathlib import Path
HERE = Path(__file__).parent

def load(tag, filename):
    spec = importlib.util.spec_from_file_location(tag, HERE / filename)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

opp_file, seed, seat = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
a = load("A", "v31.py")
b = load("B", opp_file)

dists = []
borrow_log = []
repay_log = []

_orig_cd = a._v31_clone_distance
def cd(obs):
    d = _orig_cd(obs)
    dists.append(d)
    return d
a._v31_clone_distance = cd

_orig_repay = a._v31_repay
def repay(market, due):
    out = _orig_repay(market, due)
    # recompute how much was actually cancelled
    def tot(m):
        c = collections.Counter()
        for o in m:
            if isinstance(o, list) and len(o) >= 3 and o[0] == "SELL":
                c[o[1]] += int(o[2] or 0)
        return c
    before, after = tot(market), tot(out)
    cancelled = {k: before[k] - after.get(k, 0) for k in due}
    short = {k: due[k] - cancelled.get(k, 0) for k in due if due[k] - cancelled.get(k, 0) != 0}
    repay_log.append({"due": dict(due), "cancelled": cancelled, "shortfall": short})
    return out
a._v31_repay = repay

_orig_preempt = a._v31_preempt
def preempt(obs, action):
    before = a._V31_TELEMETRY["borrows"]
    out = _orig_preempt(obs, action)
    if a._V31_TELEMETRY["borrows"] > before:
        st = a._V31_SHIFT[1 if int(a._v43_get(obs, "player", 0) or 0) == 1 else 0]
        borrow_log.append({"step": int(a._v43_get(obs, "step", 0) or 0), "due": dict(st["due"])})
    return out
a._v31_preempt = preempt

from kaggle_environments import make
env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
pair = [a.agent, b.agent] if seat == 0 else [b.agent, a.agent]
env.run(pair)
r = [s.reward for s in env.steps[-1]]
finite = [d for d in dists if d != float("inf")]
open_steps = [d for d in finite if d <= a._V31_CLONE_MAX]
print(json.dumps({
    "opp": opp_file, "seed": seed, "seat": seat,
    "score_us": r[seat], "score_them": r[1-seat],
    "distance_evals": len(dists),
    "distance_min": min(finite) if finite else None,
    "distance_max": max(finite) if finite else None,
    "distance_median": sorted(finite)[len(finite)//2] if finite else None,
    "gate_open_steps": len(open_steps),
    "distance_hist_low": dict(collections.Counter(d for d in finite if d <= 20)),
    "borrows": borrow_log,
    "repay_shortfalls": [x for x in repay_log if x["shortfall"]],
    "n_repays": len(repay_log),
    "telemetry": a._V31_TELEMETRY,
}, indent=1, default=str), flush=True)
