# COMP-C8-MINIMALITY-FENCE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Two separated marks code the words of any finite alphabet and a blank is a third symbol, but the composite machine M0 is not minimal and no smallest general-purpose machine is claimed; small-machine records are literature only.

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

State and prove in Lean the simulation of a machine over the coded alphabet by a machine over the two marks and a blank before any minimality statement.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C8b claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/29_computation/tfq_1313_comp_c8_minimality_fence.md`

- file: [dag/derivations/29_computation/tfq_1313_comp_c8_minimality_fence.md](../../../dag/derivations/29_computation/tfq_1313_comp_c8_minimality_fence.md)
- sha256 (`lf-normalised`): `edba962298bb562d50a8cd46a844ad8666afb1a081a160e280d29abcd8bede3a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1313
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C8-MINIMALITY-FENCE` `GAP_NO_DERIVATION`: [COMP-C8-BINARY-CODING](COMP-C8-BINARY-CODING.md) (PROVED_LEAN), [COMP-C6-FINITE-MARKS](COMP-C6-FINITE-MARKS.md) (PROVED_LEAN)

Outgoing (0):

