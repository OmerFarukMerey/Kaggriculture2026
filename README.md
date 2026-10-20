# Kaggriculture 2026

My agents, tooling and experiment log for Kaggle's
[Kaggriculture](https://www.kaggle.com/competitions/kaggriculture) simulation competition
(August–September 2026). It is a two-player farming game: both farms sell into one shared,
price-reactive market over a 720-turn season, and the player with more coins at the end wins.

**Final result: 1,287th of 10,148 teams (top 13%), no medal.** I made 29 submissions, from v21.2
on Aug 6 to final3 on Sep 30. The [postmortem](#postmortem-why-no-medal) at the bottom explains
why my best bot wasn't the one that counted.

## Approach

Most of the strongest agents in this competition were public notebooks, and the meta turned over
roughly every four days. So most of my submissions are a strong public **chassis** (credited in
[ATTRIBUTION.md](ATTRIBUTION.md)) with a thin, measured layer of my own on top, plus the
infrastructure to find out whether the layer actually helped.

- **Copy and mirror warfare.** Much of the ladder ran the same public artifacts. My layers detect
  an exact mirror and re-time sales ahead of it without changing quantities: v21.2's one-step
  front-run, the mirror-gated sell pull-forward in v31–v33, and the final-day **mirror-queue edge**
  ([`tools/build_mirrorq.py`](tools/build_mirrorq.py)). That last one re-orders my own market slots
  in an exact-rules simulation, keeping only orders that execute the same quantities for strictly
  more cash, so mirror ties become wins.
- **An original market policy (v50).** v50 keeps v46's reactive farming and replaces trade
  execution with new inventory netting, sale decisions and a 10-slot queue optimizer that accounts
  for cash and shed capacity ([`agents/v50/`](agents/v50/)).
- **Evaluation harness.** Head-to-heads play every seed from both seats, load a fresh module per
  game and go through Kaggle's real file loader. Live-episode autopsies are sliced by day, and live
  opponents are fingerprinted by replaying their seeds ([`harness/`](harness/)).
- **Negative results are kept.** Most of what I learned came from experiments that failed. See
  [docs/LESSONS.md](docs/LESSONS.md) and [archive/INDEX.md](archive/INDEX.md).

## Submissions

Every row links to the exact bytes sent to Kaggle, with a `NOTES.md` explaining the change and the
evidence behind it. Scores are public ratings as shown on Kaggle after the competition closed.

Kaggle keeps only a team's **latest two** submissions playing. A retired bot's rating freezes when
it is replaced, so scores from different weeks are not comparable (the field got much stronger in
September). Rating depends only on win/loss/tie, not on coin margin.

| # | Date | Submission | Base | My change | Score |
| ---: | :--- | :--- | :--- | :--- | ---: |
| 1 | 08-06 | [v21.2](submissions/v21.2-55296585/) | public v21.1 | copy detection, one-step sell front-run, step-717 pre-dump | 1929.6 |
| 2 | 08-11 | [v22](submissions/v22-55427256/) | Boatlee V16 | copy front-run + terminal ⚠ | 207.8 |
| 3 | 08-11 | [v24](submissions/v24-55428059/) | Rayk C94 | track-gated copy escalation + Boatlee layer ⚠ | 2744.3 |
| 4 | 08-11 | [v25](submissions/v25-55432745/) | Rayk C94 | + yarn-adaptive cow→sheep swap ⚠ | 2679.1 |
| 5 | 08-11 | [v26](submissions/v26-55435422/) | Rayk C94 | + yarn-gated Boatlee front-run ⚠ | 2679.5 |
| 6 | 08-12 | [v27](submissions/v27-55455484/) | Rayk C94 | entrypoint fix: the layer stack finally runs live | 1638.7 |
| 7 | 08-13 | [v28](submissions/v28-55485346/) | Rayk C94 | + double-yarn late cow→sheep conversion | 2450.3 |
| 8 | 08-14 | [readmarket](submissions/readmarket-55508026/) | Read the Market | unmodified baseline | 2266.6 |
| 9 | 08-14 | [v29](submissions/v29-55508152/) | Read the Market | clone-gated preempt layer | 2015.8 |
| 10 | 08-18 | [v30](submissions/v30-55597536/) | tetsutani adaptive | clone-escalated lead horizon | 2294.7 |
| 11 | 08-24 | [v31](submissions/v31-55740384/) | Kaito v43 | mirror-gated one-step sell pull-forward | 2058.0 |
| 12 | 08-24 | [kaito_v43](submissions/kaito_v43-55740389/) | Kaito v43 | unmodified live control for v31 | 1904.6 |
| 13 | 08-26 | [v32](submissions/v32-55799530/) | Kaito v43 | 2-turn horizon, tighter gate | 1974.0 |
| 14 | 08-29 | [v33](submissions/v33-55858025/) | Kaito v43 | 3-turn horizon | 1718.9 |
| 15 | 09-01 | [v34](submissions/v34-55938373/) | Kaito v43 | v32 resubmitted for a fresh rating | 1250.3 |
| 16 | 09-02 | [v35](submissions/v35-55959643/) | Rayk C94 | v24 resubmitted | 979.1 |
| 17 | 09-15 | [v36](submissions/v36-56252965/) | Three-Day Shop Router | C++ → pure-Python transpile, logic unchanged | 693.4 |
| 18 | 09-15 | [v37](submissions/v37-56253028/) | Farming Score V4 | unmodified | 1367.8 |
| 19 | 09-15 | [v38](submissions/v38-56253029/) | V43 Recovering Lost Harvests | unmodified | 1813.7 |
| 20 | 09-15 | [v44](submissions/v44-56253569/) | V43 Recovering Lost Harvests | enabled its dormant front-run against the mirror route | 1603.9 |
| 21 | 09-21 | [v45](submissions/v45-ready/) | MetaV4 wheat chassis | validated market stack | 1882.3 |
| 22 | 09-24 | [v46](submissions/v46-platform/) | cha22 / v45 hybrid | cash-safe hybrid, seed and queue guards | **2233.6** |
| 23 | 09-28 | [v47](submissions/v47-ready/) | v46 | same-item buy/sell isolation | 1880.1 |
| 24 | 09-28 | [v48](submissions/v48-2965-mirrorgate/) | Harvest Ledger V81 | mirror-gated 7-turn sales (V81 as extracted) | 1910.6 |
| 25 | 09-29 | [v49](submissions/v49-carrot-field-experiment/) | v48 | carrot margin −22, exploratory | 1890.2 |
| 26 | 09-29 | [v50](submissions/v50-adaptive-economy/) | my v46 farming | original inventory and market-queue policy | 1461.8 |
| 27 | 09-30 | [final1](submissions/final1-marketshock/) | MarketShock-M1 | unmodified + robust entrypoint (live probe) | 1357.9 |
| 28 | 09-30 | [**final2**](submissions/final2-harvest-mirrorq/) | Harvest Ledger V81 | mirror-queue edge v1 | 1739.8 |
| 29 | 09-30 | [**final3**](submissions/final3a-harvest-mirrorq2/) | Harvest Ledger V81 | mirror-queue edge v2 | 1768.2 |

**final2** and **final3** were the active pair at the deadline. ⚠ marks bots where Kaggle's loader
called the wrong function, so the live agent wasn't the one I meant to ship (lesson 1 below).
v24's 2744.3, for example, is really the stock Rayk C94 chassis.

Builds that were evaluated but never submitted are in [`candidates/`](candidates/README.md).

## Repository layout

```
submissions/    the 29 submitted bots: exact main.py bytes, NOTES.md, archives, build files
candidates/     built and evaluated, never submitted
agents/public/  other people's agents, extracted from public notebooks, used as local opponents
agents/v50/     readable source of the v50 market policy
harness/        evaluation: head-to-heads, loader checks, live autopsies, fingerprinting
tools/          packaging, v50 bundler, mirror-queue builder, notebook extraction
analysis/       evidence: live-episode autopsies, panels, holdouts, probe outputs
routes/         opponent routes reconstructed from replays
notebooks/      the public notebooks the chassis came from, kept for provenance
archive/        dead ends and the original v21.2 pipeline, each explained in INDEX.md
docs/           game rules, getting started, LESSONS.md
```

## Running it

```bash
pip install -r requirements.txt          # kaggle-environments 1.32.7

# head to head: 3 seeds x both seats
python harness/h2h.py v31 kaito_v43 3

# which function will Kaggle's loader actually call?
python harness/check_entrypoint.py v22 v24 v27 v31

# package a submission and prove it runs from a directory holding only main.py
python tools/package.py v31 --check

# rebuild and test v50
python tools/build_v50.py --extract
python tools/build_v50.py --bundle
python -m unittest harness.test_v50_mechanics harness.test_v50_guided
```

You can name an agent by path, by bare filename in `agents/public/` or `archive/agents/`, by
submission alias (`v31`, `final2`) or by candidate directory (`cand-gt-mq`).

Each seed is played twice, once per seat. The engine is not seat-symmetric: on some seeds the
handicap reaches ±15,000 points with an identical policy. A fresh module instance is loaded per
game, because agents keep per-seat state that would otherwise leak between games.

### Not in this repo

- **Replays** (~48 GB). The harness looks in `../kaggriculture-data/`, or set `KAGGRICULTURE_DATA`.
  Fetch one with `kaggle competitions replay <EPISODE_ID> -p ../kaggriculture-data/replays`.
- **Recent public notebooks** used only as comparison opponents. Pull them with
  `kaggle kernels pull <ref> -m`, then recover each `main.py` with
  `python tools/extract_notebooks.py <dir>`. Exact references and hashes are in
  `analysis/current_public_catalog.json`.
- The official getting-started notebook (~23 MB), available from the competition page.

## Lessons

The full list, each paid for with a failed experiment or a wasted submission, is in
[docs/LESSONS.md](docs/LESSONS.md). The ones I'd tell anyone starting a Kaggle simulation
competition:

1. **The loader calls the last *newly named* callable in your file.** Rebinding `agent = new_agent`
   at the end does not move it, because Python dicts keep a name's first insertion position. v24–v26
   silently ran as the stock chassis, and v22 ran a helper function and scored 207.8. End every
   appended layer with an entrypoint under a fresh name, and verify with a file-loaded game.
2. **Rating is win/loss/tie only.** Coin margin doesn't matter, so read W-L-T records, not mean
   margins.
3. **Slice live results by day.** v30's pooled 148-117-1 hid a collapse from 0.82 to 0.15 daily
   win rate.
4. **Local results are not the ladder.** v50 won my local pool of public agents and lived at about
   1450 on Kaggle. Only field-level live evidence counts.
5. **Mirror ties are free points.** When the opponent's farm equals yours, it will very likely
   submit your market list. Re-ordering your own slots in an exact simulation converts ties into
   wins and changes nothing against non-mirrors.
6. **Only your latest two submissions count.** See below.

## Attribution and license

Most chassis here are other people's public work. They are used under the licence of the notebook
they came from (Apache-2.0 by default on Kaggle) and credited file by file in
[ATTRIBUTION.md](ATTRIBUTION.md), with upstream notices retained in the files. My own work (the
layers, harness, tools, analysis, v50 market policy and write-ups) is under the [MIT License](LICENSE).
The game rules in `docs/` are competition material from Kaggle.

## Postmortem: why no medal

On Kaggle simulation competitions, only your **latest two** submissions keep playing, and they are
what the final leaderboard ranks. Everything older is retired and its rating freezes. I had even
written this down as lesson 6b during the competition, and it still cost me the medal.

- The bronze cutoff (top 10%) was rank 1,014, at about **1,843** rating.
- My final active pair was final2 (1739.8) and final3 (1768.2), which finished **1,287th**,
  about 270 places short.
- My strongest late-season bots weren't in that pair. **v46 was at 2233.6** when v48 retired it on
  Sep 28. v48 (1910.6) and v49 (1890.2) were also frozen above the final bronze line when they
  were replaced. On the last day, final1, an unmodified public probe that ended at 1357.9, is the
  submission that pushed v49 out of the active pair.
- August peaks were higher still (v24 2744.3, v28 2450.3), but they came from a much weaker field,
  and v24 wasn't even running my code.

A frozen rating is not a final result. Had v46 or v49 kept playing, their ratings would have kept
moving, so I can't claim either would have medalled. But the pattern is clear: in the last week I
kept spending submissions on small local edges and probes instead of protecting a slot for the
best bot already on the ladder.

What I'd do differently:

1. Lock the best live bot into one slot several days before the deadline, and experiment only in
   the other.
2. Never spend a final-day submission on a probe.
3. Trust live ladder evidence over local pools when choosing the final pair.
