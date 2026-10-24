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
- **`SU(2)_k` Racah Gauge vs. Absent `su3_level.rs`**:
  - In `code/rust/src/fusion_categories/su2_level.rs`, `su2_level` constructs `SU(2)_k` ribbon fusion categories for `1 <= k <= 6` (`MAX_LEVEL = 6`) over cyclotomic fields of root order `8 * (k + 2)` (`24..64`) with `k + 1` simple labels `a = 0..k` (`a = 2j`) and central charge `3k / (k + 2)`.
  - At `k = 3`, the integer-spin sector `{0, 2}` (`2 ⊗ 2 = 0 ⊕ 2`) has `q`-Racah associator `F^{[2,2,2,2]} = [[φ - 1, -1], [1 - φ, 1 - φ]]` over `ℚ(φ)` (`φ^2 = 1 + φ`). Under the Euclidean inner product `G = I`, `(F^T F)_{00} = 4 - 2φ ≠ 1` and `(F^T F)_{02} = 3 - 2φ ≠ 0` (`!model.category().is_unitary().unwrap()`), whereas under the diagonal tree metric `G = diag(φ, 1 + φ)` (`associator_metrics`), `F^T G F = G`.
  - `SU(2)_k` quantum dimensions are not the `SU(3)_c` Casimir invariants `C_F = 4/3` or `C_A = 3`, `SU(2)_k` labels are rank-1 self-dual (`a* = a`, count `k + 1`) rather than rank-2 `SU(3)_k` Dynkin weights `(λ_1, λ_2)` (`(1, 0)* = (0, 1) ≠ (1, 0)`, count `(k + 1)(k + 2) / 2`), and `su3_level.rs` is absent from `code/rust/src/fusion_categories/`.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignTfq0044FiniteTopological.lean::CampaignTfq0044FiniteTopological.su2_level_rank_and_root_order_bounds`](../../lean4/CampaignTfq0044FiniteTopological.lean)
- [`lean4/CampaignTfq0044FiniteTopological.lean::CampaignTfq0044FiniteTopological.su2_level_central_charge_and_level3_fibonacci_subring`](../../lean4/CampaignTfq0044FiniteTopological.lean)
- [`lean4/CampaignTfq0044FiniteTopological.lean::CampaignTfq0044FiniteTopological.qphi_golden_ratio_identities`](../../lean4/CampaignTfq0044FiniteTopological.lean)
- [`lean4/CampaignTfq0044FiniteTopological.lean::CampaignTfq0044FiniteTopological.racah_level3_fibonacci_f_matrix_not_euclidean_orthonormal`](../../lean4/CampaignTfq0044FiniteTopological.lean)
- [`lean4/CampaignTfq0044FiniteTopological.lean::CampaignTfq0044FiniteTopological.racah_level3_fibonacci_f_matrix_weighted_metric_unitarity`](../../lean4/CampaignTfq0044FiniteTopological.lean)
- [`lean4/CampaignTfq0044FiniteTopological.lean::CampaignTfq0044FiniteTopological.su2_level_quantum_dimensions_not_su3_casimirs_fence`](../../lean4/CampaignTfq0044FiniteTopological.lean)
- [`lean4/CampaignTfq0044FiniteTopological.lean::CampaignTfq0044FiniteTopological.su2_weight_lattice_rank1_not_su3_rank2_color_fusion_fence`](../../lean4/CampaignTfq0044FiniteTopological.lean)
- [`lean4/CampaignTfq0044FiniteTopological.lean::CampaignTfq0044FiniteTopological.su2_vs_su3_level_simple_object_count_separation`](../../lean4/CampaignTfq0044FiniteTopological.lean)
- [`lean4/CampaignTfq0044FiniteTopological.lean::CampaignTfq0044FiniteTopological.su2_level_budget_and_field_refusal_predicates`](../../lean4/CampaignTfq0044FiniteTopological.lean)
- [`lean4/CampaignTfq0044FiniteTopological.lean::CampaignTfq0044FiniteTopological.tfq0044_su2_level_scope_ledger_fence`](../../lean4/CampaignTfq0044FiniteTopological.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/fusion_categories/su2_level.rs::MAX_LEVEL`](../../code/rust/src/fusion_categories/su2_level.rs)
- [`code/rust/src/fusion_categories/su2_level.rs::quantum_integer`](../../code/rust/src/fusion_categories/su2_level.rs)
- [`code/rust/src/fusion_categories/su2_level.rs::associator_metrics`](../../code/rust/src/fusion_categories/su2_level.rs)
- [`code/rust/src/fusion_categories/su2_level.rs::su2_level`](../../code/rust/src/fusion_categories/su2_level.rs)
- [`code/rust/src/fusion_categories/su2_level.rs::racah_formula_replays_pentagon_hexagons_and_verlinde_through_maximum_level`](../../code/rust/src/fusion_categories/su2_level.rs)
- [`code/rust/src/fusion_categories/su2_level.rs::level_three_has_actual_fibonacci_subcategory_and_nonorthonormal_gauge`](../../code/rust/src/fusion_categories/su2_level.rs)
- [`code/rust/src/fusion_categories/su2_level.rs::unsupported_field_and_unbounded_level_are_typed_refusals`](../../code/rust/src/fusion_categories/su2_level.rs)

### Python Oracles & Numerical Evaluators
- [`checks/independent/tfq-0044.py::run_all_checks`](../../checks/independent/tfq-0044.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0045](tfq_0045_admit_an_exchange_only_after_the_exact_inverse_check_and_do_not.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
