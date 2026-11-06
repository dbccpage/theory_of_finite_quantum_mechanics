# [TFQ-2608] P and NP under efficient faithful encodings

AuthorityEffect: None.

Stage: `COMPUTATION`. Status: `CONDITIONAL`. DAG node: `COMP-POLYNOMIAL-PRESENTATION-INVARIANCE`.
Parent record: `TFQ-2604`. Parent is an index link; all prerequisites below apply.

## Statement

For two encodings with polynomial-time faithful translations in both directions, polynomial length bounds and polynomial valid-encoding recognition, language membership in P and NP is preserved.

## Prerequisites and imports

- `COMP-NP-VERIFIER-EQUIVALENCE`
- Supplied: faithful translations in both directions.
- Supplied: polynomial time and size.
- Supplied: decidable validity within polynomial time.

## Argument or unresolved obligation

Translate the input and compose with the target decider. For NP translate the input and use its target verifier; the polynomial target input size gives a polynomial witness-size bound in the source input size. Apply the reverse translation for the converse. Reject invalid encodings before translation.

## Evidence

[Combined source and derivation](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md#4-p-versus-np-encodings-and-search).
This proof sketch awaits independent replay or Lean formalization. No new Lean theorem or execution receipt is claimed by this paper.
