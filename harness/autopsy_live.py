"""Download replays for a submission's episodes and summarize W/L/T by opponent.
Usage: py -3.12 harness/autopsy_live.py <episodes_csv_stem> <out_json_stem>
"""
import csv, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS  # noqa: E402

HERE = ROOT / "analysis"
REPLAYS.mkdir(parents=True, exist_ok=True)
ME = "Omer Faruk Merey"

stem = sys.argv[1]
out = sys.argv[2]

episodes = []
with open(HERE / f"{stem}.csv", newline="", encoding="utf-8") as fh:
    for row in csv.DictReader(fh):
        state = row.get("state") or ""
        kind = row.get("type") or ""
        if "COMPLETED" in state and "PUBLIC" in kind:
            episodes.append((row["id"], row.get("createTime", ""), row.get("endTime", "")))
print(f"{len(episodes)} public completed episodes", flush=True)

results = []
for i, (ep, ctime, etime) in enumerate(episodes):
    path = REPLAYS / f"episode-{ep}-replay.json"
    if not path.exists():
        subprocess.run([sys.executable, "-m", "kaggle", "competitions", "replay", ep,
                        "-p", str(REPLAYS)], capture_output=True)
    if not path.exists():
        print(f"episode {ep}: download failed", flush=True); continue
    try:
        replay = json.load(open(path, encoding="utf-8"))
    except Exception as exc:
        print(f"episode {ep}: parse failed {exc}", flush=True); continue
    info = replay.get("info") or {}
    teams = info.get("TeamNames") or ["?", "?"]
    if ME not in teams:
        print(f"episode {ep}: we are not in {teams}?", flush=True); continue
    seat = teams.index(ME)
    steps = replay["steps"]
    final = steps[-1]
    rewards = [s.get("reward") for s in final]
    our, their = rewards[seat] or 0, rewards[1 - seat] or 0
    outcome = "WIN" if our > their else ("TIE" if our == their else "LOSS")
    # opponent action fingerprint: first 40 steps of raw actions
    fp = []
    for t in range(min(140, len(steps))):
        a = steps[t][1 - seat].get("action")
        fp.append(a)
    results.append({
        "episode": ep, "createTime": ctime, "endTime": etime, "seat": seat,
        "opponent": teams[1 - seat], "our": our, "their": their,
        "margin": our - their, "outcome": outcome,
        "nsteps": len(steps),
        "opp_status": steps[-1][1-seat].get("status"),
        "our_status": steps[-1][seat].get("status"),
        "opp_fp": fp,
    })
    if i % 20 == 0:
        print(f"...{i}/{len(episodes)}", flush=True)

wins = sum(1 for r in results if r["outcome"] == "WIN")
losses = [r for r in results if r["outcome"] == "LOSS"]
ties = sum(1 for r in results if r["outcome"] == "TIE")
n = len(results)
print(f"\nrecord: {wins}-{len(losses)}-{ties} of {n}  winrate={wins/max(n,1):.3f}")
json.dump(results, open(HERE / f"{out}.json", "w"), indent=1)
print("wrote", HERE / f"{out}.json")
