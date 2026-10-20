import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import pull_all
from paths import ROOT
tag=sys.argv[1]; stride=int(sys.argv[2]); off=int(sys.argv[3])
idx=json.load(open(ROOT/"analysis"/"eps2"/"index.json"))
idx[tag]=list(reversed(idx[tag]))
tmp=ROOT/"analysis"/"eps2"/f"index_rev_{tag.replace('.','_')}.json"
json.dump(idx,open(tmp,"w"))
_orig=json.load
def patched(f,*a,**k):
    return json.loads(open(tmp,encoding="utf-8").read()) if getattr(f,"name","").endswith("index.json") else _orig(f,*a,**k)
json.load=patched
pull_all.main(tag,stride,off)
