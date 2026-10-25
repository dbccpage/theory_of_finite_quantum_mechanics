# Review of campaign-comp-c3-no-fixed-bound

AuthorityEffect: None.

## Scope

COMP-C3-NO-FIXED-BOUND against origin/main at c50dc1b472596d1b5934408b00b9fbb72db91345. Campaign class Narrowed. Status stays CONDITIONAL. No other node is given a verdict.

## Method

The standing statement and bottleneck were read from dag/derivation_dag.json after the fragment sync. The declarations were read from lean4/CampaignCompC3NoFixedBound.lean. Axiom lines were read from the lake build and from dag/research/campaign_comp-c3-no-fixed-bound_lean_replay.json. This review did not rebuild Lean after that receipt. The independent check checks/independent/comp-c3-no-fixed-bound.py was run and printed failures=0. Scanner command: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict.

## Result

1 FULL for the standing one-letter bound-1 statement, 0 OVERCLAIM. Campaign class Narrowed. No node was raised.

## Corrections to the PR's own text

None. The standing statement is one letter, no rewrite step, and length bound 1. The earlier computability sentence is not the standing statement.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| COMP-C3-NO-FIXED-BOUND | `ReachB`, `reach_eq`, `reaches_self`, `start_in`, `empty_in`, `long_len`, `long_out`, `not_long`, `not_empty` | FULL | Each atomic claim of the standing statement is the type of one declaration or the definition of `ReachB`. Status stays CONDITIONAL. |

### Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| On lists of the one letter 0, with no rewrite step, reachability is equality | `ReachB.refl` at lean4/CampaignCompC3NoFixedBound.lean:18 and `reach_eq` at line 20 | FULL |
| The length bound is 1 | `bound` at line 7 | FULL |
| The word (0) has length 1 and reaches itself | `start_in` at line 27 and `reaches_self` at line 24 | FULL |
| The empty word has length 0 and is inside the bound | `empty_in` at line 30 | FULL |
| (0) does not reach the empty word | `not_empty` at line 45 | FULL |
| The word (0, 0) has length 2 and is outside the bound | `long_len` at line 33 and `long_out` at line 36 | FULL |
| (0) does not reach (0, 0) | `not_long` at line 39 | FULL |
| A computable start-word map, one bound on every halting start word, and normal-form reachability | outside the standing statement | outside |

## Numbers recomputed

| Where | Claimed | Recomputed | Match |
|---|---|---|---|
| statement | bound 1 | `bound` is the numeral 1; the check prints bound 1 | match |
| statement | (0) has length 1 | one entry; the check prints length 1 | match |
| statement | empty word has length 0 | the empty tuple has length 0 | match |
| statement | (0, 0) has length 2 | two entries; `long_len` and the check both give 2 | match |
| independent check | reached from (0) is only (0) | equality of lists; the empty word and (0, 0) differ from (0) | match |

## Axioms

`reach_eq` depends on no axioms. `reaches_self`, `empty_in`, `long_len`, `long_out`, `not_long` and `not_empty` depend on propext. `start_in` depends on propext and Quot.sound. Classical.choice is absent. sorryAx is absent. The module imports no package.

## Scanner output

HIGH 0, MEDIUM 0, LOW 3. The LOW rows are pre-existing and were not edited for this one-letter slice. This review did not rebuild Lean.

## What the scanner could not decide

The older citations `reachB_iff` and `nfReach_not_computable` remain on the node. They do not state this one-letter bound-1 slice, and they do not put a computable start-word map into that statement.
