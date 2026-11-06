# QM_006 — Redirect Stub (Dropped from Active Derivation Stack)

**AuthorityEffect:** None.  
**Status:** ABSORBED_REDIRECT (2026-10-17 packaging merge).

## Live Destination

The standalone manuscript is retired and dropped from the active derivation stack. Its substantive ingredients already belong to QM-001, QM-005, and the transport papers:

- **Canonical Monograph:** [`../001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md#chapter-04`](../001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md#chapter-04) (Chapter 4, §4.2.2).
- **Source Notes:** [`../006_finite_qm/finite_quantum_mechanics_source_notes.md#116-conditions-required-for-a-finite-quantum-realization-qm-006-dropped-from-active-derivation-stack`](../006_finite_qm/finite_quantum_mechanics_source_notes.md#116-conditions-required-for-a-finite-quantum-realization-qm-006-dropped-from-active-derivation-stack) (§11.6).
- **Consolidated Claims:** [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (IDs `006:QM-006-C1` through `006:QM-006-C30`).

## Retained Mathematical Formulation

### Dynamic Observer Factorization and Update Descent

If $O: X \to Y$ is an observation map representing retained information and $T: X \to X$ is an allowed transformation or update on the carrier, the update descends to a well-defined operation $\tilde{T}: O(X) \to Y$ (satisfying $O(T(x)) = \tilde{T}(O(x))$) if and only if:

$$
O(x) = O(y) \implies O(Tx) = O(Ty) \qquad \forall x, y \in X.
$$

**Physical Significance:** In quantum systems, this descent condition is physically restrictive even for a single, fixed observer. For the fixed observable $E = \begin{pmatrix}1&0\\0&0\end{pmatrix}$, two distinct quantum states
$$
\rho_\pm = \frac{1}{2} \begin{pmatrix} 1 & \pm 1 \\ \pm 1 & 1 \end{pmatrix}
$$
give identical initial expectation values under $O(\rho) = \operatorname{Tr}(E\rho)$:
$$
O(\rho_+) = O(\rho_-) = \frac{1}{2}.
$$
Under the rational unitary transformation $T(\rho) = U \rho U^\dagger$ with
$$
U = \begin{pmatrix} 3/5 & 4/5 \\ 4/5 & -3/5 \end{pmatrix},
$$
the same observer yields divergent post-update readouts:
$$
O(T(\rho_+)) = \frac{49}{50}, \qquad O(T(\rho_-)) = \frac{1}{50}.
$$
Thus $T$ does not descend through $O$: the observer identifies two states whose later observations under the same measurement differ. Manipulating or compressing representations in a way that discards these phase distinctions fails dynamical descent, losing predictive power for subsequent operations. This is the dynamic version of the quotient/transport criterion from QM-001, retained in WDP Chapter 4 (§4.2.2) rather than creating a separate "quantum survival" project.

## Retired Proposed Burdens

1. **The "Survival Theorem" Packaging:** The paper packaged conditions such as declared interface, replay, quotient compatibility, transport, metric bounds, and terminal receipts into a conjunction. The mathematical work lies in establishing the individual substantive conditions; naming their conjunction adds no separate quantum structure to derive.
2. **Comparative Census & Tower Narrative:** The comparative census of "surviving interfaces", six-role organizational map, authority receipts, and broad repair-capacity no-go programme are not prerequisites for completing finite QM and are retired.
3. **Repair-Capacity Recurrence:** The recurrence of §18 and the arithmetic of §19's conditional no-go depend on an assumed positive repair gap; whether any physical architecture has a persistent positive repair gap remains an open physical question.

## What This Folder Retains

- Historical claim ledger mapping for bijection packaging (`006:QM-006-C1`..`C30`).
- Standalone manuscript retired; substantive ingredients consolidated with QM-001 and QM-005.
