# [TFQ-2602] Encoding, input length and uniform step cost

AuthorityEffect: None.

Stage: `COMPUTATION`. Status: `IMPORTED_ASSUMPTION`. DAG node: `COMP-COST-MODEL-IMPORT`.
Parent record: `TFQ-2601`. Parent is an index link; all prerequisites below apply.

## Statement

Complexity is measured after fixing finite input encodings, input length, a uniform machine model and elementary step costs. Computable simulation alone gives no polynomial overhead bound.

## Prerequisites and imports

- `COMP-UTM-CONDITIONAL-ROUTE`
- Supplied: finite encoding.
- Supplied: input length.
- Supplied: uniform machine model.
- Supplied: elementary cost.

## Argument or unresolved obligation

Prove overhead bounds for each implementation translation used in a complexity claim. Keep computability and efficient simulation distinct.

## Evidence

[Combined source and derivation](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md#2-the-extra-step-from-computability-to-complexity).
No new Lean theorem or execution receipt is claimed by this paper.
