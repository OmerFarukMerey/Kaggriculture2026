"""Summarise rr_panel output: per-agent field W-L-T and a pairwise matrix (A's wins-losses)."""
import json, sys
from collections import defaultdict

res = [r for f in sys.argv[1:] for r in json.load(open(f))]
tot = defaultdict(lambda: [0, 0, 0, 0, 0.0])  # w l t invalid margin
pair = defaultdict(lambda: [0, 0, 0])
bad = []
for r in res:
    a, b = r["a"], r["b"]
    if not r["valid"]:
        bad.append((a, b, r["seed"], r["seat"], str(r["failures"])[:200]))
        # attribute invalidity to the seat that failed if known
        continue
    m = r["m"]
    for x, y, mm in ((a, b, m), (b, a, -m)):
        t = tot[x]
        if mm > 0: t[0] += 1; pair[(x, y)][0] += 1
        elif mm < 0: t[1] += 1; pair[(x, y)][1] += 1
        else: t[2] += 1; pair[(x, y)][2] += 1
        t[4] += mm
names = sorted(tot, key=lambda n: -(tot[n][0] + 0.5 * tot[n][2]) / max(1, sum(tot[n][:3])))
print(f"{'agent':12s} {'W':>4} {'L':>4} {'T':>3} {'score%':>7} {'meanM':>8}")
for n in names:
    w, l, t, _, m = tot[n]; g = w + l + t
    print(f"{n:12s} {w:>4} {l:>4} {t:>3} {100*(w+t/2)/max(g,1):>6.1f}% {m/max(g,1):>8.0f}")
print("\nmatrix (row W-L vs col):")
print(" " * 10 + "".join(f"{n[:7]:>8}" for n in names))
for x in names:
    print(f"{x[:10]:10s}" + "".join(f"{(str(pair[(x,y)][0])+'-'+str(pair[(x,y)][1])) if (x,y) in pair else '.':>8}" for y in names))
if bad:
    print(f"\n{len(bad)} invalid cells:")
    for b in bad[:30]: print("  ", b)
