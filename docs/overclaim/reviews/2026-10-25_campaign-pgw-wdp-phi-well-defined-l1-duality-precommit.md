# Review of campaign-pgw-wdp-phi-well-defined-l1-duality

AuthorityEffect: None.

## Scope

PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY against origin/main at 7fa69d621c27bed7045d0b7fe34bbb1d34b27248. Campaign class Narrowed. Status stays CONDITIONAL. No other node is given a verdict.

## Method

The standing statement and bottleneck were read from dag/derivation_dag.json. The declarations were read from lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean. Axiom lines were read from dag/research/campaign_pgw-wdp-phi-well-defined-l1-duality_lean_replay.json. This review did not rebuild Lean. The independent check checks/independent/pgw-wdp-phi-well-defined-l1-duality.py was run and printed failures=0. Scanner command: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict.

## Result

1 FULL for the standing integer-triangle statement, 0 OVERCLAIM. Campaign class Narrowed. No node was raised.

## Corrections to the PR's own text

None. The standing statement is the integer triangle slice. The earlier WDP-CH04 wording is not the standing statement.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY | `d0`, `d0_linear`, `residual_shift`, `absSum_shift`, `absSum_ge_two`, `absSum_attained`, `shifted_ge`, `shifted_attained` | FULL | Each atomic claim of the standing statement is the type of one declaration or the definition `d0`. Status stays CONDITIONAL. |

### Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| d0(f0, f1, f2) = (f1 - f0, f2 - f1, f2 - f0) | `d0` at lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean:5 | FULL |
| For all integer vertex triples f and g, d0(f + g) equals the componentwise sum of d0(f) and d0(g) | `d0_linear` at lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean:20 | FULL |
| (delta + d0(g)) - d0(f + g) equals delta - d0(f) | `residual_shift` at lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean:30 | FULL |
| The sum of absolute residual entries is unchanged by that shift | `absSum_shift` at lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean:42 | FULL |
| For delta = (1, 1, 0), every integer repair has absolute residual sum at least 2 | `absSum_ge_two` at lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean:69 | FULL |
| The repair (0, 1, 0) has absolute residual sum 2 | `absSum_attained` at lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean:76 | FULL |
| For every integer g, delta + d0(g) has absolute residual sum at least 2 at every integer repair | `shifted_ge` at lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean:79 | FULL |
| The repair (g0, 1 + g1, g2) has absolute residual sum 2 | `shifted_attained` at lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean:85 | FULL |
| a general cost, a real or complex repair space, weighted duality on an arbitrary complex, rational repairs, a general coefficient field | outside the standing statement | outside |

## Numbers recomputed

| Where | Claimed | Recomputed | Match |
|---|---|---|---|
| statement | residual of (1, 1, 0) at repair (0, 1, 0) has absolute sum 2 | coboundary (1, -1, 0), residual (0, 2, 0), absolute sum 0 + 2 + 0 = 2; independent check failures=0 | match |
| statement | every integer repair of (1, 1, 0) has absolute sum at least 2 | pairing with (1, 1, -1) is 2 and its absolute value is at most the absolute sum; the check audits coordinates from -4 through 4 | match |
| statement | the same bound and the value 2 hold after an integer coboundary shift | residual identity cancels d0(g); the check includes the shift (3, -2, 5) | match |

## Axioms

`d0_linear`, `residual_shift`, `absSum_shift`, `pair_d0_zero`, `pair_residual`, `natAbs_pair_le_absSum`, `absSum_ge_two`, `shifted_ge` and `shifted_attained` depend on propext and Quot.sound. `absSum_attained` depends on propext. Classical.choice is absent. sorryAx is absent. The module imports no package.

## Scanner output

HIGH 0, MEDIUM 0, LOW 3. The LOW rows are R10 on TENSOR-ASSUMPTION-COUNTERMODELS and R5 on two pre-existing derivation notes (20261019, 1/2, 1/4). Those notes were not edited for this integer triangle slice. This review did not rebuild Lean.

## What the scanner could not decide

The older citation `dual_certificate_lower_bound` remains on the node and is not the match for the standing integer-triangle statement. It does not put a general cost, a real or complex repair space, or an arbitrary complex into that statement.
