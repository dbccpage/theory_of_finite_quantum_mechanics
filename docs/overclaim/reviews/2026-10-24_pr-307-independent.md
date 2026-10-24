# Independent review of PR #307

Scope: original head 7cb872a2a5ae2cebd5ae2092479d10ac47f9d555. Exact source lean4/CampaignTfq0031StrongCouplingBoundary.lean, SHA-256 6e4b0290412ceb954e4e91b063cd61e6fdccb5322826a1e45f6390140e0aabe9.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

Natural exponent identities and integer evaluations of declared lattice/beta formulas. No lattice construction, Wilson expectation, strong-coupling expansion, or continuum limit is proved.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:15 tfq0031_vertex_count` | `: latticeV = 9 := rfl theorem tfq0031_edge_count : latticeE = 12 := rfl theorem tfq0031_tree_edges : latticeV - 1 = 8 := rfl theorem tfq0031_betti : latticeE - latticeV + 1 = 4 := rfl theorem tfq0031_beta_tilde : (2 : Int) * (3 * 3) = 18` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:26 tfq0031_beta_tilde_reduced` | `: (2 : Int) = 1 * 2 ∧ (2 : Int) * (3 * 3) = 9 * 2` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:29 tfq0031_area_exponent` | `(r t : Nat) : (r + 1) * (t + 1) + r * t = (r + 1) * t + r * (t + 1) + 1` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:42 tfq0031_side_shift` | `(r t : Nat) : (r + 1) + t = r + (t + 1)` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:45 tfq0031_perim_exponent` | `(r t : Nat) : 2 * ((r + 1) + (t + 1)) + 2 * (r + t) = 2 * ((r + 1) + t) + 2 * (r + (t + 1))` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:57 tfq0031_area_pair_22` | `: (2 : Nat) * 2 + 1 * 1 = 2 * 1 + 1 * 2 + 1` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:61 tfq0031_area_pair_23` | `: (2 : Nat) * 3 + 1 * 2 = 2 * 2 + 1 * 3 + 1` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:65 tfq0031_area_pair_32` | `: (3 : Nat) * 2 + 2 * 1 = 3 * 1 + 2 * 2 + 1` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:69 tfq0031_area_pair_33` | `: (3 : Nat) * 3 + 2 * 2 = 3 * 2 + 2 * 3 + 1` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:73 tfq0031_perim_pair_22` | `: 2 * ((2 : Nat) + 2) + 2 * (1 + 1) = 2 * (2 + 1) + 2 * (1 + 2)` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:77 tfq0031_perim_pair_23` | `: 2 * ((2 : Nat) + 3) + 2 * (1 + 2) = 2 * (2 + 2) + 2 * (1 + 3)` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:81 tfq0031_perim_pair_32` | `: 2 * ((3 : Nat) + 2) + 2 * (2 + 1) = 2 * (3 + 1) + 2 * (2 + 2)` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:85 tfq0031_perim_pair_33` | `: 2 * ((3 : Nat) + 3) + 2 * (2 + 2) = 2 * (3 + 2) + 2 * (2 + 3)` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:89 tfq0031_beta0_samples` | `: beta0Num 0 = 11 * 3 ∧ beta0Num 3 = 9 * 3 ∧ beta0Num 5 = 23 ∧ beta0Num 6 = 7 * 3 ∧ beta0Num 16 = 1 ∧ beta0Num 17 = -1` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:94 tfq0031_beta0_window` | `: beta0Window = [33, 31, 29, 27, 25, 23, 21, 19, 17, 15, 13, 11, 9, 7, 5, 3, 1]` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:98 tfq0031_beta1_16` | `: beta1Num 16 = -302` |
| `lean4/CampaignTfq0031StrongCouplingBoundary.lean:101 tfq0031_banks_zaks` | `: -beta0Num 16 * 302 = beta1Num 16` |

## Corrections and acceptance

Current capability: **L2**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_307_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
