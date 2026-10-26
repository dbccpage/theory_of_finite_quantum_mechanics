# Overclaim review: GP-IMPORT-TENSOR-PRODUCT

Scope: branch `derive/GP-IMPORT-TENSOR-PRODUCT` against `origin/main` (`4fea09ae176a`). One node statement changed. Status stays `IMPORTED_ASSUMPTION`.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). The three LOW rows are on `TENSOR-ASSUMPTION-COUNTERMODELS` and `FQ-GAP-TENSOR-UNIQUENESS` after the tensor-receipt re-pin, not on this node's new text. Read `lean4/CampaignGpImportTensorProduct.lean` against the node statement. Rebuilt that module with Lean 4.35.0. Independent checker `checks/independent/gp-import-tensor-product.py`: `checks=10048 failures=0 samples=625 witness_dump=0 witness_tensor=1 points=4`.

Result: 0 FULL, 1 NARROWED, 0 OVERCLAIM.

## Statement versus theorem

| Claim | Declaration | Verdict |
| --- | --- | --- |
| The pointwise product sends `(a, b)` to `u(a) * v(b)`. | `tensor_pointwise` | FULL |
| An additive, integer-homogeneous map that sends `(delta i, delta j)` to `delta (i, j)` agrees with that product. | `embed_eq_tensor` | FULL |
| Dump-right sends `(a, false)` to `u(a) * (v(false) + v(true))`. | `dumpRight_false_coord` | FULL |
| Dump-right sends `(a, true)` to `0`. | `dumpRight_true_coord` | FULL |
| Dump-right is additive in each argument. | `dumpRight_add_left`, `dumpRight_add_right` | FULL |
| Dump-right is integer-homogeneous in each argument. | `dumpRight_smul_left`, `dumpRight_smul_right` | FULL |
| Dump-right sends `(delta i, delta j)` to `delta (i, false)`. | `dumpRight_collapsed_tag` | FULL |
| At `delta false`, `delta true`, and `(false, true)`, the values are `0` and `1`. | `witness_dump_zero`, `witness_tensor_one` | FULL |
| A Hilbert-space tensor product is the unique way to combine systems. | not proved | NOT PROVED |

The Hilbert-space sentence is only in the bottleneck. The node is not promoted.

## Axioms

`#print axioms` reports only `propext` and `Quot.sound`, or no axioms. `Classical.choice` does not appear.

## Numbers

| Number | Recomputation | Match |
| --- | --- | --- |
| dump-right value `0` | Lean `witness_dump_zero` and the checker | match |
| pointwise value `1` | Lean `witness_tensor_one` and the checker | match |
| `4` points of `Bool × Bool` | checker `points=4` | match |
| `625` integer samples with coordinates in `-2..2` | `5**4` | match |
| `10048` checks and `0` failures | checker exit 0 | match |

README counts were rewritten by `scripts/build_readme_facts.py` and match `--check`.

## What the scanner could not decide

Whether the three LOW rows on the neighbouring tensor nodes are older than this re-pin. They do not change this node's verdict.
