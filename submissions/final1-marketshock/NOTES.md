# final1 — MarketShock-M1-WR1K (live probe)

| | |
| :--- | :--- |
| Submitted | 2026-09-30 06:49 UTC |
| Source | leoprovorov, *Kaggricult-Man: Reverse-Engineering* / *A Song of Ice and Fire* (same agent, main.py sha256 `12ad317e…`) — Apache-2.0, V39 lineage, notices retained in `main.py` |
| Policy change | none |
| Added | 3-line entrypoint: `agent = globals().pop("agent")` so the installed policy is both the name `agent` and the last callable (the unmodified file's last callable is the factory `install_water_repair_local_patch`) |
| `main.py` sha256 | `d96a2bc448719db4c32abe6ca2eecf6afe4d31cb856385c9589151423a19e18d` |

## Why

Highest recent public score among current notebooks (best-ever 2579 / 2343), built by reverse-engineering
Majkel1337's (rank ~15) winning replays. Locally it loses by 1–4k to the Step1009/1010 family
(0–16 vs gtmaster, v48, v46 in the 17-agent round robin), but the local pool is not live-representative
(our v50 wins that pool and lives at ~1450). Only a live run settles it, so this is the first of three
submissions and doubles as a probe; it is deactivated when the third submission is made.

## Checks

- Isolated self-play from a directory holding only `main.py`: 105,689 each.
- Strict file-loader game vs gtmaster: valid, both seats.
- Max action time in 256 local games: 0.28 s, no overage.
