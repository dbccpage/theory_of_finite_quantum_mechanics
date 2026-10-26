Status: AI-drafted, awaiting human review.

# FQ-GAP-C500-ORIGINAL-TARGETS

AuthorityEffect: None.

The gap register names ten C500 blocks. Each block lists 25 unresolved target ids, and those ids form one consecutive numeral run. This note records that arithmetic and the lengths of the clause lists written beside the blocks. It does not reopen an evidence file and it does not discharge an original target contract.

## Target runs

For a natural number `k`, write

```
lo(k) = 276 + 25 * k
hi(k) = 300 + 25 * k
```

Then

```
hi(k) - lo(k) + 1 = 25
hi(k) + 1 = lo(k + 1)
```

The second identity says the next run starts at the next numeral. The ten values `k = 1` through `k = 10` give

```
lo(1) = 301
hi(10) = 550
hi(10) - lo(1) + 1 = 250
10 * 25 = 250
```

So the ten runs are the 250 numerals from 301 through 550.

## Clause-list lengths

The ten clause lists have lengths

```
0, 2, 4, 2, 4, 1, 1, 1, 1, 5
```

Their sum is 21. The last length is 5, and 5 is strictly greater than each of the nine earlier lengths. The five labels in that last list are M2, M5, M7, J1 and J2, and those five names are pairwise distinct.

## What is proved

- For every natural number `k`, `hi(k) - lo(k) + 1 = 25` and `hi(k) + 1 = lo(k + 1)`.
- `lo(1) = 301`, `hi(10) = 550`, the cover has 250 numerals, and `10 * 25 = 250`.
- The ten clause-list lengths sum to 21, and the last length 5 is strictly greater than each earlier length.
- The five labels M2, M5, M7, J1 and J2 are pairwise distinct.

## What is assumed

Nothing beyond natural-number arithmetic and the ten lengths and five labels copied from the gap-register names. The copy is an input to the count. This note does not assume that an evidence file still matches those names.

## What is open

A fresh reading of each original target contract, the evidence files named beside the ten blocks, and any claim that a scoped receipt discharges a block. The gap-register titles say the original contracts remain open. These counts of register names do not discharge a block. Status stays OPEN.
