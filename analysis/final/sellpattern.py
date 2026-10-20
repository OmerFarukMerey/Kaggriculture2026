import json,sys,collections
from kaggle_environments import make
from kaggle_environments.agent import build_agent
GT='../kaggriculture-candidates/final/game-theoretic-master-discrete-optimizat/main.py'
PREM=("MILK","WOOL","EGG","STRAWBERRY","MELON","TOMATO","CARROT","WHEAT","FERTILIZER")
seed=int(sys.argv[1]) if len(sys.argv)>1 else 62011
env=make("kaggriculture",configuration={"episodeSteps":720,"seed":seed},debug=False)
a0,_=build_agent(GT,env.agents,env.name); a1,_=build_agent(GT,env.agents,env.name)
log=[]
def w(o,c):
    a=a0(o,c)
    shed=dict(o['private']['shed']); inv=o['private']['inventories']
    sells=[x for x in a.get('market',[]) if x and x[0]=='SELL']
    log.append((int(o.step),{k:shed.get(k,0) for k in PREM if shed.get(k,0)},sells,{k:o['market']['prices'].get(k) for k in PREM}))
    return a
env.run([w,a1])
print('rewards',[s.reward for s in env.steps[-1]])
hourcnt=collections.Counter(); qty=collections.Counter()
for t,shed,sells,pr in log:
    for s in sells:
        if s[1] in ("MILK","WOOL","EGG","STRAWBERRY","MELON","TOMATO"):
            hourcnt[(s[1],t%24)]+=1; qty[s[1]]+=s[2] if isinstance(s[2],int) else 0
print('sell qty',dict(qty))
for item in ("MILK","WOOL","EGG","STRAWBERRY","MELON","TOMATO"):
    print(item, sorted((h,c) for (i,h),c in hourcnt.items() if i==item))
# show a window
for t,shed,sells,pr in log[300:340]:
    print(t,t%24,shed,sells,{k:pr[k] for k in ("MILK","WOOL","EGG","STRAWBERRY","MELON")})
