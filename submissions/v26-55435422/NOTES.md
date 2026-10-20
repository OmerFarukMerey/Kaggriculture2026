# v26

| | |
| :--- | :--- |
| Kaggle submission | `55435422` |
| Submitted | 2026-08-11 |
| Live score | 2679.5 |
| Chassis | Rayk C94 |
| `main.py` | 133,703 bytes, sha256 `1948ef9cc2ecb590` |

## Our layer

Yarn-gates the v24 Boatlee front-run layer so it only fires on yarn draws.

## How it did

Also ran as stock C94 live. The gate was worth a lot offline: the ungated layer leaked ~2.8k/game on non-yarn draws while being worth up to +7.4k on yarn draws.

## Files

- `main.py`
- `tail.py`

---
Rebuild the archive with `py -3.12 tools/package.py v26-55435422 --check`.
