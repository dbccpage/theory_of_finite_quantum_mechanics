Status: AI-drafted, awaiting human review.

# FSP-THETA-TERM-COMPLEX-WEIGHT

Node status stays IMPORTED_ASSUMPTION. The standing text is a four-index Gaussian-integer table for charges 0 and 1. An exponential, a real angle, a plaquette sum, and a Monte Carlo sampler stay outside this note.

## Quarter turns

Write a Gaussian integer as an integer pair. The turn by the pair (0, -1) sends (a, b) to (b, -a). Starting at (1, 0), the values at indices 0, 1, 2, 3 and 4 are (1, 0), (0, -1), (-1, 0), (0, 1) and (1, 0). The same turn is the product

(a, b) * (c, d) = (a * c - b * d, a * d + b * c)

with (c, d) = (0, -1). In particular, (1, 0) * (0, -1) = (0, -1).

## Charges 0 and 1

Charge 0 keeps the weight (1, 0) at each index 0, 1, 2 and 3. Charge 1 uses the quarter-turn value at that index. Any other charge is outside the table.

## Real and positive coordinates

At charge 1, the second coordinate is 0, -1, 0 and 1 at indices 0, 1, 2 and 3. It differs from 0 at indices 1 and 3. At index 2 the first coordinate is -1, so that pair is not positive in the first coordinate. The pair at index 0 with charge 1 has first coordinate 1 and second coordinate 0. Among the four charge-1 pairs, only index 0 has a positive first coordinate and a zero second coordinate.

## What is proved

The five quarter-turn values, the identification of the turn with multiplication by (0, -1), the product (1, 0) * (0, -1) = (0, -1), the charge-0 weights (1, 0), the charge-1 weights, the second coordinates, the index-2 first coordinate -1, and the fact that only index 0 among 0, 1, 2 and 3 is positive-real at charge 1.

## What is assumed

Integer arithmetic and the declared turn, product, and weight table. AuthorityEffect is None.

## What is open

The source sentence that an added term i theta Q_top multiplies a Boltzmann weight by exp(-i theta Q_top), a real angle, a plaquette sum called topological charge, and a positive-weight sampler for a nonzero angle.
