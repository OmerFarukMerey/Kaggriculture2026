import requests, json, sys, collections, math
s=requests.Session(); s.headers['User-Agent']='Mozilla/5.0'
s.get('https://www.kaggle.com/competitions/kaggriculture/leaderboard',timeout=30)
H={'x-xsrf-token':s.cookies.get('XSRF-TOKEN'),'content-type':'application/json'}
def fetch(sid):
    r=s.post('https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes',json={"submissionId":sid},headers=H,timeout=60)
    r.raise_for_status(); d=r.json(); json.dump(d,open(f'analysis/final/live/list_{sid}.json','w')); return d
def perf(sid,d):
    rows=[]
    for e in d['episodes']:
        if e['state']!='COMPLETED': continue
        a=[x for x in e['agents'] if x['submissionId']==sid]; o=[x for x in e['agents'] if x['submissionId']!=sid]
        if not a or not o: continue
        a,o=a[0],o[0]
        if a.get('reward') is None or o.get('reward') is None: continue
        res=1 if a['reward']>o['reward'] else (0 if a['reward']<o['reward'] else .5)
        rows.append((e['createTime'],res,a.get('initialScore') or 0,o.get('initialScore') or 0,a.get('updatedScore') or 0,o['submissionId'],e['id']))
    rows.sort()
    return rows
if __name__=='__main__':
    for sid in map(int,sys.argv[1:]):
        d=fetch(sid); rows=perf(sid,d)
        if not rows: print(sid,'no rows'); continue
        last=rows[-40:]
        w=sum(r[1] for r in last); opp=sum(r[3] for r in last)/len(last)
        print(f"{sid}: n={len(rows)} first={rows[0][0][:16]} now={rows[-1][4]:.0f} last40: score={w}/{len(last)} oppavg={opp:.0f} all: {sum(r[1] for r in rows)}/{len(rows)}")
