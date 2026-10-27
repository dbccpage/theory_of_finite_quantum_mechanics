# L1-U1-SELECTOR-OTHER-SEGMENT

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Pointer to QM_028 / QM_062 (owned by another segment): selection of C and U(1) from finite carriers is not established here. The only general fact proved in this repository for it is that the torsion of the unit Gaussian rationals {(x,y) in Q^2 : x^2+y^2=1} is exactly mu_4 (U1SelectorSegment.circle_torsion_iff), so every finite phase group inside Q(i) lies in mu_4; a general finite-field/ring classification, cyclotomic extensions, completion and continuity remain open. Separate modulo-7 result: On the integers modulo 7, with product (a, b) * (c, d) = (a*c - b*d, a*d + b*c), the pairs (x, y) with x*x + y*y = 1 are exactly the powers g^0 through g^7, in exponent order, for g = (2, 2): (1, 0), (2, 2), (0, 1), (5, 2), (6, 0), (5, 5), (0, 6) and (2, 5). The next power g^8 is (1, 0), and g^1 through g^7 all differ from (1, 0). The count 8 equals 7 + 1 and is not 4.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 37
- distinct cited Lean declarations covered by a current replay receipt: 36
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/U1SelectorSegment.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

None recorded.

## Bottleneck

Selection of C and U(1) from finite carriers proper (finite fields/rings, cyclotomic extensions, completion, continuity) is not derived; the pointer target in QM_028 / QM_062 is unresolved. Only the explicit modulo-7 carrier and its stated operations are covered. The Nat subtraction encoding agrees with integer subtraction only on the bounded residue domain. Selection of C or U(1), general prime or ring classification, cyclotomic fields, completion and continuity remain open; the older Gaussian-rational torsion result is retained separately.

## Source status

Cross-segment U(1) selector Layers 1-3 finite algebra (conjugation involution, split-real zero-divisor exclusion, non-abelian Pauli exclusion, and Gaussian-integer cx ring injectivity) mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/L1-U1-SELECTOR-OTHER-SEGMENT/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/L1-U1-SELECTOR-OTHER-SEGMENT/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Inside the unit Gaussian rationals the only phases of finite order are the four elements of mu_4; the rational circle points outside mu_4 are exactly those with 2x not an integer and they have infinite order (kernel instance: (3/5, 4/5)), so a finite phase group inside the Gaussian rationals has order dividing 4, whereas the unit circle over a finite field F_p is a different finite carrier with p -+ 1 elements (native table, not a kernel statement).
  - does not support: Any derivation of C or U(1) from finite carriers, or a proof that no such derivation exists: the node is a pointer to QM_028 / QM_062 owned by another segment and its selection is NOT established here; finite carriers in the sense of finite fields or finite rings (the unit circle over F_p has order p -+ 1, native table only): the theorem is a no-go only for finite subgroups of the unit Gaussian rationals, and the identification of a finite phase carrier with such a subgroup is not argued; larger finite phase groups in cyclotomic extensions (Q(zeta_8), Q(zeta_3), ...) which this result does not treat; completion, continuity, compactness or Haar measure of the circle; that there are infinitely many infinite-order points as a kernel statement (only the instance u345_infinite_order and the native census); the rival split-complex hyperbola x^2 - y^2 = 1 (the H011 flag rival_excluded); the H011 selector pack, whose selector_not_free is rfl on a record with a hand-set Boolean field; any physical reading of phases.
  - next test: Determine the unit circle {x^2 + y^2 = 1} over F_p and over Z/n exactly: prove that it is cyclic of order p - (-1/p) and show which phase orders a finite scalar ring does and does not force, as the finite-carrier counterpart of the Gaussian-rational torsion result; the torsion over Q(i, sqrt 2) and Q(zeta_3) is a secondary item.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1003
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm062_u1_selector_layers_and_ring_iso` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm062_u1_selector_layers_and_ring_iso` |
| `QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle` |

- counts toward the grade: yes

### Lean: `lean4/L1U1SelectorOtherSegment.lean`

- file: [lean4/L1U1SelectorOtherSegment.lean](../../../lean4/L1U1SelectorOtherSegment.lean)
- sha256 (`bytes`): `e9c220887eccbca20473d823ab81b5b7d329c5439e190a65b43723e902f9a430`
- cited in: node.lean, node.source, receipt dag/research/campaign_l1-u1-selector-other-segment_lean_replay.json (L1U1SelectorOtherSegment), receipt dag/research/pr435_review_lean_replay.json (L1U1SelectorOtherSegment), record TFQ-1003
- replay: `verified`
  - receipt [dag/research/campaign_l1-u1-selector-other-segment_lean_replay.json](../../../dag/research/campaign_l1-u1-selector-other-segment_lean_replay.json) (module `L1U1SelectorOtherSegment`): recorded sha256 `e9c220887eccbca20473d823ab81b5b7d329c5439e190a65b43723e902f9a430` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr435_review_lean_replay.json](../../../dag/research/pr435_review_lean_replay.json) (module `L1U1SelectorOtherSegment`): recorded sha256 `e9c220887eccbca20473d823ab81b5b7d329c5439e190a65b43723e902f9a430` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build L1U1SelectorOtherSegment`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `L1U1SelectorOtherSegment.allDistinct` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.allDistinct` |
| `L1U1SelectorOtherSegment.earlier_ne_one` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.earlier_ne_one` |
| `L1U1SelectorOtherSegment.eight` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.eight` |
| `L1U1SelectorOtherSegment.eight_distinct` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.eight_distinct` |
| `L1U1SelectorOtherSegment.g` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.g` |
| `L1U1SelectorOtherSegment.isPower` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.isPower` |
| `L1U1SelectorOtherSegment.mul` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.mul` |
| `L1U1SelectorOtherSegment.norms` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.norms` |
| `L1U1SelectorOtherSegment.not_axis` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.not_axis` |
| `L1U1SelectorOtherSegment.solutions_iff` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.solutions_iff` |
| `L1U1SelectorOtherSegment.step1` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.step1` |
| `L1U1SelectorOtherSegment.step2` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.step2` |
| `L1U1SelectorOtherSegment.step3` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.step3` |
| `L1U1SelectorOtherSegment.step4` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.step4` |
| `L1U1SelectorOtherSegment.step5` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.step5` |
| `L1U1SelectorOtherSegment.step6` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.step6` |
| `L1U1SelectorOtherSegment.step7` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.step7` |
| `L1U1SelectorOtherSegment.step8` | yes | yes | yes | none | `#print axioms L1U1SelectorOtherSegment.step8` |

- counts toward the grade: yes

### Lean: `lean4/U1SelectorBoundary.lean`

- file: [lean4/U1SelectorBoundary.lean](../../../lean4/U1SelectorBoundary.lean)
- sha256 (`bytes`): `003d1730941ba102f39cdd82a0f647131050d93ef99d3e532c49e2a873a2376a`
- cited in: node.lean, record TFQ-1003
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `U1SelectorBoundary`): recorded sha256 `003d1730941ba102f39cdd82a0f647131050d93ef99d3e532c49e2a873a2376a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build U1SelectorBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `selector_not_free` | yes | yes | yes | none | `#print axioms selector_not_free` |

- counts toward the grade: yes

### Lean: `lean4/U1SelectorSegment.lean`

- file: [lean4/U1SelectorSegment.lean](../../../lean4/U1SelectorSegment.lean)
- sha256 (`bytes`): `beeffb4aefa76d734dc8999173366a040106dce3cf867c3778a0791c1cc044b2`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (U1SelectorSegment)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `U1SelectorSegment`): recorded sha256 `beeffb4aefa76d734dc8999173366a040106dce3cf867c3778a0791c1cc044b2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build U1SelectorSegment`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U1SelectorSegment.Wseq_cast` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.Wseq_cast` |
| `U1SelectorSegment.Wseq_mod` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.Wseq_mod` |
| `U1SelectorSegment.cayley_on_circle` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.cayley_on_circle` |
| `U1SelectorSegment.cayley_reaches_south_pole` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.cayley_reaches_south_pole` |
| `U1SelectorSegment.circle_integral_case` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.circle_integral_case` |
| `U1SelectorSegment.circle_torsion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.circle_torsion` |
| `U1SelectorSegment.circle_torsion_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.circle_torsion_iff` |
| `U1SelectorSegment.cube_root_trivial` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.cube_root_trivial` |
| `U1SelectorSegment.every_point_is_cayley` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.every_point_is_cayley` |
| `U1SelectorSegment.no_point_with_x_half` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.no_point_with_x_half` |
| `U1SelectorSegment.not_torsion_of_den` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.not_torsion_of_den` |
| `U1SelectorSegment.re_rec` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.re_rec` |
| `U1SelectorSegment.torsion_exponent_divides_four` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.torsion_exponent_divides_four` |
| `U1SelectorSegment.u345_infinite_order` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms U1SelectorSegment.u345_infinite_order` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1003
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1003
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1003
- counts toward the grade: no

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust, record TFQ-1003

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/l1-u1-selector-other-segment.py`

- file: [checks/independent/l1-u1-selector-other-segment.py](../../../checks/independent/l1-u1-selector-other-segment.py)
- sha256 (`bytes`): `c7f59f135fe8d796c916b685b02e5a68f2afac7a23f72a93d093e0b89ad1be56`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1003_l1_u1_selector_other_segment.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1003_l1_u1_selector_other_segment.md](../../../dag/derivations/08_l1_to_l2/tfq_1003_l1_u1_selector_other_segment.md)
- sha256 (`lf-normalised`): `bd50c46e7eece2b8494acd044911798c3e2ba3654c621b497e5de69abd0c5eaf`
- generated view: listed, not counted
- cited in: record TFQ-1003
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/l1-u1-selector-other-segment.md`

- file: [dag/derivations/independent/l1-u1-selector-other-segment.md](../../../dag/derivations/independent/l1-u1-selector-other-segment.md)
- sha256 (`lf-normalised`): `346ca89694be4477f8ce22b0e45b77c216db3880dc7a22594eefd6e530c27f88`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pr435_review_lean_replay.json`

- file: [dag/research/pr435_review_lean_replay.json](../../../dag/research/pr435_review_lean_replay.json)
- sha256 (`lf-normalised`): `a8a049ea96a6695af07f308de08728c612dda2990f635b30b83aec9a505e0ad5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/121_the_finite_qm_ingredient_ladder/qm_121_the_finite_qm_ingredient_ladder_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/121_the_finite_qm_ingredient_ladder/qm_121_the_finite_qm_ingredient_ladder_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (2):

- `L1-R-U1-SELECTOR` `GAP_NO_DERIVATION`: [L1-QM122-CIRCLE-SELECTOR-BOUNDARY](L1-QM122-CIRCLE-SELECTOR-BOUNDARY.md) (COMPUTATIONALLY_CHECKED)
- `L1-R-U1-SELECTOR-LAYERS` `GAP_NO_DERIVATION`: [DS-QM062-U1-SELECTOR-LAYERS](DS-QM062-U1-SELECTOR-LAYERS.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

