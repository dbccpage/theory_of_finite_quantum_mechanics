# Five derivations: execution on 2026-10-15

**AuthorityEffect:** None.

Research objective: determine whether the maximum number of mutually unbiased
bases in complex dimension six is three. The starting checkout is main at
`470f2039beb4880a569bf63f7d9f3e75b36b5d7e` (PR #1064); work is on
`codex/mub6-next-five-derivations`. The targets are in the
[five-derivation design](../next_five_derivations_20261015.md).

This execution obtains the family transport and quartet reduction, a stronger
exact replay at the special point, a description of the entire phase base,
odd-exponent Laurent cancellation on the block family, and an explicit
three-basis witness. The global parameter exclusion and the identities for
arbitrary actual triples remain the mathematical steps needed for the upper
bound. Their premises have not been replaced by axioms.

| Target | Result of this execution | Remaining step |
|---|---|---|
| 1. Family and ray reduction | Exact transport identity; Lean quartet/ray-basis equivalence and pair obstruction | None for the stated reduction |
| 2. Explicit open exclusion region | 120 represented real rays; all 7,140 pairs excluded; exact nonsingular Jacobians; perturbation estimate below | Independent exhaustiveness replay and a certified parameter radius |
| 3. Full Szöllősi exclusion | Exact discriminants, radial base domain, and finite phase-root fibers | Common-ray incidence cover, including exceptional strata |
| 4. Identities on every actual triple | All odd balanced Laurent sums vanish on the block family; independent-permutation orientation lemma | Polynomial or real-radical witnesses on arbitrary triples |
| 5. Dimension-six maximum | Three explicit MUBs verified exactly; upper-bound dependencies identified | Results of 3 and 4, together with the cited classification and Fourier theorem |

## 1. Family transport and concrete rays

For unit phases a,b,c,d,e,f, put A=circ(a,b,c), B=circ(d,e,f), using
`circ(a,b,c)[i,j]=(a,b,c)[j-i mod 3]`, and

\[
H=\begin{pmatrix}A&B\\B^*&-A^*\end{pmatrix},\quad
L=\operatorname{diag}(\bar a I_3,dI_3),\quad
R=\operatorname{diag}(I_3,a\bar d I_3).
\]

Direct multiplication gives

\[
LHR=S(x,y,u,v),\qquad
(x,y,u,v)=(b/a,c/b,e/d,f/e),
\]

where S has the same block form with first rows (1,x,xy) and (1,u,uv).
Both diagonal actions have unit-modulus entries. Conversely every four-phase
matrix arises by taking (a,b,c,d,e,f)=(1,x,xy,1,u,uv). This calculation makes
no root choices, so repeated-root parameters and all orderings are retained.
The 36 entry identities are checked in `symbolic_receipt.json`.

The existing theorem
`MUB.MonomialTransport.hasRawQuartet_iff_of_monomialEquivalent` transports an
entire completion: the same left monomial action acts on each further basis,
and their right monomial actions can be independent. This supplies the
simultaneous-basis step, in addition to the identity for H alone.

For a raw Hadamard H, define

\[
\mathcal V(H)=\{z\in\mathbb T^6:z_0=1,
 |(H^*z)_j|^2=6\text{ for all }j\}.
\]

A unit-modulus column w is uniquely dephased as z=conj(w_0)w. This does not
change its inner-product magnitudes. Thus a quartet containing I and H/sqrt(6)
exists exactly when there are matrices U,V whose columns belong to V(H), with

\[
U^*U=V^*V=6I,\qquad |(U^*V)_{ij}|^2=6.
\]

[SzollosiCommonRays.lean](../../../../../lean4/SzollosiCommonRays.lean)
establishes this equivalence using the existing concrete `RawHadamard`, `RawMU`
and `HasRawQuartet` predicates. Its theorem
`no_quartet_of_no_unbiased_ray_pair` then derives the stronger sufficient
obstruction: no z,w in V(H) have |z*w|²=6. No finite-ray assumption is used.

For z on the torus, sum_j |(H*z)_j|²=36. Consequently the first five overlap
equations imply the sixth. At p0=(1,-1,1,i), `special_system_binding` independently
constructs S(p0), checks its Gram matrix, matches all ten saved real equations,
and verifies the polynomial identity

\[
\sum_{j=0}^5\bigl(|(S^*z)_j|^2-6\bigr)
 =6\sum_{k=1}^5(a_k^2+b_k^2-1).
\]

## 2. Exact special-point replay and local continuation

`replay_rur.py` reads the saved rational univariate representation (RUR).
Its checks are stronger than substitution alone:

1. The degree-192 eliminant is squarefree and its coordinate denominator is
   invertible modulo the eliminant.
2. Each of the ten original polynomials vanishes after substitution.
3. The separating-form identity holds with its actual sign convention,
   sum_i lambda_i x_i + lambda_last t=0, with lambda_last nonzero. Distinct
   eliminant roots therefore give distinct solution tuples.
4. Fresh PARI Sturm counts, exact rational sign-changing isolating intervals,
   and disjointness account for every real eliminant root. Numerical root hints
   propose intervals; exact checks accept them.
5. Coordinate interval endpoints are serialized as exact rational numbers.
   Denominator exclusion is checked before coordinate division.
6. Every pair of the 120 represented real rays is enclosed. All 7,140 distinct
   pairs have a nonzero residual |z*w|²-6. The smallest certified absolute
   residual is greater than 47/100. There are 600 candidate orthogonal pairs;
   candidate orthogonality is not needed for the exclusion result.
7. For each of the 50 irreducible factors having real roots, substitute the RUR
   into the square real Jacobian, compute its exact determinant modulo that
   factor, and check gcd(det,factor)=1. All 120 represented real solutions are
   nonsingular.

The receipt is [special_replay.json](special_replay.json). It contains input and
checker hashes, isolating intervals, pair bounds, and determinant remainders.
The exact determinant calculation supersedes an attempted interval determinant
calculation that returned indeterminate values for 80 rays. That attempt did
not establish singularity.

For completeness of the original system, an independent upper bound of 192
on its complex solution count would combine with items 1–3 to establish that
the RUR misses no solutions. The merged sample record reports rational
Singular dimension 192. This execution's bounded rational Gröbner runs have
not reproduced that count, so the new receipt explicitly concerns represented
solutions. The generic 504-root RUR was not regenerated within the bounded
runs; its two 84-ray branches have no fresh replay in this directory.

There is a concrete perturbation estimate. If z,w and z',w' are unit-modulus
vectors with first coordinate one and

\[
\max_i|z_i-z'_i|\leq\varepsilon,
\qquad\max_i|w_i-w'_i|\leq\varepsilon,
\]

then |z*w-z'*w'|≤10 epsilon, because only five coordinates vary. Since each
inner product has modulus at most six,

\[
\bigl||z^*w|^2-|z'^*w'|^2\bigr|\leq120\varepsilon.
\]

For epsilon=1/1000 and distinct reference rays, the certified residual remains
greater than 47/100-120/1000=7/20. If both reference rays are the same, their
reference residual is 36-6=30, so this case is excluded as well.

This gives an explicit sufficient localization target: every nearby common
ray must lie within 1/1000 of some ray in an exhaustive sample list. Once
exhaustiveness is established, compactness implies that such a parameter
neighborhood exists: otherwise a sequence of common rays outside these balls
has a convergent torus subsequence giving a missing ray at p0. Nonsingularity
also gives local analytic branches by the implicit-function theorem. Neither
argument by itself supplies a numerical parameter radius. A quantitative
inverse/Jacobian bound and a complement exclusion are still needed to finish
target 2.

## 3. The whole phase base and its boundary

Write alpha=s+it=x+y+(xy)^(-1). The three phases x,y,(xy)^(-1) are roots of

\[
f_\alpha(z)=z^3-\alpha z^2+\bar\alpha z-1.
\]

Its discriminant, checked symbolically, is

\[
\Delta_+(s,t)=(s^2+t^2)^2+18(s^2+t^2)-27
 -8s(s^2-3t^2),\qquad
\Delta_-(s,t)=\Delta_+(-s,-t).
\]

All roots of f_alpha are on the unit circle exactly when Delta_+≤0. Here is
the sign argument, including repeated roots. The roots are invariant under
z→1/conj(z); the constant term is nonzero. An odd multiset invariant under
this involution has a unit root. If the other two roots are off the circle,
they can be written r exp(i theta), r^(-1) exp(i theta), r>0 and r≠1; the
third root is exp(-2i theta). Their discriminant is

\[
(r-r^{-1})^2(r+r^{-1}-2\cos(3\theta))^2>0.
\]

If all three roots are exp(i theta_j), the discriminant is
-64 product_{i<j} sin²((theta_i-theta_j)/2), since their product is one.
It is nonpositive, including coincidences. This establishes both directions.

The phase base for the two blocks is therefore exactly

\[
\mathcal A=\{(s,t):\Delta_+(s,t)\leq0,\ \Delta_-(s,t)\leq0\}.
\]

Equivalently, in polar coordinates,

\[
r^4+8|\cos3\theta|r^3+18r^2-27\leq0.
\]

For fixed theta the left side is strictly increasing for r>0. Thus A is
star-shaped, with a unique boundary radius in each direction. It contains
the closed unit disk and is contained in the disk of radius
sqrt(-9+6sqrt(3)). The two discriminant curves meet where

\[
s(s^2-3t^2)=0,\qquad s^2+t^2=-9+6\sqrt3.
\]

There are six such points. Each alpha in A gives at most six ordered pairs
(x,y) and six ordered pairs (u,v), by ordering the roots of f_alpha and
f_{-alpha}. These at most 36 lifts cover the four-phase domain, with fewer
distinct lifts at repeated roots. No branch is selected or discarded.

This is a description of the entire base and its phase-root branching.
It is not yet the discriminant of the common-ray equations, nor a certificate
cover of their unbiased-pair or quartet incidence set. Those additional
equations can develop exceptional strata inside A. A global cover must
discharge them too; the phase boundary cannot stand in for that computation.

## 4. Laurent cancellation and orientation

For a balanced sign vector epsilon in {−1,1}^6, define

\[
g_H(n\varepsilon)=\sum_{c=0}^5\prod_{r=0}^5H_{rc}^{n\varepsilon_r}.
\]

For the arbitrary six-phase block matrix in section 1, this expression is
zero for **every odd integer n**, even without the compatibility equation
that makes H Hadamard. The first three column terms are positive Laurent
monomials. Each of the last three has sign (−1)^(epsilon_3+epsilon_4+epsilon_5)
=−1. For each of the 20 balanced masks, the exponent vectors of the first
three columns are a permutation of those of the last three. Hence they
cancel in three pairs. Multiplying the exponent vectors by any odd n
preserves equality of the exponents and the opposite signs.

`symbolic_receipt.json` records all 20 permutations against the actual block
matrix. The independently written integer exponent formulas in
[SzollosiLaurentPairing.lean](../../../../../lean4/SzollosiLaurentPairing.lean)
check these pairings and the odd sign in the Lean kernel. This module verifies
the finite exponent calculation; the passage from signed monomials to the
complex Laurent identity is the argument just given.

For the arbitrary-triple problem there is also a symmetry reduction. Suppose
the representative identities hold on every ordered actual MUB triple, for
gamma1=(1,1,1,−1,−1,−1) and gamma2=3 gamma1:

\[
g_H(\gamma_1)=0,\qquad g_H(\gamma_2)g_{H^*}(\gamma_2)=0.
\]

Independently permuting the first and second bases independently permutes the
rows and columns of H. Column permutation leaves g_H unchanged and becomes
row permutation in H*. Consequently the second identity gives
g_H(mu)g_{H*}(nu)=0 for every independent pair of balanced cubic masks mu,nu.
If any first factor is nonzero, every second factor is zero; otherwise every
first factor is zero. The choice of side is therefore uniform across all
masks. `uniform_orientation` formalizes this logical step. Reversing the
first two bases supplies the linear identity for H* as well.

Diagonal phases also preserve vanishing: column phases contribute the power
sum_r gamma_r=0, while row phases multiply the sum by the same nonzero scalar.
Thus the identities can be used after monomial dephasing once they have been
established on actual triples.

The missing algebraic task can be stated without an auxiliary sqrt(6): let
H,K be arbitrary raw 6×6 matrices. Impose their 72 entry circle equations,
the real and imaginary parts of their 30 complex off-diagonal column-Gram
equations (60 real equations), and the 36 equations |(H*K)ij|²=6.
These 168 equations in 144 real coordinates describe actual triples
(I,H/sqrt(6),K/sqrt(6)); diagonal Gram equations follow from the circles.
The four real target polynomials are the real and imaginary parts of
g_H(gamma1) and g_H(gamma2)g_H*(gamma2), of degree at most 6 and 36.
No ideal-membership or real-radical witnesses for these four targets were
obtained here. The block-family cancellation does not supply those witnesses.

## 5. Lower bound and upper-bound assembly

Let omega=(-1+i sqrt(3))/2 and F[j,k]=omega^(jk)/sqrt(3). Take

\[
Q_0=I_2,\quad Q_1=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},
\quad Q_2=\frac1{\sqrt2}\begin{pmatrix}1&1\\i&-i\end{pmatrix},
\]

and R0=I3, R1=F, R2=diag(1,omega,omega)F. The three bases are Qk⊗Rk.
`verify_three_bases` checks all 108 Gram entries and 108 squared cross-Gram
entries in exact algebraic arithmetic. The former equal I6; the latter
equal 1/6. Thus three MUBs exist in dimension six.

For the upper bound, the uniform orientation in section 4 is the input to
the matrix argument in Matolcsi et al., Proposition 4.2. Their Conjecture 2
and the exclusion of quartets containing the Szöllősi family (Conjecture 3)
together imply that no quartet exists, using the Fourier-family exclusion.
The intended assembly is: arbitrary quartet → an oriented transition in a
classified family → Fourier or Szöllősi contradiction → at most three bases.
Sections 3 and 4 have not discharged the two global premises, so this chain
does not yet produce the requested upper bound.

Primary references checked for this route:

- [Szöllősi, arXiv:0811.3930v2](https://arxiv.org/abs/0811.3930v2), block construction and phase cubics.
- [Matolcsi et al., 2026, Proposition 4.2](https://link.springer.com/article/10.1007/s10801-026-01506-x), Conjectures 2 and 3 and the classification route.
- [Jaming et al., arXiv:0902.0882v2](https://arxiv.org/abs/0902.0882v2), full Fourier-family nonextension theorem.

## Reproduction and validation

Use Python 3.12 with SymPy 1.14.0, python-flint 0.9.0, and PARI/GP 2.17.2.
From this directory, with `gp` on PATH:

```sh
python verify_symbolic.py --output symbolic_receipt.json
python -m unittest test_symbolic test_rur
python replay_rur.py \
  --system ../szollosi_vectors/special_1_m1_1_i/special.ms \
  --param ../szollosi_vectors/special_1_m1_1_i/special.par \
  --approx ../szollosi_vectors/special_1_m1_1_i/special_approx.txt \
  --gp gp --check-jacobians --output special_replay.json
```

The mutation controls reject wrong monomial signs, exponents, non-bijective
pairings, corrupted basis entries, repeated bases, inconsistent separating
forms, repeated eliminants, missing coordinates and vanishing denominators.
The bound-serialization control checks enclosure of the non-dyadic rational 1/3.
The Jacobian controls accept simple roots and reject a singular root. All 14
focused tests passed, as did the scoped Ruff F401/F841/I check.

From `lean4/research_programs/mub6`, use its pinned Lean 4.33.1:

```sh
lake --no-cache build SzollosiCommonRays SzollosiLaurentPairing
```

The scoped build passed. Both quartet endpoints and all four Laurent/orientation
endpoints were inspected with `#print axioms`; their dependencies are subsets
of `[propext, Classical.choice, Quot.sound]`, with no `sorryAx` or custom axiom.
The finite pairing theorem uses `decide`, not native evaluation as a new axiom.
The full MUB package was not rebuilt.

The generic msolve 0.7.5 runs timed out at 900 seconds (`-L 1 -t 4`) and 600
seconds (default lifting, `-t 2`), with empty output parametrization files.
The rational Singular 4.4.1 generic `modStd` run timed out at 900 seconds;
the special-point `modStd` run with its arithmetic modules configured timed
out at 600 seconds. These timeouts establish no root-count conclusion.
An additional special-point rational `slimgb` attempt timed out at 240 seconds.
Logs and temporary tool installations are under `/workspace/scratch/` and
are not part of the research receipt. The original user changes are preserved.
