# PG-ADMISSION-FLOOR

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For an exhibited cut (two distinct endpoints under a law), the endpoints are apart, no cut exists on a subsingleton carrier, and identifying the endpoints breaks the law; instance-without-law and law-without-instance each allow a singleton. A pointed relation does not decide distinctness in either direction (pointed_relation_independence).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- distinct cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Exhibited cut with law (assumption: supplied, not selected from equality alone)

## Bottleneck

Shows a law is needed to separate endpoints; does not derive the law from \<\> or from Real_0.

## Source status

WDP primitive admission floor (Lean file); WDP-CH01-P01/P02 FINITE_PROVED

## Review

- PFP review: [dag/results/PG-ADMISSION-FLOOR/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/PG-ADMISSION-FLOOR/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: A law-bearing cut (an irreflexive relation with an exhibited pair) exists exactly on carriers with two distinct points, its endpoints are apart, and a map separates the endpoints of every cut it carries into an irreflexive target; the pair of marks alone does not supply the relation or its law.
  - does not support: Deriving the law (irreflexivity) from the primitive difference \<\> or from Real_0: the relation and its law remain supplied data; any selection of a preferred cut or orientation (two orientations exist on two points); infinite carriers beyond the Lean statements; the arity-cost tie-breaker of the source (declared_arity_cost_selects is a decide on a priced toy, not used here); the aggregate local theorem pg_to_sn_and_wdp_route_chain_composition, which is a fixed enumeration.
  - next test: Replay the admission-floor model counts on 1..4 points with the declared Real_0 axiom list added as constraints and decide whether any declared axiom forces irreflexivity of the relation, i.e. whether the counts of relations with an exhibited pair but no law drop to zero.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AdmissionFloor.lean`

- file: [lean4/AdmissionFloor.lean](../../../lean4/AdmissionFloor.lean)
- sha256 (`bytes`): `6974f4c9df701c53aac00d5831e99669b5f2810c7a2e1587763cc6ed1324a717`
- cited in: node.lean, receipt dag/research/pfp_batch01_lean_replay.json (AdmissionFloor)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `AdmissionFloor`): recorded sha256 `6974f4c9df701c53aac00d5831e99669b5f2810c7a2e1587763cc6ed1324a717` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build AdmissionFloor`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AdmissionFloor.cut_exists_iff_nontrivial` | yes | yes | yes | none | `#print axioms AdmissionFloor.cut_exists_iff_nontrivial` |
| `AdmissionFloor.endpoints_apart` | yes | yes | yes | none | `#print axioms AdmissionFloor.endpoints_apart` |
| `AdmissionFloor.exists_law_target_iff` | yes | yes | yes | none | `#print axioms AdmissionFloor.exists_law_target_iff` |
| `AdmissionFloor.identification_breaks_law` | yes | yes | yes | none | `#print axioms AdmissionFloor.identification_breaks_law` |
| `AdmissionFloor.instance_without_law` | yes | yes | yes | none | `#print axioms AdmissionFloor.instance_without_law` |
| `AdmissionFloor.law_not_derived_from_distinctness` | yes | yes | yes | none | `#print axioms AdmissionFloor.law_not_derived_from_distinctness` |
| `AdmissionFloor.law_without_instance` | yes | yes | yes | none | `#print axioms AdmissionFloor.law_without_instance` |
| `AdmissionFloor.no_cut_on_subsingleton` | yes | yes | yes | none | `#print axioms AdmissionFloor.no_cut_on_subsingleton` |
| `AdmissionFloor.one_point_cut_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdmissionFloor.one_point_cut_count` |
| `AdmissionFloor.pointed_relation_independence` | yes | yes | yes | none | `#print axioms AdmissionFloor.pointed_relation_independence` |
| `AdmissionFloor.two_point_cut_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AdmissionFloor.two_point_cut_count` |

- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean)
- sha256 (`bytes`): `9a5d905d70db6124a31a54d1616dfb70308ee04c095302061e86919afbe9d5d8`
- cited in: node.lean, node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.WitnessedDifference.WitnessedDifference.PointedRelation`): recorded sha256 `9a5d905d70db6124a31a54d1616dfb70308ee04c095302061e86919afbe9d5d8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pointed_relation_independence` | yes | yes | yes | none | `#print axioms pointed_relation_independence` |

- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/PrimitiveAdmissionFloor.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/PrimitiveAdmissionFloor.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/PrimitiveAdmissionFloor.lean)
- sha256 (`bytes`): `e96f39ed83bdbf1bbf0b2141181770a58ee100528400ddda415e09a9426279ac`
- cited in: node.lean, node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.WitnessedDifference.WitnessedDifference.PrimitiveAdmissionFloor`): recorded sha256 `e96f39ed83bdbf1bbf0b2141181770a58ee100528400ddda415e09a9426279ac` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/PrimitiveAdmissionFloor.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `endpoints_apart` | yes | yes | yes | none | `#print axioms endpoints_apart` |
| `identification_breaks_law` | yes | yes | yes | none | `#print axioms identification_breaks_law` |
| `no_cut_on_subsingleton` | yes | yes | yes | none | `#print axioms no_cut_on_subsingleton` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_admission_execution.rs`

- file: [code/rust/src/wdp/genesis_admission_execution.rs](../../../code/rust/src/wdp/genesis_admission_execution.rs)
- sha256 (`bytes`): `8a4f92fda652d2311116b3aa81b4294d5004c705634966eb6a234be79cb9a475`
- cited in: record TFQ-0360
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/primitive_axiomatics.rs`

- file: [code/rust/src/wdp/primitive_axiomatics.rs](../../../code/rust/src/wdp/primitive_axiomatics.rs)
- sha256 (`bytes`): `c1ae6edba4d807a8247b3a2726dd7d07f30d83dbb27611e036c09e5e6ef26efc`
- cited in: record TFQ-0360
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md)
- sha256 (`lf-normalised`): `1596c27b09af32aec26710dacafcbe1dcb5081bc06d35d094b4c0b0353932e64`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/01_pregenesis/tfq_0395_law_bearing_cut_not_two_marks.md`

- file: [dag/derivations/01_pregenesis/tfq_0395_law_bearing_cut_not_two_marks.md](../../../dag/derivations/01_pregenesis/tfq_0395_law_bearing_cut_not_two_marks.md)
- sha256 (`lf-normalised`): `144cf2a458eaa98b2d5277e88f08d9bd4280270bf9e48f1d681847a36b2d58f0`
- generated view: listed, not counted
- cited in: record TFQ-0395
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0360_supply_the_admitted_cut_x_e_tau_k_as_data_and_do.md`

- file: [dag/derivations/06_wdp/tfq_0360_supply_the_admitted_cut_x_e_tau_k_as_data_and_do.md](../../../dag/derivations/06_wdp/tfq_0360_supply_the_admitted_cut_x_e_tau_k_as_data_and_do.md)
- sha256 (`lf-normalised`): `efb5ec728113d8cfbc622bdb8d6e8d689285d1ae32cfe44653c47687555b8d1e`
- generated view: listed, not counted
- cited in: record TFQ-0360
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`

## Absences recorded by the TFQ records

- TFQ-0395 lean4: missing declaration obligation: endpoints-apart under a law, no cut on a subsingleton, beyond TwoPointMarks
- TFQ-0395 lean4: no local lean twin located for external:sha256:2e264c28e45671b646ce8e6ad290f689f7fb8ecf3625b109b9e97df3a74ee073
- TFQ-0395 python: missing obligation: test_zero_laws.py was listed and not opened; a law must stay an input, not a consequence of two marks
- TFQ-0395 python: no local python twin located for external:sha256:dfd5a9d9f39a47b64ef5618e637944f21532c403db19c64a7232c538f9852b9c
- TFQ-0395 rust: missing obligation: a cut struct with an explicit law field, absent from the opened genesis regime header

## Routes

Incoming (1):

- `PG-R-ROOT-TO-ADMISSION-FLOOR` `CONDITIONAL_ON_IMPORT`: [PG-ROOT-DIFF-STRUCTURE](PG-ROOT-DIFF-STRUCTURE.md) (ADMITTED_PRIMITIVE)

Outgoing (6):

- `PG-R-IRREFLEXIVE` `DERIVED_LEAN`: [PG-GEN-IRREFLEXIVE-DISTINCT](PG-GEN-IRREFLEXIVE-DISTINCT.md) (PROVED_LEAN)
- `PG-R-PROTECTED` `DERIVED_LEAN`: [PG-WDP-PROTECTED-QUESTIONS](PG-WDP-PROTECTED-QUESTIONS.md) (PROVED_LEAN)
- `PGW-R-WDP-FAILED-SAMENESS` `DERIVED_PROSE`: [PGW-WDP-FAILED-SAMENESS](PGW-WDP-FAILED-SAMENESS.md) (PROVED_PROSE)
- `PGW-R-WDP-GRAPH-COCHAIN-HOST` `DERIVED_PROSE`: [PGW-WDP-GRAPH-COCHAIN-HOST](PGW-WDP-GRAPH-COCHAIN-HOST.md) (DEFINITION)
- `PGW-R-WDP-POINTED-APARTNESS` `DERIVED_LEAN`: [PGW-WDP-POINTED-APARTNESS](PGW-WDP-POINTED-APARTNESS.md) (PROVED_LEAN)
- `UDG-R-TFQ-0396` `GAP_NO_DERIVATION`: [TFQ-0396](TFQ-0396.md) (OPEN)
