Status: AI-drafted, awaiting human review.

# PGW-WDP-BRIDGE-ONGOING-TO-WINDOW

Node status stays OPEN. This note records the carrier {0, 1}.

## Slots

The carrier has two vertices. The directed table has four integer slots: the loop at 0, the loop at 1, the arc from 0 to 1, and the arc from 1 to 0. A vertex pair (g0, g1) raises the table by (0, 0, g0 - g1, g1 - g0). Both loops of a coboundary are 0, and the two arcs are negatives of each other.

## One unbalanced mark

The mark (0, 1, 0) repeats vertex 0. Its diagnostic reads the arc 0 to 1, the arc 1 to 0, and the loop at 0. It does not read the loop at 1. On a coboundary the three read slots cancel, so the diagnostic is 0. Adding a coboundary does not change the diagnostic of an arbitrary integer table.

## Denominator

Suppose a nonzero integer b scales an integer slot difference onto a coboundary of some vertex pair. The two loop differences are 0, and the two arc differences are negatives. That difference is already the coboundary of the vertex pair (0, -d01), where d01 is the difference on the arc from 0 to 1.

## Two quotients on this carrier

The table (1, 0, 0, -1) has diagnostic 0, and its loop at 0 is 1, so it is not a coboundary. The table (0, 1, 0, 0) has diagnostic 0, and its loop at 1 is 1, so it is not a coboundary. The one-arc table (0, 0, 1, 0) has diagnostic 1. The two-way table (0, 0, 1, 1) has arc sum 2 and arc difference 0.

## What is proved

The coboundary slots, the cancellation on the unbalanced mark, repair invariance of that diagnostic, reflection of a nonzero integer denominator, the two closed tables that are not coboundaries, the one-arc diagnostic 1, and the two-way sum 2 with difference 0.

## What is assumed

The four slots and the diagnostic e01 + e10 + e00 are the definitions above. The carrier is fixed as {0, 1}. AuthorityEffect is None.

## What is open

A general carrier, an arbitrary marked family, the degree-1 window of TFQ-0004, a continuous norm, and carrier-changing term operations stay open.
