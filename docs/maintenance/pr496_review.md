# PR #496 review and repair

AuthorityEffect: None. The FQ-GLEASON-QI3-FRAME-FUNCTIONS target remains OPEN;
the parent FQ-GAP-BORN-UNIQUENESS-GLEASON node remains CONDITIONAL.

The review of `091ed042e174a1c0112ffeffb5d000708064368e` found three issues:
field-extension claims omitted the partner-vanishing hypothesis, old replay
receipts had been rebound to a new lakefile, and a signed residual was described
as a nonnegative probability function. Commit
`e4967ff43dba7b8765079c66763b62e4326f12bb` narrows the claims, restores the
historical receipt pins and records a separate build-configuration migration.
That migration is not a fresh Lean replay.

The follow-up review repairs two defects in the migration checks. A library
with a different name must not claim a protected module root or an overlapping
namespace. Test migrations must preserve the original bytes, including LF or
CRLF line endings. Regression tests cover both line endings, renamed libraries
with protected roots, ancestor roots, and an unrelated namespace that shares
only a textual prefix.

The research follow-up also now distinguishes a near-identity continuity
squeeze from exact invariance at a fixed rotation. Applying a pole-one theorem
around several coordinate axes requires separate justification; coordinate
permutations do not supply those hypotheses for the same frame function.

## Validation

- 66 tests passed in the governance-policy, changed-contract, replay-evidence,
  Gaussian-rational frame-function and atlas suites. Command:
  `python -I -X utf8 -m pytest scripts/test_governance_policy.py scripts/test_changed_since_contracts.py scripts/test_replay_fqcd_lean.py code/python/tests/test_fq_gleason_qi3_frame_functions.py code/python/tests/test_qm_atlas_loc.py -q -p no:cacheprovider`.
- `scripts/replay_pr492_lean.py --verify-receipts` passed with 33 FQCD anchors
  and 12 FSP anchors. This verifies retained reports and migration boundaries.
- `scripts/verify_qm_atlas_loc.py` passed: 65 questions and 403 links.
- The new Lean module was independently elaborated with Lean 4.35.0 and cached
  dependencies during the earlier review in this chat. Its SHA-256 remains
  `745cd957f5d93e9bcb10f2f28154d779a152f9718caf4fcc788d7a714c3a371a`;
  no Lean source changed during this follow-up. This is a focused module check,
  not a clean rebuild of all dependencies or the repository.

Existing contract grades are retained, with new records for changed source or
evidence bindings; historical contract records and Lean execution logs remain
intact. Hosted checks are assessed separately on the final pushed commit.
