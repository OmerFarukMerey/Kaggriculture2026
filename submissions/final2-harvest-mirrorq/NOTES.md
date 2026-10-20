# final2 — Harvest Ledger V81 + mirror-queue edge

| | |
| :--- | :--- |
| Submitted | 2026-09-30 07:08 UTC |
| Base | haodou092, *Kaggriculture \| Harvest Ledger* V81 (Apache-2.0), byte-identical prefix = our v48 (`531a423a…`) |
| Layer | `tools/build_mirrorq.py` (v1), appended after the unmodified base |
| `main.py` sha256 | `45571085ff93c1253ce4bf24eb1795d4490e5794c3201d24b61cc9d670258a89` |

## Why this base

Live fingerprinting (replaying live seeds with the recorded opponent and each public agent in the
target seat) showed the 1850–2270 ladder band is overwhelmingly the Step1009/1010 family:
exact gtmaster copies live at 1753/1911/1976, exact Harvest (our v48) at ~1910, and those games are
decided by coins (e.g. 62,902 vs 62,900). gtmaster self-play is an exact tie on 11 of 12 seeds.
Harvest V81 edges gtmaster (Step1010) both locally (19–3–2) and live.

## The layer

Kaggriculture executes both players' market slots aligned by index, one unit at a time, quoting both
units before committing either. When the opponent's public farm equals ours (tiles, quadrants, hand
count, farmer position), the layer assumes the rival submits the list our base just produced and
searches re-orderings of our own list (sells only move earlier or permute within runs of sells).
A candidate is kept only if the exact-rules simulation executes the same quantities as the base list
and yields strictly more cash. Otherwise the base action is returned untouched. Engine rules are
`agents/v50/_engine.py` (extracted from kaggle-environments 1.32.7, Apache-2.0), executed in a private
namespace so no base global is shadowed. Time budget 80 ms, 240 candidates.

## Local evidence (fresh seeds, both seats, Kaggle file loader)

| Matchup | Base | With layer |
| :--- | ---: | ---: |
| vs exact v48 (12 seeds) | ties | 17–3–4 |
| vs gtmaster (12 seeds) | 19–3–2 | 21–3–0 |
| vs 12 family variants (6 seeds) | 132–8–4 | 138–6–0 |
| vs herdwin, V57, MarketShock, v46, v50, godmode, V53 | — | unchanged or better (gt+layer vs gt) |

Fires on 1–3 turns per game for +14 to +63 coins, 0 errors. Max action 0.74 s (first-step load).
