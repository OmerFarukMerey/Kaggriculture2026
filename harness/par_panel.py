"""Parallel W-L-T panel runner. Runs (A,B,seed,seat) cells across processes.

    py -3.12 harness/par_panel.py <outjson> <workers> <A:B[:seats]> ...
seats: "2" (default, both seats) or "1". Optional --seeds accepts comma-separated seeds.
"""
import hashlib, json, math, sys, time, traceback
from importlib.metadata import version
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import resolve_agent

PANELS={"wide":[5000, 5013, 5026, 7001, 7013, 7027, 7041, 9001, 9007, 9101,
        9203, 9311, 11017, 13049, 17093, 19121],
  "near":[5000,5013,5026,5039,5052,5065,5078,5091],
  "far":[21031,23087,29101,31513,37217,41603,43991,47237]}
WIDE=PANELS["wide"]




def cell(job):
    a_ref, b_ref, fa, fb, seed, a_seat = job
    started = time.perf_counter()
    result = dict(a=a_ref, b=b_ref, seed=seed, seat=a_seat, ar=None, br=None, m=None,
                  valid=False, failures=[],
                  hashes=[hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (fa, fb)])
    try:
        from kaggle_environments import make
        from kaggle_environments.agent import build_agent
        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
        # Retain Kaggle's lazy, timed file loader; reject non-object returns before
        # the engine silently replaces them with its default PASS action.
        def monitored(path, seat):
            loaded, _ = build_agent(path, env.agents, env.name)
            reported = False

            def act(observation, configuration):
                nonlocal reported
                action = loaded(observation, configuration)
                if not isinstance(action, dict) and not reported:
                    result["failures"].append(dict(
                        step=int(observation.step), seat=seat,
                        error=f"Expected action object, got {type(action).__name__}"))
                    reported = True
                return action

            return act

        files = [fa, fb] if a_seat == 0 else [fb, fa]
        env.run([monitored(path, seat) for seat, path in enumerate(files)])
        rewards = [s.reward for s in env.steps[-1]]
        result.update(ar=rewards[a_seat], br=rewards[1-a_seat], steps=len(env.steps),
                      statuses=[s.status for s in env.steps[-1]],
                      configuration=dict(env.configuration), engine=version("kaggle-environments"))
        for t, states in enumerate(env.steps):
            for seat, state in enumerate(states):
                if state.status in ("ERROR", "INVALID", "TIMEOUT"):
                    result["failures"].append(dict(step=t, seat=seat, status=state.status))
        durations = [[], []]
        for t, logs in enumerate(env.logs):
            for seat, log in enumerate(logs[:2]):
                durations[seat].append(log.get("duration", 0))
                error = log.get("stderr", "")
                if "Traceback (most recent call last)" in error:
                    result["failures"].append(dict(log_index=t, seat=seat, error=error[-2000:]))
        result["max_action_seconds"] = [max(d, default=0) for d in durations]
        result["overage_used"] = [sum(max(0, t-env.configuration.actTimeout) for t in d)
                                  for d in durations]
        complete = len(env.steps) == 720 and all(s.status == "DONE" for s in env.steps[-1])
        finite = all(isinstance(r, (int, float)) and math.isfinite(r) for r in rewards)
        result["valid"] = complete and finite and not result["failures"]
        if result["valid"]:
            result["m"] = result["ar"] - result["br"]
    except Exception:
        result["failures"].append(dict(error=traceback.format_exc()))
    result["elapsed"] = time.perf_counter() - started
    return result


def main():
    out, workers = sys.argv[1], int(sys.argv[2])
    panel = "wide"
    if "--panel" in sys.argv: panel = sys.argv[sys.argv.index("--panel")+1]
    jobs = []
    seeds = PANELS[panel]
    if "--seeds" in sys.argv:
        seeds = [int(s) for s in sys.argv[sys.argv.index("--seeds")+1].split(",")]
    for spec in [x for x in sys.argv[3:] if ":" in x]:
        parts = spec.split(":")
        a_ref, b_ref = parts[0], parts[1]
        seats = (0,) if len(parts) > 2 and parts[2] == "1" else (0, 1)
        fa, fb = str(resolve_agent(a_ref)), str(resolve_agent(b_ref))
        for s in seeds:
            for st in seats:
                jobs.append((a_ref, b_ref, fa, fb, s, st))
    print(f"{len(jobs)} cells, {workers} workers", flush=True)
    res = []
    with ProcessPoolExecutor(max_workers=workers, max_tasks_per_child=1) as ex:
        for i, r in enumerate(ex.map(cell, jobs)):
            res.append(r)
            margin = f"{r['m']:+.0f}" if r["valid"] else "INVALID"
            print(f"[{i+1}/{len(jobs)}] {r['a']} vs {r['b']} seed={r['seed']} seat={r['seat']} "
                  f"A={r['ar']} B={r['br']} {margin}", flush=True)
            Path(out).write_text(json.dumps(res))
    Path(out).write_text(json.dumps(res))
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
