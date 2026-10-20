"""Lifetime- and band-matched controlled comparisons.
Both agents restricted to the same calendar window AND the same opponent-rating band,
which removes (a) the day-1 easy-matchmaking inflation and (b) field turnover."""
import sys, statistics, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from adjrate import load, elo_perf

def sel(tag, d0, d1, lo, hi, skip_first_day=False):
    rs = [r for r in load(tag) if r["opp_rating"] is not None]
    if skip_first_day:
        f = min(r["createTime"][:10] for r in rs)
        rs = [r for r in rs if r["createTime"][:10] != f]
    return [r for r in rs if d0 <= r["createTime"][:10] <= d1 and lo <= r["opp_rating"] < hi]

def show(lbl, rows):
    w = sum(1 for r in rows if r["outcome"] == "WIN"); l = sum(1 for r in rows if r["outcome"] == "LOSS")
    t = len(rows) - w - l
    print(f"   {lbl:26s} n={len(rows):4d} {w:3d}-{l:3d}-{t:2d} wr={(w+.5*t)/len(rows):.3f} "
          f"meanOpp={statistics.mean(r['opp_rating'] for r in rows):6.0f} eloPerf={elo_perf(rows):6.0f}")

def cmp2(la, A, lb, B, k=3000):
    if len(A) < 10 or len(B) < 10:
        print(f"   (too few: {len(A)},{len(B)})"); return
    show(la, A); show(lb, B)
    rnd = random.Random(77); d = []
    for _ in range(k):
        sa = [A[rnd.randrange(len(A))] for _ in A]; sb = [B[rnd.randrange(len(B))] for _ in B]
        d.append(elo_perf(sa) - elo_perf(sb))
    d.sort()
    print(f"   => {la} minus {lb} = {elo_perf(A)-elo_perf(B):+.0f} "
          f"[{d[int(.025*k)]:+.0f},{d[int(.975*k)]:+.0f}] P>0={sum(1 for x in d if x>0)/k:.3f}")

CASES = [
    ("EXP-1 readmarket: v29(layer ON) vs rm(stock), both live 08-14..08-18", "v29", "rm", "2026-08-14", "2026-08-18"),
    ("EXP-2 kaito_v43: v31(layer h1) vs v43c(stock), both submitted 08-24 10:42, live 08-24..08-26", "v31", "v43c", "2026-08-24", "2026-08-26"),
    ("EXP-2b kaito_v43: v32(layer h2) vs v43c(stock), both live 08-26..08-29", "v32", "v43c", "2026-08-26", "2026-08-29"),
    ("EXP-2c kaito_v43: v33(layer h3) vs v32(layer h2), both live 08-29", "v33", "v32", "2026-08-29", "2026-08-29"),
    ("EXP-3 Rayk C94: v27(layer, real) vs v26(ran as STOCK), both live 08-12..08-13", "v27", "v26", "2026-08-12", "2026-08-13"),
]
for title, a, b, d0, d1 in CASES:
    print("\n" + title)
    for lo, hi, nm in [(0, 9999, "all opponents"), (1200, 2400, "opp 1200-2400"), (1600, 2600, "opp 1600-2600")]:
        A = sel(a, d0, d1, lo, hi); B = sel(b, d0, d1, lo, hi)
        if len(A) < 10 or len(B) < 10: continue
        print(f"  [{nm}]")
        cmp2(a, A, b, B)
    # and again dropping each agent's own first live day (kills matchmaking warm-up inflation)
    A = sel(a, d0, d1, 0, 9999, True); B = sel(b, d0, d1, 0, 9999, True)
    if len(A) >= 10 and len(B) >= 10:
        print("  [excluding each agent's own first live day]")
        cmp2(a, A, b, B)
