"""Adversarial loader verification: file-loaded vs module-imported, same seed.
Usage: py -3.12 verify_loader.py <case> <seed>   (one case per fresh process)"""
import importlib.util, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[2]

def load(tag, filename):
    spec = importlib.util.spec_from_file_location(tag, HERE / filename)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def run(pair, seed):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run(pair)
    return [s.reward for s in env.steps[-1]]

F = lambda n: str(HERE / n)

CASES = {
 "file_v31_k43": lambda s: run([F("v31.py"), F("kaito_v43.py")], s),
 "mod_v31_k43":  lambda s: run([load("mA","v31.py").agent, load("mB","kaito_v43.py").agent], s),
 "file_k43_v31": lambda s: run([F("kaito_v43.py"), F("v31.py")], s),
 "mod_k43_v31":  lambda s: run([load("mA","kaito_v43.py").agent, load("mB","v31.py").agent], s),
 "file_k43_k43": lambda s: run([F("kaito_v43.py"), F("kaito_v43.py")], s),
 "mod_k43_k43":  lambda s: run([load("mA","kaito_v43.py").agent, load("mB","kaito_v43.py").agent], s),
 "file_v31_v31": lambda s: run([F("v31.py"), F("v31.py")], s),
 "mod_v31_v31":  lambda s: run([load("mA","v31.py").agent, load("mB","v31.py").agent], s),
 "file_v31_tetsu": lambda s: run([F("v31.py"), F("tetsu_esc.py")], s),
 "mod_v31_tetsu":  lambda s: run([load("mA","v31.py").agent, load("mB","tetsu_esc.py").agent], s),
}

case = sys.argv[1]; seed = int(sys.argv[2])
r = CASES[case](seed)
print(f"RESULT seed={seed} {case}: p0={r[0]} p1={r[1]} margin_p0={(r[0] or 0)-(r[1] or 0):+.0f}", flush=True)
