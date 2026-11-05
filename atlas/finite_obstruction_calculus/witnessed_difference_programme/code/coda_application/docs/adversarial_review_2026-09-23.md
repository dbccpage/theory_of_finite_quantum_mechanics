# CODA adversarial review

Historical record: all source locations, counts, runtime measurements and repair claims below refer to the stated September revisions. Current code uses the native functional evaluator, a separate composition root and the [current scoped catalog](test_catalog_and_failure_modes.md). Passing the old finite fixtures did not exclude later defects; reproducing an expected failure also does not by itself rule out every possible test bug.

**AuthorityEffect:** None.

**Date:** 2026-09-23. **Target:** `apps/coda` at `origin/main` `cc4f3c4a`.
**Suite:** [`apps/coda/tests/adversarial/`](../tests/adversarial), 215 tests in eight files.
**Interpreters:** CPython 3.12.10 and 3.14.2. The results were identical on both.

**Repair status (later on 2026-09-23):** every break below has been fixed. §§1–6 record the review as run against `cc4f3c4a` and are left unchanged; §7 records the repair.

## 1. Verdict

`apps/coda` presents itself as an exact-arithmetic referee and a fail-closed
authority firewall. The suite tried to break the claims that make up that
description, and 153 of the 215 tests succeeded. Each break is recorded as a
strict `xfail`. The other 62 tests are controls, and each of them confirmed that
a stated defence holds.

| Severity | Breaks | Meaning |
|---|---:|---|
| Critical | 34 | An input or call reaches `AUTHORIZED`, or an authorized-looking token or outcome, where the stated claims forbid it |
| High | 45 | Wrong mathematics (Φ₁, witnesses, Γ₂), falsified evidence, a genuine residual refused, or a fail-open guard |
| Medium | 50 | A crash where a refusal was claimed, a gap in integrity or immutability, a budget or architecture defect |
| Low | 24 | Drift between documentation and claims, or CLI and packaging hygiene |
| **Held** | **62** | Controls that confirm a stated defence works |

The full `apps/coda/tests` run passes on both interpreters: 91 passed (the 29
original tests plus the 62 controls), 153 strict xfails, 0 failures and 0 XPASS.
A second run with `--runxfail` made all 153 breaks fail, each on its claim line
or with its pinned exception. That rules out a precondition or a bug in a test
as the cause of any recorded break.

Six findings matter most:

- **FOC-01..09, FOC-24..26.** The Layer-1 Φ₁ is not the L1 quotient distance.
  It is a single feasible dual pairing, so it is a lower bound that is often
  loose and sometimes **zero on an obstructed cochain**. Against the FOC
  package's exact LP, it disagreed on 27 of 60 seeded general complexes and on
  14 of 40 random digraphs. It also reported 5 false zeros.
- **FOC-02/05/14, EXA-04.** Those false zeros become **AUTHORIZED**. Four
  independent constructions obtain a token for an obstructed instance: a zero
  repair column, cancelling circulations, extra cochain rows, and a float cochain.
- **FW-17/19, PIPE-01, CLI-01, REG-10/13.** Authority is **a boolean supplied by
  the caller**. The strings `"no"` and `"false"` authorize. The PROPOSER role
  authorizes itself. Any caller can construct an `AuthorityToken` that compares
  equal to an issued one.
- **FW-01..12.** The firewall **trusts hand-built evidence**. It believes
  `is_mathematically_valid`. GUARD_3 checks only the pairing: it checks neither
  ker(D₀ᵀ) nor ‖y‖∞ ≤ 1. Evidence is not bound to the problem it is presented for.
- **PIPE-02..09, TRI-01..04.** **Layers 2–5 never gate the outcome.** The triad
  path also discards the Layer-7 refusal. An empty support sieve with a license
  is REFUSED by one entry point and AUTHORIZED by the other. On random instances
  the two paths disagree 23 times in 40.
- **AUD-01/02.** The firewall audit use case is made of bare `assert`
  statements that re-run the same solver. Under `python -O` it reports a
  planted breach as passed. In normal mode it passes the false-zero
  obstruction.

## 2. Method

- **Claims, not guesses.** Each test states an invariant that CODA asserts about
  itself and cites where it is asserted: the README, a docstring, the
  [catalog](test_catalog_and_failure_modes.md), or an F005 claim ID. When a test
  holds a debatable reading to account, the break text says so. Examples are
  "unknown roles should refuse" and "a blank hypothesis does not inhabit the sieve".
- **Oracle.** Φ₁ is compared against
  `coda_atlas/F005_coda/foc/code/finite_obstruction.py`
  (`LinearRepairProblem.quotient_l1_distance`). That function is an exact
  primal/dual vertex enumeration whose `QuotientDistanceCertificate` rechecks
  itself. It is loaded by file path, so this suite adds no oracle code.
- **Recording breaks.** `BREAK(id, why, raises=...)` in
  [`_support.py`](../tests/adversarial/_support.py) is
  `pytest.mark.xfail(strict=True, raises=...)`. Pinning `raises` means a
  different crash is not counted as the recorded break. Once a fix lands, the
  test XPASSes and fails the run, so the marker has to be removed along with the
  fix. The crash tests treat a clean `ValueError`/`TypeError` refusal as a pass.
  A proper fix therefore flips them too.
- **Randomness is seeded:** 20260923 and its offsets. Timing tests (TRI-12,
  CLI-04) compare a budget against wall time. They are machine-dependent only
  in their margin: the observed ratios are 50–90× and about 4×.

Reproduce from the repository root:

```bash
python -m pytest apps/coda/tests -n 8 -p no:cacheprovider --basetemp "$TEMP/coda-adv" -q
```

```bash
python -m pytest apps/coda/tests/adversarial -n 8 -p no:cacheprovider --basetemp "$TEMP/coda-adv" -q --runxfail
```

## 3. Findings by root cause

### 3.1 Φ₁ is a single dual pairing, not an L1 quotient distance (High → Critical)

- **General path**
  ([exact_solver_adapter.py:215](../infrastructure/exact_solver_adapter.py#L215),
  duplicated in [solve_l1_repair.py:43](../use_cases/solve_l1_repair.py#L43)).
  The code takes `nullspace()[0]`, scales it to ‖w‖∞ = 1, and returns |⟨w, c⟩|.
  When dim ker(D₀ᵀ) > 1, that is one feasible point of the dual LP and not its
  maximum (FOC-T2). If the first basis vector annihilates c, the result is
  **0 for an obstructed cochain**, which violates FOC-T1 definiteness and
  FOC-C1.
  - Repro: `d0 = zeros(2,1)` with `c = [0, 5]` gives Φ₁ = 0; the true value is 5.
  - Repro: `d0 = [[1],[1],[1]]` with `c = [1,1,0]` gives 0; the true value is 1.
- **Graph path**
  ([exact_solver_adapter.py:163](../infrastructure/exact_solver_adapter.py#L163)).
  The code sets y = +1 on disjoint directed cycles regardless of the sign of
  each cycle's circulation.
  - Repro: two 2-cycles with circulations +2 and −2 give Φ₁ = 0; the true value is 4.
- **Sign.** Φ₁ is reported as |⟨w, c⟩|, but w is never flipped (FOC-10). The
  firewall's own GUARD_3 then refuses the genuine residual (FOC-11).
- **Invariance.** Re-orienting edges changes the reported value (FOC-12).
  An L1 distance cannot change under re-orientation.
- **Fix direction.** Use `LinearRepairProblem.quotient_l1_distance` as the
  reference, and a genuine exact LP (a rational simplex, or the `omega_solvers`
  crate once the bridge actually runs) for large instances. Return and check a
  primal repair so that "zero duality gap" is certified (DOC-08). At minimum,
  the false-zero case can be closed by picking a kernel vector with ⟨v, c⟩ ≠ 0,
  as the FOC exactness certificate already does.

### 3.2 Authority is a caller-supplied boolean (Critical)

- **The flag is only truth-tested.**
  [layer8_fda.py:48](../domain/layers/layer8_fda.py#L48) reads
  `fda_license_granted`, and the firewall's `external_license_granted` is
  handled the same way (PIPE-01, FW-19: `"no"`, `"False"` and `[False]` all
  authorize).
- **The caller who wants authority is the one who supplies it.** Any caller,
  including the PROPOSER role, passes the flag (FW-17). The resulting token
  names the proposer as its own licensee (FW-18). `coda evaluate --licensed`
  mints a token from the command line (CLI-01).
- **`AuthorityToken` checks a boolean it is handed**
  ([entities.py:101](../domain/entities.py#L101)).
  - Any caller constructs one (REG-10).
  - `object.__new__` skips the check (REG-11).
  - `dataclasses.replace` re-issues a token to a new licensee (REG-12).
  - The predictable id `AUTH-<problem_id>` makes a forged token compare equal
    to the issued one (REG-13).
  - The token is not bound to evidence, so it replays into another outcome
    (REG-14).
- **Fix direction.** Represent a license as verified evidence, not a bool, and
  compare with strict identity (`is True`) at the very least. Derive guards from
  an evidence record, as `coda_atlas/F005_coda/fda/code/coda_fda_core.py`
  (`derive_guards`, `_validate_exact_bool`) already does. Bind each token to a
  hash of the problem and the evidence.

### 3.3 The firewall trusts forged evidence (Critical/High)

- **Validity is self-declared.**
  [firewall_engine.py:158](../domain/firewall_engine.py#L158) routes on
  `evaluation.is_mathematically_valid`. Φ₁ = 2 or Γ₂ = 3 is authorized when the
  flag says valid (FW-01, FW-02).
- **GUARD_3 checks only the pairing**
  ([firewall_engine.py:123](../domain/firewall_engine.py#L123)).
  - A witness outside ker(D₀ᵀ) is accepted (FW-03).
  - y = [100, 100] inflates Φ₁ from 2 to 200, and the register stores 200 (FW-04, FW-05).
  - A negative Φ₁ skips the guard (FW-06).
- **Some guards cannot refuse anything.**
  - GUARD_2 validates a value that is already a `Rational` (FW-07).
  - GUARD_5 is appended unconditionally
    ([firewall_engine.py:145](../domain/firewall_engine.py#L145), FW-20).
  - GUARD_3 is reported as passed when no witness was checked (FW-21).
- **Unknown roles pass GUARD_1.** So do `"AUTHORITY "` with a trailing space and
  a Greek Omicron homoglyph (FW-13..15). `caller_role=None` crashes (FW-16).
- **Evidence is not bound to its problem.** Evidence for problem A authorizes
  problem B, and a proposal for A yields a token for B (FW-11, FW-12). Evidence
  that carries a FAILED Layer-7 record is still authorized (FW-09).
- **Fix direction.** The firewall should recompute evidence or fully verify it:
  kernel membership, norm, pairing, primal/dual equality, and a problem hash. It
  should reject unknown roles and route on the recomputed Φ₁ and Γ₂ rather than
  on a flag.

### 3.4 Layer failures do not gate; the two entry points disagree (Critical)

- **The pipeline drops layer results.**
  [evaluate_pipeline.py:52-64](../use_cases/evaluate_pipeline.py#L52) binds the
  Layer 2–5 results to `_loss`, `_refinement`, `_sep` and `_diam`, then drops
  them. Layer 8 sees only Φ₁, Γ₂ and the Layer 7 result.
  - An inverted enclosure, a failed fiber check, or a measured transport loss
    of 13/2 each end AUTHORIZED (PIPE-02..05, PIPE-09). This contradicts
    catalog PIP-01 and G4/G5.
  - Layer 4 has no failing branch at all (PIPE-08).
- **The triad drops Layer 7.** The triad binds the Layer-7 verdict to
  `_refused` ([evaluate_pipeline.py:154](../use_cases/evaluate_pipeline.py#L154))
  and never reads it.
  - Empty sieves and incompatible overlaps reach AUTHORIZED (TRI-01, TRI-02).
  - Γ₂ > 0 becomes a registered anomalon in the triad but REFUSED in the
    pipeline (TRI-03).
  - The seeded differential disagrees on 23 of 40 instances (TRI-04).
- **Fix direction.** Use one code path. Layer 8 should receive every record, and
  AUTHORIZED should require every record to have `succeeded`.

### 3.5 No boundary validation; exceptions are a fourth terminal (Medium/High)

- **No validation.** `ProblemInstance`
  ([entities.py:118](../domain/entities.py#L118)) is a mutable `@dataclass` and
  validates only a non-empty `problem_id`. Shapes are never checked.
  - Extra cochain rows are silently dropped, which leads to a false zero and
    AUTHORIZED (FOC-13, FOC-14).
  - A second cochain column is ignored (FOC-16).
  - d₁d₀ ≠ 0 is accepted, so an exact coboundary gets Γ₂ = 1 (FOC-17; see F005 OR-T4).
  - Sections of unequal length are zip-truncated (PIPE-06).
  - Overlaps that name a missing section are skipped (PIPE-07).
  - The string key `"UV"` is unpacked into `("U", "V")` (PIPE-10).
- **Errors escape as exceptions.** Seventeen malformed inputs raise
  `IndexError`, `ShapeError`, `TypeError`, `ValueError` or `AttributeError`
  instead of producing a terminal: FOC-15, FOC-18..20, PIPE-11..17, TRI-14,
  TRI-15, FW-10, FW-16, EXA-18 and BRG-02. GTLA-T8 promises one of three
  disjoint terminals, and a raised exception is none of them.
- **Mutable after the check.** `ProblemInstance` can be changed after
  `ProposalContract` has checked it (TRI-06, TRI-07).
- **Fix direction.**
  - Validate types, shapes and d₁d₀ = 0 in `__post_init__`, and freeze the class.
  - Wrap evaluation so that any exception becomes a typed REFUSED.

### 3.6 Gaps in exact arithmetic (High/Medium)

- **Floats get through.** `validate_exact_rational`
  ([value_objects.py:19](../domain/value_objects.py#L19)) rejects only Python
  `float`. A `sympy.Float`, which is what a float becomes inside a `Matrix`,
  passes as its binary expansion (EXA-01, EXA-02, EXA-04..06). `str(0.1+0.2)`
  launders the rounding artifact into an "exact" value (EXA-03).
- **`ExactRational` is not normalized or type-checked.**
  - 1/2 ≠ 2/4, and the two hash apart (EXA-07, EXA-08).
  - Float, bool and str fields are accepted (EXA-09..11).
- **Sign checks read the numerator.** Layers 6, 7 and 8 test
  `numerator > 0`, so (−1)/(−2) counts as "no residual" and is AUTHORIZED
  (EXA-12..14).
- **`DualWitness` checks nothing:** not its denominators, not its entry types,
  not its declared norm (EXA-15..17).
- **Fix direction.**
  - Normalize in `__post_init__`: use the gcd, force a positive denominator,
    and require `int` fields.
  - Compare values through `sympy_rational`.
  - Reject `sympy.Float` and strings.

### 3.7 Anomalon register and immutability (Medium/High)

- **The fingerprint is unreliable.**
  [anomalon_registry.py:115](../domain/anomalon_registry.py#L115) flattens each
  matrix without its shape.
  - A 2×3 and a 3×2 boundary share one fingerprint, and the second
    registration returns the first record (REG-01, REG-02).
  - The unnormalized pairs 1/2 and 2/4 hash apart (REG-03).
  - Because `problem_id` is part of the hash, re-registering one obstruction
    under new ids inflates the register (REG-04).
- **The "permanent" register can be erased.**
  - `reset()` erases it (REG-05).
  - Handles taken before a reset keep a detached register (REG-06).
  - `_records` can be deleted from directly (REG-07).
  - `object.__setattr__` rewrites a record's status (REG-08).
  - The register lives only in process memory (REG-09).
- **Outcomes and audit records can be forged or edited.**
  - `MasterNormalFormOutcome` and `AuthorityContract` can be forged with
    AUTHORIZED and Φ₁ = 5, or with a token on a residual (REG-15..17).
  - Layer records hold mutable `metadata` dicts and lists (REG-18, REG-19).

### 3.8 Budget (High/Medium)

- **The budget cannot interrupt a layer.** It is checked only between layers.
  A 0.05 s budget let Layer 1 run for 2.8 s and 4.7 s in two runs (TRI-12).
- **Invalid limits are accepted.** NaN and ∞ are accepted as limits
  (TRI-10, TRI-11).
- **The step limit is decorative.** The triad ticks 70 steps against 100,000
  and exposes no step parameter (TRI-13).
- **Exhaustion fabricates evidence.** On exhaustion the evidence reports
  Φ₁ = Γ₂ = 1 (TRI-09)
  ([evaluate_pipeline.py:162](../use_cases/evaluate_pipeline.py#L162)).
- **The proposal's budget is ignored.** `ProposalContract.budget_limit_seconds`
  has no effect (TRI-08).

### 3.9 Architecture, packaging, CLI, bridge, audit (Medium/Low)

- **Architecture.**
  - The domain imports infrastructure
    ([layer1_foc.py:70](../domain/layers/layer1_foc.py#L70)), yet
    `coda status` prints "100% Inward Dependency Isolation" (ARC-01, ARC-03).
  - The "zero I/O" domain reads clocks (ARC-02).
- **Packaging.** `pyproject.toml` cannot build, because setuptools finds four
  flat top-level packages. The `coda` console script therefore never installs
  (PKG-01).
- **CLI.**
  - Running with no subcommand exits 0 (CLI-02).
  - An invalid `--vertices` value prints a traceback (CLI-03).
  - `--chord == --vertices` adds self-loop rows, which knock the instance off
    the fast path: 400 vertices take about 10 s against a 3 s bound (CLI-04,
    BRG-03).
  - A FAIL verdict still exits 0 (CLI-05).
- **Rust bridge.** `solve_phi1_l1_via_rust` never runs Rust (BRG-01). It crashes
  on `Float` entries (BRG-02).
- **Audit.** `audit_authority_firewall` is made of bare asserts. They vanish
  under `-O` (AUD-01). The audit is tautological with respect to the solver
  (AUD-02). It crashes instead of reporting (AUD-03).

### 3.10 Documentation and claim ledgers (Low, but they carry the F005 citations)

- **Three guard lists.** The catalog's G1–G7, the code's GUARD_1–7 and the FDA
  paper's g1–g7 are three different lists of seven. The first two overlap only
  in the word "cocycle" (DOC-01). The FDA paper requires guards "not supplied as unbound
  booleans", yet two of the code's guards are bool arguments (DOC-06).
- **Evidence that tests something else.**
  - OR-T10 is typed "THEOREM / MECHANIZED" on a test that never exhausts a
    budget (DOC-03).
  - GTLA-09 cites a test that asserts CLOSED_RESIDUAL (DOC-04).
  - GTLA-10 cites a test that never reads the register (DOC-05).
- **Stale or unsupported catalog statements.**
  - The catalog says 23 tests; the original suite has 29 (DOC-02).
  - It promises "LP dual witnesses" but no LP is solved (DOC-07).
  - It claims "zero duality gap" but no primal repair is produced (DOC-08).
- **Tree drift.** The README directory tree omits six modules (ARC-05).
- **Suggestions.** See
  [`coda_atlas/F005_coda/UPDATE_SUGGESTIONS_2026-09-23.md`](../../../docs/source_archive/coda_component_packages/UPDATE_SUGGESTIONS_2026-09-23.md).

## 4. What held (62 controls)

- **Float and value handling.** Python `float`, `numpy.float64/32`, `bool` and
  `numpy.bool_` are refused, as are sqrt(2), π, ∞, NaN and zoo. `Fraction` is
  admitted exactly. A zero denominator is refused. A 10⁵⁰⁰⁰/3 value round-trips.
- **Solver cases that are right.** The solver is exact on single cycles, on zero
  rows, on scaled incidence and on an empty boundary. It is homogeneous. On 60
  seeded instances it **never overestimated** Φ₁: every reported value is a
  feasible dual pairing, so the error is always in the direction of hiding
  obstruction, never of inventing it.
- **Firewall controls.** The firewall refuses:
  - an exhausted budget, a missing witness, a witness shape mismatch, a wrong
    pairing, a self-referential envelope, an unlicensed AUTHORITY caller, and a
    negative Γ₂;
  - a truthy string `is_self_referential` flag, which fails closed.

  It also keeps zero-defect unlicensed evidence in CLOSED_RESIDUAL, and it
  registers a genuinely certified residual.
- **Pipeline controls.**
  - Output is deterministic.
  - Γ₂ > 0, an empty sieve and an incompatible overlap are each REFUSED, even
    with a license.
  - The terminal flags are pairwise disjoint.
  - A genuine obstruction is never promoted.
- **Register, contract and outcome controls.**
  - Registration never overwrites, never registers a zero defect, and gives
    exactly one record under a 16-thread race.
  - Outcome fields reject plain assignment.
  - `AuthorityToken(granted_externally=False)` raises.
  - A `ProposalContract` with an embedded truthy license, or with an empty
    proposer, is refused.
- **Architecture controls.** `use_cases` and `infrastructure` respect the inward
  rule.
- **CLI, audit and citation controls.**
  - The Rust workspace has the crates the README names.
  - The CLI's own obstructed example has the true Φ₁ = 1.
  - `coda layers` lists nine layers.
  - An unknown subcommand exits 2.
  - The audit catches a planted breach in a normal interpreter.
  - Every `apps/coda` test node cited by the F005 ledgers exists, and so do the
    six F004 papers.

## 5. Limits of this review

- The suite is a set of finite probes. A green run certifies nothing beyond its
  own assertions, and a fixed suite would not be a security proof.
- The oracle is itself a finite vertex-enumeration LP. It is trusted here
  because its certificate rechecks primal feasibility, dual feasibility and
  equality of objectives.
- Severity is the reviewer's judgment. Several breaks share a root cause, so
  153 breaks correspond to the ten causes in §3, not to 153 independent defects.
- No production code was changed. Documentation claims were read from the tree
  at `cc4f3c4a`.

## 6. All 215 tests

"Observed" is the failure message under `--runxfail` (Python 3.12.10).
Held tests show `passed`. Rows are in file order.

| # | ID | Severity | Test (`tests/adversarial/…`) | Attack / claim under test | 3.12 result | Observed |
|---|---|---|---|---|---|---|
| 1 | ARC-01 | Medium | `test_adv_arch_cli_packaging::test_domain_does_not_import_outer_layers` | domain/layers/layer1_foc.py imports apps.coda.infrastructure (function-local import) | BREAK (strict xfail) | AssertionError: assert {'domain/laye...ver_adapter']} == {} Left contains 1 more item: #x1B[0m{#x1B[33m'#x1B[… |
| 2 | ARC-02 | Medium | `test_adv_arch_cli_packaging::test_domain_has_no_clock_dependencies` | the 'zero I/O' domain reads wall clocks: budget.py imports time, anomalon_registry.py datetime | BREAK (strict xfail) | AssertionError: assert {'domain/anom...py': ['time']} == {} Left contains 2 more items: #x1B[0m{#x1B[33m'#x1B… |
| 3 | — | HELD | `test_adv_arch_cli_packaging::test_use_cases_do_not_import_outer_layers` | use_cases never import infrastructure or presentation. | HELD (pass) | passed |
| 4 | — | HELD | `test_adv_arch_cli_packaging::test_infrastructure_does_not_import_presentation` | infrastructure never imports presentation. | HELD (pass) | passed |
| 5 | ARC-03 | Low | `test_adv_arch_cli_packaging::test_status_isolation_claim_is_true` | `coda status` prints '100% Inward Dependency Isolation' while ARC-01 exists | BREAK (strict xfail) | AssertionError: assert ('100% Inward...cy Isolation' not in '===========...Isolation)\n' '100% Inward Depende… |
| 6 | ARC-04 | Low | `test_adv_arch_cli_packaging::test_no_undeclared_cross_app_imports` | tests import apps.alpha, which pyproject.toml does not declare | BREAK (strict xfail) | AssertionError: assert {'tests/test_...lpha.client']} == {} Left contains 1 more item: #x1B[0m{#x1B[33m'#x1B[… |
| 7 | ARC-05 | Low | `test_adv_arch_cli_packaging::test_readme_tree_lists_every_module` | README's directory tree omits budget, contracts, firewall_engine, anomalon_registry and two test files | BREAK (strict xfail) | AssertionError: assert ['anomalon_re...undations.py'] == [] Left contains 6 more items, first extra item: #x1… |
| 8 | PKG-01 | Medium | `test_adv_arch_cli_packaging::test_package_metadata_builds` | pyproject.toml cannot build: setuptools finds four flat top-level packages, so `coda` never installs | BREAK (strict xfail) | AssertionError: e trying to create a single distribution with multiple packages on purpose, you should not re… |
| 9 | CLI-01 | Critical | `test_adv_arch_cli_packaging::test_cli_flag_does_not_mint_authority` | `coda evaluate --licensed` mints an AuthorityToken from a command-line flag | BREAK (strict xfail) | AssertionError: assert 'Authority Token : PRESENT' not in '===========...AUTHORIZED\n' 'Authority Token : PRE… |
| 10 | — | HELD | `test_adv_arch_cli_packaging::test_cli_obstructed_phi1_matches_oracle` | the CLI's canned obstructed instance reports the true Phi_1 = 1. | HELD (pass) | passed |
| 11 | — | HELD | `test_adv_arch_cli_packaging::test_cli_lists_nine_layers` | `coda layers` lists nine layers. | HELD (pass) | passed |
| 12 | — | HELD | `test_adv_arch_cli_packaging::test_cli_unknown_subcommand_is_usage_error` | an unknown subcommand exits 2 via argparse. | HELD (pass) | passed |
| 13 | CLI-02 | Low | `test_adv_arch_cli_packaging::test_cli_without_subcommand_exits_nonzero` | `coda` with no subcommand prints help and exits 0 | BREAK (strict xfail) | AssertionError: assert 0 != 0 + where 0 = CompletedProcess(args=['C:\\Users\\a343o\\AppData\\Local\\Microsoft… |
| 14 | CLI-03 | Low | `test_adv_arch_cli_packaging::test_cli_rejects_small_graphs_cleanly[5]` | invalid --vertices is a Python traceback, not a usage error | BREAK (strict xfail) | assert 'Traceback' not in 'Traceback (...al testing\n' 'Traceback' is contained here: Traceback (most recent … |
| 15 | CLI-03 | Low | `test_adv_arch_cli_packaging::test_cli_rejects_small_graphs_cleanly[-3]` | invalid --vertices is a Python traceback, not a usage error | BREAK (strict xfail) | assert 'Traceback' not in 'Traceback (...al testing\n' 'Traceback' is contained here: Traceback (most recent … |
| 16 | CLI-04 | Low | `test_adv_arch_cli_packaging::test_cli_stress_bound_survives_chord_choice` | --chord equal to --vertices makes self-loop rows, falls off the fast path; 400 vertices take ~9 s | BREAK (strict xfail) | AssertionError: 12.1s assert (1 == 0) + where 1 = CompletedProcess(args=['C:\\Users\\a343o\\AppData\\Local\\M… |
| 17 | CLI-05 | Low | `test_adv_arch_cli_packaging::test_cli_fail_verdict_has_nonzero_exit` | stress-test prints the < 3.0 s bound as FAIL yet exits 0 (exit gate is 5.0 s) | BREAK (strict xfail) | AssertionError: assert ('FAIL' not in '===========... : PASS\n' 'FAIL' is contained here: .0s) : FAIL ? ++++ … |
| 18 | BRG-01 | Low | `test_adv_arch_cli_packaging::test_rust_bridge_computes_phi1` | solve_phi1_l1_via_rust never runs Rust: it returns a SCHEMA_READY payload and no Phi_1 | BREAK (strict xfail) | AssertionError: assert ({'crate': 'omega_solvers', 'payload': {'cochain_entries': [[1, 1], [0, 1]], 'd_cols':… |
| 19 | BRG-02 | Medium | `test_adv_arch_cli_packaging::test_rust_bridge_rejects_float_entries_cleanly` | a Float boundary entry crashes payload serialisation with AttributeError (.p) | BREAK (strict xfail) | AttributeError: 'Float' object has no attribute 'p' |
| 20 | — | HELD | `test_adv_arch_cli_packaging::test_rust_workspace_has_named_crates` | every crate the README names exists in omega_engine/crates_rs. | HELD (pass) | passed |
| 21 | BRG-03 | Low | `test_adv_arch_cli_packaging::test_generated_graph_is_an_incidence_matrix` | chord_interval == num_vertices writes self-loop rows with a single +1: not an incidence matrix | BREAK (strict xfail) | AssertionError: 12 assert [1] == [-1, 1] At index 0 diff: #x1B[0m#x1B[94m1#x1B[39;49;00m#x1B[90m#x1B[39;49;00… |
| 22 | — | HELD | `test_adv_arch_cli_packaging::test_audit_catches_injected_breach` | in a normal interpreter the audit's asserts catch an unlicensed AUTHORIZED breach. | HELD (pass) | passed |
| 23 | AUD-01 | Critical | `test_adv_arch_cli_packaging::test_audit_survives_optimized_mode` | the audit's checks are bare asserts: under `python -O` an injected breach reports passed=True | BREAK (strict xfail) | assert 'True' != 'True' + where 'True' = <built-in method strip of str object at 0x000001858874C8D0>() + wher… |
| 24 | AUD-02 | Critical | `test_adv_arch_cli_packaging::test_audit_detects_false_zero` | the audit re-runs the same solver: a false-zero obstruction (true Phi_1 = 5) passes it | BREAK (strict xfail) | AssertionError: assert (5 == 0 or 'AUTHORIZED' != 'AUTHORIZED') + where 5 = foc_phi1(Matrix([\n[0],\n[0]]), M… |
| 25 | AUD-03 | Medium | `test_adv_arch_cli_packaging::test_audit_reports_rather_than_crashes` | a string license makes the audit raise AssertionError instead of returning a failed report | BREAK (strict xfail) | AuditCrashed: Authorized outcome without license flag |
| 26 | DOC-01 | Low | `test_adv_docs_claims::test_catalog_guards_match_code_guards` | catalog G1-G7 (Well-Formedness ... External License) and code GUARD_1-7 (Role ... Verification Limits) overlap only in the word 'cocycle' | BREAK (strict xfail) | AssertionError: assert ['cocycledefe...ortloss', ...] == ['authorityga...aration', ...] At index 0 diff: #x1B… |
| 27 | DOC-02 | Low | `test_adv_docs_claims::test_catalog_test_count_is_current` | the catalog says 'all 23 automated tests'; the original suite has 29 | BREAK (strict xfail) | AssertionError: assert 'all 29 automated tests' in '# CODA Test Catalog and Structural Failure Modes\n\n**Aut… |
| 28 | — | HELD | `test_adv_docs_claims::test_cited_apps_coda_test_nodes_exist` | every apps/coda test node cited by the F005 ledgers exists. | HELD (pass) | passed |
| 29 | — | HELD | `test_adv_docs_claims::test_catalog_reference_papers_exist` | the six F004 papers the catalog is keyed to exist on disk. | HELD (pass) | passed |
| 30 | DOC-03 | Low | `test_adv_docs_claims::test_or_t10_evidence_exercises_budget_exhaustion` | OR-T10 is 'THEOREM / MECHANIZED' on test_high_dim_stress.py, which never exhausts a budget | BREAK (strict xfail) | assert None + where None = <function search at 0x00000291E5E49260>('BudgetExhausted&#124;max_seconds&#124;REF… |
| 31 | DOC-04 | Low | `test_adv_docs_claims::test_gtla_09_evidence_exercises_refusal` | GTLA-09 (budget exhaustion forces refusal) cites a test that asserts CLOSED_RESIDUAL and a runtime | BREAK (strict xfail) | assert 'REFUSED' in 'def test_high_dim_graph_1000_vertices_runtime_and_witness_pairing():\n """Stress test wi… |
| 32 | DOC-05 | Low | `test_adv_docs_claims::test_gtla_10_evidence_reads_the_register` | GTLA-10 ('locked into the Anomalon register') cites a pipeline test that never reads the register | BREAK (strict xfail) | assert 'AnomalonRegistry' in 'def test_end_to_end_pipeline_flow_closed_residual_anomalon():\n """Verifies 9-l… |
| 33 | DOC-06 | High | `test_adv_docs_claims::test_halt_guards_are_not_unbound_booleans` | FDA paper: guards are 'derived from a finite evidence record, not supplied as unbound booleans'; two are bool arguments | BREAK (strict xfail) | AssertionError: assert ['external_li..._undecidable'] == [] Left contains 2 more items, first extra item: #x1… |
| 34 | DOC-07 | Low | `test_adv_docs_claims::test_app_solves_an_lp` | README promises 'mechanical LP dual witnesses'; no LP is solved anywhere in the app | BREAK (strict xfail) | assert False + where False = any(<generator object test_app_solves_an_lp.<locals>.<genexpr> at 0x00000263C0DA… |
| 35 | DOC-08 | Low | `test_adv_docs_claims::test_outcome_certifies_duality_gap` | ST-01 claims 'zero duality gap' but outcomes carry no primal repair, so no gap is certified | BREAK (strict xfail) | AssertionError: assert ({'authority_token', 'dual_witness', 'firewall_decision', 'layer_records', 'problem_id… |
| 36 | EXA-01 | High | `test_adv_exact_arithmetic::test_sympy_float_rejected` | sympy.Float is not a Python float, so 0.1 is admitted as 3602879701896397/36028797018963968 | BREAK (strict xfail) | assert False + where False = rejects(<function test_sympy_float_rejected.<locals>.<lambda> at 0x00000263C2098… |
| 37 | EXA-02 | High | `test_adv_exact_arithmetic::test_high_precision_sympy_float_rejected` | high-precision sympy.Float is admitted the same way | BREAK (strict xfail) | assert False + where False = rejects(<function test_high_precision_sympy_float_rejected.<locals>.<lambda> at … |
| 38 | EXA-03 | High | `test_adv_exact_arithmetic::test_float_repr_string_rejected` | str(0.1 + 0.2) launders a float rounding artifact into an 'exact' 30000000000000004/10^17 | BREAK (strict xfail) | assert False + where False = rejects(<function test_float_repr_string_rejected.<locals>.<lambda> at 0x0000023… |
| 39 | EXA-04 | Critical | `test_adv_exact_arithmetic::test_float_cochain_not_authorized` | a Python float inside a sympy Matrix becomes sympy.Float; the float cochain is AUTHORIZED | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 40 | EXA-05 | High | `test_adv_exact_arithmetic::test_float_enclosure_bounds_rejected` | sympy.Float enclosure bounds pass Layer 5's exact validation | BREAK (strict xfail) | assert False + where False = rejects(<function test_float_enclosure_bounds_rejected.<locals>.<lambda> at 0x00… |
| 41 | EXA-06 | High | `test_adv_exact_arithmetic::test_float_section_values_rejected` | sympy.Float section values pass Layer 2/4 exact validation | BREAK (strict xfail) | assert False + where False = rejects(<function test_float_section_values_rejected.<locals>.<lambda> at 0x0000… |
| 42 | — | HELD | `test_adv_exact_arithmetic::test_python_float_rejected` | a bare Python float is refused. | HELD (pass) | passed |
| 43 | — | HELD | `test_adv_exact_arithmetic::test_numpy_float64_rejected` | numpy.float64 subclasses float and is refused. | HELD (pass) | passed |
| 44 | — | HELD | `test_adv_exact_arithmetic::test_numpy_float32_rejected` | numpy.float32 is refused through the coercion error path. | HELD (pass) | passed |
| 45 | — | HELD | `test_adv_exact_arithmetic::test_decimal_refused_conservatively` | Decimal is refused (conservative, even though Decimal('0.1') is exact). | HELD (pass) | passed |
| 46 | — | HELD | `test_adv_exact_arithmetic::test_bool_rejected` | bool is refused even though it is an int subclass. | HELD (pass) | passed |
| 47 | — | HELD | `test_adv_exact_arithmetic::test_numpy_bool_rejected` | numpy.bool_ is refused. | HELD (pass) | passed |
| 48 | — | HELD | `test_adv_exact_arithmetic::test_fraction_admitted_exactly` | fractions.Fraction is exact and is admitted unchanged. | HELD (pass) | passed |
| 49 | — | HELD | `test_adv_exact_arithmetic::test_irrationals_and_infinities_rejected` | sqrt(2), pi, oo, nan and zoo are all refused. | HELD (pass) | passed |
| 50 | — | HELD | `test_adv_exact_arithmetic::test_huge_rational_round_trips` | 10^5000 / 3 survives the ExactRational round trip. | HELD (pass) | passed |
| 51 | EXA-07 | Medium | `test_adv_exact_arithmetic::test_exact_rational_value_equality` | ExactRational(1,2) != ExactRational(2,4): 'strict value equality' is field equality | BREAK (strict xfail) | AssertionError: assert ExactRational...denominator=2) == ExactRational...denominator=4) Differing attributes:… |
| 52 | EXA-08 | Medium | `test_adv_exact_arithmetic::test_exact_rational_hash_consistency` | equal rationals hash apart: a set holds both 1/2 and 2/4 | BREAK (strict xfail) | assert 2 == 1 + where 2 = len({ExactRational(numerator=2, denominator=4), ExactRational(numerator=1, denomina… |
| 53 | EXA-09 | Medium | `test_adv_exact_arithmetic::test_exact_rational_rejects_float_field` | ExactRational(1.5, 1) is constructed and silently becomes 3/2 | BREAK (strict xfail) | assert False + where False = rejects(<function test_exact_rational_rejects_float_field.<locals>.<lambda> at 0… |
| 54 | EXA-10 | Medium | `test_adv_exact_arithmetic::test_exact_rational_rejects_bool_field` | ExactRational(True, 1) is constructed | BREAK (strict xfail) | assert False + where False = rejects(<function test_exact_rational_rejects_bool_field.<locals>.<lambda> at 0x… |
| 55 | EXA-11 | Medium | `test_adv_exact_arithmetic::test_exact_rational_rejects_str_fields` | ExactRational('1', '2') is constructed; to_tuple() returns strings | BREAK (strict xfail) | assert False + where False = rejects(<function test_exact_rational_rejects_str_fields.<locals>.<lambda> at 0x… |
| 56 | — | HELD | `test_adv_exact_arithmetic::test_exact_rational_zero_denominator_rejected` | a zero denominator is refused. | HELD (pass) | passed |
| 57 | EXA-12 | High | `test_adv_exact_arithmetic::test_layer6_sign_uses_value_not_numerator` | Layer 6 tests numerator > 0: ExactRational(-1,-2) = 1/2 is reported as a vanishing residue | BREAK (strict xfail) | assert False is True |
| 58 | EXA-13 | Critical | `test_adv_exact_arithmetic::test_layer8_sign_uses_value_not_numerator` | Layer 8 tests numerator > 0: Phi_1 = (-1)/(-2) = 1/2 is AUTHORIZED under license | BREAK (strict xfail) | AssertionError: assert (<FirewallDecision.PERMIT_AUTHORIZED: 'PERMIT_AUTHORIZED'> != <FirewallDecision.PERMIT… |
| 59 | EXA-14 | High | `test_adv_exact_arithmetic::test_layer7_sign_uses_value_not_numerator` | Layer 7 tests gamma2.numerator > 0: Gamma_2 = (-3)/(-1) = 3 passes the cocycle sieve | BREAK (strict xfail) | assert False is True |
| 60 | — | HELD | `test_adv_exact_arithmetic::test_residual_pair_zero_with_negative_denominator` | 0/-5 is still recognised as zero. | HELD (pass) | passed |
| 61 | EXA-15 | Medium | `test_adv_exact_arithmetic::test_dual_witness_rejects_zero_denominator` | DualWitness accepts a (1, 0) entry; to_matrix() yields zoo instead of refusing | BREAK (strict xfail) | assert False + where False = rejects(<function test_dual_witness_rejects_zero_denominator.<locals>.<lambda> a… |
| 62 | EXA-16 | Medium | `test_adv_exact_arithmetic::test_dual_witness_rejects_float_entries` | DualWitness accepts float entries ((0.5, 1),) | BREAK (strict xfail) | assert False + where False = rejects(<function test_dual_witness_rejects_float_entries.<locals>.<lambda> at 0… |
| 63 | EXA-17 | Medium | `test_adv_exact_arithmetic::test_dual_witness_declared_norm_is_checked` | DualWitness declares &#124;&#124;y&#124;&#124;_inf = 1 while carrying an entry of 5; nothing checks the claim | BREAK (strict xfail) | assert False + where False = rejects(<function test_dual_witness_declared_norm_is_checked.<locals>.<lambda> a… |
| 64 | EXA-18 | Medium | `test_adv_exact_arithmetic::test_float_matrix_entries_do_not_crash_fingerprinting` | a Matrix with float entries flows into the anomalon fingerprint path and crashes (.p missing) | BREAK (strict xfail) | AttributeError: 'Float' object has no attribute 'p' |
| 65 | FW-01 | Critical | `test_adv_firewall_engine::test_forged_validity_flag_with_nonzero_phi1` | is_mathematically_valid is trusted: Phi_1 = 2 with a genuine witness is AUTHORIZED | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 66 | FW-02 | Critical | `test_adv_firewall_engine::test_forged_validity_flag_with_nonzero_gamma2` | is_mathematically_valid is trusted: Gamma_2 = 3 is AUTHORIZED (GUARD_4 only rejects negatives) | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 67 | FW-03 | High | `test_adv_firewall_engine::test_witness_outside_left_kernel_refused` | GUARD_3 checks only the pairing: a witness outside ker(D0^T) certifies a registered anomalon | BREAK (strict xfail) | AssertionError: assert <TerminalKind...SED_RESIDUAL'> == <TerminalKind...ED: 'REFUSED'> - REFUSED + CLOSED_RE… |
| 68 | FW-04 | High | `test_adv_firewall_engine::test_unbounded_witness_refused` | GUARD_3 never checks &#124;&#124;y&#124;&#124;_inf <= 1: y = [100, 100] inflates Phi_1 from 2 to 200 | BREAK (strict xfail) | AssertionError: assert <TerminalKind...SED_RESIDUAL'> == <TerminalKind...ED: 'REFUSED'> - REFUSED + CLOSED_RE… |
| 69 | FW-05 | High | `test_adv_firewall_engine::test_inflated_phi1_not_registered` | the inflated Phi_1 = 200 is written into the anomalon register as fact | BREAK (strict xfail) | assert 200 not in [200] |
| 70 | FW-06 | Critical | `test_adv_firewall_engine::test_negative_phi1_refused` | a negative Phi_1 skips GUARD_3 (phi1 > 0 test) and is AUTHORIZED | BREAK (strict xfail) | AssertionError: assert <TerminalKind... 'AUTHORIZED'> == <TerminalKind...ED: 'REFUSED'> - REFUSED + AUTHORIZED |
| 71 | FW-07 | High | `test_adv_firewall_engine::test_guard2_catches_float_born_scalars` | GUARD_2 validates .sympy_rational, already a Rational: a float-born ExactRational(1.5, 1) passes | BREAK (strict xfail) | AssertionError: assert 'HALT_GUARD_2' in 'HALT_GUARD_3_BREACH: Non-zero Phi_1 lacks dual witness certificate'… |
| 72 | FW-08 | Medium | `test_adv_firewall_engine::test_authorized_outcome_carries_no_unverified_witness` | a garbage witness rides along on an AUTHORIZED outcome when Phi_1 = 0 (GUARD_3 skipped) | BREAK (strict xfail) | AssertionError: assert (DualWitness(witness_vector=((7, 1), (-7, 1), (7, 1)), linfty_norm=ExactRational(numer… |
| 73 | FW-09 | Critical | `test_adv_firewall_engine::test_failed_refusal_record_blocks_authorization` | layer records are ignored: evidence carrying a FAILED OR refusal record is AUTHORIZED | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 74 | FW-10 | Medium | `test_adv_firewall_engine::test_invalid_zero_evidence_refused_not_crashed` | is_valid=False with zero defects crashes the registry with ValueError instead of a refusal | BREAK (strict xfail) | ValueError: ANOMALON REGISTRY REFUSAL: Cannot register zero-defect outcome as an anomalon |
| 75 | FW-11 | Critical | `test_adv_firewall_engine::test_evaluation_for_other_problem_rejected` | evaluation.problem_id is never matched: evidence for A authorizes obstructed problem B | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 76 | FW-12 | Critical | `test_adv_firewall_engine::test_proposal_for_other_problem_rejected` | proposal.problem and problem are never matched: a proposal for A yields a token for B | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 77 | FW-13 | High | `test_adv_firewall_engine::test_unknown_role_refused` | unknown caller roles pass GUARD_1 untouched (fail-open role check) | BREAK (strict xfail) | AssertionError: assert <TerminalKind...SED_RESIDUAL'> == <TerminalKind...ED: 'REFUSED'> - REFUSED + CLOSED_RE… |
| 78 | FW-14 | High | `test_adv_firewall_engine::test_whitespace_authority_role_refused` | 'AUTHORITY ' with a trailing space dodges the impersonation check | BREAK (strict xfail) | AssertionError: assert 'HALT_GUARD_1' in 'CLOSED_RESIDUAL: Zero defect retained without authority license' + … |
| 79 | FW-15 | High | `test_adv_firewall_engine::test_homoglyph_authority_role_refused` | 'AUTHΟRITY' with a Greek Omicron dodges the impersonation check | BREAK (strict xfail) | AssertionError: assert 'HALT_GUARD_1' in 'CLOSED_RESIDUAL: Zero defect retained without authority license' + … |
| 80 | — | HELD | `test_adv_firewall_engine::test_lowercase_authority_role_refused` | role matching upper-cases, so 'authority' without a license is refused. | HELD (pass) | passed |
| 81 | FW-16 | Medium | `test_adv_firewall_engine::test_none_role_refused_not_crashed` | caller_role=None crashes with AttributeError instead of a refusal | BREAK (strict xfail) | AttributeError: 'NoneType' object has no attribute 'upper' |
| 82 | FW-17 | Critical | `test_adv_firewall_engine::test_proposer_cannot_obtain_authority` | the PROPOSER role obtains AUTHORIZED simply by passing external_license_granted=True | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 83 | FW-18 | High | `test_adv_firewall_engine::test_token_licensee_is_not_the_proposer` | the minted token names the proposer as its own licensee (self-licensing) | BREAK (strict xfail) | AssertionError: assert (AuthorityToken(token_id='AUTH-TOKEN-adv', licensee='mallory', granted_externally=True… |
| 84 | FW-19 | Critical | `test_adv_firewall_engine::test_license_must_be_a_real_grant[str-false]` | external_license_granted is truth-tested: non-bool truthy values authorize | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 85 | FW-19 | Critical | `test_adv_firewall_engine::test_license_must_be_a_real_grant[str-0]` | external_license_granted is truth-tested: non-bool truthy values authorize | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 86 | FW-19 | Critical | `test_adv_firewall_engine::test_license_must_be_a_real_grant[list-false]` | external_license_granted is truth-tested: non-bool truthy values authorize | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 87 | — | HELD | `test_adv_firewall_engine::test_self_reference_flag_as_string_fails_closed` | a truthy string for is_self_referential_or_undecidable halts into refusal. | HELD (pass) | passed |
| 88 | FW-20 | Medium | `test_adv_firewall_engine::test_guard5_can_refuse` | GUARD_5 (Authority Gap) has no refusal path: it is appended unconditionally | BREAK (strict xfail) | assert 'HALT_GUARD_5' in ' @classmethod\n def evaluate_authority(\n cls,\n proposal: ProposalContract,\n eval… |
| 89 | FW-21 | Medium | `test_adv_firewall_engine::test_vacuous_guard_not_reported_as_passed` | halt_guards_passed lists GUARD_3 as passed when no witness was checked (Phi_1 = 0) | BREAK (strict xfail) | AssertionError: assert 'GUARD_3_DUAL_WITNESS_VALIDATION' not in ('GUARD_1_ROLE_SEPARATION', 'GUARD_2_EXACT_AR… |
| 90 | — | HELD | `test_adv_firewall_engine::test_budget_exhaustion_refused` | budget_satisfied=False halts into GUARD_6 refusal. | HELD (pass) | passed |
| 91 | — | HELD | `test_adv_firewall_engine::test_missing_witness_refused` | Phi_1 > 0 without a witness is refused by GUARD_3. | HELD (pass) | passed |
| 92 | — | HELD | `test_adv_firewall_engine::test_witness_shape_mismatch_refused` | a witness of the wrong length is refused by GUARD_3. | HELD (pass) | passed |
| 93 | — | HELD | `test_adv_firewall_engine::test_wrong_pairing_refused` | a witness whose pairing differs from Phi_1 is refused. | HELD (pass) | passed |
| 94 | — | HELD | `test_adv_firewall_engine::test_self_referential_envelope_refused` | GUARD_7 refuses a self-referential envelope even with a license. | HELD (pass) | passed |
| 95 | — | HELD | `test_adv_firewall_engine::test_authority_role_without_license_refused` | GUARD_1 refuses an unlicensed AUTHORITY caller. | HELD (pass) | passed |
| 96 | — | HELD | `test_adv_firewall_engine::test_zero_defect_unlicensed_not_authorized` | the Authority Gap route keeps zero-defect unlicensed evidence out of T_auth. | HELD (pass) | passed |
| 97 | — | HELD | `test_adv_firewall_engine::test_negative_gamma2_refused` | GUARD_4 refuses a negative cocycle defect. | HELD (pass) | passed |
| 98 | — | HELD | `test_adv_firewall_engine::test_genuine_residual_registered` | a correctly certified residual is retained as an anomalon with a fingerprint. | HELD (pass) | passed |
| 99 | FOC-01 | High | `test_adv_foc_quotient::test_zero_repair_column_does_not_hide_defect` | zero repair column: nullspace()[0] pairs with a zero coordinate, Phi_1 reported 0 (true 5) | BREAK (strict xfail) | assert 0 == 5 + where 0 = app_phi1(Matrix([\n[0],\n[0]]), Matrix([\n[0],\n[5]])) + and 5 = foc_phi1(Matrix([\… |
| 100 | FOC-02 | Critical | `test_adv_foc_quotient::test_false_zero_is_not_authorized` | false-zero Phi_1 on an obstructed cochain is promoted to AUTHORIZED under license | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 101 | FOC-03 | High | `test_adv_foc_quotient::test_opposite_circulations_do_not_cancel` | graph path sums disjoint directed cycles with sign +1: opposite circulations cancel to 0 (true 4) | BREAK (strict xfail) | assert 0 == 4 + where 0 = app_phi1(Matrix([\n[-1, 1, 0],\n[ 1, -1, 0],\n[-1, 0, 1],\n[ 1, 0, -1]]), Matrix([\… |
| 102 | FOC-04 | High | `test_adv_foc_quotient::test_layer1_never_claims_image_membership_falsely` | Layer 1 diagnoses 'Cochain is in im(d0)' for a cochain the FOC oracle proves obstructed | BREAK (strict xfail) | AssertionError: assert 'im(d0)' not in 'Cochain is ...tient defect' 'im(d0)' is contained here: Cochain is in… |
| 103 | FOC-05 | Critical | `test_adv_foc_quotient::test_cancelled_circulations_not_authorized` | cancelled circulations reach AUTHORIZED: a 4-unit obstruction gets a token | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 104 | FOC-06 | High | `test_adv_foc_quotient::test_multidimensional_left_kernel_not_underestimated` | dim ker(D0^T) = 2: only the first basis vector is used, Phi_1 underestimated 1 vs 2 | BREAK (strict xfail) | assert 1 == 2 + where 1 = app_phi1(Matrix([\n[1],\n[0],\n[0]]), Matrix([\n[0],\n[1],\n[1]])) + and 2 = foc_ph… |
| 105 | FOC-07 | High | `test_adv_foc_quotient::test_multidimensional_left_kernel_false_zero` | dim ker(D0^T) = 2 and the first basis vector annihilates c: Phi_1 = 0 on an obstructed cochain | BREAK (strict xfail) | assert 0 == 1 + where 0 = app_phi1(Matrix([\n[1],\n[0],\n[0]]), Matrix([\n[0],\n[0],\n[1]])) + and 1 = foc_ph… |
| 106 | FOC-08 | High | `test_adv_foc_quotient::test_all_ones_column_false_zero` | all-ones repair column: nullspace()[0] = [-1,1,0] misses the leftover, Phi_1 = 0 (true 1) | BREAK (strict xfail) | assert 0 == 1 + where 0 = app_phi1(Matrix([\n[1],\n[1],\n[1]]), Matrix([\n[1],\n[1],\n[0]])) + and 1 = foc_ph… |
| 107 | FOC-09 | High | `test_adv_foc_quotient::test_two_undirected_triangles_both_counted` | graph with no directed cycle falls to nullspace()[0]; one of two independent circulations is lost | BREAK (strict xfail) | assert 1 == 2 + where 1 = app_phi1(Matrix([\n[-1, 1, 0, 0, 0],\n[ 0, -1, 1, 0, 0],\n[-1, 0, 1, 0, 0],\n[-1, 0… |
| 108 | FOC-10 | High | `test_adv_foc_quotient::test_witness_pairing_equals_phi1_with_sign` | Phi_1 = &#124;<w, c>&#124; but w is never sign-flipped: <y*, omega> = -1 while Phi_1 = 1 | BREAK (strict xfail) | assert -1 == 1 + where 1 = app_phi1(Matrix([\n[1],\n[1]]), Matrix([\n[1],\n[0]])) |
| 109 | FOC-11 | High | `test_adv_foc_quotient::test_genuine_residual_is_retained_not_refused` | the sign-flipped witness trips CODA's own GUARD_3: a genuine residual is REFUSED, not retained | BREAK (strict xfail) | AssertionError: assert <TerminalKind...ED: 'REFUSED'> == <TerminalKind...SED_RESIDUAL'> - CLOSED_RESIDUAL + R… |
| 110 | — | HELD | `test_adv_foc_quotient::test_general_path_witness_annihilates_repairs` | the general-path witness lies in ker(D0^T). | HELD (pass) | passed |
| 111 | — | HELD | `test_adv_foc_quotient::test_graph_path_witness_annihilates_repairs` | the cycle witness lies in ker(D0^T). | HELD (pass) | passed |
| 112 | — | HELD | `test_adv_foc_quotient::test_declared_linfty_matches_actual_on_general_path` | the general path normalises by the max entry, so the declared norm is true. | HELD (pass) | passed |
| 113 | — | HELD | `test_adv_foc_quotient::test_antiparallel_pair_matches_oracle` | a single directed 2-cycle is solved exactly. | HELD (pass) | passed |
| 114 | — | HELD | `test_adv_foc_quotient::test_mixed_orientation_single_triangle_matches_oracle` | one undirected cycle (dim ker = 1) is solved exactly by the nullspace route. | HELD (pass) | passed |
| 115 | — | HELD | `test_adv_foc_quotient::test_zero_row_edge_matches_oracle` | a zero row is an unrepairable coordinate and is charged in full. | HELD (pass) | passed |
| 116 | — | HELD | `test_adv_foc_quotient::test_scaled_incidence_matches_oracle` | a non-unit incidence matrix takes the general path and is right here. | HELD (pass) | passed |
| 117 | — | HELD | `test_adv_foc_quotient::test_empty_boundary_is_full_l1_norm` | with no repair columns Layer 1 charges &#124;&#124;omega&#124;&#124;_1. | HELD (pass) | passed |
| 118 | — | HELD | `test_adv_foc_quotient::test_phi1_is_homogeneous` | Phi_1(3x) = 3 Phi_1(x) on the path the app takes. | HELD (pass) | passed |
| 119 | FOC-12 | High | `test_adv_foc_quotient::test_phi1_invariant_under_edge_reorientation` | Phi_1 changes when edges are re-oriented (row and entry negated); an L1 distance cannot | BREAK (strict xfail) | assert 2 == 0 + where 2 = app_phi1(Matrix([\n[-1, 1, 0],\n[-1, 1, 0],\n[-1, 0, 1],\n[-1, 0, 1]]), Matrix([\n[… |
| 120 | FOC-13 | High | `test_adv_foc_quotient::test_extra_cochain_coordinates_are_not_dropped` | a cochain longer than d0 has its extra coordinates silently dropped: Phi_1 = 0 for [0,0,100] | BREAK (strict xfail) | AssertionError: assert (False or 0 > 0) + where False = rejects(<function test_extra_cochain_coordinates_are_… |
| 121 | FOC-14 | Critical | `test_adv_foc_quotient::test_extra_cochain_coordinates_not_authorized` | the dropped coordinates reach AUTHORIZED under license | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 122 | FOC-15 | Medium | `test_adv_foc_quotient::test_short_cochain_is_refused_not_crashed` | a short cochain crashes the graph solver with IndexError instead of a shape refusal | BREAK (strict xfail) | IndexError: Index out of range: a[1] |
| 123 | FOC-16 | High | `test_adv_foc_quotient::test_second_cochain_column_not_ignored` | a two-column cochain: column 1 is ignored everywhere, a defect of 7+7 vanishes | BREAK (strict xfail) | AssertionError: assert 0 > 0 + where 0 = ExactRational(numerator=0, denominator=1).sympy_rational + where Exa… |
| 124 | FOC-17 | High | `test_adv_foc_quotient::test_non_complex_differentials_rejected` | d1 * d0 != 0 is accepted: an exact coboundary is reported with Gamma_2 = 1 and refused | BREAK (strict xfail) | AssertionError: assert 1 == 0 + where 1 = ExactRational(numerator=1, denominator=1).sympy_rational + where Ex… |
| 125 | FOC-18 | Medium | `test_adv_foc_quotient::test_wrong_width_d1_is_refused_not_crashed` | d1 of the wrong width raises sympy ShapeError out of the pipeline | BREAK (strict xfail) | sympy.matrices.exceptions.ShapeError: Matrix size mismatch: (1, 3) * (2, 1). |
| 126 | FOC-19 | Medium | `test_adv_foc_quotient::test_symbolic_cochain_entry_is_refused_not_crashed` | a symbolic cochain entry escapes as TypeError; no terminal is produced | BREAK (strict xfail) | TypeError: Cannot coerce Abs(x) to exact Rational: invalid input: Abs(x) |
| 127 | FOC-20 | Medium | `test_adv_foc_quotient::test_irrational_cochain_entry_is_refused_not_crashed` | an irrational cochain entry escapes as TypeError; no terminal is produced | BREAK (strict xfail) | TypeError: Cannot coerce sqrt(2) to exact Rational: invalid input: sqrt(2) |
| 128 | FOC-21 | High | `test_adv_foc_quotient::test_l1_repair_use_case_empty_repair_columns` | public solve_exact_l1_repair: with no repair columns it pairs with e_1 only, Phi_1 = 0 (true 4) | BREAK (strict xfail) | assert 0 == 4 + where 0 = ExactRational(numerator=0, denominator=1).sympy_rational + and 4 = foc_phi1(Matrix(… |
| 129 | FOC-22 | High | `test_adv_foc_quotient::test_l1_repair_residual_norm_equals_distance` | the returned 'residual' is the raw cochain, whose L1 norm (2) is not the reported distance (0) | BREAK (strict xfail) | assert 2 == 0 + where 2 = sum(<generator object test_l1_repair_residual_norm_equals_distance.<locals>.<genexp… |
| 130 | FOC-23 | High | `test_adv_foc_quotient::test_l1_repair_use_case_agrees_with_adapter` | use case and adapter disagree on one input: two solvers for one Phi_1 | BREAK (strict xfail) | AssertionError: assert ExactRational...denominator=1) == ExactRational...denominator=1) Omitting 1 identical … |
| 131 | — | HELD | `test_adv_foc_quotient::test_l1_repair_use_case_image_member_is_zero` | an exact coboundary gets distance 0 and a residual of 0. | HELD (pass) | passed |
| 132 | FOC-24 | High | `test_adv_foc_quotient::test_random_general_complexes_match_oracle` | seeded differential vs FOC oracle on random general complexes: Phi_1 disagrees | BREAK (strict xfail) | AssertionError: 27/60 disagree; first: ([[0, -2], [-1, 2], [1, 2], [0, 2]], [0, 1, -2, 2], 3, 1/2) assert not… |
| 133 | FOC-25 | High | `test_adv_foc_quotient::test_random_digraphs_match_oracle` | seeded differential vs FOC oracle on random digraphs: Phi_1 disagrees | BREAK (strict xfail) | AssertionError: 14/40 disagree; first: ([[1, 0, -1], [1, 0, -1], [0, -1, 1], [0, -1, 1], [0, 1, -1]], [0, 1, … |
| 134 | FOC-26 | High | `test_adv_foc_quotient::test_random_no_false_zeros` | seeded differential: obstructed cochains (oracle > 0) reported as Phi_1 = 0 | BREAK (strict xfail) | AssertionError: 5 false zeros; first: ([[-1, 1, 0], [1, 0, -1], [0, 1, -1], [1, -1, 0], [0, 1, -1]], [-2, 0, … |
| 135 | — | HELD | `test_adv_foc_quotient::test_random_never_overestimates` | every app value is a feasible dual pairing, so it never exceeds the true Phi_1. | HELD (pass) | passed |
| 136 | PIPE-01 | Critical | `test_adv_pipeline_routing::test_license_flag_must_be_bool_true[str-no]` | fda_license_granted is truth-tested: non-bool truthy values mint a token | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 137 | PIPE-01 | Critical | `test_adv_pipeline_routing::test_license_flag_must_be_bool_true[str-False]` | fda_license_granted is truth-tested: non-bool truthy values mint a token | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 138 | PIPE-01 | Critical | `test_adv_pipeline_routing::test_license_flag_must_be_bool_true[list-False]` | fda_license_granted is truth-tested: non-bool truthy values mint a token | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 139 | — | HELD | `test_adv_pipeline_routing::test_license_none_not_authorized` | a falsy None license keeps the instance out of T_auth. | HELD (pass) | passed |
| 140 | PIPE-02 | Critical | `test_adv_pipeline_routing::test_inverted_enclosure_blocks_authorization` | Layer 5 marks an inverted enclosure [5, 1] as FAILED, yet the run is AUTHORIZED | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 141 | PIPE-03 | Critical | `test_adv_pipeline_routing::test_empty_projection_blocks_authorization` | Layer 3 FAILS on an empty projection map, yet the run is AUTHORIZED (catalog G5) | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 142 | PIPE-04 | Critical | `test_adv_pipeline_routing::test_inconsistent_fiber_blocks_authorization` | Layer 3 FAILS on a projection outside the coarse profile, yet the run is AUTHORIZED | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 143 | PIPE-05 | Critical | `test_adv_pipeline_routing::test_measured_transport_loss_blocks_authorization` | declared-compatible overlap with measured transport loss 13/2 is AUTHORIZED (catalog G4) | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 144 | PIPE-06 | Medium | `test_adv_pipeline_routing::test_section_length_mismatch_not_truncated` | sections of unequal length are zip-truncated: (1,) vs (1, 999) measures zero loss | BREAK (strict xfail) | AssertionError: assert (0 > 0 or not True) + where 0 = ExactRational(numerator=0, denominator=1).sympy_ration… |
| 145 | PIPE-07 | Medium | `test_adv_pipeline_routing::test_overlap_with_missing_section_rejected` | an overlap naming a section that does not exist is silently skipped | BREAK (strict xfail) | AssertionError: assert not True + where True = LayerExecutionRecord(layer_id=<LayerId.MUR: 'MUR'>, succeeded=… |
| 146 | PIPE-08 | Medium | `test_adv_pipeline_routing::test_layer4_can_detect_a_collision` | Layer 4 has no failing branch: near-collisions at 10^-30 still 'verify metric separation' | BREAK (strict xfail) | assert False + where False = any(<generator object test_layer4_can_detect_a_collision.<locals>.<genexpr> at 0… |
| 147 | PIPE-09 | Critical | `test_adv_pipeline_routing::test_authorized_implies_every_layer_succeeded` | property: an AUTHORIZED outcome carries a FAILED layer record (catalog PIP-01) | BREAK (strict xfail) | AssertionError: {'enclosure_interval': (2, 1)} assert False + where False = all(<generator object test_author… |
| 148 | PIPE-10 | Medium | `test_adv_pipeline_routing::test_string_overlap_key_rejected` | a 2-char string overlap key 'UV' is unpacked into ('U', 'V') and accepted | BREAK (strict xfail) | assert False + where False = rejects(<function test_string_overlap_key_rejected.<locals>.<lambda> at 0x000001… |
| 149 | PIPE-11 | Medium | `test_adv_pipeline_routing::test_three_char_overlap_key_refused_not_crashed` | a 3-char string overlap key crashes Layer 2 with ValueError (no terminal) | BREAK (strict xfail) | ValueError: too many values to unpack (expected 2) |
| 150 | PIPE-12 | Medium | `test_adv_pipeline_routing::test_list_d0_refused_not_crashed` | d0 as a list of lists crashes with AttributeError (no boundary validation) | BREAK (strict xfail) | AttributeError: 'list' object has no attribute 'cols' |
| 151 | PIPE-13 | Medium | `test_adv_pipeline_routing::test_numpy_d0_refused_not_crashed` | d0 as a numpy array crashes with AttributeError | BREAK (strict xfail) | AttributeError: 'numpy.ndarray' object has no attribute 'cols' |
| 152 | PIPE-14 | Medium | `test_adv_pipeline_routing::test_float_section_refused_not_crashed` | a Python float in a local section escapes as TypeError from Layer 4 | BREAK (strict xfail) | TypeError: CODA exact arithmetic rejects float value 0.5 |
| 153 | PIPE-15 | Medium | `test_adv_pipeline_routing::test_float_enclosure_refused_not_crashed` | a Python float enclosure bound escapes as TypeError from Layer 5 | BREAK (strict xfail) | TypeError: CODA exact arithmetic rejects float value 0.0 |
| 154 | PIPE-16 | Medium | `test_adv_pipeline_routing::test_symbolic_d1_refused_not_crashed` | a symbolic d1 entry escapes as TypeError from the Gamma_2 computation | BREAK (strict xfail) | TypeError: Cannot coerce t to exact Rational: invalid input: t |
| 155 | PIPE-17 | Medium | `test_adv_pipeline_routing::test_none_sieve_refused_not_crashed` | candidate_sieve=None crashes Layer 7 with TypeError | BREAK (strict xfail) | TypeError: object of type 'NoneType' has no len() |
| 156 | PIPE-18 | Critical | `test_adv_pipeline_routing::test_blank_hypothesis_does_not_inhabit_sieve` | a sieve holding only the empty string counts as an admitted hypothesis (OR-T5 bypass) | BREAK (strict xfail) | AssertionError: assert <TerminalKind... 'AUTHORIZED'> == <TerminalKind...ED: 'REFUSED'> - REFUSED + AUTHORIZED |
| 157 | PIPE-19 | Low | `test_adv_pipeline_routing::test_blank_problem_id_rejected` | a whitespace problem_id passes the 'cannot be empty' check | BREAK (strict xfail) | assert False + where False = rejects(<function test_blank_problem_id_rejected.<locals>.<lambda> at 0x000002A0… |
| 158 | PIPE-20 | Low | `test_adv_pipeline_routing::test_non_string_problem_id_rejected` | a non-string problem_id (7) is accepted and minted into token 'AUTH-7' | BREAK (strict xfail) | assert False + where False = rejects(<function test_non_string_problem_id_rejected.<locals>.<lambda> at 0x000… |
| 159 | PIPE-21 | Low | `test_adv_pipeline_routing::test_layer8_guard_count_matches_message` | Layer 8 says 'All seven halt guards satisfied' but evaluates four guard_* conditions | BREAK (strict xfail) | AssertionError: ['guard_coherent', 'guard_license_granted', 'guard_or_passed', 'guard_zero_defect'] assert ('… |
| 160 | PIPE-22 | Medium | `test_adv_pipeline_routing::test_pipeline_closed_residual_registers_anomalon` | Layer 6 says the residual is 'retained ... as Anomalon' but the pipeline never registers one (catalog PIP-02) | BREAK (strict xfail) | assert 0 == 1 + where 0 = count() + where count = <apps.coda.domain.anomalon_registry.AnomalonRegistry object… |
| 161 | PIPE-23 | Low | `test_adv_pipeline_routing::test_layer6_metadata_consistent_for_zero_residual` | Layer 6 metadata claims residual_retained_in_cokernel=True when there is no residual | BREAK (strict xfail) | assert True is False |
| 162 | PIPE-24 | Low | `test_adv_pipeline_routing::test_zero_defect_not_labelled_anomalon` | zero-defect unlicensed runs are labelled '(Anomalon)', which the registry itself refuses to register | BREAK (strict xfail) | AssertionError: assert 'Anomalon' not in 'Pipeline te...non-promoted' 'Anomalon' is contained here: Pipeline … |
| 163 | — | HELD | `test_adv_pipeline_routing::test_pipeline_is_deterministic` | the same instance yields the same outcome twice. | HELD (pass) | passed |
| 164 | — | HELD | `test_adv_pipeline_routing::test_incoherent_residual_refused` | Gamma_2 > 0 routes to REFUSED even under license. | HELD (pass) | passed |
| 165 | — | HELD | `test_adv_pipeline_routing::test_zero_defect_unlicensed_is_closed_residual` | the non-promotion route keeps a clean unlicensed instance out of T_auth. | HELD (pass) | passed |
| 166 | — | HELD | `test_adv_pipeline_routing::test_empty_sieve_refused_under_license` | an empty support sieve is refused (OR-T5) in the plain pipeline. | HELD (pass) | passed |
| 167 | — | HELD | `test_adv_pipeline_routing::test_incompatible_overlap_refused_under_license` | a declared-incompatible overlap is refused (OR-T3). | HELD (pass) | passed |
| 168 | — | HELD | `test_adv_pipeline_routing::test_terminal_flags_disjoint` | exactly one of is_authorized / is_closed_residual / is_refused holds. | HELD (pass) | passed |
| 169 | — | HELD | `test_adv_pipeline_routing::test_genuine_obstruction_is_closed_residual` | a correctly computed obstruction is not promoted even with a license. | HELD (pass) | passed |
| 170 | REG-01 | High | `test_adv_registry_tokens::test_fingerprint_distinguishes_matrix_shape` | matrices are flattened without their shape: a 2x3 and a 3x2 boundary share one fingerprint | BREAK (strict xfail) | AssertionError: assert '7caaa333e667eca62c9305a655517c888dd85e8a9637c4aac630c26cf7c6526d' != '7caaa333e667eca… |
| 171 | REG-02 | High | `test_adv_registry_tokens::test_colliding_registration_keeps_both_records` | a shape collision returns the FIRST problem's record for the second problem | BREAK (strict xfail) | assert 1 == 2 + where 1 = count() + where count = <apps.coda.domain.anomalon_registry.AnomalonRegistry object… |
| 172 | REG-03 | Medium | `test_adv_registry_tokens::test_fingerprint_uses_normalised_rationals` | the fingerprint hashes non-normalised pairs: Phi_1 = 1/2 and 2/4 are two anomalons | BREAK (strict xfail) | AssertionError: assert '4696ca1093b9...56cae2d785aaf' == 'b8d02c38d035...ad74071d398d7' - b8d02c38d0359fd0812… |
| 173 | REG-04 | Medium | `test_adv_registry_tokens::test_same_obstruction_is_one_anomalon` | problem_id is hashed: one obstruction re-registered under fresh ids inflates the register | BREAK (strict xfail) | AssertionError: assert 5 == 1 + where 5 = len({'13a13b8fbfda73fc214d65d35f1f48c0978c7ad3c7b50bbdd6c1d9ba14261… |
| 174 | — | HELD | `test_adv_registry_tokens::test_reregistration_does_not_overwrite` | registering an existing fingerprint returns the original record unchanged. | HELD (pass) | passed |
| 175 | — | HELD | `test_adv_registry_tokens::test_zero_defect_registration_refused` | a zero defect is never registered as an anomalon. | HELD (pass) | passed |
| 176 | — | HELD | `test_adv_registry_tokens::test_concurrent_registration_is_single_record` | sixteen threads racing on one fingerprint leave exactly one record. | HELD (pass) | passed |
| 177 | REG-05 | Medium | `test_adv_registry_tokens::test_reset_does_not_erase_anomalons` | reset() erases every anomalon, contradicting 'forbids deletion' | BREAK (strict xfail) | assert 0 == 1 + where 0 = count() + where count = <apps.coda.domain.anomalon_registry.AnomalonRegistry object… |
| 178 | REG-06 | Medium | `test_adv_registry_tokens::test_no_split_brain_after_reset` | after reset() old handles keep a detached register: two 'global' registers diverge | BREAK (strict xfail) | assert 0 == 1 + where 0 = count() + where count = <apps.coda.domain.anomalon_registry.AnomalonRegistry object… |
| 179 | REG-07 | Medium | `test_adv_registry_tokens::test_records_cannot_be_deleted_directly` | the backing dict is reachable: del reg._records[k] removes an anomalon | BREAK (strict xfail) | assert (False or 0 == 1) + where False = rejects(<function test_records_cannot_be_deleted_directly.<locals>.d… |
| 180 | REG-08 | Medium | `test_adv_registry_tokens::test_anomalon_record_status_cannot_be_rewritten` | object.__setattr__ rewrites a 'frozen' anomalon's status to RESOLVED | BREAK (strict xfail) | AssertionError: assert 'RESOLVED' == 'RETAINED_OPEN' - RETAINED_OPEN + RESOLVED |
| 181 | REG-09 | Medium | `test_adv_registry_tokens::test_registry_persists_across_processes` | the register lives in process memory: a second process sees none of the first's anomalons | BREAK (strict xfail) | AssertionError: assert '0' == '1' - 1 + 0 |
| 182 | REG-10 | Critical | `test_adv_registry_tokens::test_token_cannot_be_minted_by_caller` | any caller mints AuthorityToken(granted_externally=True); the check is a self-declared bool | BREAK (strict xfail) | assert False + where False = rejects(<function test_token_cannot_be_minted_by_caller.<locals>.<lambda> at 0x0… |
| 183 | REG-11 | High | `test_adv_registry_tokens::test_token_post_init_cannot_be_skipped` | object.__new__ skips __post_init__: a token with granted_externally=False exists | BREAK (strict xfail) | AssertionError: assert not True + where True = MasterNormalFormOutcome(problem_id='lic', terminal_kind=<Termi… |
| 184 | REG-12 | Medium | `test_adv_registry_tokens::test_token_licensee_cannot_be_replaced` | dataclasses.replace re-issues a genuine token to a new licensee | BREAK (strict xfail) | assert False + where False = rejects(<function test_token_licensee_cannot_be_replaced.<locals>.<lambda> at 0x… |
| 185 | REG-13 | Critical | `test_adv_registry_tokens::test_forged_token_not_equal_to_issued_token` | token ids are predictable 'AUTH-<problem_id>': a caller forges a token equal to the real one | BREAK (strict xfail) | AssertionError: assert AuthorityToken(token_id='AUTH-target', licensee='ExternalSovereignAuthority', granted_… |
| 186 | REG-14 | Critical | `test_adv_registry_tokens::test_token_replay_into_other_outcome_rejected` | tokens are not bound to evidence: problem A's token authorizes an obstructed outcome for B | BREAK (strict xfail) | AssertionError: assert (False or not True) + where False = rejects(<function test_token_replay_into_other_out… |
| 187 | REG-15 | High | `test_adv_registry_tokens::test_authorized_outcome_requires_zero_residual` | MasterNormalFormOutcome(AUTHORIZED) with Phi_1 = 5 is constructible outside Layer 9 | BREAK (strict xfail) | assert False + where False = rejects(<function test_authorized_outcome_requires_zero_residual.<locals>.build … |
| 188 | REG-16 | High | `test_adv_registry_tokens::test_residual_outcome_cannot_carry_token` | a CLOSED_RESIDUAL outcome can carry an AuthorityToken (GTLA-T8 only enforced in Layer 9) | BREAK (strict xfail) | assert False + where False = rejects(<function test_residual_outcome_cannot_carry_token.<locals>.<lambda> at … |
| 189 | REG-17 | High | `test_adv_registry_tokens::test_authority_contract_cannot_be_forged` | AuthorityContract(AUTHORIZED) with a forged token is constructible outside the firewall | BREAK (strict xfail) | assert False + where False = rejects(<function test_authority_contract_cannot_be_forged.<locals>.forge at 0x0… |
| 190 | REG-18 | Medium | `test_adv_registry_tokens::test_layer_record_metadata_is_immutable` | 'frozen' layer records hold a mutable metadata dict: the audit trail is edited after the fact | BREAK (strict xfail) | assert (False) + where False = rejects(<function test_layer_record_metadata_is_immutable.<locals>.tamper at 0… |
| 191 | REG-19 | Medium | `test_adv_registry_tokens::test_refusal_reasons_are_immutable` | Layer 7's refusal reasons are a mutable list inside the frozen record | BREAK (strict xfail) | assert False + where False = rejects(<function test_refusal_reasons_are_immutable.<locals>.<lambda> at 0x0000… |
| 192 | — | HELD | `test_adv_registry_tokens::test_outcome_fields_are_frozen` | plain attribute assignment on an outcome is refused. | HELD (pass) | passed |
| 193 | — | HELD | `test_adv_registry_tokens::test_internal_token_refused` | AuthorityToken(granted_externally=False) raises PermissionError. | HELD (pass) | passed |
| 194 | — | HELD | `test_adv_registry_tokens::test_unknown_anomalon_lookup_is_none` | looking up an unknown fingerprint returns None. | HELD (pass) | passed |
| 195 | TRI-01 | Critical | `test_adv_triad_divergence::test_triad_honours_empty_sieve` | the triad discards the Layer-7 refusal: an empty sieve + license is AUTHORIZED (pipeline: REFUSED) | BREAK (strict xfail) | AssertionError: assert <TerminalKind... 'AUTHORIZED'> == <TerminalKind...ED: 'REFUSED'> - REFUSED + AUTHORIZED |
| 196 | TRI-02 | Critical | `test_adv_triad_divergence::test_triad_honours_incompatible_overlap` | the triad ignores declared-incompatible overlaps: AUTHORIZED (pipeline: REFUSED) | BREAK (strict xfail) | AssertionError: assert <TerminalKind... 'AUTHORIZED'> == <TerminalKind...ED: 'REFUSED'> - REFUSED + AUTHORIZED |
| 197 | TRI-03 | High | `test_adv_triad_divergence::test_triad_and_pipeline_agree_on_incoherent_residual` | Gamma_2 > 0 is a registered anomalon in the triad but REFUSED in the pipeline | BREAK (strict xfail) | AssertionError: assert <TerminalKind...SED_RESIDUAL'> == <TerminalKind...ED: 'REFUSED'> - REFUSED + CLOSED_RE… |
| 198 | TRI-04 | High | `test_adv_triad_divergence::test_triad_and_pipeline_agree_on_random_instances` | seeded differential: triad and pipeline disagree on unlicensed random instances | BREAK (strict xfail) | AssertionError: 23/40: [(1, 'REFUSED', 'CLOSED_RESIDUAL'), (2, 'REFUSED', 'CLOSED_RESIDUAL'), (4, 'REFUSED', … |
| 199 | TRI-05 | Low | `test_adv_triad_divergence::test_triad_trace_covers_nine_layers` | the triad trace has 7 layer records; the outcome claims a comprehensive 9-layer trace | BREAK (strict xfail) | AssertionError: assert 7 == 9 + where 7 = len((LayerExecutionRecord(layer_id=<LayerId.FOC: 'FOC'>, succeeded=… |
| 200 | TRI-06 | Medium | `test_adv_triad_divergence::test_proposal_problem_cannot_be_mutated_after_check` | ProblemInstance is mutable: the license flag is flipped after ProposalContract checked it | BREAK (strict xfail) | assert False + where False = rejects(<function test_proposal_problem_cannot_be_mutated_after_check.<locals>.m… |
| 201 | TRI-07 | Critical | `test_adv_triad_divergence::test_mutated_proposal_problem_not_authorized` | after the TOCTOU flip the same proposal's problem is AUTHORIZED by the plain pipeline | BREAK (strict xfail) | AssertionError: assert <TerminalKind.AUTHORIZED: 'AUTHORIZED'> != <TerminalKind.AUTHORIZED: 'AUTHORIZED'> + w… |
| 202 | — | HELD | `test_adv_triad_divergence::test_proposal_rejects_embedded_string_license` | a truthy embedded license (even the string 'yes') is refused at construction. | HELD (pass) | passed |
| 203 | — | HELD | `test_adv_triad_divergence::test_proposal_rejects_empty_proposer` | an empty proposer_id is refused. | HELD (pass) | passed |
| 204 | TRI-08 | Critical | `test_adv_triad_divergence::test_proposal_budget_limit_is_enforced` | ProposalContract.budget_limit_seconds is ignored: a 1 ns budget still runs to AUTHORIZED | BREAK (strict xfail) | AssertionError: assert <TerminalKind... 'AUTHORIZED'> == <TerminalKind...ED: 'REFUSED'> - REFUSED + AUTHORIZED |
| 205 | TRI-09 | High | `test_adv_triad_divergence::test_budget_exhaustion_does_not_fabricate_evidence` | on budget exhaustion the EvaluationContract reports fabricated Phi_1 = Gamma_2 = 1 as evidence | BREAK (strict xfail) | assert (1, 1) != (1, 1) |
| 206 | TRI-10 | Medium | `test_adv_triad_divergence::test_budget_rejects_nan` | max_seconds = NaN is accepted and can never be exceeded | BREAK (strict xfail) | assert False + where False = rejects(<function test_budget_rejects_nan.<locals>.<lambda> at 0x000001B80AAF5BC… |
| 207 | TRI-11 | Medium | `test_adv_triad_divergence::test_budget_rejects_infinity` | max_seconds = inf is accepted: an unbounded 'finite' budget | BREAK (strict xfail) | assert False + where False = rejects(<function test_budget_rejects_infinity.<locals>.<lambda> at 0x000001B80A… |
| 208 | — | HELD | `test_adv_triad_divergence::test_budget_rejects_negative_seconds` | a negative budget is refused. | HELD (pass) | passed |
| 209 | — | HELD | `test_adv_triad_divergence::test_budget_step_limit_trips` | the step counter raises once max_steps is exceeded. | HELD (pass) | passed |
| 210 | — | HELD | `test_adv_triad_divergence::test_tiny_time_budget_refuses` | an exhausted time budget routes to REFUSED via GUARD_6. | HELD (pass) | passed |
| 211 | TRI-12 | High | `test_adv_triad_divergence::test_budget_interrupts_a_long_layer` | the budget is only checked between layers: a 0.05 s budget lets Layer 1 run for seconds | BREAK (strict xfail) | AssertionError: budget 0.05 s, wall time 2.81 s assert 2.8085191000063787 < 0.5 |
| 212 | TRI-13 | Low | `test_adv_triad_divergence::test_triad_exposes_step_budget` | the triad exposes no step budget: it ticks 70 steps against a fixed 100,000 limit | BREAK (strict xfail) | assert 'max_steps' in mappingproxy(OrderedDict({'proposal': <Parameter "proposal: 'ProposalContract'">, 'call… |
| 213 | TRI-14 | Medium | `test_adv_triad_divergence::test_triad_refuses_shape_error` | a wrong-width d1 raises ShapeError out of the triad instead of an AuthorityContract | BREAK (strict xfail) | sympy.matrices.exceptions.ShapeError: Matrix size mismatch: (1, 3) * (2, 1). |
| 214 | TRI-15 | Medium | `test_adv_triad_divergence::test_triad_refuses_type_error` | a float section raises TypeError out of the triad (only BudgetExhaustedError is caught) | BREAK (strict xfail) | TypeError: CODA exact arithmetic rejects float value 0.5 |
| 215 | — | HELD | `test_adv_triad_divergence::test_triad_genuine_residual_retained` | a correctly witnessed obstruction is retained as a registered anomalon. | HELD (pass) | passed |

## 7. Repair status (2026-09-23)

All 148 break IDs (153 test items, counting parameters) are fixed. Each fixed
test's strict-`xfail` marker has been replaced by a comment of the form
`# FIXED 2026-09-23 (was BREAK ID: why)`, so the test file keeps the history.
The test body still asserts the secure property, and it now passes. A few
bodies were adapted where the repair changed the API the attack went through:
they now build outcomes with `dataclasses.replace`, obtain grants from a test
authority, and accept a typed `REFUSED` terminal for malformed input. None of
the adaptations weakens the property the test states.

Full run on CPython 3.14.2 and 3.12.10, `pytest -n 8`, over `apps/coda/tests`
and `apps/alpha/tests`: **249 passed, 0 xfail, 0 failed**. That is 33 original
tests (one new: `test_token_minting_requires_a_verified_spent_grant`), 215 adversarial
tests and 1 Alpha-client test. The Alpha test moved out
of `apps/coda` so that `apps/coda` imports no sibling app.

| Cause (§3) | Repair |
|---|---|
| 3.1 Φ₁ was one dual pairing | `domain/l1_quotient.py` computes the exact L1 quotient with a certificate: a primal repair and a dual witness of equal value. Incidence (graph) matrices use a spanning-forest potential and sign-oriented cycle packing. Any other matrix uses exact Gaussian elimination for image membership, then an exact rational simplex with Bland's rule. On 200 random instances it agreed with the F005 FOC oracle every time. Layer 1, the repair use case and the solver adapter all call this one solver. |
| 3.2 Authority was a caller boolean | `domain/authority.py`: an `ExternalAuthority` signs an `AuthorityGrant` (HMAC-SHA256). The grant binds the problem digest, the evidence digest, the licensee and a nonce. The firewall verifies it against a keyring the caller supplies and spends the nonce. A bool, a string, a bare claim, a forged, replayed or mis-bound grant is refused (`HALT_GUARD_5_BREACH`). Tokens carry a process-private seal and cannot be constructed without one. |
| 3.3 The firewall trusted forged evidence | Evidence is sealed and digested. Unsealed evidence is recomputed and compared. A supplied witness is checked for shape, ‖y‖∞ ≤ 1, Dᵀy = 0 and pairing. |
| 3.4 Failed layers did not gate | Any failed layer record refuses. The direct pipeline is the triad with an internal proposal, so the two entry points can no longer disagree. |
| 3.5 No boundary validation | `domain/intake.py` validates types, shapes, overlap keys, the cochain column and d₁d₀ = 0, and computes the problem digest. Any fault becomes a typed `REFUSED` with a reason, not an exception. |
| 3.6 Exact-arithmetic gaps | `ExactRational` normalises and accepts only integer fields. Floats, strings and decimals are refused. `DualWitness` checks its declared norm. |
| 3.7 Register | `use_cases/anomalon_store.py` is a JSONL file at `$CODA_ANOMALON_REGISTER` (default `~/.coda/anomalon_register.jsonl`), append-only; the first registration of a fingerprint wins. The fingerprint covers shape and non-zeros. `reset()` drops the handle, not the records. `status` is read-only. The direct pipeline registers through the firewall. |
| 3.8 Budget | The clock is injected (the domain imports no clock). The budget is ticked on every solver pivot, rejects NaN, ∞ and bool, and honours the proposal's own limit. On exhaustion Φ₁ and Γ₂ are reported as unknown (`None`), never as fabricated values. |
| 3.9 Architecture, CLI, bridge, audit | The domain imports no outer layer. `pyproject.toml` maps `apps.coda` onto the flat directory. The CLI never mints from `--licensed`, exits non-zero on any FAIL verdict, and rejects bad arguments as usage errors. The Rust bridge reports `PYTHON_EXACT_RUST_NOT_EXECUTED` with the exact Python value. The audit returns named checks, uses no `assert`, and checks the certificate independently. |
| 3.10 Documentation | The catalog's guard list and test count match the code. The README tree lists every module. F005 ledger rows that cite `apps/coda` were re-cited or retyped (see the F005 change logs of 2026-09-23 in `a/`, `fda/`, `or/`, `coda_gtla/` and `coda/`). |

What the repair does not certify:

- The suite is still a finite set of probes (§5).
- Key management belongs to the caller. The test authority's key lives in the
  test tree and authorizes nothing outside the tests.
- The seals stop forgery through the public API. They do not stop code that
  bypasses constructors (`object.__new__`, `object.__setattr__`). The audit test
  builds its injected breach exactly that way, and the audit reports it.
- No Rust runner is wired. Every value comes from the exact Python solver.
