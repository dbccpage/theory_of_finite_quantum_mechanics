# DEC-WDP-REPIN: Owner decides whether to repin the sealed WDP release

**AuthorityEffect:** None.

## Scope

Finite release-repin decision and manifest-tieout control: verifies that MANIFEST.sha256 and SHA256SUMS match current source digests under explicit owner-authorized release verification.

- Python witness: `witness_dec_wdp_repin` in `witness.py`
- Rust witness test: `test_dec_wdp_repin_scoped_control` in `omega_engine/crates_rs/tests/omega_wdp/derivation_controls/dec_wdp_repin.rs`
