Status: AI-drafted, awaiting human review.

# PGW-PYTHON-LEAN-CARRIER-BRIDGE

Node status stays OPEN. This note records two sealed Lean replays. It does not join a Python computation to a Lean statement.

## Histories

Reading L, from the empty genesis regime, is the event list supply 0, supply 1, supply 1, supply 2, admit datum, admit datum, impose (0, 1). That list has length 7.

Reading F is supply 0, admit datum, supply 1, supply 1, supply 2, admit datum, admit datum, impose (1, 2). That list has length 8.

A supply leaves the regime unchanged. Admit datum adds one to the data count. Impose (i, j) records the pair when i < j and j is strictly below the data count.

## Results

Reading L replays to the regime with data count 2, empty form, instance, and rule lists, and requirement list (0, 1).

Reading F replays to the regime with data count 3, empty form, instance, and rule lists, and requirement list (1, 2).

Those two regimes are different, and the two replay results are different.

## What is proved

The two replays, the two data counts, the two requirement lists, the empty carrier lists, the two history lengths, and the inequality of the regimes and of the replay results.

## What is assumed

The event step is the sealed Lean step on one regime. The two lists are the histories recorded for readings L and F. No Python program was executed. AuthorityEffect is None.

## What is open

A refinement from a Python computation to a Lean statement stays open. Token erasure, the license binding, rung-two track one, and the Python histories that stop before the requirement stay open.
