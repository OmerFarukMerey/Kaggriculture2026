import csv,json,os,statistics
from collections import defaultdict
import importlib.util
spec=importlib.util.spec_from_file_location("te","tetsu_esc.py"); te=importlib.util.module_from_spec(spec); spec.loader.exec_module(te)
ME="Omer Faruk Merey"
res=json.load(open('scan30.json'))
out=[]
for r in res:
    p='replays/episode-%s-replay.json'%r['episode']
    rep=json.load(open(p,encoding='utf-8'))
    steps=rep['steps']
    n=len(steps)
    seat=r['seat']
    gate_open=0; tot=0; gate_open_pre=0; totpre=0
    dists=[]
    for t in range(0,n):
        o=steps[t][0].get('observation') or {}
        if 'farms' not in o: continue
        d=te._clone_distance(o)
        if 120<=t<680:
            totpre+=1; gate_open_pre+= (d<=6)
        if t>=240:
            tot+=1; gate_open+= (d<=6)
            dists.append(d)
    # score curve
    def rw(t,s):
        v=steps[t][s].get('reward')
        return v if v is not None else 0
    curve=[(rw(t,seat)-rw(t,1-seat)) for t in range(n)]
    town=(steps[0][0].get('observation') or {}).get('town') or {}
    shops=list(town.get('unlocked_shops') or [])
    # final-step town
    town_end=(steps[n-1][0].get('observation') or {}).get('town') or {}
    shops_end=list(town_end.get('unlocked_shops') or [])
    out.append(dict(r, gate_frac=gate_open/max(1,tot), gate_frac_pre=gate_open_pre/max(1,totpre),
        med_dist=statistics.median(dists) if dists else None,
        min_dist=min(dists) if dists else None,
        shops0=shops, shops_end=shops_end,
        m240=curve[240] if n>240 else None, m480=curve[480] if n>480 else None,
        m600=curve[600] if n>600 else None, m700=curve[700] if n>700 else None,
        mfinal=curve[-1]))
json.dump(out,open('gate30.json','w'),indent=1)
print('games',len(out))
# correlation: gate open vs outcome
for lo,hi,lab in ((0.0,0.05,'gate ~never'),(0.05,0.5,'gate sometimes'),(0.5,1.01,'gate mostly/always')):
    s=[r for r in out if lo<=r['gate_frac']<hi]
    if not s: continue
    W=sum(1 for r in s if r['outcome']=='WIN')
    print('%-20s n=%3d W=%3d L=%3d wr=%.3f meanMargin=%+8.0f medMargin=%+8.0f'%(lab,len(s),W,len(s)-W-sum(1 for r in s if r['outcome']=='TIE'),W/len(s),statistics.mean(r['margin'] for r in s),statistics.median(r['margin'] for r in s)))
print()
print('overall gate_frac(step>=240) mean=%.3f  share of games with gate_frac>0.5: %.3f'%(
   statistics.mean(r['gate_frac'] for r in out), sum(1 for r in out if r['gate_frac']>0.5)/len(out)))
print('share of games gate EVER open at step>=240: %.3f'%(sum(1 for r in out if r['gate_frac']>0)/len(out)))
