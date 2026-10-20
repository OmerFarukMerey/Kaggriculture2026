# v32

| | |
| :--- | :--- |
| Kaggle submission | `55799530` |
| Submitted | 2026-08-26 |
| Live score | *pending* |
| Chassis | Kaito v43 sparse-shop hybrid (byte-identical 63,309-byte prefix, sha256 `69f06a802b62aa08`) |
| `main.py` | 74,123 bytes |

## Our layer

Same mechanism as [v31](../v31-55740384/NOTES.md) — a mirror-gated, quantity-conserving sell
pull-forward — with three constants changed:

| knob | v31 | v32 | why |
| :--- | ---: | ---: | :--- |
| `_CG_HORIZON` | 1 | **2** | may borrow from the tape's next *two* turns of premium sells |
| `_CG_MAX_BATCH` | 12 | **40** | units per item per turn (already non-binding; batch 100 measured identical) |
| `_CG_CLONE_MAX` | 6 | **3** | tighter clone gate |

Set the three knobs back to v31's values and the file reproduces v31 **to the coin** on seeds
5000/5013/7027 both seats — so the gain is attributable to the constants, not to a rewrite.

## Why these constants

The flippable population was measured, not guessed. In `kaito_v43` **self-play on the 16-seed wide
panel, 11 of 16 seeds are an exact coin tie (margin 0.0)** and 3 more land within 92 coins. Only 2
seeds carry a real seat handicap. So 14 of 16 mirror games are decided by ≤92 coins — and under
win/loss/tie scoring (see [LESSONS #6a](../../docs/LESSONS.md)) a tie is worth half a win, making
those the highest-leverage games on the board. The live record agrees: stock v43 has 5 exact
0-margin ties and 11 sub-1k losses, 13 of 16 of them in mirrors.

Coin curves show the edge is not a single event but a slow compounding of price-ladder rungs that
only becomes visible in the second half, with ~30% of it landing in steps 680–719.

## How it did

Offline, before submission:

- **46-2-0 vs v31** (0.958) across the wide and far panels; **47-1-0 vs stock v43**. Both losses are
  proven by telemetry to be layer-*dormant* games — the chassis' own ±14,999 seat handicap on seed
  5026, not damage the layer did.
- **20-0-0 vs v31 and 20-0-0 vs stock v43** on a genuinely disjoint 10-seed panel built by a verifier.
- **Neutrality: 768 paired candidate-vs-stock cells across 16 non-clone opponents, max |coin delta| = 0.**
  The clone gate opened at all in 7 of 768 games, for 1–2 steps, and borrowed 0 units each time.
  Against a non-clone this agent *is* stock kaito_v43, which is a hard rating floor.

**Tempering:** the conversion of mirror dominance into live rating is unproven. v31 also beats stock
v43 in mirrors (1-47-0) yet posted a lower rating for two days — though opponent-adjusted analysis
of ~120 live episodes each put v31 *ahead* by +65 Elo (2319 vs 2254), suggesting that gap was
opponent-draw noise rather than a real deficit.

## Files

- `main.py`
- `submission.tar.gz`

---
Rebuild with `py -3.12 tools/package.py submissions/v32-55799530/main.py --check`.
