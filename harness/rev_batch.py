import json, sys, time, collections, statistics
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS
import replay_drive as RD
eps = json.load(open(ROOT/"analysis"/sys.argv[1], encoding="utf-8"))
out=[]
for e in eps:
    if not (REPLAYS/f"episode-{e['episode']}-replay.json").exists(): continue
    t0=time.time()
    try: r = RD.rerun(e["episode"])
    except Exception as ex:
        print("FAIL", e["episode"], ex, flush=True); continue
    s=e["seat"]
    rec={"episode":e["episode"],"opponent":e["opponent"],"outcome":e["outcome"],"margin":e["margin"],
         "seat":s,"match":r["match"],"want":r["want"],"got":r["got"],
         "our_rev":r["revenue"][s],"opp_rev":r["revenue"][1-s],
         "our_spend":r["spend"][s],"opp_spend":r["spend"][1-s]}
    out.append(rec)
    print(f"{e['episode']} {e['opponent'][:20]:22s} m={e['margin']:+7.0f} rev us={sum(rec['our_rev'].values()):8,.0f} them={sum(rec['opp_rev'].values()):8,.0f} ({time.time()-t0:.0f}s)", flush=True)
json.dump(out, open(ROOT/"analysis"/(sys.argv[2]), "w"), indent=1)
items=set()
for r in out: items|=set(r["our_rev"])|set(r["opp_rev"])
print(f"\n{'item':12s} {'US rev':>10s} {'OPP rev':>10s} {'diff':>10s}")
for it in sorted(items, key=lambda i:-statistics.mean(r['opp_rev'].get(i,0)-r['our_rev'].get(i,0) for r in out)):
    a=statistics.mean(r["our_rev"].get(it,0) for r in out); b=statistics.mean(r["opp_rev"].get(it,0) for r in out)
    print(f"{it:12s} {a:10,.0f} {b:10,.0f} {b-a:+10,.0f}")
a=statistics.mean(sum(r["our_rev"].values()) for r in out); b=statistics.mean(sum(r["opp_rev"].values()) for r in out)
print(f"{'TOTAL':12s} {a:10,.0f} {b:10,.0f} {b-a:+10,.0f}")
sa=statistics.mean(sum(r["our_spend"].values()) for r in out); sb=statistics.mean(sum(r["opp_spend"].values()) for r in out)
print(f"{'mkt spend':12s} {sa:10,.0f} {sb:10,.0f} {sb-sa:+10,.0f}")
