import math, itertools
from ball import *
FT=0.3048
# App readings (machine at baseline center, Stand Off, Riser Off):
#  (1) 60 km/h, -500 rpm, middle row wide lane : OK,   height at net 10'0"
#  (2) 60 km/h,    0 rpm, middle row 2nd lane  : FAIL, height at net 10'2"   (shown at max tilt)
#  (3) 80 km/h,    0 rpm, middle row center    : OK,   height at net 4'10"
h1,h2,h3=10*FT,(10+2/12)*FT,(4+10/12)*FT
def dist(z,x): return math.hypot(z,x)
def netd(z,x): return NET*dist(z,x)/z
best=None
for cd in (0.50,0.55,0.60,0.65):
  for h0 in (0.3,0.4,0.5,0.6):
    p=dict(P,cd=cd,h0=h0)
    # theta_max from (2): flat 60 at max tilt crosses net at h2
    lo,hi=10,45
    for _ in range(40):
        mid=(lo+hi)/2; _,hn=fly(60,0,mid,h0,p,netd(19.8,1.6))
        if hn<h2: lo=mid
        else: hi=mid
    thm=hi; reach_flat60,_=fly(60,0,thm,h0,p)
    # zM from (3): flat 80 to center with net height h3
    lo,hi=0,25
    for _ in range(40):
        mid=(lo+hi)/2; d,hn=fly(80,0,mid,h0,p)
        if hn<h3: lo=mid
        else: hi=mid
    zM,_=fly(80,0,hi,h0,p)
    # cl scale from (1): -500@60 to the wide lane lands at dist(zM,3.2) with net height h1
    res=[]
    for cl in (0.6,0.8,1.0,1.2,1.4,1.6,2.0):
        p2=dict(p,cl=cl,th_max=thm); s=solve(60,-500,dist(zM,3.2),h0,p2,netd(zM,3.2))
        res.append((cl,s['ok'],round(s['hnet'] or 0,2),round(s.get('reach',0),1)))
    print(f"cd={cd} h0={h0}: th_max={thm:.1f}  flat60 max reach={reach_flat60:.1f}  zM={zM:.1f}  flat60 fails M? {reach_flat60<dist(zM,1.6)}  | -500@60 by cl:",res)
