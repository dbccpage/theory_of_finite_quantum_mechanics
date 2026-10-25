Status: AI-drafted, awaiting human review.

# PGW-RUNS-PAST-DECLARED-BOUNDS

Node status stays OPEN. This note records five records on the declared bound line. It does not replay a forward run.

## The line

A record has four coordinates: rounds, nodes, data, and items. It is inside the declared line when the rounds are at most 15, the nodes are at most 250, the data count is below 4, and the items are at most 2. A coordinate at its cap is inside, except data, where the words say below 4, so 3 is inside and 4 is outside.

## Five records

(15, 250, 3, 2) is inside.

(16, 250, 3, 2) is outside, by one round.

(15, 251, 3, 2) is outside, by one node past the guard.

(15, 250, 4, 2) is outside, because the data count is not below 4.

(15, 250, 3, 3) is outside, by one item past two.

## What is proved

Those five comparisons, and nothing about a stored run.

## What is assumed

The declared line is the four inequalities above. No forward-run program was executed. AuthorityEffect is None.

## What is open

The census of stopped runs is not proved. Leftovers H-2 to H-9 stay open. Whether the augmentation sequence is unbounded stays open. Running the declared class past the bounds stays open.
