# OpenAI's kernel-checked bound N(6) <= 5: recorded as an external, imported theorem

> **AuthorityEffect**: None. Dated 2026-10-21.
> Status in this repository: `IMPORTED_ASSUMPTION` (external theorem; not vendored; not built here).

## 1. The imported statement

Upstream repository: <https://github.com/openai/math>, commit
`1581d4cbdd69a0faf34b2089614fe2a814316a6a` (HEAD of `main` on 2026-10-21; merge of PR #2, 2026-10-12).
License: Apache License 2.0 (`LICENSE` at the repository root and in `lean/`).

Lean files (all under `lean/OAI/Analysis/MutuallyUnbiased/`), toolchain `leanprover/lean4:v4.34.1`,
Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`:

```lean
-- Model.lean
abbrev Coord := Fin 6
abbrev Space := EuclideanSpace ℂ Coord
abbrev Basis := OrthonormalBasis Coord ℂ Space
def IsMUBFamily {n : ℕ} (B : Fin n → Basis) : Prop :=
  ∀ r s, r ≠ s → ∀ i j, Complex.normSq (inner ℂ (B r i) (B s j)) = (1 : ℝ) / 6
def Attainable (n : ℕ) : Prop := ∃ B : Fin n → Basis, IsMUBFamily B

-- Results/Bounds.lean
theorem no_seven_mutually_unbiased_bases : ¬Attainable 7
theorem six_extend_to_seven : SixExtendToSeven          -- Weiner completion, Completion/Completion.lean
theorem family_size_le_five (n : ℕ) (hn : Attainable n) : n ≤ 5

-- Main.lean
theorem fourier_and_family_bound :
    (∀ H : CMatrix, IsHadamard H → ¬Equivalent H tao →
      ∀ π : Equiv.Perm Coord, g H (permuteCharge π alpha) = 0) ∧
    (∀ n : ℕ, Attainable n → n ≤ 5)
```

(namespace `OAI.MUB6`). The Lean tree is checked upstream against `ComparatorChallenges/MUBSix.json`
with only `propext`, `Quot.sound` and `Classical.choice` permitted. Upstream's `lean/docs/266.md` says that
the formalization proves "a weaker bound: every family in its mutually unbiased bases model has at most five
members" and "does not establish the paper's upper bound of three". `formalization.yaml` has no entry for
this family and its review field is `unchecked`.

## 2. Why it is not vendored or built here

- **License**: Apache 2.0 permits copying with attribution. That is not the obstacle.
- **Size**: the import closure of `Main` and `Results/Bounds` is 3381 Lean files and about 205 MB of source
  (compressing to about 17 MB), dominated by generated certificate data (`MixedSemantics` 121 MB,
  `GramRows` 23 MB, `PairSemantics` 22 MB). That is not a reasonable addition to this repository.
- **Toolchain**: upstream pins Lean 4.34.1 and its own Mathlib commit. This repository is on Lean 4.35.0
  and Mathlib v4.35.0. A build would need either the upstream pinned environment or a port; the
  mismatch is recorded, not worked around.
- **Resources**: the machine ran out of disk during this work. Building the closure was stopped before it
  began, on the coordinator's instruction.

What was checked before stopping, under this repository's Lean 4.35.0 and Mathlib v4.35.0 (no output
messages, exit code 0): upstream `Model.lean` (356 s, includes the cold `import Mathlib`) and
`Tao/Tao.lean` (228 s). So the model layer has no toolchain mismatch. The heavy certificate layer
(`MixedSemantics`, `Gram*`, `Pair*`) was not attempted. Nothing here is a replay of the upstream proof.

## 3. What this repository does with it

`lean4/MubOpenAIBridge.lean` (build **pending**; not a lake root) states the imported bound as the Prop
`OpenAIFamilyBound := ∀ n, OAI.MUB6.Attainable n → n ≤ 5`, proves that `OAI.MUB6.Attainable n` is the
existence of an `n`-member pairwise-MU family of unitary `6 x 6` matrices
(`ConcreteMubPolynomialSystem.Candidate`, `SzollosiQuartetSystem.Quartet` form), proves
`RawMU H U <-> normalised 1/6 overlap` for the repository's raw Hadamard form, and concludes
`mub6_family_le_five (h : OpenAIFamilyBound) : MatrixMUBFamily B -> n <= 5`. The conclusion is therefore
**conditional on the imported theorem**. It is not "PROVED_LEAN" in this repository.

It also states `tao_phase_bridge`: `Conjecture2GeneralMechanization.phaseTable (p i) (p j) = taoExponent i j`
for the involution `p = (3 5)`. This was verified by exhaustive search in Python
(`phaseTable r c = taoExponent` after reindexing; 20 (permutation, sign) solutions exist, `p = [0,1,2,5,4,3]`
with sign +1 is one). The Lean statement has not been compiled. It lets `MUB6-DERIV-076` cite OpenAI's
Fourier-vanishing theorem as stated for `tao`: the repository's `taoNormSq = 9` evaluation (all 20 balanced
masks) concerns the exceptional class of that theorem.

## 4. External context (not imported)

OpenAI's main paper claims N(6) = 3 (no four MUBs in C^6) by a classification-free seed cover, Stages A, B
and C and a clique search, evaluated in binary64 by seven C++ files. The code and run archive are not in the
public repository (the `verification/` tree returns HTTP 404 on 2026-10-21), and the Lean tree does not
formalize it. It is recorded as external context only. `MUB6-NO-QUARTET-D6` and
`MUB6-MAX-MUB-SIX-EQUALS-THREE` remain OPEN. See the corrected comparison in
`mub6_master_classification_and_openai_comparative_synthesis.md`.
