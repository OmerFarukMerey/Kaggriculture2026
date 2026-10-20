import csv,json,statistics as st
from collections import defaultdict
res={r['episode']:r for r in json.load(open('scan30.json'))}
rows=[]
for r in csv.DictReader(open('episodes_v30.csv',newline='',encoding='utf-8')):
    if r['id'] in res:
        rows.append((r['endTime'][:10],r['endTime'],res[r['id']]))
rows.sort()
by=defaultdict(list)
for d,t,x in rows: by[d].append(x)
print('%-12s %5s %4s %4s %6s %10s %10s'%('date','n','W','L','wr','meanMargin','medMargin'))
cum=[]
for d in sorted(by):
    s=by[d]; W=sum(1 for x in s if x['outcome']=='WIN'); L=sum(1 for x in s if x['outcome']=='LOSS')
    print('%-12s %5d %4d %4d %6.3f %10.0f %10.0f'%(d,len(s),W,L,W/len(s),st.mean(x['margin'] for x in s),st.median(x['margin'] for x in s)))
print()
# rolling halves
n=len(rows); h=n//2
for lab,s in (('FIRST half (oldest)',[x for _,_,x in rows[:h]]),('SECOND half (newest)',[x for _,_,x in rows[h:]])):
    W=sum(1 for x in s if x['outcome']=='WIN');L=sum(1 for x in s if x['outcome']=='LOSS')
    print('%-22s n=%3d %d-%d wr=%.3f meanMargin=%+.0f medMargin=%+.0f'%(lab,len(s),W,L,W/len(s),st.mean(x['margin'] for x in s),st.median(x['margin'] for x in s)))
print()
for lab,s in (('last 60 games',[x for _,_,x in rows[-60:]]),('last 100 games',[x for _,_,x in rows[-100:]]),('first 100 games',[x for _,_,x in rows[:100]])):
    W=sum(1 for x in s if x['outcome']=='WIN');L=sum(1 for x in s if x['outcome']=='LOSS')
    print('%-16s %d-%d wr=%.3f meanMargin=%+.0f'%(lab,W,L,W/len(s),st.mean(x['margin'] for x in s)))
json.dump([[d,t,x] for d,t,x in rows],open('timeline30.json','w'),indent=1)
