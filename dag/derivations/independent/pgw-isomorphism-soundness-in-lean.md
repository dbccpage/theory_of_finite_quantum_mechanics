Status: AI-drafted, awaiting human review.

# PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN

Node status stays OPEN. This note records the two-data coloring key. It does not check an implemented regime key.

## Colorings

A coloring is a pair of bits. There are four: (false, false), (false, true), (true, false), and (true, true).

The swap exchanges the two bits. Doing it twice returns the original pair. The two constant pairs are fixed by the swap.

The serialization reads false as 0 and true as 1. The key of a coloring is the lexicographic minimum of its serialization and the serialization of its swap.

## Keys

The four keys are (0, 0), (0, 1), (0, 1), and (1, 1), in the order of the four colorings above. Two colorings share the key (0, 1). The constant colorings have different keys.

For every pair of these colorings, the keys are equal exactly when one coloring is the other or the swap of the first is the second. Swapping a coloring does not change its key.

## What is proved

The swap is an involution. The four keys are the pairs named above. Equal keys on this four-element set hold exactly under equality or one swap. The two constant colorings are fixed points with different keys. The universe has length 4, and two of its members have key (0, 1).

## What is assumed

The order on pairs of numbers is lexicographic, first component then second. The universe is every pair of bits. No Python or Rust key procedure was executed. AuthorityEffect is None.

## What is open

The implemented key is not proved. Regimes past the brute-force limit of a key cross-check stay open. A comparison of Python automorphism orbits with Lean orbits on exported regimes stays open.
