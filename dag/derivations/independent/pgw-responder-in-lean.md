Status: AI-drafted, awaiting human review.

# PGW-RESPONDER-IN-LEAN narrowed boundary

AuthorityEffect: None.

The node stays OPEN. The shadow below is a declared flag table and two copied lists. It is not the sealed responder.

## Shadow

A demand is read only when its kind is collapsed and the uniform-rule flag is false. The four pairs and their read values are (collapsed, false) = true, (collapsed, true) = false, (separable, false) = false, and (separable, true) = false. The number of true values is 1.

The mark copies `deltaU0`: a form of arity 1 followed by the argument list [0]. The link copies `deltaBL`: a form of arity 2 followed by [0, 1]. Each list has length 2. The new-form arity sums are 1 and 2. Item-count cost mu1 is 2 on both lists, so they tie at cost 2. Pair cost mu2 is (2, 1) for the mark and (2, 2) for the link. These pairs are ordered by the first component and then the second, so (2, 1) comes before (2, 2) because 2 = 2 and 1 < 2.

The shadow bound accepts a list only when its length is at most 2, its new-form arity sum is at most 2, and it contains no rule item. The mark and the link meet that bound. The list [form 1, rule 0] has length 2 and contains a rule item, so it falls outside the bound. The list [form 1, inst [0], inst [1]] has length 3, so it falls outside the length bound 2.

## What is proved

The four-row read table and its count of 1, the lengths and arities of the copied mark and link, the mu1 tie at 2, the mu2 pairs (2, 1) and (2, 2) and their order, and the bound membership of those two lists, of the rule list, and of the three-item list.

## What is assumed

The mark and the link are the item shapes written at `deltaU0` and `deltaBL` in `lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`. The shadow does not apply either list to a regime. The uniform-rule flag and the two demand kinds are data of this shadow, not a reading of a sealed regime.

## What is open

The sealed responder in the second derivation's packages, including a minimum, a cost, or a tie of that responder (S-3), a refusal of a regime that holds a uniform rule (S-1), a reading of a same pair that is separable (S-2), and any identification of the length bound 2 with the grammar (S-4). Attempt one's G-4 and attempt two's H-1 stay open. The node status stays OPEN.
