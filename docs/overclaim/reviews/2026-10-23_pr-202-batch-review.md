# Review of PR #202

AuthorityEffect: None. AI-assisted review; no human attestation.

Scope: 7c2ec2541b18fe7a7f9b6b9afd93f4de697740d9 and the replay-driver repairs in this commit. The import/replay campaign does not change node statuses. A file compilation and an axiom audit remain distinct from proving a node's full statement.

Method: read the replay scheduler, admission lexer, symbol resolver, reference rewriting and provenance inventory; inspect changed-source contract coverage; run the focused regression suite and an actual nine-module Lean replay plus receipt assembly in an isolated fixture checkout. The 236 imported sources were not all rebuilt in this review. Current receipt hashes and existing compilation evidence were not promoted into a new full-campaign claim.

Corrections made:

- `replay_campaign.py`: include `public`, `private` and `meta` imports in the dependency graph. Otherwise a changed public import can escape the resume key.
- Bind resume keys to `lean-toolchain`, `lake-manifest.json`, `lakefile.lean` and actual compiler versions, as well as local dependencies and cited symbols.
- Refuse a failed paper-local sibling compile before a caller can use a stale object.
- Bind paper-local replays to their referenced local Lake modules, and refuse stale inputs again at receipt assembly.

Validation: 29 focused tests pass. The real driver processes nine local modules, audits the named declaration, and assembles a passing fixture receipt. `review_validation.json` retains commands and outputs. The strict mypy diagnostic still reports missing typing in the existing driver/test design; no strict-typing success is claimed.

The overclaim scan reports HIGH=0, MEDIUM=1, LOW=87 against the pre-main merge base. The MEDIUM finding is `PGW-INCIDENCE-CONSTRUCTION-BETTI`: the statement explicitly restricts the Lean claim to the worked cycle/filled triangle and says the general face-closed construction rests on a written argument. `GenesisIncidence.lean:226` and `:238` calculate the worked values (1,1) and (1,0,0) from its proved integer kernels/images. This review accepts the stated finite scope and does not turn it into a general Lean homology theorem. The LOW inventory flags are not all recomputations; no blanket numerical re-verification is claimed.

Merge decision: **not ready**. Of 245 changed code files, 242 still lack companions after the two driver repair companions are added (see `review_contract_coverage.json`). The existing Lake companion also requires current-source assessment. The user-authorized exception for build files, regression tests and byte-identical archives does not waive source custody, the grade-D minimum or honest capability assessment. Some imported Lean files have namespace/import adaptations, so byte-identical-archive treatment cannot be assumed for them. Do not fill these gaps with invented L4 labels.

The driver repair is assessed L4D and its regression suite L2D under the support-file exception; those two assessments do not certify the rest of this PR. Timeout/cancellation propagation, a strict-typing cleanup and the full source-assessment campaign remain open.
