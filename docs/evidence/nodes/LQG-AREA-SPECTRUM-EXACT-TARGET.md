# LQG-AREA-SPECTRUM-EXACT-TARGET

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite statement, checked in Lean 4 in the formal radical basis. With the dimensionless area a = sum over punctures of sqrt(j(j+1)) for spins j in {1/2, 1, 3/2, 2, 5/2, 3}, each term is c_j sqrt(s_j) with squarefree radicand s_j in {2, 3, 6, 15, 35}: sqrt(3)/2, sqrt(2), sqrt(15)/2, sqrt(6), sqrt(35)/2 and 2 sqrt(3) for j = 1/2, 1, 3/2, 2, 5/2, 3 (radicands 3, 2, 15, 6, 35, 3); Lean checks k(k+2) = m_k^2 d_k with d_k squarefree for the twice-spins k = 1..6, and holds each term as a vector in the formal Q-module on the basis (sqrt2, sqrt3, sqrt6, sqrt15, sqrt35)/2. On that module: (i) the 210 puncture multisets of size at most 4 (the empty one and 209 nonempty ones) have 209 distinct reduced vectors, the zero vector included (208 nonzero); (ii) the unique collision is one puncture of spin 3 with four punctures of spin 1/2 (2 sqrt(3) = 4 x sqrt(3)/2); (iii) for a single puncture the squared area j(j+1) = k(k+2)/4 is at least 3/4, strictly increasing in k, with minimum 3/4 at j = 1/2 (area sqrt(3)/2).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declaration references covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not proved in Lean: that the formal vector is the real area (no real square root occurs in the module) and that two multisets have equal real area if and only if their vectors agree, which needs the linear independence over Q of sqrt(2), sqrt(3), sqrt(6), sqrt(15), sqrt(35) (stated in the module header, not a Lean theorem); the agreement of the hand-entered punctureArea table with the m_k, d_k table beyond inspection; the minimum over multisets of several punctures (only single punctures). The physical constant, the Immirzi parameter and the gauge-invariance constraint on admissible puncture lists are not part of the target.

## Source status

Casimir values j(j+1) = a(a+2)/4 in {3/4, 2, 15/4, 6, 35/4, 12} for j in {1/2..3} and the squarefree-radical degeneracy 2 sqrt(3) = 4 x (sqrt(3)/2) recomputed with Python fractions.Fraction on 2026-10-22. Lean: checked in Lean 4.35.0 via lake build FrontierAreaSpectrum (library FrontierTargets in lean4/lakefile.lean) in the form recorded in the statement; replay receipt in dag/research/frontier_targets_lean_replay.json; per-node review in dag/research/frontier_targets_lean_review.md.

## Review

- Frontier Lean review: [dag/research/frontier_targets_lean_review.md](../../../dag/research/frontier_targets_lean_review.md); verdict `NARROWED`; qualifies for E4: yes.
  - theorems that discharge the node, as listed by the review: `casimir_squarefree_factorizations`, `spin3_equals_four_spin_half`, `area_spectrum_table_and_unique_degeneracy`, `smallest_nonzero_area_level_is_spin_half`, `single_puncture_area_sq_strictly_increasing`
  - the review's reason for its verdict is in the row of this node in the review file

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FrontierAreaSpectrum.lean`

- file: [lean4/FrontierAreaSpectrum.lean](../../../lean4/FrontierAreaSpectrum.lean)
- sha256 (`bytes`): `4559931b4f2cdf9b3d83eba2085b3175648b73e99db28b154240f19745cd53df`
- cited in: node.lean, node.source, receipt dag/research/frontier_targets_lean_replay.json (FrontierAreaSpectrum)
- replay: `verified`
  - receipt [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json) (module `FrontierAreaSpectrum`): recorded sha256 `4559931b4f2cdf9b3d83eba2085b3175648b73e99db28b154240f19745cd53df` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FrontierAreaSpectrum`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FrontierAreaSpectrum.area_spectrum_table_and_unique_degeneracy` | yes | yes | yes | none | `#print axioms FrontierAreaSpectrum.area_spectrum_table_and_unique_degeneracy` |
| `FrontierAreaSpectrum.casimir_squarefree_factorizations` | yes | yes | yes | propext | `#print axioms FrontierAreaSpectrum.casimir_squarefree_factorizations` |
| `FrontierAreaSpectrum.single_puncture_area_sq_strictly_increasing` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierAreaSpectrum.single_puncture_area_sq_strictly_increasing` |
| `FrontierAreaSpectrum.smallest_nonzero_area_level_is_spin_half` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FrontierAreaSpectrum.smallest_nonzero_area_level_is_spin_half` |
| `FrontierAreaSpectrum.spin3_equals_four_spin_half` | yes | yes | yes | none | `#print axioms FrontierAreaSpectrum.spin3_equals_four_spin_half` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2304_lqg_area_spectrum_exact_target.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2304_lqg_area_spectrum_exact_target.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2304_lqg_area_spectrum_exact_target.md)
- sha256 (`lf-normalised`): `3ccdf5dd253e15146ba95d23d3bb58ccbe329a9200250824078b7055d8c6f17a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2304
- counts toward the grade: no

### Documents and data: `dag/research/frontier_targets_lean_replay.json`

- file: [dag/research/frontier_targets_lean_replay.json](../../../dag/research/frontier_targets_lean_replay.json)
- sha256 (`lf-normalised`): `1c66aabd3bb726fafcd0238c259644d6f79dd304178d171a75ea36d6522bd2cc`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:gr-qc/9411005`
- `external:arXiv:gr-qc/9602046`

## Routes

Incoming (1):

- `FRO-R-LQG-AREA-SPECTRUM-EXACT-TARGET` `DERIVED_LEAN`: [LQG-AREA-VOLUME-SPECTRA-SOURCE](LQG-AREA-VOLUME-SPECTRA-SOURCE.md) (SOURCE_RECORD), [LQG-SPIN-NETWORK-STATES-IMPORT](LQG-SPIN-NETWORK-STATES-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

