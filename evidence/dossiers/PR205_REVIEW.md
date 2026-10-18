# PR #205 review and repair

AuthorityEffect: None.

Reviewed incoming head: `516e14b61f9c292d52f66ce1d9d07e4bd7ab033b`.
Integration base: `3f5d93597b195ab4b04c1ac4f9a187574b309d66`, after PRs #204 and #206.
The main integration preserved both sides of the three historical agent-note conflicts.
The foreign shared checkout and Gemini worktree were not altered or cleaned.

## Repairs

- The PSD gate now checks all 15 principal minors of a symmetric 4x4 matrix.
  The old leading-minor shortcut accepted diag(0,-1,0,0). Identity gluing is not a PSD repair.
- Cyclotomic constructors reject invalid conductor/basis degrees, and polynomial
  division rejects nonintegral quotients and remainders instead of truncating.
- Conductor divisibility is not field inclusion iff: zeta_6=1+zeta_3.
  Carrier labels and their LCM are not a proved minimal universal field. A
  normalized state is not a generator, projector, or parity-check matrix.
- The Tiles certificate constructs the rational 9x9 matrix, checks its projector
  and partial-transpose identities, and covers all 32 local rank assignments.
  Duplicate/zero vectors are rejected. This is a finite computation under the
  declared UPB-complement criterion, not a Lean UPB theorem.
- Cabello's negative eigenvector is computed. The Peres residual about 1/3,
  not the entire frame function, is orthogonal to the declared quadratic rows.
- Rust's six unconstructed higher triads were withdrawn; it checks four rational
  triads, while Python constructs ten. No higher-triad cross-language parity.
- Untested topology, density, rational-sphere colorability, p-adic and nonstandard
  assertions are unknown rather than constant true flags.
- H052-H057 documentation now matches their actual types. Divisibility labels,
  integer partitions, integer-labelled records, and 2x2 Int commutators are not
  respectively field colimits, dense-sphere topology, continuous Hamiltonians,
  or all-dimensional completion theorems.
- All seven sealed plaintext hashes survive. Historical predictions/resolutions
  are retained but all-HIT scoring is withdrawn. The 010 YAML refusal was stronger
  than its Lean result and is now OPEN (CONDITIONAL), like 004. Claude clause 5
  did not establish its predicted two refusals. Global terminal claims stay open.

## Local verification

- Python: 593 passed, zero skips, 8 workers; final coverage run 44.64 seconds.
- Coverage on all 27 non-test application Python files: 3,790/4,115 statements
  (92.10%); 1,200/1,418 branches (84.63%). The old 95%+ claim is withdrawn.
  This is not a new full-coverage or mutation-score claim.
- Rust: 112 unit + 12 integration tests passed; zero doc tests. No current
  clippy or formatting-clean claim is made.
- Lean: `lake build` exited 0, 124 jobs. Fresh application input hash
  `0d9b3936739a635d7e8240f2af74d1e31a8a5c5dbc9d71fb5b3610c162c54b5b`.
  1,034 unique emitted reports, 46 using Classical.choice (old count 35 was stale).
  This emitted inventory is not proof of declaration completeness. QM_122's
  two-axiom policy is not the whole application's policy; its existing exception
  remains recorded separately as GAP-FQM-020.
- `consolidate_sources.py --check`: zero drift.
- `replay_review_receipts.py --check`: two byte-identical generated receipts;
  negative tests reject missing and modified bytes. Legacy Band B/D/E JSON is
  preserved as explicitly historical narrative, not current proof receipts.
- The other Lean-project receipt entries remain historical and byte-bound,
  not newly claimed builds. The application replay alone was refreshed.

These are local witnesses. GitHub Actions is not claimed green or inferred from
metadata. The PR body records the final head and hosted status before merge.
Tests, hashes, and elaboration do not close the mathematical open clauses.
