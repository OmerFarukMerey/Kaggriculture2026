# Submissions

One directory per submitted artifact, frozen at the exact bytes sent to
Kaggle. Regenerate this table with `python package_submission.py --reindex`
after editing any `manifest.json`.

| # | Version | Built (UTC) | Submitted | main.py sha256 | Result | Message |
|---|---|---|---|---|---|---|
| [001](001-v21.2/) | v21.2 | 2026-08-06 | unknown | `5ac3cdf21fda` |  | v21.2: public-copy detection, one-step SELL front-running, step-717 terminal pre-dump |

## Packaging a new submission

```bash
python build_v212.py <base_proto_index> <mirror_threshold>   # writes main.py
python evaluate.py 3 all                                     # sanity-check it
python package_submission.py "what changed"                  # freezes the next NNN
```

Archives are reproducible (tar/gzip timestamps pinned to 0), so re-packaging
an unchanged `main.py` yields a byte-identical `.tar.gz`.

After Kaggle accepts one, set `"submitted": true` and fill in `"result"`
in that submission's `manifest.json`, then re-run `--reindex`.
