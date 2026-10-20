"""Era / field-strength decomposition across all submissions."""
import json, sys, csv, io, zipfile, math, statistics, collections, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT
sys.path.insert(0, str(ROOT / "harness"))
from adjrate import LB, LASTSUB, ORDER, POSTED, load, elo_perf, boot, sc, frozen

def wlt(rows):
    w = sum(1 for r in rows if r["outcome"] == "WIN")
    l = sum(1 for r in rows if r["outcome"] == "LOSS")
    return w, l, len(rows) - w - l

print("=== FIELD STRENGTH BY CALENDAR DAY (opponents we actually met, today's ratings) ===")
byday = collections.defaultdict(list)
for tag in ORDER:
    for r in load(tag):
        if r["opp_rating"] is None: continue
        byday[r["createTime"][:10]].append(r)
for d in sorted(byday):
    g = byday[d]
    rat = [r["opp_rating"] for r in g]
    w, l, t = wlt(g)
    tags = collections.Counter(r["tag"] for r in g)
    print(f"{d} n={len(g):4d} meanOpp={statistics.mean(rat):6.0f} medOpp={statistics.median(rat):6.0f} "
          f"p90={sorted(rat)[int(.9*len(rat))]:6.0f} frac2600+={sum(1 for x in rat if x>=2600)/len(g):.3f} "
          f"our {w}-{l}-{t} wr={(w+.5*t)/len(g):.3f}  subs={dict(tags)}")

print("\n=== WARM-UP: elo-perf over first 60 episodes vs the rest ===")
for tag in ORDER:
    rows = [r for r in load(tag) if r["opp_rating"] is not None]
    if len(rows) < 40: continue
    rows.sort(key=lambda r: r["createTime"])
    a, b = rows[:60], rows[60:]
    pa = elo_perf(a); wa = wlt(a)
    s = f"{tag:6s} first{len(a):3d}: meanOpp={statistics.mean(r['opp_rating'] for r in a):5.0f} perf={pa:5.0f} {wa[0]}-{wa[1]}-{wa[2]}"
    if len(b) >= 20:
        pb = elo_perf(b); wb = wlt(b)
        s += f" | rest{len(b):4d}: meanOpp={statistics.mean(r['opp_rating'] for r in b):5.0f} perf={pb:5.0f} {wb[0]}-{wb[1]}-{wb[2]}"
    print(s)

print("\n=== THE 2600+ BAND (the ceiling) ===")
for tag in ORDER:
    rows = [r for r in load(tag) if r["opp_rating"] is not None and r["opp_rating"] >= 2600]
    all_ = [r for r in load(tag) if r["opp_rating"] is not None]
    if not all_: continue
    w, l, t = wlt(rows)
    print(f"{tag:6s} vs2600+: n={len(rows):3d} ({len(rows)/len(all_):.2f} of field) {w}-{l}-{t} "
          f"wr={(w+.5*t)/max(len(rows),1):.3f}")

print("\n=== VARIANCE DECOMPOSITION of posted rating ===")
xs, ys, zs, tg = [], [], [], []
for tag in ORDER:
    rows = [r for r in load(tag) if r["opp_rating"] is not None]
    if len(rows) < 10: continue
    w, l, t = wlt(rows)
    s = (w + .5 * t) / len(rows)
    s = min(max(s, 1e-3), 1 - 1e-3)
    mo = statistics.mean(r["opp_rating"] for r in rows)
    xs.append(mo); ys.append(400 * math.log10(s / (1 - s))); zs.append(POSTED[tag]); tg.append(tag)
print(" tag    posted  meanOpp  400logit(wr)  meanOpp+logit")
for a, b, c, d in zip(tg, zs, xs, ys):
    print(f" {a:6s} {b:7.1f} {c:8.0f} {d:13.0f} {c+d:14.0f}")
vp = statistics.pvariance(zs); vo = statistics.pvariance(xs); vl = statistics.pvariance(ys)
cov = statistics.mean([(o - statistics.mean(xs)) * (l - statistics.mean(ys)) for o, l in zip(xs, ys)])
print(f"\n sd(posted)={vp**.5:.0f}  sd(meanOpp)={vo**.5:.0f}  sd(400logit wr)={vl**.5:.0f}  cov={cov:+.0f}")
print(f" var(meanOpp+logit)={vo+vl+2*cov:.0f} -> sd={((vo+vl+2*cov))**.5:.0f}")
# correlation of posted with each part
def corr(a, b):
    ma, mb = statistics.mean(a), statistics.mean(b)
    return sum((x-ma)*(y-mb) for x, y in zip(a, b)) / math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))
print(f" corr(posted, meanOpp)={corr(zs,xs):+.3f}   corr(posted, 400logit wr)={corr(zs,ys):+.3f}")
perfs = []
for tag in tg:
    rows = [r for r in load(tag) if r["opp_rating"] is not None]
    perfs.append(elo_perf(rows))
print(f" sd(eloPerf across submissions)={statistics.pvariance(perfs)**.5:.0f}  corr(posted, eloPerf)={corr(zs,perfs):+.3f}")
