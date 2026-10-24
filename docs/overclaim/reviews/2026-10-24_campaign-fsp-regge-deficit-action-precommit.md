# Pre-Commit Claim Hygiene & Overclaim Review: `FSP-REGGE-DEFICIT-ACTION` (`TFQ-1212`)

- **Date**: 2026-10-24
- **Branch**: `campaign/fsp-regge-deficit-action`
- **Target Node**: `FSP-REGGE-DEFICIT-ACTION` (`TFQ-1212` / `FSP-DERIV-048`)
- **Stage**: `FERMION_SIGN`
- **Status**: `IMPORTED_ASSUMPTION` (`E1 -> E3`, `L4D`)
- **AuthorityEffect**: `None`

## 1. What It Supports
- `lean4/CampaignFspReggeDeficitAction.lean` (10 exported theorems, 0 `sorry`, standard axioms only, 6/6 semantic mutations killed) formalizes:
  - Heron / Cayley-Menger squared triangle area `heronAreaSq` and the `orthogonal_pentatope` hinge area classes (`heronAreaSq_symmetric_and_orthogonal_pentatope_hinges`).
  - Hinge deficit flatness and `reggeAction` bilinearity (`hingeDeficit_flat_sum_zero_and_reggeAction_bilinear`) and mixed-sign saddle curvature indefiniteness (`reggeAction_positive_vs_mixed_deficit_sign`).
  - Combinatorial face vector and Euler characteristic $\chi(\partial \Delta^5) = 2$ (`s4_boundary_delta5_face_counts_and_euler_characteristic`).
  - Cyclic holonomy telescoping for the discrete first Bianchi identity (`discrete_bianchi_cyclic_holonomy_telescoping`) and Schläfli variational reduction (`schlaefli_variation_reduces_regge_variation_to_area_term`).
  - Rational refinement bound predicate `defectBoundHolds` matching `code/rust/src/general_relativity/exact_regge/action.rs` (`defectBoundHolds_exact_rust_witnesses_and_zero_scale_limit`).
  - `GIN-C13` scope fences for fermion-sign independence (`regge_action_independent_of_fermion_occupation_fence`), Lorentzian half-turn phase sign reversal (`euclidean_vs_lorentzian_regge_phase_fence`), and `Nat` vs signed `ℚ` deficit cancellation (`flat_vertex_sum_vs_signed_cancellation_fence`).
- `checks/independent/fsp-regge-deficit-action.py` independently verifies all rational identities and scope fences with zero failures.

## 2. What It Does Not Support
- Does not derive continuum Einstein-Hilbert convergence under triangulation refinement (which remains an explicit literature import) or claim any fermion-sign consequence from Regge calculus (`GIN-C13`).

## 3. Narrowest Defensible Claim
- Within the finite rational simplicial model, `heronAreaSq`, `hingeDeficit`, `reggeAction`, and `defectBoundHolds` satisfy exact algebraic, combinatorial, and variational identities on $\partial \Delta^5$ and `orthogonal_pentatope`, while carrying no fermion-sign cancellation content (`GIN-C13`).

## 4. Next Test Needed
- Formalize the direct-sum Wheeler-DeWitt gauge cochain system on `FSP-DISCRETE-WDW-CONSTRAINT` (`TFQ-1213`) and test its spectrum and projection properties separately from thermal fermion Hamiltonians.
