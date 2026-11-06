# Remaining derivations after this run

Items 2 to 6 of the prior run's list are done here (item 1 was done by `HilbertLiftComplexCarrier`;
the optional atlas row of item 6 is not, see `claim_status.json`). What remains:

1. Complex operators: restate `BoundedExactOperator` for pairs `(a, b)` of exact sequences acting on
   `liftPair`, with the Gaussian-rational inner product of `HilbertLiftComplexCarrier`, and lift to
   `HilbertLiftSpace ℂ`; the intrinsic uniformity on pairs (`sqdist a c + sqdist b d`) and
   `Completion (Carrier × Carrier) ≃ᵤ HilbertLiftSpace ℂ` follow the real pattern.
2. Selection of the hypotheses (the content left at `FQ-GAP-CONTINUUM-HILBERT-LIFT`): a finite-theory
   argument that picks the ℓ² uniformity (for instance from the finite-stage inner product supplied by
   the report contract and a stability requirement under refinement) and the scalar field; or a proof
   that no such selection is available below the continuum.
3. Dynamics: a padding-compatible family of bounded exact operators `U_n` with `qinner (U_n f) (U_n f)
   = qinner f f` lifts to isometries; a one-parameter structure and a generator are the open content of
   `FQ-GAP-STONE-CONTINUOUS-TIME`, to which `BoundedExactOperator` now supplies the lifted carrier.
4. Atlas row: add a `Q66` entry for the Hilbert lift to `docs/QM_PROBLEM_AND_PROOF_ATLAS.md` together
   with `build_qm_question_atlas` in Python and Rust and the count in `scripts/verify_qm_atlas_loc.py`.
5. Instance hygiene: if any future module places a uniform or normed structure on `Finsupp`, wrap
   `Carrier` and `PreH 𝕜` in structures instead of abbreviations.
