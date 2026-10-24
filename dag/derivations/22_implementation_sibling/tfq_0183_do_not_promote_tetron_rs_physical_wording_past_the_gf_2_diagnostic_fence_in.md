# [TFQ-0183] Do not promote tetron.rs physical wording past the GF(2) diagnostic fence in

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `0511d25b-6430-5ce5-bb5e-3bcde17cf8e7`  
> **Parent Derivation**: [TFQ-0181](tfq_0181_keep_omega_majorana_a_gf_2_diagnostic_and_do_not_treat_it_as_an.md)

---

## 1. Abstract & Formal Statement

Tetron wording in the crate outruns the diagnostic fence and must not be promoted. src/tetron.rs says a tetron is a 2-cell, one superconducting island with four Majorana zero modes, and it assigns C0 to modes, C1 to parity channels, and C2 to islands. src/lib.rs, which owns the crate fence, says the playground does not claim physical Majorana modes. The obligation is to keep the tetron array inside the GF(2) schedule and to withhold any hardware reading. Noise modules noise_mc.rs and pauli_noise.rs are present in the source list; their sweeps are not an authority terminal either.

### Governing Obligation
Do not promote tetron.rs physical wording past the GF(2) diagnostic fence in lib.rs.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Exact `GF(2)` Cellular Homology of `build_tetron_array` (`tetron.rs`)**: For any $R, C \ge 2$, `build_tetron_array(R, C, topology)` builds a $\mathbb{F}_2$ chain complex $C_2 \xrightarrow{d_1} C_1 \xrightarrow{d_0} C_0$ with $d_1 \circ d_0 = 0 \pmod 2$, $\operatorname{rank}_{\mathbb{F}_2}(d_0) = |C_0| - 1$, $\chi(\text{Disk}) = 1, \chi(\text{Cylinder}) = 0, \chi(\text{Torus}) = 0$, and $\dim H_1 = 0, 1, 2$ for `Disk`, `Cylinder`, `Torus` respectively.
- **Hardware Wording Withheld by Crate `GF(2)` Diagnostic Fence**: Although `Topology::hardware_reading` and comments in `tetron.rs` assign `C0` to Majorana zero modes, `C1` to parity channels, and `C2` to superconducting islands, `TetronReport.authority_effect = "None"` and the crate fence keep the carrier strictly within the $\mathbb{F}_2$ chain-complex diagnostic schedule.
- **Noise Sweeps Are Not Authority Terminals (`noise_mc.rs`, `pauli_noise.rs`, `majorana_noise_sweep.py`)**: `LocalMajoranaNoise` ($K^T = -K, K_{ii} = 0$ over $\mathbb{Q}$) and `noise_mc_planar_grid` (3-way `GF2ScheduleStatus` partition with `authority_effect = "None"`) are diagnostic sweeps and not authority terminals.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `lean4/CampaignTfq0183ImplementationSibling.lean`:
  - `CampaignTfq0183ImplementationSibling.tetron_disk_cylinder_torus_euler_and_betti_formulas`
  - `CampaignTfq0183ImplementationSibling.tetron_boundary_squares_to_zero_over_gf2`
  - `CampaignTfq0183ImplementationSibling.tetron_gf2_ranks_and_first_betti_numbers`
  - `CampaignTfq0183ImplementationSibling.local_majorana_noise_skew_symmetry_and_zero_diagonal`
  - `CampaignTfq0183ImplementationSibling.noise_mc_schedule_partition_conservation`
  - `CampaignTfq0183ImplementationSibling.tetron_hardware_reading_withheld_by_gf2_diagnostic_fence`
  - `CampaignTfq0183ImplementationSibling.noise_sweeps_are_not_authority_terminals_fence`
  - `CampaignTfq0183ImplementationSibling.missing_tetron_carrier_py_recorded_and_repaired_fence`
  - `CampaignTfq0183ImplementationSibling.gf2_cell_incidence_is_not_superconducting_device_proof_fence`
  - `CampaignTfq0183ImplementationSibling.tfq0183_tetron_gf2_diagnostic_and_noise_scope_ledger_fence`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `code/rust/src/majorana/tetron.rs`:
  - `build_tetron_array`
- `code/rust/src/wdp/lib.rs`:
  - `carrier_manifest`
- `code/rust/src/majorana/noise_mc.rs`:
  - `noise_mc_planar_grid`
- `code/rust/src/majorana/pauli_noise.rs`:
  - `LocalMajoranaNoise::from_rows`

### Python Oracles & Numerical Evaluators
- `code/python/src/majorana/majorana_noise_sweep.py`:
  - `DeterministicRationalNoiseGenerator`
- `checks/independent/tfq-0183.py`:
  - `run_all_checks`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `lean4/CampaignTfq0183ImplementationSibling.lean`
  - `code/rust/src/majorana/tetron.rs`
  - `code/rust/src/majorana/pauli_noise.rs`
  - `code/rust/src/majorana/noise_mc.rs`
  - `checks/independent/tfq-0183.py`
