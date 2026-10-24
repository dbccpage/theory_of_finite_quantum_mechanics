# [TFQ-0040] Close the missing Python or Lean twins before treating a control as

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `96015c4e-4be5-5cec-a7eb-3987ef2524a0`  
> **Parent Derivation**: [TFQ-0039](tfq_0039_cite_f002_s001_as_an_open_bridge_and_do_not_convert_the_finite.md)

---

## 1. Abstract & Formal Statement

The tri-language obligation is uneven. Rust, Python, and Lean agree on the rational QM-221 matrix, beta0, beta1, and Creutz identities, with Lean covering scalar Fierz identities rather than the 81-entry loop. QM-213 has Rust and Python but no Lean twin in FiniteQM.lean. Lattice Dirac doubling has Rust only. The Gribov diamond has Rust and a Lean rational shadow, and no Python twin was found under the finite_qm use cases. Hopf gauge data, su3_level.rs, and a three-quark color contraction are absent. F002.S001 stays an open bridge. A float print cannot authorize any exact identity listed here.

### Governing Obligation
Close the missing Python or Lean twins before treating a control as tri-language, and keep F002.S001 open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Tri-Language Coverage Gate**: A finite control is classified as `TriLanguageComplete` only when Rust, Python, and Lean twins are all present. Controls with missing twins (`QM-213` in `FiniteQM.lean`, `lattice_dirac_doubling.rs`, the Gribov diamond under `finite_qm/use_cases`, and absent `Hopf` / `su3_level.rs` / `QM-221` baryon contraction) are explicitly audited.
- **Explicit Lean 4 & Python Checkers for `QM-213`, `81`-Entry Fierz, and `3! = 6` Levi-Civita Contraction**: `lean4/CampaignTfq0040FiniteQcd.lean` and `checks/independent/tfq-0040.py` verify the `B_2(\mathbb{Q})` punctured-diamond holonomy split ($\mathrm{tr} = 5/2, \det = 1$ vs $I_2$), the $3^4 = 81$ two-quark color projector decomposition ($\mathrm{Tr}(P_{\mathrm{sextet}}) = 6, \mathrm{Tr}(P_{\mathrm{antitrip}}) = 3$), and the 3-color Levi-Civita contraction $\sum_{i,j,k} \varepsilon_{ijk}^2 = 6$, while keeping `F002.S001` an open bridge and rejecting float prints.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `lean4/CampaignTfq0040FiniteQcd.lean`:
  - `CampaignTfq0040FiniteQcd.qm221_casimir_fierz_scalar_and_81_entry_dimension_identities`
  - `CampaignTfq0040FiniteQcd.qm213_borel_punctured_diamond_artificial_vs_substantial_holonomy`
  - `CampaignTfq0040FiniteQcd.levi_civita_three_quark_color_singlet_contraction`
  - `CampaignTfq0040FiniteQcd.abj_and_gmo_color_octet_decuplet_identities`
  - `CampaignTfq0040FiniteQcd.gribov_diamond_klein_four_and_lattice_dirac_doubling_controls`
  - `CampaignTfq0040FiniteQcd.tri_language_coverage_gate_requires_all_three_twins_fence`
  - `CampaignTfq0040FiniteQcd.absent_hopf_su3_level_and_baryon_contraction_recorded_fence`
  - `CampaignTfq0040FiniteQcd.f002_s001_remains_open_bridge_fence`
  - `CampaignTfq0040FiniteQcd.float_print_cannot_authorize_exact_identity_fence`
  - `CampaignTfq0040FiniteQcd.tfq0040_tri_language_audit_and_f002_s001_scope_ledger_fence`
- `lean4/FiniteQM.lean`:
  - `FiniteQM.su3_casimir_and_channel_identities`
  - `FiniteQM.su3_fierz_diagonal_and_offdiagonal_identities`
  - `FiniteQM.qcd_beta0_asymptotic_freedom_window`
  - `FiniteQM.qcd_beta1_and_banks_zaks_fixed_point`
  - `FiniteQM.wilson_creutz_ratio_area_vs_perimeter`
  - `FiniteQM.su3_diagonal_klein_four_landau_gribov_copies`
  - `FiniteQM.spanning_tree_dfm_eliminates_gribov_copies`
- `lean4/FiniteQFTAndGravity.lean`:
  - `FiniteQFTAndGravity.abj_factor_closed`
  - `FiniteQFTAndGravity.abj_factor_values`
  - `FiniteQFTAndGravity.abj_rate_ratio`
  - `FiniteQFTAndGravity.gmo_octet`
  - `FiniteQFTAndGravity.gmo_decuplet_equal_spacing`

### Independent Python Verification
- `checks/independent/tfq-0040.py`:
  - `run_all_checks`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S001`
- **Primary Source Paths**:
  - `lean4/FiniteQM.lean`
  - `lean4/FiniteQFTAndGravity.lean`
  - `lean4/CampaignTfq0040FiniteQcd.lean`
  - `checks/independent/tfq-0040.py`
