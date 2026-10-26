# FQ-PRIMDIFF-QUOTIENT-KERNEL

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a supplied difference delta : A x A -\> B with a supplied Zero predicate that is reflexive, symmetric and transitive on delta values, ZeroRel is an equivalence and the quotient ResidualQuotient exists; a finite presented carrier X -\> Q has same-report iff equal reports (sameReport_iff). The Zero predicate and the report map are inputs.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Zero predicate on difference values (assumption)
- finite report map X -\> Q (assumption)

## Bottleneck

Content is the quotient construction only; nothing here yields a field, norm or Hilbert structure.

## Source status

LEAN PROVED (RECEIPTED) per ledger; Lean header for the H000..H018 family says Candidate only

## Review

- PFP review: [dag/results/FQ-PRIMDIFF-QUOTIENT-KERNEL/reviews/20261019_structure_audit/review_result.json](../../../dag/results/FQ-PRIMDIFF-QUOTIENT-KERNEL/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: The supplied ZeroRel is an equivalence and class equality iff ZeroRel is rechecked generally; finite report partitions and their full equality kernels are recomputed on the retained inputs.
  - does not support: Zero, difference laws and report map remain inputs. A quotient construction alone supplies no coefficient field, norm, Hilbert structure or preferred physical readout.
  - next test: Zero, difference laws and report map remain inputs. A quotient construction alone supplies no coefficient field, norm, Hilbert structure or preferred physical readout.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/H000FinitePresentedCarrier.lean`

- file: [lean4/H000FinitePresentedCarrier.lean](../../../lean4/H000FinitePresentedCarrier.lean)
- sha256 (`bytes`): `789978ed31d30571cffbfe7efa8e8f46f6340649ab09e876289896eb5ca1a5ce`
- cited in: node.lean, record TFQ-1007
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H000FinitePresentedCarrier`): recorded sha256 `789978ed31d30571cffbfe7efa8e8f46f6340649ab09e876289896eb5ca1a5ce` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build H000FinitePresentedCarrier`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `presented_carrier_separates` | yes | yes | yes | none | `#print axioms presented_carrier_separates` |
| `sameReport_iff` | yes | yes | yes | none | `#print axioms sameReport_iff` |

- counts toward the grade: yes

### Lean: `lean4/PrimitiveDifference.lean`

- file: [lean4/PrimitiveDifference.lean](../../../lean4/PrimitiveDifference.lean)
- sha256 (`bytes`): `8748733821f0d959e698794f70d4db6595e8fe4a1a00581acd52961f751833a8`
- cited in: node.lean, record TFQ-1007
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `PrimitiveDifference`): recorded sha256 `8748733821f0d959e698794f70d4db6595e8fe4a1a00581acd52961f751833a8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build PrimitiveDifference`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `zeroRel_equivalence` | yes | yes | yes | none | `#print axioms zeroRel_equivalence` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1007
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1007_fq_primdiff_quotient_kernel.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1007_fq_primdiff_quotient_kernel.md](../../../dag/derivations/10_finite_qm_core/tfq_1007_fq_primdiff_quotient_kernel.md)
- sha256 (`lf-normalised`): `b61e8dc286ec0642dfd429621f9dfd0b6a9b7af3ff537967bdcc83039301e1f9`
- generated view: listed, not counted
- cited in: record TFQ-1007
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

## Routes

Incoming (1):

- `X-R-ROOT-TO-PRIMDIFF-KERNEL` `CONDITIONAL_ON_IMPORT`: [PG-ROOT-DIFF-STRUCTURE](PG-ROOT-DIFF-STRUCTURE.md) (ADMITTED_PRIMITIVE)

Outgoing (6):

- `FQ-R-CONTEXTUALITY` `DERIVED_LEAN`: [FQ-CONTEXTUALITY-CECH-F2](FQ-CONTEXTUALITY-CECH-F2.md) (PROVED_LEAN)
- `FQ-R-GAP-PRIM-TO-INTERFACE` `GAP_NO_DERIVATION`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)
- `FQ-R-GAP-PRIM-TO-SELECTION` `CONDITIONAL_ON_IMPORT`: [FQ-PRIM-TO-QM-SELECTION-OPEN](FQ-PRIM-TO-QM-SELECTION-OPEN.md) (CONDITIONAL)
- `FQ-R-PHASE-FIBER` `CONDITIONAL_ON_IMPORT`: [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN)
- `FQ-R-REALIFICATION` `COMPUTED`: [FQ-IMPL-REALIFICATION-ADAPTER](FQ-IMPL-REALIFICATION-ADAPTER.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-TRACE-ZERO-DUAL` `COMPUTED`: [FQ-TRACE-ZERO-DUALITY-K23](FQ-TRACE-ZERO-DUALITY-K23.md) (COMPUTATIONALLY_CHECKED)
