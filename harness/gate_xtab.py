import json,sys,zipfile,csv,io,statistics,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from paths import ROOT, REPLAYS
z=zipfile.ZipFile(ROOT/"analysis"/"kaggriculture.zip"); nm=z.namelist()[0]
lb={r["TeamName"]:float(r["Score"]) for r in csv.DictReader(io.TextIOWrapper(z.open(nm),encoding="utf-8-sig"))}
g=json.load(open(ROOT/"analysis"/"gate_autopsy_v31_live.json",encoding="utf-8"))
clone=[r for r in g if r["prefix_agree"]>=124]
near=[r for r in g if 60<=r["prefix_agree"]<124]
other=[r for r in g if r["prefix_agree"]<60]
rec=lambda x:(sum(1 for r in x if r['outcome']=='WIN'),sum(1 for r in x if r['outcome']=='LOSS'),sum(1 for r in x if r['outcome']=='TIE'))
for lbl,grp in [("v43-clone (prefix==124)",clone),("near (60-123)",near),("other",other)]:
    rs=[lb[r["opponent"]] for r in grp if r["opponent"] in lb]
    print(f"{lbl}: n={len(grp)} rec={rec(grp)} wr={rec(grp)[0]/len(grp):.2f} "
          f"meanOppRating={statistics.mean(rs):.0f} meanGateFrac={statistics.mean(r['gate_frac'] for r in grp):.2f} "
          f"gate_ever={sum(1 for r in grp if r['gate_steps']>0)}/{len(grp)}")
print()
# cross tab gate vs clone
ct=collections.Counter()
for r in g: ct[(r["prefix_agree"]>=124, r["gate_steps"]>0)]+=1
print("crosstab (is_v43_clone, gate_ever_open):", dict(ct))
fp=[r for r in g if r["gate_steps"]>0 and r["prefix_agree"]<124]
print(f"FALSE-FIRE games (gate opened but opponent is NOT a v43 clone): {len(fp)}/{len(g)} = {len(fp)/len(g):.1%}")
print("  their record:", rec(fp), " mean gate_frac", round(statistics.mean(r['gate_frac'] for r in fp),3))
tf=[r for r in g if r["gate_steps"]>0 and r["prefix_agree"]>=124]
print(f"TRUE-FIRE games: {len(tf)} record {rec(tf)}")
mis=[r for r in g if r["gate_steps"]==0 and r["prefix_agree"]>=124]
print(f"MISSED clones (gate never opened vs a real v43 clone): {len(mis)} record {rec(mis)}")
# gate vs opponent rating
hi=[r for r in g if r["opponent"] in lb and lb[r["opponent"]]>=2000]
print(f"\ngate_ever rate vs opp>=2000: {sum(1 for r in hi if r['gate_steps']>0)}/{len(hi)}")
lo=[r for r in g if r["opponent"] in lb and lb[r["opponent"]]<2000]
print(f"gate_ever rate vs opp<2000: {sum(1 for r in lo if r['gate_steps']>0)}/{len(lo)}")

# divergence: in clone games do our market actions differ from opponent's in 160..700?
res=json.load(open(ROOT/"analysis"/"autopsy_v31_live.json",encoding="utf-8"))
byep={r["episode"]:r for r in res}
print("\n--- mirror divergence in v43-clone games (evidence the v31 layer acted) ---")
for r in clone:
    ep=r["episode"]; seat=byep[ep]["seat"]
    d=json.load(open(REPLAYS/f"episode-{ep}-replay.json",encoding="utf-8"))
    st=d["steps"]; diff=0; pre=0; first=None
    for t in range(160,min(700,len(st))):
        a=json.dumps((st[t][seat].get("action") or {}).get("market"),sort_keys=True)
        b=json.dumps((st[t][1-seat].get("action") or {}).get("market"),sort_keys=True)
        if a!=b:
            diff+=1
            if first is None: first=t
    for t in range(0,160):
        a=json.dumps((st[t][seat].get("action") or {}).get("market"),sort_keys=True)
        b=json.dumps((st[t][1-seat].get("action") or {}).get("market"),sort_keys=True)
        if a!=b: pre+=1
    print(f"  ep={ep} vs {r['opponent']!r} {r['outcome']} m={r['margin']:+.0f} gate_frac={r['gate_frac']:.2f} "
          f"market-diff steps 0-159={pre} 160-700={diff} first_diff={first}")
