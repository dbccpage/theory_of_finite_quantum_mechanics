Status: AI-drafted, awaiting human review.

# COMP-C2-STEP3-NOT-WORD-STEP concrete word steps

The node stays OPEN. This note records three list moves and one non-injective map. It does not encode every Genesis Step3 state.

## One-hole replacement

A hole rule is a pair of lists `(lhs, rhs)`. It applies to a word when the word splits as `left ++ lhs ++ right`, and the result is `left ++ rhs ++ right`.

## Three moves

- `left = [0]`, `lhs = []`, `right = []`, `rhs = [1]` sends `[0]` to `[0, 1]`.
- `left = [0, 1]`, `lhs = []`, `right = []`, `rhs = [0, 1]` sends `[0, 1]` to `[0, 1, 0, 1]`.
- `left = [0]`, `lhs = [1]`, `right = []`, `rhs = []` sends `[0, 1]` to `[0]`.

## The merge map

`merge01` sends `1` to `0` and sends every other natural number to itself. Then `merge01 0 = 0` and `merge01 1 = 0`, while `0` and `1` are distinct.

## What is proved

- The three list moves above are one-hole replacements.
- `merge01` sends both `0` and `1` to `0`.

The Lean declarations are `addTermWordStep`, `addAssertionWordStep`, `identifyWordStep`, `merge01SendsBothToZero`, and `merge01FixesOther` in `lean4/CampaignCompC2Step3NotWordStep.lean`. `merge01FixesOther` states that a natural number other than 1 is fixed.

## What is assumed

List concatenation in the Lean kernel. No new axiom is declared. The node status stays OPEN.

## What is open

An encoding of every Genesis Step3 state, with a finite term set, a finite assertion set and two named terms, under which add-term, add-assertion and identify are word steps, is not given here. A demonstration that no such encoding exists is not given here.
