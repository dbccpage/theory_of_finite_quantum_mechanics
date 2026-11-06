# Exact-source support exception proposal

PR: https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/421

The mathematical implementation and independent checks are complete. This proposal does not apply a policy change or authorize a merge.

| Source | Exact SHA-256 | Assessed score | Category |
|---|---|---|---|
| `lean4/FiniteGroupPachner.lean` | `e8b2c28cf6e0a0536ba15941742f07d59dc2adcbae86bdfa7311678f6c00cdca` | L3D | `finite_proof_example` |

The proof covers every finite group, every flat boundary of the canonical 4D Pachner pairs, and every finite compatible exterior family represented by dependent pairs. Only that revised node statement changes OPEN to PROVED_LEAN. The historical unnamed state sum, Regge action, general PL topology and fermion-sign claims are not established. Human review remains pending.

Evidence: exact-source `lake build`, all 99 explicit-declaration axiom reports, independent edge enumeration for C1–C5 and noncommutative S3, full C2 Cartesian cross-check, negative controls, and Python optimized-mode execution all pass. All 191 repository regression tests and all DAG, evidence, contract-history and overclaim checks pass. Source bytes were unchanged through replay and publishing. Mathlib source is clean at the recorded pin.

Governance without this pin: 1 failure, solely this L3D proof below L4. A temporary trial with exactly this proposed pin: 0 failures. The policy file was restored. The existing 48 proof pins and the default L4/D floor remain unchanged.

`CONTRIBUTING.md:19` requires “a completed L4-or-higher score ... except for explicitly authorized, exact-source support exceptions.” Earlier approvals cover other hashes. Approval here would authorize only this path/digest at its honest L3D score.

Local validation logs: `/workspace/pachner-derivation/validation.json`, `governance-current.log`, `governance-proposed.log`, `scope-guard.json`.
