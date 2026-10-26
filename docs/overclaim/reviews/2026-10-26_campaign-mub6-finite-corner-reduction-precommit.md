# Review of campaign-mub6-finite-corner-reduction-precommit

Scope: uncommitted derivation of MUB6-FINITE-CORNER-REDUCTION on derive/MUB6-FINITE-CORNER-REDUCTION, merge base 4fea09ae176aae31115e38bb2b21819237055811. Reviewed against the standing statement in dag/fragments/unified_dag.json. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: scripts/overclaim_scan.py --changed-since origin/main --strict. Read the standing statement, obligation, and the cited declarations in lean4/CampaignMub6FiniteCornerReduction.lean with the #print axioms lines from the campaign build. That build was lake build CampaignMub6FiniteCornerReduction, exit 0, Lean 4.35.0. This review did not rebuild. Cargo was not run.

Result: 1 node FULL against the narrowed standing statement, 0 NARROWED, 0 OVERCLAIM. No node was raised. The campaign outcome is Narrowed because the source claim uses an external finite-corner classification. Status stays IMPORTED_ASSUMPTION.

Corrections to the PR's own text:
- None remaining. The standing statement is the integer block identity. The external classification stays in the obligation.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| MUB6-FINITE-CORNER-REDUCTION | b_inv_left, b_inv_right, d_formula, cross_zero, zero_cross_ne | FULL | Each atomic claim of the standing integer statement is the type of a cited declaration. The complex classification and quartet equivalence are in the obligation and are not claimed. Status stays IMPORTED_ASSUMPTION. |

Atomic claims:

- B, E, C, the inverse, and D are the matrices named by bMat, eMat, cMat, bInv, and dMat (lean4/CampaignMub6FiniteCornerReduction.lean:39-78).
- The inverse is two-sided: b_inv_left (line 98) and b_inv_right (line 101). Axioms: propext, Quot.sound.
- D equals the negative of C times the transpose of E times the transpose of the inverse: d_formula (line 104). Axioms: propext, Quot.sound.
- C E^T + D B^T is zero: cross_zero (line 108). Axioms: propext, Quot.sound.
- The same sum with the zero matrix is not zero: zero_cross_ne (line 112). Axioms: propext.

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| derivation note | 3 nonzero entries in the zero-matrix sum | python -I -X utf8 checks/independent/mub6-finite-corner-reduction.py printed cross_nonzero_entries=3 and exited 0 | match |
| README.md | derivation papers 1116; resolving Lean refs 2550; lean4 files 1047; lake libraries 138; module roots 990 | scripts/build_readme_facts.py --check passed. Increments from the base row are +1 paper, +5 Lean refs, +1 lean4 file, +1 library, +1 root. | match |
| standing statement | 3 by 3 integer blocks and the listed rows | the five cited theorems, decided entrywise | match |

The count of 3 nonzero entries is an independent-check count. zero_cross_ne states inequality with the zero matrix and does not state that count.

## Scanner output
HIGH 0, MEDIUM 0, LOW 3. No new HIGH findings. The three LOW findings are the existing baseline items: R10 TENSOR-ASSUMPTION-COUNTERMODELS, R5 tfq_1019 number 20261019, and R5 tfq_0413 fractions 1/2 and 1/4. No baseline change.

What the scanner could not decide: the module has no import. Keeping IMPORTED_ASSUMPTION while the narrowed statement matches Lean is a campaign choice, not a status rise. The external finite-corner classification is not a theorem of this module.
