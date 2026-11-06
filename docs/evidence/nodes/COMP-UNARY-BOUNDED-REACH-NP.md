# COMP-UNARY-BOUNDED-REACH-NP

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `CONDITIONAL`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a fixed finite rewriting rule list, the language of triples (a,b,1^t) for which a reaches b in at most t steps belongs to NP.

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

- fixed finite alphabet and rule list
- unary step bound
- explicit intermediate words

## Bottleneck

With c the largest right-hand-side length, each intermediate word has length at most |a|+tc. List at most t words, rule indices and positions. Verify each local substitution and the endpoints by polynomially many symbol comparisons. Binary t invalidates this certificate-size bound, not membership in NP by itself. Independent proof review or Lean formalization is still required.

## Source status

Editorial proof sketch awaiting independent replay; no new Lean build.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md`

- file: [atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md)
- sha256 (`lf-normalised`): `b6f7b89589ac601c37dda7e659a4b484f37b68b57d1c1227ed3581ebff25137b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_2605_comp_unary_bounded_reach_np.md`

- file: [dag/derivations/29_computation/tfq_2605_comp_unary_bounded_reach_np.md](../../../dag/derivations/29_computation/tfq_2605_comp_unary_bounded_reach_np.md)
- sha256 (`lf-normalised`): `18f0b0c692ebef6f6fa4f339580865ad1f61ac8e77b92caaa0c9ba8e4e47a92b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2605
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-COMP-UNARY-BOUNDED-REACH-NP` `DERIVED_PROSE`: [COMP-C2-WORD-REWRITING](COMP-C2-WORD-REWRITING.md) (DEFINITION), [COMP-NP-VERIFIER-EQUIVALENCE](COMP-NP-VERIFIER-EQUIVALENCE.md) (CONDITIONAL)

Outgoing (0):

