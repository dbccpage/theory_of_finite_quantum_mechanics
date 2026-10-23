Status: AI-drafted, awaiting human review.

Node `GTH-SHADOW`, record TFQ-2400, parent record TFQ-0481 (`PGW-GO-ADMISSION-GATE`).

No construction turns PGW-GO-ADMISSION-GATE into a finite semi-simplicial set or a finite globular set. That gate keeps a two-valued admission record with a reached result: reaching leaves not-admitted, and admission is not one of the four kinds of change. A finite semi-simplicial set of dimension at most N is finite sets X_0, ..., X_N and face maps d_i from X_n to X_{n-1} such that d_i composed with d_j equals d_{j-1} composed with d_i whenever i < j. It carries no degeneracy maps. A finite globular set is finite sets with source and target maps s, t from X_{n+1} to X_n such that s composed with s equals s composed with t, and t composed with t equals t composed with s. Neither family is defined from the admission record.

The route `GTH-R-GTH-SHADOW` takes that gate as input and has status `GAP_NO_DERIVATION`. See also `PG-GEN-REGIME-EVENTS` and `PGW-ADMISSION-BEFORE-DISTINCTION`. Those nodes are not inputs of the route.

## What is proved

Nothing in Lean.

## What is assumed

The admission gate is the existing node `PGW-GO-ADMISSION-GATE`: a two-valued record kept with a reached result. The definitions of a finite semi-simplicial set and of a finite globular set are the usual finite ones, stated above, and are not claimed as constructions from that gate.

## What is open

A construction of either finite structure from the admission record. Any later use of degeneracies, which this note does not include.
