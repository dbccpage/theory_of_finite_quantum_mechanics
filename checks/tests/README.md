# Reviewed-checker verification

AuthorityEffect: None.

Install the pinned dependencies in `requirements.txt`. Run each `test_*.py`
suite with `python -I -B -X utf8`, and again with `-O`. The workflow supplies
these commands for the reviewed populations. A passing suite certifies only
its named finite cases, boundaries and source versions.

`test_review_repairs.py` runs the 20 alphabetical independent checkers through
`dfm-continuum-refinement-limit.py` in separate, time-bounded processes. The six
computation entry points now compose into one application; earlier receipts
retain their original 25-source population. `test_ads_checkers.py` adds generated exact
properties and input/lifecycle tests for the four AdS checkers. The shared
infrastructure has its own property, mutation-accounting and lifecycle suites.

`test_authority_checkers.py` checks bounded request codecs, finite behavior
quotients and the direct-candidate ceiling read from its recovered record.
`authority_mutations.json` uses the same candidate format and snapshot replay
steps as the AdS manifest below; substitute the authority suite and
`AuthorityCheckerTests` class. Also copy the recorded JSON from
`papers/foundations/authorization_incompleteness/evidence/original/`
into the corresponding location beside the snapshot's `checks` directory.
The final authority receipts retain 43 candidates: 42 killed and one equivalent
under the declared result contract, with the raw survivor and proof preserved.

For the support mutation campaign, run:

```powershell
python -I -B -X utf8 checks/tests/run_support_mutations.py checks/tests/support_mutations.json support-results.json
```

The runner preserves all six outcome classes. A raw survivor remains visible
even when a separate, domain-specific proof establishes equivalence.

`ads_mutations.json` contains the exact source replacement and selected test
names for each AdS campaign candidate. Its source paths are relative to
`checks`; the support runner above intentionally accepts only its own support
population. To replay an AdS candidate:

1. Copy `checks` to a disposable directory, excluding caches. Run
   `python -I -B -X utf8 <snapshot>/tests/test_ads_checkers.py` and require a
   successful baseline with a nonzero test count.
2. Verify the candidate's `before` string occurs exactly once in its source;
   replace it with `after` only in that snapshot. Compile before testing;
   syntax-invalid candidates are `invalid`, not killed.
3. Run `python -I -B -X utf8 <snapshot>/tests/test_ads_checkers.py`
   followed by `AdsCheckerTests.<test>` for every listed test. Use a 30-second
   subprocess timeout. A unittest failure is a kill; a successful nonempty
   test run survives. Timeout or harness failure is inconclusive.
4. Restore the original bytes before another candidate. Retain every candidate,
   including unrun candidates after interruption, with source/test hashes and
   captured output. Dispose of the snapshot even on failure or cancellation.

The November 3 raw and follow-up receipts under `reviews/repository_file_review`
preserve the original 66/68 result, the two additional regression challenges,
and the final 68/68 detection result. These finite campaigns are not exhaustive
proofs of correctness.

`test_wilson_checker.py` adds generated receipt accounting, malformed/duplicate
cases, injected matrix faults and CLI/cancellation tests for TFQ-1050. Replay
`wilson_mutations.json` by substituting that suite and `WilsonCheckerTests` in
the four snapshot steps above. Its recorded campaign kills all 17 candidates;
the shared support and first-25 suites supply independent matrix oracles.

`test_strong_coupling_checker.py` checks exact arithmetic and threshold scales,
combined power budgets, immutable subgroup tables and TFQ-1052 receipt behavior.
Replay `strong_coupling_mutations.json` with `StrongCouplingCheckerTests` using
the same snapshot protocol. The 73 retained candidates have 72 detected faults
and one algebraically equivalent internal gamma-sign change. Original survivors,
additive test repairs, exact prior-manifest copies and the equivalence proof are
retained under `reviews/repository_file_review`; no candidate was discarded.

`test_lineon_checker.py` verifies path snapshots, site/edge witnesses, exact
holonomy, symbolic curvature, literal toy rules and the TFQ-1219 receipt.
Replay `lineon_mutations.json` with `LineonCheckerTests`. All 48 candidates are
detected. Two original selected-property runs missed faults that the existing
fixed fixture suite detects; the updated selectors include those fixtures, and
the original manifest and all raw outcomes remain available.

`test_computation_controls.py` verifies the immutable finite-word system,
bounded shortest paths, trace certificates, conservative resource refusals and
all six original computation controls. Replay `computation_mutations.json`
with `ComputationControlTests`. All 64 retained candidates are detected.
Three originally selected tests missed faults caught by existing fixed-control
or independent graph tests; both original and amended selections are retained.
The old six source/companion pairs have byte-preserved archives and a migration
map in `reviews/repository_file_review/2026-11-03-computation-retirement.json`.

`test_cqft_checkers.py` verifies bounded rational matrices, integer operator
products, the four-point order and exact qubit unfoldings with separate SymPy
and bit-insertion oracles. Replay `cqft_mutations.json` with `CqftCheckerTests`.
The 69 retained candidates comprise 67 detected faults and two equivalent
validation bypasses, with written equivalence arguments. The initial run,
strengthened ownership/index/order challenges, full rerun and a runtime-neutral
local type annotation are recorded separately; no original outcome was removed.

`test_constructor_theory.py` verifies owned finite task tables, rectangular
inverses, product regrouping, blank-slice predicates, normalized concurrence and
the exact rank family. Replay `constructor_theory_mutations.json` with
`ConstructorTheoryTests`. All 55 candidates remain recorded: 54 detected faults
and one determinant-only equivalent transpose. Initial survivors, targeted
follow-ups and additive test custody are retained. The suite also corrects the
Gaussian squared-norm cost bound using coprime 4096-bit denominators; unchanged
Gaussian source retains its earlier mutation evidence. Run the support suite
alongside this suite and the integration suite, in normal and optimized Python.

`test_bphz_checker.py` verifies finite forest enumeration, owned edge mappings,
bounded scalar/matrix arithmetic and the commuting-projector aggregate. Replay
`bphz_mutations.json` with `BphzCheckerTests`; all 40 retained candidates are
detected. Independent bitmask, symbolic-matrix, partial-fraction and diagonal
projector oracles support its 12 groups. Run it and the integration suite in
normal and optimized Python; no continuum conclusion follows from these tests.

`test_ckm_checker.py` verifies bounded Gaussian rephasing tables, constructive
witnesses, exact quartets/counting and failed-refusal handling. Replay
`ckm_mutations.json` with `CkmCheckerTests`. The 39 candidates have 38 detected
faults and one typed-boundary equivalent width check. The original six timeouts
and two survivors remain in the raw receipt; the closure receipt records fast
nonreal fixtures, shape-preflight error precedence and their exact additive
custody. Run the 14-group suite and the integration suite in both Python modes.

`test_continuum_interface.py` verifies bounded SL2 connections, exact path order,
rooted dressing, validated footprints and immutable ownership. Replay
`continuum_interface_mutations.json` with `ContinuumInterfaceTests`. All 39
candidates remain: 38 detected faults and one typed-boundary equivalent early
label check. The initial two survivors, added prefix-preflight challenge and
diagnostic-text distinction are retained in separate receipts. Run its 13 groups
and the integration suite in normal and optimized Python.

`test_refinement_limit.py` verifies owned dyadic cells, exact callback results,
bounded scalar accumulations and ordered S3 transport with independent recursive
oracles. Replay `refinement_limit_mutations.json` with `RefinementLimitTests`.
All 35 candidates are detected. The original coherent-inverse survivor and the
added non-involutive endpoint fixtures remain separately recorded with exact
test custody. Run its 13 groups and the integration suite in both Python modes;
the default checker retains all 14642 obligations.
`test_electroweak_checker.py` verifies owned Gaussian doublets, supplied rational
roots, unit-phase actions and exact residual covariance with independent SymPy
and rational-sphere oracles. Replay `electroweak_mutations.json` with
`ElectroweakCheckerTests`. All 39 candidates are detected; the original survivor
and three shrinking timeouts remain, with a separate exactly additive fixed
nonreal fixture and follow-up receipt. Run its 15 groups and the integration
suite in normal and optimized Python. The checker reports 761 obligations and
does not infer continuum dynamics or universal rational root existence.

`test_gribov_checker.py` verifies owned rational3x3 weighted trace forms, strict
shape admission, per-operation budgets and typed value/difference results with
independent SymPy oracles and nonsymmetric fixed data. Replay
`gribov_mutations.json` with `GribovCheckerTests`: all 30 candidates are detected.
The original constructor-selector survivor and its one-line additive closure
remain separately recorded. Run its 11 groups and the integration suite in both
Python modes. The checker counts 10 finite obligations, with no continuum claim.

`test_hierarchical_borel.py` verifies owned B2(Q) trees, exact matrix factors,
finite cycle detection, bounded transport and two-stage residuals. Independent
symbolic matrices and path products support its 12 groups. Replay both
`hierarchical_borel_mutations.json` and `hierarchical_borel_cycle_mutation.json`
with `HierarchicalBorelTests`: all45 candidates are detected. The separate cycle
challenge uses a finite lookup sentinel, not a harness-timeout-as-kill. Run this
suite and integration in both Python modes. Default93 mathematical obligations
replace99 after retiring seven literal/lexical sentinels and adding one general
torus homomorphism check; original source/counts remain archived.

`test_regge_checker.py` verifies bounded signed-rational cosine formulas and an
independently supplied Cayley block through matrix inversion and coordinate
projections on right triangles. Replay `regge_mutations.json` with
`ReggeCheckerTests`: all32 candidates are detected. The original denominator
survivor and added4097-bit denominator/4096-bit quotient case remain separately
recorded. Run its12 groups and integration in both Python modes. Default19
obligations do not construct a Regge complex or continuum equation.

`test_relational_time.py` verifies owned S3 schedules, chronological frames,
closure/seams, reversible endpoint coordinates and rational packed clocks.
Independent point-action and Kronecker oracles support its12 groups. Replay
`relational_time_mutations.json` with `RelationalTimeTests`:45 detected faults
and one typed-boundary equivalent outer empty guard among46 retained candidates.
Initial outcomes and the exactly additive three-cycle direction test remain
separate. Run this suite and integration in both Python modes. The default
checker records347936 obligations; no continuous-time generator is constructed.

`test_symanzik_checker.py` verifies owned indexed multigraphs, exact mask/weight
admission, cotree sums and intermediate budgets. Independent BFS and weighted
Laplacian determinants support12 groups with80 examples per property. Replay
`symanzik_mutations.json` with `SymanzikCheckerTests`; for the helper-polarity
candidate also run `test_mask_and_weight_refusals` as recorded in the closure
receipt. All36 candidates are detected, with the original selected-test survivor
retained. Run the suite and integration in both Python modes. Default22
obligations preserve247 and8; no QED interval is constructed.

`test_counterterm_checker.py` verifies owned exact Dirac kernels, immutable
Gaussian matrices, propagator inversion and lowered vertex contractions.
Independent Kronecker and symbolic inversion oracles support13 groups with80
examples per property. Replay `counterterm_mutations.json` with
`CountertermCheckerTests`; the closure receipt adds the distinct row-major and
inverse-operator-sign fixture for the two original selected-test survivors.
All36 candidates are detected, with original suite/quality and outcomes retained.
Run the suite and integration in both modes. Default25 obligations preserve
the original witness; no counterterm ratio or loop integral is computed.

`test_continuous_time_checker.py` verifies owned finite maps, exhaustive square
roots, bounded iteration and exact Gaussian/polynomial branch witnesses.
Independent matrix-power/root and symbolic arithmetic oracles support13 groups.
Replay `continuous_time_mutations.json` with `ContinuousTimeCheckerTests`; the
closure receipt adds `test_composition_refuses_carrier_loss` for the original
carrier-guard survivor. All36 candidates are detected with initial evidence
retained. Run this suite and integration in both modes. Import is silent and
default355 checks retain all distinct original claims; no continuous-time
generator or measure is constructed.

`test_positive_form_controls.py` verifies the composed integer Gram application,
including exact bilinear/event/diagonal weights and carrier-preserving coarse
partitions. Independent symbolic Gram/incidence oracles support14 groups with80
examples per property. Replay `positive_form_mutations.json` with
`PositiveFormTests`: all43 candidates are detected. Run this suite and integration
in both modes. Two original import-time applications are byte-archived and
replaced;4017 current obligations retain both distinct scientific boundaries.

The current `test_continuous_time_checker.py` also covers the composed order-four
residue application. Its19 groups retain the earlier13 and add six integer
matrix/power/domain/lifecycle groups. Replay `discrete_dynamics_mutations.json`
with `ContinuousTimeCheckerTests`: all53 faults are detected. The original36-case
manifest and prior assessment remain historical evidence, with exact migration
recorded. Default612 checks split355 root/branch and257 residue obligations.
Run the current suite and integration in both modes; no U1 fiber is inferred.

The current `test_positive_form_controls.py` also covers the composed Born-boundary
controls. Its20 groups retain the prior14 and add six normalization/rotation
groups. Replay `born_controls_mutations.json` with `PositiveFormTests`:63 of65
mutants are killed; two survivors are explicitly adjudicated as public-contract
equivalents in the review receipt. The prior43-case manifest remains historical evidence.
Default6550 checks split619 positivity,3398 decoherence and2533 Born-boundary
obligations. Run the current suite and integration in both modes. These exact
finite controls do not derive Born uniqueness or select a probability rule.

The observer-presheaf checker composes owned measurement scenarios, empirical
models, exact linear programs/certificates and a bounded Cech complex. Run
`test_exact_linear_program.py` (9 groups), `test_empirical_model.py` (8),
`test_cech_complex.py` (8) and `test_observer_presheaf.py` (8) in both ordinary
and optimized modes, plus `checks/tests/test_foc035_lp_certificates.py` (20 existing
adapter cases). Each generated property uses80 deterministic examples.
The app retains50 named CLI check groups and the legacy scalar/ValueError
certificate adapter. LP witnesses distinguish optimum, infeasibility and
unboundedness; a pivot budget refusal never means infeasibility.

`observer_presheaf_mutations.json` carries80 recipes with per-case `suite` and
test selections. Use the matching unittest class: `ExactLinearProgramTests`,
`EmpiricalModelTests`, `CechComplexTests` or `ObserverPresheafTests`. The initial
76-kill/4-survivor campaign and two additive isolation fixtures remain recorded.
The current manifest includes those four closing selections. Final replay uses
isolated snapshots and retains every outcome; receipts are in the observer
review evidence. These Python bounds do not claim to replay the imported Rust
resource ceilings or to establish the source's general presheaf theorems.

The Gaussian modulo-two checker uses an owned56-frame system and a shared
bounded rational inverse verifier. `test_mod2_frame_system.py` has13 groups;
run it normally and under `-O`. Its independent bases include symbolic
adjugate/determinant, all56 parsed Lean frames and inverse coefficient rows,
Hermitian products, and generated odd-scaled/permuted frame systems. The
default CLI checks567 conditions:565 retained obligations plus two explicit
inverse coefficient bounds. It certifies this class ansatz only.

`mod2_mutations.json` has38 recipes for `Mod2FrameSystemTests`, replayed in
isolated snapshots with the Lean fixture copied beside the snapshot. The
initial32-kill/6-survivor results remain; two additive methods isolate eager
shape/normalization checks, product versus difference budgets and malformed
Gaussian pairs. Final full replay uses all38 retained faults with the closing
test selections. Import is silent, expected failures are typed and nonzero at
the CLI, and resource refusal remains distinct from singularity.

The rational-rays checker owns canonical primitive integer representatives and
composes the shared inverse certificate for its seven-ray obstruction.
`test_rational_ray_obstruction.py` has12 groups; run normally and under `-O`.
It checks independent projective fractions, all1854 original admitted box
vectors, symbolic cross products/quadratic rows, raw small-box pair coverage,
and a separate symbolic rank/nullspace certificate. Default20872 checks cover
865 distinct box rays and5502 completed orthogonal pairs; completing rays may
leave the box. All64 parity-admitted mod4 tuples replace repeated sampling.

`rational_rays_mutations.json` retains41 faults. Initial36 kills and5 survivors
remain recorded; one additive fixture closes three masked boundary tests.
Final replay kills39. The remaining two scaling-guard removals are explicitly
adjudicated as equivalent at the declared API because the constructor repeats
the same checks before normalization; both guards remain. The adjudication
includes120 paired API comparisons and the original raw survivor outputs.

The Gaussian extension application owns its exact closed-schema certificate and
composes `ExactJsonDocument` for bounded UTF-8 input. The unchanged JSON has277
literal primitive vectors,210 frames and19 real prescriptions. The16 groups in
`test_gaussian_extension_certificate.py` compare every frame/value/weight with
Lean, independently replay the symbolic linear contradiction, generate exact
Hermitian and residue controls, and exercise reindexing, ownership, malformed
inputs, resource limits, CLI compatibility and cancellation. Run normally and
with `-O`; source-checkout verification also runs the existing focused consumer.

`extension_mutations.json` retains41 critical fault recipes for
`GaussianExtensionTests`. Initial34 kills and7 survivors remain recorded;
one additive test isolates masked admission, arithmetic and parser guards.
Replay the full manifest in isolated snapshots carrying the unchanged JSON
and Lean fixture; do not treat a failed baseline or timeout as a kill. The
certificate excludes this prescribed extension only; its metadata commit is
an identifier, not authentication, and no new Lean build is claimed.

The binary-colouring checker owns the49-ray witness and composes
`BinaryFrameSystem`. The14 groups in `test_binary_colouring.py` compare every
one of the1024 four-variable pair/triple systems to direct enumeration, add100
generated solver/partial-propagation cases, and independently reconstruct the
projective geometry and symbolic Boolean contradiction. The Lean proof's49
rays,82 selected pairs, their literal cross completions and26 internal frames
are compared with the full138-pair checker; the pruned system is independently
UNSAT too. This source comparison is not a new Lean build.

`colouring_mutations.json` retains40 critical fault recipes for
`BinaryColouringTests`. The initial37 kills and3 survivors remain archived;
one additive method isolates the three masked guards and another checks the
Lean table. Search exhaustion is a successful UNSAT result; reaching the
node limit is a separate resource failure and cannot certify an obstruction.
Run the suite normally and under `-O`, with the Lean fixture beside a mutation
snapshot. The original CLI census,90 outside raw completions and11 search
nodes are retained. The source-checkout focused consumer is also retested.

## Tomography witness composition

The tomography application composes GaussianVector3, InertPrimeResidual,
OrthogonalGaussianPair, EquatorialRayGeometry and HermitianTomography. Each
owns its admitted state. The three suites test exact vector arithmetic,
independent prime factorization/quadratic characters, symbolic projectors,
rotation formulas, input/resource boundaries and the complete CLI. Run each
normally and under `-O`:

```
python -I -B -X utf8 checks/tests/test_inert_prime_geometry.py
python -I -B -X utf8 checks/tests/test_tomography_geometry.py
python -I -B -X utf8 checks/tests/test_gaussian_tomography_controls.py
```

`tomography_obligations.json` maps all65 original static guards to their
replacement symbols. The exact original source and315-check runtime trace
remain archived; the composed runner now records979 actual control calls.
The population checks retain all six original frames and all original
oscillation/geometry grids. Source custody is distinct from the independent
mathematical oracles. These finite controls establish neither pointwise-to-
uniform continuity nor general frame-function rigidity.

`tomography_mutations.json` specifies99 faults with `suite:class.method`
selectors. Snapshots need the three test modules, the obligation map and the
archived original source/initial-review receipt at their repository-relative
paths. Each worker has a30-second timeout; failfast stops after a recorded
unittest failure. All three unmodified suites must pass before challenges.
Retain the initial89 kills,7 survivors and3 inconclusive timeouts separately
from subsequent outcomes. Five additive methods isolate missing edge cases
and add deterministic small counterexamples; prior assertions/selectors are
retained. A timeout or failed baseline is never a kill. CI is wired for both
Python3.12/3.14; local receipts state the interpreter actually executed.

Run `python -I -B -X utf8 checks/tests/test_integer_obstructions.py` to verify
the bounded Hilbert, Stone and U1 controls. Repeat with `-O` to exercise the
optimized interpreter. The suite compares roots against SymPy factorization,
enumerates the original integer windows and checks resource and failure paths.
The 53 fault recipes are in `integer_obstructions_mutations.json`.
