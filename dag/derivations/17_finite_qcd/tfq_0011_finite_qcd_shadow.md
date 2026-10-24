# [TFQ-0011] Finite QCD shadow

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `171bfea4-4046-5794-a9e5-ae2e8572b427`  
> **Parent Derivation**: [TFQ-0009](../14_finite_gauge/tfq_0009_finite_gauge_cochain.md)

---

## 1. Abstract & Formal Statement

Finite QCD here means a finite non-abelian gauge datum, a Wilson loop on a finite complex, a beta0-style finite control, and an explicit gap where confinement in a continuum theory is not identified with that control. Lattice Dirac doubling is an obstruction to record, not a nuisance to hide. Python, Rust, and Lean 4 must separate an exact rational certificate from a float benchmark. A float benchmark cannot authorize the finite statement. Continuum QCD remains an open interface on F002.

### Governing Obligation
Carry a finite color, Wilson, and beta0 control without calling it continuum confinement.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Finite Color Casimir & Fierz Controls**: Over $\mathbb{Q}$, $\mathrm{SU}(3)$ color Casimir invariants ($C_2(3) = 4/3, C_2(8) = 3$), two-quark channel coefficients (singlet $-4/3 < 0$, antitriplet $-2/3 < 0$, octet $+1/6 > 0$, sextet $+1/3 > 0$), and Cartan Fierz weights ($1/3$ diagonal, $-1/6$ off-diagonal) are exact rational identities.
- **Finite Wilson-Loop Creutz Ratio & $\beta_0$ Control**: The Creutz ratio $\frac{W(2,2)W(1,1)}{W(2,1)W(1,2)}$ isolates the area-law factor $b$ vs perimeter-law $1$, the $3\times 3$ planar grid has $b_1 = 4$, and the 1-loop rational polynomial $\beta_0(3, N_f) = 11 - \frac{2}{3}N_f$ ($> 0 \iff N_f < 33/2$) and 2-loop $\beta_1(3, N_f) = 102 - \frac{38}{3}N_f$ give the Banks--Zaks ratio $-\beta_0(16)/\beta_1(16) = 1/302$.
- **Lattice Dirac Doubling Obstruction**: Naive symmetric-difference fermions in dimension $d \in \{1,2,3,4\}$ produce $2^d - 1 > 0$ spurious Brillouin-corner doublers ($1, 3, 7, 15$), which must be recorded as an explicit topological obstruction rather than hidden.
- **Epistemic Separation & `F002` Fence**: Exact rational certificates are separated from floating-point benchmarks (`floatBenchmarkAuthorizesFiniteStatement = false`), finite Wilson/$\beta_0$ controls are separated by an explicit gap from continuum confinement, and continuum QCD remains an open interface on `F002`.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
- `lean4/CampaignTfq0011FiniteQcd.lean`:
  - `CampaignTfq0011FiniteQcd.su3_color_casimir_and_fierz_channel_identities`
  - `CampaignTfq0011FiniteQcd.wilson_plaquette_creutz_ratio_area_vs_perimeter_and_3x3_betti`
  - `CampaignTfq0011FiniteQcd.qcd_beta0_asymptotic_freedom_window_and_beta1_banks_zaks`
  - `CampaignTfq0011FiniteQcd.naive_lattice_dirac_doubling_obstruction_and_wilson_lift`
  - `CampaignTfq0011FiniteQcd.nonabelian_su3_klein_four_gribov_copies_and_spanning_tree_gauge`
  - `CampaignTfq0011FiniteQcd.exact_rational_certificate_vs_float_benchmark_epistemic_separation_fence`
  - `CampaignTfq0011FiniteQcd.finite_wilson_beta0_control_not_continuum_confinement_fence`
  - `CampaignTfq0011FiniteQcd.lattice_dirac_doubling_recorded_as_explicit_obstruction_fence`
  - `CampaignTfq0011FiniteQcd.f002_continuum_qcd_remains_open_interface_fence`
  - `CampaignTfq0011FiniteQcd.tfq0011_finite_qcd_shadow_scope_ledger_fence`
- `lean4/FiniteQM.lean`:
  - `FiniteQM.su3_casimir_and_channel_identities`
  - `FiniteQM.su3_fierz_diagonal_and_offdiagonal_identities`
  - `FiniteQM.qcd_beta0_asymptotic_freedom_window`
  - `FiniteQM.qcd_beta1_and_banks_zaks_fixed_point`
  - `FiniteQM.wilson_creutz_ratio_area_vs_perimeter`
  - `FiniteQM.wilson_lattice_3x3_dfm_betti_identity`
  - `FiniteQM.su3_diagonal_klein_four_landau_gribov_copies`
  - `FiniteQM.spanning_tree_dfm_eliminates_gribov_copies`

### Independent Python Verification
- `checks/independent/tfq-0011.py`:
  - `run_all_checks`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002`
- **Primary Source Paths**:
  - `lean4/FiniteQM.lean`
  - `lean4/CampaignTfq0011FiniteQcd.lean`
  - `checks/independent/tfq-0011.py`
