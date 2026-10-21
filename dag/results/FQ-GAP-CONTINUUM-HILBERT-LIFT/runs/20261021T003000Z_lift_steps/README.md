# Intrinsic uniformity, ℓ² model, operator lift and DAG split — the next steps of the controlled completion

Status: **constructed, compiled, sealed, stopped for review**. AuthorityEffect: None.

This run carries out items 2 to 6 of [runs/20261020T230000Z_completion/next_steps.md](../20261020T230000Z_completion/next_steps.md)
(item 1, the Gaussian-rational carrier, was already discharged there by `HilbertLiftComplexCarrier`).
The four modules of that run are copied byte for byte into this directory and re-replayed first, so the
bundle is self-contained; three new modules follow.

- [HilbertLiftIntrinsicUniformity.lean](HilbertLiftIntrinsicUniformity.lean) (item 2, 16 receipts): the
  exact carrier `ℕ →₀ ℚ` carries the uniformity whose entourages are the rational squared-distance balls;
  `uniformity_eq_iInf_sqdist` identifies the uniformity filter with the infimum of those principal
  filters (no real number in the description), `cauchySeq_iff_isCauchyL2` identifies its Cauchy sequences
  with the rational ℓ²-Cauchy sequences, and `completionEquivLift : Completion Carrier ≃ᵤ HilbertLiftSpace ℝ`
  shows that the Hausdorff completion of the exact carrier under this uniformity is the real Hilbert lift,
  restricting to `lift ℝ` on exact vectors.
- [HilbertLiftL2Model.lean](HilbertLiftL2Model.lean) (item 3, 15 receipts): the coordinate map
  `ℕ →₀ 𝕜 → lp (fun _ => 𝕜) 2` is a linear isometry preserving the inner product with dense range
  (`lp.hasSum_single`), and extends to `liftEquivL2 : HilbertLiftSpace 𝕜 ≃ₗᵢ[𝕜] ℓ²(ℕ, 𝕜)` under which an exact
  vector is its own coordinate sequence (`liftEquivL2_lift_apply`).
- [HilbertLiftOperators.lean](HilbertLiftOperators.lean) (item 4, 25 receipts): a `BoundedExactOperator`
  (a `ℚ`-linear map `A` with `qinner (A f) (A f) ≤ C qinner f f`) is uniformly continuous for the intrinsic
  uniformity, preserves rational ℓ²-Cauchy sequences, and extends uniquely to a continuous `ℝ`-linear
  operator `toCLM` on the real lift with `‖T x‖² ≤ C ‖x‖²` and `‖T‖ ≤ √C`; the stage projections (bound 1,
  Bessel) and the unilateral shift (isometric, `norm_shift_liftOp`) are examples; the `ℚ`-linear
  coordinate-sum functional admits no continuous extension (`no_continuous_extension_coordSum`) although
  the harmonic vectors it diverges on keep squared norm at most 2 (`qinner_harmonic_le_two`).
- Item 5, the DAG split: [tools/dag_update.py](tools/dag_update.py) adds the node
  `FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION` (status `PROVED_LEAN`, with the scalar field and the ℓ²
  uniformity named in `imported_structure`), a route to it from `FQ-CARRIER-CONTRACT-V2`
  (`CONDITIONAL_ON_IMPORT`), and a `GAP_NO_DERIVATION` route from it to `FQ-GAP-CONTINUUM-HILBERT-LIFT`,
  whose statement, source_status, bottleneck and see_also now record that only the selection of the two
  hypotheses remains there (status `CONDITIONAL` unchanged).
- Item 6: the Python twin now carries a locked certificate entry point `certify()` returning the harmonic
  gap `coordSum (h₂) − coordSum (h₁) = 1/2` (`coordSum_harmonic_gap` at `n = 1`) with the shared refusal
  boundary, and a `Certificate` row in `code/python/src/qm/tests/test_isolated_certificates.py`; the atlas
  row was not added because `scripts/verify_qm_atlas_loc.py` fixes the question count at 65 and would need
  a coordinated change of the Python and Rust atlases.
- Exact twins extended: [code/python/src/qm/hilbert_lift_completion.py](../../../../../code/python/src/qm/hilbert_lift_completion.py)
  (bounded-operator certificates, Lipschitz consequence, transported Cauchy modulus, shift, stage
  projection, coordinate sum and its harmonic gap, bounded harmonic norms, `certify`/`main`; 20 tests) and
  [code/rust/src/qm/hilbert_lift_completion.rs](../../../../../code/rust/src/qm/hilbert_lift_completion.rs)
  (the same, 18 inline tests of which the 4 new ones are **unverified in this session**: the cargo
  build was stopped twice by the host, once for a full disk and once by the session supervisor for low
  memory, and was not restarted; the 14 earlier tests passed before the extension). The three new
  modules are installed under `lean4/` and registered in `lean4/lakefile.lean`.
- [Compile receipts](verification/) (seven labels, `tools/replay.py`), [kernel axioms](verification/kernel_axioms.json),
  [accepted modules](accepted_modules.json), [7 scoped operation records HL-17 to HL-23](operad_delta.json),
  [claim statuses](claim_status.json), [mathematical review and boundaries](review.md),
  [remaining derivations](next_steps.md), [prior-evidence digests](provenance.json),
  [validation](validation.json), [file seal](manifest.json).

Seven accepted compilations, **168 printed axiom receipts** (112 re-replayed, 56 new), every one within
`[propext, Classical.choice, Quot.sound]`; no accepted source contains `sorry`, `axiom`, `opaque` or
`unsafe`, and no compile output contains a warning. The sealed prior run is unchanged.

**Review boundaries.** The scalar field and the ℓ² uniformity remain supplied; the intrinsic-uniformity
module removes the real numbers from the *domain* of the completion but its target is still the real lift.
The operator lift is stated over `ℝ` only; the complex case (Gaussian-rational pairs) is listed in
`next_steps.md`. The bound `C` of an exact operator is a hypothesis; nothing selects physical operators,
and no dynamics or generator is lifted. The uniform structure on `ℕ →₀ ℚ` is a global instance on an
abbreviation (as `PreH 𝕜` already was). See [review.md](review.md).

Replay in a fresh copy with `python tools/replay.py SOURCE NEW_LABEL --lean PINNED_LEAN --project CONFIGURED_LEAN4_PROJECT`
in the order HilbertLiftFiniteTower, HilbertLiftRationalUniformity, HilbertLiftCompletion,
HilbertLiftComplexCarrier, HilbertLiftIntrinsicUniformity, HilbertLiftL2Model, HilbertLiftOperators, then
`python tools/seal.py receipts` and `python tools/seal.py verify`; keep the absolute run path short enough
that `verification/<label>/<Source>.lean` stays below 260 characters on Windows.

No provider inference was used; the proofs were written in this session by the host. Commit and push are
reported in the pull request; no merge was performed.
