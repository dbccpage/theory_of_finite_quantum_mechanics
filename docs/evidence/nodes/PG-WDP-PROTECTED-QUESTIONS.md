# PG-WDP-PROTECTED-QUESTIONS

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On an unstructured set with at least two elements no point is fixed by every permutation (the bare-set form of: no Sym(X)-equivariant distinguished-point selection exists). In the pointwise-stabiliser model, in which a declared input set is fixed pointwise, the inclusion-minimal declarations that make some point invariant are exactly the singletons (price one declared point; price zero on a one-point carrier; no selection on the empty carrier). The ledger definition D01 of the asymmetry-price frontier relative to an implementation class and dependency preorder is not formalised. The result says selection is not free on a bare set; it does not say retention or observers cannot exist.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- distinct cited Lean declarations covered by a current replay receipt: 13
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

WDP-CH03-P03 (no response of at most one item separates a from b in the declare-then-assert grammar) has no Lean port; the asymmetry-price frontier is proved only in the pointwise-stabiliser modelling choice, not for D01 with an implementation class and dependency preorder.

## Source status

WDP-CH03-P01 FINITE_PROVED; WDP-CH03-D01 definition; WDP-CH03-N01 nonclaim

## Review

- PFP review: [dag/results/PG-WDP-PROTECTED-QUESTIONS/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-WDP-PROTECTED-QUESTIONS/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: On a bare set of at least two points no point is invariant under all permutations, and in the pointwise-stabiliser model the minimal selecting declarations are exactly the single declared points (price one declared point; price zero on a one-point carrier; no selection on the empty carrier); symmetry-price bookkeeping only.
  - does not support: Retention, dynamics or observers being not possible or available (WDP-CH03-N01 is a nonclaim, not formalised); that Selecting / MinimalSelecting formalises WDP-CH03-D01 (D01 minimises declared input sets whose removal restores a symmetry that moves the output, relative to an implementation class and dependency preorder; here the minimal declarations making some point invariant under the pointwise stabiliser are computed, and the two agree on singletons only because the output is the declared point); a Lean notion of equivariant selection function (no_fully_invariant_point is its bare-set specialisation); the price of selection on structured carriers (rigid, cyclic, graph) or under the setwise stabiliser; WDP-CH03-P03; infinite-carrier cardinality; any physical or interpretive claim.
  - next test: On structured carriers compute the same selecting and minimal tables with Sym(X) replaced by an explicit automorphism group G (n-cycle with rotations, K4 graph with its automorphisms, a rigid carrier with trivial G) and test whether the frontier is still the singletons: a rigid carrier must give price 0 and the n-cycle with rotations price 1; any other value falsifies the claim that the singleton frontier is generic.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` |

- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Symmetry.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Symmetry.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Symmetry.lean)
- sha256 (`bytes`): `3ce0aff3e18ce1934e1aba37e3a0f0e1687c8c9cff2bac911e0727c112e912b9`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Symmetry`): recorded sha256 `3ce0aff3e18ce1934e1aba37e3a0f0e1687c8c9cff2bac911e0727c112e912b9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Symmetry.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `no_fully_invariant_point` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms no_fully_invariant_point` |

- counts toward the grade: yes

### Lean: `lean4/WdpProtectedQuestions.lean`

- file: [lean4/WdpProtectedQuestions.lean](../../../lean4/WdpProtectedQuestions.lean)
- sha256 (`bytes`): `a7d5d6803298dea34d336f5502e0ce9826646983a4d8a0731f54cfdbe2296937`
- cited in: node.lean, receipt dag/research/pfp_batch01_lean_replay.json (WdpProtectedQuestions)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `WdpProtectedQuestions`): recorded sha256 `a7d5d6803298dea34d336f5502e0ce9826646983a4d8a0731f54cfdbe2296937` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build WdpProtectedQuestions`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WdpProtectedQuestions.bool_instance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpProtectedQuestions.bool_instance` |
| `WdpProtectedQuestions.empty_carrier_no_selection` | yes | yes | yes | Quot.sound | `#print axioms WdpProtectedQuestions.empty_carrier_no_selection` |
| `WdpProtectedQuestions.frontierEquiv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpProtectedQuestions.frontierEquiv` |
| `WdpProtectedQuestions.frontier_card` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpProtectedQuestions.frontier_card` |
| `WdpProtectedQuestions.invariantUnder_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpProtectedQuestions.invariantUnder_iff` |
| `WdpProtectedQuestions.minimalSelecting_iff_singleton` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpProtectedQuestions.minimalSelecting_iff_singleton` |
| `WdpProtectedQuestions.no_fully_invariant_point` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpProtectedQuestions.no_fully_invariant_point` |
| `WdpProtectedQuestions.no_fully_invariant_point_card` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpProtectedQuestions.no_fully_invariant_point_card` |
| `WdpProtectedQuestions.one_point_empty_selects` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpProtectedQuestions.one_point_empty_selects` |
| `WdpProtectedQuestions.selecting_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpProtectedQuestions.selecting_iff` |
| `WdpProtectedQuestions.selecting_iff_nonempty` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpProtectedQuestions.selecting_iff_nonempty` |

- counts toward the grade: yes

### Rust: `code/rust/src/operad_theory/kernel/observer.rs`

- file: [code/rust/src/operad_theory/kernel/observer.rs](../../../code/rust/src/operad_theory/kernel/observer.rs)
- sha256 (`bytes`): `4b4066b2a8e0bfe304745204064a0fbeb159d3974b998191e192e0a1fd57fb0a`
- cited in: record TFQ-0340
- note: no test is cited for this symbol; its crate is tfqm_operad_theory
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/primitive_axiomatics.rs`

- file: [code/rust/src/wdp/primitive_axiomatics.rs](../../../code/rust/src/wdp/primitive_axiomatics.rs)
- sha256 (`bytes`): `ec684060aeb104e94b73d1e3f72802ada1fa8bb5755232199380e454e66fd45d`
- cited in: record TFQ-0339
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md)
- sha256 (`lf-normalised`): `1596c27b09af32aec26710dacafcbe1dcb5081bc06d35d094b4c0b0353932e64`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0339_preserve_a_protected_answer_exactly_on_report_fibers_and_do_not_derive.md`

- file: [dag/derivations/06_wdp/tfq_0339_preserve_a_protected_answer_exactly_on_report_fibers_and_do_not_derive.md](../../../dag/derivations/06_wdp/tfq_0339_preserve_a_protected_answer_exactly_on_report_fibers_and_do_not_derive.md)
- sha256 (`lf-normalised`): `e8e6ce9ac3dbd85b140abd82a6e1cbb5570a2328bc4388abd1a245ae5ecce16e`
- generated view: listed, not counted
- cited in: record TFQ-0339
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0340_refuse_a_symmetry_equivariant_distinguished_point_on_a_finite_set_of_size_at.md`

- file: [dag/derivations/06_wdp/tfq_0340_refuse_a_symmetry_equivariant_distinguished_point_on_a_finite_set_of_size_at.md](../../../dag/derivations/06_wdp/tfq_0340_refuse_a_symmetry_equivariant_distinguished_point_on_a_finite_set_of_size_at.md)
- sha256 (`lf-normalised`): `3b1ec15c906a82c529f424343cd4578a694878720e499274d6abe4c1911240fe`
- generated view: listed, not counted
- cited in: record TFQ-0340
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`

## Routes

Incoming (1):

- `PG-R-PROTECTED` `DERIVED_LEAN`: [PG-ADMISSION-FLOOR](PG-ADMISSION-FLOOR.md) (PROVED_LEAN), [PG-HISTORY-REPORT-CRITERION](PG-HISTORY-REPORT-CRITERION.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-WDP-ASYMMETRY-INJECTION-LEDGER` `DERIVED_PROSE`: [PGW-WDP-ASYMMETRY-INJECTION-LEDGER](PGW-WDP-ASYMMETRY-INJECTION-LEDGER.md) (DEFINITION)
- `PGW-R-WDP-OBSERVER-QUOTIENT-PASSIVITY` `DERIVED_PROSE`: [PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY](PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY.md) (DEFINITION)
