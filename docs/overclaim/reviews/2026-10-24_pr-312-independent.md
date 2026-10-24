# Independent review of PR #312

Scope: original head 2845b1de9d7a2e5b37e990abf5b18aeaad3ef33d. Exact source lean4/CampaignFspKitaevHoneycombSolution.lean, SHA-256 b73b461fe2757d85dcdb6efb82fbd0e30aa98b76d3e0ed9425d67abce8508b52.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

Explicit integer matrices obey Clifford identities; one anticommutation hypothesis gives bond factorization; a six-factor commutative-ring flux is gauge invariant; a product of all supplied involutions squared equals one; and a 4x4 skew matrix has determinant equal to the squared explicit Pfaffian polynomial. No cellular surface incidence map is built, so the product-square lemma is not a theorem about all plaquettes on closed tori. The independent diagonal parity matrix is not identified with the supplied Majorana gauge operator. No physical Hilbert-space projection or thermal partition function is constructed.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignFspKitaevHoneycombSolution.lean:60 majorana_site_clifford_relations` | `: bX * bX = 1 ∧ bY * bY = 1 ∧ bZ * bZ = 1 ∧ ic * ic = -1 ∧ bX * bY + bY * bX = 0 ∧ bX * bZ + bZ * bX = 0 ∧ bY * bZ + bZ * bY = 0 ∧ bX * ic + ic * bX = 0 ∧ bY * ic + ic * bY = 0 ∧ bZ * ic + ic * bZ = 0` |
| `lean4/CampaignFspKitaevHoneycombSolution.lean:74 kitaev_spin_operators_pauli_algebra_and_gauge_commutation` | `: tildeSigmaX * tildeSigmaX = 1 ∧ tildeSigmaY * tildeSigmaY = 1 ∧ tildeSigmaZ * tildeSigmaZ = 1 ∧ tildeSigmaX * tildeSigmaY + tildeSigmaY * tildeSigmaX = 0 ∧ tildeSigmaX * tildeSigmaZ + tildeSigmaZ * tildeSigmaX = 0 ∧ tildeSigmaY * tildeSigmaZ + tildeSigmaZ * tildeSigmaY = 0 ∧ siteGaugeJD * siteGaugeJD = -1 ∧ siteGaugeJD * tildeSigmaX = tildeSigmaX * siteGaugeJD ∧ siteGaugeJD * tildeSigmaY = tildeSigmaY * siteGaugeJD ∧ siteGaugeJD * tildeSigmaZ = tildeSigmaZ * siteGaugeJD ∧ siteGaugeJD * bX + bX * siteGaugeJD = 0 ∧ siteGaugeJD * ic + ic * siteGaugeJD = 0 ∧ tildeSigmaX * tildeSigmaY * tildeSigmaZ = siteGaugeJD` |
| `lean4/CampaignFspKitaevHoneycombSolution.lean:91 abstract_bond_spin_product_factorization` | `{R : Type*} [Ring R] (bj cj bk ck : R) (h_anticomm : cj * bk = -(bk * cj)) : (bj * cj) * (bk * ck) = -((bj * bk) * (cj * ck))` |
| `lean4/CampaignFspKitaevHoneycombSolution.lean:109 plaquette_flux_local_z2_gauge_invariance` | `{R : Type*} [CommRing R] (u01 u12 u23 u34 u45 u50 : R) (e0 e1 e2 e3 e4 e5 : R) (he0 : e0 * e0 = 1) (he1 : e1 * e1 = 1) (he2 : e2 * e2 = 1) (he3 : e3 * e3 = 1) (he4 : e4 * e4 = 1) (he5 : e5 * e5 = 1) : hexPlaquetteFlux (e0 * u01 * e1) (e1 * u12 * e2) (e2 * u23 * e3) (e3 * u34 * e4) (e4 * u45 * e5) (e5 * u50 * e0) = hexPlaquetteFlux u01 u12 u23 u34 u45 u50` |
| `lean4/CampaignFspKitaevHoneycombSolution.lean:130 hexPlaquetteFlux_sq_eq_one` | `{R : Type*} [CommRing R] (u01 u12 u23 u34 u45 u50 : R) (h01 : u01 * u01 = 1) (h12 : u12 * u12 = 1) (h23 : u23 * u23 = 1) (h34 : u34 * u34 = 1) (h45 : u45 * u45 = 1) (h50 : u50 * u50 = 1) : hexPlaquetteFlux u01 u12 u23 u34 u45 u50 * hexPlaquetteFlux u01 u12 u23 u34 u45 u50 = 1` |
| `lean4/CampaignFspKitaevHoneycombSolution.lean:145 single_link_flip_inverts_two_incident_plaquettes` | `{R : Type*} [CommRing R] (u_shared p_rest q_rest : R) : ((-u_shared) * p_rest = -(u_shared * p_rest)) ∧ ((-u_shared) * q_rest = -(u_shared * q_rest)) ∧ (((-u_shared) * p_rest) * ((-u_shared) * q_rest) = (u_shared * p_rest) * (u_shared * q_rest))` |
| `lean4/CampaignFspKitaevHoneycombSolution.lean:155 closed_surface_total_plaquette_flux_eq_one` | `{ι : Type*} [Fintype ι] {R : Type*} [CommRing R] (u : ι → R) (hu : ∀ e, u e * u e = 1) : (∏ e : ι, u e) * (∏ e : ι, u e) = 1` |
| `lean4/CampaignFspKitaevHoneycombSolution.lean:176 quadratic_matter_matrix_skew_symmetric_and_pfaffian_sq_eq_det` | `{R : Type*} [CommRing R] (a01 a02 a03 a12 a13 a23 : R) : (matterSkewMatrix4 a01 a02 a03 a12 a13 a23)ᵀ = -matterSkewMatrix4 a01 a02 a03 a12 a13 a23 ∧ (matterSkewMatrix4 a01 a02 a03 a12 a13 a23).det = (pfaffian4 a01 a02 a03 a12 a13 a23) ^ 2` |
| `lean4/CampaignFspKitaevHoneycombSolution.lean:200 unprojected_majorana_fock_overcounts_physical_spin_space_fence` | `(N : ℕ) : 4 ^ N = 2 ^ N * 2 ^ N ∧ siteGaugeParityDiag * siteGaugeParityDiag = 1 ∧ Matrix.trace siteGaugeParityDiag = 0 ∧ unnormalizedPhysProjector * unnormalizedPhysProjector = 2 • unnormalizedPhysProjector ∧ Matrix.trace unnormalizedPhysProjector = 4` |
| `lean4/CampaignFspKitaevHoneycombSolution.lean:213 link_flip_flips_matter_pfaffian_sign_while_det_stays_positive_fence` | `: pfaffian4 (1 : ℤ) 0 0 0 0 1 = 1 ∧ pfaffian4 (-1 : ℤ) 0 0 0 0 1 = -1 ∧ (matterSkewMatrix4 (1 : ℤ) 0 0 0 0 1).det = 1 ∧ (matterSkewMatrix4 (-1 : ℤ) 0 0 0 0 1).det = 1 ∧ pfaffian4 (1 : ℤ) 0 0 0 0 1 + pfaffian4 (-1 : ℤ) 0 0 0 0 1 = 0` |
| `lean4/CampaignFspKitaevHoneycombSolution.lean:228 physical_parity_projection_excludes_mismatched_sector_states_fence` | `(pGauge : ℤ) (hp : pGauge * pGauge = 1) : parityProjectionWeight pGauge pGauge = 2 ∧ parityProjectionWeight (-pGauge) pGauge = 0` |

## Corrections and acceptance

Current capability: **L3**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_312_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
