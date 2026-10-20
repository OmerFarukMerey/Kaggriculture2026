# v33

| | |
| :--- | :--- |
| Kaggle submission | `55858025` |
| Submitted | 2026-08-29 |
| Live score | *pending* |
| Chassis | Kaito v43 sparse-shop hybrid (byte-identical 63,309-byte prefix, sha256 `69f06a802b62aa08`) |
| `main.py` | 77,316 bytes, sha256 `05185973f2a1ab03` |

## Our layer

[v32](../v32-55799530/NOTES.md)'s mirror-gated sell pull-forward with one constant changed:

| knob | v32 | v33 |
| :--- | ---: | ---: |
| `_CG_HORIZON` | 2 | **3** |
| `_CG_MAX_BATCH` | 40 | 40 |
| `_CG_CLONE_MAX` | 3 | 3 |

A knob sweep over 2,304 games found horizon has a genuine interior optimum at 3
(2→3→4→5 scores 0.500 → 0.719 → 0.688 → 0.656 against v32). v32's own header comment claimed
horizon 3 was worse — that was measured against **v31**, and is chassis- and opponent-specific.

**The sweep promoted `CLONE_MAX 4`; this ships 3.** c4 beat c3 by 23-9 vs 22-10 — one game in 32,
i.e. noise — and both were perfectly neutral across 192 *offline* paired non-clone games. But
replaying v32's 160 **real live episodes** through the gate, c4 opens against a validated non-clone
in 6.9% of games versus c3's 4.4%, and a verifier measured horizon 3 amplifying the cost of a false
fire ~21× (−15,470 coins vs horizon 2's −748 on rayk_c94 seed 5000, gate forced open). Pairing a
deeper horizon with a looser gate is the one combination that compounds the v30 failure mode, so the
horizon gain is taken and the gate loosening refused. Constants are literal — no env indirection.

## Validation

- **22-10-0 (0.688) vs live v32** on the wide panel — reproduces the sweep's h3/c3 cell exactly.
- **Non-clone neutrality:** vs readmarket, v33 and stock kaito_v43 both post 16-0-0 mean +7578 —
  identical to the coin. The layer is dormant outside mirrors.
- Chassis prefix byte-identical; entrypoint `_kaggriculture_knobs_entrypoint` (fresh, not `agent`);
  runs from a directory containing only `main.py`; self-play +1476, inside the chassis' own +1462
  seat-handicap band.

## Why it was worth a slot

It evicted the stock kaito_v43 control (1931.5), not v32 (2520.8). Both active submissions count
toward the final Bradley-Terry evaluation, so replacing a 1931-rated bot with a v32-strength-or-better
one is a strict gain. The control had already answered its question — see the +738 Elo finding below.

## Context: what the live data says

- The layer is worth **+738 Elo inside mirrors** (v32 mirror elo-perf 2384 [2265, 2487] vs the
  control's 1646 [1492, 1765], non-overlapping).
- **v32 is decaying and over-rated.** By day: 0.844 → 0.243 → 0.222. Posted 2525 sits above the top
  of its own 95% CI (elo-perf 2342 [2224, 2433]).
- **The real ceiling is the 2600+ band**, where v32 is 2-34-0 (0.056) and the mirror layer buys
  nothing (clone 1-21, non-clone 1-13). v33 does not address this. It is a mirror-bucket refinement.

## Files

- `main.py`
- `submission.tar.gz`

---
Rebuild with `py -3.12 tools/package.py submissions/v33-55858025/main.py --check`.
