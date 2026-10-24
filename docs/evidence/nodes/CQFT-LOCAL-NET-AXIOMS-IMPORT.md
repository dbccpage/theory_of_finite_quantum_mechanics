# CQFT-LOCAL-NET-AXIOMS-IMPORT

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the four-point strict order with the ordered relations 0\<2, 1\<2 and 1\<3, the scan of all 64 triples holds, no point is related to itself, there are exactly 3 ordered relations, and exactly 3 of the 6 unordered pairs are spacelike: {0,1}, {0,3} and {2,3}. For the integer matrices A=\[\[1,2\],\[3,4\]\], B=\[\[5,6\],\[7,8\]\], X=\[\[0,1\],\[1,0\]\] and Z=\[\[1,0\],\[0,-1\]\], both (A tensor I)(I tensor B) and (I tensor B)(A tensor I) equal A tensor B, whose sixteen entries sum to 260. The products (X tensor I)(Z tensor I) and (Z tensor I)(X tensor I) differ, their (0,2) entries are -1 and 1, and XZ+ZX is the zero matrix. The determinants are det A = -2, det B = -2, det X = -1 and det Z = -1. A net of unital star-algebras indexed by continuum regions, and a Minkowski light cone, stay imported. This record does not import CausalOrder.lean and does not transport these finite counts to a continuum net.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- spacetime with causal order (assumption)
- net of local algebras with isotony and locality (assumption)

## Bottleneck

The counts and products are one supplied four-point order and four supplied integer matrices. They are not a net indexed by continuum regions and not a Minkowski light cone. The Haag-Kastler import and the external light-cone lift named by DS-QM033-064-074-083-QHELD-CONTINUUM stay open. CausalOrder.lean is not a premise of a continuum theorem in this record.

## Source status

Finite pair counts and the stated integer-matrix products were checked in Lean 4 on 2026-10-23. The continuum net and the light cone remain an imported assumption; the 1964 source wording is not audited here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignCqftLocalNetAxiomsImport.lean`

- file: [lean4/CampaignCqftLocalNetAxiomsImport.lean](../../../lean4/CampaignCqftLocalNetAxiomsImport.lean)
- sha256 (`bytes`): `3cd6c4e177ca23ac28ede54d6d85e7ab415c519b5f5fedf4e0f2af81708e1645`
- cited in: node.lean, node.source, receipt dag/research/campaign_cqft-local-net-axioms-import_lean_replay.json (CampaignCqftLocalNetAxiomsImport), record TFQ-2103
- replay: `verified`
  - receipt [dag/research/campaign_cqft-local-net-axioms-import_lean_replay.json](../../../dag/research/campaign_cqft-local-net-axioms-import_lean_replay.json) (module `CampaignCqftLocalNetAxiomsImport`): recorded sha256 `3cd6c4e177ca23ac28ede54d6d85e7ab415c519b5f5fedf4e0f2af81708e1645` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignCqftLocalNetAxiomsImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignCqftLocalNetAxiomsImport.disjoint_site_products` | yes | yes | yes | none | `#print axioms CampaignCqftLocalNetAxiomsImport.disjoint_site_products` |
| `CampaignCqftLocalNetAxiomsImport.n_poset_pair_counts` | yes | yes | yes | none | `#print axioms CampaignCqftLocalNetAxiomsImport.n_poset_pair_counts` |
| `CampaignCqftLocalNetAxiomsImport.same_site_and_star` | yes | yes | yes | none | `#print axioms CampaignCqftLocalNetAxiomsImport.same_site_and_star` |
| `disjoint_site_products` | yes | yes | yes | none | `#print axioms disjoint_site_products` |
| `n_poset_pair_counts` | yes | yes | yes | none | `#print axioms n_poset_pair_counts` |
| `same_site_and_star` | yes | yes | yes | none | `#print axioms same_site_and_star` |
- counts toward the grade: yes

### Python: `checks/independent/cqft-local-net-axioms-import.py`

- file: [checks/independent/cqft-local-net-axioms-import.py](../../../checks/independent/cqft-local-net-axioms-import.py)
- sha256 (`bytes`): `dfb013648776b7adad411c5a10779b82086a053aa9351434bdeb37b62fbd5ff4`
- cited in: node.source, record TFQ-2103
- counts toward the grade: yes

### Documents and data: `dag/derivations/31_causal_qft/tfq_2103_cqft_local_net_axioms_import.md`

- file: [dag/derivations/31_causal_qft/tfq_2103_cqft_local_net_axioms_import.md](../../../dag/derivations/31_causal_qft/tfq_2103_cqft_local_net_axioms_import.md)
- sha256 (`lf-normalised`): `6386188f7d0c019a214834dcf05f7d45e8be9f5e05d3024e02620f3cdfcf35cd`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2103
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/cqft-local-net-axioms-import.md`

- file: [dag/derivations/independent/cqft-local-net-axioms-import.md](../../../dag/derivations/independent/cqft-local-net-axioms-import.md)
- sha256 (`lf-normalised`): `cdbd16a64ec875133bc176326d8fd70c16ccd8183e0102114fd0bd84d2ef4e24`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:doi:10.1063/1.1704187`

## Routes

Incoming (1):

- `FRO-R-CQFT-LOCAL-NET-AXIOMS-IMPORT` `CONDITIONAL_ON_IMPORT`: [CQFT-HAAG-KASTLER-1964-SOURCE](CQFT-HAAG-KASTLER-1964-SOURCE.md) (SOURCE_RECORD)

Outgoing (4):

- `FRO-R-BACK-CQFT-NET-TO-QHELD` `GAP_NO_DERIVATION`: [DS-QM033-064-074-083-QHELD-CONTINUUM](DS-QM033-064-074-083-QHELD-CONTINUUM.md) (IMPORTED_ASSUMPTION)
- `FRO-R-CQFT-EPSTEIN-GLASER-1973-SOURCE` `RECORD_PARENT`: [CQFT-EPSTEIN-GLASER-1973-SOURCE](CQFT-EPSTEIN-GLASER-1973-SOURCE.md) (SOURCE_RECORD)
- `FRO-R-CQFT-FINITE-POSET-NET-TARGET` `DERIVED_LEAN`: [CQFT-FINITE-POSET-NET-TARGET](CQFT-FINITE-POSET-NET-TARGET.md) (PROVED_LEAN)
- `FRO-R-CQFT-REEH-SCHLIEDER-1961-SOURCE` `RECORD_PARENT`: [CQFT-REEH-SCHLIEDER-1961-SOURCE](CQFT-REEH-SCHLIEDER-1961-SOURCE.md) (SOURCE_RECORD)
