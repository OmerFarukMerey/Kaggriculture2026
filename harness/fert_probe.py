"""Measure FERTILIZER sell volume / market-slot usage / price impact for a given agent file."""
import importlib.util, sys, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import resolve_agent  # noqa: E402

def load(tag, fn):
    spec = importlib.util.spec_from_file_location(tag, resolve_agent(fn))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def probe(fa, fb, seed=5000):
    from kaggle_environments import make
    a, b = load("pa", fa), load("pb", fb)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run([a.agent, b.agent])
    st = env.steps
    sold = Counter(); sell_actions = Counter(); slots = []
    for t in range(len(st)):
        act = st[t][0].get("action")
        if not act: continue
        mk = act.get("market", []) or []
        slots.append(len(mk))
        for m in mk:
            if m and m[0] == "SELL":
                sell_actions[m[1]] += 1
                sold[m[1]] += (m[2] if len(m) > 2 else 1)
    px = [(t, dict(st[t][0]["observation"]["market"]["prices"]).get("FERTILIZER"))
          for t in (0, 120, 240, 360, 480, 600, 719)]
    print(f"--- {fa} vs {fb} seed={seed} final={[s.reward for s in st[-1]]}")
    print(f"  FERTILIZER: {sold['FERTILIZER']} units in {sell_actions['FERTILIZER']} sell actions")
    print(f"  all sold units: {dict(sold.most_common())}")
    print(f"  total sell actions: {sum(sell_actions.values())}")
    print(f"  market slots used: mean {sum(slots)/len(slots):.2f}, at-cap(10) on {sum(1 for s in slots if s>=10)} steps of {len(slots)}")
    print(f"  FERTILIZER price: {px}")

if __name__ == "__main__":
    probe(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 5000)
