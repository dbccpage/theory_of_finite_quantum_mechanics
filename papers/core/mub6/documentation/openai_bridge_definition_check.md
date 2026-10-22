# Symbol-by-Symbol Definition Check: `lean4/MubOpenAIBridge.lean` Against Upstream `openai/math`

> **AuthorityEffect**: None.
> **Audit Date**: 2026-10-22
> **Branch**: `gemini/openai-bridge-check`
> **Upstream Repository**: `https://github.com/openai/math` (shallow clone outside the repository, deleted after comparison)
> **Pinned Upstream Commit**: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`
> **Local Bridge File**: `lean4/MubOpenAIBridge.lean` (SHA-256: `b1e325ed5a5ade354736155489d05860d51d8ec2c453b0efe424493b020e12e1`)
> **DAG Node Status**: `MUB6-OPENAI-FAMILY-LE-FIVE` remains `IMPORTED_ASSUMPTION`

---

## 1. Executive Summary & Claim Hygiene

This report records a symbol-by-symbol audit of the six upstream definitions restated in `lean4/MubOpenAIBridge.lean` (namespace `MUB.OpenAIBridge.OAIModel`) and the hypothesis `OpenAIFamilyBound` against the pinned upstream commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a` of `https://github.com/openai/math`.

All six definitions in `MUB.OpenAIBridge.OAIModel` (`Coord`, `Space`, `Basis`, `IsMUBFamily`, `Attainable`, `taoExponent`) match `lean/OAI/Analysis/MutuallyUnbiased/Model.lean` (and `lean/ComparatorChallenges/MUBSix.lean`) character for character, including types, implicit and explicit binders, index sets, normalisation constants, and matrix entries. The hypothesis `OpenAIFamilyBound` matches the second conjunct of `OAI.MUB6.fourier_and_family_bound` in `lean/OAI/Analysis/MutuallyUnbiased/Main.lean` character for character (modulo the `OAIModel.` namespace prefix on `Attainable`) and is definitionally equal to the proposition of `OAI.MUB6.family_size_le_five` in `lean/OAI/Analysis/MutuallyUnbiased/Results/Bounds.lean`. Because zero mismatches were found, no edit to `lean4/MubOpenAIBridge.lean` or `papers/core/mub6/documentation/mub_openai_bridge_compile_receipt.md` was needed.

### Claim Hygiene Summary

1. **What it supports:** The six definitions restated in `MUB.OpenAIBridge.OAIModel` (`Coord`, `Space`, `Basis`, `IsMUBFamily`, `Attainable`, `taoExponent`) and the proposition `OpenAIFamilyBound` in `lean4/MubOpenAIBridge.lean` match their upstream counterparts in `openai/math` at commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a` symbol for symbol.
2. **What it does not support:** This definition audit does not replay or verify the upstream 3,381-file certificate closure of `OAI.MUB6.family_size_le_five` inside this repository, nor does it establish $N(6) \le 5$ or $N(6) = 3$ as an internal theorem of this repository.
3. **Narrowest defensible claim:** Under the pinned upstream definitions at commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a`, the conditional theorems `MUB.OpenAIBridge.mub6_family_le_five` and `MUB.OpenAIBridge.mub6_card_le_five` in `lean4/MubOpenAIBridge.lean` take as their premise the exact `Attainable` predicate and bound statement used in `lean/OAI/Analysis/MutuallyUnbiased/Model.lean` and `lean/OAI/Analysis/MutuallyUnbiased/Results/Bounds.lean`.
4. **Next test needed:** If a full standalone verification of the upstream proof closure is desired in the future, replay `OAI.Analysis.MutuallyUnbiased.Main` in an isolated external environment pinned to upstream's `leanprover/lean4:v4.34.1` toolchain and Mathlib commit `d13f23b723b8a846827a245b89c10fc7d3f11612`.

---

## 2. Upstream Files Inspected at Commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a`

The upstream repository was shallow-fetched at commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a` into a temporary directory outside the repository (`C:\gw\oai_math_tmp`), inspected, and deleted immediately afterwards.

| Upstream Path | Lines | LF-Normalized SHA-256 | Role in Upstream `OAI.MUB6` |
|---|---|---|---|
| `lean/OAI/Analysis/MutuallyUnbiased/Model.lean` | 60 | `ce243d2537bca07981e1adc9ae8cde829600dc0a8278b4ec32c14f0e96945c24` | Defines `Coord`, `CMatrix`, `Charge`, `IsHadamard`, `character`, `g`, `alpha`, `permuteCharge`, `Equivalent`, `omega`, `taoExponent`, `tao`, `Space`, `Basis`, `IsMUBFamily`, `Attainable` |
| `lean/OAI/Analysis/MutuallyUnbiased/Results/Bounds.lean` | 45 | `f0f39c93d2caad4ec8cddb3dcd820f2aa71dce633754be1fb6a0fe0eb9c3156d` | States `no_seven_mutually_unbiased_bases`, `six_extend_to_seven`, `family_size_le_five`, and `N6_le_five` |
| `lean/OAI/Analysis/MutuallyUnbiased/Main.lean` | 33 | `13495f1c2248552ad2766a12b80e5593cf682dab271a24c7b9f7df7052f724d4` | Combines `fourier_vanishing` and `family_size_le_five` into `fourier_and_family_bound` |
| `lean/OAI/Analysis/MutuallyUnbiased/Tao/Tao.lean` | 95 | `31ac70b4a7fc922c14f856c86884bfc8271f716baae619ed14082f6843ddfd8b` | Establishes `tao_isHadamard : IsHadamard tao` and `tao_square_isHadamard` |
| `lean/OAI/Analysis/MutuallyUnbiased/Bases/Basic.lean` | 19 | `2e1c872629eefad47a6a3932839d2fbf084ee82dfd726fda2281cf1a5ff84212` | Defines `N6 : ℕ := sSup {n : ℕ | Attainable n}` |
| `lean/OAI/Analysis/MutuallyUnbiased/Bases/Families.lean` | 52 | `d93fdd429fbd574a6945540635aa8f60237423d23a57b904cabb3584b81f500e` | Defines `SixExtendToSeven` and establishes `family_size_le_five_of_no_six` |
| `lean/ComparatorChallenges/MUBSix.lean` | 66 | `7a634ee492b54abe357901a69272c42aa8dfc85b7a3401eef723468bb0c6c355` | Comparator challenge specification repeating `Model.lean` definitions verbatim |
| `lean/ComparatorChallenges/MUBSix.json` | 14 | `44b6a812682454988656f7c4cc85629d1cba5b3725f8cf3c03677c4f2535358f` | Challenge config (`permitted_axioms`: `propext`, `Quot.sound`, `Classical.choice`) |

---

## 3. Per-Definition Symbol-by-Symbol Comparison Table

All upstream definitions below reside in `namespace OAI` / `namespace MUB6` (`OAI.MUB6`), within a `noncomputable section` with `open scoped BigOperators ComplexConjugate`. All local restated definitions reside in `namespace MUB.OpenAIBridge` / `namespace OAIModel` (`MUB.OpenAIBridge.OAIModel`), within a `noncomputable section` with `open scoped BigOperators ComplexConjugate`.

| # | Symbol | Upstream Location (`openai/math`) | Local Location (`lean4/MubOpenAIBridge.lean`) | Verdict | Explanation (Types, Binders, Normalisation, Index Sets) |
|---|---|---|---|---|---|
| 1 | `Coord` | `Model.lean:10`, `MUBSix.lean:10` | Line 45 | **MATCH** | Both write `abbrev Coord := Fin 6` character for character. `Coord` is the 6-element index type `Fin 6` used for coordinates and basis vectors. |
| 2 | `Space` | `Model.lean:47`, `MUBSix.lean:47` | Line 47 | **MATCH** | Both write `abbrev Space := EuclideanSpace ℂ Coord` character for character. In Mathlib, `EuclideanSpace ℂ Coord` is `PiLp 2 (fun _ : Coord => ℂ)` equipped with the standard $\ell^2$ inner product `inner ℂ x y = ∑ k, conj (x k) * y k`. |
| 3 | `Basis` | `Model.lean:48`, `MUBSix.lean:48` | Line 48 | **MATCH** | Both write `abbrev Basis := OrthonormalBasis Coord ℂ Space` character for character. Every `b : Basis` is an orthonormal family of 6 unit vectors in `Space` (`⟪b i, b j⟫_ℂ = if i = j then 1 else 0`). |
| 4 | `IsMUBFamily` | `Model.lean:50-52`, `MUBSix.lean:50-52` | Lines 50–52 | **MATCH** | Both write `def IsMUBFamily {n : ℕ} (B : Fin n → Basis) : Prop := ∀ r s, r ≠ s → ∀ i j, Complex.normSq (inner ℂ (B r i) (B s j)) = (1 : ℝ) / 6` character for character. Implicit binder `{n : ℕ}`, explicit family binder `(B : Fin n → Basis)`, distinct family indices `r s : Fin n` (`r ≠ s`), basis vector indices `i j : Coord`, and normalised squared overlap `(1 : ℝ) / 6`. |
| 5 | `Attainable` | `Model.lean:54`, `MUBSix.lean:54` | Line 54 | **MATCH** | Both write `def Attainable (n : ℕ) : Prop := ∃ B : Fin n → Basis, IsMUBFamily B` character for character. Explicit binder `(n : ℕ)`, existential over `Fin n → Basis`. |
| 6 | `taoExponent` | `Model.lean:35-43`, `MUBSix.lean:35-43` | Lines 56–64 | **MATCH** | Both write the identical docstring and `def taoExponent : Matrix Coord Coord ℕ := !![0, 0, 0, 0, 0, 0; 0, 0, 1, 2, 2, 1; 0, 1, 0, 1, 2, 2; 0, 2, 1, 0, 1, 2; 0, 2, 2, 1, 0, 1; 0, 1, 2, 2, 1, 0]` character for character across all 36 entries. |
| 7 | `OpenAIFamilyBound` | `Main.lean:25`, `MUBSix.lean:59`, `Results/Bounds.lean:32` | Line 215 | **MATCH** | Local `def OpenAIFamilyBound : Prop := ∀ n : ℕ, OAIModel.Attainable n → n ≤ 5` matches the second conjunct `(∀ n : ℕ, Attainable n → n ≤ 5)` of `OAI.MUB6.fourier_and_family_bound` (`Main.lean:25`) and the type of `OAI.MUB6.family_size_le_five (n : ℕ) (hn : Attainable n) : n ≤ 5` (`Results/Bounds.lean:32`). |

---

## 4. Exact Code Side-by-Side Verification

### 4.1 Upstream `lean/OAI/Analysis/MutuallyUnbiased/Model.lean` (lines 10, 35–55)

```lean
abbrev Coord := Fin 6
...
/-- The five-cycle exponent matrix in equation (cubic-matrix).
The entries 2 represent the exponents -1 modulo three. -/
def taoExponent : Matrix Coord Coord ℕ :=
  !![0, 0, 0, 0, 0, 0;
     0, 0, 1, 2, 2, 1;
     0, 1, 0, 1, 2, 2;
     0, 2, 1, 0, 1, 2;
     0, 2, 2, 1, 0, 1;
     0, 1, 2, 2, 1, 0]

def tao : CMatrix := fun i j => omega ^ taoExponent i j

abbrev Space := EuclideanSpace ℂ Coord
abbrev Basis := OrthonormalBasis Coord ℂ Space

def IsMUBFamily {n : ℕ} (B : Fin n → Basis) : Prop :=
  ∀ r s, r ≠ s → ∀ i j,
    Complex.normSq (inner ℂ (B r i) (B s j)) = (1 : ℝ) / 6

def Attainable (n : ℕ) : Prop := ∃ B : Fin n → Basis, IsMUBFamily B
```

### 4.2 Local `lean4/MubOpenAIBridge.lean` (lines 43–66, 215)

```lean
namespace OAIModel

abbrev Coord := Fin 6

abbrev Space := EuclideanSpace ℂ Coord
abbrev Basis := OrthonormalBasis Coord ℂ Space

def IsMUBFamily {n : ℕ} (B : Fin n → Basis) : Prop :=
  ∀ r s, r ≠ s → ∀ i j,
    Complex.normSq (inner ℂ (B r i) (B s j)) = (1 : ℝ) / 6

def Attainable (n : ℕ) : Prop := ∃ B : Fin n → Basis, IsMUBFamily B

/-- The five-cycle exponent matrix in equation (cubic-matrix).
The entries 2 represent the exponents -1 modulo three. -/
def taoExponent : Matrix Coord Coord ℕ :=
  !![0, 0, 0, 0, 0, 0;
     0, 0, 1, 2, 2, 1;
     0, 1, 0, 1, 2, 2;
     0, 2, 1, 0, 1, 2;
     0, 2, 2, 1, 0, 1;
     0, 1, 2, 2, 1, 0]

end OAIModel
...
def OpenAIFamilyBound : Prop := ∀ n : ℕ, OAIModel.Attainable n → n ≤ 5
```

---

## 5. Normalisation, Index Sets, and Convention Bridge Analysis

1. **Orthonormal Basis Normalisation (`1/6` Squared Overlap) vs. Unnormalised Hadamard Scaling (`1` Entry Norm, `6` Gram Diagonal):**
   - In upstream `Model.lean`, two distinct conventions appear for two distinct roles:
     - **Unnormalised Complex Hadamard Matrices (`IsHadamard`):** Lines 14–16 define `IsHadamard (H : CMatrix) : Prop := (∀ i j, Complex.normSq (H i j) = 1) ∧ H.conjTranspose * H = (6 : ℂ) • (1 : CMatrix)`. Here entries have modulus $1$ (`normSq = 1`) and columns have squared norm $6$. This is the convention used in the first conjunct of `fourier_and_family_bound` (`∀ H : CMatrix, IsHadamard H → ¬Equivalent H tao → ...`).
     - **Orthonormal Basis Families (`Basis`, `IsMUBFamily`, `Attainable`):** Lines 47–54 define `Basis := OrthonormalBasis Coord ℂ Space`, where each vector `B r i` has $\ell^2$ norm $1$, and `IsMUBFamily` requires `Complex.normSq (inner ℂ (B r i) (B s j)) = (1 : ℝ) / 6` for `r ≠ s`.
   - In `lean4/MubOpenAIBridge.lean`:
     - `MatrixMUBFamily` (lines 74–76) uses unitary $6 \times 6$ matrices `(B a).conjTranspose * B a = 1` with `Complex.normSq (((B a).conjTranspose * B b) i j) = 1 / 6` for `a ≠ b`. Because the columns of a unitary matrix have unit $\ell^2$ norm and `inner ℂ (colVec M i) (colVec N j) = (M.conjTranspose * N) i j` (`inner_colVec`, line 87), `attainable_iff` (line 121) establishes `OAIModel.Attainable n ↔ ∃ B : Fin n → Cand, MatrixMUBFamily B` without any rescaling factor.
     - For the repository's unnormalised Hadamard convention `MonomialTransport.RawHadamard H` (`|H i j|^2 = 1` and `Hᴴ H = 6 • 1`) and `MonomialTransport.RawMU H U` (`|(Hᴴ U) i j|^2 = 6`), `MubOpenAIBridge.lean` defines the explicit $1/\sqrt{6}$ scaling map `scale (H : Cand) : Cand := (((Real.sqrt 6 : ℝ) : ℂ)⁻¹) • H` (line 138) and establishes `rawMU_iff_pairMU` (line 168), `scale_unitary` (line 191), and `scale_one_overlap` (line 198).
2. **Index Sets (`Fin n` and `Coord = Fin 6`):**
   - Both upstream `Model.lean` and local `MubOpenAIBridge.lean` index basis families by `Fin n` (`{n : ℕ} (B : Fin n → Basis)`) and basis vectors/coordinates by `Coord := Fin 6`.
   - `mub6_card_le_five` (line 223) transports `mub6_family_le_five` from indexed families `Fin n → Cand` to finite sets `S : Finset Cand` via `S.equivFin.symm`, preserving pairwise inequality `(a ≠ b)` by injectivity of `S.equivFin.symm`.
3. **Tao Matrix Exponent Table (`taoExponent`):**
   - Upstream `Model.lean:37-43` defines `taoExponent : Matrix Coord Coord ℕ` with entries in `{0, 1, 2}` (representing exponents modulo $3$ of $\omega = \exp(2\pi i / 3)$ in `tao i j = omega ^ taoExponent i j`).
   - Local `MubOpenAIBridge.lean:242-245` (`tao_phase_bridge`) shows by `fin_cases i <;> fin_cases j <;> rfl` that `Conjecture2GeneralMechanization.phaseTable (taoPerm i).val (taoPerm j).val = (OAIModel.taoExponent i j : ℤ)` for the transposition `taoPerm = ![0, 1, 2, 5, 4, 3]`.

---

## 6. Conclusion

All six restated model definitions in `MUB.OpenAIBridge.OAIModel` and `OpenAIFamilyBound` in `lean4/MubOpenAIBridge.lean` match upstream `openai/math` at commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a` without discrepancy. No modification to `lean4/MubOpenAIBridge.lean` or `papers/core/mub6/documentation/mub_openai_bridge_compile_receipt.md` is required, and `MUB6-OPENAI-FAMILY-LE-FIVE` remains `IMPORTED_ASSUMPTION`.
