# Review of campaign FQ-GAP-C500-ORIGINAL-TARGETS

Scope: worktree branch derive/FQ-GAP-C500-ORIGINAL-TARGETS against origin/main db7b836997721d17ca705f12e168630d1c44cfb8. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the standing statement, bottleneck, and pfp_review; read the nine cited declarations and the printed axiom lines from the lake build. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). Lean was built before this review; this review step did not rebuild.

Result: 1 node NARROWED, 0 FULL, 0 OVERCLAIM. No node was raised. Status stays OPEN.

Corrections to the PR's own text:
- The prior sentence that each original target contract remains open is no longer the standing statement. It remains prior_statement, and the bottleneck says that reading is not run here.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| FQ-GAP-C500-ORIGINAL-TARGETS | `spanLen` (lean4/CampaignFqGapC500OriginalTargets.lean:14), `abut` (line 18), `tenRunEndpoints` (line 22), `tenRunCover` (line 25), `clauseCountsLength` (line 30), `clauseCountSum` (line 32), `lastClauseCountStrict` (line 35), `block10ClauseCount` (line 50), `block10ClausesNodup` (line 52) | NARROWED | Standing text matches those declarations. The original contracts and the evidence files are not declarations. |

## Statement versus theorem
| Claim in the standing statement | Declaration | Verdict |
|---|---|---|
| for every natural number k, 276 + 25 * k through 300 + 25 * k is a run of 25 | spanLen | FULL |
| the next run starts at the next numeral | abut | FULL |
| the ten runs begin at 301 and end at 550 | tenRunEndpoints | FULL |
| those runs cover 250 numerals and 10 * 25 = 250 | tenRunCover | FULL |
| the ten clause-list lengths are 0, 2, 4, 2, 4, 1, 1, 1, 1, 5 | clauseCounts and clauseCountsLength | FULL |
| those lengths sum to 21 | clauseCountSum | FULL |
| the last length 5 is strictly greater than each earlier length | lastClauseCountStrict | FULL |
| the five labels M2, M5, M7, J1 and J2 are pairwise distinct | block10ClausesNodup and block10ClauseCount | FULL |
| each original target contract remains open | not proved | NOT PROVED |
| a scoped receipt discharges a block | not proved | NOT PROVED |

Axiom lines from the build: spanLen and abut use propext and Quot.sound. tenRunEndpoints, tenRunCover, clauseCountsLength, clauseCountSum, lastClauseCountStrict, block10ClauseCount, and block10ClausesNodup depend on no axioms.

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement and independent check | run length 25 and abutment for every k | SymPy on the closed form, plus k = 0 through 20 | match |
| statement and independent check | 301, 550, cover 250, 10 * 25 = 250 | integer arithmetic | match |
| statement and independent check | lengths sum to 21 and last length 5 is strictly greatest | integer sum and comparison | match |
| statement and independent check | five distinct labels | set of five strings | match |

## Scanner output

HIGH 0, MEDIUM 0, LOW 3. No new HIGH finding. The LOW findings are outside the standing statement of this node.
