# [TFQ-0033] Construct an explicit three-index color contraction before using a baryon singlet label

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `2e607c92-575b-5f49-b4d2-8ef9181506b8`  
> **Parent Derivation**: [TFQ-0032](tfq_0032_build_a_finite_meson_carrier_or_keep_meson_language_at_the_channel_name.md)

---

## 1. Abstract & Formal Statement

The antitriplet factor -2/3 is a two-index diquark channel, stored as antitriplet_diquark_casimir. A baryon color singlet would need a third tensor factor and an alternating contraction on three color indices. No such epsilon contraction is defined in the QCD control, in su_n.rs, or in the weighted generator list. The sextet factor +1/3 is likewise a two-quark channel. The obligation is to build that three-factor contraction explicitly, or to keep baryon language off this node. The diquark signs are a computational control of Casimir arithmetic only.

### Governing Obligation
Construct an explicit three-index color contraction before using a baryon singlet label.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems (`lean4/DiquarkAntitripletChannel.lean`)
- `DiquarkAntitripletChannel.su3_qq_diquark_casimir_channels`: Proves `antitripletDiquarkCasimir = -2/3`, `sextetDiquarkCasimir = 1/3`, `3 * 3 = 3 + 6`, and `3 * (-2/3) + 6 * (1/3) = 0`.
- `DiquarkAntitripletChannel.diquark_to_qqbar_singlet_half_strength_rule`: Proves `-2/3 = (1/2) * (-4/3)` and `c2Antitriplet ≠ 0 ∧ c2Sextet ≠ 0`.
- `DiquarkAntitripletChannel.su3_three_quark_dimension_decomposition`: Proves `3 * 3 * 3 = 27 = 1 + 8 + 8 + 10`.
- `DiquarkAntitripletChannel.levi_civita_3d_antisymmetry_and_six_nonzero_permutations`: Proves total antisymmetry and diagonal vanishing of `eps3`.
- `DiquarkAntitripletChannel.levi_civita_contracted_square_and_norm_six`: Proves `eps3NormSq = 6` and `eps3Contract2 i i' = 2 δ_{ii'}`.
- `DiquarkAntitripletChannel.three_index_epsilon_contraction_equals_det3`: Proves `baryonEpsilonContract u v w = det3Color u v w` and `baryonEpsilonContract R G B = 1`.
- `DiquarkAntitripletChannel.baryon_contraction_vanishes_on_identical_color_states`: Proves Pauli exclusion and pairwise swap antisymmetry.
- `DiquarkAntitripletChannel.baryon_singlet_total_pairwise_casimir_equals_minus_two`: Proves `3 * (-2/3) = -2 = (0 - 3 * C_2(3))/2`.
- `DiquarkAntitripletChannel.two_index_diquark_not_three_index_baryon_singlet_fence`: Proves `C(3, 2) = 3 ≠ 1 = C(3, 3)` and `c2Antitriplet ≠ 0`.
- `DiquarkAntitripletChannel.tfq0033_baryon_contraction_scope_ledger_fence`: Audits `Tfq0033ScopeLedger`.

### Independent Python Verification (`checks/independent/tfq-0033.py`)
- Executes `839` exact rational (`fractions.Fraction`) and combinatorial checks across `SU(3)` diquark Casimir channels, 3-index Levi-Civita `ε_{ijk}` antisymmetry and contractions, `baryon_epsilon_contract == det3_color`, Pauli exclusion, Hypothesis property tests, and 6 negative-control mutation kills (`0` failures).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0034](tfq_0034_keep_the_baryon_and_tetraquark_rows_labeled_as_channel_decompositions_not.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
