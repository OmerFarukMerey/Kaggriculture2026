"""Seeded head-to-head: python h2hs.py fileA.py fileB.py "s1,s2,s3" [seats]
seats: "both" (default) or "0" or "1"
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).parent


def load(tag, filename):
    spec = importlib.util.spec_from_file_location(tag, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    file_a, file_b = sys.argv[1], sys.argv[2]
    seeds = [int(x) for x in sys.argv[3].split(",")]
    seats = sys.argv[4] if len(sys.argv) > 4 else "both"
    seat_list = (0, 1) if seats == "both" else (int(seats),)
    from kaggle_environments import make

    wins = losses = ties = 0
    margins = []
    for seed in seeds:
        for a_seat in seat_list:
            a_mod = load(f"agent_a_{seed}_{a_seat}", file_a)
            b_mod = load(f"agent_b_{seed}_{a_seat}", file_b)
            env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
            pair = [a_mod.agent, b_mod.agent] if a_seat == 0 else [b_mod.agent, a_mod.agent]
            env.run(pair)
            final = env.steps[-1]
            rewards = [s.reward for s in final]
            a_r, b_r = rewards[a_seat], rewards[1 - a_seat]
            margin = (a_r or 0) - (b_r or 0)
            margins.append(margin)
            wins += margin > 0
            losses += margin < 0
            ties += margin == 0
            print(f"seed={seed} A_seat={a_seat} A={a_r} B={b_r} margin={margin:+.0f} "
                  f"{'WIN' if margin > 0 else 'TIE' if margin == 0 else 'LOSS'}", flush=True)
    print(f"A={file_a} vs B={file_b}: W-L-T {wins}-{losses}-{ties}, "
          f"mean margin {sum(margins) / len(margins):+.1f}", flush=True)


if __name__ == "__main__":
    main()
