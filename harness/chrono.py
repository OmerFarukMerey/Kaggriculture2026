import json,sys,zipfile,csv,io,statistics,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from paths import ROOT
z=zipfile.ZipFile(ROOT/"analysis"/"kaggriculture.zip"); nm=z.namelist()[0]
lb={r["TeamName"]:float(r["Score"]) for r in csv.DictReader(io.TextIOWrapper(z.open(nm),encoding="utf-8-sig"))}
def sc(r): return 1.0 if r["outcome"]=="WIN" else (0.5 if r["outcome"]=="TIE" else 0.0)
def eloperf(rows):
    rows=[r for r in rows if r["opponent"] in lb]
    if not rows: return float('nan')
    tgt=sum(sc(r) for r in rows); lo,hi=0.,5000.
    for _ in range(120):
        mid=(lo+hi)/2
        e=sum(1/(1+10**((lb[r["opponent"]]-mid)/400)) for r in rows)
        if e<tgt: lo=mid
        else: hi=mid
    return (lo+hi)/2
for stem,label in [("v31_live","v31"),("v43_live","v43stock")]:
    ap=json.load(open(ROOT/"analysis"/f"autopsy_{stem}.json",encoding="utf-8"))
    g={r["episode"]:r for r in json.load(open(ROOT/"analysis"/f"gate_autopsy_{stem}.json",encoding="utf-8"))}
    srt=sorted(ap,key=lambda r:r["createTime"])
    q=len(srt)//4
    print(f"\n=== {label} chronological quartiles (n={len(srt)}) ===")
    for i in range(4):
        chunk=srt[i*q:(i+1)*q] if i<3 else srt[3*q:]
        w=sum(1 for r in chunk if r['outcome']=='WIN'); l=sum(1 for r in chunk if r['outcome']=='LOSS'); t=len(chunk)-w-l
        rs=[lb[r["opponent"]] for r in chunk if r["opponent"] in lb]
        mir=sum(1 for r in chunk if g.get(r["episode"],{}).get("prefix_agree",0)>=124)
        print(f"  Q{i+1} {chunk[0]['createTime'][:16]} -> {chunk[-1]['createTime'][:16]}  n={len(chunk):3d} "
              f"{w}-{l}-{t} score={(w+0.5*t)/len(chunk):.3f} meanOpp={statistics.mean(rs):.0f} "
              f"eloPerf={eloperf(chunk):.0f} mirrors={mir} ({mir/len(chunk):.0%})")
    # mirror share by day
    print("  mirror share by day:")
    byd={}
    for r in srt: byd.setdefault(r["createTime"][:10],[]).append(r)
    for d,v in byd.items():
        mir=[r for r in v if g.get(r["episode"],{}).get("prefix_agree",0)>=124]
        w=sum(1 for r in mir if r['outcome']=='WIN'); l=sum(1 for r in mir if r['outcome']=='LOSS'); t=len(mir)-w-l
        print(f"    {d}: n={len(v):3d} mirrors={len(mir):2d} ({len(mir)/len(v):.0%}) mirror-rec {w}-{l}-{t}")
