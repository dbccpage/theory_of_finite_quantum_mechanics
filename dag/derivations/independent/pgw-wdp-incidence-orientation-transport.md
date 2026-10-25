Status: AI-drafted, awaiting human review.

# PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT

Node status stays OPEN. This note records one triangle. It does not transport every window quantity.

## Orders

The incidence boundary uses edges in the order 01, 02, 12. Its columns are (-1, 1, 0), (-1, 0, 1) and (0, -1, 1). The face column is (1, -1, 1), and the incidence boundary of that column is (0, 0, 0).

Reordering (a, b, c) to (a, c, b) sends the face column to (1, 1, -1) on the order 01, 12, 02.

## Transpose and evaluation

The dot products of a vertex triple with those columns, read in the order 01, 12, 02, are (f1 - f0, f2 - f1, f2 - f0). That is the WDP coboundary. The evaluation x01 + x12 - x02 vanishes on every such coboundary. Storing the reversed edge 20 as the negation of edge 02 makes the cyclic sum equal that evaluation.

## One filled triangle

On the cochain (1, 1, 0) the evaluation is 2. The unit-weight residual against the coboundary is 2 at the vertex values (0, 1, 0), and it is at least 2 for every integer vertex triple, because the pairing with (1, 1, -1) is identically 2.

## What is proved

The three columns, the reorder of the face, the zero incidence boundary of that face, the transpose identity, the vanishing of the evaluation on coboundaries, the sign flip for edge 20, the charge 2, and the residual lower bound 2 attained at (0, 1, 0).

## What is assumed

The two edge orders, the incidence boundary, and the evaluation x01 + x12 - x02 are the definitions above. No monograph identity is imported. AuthorityEffect is None.

## What is open

A transport for every window quantity, a derivation of the WDP window from Genesis admission, and the external orientation test stay open.
