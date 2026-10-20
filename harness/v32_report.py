import json, sys, csv, io, zipfile, math, random, statistics, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT

A = ROOT / "analysis"
z = zipfile.ZipFile(A / "kaggriculture.zip"); n = z.namelist()[0]
LB = {r["TeamName"]: float(r["Score"]) for r in csv.DictReader(io.TextIOWrapper(z.open(n), encoding="utf-8-sig"))}
print("leaderboard snapshot:", n, len(LB), "teams\n")

CLONE_T = 0.5
def sc(r): return 1.0 if r["outcome"] == "WIN" else (0.5 if r["outcome"] == "TIE" else 0.0)
def wlt(rows):
    w = sum(1 for r in rows if r["outcome"] == "WIN")
    l = sum(1 for r in rows if r["outcome"] == "LOSS")
    t = len(rows) - w - l
    return w, l, t, (sum(sc(r) for r in rows) / len(rows) if rows else float("nan"))
def elo_perf(rows):
    rows = [r for r in rows if r["opponent"] in LB]
    if not rows: return float("nan"), 0
    tgt = sum(sc(r) for r in rows)
    lo, hi = 0., 5000.
    for _ in range(200):
        mid = (lo + hi) / 2
        e = sum(1 / (1 + 10 ** ((LB[r["opponent"]] - mid) / 400)) for r in rows)
        if e < tgt: lo = mid
        else: hi = mid
    return (lo + hi) / 2, len(rows)
def boot(rows, iters=2000, seed=7):
    rows = [r for r in rows if r["opponent"] in LB]
    if len(rows) < 5: return (float("nan"), float("nan"))
    rnd = random.Random(seed); bs = []
    for _ in range(iters):
        s = [rows[rnd.randrange(len(rows))] for _ in rows]
        v, _ = elo_perf(s)
        bs.append(v)
    bs.sort()
    return bs[int(.025 * len(bs))], bs[int(.975 * len(bs))]

def load(stem):
    return json.load(open(A / f"{stem}.json", encoding="utf-8"))

def section(title): print("\n" + "=" * 78 + "\n" + title + "\n" + "=" * 78)

v32 = load(sys.argv[1] if len(sys.argv) > 1 else "autopsy_v32_live_clone")
try:
    v43 = load(sys.argv[2] if len(sys.argv) > 2 else "autopsy_v43b_live_clone")
except Exception:
    v43 = load("autopsy_v43_live_clone")

section("1. OVERALL + CHRONOLOGICAL")
w, l, t, s = wlt(v32)
print("v32 ALL: %d-%d-%d of %d   winrate(W/n)=%.3f   score(W+.5T)/n=%.3f" % (w, l, t, len(v32), w/len(v32), s))
e, ne = elo_perf(v32); lo, hi = boot(v32)
mo = statistics.mean(LB[r["opponent"]] for r in v32 if r["opponent"] in LB)
print("    elo-perf=%.0f (n matched %d)  boot95=[%.0f,%.0f]  meanOpp=%.0f" % (e, ne, lo, hi, mo))
print("\nby DAY (createTime):")
byday = collections.defaultdict(list)
for r in v32: byday[r["createTime"][:10]].append(r)
for d in sorted(byday):
    g = byday[d]; w, l, t, s = wlt(g); ep, _ = elo_perf(g)
    mo = statistics.mean(LB[r["opponent"]] for r in g if r["opponent"] in LB)
    nc = sum(1 for r in g if r["opp_match"] >= CLONE_T)
    print("  %s: n=%3d  %d-%d-%d  wr=%.3f score=%.3f  meanOpp=%.0f eloPerf=%.0f  clones=%d (%.2f)"
          % (d, len(g), w, l, t, w/len(g), s, mo, ep, nc, nc/len(g)))
print("\nby THIRD (chronological, oldest first):")
srt = sorted(v32, key=lambda r: r["createTime"])
k = len(srt) // 3
for i, g in enumerate([srt[:k], srt[k:2*k], srt[2*k:]]):
    w, l, t, s = wlt(g); ep, _ = elo_perf(g)
    mo = statistics.mean(LB[r["opponent"]] for r in g if r["opponent"] in LB)
    print("  T%d %s..%s: n=%d %d-%d-%d wr=%.3f score=%.3f meanOpp=%.0f eloPerf=%.0f"
          % (i+1, g[0]["createTime"][:16], g[-1]["createTime"][:16], len(g), w, l, t, w/len(g), s, mo, ep))

section("2. CLONE vs NON-CLONE (behavioural probe: opponent obs -> fresh stock v43, exact action match, first 120 steps)")
print("opp_match histogram:", sorted(collections.Counter(round(r["opp_match"], 1) for r in v32).items()))
print("our_match (sanity; v32==stock v43 before step 160):", sorted(collections.Counter(round(r["our_match"], 2) for r in v32).items()))
for label, rows in [("CLONE     (match>=0.5)", [r for r in v32 if r["opp_match"] >= CLONE_T]),
                    ("NON-CLONE (match< 0.5)", [r for r in v32 if r["opp_match"] < CLONE_T])]:
    if not rows: print("  " + label + ": none"); continue
    w, l, t, s = wlt(rows); ep, ne = elo_perf(rows); lo, hi = boot(rows)
    mo = statistics.mean(LB[r["opponent"]] for r in rows if r["opponent"] in LB)
    print("  %s: n=%3d  %d-%d-%d  winrate=%.3f  score=%.3f  meanOpp=%.0f  eloPerf=%.0f boot95=[%.0f,%.0f]"
          % (label, len(rows), w, l, t, w/len(rows), s, mo, ep, lo, hi))
print("\n  same split for the STOCK v43 CONTROL:")
for label, rows in [("CLONE    ", [r for r in v43 if r["opp_match"] >= CLONE_T]),
                    ("NON-CLONE", [r for r in v43 if r["opp_match"] < CLONE_T])]:
    if not rows: continue
    w, l, t, s = wlt(rows); ep, _ = elo_perf(rows)
    mo = statistics.mean(LB[r["opponent"]] for r in rows if r["opponent"] in LB)
    print("  %s: n=%3d  %d-%d-%d  winrate=%.3f  score=%.3f  meanOpp=%.0f  eloPerf=%.0f"
          % (label, len(rows), w, l, t, w/len(rows), s, mo, ep))

section("3. FIELD COMPOSITION")
for lab, rows in [("v32              ", v32), ("stock v43 control", v43)]:
    c = sum(1 for r in rows if r["opp_match"] >= CLONE_T)
    print("  %s: %d/%d = %.3f of games vs v43-family" % (lab, c, len(rows), c/len(rows)))
print("\n  v32 clone share by day:")
for d in sorted(byday):
    g = byday[d]; c = sum(1 for r in g if r["opp_match"] >= CLONE_T)
    print("    %s: %2d/%-3d = %.3f" % (d, c, len(g), c/len(g)))
print("\n  v43 control clone share by day:")
bd43 = collections.defaultdict(list)
for r in v43: bd43[r["createTime"][:10]].append(r)
for d in sorted(bd43):
    g = bd43[d]; c = sum(1 for r in g if r["opp_match"] >= CLONE_T)
    print("    %s: %2d/%-3d = %.3f" % (d, c, len(g), c/len(g)))

section("4. NON-CLONE LOSSES / TIES (flippable = margin > -1000)")
nl = [r for r in v32 if r["opp_match"] < CLONE_T and r["outcome"] == "LOSS"]
nt = [r for r in v32 if r["opp_match"] < CLONE_T and r["outcome"] == "TIE"]
close = [r for r in nl if abs(r["margin"]) < 1000]
print("  non-clone losses: %d;  within 1000 coins: %d;  non-clone ties: %d" % (len(nl), len(close), len(nt)))
print("  CLOSEST non-clone losses:")
for r in sorted(nl, key=lambda x: -x["margin"])[:22]:
    print("    %9.0f  ep=%s seat=%d vs %-26s lb=%7.1f match=%.2f"
          % (r["margin"], r["episode"], r["seat"], r["opponent"][:26], LB.get(r["opponent"], float("nan")), r["opp_match"]))
print("  BIGGEST non-clone losses:")
for r in sorted(nl, key=lambda x: x["margin"])[:12]:
    print("    %9.0f  ep=%s seat=%d vs %-26s lb=%7.1f"
          % (r["margin"], r["episode"], r["seat"], r["opponent"][:26], LB.get(r["opponent"], float("nan"))))
if nt:
    print("  non-clone TIES:")
    for r in nt:
        print("    ep=%s vs %-26s lb=%7.1f coins=%.0f" % (r["episode"], r["opponent"][:26], LB.get(r["opponent"], float("nan")), r["our"]))
cl = [r for r in v32 if r["opp_match"] >= CLONE_T and r["outcome"] != "WIN"]
print("\n  CLONE non-wins (%d):" % len(cl))
for r in sorted(cl, key=lambda x: -x["margin"]):
    print("    %-5s %9.0f  ep=%s seat=%d vs %-26s lb=%7.1f"
          % (r["outcome"], r["margin"], r["episode"], r["seat"], r["opponent"][:26], LB.get(r["opponent"], float("nan"))))

section("5. OPPONENT TABLE / STRENGTH BANDS")
bands = [(0, 1500), (1500, 2000), (2000, 2300), (2300, 2600), (2600, 3200)]
for lo_, hi_ in bands:
    for lab, thr in [("clone", True), ("non-clone", False)]:
        g = [r for r in v32 if r["opponent"] in LB and lo_ <= LB[r["opponent"]] < hi_ and ((r["opp_match"] >= CLONE_T) == thr)]
        if not g: continue
        w, l, t, s = wlt(g)
        print("  opp %4d-%4d %-10s: n=%3d  %d-%d-%d  wr=%.3f score=%.3f" % (lo_, hi_, lab, len(g), w, l, t, w/len(g), s))
print("\n  per-opponent (>=2 games), sorted by lb rating desc:")
by = collections.defaultdict(list)
for r in v32: by[r["opponent"]].append(r)
for opp, g in sorted(by.items(), key=lambda kv: -LB.get(kv[0], 0)):
    if len(g) < 2: continue
    w, l, t, s = wlt(g)
    cm = statistics.mean(r["opp_match"] for r in g)
    print("    %7.1f %-28s n=%2d %d-%d-%d wr=%.2f clone=%.2f" % (LB.get(opp, float("nan")), opp[:28], len(g), w, l, t, w/len(g), cm))
