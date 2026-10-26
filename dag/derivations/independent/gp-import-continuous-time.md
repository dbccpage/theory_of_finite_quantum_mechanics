Status: AI-drafted, awaiting human review.

# GP-IMPORT-CONTINUOUS-TIME, finite toggle slice

## Toggle

The labels are false and true. Toggle sends false to true and true to false. A square root of toggle would be a map sigma on those labels with sigma(sigma(q)) = toggle(q) for both labels. There are four maps on two labels. Each fails that equation: the constant maps land on one label, and each of the two bijections squares to the identity rather than to toggle.

## Gaussian pairs

A Gaussian integer in this note is a pair of ordinary integers. Addition is coordinatewise. Multiplication is (a, b) * (c, d) = (a*c - b*d, a*d + b*c).

A state is a pair (x, y) of Gaussian integers. Swap exchanges the coordinates. Scaling by (4, 0) multiplies each integer coordinate by 4.

## Interpolants

The interpolant sends (x, y) to

((1, 1) * x + (1, -1) * y, (1, -1) * x + (1, 1) * y).

Expanding the composition in the four integer coordinates gives the swap of the state scaled by (4, 0). The coordinatewise negation of the interpolant is another map. Negating twice returns the original pair, and the same expansion shows that this second map has the same square.

At ((1, 0), (0, 0)) the interpolant returns ((1, 1), (1, -1)) and the negation returns ((-1, -1), (-1, 1)). Those pairs differ, so the two interpolants are not the same map.

## What is proved

The two toggle values, the absence of a Boolean square root, the pair sum and product, the exchange under swap, the scale-4 square of both interpolants, and the two witness values.

## What is assumed

The labels are the two Boolean values. The pairs are integer coordinates with the sum and product written above. No continuity or inner-product structure is used.

## What is open

Continuous time, a topology, a one-parameter unitary group, and Stone's theorem remain imported. A rational Cayley transform and a hyperoctahedral residue are outside this case.
