import json,sys,importlib.util,copy
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ME="Omer Faruk Merey"
cands=['tetsu.py','tetsu_v2.py','tetsu_esc.py']
for ep in sys.argv[1:]:
    rep=json.load(open('replays/episode-%s-replay.json'%ep,encoding='utf-8'))
    teams=rep['info']['TeamNames']; seat=teams.index(ME); opp=1-seat
    steps=rep['steps']; n=len(steps)
    line=[]
    for c in cands:
        M=load('m_%s_%s'%(ep,c.replace('.','_')),c)
        match=0; tot=0; firstmis=None
        for t in range(n-1):
            o=steps[t][opp].get('observation') or {}
            if 'farms' not in o: continue
            oo=copy.deepcopy(o); oo['step']=t
            try: a=M.agent(oo)
            except Exception: a={}
            live=steps[t+1][opp].get('action') or {}
            ka=(sorted(map(tuple,a.get('market') or [])),a.get('farmer'),tuple(map(tuple,a.get('hands') or [])))
            kl=(sorted(map(tuple,live.get('market') or [])),live.get('farmer'),tuple(map(tuple,live.get('hands') or [])))
            tot+=1
            if ka==kl: match+=1
            elif firstmis is None: firstmis=t
        line.append('%s %d/%d(firstmis=%s)'%(c,match,tot,firstmis))
    print('ep=%s opp=%-20s  %s'%(ep,teams[opp][:20],'  |  '.join(line)))
