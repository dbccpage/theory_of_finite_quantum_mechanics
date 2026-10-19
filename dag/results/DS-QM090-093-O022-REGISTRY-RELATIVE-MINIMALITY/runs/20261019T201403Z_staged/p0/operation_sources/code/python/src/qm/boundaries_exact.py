"""Exact scoped boundary/control computations, with no physical-authority oracle."""
from fractions import Fraction as Q
from itertools import product
def need(ok):
    if not ok:raise ValueError('outside declared boundary domain')
def integer(q,lo,hi):need(q.denominator==1 and lo<=q<=hi);return int(q)
def bits(v):return [integer(q,0,1) for q in v]
def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def tr(a):return list(map(list,zip(*a)))
def flat(a):return [q for r in a for q in r]
def trace(a):return sum(a[i][i] for i in range(len(a)))
def rot(t):return [[(1-t*t)/(1+t*t),-2*t/(1+t*t)],[2*t/(1+t*t),(1-t*t)/(1+t*t)]]
def conjugate(u,a):return mm(mm(u,a),tr(u))
def add(a,b,k=1):return [[q+k*z for q,z in zip(r,s)] for r,s in zip(a,b)]
def scale(a,k):return [[k*q for q in r] for r in a]
def eye(n):return [[Q(i==j) for j in range(n)] for i in range(n)]
def parity(n):
    b=[(n>>i)&1 for i in range(9)];return sum((sum(b[i] for i in c)%2)<<j for j,c in enumerate([(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8)]))
def mp_solutions(mask):return [n for n in range(512) if (parity(n)^32)&mask==0]
def quat(code):return tuple(((-1)**(code//4))*int(i==code%4) for i in range(4))
def qmul(a,b):
    w,x,y,z=a;v,p,q,r=b
    return (w*v-x*p-y*q-z*r,w*p+x*v+y*r-z*q,w*q-x*r+y*v+z*p,w*r+x*q-y*p+z*v)
def qcode(a):return next(i for i in range(8) if quat(i)==a)
def qinv(a):return (a[0],-a[1],-a[2],-a[3])
def proxy_fields(k):
    A=[[Q(0),Q(1)],[Q(1),Q(0)]];B=[[Q(1),Q(0)],[Q(0),Q(-1)]];rho=[[Q(1,2),Q(0)],[Q(0),Q(1,2)]];T=[[Q(0),Q(-1)],[Q(1),Q(0)]]
    local,joint=(8,9) if k==0 else (15,15);power=4 if k==1 else 2
    I3=3**power-3*2**power+3
    if k==2:A=[[Q(1),Q(0)],[Q(0),Q(-1)]];B=[[Q(2),Q(0)],[Q(0),Q(3)]]
    if k==3:rho=[[Q(1,2),Q(3,4)],[Q(3,4),Q(1,2)]]
    if k==4:T=[[Q(1),Q(0)],[Q(0),Q(0)]]
    comm=add(mm(A,B),mm(B,A),-1);orth=mm(tr(T),T);det=T[0][0]*T[1][1]-T[0][1]*T[1][0]
    probes=[rho[0][0],rho[1][1],rho[0][0]-rho[0][1]-rho[1][0]+rho[1][1]]
    verdict=[int(local==joint),int(I3==0),int(any(q!=0 for q in flat(comm))),int(trace(rho)==1 and min(probes)>=0),int(orth==eye(2) and det==1)]
    return [local,joint,I3]+flat(A)+flat(B)+flat(rho)+flat(T)+flat(comm)+probes+flat(orth)+[det]+verdict
def evaluate(kind,values):
    x=list(map(Q,values))
    if kind=='registry':
        need(len(x)==9);caps=[integer(q,0,15) for q in x[:7]];a,b=x[7:];need(a>=0 and b>=0);v=[int(c==15) for c in caps];out=v+[sum(v),a,min(a,b),a-min(a,b)]
    elif kind=='uniqueness':
        n=integer(x[0],1,4);table=[Q(0),Q(1,2),Q(1,2),Q(0)]*3;assignments=list(product(range(2),repeat=3));out=table+[sum(table[4*k:4*k+4]) for k in range(3)]+[Q(1,2)]*6+[sum(all(a!=b for a,b in [(s[0],s[1]),(s[1],s[2]),(s[2],s[0])]) for s in assignments),n,2*n]+[q/n for _ in range(n) for q in table]
    elif kind=='cochain':
        a,b,d,e,f,g,t,u=x;rho=[[a,b],[b,d]];E=[[e,f],[f,g]];U=rot(t);V=rot(u);r1=conjugate(U,rho);e1=conjugate(U,E);r2=conjugate(V,r1);e2=conjugate(V,e1);r3=conjugate(mm(V,U),rho)
        z0=trace(mm(rho,E));z1=trace(mm(r1,e1));z2=trace(mm(r2,e2));out=flat(r1)+flat(e1)+flat(r2)+flat(r3)+[z0,z1,z2,z1-z0,z2-z1,z0-z2,(z1-z0)+(z2-z1)+(z0-z2)]
    elif kind=='survival':
        v=bits(x);need(len(v)==3);out=v+[int(all(v)),int(v[0] and v[1]),int(v[0] and v[1] and not v[2])]
    elif kind=='relative':
        a,b,c,d,u,v,w=x;need(a*a+b*b==1 and c*c+d*d==1);psi=[a,Q(0),b*c,b*d];rho=[[s*t for t in psi] for s in psi];red=[[sum(rho[2*i+k][2*j+k] for k in range(2)) for j in range(2)] for i in range(2)];E=[[u,v],[v,w]];dephase=[[red[0][0],0],[0,red[1][1]]];full=trace(mm(red,E));diag=trace(mm(dephase,E));off=2*abs(a*b*c)
        out=psi+flat(rho)+flat(red)+[off,full,diag,full-diag,abs(v)*off]
    elif kind=='threshold':
        need(len(x)==9);la,mu,W,k=[integer(q,0,10000) for q in x[:4]];need(k<=32);v=bits(x[4:]);q=W;out=[q]
        for _ in range(k):q=max(0,q+la-mu);out.append(q)
        out += [int(all(v) and mu>=la),max(0,la-mu)]
    elif kind=='syndrome':
        n=integer(x[0],1,7);need(n%2==1);t=(n-1)//2;out=[n,t,2*t];small=0;zero=0
        for e in range(2**n):
            b=[(e>>j)&1 for j in range(n)];wt=sum(b);s=sum((b[j]^b[j+1])<<j for j in range(n-1));logical=int(wt>n//2);small+=int(wt<=t and not logical);zero+=int(s==0);out += [wt,s,logical]
        out += [small,zero]
    elif kind=='packet':
        need(len(x)==7);v=bits(x[:4]);W=integer(x[4],0,1000000);T=integer(x[5],1,1000000);claim=integer(x[6],0,1);missing=4-sum(v);at=int(W>=T);eligible=int(missing==0 and at);verdict=3 if claim and not eligible else 0 if missing else 1 if not at else 2;out=v+[missing,at,eligible,verdict]
    elif kind=='q8':
        g0,g1,g2,a,b=[quat(integer(q,0,7)) for q in x];edges=[qmul(qinv(g0),g1),qmul(qinv(g1),g2),qmul(qinv(g2),g0)];loop=qmul(qmul(edges[0],edges[1]),edges[2]);comm=qmul(qmul(qmul(a,b),qinv(a)),qinv(b));out=[qcode(e) for e in edges]+[qcode(loop),qcode(comm)]+list(loop)+list(comm)+[loop[0],comm[0]]
    elif kind=='parity':
        mask=integer(x[0],0,63);sol=[mp_solutions(m) for m in range(64)];s=sol[mask];first=s[0] if s else -1;out=[len(a) for a in sol]+[len(s),first,parity(first) if s else -1]+[sol[63^(1<<j)][0] for j in range(6)]
    elif kind=='born':
        a,b,t=x;need(a*a+b*b>0);norms=[abs(a)**p+abs(b)**p for p in (1,2,4)];v=flat(mm(rot(t),[[a],[b]]));out=[q for p,N in zip((1,2,4),norms) for q in [abs(a)**p/N,abs(b)**p/N]]+v+[a*a+b*b,sum(q*q for q in v),a**4+b**4,sum(q**4 for q in v)]
    elif kind=='synthesis':
        k=integer(x[0],0,3);images=[2*j%4 for j in range(4)];out=images+[int(j in images) for j in range(4)]+[2*k%4,2*((k+2)%4)%4]+[(2*((a+b)%4)-(2*a%4+2*b%4))%4 for a,b in product(range(4),repeat=2)]
    elif kind=='cascade':
        a,b=x;A=[[Q(0),Q(1)],[Q(1),Q(0)]];B=[[Q(1),Q(0)],[Q(0),Q(-1)]];comm=add(mm(A,B),mm(B,A),-1);out=[a*a+b*b,a**4+b**4,(a+b)**2-a*a-b*b,2*a*b]+flat(comm)+[sum([a*a,b*b]),(a*a+b*b)**2-(a**4+b**4)]
    elif kind=='majorana':
        a,b=x;G=[[a,0],[0,-a]];H=[[0,b],[b,0]];P=mm(G,H);B=add(eye(2),P);den=1+(a*b)**2;out=[q for M in [G,H,mm(G,G),mm(H,H),add(mm(G,H),mm(H,G)),P,mm(P,P),mm(B,B),mm(B,tr(B)),scale(conjugate(B,G),1/den),scale(conjugate(B,H),1/den)] for q in flat(M)]
    elif kind=='busch':
        a,b,c,d=x;effects=[[Q(1,6),Q(s,6),Q(0),Q(1,6)] for s in (1,-1)]+[[Q(1,6),Q(0),Q(-s,6),Q(1,6)] for s in (1,-1)]+[[Q(1+s,6),Q(0),Q(0),Q(1-s,6)] for s in (1,-1)]
        probs=[a*A+d*D+2*(b*B+c*C) for A,B,C,D in effects];summed=[sum(E[j] for E in effects) for j in range(4)];det=a*d-b*b-c*c;recon=[(sum(probs)+3*(probs[4]-probs[5]))/2,3*(probs[0]-probs[1])/2,3*(probs[3]-probs[2])/2,(sum(probs)-3*(probs[4]-probs[5]))/2];quad=a+2*d-2*b-2*c
        out=[q for E in effects for q in E]+summed+probs+recon+[det,quad,sum(probs)]
    elif kind=='choi':
        p=x[0];J=scale(eye(4),(1-p)/2);v=[1,0,0,1];J=add(J,[[p*a*b for b in v] for a in v]);vs=[[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]];ev=[(1+3*p)/2]+[(1-p)/2]*3;pt=[[sum(J[2*i+k][2*j+k] for k in range(2)) for j in range(2)] for i in range(2)];out=flat(J)+flat(pt)+ev+[z for v in vs for z in flat(mm(J,[[Q(q)] for q in v]))]+[sum(q!=0 for q in ev),min(ev),trace(J)]
    elif kind=='proxy':out=proxy_fields(integer(x[0],0,4))
    elif kind=='maps':
        z=x[0];E=z*z-Q(27,8)*z;opt=Q(27,16);T=opt*opt;V=-4*opt+Q(5,8)*opt;out=[z,E,opt,T,V,T+V,2*T+V,E-(T+V),(z-opt)**2,-4+Q(5,4)]
    elif kind=='tensor':
        a,b,c,d=x;v=[a*c,a*d,b*c,b*d];vz=[a*c,-a*d,b*c,-b*d];dump=[(c+d)*a,(c+d)*b];dumpz=[(c-d)*a,(c-d)*b];out=v+vz+dump+dumpz+[a,b,a,b,a,b,-a,-b]
    elif kind=='torsion':
        need(len(x)==10);N=integer(x[0],1,5);e=[integer(q,0,N-1) for q in x[1:6]];g=[integer(q,0,N-1) for q in x[6:]];edges=[(0,1),(1,2),(2,3),(3,0),(0,2)];shift=[(v+g[j]-g[i])%N for v,(i,j) in zip(e,edges)]
        canon=lambda a:((a[3]+a[0]+a[1]+a[2])%N,(a[4]-a[0]-a[1])%N)
        forms={canon(a) for a in product(range(N),repeat=5)};c=canon(e);d=canon(shift);path=(e[0]+e[1]-e[4])%N;out=shift+list(c)+list(d)+[len(forms),N*N,path,(-c[1])%N,int(any(2*k%N!=0 for k in range(N)))]+[v for pair in sorted(forms) for v in pair]
    else:raise ValueError('unknown boundary operation')
    return [str(Q(v)) for v in out]
def certify(kind,cases):return {'records':[{'input':v,'output':evaluate(kind,v)} for v in cases]}
