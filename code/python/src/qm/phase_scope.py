"""Exact local operations for ten scoped PFP steps; no completion/status oracle."""
from fractions import Fraction as Q
import re
from pathlib import Path

def _exact(value):
    if type(value) not in (int, Q, str):
        raise TypeError('exact integer, Fraction or rational text required')
    if type(value) is str and (len(value) > 1024 or re.fullmatch(r'[+-]?[0-9]+(?:/[0-9]+)?', value) is None):
        raise ValueError('bounded integer or numerator/denominator text required')
    if type(value) is int and value.bit_length() > 1024:
        raise ValueError('integer exceeds 1024-bit limit')
    q=Q(value)
    if max(q.numerator.bit_length(),q.denominator.bit_length()) > 1024:
        raise ValueError('rational exceeds 1024-bit limit')
    return q


def binary_ray(x,y):
    return Q(1 if x*y>0 or (x*y==0 and y==0) else 0)


def probe(a,b,c,d,x,y):
    return [x*x,y*y,(a*x+b*y)**2,(c*x+d*y)**2,
            (a*x-b*y)**2,(c*x-d*y)**2,4*a*b*x*y,4*c*d*x*y]


def evaluate(kind,values,root=None):
    if type(values) not in (list, tuple) or len(values)>64:
        raise ValueError('bounded sequence required')
    if kind in ('corpus','custody'):
        if root is None or len(values)!=1 or type(values[0]) is not str:
            raise ValueError('declared root and one relative path required')
        relative=Path(values[0])
        if relative.is_absolute() or '..' in relative.parts or '\\' in values[0] or ':' in values[0]:
            raise ValueError('relative path below the declared root required')
        base=Path(root).resolve();path=(base/relative).resolve()
        if not path.is_relative_to(base):raise ValueError('path escapes the declared root')
        if not path.is_file():raise ValueError('regular file required')
        with path.open('rb') as stream:
            data=stream.read((16<<20)+1)
        if len(data)>(16<<20):raise ValueError('file exceeds 16 MiB input budget')
        # These are literal byte counts, not an axiom or proof audit.
        return list(map(str,[len(data),data.count(b'\n'),data.count(b'sorry'),
                             data.count(b'Classical.choice'),data.count(b'axiom')]))
    xs=[_exact(v) for v in values]
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
