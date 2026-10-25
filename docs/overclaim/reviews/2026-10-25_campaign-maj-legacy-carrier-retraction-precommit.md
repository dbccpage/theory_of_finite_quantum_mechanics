# Review of campaign-maj-legacy-carrier-retraction

AuthorityEffect: None.

## Scope

MAJ-LEGACY-CARRIER-RETRACTION against origin/main at c50dc1b472596d1b5934408b00b9fbb72db91345. Campaign class Narrowed. Status stays CONDITIONAL. No other node is given a verdict.

## Method

The standing statement and bottleneck were read from dag/derivation_dag.json after the fragment sync. The declarations were read from lean4/CampaignMajLegacyCarrierRetraction.lean. Axiom lines were read from the lake build of that module and from dag/research/campaign_maj-legacy-carrier-retraction_lean_replay.json. This review did not rebuild Lean after that receipt. The independent check checks/independent/maj-legacy-carrier-retraction.py was run and printed failures=0. Scanner command: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict.

## Result

1 FULL for the standing identity-coboundary statement, 0 OVERCLAIM. Campaign class Narrowed. No node was raised.

## Corrections to the PR's own text

None. The standing statement is the identity coboundary on Fin t to Bool. The earlier tetron_carrier.py measurement is not the standing statement.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| MAJ-LEGACY-CARRIER-RETRACTION | `d0`, `d1`, `d0_id`, `nilpotent`, `all_cocycle`, `all_exact`, `isClosed`, `no_closed`, `window_no_closed` | FULL | Each atomic claim of the standing statement is the type of one declaration or the definitions of d0, d1 and isClosed. Status stays CONDITIONAL. |

### Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| A 1-cochain is a function from Fin t to Bool | `V` at lean4/CampaignMajLegacyCarrierRetraction.lean:5 | FULL |
| d0 is the identity on those functions | `d0` at line 9 and `d0_id` at line 22 | FULL |
| d1 sends each 1-cochain to the zero function Fin 1 to Bool | `d1` and `zero1` at lines 7 and 11 | FULL |
| For every vertex function a, d1(d0(a)) equals that zero function | `nilpotent` at line 24 | FULL |
| Every 1-cochain is a cocycle | `all_cocycle` at line 26 | FULL |
| Every 1-cochain is exact | `all_exact` at line 28 | FULL |
| A closed residual is a cocycle that is not exact | `isClosed` at line 19 | FULL |
| No 1-cochain is a closed residual | `no_closed` at line 31 | FULL |
| The same holds for t = 1, t = 2, t = 3 and t = 4 | `window_no_closed` at line 35 | FULL |
| The recorded tetron_carrier.py measurement, a logical-sector reading, and a comparison with the tetron-array family | outside the standing statement | outside |

## Numbers recomputed

| Where | Claimed | Recomputed | Match |
|---|---|---|---|
| statement | t = 1, 2, 3, 4 | the four conjuncts of window_no_closed; independent check vector counts 2, 4, 8, 16 | match |
| independent check | sum of those counts is 30 | 2 + 4 + 8 + 16 = 30 | match |
| independent check | closed residual counts 0 0 0 0 | each enumerated cochain equals d0 of itself, so the unhit count is 0 | match |
| independent check | constant-false coboundary on size 1 has 1 unhit cocycle | the true singleton is not the false singleton; this contrast is a script check, not a standing claim | match |

## Axioms

`d0_id`, `nilpotent`, `all_cocycle`, `all_exact`, `no_closed` and `window_no_closed` depend on no axioms. propext, Classical.choice, Quot.sound and sorryAx are absent. The module imports no package.

## Scanner output

HIGH 0, MEDIUM 0, LOW 3. The LOW rows are pre-existing and were not edited for this identity-coboundary slice. This review did not rebuild Lean.

## What the scanner could not decide

The older citation `legacy_carrier_obstruction` remains on the node. Its hypothesis is trivial first cohomology of a supplied complex. It is not the match for the standing identity coboundary, and it does not put the missing carrier file into that statement.
