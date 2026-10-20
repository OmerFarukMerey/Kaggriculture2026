import json,importlib.util,copy,statistics,sys
from collections import defaultdict
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
res=json.load(open('gate30.json'))
out=[]
for i,r in enumerate(res):
    ep=r['episode']
    rep=json.load(open('replays/episode-%s-replay.json'%ep,encoding='utf-8'))
    teams=rep['info']['TeamNames']; seat=teams.index("Omer Faruk Merey")
    steps=rep['steps']; n=len(steps)
    A=load('a%s'%ep,'tetsu_esc.py'); B=load('b%s'%ep,'tetsu.py')
    prices=[]
    for t in range(n):
        o=steps[t][seat].get('observation') or {}
        prices.append(((o.get('market') or {}).get('prices') or {}))
    sellA=defaultdict(lambda: defaultdict(int)); sellB=defaultdict(lambda: defaultdict(int))
    ndiff=0
    for t in range(n):
        o=steps[t][seat].get('observation') or {}
        if 'farms' not in o: continue
        oa=copy.deepcopy(o); oa['step']=t; ob=copy.deepcopy(o); ob['step']=t
        try: a=A.agent(oa)
        except Exception: a={}
        try: b=B.agent(ob)
        except Exception: b={}
        ma=sorted(map(tuple,a.get('market') or [])); mb=sorted(map(tuple,b.get('market') or []))
        if ma!=mb or a.get('farmer')!=b.get('farmer') or a.get('hands')!=b.get('hands'): ndiff+=1
        for x in ma:
            if x[0]=='SELL': sellA[x[1]][t]+=x[2]
        for x in mb:
            if x[0]=='SELL': sellB[x[1]][t]+=x[2]
    # revenue at observed prices
    def rev(d):
        s=0.0
        for item,byt in d.items():
            for t,q in byt.items():
                s+=q*float(prices[t].get(item,0) or 0)
        return s
    ra,rb=rev(sellA),rev(sellB)
    qa=sum(sum(v.values()) for v in sellA.values()); qb=sum(sum(v.values()) for v in sellB.values())
    out.append(dict(episode=ep,opponent=r['opponent'],outcome=r['outcome'],margin=r['margin'],
                    gate_frac=r['gate_frac'],ndiff=ndiff,revA=ra,revB=rb,edge_value=ra-rb,qA=qa,qB=qb))
    if i%20==0: print('..%d/%d'%(i,len(res)),flush=True)
json.dump(out,open('edgeval.json','w'),indent=1)
print('DONE')
