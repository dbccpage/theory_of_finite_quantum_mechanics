# Review of campaign-fq-gap-continuum-hilbert-lift

AuthorityEffect: None.

## Scope

FQ-GAP-CONTINUUM-HILBERT-LIFT against origin/main at 7fa69d621c27bed7045d0b7fe34bbb1d34b27248. Campaign class Narrowed. Status stays CONDITIONAL. No other node is given a verdict.

## Method

The standing statement and bottleneck were read from dag/derivation_dag.json. The four declarations were read from lean4/CampaignFqGapContinuumHilbertLift.lean. Axiom lines were read from dag/research/campaign_fq-gap-continuum-hilbert-lift_lean_replay.json. This review did not rebuild Lean. The independent check checks/independent/fq-gap-continuum-hilbert-lift.py was run and printed failures=0. Scanner command: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict.

## Result

1 FULL for the standing integer statement, 0 OVERCLAIM. Campaign class Narrowed. No node was raised.

## Corrections to the PR's own text

None. The standing statement is the integer slice. The prior selection fence remains pfp_review.prior_statement.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| FQ-GAP-CONTINUUM-HILBERT-LIFT | `twoMulNeOne`, `discIdentity`, `intSqNeFive`, `intPolyNeZero` | FULL | Each atomic claim of the standing statement is the type of one declaration. Status stays CONDITIONAL. |

### Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| No integer a satisfies 2 * a = 1 | `twoMulNeOne` at lean4/CampaignFqGapContinuumHilbertLift.lean:5 | FULL |
| For every integer t, 4 * (t * t - t - 1) + 5 = (2 * t - 1) * (2 * t - 1) | `discIdentity` at lean4/CampaignFqGapContinuumHilbertLift.lean:17 | FULL |
| For every integer n, n * n is not 5 | `intSqNeFive` at lean4/CampaignFqGapContinuumHilbertLift.lean:58 | FULL |
| For every integer t, t * t - t - 1 is not 0 | `intPolyNeZero` at lean4/CampaignFqGapContinuumHilbertLift.lean:66 | FULL |
| scalar-field selection, l2 uniformity, a completion, a Gaussian-integer eigenvalue, the matrix, and Z[i] as a field | outside the standing statement | outside |

## Numbers recomputed

| Where | Claimed | Recomputed | Match |
|---|---|---|---|
| statement | 2 * a = 1 has no integer solution | 2 * a is even and 1 is odd; the independent check audits a from -32 through 32 | match |
| statement | the discriminant identity | both sides expand to 4 * (t * t) - 4 * t + 1; the check audits t from -32 through 32 | match |
| statement | n * n is not 5 | squares of 0, 1 and 2 are 0, 1 and 4; absolute value at least 3 gives a square at least 9, and 9 is greater than 5 | match |
| derivation note | 9 | 3 * 3 = 9 and 9 is greater than 5 | match |

## Axioms

`twoMulNeOne`, `discIdentity`, `intSqNeFive` and `intPolyNeZero` each depend on propext and Quot.sound. Classical.choice is absent. sorryAx is absent. The module imports no package.

## Scanner output

HIGH 0, MEDIUM 0, LOW 7. The LOW rows sit on pre-existing derivation notes and a tensor receipt pin. Those notes were not edited for this integer slice. This review did not rebuild Lean.

## What the scanner could not decide

Older Hilbert-lift citations remain on the node and are not the match for the standing integer statement. They do not put scalar-field selection, l2 uniformity, or a completion into that statement.
