# [TFQ-2615] Gate errors telescope across a finite circuit

AuthorityEffect: None.

Stage: `COMPUTATION`. Status: `CONDITIONAL`. DAG node: `QC-GATE-ERROR-BUDGET`.
Parent record: `TFQ-2614`. Parent is an index link; all prerequisites below apply.

## Statement

For two L-gate unitary circuits whose corresponding gates differ in operator norm by at most epsilon/L, with L positive, their products differ by at most epsilon.

## Prerequisites and imports

- `QC-UNIFORM-CIRCUITS-BQP`
- Supplied: unitary gates.
- Supplied: operator norm.
- Supplied: positive gate count.
- Supplied: nonnegative error budget.

## Argument or unresolved obligation

Subtract the two products by replacing one factor at a time. Each term is a gate difference multiplied on either side by unitaries, so its norm is at most epsilon/L. Triangle inequality sums L terms. Efficient synthesis to this precision requires a separate theorem for the chosen gate set.

## Evidence

[Combined source and derivation](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md#6-quantum-circuits-and-bqp).
This proof sketch awaits independent replay or Lean formalization. No new Lean theorem or execution receipt is claimed by this paper.
