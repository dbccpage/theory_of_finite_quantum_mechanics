# Reviewed target restoration and cleanup

AuthorityEffect: None. Date: 26 October 2026.

The human selected “Keep restoration; remove new enforcement” for PR427.
The four validator/synchronizer/test files are restored byte-for-byte to their
pre-existing main versions. No new rejection rule or development gate remains;
all pre-existing checks and tests are retained.

The 77 changed targets retain their statuses: 35 OPEN, 13 CONDITIONAL and
29 IMPORTED_ASSUMPTION. Seventy-five are literal historical restorations; two
are explicit claim corrections. The initial 43 fragment-owner recoveries are
traced in the [provenance record](../../dag/research/qm427_historical_target_provenance_final_20261026.json);
the additional 14 have separate historical provenance. These targets do not
all originate from a node-level prior_statement field.

The Minkowski statement now requires two nonzero inputs, while its literal
historical prior remains unchanged. C8 no longer claims that M0 is not minimal;
minimality is not claimed. The optional README-generator change is omitted,
leaving that generator byte-identical to the baseline too.

The L1 sector-weight decision now explicitly names the original declared-mass
target. Its overwritten prior_statement metadata is corrected to that original
text. The later unweighted n-cycle theorem and its weighted/sum-of-squares
limitations remain in the existing narrowest_claim and caveat fields. No status,
research status is promoted.

The finite proof sources and retained campaign receipts remain unchanged.
Current Lean citations are restored without presenting finite witnesses as
proofs of their wider targets. H016 cites its actual qualified declarations,
not an imported alias. The U1 citation similarly names the actual declaration;
the old retained receipt's unresolved alias is not silently rewritten. Existing
source-bound build and axiom records support the corrected current citation;
this is not a fresh kernel replay.
The full finite-group Pachner statement remains PROVED_LEAN and is not replaced
by an open historical target. No new Lean/native replay is asserted.

The cleanup removes one root model-generated report and 16 raw transcript files
from the current tree. It is not a newly created archive. Exact Git recovery
objects and retained request/answer/receipt and successful Lean snapshot custody
are recorded in the [deletion disposition](../../dag/research/qm427_deletion_custody_disposition_20261026.json).
Do not prune that history or claim shallow/current-tree-only raw custody.

Existing owners regenerate the active DAG, views and current metadata digest
observations. Historical proof receipts and source snapshots are not rewritten.
Both integration lineages' eight additional current-metadata observations are
retained, together with the prior history and final current-file rebindings.
Six of those eight recorded intermediate digests match retained authored Git
snapshots. Two remain author-recorded intermediate observations without a
matching blob in those snapshots; they are not independently replayed evidence.

The existing receipt/validator tests pass (17), as do all five README tests.
An expanded 30-test run exposed two pre-existing PFP assertion failures and
a README-generation race; the README tests passed after generation completed.
The two PFP failures have identical failing inputs on main at 24afb82a6c84:
the Minkowski review is stored in research rather than a node review folder,
and the custody node has an existing next-test/does-not-support mismatch.
They are reported, not waived or presented as passing. No test was weakened.

This review does not close the original broad research targets, establish a
repository grade, or resolve native-workspace/publication blockers.
