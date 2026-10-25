# Independent review of PR #320

Scope: original head 84599c5b2b496f913dcce664cfbf8bdf1c2bfd9f. Exact source lean4/CampaignPgwPythonLeanCarrierBridge.lean, SHA-256 096d8f363f7190fcf8f5d9cb4058b440307229794ae2507c1d7bf87d827740f3.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

Two closed imported Lean histories replay to the stated distinct regimes. This is not a refinement proof connecting Python execution to Lean semantics, token erasure, or license binding.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignPgwPythonLeanCarrierBridge.lean:20 pgwHistoryL_replays` | `: replayE pgwHistoryL genesis = some R2L` |
| `lean4/CampaignPgwPythonLeanCarrierBridge.lean:24 pgwHistoryF_replays` | `: replayE pgwHistoryF genesis = some R2F` |
| `lean4/CampaignPgwPythonLeanCarrierBridge.lean:28 pgwR2L_ne_R2F` | `: R2L ≠ R2F` |
| `lean4/CampaignPgwPythonLeanCarrierBridge.lean:31 pgwReplay_ne` | `: replayE pgwHistoryL genesis ≠ replayE pgwHistoryF genesis` |
| `lean4/CampaignPgwPythonLeanCarrierBridge.lean:35 pgwData_counts` | `: R2L.data = 2 ∧ R2F.data = 3` |
| `lean4/CampaignPgwPythonLeanCarrierBridge.lean:38 pgwReqs` | `: R2L.reqs = [(0, 1)] ∧ R2F.reqs = [(1, 2)]` |
| `lean4/CampaignPgwPythonLeanCarrierBridge.lean:41 pgwEmpty_carriers` | `: R2L.forms = [] ∧ R2L.insts = [] ∧ R2L.rules = [] ∧ R2F.forms = [] ∧ R2F.insts = [] ∧ R2F.rules = []` |
| `lean4/CampaignPgwPythonLeanCarrierBridge.lean:46 pgwHistory_lengths` | `: pgwHistoryL.length = 7 ∧ pgwHistoryF.length = 8` |

## Corrections and acceptance

Current capability: **L2**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_320_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
