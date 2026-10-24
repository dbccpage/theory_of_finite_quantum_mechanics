Status: AI-drafted, awaiting human review.

# Pre-Commit Overclaim & Falsification Review: `ADS-CFT-DUALITY-IMPORT` (`TFQ-2202`)

**Date:** 2026-10-23  
**Campaign Node:** `ADS-CFT-DUALITY-IMPORT` (`TFQ-2202`, source ID `ADS-01`, stage `ADS_CFT`)  
**Outcome:** `Narrowed` (`IMPORTED_ASSUMPTION` status preserved; rational GKPW scalar mass-dimension quadratic and Breitenlohner-Freedman bound, 't Hooft large-$N$ ribbon-graph genus factorization and planar-vs-torus $N^2$ suppression, and finite isometric bulk-to-boundary operator dictionary together with its non-surjectivity witness formalized in Lean 4 and checked by an independent Python script)  
**AuthorityEffect:** `None`

---

## 1. Falsification & Boundary Audit

1. **Historical Fixture Replacement (`lean4/ads_cft_core.lean`)**:
   - The legacy binding `lean4/ads_cft_core.lean::ads_cft_dictionary_consistency` was `True := by trivial` (`rfl`/triviality placeholder).
   - `lean4/CampaignAdsCftDualityImport.lean` replaces that placeholder with 21 non-vacuous theorems across three finite/rational algebraic shadows of the AdS/CFT dictionary:
     - GKPW scalar mass-dimension quadratic `gkpwMassSq d Δ = Δ * (Δ - d)`, shadow involution `shadowDimension d Δ = d - Δ`, completed square `(2 * Δ - d)^2 = d^2 + 4 * gkpwMassSq d Δ`, root recovery `gkpw_roots_from_square_discriminant`, and Breitenlohner-Freedman lower bound `bfBound d = -(d^2)/4` (`bf_bound_iff_discriminant_nonneg`, `bf_saturation_double_root`, `gkpwMassSq_ge_bfBound`, `no_rational_root_below_bf_bound`, `recorded_ads5_and_ads3_gkpw_points`).
     - 't Hooft large-$N$ ribbon-graph scaling (`thooft_factorization`, `thooft_planar_vs_torus_suppression`, `recorded_thooft_and_gauge_counts`).
     - Finite isometric bulk-to-boundary dictionary (`pullback_pushforward_id`, `pushforward_mul_of_isometry`, `correlator_dictionary_pullback`, `correlator_dictionary_match`).

2. **Explicit Non-Equivalence & Field-Extension Obstructions**:
   - `recorded_ads5_and_ads3_gkpw_points` shows that at $(d=4, m_{\mathrm{sq}}=1)$ the GKPW discriminant is $D = 20$ with $4^2 < 20 < 5^2$, so rational conformal dimensions do not close the spectrum even above the Breitenlohner-Freedman bound.
   - `codeIsometry12_projector_ne_one` and `boundary_annihilator_obstruction` exhibit the $1 \to 2$ isometric code embedding $V = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$ for which $V^T V = I_1$ but $V V^T \ne I_2$, and the nonzero boundary observable $O_\perp = \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}$ has vanishing bulk pullback $\pi_V(O_\perp) = 0$ and no bulk preimage under $\iota_V$.

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - In `lean4/CampaignAdsCftDualityImport.lean` (`L4D`), the rational GKPW scalar mass-dimension relation $\Delta(\Delta - d) = m_{\mathrm{sq}}$ satisfies shadow involution $\Delta \mapsto d - \Delta$, $(2\Delta - d)^2 = d^2 + 4\Delta(\Delta - d)$, and the Breitenlohner-Freedman lower bound $-d^2/4 \le \Delta(\Delta - d)$ with no rational root below $-d^2/4$; the 't Hooft double-line weight satisfies $(g_{\mathrm{YM}}^2)^{E-V} N^F \cdot N^{E-V} = \lambda^{E-V} N^F$ with exact $N^2$ suppression of the genus-1 torus vacuum graph $(V=2, E=3, F=1)$ relative to the planar dipole $(V=2, E=3, F=3)$; and any finite isometric bulk-to-boundary map $V^T V = I_b$ satisfies $\pi_V(\iota_V(O_{\mathrm{bulk}})) = O_{\mathrm{bulk}}$, $\iota_V(A)\iota_V(C) = \iota_V(AC)$, and $\langle V\psi, O_{\mathrm{bdry}}(V\psi)\rangle = \langle\psi, \pi_V(O_{\mathrm{bdry}})\psi\rangle$, while failing surjectivity for $b=1 < B=2$.
   - In `checks/independent/ads-cft-duality-import.py` (`L4D`), 963 exact rational and matrix checks pass with 0 failures, and 6 of 6 semantic Lean mutations are killed in `dag/research/campaign_ads-cft-duality-import_lean_mutation.json`.
2. **What it does not support**:
   - A derivation of continuum AdS/CFT partition-function equality $Z_{\mathrm{grav}}[\phi_0] = Z_{\mathrm{CFT}}[\phi_0]$, full Hilbert space isomorphism between type IIB string theory on $\mathrm{AdS}_5 \times S^5$ and $4\mathrm{D}$ $\mathcal{N}=4$ super-Yang-Mills theory, or continuum gravitational dynamics from finite rules.
3. **Narrowest defensible claim**:
   - The imported continuum AdS/CFT dictionary remains an `IMPORTED_ASSUMPTION`, while its finite/rational algebraic shadows—the GKPW quadratic $\Delta(\Delta - d) = m_{\mathrm{sq}}$ and Breitenlohner-Freedman bound $-d^2/4 \le \Delta(\Delta - d)$, the polynomial 't Hooft ribbon-graph identity $(g_{\mathrm{YM}}^2)^{E-V} N^F \cdot N^{E-V} = \lambda^{E-V} N^F$ with planar-to-torus ratio $N^2$, and the isometric code pullback/pushforward dictionary $\pi_V(\iota_V(O_{\mathrm{bulk}})) = O_{\mathrm{bulk}}$ together with its $1 \to 2$ non-surjectivity witness—are checked in Lean 4 and by a standalone Python verifier.
4. **Next test needed**:
   - Proceed to the next available derivation in `dag/pfp/campaign/derivation_queue.json`.
