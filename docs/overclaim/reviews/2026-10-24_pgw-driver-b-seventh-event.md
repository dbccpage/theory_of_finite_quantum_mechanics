# Review of PGW-DRIVER-B-SEVENTH-EVENT

Scope: pre-commit derivation on `derive/PGW-DRIVER-B-SEVENTH-EVENT`, base `1fa451fe1eac640d84f0c34ba88a71dcdd32dfb6`. Reviewed against the statement as it stands in `dag/derivation_dag.json`. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full original claim and compile with only propext, Classical.choice and Quot.sound.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH=0 MEDIUM=0 LOW=0) and `scripts/auto/anti_pattern_lint.py --changed-since origin/main` (0 findings). Read the node statement, bottleneck, obligation, `lean4/CampaignPgwDriverBSeventhEvent.lean`, the `#print axioms` lines in `dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json`, and `inductive Event` in `lean4/Imported/Genesis19l57g1/Derivation/Basic.lean`. Re-ran `python -I -X utf8 checks/independent/pgw-driver-b-seventh-event.py`. The lake build was not rerun for this review; the receipt records exit 0 and wall 6055 ms.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN. Record status stays OPEN_OBLIGATION. AuthorityEffect stays None.

The original claim keeps Driver B open and treats a harness refusal of a seventh constructor as the reason no further lift is admitted. That harness refusal is not a Lean theorem. The current statement is the finite name boundary below. Route `PGW-R-DRIVER-B-SEVENTH-EVENT` is unchanged.

Corrections to the PR's own text:
- None. The name list is stated by `pgwDrvB_kindNames` and the membership theorems. The harness function `append_sealed_event` is not cited as a Lean declaration.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-DRIVER-B-SEVENTH-EVENT | `pgwDrvB_kind_count`, `pgwDrvB_kind_nodup`, `pgwDrvB_kindName_mem`, `pgwDrvB_names_realized`, `pgwDrvB_seventh_outside`, `pgwDrvB_no_seventh_name` | NARROWED | Six constructor names match the declarations. A harness refusal and a theorem that six kinds suffice for every lift stay open. Status stays OPEN. |

Statement-vs-theorem, current statement only:

| Atomic claim | Declaration | Match |
|---|---|---|
| six constructor names Supply, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Impose | `pgwDrvB_kindNames` and `pgwDrvB_kindName` (`CampaignPgwDriverBSeventhEvent.lean:11-20`); constructors at `Derivation/Basic.lean:143-149` | list and match arms |
| name list has length 6 | `pgwDrvB_kind_count` | `length = 6` |
| no duplicate names | `pgwDrvB_kind_nodup` | `Nodup` |
| every event's constructor name is in the list | `pgwDrvB_kindName_mem` | `∀ e, kindName e ∈ kindNames` |
| each of the six names is the name of an event | `pgwDrvB_names_realized` | six equalities |
| the name Seventh is outside the list | `pgwDrvB_seventh_outside` | `"Seventh" ∉ kindNames` |
| every event name differs from Seventh | `pgwDrvB_no_seventh_name` | `∀ e, kindName e ≠ "Seventh"` |
| a harness refuses a seventh constructor | none | open |
| six kinds suffice for every lift | none | open |

Axiom lines recorded in the receipt, inside propext, Classical.choice, and Quot.sound. Classical.choice and Quot.sound do not appear. `pgwDrvB_kind_count`, `pgwDrvB_kind_nodup`, `pgwDrvB_names_realized`, and `pgwDrvB_no_seventh_name` have empty axiom lists. `pgwDrvB_kindName_mem` and `pgwDrvB_seventh_outside` list propext.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement and note | six names, length 6 | checker `len(KINDS) == 6` and `len(set(KINDS)) == 6` | match |
| note | Seventh outside the list | checker `SEVENTH not in KINDS` | match |
| note | example payloads token 0, arity 1, form 0, pair 0 and 1 | those literals are the witnesses in `pgwDrvB_names_realized`; the name does not depend on them | match, name only |
| receipt | wall 6055 ms | lake timing already recorded; not an arithmetic identity | unrecomputed measurement |

Independent check on this review pass: `checked 20 claims, failures 0`.

## Scanner output

Before the receipt re-pin: HIGH=0, MEDIUM=0, LOW=0. After the re-pin, the same scan is HIGH=0, MEDIUM=0, LOW=3. The three LOW rows are pre-existing and sit on TENSOR-ASSUMPTION-COUNTERMODELS and FQ-GAP-TENSOR-UNIQUENESS, whose evidence pages changed only because the tensor receipt pins moved. No baseline entry. Anti-pattern lint 0. The route diff does not contain `PGW-R-DRIVER-B-SEVENTH-EVENT`.

## What the scanner cannot decide

Whether the six constructor names are the Alpha harness's refusal behavior. They are not: `kindName` reads the sealed derivation inductive, and `append_sealed_event` is not an input of these declarations.
