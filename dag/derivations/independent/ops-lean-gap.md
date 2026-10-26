Status: AI-drafted, awaiting human review.

# OPS-LEAN-GAP

Node status stays OPEN. The standing text is one box of four Boolean parity constraints. Equivalences for the noncontextual fraction, Vorob'ev's theorem, and a link to a Rust scenario stay outside this note.

## The four constraints

Take Boolean values a, a', b and b'. Ask whether all four of these can hold together:

- a xor b = false
- a xor b' = false
- a' xor b = false
- a' xor b' = true

## The two exclusive-or totals

Each variable occurs in exactly two of the left-hand sides, so the exclusive-or of the four left-hand sides is false for every assignment. The exclusive-or of the four right-hand sides is false xor false xor false xor true, which is true. A common solution would force those two totals to agree, and they do not.

## The census

There are 2 * 2 * 2 * 2 = 16 assignments. None of them meets all four constraints.

## What is proved

The exclusive-or identity for the four left-hand sides, the exclusive-or of the four right-hand sides, the refusal of every assignment, and the count 16.

## What is assumed

The exclusive-or of two Boolean values, and nothing else. AuthorityEffect is None.

## What is open

Equivalences among global sections, the convex hull of the assignment matrix and the noncontextual fraction; strong contextuality and a zero noncontextual fraction; Vorob'ev sufficiency and its converse; the coboundary criterion for no-signalling; rational normalisation of weights; and any link from natural-number-weighted lists to a Rust scenario type.
