# QM_021 — Redirect Stub (Absorbed into Finite Quantum Mechanics)

**AuthorityEffect:** None.  
**Status:** ABSORBED_REDIRECT (2026-10-17 packaging merge).

## Live Destination

The standalone manuscript is retired. Its surviving mathematical content is merged beside normalized weights into Finite Quantum Mechanics:

- **Source Notes:** [`../006_finite_qm/finite_quantum_mechanics_source_notes.md#1112-measurement-update-as-idempotent-conditioning-qm-021-merged-and-retired`](../006_finite_qm/finite_quantum_mechanics_source_notes.md#1112-measurement-update-as-idempotent-conditioning-qm-021-merged-and-retired) (§11.12).
- **Certified Rust Implementation:** `omega_engine/crates_rs/omega_quantum_physics/src/sector_conditioning.rs` (`sector_conditioning::{condition, sector_probability, luders_update, sector_projector}`).
- **Integration Tests:** `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/tests/measurement_conditioning.rs`.
- **Consolidated Claims:** [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (IDs `021:QM-021-C1` through `021:QM-021-C12`).

## Retained Mathematical Formulation

**Proposition (Finite conditioning and compatible composition).**  
For nonnegative weights $w_i$, a declared event $S$, and positive sector mass $Z_S = \sum_{i \in S} w_i > 0$, define the normalized conditioned weights:

$$
C_S(w)_i = \frac{\mathbf{1}_S(i) w_i}{Z_S}.
$$

Then $C_S(w)$ is normalized, supported on $S$, and satisfies idempotence:

$$
C_S(C_S(w)) = C_S(w).
$$

The event $S$ has probability one after this update ($\sum_{i \in S} C_S(w)_i = 1$). The original event probability is the prior sector mass fraction $p_S(w) = Z_S / \sum_i w_i$. Furthermore, compatible composition holds for arbitrary events on the same classical carrier:

$$
C_T(C_S(w)) = C_{S \cap T}(w) = C_S(C_T(w))
$$

whenever the intersection has positive mass $Z_{S \cap T} > 0$, since intermediate normalizations cancel directly.

### Preserved Qualifications & Boundaries

1. **Undefined at Zero Sector Mass:** When $Z_S = 0$, conditioning is undefined; no missing state is manufactured.
2. **Nonlinear Retraction vs. Linear Projection:** The normalized update $C_S$ is an idempotent nonlinear retraction onto a face of the probability simplex. The raw indicator mask $w \mapsto \mathbf{1}_S w$ is the linear projection. This distinction separates classical conditioning from a linear Hilbert-space projector.
3. **Idempotence Does Not Derive the Quantum Lüders Update:** Establishing that conditioning is idempotent on diagonal outcome weights does not reconstruct the Lüders rule $\mathcal{I}_S(\rho) = P_S \rho P_S$. If $P_S = \sum_{i \in S} P_i$ contains $\ge 2$ one-dimensional sectors, compare $\mathcal{I}_S^L(\rho) = P_S \rho P_S$ with $\mathcal{I}_S^D(\rho) = \sum_{i \in S} P_i \rho P_i$: both have outcome probability $\operatorname{Tr}(P_S \rho)$, both produce states supported on $S$, and both selective updates are idempotent and repeatable, yet they differ on coherence within $S$. The operational condition selecting the instrument remains an open problem.
4. **Current Implementation Surpasses the Paper:** The Rust module `omega_quantum_physics::sector_conditioning` provides exact conditioning, full Lüders updates for declared projectors, and nonselective Lüders channels, verified by `native/tests/measurement_conditioning.rs`.

## What This Folder Retains

- Historical claim ledger mapping (`021:QM-021-C1`..`C12`) for provenance.
- Standalone manuscript retired; elementary extensions are closed and not reopened as research projects.
