# Discrete Deformation Calculus: retained source package

AuthorityEffect: None. Consolidation baseline: `e4648bc6e7344cd6c470dea3dcbd1ce750b8ce35`.

The Discrete Deformation Calculus (DDC) v1.0.3 package, formerly a separate atlas
root, is retained under [`source_archive/discrete_deformation_calculus_package/`](source_archive/discrete_deformation_calculus_package/README.md),
alongside the [Prime source package](source_archive/prime_algorithm_package/README.md).
This follows the existing source-custody pattern of [CODA and Prime](coda_prime_integration.md).

## What moved

| Item | Result |
| --- | --- |
| Original root | `omega_engine_atlas/coda_atlas/omega_engine_discrete_deformation_calculus`, now absent. |
| Files | All 86 tracked files moved with unchanged bytes (git reports 86 renames at 100% similarity). |
| Change log | Retained as `discrete_deformation_calculus_change_log.md.txt`, as for the other imported change logs, so the WDP release inventory keeps one live change log. Bytes are unchanged. |
| Release record | The original 2026-10-03 ZIP, PDF, TeX, Lean sources, notebooks, scripts and checksum manifests are retained. |
| Prime redirect | The one-file redirect at `omega_engine_prime_algos` is retired. Its target, the Prime source package, was already in place. |

The [asset map](../manifests/ddc_consolidation.json) binds every original path to its destination with source and
destination digests. The [consolidation verifier](../scripts/verify_consolidation.py) now checks both
consolidation maps and confirms that the two retired roots are absent.

## Scope

This is a custody and relocation record. The WDP manuscript and claim registry do not cite DDC results, and
no DDC theorem is promoted into them here. The retained package's README, verifier and deposit instructions
describe the original package. They were not rerun after relocation, and the ZIP was not rebuilt. Its recorded
2026-10-03 review remains historical evidence.

The DDC reading route for learners stays in the
[education course](../../../../../../omega_engine_education/documentation/140_discrete_deformation_calculus_ddc/README.md),
whose source links now point at the retained package.

## Claim hygiene

- **Supports:** every original DDC tracked file survives byte for byte at a recorded path.
- **Does not support:** that DDC is integrated into WDP mathematics, or that any DDC check was replayed after the move.
- **Narrowest defensible claim:** the DDC source package is custody-preserved inside the WDP package.
- **Next test:** `py -3.12 scripts/verify_consolidation.py --baseline` from the package root.
