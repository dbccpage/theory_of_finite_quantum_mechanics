Status: AI-drafted, awaiting human review.

# PGW-DRIVER-B-SEVENTH-EVENT

Node status stays OPEN. This note records one six-label model. It does not run the Alpha harness.

## Labels

The six names Supply, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll and Impose are given the indices 0, 1, 2, 3, 4 and 5. Each index returns the name that produced it, and each name returns the index that produced it. None of those indices equals 6.

## Guard

The sealed guard accepts a natural number exactly when the number is strictly less than 6. It accepts 0, 1, 2, 3, 4 and 5, and it refuses 6. The amended guard accepts a natural number exactly when the number is strictly less than 7, so it accepts 6. The refusal of 6 is the choice of bound. It is not a proof that six labels are enough for every lift.

## What is proved

The six indices, both round trips, the sealed guard on those indices and on 6, and the amended guard on 6.

## What is assumed

The six names and the two bounds are the definitions above. No harness was executed. AuthorityEffect is None.

## What is open

The Alpha harness, a seventh sealed constructor, SeventhEventError, a seal amendment, and a theorem that every lift factors through the six kinds stay open.
