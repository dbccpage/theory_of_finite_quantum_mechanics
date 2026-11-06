# [TFQ-2603] Deterministic polynomial time

AuthorityEffect: None.

Stage: `COMPUTATION`. Status: `DEFINITION`. DAG node: `COMP-P-DEFINITION`.
Parent record: `TFQ-2602`. Parent is an index link; all prerequisites below apply.

## Statement

P is the class of languages decided by one deterministic machine in time bounded by a polynomial in encoded input length.

## Prerequisites and imports

- `COMP-COST-MODEL-IMPORT`
- Supplied: cost model.
- Supplied: uniform polynomial bound.

## Argument or unresolved obligation

This defines a class of language families over inputs of unbounded length. A finite truth table does not establish membership for an unbounded family.

## Evidence

[Combined source and derivation](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md#2-the-extra-step-from-computability-to-complexity).
No new Lean theorem or execution receipt is claimed by this paper.
