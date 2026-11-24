"""Tennis-ball flight model for the Proton: drag + spin lift, limited launch angle.
Calibrated against readings from the Proton app (see calib())."""
import math
G=9.81; M=0.0577; R=0.033; A=math.pi*R*R; RHO=1.2
NET=11.885
P=dict(cd=0.55, cl=1.0, h0=0.40, th_max=26.0, th_min=-10.0, zM=19.8, zS=14.7, zD=22.1, net_clear=1.0)

def fly(v_kmh, rpm, theta_deg, h0, p=P, x_net=NET, dt=0.002):
    """returns (landing distance, height when crossing x_net or None)"""
    v=v_kmh/3.6; th=math.radians(theta_deg)
    x,y=0.0,h0; vx,vy=v*math.cos(th),v*math.sin(th)
    kd=RHO*A*p['cd']/(2*M); w=abs(rpm)*2*math.pi/60; sgn=-1 if rpm>0 else 1  # topspin pushes down
    hn=None
    while y>0 or vy>0:
        sp=math.hypot(vx,vy)
        cl=p['cl']/(2+sp/(R*w)) if w>0 else 0.0
        kl=RHO*A*cl/(2*M)
        ax=-kd*sp*vx + sgn*kl*sp*(-vy)
        ay=-G-kd*sp*vy + sgn*kl*sp*(vx)
        nx=x+vx*dt; ny=y+vy*dt
        if hn is None and nx>=x_net: hn=y+(ny-y)*(x_net-x)/(nx-x)
        if ny<=0 and vy<0:
            return x+(nx-x)*y/(y-ny), hn
        x,y=nx,ny; vx+=ax*dt; vy+=ay*dt
        if x>60: break
    return x,hn

def solve(v_kmh, rpm, dist, h0, p=P, x_net=NET, th_max=None, th_min=None):
    """lowest launch angle that lands at dist. returns dict(ok, theta, hnet, reason)"""
    th_max=p['th_max'] if th_max is None else th_max; th_min=p['th_min'] if th_min is None else th_min
    lo,hi=th_min,th_max
    d_hi,h_hi=fly(v_kmh,rpm,hi,h0,p,x_net)
    if d_hi<dist: return dict(ok=False,theta=hi,hnet=h_hi,reason='short',reach=d_hi)
    d_lo,_=fly(v_kmh,rpm,lo,h0,p,x_net)
    if d_lo>dist: return dict(ok=False,theta=lo,hnet=None,reason='long',reach=d_lo)
    for _ in range(40):
        mid=(lo+hi)/2; d,_=fly(v_kmh,rpm,mid,h0,p,x_net)
        if d<dist: lo=mid
        else: hi=mid
    d,hn=fly(v_kmh,rpm,hi,h0,p,x_net)
    if x_net is not None and x_net>0 and dist>x_net and (hn is None or hn<p['net_clear']):
        return dict(ok=False,theta=hi,hnet=hn,reason='net',reach=d)
    return dict(ok=True,theta=hi,hnet=hn,reason='',reach=d)
