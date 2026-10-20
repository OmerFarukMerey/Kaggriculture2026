"""Structural economy comparison: us vs opponent, over a set of episodes."""
import json, sys, statistics, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS
from route_recon import load, summarize

def feats(sm, s):
    d = {r["day"]: r for r in sm["days"]}
    def ti(day, key): return d[day][f"tiles{s}"].get(key, 0) if day in d else 0
    sells = collections.Counter(); harv = 0; plants = 0; hires = 0
    water = fert = feed = care = 0
    for r in sm["days"]:
        for k, v in r[f"sold{s}"].items(): sells[k] += v
        a = r[f"acts{s}"]; harv += a["harvest"]; plants += a["plant"]; water += a["water"]
        fert += a["fert"]; feed += a["feed"]; care += a["care"]
        hires += r[f"hires{s}"]
    land_day = {}
    for r in sm["days"]:
        land_day.setdefault(r[f"land{s}"], r["day"])
    return {
        "melon_d10": ti(10,"C_MELON"), "melon_max": max(d[k][f"tiles{s}"].get("C_MELON",0) for k in d),
        "straw_d12": ti(12,"C_STRAWBERRY"), "straw_max": max(d[k][f"tiles{s}"].get("C_STRAWBERRY",0) for k in d),
        "cow_d12": ti(12,"A_COW"), "cow_max": max(d[k][f"tiles{s}"].get("A_COW",0) for k in d),
        "sheep_max": max(d[k][f"tiles{s}"].get("A_SHEEP",0) for k in d),
        "goose_max": max(d[k][f"tiles{s}"].get("A_GOOSE",0) for k in d),
        "wheat_d20": ti(20,"C_WHEAT"),
        "L2day": land_day.get(2), "L3day": land_day.get(3), "L4day": land_day.get(4),
        "hands_mean": statistics.mean(d[k][f"hands{s}"] for k in d if k>=12),
        "hires": hires, "harv": harv, "plants": plants, "water": water, "fert": fert,
        "feed": feed, "care": care,
        "sells": dict(sells), "sell_units": sum(sells.values()),
        "money_d10": d[10][f"money{s}"], "money_d15": d[15][f"money{s}"], "money_d20": d[20][f"money{s}"],
    }

eps = json.load(open(ROOT/"analysis"/sys.argv[1], encoding="utf-8"))
only = sys.argv[2] if len(sys.argv)>2 else None
if only in ("LOSS","WIN"): eps=[e for e in eps if e["outcome"]==only]
US=[]; TH=[]
print(f"{'ep':11s} {'opp':20s} side  ME  ST  CO SH GO  L3d  hnd hire harv wtr frt sellU  fin")
for e in eps:
    p = REPLAYS/f"episode-{e['episode']}-replay.json"
    if not p.exists(): continue
    sm = summarize(load(e["episode"])); s=e["seat"]
    fu, ft = feats(sm,s), feats(sm,1-s)
    US.append(fu); TH.append(ft)
    for lab,f,m in (("US ",fu,e["our"]),("OPP",ft,e["their"])):
        print(f"{e['episode']:11s} {e['opponent'][:19]:20s} {lab} {f['melon_max']:3d} {f['straw_max']:3d} "
              f"{f['cow_max']:3d} {f['sheep_max']:2d} {f['goose_max']:2d} {str(f['L3day']):>4s} "
              f"{f['hands_mean']:5.1f} {f['hires']:4d} {f['harv']:4d} {f['water']:4d} {f['fert']:3d} {f['sell_units']:5d} {m:7.0f}")
print("\n=== means (n=%d pairs) ===" % len(US))
keys=["melon_max","straw_max","cow_max","sheep_max","goose_max","hands_mean","hires","harv","plants","water","fert","feed","care","sell_units","money_d10","money_d15","money_d20"]
print(f"{'feature':12s} {'US':>10s} {'OPP':>10s} {'diff':>10s}")
for k in keys:
    a=statistics.mean(f[k] for f in US); b=statistics.mean(f[k] for f in TH)
    print(f"{k:12s} {a:10.1f} {b:10.1f} {b-a:+10.1f}")
def L(k):
    a=[f[k] for f in US if f[k] is not None]; b=[f[k] for f in TH if f[k] is not None]
    print(f"{k:12s} {statistics.mean(a) if a else float('nan'):10.1f} {statistics.mean(b) if b else float('nan'):10.1f}   (n {len(a)}/{len(b)})")
for k in ("L2day","L3day","L4day"): L(k)
print("\n--- sell units by item ---")
items=set()
for f in US+TH: items|=set(f["sells"])
print(f"{'item':12s} {'US':>8s} {'OPP':>8s}")
for it in sorted(items):
    print(f"{it:12s} {statistics.mean(f['sells'].get(it,0) for f in US):8.1f} {statistics.mean(f['sells'].get(it,0) for f in TH):8.1f}")
