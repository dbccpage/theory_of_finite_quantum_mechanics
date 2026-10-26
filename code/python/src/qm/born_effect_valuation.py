"""Exact effect-additive valuations on rational matrices; the Born trace form from effect additivity, not from Gleason.

Replays in exact rational arithmetic the Lean modules of
dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T205000Z_effect_valuation_lean:
rational PSD certification by a Gram (LDL^T) decomposition with exact negative witnesses, effects
0 <= E <= 1 in the quadratic-form preorder, the order-unit bound, the midpoint extension of a
valuation to a rational linear functional, its representing matrix rho with trace(rho E) = v(E),
and the parity frame function on rational rays of S^2 that no quadratic form reproduces.
The matrix algebra and its order are supplied; only the form of the valuation is derived.
AuthorityEffect: None.
"""
from fractions import Fraction as Q
from itertools import product
from math import ceil,isqrt
def _q(x):
    if type(x) not in (int,Q):raise ValueError('exact integer or Fraction entries required')
    return Q(x)
def matrix(rows):
    m=[[_q(x) for x in r] for r in rows];n=len(m)
    if n==0 or any(len(r)!=n for r in m):raise ValueError('nonempty square matrix required')
    return m
def vector(xs):
    v=[_q(x) for x in xs]
    if not v:raise ValueError('nonempty vector required')
    return v
def _same_shape(A,B):
    if len(A)!=len(B) or any(len(a)!=len(b) for a,b in zip(A,B)):raise ValueError('equal matrix shapes required')
def _same_length(x,y):
    if len(x)!=len(y):raise ValueError('equal vector lengths required')
def identity(n):return [[Q(int(i==j)) for j in range(n)] for i in range(n)]
def single(n,i,j):
    if not (0<=i<n and 0<=j<n):raise ValueError('index out of range')
    return [[Q(int(r==i and c==j)) for c in range(n)] for r in range(n)]
def add(A,B):_same_shape(A,B);return [[a+b for a,b in zip(ra,rb)] for ra,rb in zip(A,B)]
def sub(A,B):_same_shape(A,B);return [[a-b for a,b in zip(ra,rb)] for ra,rb in zip(A,B)]
def scale(c,A):return [[c*a for a in r] for r in A]
def transpose(A):return [list(r) for r in zip(*A)]
def mat_vec(A,x):
    if any(len(r)!=len(x) for r in A):raise ValueError('vector length must equal the matrix width')
    return [sum(a*b for a,b in zip(r,x)) for r in A]
def dot(x,y):_same_length(x,y);return sum(a*b for a,b in zip(x,y))
def outer(x,y):return [[a*b for b in y] for a in x]
def trace(A):return sum(A[i][i] for i in range(len(A)))
def trace_mul(A,B):_same_shape(A,B);n=len(A);return sum(A[i][j]*B[j][i] for i in range(n) for j in range(n))
def quadratic_form(A,x):return dot(x,mat_vec(A,x))
def is_symmetric(A):return A==transpose(A)
def symmetric_part(A):return scale(Q(1,2),add(A,transpose(A)))
def _unit(n,p):return [Q(int(i==p)) for i in range(n)]
def _lift_witness(terms,y):
    x=y[:]
    for k,_,w in reversed(terms):x[k]=-sum(w[i]*x[i] for i in range(k+1,len(x)))
    return x
def gram_decomposition(E):
    """('psd',[(d_k,w_k),...]) with E == sum d_k w_k w_k^T and d_k >= 0, or ('not_psd',x) with x^T E x < 0; symmetric E required."""
    E=matrix(E)
    if not is_symmetric(E):raise ValueError('symmetric matrix required')
    n=len(E);M=[r[:] for r in E];terms=[]
    for p in range(n):
        piv=M[p][p]
        if piv<0:return 'not_psd',_lift_witness(terms,_unit(n,p))
        if piv==0:
            for j in range(p+1,n):
                c=M[j][p]
                if c!=0:
                    m=M[j][j];s=Q(-1 if c>0 else 1) if m<=0 else -c/m;y=_unit(n,p);y[j]=s
                    return 'not_psd',_lift_witness(terms,y)
            continue
        w=[M[p][i]/piv for i in range(n)];terms.append((p,piv,w));M=sub(M,scale(piv,outer(w,w)))
    return 'psd',[(d,w) for _,d,w in terms]
def verify_gram(E,terms):
    E=matrix(E);n=len(E);S=[[Q(0)]*n for _ in range(n)]
    for d,w in terms:
        w=vector(w);_same_length(w,E)
        if _q(d)<0:return False
        S=add(S,scale(_q(d),outer(w,w)))
    return S==E
def psd_certificate(E):
    E=matrix(E);kind,data=gram_decomposition(symmetric_part(E))
    if kind=='psd':return {'status':'psd','terms':[(str(d),list(map(str,w))) for d,w in data],'reconstructs':verify_gram(symmetric_part(E),data)}
    return {'status':'not_psd','witness':list(map(str,data)),'value':str(quadratic_form(E,data))}
def is_psd(E):return gram_decomposition(symmetric_part(matrix(E)))[0]=='psd'
def extension_layer(matrix,identity,add,sub,scale,is_psd,psd_certificate,order_unit_bound,
                    is_carrier=lambda A: True, project=lambda A: A):
    """Shared effect/extension layer with an explicit carrier and projection.

    The rational model uses its whole matrix space and quadratic preorder.
    The Hermitian model admits only Hermitian effects and extends through the
    Hermitian projection. Valuations and bounds are real Fractions.
    """
    def is_effect(E):E=matrix(E);return is_carrier(E) and is_psd(E) and is_psd(sub(identity(len(E)),E))
    def effect_certificate(E):
        E=matrix(E);lower=psd_certificate(E);upper=psd_certificate(sub(identity(len(E)),E))
        carrier=is_carrier(E)
        return {'lower':lower,'upper':upper,'is_carrier':carrier,'is_effect':carrier and lower['status']=='psd' and upper['status']=='psd'}
    def midpoint(A,t):
        A=matrix(A);t=_q(t)
        if t<=0:raise ValueError('positive bound required')
        return scale(1/(2*t),add(A,scale(t,identity(len(A)))))
    def extend(valuation,A,t=None):
        A=project(matrix(A));t=Q(order_unit_bound(A)+1) if t is None else _q(t)
        return 2*t*_q(valuation(midpoint(A,t)))-t
    def extension_consistency(valuation,A,bounds):
        values=[extend(valuation,A,t) for t in bounds]
        return {'bounds':list(map(str,bounds)),'values':list(map(str,values)),'consistent':len(set(values))==1}
    def effects_of_dimension(n,effects):
        effects=[matrix(E) for E in effects]
        if any(len(E)!=n for E in effects):raise ValueError('effects of dimension n required')
        return effects
    def valuation_axioms(valuation,n,effects,pairs):
        effects=effects_of_dimension(n,effects);pairs=[tuple(effects_of_dimension(n,[E,F])) for E,F in pairs]
        if not all(is_effect(E) for E in effects) or not all(is_effect(E) and is_effect(F) and is_effect(add(E,F)) for E,F in pairs):raise ValueError('effects and effect pairs with effect sums required')
        return {'unit':_q(valuation(identity(n)))==1,'nonneg':all(_q(valuation(E))>=0 for E in effects),'additive':all(_q(valuation(add(E,F)))==_q(valuation(E))+_q(valuation(F)) for E,F in pairs)}
    return is_effect,effect_certificate,midpoint,extend,extension_consistency,effects_of_dimension,valuation_axioms
def rank_one_effect(x):
    x=vector(x);nrm=dot(x,x)
    if nrm==0:raise ValueError('nonzero vector required')
    return scale(1/nrm,outer(x,x))
def order_unit_bound(A):return ceil(sum(abs(a) for r in matrix(A) for a in r))
def bounded_by(A,t,x):A=matrix(A);t=_q(t);x=vector(x);q=quadratic_form(A,x);s=t*dot(x,x);return -s<=q<=s
is_effect,effect_certificate,midpoint,extend,extension_consistency,_effects_of_dimension,valuation_axioms=extension_layer(matrix,identity,add,sub,scale,is_psd,psd_certificate,order_unit_bound)
def representing_matrix(valuation,n):return [[extend(valuation,single(n,j,i)) for j in range(n)] for i in range(n)]
def born_valuation(rho):rho=matrix(rho);return lambda E:trace_mul(rho,matrix(E))
def born_certificate(valuation,n,effects=()):
    effects=_effects_of_dimension(n,effects)
    if not all(is_effect(E) for E in effects):raise ValueError('effects required')
    rho=representing_matrix(valuation,n);cert=psd_certificate(rho)
    return {'rho':[list(map(str,r)) for r in rho],'symmetric':is_symmetric(rho),'trace':str(trace(rho)),'psd':cert['status']=='psd','psd_certificate':cert,'agrees_on_effects':all(trace_mul(rho,E)==_q(valuation(E)) for E in effects),'effects_checked':len(effects)}
def square_valuation(E):E=matrix(E);return E[0][0]**2
def bad_linear_valuation(E):
    E=matrix(E)
    if len(E)!=3:raise ValueError('three-dimensional control')
    return 2*E[0][0]-E[2][2]
def is_ray(v):
    if len(v)!=3 or any(type(x) is not int for x in v):raise ValueError('integer triple required')
    a,b,c=v
    if a%2==0 and b%2==0 and c%2==0:return False
    s=a*a+b*b+c*c;r=isqrt(s);return r*r==s
def parity(v):
    if not is_ray(v):raise ValueError('ray required')
    return Q(int(v[2]%2==1))
def rays_in_box(N):return [v for v in product(range(-N,N+1),repeat=3) if is_ray(v)]
def orthogonal_triples(rays):
    rays=list(rays);out=[]
    for i,u in enumerate(rays):
        for j in range(i+1,len(rays)):
            v=rays[j]
            if dot(u,v)!=0:continue
            for k in range(j+1,len(rays)):
                w=rays[k]
                if dot(u,w)==0 and dot(v,w)==0:out.append((u,v,w))
    return out
def parity_frame_check(N):
    rays=rays_in_box(N);triples=orthogonal_triples(rays);sums=[parity(u)+parity(v)+parity(w) for u,v,w in triples]
    return {'box':N,'rays':len(rays),'orthogonal_triples':len(triples),'nonvacuous':bool(triples),'all_sum_to_one':bool(triples) and all(s==1 for s in sums),'values':sorted({str(parity(v)) for v in rays})}
def solve_linear_system(rows,rhs):
    if not rows or len(rows)!=len(rhs) or not rows[0] or any(len(r)!=len(rows[0]) for r in rows):raise ValueError('nonempty rectangular system with one right-hand side per row required')
    M=[list(map(_q,r))+[_q(b)] for r,b in zip(rows,rhs)];m=len(M);n=len(M[0])-1;r=0;pivots=[]
    for c in range(n):
        p=next((i for i in range(r,m) if M[i][c]!=0),None)
        if p is None:continue
        M[r],M[p]=M[p],M[r];M[r]=[x/M[r][c] for x in M[r]]
        for i in range(m):
            if i!=r and M[i][c]!=0:M[i]=[a-M[i][c]*b for a,b in zip(M[i],M[r])]
        pivots.append(c);r+=1
    if any(all(x==0 for x in row[:n]) and row[n]!=0 for row in M):return 'inconsistent',None
    sol=[Q(0)]*n
    for i,c in enumerate(pivots):sol[c]=M[i][n]
    return 'solution',sol
def parity_quadratic_system(rays):
    rays=[tuple(v) for v in rays]
    if not all(is_ray(v) for v in rays):raise ValueError('rays required')
    rows=[[Q(a*a),Q(b*b),Q(c*c),Q(2*a*b),Q(2*a*c),Q(2*b*c)] for a,b,c in rays];rhs=[parity(v)*(v[0]**2+v[1]**2+v[2]**2) for v in rays]
    status,sol=solve_linear_system(rows,rhs)
    return {'rays':[list(v) for v in rays],'unknowns':['r00','r11','r22','r01','r02','r12'],'status':status,'solution':None if sol is None else list(map(str,sol))}
PARITY_WITNESS_RAYS=[(1,0,0),(0,1,0),(0,0,1),(3,4,0),(0,3,4),(0,4,3)]
