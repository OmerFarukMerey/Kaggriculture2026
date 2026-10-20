"""Cluster the live field by the opponent's OWN recorded action tape (chassis-free),
then attach each cluster to a known chassis family where one matches."""
import json, sys, collections, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS

recs = json.load(open(ROOT / "analysis" / "field_labelled.json", encoding="utf-8"))
K = int(sys.argv[1]) if len(sys.argv) > 1 else 60

FAM = {"kaito_v43": "kaito-v43 lineage", "kaito_v48": "kaito-v43 lineage",
       "v31": "kaito-v43 lineage", "v32": "kaito-v43 lineage", "v33": "kaito-v43 lineage",
       "readmarket": "readmarket/tetsu family", "tetsu": "readmarket/tetsu family",
       "tetsu_v2": "readmarket/tetsu family", "boatlee_v20": "readmarket/tetsu family",
       "frontier_moon": "readmarket/tetsu family", "breaking_tie": "readmarket/tetsu family",
       "salem3000": "salem/rc5 family", "rc5": "salem/rc5 family", "frontier_soil": "salem/rc5 family",
       "kaito_v27": "kaito_v27/boatlee16", "boatlee_v16": "kaito_v27/boatlee16",
       "rayk_c94": "rayk", "rayk_c92": "rayk",
       "opp_bohannn": "bohannn route", "opp_yy": "yy route", "public_v211": "public_v211"}

def tape(ep, seat, k):
    rep = json.load(open(REPLAYS / f"episode-{ep}-replay.json", encoding="utf-8"))
    return [json.dumps(rep["steps"][t + 1][seat].get("action"), sort_keys=True)
            for t in range(min(k, len(rep["steps"]) - 1))]

for r in recs:
    r["h"] = hashlib.md5("|".join(tape(r["episode"], 1 - r["seat"], K)).encode()).hexdigest()[:8]

def famof(rs):
    """Best known family for a cluster, else NEW/private."""
    best, bv = None, 0.0
    for r in rs:
        for c, v in r["m"].items():
            if v is not None and v > bv:
                best, bv = c, v
    return (FAM.get(best, best) if bv >= 0.85 else "NEW / private (no file matches)"), bv

def report(rows, title):
    g = collections.defaultdict(list)
    for r in rows:
        g[r["h"]].append(r)
    print(f"\n########## {title}   n={len(rows)} episodes, {len(g)} distinct {K}-step tapes ##########")
    fam = collections.Counter(); famw = collections.Counter(); famt = collections.Counter()
    print(f"  {'tape':9s} {'eps':>4s} {'teams':>6s} {'share':>7s}  {'ourW-L-T':>10s}  {'lbrange':>12s}  family (best chassis match)")
    for h, rs in sorted(g.items(), key=lambda kv: -len(kv[1])):
        f, bv = famof(rs)
        w = sum(1 for x in rs if x["outcome"] == "WIN"); t = sum(1 for x in rs if x["outcome"] == "TIE")
        fam[f] += len(rs); famw[f] += w; famt[f] += t
        if len(rs) < 3: continue
        lbs = [x["lb"] for x in rs if x["lb"]]
        print(f"  {h} {len(rs):4d} {len(set(x['opponent'] for x in rs)):6d} {len(rs)/len(rows):7.3f}  "
              f"{w:2d}-{len(rs)-w-t:2d}-{t:1d}   {min(lbs,default=0):5.0f}-{max(lbs,default=0):5.0f}  {f} ({bv:.3f})")
    print(f"  ... plus {sum(1 for rs in g.values() if len(rs)<3)} tapes seen 1-2 times")
    print(f"\n  --- FAMILY ROLLUP ({title}) ---")
    for f, n in fam.most_common():
        w, t = famw[f], famt[f]
        print(f"    {f:34s} {n:4d}  {n/len(rows):.3f}   our record {w}-{n-w-t}-{t}  wr={(w+0.5*t)/n:.3f}")
    return fam

days = sorted(set(r["day"] for r in recs))
report([r for r in recs if r["day"] >= "2026-08-29"], "LIVE FIELD 08-29..08-30 (most recent)")
report([r for r in recs if r["day"] == "2026-08-30"], "LIVE FIELD 08-30 only")
for d in days:
    rows = [r for r in recs if r["day"] == d]
    g = collections.defaultdict(list)
    for r in rows: g[r["h"]].append(r)
    fam = collections.Counter()
    for h, rs in g.items():
        f, _ = famof(rs); fam[f] += len(rs)
    print(f"\n{d} n={len(rows):3d}: " + "  ".join(f"{k}={v}({v/len(rows):.2f})" for k, v in fam.most_common()))

print("\n\n########## BY OPPONENT RATING BAND (recent 08-29..08-30) ##########")
rec = [r for r in recs if r["day"] >= "2026-08-29" and r["lb"] is not None]
for lo, hi in [(0, 2000), (2000, 2200), (2200, 2400), (2400, 2600), (2600, 3200)]:
    rows = [r for r in rec if lo <= r["lb"] < hi]
    if not rows: continue
    g = collections.defaultdict(list)
    for r in rows: g[r["h"]].append(r)
    fam = collections.Counter(); famw = collections.Counter(); famt = collections.Counter()
    for h, rs in g.items():
        f, _ = famof(rs); fam[f] += len(rs)
        famw[f] += sum(1 for x in rs if x["outcome"] == "WIN"); famt[f] += sum(1 for x in rs if x["outcome"] == "TIE")
    w = sum(1 for r in rows if r["outcome"] == "WIN"); t = sum(1 for r in rows if r["outcome"] == "TIE")
    print(f"\n  opp {lo}-{hi}: n={len(rows)}  our {w}-{len(rows)-w-t}-{t} wr={(w+0.5*t)/len(rows):.3f}")
    for f, n in fam.most_common():
        print(f"     {f:34s} {n:3d} {n/len(rows):.3f}  our {famw[f]}-{n-famw[f]-famt[f]}-{famt[f]}")
