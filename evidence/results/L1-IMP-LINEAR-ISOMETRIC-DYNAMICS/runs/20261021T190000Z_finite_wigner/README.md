# Finite exact Wigner theorem over ℚ(i)ⁿ — transition-probability-preserving ray maps are linear or conjugate-linear similarities, kernel-checked, with exact Python and Rust twins

Status: **constructed, compiled, sealed, stopped for review**. AuthorityEffect: None.

Target: DAG node `L1-IMP-LINEAR-ISOMETRIC-DYNAMICS` ("dynamics on the lift are reversible linear
isometries", imported; the only route into it, `L1-R-DYNAMICS-GAP`, is a gap). The sector-form run
(`L1-IMP-HILBERT-INNER-PRODUCT`, 20261021T013500Z) fixed the inner product of the exact carrier up to a
unit scale and left this node as its next step 2. This run shows that linearity, reversibility and
isometry up to a positive rational scale are not free admissions: one operational law — the ray
dynamics preserves the Born transition probabilities of rank-one effects — forces them, with no
continuity hypothesis, and the scale is exactly what the finite carrier cannot remove in general.

- [FiniteWignerKernel.lean](FiniteWignerKernel.lean) (imports `BornHermitianCarrier`,
  `BornHermitianPsdDecomposition`): inner product `ip`, squared norm `vnorm = hf 1`, transition
  probability `tp x y = |⟨x, y⟩|² / (‖x‖² ‖y‖²)` and its identity with the normalised Born readout of
  the rank-one effect `P x` (`tp_eq_born`); scale invariance, `tp = 1` on a ray, `tp = 0` iff
  orthogonal; the equality case of Cauchy–Schwarz over ℚ(i) (`eq_smul_of_normSq_ip_eq`,
  `tp_eq_one_iff`); the twist `tw ε` / `twist ε` (`ε = 1` identity, `ε = −1` conjugation) and its
  compatibility with `tp`; similarities `Fᴴ F = d • 1` (`Similarity`) with the exact transport
  `ip (F x) (F y) = d • ip x y`, `tp (F x) (F y) = tp x y`, the two-sided inverse `(1/d) • Fᴴ` and
  `F Fᴴ = d • 1`; column matrices and the orthogonal expansion `y = colMatrix f *ᵥ coords f y` in any
  pairwise orthogonal family of `n` nonzero vectors (`expansion`, through `mul_eq_one_comm`)
  (110 receipts).
- [FiniteWignerTheorem.lean](FiniteWignerTheorem.lean): `TpPreserving T` (nonzero to nonzero, `tp`
  preserved); the probes `p i₀ j = e i₀ + e j` and `qs i₀ s j = e i₀ + (s i) e j`; **reconstruction**
  of the aligned orthogonal basis `f` from the images of the sector basis and of the probes
  `e i₀ + e j` (`g`, `align`, `f`, `F`, `d`, `vnorm_f`, `similarity_F`, `T_e_eq`, `T_p_eq`); the sign
  `sgn j ∈ {±1}` carried by the probes `e i₀ + i e j` (`sgn_spec`) and its consistency across
  coordinates through the probe `e i₀ + i e j + i e k` (`sgn_consistent`); **coordinate rigidity**
  against the three probe families (`coord_rigidity`); **stage 1** (`x i₀ ≠ 0`) and **stage 2**
  (`x i₀ = 0`, via the probe `e i₀ + x` and Cauchy–Schwarz equality); the theorem `finite_wigner`,
  its two-case form `finite_wigner_cases`, the converse `tpPreserving_of_similarity` and
  reversibility `similarity_bijective` (79 receipts).
- [FiniteWignerSimilarity.lean](FiniteWignerSimilarity.lean) (also imports `SectorFormHermitian`):
  `Unitary`; a scalar multiple of a unitary is a similarity with scale `|c|²` and a similarity rescales
  to a unitary iff its scale is a norm from ℚ(i), i.e. a sum of two rational squares
  (`exists_unitary_iff`, `norm_iff_sum_two_sq`); `3` is not such a sum (`three_not_sum_two_sq`,
  descent modulo 3); the countermodel `F3 = [[1, −1 + i], [1 + i, 1]]` with `F3ᴴ F3 = 3 • 1`
  (`F3_similarity`, `F3_tpPreserving`) whose ray map is induced by no ℚ(i)-unitary and no
  ℚ(i)-antiunitary (`F3_not_induced_by_unitary`, `F3_not_induced_by_antiunitary`, with
  `eq_smul_one_of_rays`: a matrix fixing every ray is a scalar); the H006 permutation envelope as the
  unitary `permMatrix σ` (`permMatrix_mulVec`, `permMatrix_unitary`); the Born form of the hypothesis
  (`tpPreserving_iff_born`) (36 receipts).
- [GaussRatAutomorphisms.lean](GaussRatAutomorphisms.lean) (imports `BornGaussRat`): every ring
  homomorphism `ℚ(i) → ℚ(i)` is the identity or conjugation (`ringHom_eq_id_or_star`); the only square
  roots of `−1` are `±i` (8 receipts).
- Exact twins: [code/python/src/qm/finite_wigner.py](../../../../../code/python/src/qm/finite_wigner.py)
  with [24 tests](../../../../../code/python/tests/test_finite_wigner.py) and
  [code/rust/src/qm/finite_wigner.rs](../../../../../code/rust/src/qm/finite_wigner.rs) with 29 inline
  tests (full crate build, no warnings in the module): transition probabilities as Born readouts, the
  similarity certificate `Fᴴ F = d·I` with an offending entry otherwise, the probe-driven
  reconstruction of `(F, d, ε)` with an exact witness for whichever step fails (`zero_image`,
  `orthogonality`, `alignment`, `sign`, `consistency`), verification that a map is induced by its
  reconstruction on samples, the deterministic ray-scalar map `induced_ray_map`, sums of two rational
  squares with the obstructing prime `≡ 3 (mod 4)` (`sum_of_two_rational_squares`), unitary
  normalisation, `f3`, `hadamard2` (`d = 2 = |1 + i|²`) and the permutation matrices. The four Lean
  modules are installed under `lean4/` and registered in the lakefile.
- [Compile receipts](verification/), [kernel axioms](verification/kernel_axioms.json),
  [accepted modules](accepted_modules.json), [15 operation records](operad_delta.json),
  [claim statuses](claim_status.json), [review and boundaries](review.md), [next steps](next_steps.md),
  [provenance](provenance.json) (including the restored import oleans), [validation](validation.json),
  [DAG update tool](tools/dag_update.py), [receipt rebind tool](tools/rebind_receipts.py),
  [seal](manifest.json).

Four accepted compilations under **Lean 4.35.0** (Mathlib `56a00585`), **233 printed axiom receipts**,
every one within `[propext, Classical.choice, Quot.sound]` (218 need all three, 13 need
`[propext, Quot.sound]`, 2 need `[Quot.sound]`); no `sorry`, `axiom`, `opaque` or `unsafe`; no compile
warnings; no noncomputable definitions. The DAG node `L1-IMP-LINEAR-ISOMETRIC-DYNAMICS` moves from
`IMPORTED_ASSUMPTION` to `CONDITIONAL` (on the transition-probability law, which gets its own imported
node `L1-IMP-TRANSITION-PROBABILITY-LAW` and master record `TFQ-1047`), the conditional route
`L1-R-DYNAMICS-FINITE-WIGNER` (inputs `L1-IMP-HILBERT-INNER-PRODUCT`,
`L1-IMP-TRANSITION-PROBABILITY-LAW`) sits beside the retained gap route `L1-R-DYNAMICS-GAP`;
`dag/validate_derivation_dag.py --repo-root . --no-files` reports `nodes=738 routes=735 failures=0`
and the three syncs, their `--check` and `--invariants` are clean.

**Result in one line.** On `Fin n → ℚ(i)`, a map sending nonzero vectors to nonzero vectors and
preserving transition probabilities is, on rays, `x ↦ F x` or `x ↦ F (star x)` with `Fᴴ F = d • 1`,
`d > 0` rational; `F` rescales to a unitary iff `d` is a sum of two rational squares, and the scale-3
countermodel `F3` shows this is a real restriction over the exact carrier.

**Review boundaries.** The carrier, the scalar field ℚ(i) and the quadratic readout are supplied; the
transition-probability law is a hypothesis, not derived from primitive difference; the theorem selects
a similarity, not a unitary, and cannot do better; continuous time is untouched. See
[review.md](review.md).

Replay: `python tools/replay.py SOURCE NEW_LABEL --lean PINNED_LEAN_4.35.0 --project CONFIGURED_LEAN4_PROJECT`
for `FiniteWignerKernel.lean`, then `FiniteWignerTheorem.lean`, then `FiniteWignerSimilarity.lean`,
and `GaussRatAutomorphisms.lean`, with `build/BornEffectValuation.olean`, `build/BornGaussRat.olean`,
`build/BornHermitianCarrier.olean`, `build/BornHermitianPsdDecomposition.olean` and
`build/SectorFormHermitian.olean` restored first from a lake build of this branch under v4.35.0
(digests in `tools/restored_oleans.json` and `provenance.json`; the receipts of the earlier runs were
compiled under v4.33.1 and cannot be loaded by v4.35.0); then `python tools/seal.py receipts`,
`python tools/operads.py`, `python tools/provenance.py`, `python tools/companions.py`,
`python tools/dag_update.py`, the master record `TFQ-1047` in `dag/fragments/unified_dag.json`,
`python dag/sync_unified_dag.py`, `python dag/sync_application_branches.py`,
`python dag/sync_pregenesis_to_wdp.py`, `python tools/rebind_receipts.py`, `python tools/seal.py manifest`
and `python tools/seal.py verify`.
