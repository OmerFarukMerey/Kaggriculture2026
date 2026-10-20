"""Replay live episodes through v31's clone gate + fingerprint opponents vs the v43 prefix."""
import json, sys, collections, importlib.util
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS

ME = "Omer Faruk Merey"
spec = importlib.util.spec_from_file_location("v31mod", ROOT/"submissions"/"v31-55740384"/"main.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
cd = mod._v31_clone_distance
CMAX = mod._V31_CLONE_MAX
START, STOP = mod._V31_START, mod._V31_STOP
print("gate params", CMAX, START, STOP)

which = sys.argv[1]           # autopsy_v31_live / autopsy_v43_live
rs = json.load(open(ROOT/"analysis"/f"{which}.json", encoding="utf-8"))

def canon(a):
    return json.dumps(a, sort_keys=True)

rows = []
our_prefixes = collections.Counter()
for r in rs:
    p = REPLAYS/f"episode-{r['episode']}-replay.json"
    if not p.exists(): continue
    d = json.load(open(p, encoding="utf-8"))
    steps = d["steps"]; seat = r["seat"]
    ours = [canon(steps[t][seat].get("action")) for t in range(min(124, len(steps)))]
    opps = [canon(steps[t][1-seat].get("action")) for t in range(min(124, len(steps)))]
    our_prefixes["|".join(ours)] += 1
    # gate
    fires = 0; total = 0; first = None
    for t in range(START, min(STOP, len(steps))):
        o = steps[t][0].get("observation")
        if not o or "farms" not in o: continue
        try: dist = cd(o)
        except Exception: continue
        total += 1
        if dist <= CMAX:
            fires += 1
            if first is None: first = t
    # prefix agreement length with our own actions
    agree = 0
    for a, b in zip(ours, opps):
        if a == b: agree += 1
        else: break
    rows.append({"episode": r["episode"], "opponent": r["opponent"], "outcome": r["outcome"],
                 "margin": r["margin"], "gate_steps": fires, "gate_total": total,
                 "gate_frac": fires/total if total else 0.0, "gate_first": first,
                 "prefix_agree": agree, "our_pref": "|".join(ours), "opp_pref": "|".join(opps)})

print(f"\ndistinct OUR 124-step prefixes across {len(rows)} games: {len(our_prefixes)}")
for k, v in our_prefixes.most_common(5):
    print(f"  count={v} hash={hash(k)}")
canon_pref = our_prefixes.most_common(1)[0][0] if our_prefixes else None

exact = [r for r in rows if r["opp_pref"] == canon_pref]
print(f"\nopponents whose FULL 124-step prefix == our v43 prefix: {len(exact)}/{len(rows)}")
for r in exact:
    print(f"   ep={r['episode']} vs {r['opponent']!r} {r['outcome']} margin={r['margin']:+.0f}")
buckets = collections.Counter()
for r in rows:
    a = r["prefix_agree"]
    buckets[("124" if a >= 124 else "60-123" if a >= 60 else "10-59" if a >= 10 else "1-9" if a >= 1 else "0")] += 1
print("prefix-agreement buckets:", dict(buckets))

fired = [r for r in rows if r["gate_steps"] > 0]
print(f"\nclone gate (distance<={CMAX}) opened at least once in {len(fired)}/{len(rows)} games = {len(fired)/max(len(rows),1):.1%}")
print("mean fraction of steps 160-700 with gate open:", round(sum(r['gate_frac'] for r in rows)/max(len(rows),1), 3))
allopen = [r for r in rows if r["gate_frac"] > 0.9]
print(f"games with gate open >90% of window: {len(allopen)}")
w=lambda g: (sum(1 for r in g if r['outcome']=='WIN'), sum(1 for r in g if r['outcome']=='LOSS'), sum(1 for r in g if r['outcome']=='TIE'))
print("record when gate ever fired:", w(fired), " n=",len(fired))
notf=[r for r in rows if r["gate_steps"]==0]
print("record when gate never fired:", w(notf), " n=",len(notf))
hi=[r for r in rows if r["gate_frac"]>0.5]; lo=[r for r in rows if r["gate_frac"]<=0.5]
print("record gate_frac>0.5:", w(hi), "n=",len(hi), " <=0.5:", w(lo), "n=",len(lo))
for r in rows: r.pop("our_pref"); r.pop("opp_pref")
json.dump(rows, open(ROOT/"analysis"/f"gate_{which}.json","w"), indent=1)
print("wrote", ROOT/"analysis"/f"gate_{which}.json")
