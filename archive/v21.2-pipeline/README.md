# v21.2 pipeline (archived)

This folder is the original standalone repo as it stood on 2026-08-06, when v21.2 was my
first Kaggle submission ([`submissions/v21.2-55296585`](../../submissions/v21.2-55296585/)).
Everything here still runs from this folder. Later work replaced it with the shared
[`harness/`](../../harness/) and [`tools/`](../../tools/); see the [top-level README](../../README.md).

Agent for [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture), a
two-player farming sim where the winner is whoever banks the most coins over a
720-turn season.

## How the agent works

It is a **precomputed route replayer with a conditional market controller**, not
a live planner. `public_v211.py` carries two zlib+base85-packed blobs:

- `_ACTIONS` — a complete 719-step action route (the production plan);
- `_PROTOTYPES` — 30 identity-free route memories, each a public farm signature
  plus the set of products that route sold, at every step.

At runtime the route is replayed and four layers sit on top of it:

| Layer | What it does |
|---|---|
| `_weed_repair_action` | bounded recovery when a random weed knocks the route off its tile plan |
| `_safe_market` | clamps orders against the projected shed so nothing is dropped |
| `_conditional_reorder` | matches the opponent's public farm state to the nearest prototype and may **reorder** existing market orders — it never invents an ordinary-turn SELL or changes a quantity |
| `_terminal_market` | end-of-season liquidation at step 718 |

`v212_tail.py` adds the v21.2 delta on top of that public v21.1 base:

- `_mirror_detect` — is the opponent replaying the same public artifact? Decided
  by signature distance against prototype 11, with a sustained-hit-ratio gate;
- `_mirror_frontrun` — against a detected copy, place the route's *next* step
  SELLs one step early, ahead of the copy's identical orders. `_consume_early`
  subtracts them from the following step, so per-product season totals stay
  exactly equal to the route's;
- a step-**717** terminal pre-dump, ahead of the meta's standard step-718
  liquidation.

Copy detection has a wide margin: calibration puts an exact copy at ≤ 0.25
signature distance and the nearest non-copy at ≥ 98.1, against a threshold of
8.0 (`calibration.json`).

## Layout

| Path | Role |
|---|---|
| `public_v211.py` | the public v21.1 base artifact — route + prototype blobs + runtime layers |
| `v212_tail.py` | v21.2 additions, templated on `__BASE_PROTO_INDEX__` / `__MIRROR_THRESHOLD__` |
| `build_v212.py` | splices the v21.1 head + v21.2 tail into `main.py` |
| `main.py` | **build output** — the agent that gets submitted |
| `calibrate.py` → `calibration.json` | self-play calibration: which prototype matches the deployed route, and the copy / non-copy distance split |
| `evaluate.py` | head-to-head vs the v21.1 base (both seats), self-play tie check, vs `starter` |
| `package_submission.py` | freezes `main.py` into the next `submissions/NNN-<version>/` |
| `submissions/` | one frozen directory per submitted artifact — see [INDEX.md](submissions/INDEX.md) |
| [`../../notebooks/2962.4-solution.ipynb`](../../notebooks/2962.4-solution.ipynb) | the public v21.1 writeup this was built on: method, frozen results, failure audit, credit |
| [`docs/GAME_RULES.md`](../../docs/GAME_RULES.md) | official competition rules — crop/animal/shop tables, price function, turn order |
| [`docs/GETTING_STARTED.md`](../../docs/GETTING_STARTED.md) | getting started: observation/action API, local testing, Kaggle CLI workflow |

## Build → evaluate → submit

```bash
python build_v212.py 11 8.0            # base_proto_index, mirror_threshold -> main.py
python evaluate.py 3 all               # h2h vs v21.1 + self-play + starter
python package_submission.py "what changed"
kaggle competitions submit kaggriculture -f submissions/00N-vXX/submission-00N.tar.gz -m "..."
```

`evaluate.py` and `calibrate.py` need a Python with
`kaggle-environments` installed (results in the notebook were produced on
`kaggle-environments==1.32.4`); `build_v212.py` and `package_submission.py` are
standard library only.

Archives are reproducible — tar and gzip timestamps are pinned to 0, so
re-packaging an unchanged `main.py` yields a byte-identical `.tar.gz`, and the
hashes in each `manifest.json` are meaningful.

## Not in the repo

`.gitignore` excludes two large re-downloadable artifacts:

```bash
kaggle competitions replay <EPISODE_ID> -p ./replays   # replays/*.json
```

plus `kaggriculture-getting-started.ipynb` (~23 MB, from the competition page)
and the usual `__pycache__` / `.DS_Store` noise.
