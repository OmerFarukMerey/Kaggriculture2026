"""Phase 2 downloader: fetch missing replays, extract a summary row + slim replay,
and (for historical eras) delete the 29MB full file to keep disk flat.
Usage: py -3.12 harness/pull_all.py <tag>
"""
import csv, json, subprocess, sys, os, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS, DATA_ROOT

ME = "Omer Faruk Merey"
SLIM = DATA_ROOT / "slim"; SLIM.mkdir(parents=True, exist_ok=True)
SUMM = ROOT / "analysis" / "summ"; SUMM.mkdir(parents=True, exist_ok=True)
KEEP_FULL = {"v30", "v31", "v32", "v33", "v43c"}
NSLIM = 62

def summarize(rep, ep, ctime, tag):
    info = rep.get("info") or {}
    teams = info.get("TeamNames") or ["?", "?"]
    if ME not in teams:
        return None
    seat = teams.index(ME)
    steps = rep["steps"]
    fin = steps[-1]
    our = fin[seat].get("reward") or 0
    their = fin[1 - seat].get("reward") or 0
    return {"tag": tag, "episode": ep, "createTime": ctime, "seat": seat,
            "opponent": teams[1 - seat], "our": our, "their": their,
            "margin": our - their,
            "outcome": "WIN" if our > their else ("TIE" if our == their else "LOSS"),
            "nsteps": len(steps),
            "our_status": fin[seat].get("status"), "opp_status": fin[1 - seat].get("status")}

def slim(rep):
    return {"configuration": rep.get("configuration"), "info": rep.get("info"),
            "steps": rep["steps"][:NSLIM]}

def main(tag, stride=1, offset=0):
    idx = json.load(open(ROOT / "analysis" / "eps2" / "index.json"))
    eps = idx[tag][offset::stride]
    outp = SUMM / f"{tag}.jsonl"
    done = set()
    if outp.exists():
        for line in open(outp, encoding="utf-8"):
            try: done.add(json.loads(line)["episode"])
            except Exception: pass
    fh = open(outp, "a", encoding="utf-8")
    fails = []
    for i, (ep, ctime) in enumerate(eps):
        if ep in done: continue
        full = REPLAYS / f"episode-{ep}-replay.json"
        newly = False
        if not full.exists():
            for attempt in range(4):
                subprocess.run([sys.executable, "-m", "kaggle", "competitions", "replay", ep,
                                "-p", str(REPLAYS)], capture_output=True)
                if full.exists(): break
                time.sleep(5 * (attempt + 1))
            newly = True
        if not full.exists():
            fails.append(ep); print(f"FAIL dl {ep}", flush=True); continue
        try:
            rep = json.load(open(full, encoding="utf-8"))
        except Exception as e:
            fails.append(ep); print(f"FAIL parse {ep} {e}", flush=True)
            if newly:
                try: full.unlink(missing_ok=True)
                except OSError: pass
            continue
        row = summarize(rep, ep, ctime, tag)
        sp = SLIM / f"episode-{ep}-slim.json"
        if not sp.exists():
            json.dump(slim(rep), open(sp, "w"))
        if row: fh.write(json.dumps(row) + "\n"); fh.flush()
        else: print(f"NOTME {ep}", flush=True)
        if newly and tag not in KEEP_FULL:
            try: full.unlink(missing_ok=True)
            except OSError: pass
        if i % 25 == 0: print(f"{tag} {i}/{len(eps)}", flush=True)
    fh.close()
    n = len(set(json.loads(l)["episode"] for l in open(outp, encoding="utf-8")))
    print(f"DONE {tag}: asked={len(eps)} have={n} fails={len(fails)} {fails[:20]}", flush=True)

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1,
         int(sys.argv[3]) if len(sys.argv) > 3 else 0)
