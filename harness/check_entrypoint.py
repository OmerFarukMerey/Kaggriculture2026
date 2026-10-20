"""Report which callable Kaggle's loader will actually run for an agent file.

    py -3.12 harness/check_entrypoint.py <agent> [<agent> ...]

Kaggle resolves an agent with `get_last_callable`, which returns the last
callable *by dict insertion order*. Rebinding an existing name does not move it,
so `agent = my_wrapper` at the end of a file leaves `agent` in its original
position and a different callable gets picked. This prints the resolved name so
you can confirm your entrypoint is the one that runs. See docs/LESSONS.md #1.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, resolve_agent  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return 2
    from kaggle_environments.agent import get_last_callable
    bad = 0
    for ref in sys.argv[1:]:
        path = resolve_agent(ref)
        fn = get_last_callable(path.read_text(encoding="utf-8"))
        flag = "  <-- generic name; is this really your entrypoint?" if fn.__name__ == "agent" else ""
        print(f"{ref:24} {path.relative_to(ROOT)}\n"
              f"{'':24} resolves to {fn.__name__}() argcount={fn.__code__.co_argcount}{flag}")
        bad += fn.__name__ == "agent"
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
