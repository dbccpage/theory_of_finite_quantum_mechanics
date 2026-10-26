# Review of campaign GP-IMPORT-CIRCLE-U1

Scope: campaign checkout against origin/main 2064d71f81813cb90f819bb123db7152124b0e09, before the pull request opened. The node is named in the table. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the standing statement, bottleneck and pfp_review in dag/derivation_dag.json; read lean4/CampaignGpImportCircleU1.lean through the declarations and the #print axioms lines; read checks/independent/gp-import-circle-u1.py and dag/derivations/independent/gp-import-circle-u1.md. Scanner: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict (exit 0, HIGH 0, MEDIUM 0, LOW 3). Lean was built in this worktree; this note does not rebuild it again.

Result: 0 FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays IMPORTED_ASSUMPTION.

Corrections to the PR's own text:
- The standing sentence is the integer arithmetic below. The circle group, continuity of a one-parameter phase group, and a selector for that circle stay in the bottleneck.
- The generated audit row still quotes the 2026-10-19 review narrowest_claim (group tables and exponent-two controls). That sentence is the untouched review file, not the standing statement.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| GP-IMPORT-CIRCLE-U1 | signSquare, pairsDiffer, pairCoordsAreSigns, iNorm, iSquare, iSquareNeOne, cycTwice, cycThrice | NARROWED | Standing arithmetic matches the declarations. The prior circle sentence is not the standing statement. |

Statement-vs-theorem:

| Atomic claim | Declaration | Where | Axioms |
|---|---|---|---|
| A sign, an integer equal to 1 or -1, squares to 1 | signSquare | lean4/CampaignGpImportCircleU1.lean:10 | none |
| The pairs (1, 1) and (1, -1) differ | pairsDiffer | lean4/CampaignGpImportCircleU1.lean:15 | none |
| Each coordinate of those pairs is a sign | pairCoordsAreSigns | lean4/CampaignGpImportCircleU1.lean:18 | none |
| The pair 0, 1 has square norm 1, with square norm a * a + b * b | iNorm, gNorm | lean4/CampaignGpImportCircleU1.lean:24 and :27 | none |
| The product of that pair with itself is (-1, 0), with product (a * c - b * d, a * d + b * c) | iSquare, gMul | lean4/CampaignGpImportCircleU1.lean:22 and :30 | none |
| That product differs from (1, 0) | iSquareNeOne | lean4/CampaignGpImportCircleU1.lean:33 | none |
| The map sends 0 to 1, 1 to 2 and 2 to 0, and the second step from 0 is 2 | cyc, cycTwice | lean4/CampaignGpImportCircleU1.lean:35 and :39 | none |
| The third step from 0 is 0 | cycThrice | lean4/CampaignGpImportCircleU1.lean:42 | none |

The circle group, continuity, and a selector are not declarations in this module.

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| sign squares | 1 * 1 = 1 and (-1) * (-1) = 1 | integer product in checks/independent/gp-import-circle-u1.py | match |
| square norm of 0, 1 | 0 * 0 + 1 * 1 = 1 | same script | match |
| product of 0, 1 with itself | (0 * 0 - 1 * 1, 0 * 1 + 1 * 0) = (-1, 0) | same script | match |
| cycle from 0 | second step 2, third step 0 | same script, exit 0 | match |
| lake build | exit 0, wall 18675 ms, module job 782 ms | lake log for CampaignGpImportCircleU1 | match |
| axiom lines | eight empty lists | #print axioms in that build | match |
| README census rows touched by this change | papers 1099, resolving Lean refs 2479, consistent 65, statement_narrowed 69, lean4 files 1030, libraries 121, roots 973 | scripts/build_readme_facts.py --check exit 0 | match |

## Scanner output
HIGH findings: none. MEDIUM findings: none.

LOW findings, left as they stood (they name other nodes and were already present on the base):
- R10 TENSOR-ASSUMPTION-COUNTERMODELS: cited Lean modules in no replay receipt.
- R5 dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md: number 20261019.
- R5 dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md: fractions 1/2 and 1/4.

No baseline entry added. The evidence page lists each cited name twice (qualified and bare), 16 rows for 8 declarations. The receipt covers the 8 declarations.
