# GTH-LANG-IMPORT

Stage: [GENESIS_TO_HIGHER](../stages/GENESIS_TO_HIGHER.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> An import record for the priced admission language names a theory, the axioms added, the cost as the sentences the core does not derive, and a conservativity status that is either established or still open. Writing that record does not derive the added axioms from the core. No format for the record is defined. The language is not shown to state, of itself, a sentence it does not derive.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

An import record names axioms, cost and a conservativity status (established or open). The record is not a derivation of those axioms. No record format is defined.

## Source status

Open. An import record is specified as a name, a cost and a conservativity status. Writing it down is not a derivation.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/34_genesis_to_higher/tfq_2410_gth_lang_import.md`

- file: [dag/derivations/34_genesis_to_higher/tfq_2410_gth_lang_import.md](../../../dag/derivations/34_genesis_to_higher/tfq_2410_gth_lang_import.md)
- sha256 (`lf-normalised`): `35fb9c2ad44336a23623bbd5e927c4146f68d9edc424a376a073cb25d221b63c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2410
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/gth_lang_import.md`

- file: [dag/derivations/independent/gth_lang_import.md](../../../dag/derivations/independent/gth_lang_import.md)
- sha256 (`lf-normalised`): `9178701e8ab04c496024e67056d43da8e121bd95b8d5b220f5bd55fa0baca0ad`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `GTH-R-GTH-LANG-IMPORT` `GAP_NO_DERIVATION`: [GTH-LANG-INTERPRET](GTH-LANG-INTERPRET.md) (OPEN)

Outgoing (1):

- `GTH-R-GTH-LANG-LIMITS` `RECORD_PARENT`: [GTH-LANG-LIMITS](GTH-LANG-LIMITS.md) (PROVED_PROSE)
