# L1-QM122-CIRCLE-SELECTOR-BOUNDARY

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A sign carrier ({+1,-1}) suffices for the finite phase tasks tested (sign_carrier_suffices) and the circle is not forced: excluding the sign group needs an extra condition, and the circle itself stays imported.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- circle group: assumption

## Bottleneck

Lean states, for the declared finite carriers, that the sign group fails the connectedness condition while the Gaussian units and the order-3 cyclic group meet it, and that two states with equal weights have different coherent readouts. That the circle is not forced is a statement about the absence of a derivation, recorded in the bottleneck rather than proved.

## Source status

U1SelectorBoundary / HilbertWalkCircle; headers: candidate; sign group excluded only under 'not of exponent two'

## Review

- PFP review: [dag/results/L1-QM122-CIRCLE-SELECTOR-BOUNDARY/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM122-CIRCLE-SELECTOR-BOUNDARY/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual cyclic regular-representation shift/square matrices and group-order controls, plus finite modular alternatives in Lean.
  - does not support: Provide genuine topological connectedness, selector uniqueness and source refinement. A Boolean selector pack or finite shadow cannot discharge U(1).
  - next test: Provide genuine topological connectedness, selector uniqueness and source refinement. A Boolean selector pack or finite shadow cannot discharge U(1).

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/HilbertWalkCircle.lean`

- file: [lean4/HilbertWalkCircle.lean](../../../lean4/HilbertWalkCircle.lean)
- sha256 (`bytes`): `c3326f87aa656cbec551fc23ecf89675379ae738888b497b8ecc3c748093acfa`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `HilbertWalkCircle`): recorded sha256 `c3326f87aa656cbec551fc23ecf89675379ae738888b497b8ecc3c748093acfa` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkCircle`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `sign_excluded_circle_still_imported` | yes | yes | yes | propext | `#print axioms sign_excluded_circle_still_imported` |
| `sign_fails_connectedness_shadow` | yes | yes | yes | none | `#print axioms sign_fails_connectedness_shadow` |

- counts toward the grade: yes

### Lean: `lean4/U1SelectorBoundary.lean`

- file: [lean4/U1SelectorBoundary.lean](../../../lean4/U1SelectorBoundary.lean)
- sha256 (`bytes`): `003d1730941ba102f39cdd82a0f647131050d93ef99d3e532c49e2a873a2376a`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `U1SelectorBoundary`): recorded sha256 `003d1730941ba102f39cdd82a0f647131050d93ef99d3e532c49e2a873a2376a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build U1SelectorBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `selector_not_free` | yes | yes | yes | none | `#print axioms selector_not_free` |
| `u1_selector_boundary` | yes | yes | yes | none | `#print axioms u1_selector_boundary` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0312_four_necessity_verdicts_stay_open_beside_the_matrix_gap.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0312_four_necessity_verdicts_stay_open_beside_the_matrix_gap.md](../../../dag/derivations/09_finite_hilbert/tfq_0312_four_necessity_verdicts_stay_open_beside_the_matrix_gap.md)
- sha256 (`lf-normalised`): `7a88ebef332ac78cab8de69c4643d54ce5f272c58f21c8d24bd3396a68a9e0e9`
- generated view: listed, not counted
- cited in: record TFQ-0312 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- `external:sha256:86710ba8ef7db719a42a2165e71d3bc72ac5db63d0b2a51e57f48f14e137754e`
- `external:sha256:ddaee3d0d77722244a6451750ca1e5acf7a57b4f02e75ecec70e810976d57d9e`

## Absences recorded by the TFQ records

- TFQ-0312 python: no local python twin located for sources/atlas/papers/quantum_foundations/_code/qm_122/qm122_lib/qm122_dual.py

## Routes

Incoming (1):

- `L1-R-CIRCLE-BOUNDARY` `COMPUTED`: [L1-IMP-U1-PHASES](L1-IMP-U1-PHASES.md) (IMPORTED_ASSUMPTION)

Outgoing (3):

- `L1-R-MNC-LEFTOVER` `GAP_NO_DERIVATION`: [L1-QM122-LEFTOVER-MNC-NOT-RECOVERED](L1-QM122-LEFTOVER-MNC-NOT-RECOVERED.md) (OPEN)
- `L1-R-U1-SELECTOR` `GAP_NO_DERIVATION`: [L1-U1-SELECTOR-OTHER-SEGMENT](L1-U1-SELECTOR-OTHER-SEGMENT.md) (OPEN)
- `UDG-R-TFQ-0313` `GAP_NO_DERIVATION`: [TFQ-0313](TFQ-0313.md) (OPEN)
