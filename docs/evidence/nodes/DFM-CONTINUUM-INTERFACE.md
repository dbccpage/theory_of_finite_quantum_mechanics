# DFM-CONTINUUM-INTERFACE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A finite graph dressing theorem leaves smooth-field existence, patching, topology, locality and continuum dynamics as separate obligations.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Finite witness, not a continuum theorem: on the supplied rooted tree root-p-a, root-b with chord a-b, the dressed chord is U(root-b)^{-1} U(a-b) U(p-a) U(root-p). Outer labels 2 and 5 with the other three labels trivial give dressed chords 2 and 5, while every edge incident to {a, b} is unchanged. A refinement family, compatibility maps, a topology and a convergence theorem are still required before transporting finite identities to smooth gauge theory. Smooth-field existence, continuum patching and continuum dynamics stay open.

## Source status

Source record or explicit branch obligation; status scoped to the statement.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignDfmContinuumInterface.lean`

- file: [lean4/CampaignDfmContinuumInterface.lean](../../../lean4/CampaignDfmContinuumInterface.lean)
- sha256 (`bytes`): `251415c6989141c8c9414b1b41d6c80169d272fb0f05fd8bd01bb2a5a962bb0d`
- cited in: node.lean, receipt dag/research/campaign_dfm-continuum-interface_lean_replay.json (CampaignDfmContinuumInterface), record TFQ-0401
- replay: `verified`
  - receipt [dag/research/campaign_dfm-continuum-interface_lean_replay.json](../../../dag/research/campaign_dfm-continuum-interface_lean_replay.json) (module `CampaignDfmContinuumInterface`): recorded sha256 `251415c6989141c8c9414b1b41d6c80169d272fb0f05fd8bd01bb2a5a962bb0d` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDfmContinuumInterface`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDfmContinuumInterface.dressed_chord_formula` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.dressed_chord_formula` |
| `CampaignDfmContinuumInterface.dressed_chord_witness` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.dressed_chord_witness` |
| `CampaignDfmContinuumInterface.not_star_local` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.not_star_local` |
| `CampaignDfmContinuumInterface.outer_misses_star` | yes | yes | yes | none | `#print axioms CampaignDfmContinuumInterface.outer_misses_star` |
| `CampaignDfmContinuumInterface.witness_star_agrees` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.witness_star_agrees` |
| `CampaignDfmContinuumInterface.witness_two_five` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmContinuumInterface.witness_two_five` |
| `CampaignDfmContinuumInterface.witness_two_ne_five` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDfmContinuumInterface.witness_two_ne_five` |
| `dressed_chord_formula` | yes | yes | yes | propext | `#print axioms dressed_chord_formula` |
| `not_star_local` | yes | yes | yes | propext | `#print axioms not_star_local` |
| `outer_misses_star` | yes | yes | yes | none | `#print axioms outer_misses_star` |
| `witness_star_agrees` | yes | yes | yes | propext | `#print axioms witness_star_agrees` |
| `witness_two_ne_five` | yes | yes | yes | Quot.sound, propext | `#print axioms witness_two_ne_five` |
- counts toward the grade: yes

### Python: `checks/independent/dfm-continuum-interface.py`

- file: [checks/independent/dfm-continuum-interface.py](../../../checks/independent/dfm-continuum-interface.py)
- sha256 (`bytes`): `5e27ec1ae53867db474e0e71f8065fd570f653132bfa77d5bf8ca7bf8c1e2a31`
- cited in: record TFQ-0401
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_0401_dfm_continuum_interface.md`

- file: [dag/derivations/24_dressing_field/tfq_0401_dfm_continuum_interface.md](../../../dag/derivations/24_dressing_field/tfq_0401_dfm_continuum_interface.md)
- sha256 (`lf-normalised`): `07382677404f96207c41331bcad7fadfdcf634571bb9b6957cc7981f9cad07f4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0401
- counts toward the grade: no

### Documents and data: `dag/research/electroweak_dfm_weinberg_finite_map.md`

- file: [dag/research/electroweak_dfm_weinberg_finite_map.md](../../../dag/research/electroweak_dfm_weinberg_finite_map.md)
- sha256 (`lf-normalised`): `9085e0b276afee079a11b980fc73e2c76a57d7d9b9d70fe29f97a0bd6f0b7fee`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-CONTINUUM-INTERFACE` `GAP_NO_DERIVATION`: [DFM-HIERARCHICAL-BOREL](DFM-HIERARCHICAL-BOREL.md) (OPEN), [FQ-GAP-CONTINUUM-HILBERT-LIFT](FQ-GAP-CONTINUUM-HILBERT-LIFT.md) (CONDITIONAL)

Outgoing (7):

- `APP-R-DFM-BPHZ-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-BPHZ-CONTINUUM-FENCE](DFM-BPHZ-CONTINUUM-FENCE.md) (OPEN)
- `APP-R-DFM-ELECTROWEAK-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-ELECTROWEAK-CONTINUUM-FENCE](DFM-ELECTROWEAK-CONTINUUM-FENCE.md) (OPEN)
- `APP-R-DFM-GRIBOV-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-GRIBOV-CONTINUUM-FENCE](DFM-GRIBOV-CONTINUUM-FENCE.md) (OPEN)
- `APP-R-DFM-REGGE-GRAVITY-FENCE` `GAP_NO_DERIVATION`: [DFM-REGGE-GRAVITY-FENCE](DFM-REGGE-GRAVITY-FENCE.md) (OPEN)
- `APP-R-DFM-RELATIONAL-TIME-FENCE` `GAP_NO_DERIVATION`: [DFM-RELATIONAL-TIME-FENCE](DFM-RELATIONAL-TIME-FENCE.md) (OPEN)
- `APP-R-DFM-SYMANZIK-QED-AE-FENCE` `GAP_NO_DERIVATION`: [DFM-SYMANZIK-QED-AE-FENCE](DFM-SYMANZIK-QED-AE-FENCE.md) (OPEN)
- `APP-R-DFM-Z1-Z2-COUNTERTERM-FENCE` `GAP_NO_DERIVATION`: [DFM-Z1-Z2-COUNTERTERM-FENCE](DFM-Z1-Z2-COUNTERTERM-FENCE.md) (OPEN)
