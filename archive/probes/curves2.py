import json,sys
from collections import Counter
ME="Omer Faruk Merey"
for ep in sys.argv[1:]:
    rep=json.load(open('replays/episode-%s-replay.json'%ep,encoding='utf-8'))
    teams=rep['info']['TeamNames']; seat=teams.index(ME)
    steps=rep['steps']; n=len(steps)
    cur=[]
    for t in range(n):
        o=steps[t][seat].get('observation') or steps[t][0].get('observation') or {}
        f=o.get('farms') or []
        if len(f)<2: cur.append(cur[-1] if cur else 0.0); continue
        cur.append(float(f[seat].get('money',0) or 0)-float(f[1-seat].get('money',0) or 0))
    o_end=steps[n-1][0].get('observation') or {}
    shops=Counter((o_end.get('town') or {}).get('unlocked_shops') or [])
    fin=steps[n-1]
    fr=[fin[s].get('reward') or 0 for s in range(2)]
    marks=[0,60,120,180,240,300,360,420,480,540,600,660,700,n-1]
    print('ep=%s seat=%d vs %-22s FINALreward %+.0f | cash-gap@end %+.0f'%(ep,seat,teams[1-seat][:22],fr[seat]-fr[1-seat],cur[-1]))
    print('   shops: %s'%dict(shops))
    print('   cashgap: '+' '.join('t%d=%+.0f'%(t,cur[t]) for t in marks))
    seg=[(cur[min(t+60,n-1)]-cur[t],t) for t in range(0,n-60,60)]
    seg.sort()
    print('   worst 60-step cash swings: '+' '.join('t%d:%+.0f'%(t,d) for d,t in seg[:3]))
