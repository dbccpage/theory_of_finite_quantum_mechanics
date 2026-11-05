# Checker infrastructure review and repair

AuthorityEffect: None.

This record assesses the nine retained checker-support modules and three new
verification applications. Each receives retention label **5** and **L4B** for
its concrete production role described below. A label is not a claim of
perfection. The remaining independent checker files are reviewed separately;
their use of these modules does not promote their own capability or grade.

| File under `checks/` | Label | Delivered role |
|---|---:|---|
| `checker_support/boundary.py` | 5 | Typed exception adapter, Railway evaluation and resilient CLI failure boundary |
| `checker_support/cases.py` | 5 | Transactional per-run case aggregate, bounded identities and invocation-owned obligation count |
| `checker_support/domains.py` | 5 | Validated exact input schemas, immutable refusal value and bounded word replacement |
| `checker_support/gaussian_matrix2.py` | 5 | Immutable validated Gaussian matrix value object with exact operations and partial inversion |
| `checker_support/gaussian_rational.py` | 5 | Immutable bounded Q(i) value object, exact field operations and operand admission |
| `checker_support/happy_boundary.py` | 5 | Validated stabilizer, entropy and finite-cut services with immutable cached admission |
| `checker_support/mutation_case.py` | 5 | Immutable bounded fault-injection request and unambiguous replacement protocol |
| `checker_support/outcome.py` | 5 | Explicit typed success/failure variants, nullable success and validated Railway composition |
| `checker_support/wilson_operator.py` | 5 | Validated finite Wilson constructions, Clifford checks and exact determinant elimination |
| `tests/test_checker_support.py` | 5 | Independent exact-oracle, boundary and property verification application |
| `tests/run_support_mutations.py` | 5 | Reproducible bounded mutation execution, six-outcome accounting and durable receipts |
| `tests/test_mutation_campaign.py` | 5 | Operational failure injection, accounting mutation calibration and cleanup verification |

Five standalone sources receive label **1** and are removed after composition:
`failure.py` and `word_replacement.py` into `domains.py`; `violation.py` into
`boundary.py`; `run_counter.py` into `cases.py`; and `wilson_determinant.py` into
`wilson_operator.py`. Their former companions receive label **3**, with unchanged
historical bytes composed into the review archive at `retired_support_contracts/`.
All executable consumers have been updated. Every retained module has at most
one class. No low-capability wrapper is retained merely to attach a higher label.

The support README, pinned test requirements, strict mypy configuration and
explicit mutation manifest each receive label **5**. Current adjacent contract
files receive label **5** after source/evidence/history validation.

## Corrected behavior and verification

Exact admission rejects booleans, floats, malformed matrix/word/permutation
carriers, invalid flags, inverted ranges and excessive resource demands.
Gaussian values remain immutable and refuse invalid operands or zero inverses.
Case admission rejects duplicates without partial state changes; iteration is a
snapshot. Named cases and attempted obligations share an invocation-owned count.
The result type requires an explicit variant, supports successful `None`, rejects
simultaneous value/error states, short-circuits failures and validates callbacks'
returned result types. OS errors become resource failures; a broken diagnostic
stream still produces a nonzero CLI status. Unexpected programmer exceptions and
cancellation propagate through the synchronous boundary.

Stabilizer admission now validates before caching and freezes caller-owned input.
The pure-state entropy interface requires independent commuting generators.
Wilson interfaces validate shapes, scalar types, signs and index domains before
indexing. Full operator entries are checked against a separate SymPy block and
Kronecker-product construction, alongside Clifford and gamma5 checks. The
8-by-8 determinant fixture is checked independently by Bareiss elimination.

Verification includes 25 support test groups, 10 mutation-runner groups, and the
24 existing integration groups covering all first 25 reviewed checker CLIs, in
normal and optimized Python. Pinned strict mypy passes for these 12 assessed
source files. The five accounting-replacement mutants in the runner's tests are
also detected. Per-function metrics satisfy CCN <=15, cognitive complexity <=20
and nesting <=4. No production assertion is used, and no module has multiple
classes. Algorithmic and storage bounds are recorded in the support README and
the requirement mapping. Local results do not imply hosted CI execution.

The source mutation campaign executes all 70 explicit candidates: 69 are killed
and one survives. The surviving row-swap-sign mutation is equivalent on the
admitted fixed rational fixture, by the separate
[case argument](2026-11-03-wilson-swap-equivalence.md). Its observed outcome stays
`survived` in the raw receipt. The adjudicated ledger records `equivalent` with
that justification, yielding an exact detection fraction of 69/69 over eligible
candidates. No timeout or harness failure is excluded as a kill. The runner's
raw exit status is 1 because its deliberately stricter execution rule requires
every observed candidate to be killed; this is recorded rather than hidden.

## Boundaries and custody

The source-to-requirement mapping is bidirectional and includes the executable
consumer imports, their paths and hashes, tests and per-module resource bounds.
The assessed roles are concrete runtime boundaries, aggregates, validated value
objects and bounded verification applications. Capability is assigned to those
delivered mechanisms, not inferred from the subject's prestige or from test
counts. The five small standalone helper files were actually composed and removed.

The error vocabulary is closed: `input` for malformed domains and expected
type/value/zero-division refusals; `resource` for declared budgets and OS failures;
`duplicate` for repeated identities; and `check` for failed obligations.
Constructing an invalid refusal value raises `ValueError`, which the application
boundary translates to `input`. Bound-checked indexing, finite loops and validated
immutable states cover admitted computation paths. The callback boundary accepts
trusted synchronous code and promises no termination or resource ownership for
arbitrary callbacks. Mutation recipes are repository-owned executable inputs;
temporary subprocesses are isolation for replay, not a security sandbox.

The hand-encoded stabilizer fixture is not a derived tensor network, and the
two finite Wilson fixtures do not establish continuum or physical statements.
Shared helpers are not independent confirmation of each other. Independent
oracles and generated properties supply the separate checks stated here.

Machine-readable evidence is in `2026-11-03-support-requirements.json`,
`2026-11-03-support-quality-complete.json`,
`2026-11-03-support-mutations-composed.json`, and
`2026-11-03-support-mutations-adjudicated.json`. The quality record includes a
hash-verified, assertion-only test amendment after the mutation snapshot and
its focused normal/optimized retest; production source bytes are unchanged.
Earlier unsuccessful and superseded mutation runs remain separately recorded.
