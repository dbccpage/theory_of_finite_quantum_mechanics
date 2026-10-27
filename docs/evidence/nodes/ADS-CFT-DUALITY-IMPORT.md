# ADS-CFT-DUALITY-IMPORT

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported as an assumption, not as a result of this repository: a continuum quantum gravity theory on an asymptotically anti-de Sitter spacetime has the same generating functional and observables as a conformal field theory on its boundary.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 21
- distinct cited Lean declarations covered by a current replay receipt: 21
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- continuum quantum field theory and gravity (assumption)
- large-N limit (assumption)

## Bottleneck

The continuum partition-function equality Z_grav\[phi_0\] = Z_CFT\[phi_0\], the full AdS_5 x S^5 / N=4 SYM Hilbert space isomorphism, and the continuum inputs FQ-GAP-CONTINUUM-HILBERT-LIFT and TFQ-0085 remain unconstructed; at b \< B a finite isometric encoding V^T V = I_b has non-surjective pushforward iota_V and a nontrivial boundary kernel of pi_V. Checked slice, status unchanged. Narrowed to its exact finite/rational algebraic shadows: (1) over Q, the GKPW scalar mass-dimension quadratic gkpwMassSq(d, Delta) = Delta(Delta - d) = mSq satisfies the shadow involution Delta |-\> d - Delta, (2 Delta - d)^2 = d^2 + 4 Delta(Delta - d), and the Breitenlohner-Freedman lower bound -(d^2)/4 \<= Delta(Delta - d) with double root Delta = d/2 at saturation and no rational root strictly below -(d^2)/4; (2) in 't Hooft double-line counting with lambda = g_YM^2 N and Euler characteristic chi = V - E + F = 2 - 2g, the ribbon weight satisfies (g_YM^2)^(E - V) N^F * N^(E - V) = lambda^(E - V) N^F, suppressing the genus-1 torus vacuum graph (V=2, E=3, F=1) relative to the planar dipole (V=2, E=3, F=3) by N^2; and (3) for any finite isometric bulk-to-boundary encoding V^T V = I_b, the pushforward iota_V(O_bulk) = V O_bulk V^T and pullback pi_V(O_bdry) = V^T O_bdry V satisfy pi_V(iota_V(O_bulk)) = O_bulk, iota_V(A) iota_V(C) = iota_V(A C), and \<V psi, O_bdry(V psi)\> = \<psi, pi_V(O_bdry) psi\>, whereas for b = 1 \< B = 2 (V = \[\[1\],\[0\]\]) V V^T != I_2 and the nonzero boundary operator O_perp = \[\[0,0\],\[0,1\]\] pulls back to 0 and has no bulk preimage.

## Source status

Audited against arXiv:hep-th/9711200, arXiv:hep-th/9802109 and arXiv:hep-th/9802150 on 2026-10-23; narrowed to finite/rational algebraic shadows in Lean 4 and an independent Python verifier while keeping the continuum duality as an imported assumption.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AdsCftDualityImport.lean`

- file: [lean4/AdsCftDualityImport.lean](../../../lean4/AdsCftDualityImport.lean)
- sha256 (`bytes`): `19365b284177fa7eb6fbe532f016248ea5143a1a8ead08e77d772539ac89f61b`
- cited in: node.lean, receipt dag/research/campaign_ads-cft-duality-import_lean_replay.json (AdsCftDualityImport), record TFQ-2202
- replay: `verified`
  - receipt [dag/research/campaign_ads-cft-duality-import_lean_replay.json](../../../dag/research/campaign_ads-cft-duality-import_lean_replay.json) (module `AdsCftDualityImport`): recorded sha256 `19365b284177fa7eb6fbe532f016248ea5143a1a8ead08e77d772539ac89f61b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build AdsCftDualityImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AdsCftDualityImport.bf_bound_iff_discriminant_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.bf_bound_iff_discriminant_nonneg` |
| `AdsCftDualityImport.bf_saturation_double_root` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.bf_saturation_double_root` |
| `AdsCftDualityImport.boundary_annihilator_obstruction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.boundary_annihilator_obstruction` |
| `AdsCftDualityImport.codeIsometry12_is_isometry` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.codeIsometry12_is_isometry` |
| `AdsCftDualityImport.codeIsometry12_projector_ne_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.codeIsometry12_projector_ne_one` |
| `AdsCftDualityImport.correlator_dictionary_match` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.correlator_dictionary_match` |
| `AdsCftDualityImport.correlator_dictionary_pullback` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.correlator_dictionary_pullback` |
| `AdsCftDualityImport.gkpwMassSq_ge_bfBound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.gkpwMassSq_ge_bfBound` |
| `AdsCftDualityImport.gkpwMassSq_shadow_eq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.gkpwMassSq_shadow_eq` |
| `AdsCftDualityImport.gkpw_completed_square` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.gkpw_completed_square` |
| `AdsCftDualityImport.gkpw_roots_from_square_discriminant` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.gkpw_roots_from_square_discriminant` |
| `AdsCftDualityImport.gkpw_vieta_product` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.gkpw_vieta_product` |
| `AdsCftDualityImport.no_rational_root_below_bf_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.no_rational_root_below_bf_bound` |
| `AdsCftDualityImport.pullback_pushforward_id` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.pullback_pushforward_id` |
| `AdsCftDualityImport.pushforward_mul_of_isometry` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.pushforward_mul_of_isometry` |
| `AdsCftDualityImport.recorded_ads5_and_ads3_gkpw_points` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.recorded_ads5_and_ads3_gkpw_points` |
| `AdsCftDualityImport.recorded_thooft_and_gauge_counts` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.recorded_thooft_and_gauge_counts` |
| `AdsCftDualityImport.shadowDimension_involutive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.shadowDimension_involutive` |
| `AdsCftDualityImport.shadowDimension_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.shadowDimension_sum` |
| `AdsCftDualityImport.thooft_factorization` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.thooft_factorization` |
| `AdsCftDualityImport.thooft_planar_vs_torus_suppression` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsCftDualityImport.thooft_planar_vs_torus_suppression` |

- counts toward the grade: yes

### Python: `checks/independent/ads-cft-duality-import.py`

- file: [checks/independent/ads-cft-duality-import.py](../../../checks/independent/ads-cft-duality-import.py)
- sha256 (`bytes`): `33a8f4e4f820bf0c0f84f21af5602d80b0f89877e880abc0d8220f1d3db40ef7`
- cited in: node.source, record TFQ-2202
- counts toward the grade: yes

### Documents and data: `dag/derivations/32_ads_cft/tfq_2202_ads_cft_duality_import.md`

- file: [dag/derivations/32_ads_cft/tfq_2202_ads_cft_duality_import.md](../../../dag/derivations/32_ads_cft/tfq_2202_ads_cft_duality_import.md)
- sha256 (`lf-normalised`): `ba4dcbaa0e64e9b209f3cf641d762c5f9555a47446767191bbf9f4eaee39f116`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2202
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ads-cft-duality-import.md`

- file: [dag/derivations/independent/ads-cft-duality-import.md](../../../dag/derivations/independent/ads-cft-duality-import.md)
- sha256 (`lf-normalised`): `01b23af1ec664eb54ad3bb3f9f16e401b4193fdbdee4710e6c95f9d5eaeab03b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ads-cft-duality-import_independent.json`

- file: [dag/research/campaign_ads-cft-duality-import_independent.json](../../../dag/research/campaign_ads-cft-duality-import_independent.json)
- sha256 (`lf-normalised`): `084644db1aea5b0bd0dabc81e653f451cceb20c9ed8ad0a34a99f1a6f5cb152b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ads-cft-duality-import_lean_mutation.json`

- file: [dag/research/campaign_ads-cft-duality-import_lean_mutation.json](../../../dag/research/campaign_ads-cft-duality-import_lean_mutation.json)
- sha256 (`lf-normalised`): `53c66627619609fb2558eb4383856ad4fd82e7238d33b2b9a2028b034a17b3be`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ads-cft-duality-import_lean_replay.json`

- file: [dag/research/campaign_ads-cft-duality-import_lean_replay.json](../../../dag/research/campaign_ads-cft-duality-import_lean_replay.json)
- sha256 (`lf-normalised`): `9b3bc6f924420c2ca467bd0d423a3693770d9ab376a5cb4c97aed67cc03255df`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:hep-th/9711200`
- `external:arXiv:hep-th/9802109`
- `external:arXiv:hep-th/9802150`

## Routes

Incoming (1):

- `FRO-R-ADS-CFT-DUALITY-IMPORT` `CONDITIONAL_ON_IMPORT`: [ADS-GKPW-DICTIONARY-SOURCE](ADS-GKPW-DICTIONARY-SOURCE.md) (SOURCE_RECORD)

Outgoing (2):

- `FRO-R-ADS-HAPPY-TOY-NOT-DUALITY-GAP` `GAP_NO_DERIVATION`: [ADS-HAPPY-TOY-NOT-DUALITY-GAP](ADS-HAPPY-TOY-NOT-DUALITY-GAP.md) (OPEN)
- `FRO-R-BACK-ADS-DUALITY-TO-CONTINUUM-INTERFACE` `GAP_NO_DERIVATION`: [TFQ-0085](TFQ-0085.md) (OPEN)
