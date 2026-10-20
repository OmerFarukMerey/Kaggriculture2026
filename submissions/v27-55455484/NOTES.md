# v27

| | |
| :--- | :--- |
| Kaggle submission | `55455484` |
| Submitted | 2026-08-12 |
| Live score | 1638.7 |
| Chassis | Rayk C94 |
| `main.py` | 134,099 bytes, sha256 `03f6398ff9cc09f3` |

## Our layer

v26 plus a delegating `kaggriculture_entrypoint` at the file end — the fix for LESSONS #1.

## How it did

**The important submission.** First one where our layer actually ran. The low rating is the honest cost of discovering that three prior submissions had been measuring someone else's agent. Live record 75-12-0 (86%) through 87 episodes.

## Files

- `main.py`

---
Rebuild the archive with `py -3.12 tools/package.py v27-55455484 --check`.
