Status: AI-drafted, awaiting human review.

# OPS-LEAN-GAP

The original list of OPS Lean obligations remains OPEN. This separate four-variable parity box does not replace those targets or establish the noncontextual-fraction equivalences, Vorob'ev theorem or a Rust-scenario refinement.

## The four constraints

Take Boolean values a, a', b and b'. Ask whether all four of these can hold together:

- a xor b = false
- a xor b' = false
- a' xor b = false
- a' xor b' = true

## The two exclusive-or totals

Each variable occurs in exactly two of the left-hand sides, so the exclusive-or of the four left-hand sides is false for every assignment. The exclusive-or of the four right-hand sides is false xor false xor false xor true, which is true. A common solution would force those two totals to agree, and they do not.

## The census

The independent checker enumerates all four-variable Boolean assignments and counts 16. The Lean declaration `sixteen` proves the arithmetic identity 2 * 2 * 2 * 2 = 16; it does not state a type-cardinality theorem. `noAssignment` quantifies over all four Boolean variables and rules out the four constraints simultaneously.

## Independent review controls

Integer sums modulo two provide a separate route to each Boolean exclusive-or. The checker computes its assignment count and solution count. As negative controls, each three-constraint subsystem has two solutions, and changing the odd right-hand side to false gives two common solutions. These show that the obstruction depends on the full stated box, rather than an empty or broken search. The printed results are taken from the enumeration and both normal and optimized Python runs use explicit failure checks.

## What is proved

The exclusive-or identity for the four left-hand sides, the exclusive-or of the four right-hand sides, the refusal of every assignment, and the arithmetic product 2 * 2 * 2 * 2 = 16. The independent enumeration supplies the assignment count.

## What is assumed

The exclusive-or of two Boolean values, and nothing else. AuthorityEffect is None.

## What is open

Equivalences among global sections, the convex hull of the assignment matrix and the noncontextual fraction; strong contextuality and a zero noncontextual fraction; Vorob'ev sufficiency and its converse; the coboundary criterion for no-signalling; rational normalisation of weights; and any link from natural-number-weighted lists to a Rust scenario type.
