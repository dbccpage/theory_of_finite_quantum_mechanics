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

### Lean: `lean4/DressingFieldContinuumInterface.lean`

- file: [lean4/DressingFieldContinuumInterface.lean](../../../lean4/DressingFieldContinuumInterface.lean)
- sha256 (`bytes`): `3f1ecf2586d69c69db693eba7867a68daafea77f6834dfb26b6369f9125d3f9b`
- cited in: node.lean, receipt dag/research/campaign_dfm-continuum-interface_lean_replay.json (DressingFieldContinuumInterface), record TFQ-0401
- replay: `verified`
  - receipt [dag/research/campaign_dfm-continuum-interface_lean_replay.json](../../../dag/research/campaign_dfm-continuum-interface_lean_replay.json) (module `DressingFieldContinuumInterface`): recorded sha256 `3f1ecf2586d69c69db693eba7867a68daafea77f6834dfb26b6369f9125d3f9b` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DressingFieldContinuumInterface`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DressingFieldContinuumInterface.Dependency.Plan.changed_label` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldContinuumInterface.Dependency.Plan.changed_label` |
| `DressingFieldContinuumInterface.Dependency.Plan.evaluate_agrees` | yes | yes | yes | propext | `#print axioms DressingFieldContinuumInterface.Dependency.Plan.evaluate_agrees` |
| `DressingFieldContinuumInterface.Dependency.Plan.evaluate_agrees_on_superset` | yes | yes | yes | propext | `#print axioms DressingFieldContinuumInterface.Dependency.Plan.evaluate_agrees_on_superset` |
| `DressingFieldContinuumInterface.Dependency.Plan.evaluate_formula` | yes | yes | yes | propext | `#print axioms DressingFieldContinuumInterface.Dependency.Plan.evaluate_formula` |
| `DressingFieldContinuumInterface.Dependency.transport_agrees` | yes | yes | yes | propext | `#print axioms DressingFieldContinuumInterface.Dependency.transport_agrees` |
| `DressingFieldContinuumInterface.dressed_chord_formula` | yes | yes | yes | propext | `#print axioms DressingFieldContinuumInterface.dressed_chord_formula` |
| `DressingFieldContinuumInterface.dressed_chord_witness` | yes | yes | yes | propext | `#print axioms DressingFieldContinuumInterface.dressed_chord_witness` |
| `DressingFieldContinuumInterface.not_star_local` | yes | yes | yes | propext | `#print axioms DressingFieldContinuumInterface.not_star_local` |
| `DressingFieldContinuumInterface.outer_in_footprint` | yes | yes | yes | propext | `#print axioms DressingFieldContinuumInterface.outer_in_footprint` |
| `DressingFieldContinuumInterface.outer_misses_star` | yes | yes | yes | none | `#print axioms DressingFieldContinuumInterface.outer_misses_star` |
| `DressingFieldContinuumInterface.witness_plan_evaluate` | yes | yes | yes | propext | `#print axioms DressingFieldContinuumInterface.witness_plan_evaluate` |
| `DressingFieldContinuumInterface.witness_star_agrees` | yes | yes | yes | propext | `#print axioms DressingFieldContinuumInterface.witness_star_agrees` |
| `DressingFieldContinuumInterface.witness_two_five` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldContinuumInterface.witness_two_five` |
| `DressingFieldContinuumInterface.witness_two_ne_five` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldContinuumInterface.witness_two_ne_five` |
| `dressed_chord_formula` | yes | yes | yes | propext | `#print axioms dressed_chord_formula` |
| `not_star_local` | yes | yes | yes | propext | `#print axioms not_star_local` |
| `outer_misses_star` | yes | yes | yes | none | `#print axioms outer_misses_star` |
| `witness_star_agrees` | yes | yes | yes | propext | `#print axioms witness_star_agrees` |
| `witness_two_ne_five` | yes | yes | yes | Quot.sound, propext | `#print axioms witness_two_ne_five` |

- counts toward the grade: yes

### Lean: `lean4/DressingFieldRefinementLimit.lean`

- file: [lean4/DressingFieldRefinementLimit.lean](../../../lean4/DressingFieldRefinementLimit.lean)
- sha256 (`bytes`): `19ff11d132d403af3df0b05d760411a9394d25fc0b36b4e8b7fdb1f06309f1af`
- cited in: node.lean, node.source, receipt dag/research/campaign_dfm-continuum-refinement-limit_lean_replay.json (DressingFieldRefinementLimit), record TFQ-0401
- replay: `verified`
  - receipt [dag/research/campaign_dfm-continuum-refinement-limit_lean_replay.json](../../../dag/research/campaign_dfm-continuum-refinement-limit_lean_replay.json) (module `DressingFieldRefinementLimit`): recorded sha256 `19ff11d132d403af3df0b05d760411a9394d25fc0b36b4e8b7fdb1f06309f1af` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DressingFieldRefinementLimit`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DressingFieldRefinementLimit.Controlled` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.Controlled` |
| `DressingFieldRefinementLimit.Controlled.dressed_tendsto` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.Controlled.dressed_tendsto` |
| `DressingFieldRefinementLimit.Controlled.error_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.Controlled.error_bound` |
| `DressingFieldRefinementLimit.Controlled.exists_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.Controlled.exists_limit` |
| `DressingFieldRefinementLimit.Controlled.limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.Controlled.limit` |
| `DressingFieldRefinementLimit.Controlled.limit_split` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.Controlled.limit_split` |
| `DressingFieldRefinementLimit.Controlled.limit_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.Controlled.limit_unique` |
| `DressingFieldRefinementLimit.Controlled.tendsto_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.Controlled.tendsto_limit` |
| `DressingFieldRefinementLimit.EndpointGauge` | yes | yes | yes | none | `#print axioms DressingFieldRefinementLimit.EndpointGauge` |
| `DressingFieldRefinementLimit.EndpointGauge.dress` | yes | yes | yes | propext | `#print axioms DressingFieldRefinementLimit.EndpointGauge.dress` |
| `DressingFieldRefinementLimit.Word` | yes | yes | yes | none | `#print axioms DressingFieldRefinementLimit.Word` |
| `DressingFieldRefinementLimit.continuous_refinement_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.continuous_refinement_limit` |
| `DressingFieldRefinementLimit.continuous_transport` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.continuous_transport` |
| `DressingFieldRefinementLimit.criticalEdge` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.criticalEdge` |
| `DressingFieldRefinementLimit.critical_no_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.critical_no_limit` |
| `DressingFieldRefinementLimit.critical_split_defect` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.critical_split_defect` |
| `DressingFieldRefinementLimit.critical_transport` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.critical_transport` |
| `DressingFieldRefinementLimit.step_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.step_bound` |
| `DressingFieldRefinementLimit.transport` | yes | yes | yes | none | `#print axioms DressingFieldRefinementLimit.transport` |
| `DressingFieldRefinementLimit.transport_dress` | yes | yes | yes | propext | `#print axioms DressingFieldRefinementLimit.transport_dress` |
| `DressingFieldRefinementLimit.uniform_refinement_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldRefinementLimit.uniform_refinement_limit` |

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
- sha256 (`lf-normalised`): `9811fef616bbe4a7974c1cdb1ccf9b2574e07e74b70ed6e3ff128fec59c4e378`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0401
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-continuum-refinement-limit.md`

- file: [dag/derivations/independent/dfm-continuum-refinement-limit.md](../../../dag/derivations/independent/dfm-continuum-refinement-limit.md)
- sha256 (`lf-normalised`): `fbcba7e57b6eddd5b53eaf9bac795fd4e3d5153eeb11786abf84e0a2e6dca493`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_dfm-continuum-refinement-limit_lean_replay.json`

- file: [dag/research/campaign_dfm-continuum-refinement-limit_lean_replay.json](../../../dag/research/campaign_dfm-continuum-refinement-limit_lean_replay.json)
- sha256 (`lf-normalised`): `900745fe5193694ae7595e86b5c563b88c48ba31a6cac90225e458937a4435ee`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/electroweak_dfm_weinberg_finite_map.md`

- file: [dag/research/electroweak_dfm_weinberg_finite_map.md](../../../dag/research/electroweak_dfm_weinberg_finite_map.md)
- sha256 (`lf-normalised`): `455adaf17dfdca6638d17a8882f0ef419bbd3f08adfaacf30de3c1516c42611e`
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
