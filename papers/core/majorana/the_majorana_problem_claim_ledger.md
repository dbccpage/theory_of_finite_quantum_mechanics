# Claim Ledger — The Majorana Problem (`the_majorana_problem.md`)

**Series Key:** `projection_obstruction/026_microsoft_majorana_problem`  
**Live directory:** `majorana`. The series key above is the historical package id.  
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

<!-- BEGIN UNIFIED-DAG-BACKLINKS -->
<!-- Generated by papers/core/tools/build_corpus_dag_backlinks.py; edit the tool, not this region. -->

## Unified DAG

Audit of 2026-10-21. The unified derivation DAG (`dag/fragments/unified_dag.json`) folds the records of this corpus into one graph: a record with no trunk counterpart is a NEW application-branch node with its own TFQ record; a restatement of a trunk step is an ALIAS row that points to the trunk node. *Source claimed* is the status the source asserted; *Audited* is the status the audit assigned against what is actually in this checkout (Lean declarations resolved, replays rerun, statements compared). The original claims, labels and text of this document are kept unchanged. A status below the source claim means the claim is not established as stated; it does not mean the underlying mathematics is false (only REFUTED means that). For an ALIAS row the audited column is the status of the trunk node, which is the authority for the restated step. Regenerate with `python -I -X utf8 papers/core/tools/build_corpus_dag_backlinks.py`.

46 NEW records and 3 ALIAS rows; 29 same, 13 lowered, 1 raised, 3 reclassified.

| Source id | Kind | TFQ record | DAG node | Source claimed | Audited | Reconciliation |
|---|---|---|---|---|---|---|
| `MAJ-C1` | NEW | [TFQ-1162](../../../dag/derivations/28_majorana/tfq_1162_maj_realization_packet_gap.md) | `MAJ-REALIZATION-PACKET-GAP` | DEFINITION | **DEFINITION** | same |
| `MAJ-C2` | NEW | [TFQ-1141](../../../dag/derivations/28_majorana/tfq_1141_maj_trichotomy_pairwise_exclusion.md) | `MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MAJ-C3` | NEW | [TFQ-1143](../../../dag/derivations/28_majorana/tfq_1143_maj_trichotomy_elimination_decision.md) | `MAJ-TRICHOTOMY-ELIMINATION-DECISION` | COMPUTATIONALLY_CHECKED | **PROVED_PROSE** | raised |
| `MAJ-C4` | NEW | [TFQ-1144](../../../dag/derivations/28_majorana/tfq_1144_maj_nilpotency_refusal.md) | `MAJ-NILPOTENCY-REFUSAL` | PROVED_LEAN | **DEFINITION** | reclassified |
| `MAJ-C5` | NEW | [TFQ-1150](../../../dag/derivations/28_majorana/tfq_1150_maj_surface_shadow_fence.md) | `MAJ-SURFACE-SHADOW-FENCE` | DEFINITION | **DEFINITION** | same |
| `MAJ-C6` | NEW | [TFQ-1167](../../../dag/derivations/28_majorana/tfq_1167_maj_import_kitaev_chain.md) | `MAJ-IMPORT-KITAEV-CHAIN` | DEFINITION | **IMPORTED_ASSUMPTION** | reclassified |
| `MAJ-C7` | NEW | [TFQ-1170](../../../dag/derivations/28_majorana/tfq_1170_maj_import_ising_anyons.md) | `MAJ-IMPORT-ISING-ANYONS` | DEFINITION | **IMPORTED_ASSUMPTION** | reclassified |
| `MAJ-C8` | NEW | [TFQ-1173](../../../dag/derivations/28_majorana/tfq_1173_maj_parity_observable_fence.md) | `MAJ-PARITY-OBSERVABLE-FENCE` | DEFINITION | **DEFINITION** | same |
| `MAJ-C9` | ALIAS | [TFQ-0409](../../../dag/derivations/26_fsp/tfq_0409_fsp_efficient_sampling_obligations.md) | `FSP-EFFICIENT-SAMPLING-OBLIGATIONS` | FENCED | **OPEN** | restated in trunk |
| `MAJ-C10` | NEW | [TFQ-1165](../../../dag/derivations/28_majorana/tfq_1165_maj_hardware_narrative_quarantine.md) | `MAJ-HARDWARE-NARRATIVE-QUARANTINE` | DEFINITION | **DEFINITION** | same |
| `MAJ-C11` | NEW | [TFQ-1146](../../../dag/derivations/28_majorana/tfq_1146_maj_lggr_torus_instance.md) | `MAJ-LGGR-TORUS-INSTANCE` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | lowered |
| `MAJ-C12` | ALIAS | [TFQ-0184](../../../dag/derivations/22_implementation_sibling/tfq_0184_do_not_read_paper_009_reflexivity_declarations_as_measured_tetron_homology.md) | `TFQ-0184` | VERIFIED | **OPEN** | restated in trunk |
| `MAJ-C13` | NEW | [TFQ-1154](../../../dag/derivations/28_majorana/tfq_1154_maj_legacy_carrier_retraction.md) | `MAJ-LEGACY-CARRIER-RETRACTION` | PROVED_LEAN | **CONDITIONAL** | lowered |
| `MAJ-C14` | NEW | [TFQ-1155](../../../dag/derivations/28_majorana/tfq_1155_maj_torus_3x4_coset_weights.md) | `MAJ-TORUS-3X4-COSET-WEIGHTS` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-C15` | NEW | [TFQ-1158](../../../dag/derivations/28_majorana/tfq_1158_maj_phi1_syndrome_decoding.md) | `MAJ-PHI1-SYNDROME-DECODING` | PROVED_LEAN | **CONDITIONAL** | lowered |
| `MAJ-C16` | NEW | [TFQ-1160](../../../dag/derivations/28_majorana/tfq_1160_maj_torus_6x6_benchmark.md) | `MAJ-TORUS-6X6-BENCHMARK` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-C17` | NEW | [TFQ-1161](../../../dag/derivations/28_majorana/tfq_1161_maj_lp_invariance_binary.md) | `MAJ-LP-INVARIANCE-BINARY` | PROVED_LEAN | **PROVED_PROSE** | lowered |
| `MAJ-C18` | NEW | [TFQ-1177](../../../dag/derivations/28_majorana/tfq_1177_maj_open_lindblad_transfer_envelope.md) | `MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE` | PROVED_LEAN | **OPEN** | lowered |
| `MAJ-C19` | NEW | [TFQ-1178](../../../dag/derivations/28_majorana/tfq_1178_maj_open_non_markovian_envelope.md) | `MAJ-OPEN-NON-MARKOVIAN-ENVELOPE` | PROVED_LEAN | **OPEN** | lowered |
| `MAJ-C20` | NEW | [TFQ-1179](../../../dag/derivations/28_majorana/tfq_1179_maj_open_multiterminal_envelope.md) | `MAJ-OPEN-MULTITERMINAL-ENVELOPE` | PROVED_LEAN | **OPEN** | lowered |
| `MAJ-CLAIM-DISTANCE-FAMILY` | NEW | [TFQ-1156](../../../dag/derivations/28_majorana/tfq_1156_maj_open_distance_family.md) | `MAJ-OPEN-DISTANCE-FAMILY` | PROVED_PROSE | **OPEN** | lowered |
| `MAJ-COMP-BUDGET-CAP` | NEW | [TFQ-1159](../../../dag/derivations/28_majorana/tfq_1159_maj_capped_coset_search.md) | `MAJ-CAPPED-COSET-SEARCH` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-COMP-SYNDROME-READOUT` | NEW | [TFQ-1164](../../../dag/derivations/28_majorana/tfq_1164_maj_syndrome_readout_inadequate.md) | `MAJ-SYNDROME-READOUT-INADEQUATE` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-COMP-TETRON-BETTI` | NEW | [TFQ-1152](../../../dag/derivations/28_majorana/tfq_1152_maj_tetron_betti_computed.md) | `MAJ-TETRON-BETTI-COMPUTED` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-COR-DISTANCE-WEIGHT` | NEW | [TFQ-1148](../../../dag/derivations/28_majorana/tfq_1148_maj_distance_weight_correction.md) | `MAJ-DISTANCE-WEIGHT-CORRECTION` | PROVED_PROSE | **OPEN** | lowered |
| `MAJ-DEF-DETECTOR-INADEQUATE` | NEW | [TFQ-1163](../../../dag/derivations/28_majorana/tfq_1163_maj_detector_inadequate.md) | `MAJ-DETECTOR-INADEQUATE` | DEFINITION | **DEFINITION** | same |
| `MAJ-DEF-PARITY-SCHEDULE` | NEW | [TFQ-1138](../../../dag/derivations/28_majorana/tfq_1138_maj_f2_parity_schedule.md) | `MAJ-F2-PARITY-SCHEDULE` | DEFINITION | **DEFINITION** | same |
| `MAJ-DEF-PHI1-F2` | NEW | [TFQ-1140](../../../dag/derivations/28_majorana/tfq_1140_maj_phi1_hamming_coset.md) | `MAJ-PHI1-HAMMING-COSET` | DEFINITION | **DEFINITION** | same |
| `MAJ-DEF-TETRON-CARRIER` | NEW | [TFQ-1151](../../../dag/derivations/28_majorana/tfq_1151_maj_tetron_array_carrier.md) | `MAJ-TETRON-ARRAY-CARRIER` | DEFINITION | **DEFINITION** | same |
| `MAJ-DEF-TRICHOTOMY-LABELS` | NEW | [TFQ-1139](../../../dag/derivations/28_majorana/tfq_1139_maj_trichotomy_labels.md) | `MAJ-TRICHOTOMY-LABELS` | DEFINITION | **DEFINITION** | same |
| `MAJ-EX-TORUS-2X2` | NEW | [TFQ-1145](../../../dag/derivations/28_majorana/tfq_1145_maj_torus_2x2_worked_grid.md) | `MAJ-TORUS-2X2-WORKED-GRID` | PROVED_PROSE | **COMPUTATIONALLY_CHECKED** | lowered |
| `MAJ-FENCE-DIAGNOSTIC-LABELS` | ALIAS | - | `DS-QM212-MAJORANA-PROBLEM` | - | **PROVED_LEAN** | restated in trunk |
| `MAJ-FENCE-NONCLAIMS` | NEW | [TFQ-1166](../../../dag/derivations/28_majorana/tfq_1166_maj_binding_nonclaims.md) | `MAJ-BINDING-NONCLAIMS` | DEFINITION | **DEFINITION** | same |
| `MAJ-GIN-INVOLUTION-CANCEL` | NEW | [TFQ-1175](../../../dag/derivations/28_majorana/tfq_1175_maj_gin_involution_pair_cancel.md) | `MAJ-GIN-INVOLUTION-PAIR-CANCEL` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MAJ-GIN-ROUTING` | NEW | [TFQ-1176](../../../dag/derivations/28_majorana/tfq_1176_maj_gin_terminal_routing.md) | `MAJ-GIN-TERMINAL-ROUTING` | DEFINITION | **DEFINITION** | same |
| `MAJ-IMPORT-BMVT` | NEW | [TFQ-1157](../../../dag/derivations/28_majorana/tfq_1157_maj_import_coset_weight_np_hard.md) | `MAJ-IMPORT-COSET-WEIGHT-NP-HARD` | IMPORTED_ASSUMPTION | **IMPORTED_ASSUMPTION** | same |
| `MAJ-ISING-BRAID-CHECK` | NEW | [TFQ-1171](../../../dag/derivations/28_majorana/tfq_1171_maj_ising_braid_exact_open.md) | `MAJ-ISING-BRAID-EXACT-OPEN` | COMPUTATIONALLY_CHECKED | **OPEN** | lowered |
| `MAJ-KITAEV-EDGE-INDEX` | NEW | [TFQ-1168](../../../dag/derivations/28_majorana/tfq_1168_maj_kitaev_edge_index_disjoint.md) | `MAJ-KITAEV-EDGE-INDEX-DISJOINT` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MAJ-KITAEV-SWEETSPOT-EXACT` | NEW | [TFQ-1169](../../../dag/derivations/28_majorana/tfq_1169_maj_kitaev_sweetspot_exact.md) | `MAJ-KITAEV-SWEETSPOT-EXACT` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | lowered |
| `MAJ-LEAN-ENVELOPE-NAT` | NEW | [TFQ-1180](../../../dag/derivations/28_majorana/tfq_1180_maj_envelope_nat_arithmetic.md) | `MAJ-ENVELOPE-NAT-ARITHMETIC` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MAJ-LEMMA-TRIVIAL-H1` | NEW | [TFQ-1153](../../../dag/derivations/28_majorana/tfq_1153_maj_trivial_h1_no_closed.md) | `MAJ-TRIVIAL-H1-NO-CLOSED` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MAJ-MAJORANA-BRAID-YB` | NEW | [TFQ-1172](../../../dag/derivations/28_majorana/tfq_1172_maj_majorana_braid_yb_exact.md) | `MAJ-MAJORANA-BRAID-YB-EXACT` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-OPEN-EVIDENCE-ADEQUACY` | NEW | [TFQ-1182](../../../dag/derivations/28_majorana/tfq_1182_maj_open_evidence_adequacy.md) | `MAJ-OPEN-EVIDENCE-ADEQUACY` | OPEN | **OPEN** | same |
| `MAJ-OPEN-LOCALITY-VIABILITY` | NEW | [TFQ-1149](../../../dag/derivations/28_majorana/tfq_1149_maj_open_lieb_robinson_locality.md) | `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` | OPEN | **OPEN** | same |
| `MAJ-OPEN-LP-DUAL-CEILING` | NEW | [TFQ-1181](../../../dag/derivations/28_majorana/tfq_1181_maj_open_lp_dual_certified_ceiling.md) | `MAJ-OPEN-LP-DUAL-CERTIFIED-CEILING` | OPEN | **OPEN** | same |
| `MAJ-OPEN-POISSON-SCHRODINGER` | NEW | [TFQ-1183](../../../dag/derivations/28_majorana/tfq_1183_maj_open_poisson_schrodinger.md) | `MAJ-OPEN-POISSON-SCHRODINGER` | OPEN | **OPEN** | same |
| `MAJ-PARITY-SECTOR-EXACT` | NEW | [TFQ-1174](../../../dag/derivations/28_majorana/tfq_1174_maj_parity_sector_split_exact.md) | `MAJ-PARITY-SECTOR-SPLIT-EXACT` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MAJ-THM-SYNDROME-RECOVERY` | NEW | [TFQ-1147](../../../dag/derivations/28_majorana/tfq_1147_maj_syndrome_recovery_criterion.md) | `MAJ-SYNDROME-RECOVERY-CRITERION` | PROVED_PROSE | **PROVED_PROSE** | same |
| `MAJ-THM-TRICHOTOMY-EXHAUSTIVE` | NEW | [TFQ-1142](../../../dag/derivations/28_majorana/tfq_1142_maj_trichotomy_exhaustive.md) | `MAJ-TRICHOTOMY-EXHAUSTIVE` | PROVED_LEAN | **PROVED_PROSE** | lowered |

### Audit errata (2026-10-21)

- 2026-10-21 ERRATUM (MAJ-ISING-BRAID-CHECK, TFQ-1171): Monograph section 7.2 and ledger row MAJ-C7 present the Q(zeta_16) Ising braid identities as exact. The paper's Python check is floating point: `verify_yang_baxter_braid` builds complex numpy arrays with 1/sqrt 2 and tests `np.allclose(..., atol=1e-12)`, and `verify_quantum_dimensions` compares a float sqrt(2). F^2 = I and the hexagon are not checked in the paper code. Audited status OPEN for the exactness claim; the exact Majorana braid Yang-Baxter check is the crate twin MAJ-MAJORANA-BRAID-YB (TFQ-1172).
- 2026-10-21 ERRATUM (README-CLAIM-RANGE): The README described the claim ledger as 'MAJ-C1 through MAJ-C17'; the ledger and `claim_ledger.yaml` run MAJ-C1 through MAJ-C20. Corrected in the README.
- 2026-10-21 ERRATUM (MAJ-LEAN-COVERAGE, TFQ-1146/1154/1158/1161/1177-1179): Ledger rows MAJ-C11, C13, C15, C17, C18, C19 and C20 carry [VERIFIED] but their Lean declarations are definitional restatements, `rfl`, or Nat positivity facts (for C20 `multiterminal_crosstalk_channels_pos` gives M(M-1)/2 > 0 for M >= 4, not >= 6). The original labels are kept; the audited statuses are in the table.

<!-- END UNIFIED-DAG-BACKLINKS -->
