# FQ-BUSCH-EFFECT-FRAME

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> At declared real places, an informationally-complete POVM family and a polyhedral frame cone are distinguished (busch_ic_povm_vs_polyhedral_frame_cone); Galois-conjugate negativity versus SOS total positivity is witnessed (galois_conjugate_negativity_vs_sos_total_positivity). Busch-type effect hypotheses are explicit.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- effect algebra and trace frame function (assumption)
- declared real places (assumption)

## Bottleneck

Lean evaluates fixed rational traces, determinants, Bloch sums and minors for the declared effects and frame cone. No general Busch-type theorem is stated.

## Source status

H058 theorem family (38 theorems); Rust exact effects at declared cyclotomic real places

## Review

- PFP review: [dag/results/FQ-BUSCH-EFFECT-FRAME/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/FQ-BUSCH-EFFECT-FRAME/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact six-effect readouts and reconstruction, plus a finite-probe-versus-PSD counterexample, are native/kernel checked at the stated scalar/coordinate scopes.
  - does not support: Prove full effect positivity, matrix/trace transport, arbitrary Busch hypotheses and the separate real-place/Galois/SOS claims. Finite informational completeness alone is not full positivity or Born uniqueness.
  - next test: Prove full effect positivity, matrix/trace transport, arbitrary Busch hypotheses and the separate real-place/Galois/SOS claims. Finite informational completeness alone is not full positivity or Born uniqueness.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/EffectFrameBusch.lean`

- file: [lean4/EffectFrameBusch.lean](../../../lean4/EffectFrameBusch.lean)
- sha256 (`bytes`): `c748ec2f46ff05066ded95e704b5a80c72309d2332a31930601e54561f921c90`
- cited in: node.lean, record TFQ-1017
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `EffectFrameBusch`): recorded sha256 `c748ec2f46ff05066ded95e704b5a80c72309d2332a31930601e54561f921c90` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build EffectFrameBusch`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `two_mul_half` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms two_mul_half` |

- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: node.lean, record TFQ-1017
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `busch_ic_povm_vs_polyhedral_frame_cone` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms busch_ic_povm_vs_polyhedral_frame_cone` |
| `galois_conjugate_negativity_vs_sos_total_positivity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms galois_conjugate_negativity_vs_sos_total_positivity` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_1017_fq_busch_effect_frame.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_1017_fq_busch_effect_frame.md](../../../dag/derivations/12_finite_qm_structure/tfq_1017_fq_busch_effect_frame.md)
- sha256 (`lf-normalised`): `a8a879bf7db7c7e4cc8a88cafe4d7f992ffd8c982f234edfb3f8537c296c8dd6`
- generated view: listed, not counted
- cited in: record TFQ-1017
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics_claim_ledger.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics_claim_ledger.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics_claim_ledger.md)
- sha256 (`lf-normalised`): `259e971c72c485503b9c9f157bec6ec9412fe24b8c4cc266e1d0ab6aa7e2d1e0`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:3e7e1210d5c49a5c5f40835b086b7d56e6812c4eb788e1714d989c931a3a1bf1::EffectAlgebra`
- `external:sha256:3e7e1210d5c49a5c5f40835b086b7d56e6812c4eb788e1714d989c931a3a1bf1::TraceFrameFunction`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`

## Routes

Incoming (1):

- `FQ-R-BUSCH` `COMPUTED`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION), [FQ-CABELLO-NO-INTEGER-FRAME](FQ-CABELLO-NO-INTEGER-FRAME.md) (PROVED_LEAN)

Outgoing (1):

- `FQ-R-EMBEDDING` `COMPUTED`: [FQ-GAP-REAL-EMBEDDING-CHOICE](FQ-GAP-REAL-EMBEDDING-CHOICE.md) (COMPUTATIONALLY_CHECKED)
