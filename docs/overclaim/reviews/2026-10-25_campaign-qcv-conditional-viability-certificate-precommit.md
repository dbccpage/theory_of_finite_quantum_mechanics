# Review of campaign QCV-CONDITIONAL-VIABILITY-CERTIFICATE

Scope: branch derive/QCV-CONDITIONAL-VIABILITY-CERTIFICATE before the pull request, merge base c50dc1b47259. Reviewed against the statements as they stand in this worktree. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the domain record in dag/fragments/unified_dag.json, lean4/CampaignQcvConditionalViabilityCertificate.lean, and lean4/QcSelfObstruction.lean lines 78-108. Scanner: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict (HIGH 0, MEDIUM 0, LOW 3). The lake build of CampaignQcvConditionalViabilityCertificate exited 0 before this review and is recorded in the campaign receipt. This review pass did not run lake again.

Result: 1 node FULL, 0 NARROWED, 0 OVERCLAIM. This review raises nothing. The campaign statement was already narrowed to a nonnegative initial backlog.

Corrections to the PR's own text:
- None. The standing statement includes nonnegative q0 and the explicit level inequality. A negative initial backlog is outside it.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| QCV-CONDITIONAL-VIABILITY-CERTIFICATE | viability_nonneg_initial (lean4/CampaignQcvConditionalViabilityCertificate.lean:7); viability_explicit_level (lean4/CampaignQcvConditionalViabilityCertificate.lean:19) | FULL | every atomic claim matched: nonnegative q0, g < 1, kappa > 0, the supply bound, c(k) <= C, p(k) >= 0, max(C,1)*p(0) < 1, and the recurrence whenever BacklogBounded lam g (kappa*r) q0 -> viability_nonneg_initial; the explicit level under max(C,1)*p(0) <= 1/2 -> viability_explicit_level. Printed axioms are propext, Classical.choice, and Quot.sound. |

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| checks/independent/qcv-conditional-viability-certificate.py | threshold 2; D*p0 = 2/5; p1 = 1/25; 16 * p1 = 16/25 <= 1 | python -I -X utf8 checks/independent/qcv-conditional-viability-certificate.py, failures=0. By hand: 1/((1-1/2)*1) = 2; 4*(1/10) = 2/5; 4*(1/10)^2 = 1/25; 1*4*2^(2^1) = 16; 16/25 <= 1 | match |
| dag/research/campaign_qcv-conditional-viability-certificate_lean_replay.json | wall_clock_ms 92118 | lake timing of the successful target build; not an arithmetic identity | unrecomputed timing |

## Scanner output
HIGH findings: none. MEDIUM findings: none. LOW findings left in place: R10 on TENSOR-ASSUMPTION-COUNTERMODELS, and R5 on the pre-existing notes for FQ-GAP-TENSOR-UNIQUENESS (20261019) and TENSOR-ASSUMPTION-COUNTERMODELS (1/2, 1/4). No baseline change.

## What the scanner could not decide
Whether the English phrase "that backlog predicate" is BacklogBounded lam g (kappa * r) q0. The declarations use that predicate, and the statement names it. The recurrence remains a hypothesis. No device is in the type.
