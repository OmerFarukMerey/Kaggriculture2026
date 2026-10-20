# v24

| | |
| :--- | :--- |
| Kaggle submission | `55428059` |
| Submitted | 2026-08-11 |
| Live score | 2744.3 |
| Chassis | Rayk C94 |
| `main.py` | 130,167 bytes, sha256 `032ab3cd0a1dabbf` |

## Our layer

Horizon-2 split escalation gated on an exact C94 route-track match, plus Boatlee-family detection with a premium front-run and a 711/712 flush.

## How it did

Our best-rating submission — but see the caveat: v24, v25 and v26 all silently **ran as stock C94** because of the entrypoint bug. Stock C94 alone was worth ~2814, so this number measures the chassis, not our layer.

## Files

- `build.py`
- `main.py`
- `tail.py`

---
Rebuild the archive with `py -3.12 tools/package.py v24-55428059 --check`.
