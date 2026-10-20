"""Rank two agents by WIN RATE over a wide seed panel.

    py -3.12 harness/winrate.py <A> <B> [n_seeds] [--panel wide|near|far]

Kaggriculture rating depends ONLY on win/loss/tie -- the coin margin does not
affect it (docs/LESSONS.md #6a). This reports the W-L-T record as the headline
number and relegates margin to a diagnostic, which is the opposite of h2h.py.

Seeds are spread across a wide range rather than the 5000+13k arithmetic run,
because adjacent seeds share shop draws and overstate agreement. Every seed is
played twice, once per seat.
"""
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import resolve_agent  # noqa: E402

PANELS = {
    "wide": [5000, 5013, 5026, 7001, 7013, 7027, 7041, 9001, 9007, 9101,
             9203, 9311, 11017, 13049, 17093, 19121],
    "near": [5000, 5013, 5026, 5039, 5052, 5065, 5078, 5091],
    "far":  [21031, 23087, 29101, 31513, 37217, 41603, 43991, 47237],
}


def load(tag, path):
    spec = importlib.util.spec_from_file_location(tag, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    if len(sys.argv) < 3:
        print(__doc__.strip())
        return 2
    a_ref, b_ref = sys.argv[1], sys.argv[2]
    file_a, file_b = resolve_agent(a_ref), resolve_agent(b_ref)
    panel = "wide"
    if "--panel" in sys.argv:
        panel = sys.argv[sys.argv.index("--panel") + 1]
    seeds = PANELS[panel]
    rest = [a for a in sys.argv[3:] if not a.startswith("--")]
    if rest and rest[0].isdigit():
        seeds = seeds[: int(rest[0])]

    from kaggle_environments import make
    w = l = t = 0
    margins = []
    per_seed = []
    for k, seed in enumerate(seeds):
        cells = []
        for a_seat in (0, 1):
            a_mod = load(f"a_{k}_{a_seat}", file_a)
            b_mod = load(f"b_{k}_{a_seat}", file_b)
            env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
            env.run([a_mod.agent, b_mod.agent] if a_seat == 0 else [b_mod.agent, a_mod.agent])
            r = [s.reward for s in env.steps[-1]]
            a_r, b_r = r[a_seat], r[1 - a_seat]
            m = (a_r or 0) - (b_r or 0)
            margins.append(m)
            w += m > 0
            l += m < 0
            t += m == 0
            cells.append(m)
            print(f"  seed={seed:>6} seat={a_seat} A={a_r:>9} B={b_r:>9} {m:+9.0f} "
                  f"{'W' if m > 0 else 'T' if m == 0 else 'L'}", flush=True)
        per_seed.append((seed, cells))
        if cells[0] == cells[1]:
            print(f"  seed={seed:>6} NOTE seat-symmetric (1 effective sample, not 2)", flush=True)

    n = w + l + t
    eff = sum(1 if c[0] == c[1] else 2 for _, c in per_seed)
    print(f"\nA={a_ref} vs B={b_ref}  panel={panel}")
    print(f"  W-L-T        {w}-{l}-{t}  of {n} games ({eff} effective samples)")
    print(f"  WIN RATE     {w / n:.3f}   (ties counted as losses: {w / n:.3f}; as half: {(w + 0.5 * t) / n:.3f})")
    print(f"  mean margin  {sum(margins) / len(margins):+.0f}   <- diagnostic only, does NOT affect rating")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
