"""Scan every locally stored replay; index our games by opponent + current lb rating."""
import json, sys, csv, io, zipfile, collections, statistics
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS, REPLAYS_TOP
ME = "Omer Faruk Merey"
z = zipfile.ZipFile(ROOT/"analysis"/"kaggriculture.zip"); nm=z.namelist()[0]
lb = {r["TeamName"]: float(r["Score"]) for r in csv.DictReader(io.TextIOWrapper(z.open(nm), encoding="utf-8-sig"))}
rows=[]
files = list(REPLAYS.glob("episode-*-replay.json")) + list(REPLAYS_TOP.glob("episode-*-replay.json"))
for p in files:
    try: r = json.load(open(p, encoding="utf-8"))
    except Exception: continue
    info = r.get("info") or {}; teams = info.get("TeamNames") or []
    if ME not in teams or len(teams)!=2: continue
    s = teams.index(ME); st=r["steps"]
    rw = [st[-1][i].get("reward") or 0 for i in (0,1)]
    opp = teams[1-s]
    rows.append({"episode": p.stem.split("-")[1], "opponent": opp, "seat": s,
                 "our": rw[s], "their": rw[1-s], "margin": rw[s]-rw[1-s],
                 "outcome": "WIN" if rw[s]>rw[1-s] else ("TIE" if rw[s]==rw[1-s] else "LOSS"),
                 "lb": lb.get(opp), "path": str(p)})
print(f"{len(files)} replay files, {len(rows)} contain us")
json.dump(rows, open(ROOT/"analysis"/"all_replays_index.json","w"), indent=1)
hi=[r for r in rows if (r["lb"] or 0) >= 2600]
w=sum(1 for r in hi if r["outcome"]=="WIN"); l=sum(1 for r in hi if r["outcome"]=="LOSS")
print(f"\nALL local replays vs opponents now rated 2600+: {w}-{l}-{len(hi)-w-l} of {len(hi)}  "
      f"wr={(w+0.5*(len(hi)-w-l))/max(len(hi),1):.3f} meanMargin={statistics.mean(r['margin'] for r in hi):+.0f}")
c=collections.Counter(r["opponent"] for r in hi)
for o,n in c.most_common():
    g=[r for r in hi if r["opponent"]==o]
    w=sum(1 for r in g if r["outcome"]=="WIN"); l=sum(1 for r in g if r["outcome"]=="LOSS")
    print(f"  {o[:32]:34s} lb={lb[o]:7.1f} n={n:2d} {w}-{l}-{n-w-l} margins={sorted(int(x['margin']) for x in g)}")
