# Independent review of PR #306

Scope: original head 9b4835c5296d064dfd2f2d2bc34145d20ec493ae. Exact source lean4/CampaignFqGapC500Blocks.lean, SHA-256 c62beca8381b733facbb47a957f171488cdcc26f64ebfb0e92e921916c0bc035.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

A transcribed ten-row clause table and literal arithmetic. Neither target-contract discharge nor a real spectral theorem is established.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignFqGapC500Blocks.lean:24 c500_block_count` | `: c500ClauseRows.length = 10 := rfl theorem c500_clause_sum : c500ClauseSum = 21 := rfl theorem c500_block01_clauses : c500ClauseRows.get ⟨0, by decide⟩ = ("GAP-C500-B01", [])` |
| `lean4/CampaignFqGapC500Blocks.lean:32 c500_block10_clauses` | `: c500ClauseRows.get ⟨9, by decide⟩ = ("GAP-C500-B10", ["M2", "M5", "M7", "J1", "J2"])` |
| `lean4/CampaignFqGapC500Blocks.lean:36 c500_block10_length` | `: (c500ClauseRows.get ⟨9, by decide⟩).snd.length = 5` |
| `lean4/CampaignFqGapC500Blocks.lean:40 c500_target_product` | `: 25 * 10 = 250 := rfl theorem c500_target_last : 301 + 250 - 1 = 550 := rfl theorem ising_poly_one : isingPoly 1 = 0` |
| `lean4/CampaignFqGapC500Blocks.lean:47 ising_poly_neg_one` | `: isingPoly (-1) = 0` |
| `lean4/CampaignFqGapC500Blocks.lean:50 ising_poly_on_square_five` | `: (5 : Int) * 5 - 6 * 5 + 5 = 0` |

## Corrections and acceptance

Current capability: **L1**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_306_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
