# Changes Summary — Milestone 1 (Reconciliation)

## 1. Claim Hygiene Token Remediation (TFQ-0293)
- **Monograph**: `dag/derivations/08_l1_to_l2/tfq_0293_complex_field_as_a_declared_carrier.md`
  - Line 73: Replaced `"impossible in Z"` with `"has no integer solution in Z"`.
- **Snapshots**:
  - `dag/results/custody/20261019T174819Z_filename_repair/snapshots/after/dag/derivations/08_l1_to_l2/tfq_0293_complex_field_as_a_declared_carrier.md`
  - `dag/results/custody/20261019T174819Z_filename_repair/snapshots/before/dag/derivations/08_l1_to_l2/TFQ-0293_complex_field_as_a_declared_carrier.md`
- **PFP Filename Custody Ledger**:
  - `dag/pfp/filename_custody.json`: Updated `historical_sha256`, `historical_git_blob`, `current_sha256`, `current_git_blob` for `dag/derivations/08_l1_to_l2/tfq_0293_complex_field_as_a_declared_carrier.md`.
- **Operads**:
  - `dag/operads/gp_import_complex_field.yaml`: Updated `paper_source_pins` SHA256 to new hash `a6dd14b6214309a96f1b4c483a903c73449339e0839e5590928a6f44d8b941b6`.
  - `dag/operads/l1_imp_complex_field.yaml`: Updated `paper_source_pins` SHA256 to new hash `a6dd14b6214309a96f1b4c483a903c73449339e0839e5590928a6f44d8b941b6`.

## 2. Master Derivation Ledger Rebinding (`dag/theory_of_finite_qm.jsonl`)
- Rebound all 397 records (`TFQ-0000` through `TFQ-0396`):
  - Rewrote legacy `omega_engine_atlas/...` citations to local Python repository paths under `code/python/src/...` or prefixed with `absent: no local python twin located for ...` where no local module exists.
  - Rewrote legacy `omega_engine/crates_rs/...` citations to local Rust repository paths under `code/rust/src/...` or prefixed with `absent: no local rust twin located for ...` where no local module exists.
  - Rewrote legacy `lean4/quantum_mechanics/...` citations to local flat paths under `lean4/*.lean` or prefixed with `absent: ...` where no local Lean 4 declaration exists.
  - Retained all `external:` and `pr:` citations verbatim.
  - Maintained all 397 version 5 UUIDs without modification.
  - Maintained exact 17 sorted keys per record.
  - Maintained tree structure: `TFQ-0000` `parent_id = null`, all other 396 records point to valid existing parent.
  - Preserved strict status discipline: unearned derivations remain `GAP` or `OPEN_OBLIGATION`; computational controls remain `COMPUTATIONAL_CONTROL` or `SOURCE_RECORD`.
  - Zero forbidden Claim Hygiene tokens.

## 3. Master Monograph & README Synchronization
- Verified 1-to-1 parity between `dag/theory_of_finite_qm.md` and `dag/theory_of_finite_qm.jsonl`:
  - 397/397 node IDs match.
  - 397/397 UUIDs match.
  - 397/397 Statuses match.
  - 397/397 Parents match.
  - 397/397 Obligations match.
- Verified 1-to-1 parity between `dag/derivations/README.md` and `dag/theory_of_finite_qm.jsonl`:
  - 397/397 IDs, names, statuses, and parents match.

## 4. Individual Monograph Synchronization (`dag/derivations/*/*.md`)
- **Custody Monographs (144 files)**:
  - Preserved Section 6 in its entirety across all 144 files.
  - Retained exact cryptographic source pin bytes required by PFP prompt custody (`test_custody.py`).
- **Non-Custody Monographs (253 files)**:
  - Rebound `## 3. Multi-Tier Code & Proof Witnesses` in all 253 monographs:
    - Updated Lean 4 links to `../../lean4/` or active formalization placeholder.
    - Updated Rust links to `../../code/rust/src/` or sovereign certifier placeholder.
    - Updated Python links to `../../code/python/` matching rebound JSONL master ledger.
  - Preserved Sections 1, 2, 4, 5 in all monographs.
  - Zero forbidden Claim Hygiene tokens across all 397 files.
