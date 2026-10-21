"""Exact replay of the finite Wigner theorem over Q(i)^n: a map preserving transition probabilities is, up to ray freedom, a linear or conjugate-linear similarity, and a unitary only when its scale is a norm from Q(i).

Replays in exact Gaussian-rational arithmetic the Lean modules of
dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner (FiniteWignerKernel,
FiniteWignerTheorem, FiniteWignerSimilarity, GaussRatAutomorphisms): the transition probability
tp(x,y) = |ip(x,y)|^2/(vnorm(x) vnorm(y)) and its identity with the Born readout of the rank-one effect
P_x, the similarity certificate F^H F = d*I with an exact first-offending-entry witness, the twist by the
two field automorphisms of Q(i), the reconstruction of (F, d, eps) from the images of the probes e_m,
e_i0 + e_j and e_i0 + i*e_j (steps 1-5 of the Lean proof, every failure an exact witness that the map does
not preserve tp), the check that T x is a nonzero multiple of F twist(eps, x), and the unitary
normalisation decided by the two-squares theorem for positive rationals (F3 with F3^H F3 = 3*I is the
countermodel: tp-preserving, induced by no Q(i)-unitary or antiunitary). The carrier Q(i)^n, its inner
product, the Born readout and the automorphism twist are supplied; tp-preservation with nonvanishing
images is the hypothesis; only the form of the map is derived. Stages 1 and 2 of the theorem (every
nonzero x, not only the probes) are replayed on supplied samples, not for all x. AuthorityEffect: None.
"""
from fractions import Fraction as Q
from math import isqrt
from .born_effect_valuation import _q,_same_length,_same_shape
from .born_hermitian_valuation import G,I,_g,matrix,vector,adjoint,identity,scale,inner as _ip,mat_vec as _mv,rank_one_effect,re_hermitian_form
from .inner_product_uniqueness import permutation,permute
# ---------------------------------------------------------------- admission, vectors, transition probability
def _dim(n):
    if type(n) is not int or n<1:raise ValueError('positive integer dimension required')
    return n
def _eps(eps):
    if type(eps) is not int or eps not in (1,-1):raise ValueError('eps in {+1,-1} required')
    return eps
def unit_vector(n,i,c=1):
    """c*e_i in Q(i)^n."""
    n=_dim(n)
    if type(i) is not int or not (0<=i<n):raise ValueError('index out of range')
    c=G(c);return [c if k==i else G(0) for k in range(n)]
def inner(x,y):
    """ip(x,y) = sum conj(x_i) y_i, conjugate-linear in the first slot."""
    x,y=vector(x),vector(y);_same_length(x,y);return _ip(x,y)
def vnorm(x):
    """re ip(x,x) = sum |x_i|^2, a nonnegative rational."""
    x=vector(x);return _ip(x,x).re
def _nonzero_pair(x,y):
    x,y=vector(x),vector(y);_same_length(x,y);nx,ny=_ip(x,x).re,_ip(y,y).re
    if nx==0 or ny==0:raise ValueError('nonzero vectors required')
    return x,y,nx,ny
def transition_probability(x,y):
    """tp(x,y) = normSq(ip(x,y))/(vnorm(x) vnorm(y)), a rational in [0,1]; nonzero vectors of equal length required."""
    x,y,nx,ny=_nonzero_pair(x,y);return _ip(x,y).norm_sq()/(nx*ny)
def born_transition(x,y):
    """re(y^* P_x y)/vnorm(y) with P_x = x x^*/vnorm(x) the rank-one effect of x (hf_rankOne): the Born readout, equal to tp(x,y)."""
    x,y,nx,ny=_nonzero_pair(x,y);return re_hermitian_form(rank_one_effect(x),y)/ny
def same_ray(x,y):
    """True when x and y are nonzero and y = mu*x (mu then nonzero): ip(x,y) x == vnorm(x) y, i.e. tp(x,y) == 1."""
    x,y=vector(x),vector(y);_same_length(x,y);nx=_ip(x,x).re
    if nx==0 or not any(y):return False
    p=_ip(x,y);return [p*a for a in x]==[nx*b for b in y]
def twist(eps,x):
    """twist(+1,x) = x and twist(-1,x) = conj(x) componentwise: the two field automorphisms of Q(i) on coordinates."""
    eps=_eps(eps);x=vector(x);return x if eps==1 else [a.conj() for a in x]
# ---------------------------------------------------------------- matrices and similarities
def conj_transpose(F):F=matrix(F);return adjoint(F)
def mat_vec(F,x):F,x=matrix(F),vector(x);return _mv(F,x)
def mat_mul(A,B):
    A,B=matrix(A),matrix(B);_same_shape(A,B);n=len(A)
    return [[sum((A[i][k]*B[k][j] for k in range(n)),G(0)) for j in range(n)] for i in range(n)]
def gram(F):
    """F^H F: entry (i,j) is ip(column i, column j)."""
    F=matrix(F);return mat_mul(adjoint(F),F)
def similarity_certificate(F):
    """('similarity',d) when F^H F == d*I with d = re((F^H F)[0][0]) > 0, else ('not_similarity',(i,j,(F^H F)[i][j],expected)) for the first offending entry in row-major order, expected = d*delta_ij; a non-positive diagonal is offending, so a zero first column is reported at (0,0) with entry and expected both 0."""
    M=gram(F);n=len(M);d=M[0][0].re
    for i in range(n):
        for j in range(n):
            e=G(d) if i==j else G(0)
            if M[i][j]!=e or (i==j and M[i][i].re<=0):return 'not_similarity',(i,j,M[i][j],e)
    return 'similarity',d
def apply(F,eps,x):
    """F * twist(eps, x)."""
    return mat_vec(F,twist(eps,x))
def inverse_similarity(F):
    """(1/d) F^H, the two-sided inverse of a similarity of scale d; ValueError('not_similarity',witness) otherwise."""
    F=matrix(F);verdict,data=similarity_certificate(F)
    if verdict!='similarity':raise ValueError(verdict,data)
    return scale(1/data,adjoint(F))
def diagonal(entries):v=vector(entries);n=len(v);return [[v[i] if i==j else G(0) for j in range(n)] for i in range(n)]
def quaternion_block(a,b):
    """[[a,-conj b],[b,conj a]], a similarity of scale |a|^2+|b|^2 when (a,b) != (0,0)."""
    a,b=G(a),G(b);return [[a,-b.conj()],[b,a.conj()]]
def block_diagonal(*blocks):
    bs=[matrix(B) for B in blocks]
    if not bs:raise ValueError('at least one block required')
    n=sum(len(B) for B in bs);M=[[G(0)]*n for _ in range(n)];k=0
    for B in bs:
        for i,r in enumerate(B):
            for j,a in enumerate(r):M[k+i][k+j]=a
        k+=len(B)
    return M
def permutation_matrix(sigma):
    """P with P e_j = e_{sigma(j)}, so mat_vec(P,x) == permute(sigma,x) (the H006 envelope); unitary, d = 1."""
    s=permutation(sigma);n=len(s)
    if n==0:raise ValueError('nonempty permutation required')
    return [[G(int(i==s[j])) for j in range(n)] for i in range(n)]
def f3():
    """[[1,-1+i],[1+i,1]] with F3^H F3 = 3*I: a similarity whose scale 3 is not a norm from Q(i)."""
    return [[G(1),G(-1,1)],[G(1,1),G(1)]]
def hadamard2():
    """[[1,1],[1,-1]] with scale 2 = |1+i|^2, so hadamard2/(1+i) is unitary."""
    return [[G(1),G(1)],[G(1),G(-1)]]
# ---------------------------------------------------------------- coordinates, probes, reconstruction
def coordinates(f,y):
    """z with y == sum z_i f_i and z_i = ip(f_i,y)/vnorm(f_i), for n pairwise orthogonal nonzero vectors f_i of length n; raises ValueError('zero_vector',i), ValueError('not_orthogonal',(i,j,ip(f_i,f_j))) or ValueError('not_in_span',(y,sum z_i f_i))."""
    f=[vector(v) for v in f];y=vector(y);n=len(f)
    if any(len(v)!=n for v in f) or len(y)!=n:raise ValueError('n vectors of length n and a vector of length n required')
    norms=[_ip(v,v).re for v in f]
    for i,v in enumerate(norms):
        if v==0:raise ValueError('zero_vector',i)
    for i in range(n):
        for j in range(i+1,n):
            p=_ip(f[i],f[j])
            if p:raise ValueError('not_orthogonal',(i,j,p))
    z=[_ip(f[i],y)/norms[i] for i in range(n)];s=[sum((z[i]*f[i][k] for i in range(n)),G(0)) for k in range(n)]
    if s!=y:raise ValueError('not_in_span',(y,s))
    return z
def probe(n,i0,j,c=1):
    """e_i0 + c*e_j for j != i0: the probes e_i0 + e_j (step 2) and e_i0 + i*e_j (step 3)."""
    if i0==j:raise ValueError('distinct indices required')
    return [a+b for a,b in zip(unit_vector(n,i0),unit_vector(n,j,c))]
def reconstruction_probes(n,i0=0):
    """The probes of steps 1-3: e_m for every m, then e_i0 + e_j and e_i0 + i*e_j for every j != i0."""
    n=_dim(n);unit_vector(n,i0);others=[j for j in range(n) if j!=i0]
    return [unit_vector(n,m) for m in range(n)]+[probe(n,i0,j) for j in others]+[probe(n,i0,j,I) for j in others]
def consistency_probes(n,i0,j,k):
    """(e_i0 + i e_j + i e_k, e_i0 + e_j + e_k) with tp 5/9; the images forced by eps_j != eps_k have tp 1/9 (the step 4 probe)."""
    if len({i0,j,k})!=3:raise ValueError('three distinct indices required')
    e0,ej,ek=unit_vector(n,i0),unit_vector(n,j),unit_vector(n,k)
    return [a+I*b+I*c for a,b,c in zip(e0,ej,ek)],[a+b+c for a,b,c in zip(e0,ej,ek)]
def _image(T,x,n):
    y=vector(T(x))
    if len(y)!=n:raise ValueError('T must return vectors of length n')
    return y
def _two_term(z,i0,j,tag):
    """The alignment failure of a coordinate vector that must be a*e_i0 + b*e_j with a, b nonzero, or None."""
    k=next((k for k in range(len(z)) if k not in (i0,j) and z[k]),None)
    if k is not None:return (tag+'support',k,z[k])
    if not z[i0] or not z[j]:return (tag+'vanishing',z[i0],z[j])
    return None
def reconstruct(T,n,i0=0):
    """Steps 1-5 of the finite Wigner proof on the images of the probes: ('reconstructed',(F,d,eps)) or ('not_tp_preserving',witness).

    1. g_i = T(e_i) nonzero and pairwise orthogonal: ('zero_image',x) (for any probe x), ('orthogonality',i,j,ip(g_i,g_j)).
    2. h_j = T(e_i0 + e_j) = a g_i0 + b g_j, a and b nonzero, |a|^2 vnorm(g_i0) == |b|^2 vnorm(g_j):
       ('alignment',j,'support',k,z_k), ('alignment',j,'vanishing',a,b), ('alignment',j,'balance',lhs,rhs);
       then f_i0 = g_i0, f_j = (b/a) g_j, vnorm(f_j) == d = vnorm(g_i0) and h_j = a (f_i0 + f_j).
    3. k_j = T(e_i0 + i e_j) = a' f_i0 + b' f_j, u = b'/a' with |u|^2 == 1 and |1+u|^2 == 2, so u = i (eps_j = +1) or
       u = -i (eps_j = -1): ('alignment',j,'phase_support',k,z_k), ('alignment',j,'phase_vanishing',a',b'), ('sign',j,u).
    4. every eps_j equals eps_j0, j0 the first index != i0 (eps = +1 when n == 1): ('consistency',j0,k,eps_j0,eps_k).
    5. F has columns f_0..f_{n-1} and F^H F == d*I.
    Each witness is a tp equation failing among reconstruction_probes(n,i0) (consistency: together with
    consistency_probes(n,i0,j0,k)). For T x = c(x) F0 twist(eps,x) the result is F = c(e_i0) F0, d = |c(e_i0)|^2 d0."""
    n=_dim(n)
    if not callable(T):raise ValueError('callable T required')
    unit_vector(n,i0);e=[unit_vector(n,i) for i in range(n)];others=[j for j in range(n) if j!=i0];g=[]
    for x in e:
        y=_image(T,x,n)
        if not any(y):return 'not_tp_preserving',('zero_image',x)
        g.append(y)
    for i in range(n):
        for j in range(i+1,n):
            p=_ip(g[i],g[j])
            if p:return 'not_tp_preserving',('orthogonality',i,j,p)
    f=list(g)
    for j in others:
        x=probe(n,i0,j);h=_image(T,x,n)
        if not any(h):return 'not_tp_preserving',('zero_image',x)
        z=coordinates(g,h);w=_two_term(z,i0,j,'')
        if w:return 'not_tp_preserving',('alignment',j)+w
        a,b=z[i0],z[j];lhs,rhs=a.norm_sq()*vnorm(g[i0]),b.norm_sq()*vnorm(g[j])
        if lhs!=rhs:return 'not_tp_preserving',('alignment',j,'balance',lhs,rhs)
        f[j]=[(b/a)*c for c in g[j]]
    d=vnorm(g[i0]);eps={}
    for j in others:
        x=probe(n,i0,j,I);k=_image(T,x,n)
        if not any(k):return 'not_tp_preserving',('zero_image',x)
        z=coordinates(f,k);w=_two_term(z,i0,j,'phase_')
        if w:return 'not_tp_preserving',('alignment',j)+w
        u=z[j]/z[i0]
        if u.norm_sq()!=1 or (1+u).norm_sq()!=2:return 'not_tp_preserving',('sign',j,u)
        eps[j]=1 if u==I else -1
    s=eps[others[0]] if others else 1
    for k in others:
        if eps[k]!=s:return 'not_tp_preserving',('consistency',others[0],k,s,eps[k])
    F=[[f[i][r] for i in range(n)] for r in range(n)];assert similarity_certificate(F)==('similarity',d)
    return 'reconstructed',(F,d,s)
def verify_induced(T,F,eps,samples):
    """('induced',None) when T(x) is a nonzero multiple of apply(F,eps,x) for every supplied sample, else ('not_induced',x) for the first failing one; nonzero samples of length n required. Stages 1 and 2 replayed on finite data."""
    F=matrix(F);eps=_eps(eps);n=len(F)
    for x in samples:
        x=vector(x)
        if len(x)!=n or not any(x):raise ValueError('nonzero samples of length n required')
        if not same_ray(apply(F,eps,x),_image(T,x,n)):return 'not_induced',x
    return 'induced',None
def tp_defect(T,probes):
    """('tp_preserved',None) when tp(T x,T y) == tp(x,y) for every pair of supplied nonzero probes, else ('zero_image',x) or ('tp_defect',(x,y,tp(x,y),tp(T x,T y))) for the first offending pair."""
    xs=[vector(x) for x in probes]
    if not all(any(x) for x in xs):raise ValueError('nonzero probes required')
    ys=[]
    for x in xs:
        y=_image(T,x,len(x))
        if not any(y):return 'zero_image',x
        ys.append(y)
    for a in range(len(xs)):
        for b in range(a+1,len(xs)):
            s,t=transition_probability(xs[a],xs[b]),transition_probability(ys[a],ys[b])
            if s!=t:return 'tp_defect',(xs[a],xs[b],s,t)
    return 'tp_preserved',None
def ray_scalar(x):
    """The deterministic nonzero ray factor c(x) = (1 + s mod 2) + ((s mod 3) - 1) i, s = sum_k (k+1)(num re x_k + 2 num im x_k)."""
    x=vector(x);s=sum((k+1)*(a.re.numerator+2*a.im.numerator) for k,a in enumerate(x));return G(1+s%2,s%3-1)
def induced_ray_map(F,eps):
    """T(x) = ray_scalar(x) * F * twist(eps,x): tp-preserving when F is a similarity, with the ray freedom exercised."""
    F=matrix(F);eps=_eps(eps)
    def T(x):return [ray_scalar(x)*a for a in apply(F,eps,x)]
    return T
# ---------------------------------------------------------------- unitary normalisation: norms from Q(i)
def _factor(N):
    """Trial-division factorisation [(p,e),...] of a positive integer, primes increasing."""
    out=[];p=2
    while p*p<=N:
        e=0
        while N%p==0:N//=p;e+=1
        if e:out.append((p,e))
        p+=1 if p==2 else 2
    if N>1:out.append((N,1))
    return out
def _fermat(p):
    """(x,y) with x^2 + y^2 == p for p = 2 or a prime p = 1 (mod 4), by bounded search over x <= isqrt(p)."""
    for x in range(1,isqrt(p)+1):
        y=isqrt(p-x*x)
        if y*y==p-x*x:return x,y
    raise ValueError('no two-squares representation')
def _bf(u,v):
    """Brahmagupta-Fibonacci: (a^2+b^2)(c^2+d^2) = (ac-bd)^2 + (ad+bc)^2."""
    (a,b),(c,d)=u,v;return a*c-b*d,a*d+b*c
def sum_of_two_rational_squares(d):
    """('representable',(a,b)) with rationals a, b >= 0 and a^2 + b^2 == d, or ('not_representable',p) with p the least prime = 3 (mod 4) dividing num*den to an odd power; positive rational d required.

    d = num/den in lowest terms equals (A/den)^2 + (B/den)^2 with A^2 + B^2 = num*den, composed by Brahmagupta-Fibonacci
    from the prime factors: 2 = 1 + 1, p = 1 (mod 4) by Fermat (bounded search), p^2 = p^2 + 0 for p = 3 (mod 4)."""
    d=_q(d)
    if d<=0:raise ValueError('positive rational required')
    fs=_factor(d.numerator*d.denominator)
    for p,e in fs:
        if p%4==3 and e%2:return 'not_representable',p
    w=(1,0)
    for p,e in fs:
        base,times=((p,0),e//2) if p%4==3 else (_fermat(p),e)
        for _ in range(times):w=_bf(w,base)
    a,b=Q(abs(w[0]),d.denominator),Q(abs(w[1]),d.denominator);assert a*a+b*b==d
    return 'representable',(a,b)
def unitary_normalisation(F):
    """('unitary',(c,U)) with |c|^2 == d, U = F/c and U^H U == I; ('not_a_norm',(d,p)) when the scale d is not a sum of two rational squares (p the obstructing prime); or ('not_similarity',witness)."""
    F=matrix(F);verdict,d=similarity_certificate(F)
    if verdict!='similarity':return verdict,d
    verdict,w=sum_of_two_rational_squares(d)
    if verdict!='representable':return 'not_a_norm',(d,w)
    c=G(*w);U=[[a/c for a in r] for r in F];assert gram(U)==identity(len(F))
    return 'unitary',(c,U)
