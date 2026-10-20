"""Day-0 opening: turn-0 market order list + hands-per-step profile for both seats."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS
eps = json.load(open(ROOT/"analysis"/(sys.argv[1] if len(sys.argv)>1 else "top_band_eps.json"), encoding="utf-8"))
seen=set()
for e in sorted(eps, key=lambda x:(x["opponent"], -x["margin"])):
    p = REPLAYS/f"episode-{e['episode']}-replay.json"
    if not p.exists(): continue
    r = json.load(open(p, encoding="utf-8")); st=r["steps"]; s=e["seat"]
    a0 = st[1][1-s].get("action") or {}
    key = (e["opponent"], json.dumps(a0.get("market")))
    if key in seen: continue
    seen.add(key)
    hh=[]
    for d in range(0,6):
        tot=sum(len(st[t][0]["observation"]["farms"][1-s]["hands"]) for t in range(d*24,(d+1)*24))
        our=sum(len(st[t][0]["observation"]["farms"][s]["hands"]) for t in range(d*24,(d+1)*24))
        hh.append(f"d{d}:{our}/{tot}")
    print(f"\n{e['opponent'][:30]:32s} ep={e['episode']} m={e['margin']:+.0f}")
    print(f"   t0 market: {a0.get('market')}")
    print(f"   hand-hours us/them: {' '.join(hh)}")
