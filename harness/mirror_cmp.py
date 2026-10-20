import json,sys,zipfile,csv,io,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from paths import ROOT
z=zipfile.ZipFile(ROOT/"analysis"/"kaggriculture.zip"); nm=z.namelist()[0]
lb={r["TeamName"]:float(r["Score"]) for r in csv.DictReader(io.TextIOWrapper(z.open(nm),encoding="utf-8-sig"))}
rec=lambda x:(sum(1 for r in x if r['outcome']=='WIN'),sum(1 for r in x if r['outcome']=='LOSS'),sum(1 for r in x if r['outcome']=='TIE'))
def sc(x):
    w,l,t=rec(x); return (w+0.5*t)/max(len(x),1)
for stem,label in [("gate_autopsy_v31_live","v31"),("gate_autopsy_v43_live","v43stock")]:
    g=json.load(open(ROOT/"analysis"/f"{stem}.json",encoding="utf-8"))
    clone=[r for r in g if r["prefix_agree"]>=124]
    nonclone=[r for r in g if r["prefix_agree"]<124]
    ff=[r for r in nonclone if r["gate_steps"]>0]
    nf=[r for r in nonclone if r["gate_steps"]==0]
    def rr(x):
        rs=[lb[r["opponent"]] for r in x if r["opponent"] in lb]
        return statistics.mean(rs) if rs else float('nan')
    print(f"{label}: total n={len(g)} rec={rec(g)}")
    print(f"   TRUE MIRROR (opp prefix identical to ours): n={len(clone)} {rec(clone)} score={sc(clone):.3f} meanOpp={rr(clone):.0f}")
    print(f"   non-clone, gate opened  : n={len(ff)} {rec(ff)} score={sc(ff):.3f} meanOpp={rr(ff):.0f} meanGateFrac={statistics.mean(r['gate_frac'] for r in ff):.3f}")
    print(f"   non-clone, gate never   : n={len(nf)} {rec(nf)} score={sc(nf):.3f} meanOpp={rr(nf):.0f}")
    print(f"   all non-clone           : n={len(nonclone)} {rec(nonclone)} score={sc(nonclone):.3f} meanOpp={rr(nonclone):.0f}")
    near=[r for r in g if 60<=r["prefix_agree"]<124]
    print(f"   near-chassis (60-123)   : n={len(near)} {rec(near)} meanOpp={rr(near):.0f}")
