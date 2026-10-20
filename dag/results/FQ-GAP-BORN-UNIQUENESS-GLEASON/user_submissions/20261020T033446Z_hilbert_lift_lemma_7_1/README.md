# Revised Lemma 7.1: Hilbert lift review

AuthorityEffect: None.

The [original attachment](submission/original.txt) is preserved byte for byte. This revision repairs the major earlier closability gap and has a sound conditional Hilbert/Galerkin core. It is not accepted verbatim and does not close the physical continuum or generator-identification rows.

See the [review](review.md), [corrected lemma](lemma_7_1_corrected.md), [claim statuses](lemma_status.json), [operation records](operad_delta.json), [source observations](source_observations.json), and [five small next targets](next_targets.md). Exact snapshots of the earlier review and lemma are in inputs, with hashes in input_sources.json.

The [exact controls](verification/exact_checks.py) passed 60 checks and three invalid-input refusals in both [normal](verification/normal.json) and [optimized](verification/optimized.json) Python. They check graph forward/adjoint compatibility separately, weighted refinement, Born mass versus projected amplitudes, persistent atoms and a genuine Galerkin spectral-pollution construction. Finite samples are controls for the written general constructions, not general convergence certificates.

All 630 files in fifteen prior manifests were reverified. No provider inference, general Lean proof, live Rust/Python/Lean source changes, Git publication or merge occurred. Stop for review.
