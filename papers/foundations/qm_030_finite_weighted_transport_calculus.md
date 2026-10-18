# QM_030 — Redirect Stub (Extracted into Finite Transport Calculus and Holonomy)

**AuthorityEffect:** None.  
**Status:** ABSORBED_REDIRECT (2026-10-17 packaging merge).

## Live Destination

The standalone synthesis is retired. Its surviving mathematical kernel (finite path sums with a unique cut) and corrected gauge boundaries are merged into Finite Quantum Mechanics and the general obstruction framework:

- **Source Notes:** [`../006_finite_qm/finite_quantum_mechanics_source_notes.md#1114-finite-weighted-transport-calculus-qm-030-extracted-and-retired`](../006_finite_qm/finite_quantum_mechanics_source_notes.md#1114-finite-weighted-transport-calculus-qm-030-extracted-and-retired) (§11.14).
- **Certified Graded Transport:** `TimeSlicedTransport::{path_sum, propagator, sliced_composition}` in `omega_engine/crates_rs/omega_quantum_physics`.
- **Integration Tests:** `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/tests/dynamics/weighted_transport_calculus.rs`.
- **Consolidated Claims:** [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (IDs `030:QM-030-C1` through `030:QM-030-C27`).

## Retained Mathematical Formulation

**Proposition (Finite path sums with a unique intermediate cut).**  
Let $X_0, \ldots, X_n$ be finite layers of carriers. For transitions between adjacent layers, define the transfer matrix over a commutative semiring:

$$
A_k(y, x) = \sum_{e: x \to y} w(e).
$$

Then:

$$
\sum_{\gamma: a \to b} \prod_{e \in \gamma} w(e) = (A_{n-1} \cdots A_0)_{ba}.
$$

This is finite distributivity over a commutative semiring; no inner product, metric, or Hamiltonian generator is required. The essential condition is that every allowed history crosses the chosen intermediate cut exactly once.

### Key Corrections, Boundaries & Retired Syntheses

1. **The Overcounting Example:** On $a \to b \to c$, splitting the history at $a$, $b$, and $c$ counts it three times ($\sum_\gamma (|\gamma|+1)w(\gamma)$), while a fixed intermediate cut counts it once. Crucially, the vanishing of cohomological obstruction ($H^1 = 0$) does not certify that a path decomposition counts each history exactly once.
2. **Correct Multiplicative Gauge-Triviality Criterion:** Exponentiation loses integral periods: $w = \exp(a)$ gauge-trivial $\iff a = d^0 \varphi$ fails in the forward direction. On edges $0 \to 1$, $1 \to 2$, and $0 \to 2$ with angles $\theta_{01} = \theta_{12} = 0, \theta_{02} = 2\pi$, all multiplicative weights $e^{i\theta_e} = 1$ are gauge-trivial, yet the angle assignment requires winding: $\theta = d^0 \varphi + 2\pi k$ with $k \in \mathbb{Z}^E$. The correct multiplicative criterion is trivial phase holonomy around every cycle.
3. **Endpoint Potentials Telescope vs General Action:** A globally defined action $S[\gamma]$ additive under concatenation can assign different values to different paths between identical endpoints (interference). Only when $S[\gamma] = V(\operatorname{end}\gamma) - V(\operatorname{start}\gamma)$ does the action telescope. "Endpoint potentials telescope" is retained; the blanket classification of dynamical phase as an exact coboundary is discarded.
4. **Structural Exclusions Left Behind:**
   - *Dagger compactness does not select complex Hilbert space:* Real inner-product spaces and relational categories provide counterexamples.
   - *Cancellation does not force $\mathbb{Z}$-embedding:* In $\mathbb{F}_2$, $1+1=0$ shows cancellation without embedding $\mathbb{Z}$.
   - *Organizational Syntheses Retired:* Proving the tuple is a "weakest host", turning "equipment" into formal categorical equipment, and extending the interface census are retired as finite QM requirements.
   - Repeated pairing, density, quotient, and terminalization sections point to their existing homes in WDP and QM-002..006.

## What This Folder Retains

- Historical claim ledger mapping (`QM-030-C1`..`C27`) for provenance.
- Standalone synthesis retired; finite path-sum identity extracted and gauge statement merged into existing gauge material.
