import json, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS
import clone_probe as CP
eps = json.load(open(ROOT/"analysis"/"top_band_eps.json", encoding="utf-8"))
K = int(sys.argv[1]) if len(sys.argv)>1 else 120
out=[]
for e in sorted(eps, key=lambda x: x["opponent"]):
    p = REPLAYS/f"episode-{e['episode']}-replay.json"
    if not p.exists(): print("missing", e["episode"]); continue
    r = json.load(open(p, encoding="utf-8"))
    us = e["seat"]; opp = 1-us
    mo,co,_ = CP.probe(r, opp, K)
    mu,cu,_ = CP.probe(r, us, K)
    out.append({**{k:e[k] for k in ("episode","opponent","outcome","margin","seat")},
                "opp_v43_match": mo/max(co,1), "our_v43_match": mu/max(cu,1),
                "opp_m": mo, "opp_c": co})
    print(f"{e['episode']:11s} {e['opponent'][:24]:26s} {e['outcome']:5s} m={e['margin']:+7.0f} "
          f"OPPv43={mo}/{co}={mo/max(co,1):.3f}  USv43={mu}/{cu}={mu/max(cu,1):.3f}", flush=True)
json.dump(out, open(ROOT/"analysis"/"top_band_clone.json","w"), indent=1)
