"""Extract an opponent's recorded 720-step action stream into a standalone open-loop agent."""
import json, sys, zlib, base64
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS
name, out = sys.argv[1], sys.argv[2]
eps = sys.argv[3:]
streams = []
for ep in eps:
    r = json.load(open(REPLAYS/f"episode-{ep}-replay.json", encoding="utf-8"))
    t = r["info"]["TeamNames"]
    if name not in t: print("not in", ep, t); continue
    s = t.index(name)
    acts = [r["steps"][k][s].get("action") for k in range(len(r["steps"]))]
    streams.append(acts)
base = streams[0]
for o in streams[1:]:
    n=min(len(base),len(o))
    d=sum(1 for i in range(n) if json.dumps(base[i],sort_keys=True)!=json.dumps(o[i],sort_keys=True))
    print(f"  cross-episode diffs: {d}/{n}")
# actions recorded at index t were produced from observation t-1 -> shift by one
route = base[1:] + [base[-1]]
blob = base64.b85encode(zlib.compress(json.dumps(route).encode(), 9)).decode()
src = f'''"""Open-loop replay of {name}'s recorded route (extracted from public replays {eps})."""
import base64, json, zlib

_ROUTE = json.loads(zlib.decompress(base64.b85decode(
    "{blob}"
)).decode())


def _extracted_route_entrypoint(obs, config=None):
    step = int((obs.get("step", 0) if hasattr(obs, "get") else getattr(obs, "step", 0)) or 0)
    if step < len(_ROUTE):
        a = _ROUTE[step]
        if a is not None:
            return a
    return {{"farmer": ["PASS"], "hands": [], "market": []}}


agent = _extracted_route_entrypoint
'''
Path(out).write_bytes(src.encode())
print("wrote", out, len(src), "bytes; route steps:", len(route))
