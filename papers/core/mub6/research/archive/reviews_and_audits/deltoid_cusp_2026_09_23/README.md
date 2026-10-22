# Exact certificate for the literal matrix in the cusp prompt

AuthorityEffect: None.

`stated region only; mints no authority`

## Input and scope

Baseline: `a4ae32f2201a92330c2a237490a545c6c7cee35d`, equal to freshly
fetched `origin/main` on 2026-09-23. The existing dirty `main` checkout was
preserved; this work is isolated on `codex/deltoid-cusp-certificate`.

Input attachment SHA256:
`8d8ec53ee42d94304210cf16e7935bb8628521f85210ae9eeb270d8a42c7d647`.

The literal matrix is **not a complex Hadamard matrix**. Its first two
unnormalized rows have inner product `2`, rather than `0`. Also, its first
column and that of the displayed Fourier matrix coincide, so their normalized
overlap squared is `1`, rather than `1/6`. These are exact entries in
[`input_audit.json`](input_audit.json), replayed by
`code/mub_verify/deltoid_cusp_input.py` (formerly `omega_engine/crates/mub_verify/`).

Consequently the result below concerns the **literal overlap equations in the
attachment**, and does not identify a singular deltoid cusp or an MU triple.
No alternative matrix was substituted. The baseline catalog receipt
`omega_engine/crates_rs/omega_mub/artifacts/mub_deltoid_cusps.json` describes
scalar hypocycloid enclosures and explicitly lists identification of the CHM
family/cusp chart as missing. The inspected `Szollosi_B6_family` is opaque;
`deltoid_cusp_extension_obstruction` requires a supplied curvature bound.

## Rational sources and the identity

Write each supplied matrix entry as `a + i sqrt(3) b`, with `a,b` rational.
Use `z = sqrt(6) u`, set `z_1=1`, and put
`z_k=x_k+i sqrt(3) t_k`. Thus the original imaginary coordinate is
`y_k=sqrt(3) t_k`. This is an invertible change of real coordinates; it avoids
the prompt's incorrect assertion that the original overlap polynomials all
have rational coefficients in `x,y`.

The coordinate order is `x2,t2,x3,t3,x4,t4,x5,t5,x6,t6`. For each supplied row,
define

```text
R = sum_k (a_k*x_k + 3*b_k*t_k)
T = sum_k (a_k*t_k - b_k*x_k)
overlap residue = R^2 + 3*T^2 - 6.
```

The seventeen sources are five unit residues `x_k^2+3*t_k^2-1`, six Fourier
residues, then six literal-D residues. The common all-ones row is retained
twice, exactly as in the prompt. Every expanded coefficient is provided in
`input_audit.json`, with rationals encoded as `[numerator, denominator]`.
The Fourier convention is `F[j,k]=omega^(j*k)` for `j,k=0,...,5`, so its first
row and column are all ones. The complete exponent tables are fixed in both
the receipt and the Lean input audit.

[`literal_certificate.json`](literal_certificate.json) supplies all seventeen
explicit multipliers. Each has degree at most two. Together they contain 856
nonzero terms and satisfy the exact polynomial identity

```text
-1 = sum_{j=0}^{16} multiplier_j * source_j.
```

No sum-of-squares terms are needed. The identity has total degree at most four.
It gives a unit-ideal certificate over the rationals and hence the reduced
Groebner basis `{1}` for this literal ideal, for any monomial order. Evaluating
the same identity at a common real or complex zero yields `-1=0`.
The certificate's source digest is
`817e812ce44a5f060e6fbc8be4aeca3b4e3afd3ccb7c775f71dd60f0ff15becc`.
These statements are restricted to the fixed sources in the receipt.

The verifier recomputes those sources from the complete exponent matrices,
checks identifiers/order/digest, expands every product using `Fraction`, and
compares every coefficient with the constant `-1`. Hashes or success flags
alone are not acceptance evidence.

## Lean theorem chain

The formal modules separate the literal calculation from the input's incorrect
Hadamard identification:

1. [`DeltoidCuspInputAudit.lean`](../../../../../../../lean4/DeltoidCuspInputAudit.lean)
   defines the complete matrices in `Complex`, checks the failed Gram entry,
   and establishes `supplied_D6_not_IsCH6`.
2. [`LiteralCuspCertificate.lean`](../../../../../../../lean4/LiteralCuspCertificate.lean)
   contains every polynomial and integer-denominator-cleared multiplier.
   `MUB6.LiteralCuspCertificate.identity` is checked by `ring`, and
   `no_common_zero` derives the contradiction when every residue vanishes.
3. [`DeltoidCuspLiteralSemantics.lean`](../../../../../../../lean4/DeltoidCuspLiteralSemantics.lean)
   relates each of the seventeen source polynomials to the norm square of the
   corresponding coordinate or matrix row amplitude. It reconstructs any
   dephased complex vector through the invertible real coordinate change.
4. [`DeltoidCuspPhaseReduction.lean`](../../../../../../../lean4/DeltoidCuspPhaseReduction.lean)
   handles multiplication by a common unit phase and the `sqrt(6)` scaling.
5. [`DeltoidCuspLiteralVector.lean`](../../../../../../../lean4/DeltoidCuspLiteralVector.lean)
   assembles `no_literal_unit_entry_vector` and
   `no_literal_normalized_vector`, without a phase-gauge hypothesis.

The normalized statement concerns any `u : Fin 6 → Complex` satisfying
`normSq (u k) = 1/6` and the displayed Fourier/literal-D row amplitudes having
norm square `1`. It makes no Hadamard or cusp-family assumption. See the replay
status below; all five modules passed their targeted builds.

## Replay

From the repository root, using Python 3.11 or later:

```powershell
PYTHONPATH=code python -m mub_verify.deltoid_cusp_input --verify-certificate research/deltoid_cusp_2026_09_23/literal_certificate.json
python research/deltoid_cusp_2026_09_23/generate_certificate.py --output scratch/reconstructed_literal_certificate.json
python research/deltoid_cusp_2026_09_23/generate_lean.py --output lean4/LiteralCuspCertificate.lean
python research/deltoid_cusp_2026_09_23/independent_replay.py
python -m pytest tests/mub_verify/test_deltoid_cusp_input.py -n 8 --basetemp=scratch/pytest_cusp_input -o cache_dir=scratch/pytest_cache_cusp_input
```

From `lean4/012_mutually_unbiased_bases`, the targeted build command is:

```powershell
lake build MUB.DeltoidCuspInputAudit MUB.LiteralCuspCertificate MUB.DeltoidCuspLiteralSemantics MUB.DeltoidCuspPhaseReduction MUB.DeltoidCuspLiteralVector
```

The certificate verifier uses the Python standard library. Tests additionally
need `pytest` and `pytest-xdist`. Exact symbolic independent replay used
SymPy 1.14.0; rational reconstruction uses python-flint 0.9.0.
The generator's row/column selections are untrusted hints. It solves an
861-by-861 rational subsystem of the 1122-by-1001 degree-four Macaulay matrix,
then checks the complete polynomial identity. No rank or acceptance claim
depends on the hints. Fresh reconstruction produced the same certificate
bytes, SHA256
`a1647d5b9cdb3af4de7790bf86d9092155f3827f255129ee331479475bb41a5e`.
Generated files use explicit LF line endings so the checked bytes also match
Git's stored bytes across platforms.

Completed validation:

- Complete exact identity replay: passed.
- Independent SymPy reconstruction from complex matrix entries: all seventeen
  source coefficient dictionaries match; expanded identity equals `-1`.
- Focused regression suite: 18 passed, including coefficient, source, variable,
  target, and malformed exact-data corruption controls.
- Full `tests/mub_verify` suite: 522 passed, 1 skipped, with eight workers and
  isolated `scratch/pytest_cusp_full` basetemp/cache. Transcript:
  `scratch/pytest_cusp_full.log` (ignored).
- Targeted `lake build MUB.DeltoidCuspInputAudit`: passed. Its fourteen printed
  axiom sets contain only `propext`, `Classical.choice`, and `Quot.sound`.
- Targeted `lake build MUB.LiteralCuspCertificate`: passed, including
  `MUB6.LiteralCuspCertificate.identity`, `no_common_zero`, and
  `no_common_zero_sources`. All three printed axiom sets contain only the same
  standard axioms. Transcript: `scratch/certificate_search/lean_identity.log`
  (ignored). Lean checks the integer-denominator-cleared identity by `ring`.
- Targeted `lake build MUB.DeltoidCuspPhaseReduction`: passed, including all
  nine printed theorem axiom checks, using only the same standard axioms.
- The generated Lean certificate reproduces byte for byte (also under
  `python -O`), SHA256
  `14603780b4a80e98a5dc227e4dbb345842e88f2464b5c0f39698b65d3fc050e5`.
- Targeted `lake build MUB.DeltoidCuspLiteralSemantics`: passed. All seventeen
  exact source-to-matrix links feed `no_phaseVector` and
  `no_dephased_literal_vector`; the printed transitive axiom dependencies are
  only the same three standard axioms.
- Final `lake build MUB.DeltoidCuspLiteralVector`: passed. Both
  `MUB.DeltoidCuspLiteralVector.no_literal_unit_entry_vector` and
  `MUB.DeltoidCuspLiteralVector.no_literal_normalized_vector` have only
  `[propext, Classical.choice, Quot.sound]`. The final build transcript,
  including dependency axiom reports, is
  `scratch/lean-premise/literal-vector-final-build.log` (ignored).
- The five new Lean modules contain no `sorry`, custom axiom declaration,
  or `native_decide`. This is a transitive trust check of these named results,
  not an assertion about every pre-existing repository theorem.
- After LF normalization, the combined five-target Lean build passed again;
  final transcript: `scratch/final-lean-build.log` (ignored). Both generators
  reproduced the final artifacts byte for byte under `python -O`, all eighteen
  focused tests passed again, and all fourteen staged files matched their
  working-file bytes. `git diff --cached --check` passed.

Lean version: `4.33.1`; Mathlib commit:
`0df444a360eaa60ab8c11dca51a86af692955474` (both checked live). The isolated
worktree reuses the existing package dependency cache through a junction at
`.lake/packages`, with its own `.lake/build` outputs. Existing dependency
caches were reused; this was not a cache-free Mathlib rebuild.

No pre-existing receipts, classification assertions, or closure flags were
altered. The named cusp mission requires an identified valid matrix in a
common gauge before this literal-system certificate can be interpreted as
anything about that cusp.
