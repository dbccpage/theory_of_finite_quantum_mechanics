# Secant Remainder Breakdown for Degree-4 Two-Basis Overlap Polynomials

Type: observation
Confidence: high
Source: Candidates L01_N13, L00_N11, L00_N12
Relevant to: Rectangular Krawczyk contractors, candidate basis search, interval exclusion

## Statement
The exact midpoint secant identity:
$$F(x) - F(c) = J\left(\frac{x+c}{2}\right)(x - c)$$
holds strictly for systems of quadratic polynomials ($F \in \mathbb{R}[x]_{\le 2}$). When searching for two variable candidate bases simultaneously (120 free coordinates), the mutual unbiasedness condition:
$$|u^\dagger v|^2 = \frac{1}{6}$$
between candidate basis 3 and candidate basis 4 is degree 4 in the real variables. For degree-4 polynomials, the midpoint secant formula has a non-vanishing second-order Taylor remainder, precluding zero-remainder rectangular Krawczyk formulations unless auxiliary bilinear variables are introduced.

## Evidence
For a scalar quartic $f(x) = x^4$, the exact difference is:
$$f(x) - f(c) = (x - c)(x^3 + x^2 c + x c^2 + c^3)$$
Evaluating the derivative at the midpoint $(x+c)/2$ gives:
$$f'\left(\frac{x+c}{2}\right)(x - c) = 4\left(\frac{x+c}{2}\right)^3(x - c) = \frac{1}{2}(x^3 + 3x^2 c + 3x c^2 + c^3)(x - c)$$
The difference between the two expressions is non-zero:
$$f(x) - f(c) - f'\left(\frac{x+c}{2}\right)(x - c) = \frac{1}{2}(x - c)^3 (x + c)$$
This remainder scales with the cube of the interval diameter and cannot be dropped in interval contractor bounds.

## Implications
Formulations developed for single-basis candidate searches (where one basis is fixed and the system remains quadratic in 72 variables) do not transfer directly to two-basis quartet formulations without either lifting the degree back to 2 via auxiliary variables or explicitly bounding higher-order interval Lagrange remainders.

## Caveats
Lifting to a quadratic system via auxiliary bilinear variables restores the zero-remainder property, but increases the state dimension to 440 real variables and introduces auxiliary gauge null directions.
