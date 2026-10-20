"""Table of our record vs each opponent, bucketed by CURRENT leaderboard rating."""
import json, zipfile, csv, io, sys, statistics, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT

z = zipfile.ZipFile(ROOT/"analysis"/"kaggriculture.zip"); nm = z.namelist()[0]
lb = {r["TeamName"]: float(r["Score"]) for r in csv.DictReader(io.TextIOWrapper(z.open(nm), encoding="utf-8-sig"))}
print("leaderboard snapshot:", nm, " teams:", len(lb))

rows = []
for stem, tag in [("autopsy_v32_live","v32"),("autopsy_v33_live","v33")]:
    p = ROOT/"analysis"/f"{stem}.json"
    if not p.exists(): print("missing", p); continue
    for r in json.load(open(p, encoding="utf-8")):
        r["bot"] = tag; rows.append(r)
seen=set(); uniq=[]
for r in rows:
    if r["episode"] in seen: continue
    seen.add(r["episode"]); uniq.append(r)
rows = uniq
known = [r for r in rows if r["opponent"] in lb]
print(f"episodes total={len(rows)} matched-to-lb={len(known)}")

def rec(g):
    w=sum(1 for r in g if r["outcome"]=="WIN"); l=sum(1 for r in g if r["outcome"]=="LOSS")
    return w,l,len(g)-w-l

for tag in ("v32","v33","ALL"):
    g0=[r for r in known if tag=="ALL" or r["bot"]==tag]
    print(f"\n=== {tag}  n={len(g0)} ===")
    for lo,hi in [(0,1500),(1500,2000),(2000,2200),(2200,2400),(2400,2600),(2600,3200)]:
        g=[r for r in g0 if lo<=lb[r["opponent"]]<hi]
        if not g: continue
        w,l,t=rec(g)
        print(f"  opp {lo}-{hi}: n={len(g):3d} {w}-{l}-{t} wr={(w+0.5*t)/len(g):.3f} "
              f"meanMargin={statistics.mean(r['margin'] for r in g):+8.0f} "
              f"medMargin={statistics.median(r['margin'] for r in g):+8.0f}")

hi=[r for r in known if lb[r["opponent"]]>=2600]
w,l,t=rec(hi)
print(f"\n### 2600+ combined: {w}-{l}-{t} of {len(hi)}  wr={(w+0.5*t)/len(hi):.3f}")
c=collections.Counter(r["opponent"] for r in hi)
print(f"{'opponent':34s} {'lb':>7s} {'n':>3s}  W-L-T   margins")
for o,n in c.most_common():
    g=[r for r in hi if r["opponent"]==o]; w,l,t=rec(g)
    print(f"{o[:33]:34s} {lb[o]:7.1f} {n:3d}  {w}-{l}-{t}  {sorted(int(r['margin']) for r in g)}")
json.dump([{k:v for k,v in r.items() if k!='opp_fp'} for r in hi],
          open(ROOT/"analysis"/"top_band_eps.json","w"), indent=1)
print("\nwrote analysis/top_band_eps.json")
