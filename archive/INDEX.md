# Archive

Dead ends, superseded variants and one-off probes. Kept because the negative results are most of what
this project learned — several of these ideas look obviously good and are not.

## The original v21.2 pipeline (`archive/v21.2-pipeline/`)

The standalone repo as it stood on 2026-08-06: public v21.1 artifact + v21.2 tail, the build /
calibrate / evaluate / package scripts, and the frozen first submission. Superseded by `harness/`
and `tools/`, but kept intact and runnable. See its [README](v21.2-pipeline/README.md).

## Agent variants (`archive/agents/`)

| File | What it was | Outcome |
| :--- | :--- | :--- |
| `yarnvar_more.py`, `yarnvar_less.py`, `yarnvar_c_gated.py` | swap-more / swap-less / C94-gated variants of the v25 yarn cow→sheep swap | All lost to the shipped constants. The current swap window is a local optimum; never let it overlap kept-cow PLACE steps (161-cows place at 165–187). |
| `umataro_var.py` | yarn calibration copying Umataro: swap only the 192 batch, skip the 289 cow | Inconclusive — better vs C94-family yarn (+3,593 vs −6,666), worse vs Boatlee 9011 (+5,032 → −361). Not adopted. |
| `fert_throttle.py` | caps cumulative FERTILIZER sales at 215 units (the #1 agent's measured volume) after finding we sell 400 and crater the price to 1 | **0-4-0, mean −12,199.8 vs stock.** The shed cap discards overflow, so withheld goods are thrown away, not banked. See LESSONS #11. |
| `v31_ungated.py` | v31 with the clone gate removed (`_V31_CLONE_MAX` → 10⁹), built to measure the worst case | Confirmed the gate matters: drift against non-clones goes from 0 to −140..−530 per game once the edge fires ~81×/game instead of 0–3. |
| `v22_nodetect.py`, `v22_agent.py` | v22 without copy detection; a duplicate of `v22_main.py` | superseded |
| `main_v25_orig.py` | pre-fix v25 | superseded |
| `candidate1.py`, `candidate2.py`, `candidate3.py` | chassis candidates screened during the v25/v26 generation | not adopted |
| `dispatcher_main.py`, `mock_attacker.py` | mid-game engine switching between v22 and v24, and a test attacker | **Failed by design.** Signature-identical farms are not tile-identical layouts — the farm dies around 5k. Do not retry. |
| `cand_bestknown.py`, `cand_robust.py`, `cand_newlayer.py` | late-August chassis candidates on Kaito Fukami's v43 / v48 package framework (`analysis/verify_cand_*`) | not adopted |
| `cand_generalist.py` | behavioural reconstruction of a public-replay consensus route (12 traces), clone preemption disabled | not adopted |
| `port_a.py`, `port_b.py`, `port_b_r0.py`, `port_b_r1.py` | two independent pure-Python transpiles of yhay81's C++ *Three-Day Shop Router*, plus forced-route probes | the ports were diffed bit-identical; `port_b.py` shipped as [v36](../submissions/v36-56252965/NOTES.md) |
| `v23_tail.py`, `build_v23.py` | the v23 absorption-pacing / surplus-dumping market controller | **Never submitted.** Lost −24k to −130k. The origin of LESSONS #11. |

## Probes (`archive/probes/`)

One-off analysis scripts written to answer a single question, kept for their method rather than for
reuse. `gate.py`, `probe_gate.py` (clone-gate firing rates), `phase.py`, `timeline.py`, `curves.py`,
`curves2.py` (score-curve reconstruction from replays), `diverge.py` (cross-replay divergence),
`scan30.py` (seed scanning), `edgeval.py` (edge value attribution), `term.py` (terminal-window
analysis), `whois.py` (opponent identification), `verify.py`, `verify2.py`, `copywar_v31.py`,
`fileload_v31.py` (v31 validation), and `w_*.py` (tiny one-line experiment wrappers).

The reusable descendants of these live in `harness/`.

## `archive/logs/`, `archive/x036/`

Raw command output from validation runs, and an early conditional-milk-delay experiment.
