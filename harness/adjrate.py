"""Opponent-adjusted Elo performance ratings for every submission, with bootstrap CIs.
Reads analysis/summ/<tag>.jsonl (written by pull_all.py) and the leaderboard snapshot.
"""
import json, sys, csv, io, zipfile, math, random, statistics, collections, datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT

Z = zipfile.ZipFile(ROOT / "analysis" / "lb_snapshot_frozen.zip")
NAME = Z.namelist()[0]
LB, LASTSUB = {}, {}
for r in csv.DictReader(io.TextIOWrapper(Z.open(NAME), encoding="utf-8-sig")):
    LB[r["TeamName"]] = float(r["Score"])
    LASTSUB[r["TeamName"]] = r["LastSubmissionDate"]
SNAP = NAME.split("publicleaderboard-")[1][:19]

ORDER = ["v21.2", "v22", "v24", "v25", "v26", "v27", "v28", "rm", "v29",
         "v30", "v31", "v43c", "v32", "v33"]
# authoritative final public scores from `kaggle competitions submissions kaggriculture`
POSTED = {"v21.2": 1929.6, "v22": 207.8, "v24": 2744.3, "v25": 2679.1, "v26": 2679.5,
          "v27": 1638.7, "v28": 2450.3, "rm": 2266.6, "v29": 2015.8, "v30": 2294.7,
          "v31": 2058.0, "v43c": 1904.6, "v32": 2426.3, "v33": 1608.3}

def sc(r): return 1.0 if r["outcome"] == "WIN" else (0.5 if r["outcome"] == "TIE" else 0.0)

def elo_perf(rows):
    tgt = sum(sc(r) for r in rows)
    if tgt <= 0: return 0.0
    if tgt >= len(rows): return 4000.0
    lo, hi = -1000., 5000.
    for _ in range(120):
        mid = (lo + hi) / 2
        e = sum(1 / (1 + 10 ** ((r["opp_rating"] - mid) / 400)) for r in rows)
        if e < tgt: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def boot(rows, k=3000, seed=7):
    rnd = random.Random(seed); out = []
    for _ in range(k):
        s = [rows[rnd.randrange(len(rows))] for _ in rows]
        out.append(elo_perf(s))
    out.sort()
    return out

def load(tag):
    p = ROOT / "analysis" / "summ" / f"{tag}.jsonl"
    if not p.exists(): return []
    rows, seen = [], set()
    for line in open(p, encoding="utf-8"):
        try: r = json.loads(line)
        except Exception: continue
        if r["episode"] in seen: continue
        seen.add(r["episode"])
        r["opp_rating"] = LB.get(r["opponent"])
        r["opp_last"] = LASTSUB.get(r["opponent"])
        rows.append(r)
    return rows

def frozen(rows):
    """Opponents whose last submission predates the match -> today's rating describes
    the same agent we actually faced (modulo rating drift)."""
    out = []
    for r in rows:
        if r["opp_rating"] is None or not r["opp_last"]: continue
        if r["opp_last"][:19] < r["createTime"][:19]:
            out.append(r)
    return out

def line(tag, rows, label=""):
    kn = [r for r in rows if r["opp_rating"] is not None]
    if not kn:
        print(f"{tag:6s} {label:8s} NO DATA"); return None
    w = sum(1 for r in kn if r["outcome"] == "WIN")
    l = sum(1 for r in kn if r["outcome"] == "LOSS")
    t = len(kn) - w - l
    wr = (w + .5 * t) / len(kn)
    mo = statistics.mean(r["opp_rating"] for r in kn)
    e = elo_perf(kn); b = boot(kn)
    lo, hi = b[int(.025 * len(b))], b[int(.975 * len(b))]
    print(f"{tag:6s} {label:8s} n={len(kn):4d}/{len(rows):4d} {w:3d}-{l:3d}-{t:2d} "
          f"wr={wr:.3f} meanOpp={mo:6.0f} eloPerf={e:6.0f} [{lo:5.0f},{hi:5.0f}] posted={POSTED.get(tag,0):6.1f}")
    return {"tag": tag, "n": len(kn), "raw_n": len(rows), "w": w, "l": l, "t": t, "wr": wr,
            "meanOpp": mo, "perf": e, "lo": lo, "hi": hi, "rows": kn}

if __name__ == "__main__":
    print(f"leaderboard snapshot {SNAP}  teams={len(LB)}\n")
    res = {}
    print("=== ALL EPISODES (opponent = today's rating) ===")
    for tag in ORDER:
        rows = load(tag)
        if rows: res[tag] = line(tag, rows)
    print("\n=== FROZEN-OPPONENT SUBSET (opp last submission predates our match) ===")
    fres = {}
    for tag in ORDER:
        rows = load(tag)
        if rows:
            f = frozen(rows)
            if f: fres[tag] = line(tag, f, "frozen")
    json.dump({k: {kk: vv for kk, vv in v.items() if kk != "rows"} for k, v in res.items()},
              open(ROOT / "analysis" / "adjrate_all.json", "w"), indent=1)
    json.dump({k: {kk: vv for kk, vv in v.items() if kk != "rows"} for k, v in fres.items()},
              open(ROOT / "analysis" / "adjrate_frozen.json", "w"), indent=1)

    def diff(a, b, src, k=3000):
        A = src[a]["rows"]; B = src[b]["rows"]
        rnd = random.Random(101); d = []
        for _ in range(k):
            sa = [A[rnd.randrange(len(A))] for _ in A]
            sb = [B[rnd.randrange(len(B))] for _ in B]
            d.append(elo_perf(sa) - elo_perf(sb))
        d.sort()
        p = sum(1 for x in d if x > 0) / len(d)
        print(f"  {a} minus {b}: point={src[a]['perf']-src[b]['perf']:+.0f} "
              f"boot95=[{d[int(.025*len(d))]:+.0f},{d[int(.975*len(d))]:+.0f}] P({a}>{b})={p:.3f}")

    print("\n=== CONTROLLED EXPERIMENTS (all episodes) ===")
    for a, b in [("v29", "rm"), ("v32", "v43c"), ("v31", "v43c"), ("v33", "v43c"), ("v33", "v32")]:
        if a in res and b in res: diff(a, b, res)
    print("=== CONTROLLED EXPERIMENTS (frozen subset) ===")
    for a, b in [("v29", "rm"), ("v32", "v43c"), ("v31", "v43c")]:
        if a in fres and b in fres: diff(a, b, fres)
