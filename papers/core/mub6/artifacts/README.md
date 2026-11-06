# Artifacts

This folder holds the 13 artifacts that exist only for this program:
`manifest.json` and the 12 `mub_target_*_receipt.json` files that the
`mub_verify` Python harness produces.

All other artifacts this program cites live in
`omega_engine/crates_rs/tests/omega_mub/artifacts/`, under the same names. They
include the `dita_seed_F6*` covers, the `kernel_reflection*` box covers,
`grand_unified_mub6_verification_receipt.json`, and the `mub_*` cover and
certificate files. The 232 byte-identical copies that used to sit here were
removed when `omega_mub6/` was dissolved.
When a document here cites `artifacts/<name>` for one of those, read it as
`omega_engine/crates_rs/tests/omega_mub/artifacts/<name>`.

The notes that used to sit at the repository root `knowledge/` are in
[`knowledge/`](knowledge/).
