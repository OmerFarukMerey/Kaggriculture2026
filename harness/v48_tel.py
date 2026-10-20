"""Report v48 CloneSellPreemption telemetry against a given opponent."""
import sys, json, importlib.util
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import resolve_agent

def load(tag, p):
    s = importlib.util.spec_from_file_location(tag, p); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m

opp = sys.argv[1]; seeds = [int(x) for x in sys.argv[2:]] or [5000]
from kaggle_environments import make
for seed in seeds:
    v48 = load(f"v48_{seed}", resolve_agent("kaito_v48"))
    om  = load(f"o_{seed}", resolve_agent(opp))
    pol = v48._V48_POLICY
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([v48.agent, om.agent])
    r = [s.reward for s in env.steps[-1]]
    t = dict(pol.preemption.telemetry)
    print(f"seed={seed} opp={opp} v48={r[0]} opp={r[1]} m={(r[0] or 0)-(r[1] or 0):+.0f} "
          f"latches={t['latches']} near_turns={t['near_turns']} preempt_turns={t['preempt_turns']} "
          f"preempt_units={t['preempt_units']} repaid={t['repaid_units']} games={t['games']}", flush=True)
