# OPS-OBSERVER-DECLARATION-REFUSAL

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> As the note states it for the Rust evaluator evaluate_l1_claim (Policy A2' and the profile binding): before any arithmetic it refuses an undeclared, empty or whitespace component with UndeclaredObserverComponent(name), and a component the evaluator does not implement with UnsupportedObserverComponent { component, declared }. The kernel must equal the label of the scenario under evaluation (for the Bell scenario "support presheaf over the maximal-context cover {0,2}|{0,3}|{1,2}|{1,3} with arities 2,2,2,2"); the other four components must equal the constants for the noncontextual polytope, the l1 norm, the terminal rule and the diagnostic layer. A supported tuple yields a receipt with authority_effect None, the terminal token and the typed profile. The refusal is a policy invariant by construction; the note does not derive it from Lemma A2.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 23
- distinct cited Lean declarations covered by a current replay receipt: 22
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The computing tests are Rust tests of the source repository. The in-repo copy of the module (code/rust/src/sheaf_theory/empirical_presheaf) uses omega_solvers, an external crate that is not a member of the code/rust workspace (cargo metadata --no-deps lists no such package), and the source test file was not imported. These tests are not run here. Outside this slice: a defect receipt, Unicode whitespace other than one space, the terminal token, the typed profile, and any kernel label other than the one Bell label. The Python gate on node OPS-THREE-ROLE-GATE checks its own observer field and is not this classifier.

## Source status

Ledger rows L035-A3 and L035-A4: computed + by construction, by the Rust tests an_undeclared_observer_component_is_refused_before_any_arithmetic, pr1080_blank_observer_fields_are_refused, pr1080_receipt_does_not_accept_an_unsupported_observer_profile and evaluation_receipts_carry_the_terminal_token_and_no_authority. Held at CONDITIONAL because those tests are not run in this repository.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ObserverDeclarationRefusal.lean`

- file: [lean4/ObserverDeclarationRefusal.lean](../../../lean4/ObserverDeclarationRefusal.lean)
- sha256 (`bytes`): `037498cc1dda660449040d7cde6747c8812be83fff91546274c8b9e850afd25e`
- cited in: node.source, receipt dag/research/campaign_ops-observer-declaration-refusal_lean_replay.json (ObserverDeclarationRefusal), receipt dag/research/pr_386_round2_replay.json (ObserverDeclarationRefusal)
- replay: `verified`
  - receipt [dag/research/campaign_ops-observer-declaration-refusal_lean_replay.json](../../../dag/research/campaign_ops-observer-declaration-refusal_lean_replay.json) (module `ObserverDeclarationRefusal`): recorded sha256 `037498cc1dda660449040d7cde6747c8812be83fff91546274c8b9e850afd25e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_386_round2_replay.json](../../../dag/research/pr_386_round2_replay.json) (module `ObserverDeclarationRefusal`): recorded sha256 `037498cc1dda660449040d7cde6747c8812be83fff91546274c8b9e850afd25e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ObserverDeclarationRefusal`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ObserverDeclarationRefusal.ObserverDraft.get` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.ObserverDraft.get` |
| `ObserverDeclarationRefusal.acceptedAdmissibility` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.acceptedAdmissibility` |
| `ObserverDeclarationRefusal.acceptedDraft` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.acceptedDraft` |
| `ObserverDeclarationRefusal.acceptedLayer` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.acceptedLayer` |
| `ObserverDeclarationRefusal.acceptedNorm` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.acceptedNorm` |
| `ObserverDeclarationRefusal.acceptedTerminal` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.acceptedTerminal` |
| `ObserverDeclarationRefusal.acceptedText` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.acceptedText` |
| `ObserverDeclarationRefusal.accepted_authority` | yes | yes | yes | propext | `#print axioms ObserverDeclarationRefusal.accepted_authority` |
| `ObserverDeclarationRefusal.accepted_draft_class` | yes | yes | yes | propext | `#print axioms ObserverDeclarationRefusal.accepted_draft_class` |
| `ObserverDeclarationRefusal.accepted_not_blank` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.accepted_not_blank` |
| `ObserverDeclarationRefusal.authorityNone` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.authorityNone` |
| `ObserverDeclarationRefusal.authorityOf` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.authorityOf` |
| `ObserverDeclarationRefusal.bellKernel` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.bellKernel` |
| `ObserverDeclarationRefusal.blankText` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.blankText` |
| `ObserverDeclarationRefusal.blank_on_accepted` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ObserverDeclarationRefusal.blank_on_accepted` |
| `ObserverDeclarationRefusal.classify` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.classify` |
| `ObserverDeclarationRefusal.mismatch_on_accepted` | yes | yes | yes | propext | `#print axioms ObserverDeclarationRefusal.mismatch_on_accepted` |
| `ObserverDeclarationRefusal.setField` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.setField` |
| `ObserverDeclarationRefusal.step` | yes | yes | yes | none | `#print axioms ObserverDeclarationRefusal.step` |
| `ObserverDeclarationRefusal.step_blank` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ObserverDeclarationRefusal.step_blank` |
| `ObserverDeclarationRefusal.step_mismatch` | yes | yes | yes | propext | `#print axioms ObserverDeclarationRefusal.step_mismatch` |
| `ObserverDeclarationRefusal.step_pass` | yes | yes | yes | propext | `#print axioms ObserverDeclarationRefusal.step_pass` |

- counts toward the grade: yes

### Rust: `code/rust/src/sheaf_theory/empirical_presheaf/observer.rs`

- file: [code/rust/src/sheaf_theory/empirical_presheaf/observer.rs](../../../code/rust/src/sheaf_theory/empirical_presheaf/observer.rs)
- sha256 (`bytes`): `ad805dc728de0f9ff8e80e8cd7b80d9b3682fc86d4d9d8220a462ca556c2c61f`
- cited in: node.rust, record TFQ-2518

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `evaluate_l1_claim` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/ops-observer-declaration-refusal.py`

- file: [checks/independent/ops-observer-declaration-refusal.py](../../../checks/independent/ops-observer-declaration-refusal.py)
- sha256 (`bytes`): `a7cc4ebafe13b323cbd39f6c029495563d700d65ed635cded5b75717661419af`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2518_ops_observer_declaration_refusal.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2518_ops_observer_declaration_refusal.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2518_ops_observer_declaration_refusal.md)
- sha256 (`lf-normalised`): `8a94ee804e3e721e7402ce17389240fffef1e7face420c9d9dc97c080fcba0a4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2518
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ops-observer-declaration-refusal.md`

- file: [dag/derivations/independent/ops-observer-declaration-refusal.md](../../../dag/derivations/independent/ops-observer-declaration-refusal.md)
- sha256 (`lf-normalised`): `8f3db4fa1706d7a270bed718dadf3cc08f4c9fd17d67a397a88a960a00e3363d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ops-observer-declaration-refusal_lean_replay.json`

- file: [dag/research/campaign_ops-observer-declaration-refusal_lean_replay.json](../../../dag/research/campaign_ops-observer-declaration-refusal_lean_replay.json)
- sha256 (`lf-normalised`): `6ed3b6fd271cb0582b164ef3463be2723b7d0ae5b37a3bf687de924ee3aeeb0b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `ae5564735bb6591e0f149868f83bd9f9793f297be0f8af3cc889c293ae4059cb`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-OBSERVER-DECLARATION-REFUSAL` `RECORD_PARENT`: [OPS-OBSERVER-TUPLE](OPS-OBSERVER-TUPLE.md) (DEFINITION)

Outgoing (1):

- `OPS-R-REFUTED-EARLIER-RUST` `RECORD_PARENT`: [OPS-REFUTED-EARLIER-RUST](OPS-REFUTED-EARLIER-RUST.md) (REFUTED)
