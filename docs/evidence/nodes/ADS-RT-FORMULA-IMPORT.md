# ADS-RT-FORMULA-IMPORT

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported formula, as the source states it at leading order in Newton's constant: S(A) = Area(minimal surface anchored on the boundary of A) / (4 G). It presupposes the von Neumann entropy of a boundary reduced state on a continuum Hilbert space and the area of a surface in a bulk geometry. The repository has an exact von Neumann entropy dichotomy for algebraic spectra and an exact rational Regge area proxy that is not the Einstein-Hilbert action; neither is a minimal-surface area in a bulk geometry.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 16
- distinct cited Lean declarations covered by a current replay receipt: 16
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- von Neumann entropy of boundary regions on a continuum Hilbert space (assumption)
- bulk geometry with minimal surfaces (assumption)

## Bottleneck

No source supplies a dictionary from the repository's finite areas to the surface areas of the formula; under BakerCitedInput mixed algebraic spectra have transcendental natural-log entropy, and the TFQ-0100 rational Regge proxy scales as lam^4 and vanishes on flat charts. Checked slice, status unchanged. Narrowed in Lean 4 and an independent Python verifier to three exact finite/rational algebraic shadows and scope fences: (1) over Q, substituting the regulated AdS_3 geodesic length 2 R_AdS * logFactor into rtLeadingEntropy(area, G_N) = area / (4 G_N) reproduces the 2D CFT Calabrese-Cardy coefficient (c / 3) * logFactor under the Brown-Henneaux relation c = 3 R_AdS / (2 G_N^(3)) and eliminates both bulk couplings in S_A / c = logFactor / 3, while submodular surface pasting yields Strong Subadditivity S(ABC) + S(B) \<= S(AB) + S(BC) and all 380 proper contiguous boundary intervals of the 20-qubit 6-pentagon HaPPY patch satisfy complement symmetry A \<-\> A^c; (2) under BakerCitedInput (EntropyDichotomy.lean), no mixed algebraic spectrum can have natural-log von Neumann entropy equal to a rational RT ratio area / (4 G_N), equality holds at G_N \> 0 iff the state is pure and area = 0, and stabilizer bit counts require dividing by log 2; and (3) on the orthogonal_pentatope chart of TFQ-0100, the 6 right-triangle hinges have Cayley-Menger squared area 1/4 and the 4 equilateral-triangle hinges have squared area 3/4 (total 9/2) with no rational linear area A in Q satisfying A^2 = 3/4, the flat-chart Regge proxy (kappa = 0) vanishes identically whereas all 380 HaPPY intervals satisfy 1 \<= S(A) \<= mincut(A), and under length rescaling L -\> lam * L the Regge proxy scales as lam^4 against lam^2 for 2-surface area and lam^0 for bond counts.

## Source status

Audited against arXiv:hep-th/0603001 Section 1 eq. (1.5) p. 2, Section 2 eqs. (2.1), (2.5)-(2.6) p. 3, and Section 3.1 eq. (3.2) p. 4 on 2026-10-24; narrowed to exact rational Ryu-Takayanagi / Brown-Henneaux coupling elimination, cut-pasting Strong Subadditivity, 380-interval HaPPY complement symmetry, BakerCitedInput entropy dichotomy fences, and TFQ-0100 rational Regge proxy non-equivalence fences in Lean 4 and an independent Python verifier while keeping the continuum formula as an imported assumption.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignAdsRtFormulaImport.lean`

- file: [lean4/CampaignAdsRtFormulaImport.lean](../../../lean4/CampaignAdsRtFormulaImport.lean)
- sha256 (`bytes`): `748e566374c61a2d8204736a7b4623e2e47431ade57911e783c3081448fb90ec`
- cited in: node.lean, receipt dag/research/campaign_ads-rt-formula-import_lean_replay.json (CampaignAdsRtFormulaImport), record TFQ-2204
- replay: `verified`
  - receipt [dag/research/campaign_ads-rt-formula-import_lean_replay.json](../../../dag/research/campaign_ads-rt-formula-import_lean_replay.json) (module `CampaignAdsRtFormulaImport`): recorded sha256 `748e566374c61a2d8204736a7b4623e2e47431ade57911e783c3081448fb90ec` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignAdsRtFormulaImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignAdsRtFormulaImport.cayleyMengerTriangleAreaSq_homogeneous_deg4_in_length` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.cayleyMengerTriangleAreaSq_homogeneous_deg4_in_length` |
| `CampaignAdsRtFormulaImport.cut_pasting_strong_subadditivity_from_submodularity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.cut_pasting_strong_subadditivity_from_submodularity` |
| `CampaignAdsRtFormulaImport.happy_all_380_intervals_pos_entropy_and_mincut` | yes | yes | yes | propext | `#print axioms CampaignAdsRtFormulaImport.happy_all_380_intervals_pos_entropy_and_mincut` |
| `CampaignAdsRtFormulaImport.happy_mincut_and_entropy_complement_symmetry_all_380` | yes | yes | yes | propext | `#print axioms CampaignAdsRtFormulaImport.happy_mincut_and_entropy_complement_symmetry_all_380` |
| `CampaignAdsRtFormulaImport.nat_dvd_three_of_sq_mul_four_eq_three_mul_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.nat_dvd_three_of_sq_mul_four_eq_three_mul_sq` |
| `CampaignAdsRtFormulaImport.no_rational_linear_area_for_equilateral_pentatope_hinge` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.no_rational_linear_area_for_equilateral_pentatope_hinge` |
| `CampaignAdsRtFormulaImport.no_rational_rt_area_for_mixed_algebraic_spectrum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.no_rational_rt_area_for_mixed_algebraic_spectrum` |
| `CampaignAdsRtFormulaImport.no_scale_invariant_regge_to_rt_dictionary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.no_scale_invariant_regge_to_rt_dictionary` |
| `CampaignAdsRtFormulaImport.orthogonal_pentatope_hinge_areas_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.orthogonal_pentatope_hinge_areas_sq` |
| `CampaignAdsRtFormulaImport.rational_rt_match_iff_pure_and_zero_area` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.rational_rt_match_iff_pure_and_zero_area` |
| `CampaignAdsRtFormulaImport.reggeProxy_zero_on_flat_chart` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.reggeProxy_zero_on_flat_chart` |
| `CampaignAdsRtFormulaImport.rtLeadingEntropy_linear_in_area` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.rtLeadingEntropy_linear_in_area` |
| `CampaignAdsRtFormulaImport.rtLeadingEntropy_realCast_isAlgebraic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.rtLeadingEntropy_realCast_isAlgebraic` |
| `CampaignAdsRtFormulaImport.rt_ads3_reproduces_calabrese_cardy` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.rt_ads3_reproduces_calabrese_cardy` |
| `CampaignAdsRtFormulaImport.rt_over_brown_henneaux_eliminates_couplings` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.rt_over_brown_henneaux_eliminates_couplings` |
| `CampaignAdsRtFormulaImport.stabilizer_bits_to_nats_transcendental_conversion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAdsRtFormulaImport.stabilizer_bits_to_nats_transcendental_conversion` |

- counts toward the grade: yes

### Python: `checks/independent/ads-rt-formula-import.py`

- file: [checks/independent/ads-rt-formula-import.py](../../../checks/independent/ads-rt-formula-import.py)
- sha256 (`bytes`): `cb22ab062bdb54c3ee0d7a217fda9bdf6663e815837346524d98e569826da256`
- cited in: node.source, record TFQ-2204
- counts toward the grade: yes

### Documents and data: `dag/derivations/32_ads_cft/tfq_2204_ads_rt_formula_import.md`

- file: [dag/derivations/32_ads_cft/tfq_2204_ads_rt_formula_import.md](../../../dag/derivations/32_ads_cft/tfq_2204_ads_rt_formula_import.md)
- sha256 (`lf-normalised`): `0b30ee6e7b51eb7bed0218e07c399e6e73fdc62887c12d5c6a747c9edfb9439d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2204
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ads-rt-formula-import.md`

- file: [dag/derivations/independent/ads-rt-formula-import.md](../../../dag/derivations/independent/ads-rt-formula-import.md)
- sha256 (`lf-normalised`): `e1ea19f89a8343c680617cdeafb54c0bc23c48b478173d15f5d0fa52348d6e88`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ads-rt-formula-import_independent.json`

- file: [dag/research/campaign_ads-rt-formula-import_independent.json](../../../dag/research/campaign_ads-rt-formula-import_independent.json)
- sha256 (`lf-normalised`): `94586670fbaba3f6b4cc221b35ef34d686d32c9db6f8d9519788383c0749c093`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ads-rt-formula-import_lean_mutation.json`

- file: [dag/research/campaign_ads-rt-formula-import_lean_mutation.json](../../../dag/research/campaign_ads-rt-formula-import_lean_mutation.json)
- sha256 (`lf-normalised`): `0462e238a597b85a0ac23e60c477e2a7a29318cdd8b52b75440f44aaa0a13a38`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ads-rt-formula-import_lean_replay.json`

- file: [dag/research/campaign_ads-rt-formula-import_lean_replay.json](../../../dag/research/campaign_ads-rt-formula-import_lean_replay.json)
- sha256 (`lf-normalised`): `5d9a232287e3ea308a91b4a7fd55d6ee18da6f90b696895c4d2e05faf2124330`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:hep-th/0603001`

## Routes

Incoming (1):

- `FRO-R-ADS-RT-FORMULA-IMPORT` `CONDITIONAL_ON_IMPORT`: [ADS-RT-2006-SOURCE](ADS-RT-2006-SOURCE.md) (SOURCE_RECORD)

Outgoing (2):

- `FRO-R-ADS-HAPPY-ENTROPY-MINCUT-TARGET` `DERIVED_LEAN`: [ADS-HAPPY-ENTROPY-MINCUT-TARGET](ADS-HAPPY-ENTROPY-MINCUT-TARGET.md) (PROVED_LEAN)
- `FRO-R-ADS-REGGE-AREA-RT-GAP` `GAP_NO_DERIVATION`: [ADS-REGGE-AREA-RT-GAP](ADS-REGGE-AREA-RT-GAP.md) (OPEN)
