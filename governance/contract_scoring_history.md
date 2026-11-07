# One contract and scoring history per artifact

The adjacent metadata file for `agent_functor.rs` is now
`agent_functor.contract.score.yaml`. Rust and Python sources, tests, manifests,
registry contracts and historical evidence use the same combined document
format. Standalone registry contracts have `artifact: null`; the migration does
not invent an implementation or a score for them.

Each document contains:

- `artifact`: the associated source path, when a sibling source exists.
- `contract`: the current contract's readable projection.
- `contract_history` and `scoring_history`: every imported or appended version,
  its parsed record, exact original UTF-8 text, byte length and SHA-256.
- `current_contract` and `current_scoring`: version identifiers. These select
  a view; they do not establish a grade or invent an assessment date.
- `legacy_paths`: old receipt addresses mapped to their stored versions.

The current scoring view prefers the explicit source `.scoring.yaml` input over
the older `.score.yaml` input. All conflicting versions remain visible. Known
archived assessments whose `artifact.path` names an existing live source are
also included in that live source's history without replacing its current view.
Import/append order is not claimed to be chronological assessment order.

The migration index is [index.json](../evidence/contract_score_migration/index.json).
It maps every removed name to its combined file and original hash. Historical
receipts, their hashes, contract URNs and embedded Python contract twins are not
rewritten. Original bytes can be checked or recovered without recreating old
sidecar files:

```powershell
python scripts/contract_scores.py check
python scripts/contract_scores.py hash code/rust/src/category_theory/agent_functor.score.yaml
python scripts/contract_scores.py read code/rust/src/category_theory/agent_functor.score.yaml --sha256 ORIGINAL_SHA256
```

Use `scripts.contract_scores.load` to read a combined document. The existing
quality tools opt into `RecordPath`, a scoped adapter that resolves historical
receipt addresses and appends new versions to the combined file. It never
creates `.contract.yaml`, `.scoring.yaml` or `.score.yaml` companions. This
adapter does not replace `pathlib` globally. New code should use the combined
document directly. Old scripts outside this repository require the resolver
or an explicit export of the original bytes; old filesystem paths no longer
exist.

The migration runs complete input preflight and verifies exact reconstruction
of every original before deleting any legacy file. Re-running it preserves
existing history. It changes storage, not the validity of the mathematics,
evidence, contracts, source custody judgements or grades. Existing withdrawn,
failed and incomplete assessments keep those statuses.
