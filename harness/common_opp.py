"""Rating-drift-FREE comparison: restrict two of our submissions to opponents BOTH met,
where the opponent's last submission predates both encounters (same opponent code).
No leaderboard rating is used at all, so era rating inflation/deflation cannot bias it.
"""
import sys, collections, statistics, random, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from adjrate import load, LASTSUB, ORDER

def rows_of(tags):
    out = []
    for t in tags.split(","):
        out += load(t)
    return out

def keyed(rows, frozen_only=True):
    d = collections.defaultdict(list)
    for r in rows:
        o = r["opponent"]
        if frozen_only:
            ls = LASTSUB.get(o)
            if not ls or ls[:19] >= r["createTime"][:19]:
                continue
        d[o].append(r)
    return d

def sc(r): return 1.0 if r["outcome"] == "WIN" else (0.5 if r["outcome"] == "TIE" else 0.0)

def compare(la, ta, lb, tb, frozen_only=True):
    A = keyed(rows_of(ta), frozen_only); B = keyed(rows_of(tb), frozen_only)
    shared = sorted(set(A) & set(B))
    if not shared:
        print(f"{la} vs {lb}: NO shared frozen opponents (field turned over completely)")
        return None
    # per-opponent win rates, then unweighted mean over opponents (equal weight per opponent)
    pa = [statistics.mean(sc(r) for r in A[o]) for o in shared]
    pb = [statistics.mean(sc(r) for r in B[o]) for o in shared]
    na = sum(len(A[o]) for o in shared); nb = sum(len(B[o]) for o in shared)
    d = [x - y for x, y in zip(pa, pb)]
    rnd = random.Random(31); bs = []
    for _ in range(4000):
        s = [d[rnd.randrange(len(d))] for _ in d]
        bs.append(statistics.mean(s))
    bs.sort()
    def elo(p):
        p = min(max(p, 1e-3), 1 - 1e-3); return 400 * math.log10(p / (1 - p))
    print(f"{la} vs {lb}: {len(shared)} shared frozen opponents  (games {na} vs {nb})")
    print(f"   mean per-opponent score  {la}={statistics.mean(pa):.3f}  {lb}={statistics.mean(pb):.3f}  "
          f"delta={statistics.mean(d):+.3f} boot95=[{bs[100]:+.3f},{bs[3899]:+.3f}] "
          f"P({la}>{lb})={sum(1 for x in bs if x>0)/len(bs):.3f}")
    print(f"   implied Elo gap = {elo(statistics.mean(pa))-elo(statistics.mean(pb)):+.0f}")
    return shared

if __name__ == "__main__":
    if len(sys.argv) > 2:
        for spec in [(sys.argv[1], sys.argv[2])]:
            la, ta = spec[0].split("="); lb, tb = spec[1].split("=")
            compare(la, ta, lb, tb)
    else:
        # overlap matrix
        keys = {t: set(keyed(load(t))) for t in ORDER if load(t)}
        ks = [k for k in ORDER if k in keys]
        print("shared FROZEN-opponent counts")
        print("       " + " ".join(f"{k:>6s}" for k in ks))
        for a in ks:
            print(f"{a:6s} " + " ".join(f"{len(keys[a]&keys[b]):6d}" for b in ks))
