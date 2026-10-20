"""Adversarial verification panel: seeds DISJOINT from every harness panel.

    py -3.12 harness/verify_panel.py <A> <B> [--half 0|1]

Asserts disjointness from winrate.PANELS in code before running a single game.
"""
import importlib.util, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import resolve_agent
from winrate import PANELS

# 12 seeds, none of which appear in wide/near/far, none adjacent to them.
VERIFY = [60013, 61403, 62497, 63997, 65003, 66103,
          67213, 68389, 69499, 70607, 71711, 72823]

_used = set()
for _p in PANELS.values():
    _used |= set(_p)
_clash = sorted(set(VERIFY) & _used)
assert not _clash, f"PANEL NOT DISJOINT: {_clash}"
# also assert no seed is within 20 of a used seed (adjacent seeds share shop draws)
_near = sorted(s for s in VERIFY for u in _used if abs(s - u) <= 20)
assert not _near, f"PANEL TOO CLOSE TO USED SEEDS: {_near}"
print(f"DISJOINTNESS ASSERTED: {len(VERIFY)} verify seeds vs {len(_used)} used seeds; "
      f"intersection=0, min|delta|={min(abs(s-u) for s in VERIFY for u in _used)}", flush=True)


def load(tag, path):
    spec = importlib.util.spec_from_file_location(tag, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    a_ref, b_ref = sys.argv[1], sys.argv[2]
    file_a, file_b = resolve_agent(a_ref), resolve_agent(b_ref)
    seeds = VERIFY
    if "--half" in sys.argv:
        h = int(sys.argv[sys.argv.index("--half") + 1])
        seeds = VERIFY[:6] if h == 0 else VERIFY[6:]
    from kaggle_environments import make
    w = l = t = 0
    margins, per_seed, rows = [], [], []
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
            margins.append(m); cells.append(m)
            w += m > 0; l += m < 0; t += m == 0
            rows.append({"seed": seed, "seat": a_seat, "a": a_r, "b": b_r, "margin": m})
            print(f"  seed={seed:>6} seat={a_seat} A={a_r:>9} B={b_r:>9} {m:+9.0f} "
                  f"{'W' if m>0 else 'T' if m==0 else 'L'}", flush=True)
        per_seed.append((seed, cells))
        if cells[0] == cells[1]:
            print(f"  seed={seed:>6} NOTE seat-symmetric (1 effective sample)", flush=True)
    n = w + l + t
    eff = sum(1 if c[0] == c[1] else 2 for _, c in per_seed)
    print(f"\nA={a_ref} vs B={b_ref}  panel=VERIFY(disjoint)")
    print(f"  W-L-T        {w}-{l}-{t}  of {n} games ({eff} effective samples)")
    print(f"  wr(half)     {(w+0.5*t)/n:.3f}")
    print(f"  mean margin  {sum(margins)/len(margins):+.0f}  (diagnostic only)")
    out = Path(__file__).resolve().parent.parent / "analysis" / f"verify_{Path(file_a).stem}_vs_{Path(file_b).stem}_{'-'.join(str(s) for s in seeds[:1])}.json"
    out.write_text(json.dumps({"a": str(file_a), "b": str(file_b), "seeds": seeds, "rows": rows,
                               "W": w, "L": l, "T": t, "eff": eff}, indent=1))
    print(f"  wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
