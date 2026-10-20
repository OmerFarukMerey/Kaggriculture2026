"""Pooled group comparison with band matching. Usage:
py -3.12 harness/pool_cmp.py "labelA=v24,v25,v26" "labelB=v27" """
import sys, statistics, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from adjrate import load, elo_perf, boot

def group(spec):
    label, tags = spec.split("=")
    rows = []
    for t in tags.split(","):
        rows += [r for r in load(t) if r["opp_rating"] is not None]
    return label, rows

def show(label, rows, extra=""):
    w = sum(1 for r in rows if r["outcome"] == "WIN"); l = sum(1 for r in rows if r["outcome"] == "LOSS")
    t = len(rows) - w - l
    mo = statistics.mean(r["opp_rating"] for r in rows); e = elo_perf(rows)
    b = boot(rows, 2000)
    print(f"  {label:22s}{extra} n={len(rows):4d} {w:4d}-{l:4d}-{t:3d} wr={(w+.5*t)/len(rows):.3f} "
          f"meanOpp={mo:6.0f} eloPerf={e:6.0f} [{b[50]:5.0f},{b[1949]:5.0f}]")
    return e

def diff(la, A, lb, B, tag=""):
    rnd = random.Random(21); d = []
    for _ in range(2000):
        sa = [A[rnd.randrange(len(A))] for _ in A]; sb = [B[rnd.randrange(len(B))] for _ in B]
        d.append(elo_perf(sa) - elo_perf(sb))
    d.sort()
    print(f"  -> {la} minus {lb} {tag}: {elo_perf(A)-elo_perf(B):+.0f} "
          f"[{d[50]:+.0f},{d[1949]:+.0f}] P>0={sum(1 for x in d if x>0)/len(d):.3f}")

if __name__ == "__main__":
    la, A = group(sys.argv[1]); lb, B = group(sys.argv[2])
    print("ALL EPISODES")
    show(la, A); show(lb, B); diff(la, A, lb, B)
    for lo, hi in [(1000, 1600), (1600, 2000), (2000, 2400), (2400, 4000), (1200, 2400)]:
        a = [r for r in A if lo <= r["opp_rating"] < hi]; b = [r for r in B if lo <= r["opp_rating"] < hi]
        if len(a) < 8 or len(b) < 8: continue
        print(f"opp band {lo}-{hi}")
        show(la, a); show(lb, b); diff(la, a, lb, b, f"[{lo}-{hi}]")
