# The Witnessed Difference Programme

[The mechanism inventory](witnessed_difference_programme.md#mechanism-inventory) defines the
internal papers within this single publication. The current adversarial pass
corrects confirmed claim and implementation defects; it does not certify every
statement or replace the explicitly scoped reproduction records below.

Jeremy H. Carroll · edition 2.4.5 · 2026-10-16

Edition 2.4.5 adds [executable certificate refinement](docs/derivations/executable_reasoning_refinement.md)
and formal graph transport to the reasoning calculus. Seventeen new Lean
theorems connect concrete checkers to the abstract semantics; Python and Rust
export certificates for independent kernel replay. The
[refinement receipt](manifests/executable_reasoning_refinement.json) records the
scoped execution. Whole-program foreign-language equivalence and broader WDP
interpretation remain open.

The 2.4.1 editorial correction separated mathematical status, formalization scope
and paired reproduction status; corrected the dated evidence inventory; and
added a bibliography and proof-supplement guide to the PDF. The present
clearance pass makes the signed-weight, empirical-table and observation-budget
premises explicit and withdraws an unsupported MUB6 moduli-classification claim.
It retains the written finite theorems and six internal papers. Source, rendered artifacts and checksum
inventories are rebuilt together. The current edition remains an unpublished correction candidate,
not a new full Lean/Rust or whole-suite certification. See the
[change log](witnessed_difference_programme_change_log.md).
The Python distribution now has software version 2.4.5.

This revision rebuilds the source and PDF; a new deposit archive has not been
created. Packaging remains a separate release task. A future validated archive
for this edition should use
`dist/v2.4.5/000_witnessed_difference_programme_2026-10-16.zip`.
The dated ZIPs already in the paper root are preserved earlier editions.

Read the [manuscript](witnessed_difference_programme.md) or its
[PDF](witnessed_difference_programme.pdf). The central result concerns an
explicit report map and protected question: a report preserves the answer
exactly when the answer is constant on each report fiber. Linear repair
systems and finite observation problems give concrete instances.

The [claim ledger](witnessed_difference_programme_claim_ledger.md),
[current evidence guide](docs/current_claim_evidence.md),
[change log](witnessed_difference_programme_change_log.md) and
[source errata](docs/source_errata_20261008.md) distinguish written results,
selected formalizations, executable checks and retained historical claims.
Code correctness does not supply a physical interpretation or authorize an
action. Proposal, evaluation and authorization have separate inputs and roles.

The 2026-10-11 checks replayed the 50-module/691-declaration core audit,
115 observation tests and all 12 stored observation certificates. The changed
status notebook replayed from both supported working directories; the other
nine notebook receipts remain historical. The 2026-10-12 typesetting pass
produced a 278-page PDF with zero missing-glyph warnings and zero overfull boxes. The builder
refuses to replace the PDF while either warning remains. Full Mathlib/Rust
and whole-suite deposit verification are not established by those records.
The 2026-10-13 completion-module compatibility replay is separately scoped in
[Appendix O.1](witnessed_difference_programme.md#o1-relative-continuity-closes-the-realized-image):
two unchanged modules on Lean 4.34.0, not a full build at the pinned versions.

## Guarded schedule classification

[Appendix P.22](witnessed_difference_programme.md#p22-exact-topology-and-coherence-thresholds-for-paired-count-guards)
classifies the full legal schedule complex for paired removals and additions
on one count key. For `1 <= c < n`, it has the homotopy type of the real
no-`(c+1)`-equal arrangement complement; at `c = n-1` it is a sphere.
The [complete proof](docs/guarded_schedule_topology.md) and
[verification record](docs/guarded_schedule_topology_verification.md) separate
the written topological theorem, 37 new Lean theorems and bounded executable
checks. General guards and question-preserving execution quotients remain open.

[Appendix P.23](witnessed_difference_programme.md#p23-sparse-integral-transport-and-polynomial-bounds-at-fixed-degree)
constructs explicit integral maps with `p i = id` and
`i p - id = d H + H d`. Its
[minimum-sweep construction](docs/sparse_guarded_chain_transport.md) evaluates
sparse inputs without enumerating the execution complex, with polynomial
computation and certificate-size bounds at fixed degree. The earlier
first-descent version is retained separately. Reconstructed fillings have an
independent local boundary checker; no empirical search speedup is claimed.

## Reproduce checks

Two reproduction profiles are supported, reflecting the clean separation between standalone Python/Lean logic and surrounding-repository native solver acceleration:

### Profile A: Standalone Archive-Only Replay (Pure Python & Core Lean)
This profile reproduces from a clean archive extraction without access to the developer's surrounding checkout:
- **Environment:** Python 3.12 with `dev` dependencies in `pyproject.toml`, and Lean 4.33.1.
- **Python Execution:** Pure Python observation, linear algebra, and quantum mechanics suites execute in standalone mode. When native binaries are absent, functional evaluators gracefully refuse with typed status `NO_RULE` (never falsely claiming certificate rejection or crashing).
- **Core Lean Replay:** Standalone core-only spine verification:
  ```sh
  python scripts/verify_finite_derivations.py --lean /path/to/lean-4.33.1/bin/lean
  python scripts/freeze_current_evidence.py --check
  python scripts/verify_release.py --check
  ```

### Profile B: Selected Native and Surrounding Repository Checks
This profile builds the native exact-functionals adapter and exercises selected
observation, recovery and image-completion paths. It is not a full-suite replay:
- **Environment:** Requires checkout within the surrounding repository workspace due to path dependencies in `code/rust/Cargo.toml` (`omega_functional` and `omega_solvers` located in `omega_engine/crates_rs/`).
- **Build & Execution:**
  ```sh
  cargo build --manifest-path code/rust/Cargo.toml --bins
  export WDP_FUNCTIONALS_BIN="$PWD/code/rust/target/debug/evaluate_wdp_functionals"
  python -m pytest -q -o addopts= code/unit_tests/test_finite_observation.py code/unit_tests/test_calibrated_recovery.py code/unit_tests/test_joint_recovery.py
  python -m pytest -q -o addopts= code/tests/test_distinct_image_completion.py
  python scripts/regen_sha256sums.py --check
  ```

The three observation/recovery files above passed 115 cases in the selected
2026-10-13 Python 3.12.14 replay. That receipt is independent of the native
build and of other test files; it does not certify all adapter paths.

If `CARGO_TARGET_DIR` is set, use its binary directory instead. The native
adapter checks exact rational input, source-bound certificates and zero
authority. CODA's use cases inject this adapter into the domain; direct Layer 1
calls must supply an evaluator explicitly. This is trusted operator
configuration, like the authority keyring; proposal data cannot select it.
The seal does not protect against code running inside the same interpreter.
A missing or unbuilt executable produces a typed refusal (`NO_RULE`), not a
mathematical refutation (`CERTIFICATE_MISMATCH`).
The process is checked against the caller's wall-clock budget while running;
its simplex pivot limit is a separate bound.

The source inventory at base revision `096551f4f` contains 102 Lean files
under `lean4/`, including 100 modules. The dated 2026-10-08 standalone audit
covers 50 core-only modules and 691 selected declaration reports; later scoped
audits remain separate. Appendix D.1 distinguishes these quantities from the
29 exact canonical theorem bindings and from successful paired replays. It does not cover the full Mathlib package. A stored axiom report does not establish a fresh build
of the full package. `manifests/coverage.json` is a partial historical
report, not evidence of 95% current coverage. The withdrawn generated swarm
receipt is retained only in the source archive.

The [review report](docs/review_20261008.md) records the corrections, verification
scope and the earlier proposal now treated in Appendix X.

## Scope and next question

The conditional quantum constructions start from declared scalar, tensor,
positivity and readout assumptions. They do not select quantum theory from
all surviving models. The question-preserving encoding experiment retains a
direct-checker baseline and demonstrates no cochain efficiency advantage.

[Appendix X](witnessed_difference_programme.md#appendix-x--calibrated-reports-finite-recovery-and-observation-cost) supplies a finite reduction of calibrated interval reports,
a sound recovery-or-abstention checker, and robust observation-cost bounds.
Exact cost claims require full report realizability; outer error bounds alone
supply conservative guarantees. A shared-noise example shows why this distinction
is necessary. Units and error radii must be transported together.

[Reproduction instructions](code/calibrated_recovery/README.md) cover the exact
finite certificates, parser controls and six core Lean lemmas. Physical
calibration and source authentication remain supplied premises.

[Appendix Y](witnessed_difference_programme.md#appendix-y--exact-recovery-costs-from-joint-report-supports) retains correlated errors through explicit joint supports. It derives
fixed and adaptive costs, establishes the existence of finite cost witnesses,
and constructs such witnesses for finite unions of rational affine segments.
The [joint-support reference](code/joint_recovery/README.md) reuses the existing
cost checker. Its shared-error example has exact cost 2; its marginal product
enclosure has infinite cost. These new proofs are written, not Lean formalizations.

The next proposed target is a finite reduction for affine supports thickened
by bounded independent measurement error. One reading then leaves a range of
latent parameters, so Appendix Y's finite-fiber argument needs a replacement.
That derivation has not been started.

## Licenses and provenance

Paper, figures and documentation: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Python, Lean and release tooling: Apache 2.0. The packaged Rust crate declares
PolyForm Noncommercial 1.0.0; see [its license](code/rust/LICENSE).
Retained sources preserve their original notices and are subject to the
[current errata](docs/source_errata_20261008.md).

The earlier published v0.5.0 deposit is [10.5281/zenodo.23114399](https://doi.org/10.5281/zenodo.23114399),
in the [version family](https://doi.org/10.5281/zenodo.22880466). This correction
has no assigned version DOI and has not been republished by these edits.


## Witnessed reasoning edition, 2026-10-16

The [inference calculus](docs/derivations/witnessed_reasoning_calculus.md)
connects an explicitly admitted distinction regime to sound Horn inference,
original graph-path witnesses, conservative learned facts and report-based
limits. §14.8 now states the actual target-separating collision hypothesis.
See the [supplementary claim ledger](witnessed_difference_programme_claim_ledger.md#reasoning-supplement-2026-10-16)
and [verification receipt](manifests/witnessed_reasoning_verification.json).
General source refinement, dynamics, physical reconstruction and institutional
interpretation remain open in the reconciled planner. This is not a claim that
every derivation in the research programme has been completed or published.
