# Uniqueness of the inner product on the sector carrier — sector additivity and transitive sector symmetry select the standard form, kernel-checked, with exact Python and Rust twins

Status: **constructed, compiled, sealed, stopped for review**. AuthorityEffect: None.

Target: DAG node `L1-IMP-HILBERT-INNER-PRODUCT` ("a Hilbert inner product on the linearized carrier is
admitted, not derived; H005 exhibits more than one admissible Gram form on the same carrier") and the
gap route it blocks, `L1-IMP-ORTHOGONAL-ADDITIVITY`. This run shows that the form is not a free
admission: two laws on the quadratic readout pin it up to a unit scale, and the orthogonality of the
sector basis follows from the first law alone.

- [SectorFormUniqueness.lean](SectorFormUniqueness.lean) (imports `BornMatrixCarrier`, whose `qf` is
  the readout selected here): pairing, disjoint supports, `SectorAdditive`, the l1 transcription
  `l1_disjoint_additive`; **orthogonality** `offdiag_pair_sum_eq_zero`, `offdiag_eq_zero`,
  `eq_diagonal_of_sectorAdditive`, and the readout `Σ G i i · x i²` without any symmetry assumption
  (`qf_eq_sum_diag_sq_of_sectorAdditive`); sector permutations `permute`, `Invariant`, `TransitiveOn`,
  the generated group `Generated` with `invariant_of_generated`; **collapse** `diag_const_of_transitive`,
  `eq_smul_one`, `eq_smul_one_generated`, `qf_eq_scale_dot`, `pair_eq_scale_dot`, `scale_pos`;
  **uniqueness and nonvacuity** `unique_of_normalized`, `unique_up_to_scale`, `eq_one_of_normalized`,
  `one_sectorAdditive`, `one_invariant`, `one_posdef`; **countermodels** `diag12 = diag(1, 2)` (the H005
  form: sector additive, positive definite, not swap invariant, not scalar) and `unif12 = 1 + (all ones)`
  (swap invariant, positive definite, not sector additive, not scalar) (72 receipts).
- [SectorFormHermitian.lean](SectorFormHermitian.lean) (imports `BornHermitianCarrier` and
  `BornHermitianPsdDecomposition`): the same chain over ℚ(i) with the Hermitian readout `re (x* H x)`;
  sector additivity is tested along the two directions `e_j` and `i·e_j` (`offdiag_re_add_re`,
  `offdiag_im_sub_im`, `offdiag_eq_zero`), the generated group and the collapse to the rational scalar
  `re H i₀ i₀` (`eq_smul_one`, `eq_smul_one_generated`, `hf_eq_scale_vnorm`, `scale_pos`), uniqueness and
  nonvacuity, and the control `imagLeak12 = [[1, i], [−i, 1]]`: Hermitian, additive on `(e₀, e₁)` along
  the real direction, not sector additive (47 receipts).
- Exact twins: [code/python/src/qm/inner_product_uniqueness.py](../../../../../code/python/src/qm/inner_product_uniqueness.py)
  with [22 tests](../../../../../code/python/tests/test_inner_product_uniqueness.py) and
  [code/rust/src/qm/inner_product_uniqueness.rs](../../../../../code/rust/src/qm/inner_product_uniqueness.rs)
  with 22 inline tests: additivity defects `G_ij + G_ji` (over ℚ(i): `re(H_ij + H_ji)` and
  `im(H_ji − H_ij)`), the diagonal readout, invariance defects, the generated permutation group
  (`closure`, the replay of `Generated`) and its orbits, the scale certificate with an exact witness
  for whichever hypothesis fails first (`derive_scale`, `hermitian_derive_scale`), the uniqueness
  certificate and the three countermodels. The two Lean modules are installed under `lean4/` and
  registered in the lakefile.
- [Compile receipts](verification/), [kernel axioms](verification/kernel_axioms.json),
  [accepted modules](accepted_modules.json), [9 operation records](operad_delta.json),
  [claim statuses](claim_status.json), [review and boundaries](review.md), [next steps](next_steps.md),
  [provenance](provenance.json), [validation](validation.json), [DAG update tool](tools/dag_update.py),
  [seal](manifest.json).

Two accepted compilations, **119 printed axiom receipts**, every one within
`[propext, Classical.choice, Quot.sound]` (several need fewer); no `sorry`, `axiom`, `opaque` or
`unsafe`; no compile warnings; no noncomputable definitions. The DAG nodes
`L1-IMP-HILBERT-INNER-PRODUCT` and `L1-IMP-ORTHOGONAL-ADDITIVITY` move from `IMPORTED_ASSUMPTION` to
`CONDITIONAL` (on the two readout laws), with the new routes `L1-R-INNER-PRODUCT-SECTOR-FORM` and
`L1-R-ORTHOGONAL-ADDITIVITY-SECTOR-FORM` (`CONDITIONAL_ON_IMPORT`) beside the retained gap routes;
`dag/validate_derivation_dag.py --repo-root . --no-files` reports `nodes=197 routes=194 failures=0`.

**Result in one line.** On `Fin n → ℚ` (or `ℚ(i)`), a symmetric (Hermitian) form whose readout is
additive on disjoint sector supports and invariant under sector permutations generating a transitive
group equals `c • 1` with `c = G i₀ i₀`, `c > 0` for a positive-definite readout; the unit-normalised
form is the standard form `qf 1` / `hf 1` of the Born carriers. The H005 non-uniqueness is exactly the
failure of the symmetry law.

**Review boundaries.** The carrier, the scalar field and the quadratic shape of the readout are
supplied; the two laws are hypotheses (the first transcribed from edgewise l1 additivity, the second
from the H006 permutation envelope), not derived from primitive difference; the scale is a unit choice.
See [review.md](review.md).

Replay: `python tools/replay.py SOURCE NEW_LABEL --lean PINNED_LEAN --project CONFIGURED_LEAN4_PROJECT`
for `SectorFormUniqueness.lean` and `SectorFormHermitian.lean`, with
`build/BornEffectValuation.olean`, `build/BornMatrixCarrier.olean` (effect-valuation run receipts
`effect_valuation_01`, `matrix_carrier_01`) and `build/BornGaussRat.olean`,
`build/BornHermitianCarrier.olean`, `build/BornHermitianPsdDecomposition.olean` (Gaussian-rational run
receipts `gauss_rat_01`, `hermitian_carrier_01`, `hermitian_psd_01`) restored first; then
`python tools/seal.py receipts`, `python tools/operads.py`, `python tools/provenance.py`,
`python tools/companions.py`, `python tools/dag_update.py`, `python dag/sync_application_branches.py`
(keeps the application-branch routes last), `python tools/seal.py manifest` and
`python tools/seal.py verify`.
