# MUB(6) evidence atlas

**AuthorityEffect:** None.


This index distinguishes historical records, finite computations, and unresolved
mathematical obligations. It does not assert a complete global cover.

Lean paths below are relative to the source monorepo root, not to this deposit.
The deposit copies only three Lean export and audit files (`lean4/`).

| Surface | Current status | Evidence |
| --- | --- | --- |
| Receipt digest manifest | `verify_all_receipts.py` runs a file-integrity and metadata audit of 11 receipts: SHA-256 digests, float-token rejection, schema and firewall fields. It reports `mathematical_theorem_replay_dispatched: false`. Digest agreement shows byte identity only. | [Manifest](artifacts/manifest.json), [Verifier](code/mub_verify/verify_all_receipts.py) |
| Gap registry & roadmap | 5 Gaps (G1–G5), 9 Residuals (R1–R9); G1 OPEN; R6 and R7 NOT_A_CERTIFICATE; R8 BLOCKED by R7; R9 OPEN. The 2026-10-15 promotions of R6–R9 are withdrawn; see the [review note](research/mub6_review_and_next_derivation.md). | [Gap registry](research/mub6_gap_registry.json) |
| Subgap R6 Matolcsi-Weiner Slices | NOT_A_CERTIFICATE. The computed part is the Tao norm 9 over 20 balanced masks (claim C07). The F6 and H6 verdicts in `mub6_sporadic_chm_solver` are literals. | [R6 Receipt](artifacts/mub_subgap_r6_closure_receipt.json), Lean: `lean4/Conjecture2GeneralMechanization.lean` |
| Subgap R7 Singular Segre SOS | NOT_A_CERTIFICATE. The Stengle identity in Q[a,b,c,d] is valid, but `segre_g_sep` equals -1/1000 on the slice by construction, so it refutes a condition chosen to fail. The 55 CHM equations do not enter. | [R7 note](research/mub6_gap_registry.json), [Script](scripts/compute_r7_singular_segre_sos.py) |
| Master Classification Routing | `corner_routing_classification` checked by the Lean kernel (P_corner != 0 vs P_corner = 0) | Lean: `lean4/MasterClassification.lean` |
| Native gap solver | Fixture, not a computation: the $\Phi_1$ values are fixtures (`mub6_g1_variety.rs`), and the 13/13 count cannot fail because the classifier always returns one of its classes. | Source monorepo: `omega_engine/crates_rs/tests/omega_mub/artifacts/mub6_frontier_report.json` (not in this deposit) |
| Lean formal estate | 185 `.lean` files; the root `Mub6.lean` imports 180 at source commit `2d03b504106356593d76f5a6bafc259019d52247`. Several theorems are conditional interfaces. | Source monorepo: `lean4/research_programs/mub6/` |
| Withdrawn historical statements | "Unconditional" Route C statements in pinned research files are withdrawn. | [Superseded notice](research/superseded_notice.md) |
| Overall mathematical certification | Incomplete. G1 OPEN. R6 and R7 are not certificates; R8 is blocked by R7; R9 is open. Q (no MUB quartet in C^6) is open. | [Claim ledger](mub6_claim_ledger.md) |

See [the plan](mub6_paper_update_and_frontier_synthesis_plan.md) and [the paper](mub6.md) for theorem names, commands, exit codes, scope restrictions, and outstanding obligations.
