"""Independent scoped equations; never imports the boundary producer."""
from fractions import Fraction as Q
from itertools import product
from exact_json import require,rational
from review_exact_json import audit_bound
def eq(a,b):require(a==b,'G3_WITNESS:boundary_equations')
def integer(a,lo,hi):require(a.denominator==1 and lo<=a<=hi,'G1_SCHEMA:integer');return int(a)
def bitlist(x):return [integer(a,0,1) for a in x]
def conjugated(a,b,d,r,s):return [r*r*a-2*r*s*b+s*s*d,r*s*(a-d)+(r*r-s*s)*b,r*s*(a-d)+(r*r-s*s)*b,s*s*a+2*r*s*b+r*r*d]
def phase(t):return ((1-t*t)/(1+t*t),2*t/(1+t*t))
def mp(n):
    cells=[(n//(2**i))%2 for i in range(9)];p=[sum(cells[3*r:3*r+3])%2 for r in range(3)]+[sum(cells[j::3])%2 for j in range(3)];return sum(v*2**i for i,v in enumerate(p))
def solution_count(mask):
    rows=[sum(1<<j for j in c)+(int(i==5)<<9) for i,c in enumerate([(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8)]) if mask>>i&1];rank=0
    for j in range(9):
        pivot=next((i for i in range(rank,len(rows)) if rows[i]>>j&1),None)
        if pivot is None:continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank]
        for k in range(len(rows)):
            if k!=rank and rows[k]>>j&1:rows[k]^=rows[rank]
        rank+=1
    return 0 if 512 in rows else 2**(9-rank)
def first_solution(mask):return next((v for v in range(512) if (mp(v)^32)&mask==0),-1)
def qm(a,b):
    table=[[0,1,2,3],[1,4,3,6],[2,7,4,1],[3,2,5,4]]
    return table[a%4][b%4] ^ (4 if (a//4)^(b//4) else 0)
def inv(a):return a if a%4==0 else a^4
def qcoords(a):return [(-1 if a>=4 else 1)*int(j==a%4) for j in range(4)]
def verify(kind,values,raw):
    x=list(map(rational,values));r=list(map(rational,raw))
    if kind=='registry':
        caps=[integer(a,0,15) for a in x[:7]];a,b=x[7:];require(a>=0 and b>=0,'G1_SCHEMA:declared_ranks');v=[int(c==15) for c in caps];eq(r,v+[sum(v),a,min(a,b),max(0,a-b)])
    elif kind=='uniqueness':
        n=integer(x[0],1,4);v=[0,Q(1,2),Q(1,2),0]*3
        eq(r,v+[1]*3+[Q(1,2)]*6+[0,n,2*n]+[z/n for _ in range(n) for z in v])
        require(all(not (a!=b and b!=c and c!=a) for a,b,c in product(range(2),repeat=3)),'G3_WITNESS:odd_cycle')
    elif kind=='cochain':
        a,b,d,e,f,g,t,u=x;R,S=phase(t);T,V=phase(u);C,D=T*R-V*S,V*R+T*S;p=conjugated(a,b,d,R,S);q=conjugated(e,f,g,R,S);v=conjugated(a,b,d,C,D);z=a*e+2*b*f+d*g;eq(r,p+q+v+v+[z,z,z,0,0,0,0])
    elif kind=='survival':
        a,b,c=bitlist(x);eq(r,[a,b,c,a*b*c,a*b,a*b*(1-c)])
    elif kind=='relative':
        a,b,c,d,u,v,w=x;eq(a*a+b*b,1);eq(c*c+d*d,1);psi=[a,0,b*c,b*d];off=2*abs(a*b*c);diag=u*a*a+w*b*b;cross=2*v*a*b*c
        eq(r,psi+[p*q for p in psi for q in psi]+[a*a,a*b*c,a*b*c,b*b]+[off,diag+cross,diag,cross,abs(v)*off]);require(abs(cross)<=abs(v)*off,'G3_WITNESS:offdiagonal_bound')
    elif kind=='threshold':
        la,mu,W,k=[integer(a,0,10000) for a in x[:4]];require(k<=32,'G1_SCHEMA:bounded_horizon');v=bitlist(x[4:]);require(len(v)==5,'G1_SCHEMA:five_obligations');trajectory=[max(0,W+j*(la-mu)) for j in range(k+1)];eq(r,trajectory+[int(all(v) and mu>=la),max(0,la-mu)])
    elif kind=='syndrome':
        n=integer(x[0],1,7);require(n%2==1,'G1_SCHEMA:odd_repetition');t=(n-1)//2;out=[n,t,2*t];small=0;zero=0
        for e in range(2**n):
            weight=bin(e).count('1');syndrome=(e^(e>>1))&((1<<(n-1))-1);logical=int(weight*2>n);out += [weight,syndrome,logical];small+=int(weight<=t);zero+=int(syndrome==0)
        eq(r,out+[small,zero]);require(2*t<n and zero==2,'G3_WITNESS:distance_and_logical_control')
    elif kind=='packet':
        v=bitlist(x[:4]);W=integer(x[4],0,1000000);T=integer(x[5],1,1000000);c=integer(x[6],0,1);m=sum(1-z for z in v);at=int(W>=T);ok=int(m==0)*at;code=3 if c and not ok else 0 if m else 1 if not at else 2;eq(r,v+[m,at,ok,code])
    elif kind=='q8':
        g,h,k,a,b=[integer(z,0,7) for z in x];edges=[qm(inv(g),h),qm(inv(h),k),qm(inv(k),g)];loop=qm(qm(edges[0],edges[1]),edges[2]);comm=qm(qm(qm(a,b),inv(a)),inv(b));eq(r,edges+[loop,comm]+qcoords(loop)+qcoords(comm)+[qcoords(loop)[0],qcoords(comm)[0]]);eq(loop,0)
    elif kind=='parity':
        m=integer(x[0],0,63);counts=[solution_count(k) for k in range(64)];first=first_solution(m);eq(r,counts+[counts[m],first,mp(first) if first>=0 else -1]+[first_solution(63^(1<<j)) for j in range(6)])
        eq(counts[63],0);require(all(counts[63^(1<<j)]>0 for j in range(6)),'G3_WITNESS:all_five_context_subsets')
    elif kind=='born':
        a,b,t=x;require(a*a+b*b>0,'G1_SCHEMA:nonzero_amplitudes');R,S=phase(t);v=[R*a-S*b,S*a+R*b];out=[]
        for p in (1,2,4):N=abs(a)**p+abs(b)**p;out += [abs(a)**p/N,abs(b)**p/N]
        eq(r,out+v+[a*a+b*b,a*a+b*b,a**4+b**4,v[0]**4+v[1]**4])
    elif kind=='synthesis':
        k=integer(x[0],0,3);eq(r,[0,2,0,2,1,0,1,0,2*k%4,2*k%4]+[0]*16)
    elif kind=='cascade':
        a,b=x;eq(r,[a*a+b*b,a**4+b**4,2*a*b,2*a*b,0,-2,2,0,a*a+b*b,2*a*a*b*b])
    elif kind=='majorana':
        a,b=x;c=a*b;D=1+c*c;g=[a,0,0,-a];h=[0,b,b,0];out=g+h+[a*a,0,0,a*a,b*b,0,0,b*b]+[0]*4+[0,c,-c,0]+[-c*c,0,0,-c*c]+[1-c*c,2*c,-2*c,1-c*c]+[D,0,0,D]+[a*(1-c*c)/D,-2*a*c/D,-2*a*c/D,-a*(1-c*c)/D]+[2*b*c/D,b*(1-c*c)/D,b*(1-c*c)/D,-2*b*c/D];eq(r,out)
    elif kind=='busch':
        a,b,c,d=x;s=a+d;effects=[[Q(1,6),Q(1,6),0,Q(1,6)],[Q(1,6),Q(-1,6),0,Q(1,6)],[Q(1,6),0,Q(-1,6),Q(1,6)],[Q(1,6),0,Q(1,6),Q(1,6)],[Q(1,3),0,0,0],[0,0,0,Q(1,3)]];p=[(s+2*b)/6,(s-2*b)/6,(s-2*c)/6,(s+2*c)/6,a/3,d/3];eq(r,[z for E in effects for z in E]+[1,0,0,1]+p+[a,b,c,d,a*d-b*b-c*c,a+2*d-2*b-2*c,s])
    elif kind=='choi':
        p=x[0];a=(1+p)/2;b=(1-p)/2;ev=[(1+3*p)/2,b,b,b];vs=[[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]];eq(r,[a,0,0,p,0,b,0,0,0,0,b,0,p,0,0,a]+[1,0,0,1]+ev+[lam*z for lam,v in zip(ev,vs) for z in v]+[sum(z!=0 for z in ev),min(ev),2]);eq(all(z>=0 for z in ev),Q(-1,3)<=p<=1)
    elif kind=='proxy':
        k=integer(x[0],0,4);A=[0,1,1,0] if k!=2 else [1,0,0,-1];B=[1,0,0,-1] if k!=2 else [2,0,0,3];b=Q(3,4) if k==3 else Q(0);state=[Q(1,2),b,b,Q(1,2)];T=[1,0,0,0] if k==4 else [0,-1,1,0];comm=[0]*4 if k==2 else [0,-2,2,0];probes=[Q(1,2),Q(1,2),1-2*b];orth=[1,0,0,int(k!=4)];det=int(k!=4);local,joint=(8,9) if k==0 else (15,15);i3=36 if k==1 else 0
        eq(r,[local,joint,i3]+A+B+state+T+comm+probes+orth+[det]+[int(local==joint),int(i3==0),int(comm!=[0]*4),int(min(probes)>=0),det])
    elif kind=='maps':
        z=x[0];opt=Q(27,16);E=z*z-Q(27,8)*z;T=opt*opt;V=-Q(27,8)*opt;eq(r,[z,E,opt,T,V,-Q(729,256),0,(z-opt)**2,(z-opt)**2,-Q(11,4)]);require(r[7]>=0,'G3_WITNESS:polynomial_minimum')
    elif kind=='tensor':
        a,b,c,d=x;eq(r,[a*c,a*d,b*c,b*d,a*c,-a*d,b*c,-b*d,a*c+a*d,b*c+b*d,a*c-a*d,b*c-b*d,a,b,a,b,a,b,-a,-b])
    elif kind=='torsion':
        N=integer(x[0],1,5);a,b,c,d,e=[integer(z,0,N-1) for z in x[1:6]];g=[integer(z,0,N-1) for z in x[6:]];shift=[(a+g[1]-g[0])%N,(b+g[2]-g[1])%N,(c+g[3]-g[2])%N,(d+g[0]-g[3])%N,(e+g[2]-g[0])%N];A=(a+b+c+d)%N;B=(e-a-b)%N;eq(r,shift+[A,B,A,B,N*N,N*N,(a+b-e)%N,(-B)%N,int(N>2)]+[v for pair in product(range(N),repeat=2) for v in pair])
    else:raise ValueError('G1_SCHEMA:unknown_boundary_operation')
def check(request,candidate,task,config,root):
    _,c,p=audit_bound(request,candidate,task,config);require(set(c['data'])=={'records'} and len(c['data']['records'])==len(p['cases']),'G1_SCHEMA:coverage')
    for rec,v in zip(c['data']['records'],p['cases']):require(rec['input']==v,'G5_SCOPE:public_input_identity');verify(p['kind'],v,rec['output'])
    return {'records_checked':len(p['cases']),'scope':'Exact scoped controls and literal named rational/finite Lean signatures; original physical interfaces and unpaid transports remain explicit.'}
