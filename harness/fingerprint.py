"""Identify which local agent a live submission runs: replay the live seed with the opponent's
recorded actions and a candidate in the target seat; report the fraction of steps whose
actions match the recorded ones exactly (identical code should reproduce ~100%).

    py -3.12 harness/fingerprint.py <pick.json> <candidates.json> <out.json> <workers>
"""
import json, sys, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

REP = Path(__file__).resolve().parent.parent.parent / "kaggriculture-data" / "replays_final"
LIVE = Path(__file__).resolve().parent.parent / "analysis" / "final" / "live"


def slim(ep, sid):
    out = LIVE / f"slim_{ep}.json"
    if out.exists():
        return json.loads(out.read_text())
    r = json.load(open(REP / f"episode-{ep}-replay.json", encoding="utf-8"))
    lst = json.load(open(LIVE / f"list_{sid}.json"))
    e = [x for x in lst["episodes"] if x["id"] == ep][0]
    seat = [a.get("index", 0) for a in e["agents"] if a["submissionId"] == sid][0]
    d = dict(ep=ep, sid=sid, seed=r["info"]["seed"], seat=seat, teams=r["info"]["TeamNames"],
             actions=[[s[k]["action"] for k in range(2)] for s in r["steps"]],
             rewards=[s.get("reward") for s in r["steps"][-1]])
    out.write_text(json.dumps(d))
    return d


def job(args):
    d, name, path = args
    from kaggle_environments import make
    from kaggle_environments.agent import build_agent
    seat, acts = d["seat"], d["actions"]
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": d["seed"]}, debug=False)
    loaded, _ = build_agent(path, env.agents, env.name)
    mine = {}

    def cand(obs, cfg):
        a = loaded(obs, cfg)
        mine[int(obs.step)] = a
        return a

    def opp(obs, cfg):
        t = int(obs.step)
        return acts[t + 1][1 - seat] if t + 1 < len(acts) else {"farmer": ["PASS"], "hands": [], "market": []}

    agents = [cand, opp] if seat == 0 else [opp, cand]
    try:
        env.run(agents)
    except Exception as exc:
        return dict(ep=d["ep"], sid=d["sid"], cand=name, error=repr(exc))
    n = match = 0
    first_diff = None
    for t in range(len(acts) - 1):
        if t not in mine:
            continue
        n += 1
        if json.dumps(mine[t], sort_keys=True) == json.dumps(acts[t + 1][seat], sort_keys=True):
            match += 1
        elif first_diff is None:
            first_diff = t
    return dict(ep=d["ep"], sid=d["sid"], cand=name, n=n, match=match, frac=match / max(n, 1), first_diff=first_diff,
                reward=[s.reward for s in env.steps[-1]][seat], live_reward=d["rewards"][seat])


def main():
    pick = json.load(open(sys.argv[1])); cands = json.load(open(sys.argv[2]))
    out, workers = Path(sys.argv[3]), int(sys.argv[4])
    slims = [slim(int(ep), int(sid)) for sid, eps in pick.items() for ep in eps]
    jobs = [(d, n, p) for d in slims for n, p in cands.items()]
    print(len(jobs), "jobs", flush=True)
    res = []
    with ProcessPoolExecutor(max_workers=workers, max_tasks_per_child=1) as ex:
        for i, r in enumerate(ex.map(job, jobs)):
            res.append(r)
            if i % 25 == 0:
                out.write_text(json.dumps(res)); print(i, flush=True)
    out.write_text(json.dumps(res))
    best = {}
    for r in res:
        k = (r["sid"], r["ep"])
        if "frac" in r and r["frac"] > best.get(k, (None, -1))[1]:
            best[k] = (r["cand"], r["frac"], r["first_diff"])
    for k in sorted(best):
        print(k, best[k])


if __name__ == "__main__":
    main()
