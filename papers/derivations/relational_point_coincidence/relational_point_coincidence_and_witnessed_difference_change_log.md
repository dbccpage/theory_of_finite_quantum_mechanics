# Change Log & Provenance Record: Relational Point Coincidence, Witnessed Difference, and Dressing Field Normal Forms

**Document ID:** `GR003-CHANGELOG-V1`  
**Package:** `003_relational_point_coincidence_and_witnessed_difference`  
**Author:** Jeremy H. Carroll  
**Date:** 2026-10-01  

---

## 0. Errata recorded on absorption into WDP (2026-10-06)

The monograph and code of this package are left as published. The following
corrections were found while carrying its ideas into the Witnessed Difference
Programme (Appendices O.6 and P.4) and are checked exactly in that package's
`code/relational_coincidence/` tests:

- Postulate 2.1 / Theorem 2.1: point coincidence is the superkey property.
  Minimality is a separate claim. On this package's own three sample rows the
  minimal keys are {kretschmann}, {matter_density}, {phi0}, {phi1, phi2} and
  {phi1, phi3}, so the four invariants are not a candidate key there.
- "No update anomalies occur" (§3) does not follow from a lossless snapshot
  decomposition; the S,J,T countermodel in WDP's SQL note gives locally legal
  component edits whose rejoin violates a dependency.
- §1.2: the dressing `phi^u = rho(u) phi` lacks the inverse and is not invariant,
  even for Z3. The invariant form is `phi^u = u(phi)^{-1} . phi` with
  `u(g . phi) = g . u(phi)`.
- Prop. 4.1: the stated equivariance `u(phi^g) = g^{-1} u(phi)` has no solution
  in S3, and its proof step needs commutativity.
- Not carried: the gauge-fixing-versus-dressing table, "zero boundary edge
  modes", the undefined "holonomy defect Gamma_2", and Theorem 6.1's VERIFIED
  status (no satisfying instance is constructed).
- Reference fix: Komar (1958) is "Construction of a complete set of independent
  observables in the general theory of relativity", Phys. Rev. 111, 1182.

## 1. Genesis & Provenance Notes

- **2026-10-01 (v1.0.0):** Initial genesis and package admission.
  - Collided the relational invariant approach of Lucrezia Ravera and Jordan François (*Mechanics as a general-relativistic gauge field theory, and Relational Quantization*, arXiv:2510.19845) with Carroll's Witnessed Difference Programme (`000_witnessed_difference_programme`), Local Green Global Red (`001_local_green_global_red_foundational_series`), and Projection Obstruction (`000_projection_obstruction`).
  - Integrated foundational relational database theory (`panep-relational-algebra-theory`): formulated point coincidences as candidate keys $\mathcal{K} \to \mathcal{U}$ and reference-sheet decomposition via Heath's Theorem.
  - Defined executable YAML contracts for Relational Point Coincidence Normal Form (`nf.physics.rpcnf.yaml`) and Dressing Field Normal Form (`nf.physics.dfnf.yaml`).
  - Implemented exact rational verification module `code/relational_spacetime.py` with test suite `code/tests/test_relational_spacetime.py`.
  - Conducted Woland retinue review (Koroviev, Azazello, Behemoth) and Old Man Red Team independent fireproof audit (`AuditFindingV1`), enforcing strict claim hygiene and zero unmechanized proof hype.

---

## 2. Review & Remediation Audit Trail

| Date | Reviewer / Entity | Item / Finding | Resolution / Action Taken |
|---|---|---|---|
| 2026-10-01 | **Koroviev (Prosecutor)** | Warning on gradient degeneracies: four scalar fields may experience $\det(\partial_\mu \phi^I) = 0$ at caustics or horizons. | Added explicit non-claim `CLM-GR003-NON03` fencing universal field independence and requiring chart partitioning. |
| 2026-10-01 | **Behemoth (Challenger)** | Risk of conflating discrete cell complex coboundaries with smooth differential forms. | Clarified in §6 and claim ledger that cochain quotient $\Phi_1([\omega])$ applies strictly to discrete posets/complexes over $\mathbb{Q}$. |
| 2026-10-01 | **Azazello (Builder)** | Verified Heath's decomposition proof and exact rational LP dual witness algorithm. | Implemented test suite in `code/tests/test_relational_spacetime.py` testing candidate key detection, lossless join, and dual witness certification. |
| 2026-10-01 | **Old Man Red Team** | Mandate strict Claim Hygiene: forbid hype verbs (`proves`, `guarantees`, `universal`). | Replaced all ungrounded assertions with scoped phrases ("supports in this setting", "guarantees under declared assumptions"). |
| 2026-10-01 | **governance-symbol-game** | Terminal mapping audit. | Mapped all local verification routes to canonical PFP terminals (`ExactClosureCertified` $\to$ `Preserve`, `OptimalResidualCertified` $\to$ `Repair`). |
