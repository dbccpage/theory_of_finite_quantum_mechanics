# DS-QM081-STOCHASTIC-L1-CONTRACTION

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A column-stochastic kernel does not increase the L1 norm: |Sx|_1 \<= |x|_1 (finite classical shadow of trace-norm contraction).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Operator trace-norm contractivity on M_n(C) not mechanized (upgrade row QM-081-C4).

## Source status

\[MECHANIZED\] ENC-1055 (QM-081-C5)

## Review

- PFP review: [dag/results/DS-QM081-STOCHASTIC-L1-CONTRACTION/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM081-STOCHASTIC-L1-CONTRACTION/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Generic finite rational column-stochastic L1 contraction is kernel checked; retained three-state outputs and triangle budgets are exact.
  - does not support: Transport the array implementation to the formal finite sums and any supplied quantum/CPTP interface. Classical contraction does not derive a quantum carrier.
  - next test: Transport the array implementation to the formal finite sums and any supplied quantum/CPTP interface. Classical contraction does not derive a quantum carrier.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0264 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` |
| `QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0264_monotonicity_does_not_select_the_trace_norm.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0264_monotonicity_does_not_select_the_trace_norm.md](../../../dag/derivations/12_finite_qm_structure/tfq_0264_monotonicity_does_not_select_the_trace_norm.md)
- sha256 (`lf-normalised`): `f7afb5c8b184d4faf8cc11f6f08962e178251d4f34f7578c72c09ddb80d85458`
- generated view: listed, not counted
- cited in: record TFQ-0264 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:60cc18d70e290afb3a082e12f6a048f625b9e9dcc24a29b10c25a023ac4e39ec#QM-081-C5`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_ds_qm_dynamics_structure_and_majorana_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- `external:sha256:c223d9defa7e19e64a7c5c8c484d3063f47c07f01d8e763fcc5532ed210e33c0#QM-082-C4`

## Absences recorded by the TFQ records

- TFQ-0264 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0264 rust: no local rust twin located for external:sha256:8de9a137f60908341dba42d28fa768bf1da772772d76f839787a5fcc9b56f170
- TFQ-0264 rust: no local rust twin located for external:sha256:e17359f64c885efb596f3390cf43cc40c25011d24ded59d783982b1eb15318df

## Routes

Incoming (1):

- `DS-R-STOCHASTIC-CONTRACTION` `DERIVED_LEAN`: [DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL](DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `DS-R-TRACE-NORM-CORE-FROM-CARRIER` `COMPUTED`: [DS-QM080-IMPORT-FREE-TRACE-NORM-CORE](DS-QM080-IMPORT-FREE-TRACE-NORM-CORE.md) (COMPUTATIONALLY_CHECKED)
