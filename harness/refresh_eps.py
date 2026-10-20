import csv, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT
import kaggle
sid = int(sys.argv[1]); stem = sys.argv[2]
eps = kaggle.api.competition_list_episodes(sid)
print(len(eps), "episodes for", sid)
out = ROOT / "analysis" / f"{stem}.csv"
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["id","createTime","endTime","state","type"])
    for e in eps:
        w.writerow([e.id, e.create_time, e.end_time, e.state, e.type])
print("wrote", out)
