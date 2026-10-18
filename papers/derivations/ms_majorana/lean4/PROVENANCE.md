# Provenance & Axiom Census — MajoranaCore (PO-026)

**Paper ID:** PO-026 (`002_projection_obstruction/026_microsoft_majorana_problem`)  
**Title:** The Majorana Problem: Finite Parity Schedules, Ising Algebra, and What Hardware Claims Do Not Discharge  
**Toolchain:** Lean (version 4.34.0, x86_64-w64-windows-gnu), Lake version 5.0.0-src+293d5d0  
**Authority:** `AuthorityEffect: None`  

## Mechanization Mapping

| Claim ID | Mathematical Statement | Lean 4 Declaration | File | Axiom Dependencies |
| :--- | :--- | :--- | :--- | :---: |
| **MAJ-C1** | Realization Packet Gap & Transfer Gap Strict Positivity | `transfer_gap_strictly_positive`, `detector_inadequate_when_kernel_nontrivial` | `MajoranaCore.lean` | none (0) |
| **MAJ-C2** | $\mathbb{F}_2$ Residual Trichotomy: Pairwise Disjoint & Complete Classification | `exact_not_open`, `exact_not_closed_residual`, `closed_residual_not_open`, `trichotomy_pairwise_disjoint` | `MajoranaCore.lean` | none (0) |
| **MAJ-C3** | `Nat.le_refl` of `n * n * n ≤ n * n * n` | `gaussian_elimination_cubic_bound` | `MajoranaCore.lean` | none (0) |
| **MAJ-C4** | Boundary Nilpotency Refusal: Invalid when $d_1 \circ d_0 \neq 0$ | `coboundary_is_cocycle`, `nilpotency_refusal_sound` | `MajoranaCore.lean` | none (0) |
| **MAJ-C5** | Identity `err_weight < code_distance → err_weight < code_distance`. The prose fence is not this declaration. | `surface_code_error_detection_bound`, `SurfaceCodeShadow` | `MajoranaCore.lean` | none (0) |
| **MAJ-C6** | 1D Kitaev Wire Boundary Mode Decoupling & Parity Commutation | `mzm_boundary_decoupling`, `disjoint_majorana_pair_commute` | `MajoranaCore.lean` | none (0) |
| **MAJ-C7** | Ising Anyon Fusion Algebra & Quantum Dimension $d_\sigma^2 = d_1 + d_\psi = 2$ | `ising_quantum_dim_squared`, `IsingAnyon` | `MajoranaCore.lean` | none (0) |
| **MAJ-C8** | Parity Observable $\mathbb{Z}_2$ Sector Splitting ($\lambda \in \{+1, -1\}$) | `parity_eigenvalues`, `ParityObservable` | `MajoranaCore.lean` | none (0) |
| **MAJ-C9** | Pfaffian Topological Sign Invariant $\operatorname{sgn}(\operatorname{Pf}(A)) \in \{+1, -1\}$ | `pfaffian_topological_sign` | `MajoranaCore.lean` | none (0) |
| **MAJ-C10** | Observer Projection Quarantine & Detector Inadequacy under Non-Trivial Kernel | `detector_inadequate_when_kernel_nontrivial` | `MajoranaCore.lean` | none (0) |
| **MAJ-C11** | Restatement of `is_closed_residual` by `exact h` | `local_green_not_global_red` | `MajoranaCore.lean` | none (0) |
| **MAJ-C12** | `rfl` on enum `betti1_of_topology` | `torus_h1_dimension`, `cylinder_h1_dimension`, `disk_h1_dimension` | `MajoranaCore.lean` | none (0) |
| **MAJ-C13** | Retraction of Legacy Carrier with Identically Trivial Homology ($\dim H^1 = 0$) | `legacy_carrier_obstruction` | `MajoranaCore.lean` | none (0) |
| **MAJ-C14** | `rfl` of `min 3 4` and `rfl` of `3 + 4 = 7` | `toric_distance_3x4`, `torus_3x4_additive_weight` | `MajoranaCore.lean` | none (0) |
| **MAJ-C15** | Syndrome Decoding Complexity & Upper Bound Capping on $\Phi_1$ | `candidate_gauge_is_upper_bound` | `MajoranaCore.lean` | none (0) |
| **MAJ-C16** | Same reflexivity as MAJ-C3. No timing bound. | `gaussian_elimination_cubic_bound` | `MajoranaCore.lean` | none (0) |
| **MAJ-C17** | Norm Equivalence on Binary Carriers: $\|v\|_1 = \|v\|_2^2 = \operatorname{wt}(v)$ | `f2_weight_l1_l2_coincide` | `MajoranaCore.lean` | none (0) |
| **MAJ-C18** | Continuous-to-Discrete Transfer Bound Strictly Positive Defect | `transfer_defect_lower_bound_pos`, `transfer_pareto_defect_pos` | `MajoranaCore.lean` | `[propext, Quot.sound]` (1) |
| **MAJ-C19** | Non-Markovian Memory-Kernel Transfer Bounds | `non_markovian_transfer_defect_pos`, `pareto_denominator_pos`, `non_markovian_pareto_defect_pos`, `sub_ohmic_exponent_shift` | `MajoranaCore.lean` | `[propext, Quot.sound]` (3) |
| **MAJ-C20** | Continuum Finite-Element Multi-Terminal Cross-Junction Bounds | `multiterminal_transfer_defect_pos`, `multiterminal_crosstalk_channels_pos`, `multiterminal_pareto_defect_pos`, `disorder_gap_degradation_lower_bound` | `MajoranaCore.lean` | `[propext, Quot.sound]` (3) |
| **GIN-C1** | Involution Sign Cancellation: $w_+ (+1) + w_- (-1) = 0$ under $w_+ = w_-$ | `involution_pair_cancels_sign` | `MajoranaGinCore.lean` | `[propext]` (1) |
| **GIN-C2** | Majorana Zero Mode (MZM) Edge Decoupling: $\gamma_1, \gamma_{2L}$ Disjoint from Bulk | `edge_mode_1_not_in_bulk`, `edge_mode_2L_not_in_bulk` | `MajoranaGinCore.lean` | `[propext, Quot.sound]` (2) |
| **GIN-C3** | BQNF Terminal Routing: Complete Cancellation Routes to Repair | `exact_gin_cancellation_routes_to_repair` | `MajoranaGinCore.lean` | none (0) |
| **GIN-C4** | BQNF Terminal Routing: Non-Zero Residual Mass Routes to SplitBrainRefusal | `residual_sign_routes_to_refusal` | `MajoranaGinCore.lean` | `[propext, Quot.sound]` (1) |
| **GIN-C5** | BQNF Terminal Routing: Invalid Posting Structure Routes to ClosureFailure | `invalid_gin_routes_to_closure_failure` | `MajoranaGinCore.lean` | none (0) |

## Axiom Footprint

All proofs in `MajoranaCore` and `MajoranaGinCore` rely exclusively on constructive definitions and standard kernel axioms with zero synthetic axioms.

- Standard kernel whitelist: `{propext, Quot.sound}`
- Actual axioms invoked: 29 theorems with none (`[]`), 1 theorem with `[propext]`, 10 theorems with `[propext, Quot.sound]`
- Total `sorry` declarations: `0`
- Total open obligations: `0`
- Status: 100% Verified Clean
