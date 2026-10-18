# A faithful finite-history algebra: construction and remaining premises

2026-10-11. Written conditional proofs and exact native controls.
`realizes: null`; `authority_effect: None`; `genesis_effect: None`.

For a **declared nonempty finite groupoid** $G$, its full complex convolution
algebra with the **untwisted product below** has a faithful positive regular
representation. It is a simple matrix
algebra exactly when $G$ is connected and thin (one arrow between each ordered
pair of objects). With the full state space, standard tensor composition, and
sufficiently large available simple ancillas, this is also exactly the condition
for every state to have a pure purification. This proves a conditional route
to finite quantum kinematics; it does not derive its input groupoid, complex
scalars, states, or operational availability from `<>`.

## 1. The history quotient is an obligation

Start with specified admitted objects and legal histories, their identities and
concatenation. To obtain a category, associativity, identity laws and all legal
composites must hold. To quotient parallel histories by $\sim$, composition must
be a congruence: $h\sim h'$ must remain equivalent in every common legal left
and right context. If one representative admits a future context that the other
does not, a quotient that forgets this difference does not preserve legality.
Finite cutoff enumeration alone supplies no closure theorem.

For every protected question $Q$, the report $q(h)=[h]$ preserves $Q$ precisely
when $Q$ is constant on each fiber. This is the
[WDP criterion GEN-WDP-03](../../001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_bridge_register.md).
The same condition must apply to the relevant costs, occurrences and future
questions (GEN-WDP-06 and O02–O03), not just the final endpoint. An endpoint
quotient may produce a thin groupoid while destroying exactly those questions.
It is a proposed quotient, not a proof that its loss is admissible.

Invertibility is an additional demand. In the category with one object and
arrows $1,z$, where $z^2=z\ne1$, every functor to a groupoid satisfies
$F(z)^2=F(z)$, hence $F(z)=1$. Such a functor cannot faithfully preserve the
question distinguishing $z$ from $1$. Even an involutive composition-reversing
dagger need not give inverses: the identity dagger on this monoid is a concrete
counterexample. The native validator below rejects it. This does not assert
that this toy monoid is a particular native Genesis transition system.

Likewise, freely adjoining inverses to a graph does not generally yield a
finite groupoid: a surviving cycle has arbitrarily many winding histories.
Making it finite requires another justified relation or quotient. None of
these steps is supplied merely by a cochain identity $d^2=0$.

## 2. Positive faithful convolution, with the scalar choice exposed

Write $g:x\to y$, and use the algebra convention $gh=g\circ h$ (rightmost
first). The native category API instead spells this `compose(h, g)`.
On the complex vector space with independent basis $\{\delta_g:g\in G\}$ set

$$
\delta_g\delta_h=
\begin{cases}\delta_{gh}&s(g)=t(h),\\0&\text{otherwise},\end{cases}
\qquad \delta_g^*=\delta_{g^{-1}},\qquad
1=\sum_{x\in G_0}\delta_{1_x}.
$$

Extend the product bilinearly and $*$ conjugate-linearly. Associativity follows
from category associativity on composable triples. If a triple is not
composable, both parenthesizations are zero, using the source/target laws.
The inverse laws give $(ab)^*=b^*a^*$ and $(a^*)^*=a$.

Define the **identity-coefficient trace**
$\tau(a)=\sum_x a_{1_x}$. An identity term in $\delta_g\delta_h$ occurs exactly
when $h=g^{-1}$. Consequently

$$
\tau(ab)=\sum_g a_g b_{g^{-1}}=\tau(ba),\qquad
\tau(a^*b)=\sum_g\overline{a_g}b_g,\qquad
\tau(a^*a)=\sum_g|a_g|^2.
$$

Thus $\langle a,b\rangle=\tau(a^*b)$ is positive definite. Left multiplication
$L_a b=ab$ satisfies $L_{ab}=L_aL_b$, $L_{a^*}=L_a^\dagger$, and is faithful:
$L_a=0$ implies $a=L_a1=0$. The image is a finite-dimensional unital
$*$-subalgebra of complex matrices, hence closed and a C*-algebra in the
operator norm. No unproved positivity assumption about this trace is needed.

This theorem **starts with complex linearization**. The same coefficient
argument over $\mathbb R$ gives a real positive representation; positivity
alone does not select the complex field. Native arithmetic below uses
$\mathbb Q(i)$, an exact subfield, and checks selected finite carriers. It does
not computationally enumerate all complex elements or prove completeness.

Also, $\tau$ is not in general the matrix trace of $L_a$. Nor should a density
matrix in the redundant regular representation be used to read off operational
purity. Operational purity below uses the canonical sum of ordinary matrix
traces in the simple-block decomposition, as in PO-000 E.7.

## 3. Matrix blocks and the exact simplicity criterion

Consider a connected component with $n$ objects. Choose a root $o$, let
$H=\operatorname{Aut}(o)$, and choose $p_x:o\to x$ with $p_o=1_o$. Every arrow
$g:x\to y$ has a unique form $p_yhp_x^{-1}$, where
$h=p_y^{-1}gp_x\in H$. Therefore

$$
\Phi(\delta_g)=E_{yx}\otimes\delta_{p_y^{-1}gp_x}
\quad\text{gives}\quad
\mathbb C[G]\cong\bigoplus_C M_{n_C}(\mathbb C[H_C]).
$$

This is a linear bijection: each triple $(y,x,h)$ reconstructs its unique
arrow. For composable $g:x\to y$ and $k:w\to x$, the middle connectors cancel,
so their group coordinate multiplies in the same order; matrix units encode
the composability condition. Taking inverses swaps the matrix indices and
inverts the group coordinate, proving $*$ preservation. These verifications
prove the algebra isomorphism without a dimension count standing in for it.

If there are two or more components, their identity sums are nonzero proper
central projections. In a connected component with $|H|>1$, set

$$
e_H=\frac1{|H|}\sum_{h\in H}\delta_h.
$$

Each group element permutes the summands on either side; hence $e_H$ is
central, $e_H^*=e_H$, and $e_H^2=e_H$ (each product has $|H|$ preimages).
Independence of the group basis shows $e_H\ne0,1$. The corresponding
projection $I_n\otimes e_H$ is therefore proper and central. In groupoid
coordinates it is $|H|^{-1}$ times the sum of **all loops at every object** of
that component. This proves non-simplicity without character classification.

Conversely, if the groupoid is connected and $H$ is trivial, its algebra is
$M_n(\mathbb C)$. Every nonzero two-sided ideal contains a matrix with a
nonzero entry $a_{ij}$; multiplying by matrix units on both sides produces
$a_{ij}E_{kl}$ for every $k,l$, so the ideal is the whole algebra. Trivial
isotropy is equivalent to thinness, since $g,h:x\to y$ have
$h^{-1}g=1_x$ exactly when $g=h$. Thus, for nonempty finite $G$,

$$\boxed{\mathbb C[G]\text{ simple}\iff G\text{ connected and thin}.}$$

The word **untwisted** is substantive. For $H=C_2\times C_2$, let
$U_{ab}=X^aZ^b$ with the usual Pauli matrices $X,Z$ and $a,b\in\{0,1\}$.
Then

$$U_{ab}U_{cd}=(-1)^{bc}U_{a+c,b+d},\qquad
U_{ab}^*=(-1)^{ab}U_{ab},$$

where indices are modulo two. The four matrices $I,Z,X,XZ$ are linearly
independent: $I,Z$ span the diagonal entries and $X,XZ$ span the off-diagonal
entries. Their product and involution therefore identify this **twisted**
group algebra with $M_2(\mathbb C)$, although $H$ is nontrivial. Its cocycle
$\alpha((a,b),(c,d))=(-1)^{bc}$ satisfies associativity because both cocycle
products have exponent $bc+be+de$ for a third label $(e,f)$.
The untwisted simplicity criterion cannot be applied to projective history
composition without first excluding or accounting for such phase data. The
native control checks all 16 products, all four adjoints and full basis rank
using the existing Pauli and exact-elimination owners.

The follow-on [projective-history bridge](qm_projective_history_algebra.md)
proves the center/radical and equal-block-size theorems for finite abelian
unitary twists, with exact six-dimensional Weyl and restricted MUB controls.

## 4. What purification selects under full operational premises

Now **assume** all normalized positive linear functionals of the full algebra
are admitted states; all positive contractions are effects; composites use
the standard finite-dimensional C*-tensor product; and suitable simple
ancillas and the required pure joint states are operationally available.
For $A=\bigoplus_rM_{d_r}(\mathbb C)$, states have the form
$\omega(a)=\sum_r\operatorname{Tr}(\rho_ra_r)$ with $\rho_r\ge0$ and
$\sum_r\operatorname{Tr}\rho_r=1$. This representation follows by the
nondegenerate matrix-trace pairing; positivity on all rank-one projectors
forces each representing matrix to be positive. It is a consequence of the
chosen state/effect premises, not an independent derivation of those premises.

The [PO-000 E.7 bounds](../../002_projection_obstruction/000_projection_obstruction/projection_obstruction.md)
give, for central weights $p_r=\operatorname{Tr}\rho_r$,

$$
\operatorname{Tr}\sigma^2\le\sum_r p_r^2,
\qquad
\min_{\eta\text{ pure-composite marginal}}\frac12\|\rho-\eta\|_1
=1-\max_r p_r.
$$

Attainment requires an available simple ancilla of dimension at least the
largest block rank. If $A$ has a nonzero proper central projection, admit a
half-and-half mixture of states supported in it and its complement. Every
standard-tensor extension has purity at most $1/2$, so none is pure. Conversely,
for $A=M_n(\mathbb C)$ a spectral decomposition
$\rho=\sum_i\lambda_i|v_i\rangle\langle v_i|$ is purified by
$\sum_i\sqrt{\lambda_i}v_i\otimes e_i$ in an available ancilla of sufficient
dimension. Hence the simplicity criterion of section 3 is precisely the
universal-purification criterion under these premises.

PO-000 E.6 takes a different conditional route to a positive form, from supplied
real spectral decompositions and signed Jordan–Lie identities. Its Lean proof
does not supply the groupoid quotient or complex linearization assumed here.
These routes identify possible bridge premises; neither makes them native.

## 5. History faithfulness is weaker than algebra faithfulness

For $H=C_2=\{e,s\}$, $s^2=e$, the sign character sends $e\mapsto1$ and
$s\mapsto-1$. It is injective on the two arrows, yet its linear extension

$$q:\mathbb C[C_2]\longrightarrow\mathbb C,\qquad q(ae+bs)=a-b$$

annihilates $e+s\ne0$. Thus faithful distinction of individual histories does
not imply faithful linearization. The two projections
$p_+=(e+s)/2$ and $p_-=(e-s)/2$ satisfy
$p_+p_-=0$, $p_++p_-=1$; choosing the sign sector kills $p_+$ and retains
$p_-$. The image is simple, while the full faithful algebra is not.

For the explicitly protected algebra question $Q(a)=\tau(a^*a)$, the equal
reports $q(0)=q(e+s)=0$ have $Q$ values 0 and 2. No report-only decoder can
recover this question; on this two-element class the sharp absolute-error
floor is 1, attained by the midpoint. This is a WDP fiber obstruction for
**linear combinations**, not a claim that the sign character loses the parity
of an individual arrow. An endpoint-only quotient, in contrast, already loses
the distinction between the loop $s$ and the identity $e$.

This is why applying the purification criterion after a sector choice must
record its kernel and the protected questions it discards. One may instead
explicitly choose a narrower operational sector; that is a different premise.

## 6. Connections and outstanding obligations

| Bridge | What is established here | What must still be justified |
| --- | --- | --- |
| Native Genesis / S(n) / MSS-N | Explicit algebraic target and quotient/reflection tests | Admitted carrier, all legal histories, cost/occurrence/future preservation, finite congruence and invertibility. A mathematical realization cannot create a new native stage. |
| WDP | Fiber obstructions for endpoint loss and character-sector linear loss | Which native and operational questions are protected; preservation under all relevant contexts, not a chosen finite list. |
| Projection Obstruction | Groupoid simplicity criterion feeds the conditional E.7 selector | Full state/effect spaces, standard composition, faithful algebra and actual ancilla/purification availability. |
| Composition phases | A Pauli counterexample shows a twisted nontrivial loop group can yield a simple algebra | Justify untwisted composition, or supply and analyze the actual normalized unitary two-cocycle. |
| Finite QM | A faithful matrix-algebra route after declared history and scalar premises | GAP-FQM-021 remains open; the packet integration tests do not establish these premises or select a readout. |
| FSP | Nontrivial sign holonomy obstructs forgetting loops in an endpoint quotient | Actual configuration-history quotient and sign representation; no general sign cure or efficient sampling result follows. |
| MUB6 | The pair groupoid on six objects has algebra $M_6(\mathbb C)$ | Multiple available orthonormal bases satisfying every cross-basis overlap $1/6$; no complete seven-basis existence or exclusion theorem follows. |

For FSP, a sign character of the path groupoid on a fixed configuration graph
descends to the pair groupoid of each connected component **iff every loop
has sign $+1$**.
Necessity follows because loops become identities. For sufficiency, two paths
with the same endpoints differ by a loop, so their signs agree; composition
of signs then descends. This is the multiplicative form of the established
[cycle-parity criterion](quantum_to_classical_descent/README.md). A vertex
sign gauge changes a path sign by its two endpoint factors and leaves loop
signs unchanged. In particular, the already-declared six-hop two-particle
configuration loop with bits $(0,1,0,0,1,1)$ obstructs such descent. Its path
groupoid need not be finite; any finite quotient used above needs separate
justification. This result is restricted to the stated sign-gauge family.
An ordinary sign character on paths and a projective two-cocycle modifying
algebra multiplication are different data; the Pauli example does not identify
one with the other or remove the FSP obstruction.

The [S(n)/MSS-N manuscript](../../001_finite_obstruction_calculus/001_sn_mssn/README.md)
retains its chain-retraction and finite-demand results. This note establishes
no new native stage, no unconditional Born rule, and no dynamics, locality,
outcome selection, or continuum limit. Those remain distinct obligations.

## 7. Native implementation and reproduction scope

The [category owner](../../../../../omega_engine/crates_rs/omega_category_theory/src/finite_groupoid.rs)
strengthens the existing validated dagger category by checking every inverse
equation. It retains the 64-arrow budget, constructs deterministic component
and matrix/group coordinates, and distinguishes empty from connected thin.
It neither adds missing inverses nor silently completes a composition table.

The [group algebra owner](../../../../../omega_engine/crates_rs/omega_lie_theory/src/finite_groupoid_algebra.rs)
implements exact $\mathbb Q(i)$ convolution, involution, coefficient trace,
the full regular action, and central isotropy averages, using sovereign
number-theory scalars and linear-algebra matrices. The direct category
dependency follows the existing foundation dependency direction; no foundation
depends on the physics crate.

The [six integration tests](../../../../../omega_engine/crates_rs/tests/omega_lie_theory/finite_groupoid_algebra.rs)
check full coordinate/product/inverse tables for Pair(6), Pair(2)$\times C_2$,
Pair(2)$\times S_3$ (also with a nonidentity connector), and two isolated identities.
Noncommuting $S_3$ exposes an accidentally reversed product convention and the
nonidentity chart checks connector cancellation. Full-basis regular-product,
adjoint and trace checks use Pair(2)$\times C_2$, $S_3$, and the disconnected
example; a non-real rational superposition checks mixed coefficients.
Central-projector, character-kernel and projective-twist controls are exact. Three category
unit tests cover noninvertible daggers, bad/missing inverse/composition data,
unknown arrows, the empty case, and the validation budget.

From `omega_engine/crates_rs`, with the configured toolchain/cache:

```sh
cargo test -j 1 --offline --locked -p omega_category_theory --lib finite_groupoid::tests
cargo test -j 1 --offline --locked -p omega_lie_theory --test finite_groupoid_algebra
```

The receipt records the focused native checks on 2026-10-11. The initial category run
updated the lockfile offline for the one direct dependency and omitted
`--locked`; the final category run uses the resulting lockfile. The general proofs
in sections 1–6 are written mathematics, **not new Lean theorems**. The finite
checks do not certify arbitrary declarations beyond their validator contract,
a native source-to-groupoid reflection, or an entire operational theory.
Historical archives remain unchanged; this research note is not a new paper
release or external deposit.
