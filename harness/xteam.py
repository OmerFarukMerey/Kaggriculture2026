"""Compare action streams ACROSS teams to detect a shared chassis."""
import json, sys, itertools, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import REPLAYS
ME="Omer Faruk Merey"
pairs=[]
for spec in sys.argv[1:]:
    ep=spec
    r=json.load(open(REPLAYS/f"episode-{ep}-replay.json",encoding="utf-8"))
    t=r["info"]["TeamNames"]; s=1-t.index(ME)
    pairs.append((t[s], ep, [json.dumps(r["steps"][k][s].get("action"),sort_keys=True) for k in range(len(r["steps"]))]))
for (n1,e1,a),(n2,e2,b) in itertools.combinations(pairs,2):
    n=min(len(a),len(b)); lcp=0
    while lcp<n and a[lcp]==b[lcp]: lcp+=1
    agree=sum(1 for i in range(n) if a[i]==b[i])
    print(f"{n1[:20]:22s}({e1}) vs {n2[:20]:22s}({e2}): lcp={lcp:3d} agree={agree}/{n}={agree/n:.3f}")
