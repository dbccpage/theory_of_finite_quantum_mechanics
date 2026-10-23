Status: AI-drafted, awaiting human review.

# Finite forests for one overlapping diagram

AuthorityEffect: None.

The node `DFM-BPHZ-CONTINUUM-FENCE` says that algebraic cancellation of nested and overlapping ultraviolet boundary poles, for actual Feynman-parametric integrands, and the use of that cancellation before continuum integration, is not established by the finite artifacts. This note records a finite special case. It does not supply a Feynman integrand or an integral.

## Declared edge sets

Three subgraphs are fixed by their edges:

- `L = {0, 1, 2}`
- `R = {2, 3, 4}`
- `G = {0, 1, 2, 3, 4}`

Edge `2` lies in all three. Two of these sets are compatible when one contains the other or they are disjoint. Then `L` is compatible with `G`, and `R` is compatible with `G`, but `L` is not compatible with `R`.

A Zimmermann forest, for this finite list, is a subset in which every pair is compatible. The power set has eight subsets. The two subsets that contain both `L` and `R` are rejected. The other six are forests:

- empty
- `{L}`
- `{R}`
- `{G}`
- `{L, G}`
- `{R, G}`

A nested control with `inner = {0, 1}` and `outer = {0, 1, 2, 3}` has `inner` contained in `outer`, so all four subsets are forests.

## Order-0 evaluations

Let `I` be a rational function of two rational arguments. The order-0 operators used here are evaluations, not Taylor polynomials of positive degree:

- `T_L I(x, y) = I(0, y)`
- `T_R I(x, y) = I(x, 0)`
- `T_G I(x, y) = I(0, 0)`

The signed six-forest sum puts a minus on each singleton and a plus on the empty forest and on each doubleton. Because `T_G` sends both `T_L I` and `T_R I` to the same constant `I(0, 0)`, the two doubleton terms and the `{G}` term collapse:

```
I(x, y) - I(0, y) - I(x, 0) - I(0, 0) + I(0, 0) + I(0, 0)
  = I(x, y) - I(0, y) - I(x, 0) + I(0, 0).
```

The pair `{L, R}` is not a forest, so there is no term `T_R T_L I` coming from that pair. The same algebraic expression is reached only because `{G}` is present and absorbs the subgraph evaluations.

## The declared numerator

Take `N(x, y) = 2 + 3x + 5y + 7xy`. This polynomial is declared data. It is not obtained from a graph polynomial or a parametric integral.

Expanding the collapsed sum gives

```
N(x, y) - N(0, y) - N(x, 0) + N(0, 0)
  = (2 + 3x + 5y + 7xy) - (2 + 5y) - (2 + 3x) + 2
  = 7xy.
```

Wherever `xy ≠ 0`, the quotient of that sum by `xy` equals `7`. The constant term `2`, the pure `x` term and the pure `y` term have cancelled.

If the forests that mention `G` are omitted, the remaining sum is

```
N(x, y) - N(0, y) - N(x, 0) = 7xy - 2,
```

and the quotient is `7 - 2/(xy)`. The constant `2` is still present. At `(x, y) = (1/2, 1/3)` the six-forest numerator is `7/6`, its quotient is `7`, and the omitted-`G` quotient is `-5`.

## A different identity

The nested sector kernel `K(z; λ) = (1 + z λ) / (λ (1 + λ))` at `z = 3/5` has four-term value `(z / (1 + λ_1)) (z / (1 + λ_2))`. At `λ_1 = 1/2` and `λ_2 = 1/3` that value is `9/50`. The formal substitution `λ_1 = λ_2 = 0` gives `z² = 9/25`. Neither number is `7`. The sector-kernel check does not state the overlapping forest count or the numerator `N`.

## General finite subtraction API

Let A be an additive commutative group. A Projector supplies an additive map P
and a proof P(P(x))=P(x). Its remainder is x-P(x), which P kills. For a finite
list of pairwise commuting projectors, reduce composes these remainders.
The empty list acts as the identity. Commutation moves each projector through
the other remainders, so every projector kills the reduced value. Conversely,
a value killed by every projector is fixed by each remainder and by reduce.
Thus reduce is idempotent and packages as a reusable kernelProjector.
Concatenating lists composes reductions; applying a subfamily after a compatible
full family leaves the result unchanged. Duplicate projectors are permitted.

Evaluation at zero in the left or right argument is an additive idempotent on
rational-valued functions. These evaluations commute, and the original sixSum
is exactly their two-projector reduction. This is an order-zero client, not a
proof of a general Zimmermann formula for noncommuting Taylor subtractions.
The independent matrix check enumerates 12 exact idempotents with entries in
{-1,0,1}, and 77 compatible lists of length at most two. It tests kernel,
idempotence, repeated-family and subfamily identities, rejects a non-idempotent
and a noncommuting family, and refuses three inexact scalar inputs and two
sector poles. Four selected faults are detected. None of these finite tests
is a continuum convergence result.

## What is proved

On these three edge sets, the compatible subsets are exactly the six forests listed above, and the nested control has four forests. For every rational bivariate `I`, the signed six-forest sum of the order-0 evaluations equals `I(x, y) - I(0, y) - I(x, 0) + I(0, 0)`. For `N`, that expression equals `7xy`, and the quotient by `xy` equals `7` when `xy ≠ 0`. Omitting `G` leaves `7 - 2/(xy)`. The witness `(1/2, 1/3)` gives the quotients `7` and `-5`.

## What is assumed

The edge sets, the compatibility rule, the order-0 evaluations, and the numerator `N` are declared. No continuum measure, no loop-momentum integral, and no renormalization condition is used. Arithmetic is the field of rational numbers.

## What is open

No Feynman-parametric integrand is subtracted. No operator `T^ω` of positive degree is defined. No integral is shown to converge, and nothing is transported to a smooth gauge theory or to continuum momentum space. The original fence, that those continuum statements are not established, remains in force. The node stays open.
