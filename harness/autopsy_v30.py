"""Download all replays for a submission's episodes and summarize W/L by opponent."""
import csv
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS  # noqa: E402

HERE = ROOT / "analysis"
REPLAYS.mkdir(parents=True, exist_ok=True)
ME = "Omer Faruk Merey"

episodes = []
with open(HERE / "episodes_v30.csv", newline="", encoding="utf-8") as fh:
    for row in csv.DictReader(fh):
        state = row.get("state") or ""
        kind = row.get("type") or ""
        if "COMPLETED" in state and "PUBLIC" in kind:
            episodes.append(row["id"])
print(f"{len(episodes)} public episodes")

results = []
for ep in episodes:
    path = REPLAYS / f"episode-{ep}-replay.json"
    if not path.exists():
        subprocess.run(
            [sys.executable, "-m", "kaggle", "competitions", "replay", ep, "-p", str(REPLAYS)],
            capture_output=True,
        )
    if not path.exists():
        print(f"episode {ep}: download failed")
        continue
    try:
        replay = json.load(open(path, encoding="utf-8"))
    except Exception as exc:
        print(f"episode {ep}: parse failed {exc}")
        continue
    teams = (replay.get("info") or {}).get("TeamNames") or ["?", "?"]
    final = replay["steps"][-1]
    rewards = [s.get("reward") for s in final]
    if ME not in teams:
        print(f"episode {ep}: we are not in {teams}?")
        continue
    seat = teams.index(ME)
    our, their = rewards[seat] or 0, rewards[1 - seat] or 0
    outcome = "WIN" if our > their else ("TIE" if our == their else "LOSS")
    results.append({
        "episode": ep, "seat": seat, "opponent": teams[1 - seat],
        "our": our, "their": their, "margin": our - their, "outcome": outcome,
    })

wins = sum(1 for r in results if r["outcome"] == "WIN")
losses = [r for r in results if r["outcome"] == "LOSS"]
ties = sum(1 for r in results if r["outcome"] == "TIE")
print(f"\nrecord: {wins}-{len(losses)}-{ties} of {len(results)}")
print("\nLOSSES:")
for r in sorted(losses, key=lambda x: x["margin"]):
    print(f"  ep={r['episode']} seat={r['seat']} vs {r['opponent']!r}: "
          f"{r['our']:.0f} vs {r['their']:.0f} (margin {r['margin']:+.0f})")
from collections import Counter
opp_losses = Counter(r["opponent"] for r in losses)
print("\nloss counts by opponent:", dict(opp_losses.most_common()))
json.dump(results, open(HERE / "autopsy_v30.json", "w"), indent=1)
