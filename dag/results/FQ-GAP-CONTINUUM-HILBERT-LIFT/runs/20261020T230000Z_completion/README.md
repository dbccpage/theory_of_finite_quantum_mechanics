# Controlled Hilbert completion of the exact finite carriers — kernel-checked, with exact Python and Rust twins

Status: **constructed, compiled, sealed, stopped for review**. AuthorityEffect: None.

Starting point: the node statement (no continuum Hilbert space is constructed in any source),
the staged run [runs/20261019T145000Z_staged](../20261019T145000Z_staged/README.md) and the
[scope audit](../../reviews/20261019_scope_audit/README.md), which recorded "Construct an actual
completion with specified topology, carrier and embedding" as the remaining task. This run
constructs it: the carrier is the tower of exact finite carriers `Fin n → ℚ` and its directed
union `ℕ →₀ ℚ`; the topology is the rational ℓ² uniformity, stated with rational tolerances and
explicit moduli; the embedding is `lift 𝕜 : (ℕ →₀ ℚ) → UniformSpace.Completion (ℕ →₀ 𝕜)`; the
convergence hypothesis is the rational ℓ² Cauchy condition, discharged inside the completion.
The whole chain is kernel-checked (Lean 4.33.1, pinned Mathlib cache) and the exact-rational
half is replayed in Python and Rust.

- [HilbertLiftFiniteTower.lean](HilbertLiftFiniteTower.lean): exact finite carriers under zero
  padding (functorial, `ℚ`-linear, injective, inner-product preserving), the colimit carrier
  with canonical injections, the cocone identity, exhaustion, truncation, and Cauchy–Schwarz
  over `ℚ` (29 receipts).
- [HilbertLiftRationalUniformity.lean](HilbertLiftRationalUniformity.lean): ℓ², ℓ¹ and sup Cauchy
  conditions with rational tolerances, explicit moduli, the doubling triangle inequality, and the
  harmonic witness `h_N = Σ_{i<N} e_i/(i+1)`: ℓ²-Cauchy with modulus `k ↦ k+1`, not ℓ¹-Cauchy,
  convergent to no exact vector (28 receipts).
- [HilbertLiftCompletion.lean](HilbertLiftCompletion.lean): the inner-product core on `ℕ →₀ 𝕜`,
  the lift `UniformSpace.Completion (ℕ →₀ 𝕜)` as a complete inner product space, the explicit
  embeddings `lift`/`liftFin` with `⟪lift f, lift g⟫ = qinner f g`, `cauchySeq_lift_iff`,
  `exists_limit_of_isCauchyL2`, density over `ℝ`, `ext_of_lift`, strictness, and the packaged
  `controlled_completion` (38 receipts).
- [HilbertLiftComplexCarrier.lean](HilbertLiftComplexCarrier.lean): Gaussian-rational pairs
  `a + ib` in the complex lift, the exact inner-product identity, density, strictness, and
  `controlled_completion_complex` (17 receipts).
- Exact twins: [code/python/src/qm/hilbert_lift_completion.py](../../../../../code/python/src/qm/hilbert_lift_completion.py)
  with [16 tests](../../../../../code/python/tests/test_hilbert_lift_completion.py);
  [code/rust/src/qm/hilbert_lift_completion.rs](../../../../../code/rust/src/qm/hilbert_lift_completion.rs)
  with 14 inline tests (shape and stage errors are typed refusals). Both replay the finite
  tower, the colimit, Cauchy–Schwarz, the doubling triangle inequality, the harmonic bounds with
  the explicit modulus, the quantitative density step, and two mutation controls (unit vectors
  are not Cauchy; the shifted modulus fails); both add a modulus-based completion point with an
  exact inner-product fluctuation bound that is native only. The four modules are also installed
  under `lean4/` and registered in `lean4/lakefile.lean`.
- [Compile receipts](verification/) (one label per source, `tools/replay.py`),
  [kernel axioms](verification/kernel_axioms.json), [accepted modules](accepted_modules.json),
  [16 scoped operation records](operad_delta.json), [claim statuses](claim_status.json),
  [mathematical review and boundaries](review.md), [next derivations](next_steps.md),
  [prior-evidence digests](provenance.json), [validation](validation.json),
  [DAG node edit](tools/dag_update.py), [file seal](manifest.json).

Four accepted compilations, **112 printed axiom receipts**, every one within
`[propext, Classical.choice, Quot.sound]`; no accepted source contains `sorry`, `axiom`, `opaque`
or `unsafe`, and no compile output contains a warning. Prior sealed bundles, canonical operad
collections and monographs are unchanged. The DAG node `FQ-GAP-CONTINUUM-HILBERT-LIFT` keeps
status `CONDITIONAL`; its `source_status`, `lean` and `rust` references, `imported_structure`
and `bottleneck` were rewritten by `tools/dag_update.py` (structural validator: 197 nodes,
192 routes, 0 failures; the file-resolution validator reports the same 2062 pre-existing external
paths before and after).

**Review boundaries.** The scalar field (`ℝ` or `ℂ`) and the ℓ² uniformity are supplied, not
derived; the run proves that the uniformity is a genuine choice (`harmonic_separates_uniformities`)
and that the completion is strictly larger than the exact carrier, but nothing selects `ℓ²` or
`ℝ` from finite-theory primitives. Mathlib's Hausdorff completion is used through its universal
property; the identification with `ℓ²(ℕ)` and the completion of the exact carrier under its
intrinsic rational uniformity are listed as next steps. No operator, dynamics, Born pairing or
tensor structure is lifted. See [review.md](review.md).

The pinned Lean 4.33.1 compiler and the existing Mathlib cache of `lean4/` were used with
targeted imports. Replay in a fresh copy with
`python tools/replay.py SOURCE NEW_LABEL --lean PINNED_LEAN --project CONFIGURED_LEAN4_PROJECT`
in dependency order (HilbertLiftFiniteTower, HilbertLiftRationalUniformity,
HilbertLiftCompletion, HilbertLiftComplexCarrier), then `python tools/seal.py receipts` and
`python tools/seal.py verify`. On Windows keep the absolute path of the run directory short:
snapshot paths under `verification/<label>/` must stay below 260 characters, or Lean reports
"no such file or directory" on an existing file (see [validation.json](validation.json)).

No provider inference was used; the proofs were written in this session by the host. Commit and
push are reported in the pull request; no merge was performed.
