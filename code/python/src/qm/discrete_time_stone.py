"""Discrete time on the finite carrier: the Z-action k -> U^k of one rational rotation step, and the exact obstruction to a Q-parameter group through it.

Replays in exact rational arithmetic the Lean specification
dag/results/FQ-GAP-STONE-CONTINUOUS-TIME/runs/20261020T225000Z_discrete_time_spec/DiscreteTimeStoneSpec.lean
(namespace BornFable.DiscreteTime) for node FQ-GAP-STONE-CONTINUOUS-TIME. Specified there: the Q-parameter group
QParamGroup (U(0) = 1, U(s+t) = U(s)U(t)), the discrete evolution discreteEvolution u k = u^k with
discreteEvolution_add / discreteEvolution_zero / discreteEvolution_neg, its restriction U_int /
U_eq_discreteEvolution, the necessity U_inv_nat / roots_of_all_orders (U(1/m)^m = U(1)), and generator
non-uniqueness sq_root_neg / neg_ne_self_of_ne_zero / half_step_not_unique / matrix_half_step_not_unique.
Derived there: R345_orthogonal, R345_det, R345_pow_orthogonal, four_fifths_not_rat_square (via four_fifths_den
and nat_mul_self_ne_five), no_rational_half_step (every V with V V = R345 commutes with R345, hence
V = [[p,-r],[r,p]]; p^2 - r^2 = 3/5 and 2pr = 4/5 force p^2 = 4/5) and no_qparam_group_through_R345.
This module replays those statements exactly: rational rotations [[c,-s],[s,c]] with c^2 + s^2 = 1 and their
Z-orbit (negative powers by transpose), the half-angle criterion (a rational rotation has a rational rotation
square root iff (1+c)/2 is a rational square, and then exactly the pair +-V), the commutant form V = pI + rJ of
any square root of a 2x2 matrix with irreducible characteristic polynomial, the Pythagorean step
R345 = rotation(3/5,4/5) with no rational half-step (required square 4/5) although R345^2 has the half-steps
+-R345, the sign pair of every square root (no canonical generator), and the order of a rotation on a finite
window (rotation(0,1) has order 4; R345 never returns, consistent with the kernel-checked
fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction in lean4/DerivationDagQMClosure.lean
and the scalar U1PowerMapInjectivity.u345_infinite_order cited by the specification).
Continuous time and generator selection are not derived: a Q-parameter group with U(1) = R345 would need U(1/2),
a rational half-step, which does not exist. The general triviality of Q-parameter groups over Q(i) is the open
obligation recorded by the specification (unique factorisation in Z[i]). AuthorityEffect: None.
"""
from fractions import Fraction as Q
from math import isqrt
def _q(x):
    if type(x) not in (int,Q):raise ValueError('exact integer or Fraction entries required')
    return Q(x)
def _int(k,lo,what):
    if type(k) is not int or k<lo:raise ValueError(what)
    return k
def _strs(M):return [list(map(str,r)) for r in M]
def matrix2(rows):
    m=[[_q(x) for x in r] for r in rows]
    if len(m)!=2 or any(len(r)!=2 for r in m):raise ValueError('2x2 rational matrix required')
    return m
def identity():return [[Q(1),Q(0)],[Q(0),Q(1)]]
def zero():return [[Q(0),Q(0)],[Q(0),Q(0)]]
def mul(A,B):A=matrix2(A);B=matrix2(B);return [[A[i][0]*B[0][j]+A[i][1]*B[1][j] for j in range(2)] for i in range(2)]
def transpose(A):A=matrix2(A);return [[A[0][0],A[1][0]],[A[0][1],A[1][1]]]
def neg(A):return [[-x for x in r] for r in matrix2(A)]
def trace(A):A=matrix2(A);return A[0][0]+A[1][1]
def det(A):A=matrix2(A);return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def is_orthogonal(A):return mul(transpose(A),A)==identity()
def rotation(c,s):
    """[[c,-s],[s,c]] for a rational point (c,s) of the unit circle; any other (c,s) is refused."""
    c,s=_q(c),_q(s)
    if c*c+s*s!=1:raise ValueError('rational point of the unit circle required')
    return [[c,-s],[s,c]]
def rotation_point(R):
    """(c,s) with R == rotation(c,s); refuses every other matrix."""
    R=matrix2(R);c,s=R[0][0],R[1][0]
    if R!=[[c,-s],[s,c]] or c*c+s*s!=1:raise ValueError('rational rotation required')
    return c,s
R345=rotation(Q(3,5),Q(4,5))
def zpow(R,k):
    """R^k for an integer k; R^-1 = R^T, so a negative k needs an orthogonal R (refused otherwise). Lean: discreteEvolution, discreteEvolution_neg."""
    R=matrix2(R)
    if type(k) is not int:raise ValueError('integer exponent required')
    if k<0:
        if not is_orthogonal(R):raise ValueError('negative powers need an orthogonal matrix')
        R,k=transpose(R),-k
    P=identity()
    while k:
        if k&1:P=mul(P,R)
        R=mul(R,R);k>>=1
    return P
def discrete_evolution(R,kmax):
    """The exact Z-orbit U^k, -kmax <= k <= kmax, of one orthogonal step U = R: every power is orthogonal (U^k^T U^k = I), U^i U^j = U^(i+j) on the window, and U^-k = (U^k)^T. Lean: discreteEvolution_add, discreteEvolution_zero, discreteEvolution_neg, R345_pow_orthogonal."""
    R=matrix2(R);kmax=_int(kmax,0,'nonnegative integer bound required')
    if not is_orthogonal(R):raise ValueError('orthogonal step required')
    ks=list(range(-kmax,kmax+1));orbit={k:zpow(R,k) for k in ks}
    return {'kmax':kmax,'exponents':ks,'orbit':[_strs(orbit[k]) for k in ks],'all_orthogonal':all(is_orthogonal(U) for U in orbit.values()),'group_law':all(mul(orbit[i],orbit[j])==orbit[i+j] for i in ks for j in ks if -kmax<=i+j<=kmax),'inverse_is_transpose':all(orbit[-k]==transpose(orbit[k]) for k in ks)}
def rational_sqrt(x):
    """The nonnegative rational r with r^2 = x, or None (negative x included); decided by math.isqrt on the reduced numerator and denominator. Lean: four_fifths_not_rat_square via four_fifths_den and nat_mul_self_ne_five."""
    x=_q(x)
    if x<0:return None
    n,d=isqrt(x.numerator),isqrt(x.denominator)
    return Q(n,d) if n*n==x.numerator and d*d==x.denominator else None
def is_rational_square(x):return rational_sqrt(x) is not None
def half_step(c,s):
    """The rational rotations V with V^2 = rotation(c,s): None unless (1+c)/2 is a rational square p^2, and then exactly the pair +-rotation(p, s/(2p)) (with s/(2p) read as 1 when p = 0: rotation(-1,0) = rotation(0,+-1)^2). Lean: no_rational_half_step for R345."""
    c,s=rotation_point(rotation(c,s));p=rational_sqrt((1+c)/2)
    if p is None:return None
    r=s/(2*p) if p else Q(1)
    return [rotation(p,r),rotation(-p,-r)]
def has_rational_half_step(c,s):return half_step(c,s) is not None
def qparam_necessary_roots(R,m):
    """A Q-parameter group U with U(1) = R restricts to k -> R^k on Z and needs U(1/m) with U(1/m)^m = R. For a rational rotation R and m = 2^j this is decided exactly by iterating half_step on every branch: either the 2^j rational m-th roots (as circle points) or the depth and the rotation at which no rational square root exists. Lean: QParamGroup, U_eq_discreteEvolution, U_inv_nat, roots_of_all_orders."""
    c,s=rotation_point(R);m=_int(m,1,'power-of-two root order required')
    if m&(m-1):raise ValueError('power-of-two root order required')
    depth=m.bit_length()-1;level=[(c,s)]
    for j in range(1,depth+1):
        nxt=[]
        for a,b in level:
            hs=half_step(a,b)
            if hs is None:return {'m':m,'status':'obstructed','depth':j,'at':[str(a),str(b)],'required_square':str((1+a)/2),'roots':[]}
            nxt+=[rotation_point(V) for V in hs]
        level=nxt
    return {'m':m,'status':'roots','depth':depth,'roots':[[str(a),str(b)] for a,b in level]}
def irreducible_char_poly(R):
    """x^2 - tr(R) x + det(R) is irreducible over Q iff tr(R)^2 - 4 det(R) is not a rational square."""
    R=matrix2(R);return not is_rational_square(trace(R)**2-4*det(R))
def commutant_half_step_candidates(R):
    """Every V with V^2 = R commutes with R; when the characteristic polynomial of R is irreducible the commutant is Q[R] = span{I,J} with J = R - (tr R/2) I and J^2 = kappa I, kappa = (tr R)^2/4 - det R. For V = pI + rJ: V^2 = R <=> p^2 + kappa r^2 = tr R/2 and 2pr = 1 <=> p^2 = (tr R/2 +- sqrt(det R))/2 and r = 1/(2p). Returns the candidate values of p^2 and every rational square root V of R, each replayed as V V = R (for a rotation, p^2 = (1+c)/2: the half-angle criterion, independent of the rotation structure). Lean: the commutation step of no_rational_half_step (V R345 = R345 V forces V = [[p,-r],[r,p]])."""
    R=matrix2(R)
    if not irreducible_char_poly(R):raise ValueError('irreducible characteristic polynomial required')
    t=trace(R)/2;d=det(R);J=[[R[i][j]-(t if i==j else 0) for j in range(2)] for i in range(2)];kappa=t*t-d;rd=rational_sqrt(d)
    cands=[] if rd is None else sorted({(t+rd)/2,(t-rd)/2},reverse=True);roots=[]
    for ps in cands:
        p=rational_sqrt(ps)
        if p:
            for pp in (p,-p):
                r=1/(2*pp);roots.append([[pp*int(i==j)+r*J[i][j] for j in range(2)] for i in range(2)])
    roots=[V for V in roots if mul(V,V)==R]
    return {'half_trace':str(t),'det':str(d),'kappa':str(kappa),'J':_strs(J),'candidate_p_squares':list(map(str,cands)),'roots':[_strs(V) for V in roots]}
def no_rational_half_step_certificate(R):
    """For R = rotation(c,s): V = [[p,-r],[r,p]] (the commutant form) squares to R iff p^2 - r^2 = c and 2pr = s, which forces p^2 + r^2 = 1 and p^2 = (1+c)/2; the required square is reported with its exact decision. For R345 it is 4/5, not a rational square. Lean: no_rational_half_step, four_fifths_not_rat_square."""
    c,s=rotation_point(R);req=(1+c)/2;return {'required_square':str(req),'is_rational_square':is_rational_square(req)}
def square_root_pairs(V):
    """With U = V V: (-V)(-V) = U as well and -V != V whenever V != 0, so a square root of a step is never unique. Lean: sq_root_neg, neg_ne_self_of_ne_zero, half_step_not_unique, matrix_half_step_not_unique."""
    V=matrix2(V);U=mul(V,V);W=neg(V)
    return {'U':_strs(U),'V':_strs(V),'neg_V':_strs(W),'neg_squares_to_U':mul(W,W)==U,'distinct':W!=V,'V_nonzero':V!=zero()}
def rotation_order(c,s,max_k):
    """The least k in 1..max_k with rotation(c,s)^k = I, or None; rotation(0,1) has order 4 while R345 never returns on any finite window. Lean: U1PowerMapInjectivity.u345_infinite_order (cited by the specification); kernel: fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction."""
    R=rotation(c,s);max_k=_int(max_k,1,'positive integer bound required');P=identity()
    for k in range(1,max_k+1):
        P=mul(P,R)
        if P==identity():return k
    return None
def specification():
    """What node FQ-GAP-STONE-CONTINUOUS-TIME specifies, what this module derives, and what stays open; nothing here is a theorem about a continuum. Lean: QParamGroup, no_qparam_group_through_R345, and the open obligation in the module header."""
    return {'node':'FQ-GAP-STONE-CONTINUOUS-TIME','specified':'discrete evolution is the Z-action k -> U^k of one orthogonal step U on the finite carrier','continuity':'no topology on the finite carrier; the strongest finite notion is a Q-parameter group','generator_selection':'square roots of a step come in pairs ±V; no canonical generator','relationship':'a Q-parameter group restricts to the Z-action of its unit step and requires roots of every order; the Pythagorean rotation has no rational half-step, so no Q-parameter group of rational 2x2 matrices passes through it; continuous time needs a carrier extension (sqrt 5)','derived':'orbit orthogonality and the group law on every finite window; the half-angle criterion and its sign pair; the required square 4/5 for R345; the order of a rotation on a finite window','open':'the general triviality of Q-parameter groups over Q(i) is not proved (needs unique factorisation in Z[i])','authority_effect':'None'}
