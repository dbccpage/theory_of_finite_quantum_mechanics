Status: AI-drafted, awaiting human review.

# Three integer keep-and-scale steps with a zero addend

AuthorityEffect: None.

## Setup

Two sequences start at 1. The next keep-value is 3 times the current one. The next scale-value is 4 times the current one. A third sequence uses the same keep factor and adds 0.

## Arithmetic

The first values are u(1) = 3 and v(1) = 4, and 3 is below 4.

The second values are u(2) = 3*3 = 9 and v(2) = 4*4 = 16, and 9 is below 16.

The third values are u(3) = 3*9 = 27 and v(3) = 4*16 = 64, and 27 is below 64.

Adding 0 at each keep step leaves the keep-value unchanged, so the third sequence agrees with u at steps 0, 1, 2 and 3.

## What is proved

The two recurrence equations, the zero-addend recurrence, the four pairs (1, 1), (3, 4), (9, 16) and (27, 64), the three strict comparisons, and the agreement of the zero-addend sequence with u at those four steps.

## What is assumed

Arithmetic of the natural numbers, including decidable comparison of closed terms.

## What is open

The Aharonov, Ben-Or, Impagliazzo and Nisan limitation for noisy reversible or quantum computation with no fresh low-entropy supply, under that paper's own noise and depth hypotheses. These pairs are not a trace norm, not a depolarizing channel, and not an independent per-qubit noise model. The history-distance product for global depolarizing noise stays on its own record.
