Status: AI-drafted, awaiting human review.

# GP-IMPORT-CPTP-CLASS, finite Boolean slice

## Setup

The labels are false and true. Collapse sends every label to false. A two-sided inverse of a map f is a map inv such that inv(f(q)) = q and f(inv(q)) = q for both labels.

The integer mass image of weights wF and wT is the pair (wF + wT, 0).

An ancilla label is prepared at false. A label pair is (system, ancilla). A reversible dilation is a pair of maps on label pairs that are mutual inverses, and whose system coordinate on each prepared pair (q, false) equals collapse(q).

For Boolean swaps sP and sU, the forward map is

- (false, false) maps to (false, sP)
- (true, false) maps to (false, not sP)
- (false, true) maps to (true, sU)
- (true, true) maps to (true, not sU)

The matching inverse reads the system coordinate as the ancilla of the output and undoes the swap on that fiber.

## Collapse

collapse(false) = false and collapse(true) = false, so the two labels have one image. If inv were a two-sided inverse, then inv(false) would equal both false and true. So no such inv exists.

## Mass image

The first coordinate is wF + wT and the second is 0, so the coordinates sum to wF + wT. If both weights are nonnegative, the sum is nonnegative and the second coordinate is 0, which is nonnegative. At weights 2 and 3 the image is (5, 0).

## Four dilations

There are four swap pairs. Direct evaluation shows that each forward map and its inverse compose to the identity in both orders, and that each forward map sends a prepared pair to system label false. The four forward maps are pairwise distinct: the pairs (false, false) and (false, true) separate them.

Any reversible dilation is injective, because it has a left inverse. On the prepared ancilla, both system labels are sent to system coordinate false, and those two outputs differ in the ancilla coordinate. So the prepared images are exactly the two pairs whose system coordinate is false. An unprepared input cannot land in that fiber, so both unprepared inputs have system coordinate true, and their ancilla coordinates differ. Those two bits are a swap pair, and the forward map equals the named map of that pair. Hence every reversible dilation agrees with one of the four named maps at every label pair.

## What is proved

The Boolean collapse identities, the absence of a two-sided inverse, the integer mass image and its sum and nonnegativity, the witness (5, 0), the ancilla value false, the four pairwise distinct named dilations, and the agreement of every reversible dilation with one of those four maps.

## What is assumed

The labels are the two Boolean values. The ancilla starts at false. The mass coordinates are integers. Mutual inverse and the collapse reduction are the definition of a reversible dilation used above.

## What is open

A Hilbert-space class of completely positive trace-preserving maps, a Choi matrix, a Kraus form, and a Stinespring realization of that class remain imported. The integer mass image is a population shadow, not that class.
