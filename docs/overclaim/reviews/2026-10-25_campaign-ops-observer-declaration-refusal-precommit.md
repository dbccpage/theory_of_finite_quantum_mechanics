# Review of campaign-ops-observer-declaration-refusal

Scope: branch derive/OPS-OBSERVER-DECLARATION-REFUSAL before the pull request, base c50dc1b472596d1b5934408b00b9fbb72db91345. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the standing statement and bottleneck in dag/fragments/foc035_observer_presheaf.json, the four declarations in lean4/CampaignOpsObserverDeclarationRefusal.lean, the #print axioms lines from the lake build, and checks/independent/ops-observer-declaration-refusal.py. Scanner: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict. Lean was rebuilt in this worktree before the scan. Cargo was not run.

Result: 1 node NARROWED, 0 FULL, 0 OVERCLAIM. No node was raised. Status stays CONDITIONAL.

Corrections to the PR's own text:
- None. The standing statement is the five-field slice. The Rust evaluator, a defect receipt, Unicode whitespace other than one space, the terminal token, the typed profile, and any other kernel label stay in the bottleneck.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| OPS-OBSERVER-DECLARATION-REFUSAL | blank_on_accepted (lean4/CampaignOpsObserverDeclarationRefusal.lean:125), mismatch_on_accepted (:155), accepted_draft_class (:191), accepted_authority (:200) | NARROWED | Standing sentences match those four declarations. Axioms are propext, Classical.choice, and Quot.sound. This fragment accepts Lean references only on lean4/LggrFiniteResults.lean, so the campaign module stays in source and the status stays CONDITIONAL. |

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| independent check | blank_cases 15 | 5 fields times 3 blanks (missing, empty string, one space) | match |
| independent check | mismatch_cases 10 | 5 fields times 2 texts (a witness and two spaces) | match |
| independent check | failures 0 | script exit 0 | match |
| README.md | derivation papers 1099 in 36 stage folders | build_readme_facts.derivation_papers | match |
| README.md | lean4 tracked .lean files 1030 | build_readme_facts.lean_facts trees | match |
| README.md | lake libraries / module roots 121 / 973 | build_readme_facts.lean_facts | match |

## Scanner output
HIGH 0, MEDIUM 0, LOW 3. The LOW rows are pre-existing: R10 TENSOR-ASSUMPTION-COUNTERMODELS, R5 FQ-GAP-TENSOR-UNIQUENESS 20261019, R5 TENSOR-ASSUMPTION-COUNTERMODELS 1/2 and 1/4. They were not edited. No new HIGH finding.
