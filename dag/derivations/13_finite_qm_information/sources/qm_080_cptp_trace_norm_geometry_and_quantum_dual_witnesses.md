# CPTP-Compatible Obstruction Theory: Trace-Norm Geometry and Quantum Dual Witnesses

## GTOC Foundations — Quantum Contact Series (qm_080_cptp_trace_norm_geometry_and_quantum_dual_witnesses)

**Version:** v1.2, republication candidate · **Date:** June 2026

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

**Published:** v1.1, 5 June 2026, Zenodo, DOI 10.5281/zenodo.20550459

**Authority:** `AuthorityEffect::None`

> **Title correction pending republication.** The published record is
> titled *CPTP-Invariant Obstruction Theory*. That adjective is wrong by
> this paper's own account: CPTP monotonicity is necessary for the
> trace-distance gauge and **not sufficient to select it**, as the
> abstract of the published record itself states. The corrected title is
> the one above. Until v1.2 is uploaded, cite the published title and
> this correction together.

## Mechanism inventory

| Slot | Value / Description |
| --- | --- |
| **Primitive Differences** | $\delta c = \text{{defect mass}}$ |
| **Carriers / Structure** | Finite Graph 0-Cochain / Hilbert Space |
| **Cochain complex** | $C^0 \to C^1 \to C^2$ |
| **Coboundary maps** | $\delta^0, \delta^1$ |
| **ZeroRel** | Preserved under $L_1$ quotient |
| **Licensed repairs** | None |
| **Quotient / Q1** | Banach Quotient |
| **Residuals** | $\delta c \neq 0$ boundary defect |
| **Witnesses** | Replayable Python / Rust Certifiers |
| **Observers / profiles** | Operational Observer |
| **Anomalons** | None |
| **CompletionLaw** | Finite Cochain Completion |
| **Terminal / route** | Route to 003 Quantum Foundations |
| **AuthorityEffect** | None |

The earlier title said “CPTP-Invariant”. That is **superseded**: the corrected claim is CPTP-compatible, equivalently data-processing monotone. CPTP monotonicity alone does not select the trace-distance gauge.

This paper identifies $\ell^1(E; \text{trace norm})$ as the obstruction geometry for replica-extensive observers whose local gauge is the operational trace distance. **[INTERPRETIVE / PROVEN BY COUNTEREXAMPLE after normalization caveat]** CPTP monotonicity is necessary for this choice but not sufficient to make it unique; uniqueness requires additional operational assumptions. Binary discrimination is the standard operational motivation and normalization anchor for trace distance [6]. In the proof of Theorem 1, the load-bearing selection axiom is classical total-variation reduction.

**Author:** Jeremy H. Carroll
**Date:** June 2026
**Version:** v1.2
**Status:** republication candidate / quantum observer-geometry branch paper
**Authority:** none.
**Scope:** conditional finite-dimensional trace-distance obstruction geometry.
**Main claim:** trace-distance local gauge plus replica-extensive edge aggregation yields $\ell^1(E;\mathrm{trace})$, with quotient dual witnesses given by divergence-free observable circulations bounded in the trace-distance dual norm.
**Non-claim:** CPTP monotonicity alone does not select the trace norm; no derivation of quantum mechanics, Born rule, or universal quantum metric is claimed.
**Mechanization:** MECHANIZED (ENC-0225: `lean4/research_programs/quantum_foundations/003_qm_trace_zero_duality.lean`, `lean4/shared_kernel/primitive_difference.lean`; `TraceZeroDuality.signWitness_value`)

> **Demotion (per corpus audit):** CPTP monotonicity is **CPTP-compatible**, not
> CPTP-selecting. CPTP monotonicity is *necessary* but *not sufficient* to make
> the trace norm unique; uniqueness requires the additional operational axioms of
> Theorem 1 (cf. the $\ell^1$ obstruction framework paper, the M-compatible gauge paper). No claim that "CPTP
> selects the trace norm" is asserted by this paper.

> **What this does not claim.**
> This paper does not claim that CPTP monotonicity alone selects trace norm, that trace norm is the universal quantum metric, that quantum mechanics or the Born rule is derived, or that all quantum distinguishability measures are norms. It claims only that, once trace distance is selected by explicit operational assumptions and edge aggregation is replica-extensive, the finite obstruction geometry is $\ell^1(E;\mathrm{trace})$, with quotient dual witnesses given by divergence-free bounded observables modulo identity components.

**Authority:** none. This paper may diagnose, price, route, or construct structure inside a declared obstruction regime. It does not mint authority. Any authority-bearing use requires a separate CODA-FDA / GTLA descent packet, terminalizer, evidence ceiling, replay witness, and `IsAuth` guard.

**Import / Oracle boundary.** Any use of Hilbert space, Born uniqueness, phase, continuum, probability semantics, dynamics, physical interpretation, tensor composition, or empirical realization is an imported representation structure unless explicitly constructed at this paper's declared degree. Imported structures are not DDA operations and do not produce authority.

> **This paper is import-dense, and the imports are premises, not results.** Its title names four
> imported structures (CPTP maps, trace norm, density operators, "quantum"). None of them is
> constructed here: this paper *borrows* the quantum representation and asks what obstruction
> geometry an observer inside it sees. The non-claims above say the paper does not derive quantum
> mechanics *outward*; this block says what it assumes *inward*. Both are required. The concrete
> register, and the split between what is derived at this degree and what is imported, are in the
> GTOC / GTLA Compliance Note before the References.

Abstract

This preprint develops the trace-distance branch of the finite obstruction program for quantum edge defects. Under explicit operational assumptions selecting the local trace-distance gauge, and under replica-extensive edge aggregation, the resulting obstruction geometry is $\ell^1(E;\mathrm{trace})$. The quotient obstruction admits a finite-dimensional dual formulation in terms of divergence-free observable circulations bounded in the trace-distance dual norm. The result is conditional on the declared observer class. CPTP monotonicity is necessary for operational compatibility but does not by itself select the trace norm.

**Why a researcher should care.** Quantum networks, open-system channels, variational quantum models, and quantum error diagnostics all compare local quantum states or state differences. The choice of local distinguishability gauge changes the resulting obstruction geometry. This paper isolates the finite observer regime in which the trace-distance gauge is licensed: not by CPTP monotonicity alone, but by explicit operational assumptions such as unitary invariance, classical total-variation reduction, and binary-discrimination normalization. Once that local gauge is selected, the finite obstruction problem has a concrete dual: bounded observable circulations certify the remaining quotient defect.

1. Introduction and Structural Placement

This paper is the CPTP-symmetry instance of the M-compatible gauge classification program (the M-compatible gauge paper). It maps how CPTP-symmetry constraints, together with operational axioms, specify trace-distance geometry inside the replica-extensive $\ell^1$ observer framework. It does not propose a universal quantum metric.

The rigorous categorical classification of diagnostic geometries formalizes that structural obstruction constraints intrinsically adapt upon mapping across distinct physical regimes. The corpus-baseline scalar mapping (the coordinate-wise additivity paper) derives precisely from requiring full maximal contraction mapping independently over decoupled fields (the M-compatible gauge paper). For classical scalar networks under maximal bounded-linear contraction, the classification yields uniform $\ell^1$ evaluation (the finite obstruction framework). For architectures with rotational symmetry $\mathrm{SO}(k)$, the metric reduces to the mixed Euclidean geometry $\ell^1(E; \ell^2)$ (the $\mathrm{SO}(k)$-invariant mixed-norm paper).

Extending this geometry to evaluating quantum mechanical network fields demands mapping local topological discrepancy data onto the state space of density matrices. In this context, nodes represent isolated quantum sub-systems or spatial points, and directed graph connections parameterize expected causal or spatial transport channels. A physical network evaluating quantum failures must specify which operational distinguishability gauge it uses; CPTP monotonicity alone does not make that choice unique.

This imposes CPTP contraction as a necessary compatibility condition. The trace norm becomes the selected gauge only after the additional operational assumptions in Theorem 1 are imposed.

### Genesis-Bias Fence — No Prior Physical Host

The preceding paragraph is written in the vocabulary of a pre-existing physical world: a "state
space of density matrices", nodes that "represent isolated quantum sub-systems or spatial points",
and edges that "parameterize expected causal or spatial transport channels". **That world is an
imported antecedent, and it is priced here rather than presupposed.** This paper does not
construct a state space, a Hilbert space, a spatial manifold, a causal order, a physical system,
or an observer. It borrows them.

What the paper actually begins with is packet-local and finite: a finite directed graph $G=(V_G,E)$
and a finite-dimensional real vector space $V$ carrying a gauge $j$. Nodes are index positions in
the declared packet; edges are declared comparison sites. Neither is a place, a particle, or a
moment. The trace-distance gauge, the Hermitian trace-zero realization of $V$, and the CPTP
compatibility condition are all *specializations* of that finite datum, admitted from the imported
quantum representation.

The dependency runs one way, and it is worth being exact about which way. §2.3, §2.5, and §2.7
(Theorems 3, 4, 6) never touch $\mathcal H$: they hold for a finite digraph valued in *any*
finite-dimensional normed real vector space, and their proofs are a change of variables and a
compactness argument. Only §2.2 and §2.3 (Theorems 1 and 2) use the imported representation — the
spectral theorem, CPTP maps, density matrices, and the tensor product. **The physical reading is
therefore an interpretive layer over a finite result, not the ground the result stands on.** It is
retained because it is what motivates the specialization and what a reader in quantum information
will want; it is not load-bearing, and it licenses nothing.

> **GENESIS-BIAS AUDIT.** Does this section explain quantum edge defects by presupposing a prior
> container, substrate, state-space, law, observer, temporal order, possibility domain, sample
> space, Hilbert space, physical system, or authority source? **Yes — and all of them are declared
> as imports in the Compliance Note before the References rather than replaced.** Removing them
> costs the paper its motivation and its selection axioms (Theorem 1), but not Theorems 3, 4, or 6.
> No packet-local reconstruction of the quantum host is attempted, and none is claimed.

**Falsifiability.** A proposed use of this paper fails if it cannot specify finite-dimensional Hilbert spaces, Hermitian trace-zero edge defects, the local trace-distance gauge or the operational axioms selecting it, replica-extensive edge aggregation, the coboundary map $d_0$, and the quotient convention for identity components in dual observables. The duality theorem fails if a finite counterexample satisfies the primal quotient problem but violates the stated divergence-free quotient-operator-norm dual formula.

1.1 Related Work and Positioning

This paper is closest to five bodies of work:

1. **Quantum trace distance and operational distinguishability.** Trace distance is the standard finite-dimensional distinguishability gauge for binary state discrimination [6]. This paper differs by using that operational gauge as a declared local observer geometry for obstruction cochains.

2. **Data processing and CPTP monotonicity.** CPTP maps cannot increase trace distance between quantum states [7]. This paper differs by emphasizing that this monotonicity is necessary compatibility, not a uniqueness theorem for trace norm.

3. **Convex duality and operator-norm duality.** The dual of the trace norm is the operator norm [7]. This paper differs by applying that duality edgewise on the trace-zero subspace modulo the identity, and adding the divergence-free condition $d_0^*M=0$.

4. **Finite cochain quotient obstruction theory.** The quotient obstruction $\Phi_{\mathrm{tr}}$ is the trace-distance instance of a finite quotient-norm construction over graph cochains [1]. This paper differs by specializing the local stalks to Hermitian trace-zero operators.

5. **M-compatible gauge classification.** The paper is a quantum branch of the M-compatible observer-geometry program [3]. It differs from the maximal bounded-linear and $\mathrm{SO}(k)$ branches by using operational quantum distinguishability assumptions rather than full linear or rotational symmetry. This paper develops the full CPTP observer geometry for the boundary example in [3, §3.6 / Ex 3.6].

These references are positioning anchors. Do not cite external sources as theorem support unless the exact theorem is verified.

### 1.2 Notation

| Symbol               | Meaning                                |
| -------------------- | -------------------------------------- |
| $\mathcal H$         | finite-dimensional Hilbert space       |
| $V$                  | Hermitian trace-zero operator space    |
| $\|X\|_{\mathrm{tr}}$| $\frac12\|X\|_1$, trace-distance gauge |
| $G=(V_G,E)$          | finite directed graph                  |
| $\delta_e$           | quantum edge defect                    |
| $J_{\mathrm{tr}}$    | edge-sum trace diagnostic              |
| $\Phi_{\mathrm{tr}}$ | quotient obstruction                   |
| $M_e$                | dual observable witness                |
| $d_0^*M=0$           | divergence-free observable circulation |

2. The Trace-Norm Geometry and Quotient Obstruction Proofs

### 2.1 Setup

Let $\mathcal H$ be finite-dimensional.

Let
**[DEFINITION]**
$$
V = \{X\in B(\mathcal H): X=X^\dagger,\ \operatorname{Tr}X=0\}
$$

be the real vector space of Hermitian trace-zero operators.

For $X\in V$, define the trace-distance gauge
**[DEFINITION / STANDARD NORMALIZATION]**
$$
\|X\|_{\mathrm{tr}} := \frac12\|X\|_1 = \frac12\operatorname{Tr}|X|.
$$

For a finite directed graph $G=(V_G,E)$, a quantum 1-cochain is

$$
\delta\in C^1(G,V), \qquad \delta_e\in V.
$$

The global trace diagnostic is

$$
J_{\mathrm{tr}}(\delta) = \sum_{e\in E}\|\delta_e\|_{\mathrm{tr}}.
$$

### 2.2 **[PROVEN, CONDITIONAL + unitary invariance + classical total-variation reduction + homogeneity] Theorem 1 — Trace-Distance Identification Under Operational Normalization**

**Statement:**

Let

$$
j_n:V_n\to\mathbb R_{\ge0}
$$

be a family of local gauges on finite-dimensional Hermitian trace-zero operator spaces. Suppose:

1. **Norm structure.**
   $j_n$ is faithful, convex, absolutely homogeneous, and subadditive.

2. **CPTP monotonicity.**
   For every CPTP map $\Lambda:B(\mathcal H_n)\to B(\mathcal H_m)$,

   $$
   j_m(\Lambda X)\le j_n(X).
   $$

3. **Unitary invariance.**

   $$
   j_n(UXU^\dagger)=j_n(X).
   $$

4. **Tensor stability.**

   $$
   j_{nk}(X\otimes\rho)=j_n(X)
   $$

   for every density matrix $\rho$.

5. **Classical total-variation reduction.**
   For every diagonal trace-zero operator

   $$
   X=\operatorname{diag}(r), \qquad \sum_i r_i=0,
   $$

   one has

   $$
   j_n(X)=\frac12\|r\|_1.
   $$

Then

$$
j_n(X)=\frac12\|X\|_1
$$

for every Hermitian trace-zero $X$.

CPTP monotonicity and tensor stability are observer-compatibility requirements. They are not load-bearing in the finite spectral identification once unitary invariance and classical total-variation reduction are assumed.

**Proof:**

Let $X\in V_n$. Since $X$ is Hermitian, it admits a spectral decomposition

$$
X=U\operatorname{diag}(\lambda)U^\dagger,
$$

where

$$
\lambda=(\lambda_1,\ldots,\lambda_n), \qquad \sum_i\lambda_i=0.
$$

By unitary invariance,

$$
j_n(X) = j_n(\operatorname{diag}(\lambda)).
$$

Now $\operatorname{diag}(\lambda)$ is a diagonal trace-zero operator. By classical total-variation reduction,

$$
j_n(\operatorname{diag}(\lambda)) = \frac12\|\lambda\|_1.
$$

But for Hermitian $X$, the trace norm is the $\ell^1$-norm of the eigenvalue vector:

$$
\|X\|_1=\|\lambda\|_1.
$$

Therefore,

$$
j_n(X) = \frac12\|\lambda\|_1 = \frac12\|X\|_1.
$$

Hence $j_n$ is exactly the trace-distance gauge. $\square$

> **Audit note.** The displayed finite-dimensional uniqueness proof uses unitary invariance and classical total-variation reduction directly (plus $\|X\|_1=\|\lambda\|_1$ for Hermitian $X$); homogeneity is used only in the alternative differences-of-distributions note above. CPTP monotonicity and tensor stability are retained as operational compatibility axioms for the observer family, but they are not load-bearing in the spectral reduction step.

**Note on the classical reduction axiom:**

If one wants the classical reduction axiom stated only for differences of probability distributions,

$$
X=\operatorname{diag}(p-q),
$$

then the proof still works.

Given any trace-zero $\lambda$, write

$$
\lambda=\lambda^+-\lambda^-,
$$

where $\lambda^+,\lambda^-\ge0$ have disjoint support and equal total mass

$$
t=\|\lambda^+\|_1=\|\lambda^-\|_1.
$$

If $t=0$, then $\lambda=0$. Otherwise define

$$
p=\frac{\lambda^+}{t}, \qquad q=\frac{\lambda^-}{t}.
$$

Then

$$
\lambda=t(p-q).
$$

By homogeneity and classical reduction,

$$
j_n(\operatorname{diag}\lambda) = t\cdot j_n(\operatorname{diag}(p-q)) = t\cdot\frac12\|p-q\|_1.
$$

Since $\|p-q\|_1=2$,

$$
j_n(\operatorname{diag}\lambda)=t.
$$

Also

$$
\frac12\|\lambda\|_1 = \frac12(\|\lambda^+\|_1+\|\lambda^-\|_1) = \frac12(2t)=t.
$$

So again

$$
j_n(\operatorname{diag}\lambda) = \frac12\|\lambda\|_1.
$$

### 2.3 Theorem 2 — CPTP Monotonicity Is Necessary but Not Sufficient

**Statement:**

CPTP monotonicity is necessary for a quantum operational distinguishability gauge, but it does not uniquely select the trace norm.

**[INTERPRETIVE / AXIOMATIC] Proof: Necessity**

A physical open-system evolution is represented by a CPTP map $\Lambda$.

If ‘operational distinguishability gauge’ is defined to obey data processing under physical channels, then CPTP monotonicity is necessary by definition. Without that definition, this is an operational axiom, not a mathematical theorem.

**[PROVEN BY COUNTEREXAMPLE] Proof: Not sufficient**

CPTP monotonicity alone does not determine a unique gauge.

First, even within trace-norm geometry, for any scalar $c>0$,

$$
j_c(X)=c\|X\|_1
$$

is CPTP-monotone because the trace norm is CPTP contractive on Hermitian trace-zero differences:

$$
\|\Lambda X\|_1\le\|X\|_1.
$$

So

$$
j_c(\Lambda X) = c\|\Lambda X\|_1 \le c\|X\|_1 = j_c(X).
$$

CPTP monotonicity alone does not fix the trace-distance gauge as a normalized object: every positive scalar multiple of the trace norm is CPTP-monotone. Whether there exist non-proportional CPTP-monotone norms on Hermitian trace-zero operators is a separate strengthening target, tracked as PL-005-2.

Second, **[INTERPRETIVE / STANDARD + citation]** Other quantum distinguishability quantities are CPTP-monotone in appropriate senses, though many are not norms on the trace-zero vector space [7]. They are cited here only to show the breadth of the data-processing landscape, not as alternative gauges satisfying all norm axioms.

Therefore CPTP monotonicity is a compatibility requirement, not a selection theorem.

> **CPTP monotonicity restricts the gauge class; it does not select trace norm alone.** $\square$

### 2.4 **[PROVEN, CONDITIONAL / PARTLY DEFINITIONAL]** Theorem 3 — Global $\ell^1(E;\mathrm{trace})$ Geometry

**Statement:**

Assume:

1. the local quantum gauge is the trace-distance norm

$$
\|X\|_{\mathrm{tr}}=\frac12\|X\|_1;
$$

1. the observer is replica-extensive and edge-decomposable.

Then the general weighted global obstruction diagnostic is

$$
J_{\mathrm{tr},w}(\delta) = \sum_{e\in E} w_e\|\delta_e\|_{\mathrm{tr}}, \quad w_e > 0.
$$

The unweighted form $J_{\mathrm{tr}}(\delta) = \sum_{e\in E}\|\delta_e\|_{\mathrm{tr}}$ requires normalized unit edge weights, a single edge orbit, or an explicit edge-uniformity convention.

Equivalently, under uniform weights,

$$
C^1(G,V)
$$

is equipped with the mixed geometry

$$
\ell^1(E;|\cdot|_{\mathrm{tr}}).
$$

**Proof:**

If edge weights are declared, edge decomposability gives

$$
J(\delta)=\sum_{e\in E} w_e j(\delta_e),
$$

so Theorem 1 yields

$$
J_{\mathrm{tr},w}(\delta)=\sum_{e\in E} w_e\|\delta_e\|_{\mathrm{tr}}.
$$

The unweighted expression is the normalized case $w_e=1$, or follows from a single edge orbit / explicit edge-uniformity convention. $\square$

### 2.5 **[PROVEN]** Theorem 4 — Trace-Norm Quotient Obstruction

**Statement:**

Let

$$
d_0:C^0(G,V)\to C^1(G,V)
$$

be the coboundary operator

$$
(d_0\alpha)_e=\alpha_{t(e)}-\alpha_{s(e)}.
$$

For $\delta\in C^1(G,V)$, define the quotient obstruction

$$
\Phi_{\mathrm{tr}}([\delta]) = \inf_{\alpha\in C^0(G,V)} \sum_{e\in E} \|\delta_e-(d_0\alpha)_e\|_{\mathrm{tr}}.
$$

Then $\Phi_{\mathrm{tr}}([\delta])$ depends only on the quotient class of $\delta$ modulo coboundaries.

**Proof:**

Let

$$
\delta'=\delta+d_0\beta
$$

for some $\beta\in C^0(G,V)$. Then

$$
\Phi_{\mathrm{tr}}([\delta']) = \inf_{\alpha} \sum_e |\delta_e+(d_0\beta)_e-(d_0\alpha)_e|_{\mathrm{tr}}.
$$

Set

$$
\alpha'=\alpha-\beta.
$$

Then

$$
d_0\alpha' = d_0\alpha-d_0\beta.
$$

So

$$
\delta+d_0\beta-d_0\alpha = \delta-d_0(\alpha-\beta) = \delta-d_0\alpha'.
$$

As $\alpha$ ranges over $C^0$, so does $\alpha'$. Therefore

$$
\Phi_{\mathrm{tr}}([\delta']) = \inf_{\alpha'} \sum_e |\delta_e-(d_0\alpha')_e|_{\mathrm{tr}} = \Phi_{\mathrm{tr}}([\delta]).
$$

Thus the obstruction is a quotient invariant. $\square$

### 2.6 **[PROVEN, finite-dimensional convex duality + S1]** Theorem 5 — Trace-Norm Quotient Duality

**Statement:**

The quotient obstruction admits the dual formulation

$$
\Phi_{\mathrm{tr}}([\delta]) = \max_M \sum_{e\in E} \operatorname{Tr}(M_e\delta_e)
$$

The maximization may be restricted to Hermitian observables $M_e=M_e^\dagger$, since only the Hermitian part contributes against Hermitian $\delta_e$. Identity components are annihilated on trace-zero defects and can be quotiented away if desired.

subject to:

1. **Divergence-free constraint**

$$
d_0^*M=0.
$$

1. **Dual observable bound, trace-distance convention:**

$$
\inf_{\lambda_e\in\mathbb R}\|M_e+\lambda_e I\|_{\mathrm{op}}\le\frac12.
$$

Equivalently, for Hermitian $M_e$,

$$
\lambda_{\max}(M_e)-\lambda_{\min}(M_e)\le1.
$$

One may choose a centered representative of each equivalence class with

$$
\|M_e\|_{\mathrm{op}}\le\frac12.
$$

If working on the full Hermitian space instead of trace-zero defects, or after fixing a centered representative convention, state that convention explicitly.

**Proof:**

Work in finite dimension, so strong duality holds for closed proper convex functions.

The primal is

$$
\Phi_{\mathrm{tr}}([\delta]) = \inf_{\alpha\in C^0} J_{\mathrm{tr}}(\delta-d_0\alpha),
$$

where

$$
J_{\mathrm{tr}}(\eta) = \sum_e\|\eta_e\|_{\mathrm{tr}}.
$$

We use the dual representation of the local trace-distance norm, computed in the following lemma.

**Lemma (Trace-zero dual ball).** Let $V=\{X=X^\dagger,\ \operatorname{Tr}X=0\}$ with primal norm $\|X\|_{\mathrm{tr}}=\frac12\|X\|_1$. The dual space is the quotient of Hermitian observables modulo the scalar identity, since $\operatorname{Tr}(cIX)=c\operatorname{Tr}(X)=0$. Writing $\operatorname{diam}(M)=\lambda_{\max}(M)-\lambda_{\min}(M)$, the dual norm of the class $[M]$ of a Hermitian $M$ is
$$
\|[M]\|^* = \max_{X\in V,\ \|X\|_{\mathrm{tr}}\le1}\operatorname{Tr}(MX) = \operatorname{diam}(M) = 2\inf_{\lambda\in\mathbb R}\|M+\lambda I\|_{\mathrm{op}}.
$$
*Proof.* Let $M_c=M-\tfrac12\bigl(\lambda_{\max}(M)+\lambda_{\min}(M)\bigr)I$ be the centered representative, so $\|M_c\|_{\mathrm{op}}=\tfrac12\operatorname{diam}(M)$ and $\operatorname{Tr}(M_cX)=\operatorname{Tr}(MX)$ for every $X\in V$ (as $\operatorname{Tr}(X)=0$).

*(Upper bound.)* For $\|X\|_{\mathrm{tr}}\le1$, i.e. $\|X\|_1\le2$, the operator-norm/trace-norm duality $|\operatorname{Tr}(AB)|\le\|A\|_{\mathrm{op}}\|B\|_1$ gives
$$
\operatorname{Tr}(MX)=\operatorname{Tr}(M_cX)\le\|M_c\|_{\mathrm{op}}\,\|X\|_1\le\tfrac12\operatorname{diam}(M)\cdot2=\operatorname{diam}(M).
$$

*(Attainment.)* Diagonalize $M=U\operatorname{diag}(\mu)U^\dagger$ and let $i^\ast,j^\ast$ index $\mu_{\max},\mu_{\min}$. Then $X=U\bigl(e_{i^\ast}e_{i^\ast}^\dagger-e_{j^\ast}e_{j^\ast}^\dagger\bigr)U^\dagger\in V$ has $\|X\|_1=2$ (so $\|X\|_{\mathrm{tr}}=1$) and $\operatorname{Tr}(MX)=\mu_{\max}-\mu_{\min}=\operatorname{diam}(M)$.

Hence $\|[M]\|^*=\operatorname{diam}(M)$. Since $2\inf_\lambda\|M+\lambda I\|_{\mathrm{op}}=2\|M_c\|_{\mathrm{op}}=\operatorname{diam}(M)$, the dual unit ball is exactly $\{[M]:\inf_\lambda\|M+\lambda I\|_{\mathrm{op}}\le\tfrac12\}$ — equivalently spectral diameter $\le1$, equivalently $\|M_c\|_{\mathrm{op}}\le\tfrac12$ on the centered representative. $\square$

(Note: the maximization is over the trace-zero subspace $V$; on $V$ it equals $\operatorname{diam}(M)$, which is strictly below the all-Hermitian value $2\|M\|_{\mathrm{op}}$ unless $M$ is already centered. The $\inf_\lambda$ / centering is precisely what reconciles the two.)

The Lean result verifies the eigenvalue-level core. The matrix-level spectral lift is proved in prose and tracked as PL-005-1 for mechanization hardening.

**Formalization-status firewall.** Any Lean, Rust, or replay artifact cited here supports only the exact finite statement it mechanizes. It does not automatically discharge PL-GTOC, Q, continuum, physical-realization, or GTLA authority obligations. A status upgrade requires an explicit theorem-ledger mapping, hypotheses check, build receipt, axiom/sorry audit, and adversary acceptance. Concretely for this lemma: what is machine-checked is the **eigenvalue-level** identity for sum-zero real vectors. The step from that vector statement to the Hermitian-matrix statement is the spectral theorem, carried out in the prose above and **not** mechanized (PL-005-1). Nothing quantum, and nothing about CPTP, is mechanized anywhere in this paper.

By this lemma, for trace-zero Hermitian $X$,
$$
\frac12\|X\|_1 = \max_{\inf_\lambda\|M+\lambda I\|_{\mathrm{op}}\le1/2} \operatorname{Tr}(MX).
$$
Equivalently, maximize over centered Hermitian representatives with $\|M\|_{\mathrm{op}}\le1/2$.

Therefore, using centered representatives,

$$
J_{\mathrm{tr}}(\eta) = \sum_e \max_{\|M_e\|_{\mathrm{op}}\le1/2} \operatorname{Tr}(M_e\eta_e)
$$

and equivalently

$$
J_{\mathrm{tr}}(\eta) = \max_{\|M_e\|_{\mathrm{op}}\le1/2} \sum_e \operatorname{Tr}(M_e\eta_e).
$$

Substitute $\eta=\delta-d_0\alpha$:

$$
\Phi_{\mathrm{tr}}([\delta]) = \inf_\alpha \max_{\|M_e\|_{\mathrm{op}}\le1/2} \sum_e \operatorname{Tr}\bigl(M_e(\delta_e-(d_0\alpha)_e)\bigr).
$$

By Sion's minimax theorem [8] — the objective is bilinear, the $M$-ball $\{\|M_e\|_{\mathrm{op}}\le1/2\}$ is compact convex, and $\alpha\in C^0(G,V)$ ranges over a convex finite-dimensional space; compactness of the $M$-ball (not of the $\alpha$-space) licenses the swap — exchange infimum and maximum:

$$
\Phi_{\mathrm{tr}}([\delta]) = \max_{\|M_e\|_{\mathrm{op}}\le1/2} \left[ \sum_e\operatorname{Tr}(M_e\delta_e) + \inf_\alpha \left( -\sum_e\operatorname{Tr}(M_e(d_0\alpha)_e) \right) \right].
$$

The second term is finite if and only if $M$ annihilates the image of $d_0$:

$$
\sum_e\operatorname{Tr}(M_e(d_0\alpha)_e)=0 \quad \forall \alpha.
$$

This condition is exactly

$$
d_0^*M=0.
$$

If $d_0^*M\ne0$, one can scale $\alpha$ in the violating direction and the infimum becomes $-\infty$, so such $M$ contributes nothing to the maximum.

Thus the dual feasible set is

$$
\{M:\ d_0^*M=0,\ \|M_e\|_{\mathrm{op}}\le1/2\}.
$$

The objective is

$$
\sum_e\operatorname{Tr}(M_e\delta_e).
$$

Therefore

$$
\Phi_{\mathrm{tr}}([\delta]) = \max_{\substack{d_0^*M=0 \\ M_e\text{ centered} \\ \|M_e\|_{\mathrm{op}}\le1/2}} \sum_e \operatorname{Tr}(M_e\delta_e).
$$

$\square$

### 2.7 **[PROVEN, finite-dimensional]** Theorem 6 — Operator-Norm-Bounded Quantum Dual Witnesses

**Statement:**

A maximizer $M^*$ in the dual problem is a quantum dual witness for the obstruction class $[\delta]$. It satisfies:

$d_0^*M^*=0$, and $[M_e^*]$ lies in the quotient dual ball modulo identity components; after choosing centered representatives, $\|M_e^*\|_{\mathrm{op}}\le1/2$.

and

$$
\Phi_{\mathrm{tr}}([\delta]) = \sum_e\operatorname{Tr}(M_e^*\delta_e).
$$

Thus obstruction is detected by a divergence-free circulation of bounded quantum observables.

**Proof:**

Since the graph and Hilbert spaces are finite-dimensional, after choosing centered representatives of each observable class modulo scalar identity, define the feasible dual set

$$
\mathcal W=\{M:\ d_0^*M=0,\ M_e\text{ centered},\ \|M_e\|_{\mathrm{op}}\le1/2\}.
$$

Equivalently, without choosing representatives, require

$$
\inf_{\lambda_e\in\mathbb R}\|M_e+\lambda_e I\|_{\mathrm{op}}\le1/2.
$$

This set is closed and bounded, hence compact.

The objective

$$
M\mapsto\sum_e\operatorname{Tr}(M_e\delta_e)
$$

is continuous. Therefore a maximizer $M^*\in\mathcal W$ exists.

By feasibility,

$$
d_0^*M^*=0, \qquad \|M_e^*\|_{\mathrm{op}}\le1/2.
$$

By Theorem 5,

$$
\sum_e\operatorname{Tr}(M_e^*\delta_e) = \Phi_{\mathrm{tr}}([\delta]).
$$

Therefore $M^*$ is a dual witness attaining the quotient obstruction.

The divergence-free condition says that at every vertex, incoming and outgoing observable currents balance:

$$
\sum_{e:t(e)=v}M_e - \sum_{e:s(e)=v}M_e = 0.
$$

This sign convention corresponds to $(d_0\alpha)_e = \alpha_{t(e)} - \alpha_{s(e)}$.

So the witness is not a collection of arbitrary local observables; it is a globally compatible observable circulation. $\square$

### 2.8 Quantum $\Phi/W/R$ Signature

For the quantum trace-norm observer class, define the obstruction signature:

$$
\mathsf{Sig}_{\mathrm{qtr}}(\delta) = \left( \Phi_{\mathrm{tr}}([\delta]), W_{\mathrm{tr}}(\delta), R_{\mathrm{tr}}(\delta) \right).
$$

#### 1. $\Phi_{\mathrm{tr}}$: quotient obstruction magnitude

$$
\Phi_{\mathrm{tr}}([\delta]) = \inf_{\alpha\in C^0} \sum_e \|\delta_e-(d_0\alpha)_e\|_{\mathrm{tr}}.
$$

**Interpretation:**

> How much quantum distinguishability defect remains after all vertex-level coboundary repairs?

If

$$
\Phi_{\mathrm{tr}}([\delta])=0,
$$

then the defect is pure coboundary under the declared trace-distance observer. If

$$
\Phi_{\mathrm{tr}}([\delta])>0,
$$

then a nontrivial quantum obstruction remains.

**Detector adequacy warning.** A replayable detector/profile is not automatically adequate for a claim. A collapsing detector can make every profile exact. Any authority-bearing GTLA use requires a `DetectorAdequacy` certificate naming the protected distinctions, adversarial cases, and known blind spots for the declared claim scope.

This warning is not decorative here: $\Phi_{\mathrm{tr}}$ is a **quotient** norm, so it collapses
every coboundary to zero *by construction*. $\Phi_{\mathrm{tr}}([\delta])=0$ therefore does not say
"no defect"; it says "no defect survives vertex repair *as seen by this observer*". Two further
blind spots are structural, not incidental: the detector is edge-decomposable, so it cannot see any
defect that is not carried on a declared edge (the covering-edge restriction); and it is
replica-extensive, so it aggregates edge magnitudes and discards the relative orientation of
defects across edges. Whether the declared edge set protects the distinctions a given application
cares about is an **adequacy** question this paper does not answer for any application.

#### 2. $W_{\mathrm{tr}}$: dual witness circulation

**[DEFINITION]**
Define

$$
W_{\mathrm{tr}}(\delta) = \operatorname*{argmax}_{\substack{d_0^*M=0 \\ M_e\text{ centered} \\ \|M_e\|_{\mathrm{op}}\le1/2}} \sum_e \operatorname{Tr}(M_e\delta_e).
$$

**Interpretation:**

> The set of divergence-free bounded observable circulations that witness the obstruction.

Any

$$
M^*\in W_{\mathrm{tr}}(\delta)
$$

satisfies

$$
\Phi_{\mathrm{tr}}([\delta]) = \sum_e\operatorname{Tr}(M_e^*\delta_e).
$$

Thus $W_{\mathrm{tr}}$ is the observable certificate layer.

#### 3. $R_{\mathrm{tr}}$: residual after optimal repair

Define the residual set:

$$
R_{\mathrm{tr}}(\delta) := \operatorname*{argmin}_{r\in[\delta]} \sum_e\|r_e\|_{\mathrm{tr}}.
$$

In finite dimension, the distance from a point to the coboundary subspace is attained, so $R_{\mathrm{tr}}(\delta)$ is nonempty. If a representative is not selected, $R_{\mathrm{tr}}$ is set-valued.

A selected representative $r^*\in R_{\mathrm{tr}}(\delta)$ may be written as:

$$
r^*=\delta-d_0\alpha^*.
$$

**Interpretation:**

> The surviving edge-defect field after optimal vertex repair.

The residual satisfies

$$
J_{\mathrm{tr}}(R_{\mathrm{tr}})=\Phi_{\mathrm{tr}}([\delta])
$$

when a representative is chosen, or

$$
J_{\mathrm{tr}}(r)=\Phi_{\mathrm{tr}}([\delta]) \quad \forall r\in R_{\mathrm{tr}}(\delta)
$$

in the set-valued case.

### 2.9 **[PROVEN, CONDITIONAL on Theorem 1 operational axioms]** Final Consolidated Result

Under the operational assumptions listed in Theorem 1, with classical total-variation reduction providing the displayed normalization and binary discrimination cited as operational motivation if used, and assuming replica-extensive edge aggregation:

$$
J_{\mathrm{tr}}(\delta) = \sum_{e\in E} \frac12\|\delta_e\|_1
$$

and quotient obstruction:

$$
\Phi_{\mathrm{tr}}([\delta]) = \inf_{\alpha} \sum_e \frac12 \|\delta_e-(d_0\alpha)_e\|_1.
$$

Its dual witness form is:

$$
\Phi_{\mathrm{tr}}([\delta]) = \max_{\substack{d_0^*M=0 \\ M_e\text{ centered} \\ \|M_e\|_{\mathrm{op}}\le1/2}} \sum_e \operatorname{Tr}(M_e\delta_e).
$$

Thus the quantum obstruction signature is:

$$
\mathsf{Sig}_{\mathrm{qtr}}(\delta) = \left( \Phi_{\mathrm{tr}}([\delta]), W_{\mathrm{tr}}(\delta), R_{\mathrm{tr}}(\delta) \right).
$$

And the central non-claim remains essential:

> **CPTP monotonicity is necessary for operational compatibility, but it does not by itself select the trace norm.**

### Worked Replay — One-Qubit Cycle Obstruction and Dual Witness

Let the Hilbert space be $\mathbb C^2$, and let
$$
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
$$
$Z$ is Hermitian and trace-zero. Under the trace-distance convention,
$$
\|Z\|_{\mathrm{tr}}=\frac12\|Z\|_1=\frac12(2)=1.
$$

On a single directed cycle, take total cycle defect $S(\delta)=Z$. The quotient obstruction is
$$
\Phi_{\mathrm{tr}}([\delta])=\|S(\delta)\|_{\mathrm{tr}}=1.
$$
(The single-cycle formula is elementary: the cycle sum $S(r)=\sum_e r_e$ is invariant under coboundary repair on a consistently oriented cycle, so the triangle inequality gives $\sum_e\|r_e\|_{\mathrm{tr}}\ge\|S(\delta)\|_{\mathrm{tr}}$ for every representative $r\in[\delta]$; concentrating the whole defect on one edge attains the bound. Cf. the weighted version in the $\mathrm{SO}(k)$ paper [4], §5.)

A centered dual witness is
$$
M=\frac12 Z.
$$
Then
$$
\|M\|_{\mathrm{op}}=\frac12,
\qquad
\operatorname{Tr}(MZ)=\operatorname{Tr}\left(\frac12Z^2\right)=1.
$$
Thus the dual witness attains the primal obstruction.

Minimal replay:

```python
import numpy as np

Z = np.array([[1, 0], [0, -1]], dtype=float)
M = 0.5 * Z

trace_norm_Z = np.sum(np.abs(np.linalg.eigvalsh(Z)))
trace_distance_Z = 0.5 * trace_norm_Z
op_norm_M = np.max(np.abs(np.linalg.eigvalsh(M)))
dual_value = np.trace(M @ Z)

print(trace_distance_Z)
print(op_norm_M)
print(dual_value)
```

Expected output:

```text
1.0
0.5
1.0
```

This checks the factor-of-two convention and a finite dual witness. It does not prove the general trace-norm selection theorem.

Claim-Type Ledger

| Result | Type |
|---|---|
| Main abstract claim | [PROVEN, CONDITIONAL + finite-dimensional Hilbert spaces, trace-distance local gauge, replica-extensive edge aggregation] |
| Trace-zero operator space $V$ | [DEFINITION] |
| Trace-distance gauge | [DEFINITION / STANDARD NORMALIZATION] |
| Theorem 1 (Trace-Distance Selection) | [PROVEN, CONDITIONAL + unitary invariance + classical total-variation reduction + homogeneity] |
| CPTP Necessity (Theorem 2 part 1) | [INTERPRETIVE / AXIOMATIC] |
| CPTP Non-Sufficiency (Theorem 2 part 2) | [PROVEN BY COUNTEREXAMPLE] |
| Broader monotone examples | [INTERPRETIVE / STANDARD + citation] |
| Theorem 3 (Global $\ell^1(E;\mathrm{trace})$ Geometry) | [PROVEN, CONDITIONAL / PARTLY DEFINITIONAL] |
| Theorem 4 (Quotient Obstruction) | [PROVEN] |
| Theorem 5 (Quotient Duality) | [PROVEN, finite-dimensional convex duality + S1] |
| Theorem 6 (Dual Witnesses) | [PROVEN, finite-dimensional] |
| $W_{\mathrm{tr}}$ Dual witness circulation | [DEFINITION] |
| Final consolidated result | [PROVEN, CONDITIONAL on Theorem 1 operational axioms] |

Support Ledger

* **S1 — Trace-zero dual ball lemma (core proved in Lean).** Core proved in Lean (eigenvalue level); matrix lift by spectral theorem, in prose. Let $V=\{X=X^\dagger,\operatorname{Tr}X=0\}$ with norm $\|X\|_{\mathrm{tr}}=\frac12\|X\|_1$. The dual norm on observables modulo identity is $\|[M]\|^*=2\inf_{\lambda\in\mathbb R}\|M+\lambda I\|_{\mathrm{op}}$, so the dual unit ball is $\inf_{\lambda}\|M+\lambda I\|_{\mathrm{op}}\le\frac12$. For Hermitian $M$, this is equivalent to spectral diameter $\lambda_{\max}(M)-\lambda_{\min}(M)\le1$.
* **S2 — Centered representative lemma (easy).** Every Hermitian observable class modulo scalar identity has a centered representative $M' = M-\frac{\lambda_{\max}(M)+\lambda_{\min}(M)}2 I$ with $\|M'\|_{\mathrm{op}}=\frac12(\lambda_{\max}(M)-\lambda_{\min}(M))$.
* **S3 — Spectral trace-distance selection lemma (easy).** If $j_n$ is absolutely homogeneous, unitary invariant, and agrees with $\frac12\|\cdot\|_1$ on diagonal trace-zero operators, then $j_n(X)=\frac12\|X\|_1$ for all Hermitian trace-zero $X$.
* **S4 — Operational axiom separation lemma (easy).** CPTP monotonicity and tensor stability are compatibility axioms for the observer family. They are not needed for the finite spectral reduction once unitary invariance and classical total-variation reduction are assumed.
* **S5 — CPTP non-sufficiency lemma (easy/moderate).** CPTP monotonicity alone does not uniquely select the trace-distance gauge because $c\|X\|_1$ is CPTP-monotone for every $c>0$. If normalization is fixed, additional non-proportional CPTP-monotone norm examples require exact citation or construction.
* **S6 — Edge-normalization lemma (easy).** If local trace-distance gauges are selected but edge aggregation allows positive edge weights $w_e$, then the general diagnostic is $J_{\mathrm{tr},w}(\delta)=\sum_e w_e\|\delta_e\|_{\mathrm{tr}}$. The unweighted $\ell^1(E;\mathrm{trace})$ form requires normalized edge weights or a single edge orbit.
* **S7 — Finite trace duality theorem (proven; sum of S1 + §2.6).** Fully covered by S1 summed over edges, plus the divergence-free $d_0^*[M]=0$ Lagrangian argument already proved in §2.6. For finite-dimensional Hermitian trace-zero cochains, $\inf_{\alpha}\sum_e\|\delta_e-(d_0\alpha)_e\|_{\mathrm{tr}} = \max_{d_0^*[M]=0,\inf_{\lambda_e}\|M_e+\lambda_e I\|_{\mathrm{op}}\le1/2} \sum_e\operatorname{Tr}(M_e\delta_e)$.
* **S8 — One-qubit replay certificate (easy).** For $Z=\operatorname{diag}(1,-1)$, $\|Z\|_{\mathrm{tr}}=1$, and $M=\frac12Z$ satisfies $\|M\|_{\mathrm{op}}=1/2$ and $\operatorname{Tr}(MZ)=1$.
* **S9 — Cross-paper dependency-name consistency (easy; DONE).** Stale labels such as “Paper 000,” “Paper 001,” and “Paper 001b” have been replaced with descriptive titles.

v002 Audit Note

* Clarified that CPTP monotonicity is necessary but not sufficient for trace-norm uniqueness.
* Made the operational assumptions selecting trace distance explicit.
* Added the factor-of-two convention for the dual witness bound: $\|M_e\|_{\mathrm{op}}\le1/2$ for trace distance, $\le1$ for the unhalved trace norm.
* Rephrased $\ell^1(E;\mathrm{trace})$ as the geometry of a specified observer class, not a universal quantum metric.

v003 Audit Note

* **Theorem 5 dual-ball lemma made rigorous.** Replaced a loose intermediate identity ("$\max_{\|X\|_{\mathrm{tr}}\le1}\operatorname{Tr}(OX)=2\|O\|_{\mathrm{op}}$" — the all-Hermitian value, not the trace-zero one) with a self-contained centered-representative proof: on the trace-zero subspace the dual norm is $\operatorname{diam}(M)=\lambda_{\max}(M)-\lambda_{\min}(M)=2\inf_\lambda\|M+\lambda I\|_{\mathrm{op}}$ (Hölder upper bound + explicit maximizer). The final dual formula and the theorem are unchanged; the previous detour was non-load-bearing (the main chain runs through the all-Hermitian duality $\frac12\|\eta\|_1=\max_{\|M\|_{\mathrm{op}}\le1/2}\operatorname{Tr}(M\eta)$).
* **Labels synced to the proved duality.** Theorem 5 → [PROVEN, finite-dimensional convex duality + S1]; Theorem 6 → [PROVEN, finite-dimensional]; Final Consolidated Result → [PROVEN, CONDITIONAL on Theorem 1 operational axioms]; S1/S7 marked proven. Removed stale "after repair" / "on repaired" / "after clarification" / "(moderate)" qualifiers.
* **Minimax exchange cited.** The inf–max swap in Theorem 5 now cites Sion's minimax theorem [8] (compact $M$-ball, convex $\alpha$-space).
* **Abstract corrected.** Binary discrimination is the operational *motivation*, not a selecting hypothesis (the load-bearing selector is classical total-variation reduction); the abstract no longer lists it among the selecting assumptions, consistent with §1 and Theorem 1.
* **Mutual cross-reference.** Added the back-link to [3, §3.6 / Ex 3.6] — the CPTP boundary example whose full observer geometry this paper develops.
* **Theorem 1 audit notes reconciled.** Both notes now state the displayed proof uses unitary invariance + classical total-variation reduction (+ $\|X\|_1=\|\lambda\|_1$); homogeneity is attributed only to the alternative differences-of-distributions note.
* **Lean.** The eigenvalue-level core of the dual-ball lemma — for sum-zero $x\in\mathbb R^n$, $\tfrac12\sum_i|x_i|=\max\{\langle m,x\rangle:\operatorname{diam}(m)\le1\}$ with maximizer $m_i=\tfrac12\operatorname{sign}(x_i)$ — is machine-checked in Lean 4 + Mathlib (`QM.TraceZeroDuality`, theorem `half_l1_isGreatest`, built via the `QM` lake library; depends only on the standard `propext`/`Classical.choice`/`Quot.sound` axioms). The lift to the Hermitian-matrix statement is the spectral-theorem reduction (unitary invariance), left to the prose above.
  * *Correction (GTOC/GTLA cleanup pass, 2026-07-17).* This note previously read "built via the `QM` lake library — **there is no separate `PaperQF000` lib**". That clause was **false** and has been struck: `lakefile` does declare `lean_lib «PaperQF000»` (root `PaperQF000` → `PaperQF000.Witness`). Stale build artifacts under both `PaperQF000` and `QM` indicate the *module* was relocated `PaperQF000` → `QM` and the note over-corrected to deny the *library*. The `PaperQF000` lib is **not** cited by this paper and carries no result claimed here; readers should not credit it as mechanization of Paper 005's theorems.
  * *Build attestation refreshed (2026-07-17).* Re-verified independently rather than carried forward from the v003 audit: `Lean replay QM.TraceZeroDuality` → exit 0 (8493 jobs, `Build completed successfully`); `#print axioms TraceZeroDuality.half_l1_isGreatest` → `[propext, Classical.choice, Quot.sound]`; `sorry` count 0. The mechanized statement is the eigenvalue-level core only; scope is fenced by the formalization-status firewall in §2.6, and the matrix lift remains open as PL-005-1.

v1.2 Improver Note (2026-06-09)

* Improver hygiene pass (Stage 1). Part A rubric verified present (lead sentence, why-care, related work §1.1, one-qubit worked replay, falsifiability, non-claim box + demotion box) — no padding added; claim typing left unchanged.
* Worked replay: added the one-line proof of the single-cycle quotient formula (cycle-sum invariance + triangle-inequality lower bound + one-edge concentration attainment), with the cross-reference to [4] §5 — the formula was previously asserted without justification.
* Version lineage note: the header version line (v1.0/v1.1) and the audit-note labels (v002/v003) were parallel tracks; from this pass the header version is canonical (v1.1 ≙ post-v003-audit state; this pass = v1.2).
* Created sibling claim ledger `005_CPTP_Invariant_Obstruction_Claim_Ledger`; registered Paper 005 obligations in `proof_ledger_20260609` (PL-005-1 Lean matrix lift, not honesty-gating; PL-005-2 non-proportional CPTP-monotone gauge construction, genuine upgrade target for Theorem 2's breadth).

GTOC / GTLA Compliance Note

**Role.** Regime-relative diagnostic paper: the CPTP/trace-distance branch instance of the
M-compatible gauge classification program [3]. It specializes a finite obstruction geometry to an
imported quantum representation and computes its dual. It is not a foundations paper, not an
authority paper, and derives no physics.

**Degree.** Degree 1 over a finite directed graph. $C^0(G,V)\xrightarrow{d_0}C^1(G,V)$ with
$(d_0\alpha)_e=\alpha_{t(e)}-\alpha_{s(e)}$; $V$ = Hermitian trace-zero operators on a
finite-dimensional $\mathcal H$.

**Consumes.** A finite digraph $G=(V_G,E)$; a finite-dimensional real vector space $V$; a local
gauge $j$; the five Theorem-1 axioms (norm structure, CPTP monotonicity, unitary invariance, tensor
stability, classical total-variation reduction); replica-extensive edge-decomposable aggregation;
positive edge weights or an edge-uniformity convention. **Two of the five consumed axioms are
inert**: the paper's own audit notes (§2.2, S4) state that CPTP monotonicity and tensor stability
are *not* load-bearing in the spectral identification. They are retained as genuine
observer-compatibility constraints, but the load-bearing selector is classical total-variation
reduction. The earlier title adjective "CPTP-Invariant" was therefore misleading: it named a
compatibility condition while reading as a selection claim. This is why the title is
corrected to "CPTP-Compatible" for republication. An earlier version of this paragraph
defended the adjective as naming a compatibility condition; that defence is WITHDRAWN in
favour of the correction, since a title that has to be explained is not doing its job.

**Produces.** (i) A conditional identification of the local gauge as trace distance (Theorem 1);
(ii) a non-selection result — CPTP monotonicity does not fix the gauge (Theorem 2); (iii) the
global $\ell^1(E;\mathrm{trace})$ aggregation form (Theorem 3); (iv) quotient invariance of
$\Phi_{\mathrm{tr}}$ (Theorem 4); (v) a finite convex duality with divergence-free
operator-norm-bounded dual witnesses (Theorems 5–6); (vi) the signature
$\mathsf{Sig}_{\mathrm{qtr}}$.

**Does not produce.** Quantum mechanics; the Born rule; a universal quantum metric; a selection of
trace norm from CPTP monotonicity alone; a physical measurement procedure; a claim that
$\Phi_{\mathrm{tr}}$ tracks any global trace-norm quantity; a lift; authority of any kind.

**Authority status.** **None.** No descent packet, no terminalizer, no `IsAuth` guard, no evidence
ceiling is constructed or claimed. Diagnostics, dual witnesses, and "certificates" in this paper are
*diagnostic* objects. A dual witness $M^*$ attaining $\Phi_{\mathrm{tr}}$ certifies a **number**,
not a decision, and licenses no action.

### Three-layer split (doctrine §7, QM/Q papers)

| Layer | Content | Status |
|---|---|---|
| **Finite derived shadow** | Theorem 3 (edge aggregation), Theorem 4 (quotient invariance), Theorem 6 (witness existence), and the eigenvalue-level core of S1. These hold for a finite digraph valued in **any** finite-dimensional normed real vector space; their proofs are a change of variables, compactness + continuity, and discrete Hölder. **No quantum structure is used.** | Derived at this degree. S1's core is `[MECHANIZED]`. |
| **Imported representation layer** | $\mathcal H$, $B(\mathcal H)$, Hermiticity, trace-zero structure, the spectral theorem ($X=U\operatorname{diag}(\lambda)U^\dagger$), trace norm, operator norm, CPTP maps, density matrices $\rho$, tensor product $\otimes$. Theorem 1, Theorem 2, and S1's matrix-level lift live **entirely** here. | `IMPORTED`. Not constructed at this degree. Not DDA operations. |
| **Q-gated layer** | Physical measurement semantics (binary discrimination as an *experiment* rather than an algebraic normalization); "quantum sub-systems"; "spatial points"; "causal or spatial transport channels"; "physical open-system evolution"; any chance reading of $p,q$; any claim that $M_e$ is physically measurable. | `Q-gated` / `OracleNeeded`. **Constructed nowhere.** Referenced only as motivation. |

The practical consequence: the word "quantum" in this paper's title qualifies the *imported
representation*, not the results. Strip $\mathcal H$ and Theorems 3, 4, and 6 survive verbatim;
Theorems 1 and 2 do not survive at all.

### Declared imports (doctrine §3 register)

| Import | Where it enters | Priced as |
|---|---|---|
| `Hilbert space` | §2.1 "Let $\mathcal H$ be finite-dimensional"; §1 | `IMPORTED` — never constructed |
| `density operators` | Theorem 1 axiom 4 ("for every density matrix $\rho$"); §1 "state space of density matrices" | `IMPORTED` |
| `CPTP maps` | Theorem 1 axiom 2; Theorem 2; title | `IMPORTED` — and **inert** in the proof (§2.2 audit note, S4) |
| `tensor composition` | Theorem 1 axiom 4 ($X\otimes\rho$) | `IMPORTED` — and inert (S4) |
| `physical dynamics` | §2.3 "A physical open-system evolution is represented by a CPTP map $\Lambda$" | `Q-gated` — no dynamics is constructed; no continuum time, no $\exp(tH)$ appears |
| `spacetime` / `locality` | §1 "spatial points", "causal or spatial transport channels" | `Q-gated` — fenced in the Genesis-Bias Fence (§1) |
| `chance / probability semantics` | §2.2 note, "differences of probability distributions" $X=\operatorname{diag}(p-q)$ | **Naming only.** $p,q$ are used purely algebraically as unit-sum nonnegative weight profiles ($\lambda=t(p-q)$, $\|p-q\|_1=2$); no chance semantics is invoked anywhere. A later probabilistic adapter may read these as distributions; this paper does not supply that adapter. |
| operator algebra, spectral theorem, trace/operator norm duality | §2.1, §2.2, S1 | `IMPORTED` — `[STANDARD + citation [7]]` |
| binary state discrimination | §0, §1.1, normalization anchor [6] | `IMPORTED` — operational motivation, not a selecting hypothesis (see the v003 audit note) |

**OracleNeeded / Q-gated items.** Physical realizability of the dual witness as a measurement; any
identification of $\Phi_{\mathrm{tr}}$ with a physical distinguishability experiment; the
selection of trace distance among CPTP-monotone gauges *without* the classical-reduction axiom
(corpus obligation **PL-000BN-1**, not discharged here); the existence or non-existence of a
non-proportional CPTP-monotone norm (**PL-005-2**).

### GTOC regime declaration

* **ObstructionRegime.** $k=0$: the obstruction object is the cokernel quotient
  $C^1(G,V)/\operatorname{im}(d_0)$, normed by $\Phi_{\mathrm{tr}}$.

* **$C^k$, $d_k$.** $C^0$, $C^1$, $d_0$ are declared. **$C^2$ and $d_1$ are not constructed
  anywhere in this paper.**

* **$d_{k+1}\circ d_k=0$.**

> **OBSTRUCTION.** The following cannot be derived from what is available at this degree: the
> closure law $d_1\circ d_0=0$, and with it any exact / closed-survivor / active-closure-failure
> classification of a nonzero $\Phi_{\mathrm{tr}}$. What would have to be admitted: a degree-2
> cochain space $C^2(G,V)$ and a closure map $d_1$ — i.e. face/2-cell data this paper's digraph
> does not carry. What is lost if it is admitted: the results stop being representation-agnostic
> over an arbitrary finite digraph, and acquire whatever coherence hypotheses the 2-cells encode.
> **This paper therefore classifies only $\Phi_{\mathrm{tr}}=0$
> (`ExactClass`, relative to the declared observer) versus
> $\Phi_{\mathrm{tr}}>0$ (obstruction present, unclassified).** No $C^2$ carrier
> or $d_1$ is declared, so the closed-residual/active-closure split is unavailable.
> Neither case directly constructs a terminal.

* **ZeroRel / local sameness.** $\|X\|_{\mathrm{tr}}=0\iff X=0$ (faithfulness, Theorem 1 axiom 1).
  Sameness is quotient-relative: $\Phi_{\mathrm{tr}}([\delta])=0$ means "coboundary-equivalent to
  zero *for this observer*", not "no defect" — see the detector-adequacy warning in §2.8.

* **Observer / gauge / norm.** Observer: replica-extensive, edge-decomposable, declared. Local
  gauge: $\|\cdot\|_{\mathrm{tr}}=\frac12\|\cdot\|_1$. Global: $\ell^1(E;\mathrm{trace})$. Dual:
  operator norm modulo identity ($\operatorname{diam}\le1$). All declared, none universal.

* **Lift policy.** **Refused.** No lift is considered, triggered, or licensed. A nonzero
  $\Phi_{\mathrm{tr}}$ is a diagnostic magnitude only. Any lift would additionally require an
  obstruction witness, a preservation witness, a non-destruction check, a budget/authority
  boundary, and a terminalizer route — none supplied here.

* **Terminal policy.** **Refused.** No terminalizer, no seal. Routing terminal $\ne$ authority
  terminal; this paper reaches neither.

**GTLA boundary.** This paper is GTOC-side only. It mints no `ContractAuthority` and no
`VerifierScopedAuthority`; `SemanticAuthority` is unavailable (no semantic adapter is declared).
`SpecificationIdentity`, `DetectorAdequacy`, `ExhaustionWitness`, `EvidenceCeiling`,
`ReplayWitness`, `Terminalizer`, and `IsAuth` are **all absent** and are prerequisites for any
authority-bearing downstream use. No model-facing role in this paper owns authority. CODA-FDA
supplies non-authoritative terminal-policy checks; GTOC (this paper) routes and diagnoses only.
Any bounded promotion is a separate external authenticated human decision over checked evidence.

**Mechanization status.** `[MECHANIZED-PARTIAL]`. Machine-checked: the eigenvalue-level core of
S1 — `TraceZeroDuality.half_l1_isGreatest` in `QM.TraceZeroDuality`.
Re-verified 2026-07-17: `Lean replay QM.TraceZeroDuality` exit 0 (8493 jobs); axioms
`[propext, Classical.choice, Quot.sound]`; zero `sorry`. **Not mechanized:** the spectral lift to
the Hermitian-matrix statement (PL-005-1), and Theorems 1–6 themselves. Nothing quantum and nothing
about CPTP is mechanized. The separate `PaperQF000` lake library is **not** cited by this paper and
supports none of its claims.

**Remaining open obligations.**

* **PL-005-1** — Lean matrix-level lift of the trace-zero dual ball lemma (spectral-theorem
  reduction from the machine-checked eigenvalue core). Hardening; not honesty-gating.

* **PL-005-2** — Construct, or refute the existence of, a CPTP-monotone *norm* on Hermitian
  trace-zero operators not proportional to $\|\cdot\|_1$. Genuine upgrade target for Theorem 2's
  breadth.

* **PL-000BN-1** (inherited, corpus-wide) — operational axioms uniquely selecting trace distance
  among CPTP-monotone gauges. Theorem 1 is the *conditional* version given classical reduction; it
  does not discharge PL-000BN-1 and does not claim to.

* **Degree-2 data** — $C^2$/$d_1$ absent, so the survivor/active-failure classification is
  unavailable (see the OBSTRUCTION above). No obligation is opened here; recorded as a scope fence.

References

[1] J. H. Carroll. *Primitive Axiomatics of Finite Obstruction Calculus* 2026. Zenodo. <https://zenodo.org/records/20651224>.
[2] J. H. Carroll. *Projection Obstruction for Factorized States: Nonlinear Dynamics, Conditional ℓ1 Diagnostics, and Finite-Time Defect Bounds* 2026. Zenodo. <https://zenodo.org/records/20650922>.
[3] J. H. Carroll. *M-Compatible Gauge Classification for Banach Presheaf Coboundaries: The ℓ¹ Maximal-Symmetry Endpoint* 2026. Zenodo. <https://zenodo.org/records/20564214>.
[4] J. H. Carroll. *SO(k)-Invariant Gauge Classification and the L1(E; L2)$ Obstruction Geometry* 2026. Zenodo. <https://zenodo.org/records/20173318>.
[5] J. H. Carroll. *Coordinate-Wise Additivity and the ℓ¹ Norm on Finite Graph Cochains* 2026. Zenodo. <https://zenodo.org/records/20173236>.
[6] C. W. Helstrom. *Quantum Detection and Estimation Theory*. Academic Press, 1976.
[7] M. A. Nielsen and I. L. Chuang. *Quantum Computation and Quantum Information*. Cambridge University Press, 2010.
[8] M. Sion. *On general minimax theorems*. Pacific J. Math. **8** (1958), 171–176.

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `C1` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C1`) |
| `C2` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C2`) |
| `C3` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C3`) |
| `C4` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C4`) |
| `C5` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C5`) |
| `C6` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C6`) |
| `C7` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C7`) |
| `C8` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C8`) |
| `C9` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C9`) |
| `C10` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C10`) |
| `C11` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C11`) |
| `C12` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C12`) |
| `C13` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C13`) |
| `C14` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C14`) |
| `C15` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `080:C15`) |
| `R1` | [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md) (§11.36) |
| `R2` | [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md) (§11.36) |
| `R3` | [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md) (§11.36) |
| `R4` | [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md) (§11.36) |
| `R5` | [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md) (§11.36) |
| `R7` | [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md) (§11.36) |
| `R8` | [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md) (§11.36) |
| `R10` | [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md) (§11.36) |
| `R6` | [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md) (§11.36) |

<!-- claim-id-body-index:end -->
