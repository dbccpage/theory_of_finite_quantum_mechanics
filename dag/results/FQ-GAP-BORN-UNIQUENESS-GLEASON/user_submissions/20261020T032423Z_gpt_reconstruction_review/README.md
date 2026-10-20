# GPT reconstruction proposal: scoped review

AuthorityEffect: None.

The [original submission](submission/original.txt) is preserved byte for byte. The proposed full equivalence to all finite-dimensional complex QM is NOT ESTABLISHED. The row cannot be reduced to 'only derive A2' on this evidence.

See the [review](review.md), [corrected conditional theorem contract](conditional_contract.md), [source observations](source_observations.json), [claim statuses](lemma_status.json), [operation records](operad_delta.json), and [five small next proof targets](next_targets.md).

The central counterexample is the full quantum subtheory whose systems have dimensions 2^k. It satisfies A0--A4 but lacks a qutrit object. Other repairs concern tensor compatibility, physical versus affine reversibility, effects saturation, channel availability and coherence.

The [exact controls](verification/exact_checks.py) passed 51 checks with three invalid-input refusals in both [normal](verification/normal.json) and [optimized](verification/optimized.json) Python. These check Bell partial-transpose negativity, dimension identities, standard tensor identities, effect pairing and instrument nonuniqueness. Finite exponent samples do not prove the general countertheory; its written argument is in the review. An initial harness Boolean-admission failure and its source/receipts are retained separately.

All 588 files in fourteen earlier manifests were reverified. No general Lean proof was produced, and no native Rust/Python/Lean source or manuscript was edited. There were no provider calls or Git publication. Stop for review.
