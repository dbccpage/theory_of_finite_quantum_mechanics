# GTH-LANG-CORE

Stage: [GENESIS_TO_HIGHER](../stages/GENESIS_TO_HIGHER.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The priced admission language is not defined. The reading intended for its primitives, which this node does not derive, is: a two-valued admission record kept with a reached result (PGW-GO-ADMISSION-GATE); a regime as a tuple of admitted data, forms, instances, rules and requirements, with state change only through an admission event or impose, and with supply external (PG-GEN-REGIME-EVENTS); and the two boxed laws that S(n+1) may contain only structure forced by an unresolved obstruction at S(n), and that a realization has no authority to extend S(n) (PGW-SN-TWO-BOXED-LAWS). No syntax, no typing judgement and no deep embedding is given. Alphabet declarations of the MSS-N grammar are not a primitive derived from those three nodes.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No syntax, typing judgement or deep embedding. MSS-N alphabet declarations are not a derived primitive. The infinite imports are not inputs of the route into this node.

## Source status

Open. The priced admission language has no syntax. The three route inputs are the intended reading, not a derivation.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/34_genesis_to_higher/tfq_2407_gth_lang_core.md`

- file: [dag/derivations/34_genesis_to_higher/tfq_2407_gth_lang_core.md](../../../dag/derivations/34_genesis_to_higher/tfq_2407_gth_lang_core.md)
- sha256 (`lf-normalised`): `1302ceb769cca552189a880855033826ec0174b9894291363aef659cf663737a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2407
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/gth_lang_core.md`

- file: [dag/derivations/independent/gth_lang_core.md](../../../dag/derivations/independent/gth_lang_core.md)
- sha256 (`lf-normalised`): `c7578e78a3d38c732aad62b2457cbebdcd71eda74155be178247f0e0df5b0e07`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `GTH-R-GTH-LANG-CORE` `GAP_NO_DERIVATION`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION), [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION), [PGW-SN-TWO-BOXED-LAWS](PGW-SN-TWO-BOXED-LAWS.md) (DEFINITION)

Outgoing (1):

- `GTH-R-GTH-LANG-REFLECT` `GAP_NO_DERIVATION`: [GTH-LANG-REFLECT](GTH-LANG-REFLECT.md) (OPEN)
