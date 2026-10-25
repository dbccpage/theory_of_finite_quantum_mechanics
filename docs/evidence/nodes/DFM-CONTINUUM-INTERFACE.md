# DFM-CONTINUUM-INTERFACE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A finite graph dressing theorem leaves smooth-field existence, patching, topology, locality and continuum dynamics as separate obligations.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 19
- distinct cited Lean declarations covered by a current replay receipt: 14
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
- sha256 (`bytes`): `c6fafdba1b47375722f5c8f537a089156dcc0a4fc739f5c2b0e2dea36cbf90e4`
- cited in: node.lean, receipt dag/research/campaign_dfm-continuum-interface_lean_replay.json (CampaignDfmContinuumInterface), record TFQ-0401
- replay: `verified`
  - receipt [dag/research/campaign_dfm-continuum-interface_lean_replay.json](../../../dag/research/campaign_dfm-continuum-interface_lean_replay.json) (module `CampaignDfmContinuumInterface`): recorded sha256 `c6fafdba1b47375722f5c8f537a089156dcc0a4fc739f5c2b0e2dea36cbf90e4` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDfmContinuumInterface`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDfmContinuumInterface.Dependency.Plan.changed_label` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmContinuumInterface.Dependency.Plan.changed_label` |
| `CampaignDfmContinuumInterface.Dependency.Plan.evaluate_agrees` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.Dependency.Plan.evaluate_agrees` |
| `CampaignDfmContinuumInterface.Dependency.Plan.evaluate_agrees_on_superset` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.Dependency.Plan.evaluate_agrees_on_superset` |
| `CampaignDfmContinuumInterface.Dependency.Plan.evaluate_formula` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.Dependency.Plan.evaluate_formula` |
| `CampaignDfmContinuumInterface.Dependency.transport_agrees` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.Dependency.transport_agrees` |
| `CampaignDfmContinuumInterface.dressed_chord_formula` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.dressed_chord_formula` |
| `CampaignDfmContinuumInterface.dressed_chord_witness` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.dressed_chord_witness` |
| `CampaignDfmContinuumInterface.not_star_local` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.not_star_local` |
| `CampaignDfmContinuumInterface.outer_in_footprint` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.outer_in_footprint` |
| `CampaignDfmContinuumInterface.outer_misses_star` | yes | yes | yes | none | `#print axioms CampaignDfmContinuumInterface.outer_misses_star` |
| `CampaignDfmContinuumInterface.witness_plan_evaluate` | yes | yes | yes | propext | `#print axioms CampaignDfmContinuumInterface.witness_plan_evaluate` |
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
- sha256 (`bytes`): `17f37543b78c25ba4f84e40ffb904c0df8a0e37cb16436302d7ec7e4b5aa19de`
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

- `APP-R-DFM-CONTINUUM-INTERFACE` `GAP_NO_DERIVATION`: [DFM-HIERARCHICAL-BOREL](DFM-HIERARCHICAL-BOREL.md) (PROVED_LEAN), [FQ-GAP-CONTINUUM-HILBERT-LIFT](FQ-GAP-CONTINUUM-HILBERT-LIFT.md) (CONDITIONAL)

Outgoing (7):

- `APP-R-DFM-BPHZ-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-BPHZ-CONTINUUM-FENCE](DFM-BPHZ-CONTINUUM-FENCE.md) (OPEN)
- `APP-R-DFM-ELECTROWEAK-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-ELECTROWEAK-CONTINUUM-FENCE](DFM-ELECTROWEAK-CONTINUUM-FENCE.md) (OPEN)
- `APP-R-DFM-GRIBOV-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-GRIBOV-CONTINUUM-FENCE](DFM-GRIBOV-CONTINUUM-FENCE.md) (OPEN)
- `APP-R-DFM-REGGE-GRAVITY-FENCE` `GAP_NO_DERIVATION`: [DFM-REGGE-GRAVITY-FENCE](DFM-REGGE-GRAVITY-FENCE.md) (OPEN)
- `APP-R-DFM-RELATIONAL-TIME-FENCE` `GAP_NO_DERIVATION`: [DFM-RELATIONAL-TIME-FENCE](DFM-RELATIONAL-TIME-FENCE.md) (OPEN)
- `APP-R-DFM-SYMANZIK-QED-AE-FENCE` `GAP_NO_DERIVATION`: [DFM-SYMANZIK-QED-AE-FENCE](DFM-SYMANZIK-QED-AE-FENCE.md) (OPEN)
- `APP-R-DFM-Z1-Z2-COUNTERTERM-FENCE` `GAP_NO_DERIVATION`: [DFM-Z1-Z2-COUNTERTERM-FENCE](DFM-Z1-Z2-COUNTERTERM-FENCE.md) (OPEN)
