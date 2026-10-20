import json,sys,statistics
from collections import Counter
ME="Omer Faruk Merey"
for ep in sys.argv[1:]:
    rep=json.load(open('replays/episode-%s-replay.json'%ep,encoding='utf-8'))
    teams=rep['info']['TeamNames']; seat=teams.index(ME)
    steps=rep['steps']; n=len(steps)
    def rw(t,s):
        v=steps[t][s].get('reward'); return float(v) if v is not None else 0.0
    curve=[rw(t,seat)-rw(t,1-seat) for t in range(n)]
    # shop draw at end
    o_end=steps[n-1][0].get('observation') or {}
    shops=Counter((o_end.get('town') or {}).get('unlocked_shops') or [])
    # find where gap opened: biggest 60-step drops
    win=60
    deltas=[(curve[min(t+win,n-1)]-curve[t],t) for t in range(0,n-1,win//2)]
    deltas.sort()
    marks=[0,120,240,360,480,600,660,690,700,710,n-1]
    print('ep=%s seat=%d vs %s  FINAL %+.0f (us %.0f, them %.0f)'%(ep,seat,teams[1-seat],curve[-1],rw(n-1,seat),rw(n-1,1-seat)))
    print('   shops:',dict(shops))
    print('   margin@:',' '.join('t%d=%+.0f'%(t,curve[t]) for t in marks))
    print('   worst 3 x60-step swings:',' '.join('t%d..%d:%+.0f'%(t,t+win,d) for d,t in deltas[:3]))
    # terminal liquidation: last 30 steps
    print('   last30 swing %+.0f | last10 swing %+.0f'%(curve[-1]-curve[-31],curve[-1]-curve[-11]))
