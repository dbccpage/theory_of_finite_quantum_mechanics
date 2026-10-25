Status: AI-drafted, awaiting human review.

# GTH-SHADOW

Node status stays OPEN. This note records one triangle and one reach map.

## The triangle

The three edges are the pairs (0, 1), (0, 2) and (1, 2). The source of a pair is its first entry. The target is its second entry.

- The target of (0, 2) is 2, and the target of (1, 2) is 2.
- The target of (0, 1) is 1, and the source of (1, 2) is 1.
- The source of (0, 1) is 0, and the source of (0, 2) is 0.

These are the three face identities for this one triangle. There is no degeneracy map.

## The reach map

The reach map sends 0 to 0 and 1 to 0. The pair of those values is (0, 0). That pair differs from the edge (0, 1).

## Two parallel edges

Label two edges 0 and 1. The source map sends both to 0. The target map sends both to 1. The two source values agree, and the two target values agree.

## What is proved

The three face identities, the two reach values, the inequality of (0, 0) with (0, 1), and the agreement of the two source values and of the two target values. The campaign module CampaignGthShadow decides those evaluations. This node's lean list stays empty, because this stage rejects a Lean citation on the node.

## What is assumed

Natural-number arithmetic, pair projection, and the listed constants. The two-valued admission record is the background of the reach map, which sends both values to 0. AuthorityEffect is None.

## What is open

A construction that turns the admission gate into a finite semi-simplicial set or a finite globular set. Every complex other than this triangle and this pair of edges. Degeneracy maps. The four kinds of change. Path components, a fundamental groupoid, and horn fillers.
