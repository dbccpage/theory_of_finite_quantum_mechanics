# OPS-OBSERVER-DECLARATION-REFUSAL

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `CONDITIONAL`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> As the note states it for the Rust evaluator evaluate_l1_claim (Policy A2' and the profile binding): before any arithmetic it refuses an undeclared, empty or whitespace component with UndeclaredObserverComponent(name), and a component the evaluator does not implement with UnsupportedObserverComponent { component, declared }. The kernel must equal the label of the scenario under evaluation (for the Bell scenario "support presheaf over the maximal-context cover {0,2}|{0,3}|{1,2}|{1,3} with arities 2,2,2,2"); the other four components must equal the constants for the noncontextual polytope, the l1 norm, the terminal rule and the diagnostic layer. A supported tuple yields a receipt with authority_effect None, the terminal token and the typed profile. The refusal is a policy invariant by construction; the note does not derive it from Lemma A2.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The computing tests are Rust tests of the source repository. The in-repo copy of the module (code/rust/src/sheaf_theory/empirical_presheaf) uses omega_solvers, an external crate that is not a member of the code/rust workspace (cargo metadata --no-deps lists no such package), and the source test file was not imported. These tests are not run here. The Python gate runs the same five-component refusal on its own observer field (node OPS-THREE-ROLE-GATE).

## Source status

Ledger rows L035-A3 and L035-A4: computed + by construction, by the Rust tests an_undeclared_observer_component_is_refused_before_any_arithmetic, pr1080_blank_observer_fields_are_refused, pr1080_receipt_does_not_accept_an_unsupported_observer_profile and evaluation_receipts_carry_the_terminal_token_and_no_authority. Held at CONDITIONAL because those tests are not run in this repository.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/sheaf_theory/empirical_presheaf/observer.rs`

- file: [code/rust/src/sheaf_theory/empirical_presheaf/observer.rs](../../../code/rust/src/sheaf_theory/empirical_presheaf/observer.rs)
- sha256 (`bytes`): `ad805dc728de0f9ff8e80e8cd7b80d9b3682fc86d4d9d8220a462ca556c2c61f`
- cited in: node.rust, record TFQ-2518

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `evaluate_l1_claim` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2518_ops_observer_declaration_refusal.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2518_ops_observer_declaration_refusal.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2518_ops_observer_declaration_refusal.md)
- sha256 (`lf-normalised`): `1ac5b3d53ec9c90ed4313b7b21eeae68dce708fb942cb979970e1eba0b3c63e8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2518
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `649532625cf9e8ec085a420fd1bad9227fcc4dae9f06ba02be1eb19f497e3ec7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-OBSERVER-DECLARATION-REFUSAL` `RECORD_PARENT`: [OPS-OBSERVER-TUPLE](OPS-OBSERVER-TUPLE.md) (DEFINITION)

Outgoing (1):

- `OPS-R-REFUTED-EARLIER-RUST` `RECORD_PARENT`: [OPS-REFUTED-EARLIER-RUST](OPS-REFUTED-EARLIER-RUST.md) (REFUTED)
