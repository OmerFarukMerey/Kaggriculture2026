import csv,json,os,sys
from collections import defaultdict
ME="Omer Faruk Merey"
ids=[r['id'] for r in csv.DictReader(open('episodes_v30.csv',newline='',encoding='utf-8'))
     if 'COMPLETED' in (r.get('state') or '') and 'PUBLIC' in (r.get('type') or '')]
res=[]
for ep in ids:
    p='replays/episode-%s-replay.json'%ep
    if not os.path.exists(p): continue
    try: rep=json.load(open(p,encoding='utf-8'))
    except Exception: continue
    teams=(rep.get('info') or {}).get('TeamNames') or ['?','?']
    if ME not in teams: continue
    seat=teams.index(ME)
    fin=rep['steps'][-1]
    our=fin[seat].get('reward') or 0; their=fin[1-seat].get('reward') or 0
    res.append(dict(episode=ep,seat=seat,opponent=teams[1-seat],our=our,their=their,
                    margin=our-their,outcome='WIN' if our>their else ('TIE' if our==their else 'LOSS'),
                    nsteps=len(rep['steps'])))
json.dump(res,open('scan30.json','w'),indent=1)
W=sum(1 for r in res if r['outcome']=='WIN');L=sum(1 for r in res if r['outcome']=='LOSS');T=sum(1 for r in res if r['outcome']=='TIE')
print('analyzed',len(res),'record %d-%d-%d'%(W,L,T),'winrate %.3f'%(W/max(1,len(res))))
import statistics
print('mean margin %.0f median %.0f'%(statistics.mean(r['margin'] for r in res),statistics.median(r['margin'] for r in res)))
by=defaultdict(list)
for r in res: by[r['opponent']].append(r)
print('\n%-34s %5s %4s %4s %4s %10s %10s'%('opponent','n','W','L','T','meanMargin','medMargin'))
for opp,rs in sorted(by.items(),key=lambda kv:-len(kv[1])):
    w=sum(1 for r in rs if r['outcome']=='WIN');l=sum(1 for r in rs if r['outcome']=='LOSS');t=len(rs)-w-l
    print('%-34s %5d %4d %4d %4d %10.0f %10.0f'%(opp[:34],len(rs),w,l,t,statistics.mean(r['margin'] for r in rs),statistics.median(r['margin'] for r in rs)))
print('\nWORST 20 LOSSES')
for r in sorted(res,key=lambda x:x['margin'])[:20]:
    print('  ep=%s seat=%d vs %-28s %9.0f vs %9.0f  margin %+9.0f  steps=%d'%(r['episode'],r['seat'],r['opponent'][:28],r['our'],r['their'],r['margin'],r['nsteps']))
print('\nBEST 5 WINS')
for r in sorted(res,key=lambda x:-x['margin'])[:5]:
    print('  ep=%s vs %-28s margin %+9.0f'%(r['episode'],r['opponent'][:28],r['margin']))
