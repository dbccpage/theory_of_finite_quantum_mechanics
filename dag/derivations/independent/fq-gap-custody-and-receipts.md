Status: AI-drafted, awaiting human review.

# FQ-GAP-CUSTODY-AND-RECEIPTS

AuthorityEffect: None.

Outcome: Narrowed. The node stays OPEN.

## What was counted

The file `sources/atlas/F004_papers/006_finite_qm/claims/claim_ledger.yaml` has a top-level list named `claims`, and a later top-level list named `application_claims`. This census uses only `claims`. Each record in that list begins with `- id:` and has one `type` field. There are 834 such records and 14 distinct type labels.

Ordered by descending count, the labels are:

| Count | Label |
| ---: | --- |
| 160 | FINITE COMPUTATION |
| 156 | SCOPE FENCE |
| 115 | OPEN |
| 104 | DEFINITION |
| 80 | EXACT FINITE ALGEBRA |
| 57 | CONDITIONAL |
| 48 | UNTYPED |
| 36 | ASSERTED |
| 31 | REFUTED BY AUDIT |
| 17 | DECLARED |
| 12 | FINITE FIXTURE |
| 10 | REFUTED BY COMPUTATION |
| 7 | REFUSAL |
| 1 | PARTIAL |

These fourteen counts sum to 834. The label UNTYPED occurs once in the list and its count is 48.

## The gap-register sentence

`sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml` has an entry `GAP-FQM-002`. Its title is `24 claim rows carry no parseable type`. Its description contains the words `24 of 189`. The integers 48 and 24 differ, and the integers 834 and 189 differ. The gap sentence is not the same count as the current claims list.

## What is proved

The Lean census list has length 14, its counts sum to 834, index 6 is `("UNTYPED", 48)`, that label occurs once, `48 ≠ 24`, and `834 ≠ 189`. The independent check reads the two YAML files and finds the same fourteen pairs, the same two inequalities, and the GAP-FQM-002 title and `24 of 189` sentence. The file-wide `- id:` lines are a longer list than the 834 claims, because `application_claims` is separate.

## What is assumed

The census is a transcription of the `type` field of each record in the `claims` list. Lean does not open the file. No added Lean import is used. The six printed axiom lists are empty.

## What is open

GAP-FQM-017, GAP-FQM-019, GAP-FQM-020, GAP-FQM-022, any Zenodo publication claim, and the README code-companion check. A type-label count does not by itself show that a row is unsupported, and a receipt is not a derivation. The node status stays OPEN.
