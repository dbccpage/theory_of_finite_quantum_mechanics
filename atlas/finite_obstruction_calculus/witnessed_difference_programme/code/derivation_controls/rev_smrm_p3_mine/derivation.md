# REV-SMRM-P3-MINE

## Target
Implement **Rejection-Ledger Guard Mining & Trace Verification** (`REV-SMRM-P3-MINE`, unblocking 3 downstream nodes in `goal_dag.jsonl`). Using `rejection_reuse.core` and `rejection_reuse.trace_checker`, failed candidates are mined into reusable guards (`ledger`), parent-packet digests (`packet_digest`) are verified against bundle provenance (`bundle_matches`), and full traces are audited via `check_trace`, mapped onto `omega_engine_epistemic_immune_system`.

## Mathematical Formulation

Let $U$ be a finite universe of candidate transitions $x = (a, b, c) \in \{0, 1, 2\}^3$ with validity predicate $\mathrm{valid}(x)$.
1. **Rejection Witness Mining (`ledger`)**: Every invalid candidate $x \notin \mathrm{Valid}(U)$ encountered along a search trace is mined into a guard witness $g = \mathrm{decode}(x)$ that rejects all candidates sharing the failing feature projection ($\mathrm{rejects}(g, y) = \mathrm{True}$ while $\forall v \in \mathrm{Valid}(U),\; \mathrm{rejects}(g, v) = \mathrm{False}$).
2. **Packet Provenance Binding (`bundle_matches`)**: Each guard bundle carries the SHA-256 digest of its parent packet (`packet_digest(parent_packet())`); any mismatch in parent digest invalidates transfer.
3. **Trace Audit (`check_trace`)**: `check_trace(ledger())` verifies that every mined guard is sound (zero false positives on valid candidates), complete on the encountered failure class, and monotonically reduces repeated failure evaluations.

## Verification Summary
- `check_trace(ledger())` passes all trace invariants.
- `bundle_matches` accepts the canonical parent packet and rejects any mutated parent packet.
