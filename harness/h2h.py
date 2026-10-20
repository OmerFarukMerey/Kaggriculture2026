"""Head-to-head evaluation between two agents.

    py -3.12 harness/h2h.py <A> <B> [n_seeds]

<A> and <B> may be paths, bare filenames in agents/public/, or submission
aliases such as "v30". Each seed is played twice, once per seat, because the
engine is not seat-symmetric. A fresh module instance is loaded per game so no
per-seat state leaks between games.
"""
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import resolve_agent  # noqa: E402


def load(tag, path):
    spec = importlib.util.spec_from_file_location(tag, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    if len(sys.argv) < 3:
        print(__doc__.strip())
        return 2
    file_a, file_b = resolve_agent(sys.argv[1]), resolve_agent(sys.argv[2])
    n_seeds = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    from kaggle_environments import make

    wins = losses = ties = 0
    margins = []
    for k in range(n_seeds):
        seed = 5000 + 13 * k
        for a_seat in (0, 1):
            a_mod = load(f"agent_a_{k}_{a_seat}", file_a)
            b_mod = load(f"agent_b_{k}_{a_seat}", file_b)
            env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
            pair = [a_mod.agent, b_mod.agent] if a_seat == 0 else [b_mod.agent, a_mod.agent]
            env.run(pair)
            rewards = [s.reward for s in env.steps[-1]]
            a_r, b_r = rewards[a_seat], rewards[1 - a_seat]
            margin = (a_r or 0) - (b_r or 0)
            margins.append(margin)
            wins += margin > 0
            losses += margin < 0
            ties += margin == 0
            print(f"seed={seed} A_seat={a_seat} A={a_r} B={b_r} margin={margin:+.0f} "
                  f"{'WIN' if margin > 0 else 'TIE' if margin == 0 else 'LOSS'}", flush=True)
    print(f"A={file_a.name} ({sys.argv[1]}) vs B={file_b.name} ({sys.argv[2]}): "
          f"W-L-T {wins}-{losses}-{ties}, mean margin {sum(margins) / len(margins):+.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
