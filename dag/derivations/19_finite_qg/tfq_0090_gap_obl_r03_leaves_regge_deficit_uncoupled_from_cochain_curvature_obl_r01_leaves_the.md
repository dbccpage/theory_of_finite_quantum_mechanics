# [TFQ-0090] GAP: OBL-R03 leaves Regge deficit uncoupled from cochain curvature; OBL-R01 leaves the

> **Stage**: `FINITE_QG` | **Status**: `GAP`  
> **UUID**: `59874bf3-7ed2-5385-bd6d-09d5de83bfd8`  
> **Parent Derivation**: [TFQ-0089](tfq_0089_exact_relational_witnesses_stay_on_a_finite_schema_a_smooth_metric_and.md)

---

## 1. Abstract & Formal Statement

PO-035 starts from a zero-container complex of comparisons and refuses an ambient continuum as a primitive. Its README marks master rows REQUIRES_CORRECTION: the light-cone story still owes a scaling gap, and the Regge row still owes a split between cochain curvature and metric deficit. What is finite is the comparison network and its holonomy words. What is not discharged is lattice-spacing descent and the claim that a hinge deficit equals curvature of a smooth manifold. That identification stays GAP. A finite complex is not quantum gravity.

Narrowed in Lean 4 (`lean4/CochainCurvatureReggeDeficit.lean`) and an independent Python verifier (`checks/independent/tfq-0090.py`) to three exact algebraic components and scope fences over $\mathbb{Q}$:
1. **Finite Tetrahedral Comparison Complex & Cochain Curvature ($d_1 \circ d_0 = 0$)**: on $K_4^{(2)}$ ($4$ vertices, $6$ oriented edges, $4$ oriented faces), proves exactness $d_1(d_0 \phi) = 0$ (`cochain_curvature_of_coboundary_zero`), gauge invariance $d_1(\omega + d_0 \phi) = d_1 \omega$ (`cochain_curvature_gauge_invariant`), linear amplitude scaling (`cochain_curvature_linear_scaling`), and the discrete Bianchi identity $F_{012} - F_{013} + F_{023} - F_{123} = 0$ (`tetrahedral_bianchi_identity`).
2. **`OBL-R03` Split Between Cochain Curvature and Regge Metric Deficit**: proves that uniform edge-length rescaling leaves equilateral Regge vertex deficits invariant while cochain curvature scales linearly (`obl_r03_scaling_dichotomy_cochain_vs_regge`); a metrically flat 6-equilateral-triangle hinge ($\epsilon_v = 0$) admits 1-cochains with arbitrary nonzero curvature $q \neq 0$ (`obl_r03_flat_hinge_with_arbitrary_cochain_curvature`); any pure-gauge 1-cochain ($d_1(d_0 \phi) = 0$) on the 4-vertex equilateral tetrahedron has strictly positive Regge deficit $T_{\text{full}}/2 > 0$ per vertex (`obl_r03_zero_cochain_curvature_with_positive_regge_deficit`); and the global Gauss-Bonnet sum of vertex deficits equals $2 T_{\text{full}} \neq 0$ whereas the oriented Bianchi cycle sum of cochain curvatures equals $0$ (`obl_r03_gauss_bonnet_vs_bianchi_sum_contrast`).
3. **`OBL-R01` Continuum Light-Cone Scaling Gap & Lattice-Spacing Fence**: proves that without an intrinsic scale-fixing law, any nonzero target light-cone speed $c_{\text{target}} \neq 0$ is reproduced by $a_x = c_{\text{target}} a_t$ (`obl_r01_any_light_cone_slope_by_spacing_calibration`, `obl_r01_spacing_calibration_injective`), varying $a_x \in \{1/2, 2/3, 1\}$ flips the causal character of $(N_t, N_x) = (2, 3)$ across timelike, null, and spacelike (`obl_r01_causal_character_depends_on_uncalibrated_spacing`), and the displacements $(3, 4)$ and $(5, 0)$ share Euclidean squared radius $25$ while requiring distinct Manhattan step counts $7 \neq 5$ (`obl_r01_manhattan_vs_euclidean_light_cone_anisotropy`).

### Governing Obligation
GAP: OBL-R03 leaves Regge deficit uncoupled from cochain curvature; OBL-R01 leaves the continuum scaling gap open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
- [`lean4/CochainCurvatureReggeDeficit.lean`](../../../lean4/CochainCurvatureReggeDeficit.lean):
  - `CochainCurvatureReggeDeficit.cochain_curvature_of_coboundary_zero`
  - `CochainCurvatureReggeDeficit.cochain_curvature_gauge_invariant`
  - `CochainCurvatureReggeDeficit.cochain_curvature_linear_scaling`
  - `CochainCurvatureReggeDeficit.tetrahedral_bianchi_identity`
  - `CochainCurvatureReggeDeficit.obl_r03_scaling_dichotomy_cochain_vs_regge`
  - `CochainCurvatureReggeDeficit.obl_r03_flat_hinge_with_arbitrary_cochain_curvature`
  - `CochainCurvatureReggeDeficit.obl_r03_zero_cochain_curvature_with_positive_regge_deficit`
  - `CochainCurvatureReggeDeficit.obl_r03_gauss_bonnet_vs_bianchi_sum_contrast`
  - `CochainCurvatureReggeDeficit.obl_r01_any_light_cone_slope_by_spacing_calibration`
  - `CochainCurvatureReggeDeficit.obl_r01_spacing_calibration_injective`
  - `CochainCurvatureReggeDeficit.obl_r01_causal_character_depends_on_uncalibrated_spacing`
  - `CochainCurvatureReggeDeficit.obl_r01_manhattan_vs_euclidean_light_cone_anisotropy`

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

### Python Oracles & Numerical Evaluators
- [`checks/independent/tfq-0090.py`](../../../checks/independent/tfq-0090.py) (`checks=1011 cochain=724 obl_r03=220 obl_r01=67 failures=0`)
- [`dag/derivations/independent/tfq-0090.md`](../independent/tfq-0090.md)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0091](tfq_0091_finite_loop_words_stay_on_the_declared_graph_continuum_connection_and_the.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
