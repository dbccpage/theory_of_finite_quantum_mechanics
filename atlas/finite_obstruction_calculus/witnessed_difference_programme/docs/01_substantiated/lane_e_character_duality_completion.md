# Lane E: characters, presentation stability and completion duality

AuthorityEffect: None. This derivation shows under the declared metric
presentation assumptions how the actual CS/CS_Q/Q image-factor route reaches
continuous characters and, when local compactness is supplied, classical
Pontryagin duality. The general LCA theorem is an imported classical result;
the calculations below are written mathematical arguments. They are distinct
from the selected Lean declarations and finite executable checks.

The [existing presentation-completion supplement](cs_q_presentation_completion.md)
already contains PC-1, the dyadic compact-open calculation PC-2, and the
counterexample indexed by the 2-adic number -1/3. This supplement supplies an
explicit discontinuity sequence for **every** noninteger 2-adic index and the
general homomorphic-presentation theorem, including its exact connection to
the source objects and its necessary hypotheses.

## 1. Objects and the actual source maps

Write C(A) for metric completion and A^vee for the group of continuous
characters A -> T with the compact-open topology. Thus completion and
character duality have different notation. All characters below take additive
values in T = R/Z; exponentiation exp(2 pi i t) gives the equivalent
multiplicative U(1) convention. Put

$$
d_T(s,t)=\min_{k\in\mathbb Z}|s-t-k|,\qquad
C_n=\mathbb Z/2^n\mathbb Z,\qquad
D=\mathbb Z[1/2]/\mathbb Z.
$$

The diagram is

$$
C_0\longrightarrow C_1\longrightarrow\cdots\longrightarrow D
\longrightarrow T,\qquad
[k]_{2^n}\longmapsto[2k]_{2^{n+1}},\qquad
p_n(k)=[k/2^n].
$$

Here p_n is a homomorphism only when its rational coordinate is interpreted
modulo Z. The representative k/2^n in [0,1) with ordinary real addition is
not an additive group presentation. The source implements precisely the
representative and the modular finite arithmetic:

| Existing object | Mathematical interpretation | Additional premise for the infinite statement |
| --- | --- | --- |
| `CyclicPresentation(level)` and `inclusion_to_next` | C_n and k -> 2k | Algebraic direct limit over every n |
| `dyadic_coordinate` | A rational representative of p_n(k) | Quotient by Z and the declared circle metric |
| `PontryaginCharacter.angle_turn` | q_n(k) = [a_n k/2^n] | Compatible indices a_(n+1) = a_n mod 2^n |
| `dual_pullback_from_next` | Restriction of q_(n+1) along the inclusion | A common, all-level continuity modulus |

These are the methods in
[`coda_inductive_presentation.py`](../../../../../../omega_engine_projects/finite_to_continuum/code/coda_inductive_presentation.py),
inspected at repository checkpoint `c33fb25be7f7bb340eb7345d90134dc116bac244`.
Their colimit identification is derived in
[the dyadic supplement, sections 1-4](dyadic_refinement_and_duality.md).
Choosing the displayed finite generator fixes the index parametrization.

The runbook's literal alphabet excludes its own uppercase symbols and
equations. We retain short typed equations and bare arrows, using ordinary
mathematical notation wherever needed to distinguish the objects. In
particular Z and Z_2 are never interchangeable, and C(D) never denotes D^vee.

For a set X, metric space P, complete metric space Y, presentation p:X -> P,
and query q:X -> Y, retain the exact existing condition

$$
\forall\varepsilon>0\ \exists\delta>0\ \forall x,y\in X:\quad
d_P(p(x),p(y))<\delta\ \Longrightarrow\ d_Y(q(x),q(y))<\varepsilon.
\tag{PC}
$$

PC-1 identifies this with a unique uniformly continuous recovery map
C(p(X)) -> Y. It supplies a map on the completion of the **actual image**;
it does not assign values at arbitrary unused labels in P.

## 2. Theorem LE-1: character selection on the dyadic colimit

There is an additive group isomorphism

$$
\operatorname{Hom}(D,T)=\mathbb Z_2,
\qquad
\chi_\alpha([k/2^n])=[A_n k/2^n],
\qquad A_n=\alpha\bmod 2^n\in\{0,\ldots,2^n-1\}.
\tag{1}
$$

For p:D -> T the usual inclusion,

$$
\operatorname{PC}(p,\chi_\alpha)\quad\Longleftrightarrow\quad
\alpha\in\mathbb Z\subset\mathbb Z_2.
\tag{2}
$$

**Algebraic derivation.** The point [1/2^n] has order 2^n. Its image under
a homomorphism must therefore be [A_n/2^n] for a unique residue A_n.
Since [1/2^n] = 2[1/2^(n+1)], these residues satisfy
A_(n+1) = A_n mod 2^n. Conversely, a compatible residue family defines
(1): different representatives can be moved to a common later level,
where compatibility gives the same value. Addition is checked there too.
The two constructions are inverse and respect addition. Compatible residue
families are exactly the definition of Z_2 as an inverse limit.
The finite character parametrization is also recorded in
[Conrad, Theorem 3.1](https://kconrad.math.uconn.edu/blurbs/grouptheory/charthy.pdf#page=6).

**Integer direction.** For j in Z and a representative r of x-y of least
absolute value,

$$
d_T(jx,jy)\le |jr|=|j|d_T(x,y).
$$

The choice delta = epsilon/(|j|+1) gives PC, including j=0. Negative
integers act by the same modular formula and have eventually-one 2-adic
digits; they must not be excluded by a finite-digit convention.

**Every exotic index has a discontinuity sequence.** Write
alpha = sum_(r>=0) b_r 2^r with b_r in {0,1}. The digits are eventually
zero exactly for nonnegative integer indices. If the digits are one from
place N onward, then, in Z_2,

$$
\alpha=A_N+\sum_{r=N}^{\infty}2^r=A_N-2^N\in\mathbb Z.
$$

Conversely, each negative integer has this eventually-one expansion:
for large n its residue is 2^n+j. Hence alpha is a standard integer if
and only if its binary digits are eventually constant.

If alpha is not an integer, there are infinitely many indices n>=2 with
b_(n-1) different from b_(n-2). Enumerate them increasingly as n_m and put
x_m = [2^(-n_m)]. The two leading binary digits of A_n/2^n are then 01
or 10. Consequently

$$
\frac14\le\frac{A_{n_m}}{2^{n_m}}<\frac34,\qquad
d_T(\chi_\alpha(x_m),0)\ge\frac14,\qquad
d_T(x_m,0)=2^{-n_m}\longrightarrow0.
\tag{3}
$$

With epsilon=1/4, every positive delta is refuted by a sufficiently large
m. This supplies the required sequence for the entire complement
Z_2 minus Z, rather than inferring that complement from one example.

**The -1/3 instance.** In Z_2 the geometric series sum_(r>=0)4^r is -1/3.
For m>=1 its residue modulo 4^m and its value at x_m=[4^(-m)] are

$$
A_{2m}=\frac{4^m-1}{3},\qquad
\chi_{-1/3}(x_m)=\left[\frac13-\frac{1}{3\,4^m}\right].
\tag{4}
$$

The displayed representative is in [1/4,1/3), so its distance from zero
tends to 1/3 and is always greater than 1/5. For any delta>0 choose m with
4^(-m)<delta; epsilon=1/5 (or 1/6) then refutes PC. A finite test can check
the residues and identities for supplied m. The quantified conclusion for
every delta follows from (4) and 4^(-m) -> 0, not from a finite test loop.

If D is discrete, its character dual is all of Z_2. The compact-open
topology is its inverse-limit topology: every compact subset of discrete D
is finite and lies in some C_n, while restriction to each finite C_n is
determined by the value at its generator. This is a different topology on
the same algebraic source.

## 3. Theorem LE-2: metric-colimit dual and the failed hypothesis

For D with its circle subspace metric,

$$
D^\vee\cong\mathbb Z_{\mathrm{discrete}},\qquad
(D^\vee)^\vee\cong T,\qquad
\operatorname{ev}_D:D\longrightarrow T,\quad d\longmapsto d.
\tag{5}
$$

The evaluation map is a dense proper topological embedding; it is not
surjective. D is Hausdorff and abelian, but it is not locally compact.

**Continuity gives the common modulus.** If chi:D -> T is a continuous
homomorphism, continuity at zero gives delta for each epsilon. Translation
invariance and additivity give

$$
d_T(\chi(x),\chi(y))=d_T(\chi(x-y),0),\qquad
d_T(x,y)=d_T(x-y,0).
$$

Thus chi satisfies PC. LE-1 identifies all continuous characters as chi_j,
j in Z. This argument concerns homomorphisms; continuity alone does not
make an arbitrary map on a noncompact metric space uniformly continuous.

**Compact-open topology.** In D the set

$$
K=\{0\}\cup\{[2^{-n}]:n\ge1\}
$$

is compact: it is a convergent sequence together with its limit. Define

$$
W(K,1/4)=\{\chi:\chi(K)\subset B_T(0,1/4)\}.
$$

This is a compact-open neighborhood of the zero character. For nonzero
j=2^v u with u odd, evaluation at [2^(-(v+1))] in K gives [u/2]=[1/2].
Hence W(K,1/4) contains only chi_0. Translating this neighborhood makes
every character isolated. This verifies the topology, not only the
algebraic list of characters.

A homomorphism from discrete Z to T is uniquely n -> nt, for an arbitrary
t in T. Compact sets in discrete Z are finite. The map t -> (n -> nt) is
continuous for the compact-open topology because each finite collection of
evaluations is continuous. Its inverse is evaluation at 1, also continuous.
This identifies the bidual in (5). Under it, ev_D(d)(j)=jd, so ev_D is the
usual subspace inclusion. Dyadic floor approximations show density.
The point [1/3] is absent: 1/3 = k/2^n mod Z would force 3 to divide 2^n.
It is therefore an explicit non-surjectivity witness.

**Local compactness fails.** Suppose D had a compact neighborhood K_0 of
zero. There is an open neighborhood U of zero in T with U intersect D
contained in K_0. The image of K_0 in the Hausdorff circle is compact,
hence closed. Since D is dense, every point of U is in the closure of
U intersect D, so U is contained in K_0, hence in D. But a nonempty open
circle arc is uncountable, while D is countable. This is a contradiction.

The executable companion uses a rational witness inside each supplied
ball. For any radius r>0 choose s with a=1/(3*2^s)<min(r,1/4), and put
u_k=floor(2^k a)/2^k. Then u_k belongs to D, 0<=u_k<a<r, and
0<a-u_k<2^(-k). The sequence is Cauchy and its circle limit is [a],
which is not dyadic because its reduced denominator is divisible by 3.
Any compact neighborhood of zero would contain a sufficiently small
such ball and hence this sequence. Its compactness would give a
subsequence converging in D, contradicting uniqueness of its ambient
limit. This is the all-radius argument behind the finite tested prefixes.

Thus the missing hypothesis in the classical **LCA** theorem is local
compactness, and here the explicit evaluation calculation separately
establishes non-reflexivity. Failure of local compactness by itself is
not a theorem that every topological abelian group fails reflexivity.

## 4. Theorem LE-3: completion and circle reflexivity

The complete metric group T contains D isometrically and densely: for
t in [0,1), floor(2^n t)/2^n has distance at most 2^(-n) from t. The circle
is compact, as the continuous image of [0,1], and every compact metric
space is complete. Consequently

$$
C(D)\cong T,\qquad C(D)^\vee\cong\mathbb Z_{\mathrm{discrete}},\qquad
\operatorname{ev}_{C(D)}:C(D)\overset{\sim}{\longrightarrow}
\bigl(C(D)^\vee\bigr)^\vee.
\tag{6}
$$

**Extension and the group law.** By PC-1, each continuous character on D
extends uniquely to a uniformly continuous map F:T -> T. For dyadic
sequences d_n -> s and e_n -> t, continuity of addition and of F yields

$$
F(s+t)=\lim_n F(d_n+e_n)
=\lim_n\bigl(F(d_n)+F(e_n)\bigr)=F(s)+F(t).
$$

Also F(0)=0. Thus the extension is a character, not just a continuous map.
Conversely a continuous character of T restricts to a continuous character
of D. LE-1 identifies that restriction with a unique integer j, and density
makes F(t)=jt on the whole circle. This derives the circle character
classification from LE-1 without importing general Pontryagin duality.

The compact subset K from LE-2 also isolates the zero character on T, so
T^vee is discrete Z. The earlier direct computation of Z^vee identifies
(T^vee)^vee with T, and evaluation sends t to the character j -> jt.
Evaluation at 1 is its continuous inverse. This gives the topological
isomorphism (6) directly. The same conclusion also falls under classical
LCA duality because T is compact Hausdorff abelian.

This restoration is specific to the declared circle presentation. Metric
completion of a general metric abelian group need not be locally compact;
that additional hypothesis remains explicit in LE-4.

## 5. Theorem LE-4: compatible finite abelian presentations

Let (G_n,i_n) be a sequential system of finite abelian groups and
homomorphisms. The i_n need not be injective. Let M be an abelian group
with a **complete translation-invariant metric** d_M, and let p_n:G_n -> M
be homomorphisms satisfying p_(n+1) i_n = p_n. Set

$$
G=\varinjlim_n G_n,\qquad p:G\longrightarrow M,\qquad
S=p(G)=\bigcup_n p_n(G_n),\qquad H=\overline S^{\,M}.
\tag{7}
$$

The metric supplies the group uniformity: inversion is an isometry and
d_M(x+y,x'+y') <= d_M(x,x')+d_M(y,y'). In particular it makes M a
Hausdorff topological group.

For every algebraic character chi:G -> T, the following are equivalent:

$$
\operatorname{PC}(p,\chi)\quad\Longleftrightarrow\quad
\exists!\,F:H\longrightarrow T\text{ continuous homomorphism with }Fp=\chi.
\tag{8}
$$

If H is locally compact, it is a Hausdorff LCA group and its canonical
evaluation map H -> (H^vee)^vee is a topological isomorphism. Compactness
of H is a sufficient condition. Its continuous characters separate points,
and on the original colimit the surviving characters distinguish exactly
the presentation fibres:

$$
p(x)=p(y)\quad\Longleftrightarrow\quad
\chi(x)=\chi(y)\text{ for every character }\chi\text{ satisfying PC}.
\tag{9}
$$

**Image and completion.** Compatibility makes the images p_n(G_n) nested
subgroups and induces p. Closure preserves the subgroup operations, so H
is a closed subgroup of the complete group M and is complete. The inclusion
S -> H is isometric with dense image, identifying C(S) with H as a metric
group. If p is noninjective, d_p(x,y)=d_M(p(x),p(y)) is a pseudometric,
not a metric on G. Its zero-distance equivalence is x-y in ker p. The
separated quotient is

$$
(G/\ker p,d_p)\cong S,\qquad C(G/\ker p)\cong H.
\tag{10}
$$

No unseparated colimit is silently called a Hausdorff LCA group.

**Forward implication in (8).** PC forces chi to be constant on each
p-fibre: the output distance is less than every positive epsilon whenever
the input distance is zero. Thus chi vanishes on ker p and descends to a
unique g:S -> T. Additivity of p and chi makes g additive. PC is exactly
uniform continuity of g in the inherited metric. Completeness of T and
PC-1 extend g uniquely to a uniformly continuous F:H -> T. Passing to
limits of sums as in LE-3 gives the homomorphism law. Two continuous
extensions agreeing on dense S agree everywhere, so uniqueness also holds
among continuous homomorphisms.

**Reverse implication in (8).** A continuous homomorphism F:H -> T is
uniformly continuous for the invariant metrics: continuity at zero controls
F(s-t), hence all pairs s,t. Applying that common modulus to p(x),p(y)
gives PC. This implication does not require compact H. An arbitrary
continuous, nonhomomorphic extension would not suffice for this step.

**Where classical duality enters.** If H is locally compact, the imported
Pontryagin-van Kampen theorem identifies ev_H as a topological isomorphism
for the compact-open dual; see
[Dikranjan, Theorem 12.5.4(c)](https://users.dimi.uniud.it/~dikran.dikranjan/ITG.pdf#page=102).
Its injectivity gives character separation. When p(x) differs from p(y),
choose a character of H nonzero on p(x)-p(y) and compose it with p;
(8) makes the resulting character PC. This gives (9). Equivalently,
the intersection of the kernels of all PC characters is exactly ker p.
The complete-metric and image-factor statements do not themselves contain
this general LCA theorem, and it is not claimed as a new Lean result.

Restriction along S -> H identifies their continuous character groups
algebraically by (8). A general claim about the compact-open topologies
of these two duals requires its own argument; the explicit K argument
above supplies it for the dyadic circle. Equation (9) requires separation
on H, not an unproved topological identification of these duals.

**The countable dense colimit obstruction.** If H is nondiscrete and
connected, S is a countable proper dense subgroup and is not locally
compact. To justify properness, H is complete metric and hence Baire.
In a nondiscrete Hausdorff topological group each singleton is closed
with empty interior; a countable H would contradict the Baire theorem.
Since S is a countable union of finite images, S cannot equal H.

More generally, a proper dense subgroup S of a Hausdorff group H cannot
be locally compact in the subspace topology. Indeed, a compact
neighborhood K_0 in S and ambient open U with U intersect S contained
in K_0 give U contained in K_0 contained in S, by density and closedness
of compact subsets of H. Thus S is open in H, and an open subgroup is
closed because its other cosets are open. Density would force S=H.
This argument establishes the asserted obstruction. In the complete
metric setting above, nondiscreteness already makes H uncountable by
Baire; connectedness can therefore be dropped.

When p is injective, this conclusion applies directly to G with its
pullback metric. Otherwise it applies to the separated group G/ker p.
For this proper dense presentation, classical LCA reflexivity can be
applied to the completed H only after local compactness of H is supplied.
It cannot be applied to S. No general non-reflexivity claim for all
non-locally-compact groups is needed.

### Presentation stability

Suppose another homomorphic presentation r:G -> M' has the same kernel
as p. The image bijection f:S -> r(G), f(p(x))=r(x), is then well-defined
and additive. If f and its inverse are uniformly continuous in the
declared image metrics, PC(p,chi) and PC(r,chi) are equivalent by
composition of moduli. Their completed image maps extend to inverse
continuous group isomorphisms. They transport the character extensions
and preserve local compactness. Equality of fibres alone supplies the
image bijection; the two metric control conditions are the further
premises needed for this stability assertion.

## 6. Binding CS -> CS_Q -> Q, without a hidden LCA assumption

The names denote a dependency route through existing mathematical
statements, not a pre-existing functor that equips arbitrary program data
with a group or topology:

$$
\text{profile fibres}\longrightarrow\text{image factor}
\longrightarrow\text{uniform image factor}\longrightarrow
\text{completion character}\longrightarrow\text{LCA bidual}.
$$

1. [CS-D1 and CS-T1](source_archive/coda_component_packages/cs/coda_cs.md)
   use a source X, a profile p, a query q, and a factorization
   p = forget composed with fine. This is an equality/fibre statement.
   CS-T2 identifies equality of a bundled profile with pointwise equality
   at its indices. These definitions do not supply a group law or metric.
2. [CSQ-T1](source_archive/coda_component_packages/cs_q/coda_cs_q_bridge.md)
   supplies exactly g:p(X) -> Y when q is fibre-constant. Its
   `Coda.CSQ.ImagePoint` retains a source witness and its `ImageFactor`
   retains recovery and invariance under equal profile values. In LE-4,
   X=G, Y=T, q=chi; the missing fibre condition is precisely
   ker p contained in ker chi. PC supplies it and the further metric
   modulus. CSQ-T2's collision bound 2 epsilon and CSQ-T3's Lipschitz
   control in a **source** metric do not supply that modulus in d_M.
3. [Q-T3](source_archive/coda_component_packages/q/coda_q.md) extends a
   uniformly continuous map into a complete metric target. Apply it to
   the actual image factor g:S -> T, not to an unrelated source metric
   or an unused profile label. PC-1 already combines CSQ-T1 and Q-T3.
   LE-4 adds the homomorphism law, separated group quotient, and the
   explicit local-compactness condition needed for duality.

For the concrete cyclic source, at each n take X=G_n=C_n,
p_n(k)=[k/2^n], and q_n(k)=[a_n k/2^n]. The image is finite and p_n is
injective, so an exact finite factor exists for every a_n. The relation
a_(n+1)=a_n mod 2^n is exactly the source's `dual_pullback_from_next`;
it makes those queries compatible under the inclusions. For any two
colimit points, move their representatives to one common level.
Therefore all-level PC is equivalent to a **single** delta for each
epsilon working for every level and every pair there. The digits in
LE-1 show exactly when this extra condition holds. A separate positive
continuity radius at each finite level is insufficient.

The archived
[`ProfileFactorizationSolver`](source_archive/coda_component_packages/cs_q/code/coda_cs_q_bridge_core.py)
accepts `CofinalShadowTower`, `QueryProbe`, and a supplied finite domain.
Its `evaluate_profile` bundles callable projector values; its solve method
builds a lookup only on observed profile values or returns a collision.
For the cyclic instance one projector p_n and one query q_n instantiate
this finite image factor. The type stores arbitrary callables and does
not enforce homomorphic p_n, circle topology, infinitely many levels,
or a uniform all-level modulus. Those are the declared mathematical
premises above. The existing
[`profile_examples`](../../../../../../omega_engine_projects/finite_to_continuum/code/presentation_closure_examples.py)
also exercises a real sampling obstruction: the zero function and the
distance-to-grid tent share their four samples but have different
integrals. Character duality does not erase that query collision.

The native owners have similarly bounded meanings at the inspected source
checkpoint:

| Native entry point | Existing checked object | What still needs the theorem's premises |
| --- | --- | --- |
| [`Layer3Cs::evaluate_report_query`](../../../../../../omega_engine/crates_rs/omega_wdp/src/coda/layer3_cs.rs) | Total finite report/query tables; realized-image factor or a collision | Infinite compatible homomorphic presentations and PC |
| [`Layer4CsQ::evaluate_declared_separation`](../../../../../../omega_engine/crates_rs/omega_wdp/src/coda/layer4_cs_q.rs) | A declared finite quotient and weighted coordinate separation | Continuous character separation of H; finite positive gaps are not all-level moduli |
| [`Layer5Q::evaluate`](../../../../../../omega_engine/crates_rs/omega_wdp/src/coda/layer5_q.rs) | Order and diameter of a supplied rational interval | Construction of C(S), group operations, and local compactness |

Thus the theorem gives the general conditional foundations route and an
actual completed dyadic instance. It does not reinterpret a native finite
verdict as a completed topological-group computation.

## 7. Verification boundary and source pins

The four analytic statements above are `PROSE_PROOF` claims. LE-4's LCA
reflexivity clause explicitly depends on classical Pontryagin-van Kampen
duality. The cited primary mathematical sources, inspected 2026-10-08, are
Keith Conrad, *Characters of Finite Abelian Groups*, Theorem 3.1, printed
page 6, and Dikran Dikranjan, *Introduction to Topological Groups*,
Theorem 12.5.4(c), printed page 97 / PDF page 102. The latter uses the
compact-open dual and identifies the canonical evaluation map as a
topological isomorphism. Its pointwise-topology variant is a different
statement and is not used here.

The existing
[`PresentationCompletion.lean`](../lean4/WitnessedDifference/PresentationCompletion.lean)
contains `relativeControl_iff_unique_completion` on
`UniformSpace.Completion (Set.range p)` and `completion_routes_commute`.
The latter requires uniform continuity of the source presentation. The
[package manifest](../lean4/lake-manifest.json) pins Mathlib to
`0df444a360eaa60ab8c11dca51a86af692955474`.
The present analytic derivation does not change those hypotheses.

The companion
[`PresentationDuality.lean`](../lean4/WitnessedDifference/PresentationDuality.lean)
and its axiom report record the selected formal increment; their actual
declarations and local build output determine that scope. Its
`character_pc_of_lipschitz` assumes the supplied bound `hK` and derives PC;
it does not establish the integer-frequency bound itself.
`unique_character_extension_to_completion` retains the additive
homomorphism law on the completion of the presentation subgroup, under
`IsUniformAddGroup P` and the explicit PC hypothesis.

The formal target is Mathlib `Circle`, or `Additive Circle`, with the
chordal metric inherited from C. The analytic formulas above use turns
and d_T. If r=d_T(s,t), then 0<=r<=1/2 and

$$
4r\le |e^{2\pi i s}-e^{2\pi i t}|=2\sin(\pi r)\le2\pi r.
$$

Thus these metrics determine the same uniformity and the same PC
condition after adjusting moduli. Their numerical Lipschitz constants
are not interchangeable. This comparison is stated here analytically;
it is not an extra declaration in the companion Lean file.

`dyadic_subspace_not_complete` concerns the actual real subtype
{x in R : there exist integers n,k with x=k/2^n}. Its dyadic floor
sequence tends to sqrt(2), whose irrationality excludes it from that
subtype. This is an incompleteness result in R. The circle quotient D,
its local-compactness failure, and the evaluation map in (5) are separate
objects treated by LE-2. The written Z_2 classification, compact-open K
argument, and general LCA reflexivity are not represented as new
Lean-checked results.
Finite checks in
[`test_presentation_duality.py`](../../../../../../omega_engine_projects/finite_to_continuum/tests/test_presentation_duality.py)
exercise exact character arithmetic and countermodel prefixes. The
all-level steps are the mathematical arguments (1)-(10), not a conversion
of finitely many successful cases into an infinite assertion.

This closes the Lane E character/presentation dependency under its stated
assumptions. Separate Day 3 B/C bindings, preflight checks, native continuum
transport, and physical field-theory limits require their own evidence.

## 8. Local verification record

Verified on 2026-10-08 from base
`c33fb25be7f7bb340eb7345d90134dc116bac244`. All Python commands below run
from the repository root with Python 3.12.10 and pytest 8.3.5. Each listed
command exited 0. The test counts concern their named files only.

| Exact command | Observed result and scope |
| --- | --- |
| `py -3.12 -m pytest -v omega_engine_projects/finite_to_continuum/tests/test_presentation_duality.py` | 35 passed; finite character distances, PC counterexamples, Cauchy prefixes, Haar aliases and quadrature |
| `py -3.12 -m pytest -q omega_engine_projects/finite_to_continuum/tests/test_presentation_closure_examples.py` | 28 passed; existing presentation-closure regressions |
| `py -3.12 -m pytest -q -o addopts= omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/plans/test_goal_dag.py` | 30 passed; DAG shape, anchors, canonical representation, and rejection of a missing anchor through both validation commands |
| `py -3.12 omega_engine_projects/finite_to_continuum/code/presentation_duality.py` | Exact finite replay: 436,905 ordered dyadic pairs; four ball radii at 100 levels; seven Haar levels; constructed PC refusals. `infinite_theorems_mechanized` is false |
| `py -3.12 omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/plans/goal_dag.py validate` | 241 nodes; 516 local anchors checked; 29 external anchors explicitly unverified in this checkout |
| `py -3.12 omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/plans/goal_dag.py next` | Day 3 remains in progress because B/C native binding and runner preflight are still separate tasks |

The DAG checker validates planning structure and source anchors, not mathematical
truth. Its `validate` spelling is an alias for the existing `check` command.
Six stale references already present at the base were reconciled with current
manifest entry names and corrected Chapter 23 statements; no sealed manifest
was regenerated, and no release-approval decision was closed.

The Lean run uses Lean 4.33.1, compiler commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`, Lake `5.0.0-src+819816b`, and the package's existing
Mathlib pin. The source package was staged in the workspace's `.lane_e_lean`
and accessed through a short Windows junction. Its dependencies came from the
existing local cache; all nine dependency HEADs matched `lake-manifest.json`.
All 93 staged Lean source/config files matched the canonical package bytes.
No tracked Lake configuration was changed.

| New formal source | SHA-256 of the checked bytes |
| --- | --- |
| `PresentationDuality.lean` | `b4b98639fc31036d9f8433dae95162d89b2fc4e3f4ecce9ade32eff83398d329` |
| `PresentationDualityAxiomReport.lean` | `1bffbc2661e93a0013c320664382780740a0a91cd870bb0db1fe0cb62d646de3` |

The eight declarations in the new axiom report use only `propext`,
`Classical.choice`, and `Quot.sound`. The new module contains no `sorry`,
`admit`, or custom `axiom` declaration. This census concerns the selected
formal results described in section 7, not all four analytic duality theorems.

The full library build exited 0 with `Build completed successfully (8742 jobs)`:

```powershell
& 'C:\Users\a343o\.elan\toolchains\leanprover--lean4---v4.33.1\bin\lake.exe' -d 'C:\lk\lane_e_8162' --no-cache build WitnessedDifference +WitnessedDifference.PresentationCompletion +WitnessedDifference.PresentationDuality +WitnessedDifference.PresentationDualityAxiomReport
```

Both standalone reports below also exited 0, from working directory
`C:\lk\lane_e_8162`:

```powershell
& 'C:\Users\a343o\.elan\toolchains\leanprover--lean4---v4.33.1\bin\lake.exe' env lean WitnessedDifference/PresentationCompletionAxiomReport.lean
& 'C:\Users\a343o\.elan\toolchains\leanprover--lean4---v4.33.1\bin\lake.exe' env lean WitnessedDifference/PresentationDualityAxiomReport.lean
```

The existing completion report covers 15 declarations; the new report covers
eight. Their axiom union is exactly `propext`, `Classical.choice`, and
`Quot.sound`, with no `sorryAx`. The 93-file comparison and nine dependency-pin
comparison were repeated after both reports, with zero mismatches.
An initial report command using Lake's `-d` option from the workspace did not
resolve its relative input file; running the report from the package directory
corrected that invocation. `--no-cache` disables build-cache downloads, not all
possible network activity; this run reused the inspected local dependencies.
