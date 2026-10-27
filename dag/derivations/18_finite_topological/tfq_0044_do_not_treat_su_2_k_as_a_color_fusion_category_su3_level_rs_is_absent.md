# [TFQ-0044] Do not treat SU(2)_k as a color fusion category; su3_level.rs is absent

> **Stage**: `FINITE_TOPOLOGICAL` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `a224cd40-6e40-5b75-838c-95df3bd7e101`  
> **Parent Derivation**: [TFQ-0043](tfq_0043_keep_ribbon_charges_off_the_color_and_wilson_spine.md)

---

## 1. Abstract & Formal Statement

anyon_model.rs wraps a ribbon category after braided validation and a dimension check. Its SU(2)_k constructor uses the shared Racah gauge in omega_fusion_categories::su2_level, with a bounded pentagon and hexagon replay. That file warns the gauge is generally not orthonormal, so the F matrices must not be advertised as unitary in the ordinary inner product. Labels a=0..k are twice a spin, which is an SU(2) level family. There is no su3_level.rs beside su2_level.rs. An SU(2)_k anyon model is not the three-color matrix algebra, and its quantum dimensions are not C_F or C_A.

### Governing Obligation
Do not treat SU(2)_k as a color fusion category; su3_level.rs is absent.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems (`lean4/AnyonRibbonRacahGauge.lean`)
- `AnyonRibbonRacahGauge.su2_level_rank_and_root_order_bounds`: Proves `su2LevelRank k = k + 1` and `su2RootOrder k = 8 * (k + 2)` for `k = 1..6`.
- `AnyonRibbonRacahGauge.su2_level_central_charge_and_level3_fibonacci_subring`: Proves `su2CentralCharge k = (3 * k) / (k + 2)` for `k = 1..6` and level-3 Fibonacci fusion `2 ⊗ 2 = 0 ⊕ 2`.
- `AnyonRibbonRacahGauge.qphi_golden_ratio_identities`: Proves `φ^2 = 1 + φ` and `φ * (φ - 1) = 1` in `QPhi`.
- `AnyonRibbonRacahGauge.racah_level3_fibonacci_f_matrix_not_euclidean_orthonormal`: Proves `(F^T F)_{00} ≠ 1`, `(F^T F)_{02} ≠ 0`, and `F_{02} ≠ F_{20}` in the Euclidean inner product.
- `AnyonRibbonRacahGauge.racah_level3_fibonacci_f_matrix_weighted_metric_unitarity`: Proves exact weighted metric unitarity `F^T G F = G` and `det(F) = -1` in `QPhi`.
- `AnyonRibbonRacahGauge.su2_level_quantum_dimensions_not_su3_casimirs_fence`: Proves `C_F = 4/3` and `C_A = 3` are not `SU(2)_k` quantum dimensions.
- `AnyonRibbonRacahGauge.su2_weight_lattice_rank1_not_su3_rank2_color_fusion_fence`: Proves `SU(2)_k` labels are rank-1 self-dual whereas `SU(3)_k` weights are rank-2 non-self-dual.
- `AnyonRibbonRacahGauge.su2_vs_su3_level_simple_object_count_separation`: Proves `k + 1 < (k + 1)(k + 2)/2` for `k = 1..6`.
- `AnyonRibbonRacahGauge.su2_level_budget_and_field_refusal_predicates`: Proves budget and cyclotomic field refusal predicates.
- `AnyonRibbonRacahGauge.tfq0044_su2_level_scope_ledger_fence`: Audits `Tfq0044ScopeLedger`.

### Sovereign Rust Certifiers (`code/rust/src/fusion_categories/su2_level.rs`)
- `code/rust/src/fusion_categories/su2_level.rs::su2_level`
- `code/rust/src/fusion_categories/su2_level.rs::associator_metrics`
- `code/rust/src/fusion_categories/su2_level.rs::level_three_has_actual_fibonacci_subcategory_and_nonorthonormal_gauge`

### Independent Python Verification (`checks/independent/tfq-0044.py`)
- Executes `5933` exact rational and `ℚ(φ)` algebraic checks across `SU(2)_k` (`k = 1..6`) fusion rings, non-orthonormal Racah `F`-matrices vs. weighted metric unitarity, and `SU(2)_k` vs. `SU(3)_c`/`SU(3)_k` non-equivalence fences (`0` failures).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0045](tfq_0045_admit_an_exchange_only_after_the_exact_inverse_check_and_do_not.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
