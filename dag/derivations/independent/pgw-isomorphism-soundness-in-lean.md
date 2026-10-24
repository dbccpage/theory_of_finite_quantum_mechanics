Status: AI-drafted, awaiting human review.

# PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN

Node status stays OPEN. This note records the two-datum regimes U0, U1, and BL.

## Regimes

U0 has data count 2, one form of arity 1, instance (0, [0]), no rules, and requirement (0, 1).

U1 has the same fields, with instance (0, [1]).

BL has data count 2, one form of arity 2, instance (0, [0, 1]), no rules, and requirement (0, 1).

Each list of instances, rules, and requirements is duplicate-free. Each form arity is at least 1, and the requirement is the ordered pair (0, 1) with the second index below the data count.

## Exhaustive search

A candidate is one datum permutation together with one form permutation. Data count 2 has two datum permutations. One form has one form permutation. Lean checks that each of the three candidate lists has length 2.

## Isomorphism and keys

The swap of datum 0 with datum 1 sends (0, [0]) to (0, [1]) and sends requirement (0, 1) to itself. That swap is an isomorphism from U0 to U1. The exhaustive canonical keys of U0 and U1 are equal.

BL's form has arity 2 and U0's form has arity 1. A form bijection preserves arity, so no isomorphism from U0 to BL exists. The exhaustive canonical keys of U0 and BL differ.

An independent enumeration, separate from the Lean kernel, finds the shared unary minimum (2, [1], [(0, [0])], [], [(0, 1)]) and the binary minimum (2, [2], [(0, [0, 1])], [], [(0, 1)]).

## What is proved

U0, U1, and BL are well-formed and duplicate-free. Each exhaustive candidate list has length 2. U0 and U1 are isomorphic and have equal exhaustive keys. U0 and BL are not isomorphic and have different exhaustive keys.

## What is assumed

U0, U1, and BL are the regimes in the sealed minimality module. The exhaustive key is the minimum of the serialized relabelings over every datum permutation and every form permutation. Equality of those keys on well-formed duplicate-free regimes is the classification already recorded for that search.

## What is open

A Python key procedure, a budget-truncated search, and a comparison of Python orbits with Lean orbits on exported runs stay open. Status stays OPEN.
