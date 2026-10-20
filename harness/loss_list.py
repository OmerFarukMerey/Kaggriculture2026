import json,sys,zipfile,csv,io
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from paths import ROOT
z=zipfile.ZipFile(ROOT/"analysis"/"kaggriculture.zip"); nm=z.namelist()[0]
lb={r["TeamName"]:float(r["Score"]) for r in csv.DictReader(io.TextIOWrapper(z.open(nm),encoding="utf-8-sig"))}
for stem,label in [("v31_live","v31"),("v43_live","v43stock")]:
    ap=json.load(open(ROOT/"analysis"/f"autopsy_{stem}.json",encoding="utf-8"))
    g={r["episode"]:r for r in json.load(open(ROOT/"analysis"/f"gate_autopsy_{stem}.json",encoding="utf-8"))}
    L=[r for r in ap if r["outcome"]!="WIN"]
    print(f"\n=== {label}: {len(L)} non-wins of {len(ap)} ===")
    for r in sorted(L,key=lambda x:-x["margin"]):
        gg=g.get(r["episode"],{})
        mir = "MIRROR" if gg.get("prefix_agree",0)>=124 else ("near" if gg.get("prefix_agree",0)>=60 else "-")
        print(f"  {r['outcome']:4s} m={r['margin']:+8.0f} seat={r['seat']} opp={r['opponent']!r:38s} "
              f"oppRating={lb.get(r['opponent'],float('nan')):.0f} {mir:6s} gate_frac={gg.get('gate_frac',0):.2f} ep={r['episode']}")
    for thr in (500,1000,2000,3000,5000):
        k=sum(1 for r in L if abs(r["margin"])<=thr)
        print(f"   non-wins within {thr}: {k}")
    W=[r for r in ap if r["outcome"]=="WIN"]
    for thr in (500,1000,2000):
        print(f"   WINS within {thr} (at risk): {sum(1 for r in W if r['margin']<=thr)}")
