import sys, csv
sys.argv=["x","/home/user/games/tennis-ball-machine-game"]
from check import *
src=open('/home/user/games/tennis-ball-machine-game/tools/render.py').read(); src=src[:src.index("# ---------- card")]
ns={}; exec(src,ns)
rows=list(csv.DictReader(open('/home/user/games/tennis-ball-machine-game/levels.csv')))
cls={'model':[], 'front':[], 'pos':[], 'apex':[], 'riser':[]}
print("EDGE CASES among levels the model can judge (middle/back row, machine on the ground at the baseline, behind it, or in a corner):")
for r in rows:
    n=int(r['level']); rnd,shots=ns['parse'](r)
    if r['stand']!='Off': cls['apex'].append(n); continue
    if r['riser']=='ON': cls['riser'].append(n); continue
    if r['pos'] in('SC','NC'): cls['pos'].append(n); continue
    if any(s['depth']=='S' for s in shots): cls['front'].append(n); continue
    cls['model'].append(n)
    for s in shots:
        rpm=ns['SPIN'][s['spin']]; w=window(r['pos'],s['depth'],s['lane'],rpm)
        v=s['speed']
        if not w or v<w[0] or v>w[-1] or v-w[0]<5 or (w[-1]-v<5 and not (rpm>=0 and s['depth']=='M' and v==90)):
            print(f"  L{n:<3} {r['pos']} {r['name'][:24]:24} {s['depth']}-{s['lane']:2} {v} km/h {s['spin']:8} works {w[0] if w else '-'}-{w[-1] if w else '-'}")
print({k:(len(v),v) for k,v in cls.items()})
