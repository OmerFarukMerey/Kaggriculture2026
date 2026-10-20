"""Re-run a recorded episode locally from its stored action streams, so we can see
PRIVATE state (shed) and attribute exact per-item market revenue to each seat."""
import json, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import REPLAYS
from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as K

def rerun(ep):
    p = Path(ep)
    if not p.is_file(): p = REPLAYS / f"episode-{ep}-replay.json"
    rep = json.load(open(p, encoding="utf-8"))
    steps = rep["steps"]
    cfg = dict(rep["configuration"]); cfg["seed"] = (rep.get("info") or {}).get("seed")
    acts = [[steps[t][s].get("action") for t in range(len(steps))] for s in (0,1)]
    revenue = [collections.Counter(), collections.Counter()]
    units   = [collections.Counter(), collections.Counter()]
    spend   = [collections.Counter(), collections.Counter()]
    timeline = []   # (step, pid, item, price)
    orig_commit = K._commit_unit
    cur = {"pid": None}
    # wrap _process_market to know which player each _commit_unit belongs to
    orig_pm = K._process_market
    def commit(op, item, price, farm, private, market, shed_capacity=100):
        ok = orig_commit(op, item, price, farm, private, market, shed_capacity)
        if ok:
            pid = cur["map"].get(id(farm))
            if pid is not None:
                if op == "SELL":
                    revenue[pid][item] += price; units[pid][item] += 1
                    timeline.append((cur["step"], pid, item, price))
                else: spend[pid][op+":"+str(item)] += price
        return ok
    def pm(state, env):
        cur["map"] = {id(f): i for i, f in enumerate(state[0].observation.farms)}
        cur["step"] = int(state[0].observation.get("step", 0) if hasattr(state[0].observation,"get") else getattr(state[0].observation,"step",0))
        return orig_pm(state, env)
    K._commit_unit = commit; K._process_market = pm
    # money spent on hires/land: track via money deltas minus market
    try:
        env = make("kaggriculture", configuration=cfg, debug=False)
        def mk(s):
            def f(obs, conf):
                t = obs["step"]
                return acts[s][t+1] if t+1 < len(acts[s]) else {}
            return f
        env.run([mk(0), mk(1)])
    finally:
        K._commit_unit = orig_commit; K._process_market = orig_pm
    got = [env.steps[-1][i].reward for i in (0,1)]
    want = rep.get("rewards") or [steps[-1][i].get("reward") for i in (0,1)]
    return {"ep": str(ep), "teams": (rep.get("info") or {}).get("TeamNames"),
            "want": want, "got": got, "match": got == want,
            "revenue": [dict(r) for r in revenue], "units": [dict(u) for u in units],
            "spend": [dict(s) for s in spend], "timeline": timeline,
            "env": env}

if __name__ == "__main__":
    for ep in sys.argv[1:]:
        r = rerun(ep)
        print(f"\n=== {ep} {r['teams']} match={r['match']} want={r['want']} got={r['got']}")
        for i in (0,1):
            tot = sum(r["revenue"][i].values())
            print(f"  seat{i} gross sell revenue {tot:,.0f}")
            for k, v in sorted(r["revenue"][i].items(), key=lambda kv:-kv[1]):
                print(f"     {k:12s} {v:9,.0f}  ({100*v/max(tot,1):4.1f}%)")
            print(f"     spend: {dict(sorted(r['spend'][i].items(), key=lambda kv:-kv[1]))}")
