# Approved finite-proof source exceptions

AuthorityEffect: None. AI-drafted implementation review; no mathematical status is promoted.

The user explicitly authorized the 30 exact proof-module hashes in
`dag/research/approved_finite_proof_exceptions_2026_10_25.json` on 2026-10-25.
They cover the 29 reviewed campaign PRs (#344–#372) and the inherited L2D replay
example from #320. Their recorded L1–L3/D scores remain unchanged.

The global L4/D floor is unchanged. The new `finite_proof_example` category is
restricted to one exact `lean4/Campaign*.lean` module path, a valid SHA-256 digest,
and a nonempty review reason. A changed digest or an unlisted source uses the
ordinary floor. Grade E and incomplete assessments remain rejected. Existing
build-registration, regression-test and source-archive behavior is preserved.

The parser and verifier were tested in the actual checkout: 56 library tests and
10 binary tests passed; one documentation test is ignored. The current test
receipt is `dag/research/approved_finite_proof_policy_validation.json`.
The existing substantive policy and verifier components retain L4D assessments
with fresh source bindings and test evidence; finite examples are not relabelled
as production architecture. No new mutation coverage is claimed.

The combined branch preserves the 29 reviewed statements, statuses, and source
bytes. Its proof and independent Python replays passed before this policy-only
change; their exact source hashes are checked again against the approved pins.
Hosted CI, PR-description publication, and merging still require GitHub API
network access and the repository's normal pull-request flow.


## Additional PR #373 authorization

After the initial approval, PR #373 was reviewed and repaired. Its global Lean
names collided with the reviewed U1-circle module; the Stone declarations now
use their own namespace, DAG references are updated, and a joint import passed.
The standalone Lean proof, independent Python check and combined 87 Python tests
passed. All 30 reviewed PRs retain their exact source hashes and narrowed node
statements. The user explicitly approved this one additional exact pin, recorded
in `dag/research/approved_pr_373_finite_proof_exception_2026_10_25.json`.

The resulting policy has 31 finite-proof pins, with the initial 30 unchanged.
The new proof remains L3D and its node remains CONDITIONAL. The global L4/D floor
is unchanged. The full natural-number descent theorem is kernel checked; the
Python window is a bounded audit, and no continuous-time Stone result follows.
