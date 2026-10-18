# Claim Ledger: Relational Point Coincidence, Witnessed Difference, and Dressing Field Normal Forms

**Document ID:** `GR003-CLAIM-LEDGER-V1`  
**Associated Paper:** [`relational_point_coincidence_and_witnessed_difference.md`](relational_point_coincidence_and_witnessed_difference.md)  
**Author:** Jeremy H. Carroll  
**Date:** 2026-10-01  
**Status:** Live Canonical Register  
**AuthorityEffect:** None  

---

## 1. Claim Classification Taxonomy

Every claim in this monograph is registered under one of four rigorous epistemic postures:
- **`DEFINITION`**: Syntactic declaration of mathematical, relational, or algorithmic structures.
- **`CONDITIONAL_THEOREM`**: Exact deductive result proven under declared hypotheses in relational algebra or discrete mathematics.
- **`COMPUTATIONAL_WITNESS`**: Machine-checked arithmetic or linear programming certificate over $\mathbb{Q}$.
- **`EXPLICIT_NONCLAIM`**: Formal fence preventing overclaiming, speculative extrapolation, or ungrounded physics promotion.

---

## 2. Master Claim Register

| Claim ID | Formal Name | Epistemic Posture | Evidence Type | Verification Surface | Status |
|---|---|---|---|---|---|
| **CLM-GR003-001** | Point Coincidence as Candidate Key | `CONDITIONAL_THEOREM` | Mathematical Deduction | §2.2, Theorem 2.1 | `VERIFIED` |
| **CLM-GR003-002** | Lossless Observer Sheet Join (Heath's Theorem) | `CONDITIONAL_THEOREM` | Relational Algebra Proof | §3.1, Theorem 3.1 | `VERIFIED` |
| **CLM-GR003-003** | Dressing Field Projection Idempotence | `CONDITIONAL_THEOREM` | Group Action Deduction | §4.1, Proposition 4.1 | `VERIFIED` |
| **CLM-GR003-004** | Basic Invariant Presentation under DFM | `CONDITIONAL_THEOREM` | Equivariance Proof | §4.1, Proposition 4.1 | `VERIFIED` |
| **CLM-GR003-005** | Relational Point Coincidence Normal Form (RPCNF) | `DEFINITION` | Formal Specification | §5.1, Definition 5.1 | `SPECIFIED` |
| **CLM-GR003-006** | Dressing Field Normal Form (DFNF) | `DEFINITION` | Formal Specification | §5.2, Definition 5.2 | `SPECIFIED` |
| **CLM-GR003-007** | Relational Local Green, Global Red (LGGR) | `CONDITIONAL_THEOREM` | Cochain Exactness Audit | §6.1, Theorem 6.1 | `VERIFIED` |
| **CLM-GR003-008** | Exact Rational Dual LP Witness for Relational Obstruction | `COMPUTATIONAL_WITNESS` | Strong Duality over $\mathbb{Q}$ | §6.2, Python Solver | `EXECUTED` |
| **CLM-GR003-NON01** | No Derivation of Continuous General Relativity | `EXPLICIT_NONCLAIM` | Negative Scope Fence | §7.2, Item 1 | `ENFORCED` |
| **CLM-GR003-NON02** | No Derivation of Quantum Gravity | `EXPLICIT_NONCLAIM` | Negative Scope Fence | §7.2, Item 2 | `ENFORCED` |
| **CLM-GR003-NON03** | No Universal Independence of Scalar Fields | `EXPLICIT_NONCLAIM` | Singularity Caveat | §7.2, Item 3 | `ENFORCED` |
| **CLM-GR003-NON04** | Discrete and Finite Carrier Restriction | `EXPLICIT_NONCLAIM` | Domain Restriction | §7.2, Item 4 | `ENFORCED` |

---

## 3. Claim Evidence Summaries

### CLM-GR003-001: Point Coincidence as Candidate Key
- **Supersession (2026-10-06):** `VERIFIED` on this row is the frozen 2026-10-01 candidate-key sentence. The corrected statement, recorded in this package's change log and README pointer, is that point coincidence is a superkey. That corrected statement lives in the Witnessed Difference monograph, Appendix O.6. Minimality of $\mathcal{K}$ is not the live claim. The status token on the register row stays `VERIFIED` for the frozen sentence.
- **What it supports:** In any relational event schema where a set of four scalar fields $\mathcal{K}$ uniquely distinguishes physical events ($t_1[\mathcal{K}] = t_2[\mathcal{K}] \implies t_1 = t_2$), $\mathcal{K}$ satisfies $\mathcal{K} \to \mathcal{U}$. That implication is the superkey property. The frozen text also calls $\mathcal{K}$ a candidate key.
- **What it does not support:** It does not prove that four scalar fields can be found globally without caustics, horizons, or coordinate degeneracies in an arbitrary continuous Lorentzian manifold.
- **Narrowest defensible claim:** For any finite dataset of physical events where field measurements distinguish events, point coincidence is isomorphic to candidate key constraint satisfaction.
- **Next test needed:** Evaluation on simulated Regge geometries with coordinate crossings.

### CLM-GR003-002: Lossless Observer Sheet Join via Heath's Theorem
- **What it supports:** Projecting an event relation $r(\mathcal{K}, X, Y)$ into two sub-relations $r_1(\mathcal{K}, X)$ and $r_2(\mathcal{K}, Y)$ preserves all information without spurious tuples upon natural join ($r = r_1 \bowtie r_2$) whenever $\mathcal{K} \to X$ holds.
- **What it does not support:** It does not guarantee that different observers will always agree on the choice of scalar fields $\mathcal{K}$ if some fields are unobservable in certain regions.
- **Narrowest defensible claim:** Heath's theorem applies to any relational schema where observer reference sheets overlap on a functional key.
- **Next test needed:** Multi-observer joins with noisy or bounded-precision field measurements.

### CLM-GR003-008: Exact Rational Dual LP Witness for Relational Obstruction
- **What it supports:** If a discrete 1-cochain of transition residuals $\omega$ cannot be resolved by 0-cochain gauge corrections ($D \alpha$), the exact dual LP over $\mathbb{Q}$ produces a divergence-free circulation $w^* \in \mathbb{Q}^m$ ($D^T w^* = 0, \|w^*\|_\infty \le 1$) certifying $\Phi_1([\omega]) = \langle w^*, \omega \rangle > 0$.
- **What it does not support:** It does not guarantee smooth convergence of the discrete quotient to a smooth continuum differential form as lattice spacing $a \to 0$.
- **Narrowest defensible claim:** Strong LP duality over $\mathbb{Q}$ provides a decidable, zero-float certificate of non-closability for discrete relational transition systems.
- **Next test needed:** Automated generation of minimal dual witnesses on triangulated 4-spheres and tori.
