# Change Log for the Fermi-Hubbard Sign Problem Package

AuthorityEffect: None.

## [0.1.0 review repair] - 2026-10-03

- Vendored the Hubbard evaluator into this package and pointed it at the local schema slice. The package no longer imports `code/sign_sql` at runtime.
- Corrected the mask 15721 down determinant and limited the 4-site ring row to the auxiliary-field census. Dense Fock replay in this evaluator admits at most three sites.
- Recorded the attractive-triangle particle number, the two-site expectations, and the open-chain gauge signs in the local tests.

## [0.1.0] - 2026-10-02

### Added
- Initial canonical deposit package for *Exact Relational Mechanics and Certified Sign Boundaries of the Fermi-Hubbard Model*.
- Programmatic interface `code/hubbard_exact_model.py` exposing occupation-basis and auxiliary-field evaluation routines.
- Relational schema `code/hubbard_schema.sql` defining SQLite tables, foreign key constraints, and determinant/observable views.
- Test suite `code/tests/test_hubbard_paper_reproducibility.py` validating 100% of mathematical assertions, symmetries, and negative witnesses reported in `paper.md`.
- Formal claim ledger `paper_claim_ledger.md` mapping claims `CLAIM-HUBBARD-001` through `CLAIM-HUBBARD-012` to automated test proofs.
- Deposit verification script `verify_deposit.py` enforcing fail-closed path safety, SHA-256 manifest reconciliation, and zero untracked leaks.
- Package metadata `README.md`, `zenodo_metadata.json`, `citation.cff`, `LICENSE` (CC-BY-4.0), and `LICENSE-CODE` (MIT).
