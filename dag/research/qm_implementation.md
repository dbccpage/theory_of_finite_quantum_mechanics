# Implementation roadmap

**Scope:** Implementation and verification census across the `finite_quantum_mechanics` estate.  
**Target:** `qm_implementation.md`  
**Target:** `qm_implementation.md`  
**Updated:** 2026-10-11  

This document provides a technical census of the computational kernels, compiled Rust crates, Lean 4 formalizations, and test verification suites across the `finite_quantum_mechanics` estate.

## Standing

The computational and formal implementation is organized into three primary verification tiers:
1. **Formal Proofs (Lean 4):** Flat library in `lean4/quantum_mechanics/` verifying algebraic cochains, difference identities, and foundational quantum theorems.
2. **Compiled Rust Crates:** High-performance exact rational solvers and certifiers in `omega_engine/crates_rs/omega_quantum_physics/src/finite_qm/`.
3. **Symbolic & Prototyping Engines (Python):** Modular packages in `omega_engine/crates/finite_qm/` and `omega_engine/code/`.

### Where the live code actually lives

After relocation and facade withdrawal:

- **Python kernels (canonical crate):** `omega_engine/crates/finite_qm/` — `domain/` (4 modules: `cyclotomic_tower.py`, `gaussian_rational.py`, `primitive_difference.py`, `primitives.py`), `use_cases/` (**42** use-case `.py` files plus `__init__.py`), `entrypoints/` (consolidate, C250/C500 verifiers, replay). `omega_engine/crates/finite_qm/__init__.py` warns the Python package is deprecated in favor of workspace Rust / PyO3.
- **Remaining C750/C1000 Python:** `omega_engine/code/` holds C750 (`c750_b01_*` through `c750_b10_synthesis.py`) **and** C1000 kernels (`causal_order.py`, `causal_price_list.py`, `commuting_observables.py`, `contextuality_obstruction.py`, `group_parameter.py`, `lorentz_boost.py`, `no_signalling.py`, `rotation_groups.py`) plus `boost_composition.py`, `quantum_correlation.py`, entropy/cyclotomic helpers, `pytest.ini`, `tests/`, `_paths.py`, `_finite_qm_rs.pyd`. A C750-only census of that directory is incomplete.
- **Tests:** `omega_engine/code/tests/` with `pytest.ini` `testpaths=tests`. `tests/conftest.py` puts repo root and `omega_engine/code` on `sys.path`. Crate kernels import as `omega_engine.crates.finite_qm`; remaining C750/C1000 modules import by bare name.
- **Withdrawn application facades:** legacy `code/` directory is absent. `LOCAL_SOURCE_RELOCATION_SUPERSESSION.json` records status `FACADES_WITHDRAWN_CUSTODY_PRESERVED`, 49 withdrawn facades, destinations unchanged. Callers must import the recorded destination.
- **Rust:** Canonical finite-QM implementations live in `omega_engine/crates_rs/omega_quantum_physics/src/finite_qm/` (continuum, MUB, Gleason, CPTP, dynamics, Weyl, …). `omega_engine/crates_rs/omega_finite_qm` is a backwards-compatible `pub use` facade. `omega_engine/code_rs/src/lib.rs` is `pub use omega_finite_qm::*` plus local C750/C1000 modules and a PyO3 bridge. Cited `omega_engine/code_rs/src/continuum.rs` is absent; exact-rational Wintner–Wielandt is `omega_quantum_physics::finite_qm::continuum`.
- **Lean:** `lean4/quantum_mechanics/` is one flat PascalCase library (toolchain `leanprover/lean4:v4.33.1`). Opened listing: **154 `*.lean` files counting `lakefile.lean`**, plus `lake-manifest.json` / `lean-toolchain`. README still says 122 library modules. Do not write “154 plus lakefile.” `evidence/lake_replay_20260905.json` application row: 152 lean files / 154 jobs. `lakefile.lean` roots `FiniteQm.C750.B01.{Definitions,Reduction,Purity,AxiomCensus}`, but `lean4/quantum_mechanics/FiniteQm/` does not exist. Those four files live only at `campaigns/c750/block_01/lean4/FiniteQm/C750/B01/`.
- **Retained sources:** `sources/` holds verbatim QM_060 and QM_122 only. `coda_atlas/papers` is retired. `research/` holds the source-paper tree. Generated ledgers keep historical origin strings; `consolidate_sources` cannot rebuild without the corpus.
- **Paper layout (§6) is stale:** it still draws legacy `code/` with `consolidate_sources.py`, `cochain.py`, `density_matrix.py`. Live paths are the crate and `omega_engine/code`.

`foundations.py` is an explicit re-export facade over `rungs.py`, `discrete_walk_engines.py`, `advanced_targets.py`, and domain primitives. Paper Rung 1–8 still names `code/foundations.py`.

### What tests actually pin

**Governance and custody (not mathematics).**

- `test_c500_execution.py`: live verifier `omega_engine/crates/finite_qm/entrypoints/c500_verify_execution.py` reports `open_targets == 250`, `launch_preconditions == "NOT_ESTABLISHED"`, `campaign_target_execution_certified is False`. Mutations that promote a target, fake a HIT, or mark launch `VERIFIED` must raise even after rehashing the replay manifest.
- `test_c500_campaign.py`: planning tree verifies `PLAN_VERIFIED_NOT_EXECUTED`, 250 targets, 10 plans, 11 bets; rejects `execution_status == "COMPLETE"`.
- `test_c750_execution.py::test_b10_synthesis_and_adjudication`: `adjudicate_fqmi1_clauses()` is 10 clauses, **8 DISCHARGED / 2 OPEN** (clauses 8 signed cancellation, 9 sign-decision growth law). That is the live FQMI-1 pin, matching `campaigns/c750/block_10/result.json` terminal `FQMI1_OPEN_INTERNAL_GAPS` and `C750_FQMI1_CLOSURE.md`. It does not match `campaigns/c750/README.md` (`Execution state: NOT_STARTED`) even though `sealed_targets.json` says `EXECUTED`.
- `test_causal_price_list.py`: `select_campaign_terminal(...) == "FQMR1_CLOSED_AT_DECLARED_CLASS"`. `campaigns/c1000/block_10/result.json` and `C1000_FQMR1_CLOSURE.md` repeat that string. `campaigns/c1000/README.md` and `sealed_targets.json` still have `execution_status: NOT_STARTED` and `independence_established: false`. Conflicting receipts are not an FQMR-1 admission.
- `test_cptp_channels_stinespring.py`: **pins** `choi_theorem_ported_lean is False` and depolarizing p=1/7 dilation conductor 28. That is an honesty pin, not a Choi theorem.
- `test_lean_replay.py`: application Lean is one flat PascalCase directory with no subdirectories (`application_lean_replay.validate_layout`); zero `: True := by trivial`; no `sorry`. Receipt source-byte hashes must still match. C750 B01 modules are therefore **outside** the application library the replay validator will accept.
- `test_mub_source_snapshot.py` points at `omega_engine/crates_rs/omega_finite_qm/src/mub`. That directory is absent. `SOURCE_SNAPSHOT.json` lives at `omega_engine/crates_rs/omega_quantum_physics/src/finite_qm/mub/` with status `UNINTEGRATED_SOURCE_SNAPSHOT`. The test as written cannot bind the live snapshot without a path repair.
- `test_withdrawn_rows.py` pins the 31 audit-refuted packaging repairs against `sources/atlas/papers/quantum_foundations`, and **skips** when that tree is gone. After F004 retirement the withdrawal pins do not currently fire against `research/`.
- `test_gap_register.py` validates only `gaps:` types in `{open_bridge, continuum_interface, evidence_vacuum, triage_required, missing_implementation, false_receipt}`. YAML-nested `GAP-C1000-*` (`declared_assumption` / `proved_theorem` / `open_question`) are not in that list and would be rejected if moved into `gaps:`.

**Finite computation, not uniqueness.**

- `cochain.py`: `d1 d0 = 0`, `Phi_1` via scipy HiGHS LP with `TOL = 1e-9`, 3-way trichotomy (`ExactClass` / `ClosedResidual` / `ActiveClosureFailure`). Docstring: not an exact solver; no Refusal class. Paper §4 calling `Phi_1` an exact LP is stronger than this kernel.
- `rungs.py`: `verify_gleason_frame_additivity` checks `v†ρv` sums to 1 on **supplied numpy frames**. `gleason_dimension_2_counterexample` samples **six float angles**. `BoundaryDefense` sets `gleason_applies=(dimension >= 3)` and claims Rungs 1–7 close in discrete dimension — that overclaims relative to paper §9 and gaps 004/010.
- `density_matrix.py`: `is_valid_density_matrix` uses `numpy.linalg.eigvalsh` (float); `measure_and_update` is float `P ρ P / p`.
- `continuum_lift.py`: Wintner–Wielandt demo with numpy random matrices and `1e-12` tolerances. Exact-rational Rust is `continuum.rs` (`is_obstructed: true` hardcoded after an exact trace computation on a constructed pair). `H056ContinuumLiftBoundary.lean` is 2×2 Int matrices only. `evidence/continuum_lift_boundary.json` is `HISTORICAL_NOT_A_CURRENT_PROOF_RECEIPT`.
- `composition_tensor_mub.py`: `search_fourth_mub_d6(..., max_candidates=1000)` always returns `status: "OPEN"`.
- `born_gleason.rs`: `ConditionalUniqueness.try_prove` is a paid-assumption plus frame==Born-populations check, not a Gleason theorem.
- Domain `primitives.py`: Pauli/Hadamard as numpy complex; `trace_norm` is SVD float.

**Lean candidates, not admissions.** `DualWitness.lean` proves `|w·d| ≤ |d0|+|d1|` for coefficients in `{-1,0,1}` and `mermin_peres_parity_obstruction` (combinatorial sign-parity). GAP-F001-S000-001: a compiling Lean file is a candidate mirror, not a QM_080 duality certificate. `GleasonTheorem.lean` is integer quadratic frame-sum identities and a d=2 binary obstruction. `H058EffectFrameBusch.lean` header: no `RationalHomogeneityWitness2` constructor for every effect; squeeze may take `r=s=λ` over `Rat`; uniqueness assumes matching test-coordinate equations. `H063CptpChannelsStinespring.lean` checks nonnegative Choi diagonals and stored conductors; `choi_theorem_ported_lean=false`. `H017Finish.lean`: `gleasonUniqueness` and `cptp` remain `FinishFate.imported`. `FiniteDensity.lean` is a 2-state Nat diagonal spectrum. `H073ContinuousTimeLocalityLimit.lean` proves `2n` and `12 n^2` denominators strictly increase; it does not prove Trotter convergence or Lieb–Robinson. C750 `Reduction.lean` stores `BakerHypothesis` as a cited structure, not a proof of Baker 1975. EntropyDichotomy is a Mathlib-capable candidate in the application lake, not an admission of mixed-state von Neumann entropy as a carrier quantity.

### What was withdrawn

- **PR #205** (`evidence/PR205_REVIEW.md`; paper §9): complete-derivation / minimal-carrier / all-HIT claims. Historical 010 `REFUSED-DERIVABLE` / necessity-of-continuum reading withdrawn. Topology, p-adic, and nonstandard flags that lacked implementations are now explicitly unknown. Rust's six unconstructed higher triads withdrawn; four rational triads remain.
- **C250 completion interpretations:** superseded by `evidence/REVIEW_C250_20260907.md`. Remaining campaign files: `INSTRUCTIONS.md`, `sealed_targets.json`, `block_01.md`; `campaigns/c250/tools/` is empty. REVIEW_C250 still tells the reader to run `replay_review.py` there.
- **C500 published completion** at commit `b1b749a9c8fb1e61492673c251deb791ff2501a9`: withdrawn by `campaigns/c500_execution/WITHDRAWAL.md`. All 250 original targets stay OPEN in block reviews and in live tests. `C500_FQMC1_CLOSURE.md` naming twelve gaps `RESOLVED` / scoped FQMC-1 closure does **not** flip `test_c500_execution.py`.
- **49 legacy `code/*` facades** deleted; custody via git blob ids in the supersession record. C500 `replay_manifest.json` still lists withdrawn `code/` paths; `replay_manifest_supersession.json` preserves those digests without restoring files.
- **Central Lean scaffold** of `theorem X : True := by trivial` deleted 2026-09-05. Deleting placeholders did not promote any claim.
- **31 REFUTED BY AUDIT rows** withdrawn in place across eleven packages. That is packaging honesty, not a mathematical change.
- **Paper banner:** C250 review supersedes campaign completion interpretations; C500 withdrawal supersedes published completion and all-HIT assertions.

### Campaign standing, in one table

| Campaign | Live tests / kernels pin | Seals / README still say | Certification docs say | Honest terminal |
| --- | --- | --- | --- | --- |
| C250 | finite models, conditional proofs, counterexamples (REVIEW_C250) | tools/ empty; historical seals remain | completion interpretations superseded | not a complete derivation |
| C500 | 250 OPEN; launch NOT_ESTABLISHED; PLAN_VERIFIED_NOT_EXECUTED | planning `execution_status: NOT_STARTED` | `C500_FQMC1_CLOSURE.md` scoped RESOLVED | original launch contract OPEN; `FQMC1_OPEN_INTERNAL_GAPS` in block_10 |
| C750 | 8 DISCHARGED / 2 OPEN (clauses 8–9) | README `NOT_STARTED`; seals `EXECUTED` | `FQMI1_OPEN_INTERNAL_GAPS` | FQMI-1 not closed |
| C1000 | terminal selector `FQMR1_CLOSED_AT_DECLARED_CLASS` | README + seals `NOT_STARTED`, `independence_established: false` | `FQMR1_CLOSED_AT_DECLARED_CLASS` | conflicting receipts; GAP-C1000-010 type `open_question` |

Naming a certification file does not discharge a launch contract the live tests still keep open.

### What still has to exist for the paper's honest standing

The paper's honest standing is **scoped finite computation + candidate Lean + named gaps**. Implementation work that would support that standing, without pretending the programme closed:

1. Path and receipt hygiene so cited files exist at the cited paths (register, paper §6, MUB snapshot test, C750 Lake roots, C750/C1000 README vs seals).
2. Exact (zero-float or certified-enclosure) replacements wherever prose says "exact" and the kernel is numpy/HiGHS/float (`Phi_1`, density PSD, Gleason frames, Wintner–Wielandt Python, Mermin–Peres `allclose`).
3. The named source-paper algorithms still missing as implementations: QM_005 `V_Q` packet verifier, four-way classifier including Refusal, QM_006 descent audit, QM_002 cofiber-to-Banach bridge (`GAP-FQM-003`). `cochain.py`'s 3-way numerical trichotomy is not those objects. Register prose "`code/` holds only five kernel routines" is false against 42 crate use-cases plus C750/C1000 modules.
4. Duality, Busch uniqueness, and projection Gleason as typed theorems or typed counterexamples on declared carriers — or explicit remaining-bridge labels that match the Lean headers, not YAML overclaim (`busch_effect_frame_resolution` vs H058).
5. Application Lake actually building the C750 B01 modules it roots, **or** dropping those roots so `validate_layout` and `lakefile.lean` describe the same tree.
6. Mathlib snapshot `lean4/original_lean_20260809` replayed or the eight UNREPLAYED rows and SRC-081–083 channel theorems re-stated against in-tree files (`GAP-FQM-019`). That directory is absent.
7. Campaign receipt reconciliation so a reader cannot cite `FQMR1_CLOSED` against seals that still forbid execution, or `FQMC-1 closed` against tests that assert 250 OPEN.

Priced continuum interfaces are **not** items on this list. They are not closable inside the finite programme.

## Gaps

Estimates below are operator judgment. Priced-continuum items are marked **not closable inside the finite programme**.

### GAP-C500-B01 — C500 original 250-target launch contract remains OPEN

- **Closable:** no, for the original launch contract (a relaunch under a new freeze is a different contract).
- **Why open:** Live `test_c500_execution.py` asserts 250 OPEN targets and `launch_preconditions NOT_ESTABLISHED`. Register status is `RESOLVED_WITH_SCOPED_EVIDENCE` while titles keep original targets `C500-T301`–`T325` (and B02–B10 analogously T326–T550) as `unresolved_targets`. WITHDRAWAL.md and `c500_execution/block_10/result.json` keep `FQMC1_OPEN_INTERNAL_GAPS`. `C500_FQMC1_CLOSURE.md` does not change those tests.
- **What tests pin:** mutation gates against promoting frozen OPEN obligations; planning tree `PLAN_VERIFIED_NOT_EXECUTED`.
- **What they do not pin:** FQMC-1 closure, Hamiltonian evolution, or launch custody that was never established prospectively.

### GAP-C1000-010 — FQMR-1 named closed in tests while seals still say NOT_STARTED

- **Closable:** yes as hygiene; that hygiene is not a spacetime theorem.
- **Why open:** `test_causal_price_list.py` and block_10 / `C1000_FQMR1_CLOSURE.md` name `FQMR1_CLOSED_AT_DECLARED_CLASS`. `campaigns/c1000/sealed_targets.json` has `execution_status: NOT_STARTED` and `independence_established: false`; README matches. Register type is `open_question` (YAML-nested, not in `gaps:`). Conflicting receipts do not close FQMR-1.

### GAP-FQM-003 — named source-paper algorithms still missing; register prose is stale

- **Closable:** conditional. Register still says legacy `code/` holds only five kernel routines. Live tree has 42 crate use-cases plus C750/C1000 modules under `omega_engine/code`. That prose is false. The named objects (QM_005 `V_Q`, four-way classifier including Refusal, QM_006 descent audit, QM_002 cofiber-to-Banach bridge) were not found as implementations. `cochain.py` is a 3-way numerical LP trichotomy, not `V_Q`.
- **Object-level cofiber vs Q¹_sep is refused by `002:QM-002-C1`**, not a missing file. Φ₁=R_Λ is ill-typed (`002:QM-002-C7`).

### C750 B01 Lean roots are not in the application lean4 tree (not a register ID)

- **Closable:** yes (hygiene).
- **Why open:** `lakefile.lean` roots `FiniteQm.C750.B01.{Definitions,Reduction,Purity,AxiomCensus}`. `lean4/quantum_mechanics` has no `FiniteQm/` subdirectory. Those four files live only at `campaigns/c750/block_01/lean4/FiniteQm/C750/B01/`. `test_lean_replay.py` / `validate_layout` require one flat PascalCase directory with no subdirectories. Receipts citing `lean4/quantum_mechanics/FiniteQm/C750/B01/*.lean` (including GAP-FQM-023 source_refs) do not bind the live application library. `Reduction.lean`'s `BakerHypothesis` is a structure, not Baker 1975.

### Cited and fallback kernel paths do not match the live tree (not a register ID)

- **Closable:** yes (hygiene).
- Concrete mismatches opened here:
  - `gap_register.yaml` still cites `code/continuum_lift.py` and `code_rs/src/continuum.rs`.
  - `c750_b01_entropy.py`, `c750_b01_entropy_approx.py`, `c750_b01_entropy_verdict.py`, `c750_b01_carrier.py` keep `ImportError` fallbacks to `apps.finite_qm.code.*` (directory gone). First import succeeds via `omega_engine/code` on `sys.path`, so pytest does not exercise the dead branch.
  - `norm_approximation_frontier.py` still `from apps.finite_qm.code.gaussian_rational import Gaussian` on ImportError.
  - `test_mub_source_snapshot.py` names `omega_engine/crates_rs/omega_finite_qm/src/mub`; snapshot is under `omega_quantum_physics/src/finite_qm/mub`.
  - `c500_execution/replay_manifest.json` still lists withdrawn `code/` facade paths (supersession preserves custody, does not restore files).
  - Paper §6 and GAP-FQM-003 still locate kernels under legacy `code/`.

### GAP-F001-S000-001 — exact duality gap certificate

- **Closable:** conditional (finite Φ₁ primal/dual LP over Q plus Lean on declared graphs; general operator duality remains a separate open_bridge).
- **Why open:** `DualWitness.lean` is a 2-integer pairing bound plus Mermin–Peres sign parity. FQM-E3 is a sampled fixture. QM_080 Theorems 5–6 remain ASSERTED. Compiling Lean is a candidate mirror, not an admission.

### GAP-F001-S000-002 — continuum Hilbert lift — **not closable inside the finite programme**

- **Closable:** priced-continuum (`PRICED_CONTINUUM_INTERFACE`). Effort n/a inside this programme.
- **Why open:** No source constructs the map from a finite presented carrier to infinite-dimensional Hilbert space. QM_122 §6 refuses the lift. Canonical `[X,P]=iħI` has no finite-d matrix representation (Wintner–Wielandt). Python demo is numpy floats; Rust is exact rationals on a constructed pair; H056 is 2×2 Int. Finite Weyl–Heisenberg clock/shift is a discrete replacement, not a close of continuum CCR or unbounded domains.

### GAP-F001-S000-004 — Born uniqueness (Gleason)

- **Closable:** conditional. Typed `continuum_interface`, status `OPEN (CONDITIONAL)`. **Not** priced unclosable; **not** closed by more finite ray counts; **not** reclassified by this roadmap.
- **Why open:** Live code checks frame additivity of `v†ρv` on supplied numpy frames and a d=2 non-Bornian indicator on six angles. `GleasonTheorem.lean` is integer quadratic forms in d=2. Paper §9: neither Cabello nor Peres construction is a frame function on a dense sphere. H054 integer partitions of `{v ∈ Z³ : ||v||² = 25}` are not topology on `S(Q(ζ_n)³)`. YAML `busch_effect_frame_resolution` claims Eff_d state representation for all d≥2; H058 itself fences uniqueness as coordinate-conditional.

### GAP-F001-S000-010 — Gleason dimension extra at n ≥ 3

- **Closable:** conditional, overlapping 004. Same YAML type `continuum_interface`, status `OPEN (CONDITIONAL)`. Historical `REFUSED-DERIVABLE` withdrawn by PR 205. No necessity-of-continuum theorem is on file.
- **Why open:** `H017Gleason` falsifies a 3≤|Q| cardinality surrogate on Bool. That is not GleasonPack uniqueness. `rungs.py` `gleason_applies=(dimension >= 3)` is a flag, not a theorem.

### GAP-F001-S000-007 — CPTP class (Choi defined; Stinespring not in-base-field)

- **Closable:** conditional (exact Choi/TP on declared cyclotomic carriers with embedding threaded through; Stinespring still escalates conductor).
- **Why open:** Register status `DEFINED`; type remains `open_bridge`. Python channel maps are float; principal-minor TP/CP with tolerance; `choi_theorem_ported_lean=false` is **test-pinned**. H063 stores conductors. H017Finish `finish_cptp_imported` remains because that host defines no channel class. `stinespring_dilation.rs` and `quantum_hamiltonian.rs` are degree/label scaffolds (`AUTHORING_QUALITY: human_llm_best_effort_slop`).

### GAP-F001-S000-008 — continuous time and Stone — **not closable inside the finite programme**

- **Closable:** priced-continuum. Effort n/a.
- **Why open:** Discrete dynamics modules exist (`discrete_dynamics.py`, `dynamics_dichotomy.py`, H016/H055/H061). They partition periodic vs aperiodic unitaries. They do not construct `U(t)=exp(-iHt)` or prove Stone. H073 is Trotter-denominator arithmetic. QM_034/QM_035 are C0 stubs. QM_211 prices R and H as imports.

### GAP-C500-B06 — Hamiltonian evolution / Lieb–Robinson original contract remains open

- **Closable:** conditional (certified finite-lattice Trotter/LR with enclosures). Continuous-time / thermo-limit clauses remain priced with GAP-F001-S000-008.
- **Why open:** Register `RESOLVED_WITH_SCOPED_EVIDENCE` while unresolved_targets are `C500-T426`–`T450`. Description: no Hamiltonian evolution comparison and no volume-uniform Lieb–Robinson estimate; M5 INVALID. H073 does not prove those theorems. `quantum_hamiltonian.rs` is a scaffold.

### GAP-FQM-019 — unreplayed Mathlib Born-redundancy / channel Lean; snapshot directory absent

- **Closable:** yes as replay or re-statement.
- **Why open:** Cited `lean4/quantum_mechanics/original_lean_20260809` is absent. No prebuilt Mathlib cache is in-tree (lakefile nonetheless `require mathlib` for EntropyDichotomy / C750 roots). Eight UNREPLAYED rows: `020:C1,C4,C8`; `061:QM-061-C4`; `121:C1–C4`. SRC-081–083: `no_lean_file`. Claim maps for 208–211 bind missing `qm2NN_lib` (`GAP-FQM-017`).

### GAP-FQM-017 — QM_208–211 claim maps bind missing libraries

- **Closable:** yes (repair or delete the maps). That does not close Stone/Hamiltonian.
- **Why open:** Each of 208–211 maps claims to `qm2NN_lib.qm2NN_lib_core`; those libraries do not exist (only `qm122_lib`). False maps contribute no evidence for unitary dynamics closure.

### GAP-FQM-023 — transcendental von Neumann entropy — **not closable as a carrier-internal quantity**

- **Closable:** priced-continuum for mixed-state `S(ρ)=-Tr(ρ log ρ)` as an element of `Q(ζ_n)`. Certified rational interval enclosures for **external** thermodynamic use are an interface, not an internal close.
- **Why open:** C750 B01 Python/Rust compute exact linear forms in logs and rational enclosures; `test_c750_b01_parity.py` compares eight FQMI-1 spectra. Cited `lean4/FiniteQm/C750/B01/{Reduction,Purity}.lean` are absent from the application library. Baker is a cited hypothesis. Pure-state vanishing of the reduced form is algebraic.

### Fourth MUB in dimension 6 (not a register ID)

- **Closable:** unknown (live research problem).
- **Why open:** d=3 and d=4 complete MUB sets are constructed. d=6 has three product bases at conductor 24; bounded search tested 1000 candidates and found 0 (`status OPEN`). Nested MUB snapshot is unintegrated and refuses full MUB(6) authority (`has_full_mub6_authority` false on the f64 wall cross-validation). Existence of four (let alone seven) MUBs in d=6 is not an in-tree theorem.

### Related implementation debts not yet in the register (do not treat as closed by naming)

- **Busch positive representation (H058):** Python `recover_density_matrix` reconstructs TraceFrameFunction fixtures; Lean uniqueness is coordinate-conditional. YAML overclaims relative to the Lean header.
- **State-effect pairing (SRC-011):** ledger QM-011-C13 ASSERTED; `source_inventory` `no_lean_file` / `no_test_file`; `PairingNonSelection.lean` absent from `lean4/quantum_mechanics`.
- **Density off-diagonal coherence:** QM_012 is diagonal residual weights; `FiniteDensity.lean` is 2-state Nat diagonals; float PSD in `density_matrix.py`.
- **Operator Lüders:** QM_021 is L1 sector conditioning; inventory no Lean/tests; `measure_and_update` is float. Selective collapse remains imported (paper Rung 7).
- **Lost ENC mechanizations (070/071/120):** papers cite ENC-1123/1124/1143 Lean paths that grep does not find; inventory `no_lean_file`.
- **U(1) selector Lean (ForceComplexCarrier / U1Selector):** named files and `original_lean_20260809` absent.
- **rungs.py BoundaryDefense** overclaims Rungs 1–7 close and `gleason_applies` at d≥3 relative to paper §9.

Continuum_interface rows that remain **not closable inside the finite programme:** GAP-F001-S000-002, GAP-F001-S000-008, GAP-F001-S000-011 (Everett counting beyond Q), GAP-FQM-023. GAP-F001-S000-004 and 010 are typed `continuum_interface` and `OPEN (CONDITIONAL)`; they are **not** in the priced-unclosable set and **not** closed. GAP-F001-S000-012 is one declared real embedding, not a continuum-unclosable verdict, but every Choi/mixed-state PSD check is embedding-relative until `ι` is threaded through the kernels.

## Effort and resources

Operator judgment. Do not spend continuum-priced effort pretending it is a finite-carrier close.

**Hygiene first (supports honest standing without new theorems).** One engineer who can edit tests, Lake, and YAML together:

1. Repair or delete stale paths (register source_refs, paper §6 layout, C750/C1000 README vs `sealed_targets.json`, MUB snapshot test path, `apps.finite_qm.code` fallbacks, C500 replay_manifest facade rows documented as withdrawn-only).
2. Make `lakefile.lean` and `validate_layout` describe the same tree: either flatten/port C750 B01 into the application library under the no-subdirectory rule, or drop those four roots and cite the campaign Lake separately.
3. Rebind GAP-FQM-003 prose to the live crate; keep the missing-algorithm obligation.
4. Reconcile C1000 seals with tests (either seals become EXECUTED under a documented independence discharge, or tests stop asserting a closed terminal against NOT_STARTED seals).
5. Empty or restore `campaigns/c250/tools/` so REVIEW_C250's replay instruction is not a dangling path.
6. Point `test_withdrawn_rows.py` at `research/` now that F004 is retired, or record that those pins are skipped.

**Exact arithmetic on already-declared finite objects (closes overclaim, not uniqueness).**

- Exact rational/cyclotomic `Phi_1` primal+dual on declared graphs (replaces HiGHS `TOL=1e-9`), plus Lean on the 3-cycle already in `WorldCycle3Quotient.lean` and a second fixture.
- Exact Hermitian/PSD/trace predicates on declared cyclotomic `M_d` (replaces `eigvalsh`).
- Exact Pauli products for Mermin–Peres (replaces numpy `allclose`).
- Thread one declared real embedding through Choi and mixed-state PSD tests (GAP-F001-S000-012).

**Typed bridges the paper's standing actually needs.** Lean 4 + exact cyclotomic arithmetic; outcome unknown for Gleason:

- DualWitness → finite Φ₁ / QM_080 Thm 5–6 on declared graphs (GAP-F001-S000-001).
- H058: homogeneity constructors, positivity of recovered ρ, uniqueness for additive effect frame functions on declared d=2,3 carriers (does not close projection Gleason).
- GAP-F001-S000-004 / 010: typed uniqueness theorem **or** counterexample for projection frame functions on `Q(ζ_n)^d` at n≥3 without smuggling sphere topology. Finite Cabello/Peres/triad counts do not discharge this. d=2 obstruction is already mechanized.
- Named missing algorithms (`V_Q`, four-way classifier with Refusal, descent audit) if they remain in the paper's spine as executable claims.

**Campaign mathematics still open inside finite (not priced continuum).**

- C750 clauses 8–9 (signed cancellation completeness; conductor-growth / sign-decay bridge): the live tests pin these OPEN. May remain open.
- C500 original T301–T550: do not "close" by renaming. A new freeze with prospective bets, inhabited class, and launch census is a relaunch. Block 06 Trotter/LR specifically: certified finite-lattice enclosures; thermo-limit remains priced.
- CHSH field supremum without height bound (GAP-C1000-006): Diophantine / cyclotomic; does not prove Bell-as-nature.
- Contextuality cohomology off Z₂ (GAP-C1000-007).
- Fourth MUB in d=6: unknown; treat as research, not a sprint.

**Mathlib replay (GAP-FQM-019).** If a Mathlib toolchain/cache is admitted and the archived snapshot is restored from history; otherwise re-state the eight UNREPLAYED claims against in-tree `BornNormalization.lean` and withdraw or re-prove SRC-081–083. Promoting UNREPLAYED rows without a lake receipt would be another false receipt.

**Not a resource request inside this programme (priced continuum).** Continuum Hilbert lift; Stone / `U(t)=exp(-iHt)`; mixed-state von Neumann entropy as a carrier element; Everett counting on `Q(ζ_n)^+ \ Q`; unrestricted `C_qa` vs `C_qc` / MIP*. Implementation can keep exhibiting finite shadows and refusal certificates. It cannot close those interfaces by writing more numpy or more Lean on `Mat2Z`.

**Skills on the critical path:** Lean 4 (Mathlib-free application lake vs campaign Mathlib roots — pick one layout), exact cyclotomic / Gaussian arithmetic, pytest mutation-gate design, Lake replay hashing, campaign custody (seals vs tests), Gleason/POVM theory, Choi/Kraus only as far as the declared embedding.

## What would change our mind

**Would support a stronger implementation standing (still not programme closure):**

- Cited paths exist at the cited locations, and tests that name those paths pass without skip/fallback. Paper §6, `gap_register.yaml` source_refs, MUB snapshot test, and C750 Lake roots all describe the live tree.
- `lakefile.lean` roots equal files `validate_layout` will accept, and a fresh application lake replay receipt hashes that tree.
- C500 live tests either still assert 250 OPEN (honest) or, after a **new** freeze with prospective independent bets and an inhabited class, assert a different contract. Renaming `RESOLVED_WITH_SCOPED_EVIDENCE` while tests keep `open_targets==250` would not change our mind.
- C1000 seals, README, tests, and GAP-C1000-010 type agree. Either execution is NOT_STARTED and tests do not select `FQMR1_CLOSED_AT_DECLARED_CLASS`, or seals record EXECUTED with independence actually discharged and the register type matches.
- C750 README, seals, block_10, tests, and certification all say `FQMI1_OPEN_INTERNAL_GAPS` with clauses 8–9 OPEN — or those two clauses gain a theorem/countermodel and the tests flip for a reason written in the kernel, not in a markdown title.
- Duality: a Lean theorem that a supplied matrix witness attains the trace-norm / Φ₁ dual on a declared finite carrier, not `|w0 d0 + w1 d1| ≤ |d0|+|d1|`.
- Gleason: a typed uniqueness theorem or an explicit non-Bornian frame function on a declared dense cyclotomic sphere (not six float angles, not Cabello 18-ray, not integer norm-25 partitions). Alternatively, a proof that no such uniqueness holds on that carrier. Finite KS defects would still not suffice.
- Busch: a `RationalHomogeneityWitness2` (or cyclotomic analogue) constructor for every effect on the declared d=2,3 carriers, positivity of recovered ρ, and uniqueness not assuming the test-coordinate equations as hypotheses — **or** the register YAML withdrawn to match the H058 header.
- Exact `Phi_1` / density / Pauli kernels, with tests that fail if a float tolerance is reintroduced into a claim typed exact.
- `V_Q` / four-way classifier / descent audit existing as code with negative controls, or those paper claims downgraded so GAP-FQM-003 is only the remaining missing objects, not a false five-routine census.
- UNREPLAYED Mathlib claims either lake-replayed under a recorded toolchain or retyped ASSERTED/withdrawn. Absence of `original_lean_20260809` would no longer be cited as if the files were present.

**Would not change our mind:**

- Another certification markdown whose title says CLOSED while live tests assert OPEN.
- A compiling Lean file whose type is a 2×2 Int identity, a Bool cardinality surrogate, or a stored conductor, advertised as Gleason, Stone, Choi, or duality.
- Green pytest/cargo/lake counts, or README 593/124/122, treated as semantic closure.
- `BoundaryDefense.gleason_applies = True` at d≥3.
- More finite ray/triad/MUB candidate counts without a typed dense-sphere statement.
- Restoring legacy `code/` facades. The supersession record already says callers import destinations.
- Claiming finite QM achieved, or fully obstructed, from this tree as opened.

**Would change the programme, not the finite close:** admitting Hilbert space, Born uniqueness under sphere topology, `U(t)=exp(-iHt)`, or mixed-state `S(ρ)` as declared imports, with the finite carrier as a computational shadow. That is an honest import fence (QM_122 §6 already refuses the lift). It is not a finite presentation closing.

## Sources opened

Start files and layout: `README.md`; `finite_quantum_mechanics.md` (§0, §3–§10); `claims/gap_register.yaml`; `claims/claim_ledger.yaml`; `claims/source_inventory.yaml`; `sources/` (QM_060, QM_122 listings); `research/` listing (no `finite_qm_roadmaps/` before this write); `omega_engine/code/`, `omega_engine/crates/finite_qm/`, `omega_engine/code_rs/`, `omega_engine/crates_rs/`, `lean4/quantum_mechanics/`.

Relocation and package: `omega_engine/crates/finite_qm/README.md`; `__init__.py`; `LOCAL_SOURCE_RELOCATION.json`; `LOCAL_SOURCE_RELOCATION_SUPERSESSION.json`; `use_cases/` listing (42 `.py` plus `__init__.py`); `domain/` listing (4); `entrypoints/` listing; `use_cases/foundations.py`; `use_cases/cochain.py`; `use_cases/continuum_lift.py`; `use_cases/density_matrix.py`; `use_cases/rungs.py`; `use_cases/cptp_channels_stinespring.py`; `use_cases/composition_tensor_mub.py`; `use_cases/norm_approximation_frontier.py`; `domain/primitives.py`.

Tests and bootstrap: `omega_engine/code/tests/conftest.py`; `omega_engine/code/pytest.ini`; `omega_engine/code/tests/unit/` listing; `test_c500_execution.py`; `test_c500_campaign.py`; `test_lean_replay.py`; `test_mub_source_snapshot.py`; `test_gap_register.py`; `test_withdrawn_rows.py`; `test_c750_execution.py`; `test_causal_price_list.py`; `test_cptp_channels_stinespring.py`; `omega_engine/code/application_lean_replay.py`; `omega_engine/code/c750_b10_synthesis.py`; `omega_engine/code/c750_b01_entropy.py`; `omega_engine/code/tests/e2e/` listing.

Rust: `omega_engine/code_rs/src/lib.rs`; `omega_engine/crates_rs/omega_finite_qm/src/lib.rs` and `src/` listing (no `mub/`); `omega_engine/crates_rs/omega_quantum_physics/src/` listing; `finite_qm/continuum.rs`; `finite_qm/mub/README.md`; `born_gleason.rs`; `stinespring_dilation.rs`; `quantum_hamiltonian.rs`.

Lean: `lean4/lakefile.lean`; `DualWitness.lean`; `GleasonTheorem.lean`; `H058EffectFrameBusch.lean`; `H063CptpChannelsStinespring.lean`; `H056ContinuumLiftBoundary.lean`; `H017Finish.lean`; `H073ContinuousTimeLocalityLimit.lean`; `FiniteDensity.lean`; `campaigns/c750/block_01/lean4/FiniteQm/C750/B01/Reduction.lean`; confirmed absent: `lean4/quantum_mechanics/original_lean_20260809`, `lean4/quantum_mechanics/FiniteQm/`, legacy `code/`.

Campaigns and evidence: `campaigns/c250/INSTRUCTIONS.md`, `sealed_targets.json`, `tools/` (empty); `campaigns/c500/sealed_targets.json`; `campaigns/c500_execution/WITHDRAWAL.md`, `replay_manifest.json`, `replay_manifest_supersession.json`, `block_10/result.json`; `campaigns/c750/README.md`, `sealed_targets.json`, `block_10/result.json`; `campaigns/c1000/README.md`, `sealed_targets.json`, `block_10/result.json`; `evidence/PR205_REVIEW.md`; `evidence/REVIEW_C250_20260907.md`; `evidence/C500_FQMC1_CLOSURE.md`; `evidence/C750_FQMI1_CLOSURE.md`; `evidence/C1000_FQMR1_CLOSURE.md`; `evidence/continuum_lift_boundary.json`; `evidence/c250_block06_channels.json`.
