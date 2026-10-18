"""Points of D with x, y, u in Q(i): u a Gaussian-rational root of t^3 - d t^2 + conj(d) t - 1."""
import itertools, sys, math
from fractions import Fraction as F
from math import isqrt
N=int(sys.argv[1])
def circ(t):
    d=1+t*t; return ((1-t*t)/d,(2*t)/d)
pts=[circ(F(p,q)) for q in range(1,N+1) for p in range(-N,N+1) if math.gcd(p,q)==1]+[(F(-1),F(0))]
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a): return (a[0],-a[1])
def add(*a): return (sum(z[0] for z in a),sum(z[1] for z in a))
def sc(s,a): return (s*a[0],s*a[1])
def inv(a): n=a[0]**2+a[1]**2; return (a[0]/n,-a[1]/n)
def rsqrt(r):
    if r<0: return None
    a,b=isqrt(r.numerator),isqrt(r.denominator)
    return F(a,b) if a*a==r.numerator and b*b==r.denominator else None
def csqrt(z):
    n=rsqrt(z[0]**2+z[1]**2)
    if n is None: return None
    re=rsqrt((z[0]+n)/2)
    if re is None: return None
    if re==0:
        im=rsqrt(-z[0]) ; return (F(0),im) if im is not None else None
    return (re,z[1]/(2*re))
ONE=(F(1),F(0))
units=[ONE,(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1))]
out=[]
for x,u in itertools.product(pts,repeat=2):
    a=add(mul(u,u),sc(-1,mul(x,u)))
    b=add(mul(x,mul(u,u)),sc(-1,mul(conj(x),u)),sc(-1,add(ONE,sc(-1,mul(u,mul(u,u))))))
    c=add(mul(conj(x),mul(u,u)),sc(-1,u))
    if a==(0,0): continue
    disc=add(mul(b,b),sc(-4,mul(a,c)))
    s=csqrt(disc)
    if s is None: continue
    for sg in (1,-1):
        y=mul(add(sc(-1,b),sc(sg,s)),inv(sc(2,a)))
        if y[0]**2+y[1]**2!=1: continue
        tr=[x,y,conj(mul(x,y))]
        d=sc(-1,add(*tr))
        if any(z in units for z in tr+[u]): continue
        if any(tr[i]==sc(-1,tr[j]) or tr[i]==tr[j] for i in range(3) for j in range(3) if i!=j): continue
        q1=add(u,sc(-1,d)); q0=add(mul(u,u),sc(-1,mul(d,u)),conj(d))
        dd=add(mul(q1,q1),sc(-4,q0))
        h=max(z.denominator for z in x+y+u)
        out.append((h,x,y,u,dd,csqrt(dd) is not None))
out.sort(key=lambda o:o[0])
print(len(out))
for o in out[:6]: print(o[0],[str(z) for z in o[1]+o[2]+o[3]],"disc",[str(z) for z in o[4]],"square",o[5])
