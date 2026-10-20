# Candidates

Builds that were packaged and evaluated but **never submitted** to Kaggle. What actually went to
Kaggle is in [`../submissions/`](../submissions/). The harness resolves these by directory name,
e.g. `python harness/h2h.py cand-gt-mq final2 6`.

| Directory | What it is | Outcome |
| :--- | :--- | :--- |
| `cand-gt-mq` | gtmaster (Step1009/1010 family) + mirror-queue edge v1 | screened on the final day; Harvest base preferred |
| `cand-ms-mq`, `cand-ms-mq2` | MarketShock-M1 + mirror-queue edge v1 / v2 | `cand-ms-mq2` is byte-identical to `final3b` |
| `cand-v48-mq`, `cand-v48-mq2` | Harvest Ledger V81 (= v48) + mirror-queue edge v1 / v2 | byte-identical to the submitted `final2` / `final3a` |
| `cand-v57-mq` | public V57 + mirror-queue edge v1 | screened, not chosen |
| `final3b-marketshock-mirrorq2` | MarketShock + mirror-queue edge v2, the alternative third submission | held back because live final1 did not beat final2 ([NOTES](final3b-marketshock-mirrorq2/NOTES.md)) |
| `experimental-field`, `experimental-mgonly` | v46 variants for the barrier / field ablations | see `analysis/barrier_*` |
| `research-carrot-more` | v48 + `_CA_MARGIN = -22.0` | promoted to [v49](../submissions/v49-carrot-field-experiment/) as a live experiment |
| `research-wheat-value` | v48 + `_CA_MARGIN = 0.0` | crop-margin ablation control |
| `research-fixed-anchor` | route-replay chassis with a fixed anchor margin | see `analysis/current_fixedanchor_development.json` |
| `research-v50-complete`, `research-v50-floor`, `research-v50-guided46` | v50 development builds (`build.json` records module hashes) | `guided46` became [v50](../submissions/v50-adaptive-economy/) |
| `rejected-v50-sparse-bank`, `rejected-v50-wide-bank` | the recorded-plan controller with a sparse and a 258-schedule route bank | lost all 80 fresh-seed matchups / won 4 of 24 vs v48; never uploaded ([LESSONS](../docs/LESSONS.md#v50-preserve-farming-replace-the-market-policy)) |
| `opponent-icefire-entry` | public *A Song of Ice and Fire* policy with only the entrypoint fixed | used as a local opponent |
| `v48-notebook-2965` | extraction of *The 2965 Master Hybrid Engine* (V79) | reference for v48 |
