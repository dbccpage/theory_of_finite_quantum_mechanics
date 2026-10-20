# MUB-36 through MUB-40: review of atlas lemmas

AuthorityEffect: None.

The [original submission](submission/original.txt) is preserved byte for byte. These units are namespaced MUB, separate from Born, channel-class and residual-sector numbering. The original quartet-exclusion target remains OPEN IN THIS PROJECT.

See the [review](review.md), [corrected mathematical statements](corrected_statements.md), [source observations](source_observations.json), [operation records](operad_delta.json), and [five small next proof targets](next_targets.md).

Corrections concern tuple symmetries, the unitarity bridge calculation, strict defect thresholds, compactness margins, certificate completeness, and the literature-status claim about unavailable code. A valid coupled rebasing can transpose the first Hadamard; naive simultaneous transposition cannot.

The [exact controls](verification/exact_checks.py) passed 33 checks and rejected six invalid inputs in both [normal](verification/normal.json) and [optimized](verification/optimized.json) Python. They include dimension-two and dimension-six counterexamples to naive transposition, coefficient arithmetic and toy interval coverage. They do not compute D, produce a dimension-six atlas, prove mu(6)=3, or certify the external Lean bound locally.

The thirteen earlier manifests, comprising 554 files, were reverified. No earlier evidence was rewritten. No provider inference, native Rust/Python/Lean implementation changes, Git publication or merge occurred. Stop for review.
