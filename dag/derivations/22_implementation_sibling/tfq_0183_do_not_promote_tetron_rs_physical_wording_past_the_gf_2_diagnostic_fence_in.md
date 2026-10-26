# [TFQ-0183] Do not promote tetron.rs physical wording past the GF(2) diagnostic fence in

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `0511d25b-6430-5ce5-bb5e-3bcde17cf8e7`  
> **Parent Derivation**: [TFQ-0181](tfq_0181_keep_omega_majorana_a_gf_2_diagnostic_and_do_not_treat_it_as_an.md)

---

## 1. Abstract & Formal Statement

The counts are 4 modes, 4 channels and 1 island. Then 4 - 4 + 1 = 1. With those counts, (4 - 1) - (4 - 1) = 0. Also (1 + 1) mod 2 = 0, 4 * 2 = 8 and 8 mod 2 = 0. The mode count 4 is not 2.

### Governing Obligation
The 1-by-1 disk cell arithmetic above is the narrowed statement. A superconducting device, a physical Majorana zero mode, noise sweeps as an authority terminal, the GF(2) matrix rank of any larger grid, and the crate fence in lib.rs stay outside this statement. Do not promote tetron.rs physical wording past the GF(2) diagnostic fence in lib.rs.

---

## 2. Derivation Context & Mathematical Grounding

The standing claim is integer arithmetic on the count triple 4, 4, 1. It does not build a device. An earlier module, `CampaignTfq0183ImplementationSibling`, is not the standing statement. The independent checker also rebuilds one 1-by-1 disk and reports matrix ranks 3 and 1 and first Betti number 0; those ranks are not theorems of `CampaignTfq0183FourModeDisk`.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `lean4/CampaignTfq0183FourModeDisk.lean`:
  - `CampaignTfq0183FourModeDisk.counts`
  - `CampaignTfq0183FourModeDisk.eulerChar`
  - `CampaignTfq0183FourModeDisk.bettiArithmetic`
  - `CampaignTfq0183FourModeDisk.cornerParity`
  - `CampaignTfq0183FourModeDisk.fourNeTwo`

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
  - `lean4/CampaignTfq0183FourModeDisk.lean`
  - `code/rust/src/majorana/tetron.rs`
  - `code/rust/src/majorana/pauli_noise.rs`
  - `code/rust/src/majorana/noise_mc.rs`
  - `checks/independent/tfq-0183.py`
