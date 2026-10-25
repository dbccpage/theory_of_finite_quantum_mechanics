# Review of campaign PGW-DRIVER-B-SEVENTH-EVENT

Scope: branch `derive/PGW-DRIVER-B-SEVENTH-EVENT` against `origin/main` at `7fa69d621`. Reviewed before the pull request was opened. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only `propext`, `Classical.choice` and `Quot.sound`.

Method: read the node statement and bottleneck in `dag/derivation_dag.json`, `lean4/CampaignPgwDriverBSeventhEvent.lean`, the replay receipt, and `dag/derivations/independent/pgw-driver-b-seventh-event.md`. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). The lake build was run in this worktree and exited 0; this review does not rebuild it again. Cargo was not run.

Result: 0 FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN.

Corrections to the PR's own text:
- None. The statement is the six-label guard, not the Alpha harness.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-DRIVER-B-SEVENTH-EVENT | `sealedIndex_supply`, `sealedIndex_admitDatum`, `sealedIndex_admitForm`, `sealedIndex_admitInst`, `sealedIndex_admitRuleAll`, `sealedIndex_impose`, `ofIndex_roundtrip`, `index_roundtrip`, `six_labels_admitted`, `seventh_label_refused`, `amended_bound_accepts_seventh`, `seventh_label_not_a_sealed_index` in `lean4/CampaignPgwDriverBSeventhEvent.lean` | NARROWED | The six indices, both round trips, the bound `k < 6`, and the bound `k < 7` on label 6 are the Lean statements. The Alpha harness, a seventh constructor, a seal amendment, and a factorization of every lift stay in the bottleneck. Status stays OPEN. |

## Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| Supply, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Impose are indices 0, 1, 2, 3, 4, 5 | `sealedIndex_supply` through `sealedIndex_impose` | FULL for this model |
| Each index returns its label | `index_roundtrip` | FULL for this model |
| Each label returns its index | `ofIndex_roundtrip` | FULL for this model |
| The guard `k < 6` accepts those six indices | `six_labels_admitted` | FULL for this model |
| The guard `k < 6` refuses 6 | `seventh_label_refused` | FULL for this model |
| The guard `k < 7` accepts 6 | `amended_bound_accepts_seventh` | FULL for this model |
| No sealed index equals 6 | `seventh_label_not_a_sealed_index` | FULL for this model |
| Alpha harness refuses a seventh constructor | not proved | NOT PROVED |
| Every lift factors through the six kinds | not proved | NOT PROVED |

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Node statement and note | indices 0, 1, 2, 3, 4, 5 | `checks/independent/pgw-driver-b-seventh-event.py` (33 conditions, 0 failures) and the Lean `rfl` theorems | match |
| Node statement | label 6 is refused by `k < 6` and accepted by `k < 7` | the same script and `seventh_label_refused`, `amended_bound_accepts_seventh` | match |
| README inventory lines | regenerated counts | `scripts/build_readme_facts.py --check` passed after `--write` | match to that script |

## Scanner output

HIGH 0, MEDIUM 0, LOW 3. The three LOW findings are not about this node: R10 on `TENSOR-ASSUMPTION-COUNTERMODELS`, and R5 on two derivation notes (`20261019`, `1/2`, `1/4`). They were not introduced by the six-label statement. No baseline change.

## What the scanner could not decide

It cannot see that `appendSealed` is a bound, not `append_sealed_event`. The statement says the harness stays open, and the Lean file has no harness import.
