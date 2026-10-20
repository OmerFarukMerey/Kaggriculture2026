"""Paired neutrality audit: run EDGED and STOCK against the same opponent,
same seed, same seat, in the same process. Print margins to the decimal plus
v31 edge telemetry.

usage: py -3.12 neutral_v31.py <opponent.py> <seed,seed,...>
"""
import importlib.util, sys, json
from pathlib import Path
HERE = Path(__file__).parent

def load(tag, filename):
    spec = importlib.util.spec_from_file_location(tag, HERE / filename)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def play(agent_file, opp_file, seed, a_seat, tag):
    from kaggle_environments import make
    a = load(f"A_{tag}", agent_file)
    b = load(f"B_{tag}", opp_file)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    pair = [a.agent, b.agent] if a_seat == 0 else [b.agent, a.agent]
    env.run(pair)
    r = [s.reward for s in env.steps[-1]]
    a_r, b_r = r[a_seat], r[1 - a_seat]
    tel = dict(getattr(a, "_V31_TELEMETRY", {})) if hasattr(a, "_V31_TELEMETRY") else None
    return float(a_r or 0), float(b_r or 0), tel

EDGED = "v31.py"

def main():
    global EDGED
    if len(sys.argv) > 3: EDGED = sys.argv[3]
    opp = sys.argv[1]
    seeds = [int(x) for x in sys.argv[2].split(",")]
    rows = []
    for seed in seeds:
        for seat in (0, 1):
            e_a, e_b, tel = play(EDGED, opp, seed, seat, f"e{seed}{seat}")
            s_a, s_b, _ = play("kaito_v43.py", opp, seed, seat, f"s{seed}{seat}")
            em, sm = e_a - e_b, s_a - s_b
            drift = em - sm
            print(f"opp={opp} seed={seed} seat={seat} | EDGED {e_a:.4f}/{e_b:.4f} m={em:+.4f} "
                  f"| STOCK {s_a:.4f}/{s_b:.4f} m={sm:+.4f} | DRIFT {drift:+.4f} | tel={tel}",
                  flush=True)
            rows.append({"opp": opp, "seed": seed, "seat": seat, "edged_a": e_a, "edged_b": e_b,
                         "stock_a": s_a, "stock_b": s_b, "edged_margin": em, "stock_margin": sm,
                         "drift": drift, "tel": tel})
    nz = [r for r in rows if r["drift"] != 0.0]
    print(f"SUMMARY {opp}: games={len(rows)} nonzero_drift={len(nz)} "
          f"mean_edged={sum(r['edged_margin'] for r in rows)/len(rows):+.4f} "
          f"mean_stock={sum(r['stock_margin'] for r in rows)/len(rows):+.4f} "
          f"total_abs_drift={sum(abs(r['drift']) for r in rows):.4f}", flush=True)
    out = HERE / f"neutral_{Path(EDGED).stem}_{Path(opp).stem}.json"
    out.write_text(json.dumps(rows, indent=1))
    print("wrote", out, flush=True)

main()
