import json,sys,math,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from paths import ROOT
def fisher(a,b,c,d):
    # 2x2 exact, two-sided
    def lc(n,k): return math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)
    n=a+b+c+d
    def p(x):
        y=a+b-x; z=a+c-x; w=n-(a+b)-(a+c)+x
        if min(y,z,w,x)<0: return 0.0
        return math.exp(lc(a+b,x)+lc(c+d,z)-lc(n,a+c))
    p0=p(a); tot=0.0
    for x in range(0, min(a+b,a+c)+1):
        px=p(x)
        if px<=p0*(1+1e-9): tot+=px
    return tot
res={}
for stem,label in [("gate_autopsy_v31_live","v31"),("gate_autopsy_v43_live","v43stock")]:
    g=json.load(open(ROOT/"analysis"/f"{stem}.json",encoding="utf-8"))
    ap=json.load(open(ROOT/"analysis"/f"{stem.replace('gate_','')}.json",encoding="utf-8"))
    seat={r["episode"]:r["seat"] for r in ap}
    clone=[r for r in g if r["prefix_agree"]>=124]
    c=collections.Counter((seat[r["episode"]], r["outcome"]) for r in clone)
    print(f"{label} mirror seat x outcome: {dict(c)}")
    margins=sorted(r["margin"] for r in clone)
    print(f"   mirror margins: {['%+d'%m for m in margins]}")
    res[label]=clone
a=res["v31"]; b=res["v43stock"]
aw=sum(1 for r in a if r["outcome"]=="WIN"); al=len(a)-aw
bw=sum(1 for r in b if r["outcome"]=="WIN"); bl=len(b)-bw
print(f"\nmirror WIN vs not: v31 {aw}/{len(a)}  v43stock {bw}/{len(b)}  Fisher p={fisher(aw,al,bw,bl):.5f}")
alo=sum(1 for r in a if r["outcome"]=="LOSS"); blo=sum(1 for r in b if r["outcome"]=="LOSS")
print(f"mirror LOSS: v31 {alo}/{len(a)} v43stock {blo}/{len(b)} Fisher p={fisher(alo,len(a)-alo,blo,len(b)-blo):.5f}")
