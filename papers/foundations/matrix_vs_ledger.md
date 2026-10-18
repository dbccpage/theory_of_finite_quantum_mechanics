# Trace-Zero Locals and a Nonzero Commutator in a Fixed 3 x 3 Gaussian-Integer Model

## Claim Ledger

**Date:** 2026-07-29
**Paper Key:** `003_quantum_foundations/040_matrix_vs_diffeq_representation`  
**Paper Identity:** `QM_040`
**Paper Version:** `v1.0.0`
**AuthorityEffect:** `None`

## Normalized Claims

| Claim ID | Exact tags | Scope / statement | Evidence state | Verification target |
|---|---|---|---|---|
| `QM_040-C1` | `[DEFINITION]` | The carrier type has nine Gaussian-integer coordinate slots $(a,b)\in\mathbb Z\times\mathbb Z$ arranged as a $3\times3$ matrix, with the displayed pair arithmetic, matrix operations, trace, commutator, scalar multiplication, and explicit zero matrix. The type is not a finite set; the witness family is the five named matrices. No involution, norm, topology, or completion is included. | `LEAN_BOUND` | Carrier shared by the exact `P0_sq`, `P1_sq`, trace, and commutator declarations; receipt: `lean_post_edit_receipt.json` |
| `QM_040-C2` | `[DERIVED]` | The displayed coordinate matrices satisfy $P_0^2=P_0$ and $P_1^2=P_1$. | `LEAN_BOUND` | `QM.GellMann.P0_sq`<br>`QM.GellMann.P1_sq` |
| `QM_040-C3` | `[DERIVED]` | The displayed $\Lambda_1$, $\Lambda_2$, and $\Lambda_3$ have trace zero; in particular, $\Lambda_1$ and $\Lambda_2$ satisfy the declared local trace-zero predicate. | `LEAN_BOUND` | `QM.GellMann.lambda1_tr`<br>`QM.GellMann.lambda2_tr`<br>`QM.GellMann.lambda3_tr`<br>`QM.GellMann.lambda12_local_trace_green` |
| `QM_040-C4` | `[DERIVED]` | The three closed identities are $[\Lambda_1,\Lambda_2]=2i\Lambda_3$, $[\Lambda_2,\Lambda_3]=2i\Lambda_1$, and $[\Lambda_3,\Lambda_1]=2i\Lambda_2$. | `LEAN_BOUND` | `QM.GellMann.su2_comm_12`<br>`QM.GellMann.su2_comm_23`<br>`QM.GellMann.su2_comm_31` |
| `QM_040-C5` | `[DERIVED]` | Closed finite-witness LGGR theorem: $\Lambda_1$ and $\Lambda_2$ each have trace zero while their pairwise commutator is nonzero. LGGR has no meaning here beyond those two evaluator predicates. | `LEAN_BOUND` | `QM.GellMann.su2_comm_12_ne_zero`<br>`QM.GellMann.local_traceless_global_commutator_nonzero`<br>Encyclopedia binding: `ENC-1262`; lifecycle acceptance is recorded in independent support receipts |
| `QM_040-C6` | `[SCOPE FENCE]` | The module's false authority predicate is not inhabited for any carrier type. This grants no authority and supplies no physical or continuum interpretation. | `LEAN_BOUND` | `QM.GellMann.structure_not_auth` |

## Formal Evidence Boundary

The `LEAN_BOUND` entries are claim-local bindings to the following exact declarations in module target `003_qm_gellmann_matrix_projections`, under the QM_040 `lean_post_edit_receipt.json`:

- `QM.GellMann.P0_sq`
- `QM.GellMann.P1_sq`
- `QM.GellMann.lambda1_tr`
- `QM.GellMann.lambda2_tr`
- `QM.GellMann.lambda3_tr`
- `QM.GellMann.lambda12_local_trace_green`
- `QM.GellMann.su2_comm_12`
- `QM.GellMann.su2_comm_23`
- `QM.GellMann.su2_comm_31`
- `QM.GellMann.su2_comm_12_ne_zero`
- `QM.GellMann.local_traceless_global_commutator_nonzero`
- `QM.GellMann.structure_not_auth`

These bindings do not establish physical locality or color, full $SU(N)$, all eight $SU(3)$ generators, Hermiticity, a Hilbert space, dynamics, probability, decoherence, a continuum construction, or authority. `ENC-1262` is a present encyclopedia binding for `QM_040-C5` only; it does not enlarge that claim.
