"""Show the OPPONENT's actual action vs what stock kaito_v43 would have done, at deviating steps."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import REPLAYS
import clone_probe as cp

ep = sys.argv[1]; seat = int(sys.argv[2])
lo = int(sys.argv[3]) if len(sys.argv)>3 else 0
hi = int(sys.argv[4]) if len(sys.argv)>4 else 400
r = json.load(open(REPLAYS/f"episode-{ep}-replay.json", encoding="utf-8"))
steps = r["steps"]; cfg = r.get("configuration") or {}
fn = cp.fresh_v43()
shown = 0
for t in range(lo, min(hi, len(steps)-1)):
    obs = dict(steps[t][seat]["observation"])
    obs.setdefault("step", steps[t][0]["observation"].get("step", t))
    obs.setdefault("player", seat)
    try: pred = fn(obs, cfg)
    except Exception as e: pred = {"ERR": str(e)}
    act = steps[t+1][seat].get("action")
    if act is None: continue
    if cp.norm(pred) == cp.norm(act): continue
    shown += 1
    day, hour = t//24, t%24
    def brief(a):
        if not a: return str(a)
        return f"F={a.get('farmer')} H={a.get('hands')} M={a.get('market')}"
    print(f"--- t={t} d{day}h{hour}")
    print(f"    v43 : {brief(pred)}")
    print(f"    them: {brief(act)}")
    if shown >= int(sys.argv[5] if len(sys.argv)>5 else 20): break
