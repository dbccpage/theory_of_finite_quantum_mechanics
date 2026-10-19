"""Exact finite witnesses; declared domains and remaining imports stay explicit."""
from fractions import Fraction as Q
from itertools import product

def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,b,d=-1):return (a[0]*b[0]+d*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def mm(a,b,d=-1):
    return [[sum_pair([mul(a[i][k],b[k][j],d) for k in range(len(b))]) for j in range(len(b[0]))] for i in range(len(a))]
def sum_pair(xs):
    v=(Q(0),Q(0))
    for x in xs:v=add(v,x)
    return v
def adj(a):return [[(a[j][i][0],-a[j][i][1]) for j in range(len(a))] for i in range(len(a[0]))]
def flat(a):return [v for row in a for z in row for v in z]
def qm(a):return [[(Q(v),Q(0)) for v in row] for row in a]
def kron(a,b):return [[a[i//len(b)][j//len(b[0])]*b[i%len(b)][j%len(b[0])] for j in range(len(a[0])*len(b[0]))] for i in range(len(a)*len(b))]
def matadd(a,b,sign=1):return [[add(x,(sign*y[0],sign*y[1])) for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,s):return [[(z[0]*s,z[1]*s) for z in r] for r in a]
def i3(f,a,b,c):return f(a+b+c)-f(a+b)-f(a+c)-f(b+c)+f(a)+f(b)+f(c)-f(0)
def norm12(c):
    z=[c[0]+c[2],c[1],-c[2],-c[1]-c[3]];p=[Q(0)]*7
    for i,a in enumerate(c):
        for j,b in enumerate(z):p[i+j]+=a*b
    for k in range(6,3,-1):p[k-2]+=p[k];p[k-4]-=p[k]
    return p[0],-p[3]

def evaluate(kind,values):
    x=list(map(Q,values))
    if kind=='power':
        p=int(x[0])
        if x[0]!=p or not 1<=p<=16:raise ValueError('integer power budget 1..16')
        n=1+Q(3,5)**p+Q(4,5)**p
        out=[n,Q(1,2),1/n,Q(1,2)-1/n,i3(lambda t:abs(t)**p,Q(1),Q(1),Q(1)),i3(lambda t:abs(t)**p,Q(1),Q(1),Q(-1))]
    elif kind=='selection':
        a,b=x;n=a*a+b*b;m=a**4+b**4
        if n==0:raise ValueError('nonzero preparation')
        out=[n,m,a*a/n,b*b/n,a**4/m,b**4/m,a*a/n-a**4/m]
    elif kind=='quotient':
        if not x or any(v.denominator!=1 for v in x):raise ValueError('integral finite report labels')
        labels=sorted(set(x));classes=[labels.index(v) for v in x]
        out=[len(labels)]+classes+[int(a==b) for a in x for b in x]
    elif kind=='sorkin':
        a,b,c,alpha,beta,A,B=x
        f=lambda t:alpha*t*t+beta*t**4
        np,nm=norm12([Q(2),Q(2),Q(0),Q(-1)]),norm12([Q(2),Q(-2),Q(0),Q(1)])
        out=[i3(f,a,b,c),12*beta*a*b*c*(a+b+c),*np,*nm,A*np[0]+B*np[1],A*nm[0]+B*nm[1]]
    elif kind=='pinching':
        a,b,c=x
        if c<=0:raise ValueError('positive metric scale')
        out=[4*(a*a+b*b),4*a*a,4*b*b,c*c*4*(a*a+b*b),c*c*4*a*a]
    elif kind=='k23':
        t=x[0]
        if t<0:raise ValueError('nonnegative defect scale')
        D=[[Q(2 if k==j else -1) for j in range(3)] for k in range(3)]
        edges=[(a,2+k) for a in range(2) for k in range(3)]
        defects=[[t*v for v in D[k]] if a==0 else [Q(0)]*3 for a in range(2) for k in range(3)]
        mtz=[[v/Q(3)*(1 if a==0 else -1) for v in D[k]] for a in range(2) for k in range(3)]
        mall=[[v/Q(4)*(1 if a==0 else -1) for v in D[k]] for a in range(2) for k in range(3)]
        potential=[[t]*3]+[[Q(0)]*3 for _ in range(4)]
        residual=[[z[j]-(potential[v][j]-potential[u][j]) for j in range(3)] for z,(u,v) in zip(defects,edges)]
        def divergence(ms):return [[sum((m[j] if u==vtx else -m[j] if v==vtx else 0) for m,(u,v) in zip(ms,edges)) for j in range(3)] for vtx in range(5)]
        costs=[sum(map(abs,v))/2 for v in defects];allcosts=[sum(map(abs,v))/2 for v in residual]
        obj=lambda ms:sum(sum(a*b for a,b in zip(m,z)) for m,z in zip(ms,defects))
        arrays=[defects,mtz,mall,potential,residual,divergence(mtz),divergence(mall)]
        out=[v for ar in arrays for row in ar for v in row]+costs+allcosts+[sum(costs),obj(mtz),sum(allcosts),obj(mall)]
    elif kind=='tsirelson':
        if x not in ([Q(1)],[Q(-1)]):raise ValueError('SOS sign')
        sign=int(x[0]);I=[[1,0],[0,1]];Z=[[1,0],[0,-1]];X=[[0,1],[1,0]]
        zz,xx=kron(Z,Z),kron(X,X);P=[[a+b for a,b in zip(r,s)] for r,s in zip(zz,xx)]
        C=[[(Q(0),Q(v)) for v in row] for row in P]
        S=[matadd(qm(kron(a,I)),qm(kron(I,a)),-sign) for a in [Z,X]]
        ss=matadd(mm(S[0],S[0],2),mm(S[1],S[1],2));rhs=[[(z[1]/2,z[0]/2) for z in row] for row in ss]
        lhs=matadd([[(Q(0),Q(2 if i==j else 0)) for j in range(4)] for i in range(4)],C,-sign)
        rho=qm([[Q(1,2) if i in (0,3) and j in (0,3) else 0 for j in range(4)] for i in range(4)])
        exp=sum_pair([mm(rho,C,2)[i][i] for i in range(4)])
        out=flat(C)+flat(S[0])+flat(S[1])+flat(lhs)+flat(rhs)+list(exp)
    elif kind=='census':
        if len(x)!=8 or any(v not in (0,1) for v in x):raise ValueError('eight source-declared binary labels')
        verdict=list(map(int,x));out=[len(verdict),sum(verdict),len(verdict)-sum(verdict)]+[i for i,v in enumerate(verdict) if v]+[i for i,v in enumerate(verdict) if not v]
    elif kind=='matrix':
        if len(x)!=24 or any(v.denominator!=1 for v in x):raise ValueError('integral 2x2 Gaussian matrices and vectors')
        pairs=list(zip(x[::2],x[1::2]));A=[pairs[:2],pairs[2:4]];B=[pairs[4:6],pairs[6:8]];v=[[z] for z in pairs[8:10]];u=[[z] for z in pairs[10:12]]
        ab=mm(A,B);av=mm(A,v);abv=mm(ab,v);a_bv=mm(A,mm(B,v));ah=adj(A)
        inner=lambda a,b:sum_pair([mul((z[0][0],-z[0][1]),w[0]) for z,w in zip(a,b)])
        recovered=mm(A,qm([[1,0],[0,1]]))
        out=flat(ab)+flat(av)+flat(abv)+flat(a_bv)+flat(ah)+list(inner(av,u))+list(inner(v,mm(ah,u)))+flat(recovered)
    elif kind=='time':
        if len(x)!=2 or any(v.denominator!=1 for v in x):raise ValueError('integer branch labels')
        M=[[(Q(1),Q(1)),(Q(1),Q(-1))],[(Q(1),Q(-1)),(Q(1),Q(1))]]
        roots=[list(f) for f in product(range(2),repeat=2)];squares=[f[f[0]]*2+f[f[1]] for f in roots]
        out=[2*x[0]+1,2*x[1]+1]+squares+flat(mm(M,M))+flat(mm(scale(M,-1),scale(M,-1)))+flat(mm(adj(M),M))
    else:raise ValueError('unknown scoped domain')
    return list(map(str,out))

def certify(kind,cases):return {'records':[{'input':v,'output':evaluate(kind,v)} for v in cases]}
