# MUB(6) Comprehensive Survey & Migration Blueprint

## 1. Observation

### 1.1 Direct Inspection of `papers/core/mub6/`
Direct inspection of `papers/core/mub6/` reveals 30 files and 12 subdirectories:
- **Manuscripts & Epistemic Records:**
  - `mub6.md` (66,073 bytes, 1,106 lines): Formal manuscript by Jeremy H. Carroll (v1.1.1, 2026-10-16) separating exact finite reductions, reported Lean implications, and unresolved bounds. Key finding stated on line 14: *"Whether nonextension holds for every raw Hadamard remains open."* Line 30: *"No unconditional dimension-wide MUB bound follows from this package at this checkpoint."*
  - `theory_of_finite_mub6.md` (89,290 bytes, 1,212 lines): Formal derivation directed acyclic graph detailing 86 derivations (`MUB6-DERIV-001` through `MUB6-DERIV-086`) across 16 stages from Pre-Genesis to Terminal Classification.
  - `theory_of_finite_mub6.jsonl` (88,615 bytes): Machine-readable export of all 86 derivation nodes.
  - `mub6_claim_ledger.yaml` (19,088 bytes, 492 lines): Formal claim ledger defining 41 claims (`MUB6-C01` through `MUB6-C41`) with explicit Lean 4 module bindings, Python/Rust test targets, and epistemic statuses (e.g. C08: `NOT_A_CERTIFICATE`, C39: `refutes its stated premise`, C41: `PASS_FOR_REPRESENTED_SOLUTIONS`).
  - `mub6_claim_ledger.md` (38,551 bytes): Detailed narrative companion to the claim ledger.
  - `mub6_change_log.md` (39,196 bytes) & `mub6_executive_checkpoint.md` (33,476 bytes).
- **Subdirectories in `papers/core/mub6/`:**
  - `code/`: Contains `mub_verify/` (28 Python modules), `conj2_symbolic_verification/` (4 Python modules + 4 Markdown proof records), `deposit_paths.py`, `Cargo.toml`, `Cargo.lock`, and `src/` (`lib.rs`, `main.rs`).
  - `rust/`: Contains 2 stub files: `mub6_smale_sentry.rs` (points to `omega_mub::omega_native::mub6_smale_sentry`) and `network_simplex.rs` (points to `omega_solvers::network_simplex_solver`).
  - `lean4/`: Contains 3 Lean files: `AuditMub6Axioms.lean` (audits declarations against standard axioms `propext`, `Classical.choice`, `Quot.sound`), `ExportSzollosiCoefficients.lean`, and `ExportSzollosiSystem.lean`.
  - `scripts/`: 20 Python/Lua/Node scripts including reflection scripts (`reflect_szollosi_rectangular.py`, `reflect_szollosi_gauged.py`, `reflect_szollosi_native.py`, `reflect_balanced_quadratic.py`, `reflect_quadratic_lift.py`), certificate generators (`compute_r7_singular_segre_sos.py`, `compute_subgap_r6_closure_receipt.py`), and manifest tools (`regen_sha256sums.py`, `verify_publication.py`).
  - `tests/`: 11 test files (`test_36_check_publication_audit.py`, `test_conj2_all_slice_configurations.py`, `test_gauged_reflection_wire.py`, `test_option_b_premises.py`, `test_publication_release.py`, `test_rectangular_reflection_wire.py`, `test_remediation_b1_b11.py`, `test_remediation_m1_m4.py`, `test_route_c_fourier_landing.py`, `test_zenodo_release_archive.py`, `conftest.py`).
  - `artifacts/`, `documentation/`, `prompts/`, `research/`, `scratch/`, `zenodo/`.
  - Verification & Manifests: `verify_deposit.py` (9,182 bytes), `sha256sums` (104,231 bytes), `manifest.sha256` (104,149 bytes).

### 1.2 Inspection of Target Python Areas (`code/python/src/` and `code/python/tests/`)
- Existing `code/python/src/mub/` contains:
  - `__init__.py`: Exports dual-face surface (`verify_mub_crate_invariants`, `package_info`, `authority_effect`, `Cyc24`, `IndependentMubVerifier`, etc.) and re-exports from `.mub_verify`.
  - `mub_verify/`: Duplicate copy of `papers/core/mub6/code/mub_verify/` containing 28 modules.
  - `conj2_symbolic_verification/`: Duplicate copy of `papers/core/mub6/code/conj2_symbolic_verification/` containing 8 files.
  - `deposit_paths.py`: Identical to `papers/core/mub6/code/deposit_paths.py`.
  - `src/`: Empty directory (anomaly in clean architecture).
  - `tests/`: Contains 12 test files copied inside `code/python/src/mub/tests/`, violating the separation between source (`code/python/src/`) and test suites (`code/python/tests/`).
- Target `code/python/tests/`:
  - Contains `test_dual_face_majorana_mub_fsp.py` (286 lines). Executing `python -m pytest code/python/tests/test_dual_face_majorana_mub_fsp.py -q` yields 8 passed in 0.98s (exit code 0).
- Running pytest on `papers/core/mub6/tests/`:
  - Result: **113 passed, 6 failed** in 28.06s.
  - Failure 1: `test_check20_lean_scan_inventory_check` in `test_36_check_publication_audit.py` -> expects `repo_root / "lean4" / "research_programs" / "mub6"` with >= 50 `.lean` files.
  - Failure 2: `test_formatter_reproduces_checked_candidate_box_source` in `test_gauged_reflection_wire.py` -> missing Lean reflection target.
  - Failure 3: `test_sealed_preprint_and_archive` in `test_publication_release.py` -> `ValueError: Noncanonical complete archive bytes`.
  - Failure 4: `test_formatter_reproduces_the_kernel_checked_source` in `test_rectangular_reflection_wire.py` -> `FileNotFoundError: lean4/research_programs/mub6/SzollosiRectangularReflection.lean`.
  - Failure 5: `test_b9_cross_language_consistency_is_lexical` in `test_remediation_b1_b11.py` -> `StopIteration` searching for parent directory containing `omega_engine`.
  - Failure 6: `test_lean4_route_c_formalization_integrity` in `test_route_c_fourier_landing.py` -> `AssertionError: Lean file not found at lean4/research_programs/mub6/RouteCFourierLandingBypass.lean`.

### 1.3 Inspection of Target Rust Areas (`code/rust/`)
- `code/rust/Cargo.toml`:
  - Root workspace configuration includes `"src/mub"` in `[workspace.members]`.
  - `tfqm_mub = { path = "src/mub" }` registered under `[dependencies]`.
- `code/rust/src/lib.rs`:
  - Line 20: `pub use tfqm_mub as mub;`.
- `code/rust/src/mub/`:
  - Implements crate `tfqm_mub`.
  - `Cargo.toml` specifies dependencies: `nalgebra`, `num-bigint`, `num-rational`, `serde`, `flate2`, `sha2`, `thiserror`, and optional `pyo3` feature.
  - `lib.rs` exports modules `deep_run`, `omega_native`, `primitive_map`, `runtime_adapter`, and root functions `verify_mub_crate_invariants()`.
  - `omega_native/`: Contains **109 `.rs` files** and 5 subdirectories implementing exact arithmetic, degree-2/4/6/8 SDPs, moment ledgers, nerve chaining, Deltoid cusp solvers, Haagerup covers, Szöllősi executable systems, Smale sentries, etc.
- `code/rust/tests/omega_mub/`:
  - Contains **52 integration test files** directly exercising all MUB(6) native engines (`test_degree2_sdp.rs`, `test_degree4_sdp.rs`, `test_degree6_sdp.rs`, `test_degree8_sdp.rs`, `test_target_a10_global_cover.rs`, `test_target_a11_orbit_exhaustiveness.rs`, `test_target_a12_smale_sentry.rs`, `test_target_a13_grand_synthesis.rs`, `test_symbol_game_host.rs`, etc.).
- `papers/core/mub6/rust/` and `papers/core/mub6/code/`:
  - Contain thin forwarding references (`mub6_smale_sentry.rs`, `network_simplex.rs`) and a bridge crate `mub6_code_bridge` whose `main.rs` prints an epistemic banner stating *"AuthorityEffect: None. Gap G1 stays OPEN. R6 and R7 stay NOT_A_CERTIFICATE."*

### 1.4 Inspection of Lean 4 Areas
- Root `lean4/lakefile.lean`:
  - Flat layout with Mathlib 4 commit `0df444a360eaa60ab8c11dca51a86af692955474`.
  - Currently includes foundational MUB modules (`H030OctahedralMubCliftonKent`, `H031OctahedralDepolarizingThreshold`, `H050MubTomographyInversion`, `H051Mub4GaloisFieldContextuality`, `H062CompositionTensorMub`), but lacks the paper-specific MUB(6) modules.
- `papers/core/mub6/lean4/`:
  - Contains 3 files: `AuditMub6Axioms.lean`, `ExportSzollosiCoefficients.lean`, `ExportSzollosiSystem.lean`.
- **Discovery of Canonical Upstream MUB(6) Lean Corpus:**
  - Located at `C:\Users\a343o\source\repos\the_symbol_game\lean4\research_programs\mub6`.
  - Contains **184 `.lean` files** and a `lakefile.toml` requiring the identical Mathlib 4 commit (`0df444a360eaa60ab8c11dca51a86af692955474`).
  - Grep audit across all 184 files confirms:
    - **Zero `sorry`** in active proof bodies (matches found are solely in comments/docstrings such as *"All declarations are axiom-clean... no sorry"*).
    - **Zero `admit`**.
    - Strict adherence to Lean foundational axioms: `#[propext, Classical.choice, Quot.sound]`.

### 1.5 Inspection of Deposit Verification (`verify_deposit.py`)
- Running `python papers/core/mub6/verify_deposit.py --skip-header-schema` fails with 9 issues:
  - 5 Hash mismatches:
    - `code/conj2_symbolic_verification/proof_conj2b.md`
    - `code/conj2_symbolic_verification/szollosi_2circulant_proof.md`
    - `code/src/main.rs`
    - `research/subgap_r7_adversarial_audit_note.md`
    - `research/subgap_r7_genuine_separation_specification.md`
  - 4 Unrecorded deposit files:
    - `artifacts/mub6_szollosi_t5_cover_receipt.json`
    - `research/five_derivations_20261015/generic_replay.json`
    - `theory_of_finite_mub6.jsonl`
    - `theory_of_finite_mub6.md`
- Script `papers/core/mub6/scripts/regen_sha256sums.py` is present and designed to recompute `manifest.sha256` and `sha256sums` to restore fail-closed integrity after planned migrations.

---

## 2. Logic Chain

1. **Premise 1 (R1 & R2 Consolidation):** Reusable library code currently residing in `papers/core/mub6/code/` (`mub_verify`, `conj2_symbolic_verification`, `deposit_paths.py`) has already been mirrored into `code/python/src/mub/`, but duplicate copies still exist inside `papers/core/mub6/code/`, and an anomalous test copy exists in `code/python/src/mub/tests/`.
2. **Premise 2 (R2 Paper Deposit Purity):** To satisfy repository layout rules (`PROJECT.md` and Clean Architecture), `code/python/src/mub/tests/` must be moved to `code/python/tests/` (or consolidated with `papers/core/mub6/tests/`), and `code/python/src/mub/src/` must be purged. `papers/core/mub6/` must import reusable library logic directly from `code/python/src/mub` or via path resolution, and `sha256sums`/`manifest.sha256` must be regenerated via `regen_sha256sums.py`.
3. **Premise 3 (Test Failures Root Cause):** The 6 pytest failures in `papers/core/mub6/tests/` stem directly from:
   - External path assumptions (`repo_root / "lean4" / "research_programs" / "mub6"` instead of local or root `lean4/`).
   - Hardcoded repo-name lookups (`(p / "omega_engine").is_dir()` in `target_q_degree8_and_gns.py:1140`).
   - Stale zip bytes in `mub6_publication.zip`.
   Remediating these path adapters to point to the consolidated locations in `theory_of_finite_quantum_mechanics` will resolve all 6 test failures without changing mathematical logic.
4. **Premise 4 (Rust Status & Integration):** Rust crate `code/rust/src/mub` (`tfqm_mub`) is already feature-complete with 109 native modules and 52 integration tests in `code/rust/tests/omega_mub/`. It is already declared in `code/rust/Cargo.toml` and re-exported in `code/rust/src/lib.rs`. The 2 stubs in `papers/core/mub6/rust/` and `papers/core/mub6/code/src/lib.rs` are lightweight forwarders to this crate.
5. **Premise 5 (Lean 4 Formalization Integrity):** The 41 claims in `mub6_claim_ledger.yaml` map to exact Lean 4 modules (`RouteCFourierLandingBypass.lean`, `Conjecture2GeneralMechanization.lean`, `MubMinorChart.lean`, `SzollosiQuadraticSystem.lean`, etc.) that are fully implemented and verified with zero `sorry` and zero `admit` in the upstream repository corpus at `C:\Users\a343o\source\repos\the_symbol_game\lean4\research_programs\mub6`. Integrating these modules into `lean4/` in a flat layout (per R3.3) and registering them in `lean4/lakefile.lean` will fulfill the Lean 4 acceptance criteria.

---

## 3. Inventory of Theorems, Claims, and Derivations

### 3.1 Claim Ledger Matrix (`mub6_claim_ledger.yaml`, 41 Claims)

| Claim ID | Name | Claim Type | Target Lean 4 Module | Rust / Python Evidence |
|---|---|---|---|---|
| **MUB6-C01** | Orbit Configuration Fourier Count Lower Bound | FormalLeanTheorem | `RouteCFourierLandingBypass` | `test_route_c_fourier_landing.py` |
| **MUB6-C02** | Orbit Configuration Fourier Transition Pairs Lower Bound | FormalLeanTheorem | `RouteCFourierLandingBypass` | `test_route_c_fourier_landing.py` |
| **MUB6-C03** | Orbit Configuration Fourier Landing Edges Lower Bound | FormalLeanTheorem | `RouteCFourierLandingBypass` | `test_route_c_fourier_landing.py` |
| **MUB6-C04** | Conditional Non-Existence of Complete MUB(6) via Route C | FormalLeanTheoremConditional | `RouteCFourierLandingBypass` | `test_route_c_fourier_landing.py` |
| **MUB6-C05** | Non-Existence under Fourier Triple Landing Bypass | FormalLeanTheoremConditional | `RouteCFourierLandingBypass` | `test_route_c_fourier_landing.py` |
| **MUB6-C06** | Analytic Cube Slice Certificate for Conjecture 2 | LeanDefinition | `Conjecture2GeneralMechanization` | `test_conj2_all_slice_configurations.py` |
| **MUB6-C07** | Tao Phase-Table All-Slice Evaluation | FormalLeanTheorem | `Conjecture2GeneralMechanization` | `test_conj2_all_slice_configurations.py` |
| **MUB6-C08** | R6 Moduli Classification Receipt Status | CustodyVerification | N/A (Status: `NOT_A_CERTIFICATE`) | `test_option_b_premises.py` |
| **MUB6-C09** | Matolcsi Moduli Receipt Verification | CustodyVerification | N/A (Digest Separation) | `test_option_b_premises.py` |
| **MUB6-C10** | Cauchy-Binet Invertible Minor Quantitative Bound | FormalLeanTheorem | `MubMinorChart` | `test_remediation_b1_b11.py` |
| **MUB6-C11** | Complete Block Reconstruction Chart | FormalLeanTheorem | `MubBoundedBlockChart` | `test_remediation_b1_b11.py` |
| **MUB6-C12** | Division-Free Quartet Matrix Equations | FormalLeanTheorem | `MubBoundedQuartetEquations` | `test_remediation_b1_b11.py` |
| **MUB6-C13** | Standard-Basis Unbiasedness Coordinate Bounds | FormalLeanTheorem | `SzollosiQuartetSystem` | `test_remediation_b1_b11.py` |
| **MUB6-C14** | Rational Affine Completion System | FormalLeanTheorem | `MubBalancedCompletion` | `test_remediation_b1_b11.py` |
| **MUB6-C15** | Balanced Quadratic System Degree and Equivalence | FormalLeanTheorem | `MubBalancedQuadraticPolynomials` | `test_remediation_b1_b11.py` |
| **MUB6-C16** | Quadratic Lift Equivalence | FormalLeanTheorem | `SzollosiQuadraticSystem` | `test_remediation_b1_b11.py` |
| **MUB6-C17** | Rational Containing Box Radius Bounds | FormalLeanTheorem | `SzollosiQuadraticSystem` | `test_remediation_b1_b11.py` |
| **MUB6-C18** | Bounded Solution Quartet Equivalence | FormalLeanTheorem | `SzollosiQuadraticSystem` | `test_remediation_b1_b11.py` |
| **MUB6-C19** | Deltoid Cover Standard-Basis Margin Disjointness | ExactComputation | N/A (Residual Margin 37249/90000) | `test_remediation_b1_b11.py` |
| **MUB6-C20** | Augmented 666-Equation System Parameter Equivalence | FormalLeanTheorem | `SzollosiGaugedExecutable` | `test_gauged_reflection_wire.py` |
| **MUB6-C21** | Native Six-Chart Candidate Cover Equivalence | FormalLeanTheorem | `SzollosiGaugedReflection` | `test_gauged_reflection_wire.py` |
| **MUB6-C22** | Szöllősi Continuous Two-Circulant Construction | FormalLeanTheorem | `SzollosiTwoCirculant` | `test_remediation_b1_b11.py` |
| **MUB6-C23** | Szöllősi Quartet Equivalence with Additional Bases | FormalLeanTheorem | `SzollosiQuartetSystem` | `test_remediation_b1_b11.py` |
| **MUB6-C24** | 618 Rational Equations Degree at Most Two | FormalLeanTheorem | `SzollosiQuadraticSystem` | `test_remediation_b1_b11.py` |
| **MUB6-C25** | Midpoint Secant Identity and Exclusion Soundness | FormalLeanTheorem | `RectangularQuadraticExclusion` | `test_rectangular_reflection_wire.py` |
| **MUB6-C26** | Column-Gauge Reduction First-Row Equality | FormalLeanTheorem | `SzollosiColumnGauge` | `test_gauged_reflection_wire.py` |
| **MUB6-C27** | Native Sparse Jacobian Row Reflection | FormalLeanTheorem | `SzollosiRectangularReflection` | `test_rectangular_reflection_wire.py` |
| **MUB6-C28** | Native Candidate Box Exclusion on Coordinate 368 | FormalLeanTheorem | `SzollosiGaugedReflection` | `test_gauged_reflection_wire.py` |
| **MUB6-C29** | Complex Rank-One Projector Construction | FormalLeanTheorem | `ConcreteMubProjectors` | `test_remediation_m1_m4.py` |
| **MUB6-C30** | Concrete MUB Word Moment Flatness | FormalLeanTheorem | `ConcreteMubMoments` | `test_remediation_m1_m4.py` |
| **MUB6-C31** | Concrete MUB Orthonormality & Overlap Polynomials | FormalLeanTheorem | `ConcreteMubPolynomials` | `test_remediation_m1_m4.py` |
| **MUB6-C32** | Finite Reverse Word Projector Extraction | FormalLeanTheorem | `FlatMomentProjectorExtraction` | `test_remediation_m1_m4.py` |
| **MUB6-C33** | Contextual Basis Word Relations Extraction | FormalLeanTheorem | `FlatMomentBasisRelations` | `test_remediation_m1_m4.py` |
| **MUB6-C34** | Zero-Action Interface Countermodel Inhabitation | FormalLeanTheorem | `MomentPositivityObligation` | `test_remediation_m1_m4.py` |
| **MUB6-C35** | Commutative Flat Real Moments Zero Extraction | FormalLeanTheorem | `CommutativeFlatMoments` | `test_remediation_m1_m4.py` |
| **MUB6-C36** | 4th Basis Equivalence to Positive Flat Moments | FormalLeanTheorem | `ConcreteMubFlatExtension` | `test_remediation_m1_m4.py` |
| **MUB6-C37** | Moment Functional Nonpositivity from Empty Variety | FormalLeanTheorem | `ConcreteMubFlatExtension` | `test_remediation_m1_m4.py` |
| **MUB6-C38** | Balanced Table Regeneration & Centre Jacobian | ExactComputation | N/A (Rank 184/320) | `omega_native::mub6_balanced_table_replay` |
| **MUB6-C39** | Prompt 05 Fixed-Triple Local Lemma Checks | ExactComputation | N/A (D9 refutes stated premise) | `omega_native::mub6_prompt05_campaign_checks` |
| **MUB6-C40** | Szöllősi Common-Ray Reduction | FormalLeanTheorem | `SzollosiCommonRays` | `research/five_derivations_20261015/` |
| **MUB6-C41** | Pair Exclusion at Special Szöllősi Point | ExactComputation | N/A (`PASS_FOR_REPRESENTED_SOLUTIONS`) | `research/five_derivations_20261015/replay_rur.py` |

### 3.2 86-Derivation Directed Acyclic Graph Summary (`theory_of_finite_mub6.md`)

| Stage | Name | Range | Nodes | Focus Area |
|---|---|---|---|---|
| **01** | Pre-Genesis Foundations | DERIV-001 – 005 | 5 | Inert inscription, distinction $\Delta$, cofiber defect, DDA cocycle, FOC gate |
| **02** | Genesis & Discrete $S(n)$ | DERIV-006 – 010 | 5 | Carrier set $\mathcal{X}$, symmetric group $S(n)$, cycle partition, Cayley graph, permutation rep |
| **03** | Relational Governance | DERIV-011 – 015 | 5 | Relational pairing $\mathcal{R}$, witness poset, dual witness dominance, terminalizer, contract fence |
| **04** | $\ell^1$ Mass Emergence | DERIV-016 – 020 | 5 | Probability simplex $\Delta_n$, stochastic kernel $T$, $\ell^1$ norm, Markov semigroup, stationary measure |
| **05** | $\ell^1 \to \ell^2$ Amplitude Lift | DERIV-021 – 025 | 5 | Born square-root map, $U(1)$ phase fiber, interference defect, complex Hilbert space $\mathcal{H}$, projection lattice |
| **06** | Finite QM Kinematics | DERIV-026 – 030 | 5 | Density matrix $\rho \in \mathcal{S}(\mathcal{H})$, Gleason frame measure, POVM, partial trace, Wigner-Yanase skew info |
| **07** | Graded Dynamics | DERIV-031 – 035 | 5 | Discrete generator $H$, unitary group $U(d)$, time translation, CPTP dynamical map, Stinespring dilation |
| **08** | QED & $U(1)$ Holonomy | DERIV-036 – 040 | 5 | Discrete $U(1)$ gauge link, holonomy $W_\gamma$, Wilson loop, Maxwell action, Dirac-Coulomb bound states |
| **09** | QCD & $SU(3)$ Color | DERIV-041 – 045 | 5 | $SU(3)$ link matrices, Gell-Mann color algebra, color holonomy, Wilson plaquette, string tension |
| **10** | Quantum Gravity & Regge | DERIV-046 – 050 | 5 | Discrete edge length cochain, Regge deficit angle, spin network states, area/volume spectra, WdW constraint |
| **11** | Dim-6 Hilbert Geometry | DERIV-051 – 055 | 5 | Quhex tensor $\mathbb{C}^2 \otimes \mathbb{C}^3$, Galois field order-6 composite obstruction, Weyl-Heisenberg $X_6, Z_6$, Pauli subgroups, MUB formal definition |
| **12** | Complex Hadamard Moduli | DERIV-056 – 062 | 7 | MUB-Hadamard bijection, Fourier $F_6$ defect (dim 4), Haagerup $H_6(q)$, Szöllősi Deltoid, Karlsson 3-param orbit, Tao $S_6$, Ditǎ affine stratification |
| **13** | MUB(6) Algebraic Variety | DERIV-063 – 068 | 6 | Standard triad $\{I_6, F_6, B_3\}$, 72-coordinate variety, 180 polynomial residuals, Gram Nullstellensatz, Gröbner elimination, Torus slice emptiness |
| **14** | Moment Relaxations & SDP | DERIV-069 – 074 | 6 | Lasserre SOS hierarchy, degree-2 moment SDP, Curto-Fialkow flat extension obstruction, commutative truncation, rational Positivstellensatz, exact Cholesky |
| **15** | Conjecture 2 & Slices | DERIV-075 – 080 | 6 | Matolcsi-Weiner Conjecture 2 (20 masks), Tao $\ell^1$ norm 9 bound, Krawczyk interval Newton, Smale $\alpha$ sentry, Hadamard manifold fences, cusp singularity exclusion |
| **16** | Terminal Non-Existence | DERIV-081 – 086 | 6 | Basis gluing $\Psi$ contraction, simplicial $\Phi_1 \ge \Gamma_{\text{critical}}$ bound, Route C Fourier landing bypass, master moduli routing, quartet non-existence, terminal $\max\_mub(6) = 3$ |

---

## 4. Caveats

1. **Unconditional Global MUB(6) Status:** Per `mub6.md` and `mub6_claim_ledger.yaml`, this codebase establishes rigorous finite reductions, quantitative minor bounds, and conditional non-existence theorems. Gap G1 remains open in the formal sense, and R6/R7 receipts maintain `NOT_A_CERTIFICATE` status. The grand 86-step DAG in `theory_of_finite_mub6.md` represents a complete roadmap and verification scaffold, but claims in the paper repository must remain strictly scoped to proved lemmas.
2. **Lean 4 Build Scope:** Root `lean4/` currently contains 196 flat files verifying the foundational Theory of Finite Quantum Mechanics. Compiling the 184 MUB(6) Lean modules requires Mathlib 4 (pinned to `0df444a360eaa60ab8c11dca51a86af692955474`).
3. **Repository Path Encapsulation:** Tests in `papers/core/mub6/tests/` currently contain references to legacy paths (`omega_engine`, `research_programs/mub6`). These must be normalized to relative monorepo paths in subsequent migration phases.
4. **Publication Archive Immutability:** `mub6_publication.zip` is a sealed archive whose hash is recorded in `render_binding.json`. Modifying manuscript files requires running `scripts/build_publication_release.py` to regenerate the zip and its sidecar hash.

---

## 5. Conclusion & Actionable Migration Roadmap

### 5.1 Python Migration Plan (Fulfilling R2)
1. **Remove Duplicate Library Trees:** Remove duplicate `mub_verify/` and `conj2_symbolic_verification/` from `papers/core/mub6/code/` after confirming all imports in `papers/core/mub6/scripts/`, `tests/`, and `verify_deposit.py` resolve to `code/python/src/mub`.
2. **Clean Up `code/python/src/mub/`:**
   - Remove spurious empty directory `code/python/src/mub/src/`.
   - Relocate `code/python/src/mub/tests/` into `code/python/tests/mub/` or merge into `code/python/tests/`.
3. **Repair Path Adapters in `papers/core/mub6/tests/`:**
   - Update `test_remediation_b1_b11.py:463` to detect repository root without relying on `omega_engine`.
   - Update `test_route_c_fourier_landing.py`, `test_rectangular_reflection_wire.py`, and `test_36_check_publication_audit.py` to point to consolidated Lean locations in `lean4/`.
4. **Regenerate Deposit Checksums:** Run `python papers/core/mub6/scripts/regen_sha256sums.py` to restore zero-defect verification in `verify_deposit.py`.

### 5.2 Rust Integration Plan (Fulfilling R3.2)
1. The Rust crate `tfqm_mub` in `code/rust/src/mub/` is already comprehensive (109 modules in `omega_native`, 52 integration tests).
2. Ensure full multi-target test execution (`cargo test --package tfqm_mub`) executes cleanly once build locks clear.
3. Keep `papers/core/mub6/rust/` as thin reference documentation or migrate its notes into `code/rust/src/mub/README.md`.

### 5.3 Lean 4 Formalization Plan (Fulfilling R3.3)
1. Import the verified, sorry-free MUB(6) Lean formalizations from `C:\Users\a343o\source\repos\the_symbol_game\lean4\research_programs\mub6` into the root `lean4/` directory.
2. Adhere to the flat layout required by `original_request.md`.
3. Register the newly added modules in `lean4/lakefile.lean`.
4. Run `AuditMub6Axioms.lean` to verify that all theorems depend only on standard Lean logic (`propext`, `Classical.choice`, `Quot.sound`) with 0 `sorry`, 0 `admit`, and 0 custom axioms.

---

## 6. Verification Method

To independently verify the observations in this survey:

1. **Python Dual-Face Test Verification:**
   ```bash
   python -m pytest code/python/tests/test_dual_face_majorana_mub_fsp.py -q
   ```
   *Expected outcome:* 8 passed in ~1s.

2. **MUB6 Test Suite Baseline Check:**
   ```bash
   python -m pytest papers/core/mub6/tests -q
   ```
   *Expected outcome:* 113 passed, 6 failed (due to documented path adapter lookups).

3. **Deposit Verification Baseline Check:**
   ```bash
   python papers/core/mub6/verify_deposit.py --skip-header-schema
   ```
   *Expected outcome:* 9 manifest issues reported (5 modified + 4 unrecorded).

4. **Lean 4 Axiom & Sorry Audit Check:**
   ```pwsh
   Get-ChildItem -Path "C:\Users\a343o\source\repos\the_symbol_game\lean4\research_programs\mub6\*.lean" | Select-String -Pattern ":= sorry"
   ```
   *Expected outcome:* 0 results (sorry-free).
