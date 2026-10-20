"""Aggregate the multi-chassis field probe into composition tables."""
import json, sys, collections, csv, io, zipfile, statistics
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT

TH = float(sys.argv[1]) if len(sys.argv) > 1 else 0.85
recs = []
for p in sorted((ROOT / "analysis" / "fp").glob("shard*.json")):
    recs += json.load(open(p, encoding="utf-8"))
seen = set(); recs = [r for r in recs if not (r["episode"] in seen or seen.add(r["episode"]))]
recs.sort(key=lambda r: r["createTime"])

z = zipfile.ZipFile(ROOT / "analysis" / "lb_new" / "kaggriculture.zip")
nm = z.namelist()[0]
lb = {r["TeamName"]: float(r["Score"]) for r in csv.DictReader(io.TextIOWrapper(z.open(nm), encoding="utf-8-sig"))}
print(f"leaderboard: {nm}  teams={len(lb)}")
print(f"episodes probed: {len(recs)}  steps compared per episode: "
      f"median={statistics.median(r['n'] for r in recs)} min={min(r['n'] for r in recs)}")

V43FAM = ["kaito_v43", "kaito_v48", "v31", "v32", "v33"]

def label(r):
    m = {k: v for k, v in r["m"].items() if v is not None}
    best = max(m.values())
    if best < TH:
        return "UNMATCHED", best
    hits = sorted([k for k, v in m.items() if v >= TH], key=lambda k: -m[k])
    # v43 lineage: v43/v48/our layered subs are byte-identical for ~130 steps.
    fam = [k for k in hits if k in V43FAM]
    if fam and len(fam) == len(hits):
        exact = [k for k in fam if m[k] >= 0.999]
        if "kaito_v43" in exact:
            return "kaito_v43", best
        if exact:
            return exact[0], best
        return max(fam, key=lambda k: m[k]), best
    return hits[0], best

for r in recs:
    r["label"], r["best"] = label(r)
    r["day"] = r["createTime"][:10]
    r["lb"] = lb.get(r["opponent"])

json.dump(recs, open(ROOT / "analysis" / "field_labelled.json", "w"), indent=0)

def table(rows, title):
    c = collections.Counter(x["label"] for x in rows)
    n = len(rows)
    print(f"\n### {title}  n={n}")
    for k, v in c.most_common():
        print(f"   {k:16s} {v:4d}  {v/max(n,1):.3f}")

days = sorted(set(r["day"] for r in recs))
labels = [k for k, _ in collections.Counter(r["label"] for r in recs).most_common()]
print("\n=== PER-CHASSIS SHARE OF THE FIELD BY DAY (count / share) ===")
hdr = f"{'label':16s}" + "".join(f"{d[5:]:>14s}" for d in days) + f"{'TOTAL':>14s}"
print(hdr)
for L in labels:
    line = f"{L:16s}"
    for d in days:
        g = [r for r in recs if r["day"] == d]
        c = sum(1 for r in g if r["label"] == L)
        line += f"{c:6d}/{c/max(len(g),1):6.3f}"
    c = sum(1 for r in recs if r["label"] == L)
    line += f"{c:6d}/{c/len(recs):6.3f}"
    print(line)
line = f"{'-- n --':16s}" + "".join(f"{len([r for r in recs if r['day']==d]):13d} " for d in days) + f"{len(recs):13d} "
print(line)

print("\n=== BY OPPONENT RATING BAND (current leaderboard) ===")
known = [r for r in recs if r["lb"] is not None]
print(f"opponents matched to leaderboard: {len(known)}/{len(recs)}")
bands = [(0, 1500), (1500, 2000), (2000, 2200), (2200, 2400), (2400, 2600), (2600, 3200)]
hdr = f"{'label':16s}" + "".join(f"{f'{lo}-{hi}':>14s}" for lo, hi in bands)
print(hdr)
for L in labels:
    line = f"{L:16s}"
    for lo, hi in bands:
        g = [r for r in known if lo <= r["lb"] < hi]
        c = sum(1 for r in g if r["label"] == L)
        line += f"{c:6d}/{c/max(len(g),1):6.3f}"
    print(line)
print(f"{'-- n --':16s}" + "".join(f"{len([r for r in known if lo<=r['lb']<hi]):13d} " for lo, hi in bands))

print("\n=== LAST 2 DAYS ONLY (08-29..08-30) ===")
recent = [r for r in recs if r["day"] >= "2026-08-29"]
table(recent, "all recent")
table([r for r in recent if r["lb"] is not None and r["lb"] >= 2400], "recent, opp 2400+")
table([r for r in recent if r["lb"] is not None and r["lb"] >= 2600], "recent, opp 2600+")

print("\n=== UNMATCHED best-match distribution (are they near-misses?) ===")
um = [r for r in recs if r["label"] == "UNMATCHED"]
print(collections.Counter(round(r["best"], 1) for r in um).most_common())
print("top argmax chassis among unmatched:",
      collections.Counter(max(r["m"], key=lambda k: (r["m"][k] is not None, r["m"][k] or -1)) for r in um).most_common(6))

print("\n=== record vs each label (W-L-T, winrate) ===")
for L in labels:
    g = [r for r in recs if r["label"] == L]
    w = sum(1 for r in g if r["outcome"] == "WIN"); t = sum(1 for r in g if r["outcome"] == "TIE")
    gr = [r for r in g if r["day"] >= "2026-08-29"]
    wr2 = ""
    if gr:
        w2 = sum(1 for r in gr if r["outcome"] == "WIN"); t2 = sum(1 for r in gr if r["outcome"] == "TIE")
        wr2 = f"   recent {w2}-{len(gr)-w2-t2}-{t2} wr={(w2+0.5*t2)/len(gr):.3f}"
    print(f"   {L:16s} n={len(g):4d}  {w}-{len(g)-w-t}-{t}  wr={(w+0.5*t)/len(g):.3f}{wr2}")

print("\n=== most frequent UNMATCHED opponents (candidate new tapes) ===")
c = collections.Counter(r["opponent"] for r in um)
for o, n in c.most_common(15):
    g = [r for r in um if r["opponent"] == o]
    print(f"   {o[:30]:32s} lb={lb.get(o,float('nan')):7.1f} n={n:3d} bestmatch={statistics.mean(x['best'] for x in g):.2f} "
          f"eps={[x['episode'] for x in g][:4]}")
