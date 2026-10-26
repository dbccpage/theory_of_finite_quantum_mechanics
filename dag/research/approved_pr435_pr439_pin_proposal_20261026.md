# Exact-source proposals for repaired PRs #435 and #439

Status: proposed, awaiting explicit user authorization. AuthorityEffect: None until approved.

| PR | Source | SHA-256 | Honest score | Original target status |
|---|---|---|---|---|
| [#435](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/435) | `lean4/CampaignL1U1SelectorOtherSegment.lean` | `2e1bf569100aacfe8ddc51540eafa0d198880599a0893ab62a8cc552f2fb815d` | L2D | OPEN |
| [#439](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/439) | `lean4/CampaignOpsLeanGap.lean` | `28ba5a6e40e191c1060bd6bf67d33c795a5fdf937e95ed18b894e67649306414` | L1D | OPEN |

The request applies only these two path/hash pairs under the existing `finite_proof_example` category. Previous approvals for DFM and LQG cover different sources. Neither a score nor a node status is raised; the L4/D default floor, baseline and all prior approved hashes are preserved.

PR #435 establishes the stated modulo-7 norm-one orbit and finite solution list. Its repaired independent checker passes 3,005 exact checks: every residue-pair product checks the bounded natural-subtraction encoding against integer arithmetic, with the full orbit, solution set, group-table controls and negative controls. The original C/U(1) selection target and older Gaussian-rational evidence are retained.

PR #439 establishes the four-variable Boolean parity obstruction. Its arithmetic lemma states 2*2*2*2 = 16; the checker separately enumerates the actual 16 assignments. It passes 57 exact checks, including independent integer parity, satisfiable three-constraint subsystems and a consistent right-hand-side variant. The original NCF/Vorobev/no-signalling/normalization/Rust-refinement obligations remain OPEN. Its fragment owner keeps the node's Lean field empty for OPEN targets; all four limited declarations are cited in the TFQ record and replay, without changing that rule.

Both unchanged Lean sources pass fresh minimal Lake builds and audits of every explicit declaration with empty axiom sets. Both checkers pass normally and with Python optimization. Each branch passes 191 regressions, five README tests, required DAG syncs/validation/invariants/views, facts/status/receipt/evidence checks, strict overclaim and scoped/full contract histories.

Governance currently reports exactly one failure per PR: that new proof's below-L4 capability score. A temporary exact-pin simulation passes the full governance check with zero failures for each branch; the candidate pins were then removed. No new proof exception is currently applied.

The concrete repairs and source-bound evidence are published in each PR. Current replay files are `dag/research/pr435_review_lean_replay.json` and `dag/research/pr439_review_lean_replay.json`; current validation files are `dag/research/pr435_repair_validation_20261026.json` and `dag/research/pr439_repair_validation_20261026.json`.

[CONTRIBUTING.md](/workspace/theory_of_finite_quantum_mechanics/CONTRIBUTING.md:19) requires “a completed L4-or-higher score with composite grade D or higher, except for explicitly authorized, exact-source support exceptions.” Approval would authorize exactly the two pins above at L2D and L1D, followed by acceptance rechecks and merge. PRs #433/#437 are excluded from this work at the user's direction; PR #434 already has its separate exact-source approval.
