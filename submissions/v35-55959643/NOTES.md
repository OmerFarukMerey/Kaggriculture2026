# v35

| | |
| :--- | :--- |
| Kaggle submission | `55959643` |
| Submitted | 2026-09-02 |
| Live score | *pending* |
| Content | **byte-identical to [v24](../v24-55428059/NOTES.md)** (sha256 `032ab3cd0a1dabbfb3e7`) |

## What this is

v24's exact bytes resubmitted, at the user's request, because v24 holds the highest *posted* score of
any submission (2744.3).

## Two things this is not

**It does not run the v24 layer stack.** `harness/check_entrypoint.py` resolves these bytes to
`agent()` — the stock Rayk C94 chassis. The track-gated copy escalation and the boatlee layer are
present in the file but never execute, because of the loader bug (see
[LESSONS #1](../../docs/LESSONS.md)). What ships here is C94-core alone.

**The 2744.3 does not transfer.** That score was earned 2026-08-11 against a much weaker, more
heterogeneous field. Opponent-adjusted over its 65 rated episodes it is **1857 [1672, 2091]**, versus
v32/v34's **2285** on the same scale. Cross-era posted scores are not comparable: implied opponent
strength at match time versus today's rating drifts −1073 for v24, and there is no shared-opponent
bridge between the eras.

Expect this to settle near stock C94's level (adjusted ~1671–1857), below v34.

## Cost

Effectively zero at submission time — both live bots sat at ~1718, and it evicted v33 (the older of
the pair), leaving {v34, v35}.

## Files

- `main.py`
- `submission.tar.gz`

---
Rebuild with `py -3.12 tools/package.py submissions/v35-55959643/main.py --check`.
