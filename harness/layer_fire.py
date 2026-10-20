"""How often does v32 deviate from stock v43 on OUR seat, live, after the gate opens?"""
import json, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS
import clone_probe as cp

stem = sys.argv[1]
LO, HI = int(sys.argv[2]), int(sys.argv[3])
rows = json.load(open(ROOT / "analysis" / f"{stem}.json", encoding="utf-8"))
out = []
for i, r in enumerate(rows):
    p = REPLAYS / f"episode-{r['episode']}-replay.json"
    if not p.exists():
        continue
    rep = json.load(open(p, encoding="utf-8"))
    fn = cp.fresh_v43()
    steps = rep["steps"]; cfg = rep.get("configuration") or {}
    seat = r["seat"]
    dev = tot = 0
    firstdev = None
    for t in range(min(HI, len(steps) - 1)):
        cell = steps[t][seat]
        obs = cell.get("observation")
        if obs is None: continue
        obs = dict(obs)
        obs.setdefault("step", steps[t][0]["observation"].get("step", t))
        obs.setdefault("player", seat)
        try: pred = fn(obs, cfg)
        except Exception: pred = None
        act = steps[t + 1][seat].get("action")
        if t < LO or act is None: continue
        tot += 1
        if pred is None or cp.norm(pred) != cp.norm(act):
            dev += 1
            if firstdev is None: firstdev = t
    out.append({"episode": r["episode"], "opponent": r["opponent"], "outcome": r["outcome"],
                "margin": r["margin"], "opp_match": r.get("opp_match"), "dev": dev, "tot": tot,
                "firstdev": firstdev})
    if i % 25 == 0: print(f"...{i}/{len(rows)}", flush=True)
json.dump(out, open(ROOT / "analysis" / f"{stem}_fire.json", "w"), indent=1)
fired = [o for o in out if o["dev"] > 0]
print(f"\nepisodes analysed {len(out)}; layer deviated from stock v43 in {len(fired)} ({len(fired)/max(len(out),1):.3f}) over steps {LO}-{HI}")
cl = [o for o in out if (o['opp_match'] or 0) >= .5]; nc = [o for o in out if (o['opp_match'] or 0) < .5]
for lab, g in [("clone", cl), ("non-clone", nc)]:
    f = [o for o in g if o["dev"] > 0]
    md = sorted(o["dev"] for o in g)
    print(f"  {lab}: n={len(g)} fired={len(f)} ({len(f)/max(len(g),1):.3f}) mean deviating steps={sum(md)/max(len(md),1):.1f} max={max(md) if md else 0}")
for lab, g in [("clone-WIN", [o for o in cl if o['outcome']=='WIN']), ("clone-LOSS", [o for o in cl if o['outcome']=='LOSS'])]:
    if not g: continue
    print(f"  {lab}: n={len(g)} fired={sum(1 for o in g if o['dev']>0)} mean dev steps={sum(o['dev'] for o in g)/len(g):.1f}")
