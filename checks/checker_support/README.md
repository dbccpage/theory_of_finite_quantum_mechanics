# Independent checker support

AuthorityEffect: None.

This bounded context serves the reviewed finite checkers. It imports
no production implementation or Lean proof. Shared arithmetic is no longer
independent evidence when two checkers use it: the regression suite supplies
separate Bareiss determinant, enumerated-span, exhaustive-cut and collision
oracles for the affected computations.

`Outcome` is the public Railway result. Call
`evaluate(operation, *arguments)` from `checker_support.boundary` to receive either a value or
a typed `Failure`; `bind` short-circuits a failure. The standalone entry points
use `cli`, which turns a failed outcome into a diagnostic and exit status 1.
Low-level arithmetic and fixture helpers use `Violation` for internal control
transfer. Expected type, value and zero-division refusals become input failures;
unexpected programming errors are not silently converted into passing checks.
OS failures become resource refusals. If the diagnostic stream itself is closed
or broken, the CLI still returns a nonzero status.
Success requires an explicit value (which may be `None`); failure requires an
explicit `Failure`. The two variants cannot coexist. `map`, `bind`, and
`value_or` preserve this distinction. Callbacks are trusted synchronous code;
the boundary does not suppress cancellation or promise to terminate a callback.
APIs that already return an `Outcome` are called directly.

`Cases` owns unique case identifiers and the obligation count per invocation.
Named case admissions count once; `require` counts attempted obligations before
checking, including failures. `GaussianRational` and `GaussianMatrix2`
are immutable value objects, with one class per source file. `RationalMatrix`
owns rectangular rational rows, bounds each dimension to 64, and validates
every multiplication/dot-sum intermediate and constructed output. Exact inputs admit
integers and fractions, excluding booleans and floats. Matrix and trajectory
boundaries check shape and carrier membership before computation.
`Failure` owns the closed error vocabulary (`input`, `resource`, `check`,
`duplicate`) in `domains.py`. `Violation` in `boundary.py` is the internal exception adapter, not a second result
model. `MutationCase` is the immutable request value for fault-injection runs.
One-hole replacement is composed into `domains.py`; both Wilson fixtures are
composed into `wilson_operator.py`. Five standalone helper files have been
removed after updating their consumers. Their contract histories are retained
in git history (the retired_support_contracts folder of the review ledger was removed on 2026-11-06).

The resource limits are explicit: 4,096 ordinary sequence entries, 12 refinement
levels (4,096 leaves), 64 bits per refined word, six cells per sign-table
enumeration (64 tables and 4,096 pair comparisons), 12 forest labels, 64
projectors per reduction, and absolute topological charge at most 4,096.
These are validation budgets, not mathematical bounds on the underlying theory.
Rational inputs additionally have a 4,096-bit numerator/denominator budget.
Gaussian components obey that budget on construction and after arithmetic;
exceeding it refuses the operation rather than truncating a result. A computed
norm is an exact `Fraction`. For component numerator/denominator bit budget B,
its numerator needs at most 4B+1 bits and its denominator at most 4B bits;
different denominators can exceed twice the component width. Case
identifiers have at most 1,024 characters, and one `Cases` aggregate admits at
most 100,000 rows. Collection admission snapshots caller-owned containers.

Admission is linear in collection length and integer bit length. `Cases` uses
expected constant-time set lookup plus the identifier's hashing cost; snapshots
use linear time/storage. Gaussian arithmetic and 2-by-2 matrix operations use a
fixed number of exact rational operations. Rectangular `RationalMatrix`
multiplication uses O(mnp) operations, at most 64 cubed scalar products; tensor
dimensions are checked before output construction. Word replacement uses linear work
and storage, with each input and output bounded to 4,096 symbols. GF(2) rank uses
at most 40 basis rows, hence O(40n) bit operations on 40-bit words. Stabilizer
admission has fixed 20-row rank and commutation checks and caches at most 16
immutable tuples. Mincut evaluates ten local choices and two central choices;
it does not enumerate an unbounded graph. Wilson assembly fixes dimensions
4 and 16; determinant elimination uses O(8³) rational operations, with reduced
fractions and no floating-point conversion. These are operation-count bounds;
exact-arithmetic bit costs also depend on the admitted rational sizes.

Run `python -I -B -X utf8 checks/tests/test_review_repairs.py` from the repository
root, and repeat with `-O`. Install the explicitly listed test dependencies from
`checks/tests/requirements.txt` when needed. The workflow
`.github/workflows/reviewed-checkers.yml` runs both modes on Python 3.12 and 3.14.
Local test execution does not imply that hosted CI has run.

Additional checks are `checks/tests/test_checker_support.py` and
`checks/tests/test_mutation_campaign.py`, each in both interpreter modes.
`checks/mypy.ini` and `checks/tests/requirements.txt` pin strict typing and the
test tools. The mutation recipes in `checks/tests/support_mutations.json` replay
through `checks/tests/run_support_mutations.py MANIFEST OUTPUT.json`. The runner
uses disposable copies, checks the baseline first, preserves unfinished cases
on cancellation, and records timeouts/import failures as inconclusive. Its exit
status is deliberately stricter than the rubric: zero requires every observed
candidate to be killed. A surviving candidate proven equivalent is adjudicated
separately; the raw execution record remains unchanged.

The November 3 evidence records the exact source bytes, tool versions, normal
and optimized execution, statement tracing, per-function complexity, consumer
imports, requirements, tests and mutation outcomes. The row-swap mutation has a
separate [domain-specific equivalence argument](../review_ledger/2026-11-03-wilson-swap-equivalence.md).

Contracts beside each source bind the current bytes and fresh evidence.
Historical assessments and receipts remain historical. The required L4B floor
is not obtained by labeling a small fixture or utility L4: capability and grade
are separate axes under `SCORING.md`.
