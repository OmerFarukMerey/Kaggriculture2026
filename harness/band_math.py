"""Elo arithmetic: what is each band worth to our performance rating?"""
import json, zipfile, csv, io, math, statistics, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT
z=zipfile.ZipFile(ROOT/"analysis"/"kaggriculture.zip"); nm=z.namelist()[0]
lb={r["TeamName"]:float(r["Score"]) for r in csv.DictReader(io.TextIOWrapper(z.open(nm),encoding="utf-8-sig"))}
rows=[]
for stem in ("autopsy_v32_live",):
    for r in json.load(open(ROOT/"analysis"/f"{stem}.json",encoding="utf-8")):
        if r["opponent"] in lb: rows.append(r)
def sc(r): return 1.0 if r["outcome"]=="WIN" else (0.5 if r["outcome"]=="TIE" else 0.0)
def eloperf(pairs):   # pairs = [(oppRating, score)]
    lo,hi=0.,5000.; tgt=sum(s for _,s in pairs)
    for _ in range(200):
        mid=(lo+hi)/2
        e=sum(1/(1+10**((o-mid)/400)) for o,_ in pairs)
        if e<tgt: lo=mid
        else: hi=mid
    return (lo+hi)/2
base=[(lb[r["opponent"]], sc(r)) for r in rows]
print(f"v32 live n={len(base)} actual score={sum(s for _,s in base)/len(base):.3f} meanOpp={statistics.mean(o for o,_ in base):.0f}")
print(f"  elo-perf = {eloperf(base):.0f}   (posted rating 2426.3)")
def what_if(lo_, hi_, newwr, label):
    p=[]
    for o,s in base:
        if lo_<=o<hi_: p.append((o,newwr))
        else: p.append((o,s))
    print(f"  {label:52s} -> elo-perf {eloperf(p):.0f}  ({eloperf(p)-eloperf(base):+.0f})")
for lo_,hi_ in [(2600,4000),(2400,2600),(2000,2400),(0,2000)]:
    g=[(o,s) for o,s in base if lo_<=o<hi_]
    print(f"\nband {lo_}-{hi_}: n={len(g)} ({len(g)/len(base):.1%}) wr={sum(s for _,s in g)/len(g):.3f}")
    for tgt in (0.5, 0.65, 0.8, 1.0):
        cur=sum(s for _,s in g)/len(g)
        if tgt<=cur: continue
        what_if(lo_,hi_,tgt,f"  if band winrate -> {tgt:.2f}")
