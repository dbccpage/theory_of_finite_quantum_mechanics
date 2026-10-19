# Original User Request

## Initial Request — 2026-10-18T17:07:43Z

Use a very large team of agents. Review the three newly added core paper packages (`papers/core/mub6`, `papers/core/fsp`, and `papers/core/majorana`), migrate their library Python code into `code/python/src`, and ensure that every derivation, theorem, algorithm, and functionality described in the three papers is fully implemented and verified across Python (`code/python/src`), Rust (`code/rust/src`), and Lean 4 (`lean4/`).

Working directory: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics
Integrity mode: development

## Reference Material & Verification Resources

- **Core Paper Packages:**
  - `papers/core/mub6/` (`mub6.md`, `theory_of_finite_mub6.md`, `mub6_claim_ledger.yaml`, `verify_deposit.py`, `lean4/`, `rust/`, `code/`, `scripts/`, `tests/`)
  - `papers/core/fsp/` (`the_problem_of_the_fermion_sign.md`, `fermion_sign_problem.md`, `claim_ledger.yaml`, `verify_deposit.py`, `000_meron_sign_problem/`, `001_hubbard_sign_problem/`, `normal_forms/`, `lean4/`, `code/`)
  - `papers/core/majorana/` (`the_majorana_problem.md`, `claim_ledger.yaml`, `verify_deposit.py`, `lean4/`, `code/`, `contracts/`)
- **Canonical Target Trees:**
  - Python source: `code/python/src/` (`mub/`, `fsp/`, `majorana/`, and shared domain packages) and tests in `code/python/tests/` (including `code/python/tests/test_dual_face_majorana_mub_fsp.py`)
  - Rust workspace/crate: `code/rust/` (`code/rust/Cargo.toml`, `code/rust/src/mub/`, `code/rust/src/majorana/`, and `fsp` modules)
  - Lean 4 root project: `lean4/` (`lean4/lakefile.lean`, flat `.lean` module structure)
- **Existing Verification Runners:**
  - `pytest` (configured via root `pyproject.toml`)
  - `cargo test` (in `code/rust/`)
  - `lake build` (in `lean4/`)
  - `verify_deposit.py` (root and per-paper in `papers/core/{mub6,fsp,majorana}/verify_deposit.py`)

## Requirements

### R1. Comprehensive Paper & Derivation Audit (`mub6`, `fsp`, `majorana`)
Review all manuscripts, claim ledgers, companion scripts, and formal files in `papers/core/mub6`, `papers/core/fsp`, and `papers/core/majorana`. Produce a complete inventory of every derivation, theorem, lemma, exact certifier, and computational check stated in the three papers, and identify all gaps across `code/python/src/`, `code/rust/src/`, and `lean4/`. Maintain claim discipline (narrow claims scoped to declared finite/algebraic assumptions; no hype verbs).

### R2. Consolidate Python Code into `code/python/src`
Move reusable Python modules from `papers/core/mub6`, `papers/core/fsp`, and `papers/core/majorana` into `code/python/src/` (under `code/python/src/mub`, `code/python/src/fsp`, `code/python/src/majorana`, or appropriate domain packages), removing duplicate library modules from `papers/core/*`. Update the paper scripts, tests, `sha256sums`/manifests where applicable, and each paper's `verify_deposit.py` so they import directly from `code/python/src/` and continue to pass cleanly.

### R3. Complete Tri-Language Derivations & Functionality (`Python`, `Rust`, `Lean 4`)
Ensure that the full derivations and computational functionality described in `papers/core/mub6`, `papers/core/fsp`, and `papers/core/majorana` exist and are verified in all three target directories:
1. **Python (`code/python/src/`):** Complete exact arithmetic/symbolic/combinatorial derivations and certifiers for all three papers, with comprehensive tests in `code/python/tests/`.
2. **Rust (`code/rust/src/`):** Implement and wire all derivations and certifiers from `mub6`, `fsp`, and `majorana` (including migrating/integrating any standalone `.rs` files in `papers/core/mub6/rust/` and implementing full `fsp`, `mub`, and `majorana` modules in `code/rust/src/`) with unit and integration tests.
3. **Lean 4 (`lean4/`):** Consolidate and complete all Lean 4 formalizations from `papers/core/{mub6,fsp,majorana}/lean4/` and any missing paper theorems into the root `lean4/` directory (`lean4/lakefile.lean`), adhering to a flat module layout with zero `sorry`, zero `admit`, and zero unapproved custom axioms.

## Acceptance Criteria

### Python Migration & Verification
- [ ] Reusable Python library code from `papers/core/mub6`, `papers/core/fsp`, and `papers/core/majorana` resides in `code/python/src/` with duplicate library copies removed from `papers/core/*`.
- [ ] `pytest` passes across `code/python/tests/` and the paper test suites with zero failures.
- [ ] `python papers/core/mub6/verify_deposit.py`, `python papers/core/fsp/verify_deposit.py`, and `python papers/core/majorana/verify_deposit.py` all execute and pass.

### Rust Implementation & Verification
- [ ] `code/rust/src/` contains complete modules covering the derivations and functionality of `mub6`, `fsp`, and `majorana` (all wired into `code/rust/src/lib.rs`).
- [ ] `cargo test` in `code/rust/` compiles cleanly and passes all unit and integration tests with zero failures.

### Lean 4 Formalization & Verification
- [ ] All Lean 4 theorems and derivations for `mub6`, `fsp`, and `majorana` are integrated into root `lean4/` and registered in `lean4/lakefile.lean`.
- [ ] `lake build` in `lean4/` succeeds with exit code 0.
- [ ] Zero `sorry` or `admit` tokens and zero custom `axiom` declarations exist in any of the target `.lean` files.

### Traceability & Claim Hygiene
- [ ] A verification report / traceability matrix maps each derivation/claim across `mub6`, `fsp`, and `majorana` to its exact file and symbol in `code/python/src/`, `code/rust/src/`, and `lean4/`, adhering strictly to the repository's Claim Hygiene rules.

## Follow-up — 2026-10-18T20:27:18Z

Server restart occurred, stopping active subagents and background crons. Please revive your Project Orchestrator (`2f7c2b5c-0caf-47df-b59c-b0d9e7b0ab22`) and resume monitoring until all milestones (M1 Python, M2 Rust, M3 Lean 4, M4 Traceability) and the Victory Audit complete.

Also note two directory updates requested by the user:
1. `lean/DerivationDagQMClosure.lean` has been moved into `lean4/DerivationDagQMClosure.lean` and `lean/` has been deleted.
2. `research/lean4/` has been merged into root `lean4/` and `research/` has been deleted.
Make sure the Orchestrator and Lean 4 worker use root `lean4/` exclusively and do not recreate `lean/` or `research/`.

## Follow-up — 2026-10-18T21:42:05Z

Diagnostic note for the Project Orchestrator (`2f7c2b5c-0caf-47df-b59c-b0d9e7b0ab22`):
`worker_m2_rust` (`36adb1c9-8534-4191-92f4-412d219079a0`) has been waiting on `task-394` (`cargo test -p tfqm_mub --lib` in unoptimized debug mode) for over 67 minutes because a single exhaustive search test (`omega_native::exact::mub6_continuous_manifold_residue::tests::test_solve_continuous_manifold_residue_smoke`, PID 21404) has consumed 3,389s of CPU in debug mode while the other 390+ tests already passed.
Please instruct the Orchestrator to have `worker_m2_rust` kill `task-394`, bound or `--release`-run `test_solve_continuous_manifold_residue_smoke` (or pass `-- --skip test_solve_continuous_manifold_residue_smoke` for debug and run that single test with `--release`), so Milestone M2 can finish immediately instead of hanging in debug mode.

## Follow-up — 2026-10-18T23:02:19Z

Diagnostic update for Project Orchestrator (`2f7c2b5c-0caf-47df-b59c-b0d9e7b0ab22`):
1. `worker_m2_rust` (`36adb1c9-8534-4191-92f4-412d219079a0`) `task-534` has already passed 343/345 tests in `tfqm_mub`, and is only waiting on the 2 tests in `omega_native::exact::char_two_parametric_gate::tests` (`PID 26048`), which are slow in unoptimized debug mode and competing for RAM with Lean 4. Instruct `worker_m2_rust` to kill `task-534` (`PID 26048`), run `cargo test -p tfqm_mub --lib --release char_two_parametric_gate` (which finishes in seconds in release mode), and immediately emit the Milestone M2 completion handoff.
2. `worker_m3_lean` (`5385c5b6-0537-47d9-8119-f831571b79e5`) is at `[1317/1442]` (>91%) compiling `MasterClassification`. Once `PID 26048` is freed, a single retry of `lake build MasterClassification` will finish the remaining cached targets cleanly.

## Follow-up — 2026-10-18T23:34:59Z

Quick tip for `worker_m3_lean4` (`5385c5b6-0537-47d9-8119-f831571b79e5`):
`MasterClassification.lean` only uses `import Mathlib.Analysis.Real.Sqrt` in 4 lines (`tao_omega`, `tao_omega_im`, `tao_omega_sq_im`, `tao_omega_normSq`) for a single constant `s3 : ℝ` with `s3 ^ 2 = 3` and `s3 * s3 = 3`. All 15 other imports in `MasterClassification.lean` (`Mathlib.Data.Complex.Basic`, `ConcreteSemantics`, `PolynomialEncoding`, `CaseCoverage`, `GroebnerBranch`, `CADBranch`, etc.) already succeeded (`OK`).
Instead of debugging `Mathlib.Analysis.Real.Sqrt`'s transitive `.olean` cache on Windows, `worker_m3_lean4` can remove `import Mathlib.Analysis.Real.Sqrt` from `MasterClassification.lean` (and any other file where `Mathlib.Analysis.Real.Sqrt` crashes `lean.exe` on Windows mmap) and define the algebraic root over `ℝ` (or parameterize `sqrt3 : ℝ` with `h_sqrt3 : sqrt3 * sqrt3 = 3`, or use `Classical.choose` on an existential in `ℝ`), which will let `lake build MasterClassification` compile in ~3 seconds with zero `sorry`, zero `admit`, and zero custom axioms!

## Follow-up — 2026-10-19T00:43:42Z

CRITICAL DIAGNOSTIC FINDING FOR MILESTONE M3 (`worker_m3_lean4` / `5385c5b6-0537-47d9-8119-f831571b79e5`, `task-675` `lake build Mub6`):

Root cause identified for why `lake build Mub6` (`task-675`) has been compiling 3,200+ unrelated Mathlib files (CategoryTheory, Matroid, AlgebraicGeometry, etc.) from source:
15 files in `lean4/` imported by `lean4/Mub6.lean` have a broad top-level `import Mathlib` on line 1 instead of targeted Mathlib imports:
1. `lean4/ExtensionCurvatureObstruction.lean`
2. `lean4/BasisExtensionObstruction.lean`
3. `lean4/FiniteBasisCover.lean`
4. `lean4/FiniteVectorCover.lean`
5. `lean4/FixedTuplePsiCertificate.lean`
6. `lean4/KernelReflection1024.lean`
7. `lean4/KernelReflectionGrandUnified.lean`
8. `lean4/KernelReflectionKarlssonVolume.lean`
9. `lean4/KernelReflectionPilot.lean`
10. `lean4/KernelReflectionScaled.lean`
11. `lean4/KernelReflectionSzollosiDeltoid.lean`
12. `lean4/KernelReflectionTaoHaagerup.lean`
13. `lean4/TripleExtensionAssembly.lean`
14. `lean4/TripleGaugeReduction.lean`
15. `lean4/TripleHadamardDephase.lean`

Because `import Mathlib` imports the umbrella `Mathlib.lean` (all ~7,400 files in Mathlib), Lean is compiling the entire Mathlib library from source instead of only the already-built modules!
By contrast, `Mathlib.Analysis.InnerProductSpace.Basic`, `Mathlib.Analysis.SpecialFunctions.Sqrt`, `Mathlib.Topology.Compactness.Compact`, `Mathlib.LinearAlgebra.UnitaryGroup`, `Mathlib.Data.Matrix.Basic`, `Mathlib.Data.Complex.Basic`, `Mathlib.Data.Real.Basic`, `Mathlib.Tactic.Ring`, `Mathlib.Tactic.Linarith`, `Mathlib.Tactic.NormNum`, `Mathlib.Tactic.Positivity`, and `Mathlib.Tactic.FinCases` are ALREADY compiled in `lean4/.lake/packages/mathlib/.lake/build/lib/lean/`!

Please forward this immediately to the Project Orchestrator (`2f7c2b5c-0caf-47df-b59c-b0d9e7b0ab22`) and `worker_m3_lean4` (`5385c5b6-0537-47d9-8119-f831571b79e5`):
If `task-675` is still compiling unrelated Mathlib modules, kill `task-675`, replace `import Mathlib` in those 15 files with targeted Mathlib imports (such as the ones above), and re-run `lake build Mub6` and `lake build` — it will finish in seconds with zero new Mathlib compilations! Also remind the orchestrator/worker to ensure 0 custom `axiom` declarations exist in the target `.lean` files and no duplicate library `.py` files remain in `papers/core/fsp/000_meron_sign_problem/` or `papers/core/fsp/001_hubbard_sign_problem/` before the Victory Audit.
