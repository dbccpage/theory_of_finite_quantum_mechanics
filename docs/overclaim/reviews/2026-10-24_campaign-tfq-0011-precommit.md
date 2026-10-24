# Overclaim review: TFQ-0011 precommit

Status: AI-drafted, awaiting human review. AuthorityEffect: None.

## Scope

`derive/TFQ-0011` against merge base `f6d4a58aa3ef`. Node TFQ-0011 statement, bottleneck, and `lean` list changed. Status stayed `OPEN`. Route `UDG-R-TFQ-0011` stayed `GAP_NO_DERIVATION`.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH 0, MEDIUM 0, LOW 3. The LOW rows are R10 on `TENSOR-ASSUMPTION-COUNTERMODELS` and R5 on two tensor notes. Those node pages changed only the sha256 of `dag/research/tensor_countermodel_validation.json` after the receipt repin. No TFQ-0011 number was flagged. Lean was rebuilt on this base (`lake --dir lean4 build CampaignTfq0011FiniteQcd`, exit 0). The independent check recomputed the rationals.

## Result

1 NARROWED, 0 FULL, 0 OVERCLAIM. Status stays `OPEN`.

## Corrections to the PR text

None. The node statement is the narrowed certificate.

## Per-node table

| Claim | Declaration | Axioms |
|---|---|---|
| Gauged four-edge product equals a^{-1}(ghkm)a in any group | `plaquette_gauge` | propext |
| S3 transpositions of 0 with 1 and of 1 with 2 do not commute | `s3_swaps_do_not_commute` | propext, Classical.choice, Quot.sound |
| That product times two identities is not 1 | `s3_two_swap_product_ne_one` | propext, Classical.choice, Quot.sound |
| At color 3: C_F=4/3, C_A=3, singlet=-4/3, octet=1/6, sextet=1/3, antitriplet=-2/3, singlet < 0, octet > 0 | `su3_channel_values` | propext, Classical.choice, Quot.sound |
| 4 C_A - C_A/3 = 11, one Dirac flavor contributes -2/3, abelian coefficient -4/3 < 0 | `gluon_split_and_one_flavor` | propext, Classical.choice, Quot.sound |
| beta0(3, n_f) at 0, 3, 5, 6, 16, 17 is 11, 9, 23/3, 7, 1/3, -1/3 | `beta0_values` | propext, Classical.choice, Quot.sound |
| For every rational n_f, beta0(3, n_f) > 0 iff n_f < 33/2 | `beta0_window` | propext, Classical.choice, Quot.sound |
| beta0(3, n) > 0 for every natural n ≤ 16 | `beta0_nat_through_16` | propext, Classical.choice, Quot.sound |
| beta0(3, 17) < 0 | `beta0_17_negative` | propext, Classical.choice, Quot.sound |
| beta1(3, n_f) = 102 - (38/3) n_f | `beta1_su3` | propext, Classical.choice, Quot.sound |
| beta1(3, n_f) at 0, 5, 16 is 102, 116/3, -302/3 | `beta1_values` | propext, Classical.choice, Quot.sound |
| (-beta0(3, 16)) / beta1(3, 16) = 1/302 | `banks_zaks_ratio_nf16` | propext, Classical.choice, Quot.sound |
| Nonzero rational b and r, t ≥ 1: area Creutz ratio equals b | `creutz_area` | propext, Classical.choice, Quot.sound |
| Same hypotheses: perimeter Creutz ratio equals 1 | `creutz_perim` | propext, Classical.choice, Quot.sound |
| At b=1/9, pairs (2,2) and (3,3): area ratio 1/9, perimeter ratio 1, and 1/9 ≠ 1 | `creutz_one_ninth` | propext, Classical.choice, Quot.sound |
| 9 - 1 = 8, 12 - 9 + 1 = 4, 12 - 8 = 4 | `declared_lattice_counts` | propext, Classical.choice, Quot.sound |

`perim_exponent` uses propext and Quot.sound. `area_exponent` uses propext, Classical.choice, and Quot.sound. Both are lemmas inside the Creutz proofs. They are not extra claims.

## Numbers recomputed

`python -I -X utf8 checks/independent/tfq-0011.py` printed `tfq-0011 independent check: 86 checks, 0 failures`. The channel values, beta0 and beta1 samples, 33/2, 1/302, the Creutz ratios at b=1/9, and the count identities match the Lean statements. No float was used.

## What the scanner could not decide

The three LOW findings name other nodes. This review does not change them. Continuum confinement, a string tension, the 12-decimal alpha_s and ln(9) strings, lattice Dirac doubling, an SU(3) matrix representation, and a constructed 3x3 complex stay outside the certificate.
