Status: AI-drafted, awaiting human review.

# AUTH-DTM2-INPUT-REQUEST-PLANNED

Node status stays OPEN. This note records one closed request list. It does not run an evaluator, and it does not read the list as authorization.

## The closed request

The header tag is 1. The fuel token is 2. The machine-code length is 1. The machine segment is the one-entry list 7. The input word is the list 3, 4.

Writing the header, the fuel, the length, the segment and the input word in that order yields the list 1, 2, 1, 7, 3, 4. That list has length 6.

The list 0, 2, 1, 7, 3, 4 begins with 0. The number 0 differs from the header tag 1.

## What is proved

The five field identities, the concatenated list, its length 6, the leading 0, and the difference between 0 and the header tag.

## What is assumed

The four fields are these numbers and lists. Concatenation is list append. A missing header, on this one list, is a leading 0. AuthorityEffect is None. No package is imported.

## What is open

An encoder and decoder for a request other than this closed list stay open. The remaining named targets in the update packet stay open, including result-level agreement with a bounded evaluator. Configuration snapshots and step-by-step trace agreement stay open. No custody reading and no authorization reading are in this note.
