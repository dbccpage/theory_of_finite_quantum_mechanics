"""Exact finite dynamics and import-boundary witnesses. No continuum oracle."""
from fractions import Fraction as Q
from itertools import product
from math import gcd
from .structure_exact import add, mul, mm, adj, flat, qm, matadd, scale, certify as prior_certify

def eye(n):return [[(Q(int(i==j)),Q(0)) for j in range(n)] for i in range(n)]
def tr(a):return tuple(sum(a[i][i][j] for i in range(len(a))) for j in range(2))
def norm(v):return sum(a*a+b*b for a,b in v)
def powmat(a,n):
    r=eye(len(a))
    for _ in range(n):r=mm(r,a)
    return r
def cayley(t):
    d=1+t*t;r=(1-t*t)/d;s=2*t/d
    return qm([[r,s],[-s,r]])
def integer(v,lo,hi):
    if v.denominator!=1 or not lo<=v<=hi:raise ValueError('bounded integer domain')
    return int(v)

def evaluate(kind,values):
    x=list(map(Q,values))
    if kind=='path':
        a=qm([x[:2],x[2:4]]);m=integer(x[4],0,3);n=integer(x[5],0,3);k=m+n
        enum=[]
        for i in range(2):
            for j in range(2):
                if k==0:enum.append(Q(int(i==j)));continue
                total=Q(0)
                for mids in product(range(2),repeat=k-1):
                    path=(j,)+mids+(i,);w=Q(1)
                    for u,v in zip(path,path[1:]):w*=a[v][u][0]
                    total+=w
                enum.append(total)
        out=[z[0] for row in powmat(a,k) for z in row]+enum+[z[0] for row in mm(powmat(a,m),powmat(a,n)) for z in row]
    elif kind=='transfer':
        a=qm([x[:2],x[2:4]]);b=qm([x[4:6],x[6:8]]);v=qm([[x[8]],[x[9]]]);f=qm([x[10:12]])
        out=[z[0] for mat in [mm(a,b),mm(mm(a,b),v),mm(a,mm(b,v)),mm(f,a),mm(f,mm(a,v)),mm(mm(f,a),v)] for row in mat for z in row]
    elif kind=='overcount':
        a,b,d=x;t=qm([[0,0,0],[a,0,0],[d,b,0]]);z=matadd(matadd(eye(3),t),mm(t,t));zz=mm(z,z)
        out=[q[0] for mat in [z,zz] for row in mat for q in row]+[a*b,d,z[2][0][0],zz[2][0][0]]
    elif kind=='refinement':
        n,m,k,u=x
        out=[u+m-k+n-m,u+n-k,k+n-k,k-n,abs(k-n)]
    elif kind=='histories':
        a,b,c,d=x;p=a*c;q=b*d
        out=[p,q,p+q,(p+q)**2,p*p+q*q,2*p*q]
    elif kind=='held':
        a,b=x;out=[a*a,b*b,a*a,b*b,(a+b)**2,(a-b)**2,4*a*b]
    elif kind=='schrodinger':
        h0,h1,u,v,a,b,c,d,dt,hbar=x
        if hbar<=0:raise ValueError('positive hbar')
        h=[[(h0,Q(0)),(u,v)],[(u,-v),(h1,Q(0))]];psi=[(a,b),(c,d)]
        hp=[row[0] for row in mm(h,[[q] for q in psi])];der=[(q[1]/hbar,-q[0]/hbar) for q in hp]
        rate=2*sum(q[0]*z[0]+q[1]*z[1] for q,z in zip(psi,der));e=[add(q,(dt*z[0],dt*z[1])) for q,z in zip(psi,der)]
        out=[z for q in hp+der for z in q]+[rate,norm(psi)]+[z for q in e for z in q]+[norm(e),norm(e)-norm(psi),dt*dt*norm(der)]
    elif kind=='cayley':
        t=x[0];u=cayley(t);e=qm([[1,t],[-t,1]]);X=qm([[0,1],[1,0]]);Z=qm([[1,0],[0,-1]])
        out=[z[0] for mat in [u,mm(adj(u),u),e,mm(adj(e),e),matadd(mm(X,Z),mm(Z,X)),mm(X,X),mm(Z,Z)] for row in mat for z in row]+[1+t*t]
    elif kind=='lambda':
        r=x[0];o=(Q(0),Q(0));L1=[[o,(r,Q(0)),o],[(r,Q(0)),o,o],[o,o,o]];L2=[[o,(Q(0),-r),o],[(Q(0),r),o,o],[o,o,o]];L3=[[(r,Q(0)),o,o],[o,(-r,Q(0)),o],[o,o,o]];ls=[L1,L2,L3]
        comms=[matadd(mm(ls[i],ls[(i+1)%3]),mm(ls[(i+1)%3],ls[i]),-1) for i in range(3)]
        rhs=[[[mul((Q(0),2*r),q) for q in row] for row in ls[(i+2)%3]] for i in range(3)]
        ps=[qm([[int(i==j==k) for j in range(3)] for i in range(3)]) for k in range(2)]
        out=[q for mat in ls+comms+rhs+[mm(p,p) for p in ps] for q in flat(mat)]+[q for a in ls for q in tr(a)]
    elif kind=='heisenberg':
        t,a,b,c,v,w=x;u=cayley(t);A=qm([[a,b],[b,c]]);psi=qm([[v],[w]]);ah=mm(adj(u),mm(A,u));ps=mm(u,psi)
        f=mm(adj(ps),mm(A,ps))[0][0][0];g=mm(adj(psi),mm(ah,psi))[0][0][0]
        out=[q[0] for mat in [ah,ps,mm(adj(u),u)] for row in mat for q in row]+[f,g]
    elif kind=='decoherence':
        a,b=x;out=[a*a,a*b,a*b,b*b,a*a,b*b,Q(0),a*a+b*b,(a+b)**2,a+b,a*a+b*b]
    elif kind=='global':
        a,b,c=x;out=[a+c,a+2*b+c,2*b,a-2*b+c]
    elif kind=='ccr':
        n=integer(x[0],1,3);a=qm([x[1+i*n:1+(i+1)*n] for i in range(n)]);at=1+n*n;b=qm([x[at+i*n:at+(i+1)*n] for i in range(n)]);lam=x[-1];com=matadd(mm(a,b),mm(b,a),-1)
        out=[q[0] for row in com for q in row]+[tr(com)[0],n*lam,Q(n)]
    elif kind=='dichotomy':
        k=integer(x[0],1,8);a,b=1,0
        for _ in range(k):a,b=3*a-4*b,4*a+3*b
        z,w=0,1
        ip=(Q(1),Q(0))
        for _ in range(k):ip=mul(ip,(Q(0),Q(1)))
        den=5**k;out=[a,b,den,Q(a,den),Q(b,den),a%5,b%5,*ip,Q(a*a+b*b,den*den),int(ip==(1,0))]
    elif kind=='stone':
        return prior_certify('time',[values])['records'][0]['output']
    elif kind=='everett':
        if not x or any(q<0 for q in x) or sum(x)!=1:raise ValueError('normalized nonnegative rational weights')
        N=1
        for q in x:N=N*q.denominator//gcd(N,q.denominator)
        counts=[int(q*N) for q in x];wp=(Q(1,2),Q(1,10));wm=(Q(1,2),Q(-1,10))
        poly=lambda w:add(add(tuple(5*z for z in mul(w,w,5)),tuple(-5*z for z in w)),(Q(1),Q(0)))
        out=[N]+counts+[sum(counts)]+list(poly(wp))+list(poly(wm))+list(add(wp,wm))+list(wp)
    elif kind=='embedding':
        a,b,c,d,n=x;n=integer(n,3,120);p=(a,b);q=(c,d);gram=[mul(p,p,5),mul(p,q,5),mul(q,q,5)];conj=[(u,-v) for u,v in gram];det=add(mul(gram[0],gram[2],5),tuple(-z for z in mul(gram[1],gram[1],5)))
        phi=sum(gcd(j,n)==1 for j in range(1,n+1))
        out=[z for pair in gram+conj+[det,(-Q(2),Q(1)),(Q(3),Q(-1)),(-Q(2),Q(-1)),(Q(3),Q(1))] for z in pair]+[phi,Q(phi,2),Q(2),Q(3),Q(4),Q(5),Q(9),Q(9,4)**2-5]
    elif kind=='stone_gap':
        n=integer(x[0],0,16);k=integer(x[1],-16,16);out=[n*k%4,n*(k+4)%4,n*k%8,n*(k+4)%8,(n*(k+4)-n*k)%4]
    elif kind=='cptp':
        t=x[0]
        if t<0:raise ValueError('nonnegative Bell input scale')
        rho=[[t/2 if i in (0,3) and j in (0,3) else Q(0) for j in range(4)] for i in range(4)]
        pt=[[rho[2*(i//2)+j%2][2*(j//2)+i%2] for j in range(4)] for i in range(4)];v=[0,1,-1,0];quad=sum(v[i]*pt[i][j]*v[j] for i in range(4) for j in range(4))
        out=[z for a in [rho,pt] for row in a for z in row]+[quad,Q(2),sum(rho[i][i] for i in range(4)),sum(pt[i][i] for i in range(4)),Q(1),Q(0),Q(0),Q(1)]
    elif kind=='condition':
        n=integer(x[0],1,4);w=x[1:1+n];mask=x[1+n:]
        if len(mask)!=n or any(q<0 for q in w) or any(q not in (0,1) for q in mask):raise ValueError('weights and sector indicator')
        mass=sum(q*s for q,s in zip(w,mask))
        if mass<=0:raise ValueError('positive selected mass required')
        p=[q*s/mass for q,s in zip(w,mask)];mass2=sum(q*s for q,s in zip(p,mask));again=[q*s/mass2 for q,s in zip(p,mask)]
        out=[mass]+p+again+[sum(p)]
    else:raise ValueError('unknown scoped operation')
    return list(map(str,out))

def certify(kind,cases):return {'records':[{'input':row,'output':evaluate(kind,row)} for row in cases]}
