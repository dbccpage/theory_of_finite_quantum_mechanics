# Mathematical review and boundaries

AuthorityEffect: None.

## The question

The L1 to L2 lift imports its dynamics: "dynamics on the lift are reversible linear isometries"
(node L1-IMP-LINEAR-ISOMETRIC-DYNAMICS, QM_020 Thm 6 assumption 5). QM_122 H003 shows that a
deterministic report update need not be reversible, and H006 shows that a reversible report update
extends to a permutation isometry of the admitted form, which is not a Hilbert unitary. The sector-form
run (`L1-IMP-HILBERT-INNER-PRODUCT`, run 20261021T013500Z) fixed the inner product of the exact carrier
up to a unit scale, and its next step 2 asked for the dynamics: with the form fixed, which maps of the
carrier preserve it, and can "linear" and "isometric" be derived rather than imported?

The answer offered here is Wigner's theorem in its finite exact form. The transition probability
`tp x y = |⟨x, y⟩|² / (‖x‖² ‖y‖²)` does not see the scale of the form, and it is the normalised Born
readout of the rank-one effect `P x` in the state `y` (`tp_eq_born`, with `P` and `hf` of
`BornHermitianCarrier`). So the operational hypothesis "the dynamics preserves the Born probabilities
of rank-one effects between rays" is exactly the hypothesis of Wigner's theorem, and over the exact
carrier `Fin n → ℚ(i)` the theorem can be proved without any continuity.

## What is established

Let `V = Fin n → ℚ(i)` with `ip x y = star x ⬝ᵥ y`, `vnorm x = re (ip x x)` and `tp` as above.

- **Theorem** (`finite_wigner`). Let `T : V → V` send nonzero vectors to nonzero vectors and preserve
  `tp` between nonzero vectors (`TpPreserving`). Fix a sector `i₀`. Then there are a matrix `F` with
  `Fᴴ F = d • 1` for a positive rational `d` (`Similarity`) and a sign `ε ∈ {1, −1}` such that for
  every nonzero `x` there is a nonzero scalar `μ` with `T x = μ • (F *ᵥ twist ε x)`, where
  `twist 1 x = x` and `twist (−1) x = star x`. Equivalently (`finite_wigner_cases`) `T` is induced on
  rays by a ℚ(i)-linear similarity or by componentwise conjugation followed by one. Conversely every
  such map preserves `tp` (`tpPreserving_of_similarity`), and `x ↦ F *ᵥ twist ε x` is a bijection of
  the carrier with inverse built from `(1 / d) • Fᴴ` (`similarity_bijective`, `Similarity.inverse`):
  the dynamics is reversible and linear or antilinear, isometric up to the scale `d`
  (`Similarity.ip_mulVec`, `similarity_hf_one_mulVec`).
- **Proof shape** (Bargmann-type, exact). The images `g i = T (e i)` of the sector basis are nonzero
  and pairwise orthogonal because `tp (e i) (e j) = 0` and `tp = 0` iff `ip = 0` (`ip_g_g`); every
  vector expands in such a family because a left inverse of a square matrix over ℚ(i) is a right
  inverse (`expansion`, via `mul_eq_one_comm`). The images of the probes `e i₀ + e j` fix the phases
  and norms of the basis images (`T_p_eq`, `vnorm_f`), giving the similarity `F` (`similarity_F`).
  The images of the probes `e i₀ + i e j` carry a sign `sgn j ∈ {±1}` (`sgn_spec`), and the probe
  `e i₀ + i e j + i e k` forces all signs equal (`sgn_consistent`). For `x` with `x i₀ ≠ 0`, the
  normalised coordinates of `T x` in `F` are pinned coordinatewise by the three probe families
  (`coord_rigidity`: equal modulus from `e m`, equal real part from `e i₀ + e m`, imaginary part up to
  the sign from `e i₀ + i e m`; `stage1`). For `x` with `x i₀ = 0`, the probe `e i₀ + x` and the
  equality case of Cauchy–Schwarz over ℚ(i) finish (`eq_smul_of_normSq_ip_eq`, `stage2`).
- **No continuity.** The usual proofs over ℂ either assume continuity of the ray map or invoke the
  fundamental theorem of projective geometry and then need that the only continuous automorphisms of
  ℂ are the identity and conjugation. Over ℚ(i) the coordinate dichotomy `z m = x m` or
  `z m = star (x m)` is forced by two modulus equations, so nothing is assumed; and for the record,
  every ring homomorphism `ℚ(i) → ℚ(i)` is the identity or conjugation
  (`GaussRatAutomorphisms.ringHom_eq_id_or_star`), so the antiunitary case over the exact carrier is
  exactly "conjugate, then apply a linear map".
- **Unitary iff the scale is a norm** (`exists_unitary_iff`). `F` is a scalar multiple of a
  ℚ(i)-unitary iff `d = a² + b²` for rationals `a, b` (`norm_iff_sum_two_sq`). `3` is not such a sum
  (`three_not_sum_two_sq`, descent modulo 3 over ℤ), and `F3 = [[1, −1 + i], [1 + i, 1]]` has
  `F3ᴴ F3 = 3 • 1` (`F3_similarity`): its ray map preserves transition probabilities
  (`F3_tpPreserving`) but is induced by no ℚ(i)-unitary (`F3_not_induced_by_unitary`, via
  `eq_smul_one_of_rays`: a matrix fixing every ray is a scalar) and by no ℚ(i)-antiunitary
  (`F3_not_induced_by_antiunitary`). Over the exact carrier "unitary or antiunitary" is therefore
  strictly stronger than what transition-probability preservation gives; the honest finite statement
  is "linear or conjugate-linear similarity".
- **The permutation envelope** of H006 is the unitary `permMatrix σ` (`permMatrix_mulVec`,
  `permMatrix_unitary`): the only dynamics the finite theory supplied so far is a special case of the
  derived class.

The Python and Rust twins replay the chain on supplied data: the probe-driven reconstruction of
`(F, d, ε)` with an exact witness for whichever step fails, verification that a map is induced by its
reconstruction on sample vectors, the similarity and unitary-normalisation certificates (sums of two
rational squares with an obstructing prime `≡ 3 mod 4`), the countermodel `F3`, the Hadamard matrix
(`d = 2 = |1 + i|²`, hence unitary after rescaling) and the permutation matrices.

## Consequence for the dynamics node

Given the inner product up to scale (sector-form run) and the Born readout of rank-one effects (Born
runs), the single operational law "the ray dynamics preserves transition probabilities" yields
linearity (or antilinearity), reversibility and isometry up to a positive rational scale. The node
moves from IMPORTED_ASSUMPTION to CONDITIONAL on that law (node L1-IMP-TRANSITION-PROBABILITY-LAW),
with the correction that the imported form "isometry" is a similarity on the exact carrier, unitary
only under the arithmetic condition that the scale is a norm from ℚ(i).

## What is supplied, not derived

- The carrier `Fin n → ℚ(i)`, the scalar field and the quadratic readout are inputs (nodes
  L1-IMP-HILBERT-INNER-PRODUCT, L1-IMP-COMPLEX-FIELD); nothing derives them from primitive difference.
- Transition-probability preservation is a hypothesis. The finite theory gives no reason yet why a
  dynamics must preserve the Born readout of rank-one effects; H003 shows determinism alone does not
  even give reversibility.
- The scale `d` is removable only when it is a sum of two rational squares; the theorem does not
  select a unitary, and the countermodel shows it cannot.
- Continuous time (a ℚ-parameter group through a given step) remains the Stone gap
  (`FQ-GAP-STONE-CONTINUOUS-TIME`); nothing here concerns generators.
- No real numbers, no complex numbers, no limits: everything is exact over ℤ, ℚ and ℚ(i).

## Mechanical notes

Lean 4.35.0 with the Mathlib cache `56a00585` of the lean-v4-35 project, targeted imports; accepted
receipts `k01` (`FiniteWignerKernel`), `t01` (`FiniteWignerTheorem`), `s01`
(`FiniteWignerSimilarity`) and `a01` (`GaussRatAutomorphisms`; its receipt was taken against the
same Mathlib commit's cache in the sibling worktree `C:/t/cfs/lean4`, because the lean-v4-35 cache
was removed by another session while this run was sealing) by `tools/replay.py` with the oleans of
`BornEffectValuation`, `BornGaussRat`, `BornHermitianCarrier`, `BornHermitianPsdDecomposition` and
`SectorFormHermitian` restored into `build/` from the lake build of the lean-v4-35 branch (their
sources are byte-identical to the `lean4/` copies of this branch, digests in `provenance.json`);
`tools/seal.py receipts` checks exit codes, custody digests, absence of `sorry`/`axiom`/`opaque`/
`unsafe`, absence of diagnostics, and that every printed axiom list is within
`{propext, Classical.choice, Quot.sound}`. No noncomputable definitions are introduced; the sign `ε`
is produced inside the existence proof by case analysis, not by a choice function in a definition.
