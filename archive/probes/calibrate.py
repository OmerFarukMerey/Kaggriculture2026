"""Calibration: find which prototype matches the deployed route, and the
distance distribution of an exact-copy opponent to that prototype (self-play).

Run with a Python where kaggle-environments is installed.
"""
import importlib.util
import json
import statistics
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("pub", HERE / "public_v211.py")
pub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)

from kaggle_environments import make

env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 12345}, debug=False)
env.run([pub.agent, pub.agent])
print("self-play rewards:", [s.reward for s in env.steps[-1]])

# For each step, farm 0's public signature vs every prototype.
per_proto = {i: [] for i in range(len(pub._PROTOTYPES))}
for step in range(48, 719, 10):
    obs = env.steps[step][0].observation
    farm = obs["farms"][0]
    sig = pub._public_route_signature(farm)
    for i, proto in enumerate(pub._PROTOTYPES):
        sigs = proto["signatures"]
        if step < len(sigs):
            per_proto[i].append(pub._signature_distance(sig, sigs[step]))

means = sorted((statistics.mean(v), i) for i, v in per_proto.items() if v)
print("closest prototypes (mean distance, index):", [(round(m, 2), i) for m, i in means[:5]])
best = means[0][1]
dists = per_proto[best]
print(f"prototype {best}: mean={statistics.mean(dists):.2f} max={max(dists):.2f} "
      f"p90={sorted(dists)[int(0.9 * len(dists))]:.2f}")

# Distance of a NON-copy opponent (built-in starter) to that prototype, as the
# false-positive margin check.
env2 = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 12345}, debug=False)
env2.run([pub.agent, "starter"])
print("vs starter rewards:", [s.reward for s in env2.steps[-1]])
non_copy = []
for step in range(96, 719, 10):
    obs = env2.steps[step][0].observation
    sig = pub._public_route_signature(obs["farms"][1])
    sigs = pub._PROTOTYPES[best]["signatures"]
    if step < len(sigs):
        non_copy.append(pub._signature_distance(sig, sigs[step]))
print(f"starter-vs-proto{best}: min={min(non_copy):.2f} mean={statistics.mean(non_copy):.2f}")

json.dump({"best": best, "copy_max": max(dists), "noncopy_min": min(non_copy)},
          open(HERE / "calibration.json", "w"))
print("saved calibration.json")
