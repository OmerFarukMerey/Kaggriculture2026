"""Where does the coin gap form? Daily money gap for a set of episodes."""
import json, sys, statistics, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS
from route_recon import load, summarize

eps = json.load(open(ROOT/"analysis"/sys.argv[1], encoding="utf-8"))
if len(sys.argv) > 2 and sys.argv[2] == "loss":
    eps = [e for e in eps if e["outcome"] == "LOSS"]
rows = []
for e in eps:
    p = REPLAYS / f"episode-{e['episode']}-replay.json"
    if not p.exists(): continue
    sm = summarize(load(e["episode"]))
    s = e["seat"]
    gap = {}
    for r in sm["days"]:
        gap[r["day"]] = r[f"money{s}"] - r[f"money{1-s}"]
    rows.append({"ep": e["episode"], "opp": e["opponent"], "seat": s, "outcome": e["outcome"],
                 "final_gap": e["margin"], "gap": gap, "sm": sm})
print(f"{len(rows)} episodes\n")
hdr = "  ".join(f"d{d:02d}" for d in (5,8,10,11,12,15,18,21,24,27,29))
print(f"{'ep':11s} {'opp':22s} st {'out':5s} {hdr}   final")
for r in rows:
    g = r["gap"]
    cells = "  ".join(f"{g.get(d,0)/1000:+5.1f}" for d in (5,8,10,11,12,15,18,21,24,27,29))
    print(f"{r['ep']:11s} {r['opp'][:21]:22s} {r['seat']}  {r['outcome']:5s} {cells}  {r['final_gap']/1000:+7.1f}k")

print("\n--- mean gap by day (k coins) ---")
for d in range(30):
    v = [r["gap"].get(d) for r in rows if d in r["gap"]]
    if not v: continue
    print(f"  day {d:2d}: mean {statistics.mean(v)/1000:+7.2f}k  median {statistics.median(v)/1000:+7.2f}k")

print("\n--- gap CHANGE per day-window (mean, k) ---")
wins = [(0,5),(5,10),(10,11),(11,15),(15,20),(20,25),(25,29),(29,'final')]
for a,b in wins:
    if b == 'final':
        v=[(r['final_gap']-r['gap'].get(a,0))/1000 for r in rows if a in r['gap']]
        lab=f"d{a}->final"
    else:
        v=[(r['gap'].get(b,0)-r['gap'].get(a,0))/1000 for r in rows if a in r['gap'] and b in r['gap']]
        lab=f"d{a}->d{b}"
    print(f"  {lab:12s} mean {statistics.mean(v):+7.2f}k  median {statistics.median(v):+7.2f}k")
