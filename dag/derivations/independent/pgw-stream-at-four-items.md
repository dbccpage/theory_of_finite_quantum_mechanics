Status: AI-drafted, awaiting human review.

# PGW-STREAM-AT-FOUR-ITEMS

Node status stays OPEN. This note records one refusal pair and one search flag. It does not compute a stream tree.

## Refusal

A reply carries an item count and a refusal bit. It refuses at k when the item count is k and the bit is set.

The reply with item count 3 and the bit set refuses at 3. The same reply does not refuse at 4, because the item count is not 4.

A reply with item count 4 and the bit set refuses at 4. A reply with item count 4 and the bit clear does not refuse at 4. The three-item refusal does not choose between those two replies.

## Search

The short-circuit flag searches a target only when the target is at or before the refusal count. After a refusal at 3, a target at 4 is not searched, and the target at 3 is searched. With the flag clear, the target at 4 is searched.

## What is proved

The two readings of the three-item reply, the two replies at four items, and the three search facts.

## What is assumed

Refusal is equality of the item count together with the refusal bit. Search under the short-circuit flag is the numerical comparison above. No stream program was executed. AuthorityEffect is None.

## What is open

The retained minima are not proved. The refusal census stays open. The guard-stopped frontier stays open. The four-item stream computation stays open.
