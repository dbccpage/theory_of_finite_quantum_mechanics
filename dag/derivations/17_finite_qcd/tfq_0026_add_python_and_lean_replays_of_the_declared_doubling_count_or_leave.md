# [TFQ-0026] Add Python and Lean replays of the declared doubling count, or leave

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `03e30d86-3d2e-5196-9cae-e241acf96041`  
> **Parent Derivation**: [TFQ-0025](tfq_0025_do_not_let_a_12_decimal_print_authorize_beta0_or_the_creutz_identity.md)

---

## 1. Abstract & Formal Statement

lattice_dirac_doubling.rs declares a Euclidean Clifford family, a period N at least 3, and a rational Wilson coefficient r. The naive operator is the symmetric difference with gamma_mu, and its symbol i sum gamma_mu sin k_mu vanishes at corners k in {0, pi}^d. For even N and periodic boundaries, naive_species_count is 2^d before spin multiplicity. The file states that these counts are computed on declared lattices and that no continuum limit is taken. Carrier dimension above 128 is refused. No matching Python use case was found under 006_finite_qm/python, and FiniteQM.lean has no lattice Dirac theorem.

### Governing Obligation
Add Python and Lean replays of the declared doubling count, or leave the obstruction as Rust-only.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems (`lean4/LatticeDiracDoubling.lean`)
- `LatticeDiracDoubling.euclidean_clifford_anticommutator_relations`: Proves `γ_a² = I₂` and `{γ_a, γ_b} = 0` (`a ≠ b`) over `ℤ[i]`.
- `LatticeDiracDoubling.naive_symmetric_difference_vanishes_at_zero_and_pi_modes`: Proves the 1D symmetric difference stencil vanishes on both `k = 0` and `k = π` modes.
- `LatticeDiracDoubling.even_vs_odd_period_pi_mode_periodicity`: Proves `axisPeriodicZeroModes (2 * m) = 2` and `axisPeriodicZeroModes (2 * m + 1) = 1`.
- `LatticeDiracDoubling.naive_species_count_values_1d_to_4d`: Proves `naiveSpeciesCount d = 2, 4, 8, 16` for `d = 1, 2, 3, 4` and doubler excess `15` in `4D`.
- `LatticeDiracDoubling.wilson_term_lifts_nonzero_pi_corners`: Proves `wilsonCornerMass 0 r 0 = 0` and `0 < wilsonCornerMass 0 r c` for `r > 0, c ≥ 1`.
- `LatticeDiracDoubling.wilson_critical_mass_selects_corner_shell`: Proves `wilsonCornerMass (-2 * r * c0) r c = 0 ↔ c = c0` for `r ≠ 0`.
- `LatticeDiracDoubling.carrier_dimension_admission_guard_128`: Proves admission for `(2,4,2)` (`32 ≤ 128`) and `(2,4,3)` (`128 ≤ 128`) and refusal for `(4,4,3)` (`256 > 128`) and `(2,2,2)` (`N = 2 < 3`).
- `LatticeDiracDoubling.wilson_scalar_mass_breaks_gamma5_anticommutativity_fence`: Proves `{w I₂, γ₅} ≠ 0` for `w ≠ 0`.
- `LatticeDiracDoubling.finite_brillouin_grid_cardinality_fence`: Proves `3^4 = 81`, `4^3 = 64`, and `2^3 < 4^3`.
- `LatticeDiracDoubling.tfq0026_tri_language_replay_scope_ledger_fence`: Audits the tri-language replay and no-continuum-limit ledger.

### Independent Python Verification (`checks/independent/tfq-0026.py`)
- Executes `3075` exact Gaussian-integer, combinatorial, and rational (`fractions.Fraction`) checks across Euclidean Clifford anticommutators, `2^d` species counts, Wilson corner mass lifting, `MAX_CARRIER_DIMENSION = 128` admission guards, Hypothesis property tests, and 6 negative-control mutation kills (`0` failures).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0027](tfq_0027_do_not_cite_the_three_cycle_charge_doubling_file_as_the_lattice_dirac_obstruction.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
