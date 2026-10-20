# v25

| | |
| :--- | :--- |
| Kaggle submission | `55432745` |
| Submitted | 2026-08-11 |
| Live score | 2679.1 |
| Chassis | Rayk C94 |
| `main.py` | 132,984 bytes, sha256 `49721663c9c2e036` |

## Our layer

Adds a yarn-adaptive COW→SHEEP swap on the C94 trace (steps 161/168/192 plus a PLACE/PICKUP window).

## How it did

Also ran as stock C94 live. Offline it moved yarn seeds vs Boatlee from 0-6 (mean −8,445) to 2-4 (mean −1,467).

## Files

- `build.py`
- `main.py`
- `tail.py`

---
Rebuild the archive with `py -3.12 tools/package.py v25-55432745 --check`.
