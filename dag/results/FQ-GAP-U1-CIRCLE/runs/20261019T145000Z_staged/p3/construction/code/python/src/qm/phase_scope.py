"""Exact local operations for ten scoped PFP steps; no completion/status oracle."""
from fractions import Fraction as Q
from pathlib import Path


def binary_ray(x,y):
    return Q(1 if x*y>0 or (x*y==0 and y==0) else 0)


def probe(a,b,c,d,x,y):
    return [x*x,y*y,(a*x+b*y)**2,(c*x+d*y)**2,
            (a*x-b*y)**2,(c*x-d*y)**2,4*a*b*x*y,4*c*d*x*y]


def evaluate(kind,values,root=None):
    if kind in ('corpus','custody'):
        data=(Path(root)/values[0]).read_bytes()
        # These are literal byte counts, not an axiom or proof audit.
        return list(map(str,[len(data),data.count(b'\n'),data.count(b'sorry'),
                             data.count(b'Classical.choice'),data.count(b'axiom')]))
    xs=[Q(v) for v in values]
    if kind=='continuum':
        a,b,l=xs;out=[2*a,2*b,l*l-l-1,(2*l-1)**2, Q(5)]
    elif kind=='tensor':
        a,b,c,d=xs;v=[a*c,a*d,b*c,b*d]
        out=v+[v[0]*v[3]-v[1]*v[2],sum(z*z for z in v),(a*a+b*b)*(c*c+d*d)]
    elif kind=='u1':
        t,k=xs
        if k.denominator!=1 or abs(k)>32:raise ValueError('bounded integer exponent')
        re,im=(1-t*t)/(1+t*t),2*t/(1+t*t)
        z,w=Q(1),Q(0);base=(Q(3,5),Q(4,5) if k>=0 else Q(-4,5))
        for _ in range(abs(int(k))):z,w=z*base[0]-w*base[1],z*base[1]+w*base[0]
        out=[re,im,re*re+im*im,re+1,im/(re+1),z,w,z*z+w*w]
    elif kind=='d2':
        x,y,k,u,v=xs
        if k==0 or (x==0 and y==0) or (u==0 and v==0):raise ValueError('nonzero rays and scale')
        out=[binary_ray(x,y),binary_ray(k*x,k*y),binary_ray(-y,x),x*u+y*v,
             binary_ray(u,v),x*x+x*y,binary_ray(x,y)*(x*x+y*y)]
    elif kind in ('interference','zero'):
        out=probe(*xs)
    elif kind=='fiber':
        a,b=xs
        if a.denominator!=1 or b.denominator!=1 or abs(a)+abs(b)>10:raise ValueError('bounded integral Gaussian input')
        a,b=int(a),int(b);n=a*a+b*b;r=abs(a)+abs(b)
        orbit=sorted(set([(a,b),(-b,a),(-a,-b),(b,-a)]))
        fiber=[(x,y) for x in range(-r,r+1) for y in range(-r,r+1) if x*x+y*y==n]
        out=[n,len(orbit),len(fiber)]+[z for pair in orbit for z in pair]+[z for pair in fiber for z in pair]
    elif kind=='weights':
        p,q,s,t=xs;mass=p+q
        out=[mass,min(p,q),p*s+q*t,-2*mass,2*mass]
    else:raise ValueError('unknown operation')
    return list(map(str,out))


def certify(kind,cases,root=None):
    return {'records':[{'input':v,'output':evaluate(kind,v,root)} for v in cases]}
