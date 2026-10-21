"""Exact effect-additive valuations on Gaussian-rational Hermitian matrices; the Born trace form over Q(i).

The Hermitian twin of born_effect_valuation.py, replayed in exact arithmetic over the Gaussian rationals
for the carrier of dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T224000Z_gaussian_hermitian_carrier:
Hermitian PSD certification by a Gram (LDL^*) decomposition with conjugate pivots and exact negative
witnesses, effects 0 <= E <= 1 in the Hermitian-form preorder, the order-unit bound, the midpoint
extension of a real-valued valuation to a real-linear functional, and its representing matrix rho with
re(trace(rho E)) = v(E), recovered one matrix unit at a time along the directions 1 and i.
The *-algebra and its order are supplied; only the form of the valuation is derived.
AuthorityEffect: None.
"""
from fractions import Fraction as Q
from math import ceil
def _q(x):
    if type(x) not in (int,Q):raise ValueError('exact integer or Fraction entries required')
    return Q(x)
class G:
    """Gaussian rational re+im*i with exact Fraction parts; built from an int, Fraction, G or (re,im) pair."""
    __slots__=('re','im')
    def __init__(self,re=0,im=0):
        if isinstance(re,(G,tuple)):
            if _q(im)!=0:raise ValueError('a single Gaussian rational argument takes no imaginary part')
            re,im=(re.re,re.im) if isinstance(re,G) else re
        self.re=_q(re);self.im=_q(im)
    def conj(self):return G(self.re,-self.im)
    def norm_sq(self):return self.re*self.re+self.im*self.im
    def __add__(self,o):o=_g(o);return G(self.re+o.re,self.im+o.im)
    __radd__=__add__
    def __sub__(self,o):o=_g(o);return G(self.re-o.re,self.im-o.im)
    def __rsub__(self,o):return _g(o)-self
    def __mul__(self,o):o=_g(o);return G(self.re*o.re-self.im*o.im,self.re*o.im+self.im*o.re)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=_g(o);n=o.norm_sq()
        if n==0:raise ZeroDivisionError('division by zero Gaussian rational')
        return self*o.conj()*(1/n)
    def __rtruediv__(self,o):return _g(o)/self
    def __neg__(self):return G(-self.re,-self.im)
    def __eq__(self,o):
        if type(o) in (int,Q):o=G(o)
        return isinstance(o,G) and self.re==o.re and self.im==o.im
    def __hash__(self):return hash((self.re,self.im))
    def __bool__(self):return self.re!=0 or self.im!=0
    def __repr__(self):
        if self.im==0:return str(self.re)
        if self.re==0:return f'{self.im}i'
        return f'{self.re}{"+" if self.im>0 else "-"}{abs(self.im)}i'
def _g(x):return x if isinstance(x,G) else G(x)
I=G(0,1)
def matrix(rows):
    m=[[G(x) for x in r] for r in rows];n=len(m)
    if n==0 or any(len(r)!=n for r in m):raise ValueError('nonempty square matrix required')
    return m
def vector(xs):
    v=[G(x) for x in xs]
    if not v:raise ValueError('nonempty vector required')
    return v
def _same_shape(A,B):
    if len(A)!=len(B) or any(len(a)!=len(b) for a,b in zip(A,B)):raise ValueError('equal matrix shapes required')
def _same_length(x,y):
    if len(x)!=len(y):raise ValueError('equal vector lengths required')
def identity(n):return [[G(int(i==j)) for j in range(n)] for i in range(n)]
def single(n,i,j,c=1):
    if not (0<=i<n and 0<=j<n):raise ValueError('index out of range')
    c=G(c);return [[c if (r==i and k==j) else G(0) for k in range(n)] for r in range(n)]
def add(A,B):_same_shape(A,B);return [[_g(a)+b for a,b in zip(ra,rb)] for ra,rb in zip(A,B)]
def sub(A,B):_same_shape(A,B);return [[_g(a)-b for a,b in zip(ra,rb)] for ra,rb in zip(A,B)]
def scale(c,A):c=G(c);return [[c*a for a in r] for r in A]
def adjoint(A):return [[_g(a).conj() for a in col] for col in zip(*A)]
def mat_vec(A,x):
    if any(len(r)!=len(x) for r in A):raise ValueError('vector length must equal the matrix width')
    return [sum((_g(a)*b for a,b in zip(r,x)),G(0)) for r in A]
def inner(x,y):_same_length(x,y);return sum((_g(a).conj()*b for a,b in zip(x,y)),G(0))
def outer(x,y):return [[_g(a)*_g(b).conj() for b in y] for a in x]
def trace(A):return sum((_g(A[i][i]) for i in range(len(A))),G(0))
def trace_mul(A,B):_same_shape(A,B);n=len(A);return sum((_g(A[i][j])*B[j][i] for i in range(n) for j in range(n)),G(0))
def hermitian_form(A,x):return inner(x,mat_vec(A,x))
def re_hermitian_form(A,x):return hermitian_form(A,x).re
def is_hermitian(A):A=matrix(A);return A==adjoint(A)
def hermitian_part(A):return scale(Q(1,2),add(A,adjoint(A)))
def _unit(n,p):return [G(int(i==p)) for i in range(n)]
def _lift_witness(terms,y):
    x=y[:]
    for k,_,w in reversed(terms):x[k]=-sum((w[i].conj()*x[i] for i in range(k+1,len(x))),G(0))
    return x
def gram_decomposition(E):
    """('psd',[(d_k,w_k),...]) with E == sum d_k w_k w_k^* and d_k >= 0 rational, or ('not_psd',x) with x^* E x < 0; Hermitian E required.

    Zero pivot with off-diagonal c=E_ja: the witness e_a+s e_j has form 2re(conj(c)s)+|s|^2 m, m=E_jj, so s=-tc gives |c|^2 t(tm-2)<0 for t=1 (m<=0) or t=1/m (m>0).
    """
    E=matrix(E)
    if not is_hermitian(E):raise ValueError('hermitian matrix required')
    n=len(E);M=[r[:] for r in E];terms=[]
    for p in range(n):
        piv=M[p][p].re
        if piv<0:return 'not_psd',_lift_witness(terms,_unit(n,p))
        if piv==0:
            for j in range(p+1,n):
                c=M[j][p]
                if c!=0:
                    m=M[j][j].re;y=_unit(n,p);y[j]=-c*(Q(1) if m<=0 else 1/m)
                    return 'not_psd',_lift_witness(terms,y)
            continue
        w=[M[i][p]/piv for i in range(n)];terms.append((p,piv,w));M=sub(M,scale(piv,outer(w,w)))
    return 'psd',[(d,w) for _,d,w in terms]
def verify_gram(E,terms):
    E=matrix(E);n=len(E);S=[[G(0)]*n for _ in range(n)]
    for d,w in terms:
        w=vector(w);_same_length(w,E)
        if _q(d)<0:return False
        S=add(S,scale(_q(d),outer(w,w)))
    return S==E
def psd_certificate(E):
    E=matrix(E);H=hermitian_part(E);kind,data=gram_decomposition(H)
    if kind=='psd':return {'status':'psd','terms':[(str(d),list(map(str,w))) for d,w in data],'reconstructs':verify_gram(H,data)}
    return {'status':'not_psd','witness':list(map(str,data)),'value':str(re_hermitian_form(E,data))}
def is_psd(E):return gram_decomposition(hermitian_part(matrix(E)))[0]=='psd'
def is_effect(E):E=matrix(E);return is_psd(E) and is_psd(sub(identity(len(E)),E))
def effect_certificate(E):
    E=matrix(E);lower=psd_certificate(E);upper=psd_certificate(sub(identity(len(E)),E))
    return {'lower':lower,'upper':upper,'is_effect':lower['status']=='psd' and upper['status']=='psd'}
def rank_one_effect(x):
    x=vector(x);nrm=inner(x,x).re
    if nrm==0:raise ValueError('nonzero vector required')
    return scale(1/nrm,outer(x,x))
def order_unit_bound(A):return ceil(sum(abs(a.re)+abs(a.im) for r in matrix(A) for a in r))
def bounded_by(A,t,x):A=matrix(A);t=_q(t);x=vector(x);q=re_hermitian_form(A,x);s=t*inner(x,x).re;return -s<=q<=s
def midpoint(A,t):
    A=matrix(A);t=_q(t)
    if t<=0:raise ValueError('positive bound required')
    return scale(1/(2*t),add(A,scale(t,identity(len(A)))))
def extend(valuation,A,t=None):
    A=matrix(A);t=Q(order_unit_bound(A)+1) if t is None else _q(t)
    return 2*t*_q(valuation(midpoint(A,t)))-t
def extension_consistency(valuation,A,bounds):
    values=[extend(valuation,A,t) for t in bounds]
    return {'bounds':list(map(str,bounds)),'values':list(map(str,values)),'consistent':len(set(values))==1}
def representing_matrix(valuation,n):
    """rho with rho[j][i] = L(e_ij) - i L(i e_ij), L the extension; then L(A) = re(trace_mul(rho,A)) for every A."""
    return [[extend(valuation,single(n,i,j,1))-I*extend(valuation,single(n,i,j,I)) for i in range(n)] for j in range(n)]
def born_valuation(rho):rho=matrix(rho);return lambda E:trace_mul(rho,matrix(E)).re
def _effects_of_dimension(n,effects):
    effects=[matrix(E) for E in effects]
    if any(len(E)!=n for E in effects):raise ValueError('effects of dimension n required')
    return effects
def valuation_axioms(valuation,n,effects,pairs):
    effects=_effects_of_dimension(n,effects);pairs=[tuple(_effects_of_dimension(n,[E,F])) for E,F in pairs]
    if not all(is_effect(E) for E in effects) or not all(is_effect(E) and is_effect(F) and is_effect(add(E,F)) for E,F in pairs):raise ValueError('effects and effect pairs with effect sums required')
    return {'unit':_q(valuation(identity(n)))==1,'nonneg':all(_q(valuation(E))>=0 for E in effects),'additive':all(_q(valuation(add(E,F)))==_q(valuation(E))+_q(valuation(F)) for E,F in pairs)}
def born_certificate(valuation,n,effects=()):
    effects=_effects_of_dimension(n,effects)
    if not all(is_effect(E) for E in effects):raise ValueError('effects required')
    rho=representing_matrix(valuation,n);cert=psd_certificate(rho);tr=trace(rho)
    return {'rho':[list(map(str,r)) for r in rho],'hermitian':is_hermitian(rho),'trace':str(tr),'trace_real':tr.im==0,'psd':cert['status']=='psd','psd_certificate':cert,'agrees_on_effects':all(trace_mul(rho,E).re==_q(valuation(E)) for E in effects),'effects_checked':len(effects)}
def square_valuation(E):E=matrix(E);return E[0][0].re**2
def bad_linear_valuation(E):
    E=matrix(E)
    if len(E)!=3:raise ValueError('three-dimensional control')
    return 2*E[0][0].re-E[2][2].re
def imaginary_leak_valuation(E):
    """Unital and real-linear, but reads the skew-Hermitian direction i e_01: re(E_00)+im(E_01)."""
    E=matrix(E)
    if len(E)<2:raise ValueError('at least two-dimensional control')
    return E[0][0].re+E[0][1].im
