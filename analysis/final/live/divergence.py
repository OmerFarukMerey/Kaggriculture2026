import json,sys
from pathlib import Path
sys.path.insert(0,'harness')
L=Path('analysis/final/live')
def run(ep,cand_path,maxshow=12):
    d=json.loads((L/f'slim_{ep}.json').read_text()); seat=d['seat']; acts=d['actions']
    from kaggle_environments import make
    from kaggle_environments.agent import build_agent
    env=make("kaggriculture",configuration={"episodeSteps":720,"seed":d['seed']},debug=False)
    loaded,_=build_agent(cand_path,env.agents,env.name); mine={}
    def cand(o,c):
        a=loaded(o,c); mine[int(o.step)]=a; return a
    def opp(o,c):
        t=int(o.step); return acts[t+1][1-seat] if t+1<len(acts) else {"farmer":["PASS"],"hands":[],"market":[]}
    env.run([cand,opp] if seat==0 else [opp,cand])
    shown=0
    for t in range(719):
        live=acts[t+1][seat]; me=mine.get(t)
        if json.dumps(me,sort_keys=True)!=json.dumps(live,sort_keys=True):
            print(f"t={t} day={t//24} h={t%24}\n  LIVE: {json.dumps(live)}\n  CAND: {json.dumps(me)}")
            shown+=1
            if shown>=maxshow: break
    print('final live',d['rewards'],'cand',[s.reward for s in env.steps[-1]], 'seat',seat)
if __name__=='__main__':
    run(int(sys.argv[1]),sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 12)
