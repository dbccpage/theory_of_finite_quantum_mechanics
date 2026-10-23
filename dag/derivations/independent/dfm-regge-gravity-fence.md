Status: AI-drafted, awaiting human review.

# DFM-REGGE-GRAVITY-FENCE

AuthorityEffect: None.

The cosine law assigns a rational value to each angle of a triangle with
rational side lengths. That value is not a hinge holonomy. The block trace
below uses a hand-chosen parameter `beta = 1/2`, not the lengths 3, 4, and 5.

## Lengths and one block trace

For positive rationals `b` and `c`, write

```
cosNum(a, b, c) = b^2 + c^2 - a^2
cosLaw(a, b, c) = cosNum(a, b, c) / (2 b c)
```

For every rational `a`, `b`, and `c`,

```
cosNum(a, b, c) + cosNum(b, a, c) + cosNum(c, a, b) = a^2 + b^2 + c^2.
```

At lengths 3, 4, and 5 the numerators opposite those sides are 0, 32, and 18,
and the cosine-law values are 0, 4/5, and 3/5. Their sum is 7/5. The three
numerators add to 50, which equals `3^2 + 4^2 + 5^2`.

Separately, with `beta = 1/2`,

```
gamma = (1 + beta^2) / (1 - beta^2) = 5/3
2 beta / (1 - beta^2) = 4/3
blockTrace = 2 gamma + 2 = 16/3.
```

The denominator `1 - beta^2` equals `3/4`, so it is not zero. `16/3` differs
from 4 and from `7/5`.

## What is proved

In `lean4/CampaignDfmReggeGravityFence.lean`:

- `numerator_sum` is the numerator identity for every rational triple.
- `lengths_345` records the numerators 0, 32, and 18, the total 50, the
  cosine-law values 0, 4/5, and 3/5, and the sum 7/5.
- `block_trace_half` records the denominator gap, `gamma = 5/3`, the
  off-diagonal value 4/3, the block trace 16/3, and the two inequalities
  with 4 and with 7/5.
- `cosine_sum_ne_block_trace` records that 7/5 and 16/3 differ.

The independent check recomputes the same values and evaluates the numerator
identity on four explicit triples.

## What is assumed

The entries lie in `Q`. Squares and quotients are the field operations. The
lengths 3, 4, and 5 are supplied data, and `beta = 1/2` is supplied data.

## What is open

A 4D Regge complex, a deficit angle, a Spin+ spin-frame dressing, a discrete
Dirac action, and a continuum gravity reading stay open. The node status
stays OPEN.
