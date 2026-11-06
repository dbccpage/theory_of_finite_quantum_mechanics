# COMP-P-VS-NP-OPEN

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Determine whether every language in NP is in P, or exhibit an NP language outside P. The existing machine construction, finite checks and exponential search enumeration do not settle either alternative.

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

A proof must quantify over uniform algorithms and unbounded input lengths. An upper bound for enumeration is not a lower bound for all algorithms. The official Clay statement lists the problem as unsolved.

## Source status

Editorial reconstruction with explicit premises; no new Lean build.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md`

- file: [atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md)
- sha256 (`lf-normalised`): `b3aff2eb94aa10a76984e739451717a682e120ab83741ab0f902ca75069cae47`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_2607_comp_p_vs_np_open.md`

- file: [dag/derivations/29_computation/tfq_2607_comp_p_vs_np_open.md](../../../dag/derivations/29_computation/tfq_2607_comp_p_vs_np_open.md)
- sha256 (`lf-normalised`): `50779d268c276d4735e1b3fa4ca123246b8dc9970c0a97b7ac59d43fcb044fae`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2607
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-COMP-P-VS-NP-OPEN` `GAP_NO_DERIVATION`: [COMP-P-DEFINITION](COMP-P-DEFINITION.md) (DEFINITION), [COMP-NP-VERIFIER-EQUIVALENCE](COMP-NP-VERIFIER-EQUIVALENCE.md) (CONDITIONAL), [COMP-COOK-LEVIN-IMPORT](COMP-COOK-LEVIN-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

