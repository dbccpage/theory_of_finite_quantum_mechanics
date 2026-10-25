# Review of campaign AUTHF-CARRIER-ADMISSION-GATE

Scope: this campaign branch against origin/main at 7fa69d621c27bed7045d0b7fe34bbb1d34b27248. Reviewed against the standing statement in dag/fragments/unified_dag.json and the generated paper dag/derivations/29_computation/tfq_1362_authf_carrier_admission_gate.md:14. Rule applied: a PROVED_LEAN label needs Lean declarations in the repository that state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the standing statement, the obligation, lean4/CampaignAuthfCarrierAdmissionGate.lean, the replay receipt, and checks/independent/authf-carrier-admission-gate.py. Scanner: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict. The review did not rebuild Lean. The receipt records an earlier lake build in this worktree.

Result: 1 node FULL, 0 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN.

Corrections to the PR's own text:
- None. The standing statement is one direct-candidate slice, not the whole candidate inventory and not a refusal of every selection.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| AUTHF-CARRIER-ADMISSION-GATE | `directCeilings` (lean4/CampaignAuthfCarrierAdmissionGate.lean:18), `directNotSelected` (lean4/CampaignAuthfCarrierAdmissionGate.lean:24) | FULL | Each atomic clause of the standing statement is a conjunct of one of those two types. Axiom lines at lean4/CampaignAuthfCarrierAdmissionGate.lean:26 and :27 are empty. |

Atomic clauses of the standing statement:
- Record admission status is the string open: `recordAdmission = "open"` (line 19).
- Direct candidate identifier AIT-DTM0, admission partial, syntax-and-encoding partial, execution-semantics partial, universality open: the next five conjuncts of `directCeilings` (lines 19-21).
- Selected flag is false: `directSelected = false` (line 24).

Left in the obligation (dag/derivations/29_computation/tfq_1362_authf_carrier_admission_gate.md:17): adequacy, replay closure, extensionality, nontriviality, effective reduction, the other three candidate identifiers, a frozen carrier, and a Rice-style claim. The structural validator over the whole JSON record stays with the cited Python check.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Standing statement | open, AIT-DTM0, partial, partial, partial, open, selected false | `checks/independent/authf-carrier-admission-gate.py` | match |
| Derivation note lengths | open has length 4, partial has length 7, AIT-DTM0 has length 8 | same script | match |
| Independent check | failures=0 | `python -I -X utf8 checks/independent/authf-carrier-admission-gate.py` | match |
| Axiom lines | empty for both declarations | receipt output and the lake log for the 2026-10-25 build | match |
| Build | wall 11206 ms, module job 742 ms, exit 0, 3 jobs | `lake build CampaignAuthfCarrierAdmissionGate` in this worktree | match |
| README papers | 1068 to 1069 | `git diff origin/main -- README.md` | match |
| README Lean references | 2287 to 2289 | same diff, two new anchors | match |
| README lake libraries / roots | 90 / 942 to 91 / 943 | same diff, one new lean_lib | match |
| Evidence distinct Lean declarations | 1863 to 1865 | `docs/evidence/README.md` against origin/main | match |
| Evidence receipt-backed | 1801 to 1803 | same | match |
| Evidence itemised | 1733 to 1735 | same | match |
| Evidence grades | E1 stays 222, E2 40 to 39, E3 499 to 500 | same | match |
| OPEN row | E2 8 to 7, E3 62 to 63, E1 stays 74 | same | match |
| COMPUTATION row | E2 4 to 3, E3 64 to 65 | same | match |
| Validator | nodes=925 routes=934 records=977 failures=0 | `dag/validate_derivation_dag.py --no-files` | match |

Generator catch-up from the stale origin/main census, not this node's arithmetic: review directories 178 to 208, P4 mutations 43982 to 47271, tracked dag `.lean` files 3 to 2428, evidence flags 270 on 196 nodes to 253 on 190 nodes, `broken_reference` 70 to 53. `--check` on the README facts and the evidence map is the authority for those pages.

## Scanner output
HIGH 0, MEDIUM 0, LOW 3. No new HIGH. The three LOW findings are pre-existing and were not edited: R10 TENSOR-ASSUMPTION-COUNTERMODELS; R5 tfq_1019 date 20261019; R5 tfq_0413 fractions 1/2 and 1/4. Status did not rise, so R9 does not apply. Pytest on the six campaign DAG modules: 32 passed. The review did not rebuild Lean.
