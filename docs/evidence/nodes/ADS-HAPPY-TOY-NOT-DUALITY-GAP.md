# ADS-HAPPY-TOY-NOT-DUALITY-GAP

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No source read for this change derives AdS/CFT, or its continuum entropy formula, from a finite stabilizer-code tensor network. The HaPPY codes are discrete kinematic models of the bulk-to-boundary map on a hyperbolic tiling with no Lorentzian time, no dynamics, no gravitational action and no large-N limit.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- distinct cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Recorded as an explicit non-claim and non-equivalence fence so that finite stabilizer-code checks are not read as evidence for continuum AdS/CFT; Lorentzian time evolution, non-flat entanglement spectra, sub-AdS locality, and continuum gravitational dynamics remain open. Checked slice, status unchanged. Narrowed in Lean 4 and an independent Python verifier to three exact non-equivalence fences: (1) every stabilizer reduced state has flat Renyi spectrum S_n / S_1 = 1, whereas a 2D CFT single interval has Calabrese-Cardy / Ryu-Takayanagi Renyi ratio cftRenyiFactor(n) = (1 + 1/n)/2, yielding a strictly positive defect ((n - 1)/(2n)) * S_1 \> 0 for all n \> 1 and S_1 \> 0; (2) on the 20-qubit boundary state of the 6-pentagon {5,4} HaPPY patch (with bulk legs fixed in |0_L\>), all 280 contiguous intervals of lengths 1..7 and 13..19 satisfy S(A) = mincut(A), whereas lengths 8, 9, 10, 11, 12 exhibit 5, 10, 10, 10, 5 strict Ryu-Takayanagi deficits (S(A) = mincut(A) - 1, summing to 40), including the explicit 5-fold rotational orbit start = 4*k + 2 at len = 8 and its complement len = 12 (S = 4 \< 5 = mincut); and (3) disconnected boundary regions exhibit discrete integer mutual-information jumps (0, 0, 3, 1 bits) while for nBulk \< nBdry the bulk code subspace 2^{nBulk} has strictly positive orthogonal codimension 2^{nBdry} - 2^{nBulk} \> 0 (30, 1048512, 33552384 for 1, 6, and 11 pentagons).

## Source status

Explicit non-claim node; audited against arXiv:1503.06237 Abstract p. 1, Section 4 pp. 8-14, and Section 6 pp. 20-23 on 2026-10-23; narrowed to exact Renyi-spectrum, length-8..12 minimal-cut deficit, and Hilbert-codimension fences in Lean 4 and an independent Python verifier.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AdsHappyToyNotDualityGap.lean`

- file: [lean4/AdsHappyToyNotDualityGap.lean](../../../lean4/AdsHappyToyNotDualityGap.lean)
- sha256 (`bytes`): `8ae260255f3f65384458080171a83122187b121c24058ea128a30e5d6e9ef5c0`
- cited in: node.lean, receipt dag/research/campaign_ads-happy-toy-not-duality-gap_lean_replay.json (AdsHappyToyNotDualityGap), record TFQ-2212
- replay: `verified`
  - receipt [dag/research/campaign_ads-happy-toy-not-duality-gap_lean_replay.json](../../../dag/research/campaign_ads-happy-toy-not-duality-gap_lean_replay.json) (module `AdsHappyToyNotDualityGap`): recorded sha256 `8ae260255f3f65384458080171a83122187b121c24058ea128a30e5d6e9ef5c0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build AdsHappyToyNotDualityGap`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AdsHappyToyNotDualityGap.cftRenyiFactor_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsHappyToyNotDualityGap.cftRenyiFactor_one` |
| `AdsHappyToyNotDualityGap.cftRenyiFactor_strict_anti` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsHappyToyNotDualityGap.cftRenyiFactor_strict_anti` |
| `AdsHappyToyNotDualityGap.cftRenyiFactor_sub_half` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsHappyToyNotDualityGap.cftRenyiFactor_sub_half` |
| `AdsHappyToyNotDualityGap.cft_ne_stabilizer_renyi_of_gt_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsHappyToyNotDualityGap.cft_ne_stabilizer_renyi_of_gt_one` |
| `AdsHappyToyNotDualityGap.code_subspace_strict_codimension` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsHappyToyNotDualityGap.code_subspace_strict_codimension` |
| `AdsHappyToyNotDualityGap.happy_deficit_distribution_by_length` | yes | yes | yes | propext | `#print axioms AdsHappyToyNotDualityGap.happy_deficit_distribution_by_length` |
| `AdsHappyToyNotDualityGap.happy_disconnected_mutual_information_witnesses` | yes | yes | yes | propext | `#print axioms AdsHappyToyNotDualityGap.happy_disconnected_mutual_information_witnesses` |
| `AdsHappyToyNotDualityGap.happy_fivefold_rotational_deficit_orbit` | yes | yes | yes | propext | `#print axioms AdsHappyToyNotDualityGap.happy_fivefold_rotational_deficit_orbit` |
| `AdsHappyToyNotDualityGap.happy_short_and_long_intervals_exact_mincut` | yes | yes | yes | propext | `#print axioms AdsHappyToyNotDualityGap.happy_short_and_long_intervals_exact_mincut` |
| `AdsHappyToyNotDualityGap.happy_witness_start2_len12_deficit` | yes | yes | yes | propext | `#print axioms AdsHappyToyNotDualityGap.happy_witness_start2_len12_deficit` |
| `AdsHappyToyNotDualityGap.happy_witness_start2_len8_deficit` | yes | yes | yes | propext | `#print axioms AdsHappyToyNotDualityGap.happy_witness_start2_len8_deficit` |
| `AdsHappyToyNotDualityGap.recorded_cft_vs_stabilizer_renyi_factors` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsHappyToyNotDualityGap.recorded_cft_vs_stabilizer_renyi_factors` |
| `AdsHappyToyNotDualityGap.recorded_happy_tiling_hilbert_codimensions` | yes | yes | yes | propext | `#print axioms AdsHappyToyNotDualityGap.recorded_happy_tiling_hilbert_codimensions` |
| `AdsHappyToyNotDualityGap.renyiSpectrumDefect_formula` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsHappyToyNotDualityGap.renyiSpectrumDefect_formula` |
| `AdsHappyToyNotDualityGap.renyiSpectrumDefect_pos_of_gt_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdsHappyToyNotDualityGap.renyiSpectrumDefect_pos_of_gt_one` |

- counts toward the grade: yes

### Python: `checks/independent/ads-happy-toy-not-duality-gap.py`

- file: [checks/independent/ads-happy-toy-not-duality-gap.py](../../../checks/independent/ads-happy-toy-not-duality-gap.py)
- sha256 (`bytes`): `d123071557f5014d5e2fb57f88969974a8c68ff84a8595dffa0981c2c8f76e2a`
- cited in: node.source, record TFQ-2212
- counts toward the grade: yes

### Documents and data: `dag/derivations/32_ads_cft/tfq_2212_ads_happy_toy_not_duality_gap.md`

- file: [dag/derivations/32_ads_cft/tfq_2212_ads_happy_toy_not_duality_gap.md](../../../dag/derivations/32_ads_cft/tfq_2212_ads_happy_toy_not_duality_gap.md)
- sha256 (`lf-normalised`): `8d54e170116d2a0fe10feee741c11feaacd6537c6881b47dd7aa9a9a1e6e7ed4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2212
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ads-happy-toy-not-duality-gap.md`

- file: [dag/derivations/independent/ads-happy-toy-not-duality-gap.md](../../../dag/derivations/independent/ads-happy-toy-not-duality-gap.md)
- sha256 (`lf-normalised`): `19a0c52cc4b59b8741ff423950d447437e4d0164d4b25cfd4bac20472e60cafb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ads-happy-toy-not-duality-gap_independent.json`

- file: [dag/research/campaign_ads-happy-toy-not-duality-gap_independent.json](../../../dag/research/campaign_ads-happy-toy-not-duality-gap_independent.json)
- sha256 (`lf-normalised`): `c075e2c39474b21c6ce3b90a14d98a09f34f853e5e9f55306a838c45b98c4e7d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ads-happy-toy-not-duality-gap_lean_mutation.json`

- file: [dag/research/campaign_ads-happy-toy-not-duality-gap_lean_mutation.json](../../../dag/research/campaign_ads-happy-toy-not-duality-gap_lean_mutation.json)
- sha256 (`lf-normalised`): `074bb64c52037a51cb624c6f4d2beb3bfec219ecd2f0ad248d3d0e76821e4a46`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ads-happy-toy-not-duality-gap_lean_replay.json`

- file: [dag/research/campaign_ads-happy-toy-not-duality-gap_lean_replay.json](../../../dag/research/campaign_ads-happy-toy-not-duality-gap_lean_replay.json)
- sha256 (`lf-normalised`): `0f099654cc9e5fef3c5bc33085926ec0348391d2860bcfce409d2ac63a880faf`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1503.06237`

## Routes

Incoming (1):

- `FRO-R-ADS-HAPPY-TOY-NOT-DUALITY-GAP` `GAP_NO_DERIVATION`: [ADS-HAPPY-2015-SOURCE](ADS-HAPPY-2015-SOURCE.md) (SOURCE_RECORD), [ADS-CFT-DUALITY-IMPORT](ADS-CFT-DUALITY-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

