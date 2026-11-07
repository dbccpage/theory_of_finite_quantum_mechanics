# dag/

AuthorityEffect: None.

This folder is the derivation graph from `<>` to finite quantum mechanics. It holds the graph, the notes that derive each step, and the tools that keep the two consistent. Evidence (replay receipts, reviews, run results) lives in [`../evidence/`](../evidence/); papers live in [`../papers/`](../papers/); Lean lives in [`../lean4/`](../lean4/).

## What is here

| Path | What it is | Edit? |
|---|---|---|
| `derivation_dag.json` | The single source: nodes, routes, TFQ records, index text | yes, or through a fragment |
| `fragments/*.json` | Slices owned by one sync tool each | yes |
| `derivations/NN_stage/` | One numbered folder per stage: `tfq_*.md` record pages, stage notes, `sources/` | yes (pages a sync owns are rewritten by it) |
| `theory_of_finite_qm.jsonl`, `theory_of_finite_qm.md` | Generated views of `derivation_dag.json` | no |
| `prose_proofs.md` | Generated index from `PROVED_LEAN` nodes to prose proofs | no |
| `evidence/evidence_map.json` | Generated map from each node to its evidence, with grades | no |
| `validate_derivation_dag.py` | The validator | |
| `tools/` | Sync, render and index tools | |
| `tests/` | Tests of the graph and the tools | |

Statuses are the graph's own; the legend is `status_legend` in `derivation_dag.json`. The full layout, ownership rules and segment notes are in [`derivation_dag_reading_note.md`](derivation_dag_reading_note.md).

## Check

```bash
python -I -X utf8 dag/validate_derivation_dag.py --repo-root .   # graph and every cited path
python -I -X utf8 dag/validate_derivation_dag.py --no-files      # graph only
python -X utf8 -m pytest -q dag/tests dag/evidence/test_evidence.py
```

## Change

1. Edit `derivation_dag.json` or the fragment that owns the slice.
2. Run the syncs in this order, each with no flag: `dag/tools/sync_pfp_results.py`, `sync_unified_dag.py`, `sync_application_branches.py`, `sync_pregenesis_to_wdp.py`, `sync_frontier_branches.py`, `sync_genesis_to_higher.py`, `sync_foc035_observer_presheaf.py`. Each calls `dag/tools/render_dag_views.py`.
3. Regenerate the evidence map: `python -X utf8 dag/evidence/build_evidence.py --write`.
4. Run the checks above.

A status records the evidence behind a node; that evidence lives outside this folder (a Lean declaration in `lean4/` with a replay receipt in `evidence/lean_receipts/`, or a checked computation).

Names are lowercase; only README files use capitals.
