"""Evaluate v21.2 (main.py) against the public v21.1 artifact and baselines.

Usage: python evaluate.py [n_seeds] [mode]
  mode: all | h2h | self | starter
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reset_module_state(module):
    # Both agents keep per-episode dict state keyed by seat; fresh episodes
    # reset on step 0, but reload defensively between games anyway.
    for attr in ("_WEED_STATE", "_MIRROR_STATE"):
        if hasattr(module, attr):
            getattr(module, attr).update({0: {}, 1: {}})


def play(agent0, agent1, seed):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([agent0, agent1])
    final = env.steps[-1]
    return [s.reward for s in final], [s.status for s in final]


def main():
    n_seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    mode = sys.argv[2] if len(sys.argv) > 2 else "all"
    seeds = [1000 + 7 * k for k in range(n_seeds)]

    ours = load("ours", "main.py")
    pub = load("pub", "public_v211.py")

    if mode in ("all", "h2h"):
        wins = losses = ties = 0
        margins = []
        for seed in seeds:
            for our_seat in (0, 1):
                reset_module_state(ours)
                reset_module_state(pub)
                pair = [ours.agent, pub.agent] if our_seat == 0 else [pub.agent, ours.agent]
                rewards, status = play(pair[0], pair[1], seed)
                our_r, pub_r = rewards[our_seat], rewards[1 - our_seat]
                margin = (our_r or 0) - (pub_r or 0)
                margins.append(margin)
                outcome = "WIN" if margin > 0 else ("TIE" if margin == 0 else "LOSS")
                wins += margin > 0
                losses += margin < 0
                ties += margin == 0
                print(f"[h2h] seed={seed} our_seat={our_seat} ours={our_r} "
                      f"public={pub_r} margin={margin:+.0f} {outcome} status={status}")
        print(f"[h2h] W-L-T = {wins}-{losses}-{ties}, "
              f"mean margin = {sum(margins) / len(margins):+.1f}")

    if mode in ("all", "self"):
        reset_module_state(ours)
        rewards, status = play(ours.agent, ours.agent, seeds[0])
        print(f"[self] rewards={rewards} status={status} "
              f"{'TIE-OK' if rewards[0] == rewards[1] else 'ASYMMETRY!'}")

    if mode in ("all", "starter"):
        for our_seat in (0, 1):
            reset_module_state(ours)
            pair = [ours.agent, "starter"] if our_seat == 0 else ["starter", ours.agent]
            rewards, status = play(pair[0], pair[1], seeds[0])
            print(f"[starter] our_seat={our_seat} rewards={rewards} status={status}")


if __name__ == "__main__":
    main()
