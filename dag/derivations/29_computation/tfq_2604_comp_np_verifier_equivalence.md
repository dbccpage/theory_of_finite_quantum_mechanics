# [TFQ-2604] NP from polynomial witnesses and nondeterministic runs

AuthorityEffect: None.

Stage: `COMPUTATION`. Status: `CONDITIONAL`. DAG node: `COMP-NP-VERIFIER-EQUIVALENCE`.
Parent record: `TFQ-2603`. Parent is an index link; all prerequisites below apply.

## Statement

Under a fixed finite-branching machine model, polynomial-time nondeterministic acceptance is equivalent to existence of polynomial-length witnesses checked by a deterministic polynomial-time verifier; P is contained in NP.

## Prerequisites and imports

- `COMP-P-DEFINITION`
- `COMP-COST-MODEL-IMPORT`
- Supplied: finite branching.
- Supplied: uniform polynomial bounds.
- Supplied: finite input and witness encodings.

## Argument or unresolved obligation

A nondeterministic machine guesses the bounded witness and runs the verifier. Conversely encode the branch choices of an accepting polynomial-time run and replay them deterministically. There are polynomially many choices of constant bit length. For P containment ignore the witness and run the decider. No separation follows.

## Evidence

[Combined source and derivation](../../../atlas/computation_complexity_pvnp/from_first_mark_to_quantum_computing.md#2-the-extra-step-from-computability-to-complexity).
This proof sketch awaits independent replay or Lean formalization. No new Lean theorem or execution receipt is claimed by this paper.
