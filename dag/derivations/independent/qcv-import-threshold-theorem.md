Status: AI-drafted, awaiting human review.

# Integer orbit for one concatenation-style step

AuthorityEffect: None.

## Setup

Let t be the map on the integers given by t(n) = 2*n*n. This is one stated integer case of a quadratic concatenation step with constant 2. It is not a noise model and not a code.

## Arithmetic

By the definition, t(8) = 2*8*8. Direct expansion gives 2*8*8 = 128, so t(8) = 128.

The same definition gives the first values t(0) = 0, t(1) = 2 and t(2) = 8.

Three applications starting at 1 are t(1) = 2, t(2) = 8 and t(8) = 128, so t(t(t(1))) = 128.

The scale products at the two seeds are 2*0 = 0 and 2*1 = 2.

## What is proved

The definition t(n) = 2*n*n, the four values 0, 2, 8 and 128, the three-step orbit value 128, the product identity 2*8*8 = 128, and the two scale products 0 and 2.

## What is assumed

Integer arithmetic, including decidable equality of closed integer terms.

## What is open

The fault-tolerance threshold theorems of Shor, Aharonov and Ben-Or, Kitaev, Knill, Laflamme and Zurek, and Aliferis, Gottesman and Preskill, each under that theorem's own noise, locality and overhead hypotheses. No noise model is shown to obey t. No code constant is computed. The rational concatenation recurrence and its dichotomy stay on their own record.
