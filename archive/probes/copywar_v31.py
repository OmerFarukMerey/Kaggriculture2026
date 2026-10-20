"""Copy war v31 vs stock kaito_v43 with edge telemetry + clone-distance probe."""
import importlib.util, sys
from pathlib import Path
HERE = Path(__file__).parent

def load(tag, filename):
    spec = importlib.util.spec_from_file_location(tag, HERE / filename)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

from kaggle_environments import make
seeds = [int(x) for x in sys.argv[1].split(",")]
opp = sys.argv[2] if len(sys.argv) > 2 else "kaito_v43.py"
wins = losses = ties = 0; margins = []
for seed in seeds:
    for a_seat in (0, 1):
        a = load(f"a_{seed}_{a_seat}", "v31.py")
        b = load(f"b_{seed}_{a_seat}", opp)
        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
        pair = [a.agent, b.agent] if a_seat == 0 else [b.agent, a.agent]
        env.run(pair)
        r = [s.reward for s in env.steps[-1]]
        ar, br = r[a_seat], r[1 - a_seat]
        m = (ar or 0) - (br or 0); margins.append(m)
        wins += m > 0; losses += m < 0; ties += m == 0
        t = a._V31_TELEMETRY
        print(f"seed={seed} A_seat={a_seat} A={ar} B={br} margin={m:+.0f} "
              f"{'WIN' if m>0 else 'TIE' if m==0 else 'LOSS'} | borrows={t['borrows']} units={t['units']} "
              f"repays={t['repays']} gated_out={t['gated_out']} last_cd={t['last_distance']}", flush=True)
print(f"v31.py vs {opp}: W-L-T {wins}-{losses}-{ties}, mean margin {sum(margins)/len(margins):+.1f}", flush=True)
