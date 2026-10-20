# v29

| | |
| :--- | :--- |
| Kaggle submission | `55508152` |
| Submitted | 2026-08-14 |
| Live score | 2015.8 |
| Chassis | read-the-market |
| `main.py` | 61,979 bytes, sha256 `1299fb8279448937` |

## Our layer

Flips the chassis' own dormant `_PREEMPT_ENABLED` to True — a debt-accounted preempt gated on clone-distance ≤6.

## How it did

Beat the stock chassis 6-0 (+1,290 copy war) while staying bit-identical against non-clones. Live: 169-79-4 (67%) over 252 episodes, mean margin +5,857 — the best *field* performance of any submission here.

## Files

- `main.py`

---
Rebuild the archive with `py -3.12 tools/package.py v29-55508152 --check`.
