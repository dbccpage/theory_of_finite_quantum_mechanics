# Review of campaign GTH-LANG-CORE

Scope: branch `derive/GTH-LANG-CORE` against origin/main `7fa69d621c27bed7045d0b7fe34bbb1d34b27248`. Reviewed against the statements as they stand in `dag/fragments/genesis_to_higher.json` before the pull request. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read `lean4/CampaignGthLangCore.lean` (no import) and the node statement, bottleneck and source list. The campaign `lake build CampaignGthLangCore` exited 0 (module job 930 ms, wall 4409 ms). This review does not rebuild. Mathlib is unused; the package junction was present and not written. Independent check: `python -I -X utf8 checks/independent/gth-lang-core.py` printed `checked 15 conditions, 0 failures`. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH 0, MEDIUM 0, LOW 3.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN. The node lean list stays empty.

Corrections to the PR's own text:
- None. The standing statement is the five-slot carrier, the rule-slot variant and the reach map on 0 and 1.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| GTH-LANG-CORE | `carrier_slots`, `carrier_sum`, `withRule_differs`, `withRule_slots`, `reach_collapses` in `lean4/CampaignGthLangCore.lean` | NARROWED | The standing statement is one closed carrier. Syntax, typing, a deep embedding, the two boxed laws and the MSS-N alphabet stay in the bottleneck. The stage keeps `lean` empty and the route `GAP_NO_DERIVATION`. |

Statement-vs-theorem:

| Claim | Declaration | Verdict |
|---|---|---|
| Carrier data is 1 and forms, instances, rules and requirements are 0 | `carrier_slots` (`CampaignGthLangCore.lean:23`) | NARROWED |
| Slot sum of that carrier is 1 | `carrier_sum` (`CampaignGthLangCore.lean:28`) | NARROWED |
| The carrier with its rule slot set to 1 differs, that rule slot is 1, and data, forms, instances and requirements stay 1, 0, 0, 0 | `withRule_differs` (`CampaignGthLangCore.lean:31`), `withRule_slots` (`CampaignGthLangCore.lean:34`) | NARROWED |
| Reach sends 0 and 1 to 0 | `reach_collapses` (`CampaignGthLangCore.lean:39`) | NARROWED |
| A priced admission language, syntax, typing judgement, deep embedding, boxed laws, or MSS-N alphabet | not proved | NOT PROVED |

Axioms: each `#print axioms` line reports that the theorem does not depend on any axioms. That list is inside propext, Classical.choice and Quot.sound.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Statement, carrier slots | data 1; forms, instances, rules, requirements 0 | `carrier_slots` by `decide`; independent check compares the tuple `(1, 0, 0, 0, 0)` | match |
| Statement, slot sum | 1 | `1+0+0+0+0 = 1` in `carrier_sum` and `slot_sum` in the independent check | match |
| Statement, rule-slot variant | differs; rule slot 1 | `withRule_differs`; `withRule_slots` states rules 1, data 1, forms 0, instances 0, requirements 0 | match |
| Independent check only | slot sum of the rule-slot variant is 2 | `1+0+0+1+0 = 2`; not a sentence of the node statement | match, extra |
| Statement, reach | 0 and 1 map to 0 | `reach_collapses`; independent check calls `reach(0)` and `reach(1)` | match |

## Scanner output

HIGH 0. MEDIUM 0. LOW 3 left unchanged: R10 on TENSOR-ASSUMPTION-COUNTERMODELS, R5 on tfq_1019 number 20261019, R5 on tfq_0413 numbers 1/2 and 1/4. `dag/pfp/generate_prompts.py --write --all-missing` refused the executed prompt for GTH-LANG-CORE and left `dag/prompts/genesis_to_higher_gth_lang_core_open.yaml` unchanged. No baseline entry is proposed.
