"""Independent finite predicates: no import of either producer."""
from fractions import Fraction as Q
from itertools import product,permutations
from math import comb
from exact_json import require,rational
from review_exact_json import audit_bound

def eq(a,b):require(a==b,'G3_WITNESS:finite_equations')
def integer(z,l,h):require(z.denominator==1 and l<=z<=h,'G1_SCHEMA:finite_integer');return int(z)
def pop(n):return bin(n).count('1')
def rows(mask,n):return {(i,j) for i,j in product(range(n),repeat=2) if mask>>(n*i+j)&1}
def enc(E,n):return sum(1<<(n*i+j) for i,j in E)
def good(E):return all(i!=j for i,j in E)
def cmap(E,f):return {(f(i),f(j)) for i,j in E}
def cadd(a,b):return (a[0]+b[0],a[1]+b[1])
def cmul(a,b,c=False):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]-(a[1]*b[1] if c else 0))
def cpow3(k):return [(Q(1),Q(0)),(Q(0),Q(1)),(Q(-1),Q(-1))][k%3]
def closed_gauss(a,b,n):
    return tuple(sum(Q(comb(n,j))*a**(n-j)*b**j*((-1)**(j//2)) for j in range(parity,n+1,2)) for parity in (0,1))
def phase(k):
    z=closed_gauss(Q(3,5),Q(4,5),abs(k));return (z[0],-z[1]) if k<0 else z

def replay(h,remove):
    # Independent event guards and state transition equations.
    data=0;ar=[];instances=[];rules=[];req=[];mode=0;trace=[];failure=-1
    for index,(tag,a,b) in enumerate(h):
        if remove and tag==0:continue
        accept=True
        if tag==1:data+=1
        if tag==2:
            accept=a in (1,2,3)
            if accept:ar.append(a)
        if tag==3:
            accept=a in range(len(ar))
            if accept:
                coords=[];q=b
                for _ in range(ar[a]):coords.append(q%4);q//=4
                accept=q==0 and all(z<data for z in coords)
            if accept and (a,b) not in instances:instances.append((a,b))
        if tag==4:
            accept=a in range(len(ar))
            if accept and a not in rules:rules.append(a)
        if tag==5:
            accept=a in range(data) and b in range(data) and a!=b
            if accept and (a,b) not in req:req.append((a,b))
        if tag==6:mode^=1
        trace += [data+len(ar)+len(instances)+len(rules)+len(req),mode,int(accept)]
        if not accept:failure=index;break
    state=[failure,data,len(ar),len(instances),len(rules),len(req),mode]+ar+[z for p in sorted(instances) for z in p]+sorted(rules)+[z for p in sorted(req) for z in p]
    return trace,state

def verify(kind,values,raw):
    x=list(map(rational,values));r=list(map(rational,raw))
    if kind=='weyl':
        a,b=[integer(v,0,2) for v in x[:2]];A=x[2:];comm=[z for i,j in product(range(3),repeat=2) for z in (cpow3(-a*b) if i==j else (0,0))];coeff=[]
        for s,t in product(range(3),repeat=2):
            c=(Q(0),Q(0))
            for j in range(3):
                w=cpow3(-t*j);c=cadd(c,(A[((j+s)%3)*3+j]*w[0]/3,A[((j+s)%3)*3+j]*w[1]/3))
            coeff+=list(c)
        # Reconstruction is checked independently through the explicit Fourier sum.
        recovered=[]
        for i,j in product(range(3),repeat=2):
            c=(0,0)
            for t in range(3):
                at=2*(3*((i-j)%3)+t);c=cadd(c,cmul(tuple(coeff[at:at+2]),cpow3(t*j),True))
            recovered+=list(c);eq(c,(A[3*i+j],0))
        gram=[v for i,j in product(range(9),repeat=2) for v in (3*int(i==j),0)]
        eq(r,comm+list(cpow3(-a*b))+coeff+recovered+gram)
    elif kind=='duality':
        a,b=x;vals=[i*a+j*b for i,j in product((-1,0,1),repeat=2)];norm=abs(a)+abs(b);eq(r,[norm]+vals+[norm,0]);require(all(v<=norm for v in vals),'G3_WITNESS:dual_upper_bound')
    elif kind=='separation':
        eq(x,[0]);seqs=[()]+[(i,) for i in range(10)]+list(product(range(10),repeat=2));args=[(0,),(1,),(0,0),(0,1),(1,0),(1,1)];out=[]
        for seq in seqs:
            forms=[];inst=[];universal=False;valid=True
            for item in seq:
                if item==0:continue
                if item in (1,2):forms.append(item)
                elif not forms:valid=False;break
                elif item==9:universal=True
                elif len(args[item-3])!=forms[0]:valid=False;break
                else:inst.append(args[item-3])
            # With length at most two, every valid separating response is one
            # new form followed by one instance; datum and uniform rules cannot separate.
            sep=valid and len(seq)==2 and seq[0] in (1,2) and seq[1] in range(3,9)
            out.append([len(seq),int(valid),int(sep),sum(forms)])
        winners=[i for i,row in enumerate(out) if row[2]];best=[i for i in winners if out[i][3]==1]
        eq(r,[len(seqs)]+[z for row in out for z in row]+[2,len(winners),1,len(best)]+winners+best)
    elif kind=='distinct':
        m=integer(x[0],0,15);out=[[int(not(k&9)),int(bool(k&2)),int(bool(k&4))] for k in range(16)];eq(r,[z for row in out for z in row]+[2,2,6]+out[m])
    elif kind in ('noreturn','events','erasure','supply'):
        h=[tuple(integer(z,0,255) for z in x[i:i+3]) for i in range(0,len(x),3)];require(all(t<=6 for t,_,_ in h),'G1_SCHEMA:event_code');t,o=replay(h,False);te,oe=replay(h,True);eq(r,[len(t),len(o)]+t+o+[len(te),len(oe)]+te+oe)
        # Erasure preserves the final success/failure state, but the reported
        # failing event index is relative to the original input history.
        eq(o,oe)
        if kind=='noreturn':require(all(t[j]<=t[j+3] for j in range(0,len(t)-3,3)),'G3_WITNESS:element_monotonicity')
    elif kind=='fewest':
        seed,T,m=[integer(z,0,511) for z in x];require(seed in (0,1) and T in (3,7),'G1_SCHEMA:apart_seed');initial={(0,1)}|({(1,0)} if seed else set());E=rows(m,3);require(good(E) and all(T>>i&1 and T>>j&1 for i,j in E),'G1_SCHEMA:target_graph');states=[]
        for t in (3,7):
            for k in range(512):
                F=rows(k,3)
                if good(F) and all(t>>i&1 and t>>j&1 for i,j in F):states += [t,k,int(t==7)+len(F^initial)]
        size=pop(T)+len(E);lost=len(initial-E);base=2+len(initial);cost=int(T==7)+len(E^initial);eq(cost,size+2*lost-base);eq(r,[len(states)//3,cost,size,lost,base,cost]+states)
    elif kind=='obstruction':
        m,u,v=[integer(z,0,511) for z in x];require(u<3 and v<3 and u!=v,'G1_SCHEMA:merge');E=rows(m,3);require(good(E),'G1_SCHEMA:legal_input');f=lambda j:u if j==v else j;F=cmap(E,f);L=cmap(E-{(u,v),(v,u)},f);R=F-{(u,u)};eq(L,R);eq(good(F),(u,v) not in E and (v,u) not in E);eq(r,[enc(F,3),int(good(F)),int(good(F)),enc(L,3),enc(R,3),1]+[int(i!=j) for i,j in product(range(3),repeat=2)])
    elif kind=='rename':
        m,u,v=[integer(z,0,511) for z in x];require(u<3 and v<3 and u!=v,'G1_SCHEMA:merge');E=rows(m,3);out=[]
        for p in permutations(range(3)):
            F={(p[i],p[j]) for i,j in E};M={(p[u] if i==v else p[i],p[u] if j==v else p[j]) for i,j in E};N={(p[u] if i==p[v] else i,p[u] if j==p[v] else j) for i,j in F};eq(M,N);out+=list(p)+[enc(F,3),enc(M,3),enc(N,3),1]
        eq(r,out)
    elif kind=='sameness':
        v=[integer(z,0,5) for z in x];require(len(v)==8,'G1_SCHEMA:counts');d=[v[i]-v[i+4] for i in range(4)];norm=[max(k,0) for k in d]+[max(-k,0) for k in d];tog=[(v[i]+v[i+4]-abs(d[i]))//2 for i in range(4)];eq(sum(v),sum(norm)+2*sum(tog))
        # Burnside: four {-1,0,1} coordinates, swapped in two 2-cycles.
        eq(r,d+norm+tog+[sum(v),sum(abs(z) for z in d),2*sum(tog),3**4,(3**4+3**2)//2]+d)
    elif kind=='mss0':
        s,k=[integer(z,0,10) for z in x];eq(r,[int(s!=0 or k==0),0,0])
    elif kind=='float':
        a,b=[integer(z,0,2**55) for z in x];A=int(float(a));B=int(float(b));eq(r,[a-b,A,B,int(A==B),int(a==b),0]) # diagnostic, never an exact authorization
    elif kind=='pairing':
        a,b,d,u,v=x;eq(a+d,1);eq(u*u+v*v,1);require(a>=0 and d>=0 and a*d>=b*b,'G1_SCHEMA:density2');born=a*u*u+2*b*u*v+d*v*v;diag=a*u*u+d*v*v;eq(r,[u*u,u*v,u*v,v*v,born,diag,2*b*u*v,born*(2*born-1),0,1,0,1,Q(-1,8)])
    elif kind=='realify':
        a,b,c,d=x;z=a*c-b*d;w=a*d+b*c;eq(r,[a,-b,b,a,c,-d,d,c,z,-w,w,z,z,-w,w,z,1,0,0,-1,0,1,1,0]+[0]*8+[2,0,0,2]+[z,w])
    elif kind=='amplitude':
        e=[integer(z,-8,8) for z in x[:6]];a,b,c,d=x[6:];original=e[:3];shift=[e[0]+e[4]-e[3],e[1]+e[5]-e[4],e[2]+e[3]-e[5]];eq(sum(original),sum(shift));z=(a+c,b+d);q=cmul(phase(e[3]),z);N=z[0]**2+z[1]**2;eq(q[0]**2+q[1]**2,N)
        out=[z for k in original+shift for z in phase(k)]+list(phase(sum(original)))+list(phase(sum(shift)))+[N,N,N*N,N*N]
        for n in range(1,9):out += [int(z)%5 for z in closed_gauss(Q(3),Q(4),n)]
        eq(r,out)
    elif kind=='normal':
        k=integer(x[0],0,3);n,E=[(3,[(0,1),(1,2),(2,0)]),(3,[(0,1),(1,2)]),(4,[(0,1),(1,2),(2,0)]),(4,[(0,1),(1,2),(2,3),(3,0),(0,2)])][k];tree=[0,2] if k in (0,2) else [0,1] if k==1 else [0,3,4];components=2 if k==2 else 1;normal=[];sizes=[]
        for signing in range(1<<len(E)):
            orbit={signing ^ sum((((g>>i&1)^(g>>j&1))<<a) for a,(i,j) in enumerate(E)) for g in range(1<<n)};candidate=[m for m in orbit if all(m>>t&1==0 for t in tree)];eq(len(candidate),1);normal.append(candidate[0]);sizes.append(len(orbit));eq(len(orbit),2**(n-components))
        forms=sorted(set(normal));beta=len(E)-n+components;eq(len(forms),2**beta);eq(r,[n,len(E),components,beta,len(forms),2**beta]+tree+[-1]+normal+sizes+forms)
    elif kind=='lggr':
        n=integer(x[0],1,6);m=integer(x[1],0,2**n-1);M=integer(x[2],0,100);b=[m>>i&1 for i in range(n)];counts=[sum(((g>>i&1)^(g>>((i+1)%n)&1))==b[i] for i in range(n)) for g in range(1<<n)];sec=[s for s,z in enumerate(counts) if z==n];eq(len(sec),0 if sum(b)%2 else 2)
        w=[Q(0) if s in (0,7) else Q(1,6) for s in range(8)];slack=[Q(2-sum(((s>>i&1)^(s>>((i+1)%3)&1)) for i in range(3)),3) for s in range(8)];require(min(slack)>=0,'G3_WITNESS:dual_feasibility')
        eq(r,[sum(b)%2,len(sec),int(M==0 or sec!=[])]+counts+sec+w+[Q(2,3)]*4+slack)
    elif kind=='thymus':
        S,P,E=[integer(z,0,15) for z in x];out=[]
        for panel in range(16):
            admitted=all(not(P>>i&1) for i in range(4) if panel>>i&1);fired=sum(E>>i&1 for i in range(4) if panel>>i&1);out += [int(admitted),fired,int(not admitted or fired==0)]
        bad=[i for i in range(4) if E>>i&1 and not P>>i&1];eq(r,out+[int(not bad),bad[0] if bad else -1,int(S&P==0),pop(S&E),pop((15^S)&E)])
    else:raise ValueError('G1_SCHEMA:unknown_operation')

def check(request,candidate,task,config,root):
    _,c,p=audit_bound(request,candidate,task,config);require(set(c['data'])=={'records'} and len(c['data']['records'])==len(p['cases']),'G1_SCHEMA:coverage')
    for record,v in zip(c['data']['records'],p['cases']):require(record['input']==v,'G5_SCOPE:input_identity');verify(p['kind'],v,record['output'])
    return {'records_checked':len(p['cases']),'scope':'Exact finite controls, separately scoped literal Lean statements, explicit remaining imports. No historical label or provider receipt is a proof.'}
