# [TFQ-2605] Unary step-bounded rewriting is in NP

AuthorityEffect: None.

Stage: `COMPUTATION`. Status: `CONDITIONAL`. DAG node: `COMP-UNARY-BOUNDED-REACH-NP`.
Parent record: `TFQ-1286`. Parent is an index link; all prerequisites below apply.

## Statement

For a fixed finite rewriting rule list, the language of triples (a,b,1^t) for which a reaches b in at most t steps belongs to NP.

## Prerequisites and imports

- `COMP-C2-WORD-REWRITING`
- `COMP-NP-VERIFIER-EQUIVALENCE`
- Supplied: fixed finite alphabet and rule list.
- Supplied: unary step bound.
- Supplied: explicit intermediate words.

## Argument or unresolved obligation

With c the largest right-hand-side length, each intermediate word has length at most |a|+tc. List at most t words, rule indices and positions. Verify each local substitution and the endpoints by polynomially many symbol comparisons. Binary t invalidates this certificate-size bound, not membership in NP by itself.

## Evidence

[Combined source and derivation](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md#3-where-np-appears-in-the-admitted-rewriting-model).
This proof sketch awaits independent replay or Lean formalization. No new Lean theorem or execution receipt is claimed by this paper.
