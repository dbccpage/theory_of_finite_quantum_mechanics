<div align="center">

# Composite Quantum Systems from Local Statistics and One Controlled Shift: Proofs

**Author:** Jeremy H. Carroll

**Date:** 2026-10-26

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## Introduction

This note gives written proofs of the tensor-composition results (records TFQ-0410 to TFQ-0416)
that the derivation DAG (`dag/derivation_dag.json`) records as proved in Lean. The record
derivations are in `dag/derivations/27_tensor_composition/`. Each section states one result,
proves it, and names the Lean declarations that check it. The DAG identifier is on the line
beginning *DAG node*.

The result is a sufficient-assumption theorem. Two local finite-dimensional complex quantum
systems are given. With independent preparations and tests, local tomography, and one calibrated
reversible controlled shift, the composite is forced to be ordinary quantum theory on
$\mathbb C^n\otimes\mathbb C^m$. Local complex quantum theory, the operational premises and the
calibration are inputs. They are not derived from anything more primitive, and the countermodels
of §4 show only that particular weakenings fail, not that the package is minimal. The DAG node
`FQ-GAP-TENSOR-UNIQUENESS` remains CONDITIONAL.

**Notation.** $\mathrm{Herm}(d)$ is the real space of $d\times d$ Hermitian matrices,
$\mathrm{PSD}(d)$ its positive semidefinite cone, and $\langle X,Y\rangle=\operatorname{tr}(XY)$ the
trace pairing. $\mathrm{SEP}(n,m)$ is the conic hull of $A\otimes B$ with $A,B\ge0$.
$\mathrm{BP}(n,m)$ is the set of $X$ with $\langle a\otimes b|X|a\otimes b\rangle\ge0$ for all
local vectors. Then $\mathrm{SEP}\subseteq\mathrm{PSD}\subseteq\mathrm{BP}$.

---

## 1. Coordinates

### 1.1 Tomographic coordinates for the composite

DAG node: `TENSOR-TOMOGRAPHIC-COORDINATES`

Let $V$ be a finite-dimensional real vector space (the span of the composite's unnormalized
states). Let $\pi\colon\mathrm{Herm}(n)\times\mathrm{Herm}(m)\to V$ (product preparation) and
$\tau\colon\mathrm{Herm}(n)\times\mathrm{Herm}(m)\to V^*$ (product test) be bilinear with
$\tau(E,F)(\pi(A,B))=\operatorname{tr}(EA)\operatorname{tr}(FB)$. Assume local tomography: the
functionals $\tau(E,F)$ separate $V$.

**Theorem.** There is a unique real linear isomorphism $J\colon V\to\mathrm{Herm}(nm)$ with
$\tau(E,F)(x)=\operatorname{tr}((E\otimes F)J(x))$ for all $E,F$ and $x$. It satisfies
$J(\pi(A,B))=A\otimes B$, and the deterministic product test $\tau(I,I)$ becomes the trace.

*Proof.* (a) The trace pairing on $\mathrm{Herm}(d)$ is nondegenerate, because
$\operatorname{tr}(H^2)=\sum_{ij}|H_{ij}|^2>0$ for $H\neq0$. So every real basis $(P_a)$ of
$\mathrm{Herm}(d)$ has a trace-dual basis $(D_a)$ with $\operatorname{tr}(P_aD_b)=\delta_{ab}$.
(b) The products $E\otimes F$ span $\mathrm{Herm}(nm)$ over $\mathbb R$. Matrix units give this:
the real and imaginary Hermitian parts of $e_{ij}\otimes e_{kl}$ are real combinations of products
of the Hermitian parts of $e_{ij}$ and $e_{kl}$. Both spaces have real dimension $n^2m^2$, so the
products of the two local bases form a basis.

Define $J(x)=\sum_{a,b}\tau(P_a,Q_b)(x)\,D_a\otimes D_b$. Then
$\operatorname{tr}((P_c\otimes Q_d)J(x))=\tau(P_c,Q_d)(x)$, and by bilinearity the identity extends
to every $E,F$. If $J(x)=0$, every $\tau(E,F)(x)=0$, so $x=0$ by local tomography. Hence $J$ is
injective. The elements $\pi(D_a,D_b)$ are sent to $D_a\otimes D_b$: their $\tau(P_c,Q_d)$-values
are $\delta_{ac}\delta_{bd}$. These images form a basis, so $J$ is surjective. The same
computation gives $J(\pi(A,B))=A\otimes B$. Uniqueness holds because a linear map is fixed by its
pairings with all $E\otimes F$, which span by (b). Finally $\tau(I,I)(x)=\operatorname{tr}(J(x))$.
$\square$

A concrete choice of local basis uses $d^2$ rank-one projectors: $|i\rangle\langle i|$, and
$\frac12(|i\rangle+|j\rangle)(\langle i|+\langle j|)$ and
$\frac12(|i\rangle+i|j\rangle)(\langle i|-i\langle j|)$ for $i<j$. These are both states and
effects, so the coordinates are given by finitely many product probabilities. Preparations and
product tests give $\mathrm{SEP}\subseteq J(K)\subseteq\mathrm{BP}$ for the state cone $K$. The
coordinates do not decide where $J(K)$ lies between these cones. The same spanning argument shows
that a real linear process is fixed by its values on all product inputs and product tests, and
hence by a finite calibration table.

Lean: `lean4/TensorTomography.lean::product_span`, `lean4/TensorTomography.lean::pairing_nondegenerate`,
`lean4/TensorCoordinates.lean::tomographicEquiv`, `lean4/TensorCoordinates.lean::tomographicEquiv_prepare`,
`lean4/TensorCoordinates.lean::tomographicEquiv_test`, `lean4/TensorCoordinates.lean::tomographicEquiv_unique`,
`lean4/TensorCoordinates.lean::product_calibration`, `lean4/TensorCoordinates.lean::finite_frame_calibration`,
`lean4/TensorComposition.lean::unit_test_is_trace`, for arbitrary finite local index types. Lean uses
an arbitrary local basis. The explicit projector basis and the SEP/BP inclusions above are not
in Lean.

---

## 2. The state cone

### 2.1 A cone fixed by seeds and transports

DAG node: `TENSOR-CONE-ORBIT-KERNEL`

**Proposition.** Let $K\subseteq\mathrm{Herm}(d)$ contain $0$ and be closed under addition. Let
$S\subseteq\mathbb C^d$ be a set of seed vectors and $\mathcal G$ a set of operations, each with a
forward map $F_g$ and a backward map $B_g$ on $\mathrm{Herm}(d)$ and an action $s\mapsto gs$ on
vectors, such that:

1. $ss^*\in K$ and $s^*Xs\ge0$ for every $s\in S$ and $X\in K$;
2. $F_g$ and $B_g$ map $K$ into $K$;
3. $F_g(ss^*)=(gs)(gs)^*$ and $s^*B_g(X)s=(gs)^*X(gs)$;
4. every $v\in\mathbb C^d$ equals $gs$ for some $g\in\mathcal G$ and $s\in S$.

Then $K=\mathrm{PSD}(d)$.

*Proof.* For $X\in K$ and $v=gs$, $v^*Xv=s^*B_g(X)s\ge0$, so $X\ge0$. Conversely
$vv^*=F_g(ss^*)\in K$ for every $v$. Every $P\ge0$ is a finite sum of rank-one terms $vv^*$ (from
a Gram factorization $P=B^*B$, taking the conjugated rows of $B$), so $P\in K$. $\square$

No closure or limit is used. Seeds may be unnormalized, and $v=0$ is allowed.

Lean: `lean4/TensorConeReconstruction.lean::operational_orbit_selects_positive`,
`lean4/TensorConeReconstruction.lean::positive_mem_of_rankOne`, for every finite size. The Gram
factorization uses Mathlib's finite complex matrix order theory.

### 2.2 One calibrated controlled shift forces PSD

DAG node: `TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION`

Let $1\le n\le m$; the smaller system is the control. Assume the hypotheses of §1.1, a state cone
$K$ closed under finite sums and nonnegative scaling, nonnegative test probabilities, and local
unitaries acting by $U\otimes V$-conjugation. Assume also an available reversible transformation,
with an available inverse, whose probability table on the product projector bases of §1.1 equals
that of $C|a,b\rangle=|a,(a+b)\bmod m\rangle$.

**Theorem.** $J(K)=\mathrm{PSD}(nm)$, and the normalized states are the trace-one positive
matrices.

*Proof.* $C$ is a permutation of basis vectors, hence unitary. By the calibration remark in §1.1,
the physical gate acts on coordinates as $X\mapsto CXC^*$, and its inverse acts as
$X\mapsto C^*XC$. Local unitaries act by conjugation in the same way.

*Reachability.* Let $\psi\in\mathbb C^n\otimes\mathbb C^m$. The singular value decomposition of its
$n\times m$ coefficient matrix gives $\psi=\sum_{i<n}s_i\,u_i\otimes v_i$ with $s_i\ge0$ and
orthonormal families $(u_i)$ and $(v_i)$. Complete them to bases, and let $U|i\rangle=u_i$ and
$V|i\rangle=v_i$. With $\alpha=\sum_is_i|i\rangle$,
$$C(\alpha\otimes|0\rangle)=\sum_is_i|i,i\rangle,\qquad (U\otimes V)\,C(\alpha\otimes|0\rangle)=\psi .$$
So every vector is $R(\alpha\otimes|0\rangle)$ for $R=(U\otimes V)C$ and a local product seed.

Apply §2.1 with these seeds and operations. The seed $\alpha\alpha^*\otimes|0\rangle\langle0|$ is a
product preparation. The test $\alpha\alpha^*\otimes|0\rangle\langle0|$ is a product test and has a
nonnegative probability on every state. The forward map is conjugation by $R$, and the backward
map, conjugation by $R^*$, is available by reversibility. Both preserve $J(K)$. §2.1 gives
$J(K)=\mathrm{PSD}(nm)$, and normalization is $\operatorname{tr}=1$ by §1.1. $\square$

So the composite is identified with $(\mathrm{Herm}(nm),\mathrm{PSD}(nm),\operatorname{tr})$ with
$(A,B)\mapsto A\otimes B$. Any two composites satisfying the hypotheses are identified with each
other through their maps $J$. Only one coherent interaction is assumed. The availability of all
global unitaries is not assumed. The calibration is a table of $n^4m^4$ exact probabilities, and
the classical truth table of $C$ is not enough (§4.1).

Lean: `lean4/TensorSchmidt.lean::exists_schmidt_bases`, `lean4/TensorReachability.lean::exists_schmidt_coefficients`,
`lean4/TensorReachability.lean::schmidt_reachability`, `lean4/TensorOperationalCone.lean::controlled_shift_selects_positive`,
`lean4/TensorComposition.lean::quantum_state_cone`, `lean4/TensorComposition.lean::unit_test_is_trace`.
Lean constructs rectangular Schmidt bases, the local unitaries and the modular shift.

---

## 3. Effects and measurements

Each linear effect $f$ on $V$ has a unique Hermitian representative $E$ with
$f(x)=\operatorname{tr}(E\,J(x))$, by nondegeneracy of the trace pairing. The unit test is
represented by $I$, and a product test by $E\otimes F$.

### 3.1 Valid effects are the interval $[0,I]$

DAG node: `TENSOR-BINARY-EFFECT-INTERVAL`

**Proposition.** With $J(K)=\mathrm{PSD}$, an effect satisfies $0\le f(x)\le\operatorname{tr}J(x)$
for all $x\in K$ if and only if $0\le E\le I$. Equivalently, $\operatorname{tr}(E\rho)\in[0,1]$ for
every density matrix $\rho$. If the available binary effects are sound and, in addition, every valid
effect is available ("effect saturation"), then the available binary effects are exactly
$[0,I]$.

*Proof.* PSD is self-dual for the trace pairing. If $A,B\ge0$, then
$\operatorname{tr}(AB)=\operatorname{tr}(B^{1/2}AB^{1/2})\ge0$. Conversely, if
$\operatorname{tr}(EP)\ge0$ for all $P\ge0$, then $v^*Ev=\operatorname{tr}(E\,vv^*)\ge0$ for every
$v$. Apply this to $E$ and to $I-E$. For the normalized form, the case $x=0$ is trivial, and a
nonzero positive matrix has positive trace, so it can be rescaled to trace one. Soundness gives one
inclusion. Saturation gives the other. $\square$

Saturation is a separate no-restriction premise. It does not follow from the state cone or from
§3.2.

Lean: `lean4/TensorEffectOrder.lean::binary_iff_bounds`, `lean4/TensorEffectOrder.lean::binary_iff_interval`,
`lean4/TensorEffectOrder.lean::binary_iff_normalized`, `lean4/TensorMeasurements.lean::effectRepresentation`,
`lean4/TensorMeasurements.lean::effectRepresentation_unit`, `lean4/TensorMeasurements.lean::effectRepresentation_product`,
`lean4/TensorMeasurements.lean::validEffect_iff_binary`, `lean4/TensorMeasurements.lean::available_effects_eq_interval`.

### 3.2 The generated effect cone is PSD

DAG node: `TENSOR-GENERATED-EFFECT-CONE`

**Proposition.** Assume the available effects are sound and every product of local binary effects
is available. Assume also that the available effects are closed under pullback along the local
unitaries, the controlled shift and their inverses, that is, under $E\mapsto R^*ER$ for each of
these $R$. Then the conic hull of the available
effects (finite nonnegative combinations) is $\mathrm{PSD}(nm)$. No saturation premise is used.

*Proof.* By §3.1, every available effect is positive, so the hull lies in PSD. Every $A\ge0$ is a
positive multiple of a binary effect: with $r=\|A\|+1$, $0\le A/r\le I$. So every product
$aa^*\otimes bb^*$ of local rank-one matrices lies in the hull. Conjugation by $C$ and by local
unitaries carries the product $\alpha\alpha^*\otimes|0\rangle\langle0|$ to $\psi\psi^*$ for
$\psi=(U\otimes V)C(\alpha\otimes|0\rangle)$. By the reachability of §2.2, every rank-one
$\psi\psi^*$ arises this way, and conjugation respects sums and nonnegative scaling. Finite sums of rank-one matrices give all
of PSD. $\square$

Equality of the hull with PSD does not say which elements of $[0,I]$ are individually available.
That is §3.1 with saturation.

Lean: `lean4/TensorEffectOrder.lean::positive_iff_pairing`, `lean4/TensorEffectOrder.lean::positive_ray_binary`,
`lean4/TensorEffectCone.lean::effect_cone_eq_positive`, `lean4/TensorMeasurements.lean::operational_effect_cone`.

### 3.3 Finite tests are POVMs

DAG node: `TENSOR-FINITE-POVM-AVAILABILITY`

**Proposition.** Let $O$ be a finite outcome set. A sound available test (available outcome effects
summing to the unit) is represented by a POVM, a family $E_o\ge0$ with $\sum_oE_o=I$. Assume effect
saturation, and also that every finite family of available effects summing to the unit is jointly
available ("finite-test saturation"). Then every POVM is an available test.

*Proof.* Forward: each $E_o\ge0$ by §3.1, and the representation is linear, so the sum of the
outcomes represents $I$. Reverse: for a POVM, $0\le E_o\le\sum_{o'}E_{o'}=I$, so each $E_o$ is a
valid effect and is available by effect saturation. The family is then jointly available by
finite-test saturation. $\square$

The two saturation premises are independent requirements, and both are stated. The end-to-end
statement combines §2.2 with §§3.1–3.3. Instruments, post-measurement states and channels are
not classified.

Lean: `lean4/TensorMeasurements.lean::povm_binary`, `lean4/TensorMeasurements.lean::test_povm_of_sound`,
`lean4/TensorMeasurements.lean::test_iff_povm`, `lean4/TensorMeasurements.lean::quantum_measurements`.

---

## 4. Weakened hypotheses that fail

### 4.1 Countermodels

DAG node: `TENSOR-ASSUMPTION-COUNTERMODELS`

**Proposition.** (i) BP is the trace dual of SEP, and SEP, PSD and BP are each preserved by local
unitaries. For $n,m\ge2$ they are distinct: there is $B\in\mathrm{PSD}\setminus\mathrm{SEP}$ and
$W\in\mathrm{BP}\setminus\mathrm{PSD}$. So tomography together with local reversibility does not
select the state cone. (ii) SEP is not closed under the controlled shift, and BP is not closed
under its inverse. (iii) The cone $\Gamma(\mathrm{PSD})$, where $\Gamma$ is the partial transpose on
the first factor, is self-dual and locally invariant. It admits a reversible "twisted" controlled
shift with the same classical truth table as $C$, and the two are separated by a coherent product
test. Dephasing after $C$ also has the same truth table, is not reversible, and is separated by a
coherent product test. (iv) Without local tomography, $V=\mathrm{Herm}(d)\times\mathrm{Herm}(d)$
with cone $\mathrm{PSD}\times\mathrm{PSD}$ has distinct normalized states with identical product
statistics.

*Proof.* (i) $X\in\mathrm{BP}$ means $\operatorname{tr}(X\,aa^*\otimes bb^*)\ge0$ for all $a,b$.
Since every positive local matrix is a sum of rank-one terms, this is nonnegative pairing with
SEP. Local unitaries map product positive matrices to product positive matrices, so SEP is
preserved, and BP is preserved by duality. For two qubits, let
$B=\frac12|00+11\rangle\langle00+11|$ and $W=\Gamma(B)$. The partial transpose sends
$|ij\rangle\langle kl|$ to $|kj\rangle\langle il|$, so $W=\frac12\,\mathrm{SWAP}$. Then $B\ge0$, and
$\langle01-10|W|01-10\rangle=-1$, so $W\notin\mathrm{PSD}$. Also $W\in\mathrm{BP}$, since
$\operatorname{tr}(\Gamma(B)\,P\otimes Q)=\operatorname{tr}(B\,P^{\mathsf T}\otimes Q)\ge0$. And
$B\notin\mathrm{SEP}$, because $\Gamma$ maps SEP into PSD and $\Gamma(B)=W$ is not positive. The
isometric embedding $\mathbb C^2\otimes\mathbb C^2\hookrightarrow\mathbb C^n\otimes\mathbb C^m$
carries these witnesses to every $n,m\ge2$.
(ii) $C$ maps the separable $|+\rangle\langle+|\otimes|0\rangle\langle0|$ to $B$. Conjugating $W$
by $C^*$ and testing on the product vector $|-\rangle\otimes|1\rangle$, unnormalized, gives $-1$.
(iii) $\Gamma$ is a real linear involution preserving trace and the trace pairing, so
$\Gamma(\mathrm{PSD})$ is self-dual. Since
$\Gamma\circ\mathrm{Ad}_{U\otimes V}=\mathrm{Ad}_{\bar U\otimes V}\circ\Gamma$, the cone is locally
invariant, and $\Gamma\,\mathrm{Ad}_C\,\Gamma$ preserves it, with inverse
$\Gamma\,\mathrm{Ad}_{C^*}\,\Gamma$. Both shifts agree on computational-basis inputs. On the input
$|+\rangle\langle+|\otimes|0\rangle\langle0|$, the product test $|{+i}\rangle\langle{+i}|^{\otimes2}$
gives $0$ after $C$ and $\frac12$ after the twisted shift. The ordinary shift leaves the twisted
cone, since it produces $B$, and $\Gamma(B)=W$ is not positive. For the dephased shift, the test
$|+\rangle\langle+|^{\otimes2}$ gives $\frac12$ before dephasing and $\frac14$ after, and dephasing
is not injective. (iv) Prepare $\pi(A,B)=\frac12(A\otimes B,\,A\otimes B)$ and test
$\tau(E,F)(X,Y)=\operatorname{tr}((E\otimes F)(X+Y))$. Then $(\rho,0)$ and $(0,\rho)$ agree on
every product test but are distinct, and the first-summand trace separates them. $\square$

The twisted cone is order-isomorphic to PSD via $\Gamma$, so (iii) shows that the calibration must
be coherent. It does not exhibit an inequivalent theory. The identical-qubit reconstruction of de la
Torre, Masanes, Short and Müller is an external theorem and is not used.

Lean: `lean4/TensorPartialTranspose.lean::gamma`, `lean4/TensorPartialTranspose.lean::pairing_gamma_gamma`,
`lean4/TensorPartialTranspose.lean::gamma_conjMap_product`, `lean4/TensorPartialTranspose.lean::conjMap_inverse`,
`lean4/TensorCountermodelCones.lean::blockPositive_iff_dual_sep`, `lean4/TensorCountermodelCones.lean::sep_ppt`,
`lean4/TensorCountermodelCones.lean::twisted_self_dual`, `lean4/TensorCountermodelCones.lean::sep_local`,
`lean4/TensorCountermodelCones.lean::bp_local`, `lean4/TensorCountermodelCones.lean::twisted_local`,
`lean4/TensorCountermodelCones.lean::twist_reversible`, `lean4/TensorCountermodelCones.lean::binary_product_statistics_separate`,
`lean4/TensorCountermodelWitnesses.lean::sep_fails_controlled_shift`,
`lean4/TensorCountermodelWitnesses.lean::bp_fails_inverse_controlled_shift`,
`lean4/TensorCountermodelWitnesses.lean::twisted_fails_ordinary_calibration`,
`lean4/TensorCountermodelWitnesses.lean::twisted_same_classical_table`,
`lean4/TensorCountermodelWitnesses.lean::coherent_calibration_separates`,
`lean4/TensorCountermodelWitnesses.lean::dephased_same_classical_table`,
`lean4/TensorCountermodelWitnesses.lean::dephased_controlled_shift_not_injective`,
`lean4/TensorCountermodelWitnesses.lean::dephased_coherent_calibration_separates`,
`lean4/TensorCountermodelEmbeddings.lean::cone_separations_all_dimensions`,
`lean4/TensorHiddenCoordinates.lean::hidden_normalized_states`,
`lean4/TensorHiddenCoordinates.lean::no_local_tomography`.
