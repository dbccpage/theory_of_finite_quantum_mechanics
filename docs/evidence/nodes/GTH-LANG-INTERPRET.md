# GTH-LANG-INTERPRET

Stage: [GENESIS_TO_HIGHER](../stages/GENESIS_TO_HIGHER.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The following three items are targets, not theorems. (a) A stated fragment of Martin-Lof type theory with identity types. (b) Finite semi-simplicial or globular structure, once a shadow exists, together with whatever horn fillers are recorded. (c) Hereditarily finite sets. No interpretation function into any of these targets is defined. Faithfulness, soundness and conservativity of any such function are open.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Martin-Lof type theory with identity types, finite simplicial or globular structure, and hereditarily finite sets are named as targets. They are not theorems of this stage.

## Source status

Open. Martin-Lof type theory with identity types, finite simplicial or globular structure, and hereditarily finite sets are targets, not theorems.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/34_genesis_to_higher/tfq_2409_gth_lang_interpret.md`

- file: [dag/derivations/34_genesis_to_higher/tfq_2409_gth_lang_interpret.md](../../../dag/derivations/34_genesis_to_higher/tfq_2409_gth_lang_interpret.md)
- sha256 (`lf-normalised`): `fcc40d284aede0df2cb837cc868bb91a099f856740af31923a73b4ac6599a0a7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2409
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/gth_lang_interpret.md`

- file: [dag/derivations/independent/gth_lang_interpret.md](../../../dag/derivations/independent/gth_lang_interpret.md)
- sha256 (`lf-normalised`): `a0dc150ed6034f89b41a46d0513d0576064b3133ae7607b28a26825980d7c3cd`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:book:The-Univalent-Foundations-Program-2013-Homotopy-Type-Theory`

## Routes

Incoming (1):

- `GTH-R-GTH-LANG-INTERPRET` `GAP_NO_DERIVATION`: [GTH-LANG-REFLECT](GTH-LANG-REFLECT.md) (OPEN)

Outgoing (1):

- `GTH-R-GTH-LANG-IMPORT` `GAP_NO_DERIVATION`: [GTH-LANG-IMPORT](GTH-LANG-IMPORT.md) (OPEN)
