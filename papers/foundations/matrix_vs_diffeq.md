# QM_040 — Redirect Stub (Reduced to Gaussian Integer Matrix Commutator Example)

**AuthorityEffect:** None.  
**Status:** ABSORBED_REDIRECT (2026-10-17 packaging merge).

## Live Destination

The standalone manuscript is retired. The actual text contained no matrix-versus-differential-equation correspondence (the title was an unfulfilled promise). Its single surviving mathematical contribution—a concrete $3 \times 3$ Gaussian-integer matrix example illustrating observer information loss—is merged into the matrix/observer foundations:

- **Source Notes:** [`../006_finite_qm/finite_quantum_mechanics_source_notes.md#1120-trace-zero-matrices-and-a-non-zero-commutator`](../006_finite_qm/finite_quantum_mechanics_source_notes.md#1120-trace-zero-matrices-and-a-non-zero-commutator) (§11.20).
- **Exact Implementation:** `omega_engine/crates_rs/omega_quantum_physics` (`su_n::GellMannBasis`, `exact_field::matrix::{trace, commutator}`).
- **Integration Tests:** `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/tests/representation/gell_mann_basis.rs`.
- **Consolidated Claims:** [`qm_040_matrix_vs_diffeq_representation_claim_ledger.md`](qm_040_matrix_vs_diffeq_representation_claim_ledger.md) (`QM_040-C1` through `QM_040-C6`).

## Retained Mathematical Content

**Example (Trace-zero local summaries do not determine commutation).**  
Consider the Pauli embedding into $3 \times 3$ matrices over Gaussian integers $\mathbb{Z}[i]$:

$$
\Lambda_1 = X \oplus 0 = \begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}, \quad
\Lambda_2 = Y \oplus 0 = \begin{pmatrix} 0 & -i & 0 \\ i & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}, \quad
\Lambda_3 = Z \oplus 0 = \begin{pmatrix} 1 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 0 \end{pmatrix}.
$$

Each matrix has vanishing trace:

$$
\operatorname{Tr}(\Lambda_1) = \operatorname{Tr}(\Lambda_2) = \operatorname{Tr}(\Lambda_3) = 0.
$$

Yet their pairwise commutators are nonzero and satisfy the standard $\mathfrak{su}(2)$ algebra:

$$
[\Lambda_1, \Lambda_2] = 2i \Lambda_3, \qquad
[\Lambda_2, \Lambda_3] = 2i \Lambda_1, \qquad
[\Lambda_3, \Lambda_1] = 2i \Lambda_2.
$$

### Operational Meaning & Observer Information Loss

1. **Local Summary vs. Pairwise Relation:**  
   Individual trace readouts are lossy local summaries. For example, the pair $(X, Y)$ and the pair $(X, X)$ both exhibit identical trace profiles $(0, 0)$. However, $X$ and $Y$ anticommute ($[X,Y] = 2iZ \ne 0$), while $X$ and $X$ commute ($[X,X] = 0$). Local trace evaluation cannot distinguish commuting from non-commuting pairs.
2. **Third Coordinate Redundancy:**  
   The third coordinate row and column in the $3 \times 3$ embedding contribute nothing to this algebraic distinction beyond embedding $\mathfrak{su}(2)$ into a larger ambient space.
3. **Coordinate Projectors:**  
   The coordinate-projector idempotence identities ($P_0^2 = P_0, P_1^2 = P_1$) are elementary algebraic facts already subsumed by the measurement conditioning material in QM_021.

## What Is Retired & Excluded

- **Zero Differential-Equation Correspondence:** The original paper promised a comparison between matrix mechanics and differential equations, but contained none.
- **Trace-Zero Pair Classification Dropped:** The paper's proposed program to classify all trace-zero pairs is dropped from required foundational derivations.
- **No Physical Promotion:** The example is static Gaussian-integer algebra; it derives no continuous dynamics, color charge, or physical state space.
