# DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No function of L1 weights computes the interfered weight |sum c_s|^2: L1-equivalent configurations (1,1) and (1,-1) differ by cross terms +2 / -2. Statement is relative to the supplied complex amplitude carrier.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complex amplitudes and quadratic readout |sum c|^2 (assumption)

## Bottleneck

Lean theorem names present on disk but the lake package has no build output; not rechecked.

## Source status

\[PROVEN, MECHANIZED — REUSE of pub-010 Thm 7\] (QM-061-C4)

## Review

- PFP review: [dag/results/DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: The cross term is general over rational coordinates in Lean, and no function of the two squared coordinate weights produces every coherent squared sum.
  - does not support: Transport to a chosen complex amplitude carrier and physical measurement rule. Non-descent relative to an admitted quadratic readout is not a derivation of interference from bare populations.
  - next test: Transport to a chosen complex amplitude carrier and physical measurement rule. Non-descent relative to an admitted quadratic readout is not a derivation of interference from bare populations.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0252 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm060_061_phase_fiber_and_interference_non_descent` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm060_061_phase_fiber_and_interference_non_descent` |

- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0252 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: no

### Lean: `lean4/InterferenceDeficit.lean`

- file: [lean4/InterferenceDeficit.lean](../../../lean4/InterferenceDeficit.lean)
- sha256 (`bytes`): `bdbcd7f2fc6acc5ed136b1e089fa22f27051eff8ee6f98cb54786f7ba629cb3f`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `InterferenceDeficit`): recorded sha256 `bdbcd7f2fc6acc5ed136b1e089fa22f27051eff8ee6f98cb54786f7ba629cb3f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build InterferenceDeficit`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `L1_cannot_compute_interference` | yes | yes | yes | none | `#print axioms L1_cannot_compute_interference` |
| `deficit_eq_cross_term` | yes | yes | yes | Quot.sound, propext | `#print axioms deficit_eq_cross_term` |

- counts toward the grade: yes

### Lean: `lean4/InterferenceNonDescent.lean`

- file: [lean4/InterferenceNonDescent.lean](../../../lean4/InterferenceNonDescent.lean)
- sha256 (`bytes`): `a7247e052643452607f54ef0efa5ea98df3dc763e0620558ca81080fa73eca94`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `InterferenceNonDescent`): recorded sha256 `a7247e052643452607f54ef0efa5ea98df3dc763e0620558ca81080fa73eca94` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound; only standard axioms: yes
- check: `cd lean4 && lake build InterferenceNonDescent`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `interference_non_descent` | yes | yes | yes | Quot.sound | `#print axioms interference_non_descent` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0252_interference_as_a_resource_outside_l1_bookkeeping.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0252_interference_as_a_resource_outside_l1_bookkeeping.md](../../../dag/derivations/12_finite_qm_structure/tfq_0252_interference_as_a_resource_outside_l1_bookkeeping.md)
- sha256 (`lf-normalised`): `46017b75546479fe58333c82e7b59c2620d5ef13ae0466f953e81aa77c1447bd`
- generated view: listed, not counted
- cited in: record TFQ-0252 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- `external:sha256:be048d5e98615cff70b3cdc1ebaa78a56395d67d55ca655cbb41494e307cde65::cross_term`
- `external:sha256:be048d5e98615cff70b3cdc1ebaa78a56395d67d55ca655cbb41494e307cde65::interfered_weight`
- `external:sha256:ee82f2c4e43bc6dbbb2718dd45e38dc5b5e68f42e8ffb26b169406a562071d12#QM-061-C3`
- `external:sha256:ee82f2c4e43bc6dbbb2718dd45e38dc5b5e68f42e8ffb26b169406a562071d12#QM-061-C4`
- `external:sha256:ee82f2c4e43bc6dbbb2718dd45e38dc5b5e68f42e8ffb26b169406a562071d12#QM-061-C5`

## Absences recorded by the TFQ records

- TFQ-0252 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm

## Routes

Incoming (1):

- `DS-R-INTERFERENCE` `DERIVED_LEAN`: [DS-QM060-SUPERPOSITION-QUOTIENT-FIBER](DS-QM060-SUPERPOSITION-QUOTIENT-FIBER.md) (PROVED_LEAN)

Outgoing (5):

- `DS-R-BUILDABILITY` `COMPUTED`: [DS-QM061-BUILDABILITY-SET-S](DS-QM061-BUILDABILITY-SET-S.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-EVERETT` `COMPUTED`: [DS-QM094-EVERETT-RELATIVE-STATE-CONTACT](DS-QM094-EVERETT-RELATIVE-STATE-CONTACT.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-FIVE-IMPORT` `COMPUTED`: [DS-QM207-211-FIVE-IMPORT-CASCADE](DS-QM207-211-FIVE-IMPORT-CASCADE.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-HOLONOMY-INTENSITY` `COMPUTED`: [DS-QM063-HOLONOMY-COHERENT-INTENSITY](DS-QM063-HOLONOMY-COHERENT-INTENSITY.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-THRESHOLD` `GAP_NO_DERIVATION`: [DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE](DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE.md) (OPEN)
