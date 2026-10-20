# CC-26 through CC-30: proof manuscript review

AuthorityEffect: None.

The [submission](submission/original.txt) is preserved byte for byte. The main proofs survive with explicit repairs; the manuscript is not accepted verbatim. See the [review](review.md), [corrected statements and proof bridges](corrected_statements.md), [operation records](operad_delta.json), and [status](lemma_status.json).

Independent [exact checks](verification/exact_checks.py) passed 61 controls and rejected 4 invalid inputs in both [normal](verification/normal.json) and [optimized](verification/optimized.json) Python. These are finite controls, not general Lean certificates. General arguments are written separately. All 515 files in the twelve prior manifests were reverified; old evidence was not overwritten.

Repairs concern Q versus Q(i), normalization-query minimality, cancellation in the kernel obstruction, a missing negative diagonal term, category identities, coefficient restrictions on mixtures, CP versus CPTP adjoints, and the rational equal-Gram argument needed for Kraus mixing. The accompanying claim of 67 checks is not reproduced by the only earlier supplied script, which printed 66 PASS lines; no revised companion script was supplied with this manuscript.

[Small next targets](next_targets.md) are available for hand proof or Lean transcription. No provider calls, live Rust/Python/Lean implementation changes, Git publication, or merge were performed. Stop for review.
