# v37 — Farming Score V4 (A Better Shop)

| | |
| :--- | :--- |
| Kaggle submission | `56253028` |
| Submitted | 2026-09-15 |
| Source | public notebook *Farming Score V4 — A Better Shop*, extracted from `%%writefile main.py` (cell 6), **unmodified** |
| `main.py` | 336,431 bytes |

Route-replay chassis, pure stdlib. Its three stated mechanisms: same-day weed recovery,
confirmed-mirror sale ordering, and **shop-conditioned livestock substitution** (animal choice by
first-productive-day and production interval) — the last of which targets the day-0 capacity gap that
capped every agent we built.

## Measured

| opponent | W-L-T | panel |
| :--- | :--- | :--- |
| v32 (our previous best) | **16-0-0** (+17,685) | near |
| v36 shop router | **16-0-0** (+11,667) | near |

Packages clean, runs from a directory holding only `main.py`, self-play an exact tie (125349).
Differs from v38 at 212 of 719 steps, so the two are genuinely distinct agents.

Source notebook retained at `notebooks/farming-score-v4-a-better-shop.ipynb`.
