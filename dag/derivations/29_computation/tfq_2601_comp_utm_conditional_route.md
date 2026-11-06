# [TFQ-2601] Conditional UTM route through the existing machine construction

AuthorityEffect: None.

Stage: `COMPUTATION`. Status: `CONDITIONAL`. DAG node: `COMP-UTM-CONDITIONAL-ROUTE`.
Parent record: `TFQ-1284`. Parent is an index link; all prerequisites below apply.

## Statement

With separated marks, declared rewriting and unbounded word supply, the existing fixed TM0 machine simulates termination of every encoded partial-recursive program. Its finite mark set is established; output decoding remains a separate open obligation.

## Prerequisites and imports

- `COMP-C1-CANONICAL-SEPARATED-ALPHABET`
- `COMP-C5-TM0-STEP-SIMULATION`
- `COMP-C6-TM0-HALTING-EQUIVALENCE`
- `COMP-C6-FINITE-MARKS`
- `COMP-C4-UNBOUNDED-SUPPLY-IMPORT`
- `COMP-MARK-ADMISSION-GAP`
- Supplied: admitted separated alphabet.
- Supplied: declared rules.
- Supplied: unbounded word supply.
- Supplied: Mathlib evaluator and compilers.

## Argument or unresolved obligation

Compose the existing forward/backward rewriting simulation with the fixed evaluator compiler chain. This reuses the existing results without a new Lean claim. COMP-C6-TM0-OUTPUT-FORM-OPEN remains open; a halting iff theorem alone is not an output-value theorem.

## Evidence

[Combined source and derivation](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md#1-inscription-admission-and-a-machine-that-interprets-programs).
No new Lean theorem or execution receipt is claimed by this paper.
