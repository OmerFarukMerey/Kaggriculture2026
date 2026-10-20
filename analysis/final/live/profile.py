import json,glob,collections,sys
from pathlib import Path
L=Path('analysis/final/live')
scores=json.load(open(L/'fp3_scores.json'))
extra={'56685034':2257,'56683421':2230,'56692929':1980,'56697978':2000,'56695121':1753,'56663513':2811,'56674312':1927,'56686655':1948,'56690352':1874,'56693442':1386}
scores.update(extra)
out=[]
for f in sorted(L.glob('slim_*.json')):
    d=json.loads(f.read_text()); seat=d['seat']; acts=[a[seat] for a in d['actions'][1:]]
    c=collections.Counter()
    for t,a in enumerate(acts):
        if not isinstance(a,dict): continue
        for o in a.get('market') or []:
            if not o: continue
            k=o[0]
            if k in('BUY_ANIMAL','BUY_LAND','HIRE','BUY_SEED'):
                c[k+':'+str(o[1] if len(o)>1 else '')]+= (o[2] if len(o)>2 and isinstance(o[2],int) and k=='BUY_SEED' else 1)
            if k=='SELL' and len(o)>2: c['sold:'+str(o[1])]+=o[2] if isinstance(o[2],int) else 0
    anim={k.split(':')[1]:v for k,v in c.items() if k.startswith('BUY_ANIMAL')}
    seeds={k.split(':')[1][:3]:v for k,v in c.items() if k.startswith('BUY_SEED')}
    land=sum(v for k,v in c.items() if k.startswith('BUY_LAND')); hire=sum(v for k,v in c.items() if k.startswith('HIRE'))
    out.append((scores.get(str(d['sid']),0),d['sid'],d['rewards'][seat],d['rewards'][1-seat],anim,land,hire,seeds))
for r in sorted(out,reverse=True): print(r[0],r[1],'rew',r[2],'opp',r[3],'anim',r[4],'land',r[5],'hire',r[6],'seeds',r[7])
