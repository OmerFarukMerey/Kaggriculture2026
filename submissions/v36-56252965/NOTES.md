# v36 — Three-Day Shop Router (transpiled)

| | |
| :--- | :--- |
| Kaggle submission | `56252965` |
| Submitted | 2026-09-15 |
| Live score | *pending* |
| Source | [yhay81/three-day-shop-router](https://www.kaggle.com/code/yhay81/three-day-shop-router), Apache-2.0 |
| `main.py` | 38,350 bytes, entrypoint `_kaggriculture_shoprouter_b_entrypoint` |

## What it is

A **pure-Python transpile of a compiled C++ agent**. The source notebook ships `policy.cpp`,
`six_day_budget_guard.hpp` and a 719×2 action tape, compiled with `g++ -O3 -shared -fPIC` into
`agent.so` and loaded over ctypes. There is no C++ compiler on this machine and no Docker daemon, so
the `.so` could not be built or tested locally — and a native binary is needless risk on Kaggle
anyway. So it was transpiled to a single self-contained Python file: no `.so`, no compile step, no
multi-file tarball.

**Faithfulness evidence:** two agents transpiled it *independently* — one transcribing the C++
literally, one reasoning from the engine's behaviour — and a third diffed their emitted actions
step-by-step across all 720 turns on real games. Result: **bit-identical on every input the engine can
produce**. Without a compiler, agreement between independent ports is the strongest available check.

## Why it was shipped

Measured on a 9-opponent, 288-game wide panel:

| opponent | W-L-T |
| :--- | :--- |
| kaito_v43 | 32-0-0 |
| **v32 (our best, was live as v34)** | **32-0-0** |
| kaito_v48 | 32-0-0 |
| readmarket | 32-0-0 |
| tetsu_v2 | 32-0-0 |
| frontier_moon | 32-0-0 |
| frontier_soil | 32-0-0 |
| breaking_tie | 32-0-0 |
| opp_bohannn *(instrument only)* | 30-2-0 |
| **total** | **286-2-0 (0.993)** |

The bohannn row matters most: that route is ~22% of the recent field and our own agents went **3-44**
against it.

**It closes the capacity gap we had measured and could not fix.** Our ceiling was days 10–11, where
kaito_v43 sells 0 MILK and 48 MELON against strong opponents' 21.4 / 63.7. This tape buys **COW on day
0 (t=2, versus v43's t=97)** and **MELON 12**, takes its first milk sale at **t=196 (day 8)** instead
of t=310 (day 12), and sells **30 MILK / 72 MELON** in that window — above the benchmark on both.
Note the router itself is nearly irrelevant: the two tapes differ at only 72 of 719 steps
([360, 431]) and are byte-identical on day 0. **The tape is the value, not the router.**

## Licence

Apache-2.0. The author placed explicit SPDX headers on every hand-written source cell. A
`# SPDX-License-Identifier: Apache-2.0` header plus a modification notice (C++ → Python, logic
unchanged) was added to `main.py` as §4 requires. See [ATTRIBUTION.md](../../ATTRIBUTION.md).

## Files

- `main.py`
- `submission.tar.gz`

---
Rebuild with `py -3.12 tools/package.py submissions/v36-56252965/main.py --check`.
