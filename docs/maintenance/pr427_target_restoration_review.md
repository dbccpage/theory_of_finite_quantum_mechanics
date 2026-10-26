# Reviewed target restoration and cleanup

AuthorityEffect: None. Date: 26 October 2026.

The human selected “Keep restoration; remove new enforcement” for PR427.
The three validator/synchronizer/test files are restored byte-for-byte to their
pre-existing main versions. No new rejection rule or development gate remains;
all pre-existing checks and tests are retained.

The 63 research targets retain their statuses: 33 OPEN, 10 CONDITIONAL and
20 IMPORTED_ASSUMPTION. Twenty use retained node-level prior targets, including
the repaired weighted-sector target; 43 are traced to exact historical fragment
owners in the [provenance record](../../dag/research/qm427_historical_target_provenance_final_20261026.json).
They do not all originate from a node-level prior_statement field.

The L1 sector-weight decision now explicitly names the original declared-mass
target. Its overwritten prior_statement metadata is corrected to that original
text. The later unweighted n-cycle theorem and its weighted/sum-of-squares
limitations remain in the existing narrowest_claim and caveat fields. No status,
proof anchor or bottleneck is promoted.

The finite proof sources and retained campaign receipts remain unchanged.
The full finite-group Pachner statement remains PROVED_LEAN and is not replaced
by an open historical target. No new Lean/native replay is asserted.

The cleanup removes one root model-generated report and 16 raw transcript files
from the current tree. It is not a newly created archive. Exact Git recovery
objects and retained request/answer/receipt and successful Lean snapshot custody
are recorded in the [deletion disposition](../../dag/research/qm427_deletion_custody_disposition_20261026.json).
Do not prune that history or claim shallow/current-tree-only raw custody.

Existing owners regenerate the active DAG, views and current metadata digest
observations. Historical proof receipts and source snapshots are not rewritten.
This review does not close the original broad research targets, establish a
repository grade, or resolve native-workspace/publication blockers.
