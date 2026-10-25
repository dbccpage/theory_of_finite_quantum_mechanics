Status: AI-drafted, awaiting human review.

# PGW-WDP-HANDOFF-TO-L1

Node status stays OPEN. This note records one triangle.

## Carrier

The carrier is one triangle. The edges are 01, 12, and 02. Every weight is the integer 1. Vertex values are three integers (f0, f1, f2). Their coboundary is

d0(f0, f1, f2) = (f1 - f0, f2 - f1, f2 - f0).

An edge triple (x01, x12, x02) has face value x01 + x12 - x02. Its unit l1 length is |x01| + |x12| + |x02|. The residual against a vertex repair is the edge triple minus that coboundary.

## Distance

For every integer edge triple and every integer vertex repair, the unit l1 length of the residual is at least the absolute face value. The face of every coboundary is 0, so the face is unchanged when a coboundary is subtracted, and the triangle inequality for the absolute value gives the bound.

When the face value is negative, the vertex repair (0, h01, h01 + h12) leaves the residual (0, 0, -face). Otherwise the vertex repair (0, h01 - face, h02) leaves the residual (face, 0, 0). In both cases the residual has unit l1 length equal to the absolute face value. On this triangle, that length is the distance from the edge triple to the integer coboundaries.

If the face value is 0, the edge triple equals the coboundary of the second repair.

## Separation

The vertex values (0, 1, 0) have coboundary (1, -1, 0) and coboundary length 2. The residual of the edge triple (1, -1, 0) against itself has length 0. Those two lengths differ, so the coboundary length is not the quotient value of that edge triple.

The edge triple (1, 0, 0) has face value 1.

## Verdict and fibre

The verdict of the pair (1, 1) is 0. The verdict of the pair (0, 0) is 1. Equal fibre decisions (1, 1) pass. The decisions (0, 1) do not.

## What is proved

On this one triangle, with unit integer weights: the face of every coboundary is 0; the unit l1 residual is at least the absolute face value for every integer repair; the two repairs meet that bound; a face of 0 is an integer coboundary; the coboundary length 2 of (0, 1, 0) is not the quotient value 0 of (1, -1, 0); the face of (1, 0, 0) is 1; the two verdict instances; and the two fibre instances.

## What is assumed

Integer arithmetic on one triangle with unit weights. The verdict is the two-argument rule used for the two instances above. A fibre passes when the two decisions are equal. AuthorityEffect is None. No identification of this quotient with a boundary-leakage formula is assumed.

## What is open

The weighted certificate over the rationals, a bounded-circulation dual on a general carrier, the second coboundary diagnostic, the full trichotomy off this triangle, an adapter from the quotient value to the local-green global-red evaluator, sector weights, a quantum state, the L1 stage, and every carrier other than this triangle. A face of 0 is an integer coboundary here because the exhibited repair meets the bound. That fact is not claimed for a general complex.
