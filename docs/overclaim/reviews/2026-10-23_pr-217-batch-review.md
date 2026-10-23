# Independent review of PR #217

AuthorityEffect: None. AI-assisted review; no human approval is claimed.

Scope: 4cebcbaf1eb98f8ff418bba2a35cffa14a1588f8, its integration with reviewed main, and the evidence-label correction. Result: 2 FULL within the existing scoped mathematical claims; no status promotion. PG-GEN-SUPPLY-NO-OP and PG-GEN-SUPPLY-ERASURE remain PROVED_LEAN.

| Claim | Lean location | Result |
|---|---|---|
| Exact five-field copy/source representation and partial replay | CampaignGenesisReplayRefinement.lean:18-86 | All coordinates and refusal branches are retained; inverse maps and replay commute. |
| Independent array representation, success and failure equivalence | CampaignGenesisReplayRefinement.lean:90-188 | encode/decode inverses, transition commutation and finite-history exactness; no bounded-history hypothesis. |
| Supply erasure and actual state-dependent token erasure | CampaignGenesisReplayRefinement.lean:190-225 | Source and array supply filtering, plus Derivation.erase_replay; token erasure is not a state-independent filter. |
| Potential and unchanged sealed readings | CampaignGenesisReplayRefinement.lean:228-285 | All five coordinates mapped into SecondRun; nondecrease and strict increase on an actual state change. |

A fresh 1039-job targeted Lake build and direct Lean replay pass. All 28 printed declarations use only the permitted foundational axioms. Six dependency hashes match current bytes, and the local Basic source equals sealed Git blob 610d8fc982853807eb892eaaf683fc4eb2959cc1. The external repository commit remains a source-provided pin; it was not fetched anew. Legacy linter warnings are retained in the receipt.

The independent Python census agrees in normal and optimized modes: 92,823 histories over 13 events, lengths 0 through 4 and three bases; 88,808 failures; 429 distinct successful states; 2,289 checked strict changes; 4,681 token histories; three malformed-input refusals. Strict mypy passes. Six hard-coded incorrect-output comparisons were mislabeled as killed mutations; the checker and current review now call them negative controls. A separate real source mutation makes supply admit a datum; the independent array comparison rejects it in both Python modes. Historical author receipts remain historical, not current mutation-coverage claims.

The proof API is assessed L4D. The bounded independent regression checker is L3D under the explicitly approved regression-support exception. Lake registration is L1D under the configuration exception. Complete current assessments preserve prior records and bind the independently replayed bytes. The conservative D ceiling does not claim exhaustive implementation fault coverage, runtime refinement or whole-default-library verification.

Evidence: dag/research/campaign_pg-gen-supply-erasure_review_validation.json. Final integrated campaign checks are recorded separately. This review does not certify Alpha licensing, Python/Rust interpreter behavior, or a new primitive-difference derivation.

Structural repair: the original checker main had cognitive complexity 46, above the rubric E threshold. Its history census, transition checks, token census, negative controls and malformed-input checks now have separate functions. The measured maxima are CCN 16 and cognitive complexity 20. The census output is unchanged; both Python modes, strict mypy, and the actual supply source mutant were rerun after refactoring. The preliminary local score that overlooked the 46 measurement is superseded explicitly in the evidence and preserved assessment history.
