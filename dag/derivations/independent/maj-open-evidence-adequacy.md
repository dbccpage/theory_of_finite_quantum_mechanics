Status: AI-drafted, awaiting human review.

# MAJ-OPEN-EVIDENCE-ADEQUACY

Node status stays OPEN. This note records two integer coordinate maps.

## Two readings

Take the integer pairs topo = (1, 0) and andreev = (1, 1). Subtract coordinatewise. The first coordinates give 1 - 1 = 0. The second coordinates give 0 - 1 = -1. The difference is the pair (0, -1).

## The first coordinate

The first-coordinate map sends a pair to its first entry. It sends the difference (0, -1) to 0. It sends topo to 1 and andreev to 1. The two readings agree on this coordinate, and their difference lies in the kernel of this map.

## The second coordinate

The second-coordinate map sends a pair to its second entry. It sends the difference (0, -1) to -1. It sends topo to 0 and andreev to 1. Those two values differ, so this map separates the two readings.

## What is proved

For these two pairs and these two maps: the difference is (0, -1); the first coordinate of the difference is 0 and both readings have first coordinate 1; the second coordinate of the difference is -1, the second coordinates are 0 and 1, and those second coordinates differ.

## What is assumed

Integer arithmetic and coordinate projection. The two readings are the listed pairs. AuthorityEffect is None.

## What is open

A laboratory protocol, a device model, a density operator, and any measurement map supplied by a physical apparatus. These coordinate maps are not that protocol. Whether a declared laboratory map separates topological zero modes from Andreev bound states stays open.
