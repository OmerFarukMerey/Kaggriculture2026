# Lessons

Everything here was paid for with a failed experiment or a wasted submission. Ordered roughly by how
much they cost.

## Engine and harness

**1. The loader picks the last callable by insertion order.** `get_last_callable` ends with
`[v for v in env.values() if callable(v)][-1]`. Python dicts keep a name's *first* insertion position
when it is rebound, so `agent = my_new_agent` at the end of a file does **not** move `agent` to the
end. The last *newly named* callable wins. v24, v25 and v26 all ran live as the stock chassis because
of this; v22 scored 207.8 because a wrong-signature callable was picked. Always end an appended layer
with a delegating entrypoint under a fresh name, and verify with a file-loaded game
(`env.run(["main.py", ...])`), rather than assuming import-by-name equivalence.

You can reproduce this against the submissions in this repo:

```
$ py -3.12 harness/check_entrypoint.py v22 v24 v25 v26 v27 v31
v22   resolves to _v22_terminal_market()          <- a helper, not an agent at all
v24   resolves to agent()                         <- the stock chassis, not our layer
v25   resolves to agent()                         <- same
v26   resolves to agent()                         <- same
v27   resolves to kaggriculture_entrypoint()      <- fixed
v31   resolves to _kaggriculture_v31_entrypoint() <- fixed
```

v22 picked a helper function and scored 207.8. v24, v25 and v26 picked the chassis' own `agent` and
rated 2744 / 2679 / 2679 — respectable numbers that measured someone else's agent.

**2. Verify the actual archive in an isolated directory.** Include every required runtime
dependency and licensing notice. For this repo's single-file agents, `tools/package.py
<main.py-path-or-submission-alias> --check` stages only `main.py`; its self-play check is
not a substitute for inspecting the archive and checking runtime failures.

**3. Submission comparisons must use Kaggle's file-selected callable, not `module.agent`.**
`par_panel.py` now retains the lazy, timed Kaggle file loader, starts a fresh process per
match, and rejects non-object action returns and runtime errors. A factory can return a
function that the engine silently replaces with PASS. A terminal exception can also be
overwritten by DONE and ordinary cash rewards. Neither case is a valid draw or a useful win.

**4. Play every seed twice, once per seat.** The engine is not seat-symmetric; the handicap reaches
±15,000 points on an *identical* policy. On some seeds both seats return byte-identical scores, so
"6 games" is often only 3–4 independent samples — size your conclusions accordingly.

**5. `obs` at step *t* is `env.steps[t]`, not `t+1`.**

## Reading the live leaderboard

**6a. Rating is win/loss/tie only — coin margin does not affect it.** Straight from the Evaluation page:
"The actual coin difference in a match does not affect the rating change—only the win, loss, or tie
outcome matters." Rating change scales with the *opponent's* rating, not the score gap. Almost every
comparison in this repo is reported as a mean margin, which is the wrong statistic: read the W-L-T
record first. A candidate that wins 12 of 14 by small margins beats one that wins 8 of 14 by huge ones.
This also reframes lesson 6 below — v30's tail of 64 near-mirror losses at −5 to −1000 cost exactly as
much rating as 64 blowouts would have.

**6b. Only your latest 2 submissions are active.** Older ones stop playing entirely, and the latest 2
are also what the final evaluation uses. The leaderboard shows only your best-scoring active bot, which
is why the Submissions page lists many and the leaderboard shows one. Two practical consequences: a
throwaway submission near the deadline evicts a good bot from your final pair, and your rank drops
sharply right after any submission because fresh bots start at a default rating and climb.

**5a. Preserve bytes when deriving agents on Windows.** Text-mode writes can translate
`\n` to `\r\n`, changing an otherwise identical chassis prefix and its SHA256. Copy the
prefix with `read_bytes`/`write_bytes`, append only the intended change, and record the
source hash alongside each benchmark result.

**6. Slice live results chronologically, never pooled.** v30's pooled record was 148-117-1, which
reads as mediocre. By day it ran 0.821 → 0.571 → 0.656 → 0.424 → 0.410 → 0.306 → 0.154 — a strong
opening burst averaged against a collapse. The rating is a lagging average over a moving trajectory.

**7. Head-to-head strength does not imply ladder strength.** v30 beat v29 6-0 by +4,147 head-to-head
while rating 233 points *below* it live. Only field-level evidence counts.

**8. Re-measure every chassis-specific finding after a rebase.** "Fertilizer spam burns market slots"
and "the terminal window is half the mirror loss" were both true of one chassis and false of the next.

**9. Verify cross-replay agreement N-way, not pairwise.** A claimed "207 steps agree" collapsed to 52
when compared across three replays instead of two — and 49 of those 52 were trivial no-trade steps.

## Game economics

**10. Wheat is working capital.** It feeds animals. Selling it starves them by day 2, and dumping it
into the market cheapens your opponent's feed.

**11. Sell-pacing controllers lose.** Absorption pacing, surplus dumping and volume throttling all
lost badly (−24k to −130k in early attempts; −12.2k/game for a fertilizer cap in the latest). The
shed cap of 100 **discards** overflow, so withholding a sale throws the goods away rather than banking
them — selling at price 1 beats discarding at 0. Route sell timing is already near-optimal.

**12. Front-running a mirror caps at roughly +200–500.** Endgame goods are harvested and sold on the
same turn, so there is nothing to get ahead of. A front-run only pays if it is *quantity-conserving* —
re-timing a sale by one step into an undepressed book, then cancelling the same quantity next turn.
Selling *extra* loses.

**13. Check what a deterministic opponent is actually doing before exploiting it.** The #1 agent's
first 124 steps were byte-identical across seeds, seats and opponents — but that prefix only sold 19
wheat and 16 fertilizer, about 2,000 coins gross against 90k–150k final scores. Perfect predictability
of an opponent's cheapest activity is worth nothing.

**14. Market positions are strategic, not formatting.** Sell before a purchase when cash
funding requires it, but do not blindly move every sale ahead of every buy. Both players'
queues align by index; empty and invalid orders still occupy slots, and the ten-order cap
applies before parsing. Merging, deleting or reordering entries changes opponent alignment.
`PLACE` retains shed overflow in the actor's inventory; `DROP` and the end-of-day deposit
discard excess.

## Copy warfare

**15. A clone-similarity gate inverts from asset to liability when your chassis goes mainstream.**
v30's gate keyed on farm shape. Once the field adopted the same public chassis, our farm *was*
everyone's shape and the gate was open in 76.7% of live games, applying a mirror tactic to non-mirrors.
Gate on an exact per-step route track, not farm similarity.

**16. Rebasing onto the hot public notebook buys about four days.** The meta turns over roughly that
fast. It is still usually the right move — but expect the advantage to decay, and expect the notebook
you forked to be updated a day later.

**17. Keep a live control when promoting a change.** Retaining the incumbent in the active
pair helps separate the effect of the modification from changes in the opponent population.
Do not spend a control slot on a public chassis that already failed local field comparisons.

## Current public-source investigation

Thirteen current public notebooks were inspected through the Kaggle CLI. Many share the
same 41-route bank despite different titles and claimed scores. Provenance and entrypoint
findings are recorded in `analysis/current_public_catalog.json`,
`analysis/current_secondary_production.json`, `analysis/current_secondary_economy.json`
and `analysis/current_entrypoint_audit.json`.

Three v48 live losses were reproduced with identical actions and final balances. Feeding
instrumentation found no missing-carried-wheat failures in those games; adding a reserve
to address an unobserved shortage would not explain those losses. Recorded-opponent
counterfactuals are diagnostic only: the opponent cannot react, and changed farming can
also change future shop draws.

On twelve held-out seeds, both seats, against the same four opponents:

| Policy | Wins | Losses | Draws | Score (draw = 1/2) |
| :--- | ---: | ---: | ---: | ---: |
| v48 | 72 | 18 | 6 | 75/96 |
| v48 with carrot margin -22 | 70 | 22 | 4 | 72/96 |
| Current Cha22 | 59 | 37 | 0 | 59/96 |
| Current risk-aware feed | 55 | 41 | 0 | 55/96 |

The carrot change beat v48 directly 12–8–4 but trailed it on the common external field.
It is an exploratory artifact, not a demonstrated broad upgrade. These are twelve seed
blocks, not 96 independent worlds, and the public opponent pool is still correlated.
Do not turn the pairwise results into a claimed live Elo gain. Full evidence:
`analysis/current_research_summary.json`.

After reviewing these results, the user explicitly chose an exploratory live upload.
`v49-carrot-field-experiment` is submission **56666488**; it uses the exact verified
carrot archive and retains v48 as the active control. Upload authorization does not
change the negative common-field comparison above.

## v50: preserve farming, replace the market policy

A new recorded-plan controller passed runtime checks but lost all 80 unique
fresh-seed matchups. Expanding its bank to 258 schedules still produced only
4 wins in 24 development games against v48. Neither version was uploaded.
Whole-plan prefix compatibility locked together unrelated farming choices:
one trace committed extra sheep and missed 80 tomatoes worth 14,384 coins.
The final design therefore retains v46's reactive farming and desired stock,
while replacing the executed trade queue with the new inventory/market policy.

Mechanics and policy lessons:

- Floor-price sales pay the seller without increasing public inventory.
  A forecast that adds that supply invents a persistent glut.
- Rival slot assumptions must remain fixed while comparing our queue orders;
  moving the rival with each candidate erases the advantage of selling first.
- A small known town drain does not justify holding output when plausible rival
  supply can overwhelm it. Sale-delay and queue scoring need consistent uncertainty.
- Net working-stock targets avoid buying and selling the same input unnecessarily.
- Selling before a seed purchase can determine whether the next real PLANT succeeds.

The six-world schedule experiments are retained as rejected research, not hidden
inside the deployed guide. Attribution distinguishes the reused v46 controller,
extracted engine primitives, and original market layer.

The frozen hybrid was tested on eight untouched seed blocks, both seats:

| Opponent | v50 wins | Losses | Draws |
| :--- | ---: | ---: | ---: |
| Own v46 | 10 | 6 | 0 |
| Own v48 | 10 | 6 | 0 |
| Own v49 | 10 | 6 | 0 |
| Current Godmode | 10 | 6 | 0 |
| Icefire | 12 | 4 | 0 |

On the identical v49/Godmode/Icefire common field, v50 was **32–16–0** and
v48 was **34–10–4**. Direct wins over our controls do not establish a broad
upgrade; the common-field control scored better. These are eight seed blocks,
not 128 independent worlds, and the opponent pool is correlated.

All 128 candidate/control games completed without runtime failures or overage.
The eight focused regressions passed. The actual uploaded archive also completed
a 720-state game through Kaggle's lazy file loader, with only `main.py` present.
Its source SHA-256 is `97865d7e8ad3386ea87976191831af031b3ca9a2a626ca009b0c49c42c0fe751`.
Submission **56676239** is the requested new hybrid, not either rejected planner.
Evidence: `analysis/v50_research_summary.json`, `analysis/v50_archive_verification.json`,
and `analysis/v50_submission_status.json`.

## Final day (2026-09-30): read the live field, then exploit its mirrors

**18. Notebook `bestPublicScore` is best-ever, not current.** V38/V39 show 2625/2621 from mid-September
and lose 0–16 locally to current agents. Rank candidates by the leaderboard (current) and by live
episode lists (`competitions.EpisodeService/ListEpisodes` returns every opponent's rating per game).

**19. Fingerprint live bots by replaying their seed.** Replay a live episode locally with the recorded
opponent actions and a candidate in the target seat; identical code reproduces ~100% of the recorded
actions (`harness/fingerprint.py`). On 2026-09-30 the 1850–2270 band was almost entirely the
Step1009/1010 family (exact gtmaster copies at 1753/1911/1976, exact Harvest at ~1910); nothing public
matched the 2380+ band. Our v50, which wins the local public pool, lived at ~1450: local public pools
are not the ladder.

**20. Mirror ties are free points.** gtmaster self-play ties on 11 of 12 seeds, and four differently
titled public notebooks are behavioral clones of it. Market slots execute aligned by index, so when the
opponent's farm equals ours, predict its list = our base list and re-order our own list in an exact
rules simulation (same executed quantities, strictly more cash). It fires on 1–3 turns per game for
tens of coins and converts ties into wins with no change against non-mirrors
(`tools/build_mirrorq.py`, submissions final2/final3a).
