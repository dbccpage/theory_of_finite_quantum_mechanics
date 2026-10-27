# Two conditional continuum source exceptions

Status: proposed, awaiting explicit user authorization. AuthorityEffect: None until approved.

The request is for exactly the two source paths and SHA-256 hashes below under the existing `finite_proof_example` policy category. The category name is historical: these modules contain conditional infinite-limit theorems. No capability score, grade, node status, prior pin, acceptance floor or grandfathering entry is raised or broadened.

| PR | Source | SHA-256 | Score | Original node status |
|---|---|---|---|---|
| [433](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/433) | `lean4/DressingFieldRefinementLimit.lean` | `b56f742d6f4d0cbd6c71cc7fe5d9e08fc3660a543e5cf1e34072588009c252fb` | L3D | OPEN |
| [434](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/434) | `lean4/LqgProjectiveLimit.lean` | `44e21fe5531a266095edfbf5a78b818b9e2778dd96c8b4bccd4e800c1dac03a5` | L3D | OPEN |

The first theorem supplies quantitative binary transport convergence, exact limiting composition, endpoint gauge covariance and continuous parameter dependence, with an explicit critical-decay counterexample. It assumes a complete metric topological group and geometric refinement-error control.

The second theorem supplies existence and uniqueness of an infinite finite-alphabet probability measure from compatible normalized finite laws, plus preservation of countably many probability-one local constraints. It does not supply the laws from physical LQG amplitudes. Both original physical continuum obligations remain open.

## Tested evidence

Both exact sources build under Lean 4.35.0 and Mathlib source pin `56a005855ea17e0b0958f73ec801ae140b0a1679`. All explicit declarations pass axiom audits limited to propext, Classical.choice and Quot.sound; no admissions occur. Joint imports compile. The independent checkers pass 14,642 and 1,043 exact checks, normally and under Python `-O`. Each branch passes 191 regressions, all seven DAG sync checks, validation, invariants, views, evidence, receipts, facts/status, strict overclaim and scoped contract/history checks.

Temporary candidate-policy simulations remove exactly the corresponding new-proof acceptance failure. They **do not make the full governance gate pass**: 32 existing source/companion assessments on synchronized remote main are incomplete. A clean-main governance run confirms those exact same failures. All 32 sources and companions are byte-identical to base `948f4e7102e67661381afce3fd9ad3742b719536`. This request neither approves nor repairs them.

Detailed results are committed as `dag/research/campaign_<slug>_integration_validation.json` in each PR; exact replay receipts and full proof notes are also in each PR. Local full governance output is [main-governance.log](/workspace/continuum-two/main-governance.log), and joint replay is [receipt.json](/workspace/continuum-two/joint/receipt.json).

## Why authorization is needed

[CONTRIBUTING.md](/workspace/theory_of_finite_quantum_mechanics/CONTRIBUTING.md:19) requires “a completed L4-or-higher score with composite grade D or higher, except for explicitly authorized, exact-source support exceptions.” These research-domain modules assess honestly at L3D. Existing authorizations cover different path/hash pairs.

If approved, each PR receives only its own new exact pin and the corresponding authorization record. Its proof bytes and honest L3D assessment remain unchanged. Both PRs remain unmerged; the unrelated main assessment failures remain an acceptance blocker.
