# v38 — Kaggriculture V43: Recovering Lost Harvests

| | |
| :--- | :--- |
| Kaggle submission | `56253029` |
| Submitted | 2026-09-15 |
| Source | public notebook *Kaggriculture V43: Recovering Lost Harvests*, **unmodified** |
| `main.py` | 321,555 bytes, sha256 `919fc1d61050cd96…` |

Targets a measured warehouse failure: workers returning at dawn with cargo exceeding the shared shed.
That is our own lesson 8 — the shed cap is 100 and **discards** overflow — which we had identified as
a binding constraint but never fixed.

**Extraction is verified:** the notebook pins `EXPECTED_MAIN_SHA256`, and the bytes recovered from its
`b''.join((...))` literal hash to exactly that value, CRLF endings preserved.

## Measured — the strongest agent we hold

| opponent | W-L-T | panel |
| :--- | :--- | :--- |
| v32 (our previous best) | **16-0-0** (+18,021) | near |
| v36 shop router | **16-0-0** (+13,057) | near |

Packages clean, runs from a directory holding only `main.py`, self-play an exact tie (125349).
Its source ends with `agent=globals().pop('agent')`, deliberately forcing `agent` to be the last
callable — the author solving the same loader problem documented in [LESSONS #1](../../docs/LESSONS.md).

Source notebook retained at `notebooks/kaggriculture-v43-recovering-lost-harvests.ipynb`.
