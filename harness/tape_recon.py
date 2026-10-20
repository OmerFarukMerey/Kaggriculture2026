"""Characterise an opponent tape directly from replays: opening order, animal/seed
mix, hire cadence, sell cadence, and a first-K action fingerprint for clustering."""
import json, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS

def acts(ep, seat, k=48):
    rep = json.load(open(REPLAYS / f"episode-{ep}-replay.json", encoding="utf-8"))
    return [rep["steps"][t + 1][seat].get("action") for t in range(min(k, len(rep["steps"]) - 1))], rep

def fp(a, k=24):
    """Coarse fingerprint: farmer verb + market verbs, per step."""
    out = []
    for x in a[:k]:
        if not isinstance(x, dict):
            out.append("?"); continue
        f = (x.get("farmer") or ["-"])[0]
        mk = "".join(sorted(set((m[0][0] + (m[1][0] if len(m) > 1 and isinstance(m[1], str) else "")) for m in (x.get("market") or []))))
        h = "".join((hh or ["-"])[0][0] for hh in (x.get("hands") or []))
        out.append(f"{f[:4]}|{mk}|{h}")
    return ";".join(out)

def profile(a):
    buy_animal = collections.Counter(); buy_seed = collections.Counter()
    sells = collections.Counter(); hires = 0; verbs = collections.Counter()
    for t, x in enumerate(a):
        if not isinstance(x, dict): continue
        verbs[(x.get("farmer") or ["-"])[0]] += 1
        for m in (x.get("market") or []):
            if m[0] == "BUY_ANIMAL": buy_animal[m[1]] += m[2] if len(m) > 2 else 1
            elif m[0] == "BUY_SEED": buy_seed[m[1]] += m[2] if len(m) > 2 else 1
            elif m[0] == "HIRE": hires += 1
            elif m[0].startswith("SELL"): sells[t % 24] += 1
    return buy_animal, buy_seed, hires, sells, verbs

if __name__ == "__main__":
    pairs = json.load(open(sys.argv[1], encoding="utf-8"))   # [[ep, seat], ...]
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    groups = collections.Counter(); ex = {}
    for ep, seat in pairs:
        try: a, rep = acts(ep, seat, 48)
        except Exception as e: print("skip", ep, e); continue
        f = fp(a, K)
        groups[f] += 1; ex.setdefault(f, (ep, seat, a))
    print(f"{len(pairs)} tapes -> {len(groups)} distinct {K}-step fingerprints")
    for f, n in groups.most_common(8):
        ep, seat, a = ex[f]
        ba, bs, hi, se, vb = profile(a)
        print(f"\n--- cluster n={n}  example ep{ep} seat{seat}")
        print(f"    animals={dict(ba)} seeds={dict(bs)} hires(first48)={hi}")
        print(f"    farmer verbs={dict(vb.most_common(8))}")
        for t in range(min(12, len(a))):
            print(f"      t{t:2d} {json.dumps(a[t])[:170]}")
