"""Reconstruct both seats' economy from a replay: per-day money, farm composition,
hands, land, animals, crops, and market activity. Everything here is public state."""
import json, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import REPLAYS

TPD = 24

def load(ep):
    p = Path(ep)
    if not p.is_file():
        p = REPLAYS / f"episode-{ep}-replay.json"
    return json.load(open(p, encoding="utf-8"))

def tile_census(farm):
    c = collections.Counter()
    for row in farm["tiles"]:
        for t in row:
            if t is None: c["empty"] += 1
            elif t == "LOCKED": c["locked"] += 1
            elif isinstance(t, dict):
                k = t.get("kind")
                if k == "WEED": c["weed"] += 1
                elif "animal" in t and t.get("animal"): c["A_"+t["animal"]] += 1
                elif k in ("COOP","PASTURE"): c["empty_"+k] += 1
                elif k == "PLANT": c["C_"+t["crop"]] += 1
                else: c["?"] += 1
    return c

def summarize(replay, label=None, quiet=False):
    st = replay["steps"]; n = len(st)
    teams = (replay.get("info") or {}).get("TeamNames") or ["seat0","seat1"]
    out = {"teams": teams, "days": []}
    for day in range(30):
        idx = min(day*TPD, n-1)
        o = st[idx][0]["observation"]
        if "farms" not in o: continue
        rec = {"day": day}
        for s in (0,1):
            farm = o["farms"][s]
            rec[f"money{s}"] = farm["money"]
            rec[f"land{s}"] = len(farm["unlocked_quadrants"])
        # aggregate actions + peak hands over the day
        for s in (0,1):
            mk = collections.Counter(); sold = collections.Counter(); bought = collections.Counter()
            hires = 0; peak_hands = 0; unlocks = 0
            waters = fert = feeds = cares = harvest = plants = 0
            for t in range(day*TPD, min((day+1)*TPD, n)):
                fm = st[t][0]["observation"]["farms"][s] if "farms" in st[t][0]["observation"] else None
                if fm: peak_hands = max(peak_hands, len(fm["hands"]))
                a = st[t][s].get("action")
                if not a: continue
                units = [a.get("farmer")] + list(a.get("hands") or [])
                for u in units:
                    if not u: continue
                    v = u[0]
                    if v == "WATER": waters += 1
                    elif v == "FERTILIZE": fert += 1
                    elif v == "FEED": feeds += 1
                    elif v == "CARE": cares += 1
                    elif v == "HARVEST": harvest += 1
                    elif v == "PLANT": plants += 1
                for m in (a.get("market") or []):
                    if not m: continue
                    op = m[0]; mk[op] += 1
                    if op == "SELL": sold[m[1]] += (m[2] if len(m)>2 else 1)
                    elif op in ("BUY_SEED","BUY_ANIMAL","BUY_FERTILIZER","BUY"):
                        bought[(op, m[1] if len(m)>1 else "")] += (m[2] if len(m)>2 else 1)
                    elif op == "HIRE": hires += 1
                    elif op in ("UNLOCK_LAND","UNLOCK","BUY_LAND"): unlocks += 1
            rec[f"hands{s}"] = peak_hands
            rec[f"hires{s}"] = hires
            rec[f"sold{s}"] = dict(sold)
            rec[f"bought{s}"] = {f"{k[0]}:{k[1]}": v for k, v in bought.items()}
            rec[f"acts{s}"] = {"water":waters,"fert":fert,"feed":feeds,"care":cares,"harvest":harvest,"plant":plants}
            rec[f"tiles{s}"] = dict(tile_census(o["farms"][s]))
        out["days"].append(rec)
    fin = st[-1]
    out["final"] = [fin[0].get("reward"), fin[1].get("reward")]
    return out

def fmt(sm, seatlabel=None):
    t = sm["teams"]
    print(f"  day | {t[0][:18]:18s} money hands land  animals/crops        | {t[1][:18]:18s} money hands land  animals/crops")
    for r in sm["days"]:
        def side(s):
            ti = r[f"tiles{s}"]
            an = " ".join(f"{k[2:4]}{v}" for k,v in sorted(ti.items()) if k.startswith("A_"))
            cr = " ".join(f"{k[2:4]}{v}" for k,v in sorted(ti.items()) if k.startswith("C_"))
            return f"{r[f'money{s}']:9.0f} {r[f'hands{s}']:2d}h L{r[f'land{s}']}  {an:16s} {cr}"
        print(f"  {r['day']:3d} | {side(0):62s} | {side(1)}")
    print(f"  final: {sm['final']}  gap={sm['final'][0]-sm['final'][1]:+.0f}")

if __name__ == "__main__":
    for ep in sys.argv[1:]:
        r = load(ep)
        sm = summarize(r)
        print(f"\n===== {ep}  {sm['teams']} =====")
        fmt(sm)
