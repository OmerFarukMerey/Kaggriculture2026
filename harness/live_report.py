import json, sys, collections, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT

def load(stem):
    return json.load(open(ROOT/"analysis"/f"{stem}.json", encoding="utf-8"))

def rec(rs):
    w=sum(1 for r in rs if r["outcome"]=="WIN"); l=sum(1 for r in rs if r["outcome"]=="LOSS")
    t=len(rs)-w-l
    return w,l,t,(w/len(rs) if rs else 0)

def wilson(w,n):
    if n==0: return (0,0)
    p=w/n; z=1.96
    d=1+z*z/n; c=(p+z*z/(2*n))/d
    m=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return (c-m, c+m)

for stem,label in [(sys.argv[1],sys.argv[2])]:
    rs=load(stem)
    w,l,t,wr=rec(rs)
    lo,hi=wilson(w,len(rs))
    print(f"=== {label}: n={len(rs)}  record {w}-{l}-{t}  winrate={wr:.3f}  95%CI[{lo:.3f},{hi:.3f}]")
    print(f"    mean margin {sum(r['margin'] for r in rs)/len(rs):+.0f}  median {sorted(r['margin'] for r in rs)[len(rs)//2]:+.0f}")
    losses=[r for r in rs if r["outcome"]=="LOSS"]
    near=[r for r in losses if abs(r["margin"])<=1000]
    print(f"    losses {len(losses)}, within 1000: {len(near)} ({len(near)/max(len(losses),1):.1%} of losses)")
    for r in sorted(near,key=lambda x:-x["margin"]):
        print(f"      NEAR-LOSS ep={r['episode']} margin={r['margin']:+.0f} seat={r['seat']} vs {r['opponent']!r} ({r['our']:.0f} v {r['their']:.0f})")
    nearwin=[r for r in rs if r["outcome"]=="WIN" and r["margin"]<=1000]
    print(f"    near-WINS (<=1000): {len(nearwin)}")
    ties=[r for r in rs if r["outcome"]=="TIE"]
    for r in ties: print(f"      TIE ep={r['episode']} vs {r['opponent']!r} {r['our']:.0f}")
    # error/crash check
    bad=[r for r in rs if r.get("our_status") not in ("DONE",None) or r["nsteps"]<720]
    print(f"    episodes with nsteps<720 or bad status: {len(bad)}")
    for r in bad[:10]: print(f"      ep={r['episode']} nsteps={r['nsteps']} our={r['our_status']} opp={r['opp_status']} outcome={r['outcome']}")
    # chronological
    print("    --- chronological (by createTime, oldest first) ---")
    srt=sorted(rs,key=lambda r:r["createTime"])
    byday=collections.OrderedDict()
    for r in srt:
        k=r["createTime"][:13]
        byday.setdefault(k,[]).append(r)
    for k,v in byday.items():
        w2,l2,t2,wr2=rec(v)
        print(f"      {k}  n={len(v):3d}  {w2}-{l2}-{t2}  wr={wr2:.2f}")
    # halves / quarters
    q=len(srt)//4 or 1
    for i in range(0,len(srt),q if q else 1):
        pass
    for name,chunk in [("first half",srt[:len(srt)//2]),("second half",srt[len(srt)//2:])]:
        w2,l2,t2,wr2=rec(chunk)
        print(f"      {name}: n={len(chunk)} {w2}-{l2}-{t2} wr={wr2:.3f}")
    # opponents
    opp=collections.Counter(r["opponent"] for r in rs)
    print(f"    distinct opponents: {len(opp)}; repeats: {[(k,v) for k,v in opp.most_common() if v>1]}")
