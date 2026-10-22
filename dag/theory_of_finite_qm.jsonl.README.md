# `theory_of_finite_qm.jsonl` and `theory_of_finite_qm.md` are generated views

**AuthorityEffect:** None.

Do not edit `theory_of_finite_qm.jsonl` or `theory_of_finite_qm.md` by hand. Both are read-only views of
`derivation_dag.json` (schema `derivation_dag.v2`), which is the single source of the derivation graph: its
top-level key `records` holds every TFQ record, and `index_document` holds the hand-authored text of the
Markdown index. `render_dag_views.py` renders both views:

- the JSONL view has one line per record, in the order of `records`, each the record as JSON with sorted keys
  and non-ASCII characters kept, ended by CRLF;
- the Markdown view is the index: header, stage index, Coda atlas packages, record-to-node crosswalk and one
  section per stage.

To change a record, edit `derivation_dag.json` (or the fragment whose sync owns the record) and run the sync
cycle, which ends by rendering the views:

```
python -I -X utf8 dag/sync_pfp_results.py
python -I -X utf8 dag/sync_unified_dag.py
python -I -X utf8 dag/sync_application_branches.py
python -I -X utf8 dag/sync_pregenesis_to_wdp.py
python -I -X utf8 dag/sync_frontier_branches.py
python -I -X utf8 dag/render_dag_views.py --check
```

This note sits beside the views because a banner inside them would change their bytes; the views are kept
byte-identical to the files the earlier pipeline wrote. `validate_derivation_dag.py` fails when a view on disk
differs from the renderer. See `derivation_dag_reading_note.md`.
