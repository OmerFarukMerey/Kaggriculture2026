import json, sys, statistics, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS
import replay_drive as RD
eps = json.load(open(ROOT/"analysis"/sys.argv[1], encoding="utf-8"))
agg = collections.defaultdict(lambda: {"u":[0,0],"r":[0,0],"tsum":[0,0]})
per_ep = []
for e in eps:
    if not (REPLAYS/f"episode-{e['episode']}-replay.json").exists(): continue
    try: r = RD.rerun(e["episode"])
    except Exception as ex: print("FAIL",e["episode"],ex,flush=True); continue
    s = e["seat"]
    loc = collections.defaultdict(lambda: {"u":[0,0],"r":[0,0],"tsum":[0,0]})
    for (t,pid,item,price) in r["timeline"]:
        k = 0 if pid==s else 1
        for D in (agg, loc):
            D[item]["u"][k]+=1; D[item]["r"][k]+=price; D[item]["tsum"][k]+=t
    per_ep.append((e, {k:{kk:list(vv) for kk,vv in v.items()} for k,v in loc.items()}))
    print(f"done {e['episode']}", flush=True)
print(f"\n{'item':12s} | {'US units':>8s} {'US $/u':>7s} {'US medStep':>10s} | {'OPP units':>9s} {'OPP $/u':>8s} {'OPP medStep':>11s} | {'price adv':>9s}")
for item, v in sorted(agg.items(), key=lambda kv:-(kv[1]['r'][1]-kv[1]['r'][0])):
    u0,u1=v["u"]; r0,r1=v["r"]; t0,t1=v["tsum"]
    if u0==0 and u1==0: continue
    p0=r0/max(u0,1); p1=r1/max(u1,1)
    print(f"{item:12s} | {u0:8d} {p0:7.1f} {t0/max(u0,1):10.0f} | {u1:9d} {p1:8.1f} {t1/max(u1,1):11.0f} | {p1-p0:+9.1f}")
json.dump([{ "ep":e["episode"],"opp":e["opponent"],"outcome":e["outcome"],"margin":e["margin"],"tab":tab}
           for e,tab in per_ep], open(ROOT/"analysis"/sys.argv[2],"w"), indent=1)
