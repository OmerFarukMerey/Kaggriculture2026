import json,sys,zipfile,csv,io,collections,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from paths import ROOT
z=zipfile.ZipFile(ROOT/"analysis"/"kaggriculture.zip")
n=z.namelist()[0]
lb={}
for r in csv.DictReader(io.TextIOWrapper(z.open(n),encoding="utf-8-sig")):
    lb[r["TeamName"]]=float(r["Score"])
print("lb teams",len(lb))
out={}
for stem,label in [("autopsy_v31_live","v31"),("autopsy_v43_live","v43stock")]:
    rs=json.load(open(ROOT/"analysis"/f"{stem}.json",encoding="utf-8"))
    known=[r for r in rs if r["opponent"] in lb]
    ratings=[lb[r["opponent"]] for r in known]
    print(f"\n{label}: n={len(rs)} opponents matched to leaderboard: {len(known)}")
    print(f"  opponent rating mean={statistics.mean(ratings):.0f} median={statistics.median(ratings):.0f} "
          f"p10={sorted(ratings)[len(ratings)//10]:.0f} p90={sorted(ratings)[len(ratings)*9//10]:.0f} max={max(ratings):.0f}")
    # winrate by opponent rating band
    bands=[(0,1000),(1000,1500),(1500,2000),(2000,2500),(2500,3200)]
    for lo,hi in bands:
        g=[r for r in known if lo<=lb[r["opponent"]]<hi]
        if not g: continue
        w=sum(1 for r in g if r["outcome"]=="WIN"); l=sum(1 for r in g if r["outcome"]=="LOSS"); t=len(g)-w-l
        print(f"   opp {lo}-{hi}: n={len(g):3d} {w}-{l}-{t} wr={w/len(g):.2f}")
    # chronological opponent strength: first vs second half
    srt=sorted(known,key=lambda r:r["createTime"])
    h1=srt[:len(srt)//2]; h2=srt[len(srt)//2:]
    print(f"   opp rating mean first half={statistics.mean([lb[r['opponent']] for r in h1]):.0f} "
          f"second half={statistics.mean([lb[r['opponent']] for r in h2]):.0f}")
    out[label]=known
