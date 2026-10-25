# Review of campaign PGW-DECLARED-INPUT-FLOOR

Scope: worktree branch derive/PGW-DECLARED-INPUT-FLOOR before the pull request, against origin/main at 7fa69d621c27bed7045d0b7fe34bbb1d34b27248. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the node statement, bottleneck and TFQ-0498 record after the pregenesis sync; read lean4/CampaignPgwDeclaredInputFloor.lean; read checks/independent/pgw-declared-input-floor.py and dag/derivations/independent/pgw-declared-input-floor.md. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). This review did not rebuild Lean. The derivation build receipt is dag/research/campaign_pgw-declared-input-floor_lean_replay.json.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN.

Corrections to the PR's own text:
- None in the added paragraph. The four carriers are a finite family. They are not a floor for every later carrier, and the attempt-two search stays unreplayed.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-DECLARED-INPUT-FLOOR | vocabulary_is_two, four_engines, each_declares_stake_not_stream, each_count_is_one, one_below_two, readings_disagree, declared_bounds, empty_carrier_is_not_among_the_four | NARROWED | Two names and four stake-only carriers. A floor for every carrier is open. |

Atomic claims:

| Claim | Declaration | Verdict |
|---|---|---|
| The named list stake, stream has length 2 and the names differ | vocabulary_is_two (lean4/CampaignPgwDeclaredInputFloor.lean:35) | NARROWED |
| The family has length 4 and each pair is stake declared, stream not declared | four_engines (:40), each_declares_stake_not_stream (:43) | NARROWED |
| Each of those four has count 1, and 1 is below 2 | each_count_is_one (:47), one_below_two (:51) | NARROWED |
| On this family, the reading "count at least 2" is false and the reading "count 1" is true | readings_disagree (:56) | NARROWED |
| The numerals are 15, 250, 4, and 2 | declared_bounds (:60) | NARROWED |
| A carrier that declares neither name has count 0 and is not in the family | empty_carrier_is_not_among_the_four (:64) | NARROWED |
| A floor for every carrier, or a reduction past this family | not in the module | NOT PROVED |
| The attempt-two search and carries_forward | not replayed | NOT PROVED |
| The author's freeze ruling | not restated | NOT PROVED |

Axiom lines from the derivation build: all eight theorems depend on no axioms. The allowed set is propext, Classical.choice, and Quot.sound. No sorry, admit, axiom, native_decide or unsafe in the module.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| vocabulary_is_two | length 2 | Lean list length 2; Python len == 2 | match |
| four_engines | 4 carriers | Lean engines.length = 4; Python len == 4 | match |
| each_count_is_one, one_below_two | count 1 below count 2 | Lean count true false = 1 and count true true = 2; Python same | match |
| declared_bounds | 15, 250, 4, 2 | Lean equalities; Python the same four numerals | match |
| empty carrier | count 0 | Lean count false false = 0; Python the same | match |
| independent check | 17 conditions, 0 failures | python -I -X utf8 checks/independent/pgw-declared-input-floor.py | match |
| evidence map | E4 count 0 | build_evidence.py --write reported E4 0 | match |

The module has 8 theorems. A grade page that lists each declaration on the node and again on record TFQ-0498 counts the citation sites, not a second proof. Grade E3 counts files. It is not a statement match.

## Scanner output

HIGH 0, MEDIUM 0. LOW 3, none on this node: R10 TENSOR-ASSUMPTION-COUNTERMODELS; R5 tfq_1019; R5 tfq_0413. No baseline change.
