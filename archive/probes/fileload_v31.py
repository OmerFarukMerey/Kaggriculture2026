"""FILE-LOADED verification: env.run uses Kaggle's own get_last_callable path."""
import sys
from kaggle_environments import make

SEED = 5000
def run(a, b, seed=SEED):
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([a, b])
    r = [s.reward for s in env.steps[-1]]
    return r

for pair in (["v31.py", "kaito_v43.py"],
             ["kaito_v43.py", "kaito_v43.py"],
             ["kaito_v43.py", "v31.py"]):
    r = run(*pair)
    print(f"FILE-LOADED {pair[0]} vs {pair[1]} seed={SEED}: {r[0]} vs {r[1]} margin(seat0-seat1)={(r[0] or 0)-(r[1] or 0):+.0f}", flush=True)
