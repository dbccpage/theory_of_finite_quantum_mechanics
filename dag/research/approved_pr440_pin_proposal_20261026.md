# Tested exact-source proposal for PR #440

Status: awaiting explicit user authorization. AuthorityEffect: None until approved.

Source: `lean4/CampaignL1OrthogonalAdditivity.lean`

SHA-256: `50db47282d0bc3fedfe87161c63890be81b0c21a5708f1fc9f2514e6fa6370d2`

Honest score: L2D. Original node: L1-IMP-ORTHOGONAL-ADDITIVITY, CONDITIONAL. Published repair head: `7aeef402315a82eac38af74acb031cd3315646b5`.

Scope: The integer coefficient matrix [[1,1],[-1,1]] has nonzero off-diagonal entries whose sum is zero, and its quadratic form equals a*a+b*b and the sum of its two axis readouts for every integer a,b.

Boundary: One nonsymmetric coefficient matrix; no Gram-matrix or arbitrary orthogonal-frame/projection-measure theorem. General sector additivity remains supplied. Entrywise off-diagonal zero needs symmetry (and in the Hermitian setting the stated real/imaginary sector hypotheses).

The reviewed Lean proof and independent checker pass fresh normal/optimized replays, all declaration audits, all 191 regressions, five README tests, DAG owners/validation/invariants/views, receipt/evidence/facts/status checks, strict overclaim and scoped/full contract history checks. The historical replay bytes remain inside the active replacement after correcting the misleading source comment. The only current governance failure is this proof's L2D floor. The candidate finite_proof_example pin passes the full governance check with zero failures, and was removed after the simulation. The complete simulation and exact candidate are in dag/research/pr440_preapproval_validation_20261026.json.

[CONTRIBUTING.md](/workspace/theory_of_finite_quantum_mechanics/CONTRIBUTING.md:19) requires “explicitly authorized, exact-source support exceptions” below L4/D. Earlier approvals cover different hashes. Approval would apply only the exact path/hash above, with no score/status promotion, baseline or global floor change.
