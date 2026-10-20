"""MILK/MELON sold-volume + coin-curve probe over a step window. Adapted from fert_probe.py."""
import importlib.util, sys, json
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import resolve_agent

W0, W1 = 192, 288   # days 8-11

def load(tag, fn):
    spec = importlib.util.spec_from_file_location(tag, resolve_agent(fn))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def one(fa, fb, seed, coins=False):
    from kaggle_environments import make
    a, b = load("pa_%d"%seed, fa), load("pb_%d"%seed, fb)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([a.agent, b.agent])
    st = env.steps
    res = {}
    for seat in (0, 1):
        win = Counter(); allc = Counter(); day0 = []
        for t in range(len(st)):
            act = st[t][seat].get("action")
            if not act: continue
            for m in (act.get("market", []) or []):
                if not m: continue
                if t < 24 and m[0] != "SELL":
                    day0.append((t, m))
                if m[0] == "SELL":
                    q = m[2] if len(m) > 2 else 1
                    allc[m[1]] += q
                    if W0 <= t < W1: win[m[1]] += q
        res[seat] = {"win_milk": win["MILK"], "win_melon": win["MELON"],
                     "win_all": dict(win), "all": dict(allc), "day0": day0}
    res["final"] = [s.reward for s in st[-1]]
    if coins:
        res["coins"] = [[st[t][0]["observation"]["farms"][s].get("money") for t in range(len(st))] for s in (0,1)]
    return res

if __name__ == "__main__":
    fa, fb = sys.argv[1], sys.argv[2]
    seeds = [int(x) for x in sys.argv[3].split(",")]
    coins = "--coins" in sys.argv
    out = {}
    for sd in seeds:
        r = one(fa, fb, sd, coins)
        out[sd] = r
        print(f"seed={sd} final={r['final']}", flush=True)
        for seat, tag in ((0, fa), (1, fb)):
            d = r[seat]
            print(f"   seat{seat} {tag:22s} days8-11 MILK={d['win_milk']:>4} MELON={d['win_melon']:>4} | win_all={d['win_all']}", flush=True)
            print(f"        whole-game sold={d['all']}", flush=True)
        if coins:
            c = r["coins"]
            print("        coin curve (t: A / B):", flush=True)
            for t in list(range(0,720,24)):
                print(f"          t={t:>3} d{t//24:>2}  A={c[0][t]:>10.0f}  B={c[1][t]:>10.0f}  diff={c[0][t]-c[1][t]:>+10.0f}", flush=True)
            print("        FINE 216-300:", flush=True)
            for t in range(216, 301, 4):
                print(f"          t={t:>3}  A={c[0][t]:>10.0f}  B={c[1][t]:>10.0f}  diff={c[0][t]-c[1][t]:>+10.0f}", flush=True)
    json.dump({str(k): {kk: (vv if kk != 'coins' else None) for kk, vv in v.items()} for k, v in out.items()},
              open(sys.argv[sys.argv.index("--out")+1], "w") if "--out" in sys.argv else sys.stdout, indent=1, default=str)
