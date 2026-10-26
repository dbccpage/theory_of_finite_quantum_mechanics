# QM_005 — Redirect Stub (Absorbed into Finite Quantum Mechanics)

**AuthorityEffect:** None.  
**Status:** ABSORBED_REDIRECT (2026-10-17 packaging merge).

## Live Destination

The standalone manuscript is retired. Its surviving mathematical content is preserved as completed infrastructure in the finite quantum mechanics monograph and codebase:

- **Canonical Monograph:** [`../finite_quantum_mechanics/finite_quantum_mechanics.md#117-the-quantum-deformation-complex-tangent-gauge-directions-and-operational-residuals`](../finite_quantum_mechanics/finite_quantum_mechanics.md#117-the-quantum-deformation-complex-tangent-gauge-directions-and-operational-residuals) (§11.7).
- **Source Notes:** [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md#115-a-finite-m_2-state-effect-model-qm-005-consolidated-and-retired`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md#115-a-finite-m_2-state-effect-model-qm-005-consolidated-and-retired) (§11.5).
- **Certified Rust Verifiers:** `omega_engine/crates_rs/omega_quantum_physics/src/gauge_cochain_complex.rs` and `finite_quantum_mechanics/native/src/m2_quantum_packet.rs`.
- **Integration Tests:** `finite_quantum_mechanics/native/tests/finite_m2_packet.rs`.
- **Consolidated Claims:** [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (IDs `005:QM-005-C1` through `005:QM-005-C14`).

## Retained Mathematical Formulation

### 1. Quantum Deformation Complex and Trace Cyclicity

At a declared quantum state/effect/probability triple $(p, E, \rho)$ with $p = \operatorname{Tr}(E \rho)$, the linearized gauge complex on matrix carrier $M_n$ is:

$$
d_0(A) = (0, [A, E], [A, \rho]),
$$

$$
d_1(\delta p, \delta E, \delta\rho) = \delta p - \operatorname{Tr}(E\,\delta\rho) - \operatorname{Tr}(\delta E\,\rho),
$$

where $A$ is an anti-Hermitian gauge generator ($A^\dagger = -A$) and $\delta E, \delta\rho$ are Hermitian perturbations.

**Trace Cyclicity:**
$$
d_1(d_0(A)) = -\operatorname{Tr}(E[A,\rho]) - \operatorname{Tr}([A,E]\rho) = -\operatorname{Tr}(EA\rho - E\rho A + AE\rho - EA\rho) = 0.
$$
Trace cyclicity gives $d_1 d_0 = 0$ identically in every finite matrix dimension $M_n$. Differentiating a symmetry-invariant constraint produces a linear constraint that vanishes along the symmetry's gauge directions.

### 2. Exact Classifier Infrastructure

Over exact coefficients $\mathbb{Q}(i)$, classification partitions variations into:
1. *Exact repair:* $x \in \operatorname{im}(d_0)$, solved via exact Gaussian elimination with explicit gauge generator witness $a$.
2. *Closed nonexact residual ($H^1$):* $d_1 x = 0$ but $x \notin \operatorname{im}(d_0)$, witnessed by a separating functional $\lambda \in \ker(d_0^{\mathsf{T}})$ with $\lambda \cdot x \ne 0$.
3. *Active closure failure:* $d_1 x \ne 0$, witnessed by the nonzero Born coordinate defect.

### 3. Infinitesimal Tangent Directions vs. Finite Gauge Transformations

The linearized complex describes tangent vectors, not finite displacements within the positive state space. For $\rho = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$ and $\delta\rho = [A, \rho] = \begin{pmatrix} 0 & -1 \\ -1 & 0 \end{pmatrix}$,

$$
\det(\rho + t\,\delta\rho) = -t^2 < 0 \qquad \forall t \ne 0.
$$

Finite gauge invariance is provided by simultaneous unitary conjugation $\rho \mapsto U \rho U^\dagger, E \mapsto U E U^\dagger$, which preserves positivity and Born probabilities. Unitary basis changes cannot correct an inconsistent declared probability table.

### 4. Operational Meaning of $H^1$: Observational Ambiguity and Hidden Variation

For $\rho = I_2/2$, $E = \operatorname{diag}(1, 0)$, $\delta\rho = \begin{pmatrix} 0 & 1/4 \\ 1/4 & 0 \end{pmatrix}$, $\delta E = \delta p = 0$:
- $d_1 x = 0$ because $\operatorname{Tr}(E\,\delta\rho) = 0$;
- $x \notin \operatorname{im}(d_0)$ because $[A, I_2/2] = 0$ for all $A$;
- $\rho + \delta\rho = \begin{pmatrix} 1/2 & 1/4 \\ 1/4 & 1/2 \end{pmatrix}$ is a valid density matrix with eigenvalues $3/4$ and $1/4$;
- Expectation value $\operatorname{Tr}(E(\rho+\delta\rho)) = 1/2$ is identical to $\operatorname{Tr}(E\rho)$.

This closed nonexact residual represents a valid physical state variation that the chosen measurement cannot detect. A residual class can represent unresolved physical variation, observational ambiguity, or a consistency failure; algebraic classification alone does not distinguish among these interpretations without declaring which data are fixed, which changes are permitted, and which observations must be preserved.

## What This Folder Retains

- Historical claim ledger mapping for bijection packaging (`005:QM-005-C1`..`C14`).
- Standalone paper retired; concrete verifiers and tests live in the active codebase.
