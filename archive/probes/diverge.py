import json,sys,importlib.util,copy
from collections import defaultdict
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
eps=sys.argv[1:]
for ep in eps:
    rep=json.load(open('replays/episode-%s-replay.json'%ep,encoding='utf-8'))
    teams=rep['info']['TeamNames']; seat=teams.index("Omer Faruk Merey")
    steps=rep['steps']; n=len(steps)
    A=load('a%s'%ep,'tetsu_esc.py'); B=load('b%s'%ep,'tetsu.py')
    ndiff=0; first=None; diffsteps=[]; extra=defaultdict(int); missing=defaultdict(int)
    for t in range(n):
        o=steps[t][seat].get('observation') or {}
        if 'farms' not in o: continue
        oa=copy.deepcopy(o); oa['step']=t
        ob=copy.deepcopy(o); ob['step']=t
        try: a=A.agent(oa)
        except Exception as e: a={'ERR':str(e)}
        try: b=B.agent(ob)
        except Exception as e: b={'ERR':str(e)}
        ma=sorted(map(tuple,a.get('market') or [])); mb=sorted(map(tuple,b.get('market') or []))
        if ma!=mb or (a.get('farmer'),tuple(map(tuple,a.get('hands') or [])))!=(b.get('farmer'),tuple(map(tuple,b.get('hands') or []))):
            ndiff+=1; diffsteps.append(t)
            if first is None: first=t
            ca=defaultdict(int); cb=defaultdict(int)
            for x in ma:
                if x[0]=='SELL': ca[x[1]]+=x[2]
            for x in mb:
                if x[0]=='SELL': cb[x[1]]+=x[2]
            for k in set(ca)|set(cb):
                d=ca[k]-cb[k]
                if d>0: extra[k]+=d
                elif d<0: missing[k]+=-d
    print('ep=%s seat=%d vs %-24s diffsteps=%3d firstdiff=%s  extraSELL=%s  fewerSELL=%s'%(
        ep,seat,teams[1-seat][:24],ndiff,first,dict(extra),dict(missing)))
    if diffsteps: print('   diff step range %d..%d  sample=%s'%(min(diffsteps),max(diffsteps),diffsteps[:12]))
