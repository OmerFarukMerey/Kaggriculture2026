"""Record Boatlee V16's per-step public farm signature tracks (yarn on/off)
via self-play, plus end-of-game shed leftovers (terminal-dump upside).
"""
import base64
import importlib.util
import json
import zlib
from pathlib import Path

HERE = Path(__file__).parent


def load(tag, filename):
    spec = importlib.util.spec_from_file_location(tag, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pub = load("pub_sig", "public_v211.py")  # for _public_route_signature
from kaggle_environments import make

tracks = {}
leftovers = {}
seed = 3000
while (True not in tracks or False not in tracks) and seed < 3040:
    b0 = load(f"b0_{seed}", "boatlee_v16.py")
    b1 = load(f"b1_{seed}", "boatlee_v16.py")
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([b0.agent, b1.agent])
    yarn = bool(b0._V16_ROUTE_STATE[0].get("yarn"))
    final = env.steps[-1]
    rewards = [s.reward for s in final]
    shed = env.steps[-1][0].observation.get("private", {})
    print(f"seed={seed} yarn={yarn} rewards={rewards}", flush=True)
    if yarn not in tracks:
        sigs = []
        for step in range(719):
            # steps[t].observation is what the agent sees AT step t (matches
            # the runtime convention used by the v21.1 prototypes).
            obs = env.steps[min(step, len(env.steps) - 1)][0].observation
            sigs.append(pub._public_route_signature(obs["farms"][0]))
        tracks[yarn] = sigs
        # shed leftovers at final step (unsold value)
        last_obs = env.steps[-1][0].observation
        leftovers[yarn] = dict(last_obs.get("private", {}).get("shed", {}) or {})
    seed += 1

print("tracks recorded:", sorted(tracks))
print("final shed leftovers:", leftovers)
payload = {"yarn_on": tracks.get(True), "yarn_off": tracks.get(False)}
blob = base64.b85encode(zlib.compress(json.dumps(payload).encode(), 9)).decode()
Path(HERE / "boatlee_tracks.b85").write_text(blob, encoding="utf-8")
print("payload chars:", len(blob))
