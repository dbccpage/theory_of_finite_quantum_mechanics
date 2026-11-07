# lean4/: the Lake package of the theory

**AuthorityEffect: None.** A module here is evidence for a DAG node only through a replay receipt under
`evidence/lean_receipts/`; this page describes the folder, it certifies nothing.

Toolchain: `lean-toolchain` pins Lean v4.35.0; `lake-manifest.json` pins Mathlib at the same release.
`lakefile.lean` declares 195 `lean_lib` targets over the modules of this folder; the nine targets that CI builds
are listed in `.github/workflows/lean-gleason.yml`.

What the folder holds:

- Flat PascalCase modules (`*.lean`) with a `.contract.score.yaml` companion beside each one. Every `.lean` file
  under `lean4/` is a governed source (`governance/policy.json`, population `lean4/**/*.lean`); the companion
  regime and the grandfather list are described in `governance/README.md`.
- Two namespace folders, `AuthIncompleteness/` and `FQCD/`, with modules of the same kind.
- `Imported/`: modules taken from the paper deposits under `atlas/` with their import lines rewritten into the
  `Imported` namespace. `Imported/import_manifest.json` and `Imported/import_manifest_programmes.json` record
  each module's original sha256 and its sha256 at import.
- `RENAMES.json`: the ledger of module renames; the reasons in `governance/baseline.json` cite it.
- `provenance.md`: the provenance and axiom census of `MajoranaCore.lean`, with `test_majorana_boundary.py` and
  `majorana_claim_oracle.py`, the mutation harness that reads that module beside it.
- Sixteen `qm_*.md` files: Lean text saved as Markdown. They are reading guides that the derivation prose under
  `dag/derivations/10_finite_qm_core/sources/` names; no Lake target builds them and no replay covers them. Read
  them as plain text.
- `.gitattributes`: seals the bytes of the `Prompt*Scope` modules.

How the folder is checked: `scripts/auto/anti_pattern_lint.py` refuses added Lean lines that carry `sorry`,
`admit`, `native_decide`, `unsafe` or an axiom declaration; `governance-check` and `scripts/contract_scores.py`
verify the companions; `scripts/replay_fqcd_lean.py --verify-receipt` and `scripts/replay_pr492_lean.py
--verify-receipts` verify the replay pins that the receipts hold on the lakefile and the sources.
