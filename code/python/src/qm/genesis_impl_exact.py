"""Exact declared finite controls. No physical or authority promotion."""
from fractions import Fraction as Q
from itertools import product,permutations
from collections import deque

def need(p):
    if not p:raise ValueError('outside admitted finite domain')
def _admit_exact_scalar(v, max_bits=1024) -> Q:
    if type(v) is bool:
        raise TypeError("Boolean unadmitted on exact path")
    if isinstance(v, float):
        raise TypeError("Float unadmitted on exact path")
    if isinstance(v, (int, Q)):
        num = v.numerator if isinstance(v, Q) else v
        den = v.denominator if isinstance(v, Q) else 1
        if type(num) is not int or type(den) is not int:
            raise TypeError("Scalar numerator and denominator must be int")
        if num.bit_length() > max_bits or den.bit_length() > max_bits:
            raise ValueError(f"Integer exceeds {max_bits} bits")
        return Q(num, den)
    if isinstance(v, str):
        f = Q(v)
        if f.numerator.bit_length() > max_bits or f.denominator.bit_length() > max_bits:
            raise ValueError(f"Integer exceeds {max_bits} bits")
        return Q(f.numerator, f.denominator)
    raise TypeError(f"Unadmitted scalar type: {type(v)}")

def I(v,l,h):need(v.denominator==1 and l<=v<=h);return int(v)
def pair(a,b):return (_admit_exact_scalar(a),_admit_exact_scalar(b))
def add(z,w):return (z[0]+w[0],z[1]+w[1])
def neg(z):return (-z[0],-z[1])
def mul(z,w,cycl=False):
    a,b=z;c,d=w;return (a*c-b*d,a*d+b*c-(b*d if cycl else 0))
def star(z,cycl=False):return (z[0]-(z[1] if cycl else 0),-z[1])
def inv(z,cycl=False):
    s=star(z,cycl)
    norm=mul(z,s,cycl)[0]
    if norm==0:raise ZeroDivisionError('cannot invert zero element')
    return (s[0]/norm,s[1]/norm)
def power(z,k,cycl=False):
    if k<0:return power(inv(z,cycl),-k,cycl)
    o=pair(1,0)
    for _ in range(k):o=mul(o,z,cycl)
    return o
def pm(A,B,cycl=False):
    if not A or not B or not A[0] or not B[0]:
        raise ValueError('empty matrix unadmitted')
    k=len(A[0])
    if any(len(row)!=k for row in A):raise ValueError('ragged matrix A')
    if len(B)!=k:raise ValueError(f'incompatible matrix dimensions: {k} vs {len(B)}')
    n=len(B[0])
    if any(len(row)!=n for row in B):raise ValueError('ragged matrix B')
    return [[sum_pair(mul(A[i][p],B[p][j],cycl) for p in range(k)) for j in range(n)] for i in range(len(A))]
def sum_pair(v):
    o=pair(0,0)
    for z in v:o=add(o,z)
    return o
def dagger(A,cycl=False):return [[star(A[j][i],cycl) for j in range(len(A))] for i in range(len(A[0]))]
def pf(A):return [v for row in A for z in row for v in z]
def mm(A,B):
    if not A or not B or not A[0] or not B[0]:
        raise ValueError('empty matrix unadmitted')
    k=len(A[0])
    if any(len(row)!=k for row in A):raise ValueError('ragged matrix A')
    if len(B)!=k:raise ValueError(f'incompatible matrix dimensions: {k} vs {len(B)}')
    n=len(B[0])
    if any(len(row)!=n for row in B):raise ValueError('ragged matrix B')
    return [[sum(A[i][p]*B[p][j] for p in range(k)) for j in range(n)] for i in range(len(A))]
def flat(A):return [v for r in A for v in r]
def tr(A):return list(map(list,zip(*A)))
def graph(mask,n=3):return {(i,j) for i in range(n) for j in range(n) if mask>>(n*i+j)&1}
def mask(E,n=3):return sum(1<<(n*i+j) for i,j in E)
def image(E,f):return {(f[i],f[j]) for i,j in E}
def legal(E):return all(i!=j for i,j in E)

def regime(history,erase=False):
    d=0;forms=[];inst=set();rules=set();req=set();flip=0;trace=[];failure=-1
    for i,(op,a,b) in enumerate(history):
        if erase and op==0:continue
        ok=True
        if op==0:pass
        elif op==1:d+=1
        elif op==2:
            ok=1<=a<=3
            if ok:forms.append(a)
        elif op==3:
            ok=a<len(forms)
            if ok:
                args=tuple((b//4**j)%4 for j in range(forms[a]));ok=b<4**forms[a] and all(t<d for t in args)
                if ok:inst.add((a,b))
        elif op==4:
            ok=a<len(forms)
            if ok:rules.add(a)
        elif op==5:
            ok=a<d and b<d and a!=b
            if ok:req.add((a,b))
        elif op==6:flip=1-flip
        else:raise ValueError('event code')
        trace += [d+len(forms)+len(inst)+len(rules)+len(req),flip,int(ok)]
        if not ok:failure=i;break
    out=[failure,d,len(forms),len(inst),len(rules),len(req),flip]+forms+[v for p in sorted(inst) for v in p]+sorted(rules)+[v for p in sorted(req) for v in p]
    return trace,out

def cost_graph(seed,targetT,targetE):
    initial=(3,2 if seed==0 else 10) # 2x2 masks: arb or arb+bra
    edges=[(i,j) for i in range(3) for j in range(3) if i!=j]
    initE={(0,1)} | ({(1,0)} if seed else set());start=(3,mask(initE))
    distance={start:0};todo=deque([start])
    while todo:
        T,m=todo.popleft();E=graph(m)
        nxt=[]
        if T==3:nxt.append((7,m))
        for p in edges:
            if (T>>p[0]&1) and (T>>p[1]&1):nxt.append((T,mask(E^{p})))
        for q in nxt:
            if q not in distance:distance[q]=distance[(T,m)]+1;todo.append(q)
    target=graph(targetE);need(legal(target) and all(targetT>>i&1 and targetT>>j&1 for i,j in target))
    lost=len(initE-target);size=bin(targetT).count('1')+len(target);base=2+len(initE);formula=size+2*lost-base
    states=sorted(distance);return [len(states),distance[(targetT,targetE)],size,lost,base,formula]+[z for q in states for z in (*q,distance[q])]

def first_separation():
    # Explicit finite Item alphabet, bounded arities 1 and 2 and two data.
    items=[('d',0),('f',1),('f',2)]+[('i',a) for a in [(0,),(1,),(0,0),(0,1),(1,0),(1,1)]]+[('r',0)]
    seqs=[()]+[(i,) for i in range(len(items))]+list(product(range(len(items)),repeat=2));rows=[]
    for seq in seqs:
        forms=[];inst=set();allrule=False;d=2;valid=True;arity=0
        for j in seq:
            op,a=items[j]
            if op=='d':d+=1
            elif op=='f':forms.append(a);arity+=a
            elif not forms:valid=False;break
            elif op=='r':allrule=True
            elif len(a)!=forms[0]:valid=False;break
            else:inst.add(a)
        sep=False
        if valid and forms:
            for ar in (1,2):
                if forms[0]!=ar:continue
                for hole in range(ar):
                    for tail in product(range(d),repeat=ar-1):
                        def member(x):
                            z=list(tail);z.insert(hole,x);return allrule or tuple(z) in inst
                        sep |= member(0)!=member(1)
        rows.append([len(seq),int(valid),int(sep),arity])
    winners=[i for i,r in enumerate(rows) if r[1] and r[2]];m=min(rows[i][0] for i in winners);ties=[i for i in winners if rows[i][0]==m];a=min(rows[i][3] for i in ties);best=[i for i in ties if rows[i][3]==a]
    return [len(rows)]+flat(rows)+[m,len(ties),a,len(best)]+ties+best

def normal_graph(which):
    choices=[(3,[(0,1),(1,2),(2,0)]),(3,[(0,1),(1,2)]),(4,[(0,1),(1,2),(2,0)]),(4,[(0,1),(1,2),(2,3),(3,0),(0,2)])]
    n,E=choices[which];adj=[[] for _ in range(n)]
    for k,(i,j) in enumerate(E):adj[i].append((j,k));adj[j].append((i,k))
    parent={};tree=[];roots=[]
    for root in range(n):
        if root in parent:continue
        roots.append(root);parent[root]=None;todo=[root]
        for i in todo:
            for j,k in adj[i]:
                if j not in parent:parent[j]=(i,k);tree.append(k);todo.append(j)
    normals=[];sizes=[]
    for s in range(1<<len(E)):
        gauge={r:0 for r in roots}
        while len(gauge)<n:
            for j,p in parent.items():
                if p and j not in gauge and p[0] in gauge:gauge[j]=gauge[p[0]]^(s>>p[1]&1)
        t=sum((((s>>k)&1)^gauge[i]^gauge[j])<<k for k,(i,j) in enumerate(E));normals.append(t)
        orbit={s ^ sum((((g>>i&1)^(g>>j&1))<<k) for k,(i,j) in enumerate(E)) for g in range(1<<n)};sizes.append(len(orbit))
    forms=sorted(set(normals));beta=len(E)-n+len(roots)
    return [n,len(E),len(roots),beta,len(forms),2**beta]+tree+[-1]+normals+sizes+forms

def evaluate(kind,values):
    x=[_admit_exact_scalar(v) for v in values]
    if kind=='weyl':
        need(len(x)==11);a,b=[I(z,0,2) for z in x[:2]];A=[[pair(x[2+3*i+j],0) for j in range(3)] for i in range(3)];w=pair(0,1)
        def W(c,d):return [[power(w,d*j,True) if i==(j+c)%3 else pair(0,0) for j in range(3)] for i in range(3)]
        U=W(a,0);V=W(0,b);comm=pm(pm(pm(U,V,True),dagger(U,True),True),dagger(V,True),True);basis=[W(c,d) for c in range(3) for d in range(3)];coef=[]
        for B in basis:
            T=pm(dagger(B,True),A,True);coef.append(tuple(v/3 for v in sum_pair(T[i][i] for i in range(3))))
        recovered=[[sum_pair(mul(c,B[i][j],True) for c,B in zip(coef,basis)) for j in range(3)] for i in range(3)]
        gram=[[sum_pair(pm(dagger(B,True),C,True)[i][i] for i in range(3)) for C in basis] for B in basis]
        out=pf(comm)+list(power(w,-a*b,True))+[v for c in coef for v in c]+pf(recovered)+pf(gram)
    elif kind=='duality':
        a,b=x;out=[abs(a)+abs(b)];vals=[u*a+v*b for u,v in product((-1,0,1),repeat=2)];out+=vals+[max(vals),abs(a)+abs(b)-max(vals)]
    elif kind=='separation':need(x==[0]);out=first_separation()
    elif kind=='distinct':
        need(len(x)==1);m=I(x[0],0,15);rows=[[int(legal(graph(k,2))),int(k&2!=0),int(k&4!=0)] for k in range(16)];allowed=[k for k,r in enumerate(rows) if r[0] and r[1]];out=flat(rows)+[len(allowed)]+allowed+rows[m]
    elif kind in ('noreturn','events','erasure','supply'):
        need(len(x)%3==0 and len(x)<=30);h=[tuple(I(z,0,255) for z in x[i:i+3]) for i in range(0,len(x),3)];need(all(a[0]<=6 for a in h));t,o=regime(h);te,oe=regime(h,True);out=[len(t),len(o)]+t+o+[len(te),len(oe)]+te+oe
    elif kind=='fewest':
        seed,T,E=[I(z,0,511) for z in x];need(seed<=1 and T in (3,7));out=cost_graph(seed,T,E)
    elif kind=='obstruction':
        m,u,v=[I(z,0,511) for z in x];need(u<3 and v<3 and u!=v);E=graph(m);need(legal(E));f=[u if k==v else k for k in range(3)];merged=image(E,f);clean=E-{(u,v),(v,u)};left=image(clean,f);right=merged-{(u,u)}
        out=[mask(merged),int(legal(merged)),int((u,v) not in E and (v,u) not in E),mask(left),mask(right),int(left==right)]+[int(legal(E|{(i,j)})) for i in range(3) for j in range(3)]
    elif kind=='rename':
        m,u,v=[I(z,0,511) for z in x];need(u<3 and v<3 and u!=v);E=graph(m);out=[]
        for p in permutations(range(3)):
            f=[u if k==v else k for k in range(3)];lhs=image(image(E,f),p);g=[p[u] if k==p[v] else k for k in range(3)];rhs=image(image(E,p),g);out += list(p)+[mask(image(E,p)),mask(lhs),mask(rhs),int(legal(E)==legal(image(E,p)))]
    elif kind=='sameness':
        need(len(x)==8);v=[I(z,0,5) for z in x];r,s=v[:4],v[4:];d=[a-b for a,b in zip(r,s)];normal=[max(z,0) for z in d]+[max(-z,0) for z in d];tog=[min(a,b) for a,b in zip(r,s)];canon=lambda z:min(tuple(z),tuple(z[i] for i in (3,2,1,0)))
        all_d={tuple(a[i]-a[i+4] for i in range(4)) for a in product(range(2),repeat=8)}
        out=d+normal+tog+[sum(v),sum(normal),2*sum(tog),len(all_d),len({canon(z) for z in all_d})]+[z+1-(w+1) for z,w in zip(r,s)]
    elif kind=='mss0':
        stage,node=[I(z,0,10) for z in x];out=[int(stage>0 or node==0),0,0] # structural eligibility, mathematical authority, empirical authority
    elif kind=='float':
        a,b=[I(z,0,2**55) for z in x]
        def rounded(n):
            k=max(0,n.bit_length()-53);step=1<<k;q,r=divmod(n,step);return (q+int(2*r>step or (2*r==step and q%2)))*step
        A,B=rounded(a),rounded(b);out=[a-b,A,B,int(A==B),int(a==b),0]
    elif kind=='pairing':
        a,b,d,u,v=x;need(a+d==1 and a>=0 and d>=0 and a*d>=b*b and u*u+v*v==1);p=a*u*u+2*b*u*v+d*v*v;de=a*u*u+d*v*v;out=[u*u,u*v,u*v,v*v,p,de,p-de,2*p*p-p,Q(0),Q(1),Q(0),Q(1),Q(-1,8)]
    elif kind=='realify':
        a,b,c,d=x;R=lambda a,b:[[a,-b],[b,a]];A=R(a,b);B=R(c,d);P=mm(A,B);C=R(a*c-b*d,a*d+b*c);M=[[1,0,0,-1],[0,1,1,0]];J=[[0,-1],[1,0]];eye=[[1,0],[0,1]]
        kron=lambda A,B:[[A[i//len(B)][j//len(B[0])]*B[i%len(B)][j%len(B[0])] for j in range(len(A[0])*len(B[0]))] for i in range(len(A)*len(B))]
        L=kron(J,eye);H=kron(eye,J);D=[[p-q for p,q in zip(r,s)] for r,s in zip(L,H)];t=[a*c,a*d,b*c,b*d];out=flat(A)+flat(B)+flat(P)+flat(C)+flat(M)+flat(mm(M,D))+flat(mm(M,tr(M)))+flat(mm(M,[[z] for z in t]))
    elif kind=='amplitude':
        need(len(x)==10);e0,e1,e2,g0,g1,g2=[I(z,-8,8) for z in x[:6]];a,b,c,d=x[6:];u=pair(Q(3,5),Q(4,5));e=[e0,e1,e2];f=[e0+g1-g0,e1+g2-g1,e2+g0-g2];U=power(u,g0);z=pair(a+c,b+d);t=mul(U,z);norm=lambda z:z[0]**2+z[1]**2;out=[v for k in e+f for v in power(u,k)]+list(power(u,sum(e)))+list(power(u,sum(f)))+[norm(z),norm(t),norm(z)**2,norm(t)**2]
        for n in range(1,9):out += [int(v)%5 for v in power(pair(3,4),n)]
    elif kind=='normal':out=normal_graph(I(x[0],0,3))
    elif kind=='lggr':
        n=I(x[0],1,6);m=I(x[1],0,2**n-1);M=I(x[2],0,100);counts=[sum(((s>>i&1)^(s>>((i+1)%n)&1))==(m>>i&1) for i in range(n)) for s in range(1<<n)];sections=[i for i,z in enumerate(counts) if z==n];parity=bin(m).count('1')%2
        out=[parity,len(sections),int(M==0 or parity==0)]+counts+sections
        weights=[Q(0) if s in (0,7) else Q(1,6) for s in range(8)];sat=[sum(((s>>i&1)^(s>>((i+1)%3)&1)) for i in range(3)) for s in range(8)];out+=weights+[sum(weights[s]*((s>>i&1)^(s>>((i+1)%3)&1)) for s in range(8)) for i in range(3)]+[Q(2,3)]+[Q(2-z,3) for z in sat]
    elif kind=='thymus':
        panel,P,E=[I(z,0,15) for z in x];out=[]
        for S in range(16):out += [int(S&P==0),bin(S&E).count('1'),int(not(S&P==0) or S&E==0)]
        bad=[i for i in range(4) if E>>i&1 and not P>>i&1];out += [int(not bad),bad[0] if bad else -1,int(panel&P==0),bin(panel&E).count('1'),bin((15^panel)&E).count('1')]
    else:raise ValueError('unknown finite operation')
    return [str(Q(v)) for v in out]

def certify(kind,cases):return {'records':[{'input':v,'output':evaluate(kind,v)} for v in cases]}
