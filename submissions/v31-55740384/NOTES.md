# v31

| | |
| :--- | :--- |
| Kaggle submission | `55740384` |
| Submitted | 2026-08-24 |
| Live score | pending |
| Chassis | Kaito v43 sparse-shop hybrid |
| `main.py` | 70,091 bytes, sha256 `7ed93c20a402d2f4` |

## Our layer

Mirror-gated one-step premium sell pull-forward. v43 replays a fixed 719-step tape, so in a mirror both sides post the same SELL on the same step and split a price they jointly depress. This reads our own tape one step ahead, sells into the undepressed book today, and cancels exactly that quantity tomorrow. Quantity is conserved — pure re-timing (LESSONS #12).

## How it did

Copy war 11-1 (+6,628). Non-clone neutrality: 22 paired comparisons, total drift 0.0000. vs v30 on fresh seeds 12-4 (+6,293). **Caveat: the gain over v30 is chassis, not edge** — stock v43 vs v30 was byte-identical to v31 vs v30 in 8/8 games. The edge only pays in mirrors.

## Files

- `__pycache__`
- `main.py`
- `submission.tar.gz`

---
Rebuild the archive with `py -3.12 tools/package.py v31-55740384 --check`.
