"""Master phase-1 report: per-submission opponent-adjusted performance, era effects,
controlled experiments, and the variance decomposition."""
import sys, json, math, statistics, random, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT
from adjrate import load, elo_perf, boot, POSTED, ORDER, LB, SNAP

def rec(rows):
    w = sum(1 for r in rows if r["outcome"] == "WIN"); l = sum(1 for r in rows if r["outcome"] == "LOSS")
    return w, l, len(rows) - w - l

def block(tag, rows):
    kn = [r for r in rows if r["opp_rating"] is not None]
    w, l, t = rec(kn); n = len(kn)
    wr = (w + .5 * t) / n
    mo = statistics.mean(r["opp_rating"] for r in kn)
    e = elo_perf(kn); b = boot(kn, 3000)
    d0 = min(r["createTime"] for r in kn)[:10]; d1 = max(r["createTime"] for r in kn)[:10]
    big = sum(1 for r in kn if abs(r["margin"]) > 10000) / n
    return dict(tag=tag, n=n, nraw=len(rows), w=w, l=l, t=t, wr=wr, meanOpp=mo, perf=e,
                lo=b[75], hi=b[2924], posted=POSTED[tag], d0=d0, d1=d1, big=big)

res = {}
for tag in ORDER:
    rows = load(tag)
    if len(rows) >= 8:
        res[tag] = block(tag, rows)

print(f"LEADERBOARD SNAPSHOT {SNAP} ({len(LB)} teams)\n")
print("PER-SUBMISSION, ALL PUBLIC COMPLETED EPISODES, opponent = TODAY's leaderboard rating")
print(f"{'sub':6s} {'dates':>21s} {'n':>4s} {'W-L-T':>12s} {'winrate':>8s} {'meanOpp':>8s} "
      f"{'eloPerf':>8s} {'boot95':>14s} {'posted':>8s} {'gap':>6s} {'>10k':>5s}")
for tag in ORDER:
    if tag not in res: continue
    r = res[tag]
    print(f"{r['tag']:6s} {r['d0'][5:]+'..'+r['d1'][5:]:>21s} {r['n']:4d} "
          f"{f'{r['w']}-{r['l']}-{r['t']}':>12s} {r['wr']:8.3f} {r['meanOpp']:8.0f} {r['perf']:8.0f} "
          f"{f'[{r['lo']:.0f},{r['hi']:.0f}]':>14s} {r['posted']:8.1f} {r['posted']-r['perf']:+6.0f} {r['big']:5.2f}")

print("\nRANK BY POSTED           RANK BY OPPONENT-ADJUSTED eloPerf")
a = sorted(res.values(), key=lambda r: -r["posted"])
b_ = sorted(res.values(), key=lambda r: -r["perf"])
for i, (x, y) in enumerate(zip(a, b_), 1):
    print(f"{i:2d}. {x['tag']:6s} {x['posted']:7.1f}      {i:2d}. {y['tag']:6s} {y['perf']:7.0f} [{y['lo']:.0f},{y['hi']:.0f}]")

def diff(la, A, lb, B, k=3000, seed=21):
    rnd = random.Random(seed); d = []
    for _ in range(k):
        sa = [A[rnd.randrange(len(A))] for _ in A]; sb = [B[rnd.randrange(len(B))] for _ in B]
        d.append(elo_perf(sa) - elo_perf(sb))
    d.sort()
    print(f"  {la} minus {lb}: {elo_perf(A)-elo_perf(B):+.0f}  boot95=[{d[int(.025*k)]:+.0f},{d[int(.975*k)]:+.0f}]  "
          f"P({la}>{lb})={sum(1 for x in d if x>0)/k:.3f}   (n {len(A)} vs {len(B)})")

def rowsof(tags, lo=None, hi=None):
    out = []
    for t in tags.split(","):
        out += [r for r in load(t) if r["opp_rating"] is not None]
    if lo: out = [r for r in out if lo <= r["createTime"][:10] <= hi]
    return out

print("\n=== CONTROLLED EXPERIMENTS ===")
print("EXP-1  read-the-market stock  vs  v29 = same file, one line flipped (_PREEMPT_ENABLED)")
diff("v29", rowsof("v29"), "rm", rowsof("rm"))
print("  date-matched window 2026-08-14..2026-08-18 (both live, same field):")
A = rowsof("v29", "2026-08-14", "2026-08-18"); B = rowsof("rm", "2026-08-14", "2026-08-18")
if len(A) >= 10 and len(B) >= 10: diff("v29", A, "rm", B)
print("EXP-2  kaito_v43 stock  vs  v32 = v43 + mirror sell pull-forward (submitted same minute-ish)")
diff("v32", rowsof("v32"), "v43c", rowsof("v43c"))
print("  date-matched window 2026-08-26..2026-08-29:")
A = rowsof("v32", "2026-08-26", "2026-08-29"); B = rowsof("v43c", "2026-08-26", "2026-08-29")
if len(A) >= 10 and len(B) >= 10: diff("v32", A, "v43c", B)
print("EXP-2b v31 (horizon 1) and v33 (horizon 3) against the same stock control")
diff("v31", rowsof("v31"), "v43c", rowsof("v43c"))
diff("v33", rowsof("v33"), "v43c", rowsof("v43c"))
print("EXP-3  Rayk C94 running as STOCK (loader bug: v24,v25,v26) vs C94+our layer (v27,v28)")
diff("C94+layer", rowsof("v27,v28"), "C94stock", rowsof("v24,v25,v26"))
print("  v26 vs v27, the two that ran concurrently 2026-08-12..2026-08-13:")
A = rowsof("v27", "2026-08-12", "2026-08-13"); B = rowsof("v26", "2026-08-12", "2026-08-13")
if len(A) >= 10 and len(B) >= 10: diff("v27", A, "v26", B)

print("\n=== THE 2600+ CEILING (today's ratings) ===")
for tag in ORDER:
    if tag not in res: continue
    g = [r for r in load(tag) if r["opp_rating"] is not None and r["opp_rating"] >= 2600]
    all_ = [r for r in load(tag) if r["opp_rating"] is not None]
    w, l, t = rec(g)
    print(f"{tag:6s} n={len(g):3d} ({len(g)/len(all_):.2f} of field)  {w}-{l}-{t}  "
          f"wr={(w+.5*t)/max(len(g),1):.3f}")

print("\n=== FIELD STRENGTH BY DAY ===")
byday = collections.defaultdict(list)
for tag in ORDER:
    for r in load(tag):
        if r["opp_rating"] is not None: byday[r["createTime"][:10]].append(r)
for d in sorted(byday):
    g = byday[d]; rt = [r["opp_rating"] for r in g]; w, l, t = rec(g)
    print(f"{d} n={len(g):4d} meanOppToday={statistics.mean(rt):6.0f} frac>=2600={sum(1 for x in rt if x>=2600)/len(g):.3f} "
          f"our {w}-{l}-{t} wr={(w+.5*t)/len(g):.3f} frac|margin|>10k={sum(1 for r in g if abs(r['margin'])>10000)/len(g):.2f}")

print("\n=== VARIANCE DECOMPOSITION (posted = meanOpp_at_match + 400*logit(wr)) ===")
tg = [t for t in ORDER if t in res]
post = [res[t]["posted"] for t in tg]
mo = [res[t]["meanOpp"] for t in tg]
lg = []
for t in tg:
    p = min(max(res[t]["wr"], 1e-3), 1 - 1e-3); lg.append(400 * math.log10(p / (1 - p)))
perf = [res[t]["perf"] for t in tg]
implied = [p - g for p, g in zip(post, lg)]
drift = [m - i for m, i in zip(mo, implied)]
print(f"{'sub':6s} {'posted':>8s} {'400logit(wr)':>13s} {'impliedOpp@match':>17s} {'meanOppToday':>13s} {'drift':>7s}")
for t, p, g, i, m, d in zip(tg, post, lg, implied, mo, drift):
    print(f"{t:6s} {p:8.1f} {g:13.0f} {i:17.0f} {m:13.0f} {d:+7.0f}")
sd = lambda x: statistics.pstdev(x)
print(f"\n sd(posted)={sd(post):.0f}   sd(400logit winrate)={sd(lg):.0f}   sd(impliedOpp@match)={sd(implied):.0f}")
print(f" sd(eloPerf vs today's ratings)={sd(perf):.0f}   sd(meanOppToday)={sd(mo):.0f}")
def corr(x, y):
    mx, my = statistics.mean(x), statistics.mean(y)
    return sum((a-mx)*(b-my) for a, b in zip(x, y))/math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
print(f" corr(posted, 400logit wr)={corr(post,lg):+.3f}   corr(posted, impliedOpp@match)={corr(post,implied):+.3f}")
print(f" corr(posted, eloPerf)={corr(post,perf):+.3f}")
va = statistics.pvariance(implied); vb = statistics.pvariance(lg)
cv = statistics.mean([(a-statistics.mean(implied))*(b-statistics.mean(lg)) for a, b in zip(implied, lg)])
print(f" var share of posted spread: opponent-strength-at-match {va/(va+vb+2*cv):.1%}, "
      f"own win rate {vb/(va+vb+2*cv):.1%}, covariance {2*cv/(va+vb+2*cv):+.1%}")
json.dump(res, open(ROOT/"analysis"/"phase1_master.json", "w"), indent=1, default=str)
print("\nwrote analysis/phase1_master.json")
