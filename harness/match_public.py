"""Does any public agent in agents/public/ reproduce this opponent's recorded stream?"""
import json, sys, importlib.util, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS
ep, name = sys.argv[1], sys.argv[2]
K = int(sys.argv[3]) if len(sys.argv)>3 else 60
r=json.load(open(REPLAYS/f"episode-{ep}-replay.json",encoding="utf-8"))
teams=r["info"]["TeamNames"]; seat=teams.index(name); steps=r["steps"]; cfg=r.get("configuration") or {}
def norm(a): return json.dumps(a,sort_keys=True,default=str)
for f in sorted((ROOT/"agents"/"public").glob("*.py")):
    if f.name.startswith("opp_"): continue
    try:
        before=set(sys.modules)
        spec=importlib.util.spec_from_file_location("cand_"+f.stem, f)
        m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        fn=getattr(m,"agent",None) or getattr(m,"_kaggle_submission_entrypoint",None)
        if fn is None: print(f"{f.name:22s} no agent"); continue
        ok=tot=0
        for t in range(min(K,len(steps)-1)):
            obs=dict(steps[t][seat]["observation"])
            obs.setdefault("step", steps[t][0]["observation"].get("step",t)); obs.setdefault("player",seat)
            try: pred=fn(obs,cfg)
            except Exception: pred=None
            act=steps[t+1][seat].get("action")
            if act is None: continue
            tot+=1; ok += (pred is not None and norm(pred)==norm(act))
        print(f"{f.name:22s} {ok}/{tot} = {ok/max(tot,1):.3f}")
        for mm in set(sys.modules)-before: sys.modules.pop(mm,None)
    except Exception as e:
        print(f"{f.name:22s} ERR {type(e).__name__}: {str(e)[:60]}")
