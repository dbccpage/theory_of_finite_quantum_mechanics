# Review of campaign COMP-C8-MINIMALITY-FENCE

Scope: this campaign branch against origin/main at 7fa69d621c27bed7045d0b7fe34bbb1d34b27248. Reviewed against the standing statement in dag/fragments/unified_dag.json and the generated paper dag/derivations/29_computation/tfq_1313_comp_c8_minimality_fence.md:14. Rule applied: a PROVED_LEAN label needs Lean declarations in the repository that state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the standing statement, the obligation, lean4/CampaignCompC8MinimalityFence.lean, the replay receipt, and checks/independent/comp-c8-minimality-fence.py. Scanner: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict. The review did not rebuild Lean. The receipt records an earlier lake build in this worktree.

Result: 1 node FULL, 0 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN.

Corrections to the PR's own text:
- None. The standing statement is the closed tape, not the earlier sentence about an arbitrary alphabet, a machine simulation, or a minimality fence.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| COMP-C8-MINIMALITY-FENCE | `oneWordThenBlank` (lean4/CampaignCompC8MinimalityFence.lean:17), `blankDiffersFromMarks` (lean4/CampaignCompC8MinimalityFence.lean:21) | FULL | Each atomic clause of the standing statement is the type of one of those two declarations. Axiom lines at lean4/CampaignCompC8MinimalityFence.lean:24 and :25 are empty. |

Atomic clauses of the standing statement:
- Mark A is 1, mark B is 2, and the blank is 0: the conjuncts `markA = 1`, `markB = 2`, and `blank = 0` in `oneWordThenBlank` (line 18).
- The word mark A then mark B, followed by one blank cell, equals the list 1, 2, 0: `appendBlank [markA, markB] = [1, 2, 0]` in the same type. `appendBlank` is `word ++ [blank]` (line 15).
- The blank differs from mark A and from mark B: `blank ≠ markA ∧ blank ≠ markB` (line 21).

Left in the obligation (dag/derivations/29_computation/tfq_1313_comp_c8_minimality_fence.md:17): simulation of a machine over a coded alphabet, and a sentence that composite machine M0 is not a smallest general-purpose machine. Small-machine records stay literature only. The letter-by-letter code of a finite alphabet stays on COMP-C8-BINARY-CODING.

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Standing statement | 1, 2, 0 and the list 1, 2, 0 | `checks/independent/comp-c8-minimality-fence.py`: mark_a == 1, mark_b == 2, blank == 0, append equals [1, 2, 0] | match |
| Derivation note length | 3 | same script, `len(got) == 3` | match |
| Independent check | failures=0 | `python -I -X utf8 checks/independent/comp-c8-minimality-fence.py` | match |
| Axiom lines | empty for both declarations | receipt output and the lake log for the 2026-10-25 build | match |
| Build | wall 16137 ms, module job 747 ms, exit 0, 3 jobs | `lake build CampaignCompC8MinimalityFence` in this worktree | match |
| README papers | 1068 to 1069 | `git diff origin/main -- README.md`, one new paper | match |
| README Lean references | 2287 to 2289 | same diff, two new anchors | match |
| README lake libraries / roots | 90 / 942 to 91 / 943 | same diff, one new lean_lib | match |
| Evidence distinct Lean declarations | 1863 to 1865 | `docs/evidence/README.md` against origin/main | match |
| Evidence receipt-backed | 1801 to 1803 | same | match |
| Evidence itemised | 1733 to 1735 | same | match |
| Evidence grades | E1 222 to 221, E3 499 to 500 | same | match |
| OPEN row | E1 74 to 73, E3 62 to 63 | same | match |
| COMPUTATION row | E1 14 to 13, E3 64 to 65 | same | match |
| Validator | nodes=925 routes=934 records=977 failures=0 | `dag/validate_derivation_dag.py --no-files` | match |

Generator catch-up from the stale origin/main census, not this node's arithmetic: review directories 178 to 208, boundary directories 166 to 176, P4 mutations 43982 to 47271, tracked dag `.lean` files 3 to 2428, contract `all_passed` false to true, evidence flags 270 on 196 nodes to 253 on 190 nodes, `broken_reference` 70 to 53, L1_TO_L2 flags 13 to 5, FINITE_QM_CORE flags 41 to 32. `--check` on the README facts and the evidence map is the authority for those pages.

## Scanner output
HIGH 0, MEDIUM 0, LOW 3. No new HIGH. The three LOW findings are pre-existing and were not edited: R10 TENSOR-ASSUMPTION-COUNTERMODELS; R5 tfq_1019 date 20261019; R5 tfq_0413 fractions 1/2 and 1/4. Status did not rise, so R9 does not apply. Pytest on the six campaign DAG modules: 32 passed. The review did not rebuild Lean.
