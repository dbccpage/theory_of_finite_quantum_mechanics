# Reproducing the 2026-09-22 MUB6 audit

AuthorityEffect: None.

`stated region only; mints no authority`

The deliverable is the [five-part report](C:/Users/a343o/source/repos/MUB6/research/audit_2026_09_22/report.md). Its baseline is `a4ae32f2201a92330c2a237490a545c6c7cee35d`, which matched freshly fetched `origin/main`. No production source patch has been applied. All generated attack inputs, build output, compiled objects and transcripts belong in ignored scratch/cache directories.

| File | Role |
|---|---|
| [reproduce.py](C:/Users/a343o/source/repos/MUB6/research/audit_2026_09_22/reproduce.py) | Hash receipts, exercise malicious metadata/claims, expand polynomial identities with exact coefficients, demonstrate B1 gaps, inventory source files and numeric review sites. |
| [GluingProbes.lean](C:/Users/a343o/source/repos/MUB6/research/audit_2026_09_22/GluingProbes.lean) | Kernel-checked witnesses for weak cover predicates, circular input evidence, denominator omission and identity transport on the canonical triangle. |
| [MathlibProbes.lean](C:/Users/a343o/source/repos/MUB6/research/audit_2026_09_22/MathlibProbes.lean) | Hash collision theorems, executable substituted-source attacks, classification and pilot theorem inspection. The substituted-source checks are `#eval` observations, not reflection theorems. |
| [rust_probes.rs](C:/Users/a343o/source/repos/MUB6/research/audit_2026_09_22/rust_probes.rs) | Reproduce false Krawczyk exclusion, ignored capacity, caught arithmetic panic, and empty-scan success using the original crate. |
| [prepare_checks.py](C:/Users/a343o/source/repos/MUB6/research/audit_2026_09_22/prepare_checks.py) | Generate scratch-only declaration queries and a standalone Rust probe crate. |
| [propose_fixes.py](C:/Users/a343o/source/repos/MUB6/research/audit_2026_09_22/propose_fixes.py) | Generate exact baseline diffs and patched scratch copies. Refuses changed replacement sites. |
| [proposed_fixes.patch](C:/Users/a343o/source/repos/MUB6/research/audit_2026_09_22/proposed_fixes.patch) | Reviewable seven-file containment patch. It does not complete missing mathematical bridges or every public-input/overflow repair. |
| [check_proposed_fixes.py](C:/Users/a343o/source/repos/MUB6/research/audit_2026_09_22/check_proposed_fixes.py), [patched_rust_checks.rs](C:/Users/a343o/source/repos/MUB6/research/audit_2026_09_22/patched_rust_checks.rs) | Focused negative and positive controls against isolated proposed changes. |

Use Python 3.11 or newer. On this host the successful run used bundled Python 3.12.14, `uv` for the temporary pytest dependencies, and the pinned Lean toolchains. Run the following from `C:\Users\a343o\source\repos\MUB6`, adapting executable paths on another host:

```powershell
$auditPython = 'C:/Users/a343o/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$auditLake = 'C:/Users/a343o/.elan/bin/lake.exe'
$auditCargo = 'C:/Users/a343o/.cargo/bin/cargo.exe'
& $auditPython research/audit_2026_09_22/reproduce.py
& $auditPython research/audit_2026_09_22/propose_fixes.py
& $auditPython research/audit_2026_09_22/prepare_checks.py
git apply --check research/audit_2026_09_22/proposed_fixes.patch
& $auditPython research/audit_2026_09_22/check_proposed_fixes.py
& $auditCargo run --manifest-path scratch/audit_2026_09_22/rust_probe/Cargo.toml --bin baseline --target-dir omega_engine/crates_rs/target --offline
& $auditCargo run --manifest-path scratch/audit_2026_09_22/rust_probe/Cargo.toml --bin patched --target-dir omega_engine/crates_rs/target --offline
```

The baseline Rust program catches the expected overflow panic; a printed panic message followed by the audit result and exit code zero is intentional. Do not reinterpret that message as a successful production error return. The patched program expects an explicit `ArithmeticOverflow` result instead. Release-mode behavior was not tested.

Run in `lean4/gluing`:

```powershell
& $auditLake build
& $auditLake env lean ../../research/audit_2026_09_22/GluingProbes.lean
& $auditLake env lean ../../scratch/audit_2026_09_22/gluing_axioms.lean
```

Run in `lean4/012_mutually_unbiased_bases`:

```powershell
& $auditLake build
& $auditLake env lean ../../research/audit_2026_09_22/MathlibProbes.lean
& $auditLake env lean ../../scratch/audit_2026_09_22/mathlib_axioms.lean
& $auditLake env lean ../../scratch/audit_2026_09_22/proposed_pilot_probes.lean
```

The dependency-query generator selects plain top-level `theorem`/`lemma` declaration lines in the fourteen focal modules. This produced 158 gluing and 73 Mathlib queries, covering the requested synthesis results. It is not an enumeration of every declaration imported by Mathlib. Each `#print axioms` query reports that declaration's transitive axiom dependencies.

The patched pilot output should include its original positive control `true`, original corruption controls `false`, two final substituted-source controls `false`, and no compilation error or `sorryAx`. The baseline pilot audit should show two substituted-source evaluations `true` and standard-only dependency lists. This checks the pilot API's source binding; it does not supply generic checker soundness.

Baseline Python test command from the repository root:

```powershell
& C:/Users/a343o/.local/bin/uv.exe run --cache-dir scratch/audit_2026_09_22/uv_cache --python $auditPython --with pytest --with pytest-xdist python -m pytest tests/mub_verify -n 8 --basetemp=scratch/audit_2026_09_22/pytest_tmp -o cache_dir=scratch/audit_2026_09_22/pytest_cache
```

Use a new basetemp name when reproducing beside another run. The result here was 504 passed / 1 skipped; the skip was optional PyTorch availability, not a mathematical gate. Tests that write canonical receipts can change filesystem timestamps or Windows line endings; compare canonical contents with the pinned baseline before restoring anything.

Baseline Rust test command, run in `omega_engine/crates_rs`:

```powershell
& $auditCargo test -p omega_mub --offline --test test_target_a10_global_cover --test test_target_a11_orbit_exhaustiveness --test test_target_a12_smale_sentry --test test_target_a13_grand_synthesis --test test_target_b1_continuous_chaining --test test_target_b2_global_gluing --test test_target_b3_manifold_integration --test test_adversarial_l1_solver
```

The eight binaries passed 14, 11, 18, 13, 8, 14, 15 and 16 tests respectively, total 109. The full Cargo workspace suite and long `deep_run` jobs were not run. The proposed patch was tested with the focused probes, not that entire baseline suite; the stricter B1 and governor semantics intentionally change some existing expectations.

Recorded evidence is under [scratch/audit_2026_09_22](C:/Users/a343o/source/repos/MUB6/scratch/audit_2026_09_22): `probe_results.json`, `source_hashes.json` (545 files), `static_scan.json`, the two baseline build logs, the two axiom-query logs, `gluing_probes.log`, `mathlib_probes.log`, `rust_probes.log`, and the proposed-patch logs. The broad numeric scan is a review-site inventory; many hits are heuristic scoring, diagnostics, timing, or deliberate rejection controls. Do not count them as established certifier violations.
