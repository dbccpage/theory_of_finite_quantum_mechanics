# Independent review of PR #326

Scope: original head 7ef3bddde49172d8ea58c16a22bf2f0456e570e9. Exact source lean4/CampaignPgwDriverBSeventhEvent.lean, SHA-256 c564f055a6e8d1990a81c3100a1ddc8b0c1c70afe7cea1ab919db27d0619a19a.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

A six-constructor case split maps imported events to a supplied list of six distinct names and excludes the literal string Seventh. This does not implement Driver B, a harness refusal, a seal amendment, or sufficiency of these constructors for every lift.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignPgwDriverBSeventhEvent.lean:22 pgwDrvB_kind_count` | `: pgwDrvB_kindNames.length = 6` |
| `lean4/CampaignPgwDriverBSeventhEvent.lean:25 pgwDrvB_kind_nodup` | `: pgwDrvB_kindNames.Nodup` |
| `lean4/CampaignPgwDriverBSeventhEvent.lean:28 pgwDrvB_kindName_mem` | `(e : Event) : pgwDrvB_kindName e ∈ pgwDrvB_kindNames` |
| `lean4/CampaignPgwDriverBSeventhEvent.lean:49 pgwDrvB_names_realized` | `: pgwDrvB_kindName (.supply 0) = "Supply" ∧ pgwDrvB_kindName .admitDatum = "AdmitDatum" ∧ pgwDrvB_kindName (.admitForm 1) = "AdmitForm" ∧ pgwDrvB_kindName (.admitInst 0 []) = "AdmitInst" ∧ pgwDrvB_kindName (.admitRuleAll 0) = "AdmitRuleAll" ∧ pgwDrvB_kindName (.impose 0 1) = "Impose"` |
| `lean4/CampaignPgwDriverBSeventhEvent.lean:58 pgwDrvB_seventh_outside` | `: "Seventh" ∉ pgwDrvB_kindNames` |
| `lean4/CampaignPgwDriverBSeventhEvent.lean:61 pgwDrvB_no_seventh_name` | `(e : Event) : pgwDrvB_kindName e ≠ "Seventh"` |

## Corrections and acceptance

Current capability: **L2**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_326_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
