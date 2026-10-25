Status: AI-drafted, awaiting human review.

# MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE

Node status stays OPEN. This note records the integer envelope at T = 1, 2 and 3.

## The integer stand-in

The source envelope mixes a square term that grows as the time gets small with a term that grows as the time gets large. This note keeps one integer stand-in of that tradeoff. Fix coefficients 4 and 1. For a positive integer T, multiply 4 / T^2 + T by the positive integer T^2. The product is the polynomial

f(T) = 4 + T^3.

At T = 2 the cube is 8, so f(2) = 4 + 8 = 12. The same value is 3 times T^2, because 3 * 4 = 12. The comparison polynomial with that coefficient is

comparison(T) = 3 T^2.

The coefficient 3 is the value of the cleared polynomial at T = 2, divided by T^2 = 4, and that division is the integer identity 12 = 3 * 4. Twice the leading coefficient 4 is 8, and 8 is also 2^3, so T = 2 is an integer point where the two growths meet after clearing the denominator.

## The three times

Direct evaluation:

- T = 1. f(1) = 4 + 1 = 5. comparison(1) = 3. 5 is greater than 3.
- T = 2. f(2) = 12 and comparison(2) = 12. The two sides are equal.
- T = 3. f(3) = 4 + 27 = 31. comparison(3) = 27. 31 is greater than 27.

## A positive envelope and a zero reading

f(2) = 12 and 12 is greater than 0. The natural number 0 is strictly below 12. An envelope value that is positive can sit strictly above a transfer-defect reading of 0. The positivity of the envelope is a separate sentence from the positivity of a defect.

## What is proved

For this one polynomial: f(1) = 5 is greater than comparison(1) = 3; f(2) = 12 equals comparison(2) = 12; f(3) = 31 is greater than comparison(3) = 27; 12 is greater than 0; and 0 is strictly below f(2).

## What is assumed

Natural-number arithmetic. The coefficients are the constants 4 and 1, and the comparison coefficient is the constant 3 fixed by the value at T = 2. AuthorityEffect is None.

## What is open

The Lindblad derivation, the four-mode braiding model, the exponential poisoning term, the Landau-Zener square, every time outside {1, 2, 3}, and a positive lower bound on the physical transfer defect. A positive envelope value does not by itself force that defect to be positive.
