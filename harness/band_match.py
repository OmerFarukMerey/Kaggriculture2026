"""Common-support comparison: restrict two submissions to a shared opponent-rating band
so neither elo-perf is an extrapolation off a saturated win rate."""
import sys, statistics, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from adjrate import load, elo_perf

def band(tag, lo, hi):
    return [r for r in load(tag) if r["opp_rating"] is not None and lo <= r["opp_rating"] < hi]

def show(tag, rows):
    w = sum(1 for r in rows if r["outcome"] == "WIN"); l = sum(1 for r in rows if r["outcome"] == "LOSS")
    t = len(rows) - w - l
    if not rows: return None
    mo = statistics.mean(r["opp_rating"] for r in rows)
    e = elo_perf(rows)
    print(f"   {tag:6s} n={len(rows):4d} {w:3d}-{l:3d}-{t:2d} wr={(w+.5*t)/len(rows):.3f} meanOpp={mo:6.0f} eloPerf={e:6.0f}")
    return e

if __name__ == "__main__":
    tags = sys.argv[1].split(",")
    bands = [(1000, 1600), (1600, 2000), (2000, 2400), (2400, 2600), (2600, 4000), (1600, 2600)]
    for lo, hi in bands:
        print(f"opp band {lo}-{hi}:")
        got = {}
        for tg in tags:
            rows = band(tg, lo, hi)
            if rows: got[tg] = (rows, show(tg, rows))
        if len(tags) == 2 and all(t in got for t in tags) and all(len(got[t][0]) >= 8 for t in tags):
            A, B = got[tags[0]][0], got[tags[1]][0]
            rnd = random.Random(9); d = []
            for _ in range(2000):
                sa = [A[rnd.randrange(len(A))] for _ in A]; sb = [B[rnd.randrange(len(B))] for _ in B]
                d.append(elo_perf(sa) - elo_perf(sb))
            d.sort()
            print(f"   -> {tags[0]}-{tags[1]} = {got[tags[0]][1]-got[tags[1]][1]:+.0f} "
                  f"[{d[50]:+.0f},{d[1949]:+.0f}] P>0={sum(1 for x in d if x>0)/len(d):.3f}")
        print()
