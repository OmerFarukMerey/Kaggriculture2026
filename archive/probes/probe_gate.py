import importlib.util, sys, json
from pathlib import Path
HERE = Path(__file__).parent
def load(tag, fn):
    spec = importlib.util.spec_from_file_location(tag, HERE / fn)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
from kaggle_environments import make
a = load("pa", "kaito_v43.py"); b = load("pb", "kaito_v43.py")
import v19_terminal as vt   # whichever copy; functions are pure
log = {}
def wrap(mod, seat):
    inner = mod.agent
    def w(obs, configuration=None):
        st = int(obs.get("step", 0) or 0)
        if st >= 690:
            log.setdefault(seat, {})[st] = {
                "cd": vt.clone_distance(obs),
                "shed": dict((obs.get("private", {}) or {}).get("shed", {}) or {}),
            }
        return inner(obs, configuration)
    return w
env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 5000}, debug=False)
env.run([wrap(a,0), wrap(b,1)])
for seat in (0,1):
    print("seat", seat)
    for st in sorted(log[seat]):
        if st in (690, 700, 710, 715, 716, 717, 718, 719):
            e = log[seat][st]
            tot = sum(e["shed"].values())
            print(f"  step={st} clone_distance={e['cd']} shed_total={tot} shed={ {k:v for k,v in e['shed'].items() if v} }")
