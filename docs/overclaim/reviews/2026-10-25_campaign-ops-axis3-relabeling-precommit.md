# Review of campaign-ops-axis3-relabeling

Scope: branch derive/OPS-AXIS3-RELABELING before the pull request, base c50dc1b472596d1b5934408b00b9fbb72db91345. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the standing statement and bottleneck in dag/fragments/foc035_observer_presheaf.json, the three declarations in lean4/CampaignOpsAxis3Relabeling.lean, the #print axioms lines from the lake build, and checks/independent/ops-axis3-relabeling.py. Scanner: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict. Lean was rebuilt in this worktree before the scan. Cargo was not run.

Result: 1 node NARROWED, 0 FULL, 0 OVERCLAIM. No node was raised. Status stays CONDITIONAL.

Corrections to the PR's own text:
- None. The standing statement is the composition step and the list-length export. Hypotheses (i) and (ii), injectivity, a defect value, and repair versus reinterpretation stay in the bottleneck.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| OPS-AXIS3-RELABELING | exportVerdictRelabel (lean4/CampaignOpsAxis3Relabeling.lean:9), lengthMapInvariant (:18), lengthVerdictRelabel (:22) | NARROWED | Standing sentences match those three declarations. Axioms are none or propext. This fragment accepts Lean references only on lean4/LggrFiniteResults.lean, so the campaign module stays in source and the status stays CONDITIONAL. |

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| independent check | lists 17 at bound 3 | 1+2+4+8 words on {0,1}, plus the two lists [2,0,1] and [3] | match |
| independent check | swap01(0)=1, swap01(1)=0, swap01(2)=2, swap01(3)=3 | the same table in the script | match |
| independent check | failures 0 | script exit 0 | match |
| README.md | derivation papers 1099 in 36 stage folders | build_readme_facts.derivation_papers | match |
| README.md | lean4 tracked .lean files 1030 | build_readme_facts.lean_facts trees | match |
| README.md | lake libraries / module roots 121 / 973 | build_readme_facts.lean_facts | match |

## Scanner output
HIGH 0, MEDIUM 0, LOW 3. The LOW rows are pre-existing: R10 TENSOR-ASSUMPTION-COUNTERMODELS, R5 FQ-GAP-TENSOR-UNIQUENESS 20261019, R5 TENSOR-ASSUMPTION-COUNTERMODELS 1/2 and 1/4. They were not edited. No new HIGH finding.
