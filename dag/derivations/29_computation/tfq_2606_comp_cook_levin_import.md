# [TFQ-2606] Cook-Levin and the reduction obligation

AuthorityEffect: None.

Stage: `COMPUTATION`. Status: `IMPORTED_ASSUMPTION`. DAG node: `COMP-COOK-LEVIN-IMPORT`.
Parent record: `TFQ-2604`. Parent is an index link; all prerequisites below apply.

## Statement

The Cook-Levin theorem supplies a polynomial reduction from nondeterministic polynomial-time acceptance to SAT. Applying NP-hardness to a specific rewriting or sign problem needs a further polynomial reduction.

## Prerequisites and imports

- `COMP-NP-VERIFIER-EQUIVALENCE`
- Supplied: Cook-Levin theorem.
- Supplied: valid tableau encoding.
- Supplied: polynomial reduction cost.

## Argument or unresolved obligation

The tableau constrains initial configuration, local transitions and acceptance with polynomially many Boolean variables and clauses. This is an imported theorem, not a newly checked Lean result.

## Evidence

[Combined source and derivation](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md#3-where-np-appears-in-the-admitted-rewriting-model).
No new Lean theorem or execution receipt is claimed by this paper.
