# v22

| | |
| :--- | :--- |
| Kaggle submission | `55427256` |
| Submitted | 2026-08-11 |
| Live score | 207.8 (broken) |
| Chassis | Boatlee V16 |
| `main.py` | 68,164 bytes, sha256 `d24683d564d30b0f` |

## Our layer

Copy front-run plus terminal liquidation, appended as a tail.

## How it did

**Ran as a broken agent.** The entrypoint bug (LESSONS #1) picked a wrong-signature callable, so almost every turn errored. This score is what that bug looks like when it is total rather than silent.

## Files

- `build.py`
- `main.py`
- `tail.py`

---
Rebuild the archive with `py -3.12 tools/package.py v22-55427256 --check`.
