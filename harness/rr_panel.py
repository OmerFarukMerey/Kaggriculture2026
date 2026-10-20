"""Round-robin / list-driven W-L-T runner reusing par_panel.cell (Kaggle lazy file loader, fresh process per game).

    py -3.12 harness/rr_panel.py <spec.json> <out.json> <workers>
spec.json: {"agents": {alias: path}, "pairs": [[a, b], ...] | "all", "seeds": [...], "seats": [0, 1]}
"""
import itertools, json, sys, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from par_panel import cell


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    out, workers = Path(sys.argv[2]), int(sys.argv[3])
    agents = spec["agents"]
    pairs = spec.get("pairs", "all")
    if pairs == "all":
        pairs = list(itertools.combinations(sorted(agents), 2))
    seats = spec.get("seats", [0, 1])
    jobs = [(a, b, agents[a], agents[b], s, st) for a, b in pairs for s in spec["seeds"] for st in seats]
    done = []
    if out.exists() and "--resume" in sys.argv:
        done = json.loads(out.read_text())
        have = {(r["a"], r["b"], r["seed"], r["seat"]) for r in done}
        jobs = [j for j in jobs if (j[0], j[1], j[4], j[5]) not in have]
    print(f"{len(jobs)} cells, {workers} workers", flush=True)
    res, t0 = list(done), time.time()
    with ProcessPoolExecutor(max_workers=workers, max_tasks_per_child=1) as ex:
        for i, r in enumerate(ex.map(cell, jobs, chunksize=1)):
            r.pop("hashes", None)
            res.append(r)
            m = f"{r['m']:+.0f}" if r["valid"] else "INVALID " + json.dumps(r["failures"])[:300]
            print(f"[{i+1}/{len(jobs)} {time.time()-t0:.0f}s] {r['a']} vs {r['b']} s={r['seed']} st={r['seat']} {m}", flush=True)
            if i % 20 == 0:
                out.write_text(json.dumps(res))
    out.write_text(json.dumps(res))
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
