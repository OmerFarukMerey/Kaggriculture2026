import json,sys,importlib.util,copy
from collections import defaultdict
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
for ep in sys.argv[1:]:
    rep=json.load(open('replays/episode-%s-replay.json'%ep,encoding='utf-8'))
    teams=rep['info']['TeamNames']; seat=teams.index("Omer Faruk Merey")
    steps=rep['steps']; n=len(steps)
    A=load('v%s'%ep,'tetsu_esc.py')
    # instrument
    fired={'n':0,'items':defaultdict(int)}
    orig=A._preempt_shift
    horiz={'esc':0,'tot':0}
    origh=A._lead_horizon
    curstep={'t':0}
    def lh(obs,_o=origh):
        h=_o(obs); return h
    def ps(obs,action,step,_o=orig):
        before=len(action.get('market') or [])
        r=_o(obs,action,step)
        after=len(r.get('market') or [])
        if after>before:
            fired['n']+=1
            for x in (r.get('market') or [])[before:]:
                fired['items'][x[1]]+=x[2]
        return r
    A._preempt_shift=ps
    match=0; mism=0; mismsteps=[]; gate240=0; tot240=0
    for t in range(n):
        o=steps[t][seat].get('observation') or {}
        if 'farms' not in o: continue
        oo=copy.deepcopy(o); oo['step']=t
        if t>=240:
            tot240+=1; gate240 += (A._clone_distance(oo)<=6)
        try: a=A.agent(oo)
        except Exception as e: a={'ERR':str(e)}
        live=steps[t][seat].get('action') or {}
        ka=(sorted(map(tuple,a.get('market') or [])),a.get('farmer'),tuple(map(tuple,a.get('hands') or [])))
        kl=(sorted(map(tuple,live.get('market') or [])),live.get('farmer'),tuple(map(tuple,live.get('hands') or [])))
        if ka==kl: match+=1
        else:
            mism+=1
            if len(mismsteps)<8: mismsteps.append((t,ka[0],kl[0],ka[1],kl[1]))
    print('ep=%s seat=%d vs %-22s reproduce match=%d mismatch=%d  preempt_fired_steps=%d items=%s  gate<=6 at t>=240: %d/%d'%(
        ep,seat,teams[1-seat][:22],match,mism,fired['n'],dict(fired['items']),gate240,tot240))
    for m in mismsteps[:4]: print('    t=%d mineMkt=%s liveMkt=%s mineFarmer=%s liveFarmer=%s'%m)
