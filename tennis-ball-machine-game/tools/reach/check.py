import math, csv, re, sys, json
from ball import *
p=dict(P,cd=0.50,h0=0.40,th_max=28.6,cl=0.6,net_clear=1.15)
ROWZ={'S':14.8,'M':19.1,'D':21.8}; COLX={'FW':-3.3,'F':-1.65,'C':0,'B':1.65,'BW':3.3}
MPOS={'BC':(0,0),'BB':(0,-2.0),'CL':(-4.1,0),'CR':(4.1,0),'SC':(0,5.49),'NC':(0,10.4)}
SPEED={"S1":60,"S2":70,"S3":80,"S4":90}; SPIN={"Flat":0,"Top 1":500,"Top 2":1000,"Top 3":2000,"Slice 1":-500}
SPEEDS=list(range(60,115,5))
def geom(pos,d,l):
    mx,mz=MPOS[pos]; dx=COLX[l]-mx; dz=ROWZ[d]-mz; dist=math.hypot(dx,dz); xn=(NET-mz)/dz*dist
    return dist,xn
def test(pos,d,l,v,rpm,riser=False,h0=0.40):
    dist,xn=geom(pos,d,l)
    return solve(v,rpm,dist,h0,p,xn,th_max=p['th_max']+(25 if riser else 0))
def window(pos,d,l,rpm,riser=False):
    return [v for v in SPEEDS if test(pos,d,l,v,rpm,riser)['ok']]
if __name__=="__main__":
    print("WORKING SPEEDS from baseline center, machine on the ground, riser off (km/h)")
    print("%-22s"%"spin"+"".join("%-16s"%r for r in ("front row","middle row","back row")))
    for name,rpm in (("-500 backspin",-500),("0 flat",0),("+500 topspin",500),("+1000 topspin",1000),("+2000 topspin",2000)):
        out="%-22s"%name
        for d in "SMD":
            w=[v for v in SPEEDS if all(test('BC',d,l,v,rpm)['ok'] for l in ('C','FW'))]
            out+="%-16s"%(f"{w[0]}-{w[-1]}" if w else "none")
        print(out)
    sys.path.insert(0,'/home/user/games/tennis-ball-machine-game/tools')
    src=open('/home/user/games/tennis-ball-machine-game/tools/render.py').read(); src=src[:src.index("# ---------- card")]
    sys.argv=["x","/home/user/games/tennis-ball-machine-game"]; ns={}; exec(src,ns)
    rows=list(csv.DictReader(open('/home/user/games/tennis-ball-machine-game/levels.csv')))
    bad={}
    for r in rows:
        if r['stand']!='Off': continue
        rnd,shots=ns['parse'](r)
        for s in shots:
            t=test(r['pos'],s['depth'],s['lane'],s['speed'],ns['SPIN'][s['spin']],riser=(r['riser']=='ON'))
            if not t['ok']:
                w=window(r['pos'],s['depth'],s['lane'],ns['SPIN'][s['spin']],riser=(r['riser']=='ON'))
                bad.setdefault(int(r['level']),[]).append((s['depth']+'-'+s['lane'],s['speed'],s['spin'],t['reason'],(w[0],w[-1]) if w else None))
    print(f"\nLEVELS (machine on the ground) with at least one shot the model says can't hit: {len(bad)} of {sum(1 for r in rows if r['stand']=='Off')}")
    by={}
    for n,b in bad.items(): by.setdefault(tuple(sorted({x[3] for x in b})),[]).append(n)
    for k,v in by.items(): print("  ",k,len(v),v)
    for n in sorted(bad)[:400]:
        r=rows[n-1]; print(f"  L{n:<3} {r['pos']} {r['name'][:22]:22}", "; ".join(f"{a} {v}km/h {sp} -> {why} (works: {w})" for a,v,sp,why,w in bad[n]))
