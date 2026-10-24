Status: AI-drafted, awaiting human review.

# PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT

Node status stays OPEN. This note records one triangle, vertices 0, 1, 2.

## Slot swap

Genesis edge slots are (01, 02, 12). The swap sends (a, b, c) to (a, c, b), which is (01, 12, 02). Doing it twice returns the original triple.

The admitted face column is (1, -1, 1). After the swap it is (1, 1, -1). That is the WDP row with values 1, 1, -1 on slots 01, 12, 02.

Negating the 02 component sends (1, 1, -1) to (1, 1, 1).

## Vertex cycle and coboundary

On the swapped column (1, 1, -1) the three vertex values are -1 - (-1), 1 - 1, and 1 + (-1). Each equals 0.

The same row read by triD1 is 1 + 1 - (-1), which equals 3. That value is not the vertex cycle.

For any integers f0, f1, f2, (f1 - f0) + (f2 - f1) - (f2 - f0) equals 0. The same cancellation is the identity triD1 of triD0 on a rational vertex triple.

## What is proved

The swap is an involution. The face column (1, -1, 1) swaps to (1, 1, -1) and matches the row (1, 1, -1). Negating slot 02 yields (1, 1, 1). The swapped column has vertex boundary 0, 0, 0. triD1 of that row is 3. triD1 of triD0 is 0 on every rational vertex triple.

## What is assumed

Genesis d2 at weight 1 is the column (1, -1, 1) in slot order (01, 02, 12). The WDP row on (01, 12, 02) is (1, 1, -1), and triD1 subtracts the 02 component. The vertex formulas are the Genesis boundary read in the swapped slot order.

## What is open

A transport of a general window quantity, monograph invariance under reorientation, and a theorem that d0 and d1 of the whole WDP window are the transposes of the Genesis boundary maps stay open. Status stays OPEN.
