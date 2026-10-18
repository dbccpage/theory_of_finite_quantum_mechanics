# Five derivations toward MUB(6) = 3

**AuthorityEffect:** None.

**Research objective:** derive that the maximum number of mutually unbiased
bases in complex dimension six is exactly three. This design starts after the
sample computations merged in PR #1064, at repository commit
`470f2039beb4880a569bf63f7d9f3e75b36b5d7e`. It turns the supplied
2026-10-15 next-derivation report into five mathematical work packages.
Statements labelled **target** are the conclusions each package must establish.

The main route is to exclude Szöllősi-family quartets, establish the Laurent
identity on arbitrary actual triples, and combine these with Fourier-family
exclusion and the three-basis construction. The central improvement over the
attachment is to test the stronger absence of an unbiased pair of common rays
first, using the two-basis obstruction wherever that stronger property fails.

| Derivation | Mathematical output | Dependencies | First decisive deliverable |
|---|---|---|---|
| 1 | Exact family transport and quartet-to-ray equivalence | Existing matrix identities | A proof preserving every parameter branch and every candidate basis |
| 2 | An explicit parameter neighbourhood with no unbiased common-ray pair | 1 and the saved sample systems | A positive rational neighbourhood radius and a replayable exclusion certificate |
| 3 | No quartet anywhere in the Szöllősi family | 1; methods and initial cells from 2 | A complete parameter cover with every cell and exceptional stratum discharged |
| 4 | Laurent identities on every actual MUB triple | Actual triple equations; independent of 2 and 3 | Exact identity or real-radical witnesses for the representative polynomial targets |
| 5 | No quartet in dimension six and an explicit three-basis construction | 3, 4, Fourier exclusion and equivalence transport | A theorem whose conclusion is N(6) = 3 |

Derivations 3 and 4 are the two major mathematical challenges. Their completion
times cannot be inferred from the runtimes of the sample computations. Start the
statement and symmetry work for 4 after 1; it need not wait for 3.

## Starting evidence

The [merged computation record](szollosi_vectors/README.md) and its saved graph
files report the following. These are starting inputs to replay, rather than
assumed generic counts.

| Sample | Complex solution count | Real rays | Candidate orthogonal pairs | Candidate unbiased pairs | Candidate six-cliques |
|---|---:|---:|---:|---:|---:|
| (1, -1, 1, i) | 192 | 120 | 600 | 0 | 10 |
| Algebraic sample, first matrix branch | 504 across both branches | 84 | 132 | 0 | 1 |
| Algebraic sample, second matrix branch | Included in the same 504 | 84 | 132 | 0 | 1 |

The special sample has an independent rational Singular dimension computation.
For the algebraic sample, the record relies on msolve's 504 count, with agreement
modulo two primes; the independent rational Singular run did not finish. The
saved substitution checks establish that the represented solutions solve the
equations. Completeness requires the additional converse/count argument in 2.
The earlier numerical searches finding 60 rays do not establish completeness
there or a partition into 60-ray and 84-ray regions.

The exact candidate cliques were checked as orthonormal in the recorded runs.
For exclusion, the zero count of candidate unbiased pairs is already sufficient
once the ray enumeration and all interval enclosures are complete.

## Derivation 1 — Family identification and the common-ray reduction

**Target.** Identify the full source family with the four-phase construction,
preserve quartet existence under that identification, and derive an exact ray
system and its quartet semantics.

Let

\[
D=\{(x,y,u,v)\in\mathbb T^4:
\phi(x,y)+\phi(u,v)=0\},\qquad
\phi(x,y)=x+y+(xy)^{-1}.
\]

Write S(p) for the raw block matrix with circulant first rows (1,x,xy) and
(1,u,uv), so \(S(p)^*S(p)=6I\), where * denotes the adjoint. The normalized
basis matrix is S(p)/sqrt(6).

**Family bridge.** Start with the six-phase source blocks having first rows
(a,b,c) and (d,e,f). The block diagonal unitary matrices

\[
L=\operatorname{diag}(\bar a I_3,dI_3),\qquad
R=\operatorname{diag}(I_3,a\bar d I_3)
\]

send the source matrix to S(p), with

\[
x=b/a,\quad y=c/b,\quad u=e/d,\quad v=f/e.
\]

Check this identity entrywise and derive the parameter constraint from the
Gram equations. Apply the left unitary to every basis in a candidate quartet;
right phases and permutations only change basis representatives. Carry all
root orderings over the deltoid parameter and repeated-root boundary values.
Do not identify a matrix with its transpose without a proved transport:
adjoints arise by exchanging the first two bases, and simultaneous complex
conjugation preserves squared overlaps. These operations also handle transpose
representatives when needed.

The source construction and its transpose branches are specified in
[Szöllősi, equations (6)–(14) and Theorem 2.2](https://arxiv.org/pdf/0811.3930v2).
Reuse the existing
[SzollosiTwoCirculant.lean](../../../../../lean4/research_programs/mub6/SzollosiTwoCirculant.lean)
identities, especially `rawSix_gram`, `phaseRow_surjective`,
`parameter_equations_iff` and `parameter_covers_intersection`.

**Ray bridge.** Use raw vectors z = (1,z1,...,z5), with every coordinate on the
unit circle. Define

\[
Z_p=\{z\in\mathbb T^6:z_0=1,\ e_k(p,z)=0\ (k=0,\ldots,4)\},
\qquad e_k(p,z)=\left|\sum_i\overline{S(p)_{ik}}z_i\right|^2-6.
\]

The sixth equation follows because the sum of all six squared overlaps is 36.
Every common unbiased ray has exactly one representative z/sqrt(6) with z0=1.
In Cartesian coordinates the fixed-matrix system has ten real variables and
ten equations: five circle equations and five overlap equations. The equivalent
Laurent formulation has five phase variables; denominator clearing must retain
the nonzero-coordinate conditions.

For two raw rays define

\[
o(z,w)=z^*w,\qquad q(z,w)=|z^*w|^2-6.
\]

A quartet containing (I,S(p)/sqrt(6)) exists if and only if Zp contains two
six-element sets, each pairwise orthogonal, with q=0 on all 36 cross pairs.
This statement remains valid when Zp is infinite. Consequently, absence of
even one pair z,w with q=0 excludes a quartet. A surviving pair alone is not a
quartet: it still needs completion to those two bases.

**Deliverable and acceptance.** Add matrix-level transport and ray-equivalence
lemmas, proposed module `SzollosiCommonRays.lean`, with both directions checked.
The lower-dimensional formulation must admit all common rays, not just columns
of the known constructed third basis. Replay the three saved matrix samples as
normalization checks.

## Derivation 2 — From the sample solutions to an open exclusion region

**Target.** For at least one of the algebraic matrix branches p*, produce an
explicit rational radius delta > 0 such that

\[
p\in D,\quad\|p-p_*\|_\infty\le\delta
\quad\Longrightarrow\quad
\forall z,w\in Z_p,\ q(z,w)\ne0.
\]

The norm here is on the eight real parameter coordinates. Treat the two
algebraic matrix branches separately. Extend to the special sample using
singular methods if its relevant Jacobian is degenerate.

**First discharge completeness at the sample.** Reconstruct the rational
univariate representation and supply an exact finite quotient-dimension bound,
using a rational Groebner basis with checked reduction witnesses or a verified
border-basis certificate. Check the separating parameter identity as well as
equation substitution, squarefreeness and denominator invertibility. A
squarefree eliminant alone does not establish that different parameter roots
give different solution tuples. Match the dimension bound with that many
distinct represented solutions.

Use rational isolating endpoints, exact Sturm counts and outward-rounded
coordinate intervals. Identify the two matrix branches by an algebraic
polynomial and isolating interval. The current
[certgraph.py](szollosi_vectors/scripts/certgraph.py) uses rounded floats to
label branches; replace that identification in the proof-producing replay.
Check serialization enclosure as well: the current
[certroots.py](szollosi_vectors/scripts/certroots.py) passes decimal midpoint
and radius strings between stages. Exact rational or dyadic endpoints make
the containment obligation explicit.

**Then derive stability.** The common-ray pair incidence is closed inside the
compact space D times two phase tori. Its projection to D is closed. Therefore
complete pair exclusion at p* already implies some relative neighbourhood of
p* is pair-free, even without a simplicity assumption. The new computational
work is to produce a radius and finite evidence for it.

On a regular sample, use a parameter-uniform interval implicit-function or
Krawczyk argument on the ray boxes, plus a complete exclusion of the rest of
the phase torus. Bound |q| away from zero for every pair of possible ray boxes.
Include two rays in the same box; subdivision or a direct overlap bound must
exclude this case as well. A singular sample can instead use elimination or
a direct interval cover of the pair incidence, without assuming smooth root
continuation.

**Deliverable and acceptance.** A certificate records the exact center branch,
delta, root/exclusion boxes, coverage proof and positive rational separation
bounds. A checker verifies all of these from the defining equations. The first
milestone is one explicit nonempty region, not another isolated sample count.
If regular continuation fails, retain the identified singular locus as input
to 3 rather than dropping it.

## Derivation 3 — Complete family exclusion

**Target.** Establish, for every p in D, absence of two mutually unbiased
orthonormal six-tuples in Zp. Transport through 1 to discharge the full
Szöllősi-family nonextension statement.

**Parameter decomposition.** Work over the two real deltoid coordinates
alpha = s+it, retaining the finite choices of phase roots, or use an equivalent
certified atlas on D. For every relevant algebraic component, establish
generic finiteness and its degree before using a finite ray model. The sample
degree 504, which includes two matrix branches, is not a degree theorem for
the total family. Irreducibility is not a prerequisite: decompose the incidence
and keep every component that has real admissible points.

Build the critical parameter locus from root collisions, failures of finite
projection, leading coefficients/denominators and changes in orthogonality or
unbiasedness relations. Include roots at infinity in the algebraic projection
analysis, or eliminate that issue with a complete compact real formulation.
An edge relation that holds identically on a component must be distinguished
from one that holds only on a smaller locus. Numerical continuation at one
sample does not make this distinction.

**Cell exclusion.** Use exact projection and real sign determination to
construct cells, with rational interval subdivision as the practical fallback.
On each cell retain all possible rays and all possible orthogonality and
unbiasedness edges. Then apply the cheapest sufficient obstruction:

1. No possible unbiased ray pair.
2. Fewer than two possible orthonormal six-cliques.
3. No pair of candidate six-cliques with all 36 possible unbiased cross edges.

These graphs may overestimate the relations; an exclusion in the larger graph
remains valid. An unresolved edge stays present. Passing to one sample per
cell requires a proof that the relevant incidence and relation data are
constant there. Otherwise certify the bounds uniformly over the cell.

Treat boundary arcs, cusps, chart seams and intersections explicitly. A
positive-dimensional ray fibre needs continuous phase boxes or a separate
symbolic argument; finite vertex enumeration is insufficient there. If boxes
replace individual rays, retain possible multiple occupancy until
orthogonality excludes it. Do not assume the exceptional set is a collection
of curves until its dimension has been established. Likewise, unbiased pairs
could exist on regions of positive dimension: that defeats the stronger pair
test, but leaves the two-basis obstruction available.

**Deliverable and acceptance.** A finite cover whose union is all of D,
including every parameter branch and stratum, with a checked contradiction
for the actual quartet conditions on every part. Regions from 2 seed this
cover. A surviving cell is refined or receives a new local lemma; no cell is
declared excluded from the sample behavior of a neighbouring region.

Use [Jaming et al.'s Fourier-family exclusion](https://arxiv.org/abs/0902.0882v2)
as the method reference and a separate family-wide validation problem for a
new discretization implementation. Reproducing the 48 rays at F6 is only a
point calibration and does not replay their two-parameter theorem.

## Derivation 4 — Laurent identities on arbitrary actual triples

**Target.** Establish the two Laurent conditions on every actual MUB triple,
with a symmetry reduction that supplies the orientation needed in 5.

For a raw Hadamard matrix H and a balanced sign vector gamma, define

\[
g_H(\gamma)=\sum_c\prod_r H_{rc}^{\gamma_r},\qquad
G_H(\gamma)=|g_H(\gamma)|^2.
\]

Let gamma1 = (1,1,1,-1,-1,-1) and gamma2 = 3 gamma1. A useful representative
target on every ordered actual triple, with H its first transition matrix, is

\[
g_H(\gamma_1)=0,\qquad
g_H(\gamma_2)g_{H^*}(\gamma_2)=0.
\]

**Derive the symmetry reduction before running elimination.** Independent
permutations of the first two bases induce independent row and column
permutations of H. Column permutations leave gH unchanged, while they act as
row permutations on H*. Thus the second representative identity, quantified
over all actual triples, yields

\[
g_H(\mu)g_{H^*}(\nu)=0
\quad\text{for all independent permutations }\mu,\nu\text{ of }\gamma_2.
\]

For a fixed H this implies that either all cubic sums of H vanish, or all
cubic sums of H* vanish. Indeed, if one sum on the first side is nonzero, every
sum on the second side is zero. Reversing the first two bases supplies the
linear identities for H* as well. This establishes the needed uniform orientation;
a pointwise choice of a zero factor for each permutation would not suffice.

**Exact domain.** Normalize the first basis to I. Introduce raw matrices H,K,T
and the positive algebraic constant r = sqrt(6), with unit-modulus entries,

\[
H^*H=K^*K=6I,\qquad H^*K=rT.
\]

These equations describe actual triples (I,H/r,K/r); T is their third
transition matrix. Keep the positive embedding of r explicit. Split all
equations into real and imaginary parts, and replace inverse phases by their
conjugates using the circle equations. A smaller dephased presentation is
allowed after proving that it covers all triples and preserves the targets.

**Certificate search.** The representative targets amount to four real
polynomial vanishing problems: real and imaginary parts of the linear sum
and of the cubic product. Their degrees in the raw H coordinates are at most
6 and 36 respectively. This avoids beginning with the squared, fully summed
degree-72 expression. Use the actual symmetries to reduce the multiplier
spaces, then seek exact ideal-membership identities. If complex
ideal membership is too strong, seek real-radical identities of the form

\[
f^{2m}+\sum_\ell q_\ell^2=\sum_i a_i E_i,
\]

for each real target f, where Ei are the actual triple equations. Such an
identity forces f=0 at every real solution. Coefficients over a real algebraic
field require the specified embedding. Chart denominators and any extra
inequalities require their corresponding saturation or Positivstellensatz
terms.

Search bounded multiplier degrees and exploit sparse monomial orbits. An
initial symbolic calculation on the known two-circulant construction is useful
for discovering multipliers, but acceptance is on the full triple equations.
Numerical triple searches may falsify a candidate identity; any apparent
counterexample must be promoted to an exact triple before it changes the
mathematical conclusion. Failure to find a certificate at a chosen degree is
a reason to change the ansatz, not a disproof of the identity.

**Deliverable and acceptance.** Explicit coefficient witnesses for the four
representative targets, the relabeling and orientation lemmas, and an exact
checker tied to the actual triple equations. The target is the published
Conjecture 2 and its use in
[Matolcsi et al., equation (4.9) and Proposition 4.2](https://link.springer.com/article/10.1007/s10801-026-01506-x).
The existing
[Conjecture2GeneralMechanization.lean](../../../../../lean4/research_programs/mub6/Conjecture2GeneralMechanization.lean)
provides finite parity and table calculations, so new matrix identities are
required at this interface.

## Derivation 5 — Assemble the dimension-six theorem

**Target.** Derive no four mutually unbiased bases in C6, construct three,
and conclude N(6) = 3.

Take any proposed quartet and choose a constituent triple. Derivation 4
selects an orientation of a transition matrix in which all balanced linear
and cubic Laurent sums vanish. Apply the matrix argument underlying
Proposition 4.2 to place that oriented transition, up to equivalence, in the
Fourier or Szöllősi family. Replay its binary-vector, minus-one-entry and
family-classification lemmas with the exact matrix hypotheses. Bind the
external classification step to its cited theorem; a declared finite table
does not replace it.

The Fourier case contradicts the full family exclusion theorem. The Szöllősi
case contradicts 3. The transport of the pair extends to the entire proposed
quartet by 1, including the adjoint orientation. Hence no quartet exists.
Any larger collection contains a quartet, so the upper bound is three.

For the matching lower bound, pair three mutually unbiased qubit bases with
three mutually unbiased qutrit bases and take tensor products. Their squared
cross overlaps multiply to (1/2)(1/3)=1/6. Supply the explicit matrices and
check their Gram and cross-Gram identities exactly.

**Deliverable and acceptance.** A proposed `Mub6MaximumThree.lean` module
assembles the concrete results, and the manuscript gives the corresponding
mathematical derivation. The final theorem must not retain Conjecture 2,
Conjecture 3 or family coverage as unproved premises. For a fully local Lean
proof, the Fourier theorem and the classification lemmas also need local
proofs/certificate replays; adding them as axioms would leave that
formalization conditional. The mathematical presentation may cite established
external theorems with their exact hypotheses.

## Execution order and handoff

Complete 1 first. In 2, prioritize a completeness certificate for the
algebraic sample and one explicit open region. Then pursue the coverage in 3
and the polynomial identities in 4 as independent mathematical work streams.
Prepare the statement-level assembly in 5 early so that every intermediate
output has a precise consumer.

For each derivation retain its defining equations, parameter domain, proof
or certificate, replay command and the next unresolved sublemma. Use exact
rational arithmetic and algebraic numbers represented by defining polynomials
and rational isolating intervals. Numerical computation may propose roots,
cells or identities; every accepted implication must follow from its exact
mathematical check.

The next computation to prepare is the converse/completeness check for the
504-root parametrization. Existing regeneration commands are in the
[sample README](szollosi_vectors/README.md#reproduce). The current
`exactcheck.py` substitution test is one part of that check, not the complete
converse certificate. No new checker or theorem module named in this design
is assumed to exist yet.
