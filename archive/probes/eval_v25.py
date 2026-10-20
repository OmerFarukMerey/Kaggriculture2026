"""Evaluate the v25 portfolio dispatcher on explicit yarn/plain seeds."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).parent
YARN_SEEDS = [9009, 9011, 9022, 9025]
PLAIN_SEEDS = [9001, 9002]


def load(tag, filename):
    spec = importlib.util.spec_from_file_location(tag, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def game(file_a, file_b, seed, a_seat, tag):
    from kaggle_environments import make
    # Fresh dispatcher per game; clear cached sub-agent modules so their
    # per-seat state cannot leak across games.
    for name in ("v22_agent", "v24_agent"):
        sys.modules.pop(name, None)
    a = load(f"a{tag}", file_a)
    for name in ("v22_agent", "v24_agent"):
        sys.modules.pop(name, None)
    b = load(f"b{tag}", file_b)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    pair = [a.agent, b.agent] if a_seat == 0 else [b.agent, a.agent]
    env.run(pair)
    rewards = [s.reward for s in env.steps[-1]]
    return rewards[a_seat], rewards[1 - a_seat]


def series(file_a, file_b, seeds, label):
    wins = losses = ties = 0
    margins = []
    for k, seed in enumerate(seeds):
        for a_seat in (0, 1):
            a_r, b_r = game(file_a, file_b, seed, a_seat, f"{label}{k}{a_seat}")
            margin = (a_r or 0) - (b_r or 0)
            margins.append(margin)
            wins += margin > 0
            losses += margin < 0
            ties += margin == 0
            print(f"  seed={seed} A_seat={a_seat} A={a_r} B={b_r} {margin:+.0f}", flush=True)
    print(f"[{label}] {file_a} vs {file_b}: {wins}-{losses}-{ties}, "
          f"mean {sum(margins) / len(margins):+.1f}", flush=True)


which = sys.argv[1] if len(sys.argv) > 1 else "all"
if which in ("all", "yarn"):
    series("main_v25.py", "boatlee_v16.py", YARN_SEEDS[:3], "yarn-vs-boat")
    series("main_v25.py", "rayk_c94.py", YARN_SEEDS[:2], "yarn-vs-c94")
    series("main_v25.py", "v24_agent.py", YARN_SEEDS[:2], "yarn-vs-v24")
if which in ("all", "plain"):
    series("main_v25.py", "v24_agent.py", PLAIN_SEEDS, "plain-vs-v24")
if which in ("all", "self"):
    a_r, b_r = game("main_v25.py", "main_v25.py", YARN_SEEDS[0], 0, "selfyarn")
    print(f"[self yarn] {a_r} vs {b_r} {'TIE-OK' if a_r == b_r else 'ASYMMETRY!'}")
