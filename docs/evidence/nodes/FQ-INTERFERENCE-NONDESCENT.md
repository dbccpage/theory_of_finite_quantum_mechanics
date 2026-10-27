# FQ-INTERFERENCE-NONDESCENT

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Hadamard-style mixing separates points of one phase-blind fiber: no function f satisfies readout = f o phaseBlind once mixing is applied (no_descent_through_fiber, mix_separates). Phase information is observable only after a non-diagonal operation.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- non-diagonal measurement context (assumption)

## Bottleneck

The second (non-diagonal) context is admitted, not derived (QM-209 residual import).

## Source status

ledger: LEAN PROVED (RECEIPTED); H010 header Candidate only

## Review

- PFP review: [dag/results/FQ-INTERFERENCE-NONDESCENT/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-INTERFERENCE-NONDESCENT/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: No function of the original exact populations can reproduce the source mixed readout for all Gaussian-integer vectors. The source Hadamard witness doubles total weight; the rational rotation control separately preserves mass.
  - does not support: Derive or explicitly admit the non-diagonal context, preparation access and any physical interpretation. The raw Hadamard output is not normalized probability.
  - next test: Derive or explicitly admit the non-diagonal context, preparation access and any physical interpretation. The raw Hadamard output is not normalized probability.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: record TFQ-0252 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`
- counts toward the grade: no

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0252 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: no

### Lean: `lean4/InterferenceNonDescent.lean`

- file: [lean4/InterferenceNonDescent.lean](../../../lean4/InterferenceNonDescent.lean)
- sha256 (`bytes`): `a7247e052643452607f54ef0efa5ea98df3dc763e0620558ca81080fa73eca94`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `InterferenceNonDescent`): recorded sha256 `a7247e052643452607f54ef0efa5ea98df3dc763e0620558ca81080fa73eca94` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound; only standard axioms: yes
- check: `cd lean4 && lake build InterferenceNonDescent`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mix_separates` | yes | yes | yes | none | `#print axioms mix_separates` |
| `no_descent_through_fiber` | yes | yes | yes | Quot.sound | `#print axioms no_descent_through_fiber` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0252_interference_as_a_resource_outside_l1_bookkeeping.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0252_interference_as_a_resource_outside_l1_bookkeeping.md](../../../dag/derivations/12_finite_qm_structure/tfq_0252_interference_as_a_resource_outside_l1_bookkeeping.md)
- sha256 (`lf-normalised`): `46017b75546479fe58333c82e7b59c2620d5ef13ae0466f953e81aa77c1447bd`
- generated view: listed, not counted
- cited in: record TFQ-0252 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics_claim_ledger.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics_claim_ledger.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics_claim_ledger.md)
- sha256 (`lf-normalised`): `259e971c72c485503b9c9f157bec6ec9412fe24b8c4cc266e1d0ab6aa7e2d1e0`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:be048d5e98615cff70b3cdc1ebaa78a56395d67d55ca655cbb41494e307cde65::cross_term`

## Absences recorded by the TFQ records

- TFQ-0252 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm

## Routes

Incoming (1):

- `FQ-R-NONDESCENT` `DERIVED_LEAN`: [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN)

Outgoing (0):

