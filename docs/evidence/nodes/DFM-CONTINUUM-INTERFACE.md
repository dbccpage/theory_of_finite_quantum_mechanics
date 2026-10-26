# DFM-CONTINUUM-INTERFACE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A finite graph dressing theorem leaves smooth-field existence, patching, topology, locality and continuum dynamics as separate obligations. Conditional continuum result: In a supplied complete metric topological group with d(ab,cd) \<= d(a,c)+d(b,d), binary edge split errors bounded by C*q^depth, C \>= 0 and 0 \<= q \< 1/2, yield unique transport limits with error at most C*q^depth*(2*q)^n/(1-2*q). The limits respect binary composition and compatible endpoint gauges. Continuous parameterized edge families with a common C and q converge uniformly to continuous limiting transports. At q=1/2, the additive edge values depth/2^depth have shrinking split defects but root transport n, with no limit.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 40
- distinct cited Lean declarations covered by a current replay receipt: 35
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complete metric topological group with the stated product-distance estimate
- supplied binary edge-label family with C \>= 0, q \>= 0, 2*q \< 1 and uniform split-defect bound
- compatible endpoint gauges; for continuity, a parameter topology and continuous edge maps with common constants

## Bottleneck

New conditional result: In a supplied complete metric topological group with d(ab,cd) \<= d(a,c)+d(b,d), binary edge split errors bounded by C*q^depth, C \>= 0 and 0 \<= q \< 1/2, yield unique transport limits with error at most C*q^depth*(2*q)^n/(1-2*q). The limits respect binary composition and compatible endpoint gauges. Continuous parameterized edge families with a common C and q converge uniformly to continuous limiting transports. At q=1/2, the additive edge values depth/2^depth have shrinking split defects but root transport n, with no limit. Remaining obligation: The complete metric, group topology, refinement family and geometric local bound are supplied. Smooth-field existence, arbitrary triangulation refinements, patching, physical locality and continuum dynamics are not derived; the original node and physical bridge remain OPEN. Earlier finite witness boundary (historical): Finite witness, not a continuum theorem: on the supplied rooted tree root-p-a, root-b with chord a-b, the dressed chord is U(root-b)^{-1} U(a-b) U(p-a) U(root-p). Outer labels 2 and 5 with the other three labels trivial give dressed chords 2 and 5, while every edge incident to {a, b} is unchanged. A refinement family, compatibility maps, a topology and a convergence theorem are still required before transporting finite identities to smooth gauge theory. Smooth-field existence, continuum patching and continuum dynamics stay open.

## Source status

Source record or explicit branch obligation; status scoped to the statement. Current controlled continuum theorem kernel-checked separately; the broader node remains OPEN.

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

### Lean: `lean4/CampaignDfmRefinementLimit.lean`

- file: [lean4/CampaignDfmRefinementLimit.lean](../../../lean4/CampaignDfmRefinementLimit.lean)
- sha256 (`bytes`): `b56f742d6f4d0cbd6c71cc7fe5d9e08fc3660a543e5cf1e34072588009c252fb`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-continuum-refinement-limit_lean_replay.json (CampaignDfmRefinementLimit), record TFQ-0401
- replay: `verified`
  - receipt [dag/research/campaign_dfm-continuum-refinement-limit_lean_replay.json](../../../dag/research/campaign_dfm-continuum-refinement-limit_lean_replay.json) (module `CampaignDfmRefinementLimit`): recorded sha256 `b56f742d6f4d0cbd6c71cc7fe5d9e08fc3660a543e5cf1e34072588009c252fb` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDfmRefinementLimit`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDfmRefinementLimit.Controlled` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.Controlled` |
| `CampaignDfmRefinementLimit.Controlled.dressed_tendsto` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.Controlled.dressed_tendsto` |
| `CampaignDfmRefinementLimit.Controlled.error_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.Controlled.error_bound` |
| `CampaignDfmRefinementLimit.Controlled.exists_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.Controlled.exists_limit` |
| `CampaignDfmRefinementLimit.Controlled.limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.Controlled.limit` |
| `CampaignDfmRefinementLimit.Controlled.limit_split` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.Controlled.limit_split` |
| `CampaignDfmRefinementLimit.Controlled.limit_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.Controlled.limit_unique` |
| `CampaignDfmRefinementLimit.Controlled.tendsto_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.Controlled.tendsto_limit` |
| `CampaignDfmRefinementLimit.EndpointGauge` | yes | yes | yes | none | `#print axioms CampaignDfmRefinementLimit.EndpointGauge` |
| `CampaignDfmRefinementLimit.EndpointGauge.dress` | yes | yes | yes | propext | `#print axioms CampaignDfmRefinementLimit.EndpointGauge.dress` |
| `CampaignDfmRefinementLimit.Word` | yes | yes | yes | none | `#print axioms CampaignDfmRefinementLimit.Word` |
| `CampaignDfmRefinementLimit.continuous_refinement_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.continuous_refinement_limit` |
| `CampaignDfmRefinementLimit.continuous_transport` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.continuous_transport` |
| `CampaignDfmRefinementLimit.criticalEdge` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.criticalEdge` |
| `CampaignDfmRefinementLimit.critical_no_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.critical_no_limit` |
| `CampaignDfmRefinementLimit.critical_split_defect` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.critical_split_defect` |
| `CampaignDfmRefinementLimit.critical_transport` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.critical_transport` |
| `CampaignDfmRefinementLimit.step_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.step_bound` |
| `CampaignDfmRefinementLimit.transport` | yes | yes | yes | none | `#print axioms CampaignDfmRefinementLimit.transport` |
| `CampaignDfmRefinementLimit.transport_dress` | yes | yes | yes | propext | `#print axioms CampaignDfmRefinementLimit.transport_dress` |
| `CampaignDfmRefinementLimit.uniform_refinement_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignDfmRefinementLimit.uniform_refinement_limit` |

- counts toward the grade: yes

### Python: `checks/independent/dfm-continuum-interface.py`

- file: [checks/independent/dfm-continuum-interface.py](../../../checks/independent/dfm-continuum-interface.py)
- sha256 (`bytes`): `17f37543b78c25ba4f84e40ffb904c0df8a0e37cb16436302d7ec7e4b5aa19de`
- cited in: record TFQ-0401
- counts toward the grade: yes

### Python: `checks/independent/dfm-continuum-refinement-limit.py`

- file: [checks/independent/dfm-continuum-refinement-limit.py](../../../checks/independent/dfm-continuum-refinement-limit.py)
- sha256 (`bytes`): `f4954a40a525a19e69588eb436c2810f2c021e4456e6d4f3595998ff41c0220d`
- cited in: node.source, record TFQ-0401
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_0401_dfm_continuum_interface.md`

- file: [dag/derivations/24_dressing_field/tfq_0401_dfm_continuum_interface.md](../../../dag/derivations/24_dressing_field/tfq_0401_dfm_continuum_interface.md)
- sha256 (`lf-normalised`): `6718e2313508f6f6ff3610f99f9f0ae8c91fe48c9c10ac7e394f1deaee2206e3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0401
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-continuum-refinement-limit.md`

- file: [dag/derivations/independent/dfm-continuum-refinement-limit.md](../../../dag/derivations/independent/dfm-continuum-refinement-limit.md)
- sha256 (`lf-normalised`): `199f91dcd9bb26c55240196ad66dba656b26070a5f921f08f97bf1cef4a8066b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_dfm-continuum-refinement-limit_lean_replay.json`

- file: [dag/research/campaign_dfm-continuum-refinement-limit_lean_replay.json](../../../dag/research/campaign_dfm-continuum-refinement-limit_lean_replay.json)
- sha256 (`lf-normalised`): `7b9cbf2a84505205171e31fe5a3d7478173ef2011e41d80638a39f3dd5bb3e97`
- cited in: node.source
- counts toward the grade: yes

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
