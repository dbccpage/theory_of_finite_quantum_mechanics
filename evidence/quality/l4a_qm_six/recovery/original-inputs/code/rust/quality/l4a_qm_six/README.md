# Six-Directory QM & Math Quality Review (`l4a_qm_six`)

`AuthorityEffect: None`

Offline, source-pinned `SCORING.md` v2.0.0 evaluation, AST complexity measurement, designated semantic mutation testing, and `<filename>.scoring.yaml` / `<filename>.contract.yaml` sidecar generation across:

- `code/rust/src/majorana` (21 subjects)
- `code/rust/src/mub` (284 subjects)
- `code/rust/src/number_theory` (39 subjects)
- `code/rust/src/operad_theory` (36 subjects)
- `code/rust/src/sheaf_theory` (24 subjects)
- `code/rust/src/qm` (133 subjects)

## Commands

1. Run offline baseline tests and calibrated `syn 3.0.9` source AST complexity metrics:
   ```powershell
   python code/rust/quality/l4a_qm_six/replay.py --metrics
   ```
2. Run designated semantic mutations across the 6 directories:
   ```powershell
   python code/rust/quality/l4a_qm_six/mutations.py
   ```
3. Generate and verify all 1,074 `.scoring.yaml` and `.contract.yaml` sidecars:
   ```powershell
   python code/rust/quality/l4a_qm_six/records.py --receipt <evidence_dir>/receipt.json --mutations <mutations_dir>/mutation_receipt.json
   python code/rust/quality/l4a_qm_six/records.py --check --receipt <evidence_dir>/receipt.json --mutations <mutations_dir>/mutation_receipt.json
   ```
4. Validate all sidecars against the canonical Draft 2020-12 JSON Schema in `SCORING.md`:
   ```powershell
   pwsh -NoProfile -File code/rust/quality/l4a_qm_six/validate.ps1 -ReceiptDirectory <evidence_dir>
   ```
5. Summarize review state:
   ```powershell
   python code/rust/quality/l4a_qm_six/summarize.py --receipt <evidence_dir>/receipt.json
   ```
