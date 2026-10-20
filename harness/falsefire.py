import json,sys,zipfile,csv,io,statistics,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from paths import ROOT
z=zipfile.ZipFile(ROOT/"analysis"/"kaggriculture.zip"); nm=z.namelist()[0]
lb={r["TeamName"]:float(r["Score"]) for r in csv.DictReader(io.TextIOWrapper(z.open(nm),encoding="utf-8-sig"))}
def sc(r): return 1.0 if r["outcome"]=="WIN" else (0.5 if r["outcome"]=="TIE" else 0.0)
def eloperf(rows):
    rows=[r for r in rows if r["opponent"] in lb]
    if not rows: return float('nan')
    tgt=sum(sc(r) for r in rows); lo,hi=0.,6000.
    for _ in range(120):
        mid=(lo+hi)/2
        e=sum(1/(1+10**((lb[r["opponent"]]-mid)/400)) for r in rows)
        if e<tgt: lo=mid
        else: hi=mid
    return (lo+hi)/2
for stem,label in [("v31_live","v31"),("v43_live","v43stock")]:
    ap={r["episode"]:r for r in json.load(open(ROOT/"analysis"/f"autopsy_{stem}.json",encoding="utf-8"))}
    g=json.load(open(ROOT/"analysis"/f"gate_autopsy_{stem}.json",encoding="utf-8"))
    for r in g: r["outcome"]=ap[r["episode"]]["outcome"]
    nc=[r for r in g if r["prefix_agree"]<124]
    ff=[r for r in nc if r["gate_steps"]>0]; nf=[r for r in nc if r["gate_steps"]==0]
    mir=[r for r in g if r["prefix_agree"]>=124]
    print(f"{label}:")
    for n,x in [("MIRROR",mir),("nonclone gate-open",ff),("nonclone gate-never",nf)]:
        rs=[lb[r['opponent']] for r in x if r['opponent'] in lb]
        print(f"   {n:22s} n={len(x):3d} score={sum(sc(r) for r in x)/len(x):.3f} meanOpp={statistics.mean(rs):.0f} eloPerf={eloperf(x):.0f}")

# diff-in-diff bootstrap: (v31 gate-open minus gate-never) minus (v43 gate-open minus gate-never)
import random
cells={}
for stem,label in [("v31_live","v31"),("v43_live","v43stock")]:
    ap={r["episode"]:r for r in json.load(open(ROOT/"analysis"/f"autopsy_{stem}.json",encoding="utf-8"))}
    g=json.load(open(ROOT/"analysis"/f"gate_autopsy_{stem}.json",encoding="utf-8"))
    for r in g: r["outcome"]=ap[r["episode"]]["outcome"]
    nc=[r for r in g if r["prefix_agree"]<124 and r["opponent"] in lb]
    cells[label]=([r for r in nc if r["gate_steps"]>0],[r for r in nc if r["gate_steps"]==0])
rnd=random.Random(3); d=[]
for _ in range(3000):
    vals=[]
    for label in ("v31","v43stock"):
        ff,nf=cells[label]
        sf=[ff[rnd.randrange(len(ff))] for _ in ff]; sn=[nf[rnd.randrange(len(nf))] for _ in nf]
        vals.append(eloperf(sf)-eloperf(sn))
    d.append(vals[0]-vals[1])
d.sort()
pt=(eloperf(cells["v31"][0])-eloperf(cells["v31"][1]))-(eloperf(cells["v43stock"][0])-eloperf(cells["v43stock"][1]))
print(f"\nDiD false-fire cost (v31 vs stock, non-clone games): {pt:+.0f} Elo  boot95=[{d[int(.025*len(d))]:+.0f},{d[int(.975*len(d))]:+.0f}]  P(<0)={sum(1 for x in d if x<0)/len(d):.3f}")
# mirror DiD
mv={}
for stem,label in [("v31_live","v31"),("v43_live","v43stock")]:
    ap={r["episode"]:r for r in json.load(open(ROOT/"analysis"/f"autopsy_{stem}.json",encoding="utf-8"))}
    g=json.load(open(ROOT/"analysis"/f"gate_autopsy_{stem}.json",encoding="utf-8"))
    for r in g: r["outcome"]=ap[r["episode"]]["outcome"]
    mv[label]=[r for r in g if r["prefix_agree"]>=124 and r["opponent"] in lb]
d2=[]
for _ in range(3000):
    a=[mv["v31"][rnd.randrange(len(mv["v31"]))] for _ in mv["v31"]]
    b=[mv["v43stock"][rnd.randrange(len(mv["v43stock"]))] for _ in mv["v43stock"]]
    d2.append(eloperf(a)-eloperf(b))
d2.sort()
print(f"MIRROR edge (v31 minus stock, mirror games only): {eloperf(mv['v31'])-eloperf(mv['v43stock']):+.0f} Elo "
      f"boot95=[{d2[int(.025*len(d2))]:+.0f},{d2[int(.975*len(d2))]:+.0f}] P(>0)={sum(1 for x in d2 if x>0)/len(d2):.3f}")
