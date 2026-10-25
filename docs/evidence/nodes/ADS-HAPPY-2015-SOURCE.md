# ADS-HAPPY-2015-SOURCE

Stage: [ADS_CFT](../stages/ADS_CFT.md). Status: `SOURCE_RECORD`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Pastawski, Yoshida, Harlow and Preskill (2015, arXiv:1503.06237) define a 2n-leg perfect tensor (Section 2 Def. 2 p. 5: proportional to an isometric tensor for every bipartition into k \<= n inputs and 2n - k outputs), construct the 6-qubit perfect stabilizer tensor from the \[\[5,1,3\]\] code of Laflamme et al. (1996, arXiv:quant-ph/9602019 Table I; HaPPY Appendix A.1 eqs. (A1)-(A7) pp. 24-25), and place it on the {5,4} hyperbolic pentagon tiling to obtain an isometric bulk-to-boundary code (Section 3 Thm. 1 p. 7) in which connected boundary regions of holographic states satisfy S_A = |gamma_A| log v (Section 4.1 Thm. 2 p. 8) and general regions satisfy the greedy-geodesic lower bound (Section 4.2 Thm. 3 eq. (4.10) p. 10). This node records the paper as published.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Record only. The abstract itself calls the codes toy models.

## Source status

Audited against the full texts of arXiv:1503.06237 (Section 2 Def. 2 p. 5, Section 3 Thm. 1 p. 7, Section 4 Thms. 2, 3, 6 pp. 8-14, Appendix A.1 pp. 24-25) and arXiv:quant-ph/9602019 (Table I p. 2) on 2026-10-22; recorded as an external source record.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/H036ThreeQubitCodeSyndromeRecovery.lean`

- file: [lean4/H036ThreeQubitCodeSyndromeRecovery.lean](../../../lean4/H036ThreeQubitCodeSyndromeRecovery.lean)
- sha256 (`bytes`): `b15c930d114e54c9c99010142e46019afa0af0d2cfa4507c9634cc5d00a81ca7`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_ads_cft.json](../../../dag/research/lean_replay_campaign_ads_cft.json) (module `H036ThreeQubitCodeSyndromeRecovery`): recorded sha256 `b15c930d114e54c9c99010142e46019afa0af0d2cfa4507c9634cc5d00a81ca7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build H036ThreeQubitCodeSyndromeRecovery`
- counts toward the grade: yes

### Lean: `lean4/H037FourQubitCssSurfaceCode.lean`

- file: [lean4/H037FourQubitCssSurfaceCode.lean](../../../lean4/H037FourQubitCssSurfaceCode.lean)
- sha256 (`bytes`): `4158b6fcea88a91421d0cc9d5a4f17fd8e3bab9454d6c9ed2775afbafaba0d71`
- cited in: node.source
- replay: `none`
- check: `cd lean4 && lake build H037FourQubitCssSurfaceCode`
- counts toward the grade: yes

### Lean: `lean4/H042ShorNineQubitCode.lean`

- file: [lean4/H042ShorNineQubitCode.lean](../../../lean4/H042ShorNineQubitCode.lean)
- sha256 (`bytes`): `6bb233631905c18bbef63f8fa4a9b3b012a65d33d14c187e3e7f8b9fe2df82c9`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_ads_cft.json](../../../dag/research/lean_replay_campaign_ads_cft.json) (module `H042ShorNineQubitCode`): recorded sha256 `6bb233631905c18bbef63f8fa4a9b3b012a65d33d14c187e3e7f8b9fe2df82c9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build H042ShorNineQubitCode`
- counts toward the grade: yes

### Lean: `lean4/H044SurfaceCodeToricTopology.lean`

- file: [lean4/H044SurfaceCodeToricTopology.lean](../../../lean4/H044SurfaceCodeToricTopology.lean)
- sha256 (`bytes`): `fb7dabdab6050799ef04a17f7ca0892c4cab39b4781db08d9445a9496915e15b`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_ads_cft.json](../../../dag/research/lean_replay_campaign_ads_cft.json) (module `H044SurfaceCodeToricTopology`): recorded sha256 `fb7dabdab6050799ef04a17f7ca0892c4cab39b4781db08d9445a9496915e15b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build H044SurfaceCodeToricTopology`
- counts toward the grade: yes

### Documents and data: `dag/derivations/32_ads_cft/tfq_2207_ads_happy_2015_source.md`

- file: [dag/derivations/32_ads_cft/tfq_2207_ads_happy_2015_source.md](../../../dag/derivations/32_ads_cft/tfq_2207_ads_happy_2015_source.md)
- sha256 (`lf-normalised`): `63cecb5b096077a909f2d0c2f5c2ed391863650ce68b9ca7ee2a0f162b5a9666`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2207
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1503.06237`
- `external:arXiv:quant-ph/9602019`

## Routes

Incoming (1):

- `FRO-R-ADS-HAPPY-2015-SOURCE` `RECORD_PARENT`: [ADS-ADH-2015-SOURCE](ADS-ADH-2015-SOURCE.md) (SOURCE_RECORD), [TFQ-0048](TFQ-0048.md) (COMPUTATIONALLY_CHECKED)

Outgoing (2):

- `FRO-R-ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET` `DERIVED_LEAN`: [ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET](ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET.md) (PROVED_LEAN)
- `FRO-R-ADS-HAPPY-TOY-NOT-DUALITY-GAP` `GAP_NO_DERIVATION`: [ADS-HAPPY-TOY-NOT-DUALITY-GAP](ADS-HAPPY-TOY-NOT-DUALITY-GAP.md) (OPEN)
