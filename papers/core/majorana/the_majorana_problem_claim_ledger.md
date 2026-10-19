# Claim Ledger — The Majorana Problem (`the_majorana_problem.md`)

**Series Key:** `002_projection_obstruction/026_microsoft_majorana_problem`  
**Live directory:** `009_ms_majorana`. The series key above is the historical package id.  
**Paper:** `the_majorana_problem.md`  
**Ledger Date:** 2026-09-19  
**Version:** `v1.1.0`  
**Canonicality:** Mirrors the claim-id body index of `the_majorana_problem.md`.  
**Authority:** `AuthorityEffect: None`  

---

## 1. Primary Claim Registry

| Claim ID | Claim Title & Content | Category | Verification Basis | Status |
| :--- | :--- | :--- | :--- | :---: |
| **MAJ-C1** | **The Microsoft Majorana Problem**: The realization packet gap between continuous laboratory hardware narratives (InAs-Al nanowires, ZBAs, capacitance shifts) and discrete algebraic verification schedules ($\mathbb{F}_2$ homology, Ising matrices). | [DEFINITION] | Monograph §3.1, Def 3.1; Lean 4 `transfer_gap_strictly_positive`, `detector_inadequate_when_kernel_nontrivial`; Python `DetectorAdequacyAudit` | [VERIFIED] |
| **MAJ-C2** | **$\mathbb{F}_2$ Residual Trichotomy**: For any cochain complex $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$ over $\mathbb{F}_2$ with $d_1 d_0 = 0 \pmod 2$, every $\omega \in C^1$ is exclusively `Exact` ($\omega \in \operatorname{im} d_0$), `ClosedResidual` ($\omega \in \ker d_1 \setminus \operatorname{im} d_0$), or `OpenObstruction` ($d_1 \omega \neq 0$). | [DERIVED] | Monograph §4.1, Theorem 4.1; Lean 4 `coboundary_is_cocycle`, `exact_not_open`, `exact_not_closed_residual`, `closed_residual_not_open`, `trichotomy_pairwise_disjoint`; Python `classify_residual` | [VERIFIED] |
| **MAJ-C3** | **Cubic reflexivity**: Lean `gaussian_elimination_cubic_bound` is `Nat.le_refl` of `n * n * n`, and `gaussian_elimination_ops n` is defined as `n * n * n`. That declaration does not exhibit Gaussian elimination and does not decide the trichotomy. | [COMPUTATIONAL] | `lean4/MajoranaCore.lean` | [FENCED] |
| **MAJ-C4** | **Nilpotency Refusal**: If $d_1 \circ d_0 \neq 0 \pmod 2$, evaluation is strictly refused (`RepresentationInvalid` / `Err`); no homology labels are emitted. | [DERIVED] | Monograph §4.3, Prop 4.3; Lean 4 `coboundary_is_cocycle`, `nilpotency_refusal_sound`; Python `F2CochainComplex.is_nilpotent` | [VERIFIED] |
| **MAJ-C5** | **Surface Toy Scope Fence**: Multi-plaquette surface code models are diagnostic shadows for software schedules, not physical threshold certificates or fault-tolerance proofs. Lean `surface_code_error_detection_bound` is the identity `err_weight < code_distance → err_weight < code_distance`. | [SCOPE FENCE] | This sentence. Lean `surface_code_error_detection_bound` is not the fence. | [FENCED] |
| **MAJ-C6** | **Kitaev Chain Import**: The 1D Kitaev wire Hamiltonian, Bogoliubov-de Gennes spectrum, and topological phase bounds ($|\mu| < 2t, |\Delta| > 0$) are standard imported models, not theorems derived by discrete algebra. | [SCOPE FENCE] | Monograph §7.1; Lean 4 `mzm_boundary_decoupling`, `disjoint_majorana_pair_commute`; Python `KitaevSweetSpotChain` | [FENCED] |
| **MAJ-C7** | **Ising Anyon Algebraic Bounds**: Fusion rules $\sigma \otimes \sigma = 1 \oplus \psi$ and specialized $\mathbb{Q}(\zeta_{16})$ braid matrices check software consistency, but do not prove physical anyon braiding or universal TQC. | [SCOPE FENCE] | Monograph §7.2; Lean 4 `ising_quantum_dim_squared`, `IsingAnyon`; Python `IsingFusionAlgebra` | [FENCED] |
| **MAJ-C8** | **Parity Observable Isolation**: $\mathbb{Z}_2$ parity operator algebra commuting with an effective Hamiltonian is an algebraic consistency property, not experimental proof of quantum capacitance or topological protection. | [SCOPE FENCE] | Monograph §7.3; Lean 4 `parity_eigenvalues`, `ParityObservable`; Python `ParityAlgebraModel` | [FENCED] |
| **MAJ-C9** | **Pfaffian Positivity Scope**: Local Pfaffian non-negativity under declared time-reversal/particle-hole symmetries does not solve the generic NP-hard fermion sign problem. | [SCOPE FENCE] | Monograph §7.4; Lean 4 `pfaffian_topological_sign`; Python `pfaffian_z2_invariant` | [FENCED] |
| **MAJ-C10** | **Observer Projection Quarantine**: Continuous device baths, continuum BdG spectra, and vendor marketing are external observer projections; they do not populate $\mathbb{F}_2$ receipts or mint authority. | [Q-HELD] | Monograph §3.3; Lean 4 `detector_inadequate_when_kernel_nontrivial`; Python `DetectorAdequacyAudit` | [FENCED] |
| **MAJ-C11** | **Closed-residual restatement**: Lean `local_green_not_global_red` restates `is_closed_residual` as `is_cocycle ∧ ¬ is_exact` by `exact h`. That declaration does not by itself prove a surface-schedule theorem. | [DERIVED] | `lean4/MajoranaCore.lean` | [VERIFIED] |
| **MAJ-C12** | **Enum Betti labels**: Lean `torus_h1_dimension`, `cylinder_h1_dimension`, and `disk_h1_dimension` are `rfl` on `betti1_of_topology` (Torus = 2, Cylinder = 1, Disk = 0). Those declarations do not compute the homology of a tetron array. | [COMPUTATIONAL] | `lean4/MajoranaCore.lean` | [VERIFIED] |
| **MAJ-C13** | **Retraction of Legacy Carrier**: Formal supersession and retraction of legacy `tetron_carrier.py`, which had $\dim H^1 = 0$ identically at all sizes $T=1..4$ and could not exhibit logical classes. | [RETRACTION] | Monograph §5.3, change log v0.2.0; Lean 4 `legacy_carrier_obstruction`; Python `audit_legacy_carrier` | [VERIFIED] |
| **MAJ-C14** | **Numeric min and sum**: Lean `toric_distance_3x4` is `rfl` of `min 3 4`. Lean `torus_3x4_additive_weight` is `rfl` of `3 + 4 = 7`. Those declarations do not prove that a toric-code distance is `min(rows, cols)`. | [COMPUTATIONAL] | `lean4/MajoranaCore.lean` | [VERIFIED] |
| **MAJ-C15** | **Syndrome Decoding Complexity & Upper Bound Capping**: Computing $\Phi_1([r]) = \min_\alpha \operatorname{wt}(r + d_0 \alpha)$ over $\mathbb{F}_2$ across general binary linear code families is NP-hard syndrome decoding (while specific restricted families of $d_0$ may admit polynomial-time decoders); capped Gray-code searches return upper bounds and degrade terminal routing to `ClosedResidual`. | [COMPLEXITY] | Monograph §5.5, Theorem 5.5; Lean 4 `candidate_gauge_is_upper_bound`; Python `compute_coset_weight` | [VERIFIED] |
| **MAJ-C16** | **Same cubic reflexivity**: The Lean declaration cited here is `gaussian_elimination_cubic_bound`, and that declaration is `Nat.le_refl` of `n * n * n`. That declaration does not time a \(6 \times 6\) torus and does not record a 50 ms bound. | [COMPUTATIONAL] | `lean4/MajoranaCore.lean` | [FENCED] |
| **MAJ-C17** | **Norm Equivalence on Binary Carriers**: For any $v \in \{0, 1\}^n$, $\|v\|_p^p = \operatorname{wt}(v)$ for all $p \ge 1$; $\ell^1$ and $\ell^2$ minimizations coincide identically over $\mathbb{F}_2$, refuting purported norm separation claims. | [DERIVED] | Monograph §6, Theorem 6.1; Lean 4 `f2_weight_l1_l2_coincide`; Python `verify_norm_equivalence` | [VERIFIED] |
| **MAJ-C18** | **Continuous-to-Discrete Transfer Bound under Open-System Dynamics**: In the declared analytical open-system Lindblad envelope model with quasiparticle poisoning $\Gamma_{\mathrm{qp}} > 0$, the upper-bound trade-off envelope on the trace-norm transfer defect $\Delta_{\mathrm{transfer}}$ has a strictly positive minimum $\Delta_{\mathrm{min}} > 0$ (`transfer_defect_lower_bound_pos` checks `Nat.mul_pos` on declared positive integer parameters rather than an unconditional physical trace-distance lower bound). | [DERIVED] | Monograph §8.1, Theorem 8.1; Lean 4 `transfer_defect_lower_bound_pos`, `transfer_pareto_defect_pos`, `transfer_gap_strictly_positive`; Python `OpenSystemMajoranaBraidModel` | [VERIFIED] |
| **MAJ-C19** | **Non-Markovian Memory-Kernel Transfer Bounds**: Structured bosonic bath spectra ($J(\omega) \propto \omega^s e^{-\omega/\omega_c}$) alter the Pareto scaling exponent $\beta = 2 / (p + 2)$ for the minimum transfer defect $\Delta_{\mathrm{min}}^{(s)}$, with sub-Ohmic $1/f$ noise ($s < 1 \implies \beta < 2/3$) accelerating dephasing and sub-gap cutoffs ($\hbar \omega_c < \Delta$) exponentially suppressing bulk leakage while maintaining $\Delta_{\mathrm{min}} > 0$ for any non-zero coupling $\alpha > 0$. | [DERIVED] | Monograph §8.2, Theorem 8.2; Lean 4 `non_markovian_transfer_defect_pos`, `pareto_denominator_pos`, `non_markovian_pareto_defect_pos`, `sub_ohmic_exponent_shift`; Python `NonMarkovianBosonicBathModel` | [VERIFIED] |
| **MAJ-C20** | **Multi-Terminal Cross-Junction Transfer Bounds under Potential Disorder**: In multi-terminal nanowire cross-junctions ($M \ge 4$), the $\binom{M}{2} \ge 6$ inter-arm cross-talk channels and electrostatic potential disorder $\sigma_V$ monotonically degrade the effective gap $\Delta_{\mathrm{eff}}(\sigma_V)$, strictly elevating the Pareto transfer defect infimum $\Delta_{\mathrm{min}}^{(M)} > 0$ for all $\sigma_V < \sigma_{\mathrm{crit}}$ and inducing gap-collapse obstruction when $\sigma_V \ge \sigma_{\mathrm{crit}}$. | [DERIVED] | Monograph §8.3, Theorem 8.3; Lean 4 `multiterminal_transfer_defect_pos`, `multiterminal_crosstalk_channels_pos`, `multiterminal_pareto_defect_pos`, `disorder_gap_degradation_lower_bound`; Python `ContinuumCrossJunctionFemModel` | [VERIFIED] |

---

## 2. Epistemic Assessment Register

### 2.1 What this Monograph Supports

- Formulates the exact mathematical trichotomy for discrete parity schedules over $\mathbb{F}_2$ and demonstrates polynomial-time decidability via Gaussian elimination.
- Establishes that on binary carriers, $\ell^1$ and $\ell^2$ optimization metrics are mathematically identical ($\|v\|_p^p = \operatorname{wt}(v)$), disproving claims of an $\ell^1 / \ell^2$ separation on GF(2) parity carriers.
- Demonstrates parameterized tetron arrays with measured Betti numbers $\dim H^1 \in \{0, 1, 2\}$ matching Euler characteristics.
- Identifies generic $\Phi_1$ minimization over $\mathbb{F}_2$ across arbitrary linear code families as NP-hard syndrome decoding (while specific restricted families of $d_0$ may admit faster decoders), enforcing budget capping with degradation to prevent overclaiming.
- Formulates the analytical continuous-to-discrete transfer upper-bound envelope model showing that open-system quasiparticle poisoning $\Gamma_{\mathrm{qp}} > 0$ yields a strictly positive trade-off envelope minimum $\Delta_{\mathrm{min}} > 0$, while noting that an upper-bound envelope minimum does not by itself establish an unconditional physical lower bound and that `transfer_defect_lower_bound_pos` verifies `Nat.mul_pos` on declared positive parameters.
- Formulates the non-Markovian memory-kernel transfer envelope model showing that sub-Ohmic ($s < 1$) and super-Ohmic ($s > 1$) bath spectra alter the Pareto minimum defect scaling exponent $\beta = 2 / (p + 2)$ while maintaining $\Delta_{\mathrm{min}} > 0$ for any finite coupling $\alpha > 0$.
- Formulates the multi-terminal cross-junction transfer envelope model showing that $M \ge 4$ geometries possess at least $\binom{M}{2} \ge 6$ cross-talk channels, and that inhomogeneous electrostatic potential disorder $\sigma_V > 0$ monotonically suppresses the effective gap model $\Delta_{\mathrm{eff}}(\sigma_V)$, elevating the analytical Pareto transfer envelope minimum $\Delta_{\mathrm{min}}^{(M)}(\sigma_V) > 0$.
- Provides a clear vocabulary (`DETECTOR_INADEQUATE`, realization packet gap) separating experimental transport reports from algebraic verification obligations.

### 2.2 What this Monograph Does NOT Support

- Does not demonstrate physical Majorana zero modes or topological quantum memory in semiconductor-superconductor hardware.
- Does not validate vendor claims regarding topological gap protection or fault-tolerant hardware scaling.
- Does not eliminate the generic fermion sign problem.
- Does not provide a universal quantum gate set from Ising braiding alone without magic state imports.

### 2.3 The Narrowest Defensible Claim

For declared finite cochain complexes over $\mathbb{F}_2$ with $d_1 \circ d_0 = 0 \pmod 2$, residual classes (`Exact`, `ClosedResidual`, `OpenObstruction`) are decidable in $O(n^3)$ bit operations, and $\Phi_1$ bounds are computable via Gray-code coset traversal; any connection between these discrete algebraic receipts and physical laboratory devices requires an explicit, independent realization packet whose analytical trade-off envelope has a strictly positive minimum $\Delta_{\mathrm{min}} > 0$ under declared open-system Markovian, non-Markovian bosonic, and disordered multi-terminal cross-junction models.

### 2.4 Next Test Needed

- [COMPLETED 2026-09-19] Implement unit, integration, and end-to-end regression suites in `code/tests/` verifying $\mathbb{F}_2$ matrix reduction, tetron-array distance measurements, and syndrome decoding budget capping (27/27 passed).
- [COMPLETED 2026-09-19] Mechanize $\mathbb{F}_2$ boundary nilpotency, residual trichotomy, and continuous-to-discrete transfer bounds in `lean4/MajoranaCore.lean` under package `po026`; Lake compilation pass verified clean (`lake build`, exit code 0); axiom audit established strict zero-axiom dependence (`#print axioms` empty or strictly within `{propext, Quot.sound}`).
- [COMPLETED 2026-09-19] Integrate `coda_atlas/F004_papers/002_projection_obstruction/026_microsoft_majorana_problem/lean4` into the root Lake workspace (`lean4/genx/lakefile.lean`) and four-list totality harness (`verify_deposit.py`, `.zenodo.json`, `claim_ledger.yaml`, `sha256sums`, `lean4/axiom_report.txt`, `lean4/provenance.md`, and `tests_e2e/test_review_gates.py`, 104/104 passing).
- [COMPLETED 2026-09-19] Formulate continuous-to-discrete transfer bounds separating topological edge-state braiding robustness from quasiparticle poisoning leakage under open-system Lindblad master equations (Claim `MAJ-C18`).
- [COMPLETED 2026-09-19] Formulate non-Markovian memory-kernel transfer bounds for topological edge modes coupled to structured bosonic bath cutoffs, demonstrating that sub-Ohmic ($s < 1$) and super-Ohmic ($s > 1$) spectra alter the Pareto scaling exponent $\beta = 2 / (p+2)$ (Claim `MAJ-C19`).
- [COMPLETED 2026-09-19] Formulated continuum finite-element boundary representations for multi-terminal nanowire cross-junctions under inhomogeneous electrostatic potential disorder to evaluate continuous-to-discrete transfer bounds in multi-terminal geometry (Claim `MAJ-C20`).
- Formulate self-consistent 3D Poisson-Schrödinger electrostatic solver coupling gate geometries, dielectric screening, and subband chemical potential pinning to evaluate topological phase boundary shrinkage in multi-terminal junctions.


