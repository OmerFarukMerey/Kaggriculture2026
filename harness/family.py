"""Cluster top-band opponents into chassis families by action-stream agreement."""
import json, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS
ME="Omer Faruk Merey"
eps=json.load(open(ROOT/"analysis"/"top_band_eps.json",encoding="utf-8"))
streams={}
for e in eps:
    p=REPLAYS/f"episode-{e['episode']}-replay.json"
    if not p.exists(): continue
    r=json.load(open(p,encoding="utf-8")); t=r["info"]["TeamNames"]; s=1-t.index(ME)
    streams[e["episode"]]=(e["opponent"], [json.dumps(r["steps"][k][s].get("action"),sort_keys=True) for k in range(len(r["steps"]))])
keys=list(streams)
def sim(a,b):
    n=min(len(a),len(b)); lcp=0
    while lcp<n and a[lcp]==b[lcp]: lcp+=1
    return lcp, sum(1 for i in range(n) if a[i]==b[i])/n
# greedy clustering on lcp>=100 OR agree>=0.85
fam={}; reps=[]
for k in keys:
    nm,st=streams[k]; placed=False
    for i,(rk,rst) in enumerate(reps):
        lcp,ag=sim(st,rst)
        if lcp>=100 or ag>=0.85:
            fam[k]=i; placed=True; break
    if not placed:
        reps.append((k,st)); fam[k]=len(reps)-1
groups=collections.defaultdict(list)
for k,f in fam.items(): groups[f].append(k)
clone=json.load(open(ROOT/"analysis"/"top_band_clone.json",encoding="utf-8"))
cm={c["episode"]:c["opp_v43_match"] for c in clone}
byep={e["episode"]:e for e in eps}
for f,ks in sorted(groups.items(), key=lambda kv:-len(kv[1])):
    teams=sorted(set(streams[k][0] for k in ks))
    w=sum(1 for k in ks if byep[k]["outcome"]=="WIN"); l=sum(1 for k in ks if byep[k]["outcome"]=="LOSS")
    v43=max(cm.get(k,0) for k in ks)
    mg=sum(byep[k]["margin"] for k in ks)/len(ks)
    print(f"family {f}: n={len(ks)} record {w}-{l}-{len(ks)-w-l} meanMargin={mg:+8.0f} v43match={v43:.2f} teams={teams}")
    print(f"   eps: {ks}")
