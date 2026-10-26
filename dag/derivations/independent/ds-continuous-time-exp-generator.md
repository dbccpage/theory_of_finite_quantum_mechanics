Status: AI-drafted, awaiting human review.

# DS-CONTINUOUS-TIME-EXP-GENERATOR

The imported claim asks for a one-parameter family T(t) = exp(tH), a logarithm H = log T, and a continuum path integral. This note records finite integer facts around a two-label toggle and a 2 by 2 swap. It does not construct real or complex time, a convergent series, or a measure.

## Toggle

On the labels false and true, toggle exchanges the two labels. Any map on those labels sends each label to one of the two, so there are four maps. Each map squared fixes at least one label, while toggle fixes neither. So no such map squares to toggle.

## Two matrices

A Gaussian pair is an ordered pair of integers. Addition is coordinatewise. Multiplication is (a, b) * (c, d) = (a*c - b*d, a*d + b*c).

Let A have rows ((1, 1), (1, -1)) and ((1, -1), (1, 1)). Let B be the coordinatewise negation of A. Matrix multiplication of Gaussian pairs gives A squared and B squared both equal to the matrix whose diagonal entries are (0, 0) and whose off-diagonal entries are (4, 0). A and B differ in the first entry.

The factor 4 is kept. These two matrices are not presented as a normalized unitary square root.

## Cayley polynomial

For every integer t,

(1 - t*t) * (1 - t*t) + 4 * (t*t) = 1 - 2*t*t + (t*t)*(t*t) + 4*t*t = 1 + 2*t*t + (t*t)*(t*t) = (1 + t*t) * (1 + t*t).

This is a polynomial identity. It does not build a one-parameter group.

## Branch energies

The branch energy of an integer k is 2*k + 1. It equals 1 at k = 0 and 3 at k = 1. If k1 and k2 differ, then 2*k1 + 1 and 2*k2 + 1 differ, because their difference is 2*(k1 - k2). Distinct integer labels therefore give distinct odd energies. Selecting one generator from that family is not done here.

## Nilpotent integer logarithm

The swap matrix has rows (0, 1) and (1, 0). Adding the identity to an integer matrix with entries a, b, c, d produces rows (a + 1, b) and (c, d + 1). Matching the swap forces a = -1, b = 1, c = 1 and d = -1. The top-left entry of the square of that matrix is (-1)*(-1) + 1*1 = 2, which is not 0. The other three entries of a zero square are likewise unavailable at the same point. So no integers meet both the swap-shift equations and the four zero-square equations. A first-order exponential I + H with H squared equal to zero does not give this swap over the integers.

## What is proved

The toggle images, the absence of a Boolean square root, the two Gaussian pair operations, the two scale-4 matrix squares and their difference, the Cayley polynomial, the two sample branch energies and their separation for distinct integers, the corner value 2, and the absence of an integer nilpotent logarithm of the swap.

## What is assumed

Arithmetic of the integers and case analysis on the two Boolean labels. No operator exponential and no measure are assumed.

## What is open

A continuous one-parameter family, an analytic logarithm, generator selection among the odd branch energies, a convergence oracle, and a continuum path-integral measure. Those interfaces stay imported.
