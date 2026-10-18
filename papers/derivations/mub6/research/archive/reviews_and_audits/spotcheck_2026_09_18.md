# Random code and Lean spot check, 2026-09-18

AuthorityEffect: None.

`stated region only; mints no authority`

## Sample and custody

The checkout was clean at baseline
`11415b48271946743997462a3dc199f3420cccfd`. No branch change, commit, push, or
artifact regeneration was part of this review.

Random seed: **121648733**, drawn once before reading the sample. Within each
stratum, rank tracked candidate paths by
`SHA256(UTF8(decimal_seed + LF + repository_relative_path))`, ascending, and take
the first requested count. This is a stratified sample, not a uniform draw across
the whole repository. Reproduce the candidate lists from the baseline commit.

| Stratum | Candidate population at baseline | Draw |
|---|---|---|
| Python verifier | `omega_engine/crates/mub_verify/*.py`, excluding `__init__.py`: 7 | 3 |
| Rust MUB source | `omega_engine/crates_rs/omega_mub/src/*.rs`, including descendant directories: 95 | 2 |
| Gluing Lean | `lean4/gluing/*.lean`: 18 | 3 |
| Mathlib-backed MUB Lean | `lean4/012_mutually_unbiased_bases/MUB/*.lean`: 38 | 2 |

Supporting imports, tests, manifests, and claim documents were read to interpret
this sample. They were not a second random sample or an exhaustive audit.

## Ten sampled files and outcomes

Paths below are relative to the repository root.

| Sampled file | Finding / correction |
|---|---|
| `omega_engine/crates/mub_verify/interval.py` | Reject floats, booleans, and text endpoints instead of silently converting them; reject dimension mismatch in overlap checks. |
| `omega_engine/crates/mub_verify/verifier.py` | Honor explicit chunk selections, accurately name the default wide-cell replay, preserve empty strata, reject empty successful audits, report seeds without samples, fail on a missing requested receipt, and reject negative neighborhood radii. |
| `omega_engine/crates/mub_verify/cover.py` | Use relative volume/interiors on non-fixed coordinates; check overlaps beyond 200 leaves; reject wrong dimensions; retain counts when leaf storage is disabled. Success now explicitly concerns geometry, not the correctness of leaf labels. |
| `omega_engine/crates_rs/omega_mub/src/bin/mub_tao_cover.rs` | Reject malformed/missing numeric values, empty/out-of-range/overflowing chunk ranges, and conflicting modes. Honor an explicit wide-cell depth. Return nonzero for incomplete covers. |
| `omega_engine/crates_rs/omega_mub/src/omega_native/odd_prime_power_field_theorem_gate.rs` | A supplied failed schema now prevents acceptance. Remove unconditional claims that Lean theorems were checked; retain scope restrictions even in an accepted report. The Boolean theorem flags remain explicit declarations, not a kernel replay. |
| `lean4/gluing/Gluing.lean` | Correct documentation that conflated vector and basis extension, and note that G3 is supplied by `g3_theorem` while G1/G2 remain hypotheses. The assembly logic was retained. |
| `lean4/gluing/DeltoidCuspGluing.lean` | Replace a bare `Prop` membership field with evidence for a caller-supplied cusp relation. Correct documentation to distinguish recorded fraction arithmetic from the still-required analytic curvature bound. |
| `lean4/gluing/AlgebraicCornerReconstruction.lean` | Replace addition of off-diagonal phase labels with a signed integer difference; rename the purported root-of-unity constraint as a remainder-bound theorem. Identify constructor case splits, label predicates, and orbit-map assumptions accurately. A concrete complex interpretation remains absent. |
| `lean4/012_mutually_unbiased_bases/MUB/ComplexCoefficientScalars.lean` | No defect identified in this sample. The module explicitly limits itself to a complex scalar package, with coefficient-field construction still separate. Build and printed axiom checks passed. |
| `lean4/012_mutually_unbiased_bases/MUB/HilbertPhaseNormalization.lean` | No defect identified in this sample. Read the normalization identities and their finite-field/nonzero hypotheses; build and printed axiom checks passed. |

The corner API now exposes `crossRatioIndex` and `cross_ratio_residue_bounds`
instead of `crossRatioPhase` / `cross_ratio_constrained_to_mu6`. The cusp witness
now has a membership-relation parameter. Repository consumers build; external
callers using the old signatures would need adjustment. `CoverReport` also has
two optional total-count fields; consumers destructuring its tuple must account
for them. Named field access is retained.

## Verification receipts

| Check | Observed result |
|---|---|
| Baseline Python suite | 38 passed. |
| New interval/coverage regressions against the original implementation | 10 failed, 9 passed; failures reproduce the acceptance defects. |
| Final `tests/mub_verify` suite | **58 passed**, eight workers, Python 3.12.14. |
| Rust field-theorem gate module | **4 passed**, including a mixed successful/failed sample regression. |
| Rust Tao CLI unit tests | **2 passed**. |
| Built CLI subprocess checks | **6 passed**: missing/invalid numeric arguments, orphan end flag, empty chunk range, depth-zero incomplete wide cover, and help. |
| Gluing package | `lake build` completed, **37 jobs**, pinned Lean 4.34.0. This is build success, not a package-wide trust clearance. |
| Two sampled Mathlib-backed modules | Both targets built with their dependency graph, pinned Lean 4.33.1. Printed sampled theorem axioms were within the standard set. |
| Lean regression probe | Negative signed cross-ratio index, cancellation for constant labels, and inability to supply a cusp witness for the always-false relation all elaborated. |
| Skill validation and installation | Source and installed `mub6-manager` passed `quick_validate.py`; SHA-256 matched for all three installed files. Display name: `mub6_manager`; invocation: `$mub6-manager`. |
| Sample and patch hygiene | Replaying the recorded draw selected the same ten paths; `git diff --check` passed. No tracked scratch, cache, or build outputs were added. |

Commands, run from their respective package roots:

```text
python -m pytest tests/mub_verify -n 8 --basetemp=scratch/spotcheck-20260918/pytest-final -o cache_dir=scratch/spotcheck-20260918/pytest-cache
cargo test -p omega_mub --lib omega_native::odd_prime_power_field_theorem_gate::tests --offline
cargo test -p omega_mub --bin mub_tao_cover --offline
cargo build -p omega_mub --bin mub_tao_cover --offline
lake build
lake build MUB.ComplexCoefficientScalars MUB.HilbertPhaseNormalization
```

The shell had no usable `python` command. Python execution used the bundled
Python 3.12.14 interpreter through `uv run --no-project --with pytest --with
pytest-xdist`, with `UV_CACHE_DIR` inside `scratch/`. The prescribed shared
`scratch/pytest_tmp` was inaccessible to pytest's cleanup, so a fresh run-specific
basetemp was used. The shared pytest cache was also inaccessible; the final run
used the run-local cache above. Existing caches were not removed or repermissioned.

Raw logs, the sample JSON, CLI subprocess receipt, and temporary Lean probe are
ignored under `scratch/spotcheck-20260918/`. The review report is the maintained
summary, not a mathematical cover certificate. Existing published receipts were
not regenerated or re-certified by this work.

## Remaining trust and semantic gaps

The source scan found **18 existing custom axiom declarations** in
[`G1_Orbits.lean`](../lean4/gluing/G1_Orbits.lean) (13) and
[`GlobalGaugeChaining.lean`](../lean4/gluing/GlobalGaugeChaining.lean) (5).
The current build prints three nonstandard dependencies for
`GlobalGaugeChaining.non_dita_count_le_one`: `at_most_one_szollosi_basis`,
`at_most_one_tao_basis`, and `tao_szollosi_cross_empty`. The package therefore does
not meet the repository's stated standard-axiom-only requirement as a whole.
These were not discharged by renaming them or substituting new assumptions.

The sampled corner and cusp modules remain conditional interfaces. Their
repaired documentation does not supply concrete matrix semantics, finite-fiber
reconstruction, or analytic neighborhood bounds. The exact pair positivity
check in `KernelReflectionKarlssonVolume.karlsson_volume_pairs_all_pos_verified`
also does not construct its `KarlssonVolumeCoverCertificate.bound_certified`
field. Broad historical campaign summaries need a separate claim-by-claim audit.

This ten-file spot check found and repaired bounded implementation and interface
defects. It does not establish correctness of all engines, all receipts, the
external classification formalization, or an exhaustive MUB(6) theory.

The next five derivation targets are in
[next_derivations_2026_09_18.md](next_derivations_2026_09_18.md). The reusable
[mub6_manager skill](../skills/mub6-manager/SKILL.md) keeps these distinctions and
an initial evidence-backed lesson log.
