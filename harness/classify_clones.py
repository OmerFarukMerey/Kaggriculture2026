"""Tag every episode in an autopsy json with a behavioural v43-clone score."""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS
import clone_probe as cp

stem = sys.argv[1]
K = int(sys.argv[2]) if len(sys.argv) > 2 else 120
rows = json.load(open(ROOT / "analysis" / f"{stem}.json", encoding="utf-8"))
t0 = time.time()
out = []
for i, r in enumerate(rows):
    p = REPLAYS / f"episode-{r['episode']}-replay.json"
    if not p.exists():
        continue
    rep = json.load(open(p, encoding="utf-8"))
    opp_seat = 1 - r["seat"]
    m, c, _ = cp.probe(rep, opp_seat, K)
    om, oc, _ = cp.probe(rep, r["seat"], K)
    d = dict(r)
    d.pop("opp_fp", None); d.pop("our_fp", None)
    d["opp_match"] = m / max(c, 1)
    d["opp_match_n"] = c
    d["our_match"] = om / max(oc, 1)
    out.append(d)
    if i % 25 == 0:
        print(f"...{i}/{len(rows)} {time.time()-t0:.0f}s", flush=True)
json.dump(out, open(ROOT / "analysis" / f"{stem}_clone.json", "w"), indent=1)
print(f"wrote {stem}_clone.json  n={len(out)}  {time.time()-t0:.0f}s")
