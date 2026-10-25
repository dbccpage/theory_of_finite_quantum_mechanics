# Review of campaign AUTH-DTM2-INPUT-REQUEST-PLANNED

Scope: this campaign branch against origin/main at 7fa69d621c27bed7045d0b7fe34bbb1d34b27248. Reviewed against the standing statement in dag/fragments/unified_dag.json and the generated paper dag/derivations/29_computation/tfq_1333_auth_dtm2_input_request_planned.md:14. Rule applied: a PROVED_LEAN label needs Lean declarations in the repository that state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the standing statement, the obligation, lean4/CampaignAuthDtm2InputRequestPlanned.lean, the replay receipt, and checks/independent/auth-dtm2-input-request-planned.py. Scanner: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict. The review did not rebuild Lean. The receipt records an earlier lake build in this worktree.

Result: 1 node FULL, 0 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN.

Corrections to the PR's own text:
- None. The standing statement is one closed request list and one missing header, not the update packet's evaluator or its remaining named targets.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| AUTH-DTM2-INPUT-REQUEST-PLANNED | `oneRequestEncoding` (lean4/CampaignAuthDtm2InputRequestPlanned.lean:20), `zeroHeadDiffersFromHeader` (lean4/CampaignAuthDtm2InputRequestPlanned.lean:26) | FULL | Each atomic clause of the standing statement is a conjunct of one of those two types. Axiom lines at lean4/CampaignAuthDtm2InputRequestPlanned.lean:30 and :31 are empty. |

Atomic clauses of the standing statement:
- Header tag 1, fuel 2, machine-code length 1, segment [7], input word [3, 4]: the first five conjuncts of `oneRequestEncoding` (line 21).
- Concatenating those fields yields [1, 2, 1, 7, 3, 4]: `encodeRequest = [1, 2, 1, 7, 3, 4]` (line 23). `encodeRequest` is the concatenation at line 17.
- The list 0, 2, 1, 7, 3, 4 begins with 0, and 0 differs from the header tag: `head? = some 0`, `header = 1`, and `some 0 ≠ some header` (line 27).

Left in the obligation (dag/derivations/29_computation/tfq_1333_auth_dtm2_input_request_planned.md:17): an encoder and decoder for any other request, the remaining named targets in the update packet, result-level agreement with a bounded evaluator, configuration snapshots, and step-by-step trace agreement. No custody reading and no authorization reading are in the record.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Standing statement | fields 1, 2, 1, 7, 3, 4 and the list 1, 2, 1, 7, 3, 4 | `checks/independent/auth-dtm2-input-request-planned.py` | match |
| Missing header | leading 0 differs from header 1 | same script | match |
| Derivation note length | 6 | same script, `len(encoded) == 6` | match |
| Independent check | failures=0 | `python -I -X utf8 checks/independent/auth-dtm2-input-request-planned.py` | match |
| Axiom lines | empty for both declarations | receipt output and the lake log for the 2026-10-25 build | match |
| Build | wall 19248 ms, module job 878 ms, exit 0, 3 jobs | `lake build CampaignAuthDtm2InputRequestPlanned` in this worktree | match |
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

Generator catch-up from the stale origin/main census, not this node's arithmetic: review directories 178 to 208, P4 mutations 43982 to 47271, tracked dag `.lean` files 3 to 2428, evidence flags 270 on 196 nodes to 253 on 190 nodes, `broken_reference` 70 to 53. `--check` on the README facts and the evidence map is the authority for those pages.

## Scanner output
HIGH 0, MEDIUM 0, LOW 3. No new HIGH. The three LOW findings are pre-existing and were not edited: R10 TENSOR-ASSUMPTION-COUNTERMODELS; R5 tfq_1019 date 20261019; R5 tfq_0413 fractions 1/2 and 1/4. Status did not rise, so R9 does not apply. Pytest on the six campaign DAG modules: 32 passed. The review did not rebuild Lean.
