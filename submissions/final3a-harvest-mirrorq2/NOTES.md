# final3a — Harvest Ledger V81 + mirror-queue edge v2 (candidate for submission 3)

| | |
| :--- | :--- |
| Base | haodou092, *Kaggriculture \| Harvest Ledger* V81 (Apache-2.0), byte-identical prefix = our v48 |
| Layer | `tools/build_mirrorq.py --v2` |
| `main.py` sha256 | `f954b81dd72867fa65d568d2754bbc7a9ec3e64d484a5fdc362ee00e216b2951` |

v2 = v1's candidate set (sells move earlier / permute within sell runs) plus adjacent swaps of any two
orders and one empty-slot insertion. Same acceptance rule: identical executed quantities in the
exact-rules simulation against the predicted mirror list, strictly more cash.

## Local evidence (fresh seeds, both seats, Kaggle file loader, 0 invalid)

| Matchup | v1 (final2) | v2 |
| :--- | ---: | ---: |
| head-to-head v2 vs v1 | — | 12–0 |
| vs exact v48 | 17–3–4 (12 seeds) | 12–0 (6 seeds) |
| vs gtmaster | 21–3 (12 seeds) | 12–0 (6 seeds) |
| 18-opponent field (12 family variants + V50/V53/V55/V57/MarketShock/router7) | 208–8 | 208–8, higher margin in every pair |

Max action 0.735 s (first-step load).
