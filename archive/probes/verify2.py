import json,sys,importlib.util,copy
from collections import defaultdict
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
for ep in sys.argv[1:]:
    rep=json.load(open('replays/episode-%s-replay.json'%ep,encoding='utf-8'))
    teams=rep['info']['TeamNames']; seat=teams.index("Omer Faruk Merey")
    steps=rep['steps']; n=len(steps)
    A=load('v%s'%ep,'tetsu_esc.py'); B=load('w%s'%ep,'tetsu.py')
    firedA={'n':0,'q':defaultdict(int)}; firedB={'n':0,'q':defaultdict(int)}
    def mk(mod,rec):
        orig=mod._preempt_shift
        def ps(obs,action,step,_o=orig,_r=rec):
            b=len(action.get('market') or []); r=_o(obs,action,step); a=list(r.get('market') or [])
            if len(a)>b:
                _r['n']+=1
                for x in a[b:]: _r['q'][x[1]]+=x[2]
            return r
        mod._preempt_shift=ps
    mk(A,firedA); mk(B,firedB)
    match=mism=0; ndiff=0; diffs=[]; horizdiff=0
    for t in range(n):
        o=steps[t][seat].get('observation') or {}
        if 'farms' not in o: continue
        oa=copy.deepcopy(o); oa['step']=t; ob=copy.deepcopy(o); ob['step']=t
        ha=A._lead_horizon(oa); hb=B._lead_horizon(ob)
        if ha!=hb: horizdiff+=1
        a=A.agent(oa); b=B.agent(ob)
        ka=(sorted(map(tuple,a.get('market') or [])),a.get('farmer'),tuple(map(tuple,a.get('hands') or [])))
        kb=(sorted(map(tuple,b.get('market') or [])),b.get('farmer'),tuple(map(tuple,b.get('hands') or [])))
        if ka!=kb:
            ndiff+=1
            if len(diffs)<5: diffs.append((t,ka[0],kb[0]))
        if t+1<n:
            live=steps[t+1][seat].get('action') or {}
            kl=(sorted(map(tuple,live.get('market') or [])),live.get('farmer'),tuple(map(tuple,live.get('hands') or [])))
            if ka==kl: match+=1
            else: mism+=1
    print('ep=%s seat=%d vs %-20s repro %d/%d  ESCvsSTOCK actiondiffs=%d horizondiffs=%d  preemptFired esc=%d stock=%d  escQ=%s'%(
        ep,seat,teams[1-seat][:20],match,match+mism,ndiff,horizdiff,firedA['n'],firedB['n'],dict(firedA['q'])))
    for d in diffs: print('    t=%d esc=%s stock=%s'%d)
