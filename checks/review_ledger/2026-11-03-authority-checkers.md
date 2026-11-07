# Authority checker implementation review — 2026-11-03

AuthorityEffect: None.

The three authority checker sources and their contract test application have
been implemented and assessed at L4B for their declared bounded interfaces.
Each receives retention label 5, with matching source-bound companions. This
label is not a perfection claim. The systematic review continues through
`checks` before `code`.

## Corrections and delivered behavior

- The request script only concatenated embedded literals. It now owns an
  immutable `RequestEnvelope` with exact natural-token admission, detached
  payloads, fixed framing, a bounded parser and Railway decode results. The
  original six-token example remains a control. The codec permits syntactically
  empty segments and does not claim they encode a valid machine. It never
  executes fuel or establishes evaluator/configuration agreement.
- The Rice script exposed only a fixed table. `FiniteBehaviorCarrier` now
  admits bounded rectangular total tables, snapshots nested rows, computes
  stable behavior-equivalence classes, and verifies descent of Boolean code
  predicates. Pairwise comparison supplies an independent generated oracle.
  The original identity predicate descends; code-zero does not. These finite
  algorithms do not establish or instantiate an infinite Rice theorem.
- The candidate script compared strings it had just assigned, so it could not
  detect a changed recovered record. It now reads the actual
  `atlas/papers/foundations/authorization_incompleteness/evidence/original/`
  `computability_carrier_candidates.json`, extracts exactly one direct
  candidate, and verifies the declared open/partial ceiling and false selection.
  The current atlas source and the old worktree copy have identical bytes,
  SHA-256 `4af4d2ba26a0ea47b0f184523a2d7238d4e91d317cb526968e5ebe9bcbb1d102`.
  The repository reorganization is preserved.
- JSON handling rejects duplicate keys, NaN/infinities, malformed encoding,
  oversized input and excessive container nesting. The bounded reader hashes
  the same bytes it parses; it does not reread the file to obtain its digest.
  File contexts close on normal and exceptional paths. The lexical nesting
  scan has explicit outside/inside/escaped string states and ignores brackets
  in strings. This decomposition also repairs the first scanner's excessive
  cognitive complexity.
- All three applications retain their standalone entrypoints, use typed
  refusals, and own invocation-local counts. Each OOP source has one class.
  The request, behavior and ceiling invariants are named in their value-object
  and aggregate contracts; no approval is inferred from a successful check.

## Verification and accounting

The current quality receipt records strict pinned mypy, 16 authority test
groups and 24 first-25 regression groups in normal and optimized Python.
Generated properties cover request layout/round trips and finite behavioral
equivalence/descent. Boundary tests cover empty and maximum payloads/tables,
invalid scalars and indices, malformed records, promotion, exact file-size and
nesting limits, source-byte custody and resource cleanup. Per-source complexity
and operation bounds are recorded in the quality and requirements receipts.

The original mutation run is retained: 40 killed and two survived out of 42.
A valid otherwise-complete record containing a nonstandard JSON constant was
then added as a rejection challenge. The next run detects 41 of 42; the
remaining parser-bool-guard mutant is equivalent under the declared result
contract, as explained below. An additional mutation replacing the test
suite's refusal helper with a no-op is detected. All 43 candidates remain
accounted for: 42 killed, one equivalent, no invalid/inconclusive/unrun cases.

The atlas-path amendment changes one source path literal and preserves the
record bytes. Its previous source hash is reconstructed exactly. The final
test amendment adds only the refusal-helper challenge and import; the previous
test bytes are likewise reconstructed. New normal/optimized integration runs
bind the final sources. No old outcome is overwritten or silently dropped.

## Parser-bool-guard equivalence

The mutant removes only the exact-bool check of the local `selected` value in
`_extract_slice`. All earlier schema, identity and mapping checks are unchanged.
If selected is a bool, the removed branch was never taken and the result is
identical. If it is not a bool, either status extraction refuses it with an
input failure before construction, or construction reaches
`DirectCandidateCeiling.__post_init__`, which applies the same exact-bool
check and refuses it with an input failure. Neither path can return an admitted
value or invoke ceiling verification successfully. These operations perform no
I/O or caller callbacks. Thus acceptance, result value and failure kind are
unchanged for all inputs; diagnostic wording/order is not a stable API in this
contract. The separate constructor-guard mutant is killed by direct-constructor
tests. The parser check is retained as explicit schema narrowing at the parser
boundary; the constructor check protects direct value-object construction.

This equivalence is limited to the stated typed-result contract, not byte-for-byte
exception prose. The raw survivor remains visible in its receipt.

## Scope and consumers

Every source symbol is mapped to a requirement and tests. The three small Lean
files establish their original closed facts only; no new formal theorem is
claimed for the added Python algorithms. Existing script paths and scalar Rice
wrappers are preserved. The carrier check deliberately verifies only the direct
candidate slice: it neither resolves evidence paths nor certifies the other
candidates, the complete structural validator, adequacy, universality or
authorization. Independent code imports shared checking infrastructure only.

The workflow includes the new tests and strict typing for future hosted runs.
This review records local execution; it does not claim a hosted CI result.
