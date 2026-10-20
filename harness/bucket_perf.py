"""Opponent-adjusted performance rating split by clone / non-clone bucket."""
import json, sys, statistics, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT
from adjrate import LB, load, elo_perf, boot

def run(tag, chassis):
    cs = json.load(open(ROOT / "analysis" / f"cloneshare_{tag}_{chassis}.json", encoding="utf-8"))
    frac = {c["episode"]: c["frac"] for c in cs}
    rows = [r for r in load(tag) if r["opp_rating"] is not None and r["episode"] in frac]
    for r in rows: r["frac"] = frac[r["episode"]]
    for label, sel in [("ALL", lambda r: True),
                       ("clone", lambda r: r["frac"] >= 0.85),
                       ("nonclone", lambda r: r["frac"] < 0.85)]:
        g = [r for r in rows if sel(r)]
        if len(g) < 5:
            print(f"  {tag:6s} {label:9s} n={len(g)} (too few)"); continue
        w = sum(1 for r in g if r["outcome"] == "WIN"); l = sum(1 for r in g if r["outcome"] == "LOSS")
        t = len(g) - w - l
        mo = statistics.mean(r["opp_rating"] for r in g)
        e = elo_perf(g); b = boot(g, 2000)
        print(f"  {tag:6s} {label:9s} n={len(g):3d} {w:3d}-{l:3d}-{t:2d} wr={(w+.5*t)/len(g):.3f} "
              f"meanOpp={mo:6.0f} eloPerf={e:6.0f} [{b[50]:5.0f},{b[1949]:5.0f}]")
    return rows

if __name__ == "__main__":
    pairs = [(a, b) for a, b in zip(sys.argv[1::2], sys.argv[2::2])]
    store = {}
    for tag, ch in pairs:
        print(f"--- {tag} vs {ch} ---")
        store[tag] = run(tag, ch)
    if len(pairs) == 2:
        (ta, _), (tb, _) = pairs
        for label, sel in [("ALL", lambda r: True), ("clone", lambda r: r["frac"] >= 0.85),
                           ("nonclone", lambda r: r["frac"] < 0.85)]:
            A = [r for r in store[ta] if sel(r)]; B = [r for r in store[tb] if sel(r)]
            if len(A) < 5 or len(B) < 5: continue
            rnd = random.Random(5); d = []
            for _ in range(2000):
                sa = [A[rnd.randrange(len(A))] for _ in A]; sb = [B[rnd.randrange(len(B))] for _ in B]
                d.append(elo_perf(sa) - elo_perf(sb))
            d.sort()
            print(f"{ta}-{tb} [{label}]: point={elo_perf(A)-elo_perf(B):+.0f} "
                  f"boot95=[{d[50]:+.0f},{d[1949]:+.0f}] P>0={sum(1 for x in d if x>0)/len(d):.3f}")
