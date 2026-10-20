import json,statistics
from collections import Counter
ME="Omer Faruk Merey"
g=json.load(open('gate30.json'))
sel=[r for r in g if r['gate_frac']>0.5][:40]
rows=[]
for r in sel:
    rep=json.load(open('replays/episode-%s-replay.json'%r['episode'],encoding='utf-8'))
    teams=rep['info']['TeamNames']; seat=teams.index(ME); steps=rep['steps']; n=len(steps)
    def obs(t):
        o=steps[t][seat].get('observation') or steps[t][0].get('observation') or {}
        return o
    def cash(t,s):
        f=(obs(t).get('farms') or []);  return float(f[s].get('money',0) or 0) if len(f)>=2 else 0.0
    # sell volume by actor from actions in last 60
    def sells(t0,t1,s):
        tot=0; rev=0.0
        for t in range(t0,min(t1,n-1)):
            a=steps[t+1][s].get('action') or {}
            pr=(obs(t).get('market') or {}).get('prices') or {}
            for x in (a.get('market') or []):
                if x and x[0]=='SELL':
                    tot+=x[2]; rev+=x[2]*float(pr.get(x[1],0) or 0)
        return tot,rev
    us=sells(660,n,seat); them=sells(660,n,1-seat)
    us2=sells(600,660,seat); them2=sells(600,660,1-seat)
    rows.append((r['episode'],r['opponent'],r['margin'],cash(n-1,seat)-cash(660,seat),cash(n-1,1-seat)-cash(660,1-seat),us,them,us2,them2))
print('%-10s %-18s %8s %9s %9s %14s %14s'%('ep','opp','margin','ourTermD','theirTermD','ourSell660+','theirSell660+'))
for e,o,m,a,b,u,t_,u2,t2 in rows[:20]:
    print('%-10s %-18s %8.0f %9.0f %9.0f  q=%4d r=%7.0f  q=%4d r=%7.0f'%(e,o[:18],m,a,b,u[0],u[1],t_[0],t_[1]))
import statistics as st
print()
print('mean ourTermDelta %.0f  theirTermDelta %.0f  diff %.0f'%(st.mean(x[3] for x in rows),st.mean(x[4] for x in rows),st.mean(x[3]-x[4] for x in rows)))
print('mean sell qty last60: ours %.1f theirs %.1f | est revenue ours %.0f theirs %.0f'%(
  st.mean(x[5][0] for x in rows),st.mean(x[6][0] for x in rows),st.mean(x[5][1] for x in rows),st.mean(x[6][1] for x in rows)))
print('mean sell qty t600-660: ours %.1f theirs %.1f'%(st.mean(x[7][0] for x in rows),st.mean(x[8][0] for x in rows)))
