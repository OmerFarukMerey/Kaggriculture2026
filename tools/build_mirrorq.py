"""Append the mirror-queue edge layer to a base agent, preserving the base bytes exactly.

    py -3.12 tools/build_mirrorq.py <base main.py> <out main.py> [--tag NAME]

The layer wraps whatever callable Kaggle's loader would select from the base file. When the
opponent's public farm is identical to ours (an exact or near-exact copy of the same policy),
it assumes the rival submits the same market list our base just produced and re-orders OUR
list to take the upper rungs of the shared price ladder. A re-ordering is accepted only if it
executes exactly the same quantities as the unmodified list and strictly increases our cash.
Otherwise the base action is returned untouched.

Exact market rules come from agents/v50/_engine.py (mechanically extracted from
kaggle-environments 1.32.7, Apache-2.0) and agents/v50/mechanics.py; they are embedded as a
string and executed in a private namespace so no base-module global is shadowed.
"""
import ast
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "agents" / "v50" / "_engine.py"
MECH = ROOT / "agents" / "v50" / "mechanics.py"


def engine_source():
    eng = ENGINE.read_text(encoding="utf-8")
    mech = MECH.read_text(encoding="utf-8")
    tree = ast.parse(mech)
    keep = {"price", "project_units", "execute_market"}
    parts = [ast.get_source_segment(mech, n) for n in tree.body
             if isinstance(n, ast.FunctionDef) and n.name in keep]
    header = ("from copy import deepcopy\n"
              "PRODUCTS = tuple(PRODUCTS)\n"
              "SEED_PRICE = {item: p['seed'] for item, p in CROPS.items()}\n"
              "ANIMAL_COST = {item: p['cost'] for item, p in ANIMALS.items()}\n"
              "_PRICE_PARAMS = object()\n_PRICE_COLUMNS = {}\n_PRICE_CACHE = {}\n")
    body = "\n\n".join(parts).replace("rules.", "")
    return eng + "\n\n" + header + "\n" + body + "\n"


LAYER = r'''

# ======================================================================
# Mirror-queue edge (appended; everything above is the unmodified base).
# Kaggriculture processes both players' market slots aligned by index, one
# unit at a time, quoting both units before committing either. Against an
# exact copy of this policy both lists are identical and the game is a coin
# tie. When the opponent's public farm equals ours, we assume the rival list
# equals our base list and re-order OUR list (sells only move earlier or
# permute within runs of sells, so funding is never delayed). A candidate is
# kept only if it executes exactly the same quantities as the base list and
# strictly increases our cash. Engine rules: kaggle-environments 1.32.7
# (Apache-2.0), executed in a private namespace.
# ======================================================================
import itertools as _mq_itertools
import time as _mq_time
_MQ_SRC = __MQ_SRC__
_MQ = {"__name__": "_mq_engine"}
exec(compile(_MQ_SRC, "_mq_engine", "exec"), _MQ)
_MQ_BASE = [_mq_v for _mq_v in list(globals().values()) if callable(_mq_v)][-1]
_MQ_TAG = __MQ_TAG__
_MQ_V2 = __MQ_V2__
_MQ_MAX_PERMS = 120
_MQ_MAX_CANDS = 240
_MQ_BUDGET = 0.08
_MQ_REPORT = {"gated": 0, "changed": 0, "gain": 0.0, "errors": 0}


def _mq_gate(obs):
    me = int(obs["player"])
    farms = obs["farms"]
    a, b = farms[me], farms[1 - me]
    return (a.get("tiles") == b.get("tiles")
            and a.get("unlocked_quadrants") == b.get("unlocked_quadrants")
            and len(a.get("hands") or []) == len(b.get("hands") or [])
            and a.get("farmer") == b.get("farmer"))


def _mq_is_sell(order):
    return isinstance(order, (list, tuple)) and len(order) >= 3 and order[0] == "SELL"


def _mq_candidates(market):
    """Yield re-orderings: sells may move earlier, or permute inside runs of sells."""
    n = len(market)
    seen = {tuple(map(tuple, market))}
    sells = [i for i, o in enumerate(market) if _mq_is_sell(o)]
    # move one sell earlier to any position
    for i in sells:
        for j in range(i):
            cand = market[:j] + [market[i]] + market[j:i] + market[i + 1:]
            key = tuple(map(tuple, cand))
            if key not in seen:
                seen.add(key)
                yield cand
    # permute each maximal run of consecutive sells
    i = 0
    while i < n:
        if not _mq_is_sell(market[i]):
            i += 1
            continue
        j = i
        while j < n and _mq_is_sell(market[j]):
            j += 1
        if j - i >= 2:
            for k, perm in enumerate(_mq_itertools.permutations(market[i:j])):
                if k >= _MQ_MAX_PERMS:
                    break
                cand = market[:i] + list(perm) + market[j:]
                key = tuple(map(tuple, cand))
                if key not in seen:
                    seen.add(key)
                    yield cand
        i = j


def _mq_candidates_v2(market):
    """v1 moves plus adjacent swaps of any two orders and one empty-slot insertion.

    Every candidate is still checked in simulation for identical executed
    quantities, so a swap that starves a purchase of funding is rejected.
    """
    seen = set()
    for cand in _mq_candidates(market):
        seen.add(tuple(map(tuple, cand)))
        yield cand
    n = len(market)
    for i in range(n - 1):
        cand = list(market)
        cand[i], cand[i + 1] = cand[i + 1], cand[i]
        key = tuple(map(tuple, cand))
        if key not in seen:
            seen.add(key)
            yield cand
    if n < 10:
        for i in range(n):
            cand = market[:i] + [[]] + market[i:]
            key = tuple(map(tuple, cand))
            if key not in seen:
                seen.add(key)
                yield cand


def _mq_totals(executed):
    out = {}
    for slot, op, item, qty in executed:
        out[(op, item)] = out.get((op, item), 0) + qty
    return out


def _mq_edge(obs, config, action):
    market = [list(o) for o in (action.get("market") or []) if isinstance(o, (list, tuple))]
    if len(market) != len(action.get("market") or []):
        return action
    if sum(1 for o in market if _mq_is_sell(o)) < 1 or len(market) < (1 if _MQ_V2 else 2):
        return action
    if not _mq_gate(obs):
        return action
    _MQ_REPORT["gated"] += 1
    farm, private = _MQ["project_units"](obs, action, config)
    inventory = dict(obs["market"]["inventory"])
    base = _MQ["execute_market"](market, market, farm, private, inventory, None, config)
    want = _mq_totals(base["executed"])
    best, best_money = None, base["money"]
    started = _mq_time.perf_counter()
    for k, cand in enumerate((_mq_candidates_v2 if _MQ_V2 else _mq_candidates)(market)):
        if k >= _MQ_MAX_CANDS or _mq_time.perf_counter() - started > _MQ_BUDGET:
            break
        res = _MQ["execute_market"](cand, market, farm, private, inventory, None, config)
        if res["money"] > best_money + 0.5 and _mq_totals(res["executed"]) == want:
            best, best_money = cand, res["money"]
    if best is None:
        return action
    _MQ_REPORT["changed"] += 1
    _MQ_REPORT["gain"] += best_money - base["money"]
    out = dict(action)
    out["market"] = best
    return out


def mirror_queue_agent(observation, configuration=None):
    action = _MQ_BASE(observation, configuration)
    try:
        if isinstance(action, dict):
            return _mq_edge(observation, configuration or {}, action)
    except Exception:
        _MQ_REPORT["errors"] += 1
    return action


mirror_queue_agent.telemetry = _MQ_REPORT
agent = mirror_queue_agent
agent = globals().pop("agent")
'''


def main():
    base_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    tag = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else "mirrorq"
    base = base_path.read_bytes()
    layer = (LAYER.replace("__MQ_SRC__", repr(engine_source())).replace("__MQ_TAG__", repr(tag))
             .replace("__MQ_V2__", repr("--v2" in sys.argv)))
    out = base + layer.encode("utf-8")
    compile(out, str(out_path), "exec")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(out)
    print(f"{out_path}: base {len(base):,} B sha {hashlib.sha256(base).hexdigest()[:12]} -> "
          f"{len(out):,} B sha {hashlib.sha256(out).hexdigest()[:12]}")


if __name__ == "__main__":
    main()
