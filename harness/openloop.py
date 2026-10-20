"""Is an opponent open-loop? Compare their action stream across two episodes."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import REPLAYS
def stream(ep, name):
    r=json.load(open(REPLAYS/f"episode-{ep}-replay.json",encoding="utf-8"))
    t=r["info"]["TeamNames"]; s=t.index(name)
    return [json.dumps(r["steps"][k][s].get("action"),sort_keys=True) for k in range(len(r["steps"]))], r
name=sys.argv[1]; eps=sys.argv[2:]
base,_=stream(eps[0],name)
for ep in eps[1:]:
    o,_=stream(ep,name)
    n=min(len(base),len(o))
    agree=sum(1 for i in range(n) if base[i]==o[i])
    first=next((i for i in range(n) if base[i]!=o[i]), None)
    # longest common prefix
    lcp=0
    while lcp<n and base[lcp]==o[lcp]: lcp+=1
    print(f"{name}: {eps[0]} vs {ep}: agree {agree}/{n} = {agree/n:.3f}  first-diff at t={first} (day {first//24 if first is not None else '-'})  lcp={lcp}")
