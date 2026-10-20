import json, collections, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT
A=json.load(open(ROOT/"analysis"/"autopsy_v30.json",encoding="utf-8"))
sets={}
for stem in ("autopsy_v31_live","autopsy_v43_live"):
    p=ROOT/"analysis"/f"{stem}.json"
    if p.exists(): sets[stem]=json.load(open(p,encoding="utf-8"))
oldopp=set(r["opponent"] for r in A)
print(f"v30: n={len(A)} distinct opponents={len(oldopp)}")
for stem,rs in sets.items():
    new=set(r["opponent"] for r in rs)
    ov=new & oldopp
    print(f"{stem}: n={len(rs)} distinct={len(new)} overlap with v30 field={len(ov)} ({len(ov)/len(new):.1%})")
    # per-episode share
    shared_eps=sum(1 for r in rs if r["opponent"] in oldopp)
    print(f"   episodes vs an opponent v30 also met: {shared_eps}/{len(rs)} = {shared_eps/len(rs):.1%}")
    rec=lambda g:(sum(1 for r in g if r['outcome']=='WIN'),sum(1 for r in g if r['outcome']=='LOSS'),sum(1 for r in g if r['outcome']=='TIE'))
    old=[r for r in rs if r["opponent"] in oldopp]; nw=[r for r in rs if r["opponent"] not in oldopp]
    print(f"   vs returning opponents {rec(old)} n={len(old)}; vs new opponents {rec(nw)} n={len(nw)}")
if len(sets)==2:
    a=set(r["opponent"] for r in sets["autopsy_v31_live"]); b=set(r["opponent"] for r in sets["autopsy_v43_live"])
    print(f"\nv31 vs v43 opponent overlap: {len(a&b)} of {len(a|b)} union")
    # head to head common opponents
    ra=collections.defaultdict(list); rb=collections.defaultdict(list)
    for r in sets["autopsy_v31_live"]: ra[r["opponent"]].append(r)
    for r in sets["autopsy_v43_live"]: rb[r["opponent"]].append(r)
    common=sorted(a&b)
    aw=al=bw=bl=0
    for o in common:
        for r in ra[o]:
            aw+= r["outcome"]=="WIN"; al+= r["outcome"]=="LOSS"
        for r in rb[o]:
            bw+= r["outcome"]=="WIN"; bl+= r["outcome"]=="LOSS"
    print(f"restricted to the {len(common)} shared opponents: v31 {aw}W-{al}L  v43 {bw}W-{bl}L")
