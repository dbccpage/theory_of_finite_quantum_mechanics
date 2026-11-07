# evidence/results

One folder per DAG node, named by the node id. The tree keeps only what is cited:

- `<NODE-ID>/reviews/*/`: the review of the node. `dag/tools/sync_pfp_results.py` reads these files, checks
  their sha256 and writes the `pfp_review` object of the node in `dag/derivation_dag.json`.
- `<NODE-ID>/runs/*/` and `batches/*/`: only the files that the DAG (`pfp_review.superseded_by`), a receipt, a
  test (`code/python/tests/test_born_boundary_exact.py`, `test_l1_import_exact.py`) or a tool cites.

Raw run output, staged input copies and batch working files are regenerable and ignored (see `.gitignore`);
a cited run file is added with `git add -f`. The review folders are counted by `scripts/build_readme_facts.py`
for the facts block of the front page.
