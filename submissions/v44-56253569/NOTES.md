# v44 — V43 with its own dormant front_run enabled

| | |
| :--- | :--- |
| Kaggle submission | `56253569` |
| Submitted | 2026-09-15 |
| Chassis | [v38 / V43 Recovering Lost Harvests](../v38-56253029/NOTES.md), byte-identical 321,555-byte prefix |
| `main.py` | 324,171 bytes (chassis + 2,616-byte layer) |
| Entrypoint | `_kaggriculture_v44_entrypoint` |

## The finding

V43's `Chassis` defaults six features to `True`; this build overrides them to `False`. Five are
superseded by upper layers, but **`front_run` is dead code for a different reason** — its guard is

```python
if cfg["front_run"] and self.opponent_plan:   # opponent_plan is never supplied
```

and `_front_run` is *exactly* the quantity-conserving sell pull-forward we measured at +525 Elo on
kaito_v43: sell what we hold now if the opponent sells it next step, **bounded by `own_next`** (our own
planned sale) and **booked into `next_sup["suppress"]`** so the volume is re-timed, never increased.
The chassis owns the debt ledger, so LESSONS #2/#3/#8 are satisfied without extra code.

## The insight

`_front_run` already receives `route`. V43's router picks its tape from the **shop pair at step 144**,
which both players observe — so a mirror opponent is running our exact tape. v44 supplies
`self.routes[route]` as the opponent plan and flips the flag. Nothing else changes.

## Measured

**The opportunity** — V43 self-play, near panel: **14 of 16 games are EXACT ties** (margin 0.0), the
other 2 are ±120 on one seed. Under win/loss/tie scoring a tie is worth half a win, so this is the
densest pool of rating available.

| test | v44 | control | note |
| :--- | :--- | :--- | :--- |
| vs bare V43 (mirror) | **16-0-0** | — | converts all 14 ties plus both decided games |
| vs kaito_v43 | 8-0-0 (+12,574) | 8-0-0 (+12,704) | record identical, −130 coins |
| vs readmarket | 8-0-0 (+33,657) | 8-0-0 (+33,716) | record identical, −59 coins |

**Honest caveat:** unlike our v32 layer this is **not** byte-identical outside mirrors — the front-run
occasionally fires on a wrong prediction. Measured cost is ~60–130 coins mean with **zero record
changes** across 16 paired non-clone games, so it costs no rating at the sample sizes tested, but it is
a real drift. If a live autopsy shows losses inside 1,000 coins against non-clones, the fix is a clone
gate on an exact route-track match (LESSONS #4), which was deliberately held in reserve rather than
added speculatively.

Value is contingent on V43 mirrors existing in the field — the same dependency that made v32's layer
worth +525 Elo while the v43 field lasted and worth nothing once it emptied.

## Licence

Inherits the chassis's attribution; see [ATTRIBUTION.md](../../ATTRIBUTION.md). The layer only enables
an existing chassis feature and supplies its documented input.
