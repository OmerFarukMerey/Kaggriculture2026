# v28

| | |
| :--- | :--- |
| Kaggle submission | `55485346` |
| Submitted | 2026-08-13 |
| Live score | 2450.3 |
| Chassis | Rayk C94 |
| `main.py` | 135,284 bytes, sha256 `0dbff084d72291e5` |

## Our layer

v27 plus a double-yarn gated late conversion: a `yarn2` latch at step 288 that also swaps the 289/433 cow buys.

## How it did

Validated +2,450..+2,569 over v27 on double-yarn seeds, byte-identical when the gate is dormant.

## Files

- `main.py`
- `tail.py`

---
Rebuild the archive with `py -3.12 tools/package.py v28-55485346 --check`.
