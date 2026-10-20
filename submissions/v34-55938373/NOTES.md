# v34

| | |
| :--- | :--- |
| Kaggle submission | `55938373` |
| Submitted | 2026-09-01 |
| Live score | *pending* |
| Content | **byte-identical to [v32](../v32-55799530/NOTES.md)** (sha256 `d0ac1ba2e2acc625f0af`) |

## What this is

v32's exact bytes resubmitted to get a fresh rating: the kaito_v43 chassis plus the mirror-gated,
quantity-conserving sell pull-forward at HORIZON 2 / BATCH 40 / CLONE_MAX 3. No code change.

v32 remains our best-measured agent — opponent-adjusted performance 2285, the highest of any
submission (above v31's 2186 and every stock chassis: kaito_v43 1946 > readmarket 1773 > C94 1671).

## Why resubmit rather than ship something new

The original v32 was at 1974.0 and falling toward a projected settle of ~1851, so its slot had little
rating left to protect. A new submission evicts the *older* of the two active bots, so this replaced
the original v32 and left the pair as {v33, v34}.

Honest caveat: identical bytes will converge to the same true strength (~1850). The decay was strength
convergence, not staleness, so this buys a fresh climb rather than a better agent.

## Files

- `main.py`
- `submission.tar.gz`

---
Rebuild with `py -3.12 tools/package.py submissions/v34-55938373/main.py --check`.
