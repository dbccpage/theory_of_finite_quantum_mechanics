# Review of campaign OPS-LEAN-GAP

Scope: branch `derive/OPS-LEAN-GAP` after one rebase onto `e2caf73fa5321117fc93c8fbdd9ea39a52f38e04`. The Lean file was built on `24afb82a6c84690446fb3ae4a9655cd7ae7dba56` and was not edited again. Reviewed against the statement in `dag/fragments/foc035_observer_presheaf.json` as it stands in this worktree. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). Read the fragment statement and bottleneck, `lean4/CampaignOpsLeanGap.lean`, the replay receipt, `checks/independent/ops-lean-gap.py`, and `dag/derivations/independent/ops-lean-gap.md`. This review pass did not rebuild Lean. The receipt records the earlier `lake build CampaignOpsLeanGap` (exit 0). The source sha256 `28ba5a6e40e191c1060bd6bf67d33c795a5fdf937e95ed18b894e67649306414` matches the file on disk.

Result: 1 node FULL against its standing statement, 0 NARROWED as a mismatch, 0 OVERCLAIM. No node was raised. Campaign outcome class: Narrowed. Status stays OPEN.

Corrections to the PR's own text:
- None. The standing sentence is the four-constraint table. The prior gap (noncontextual fraction, Vorob'ev, no-signalling, rational weights, Rust Scenario) is the bottleneck.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| OPS-LEAN-GAP | `CampaignOpsLeanGap.noAssignment`, `lhsSum`, `rhsSum`, `sixteen` in `lean4/CampaignOpsLeanGap.lean` | FULL against the standing text | Each atomic sentence of the narrowed statement is the type of one declaration. Status stays OPEN: a PROVED_LEAN row in this fragment may cite only `lean4/LggrFiniteResults.lean` and needs a derived route, and this module is not that file. |

Atomic claims:
- No common assignment of the four equations: `noAssignment` (`lean4/CampaignOpsLeanGap.lean:15`).
- Exclusive-or of the four left-hand sides is false for every Boolean assignment: `lhsSum` (`lean4/CampaignOpsLeanGap.lean:7`).
- Exclusive-or of false, false, false and true is true: `rhsSum` (`lean4/CampaignOpsLeanGap.lean:12`).
- There are 16 assignments: `sixteen` states `2 * 2 * 2 * 2 = 16` (`lean4/CampaignOpsLeanGap.lean:20`), and `noAssignment` quantifies over all four `Bool` values.

The receipt lists empty axiom lists for all four declarations. That is inside the allowed set. AuthorityEffect stays None.

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Statement, derivation note, `sixteen` | 16 assignments | `2*2*2*2 = 16`; the independent script walks 16 Boolean tuples | match |
| Independent checker | 19 checks, 0 failures, 0 hits | 16 left-hand-side checks, plus hits, right-hand side, and the product 16 | match |
| Receipt wall times 17.693 s and 1700 ms | build measurement | not a mathematical identity; left as recorded | not recomputed as arithmetic |

## Scanner output
No HIGH or MEDIUM findings. Three LOW findings sit on other nodes whose evidence hashes moved with the tensor-receipt pin: R10 on TENSOR-ASSUMPTION-COUNTERMODELS, and R5 numbers `20261019`, `1/2` and `1/4` in notes this PR does not edit. They are not claims of OPS-LEAN-GAP. No baseline edit.
