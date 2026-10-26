# Follow-up review: PR #403 independent checker (GP-IMPORT-TENSOR-PRODUCT)

**AuthorityEffect:** None. Node status and statement are unchanged.

PR #403 reached `main` through the batch integration #423 with its original checker. The code review of #403 found three defects in `checks/independent/gp-import-tensor-product.py`, and this change repairs them:

1. A constant assertion (`point_count = 2 * 2; if point_count != 4`) that could never fail. Removed.
2. The witness values were printed as fixed text. They are now computed from the two maps and printed from the computation.
3. The integer sample loop never tested the dump-right map in its right argument. Additivity and integer homogeneity are now checked in both arguments, for both maps, with symbolic integer coordinates and scalar and on 625 integer samples.

The checker now also records the identity tag of the pointwise product and the collapsed tag `delta (i, false)` of dump-right on all delta pairs.

Output of `python -I -X utf8 checks/independent/gp-import-tensor-product.py`:

```
checks=20079 failures=0 samples=625 witness_dump=0 witness_tensor=1 points=4 collapsed_delta_pairs=2
```

A mutation that adds 1 to the dump-right false coordinate makes the checker fail (4618 failures, exit 1).

The Lean module `lean4/CampaignGpImportTensorProduct.lean` (sha256 `5d83a84e8099d4d38e989378b276244c701c6bbfe31aab4c78171d09e5277a42`) is unchanged. It was replayed standalone with Lean 4.35.0 on Linux: exit 0, axioms `propext` and `Quot.sound` or none.

The checker gets a score companion, `checks/independent/gp-import-tensor-product.contract.score.yaml`, as the checkers from PRs 390–392 have.
