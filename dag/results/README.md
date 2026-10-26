# dag/results

One folder per DAG node. The tree keeps only what is cited:

- `<NODE-ID>/reviews/*/`: the review of the node. `dag/sync_pfp_results.py` reads these files and checks their sha256.
- `<NODE-ID>/runs/*/` and `batches/*/`: only those files that the DAG, a receipt in `dag/research/`, a test or a tool cites.
- `custody/`: the filename-repair snapshot that `dag/pfp/test_generate_prompts.py` copies.

Raw run output, staged input copies and batch working files are regenerable and ignored (see `.gitignore`).
They were removed from the tree after commit `92a639ddc`. The `source_pins` in `dag/operads/*.yaml`
and `dag/pfp/compare/` still name files in those staged copies. Each pin carries the file's sha256, and
the bytes can be recovered with `git show 92a639ddc:<path>`.
