"""Where does a v43-family OPPONENT deviate from stock kaito_v43? Full 720 steps."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import REPLAYS
import clone_probe as cp
for ep in sys.argv[1:]:
    r = json.load(open(REPLAYS/f"episode-{ep}-replay.json", encoding="utf-8"))
    teams = r["info"]["TeamNames"]
    for seat in (0,1):
        m,c,per = cp.probe(r, seat, 719)
        # first deviation, and deviation count by 120-step block
        first = next((i for i,x in enumerate(per) if not x), None)
        blocks = []
        for b in range(0, len(per), 60):
            seg = per[b:b+60]
            blocks.append(f"{sum(1 for x in seg if not x):2d}")
        print(f"{ep} seat{seat} {teams[seat][:22]:24s} match={m}/{c}={m/max(c,1):.3f} firstdev={first} devs-per-60: {' '.join(blocks)}", flush=True)
