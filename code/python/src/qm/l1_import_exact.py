"""Exact finite l1 and import-boundary computations on declared small carriers."""
from fractions import Fraction as Q
import re
from itertools import permutations, product

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

def evaluate(kind, values):
    if type(values) not in (list, tuple) or len(values) > 64:
        raise ValueError('bounded sequence of exact values required')
    arities = {'chain':4, 'kkt':12, 'edge':4, 'gauge':4, 'observer':4,
               'quotient':9, 'window':10, 'replica':3, 'circle':1, 'gauss':2,
               'complex':4, 'time':1, 'hilbert':1, 'dilation':3, 'gleason':2,
               'tensor':4, 'lift':4, 'average':2, 'gram':4}
    if kind == 'mass':
        if not values:raise ValueError('nonempty mass vector required')
    elif kind not in arities or len(values) != arities[kind]:
        raise ValueError('unknown operation or incorrect input arity')
    x=list(map(_exact,values));o=[]
    def emit(*v):o.extend(v)
    if kind=='chain':
        a,b,c,e=x;d=[b-a,c-b,a-c];emit(e,0,-e,*d,sum(d)+e*d[2],int(e==0))
    elif kind=='kkt':
        v,w,h,z=[x[i:i+3] for i in (0,3,6,9)];d=[h[1]-h[0],h[2]-h[1],h[0]-h[2]];r=[a-b for a,b in zip(v,d)];div=[z[2]-z[0],z[0]-z[1],z[1]-z[2]];cost=sum(a*abs(b) for a,b in zip(w,r));dual=sum(a*b for a,b in zip(z,v));slack=[a*abs(b)-c*b for a,b,c in zip(w,r,z)];cap=[a-abs(b) for a,b in zip(w,z)];valid=all(a>0 for a in w) and all(a>=0 for a in cap) and not any(div) and cost==dual
        emit(*r,*div,*cap,*slack,cost,dual,cost-dual,int(valid))
    elif kind in ('edge','gauge','observer'):
        a,b,p,q=x;norm=p*abs(a)+q*abs(b);sw=p*abs(b)+q*abs(a)
        if min(p,q)<0:raise ValueError('Nonnegative supplied weights required')
        if kind=='edge':emit(p*abs(a),q*abs(b),norm,sw,sw-norm,abs(a)+abs(b),max(abs(a),abs(b)),abs(a)+abs(b)-max(abs(a),abs(b)))
        elif kind=='gauge':
            for swap,s,t in product((0,1),(-1,1),(-1,1)):
                u,v=(b,a) if swap else (a,b);emit(p*abs(s*u)+q*abs(t*v))
            emit(a*a+b*b,b*b+a*a,3*p+4*q,5*p,3*p+4*q-5*p)
        else:emit(norm,p*abs(a)+q*abs(b),abs(a)+abs(b)-max(abs(a),abs(b)),(2*a)**2+(2*b)**2-2*(a*a+b*b),sw-norm,p*0+q*abs(b),p*abs(a)+0*abs(b))
    elif kind in ('quotient','window'):
        a,b,c,p,q,t,g0,g1,g2=x[:9];weights=[p,q,t]
        if min(weights)<=0:raise ValueError('Strictly positive weights required')
        if kind=='window' and x[9]!=0:return ['0']
        v=[a,b,c];total=sum(v);k=weights.index(min(weights));r=[total if i==k else Q(0) for i in range(3)];h=[Q(0),a-r[0],a+b-r[0]-r[1]];shift=[a+g1-g0,b+g2-g1,c+g0-g2];cost=sum(w*abs(z) for w,z in zip(weights,r));emit(1,k,*r,*h,cost,*shift,min(weights)*abs(sum(shift)))
        if kind=='window':emit(abs(sum(r)),int(cost!=0),abs(sum(r))/cost if cost else 0)
    elif kind=='replica':
        a,b,n=x
        if n.denominator!=1 or not 0<=n<=8:raise ValueError('Replica bound')
        copies=[z for _ in range(int(n)) for z in (a,b)];emit(sum(abs(z) for z in copies),sum(z*z for z in copies),n*(abs(a)+abs(b)),n*(a*a+b*b),(n*a)**2+(n*b)**2,n*n*(a*a+b*b))
    elif kind=='mass':
        if min(x)<0:return ['-1']
        M=sum(x)
        if not M:return ['0']
        emit(1,M,*(v/M for v in x),sum(x[:2])/M,sum(x[2:])/M,sum(v/M for v in x))
    elif kind=='circle':
        n=int(x[0])
        if x[0]!=n or n not in (2,3,4):raise ValueError('circle order must be 2, 3 or 4')
        emit(*(int((2*k)%n==0) for k in range(n)),*( (i+j)%n for i in range(n) for j in range(n)),int(all((2*k)%n==0 for k in range(n))),4,0)
    elif kind in ('gauss','complex'):
        a,b=x[:2];N=a*a+b*b
        if kind=='gauss':
            if any(z.denominator!=1 for z in x):raise ValueError('Gaussian integers required')
            emit(N,int(N==1),int(N!=0),a/N if N else 0,-b/N if N else 0,*(Q(k*k-2) for k in range(-3,4)))
        else:
            c,d=x[2:];K=c*c+d*d;u=a*c-b*d;v=a*d+b*c;emit(N,K,u,v,u*u+v*v,N*K,int(N!=0),a/N if N else 0,-b/N if N else 0)
    elif kind=='time':
        s=x[0]
        if s not in (-1,1):raise ValueError('time sign must be -1 or 1')
        maps=list(product(range(2),repeat=2));squares=[f[f[i]] for f in maps for i in range(2)];emit(*squares,sum([f[f[0]],f[f[1]]]==[1,0] for f in maps))
        U=[(Q(1,2),s/2),(Q(1,2),-s/2),(Q(1,2),-s/2),(Q(1,2),s/2)]
        def mul(z,w):return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
        def mm(A,B):return [tuple(sum(mul(A[2*i+k],B[2*k+j])[p] for k in range(2)) for p in range(2)) for i in range(2) for j in range(2)]
        adj=[(U[2*j+i][0],-U[2*j+i][1]) for i in range(2) for j in range(2)]
        emit(*(v for z in U+mm(U,U)+mm(adj,U) for v in z))
    elif kind=='hilbert':
        n=int(x[0])
        if x[0]!=n or not 0<=n<=8:raise ValueError('Hilbert truncation must be an integer from 0 to 8')
        u=[Q(1,2**k) for k in range(1,n+1)];emit(*u,sum(v*v for v in u),Q(1,3*4**n),Q(1,4**(n+1)),Q(1,3),int(Q(1,3*4**n)>0))
    elif kind=='dilation':
        a,b,d=x
        if not (a+d==1 and a>=0 and d>=0 and a*d>=b*b):raise ValueError('positive trace-one input required')
        ds=[p for p in permutations(range(4)) if p[0]//2==0 and p[2]//2==0];emit(len(ds))
        for p in ds:emit(*p,*(p.index(i) for i in range(4)))
        # Choi in (input,output) order for reset to |0><0|, partial trace over output.
        emit(*(int(i==j and i in (0,2)) for i in range(4) for j in range(4)),1,0,0,1,a+d,0,0,0)
    elif kind=='gleason':
        a,b=x;u=(a+b)**2;v=(a-b)**2;z=a*a+b*b;emit(a*a,b*b,z,z,u,v,z,z,u+v,2*z,u*u+v*v,2*z*z,8*a*a*b*b)
    elif kind=='tensor':
        a,b,c,d=x;T=[a*c,a*d,b*c,b*d];D=[a*(c+d),0,b*(c+d),0];emit(*T,*D,*(v-w for v,w in zip(T,D)),(a*a+b*b)*(c*c+d*d),sum(v*v for v in T))
    elif kind=='lift':
        a,b,c,d=x;A=a*a+b*b;B=c*c+d*d
        if not A or not B:return ['0']
        rho=[a*a/A,a*b/A,a*b/A,b*b/A];sig=[c*c/B,c*d/B,c*d/B,d*d/B];over=(a*c+b*d)**2/(A*B);r=[a*abs(a),b*abs(b)];z=[c*abs(c),d*abs(d)];sat=sum(u*v for u,v in zip(r,z))==sum(abs(u)*abs(v) for u,v in zip(r,z));faith=all(z[i]!=0 for i in range(2) if r[i]!=0)
        emit(1,A,B,*rho,*sig,over,1-over,int(sat),int(faith),int(over>0))
    elif kind=='average':
        a,b=x;ph=[(1,0),(0,1),(-1,0),(0,-1)];vals=[(a*u+b*v)**2+(a*s+b*t)**2 for u,s in ph for v,t in ph];cor=[(a*u+b*u)**2+(a*s+b*s)**2 for u,s in ph];emit(*vals,*cor,sum(vals)/16,sum(cor)/4,a*a+b*b,2*a*b)
    elif kind=='gram':
        a,b,c,d=x;emit(a*c+b*d,a*c+2*b*d,2*a*c+3*b*d,a*a+b*b,a*a+2*b*b,2*a*a+3*b*b,b*d,a*a+2*b*b-(a*a+b*b))
    else:raise ValueError('Unknown finite operation')
    return [str(Q(v)) for v in o]

def certify(kind,cases):return {'records':[{'input':v,'output':evaluate(kind,v)} for v in cases]}
