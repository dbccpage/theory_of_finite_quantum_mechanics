# [TFQ-0032] Build a finite meson carrier or keep meson language at the channel-name

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `8f9d608e-2023-5d57-9713-3b278483823d`  
> **Parent Derivation**: [TFQ-0031](tfq_0031_do_not_treat_the_casimir_ratio_table_as_a_proof_of_linear_confinement.md)

---

## 1. Abstract & Formal Statement

The meson-side output of QM-221 is the pair of channel coefficients -4/3 and +1/6 on a quark-antiquark color decomposition. The Rust fields singlet_channel_casimir and octet_channel_potential_factor store those rationals. There is no finite Hilbert space of spatial meson orbitals, no relative wavefunction, and no mass operator in qcd_beta0_wilson_confinement_control.rs. Calling the attractive sign a meson composite would add structure the control does not build. The obligation is a separate finite composite, with a declared carrier and a color contraction, before a meson label is used as more than a channel name.

### Governing Obligation
Build a finite meson carrier or keep meson language at the channel-name layer.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems (`lean4/CampaignTfq0032FiniteQcd.lean`)
- `CampaignTfq0032FiniteQcd.suN_qqbar_casimir_channel_formulas`: Proves `suNFundCasimir 3 = 4/3`, `suNAdjCasimir 3 = 3`, `singletChannelFactor 3 = -4/3`, and `adjointChannelFactor 3 = 1/6`.
- `CampaignTfq0032FiniteQcd.su3_qqbar_dimension_and_weighted_trace_sum_zero`: Proves `3 * 3 = 1 + 8` and `1 * (-4/3) + 8 * (1/6) = 0`.
- `CampaignTfq0032FiniteQcd.singlet_attractive_vs_octet_repulsive_sign_dichotomy`: Proves `singletChannelFactor 3 < 0`, `0 < adjointChannelFactor 3`, and ratio `-8`.
- `CampaignTfq0032FiniteQcd.su2_vs_su3_qqbar_casimir_channel_contrast`: Contrasts `SU(2)` (`-3/4, +1/4`) with `SU(3)` (`-4/3, +1/6`).
- `CampaignTfq0032FiniteQcd.color_contraction_projector_idempotence_and_orthogonality`: Proves trace preservation, octet tracelessness, completeness, idempotence, and orthogonality of `singletProj` and `octetProj`.
- `CampaignTfq0032FiniteQcd.finite_meson_composite_carrier_dimension`: Proves `mesonCarrierDim 3 2 L d = 36 * L^d`.
- `CampaignTfq0032FiniteQcd.meson_mass_operator_requires_spatial_kinetic_and_potential_terms_fence`: Proves that non-zero spatial hopping `t ≠ 0` alters `mesonRadialHamDet` at fixed channel Casimir.
- `CampaignTfq0032FiniteQcd.channel_casimir_ratio_not_spatial_wavefunction_fence`: Contrasts fixed channel rationals with `L^3` spatial carrier growth.
- `CampaignTfq0032FiniteQcd.pseudoscalar_vs_vector_hyperfine_splitting_requires_spin_operator_fence`: Proves spin-0/spin-1 degeneracy at `deltaSS = 0` and splitting `deltaSS > 0`.
- `CampaignTfq0032FiniteQcd.tfq0032_meson_channel_scope_ledger_fence`: Audits `Tfq0032ScopeLedger`.

### Independent Python Verification (`checks/independent/tfq-0032.py`)
- Executes `3288` exact rational (`fractions.Fraction`) checks across `SU(N)` `q q̄` channel Casimirs, `3 × 3` color contraction projectors, `36 * L^d` composite carrier decompositions, radial mass operator determinants, spin-hyperfine splittings, Hypothesis property tests, and 6 negative-control mutation kills (`0` failures).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0033](tfq_0033_construct_an_explicit_three_index_color_contraction_before_using_a_baryon_singlet_label.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
