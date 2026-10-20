import json,sys,zipfile,csv,io,math,random,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from paths import ROOT
z=zipfile.ZipFile(ROOT/"analysis"/"kaggriculture.zip"); n=z.namelist()[0]
lb={r["TeamName"]:float(r["Score"]) for r in csv.DictReader(io.TextIOWrapper(z.open(n),encoding="utf-8-sig"))}
def score(r): return 1.0 if r["outcome"]=="WIN" else (0.5 if r["outcome"]=="TIE" else 0.0)
def perf(rows):
    s=sum(score(r) for r in rows)/len(rows)
    mo=statistics.mean(lb[r["opponent"]] for r in rows)
    s=min(max(s,1e-6),1-1e-6)
    return mo+400*math.log10(s/(1-s)), s, mo
def elo_perf_iter(rows):
    # solve R such that sum expected == sum actual, expected = 1/(1+10^((opp-R)/400))
    lo,hi=0.,5000.
    tgt=sum(score(r) for r in rows)
    for _ in range(200):
        mid=(lo+hi)/2
        e=sum(1/(1+10**((lb[r["opponent"]]-mid)/400)) for r in rows)
        if e<tgt: lo=mid
        else: hi=mid
    return (lo+hi)/2
res={}
for stem,label in [("autopsy_v31_live","v31"),("autopsy_v43_live","v43stock")]:
    rows=[r for r in json.load(open(ROOT/"analysis"/f"{stem}.json",encoding="utf-8")) if r["opponent"] in lb]
    p,s,mo=perf(rows); e=elo_perf_iter(rows)
    # bootstrap
    bs=[]
    rnd=random.Random(7)
    for _ in range(4000):
        samp=[rows[rnd.randrange(len(rows))] for _ in rows]
        try: bs.append(elo_perf_iter(samp))
        except Exception: pass
    bs.sort()
    print(f"{label}: n={len(rows)} score={s:.3f} meanOpp={mo:.0f} simple-perf={p:.0f} elo-perf={e:.0f} "
          f"boot95=[{bs[int(.025*len(bs))]:.0f},{bs[int(.975*len(bs))]:.0f}]")
    res[label]=(rows,e,bs)
# difference bootstrap
rnd=random.Random(11)
a,_,_=res["v31"]; b,_,_=res["v43stock"]
d=[]
for _ in range(4000):
    sa=[a[rnd.randrange(len(a))] for _ in a]; sb=[b[rnd.randrange(len(b))] for _ in b]
    d.append(elo_perf_iter(sa)-elo_perf_iter(sb))
d.sort()
print(f"\nv31 minus v43stock performance rating: point={res['v31'][1]-res['v43stock'][1]:+.0f} "
      f"boot95=[{d[int(.025*len(d))]:+.0f},{d[int(.975*len(d))]:+.0f}]  P(v31>v43)={sum(1 for x in d if x>0)/len(d):.3f}")
