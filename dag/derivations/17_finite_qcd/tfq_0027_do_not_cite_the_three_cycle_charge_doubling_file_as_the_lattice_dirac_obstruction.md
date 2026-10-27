# [TFQ-0027] Do not cite the three-cycle charge-doubling file as the lattice Dirac obstruction

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `10ab5fdb-fa38-5177-aed5-d92ace696890`  
> **Parent Derivation**: [TFQ-0026](tfq_0026_add_python_and_lean_replays_of_the_declared_doubling_count_or_leave.md)

---

## 1. Abstract & Formal Statement

wilson_species_count in the same file counts corners where the rational expression mass + 2*r*(number of pi components) is zero, with no trigonometric approximation. The header states that the Wilson term vanishes only at k=0 and anticommutes with no chirality matrix gamma_*. zero_mode_count is the kernel dimension s*N^d minus exact rank over Q(i) for a dense operator that must fit under MAX_CARRIER_DIMENSION. Even-N antiperiodic twists return zero species. IntegralRefinementC3C6.lean covers charge doubling on a three-cycle refined to six vertices. That file is not a stand-in for this lattice Dirac obstruction.

### Governing Obligation
Do not cite the three-cycle charge-doubling file as the lattice Dirac obstruction.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems (`lean4/WilsonSpeciesCount.lean`)
- `WilsonSpeciesCount.wilson_species_count_shell_selection`: Proves exact rational 4D `wilsonSpeciesCount4D` selects binomial shells `1, 4, 6, 4, 1` at critical masses `m = 0, -1, -2, -3, -4` for `r = 1/2`.
- `WilsonSpeciesCount.wilson_term_vanishes_only_at_origin_corner`: Proves `2 * r * c = 0 ↔ c = 0` for `r > 0`.
- `WilsonSpeciesCount.wilson_scalar_term_anticommutes_with_no_gamma_generator`: Proves `{w I₂, γ_a} ≠ 0` for `a ∈ {1, 2, 5}` and `w ≠ 0`.
- `WilsonSpeciesCount.zero_mode_count_rank_nullity_formula`: Proves `zeroModeCount s N d rank + rank = s * N^d` and 1D `N = 4` kernel transitions (`4 → 2 → 0`).
- `WilsonSpeciesCount.antiperiodic_twist_excludes_zero_and_pi_corners`: Proves `(2 * n + 1) % 2 = 1`, `2 * n + 1 ≠ 0`, and `2 * n + 1 ≠ 2 * m`.
- `WilsonSpeciesCount.even_n_periodic_vs_antiperiodic_species_contrast`: Proves `16` vs. `0` in `4D` and `8` vs. `0` in `3D`.
- `WilsonSpeciesCount.c3_to_c6_naive_duplication_vs_block_last_refinement`: Imports `IntegralRefinementC3C6` and proves `charge6 (naiveDuplicate v) = 2 * charge3 v` and `charge6 (blockLastRefine v) = charge3 v`.
- `WilsonSpeciesCount.c3_c6_charge_refinement_not_lattice_dirac_obstruction_fence`: Proves `2 ≠ 16` (`C₃ → C₆` scalar duplication factor vs. `4D` Dirac corner count).
- `WilsonSpeciesCount.max_carrier_dimension_128_dense_operator_fence`: Proves `MAX_CARRIER_DIMENSION = 128` admission/refusal.
- `WilsonSpeciesCount.tfq0027_scope_and_citation_fence`: Audits `Tfq0027ScopeLedger`.

### Independent Python Verification (`checks/independent/tfq-0027.py`)
- Executes `3404` exact rational (`fractions.Fraction`), Gaussian-integer, and row-echelon matrix rank checks across `wilson_species_count`, non-anticommutation with `γ_*`, periodic vs. antiperiodic `zero_mode_count`, `C₃ → C₆` non-equivalence, Hypothesis property tests, and 6 negative-control mutation kills (`0` failures).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0028](tfq_0028_state_the_beta0_window_as_rational_arithmetic_and_repeat_the_map_s_withheld.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
