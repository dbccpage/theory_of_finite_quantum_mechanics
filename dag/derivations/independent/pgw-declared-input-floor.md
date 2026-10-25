Status: AI-drafted, awaiting human review.

# PGW-DECLARED-INPUT-FLOOR, four stake-only carriers

The node statement says the declared-input count stays two, and that attempt two found four engines declaring the stake and not the stream. This note checks one finite family. It does not replay that search.

## Names and count

The vocabulary is the list stake, stream. Its length is 2, and the two names differ.

A carrier declares each name or not. Its count is 1 for each declared name. Declaring both names has count 2. Declaring only the stake has count 1. Declaring neither has count 0.

## Four carriers

The family has four pairs. Each pair is (declares stake, declares stream) = (true, false). Each count is 1. The length of the family is 4. The count 1 is strictly below the count 2 of declaring both names.

## Two readings on this family

The floor reading says every carrier in the family has count at least 2. That reading is false: each count is 1.

The one-input reading says some carrier in the family has count 1. That reading is true.

The two readings disagree on this family. The author's freeze ruling is not restated.

## Numerals and the empty carrier

The recorded numerals are 15 rounds, a node guard of 250, a data bound of 4, and an item bound of 2. They are numerals in this note. They are not the output of a search.

A carrier that declares neither name has count 0, which is below 1. None of the four pairs is that carrier.

## What is proved

On this vocabulary and this family of four, each carrier declares the stake and not the stream, each count is 1, and 1 is below 2. The floor reading on the family is false. The one-input reading is true. The empty carrier has count 0 and is not in the family. The numerals are 15, 250, 4, and 2.

## What is assumed

The count is the sum of two bits. The four carriers are the four pairs written above. The numerals are definitions. AuthorityEffect is None.

## What is open

A floor for every carrier is open. A reduction below two that holds past this family is open. The attempt-two search, including whether four engines carry forward past the bounds, is not replayed. The external `carries_forward` procedure is not rechecked. The node stays OPEN.
