# File review: the first authorization checkers and companions

AuthorityEffect: None.

Reviewed in the requested source checkout; source and companion bytes listed
below matched the isolated review worktree. All lines of the three Python
files and both pre-existing JSON companions were read. The three scripts ran
with Python 3.14.7 and `-I -B -X utf8`, each exiting zero. Their finite
fixtures do not discharge the open authorization or Rice-theorem questions.

## `auth-dtm2-input-request-planned.contract.score.yaml`

- **File score: 4.** This adjacent contract is required by the requested
  policy and binds the corresponding script's current bytes. Its current
  historical score was `L2D`; that is below the requested L4B floor.
- The evidence pin for `dag/research/pr_371_review_replay.json` says
  `ea5843a9…`; the file currently hashes to `1bf047c7…`. The other cited
  review file matches its pin. Preserve the old record as history and append
  a fresh review/score with valid evidence; do not silently rewrite the old
  receipt or retain a completed current assessment on stale evidence alone.
- The script's delivered capability is L1 under SCORING.md: it processes
  supplied literals and concatenates one fixed list. Its historical L2D
  rating is not a new L4B assessment.

## `auth-dtm2-input-request-planned.py`

- **File score: 3.** Referenced by the campaign note and review records; this
  small fixture can be composed with other independently maintained finite
  fixture runners, while keeping its own named case and original expected
  values. Preserve its standalone-check and provenance requirements when
  designing that composition.
- **Bytes:** `b135684142c5641965411c599eed85bf7de4cd07fbaaf6ef1d50779aa5acb7df`.
- **SCORING.md:** L1, exact finite fixture; a fresh five-gate assessment is
  incomplete and does not meet L4B. Lines 24–34 compare one manually supplied
  list with one expected result; they do not exercise a general encoder,
  decoder, evaluator or rejection function. The accompanying derivation note
  correctly leaves those broader obligations open.
- **Design and verification:** execution happens on import and raises
  `SystemExit`; `failures` is global. Put the case behind `main`, model a
  request and the check result explicitly, use typed failures for invalid
  inputs, and add independent malformed-length/header and round-trip tests
  only when an actual encoder/decoder exists. Do not relabel this fixture as
  evidence for that unimplemented functionality.

## `auth-rice-theorem-import.py`

- **File score: 3.** Referenced by TFQ-1337. Its six-entry behavior table and
  two distinct predicates can become a named finite fixture in the same
  independent checker framework, with the table and expected rows preserved.
- **Bytes:** `4cbd652df0398e081232c960b75d61d868f52e9ac040619cf1d4a6cb9d5a11fb`.
- **SCORING.md:** L1, exact finite table; the assessment remains incomplete
  and L4B is not met. It checks the finite table only; the node correctly
  leaves Rice's theorem imported and the infinite-language claim open.
- **Boundary:** `beh(-1, 0)`, `beh(3, 0)` and `beh(0, 2)` raise raw
  `KeyError`, while `beh(True, 0)` is silently treated as code 1. The CLI
  uses valid fixed values. A bounded code and carrier-index value type plus
  an explicit result/error boundary would make invalid inputs unambiguous;
  test invalid integers and booleans. A shared immutable table can avoid
  recreating the dictionary at every call. The original file had no adjacent
  contract; a new incomplete, byte-bound record is required.
- **Observed execution:** `failures=0 codes=3 rows=12 id_true=2 code_zero_true=1`.

## `authf-carrier-admission-gate.contract.score.yaml`

- **File score: 4.** Required adjacent metadata and its source binding matches.
  Its historical current score `L2D` falls below L4B.
- Its replay evidence pin is `cbade354…` while
  `dag/research/pr_372_review_replay.json` currently hashes to `2bf57189…`.
  The other cited review file matches. Preserve history and append fresh,
  byte-bound evidence and an honest assessment; the closed string fixture is
  L1, not evidence of L4 architecture.

## `authf-carrier-admission-gate.py`

- **File score: 3.** Referenced by the campaign's independent note and prior
  review. Its ten fixed string/flag comparisons can be expressed as a named
  fixture under a shared independent runner without dropping the finite case.
- **Bytes:** `ff3701bbef02f7d2840dc62dca412d05cb01d864aaa4a3964e0994ceed38bd26`.
- **SCORING.md:** L1, non-numeric literal fixture; a fresh complete five-gate
  assessment is not established and the L4B floor is not met.
- **Meaning:** the source assigns literal statuses then checks those same
  values. It verifies this closed fixture and string lengths; it does not load
  the recovered candidate record or detect a change in that record. The
  associated note declares that limitation. Add a byte-bound source-record
  comparison if live-record consistency is desired, while keeping the
  independent closed fixture distinct from the full structural validator.
- **Design:** like the prior script, it executes and exits at import time and
  uses a global failure counter. Extract a main entry point and explicit
  named status/result types if composed; do not invent carrier approval.

## Newly created AdS/CFT companion files

The four AdS/CFT sidecars created during this review each receive **file
score 4**: they are required adjacent metadata and remain incomplete until
the underlying code and all relevant evidence have been repaired and
reassessed. Their JSON history and source-byte bindings were validated with
the repository's `validate_document` helper. The existing governance
population does not include `checks/`, so this validation is not an assertion
that the repository's CI enforces the new user-requested floor there.
