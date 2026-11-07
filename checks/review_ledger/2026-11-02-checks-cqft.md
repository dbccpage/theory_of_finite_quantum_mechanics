# File review: three causal-QFT checkers

AuthorityEffect: None.

All lines of the three scripts were read in the requested source checkout;
their bytes matched the isolated review worktree. They run as standalone
finite examples and are referenced by the causal-QFT DAG/evidence pages. None
had an adjacent contract at the start of this batch. Python 3.14.7,
`-I -B -X utf8`, produced zero reported failures in all three runs.

## `cqft-causal-factorization-import.py`

- **File score: 4.** The scalar/matrix cocycle and finite-poset examples are
  useful but need domain validation, accurate scope and test coverage.
- **Bytes:** `2fe15214807bfaa155a3d0fc71d60e5f126c836010c680f841bb7ab960f84f6e`.
- **SCORING.md:** L3, Exact profile; G3 **E** is demonstrated below; remaining
  gate evidence is incomplete, composite/token null, L4B not established.
- **Optimization removes a domain check (lines 49–55).** The inverse helper
  uses `assert det in (-1, 1)`. For `((2,0),(0,1))`, normal Python raises
  `AssertionError`; under `python -O` it returns `((2,0),(0,4))`, which is
  not the inverse. Use a validated unimodular-matrix value and an explicit
  typed failure, with normal and optimized subprocess tests. The fixed CLI
  examples use unimodular matrices and passed.
- **Claim and evidence scope.** The header says counterterm dimensions are
  checked for `omega=0..10`; lines 240–243 test only `0..6`. Expand the
  checked cases or correct the header. The historical independent receipt
  binds `2d3005b2…`, not the current source hash; keep it and add a current
  replay receipt. The finite poset and matrix calculations do not establish
  continuum causal factorization.
- **Observed execution:** `checks=795 bogoliubov=356 posetN=32 diagonal=407 failures=0`.

## `cqft-local-net-axioms-import.py`

- **File score: 3.** The referenced finite four-point and matrix fixtures can
  share a small independently tested matrix/poset vocabulary with the other
  causal-QFT checkers. Retain a separate oracle and historical source bytes;
  sharing must not be represented as independent confirmation between two
  copies of the same implementation.
- **Bytes:** `dfb013648776b7adad411c5a10779b82086a053aa9351434bdeb37b62fbd5ff4`.
- **SCORING.md:** L2 for basic matrix/poset procedures, Exact profile;
  G2 is at most D because inputs are not validated, G5 is capped at D by
  Radon 6.0.1's maximum CCN **40**. Other gates are unassessed; L4B not met.
- **Shape and carrier boundaries.** `add2((1,2,3,4),(10,20))` silently
  returns `(11,22)` because `zip` truncates. `spacelike(4,5)` returns true
  although both values lie outside the four-point carrier. Use validated
  fixed-size matrices and point identifiers and explicit typed failures, with
  malformed-shape and outside-carrier tests. The CLI's fixed inputs are valid.
- **Observed execution:** all reported four-point and matrix examples passed;
  this does not verify the continuum local-net axioms.

## `cqft-reeh-schlieder-theorem-import.py`

- **File score: 4.** The referenced finite unfolding and kernel examples
  need matrix-boundary repair and a separate account of their normalization.
- **Bytes:** `817557dd378e4df7b3e2c47be62d16b2e6380b04bef27ce317c3d2800b494088`.
- **SCORING.md:** L3, Exact profile; G3 **E** is demonstrated below; maximum
  CCN 31 caps G5 at D. Other gates are unassessed; L4B not established.
- **Optimization removes a shape check (lines 22–27).** For `[[1]]` times
  `[[1],[2]]`, normal Python raises `AssertionError`; under `python -O`, the
  helper silently returns `[[1]]` even though the dimensions disagree.
  Replace assertions with explicit typed validation for nonempty rectangular
  matrices and matching dimensions, and test both interpreter modes.
- **Fixture meaning.** The displayed GHZ, W and Bell coefficient arrays use
  unnormalized representatives. Nonzero rescaling preserves the rank and
  zero-column observations, but exact left-inverse entries and normalized
  state amplitudes differ. State that convention explicitly. Validate the
  3-qubit site index and coefficient vector length at the helper boundary.
- **Evidence:** the historical independent receipt binds `eb5a18aa…`, not
  the current source hash; retain it and add a current source-bound replay.
  **Observed execution:** `checks=252 duality=227 census=24 translation=1 failures=0`.

The three new adjacent companions each receive **file score 4**: they bind
their subjects but contain deliberately incomplete assessments, requiring
later repair and reassessment. No score here establishes the requested L4B
floor, and the current repository governance population does not enforce the
new user-requested rule for `checks/`.
