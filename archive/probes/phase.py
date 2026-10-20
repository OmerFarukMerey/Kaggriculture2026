import json,statistics
from collections import Counter,defaultdict
ME="Omer Faruk Merey"
g=json.load(open('gate30.json'))
rows=[]
for r in g:
    rep=json.load(open('replays/episode-%s-replay.json'%r['episode'],encoding='utf-8'))
    teams=rep['info']['TeamNames']; seat=teams.index(ME); steps=rep['steps']; n=len(steps)
    cur=[]
    for t in range(n):
        o=steps[t][seat].get('observation') or steps[t][0].get('observation') or {}
        f=o.get('farms') or []
        cur.append(float(f[seat].get('money',0) or 0)-float(f[1-seat].get('money',0) or 0) if len(f)>=2 else (cur[-1] if cur else 0.0))
    o_end=steps[n-1][0].get('observation') or {}
    shops=(o_end.get('town') or {}).get('unlocked_shops') or []
    def at(t): return cur[min(t,n-1)]
    rows.append(dict(r, open_=at(240)-at(0), mid=at(480)-at(240), late=at(660)-at(480), term=cur[-1]-at(660),
                     final=cur[-1], shops=Counter(shops)))
json.dump([{k:(dict(v) if isinstance(v,Counter) else v) for k,v in r.items()} for r in rows],open('phase30.json','w'),indent=1)
def rep_(sel,lab):
    if not sel: return
    print('%-28s n=%3d  open %+7.0f  mid %+7.0f  late %+7.0f  TERM %+7.0f  final %+7.0f'%(lab,len(sel),
      *[statistics.mean(r[k] for r in sel) for k in ('open_','mid','late','term','final')]))
allr=rows
rep_(allr,'ALL')
rep_([r for r in allr if r['outcome']=='WIN'],'WINS')
rep_([r for r in allr if r['outcome']=='LOSS'],'LOSSES')
rep_([r for r in allr if r['gate_frac']>0.5],'gate-open (>0.5)')
rep_([r for r in allr if r['gate_frac']>0.5 and r['outcome']=='LOSS'],'gate-open LOSSES')
rep_([r for r in allr if r['gate_frac']>0.5 and r['outcome']=='WIN'],'gate-open WINS')
rep_([r for r in allr if r['gate_frac']<=0.05],'gate-closed')
rep_([r for r in allr if r['gate_frac']<=0.05 and r['outcome']=='LOSS'],'gate-closed LOSSES')
print()
print('share of total loss attributable, LOSSES only (mean):')
L=[r for r in allr if r['outcome']=='LOSS']
tot=sum(abs(statistics.mean(r[k] for r in L)) for k in ('open_','mid','late','term'))
for k in ('open_','mid','late','term'):
    print('  %-6s %+8.0f  (%.0f%% of |moves|)'%(k,statistics.mean(r[k] for r in L),100*abs(statistics.mean(r[k] for r in L))/tot))
# shop draw correlation
print()
sd=defaultdict(list)
for r in allr:
    for s,c in r['shops'].items(): sd[s].append((c,r['margin']))
print('%-16s %6s %10s %10s'%('shop','games','meanMargin@>=2','meanMargin@<=1'))
for s in sorted(sd):
    hi=[m for c,m in sd[s] if c>=2]; lo=[m for r2 in [0] for c,m in sd[s] if c<=1]
    others=[r['margin'] for r in allr if r['shops'].get(s,0)==0]
    print('%-16s %6d %10s %10s   (absent n=%d mean %+.0f)'%(s,len(sd[s]),
      '%+.0f(n=%d)'%(statistics.mean(hi),len(hi)) if hi else '-',
      '%+.0f(n=%d)'%(statistics.mean(lo),len(lo)) if lo else '-',
      len(others),statistics.mean(others) if others else 0))
