# Attribution

Most agents in `agents/public/` are **other people's work**, extracted from their public Kaggle
notebooks so they could be run as opponents in local evaluation. They are reproduced here under the
licence of the notebook they came from (Kaggle notebooks default to Apache 2.0). The source notebook
for each is kept in `notebooks/` so the provenance can be checked.

If you are one of the authors below and would prefer your agent not be mirrored here, open an issue
and it will be removed.

| File | Author | Source notebook | Notes |
| :--- | :--- | :--- | :--- |
| `rayk_c94.py`, `rayk_c92.py` | Rayk Kretzschmar | *Kaggriculture: Findings from Zero to Top Meta* | extracted from cell 51; the C94 artifact was the base for v24–v28 |
| `boatlee_v16.py` | boatlee | *V16-RC2 \| High-Score Near-Mirror Market Relay* | base for v22 |
| `boatlee_v20.py` | boatlee | *V20-Adaptive-R1 \| Multi-Route Agent* | |
| `rc5.py` | boatlee | *V16-RC5 \| High-Score 8C/4S Premium Market Lead* | screened 2026-08-18, not adopted |
| `kaito_v27.py` | Kaito Fukami | *25/27 Strict-Future \| v27 Midgame Meta Reset* | |
| `kaito_v43.py` | Kaito Fukami | *103/128 Fresh Public \| v43 Sparse Shop Hybrid* | **chassis for v31**; also submitted unmodified as a control |
| `tetsu.py`, `tetsu_v2.py` | tetsu2131 | *🌾Adaptive Farming Strategy for Kaggriculture* | `tetsu.py` = 2026-08-18 revision (chassis for v30); `tetsu_v2.py` = 2026-08-19 revision |
| `multiroute.py`, `multiroute_v2.py` | Igor Zharov (flexonafft) | *Kaggriculture \| Multi-Route Farming Agent* | `multiroute_v2` embeds boatlee's V20-Adaptive-R1 |
| `readmarket.py` | see notebook | *Read the Market, Choose the Farm* | **chassis for v29**; also submitted unmodified |
| `breaking_tie.py` | Andrey Naymushin | *Kaggriculture: Breaking the Tie* | |
| `salem3000.py` | Salem Ali | *Kaggriculture +3000 socre* | derived from boatlee's V16-RC5 lineage — the notebook carries the same `v16_rc5` metadata key as boatlee's own, though the code is not byte-identical (286 differing lines) |
| `frontier_moon.py`, `frontier_soil.py` | prvsiyan | *Kaggriculture Frontier* (Moon Counts Melons / Soil Remembers Rain) | |
| `submissions/v36-56252965/main.py`, `archive/agents/port_*.py` | Yusuke Hayashi (yhay81) | *Three-Day Shop Router* | Apache-2.0 (explicit SPDX in source). Pure-Python transpile of the notebook's C++ policy; logic unchanged. Two independent ports (`port_a.py`, `port_b.py` = v36) verified bit-identical; `port_b_r0/r1.py` are forced-route probes. |
| `fsv4.py` | see notebook | *Farming Score V4 — A Better Shop* | route-replay chassis; shop-conditioned livestock substitution |
| `v43rlh.py` | see notebook | *Kaggriculture V43: Recovering Lost Harvests* | targets warehouse/shed overflow; source sha256 pinned by the notebook and verified on extraction |
| `public_v211.py` (also `archive/v21.2-pipeline/`) | see notebook | *177/180 Fresh Top-30 \| v21.1 Conditional Memory* (`notebooks/2962.4-solution.ipynb`) | base for v21.2 |
| `submissions/v48-2965-mirrorgate/main.py`, `candidates/research-carrot-more/main.py`, `submissions/v49-carrot-field-experiment/main.py` | haodou092 and upstream contributors; haideptry repackaging | [Harvest Ledger](https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger), [The 2965 Master Hybrid Engine](https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine) | v48 is the previously extracted V81 source. The research variant and v49 preserve those bytes and append only `_CA_MARGIN = -22.0`. v49 was explicitly authorized as a live experiment, not a demonstrated broad-field upgrade. Embedded Apache-2.0 license and upstream notices are retained. |
| `submissions/final1-marketshock/`, `candidates/final3b-marketshock-mirrorq2/`, `candidates/cand-ms-mq*/` | leoprovorov | [Kaggricult-Man: Reverse-Engineering](https://www.kaggle.com/code/leoprovorov/kaggricult-man-reverse-engineering) / [A Song of Ice and Fire](https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-fixed-flexible) | Apache-2.0, notices retained. final1 adds only a 3-line entrypoint; final3b adds the mirror-queue layer. |
| `submissions/final2-harvest-mirrorq/`, `submissions/final3a-harvest-mirrorq2/`, `candidates/cand-v48-mq*/` | haodou092 and upstream contributors | [Harvest Ledger](https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger) V81 | Byte-identical base (= v48) plus the original mirror-queue layer from `tools/build_mirrorq.py`. |
| `archive/agents/cand_bestknown.py`, `cand_robust.py`, `cand_newlayer.py` | Kaito Fukami (framework) | *v43* / *v48* public notebooks | chassis candidates screened in late August, built on the author's v43 / v48 package framework; not submitted |
| `agents/v50/data.py` | Omer Faruk Merey's v46/v48, with their attributed Apache-2.0 ancestry | `submissions/v46-platform/main.py`, `submissions/v48-2965-mirrorgate/main.py` | Rejected research, not deployed: 258 farming schedules covering natural v46/v48 play and every v48 physical route across six training worlds. Source hashes and measurement provenance are embedded in the profiles. |
| `agents/v50/_engine.py` | Kaggle and kaggle-environments contributors | [kaggle-environments](https://github.com/Kaggle/kaggle-environments), installed version 1.32.7 | Dependency-closed deterministic unit and single-order rules, mechanically extracted under Apache-2.0. The original ten-slot queue processor is not copied; the new execution model is checked against it. |
| `submissions/v50-adaptive-economy/main.py` | New market policy by Omer Faruk Merey; inherited v46 and upstream Apache-2.0 contributors | `submissions/v46-platform/main.py`, `agents/v50/` | Reuses the complete v46 source as a reactive farming and working-stock guide. Its returned market queue is simulated for intent, not executed. New inventory netting, sale decisions, and cash/capacity-aware queue selection replace execution. The exact v46 hash and new module hashes are recorded in `build.json`; inherited notices remain embedded. |

`agents/public/kaito_v43_modules/` is the module bundle that `kaito_v43.py` unpacks at runtime,
extracted for readability. It is part of the same author's work.

`docs/GAME_RULES.md` / `docs/GETTING_STARTED.md` are competition-provided material from Kaggle
(Bovard Doerschuk-Tiberi). The official getting-started notebook (~23 MB) is not included; download
it from the competition page.

## What in this repo is original

The layers appended to each chassis (`submissions/*/tail.py` and the appended sections of each
`main.py`), the mirror-queue layer in `tools/build_mirrorq.py`, the evaluation harness in
`harness/`, the packaging and notebook-extraction tools, the original v21.2 pipeline in
`archive/v21.2-pipeline/`, the live-episode autopsies in
`analysis/`, the opponent routes reconstructed from replays in `routes/`, and the write-ups.

`agents/v50/guided.py`, `market.py`, and `mechanics.py` implement the original
inventory policy and market execution model. The deployed agent combines them
with the attributed v46 guide and extracted deterministic rules above.
`production.py` is an original but rejected recorded-plan controller; its route
library and plan-only market methods are not included in the deployed bundle.

Public notebooks downloaded with `kaggle kernels pull` and used only as comparison opponents are
**not** redistributed here (locally they lived in `../kaggriculture-candidates/`;
`tools/extract_notebooks.py` recovers each `main.py` statically). Exact notebook references,
source hashes, extraction methods, required notices and lineage limitations are recorded
in `analysis/current_public_catalog.json`, `analysis/current_secondary_production.json`
and `analysis/current_secondary_economy.json`. These are attributed public policies, not
original agents. `candidates/opponent-icefire-entry/main.py` preserves the downloaded
policy and only reinserts `agent` at the end of the namespace to correct file loading;
the unmodified factory-entrypoint results are excluded from strategy comparisons.
