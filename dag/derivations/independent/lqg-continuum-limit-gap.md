Status: AI-drafted, awaiting human review.

# LQG-CONTINUUM-LIMIT-GAP

AuthorityEffect: None.

The level-2 recoupling labels used by the repository are the three
twice-spin values 0, 1, and 2. This note checks a finite census of those
labels and two dimension identities in Q(sqrt 2). It does not construct a
limit.

## Admissibility

An ordered triple (a, b, c) of natural numbers is admissible when all four
of the following hold:

- a, b, and c are each at most 2;
- the triangle inequalities c ≤ a + b, b ≤ a + c, and a ≤ b + c hold;
- a + b + c is even;
- a + b + c is at most 4.

These are the eight comparisons in the repository function `ising_admissible`.
The comparison here is rechecked on its own. It is not a certified
translation of the Rust source.

There are 3 × 3 × 3 = 27 ordered triples with entries in {0, 1, 2}. Filtering
them by the predicate leaves exactly these ten, in lexicographic order:

```
(0, 0, 0), (0, 1, 1), (0, 2, 2),
(1, 0, 1), (1, 1, 0), (1, 1, 2), (1, 2, 1),
(2, 0, 2), (2, 1, 1), (2, 2, 0).
```

The triple (0, 0, 1) is excluded: the sum 1 is odd, and 0 + 0 < 1.

## Tuple counts

A six-tuple of labels has 3^6 = 729 elements. A nine-tuple has 3^9 = 19683
elements. These are counts of the finite label set. They are not a state sum,
and they are not a limit of state sums.

## Quantum dimensions

Write elements of Q(sqrt 2) as rat + coeff * sqrt(2) with rational rat and
coeff. Multiplication is

```
(r1 + c1 sqrt(2))(r2 + c2 sqrt(2))
  = (r1 r2 + 2 c1 c2) + (r1 c2 + c1 r2) sqrt(2).
```

The three quantum dimensions are d0 = 1, d1 = sqrt(2), and d2 = 1. Then

```
d1^2 - d0 = 2 - 1 = 1 = d2,
d1 d2 - d1 = sqrt(2) - sqrt(2) = 0.
```

## The counts do not pick one scale

The positive rationals 3, 729, and 19683 are pairwise distinct. The positive
rational 1 is distinct from all three. A list of three different positive
rationals, together with another positive rational outside that list, does
not by itself name one scale. Nothing in this census sends those counts to a
cosmological constant.

## What is proved

On {0, 1, 2} the admissibility predicate accepts exactly the ten ordered
triples listed above, and it rejects (0, 0, 1). The set has 729 six-tuples
and 19683 nine-tuples. The two dimension identities hold in Q(sqrt 2). The
numbers 3, 729, and 19683 are pairwise distinct, and 1 is a positive rational
distinct from all three.

## What is assumed

The eight comparisons are the admissibility predicate being counted. The
quantum dimensions are the three elements 1, sqrt(2), and 1. No identification
of this predicate with a continuum theory is assumed.

## What is open

A continuum limit, a semiclassical limit, and a physical cosmological
constant remain undischarged. No sequence of triangulations and no Einstein
equation is constructed. The exact 6j values, the area spectrum, and the
pentagon identity on all 19683 nine-tuples are not re-checked here. The routes
into and out of this node stay without a derivation of a limit. The node
stays OPEN.
