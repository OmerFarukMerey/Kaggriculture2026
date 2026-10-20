import json,sys,math
from collections import defaultdict
rows=[]
for f in sys.argv[1:]:
    rows+=json.load(open(f))
g=defaultdict(list)
for r in rows: g[(r['a'],r['b'])].append(r)
def elo(s):
    s=min(max(s,1e-6),1-1e-6)
    return 400*math.log10(s/(1-s))
print(f"{'A vs B':38} {'W-L-T':>10} {'n':>4} {'wr':>6} {'wr(t=.5)':>9} {'elo':>7} {'meanM':>9} {'ties':>5} {'invalid':>7}")
for k,v in g.items():
    invalid=sum(1 for r in v if not r.get('valid',r.get('m') is not None))
    v=[r for r in v if r.get('valid',r.get('m') is not None)]
    if not v:
        print(f"{k[0]+' vs '+k[1]:38} no valid games; invalid={invalid}")
        continue
    w=sum(1 for r in v if r['m']>0); l=sum(1 for r in v if r['m']<0); t=sum(1 for r in v if r['m']==0)
    n=len(v); s=(w+0.5*t)/n
    mm=sum(r['m'] for r in v)/n
    # per-seed tie (unique seeds)
    seeds=defaultdict(list)
    for r in v: seeds[r['seed']].append(r['m'])
    tie_seeds=sum(1 for s2,ms in seeds.items() if all(x==0 for x in ms))
    print(f"{k[0]+' vs '+k[1]:38} {f'{w}-{l}-{t}':>10} {n:>4} {w/n:>6.3f} {s:>9.3f} {elo(s):>7.0f} {mm:>+9.0f} {tie_seeds}/{len(seeds)} {invalid:>7}")
