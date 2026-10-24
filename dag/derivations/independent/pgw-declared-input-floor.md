Status: AI-drafted, awaiting human review.

# PGW-DECLARED-INPUT-FLOOR

Node status stays OPEN. This note records one declared bound record. It does not establish a floor for the declared-input count.

## Declared numerals

The node names these bounds, and the narrowed record uses them as constants:

- round count: 15
- node guard: 250
- data ceiling: 4
- item bound: 2
- input count: 2
- engine count: 4
- reading count: 2

## Comparisons

The input count is the same number as the item bound: 2 = 2.

One is strictly below the input count: 1 < 2.

The round count is strictly below the guard: 15 < 250.

The engine count is not the reading count: 4 ≠ 2.

The candidate data counts are 0, 1, 2, 3, and 4. Those strictly below the ceiling 4 are 0, 1, 2, and 3. That list has length 4. The ceiling is not strictly below itself, since 4 < 4 is false.

## What is proved

The eight comparisons above, for these seven declared numerals and this five-element candidate list.

## What is assumed

The numerals are the bounds named by the node text. No engine was run. No grammar was carried forward. AuthorityEffect is None.

## What is open

A floor for the declared-input count stays open. A reduction below two that holds past attempt two's bounds stays open. Whether four engines carry the grammar forward past the bounds stays open (H-1, SD-R-11). The other reading of the completion gate stays NOT_ESTABLISHED.
