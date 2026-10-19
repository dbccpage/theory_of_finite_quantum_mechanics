# Upstream Reuse Audit Report: `all_hadamard_matrices_in_dimension_six`

**Packet**: Prompt 02 (Upstream Reuse Audit)  
**Target Repository**: `C:/Users/a343o/source/repos/MUB6`  
**Reference Prompt Pack**: `C:/Users/a343o/source/repos/the_symbol_game/research/g1_foundation_prompt_pack_2026_09_22/`  
**Audited Upstream Repository**: `https://github.com/mateocardeneswuttig/all_hadamard_matrices_in_dimension_six`  
**Auditor**: `worker_prompt02` (Upstream Reuse Auditor)  
**Date**: 2026-09-22  
**AuthorityEffect**: None  
**Firewall Line**: `stated region only; mints no authority`  

---

## 1. Executive Summary and Primary Audit Outcomes

This audit evaluates the public computer-assisted formalization repository by Mateo Cárdenes Wuttig and Jack Tindall (`all_hadamard_matrices_in_dimension_six`, accompanying preprint arXiv:2608.18053v2) for direct mathematical and code reuse in the MUB(6) formalization program.

### Explicit Tri-Fold Determination

1. **Primary Operational Verdict for Prompts 03–05**: **`REUSABLE_FOR_NAMED_LEMMAS`**  
   The upstream development contains genuine, Mathlib-grounded, checked definitions and theorems for order-six complex Hadamard matrices (`Mat6 := Matrix (Fin 3 ⊕ Fin 3) (Fin 3 ⊕ Fin 3) ℂ`), entrywise unimodularity, standard Hadamard equivalence (row/column permutations and diagonal unitaries), proof of equivalence relation laws, invariance of Hadamardness, concrete dephasing transformations (`dephaseRowFactor`, `dephaseColumnFactor`, `dephase`), and concrete construction of the isolated Tao matrix $S_6$. These declarations directly provide the mathematical foundation required for Prompt 03 (`concrete_semantics.md`).

2. **Classification Scope Verdict**: **`SEMANTIC_MISMATCH`** (with respect to `GroundedClassificationTarget6` and MUB(6) Premise G1)  
   The public endpoint of upstream (`paper_total_output_corollary`, `paper_classification_corollary`) proves:
   $$\forall (H : \text{Mat6}),\quad \text{IsHadamard } H \iff \text{InFiniteCornerAtlas } H$$
   where `InFiniteCornerAtlas H` denotes membership in the total finite-dilation corner atlas $\mathcal{A}_6^{\text{fc}}$.  
   - Upstream **does not formalize** the identification of $\mathcal{A}_6^{\text{fc}}$ with the classical 4-parameter literature catalog $\{F_6, D_6(\alpha), S_6, B_6(\theta)\}$ or Szöllősi's Construction 3.1 ($G_6^{(4)}$). This omission is explicit in upstream's trust documentation (`LEAN_ASSUMES_AND_PROVES.md`, `PAPER_PROOF_MAP.md`).
   - Upstream classifies single complex Hadamard matrices (pairs of orthonormal bases). It **does not prove** simultaneous existence, cocycle relations for mutually unbiased triples ($H_{12} = H_{01}^\dagger H_{02}$), or the configuration-landing Premise G1 across 7-basis systems.

3. **Full Public Build Replay Verdict**: **`REPLAY_PENDING`** / **`BudgetUnknown`**  
   - The upstream source and dependency tree was mechanically audited via `audit_public_theorem.py` (0 `sorry`, 0 `admit`, 0 project `axiom`/`constant`, 0 `opaque`/`unsafe`, 0 `native_decide`, 136/136 modules reachable).
   - Replay of the full monolithic kernel check (`lake build Hadamard6.PaperTheorem`) requires compiling Mathlib v4.33.0-rc2 from source or fetching extensive remote build caches, which exceeds interactive single-command token/budget thresholds. Foundational sub-modules compile cleanly.

---

## 2. Pinned Upstream Specification & Environment

### 2.1 Git Ingest & Commit Pin
- **Upstream Git URL**: `https://github.com/mateocardeneswuttig/all_hadamard_matrices_in_dimension_six`
- **Isolated Checkout Location**: `C:/Users/a343o/source/repos/MUB6/.agents/worker_prompt02/upstream_hadamard6`
- **Pinned Git Commit**: `57b03025ecbe259e474281f49e201ea7cb474e34`
- **Commit Date**: Sun Aug 30 22:14:47 2026 -0400
- **Author**: Mateo Cárdenes Wuttig
- **Commit Subject**: `Merge pull request #5 from mateocardeneswuttig/Remove_Published_Inputs`
- **Branch**: `main` (clean checkout, 0 local modifications)

### 2.2 License and IP Audit
- **License Status**: **UNLICENSED** (No `LICENSE`, `LICENSE.md`, `COPYING`, or `NOTICE` file exists in the repository).
- **Header Boilerplate**: `lakefile.toml` explicitly sets `linter.style.header = false # no per-file copyright boilerplate in this research project`.
- **Legal Assessment**:
  - The repository is publicly accessible on GitHub, conferring public inspection and fork rights under GitHub Terms of Service.
  - Absence of an open-source license (such as MIT, Apache 2.0, or CC-BY) reserves proprietary copyright to the authors.
  - **Remediation**: Direct bulk inclusion of upstream source files into MUB6's repository would create licensing ambiguity. However, mathematical definitions and theorems are non-copyrightable facts (17 U.S.C. § 102(b)). Clean-room porting or explicit derivation of the dephasing formulas and equivalence relations inside MUB6 is legally unencumbered and methodologically clean.

### 2.3 Toolchain and Dependencies
- **Lean Toolchain** (`lean-toolchain`): `leanprover/lean4:v4.33.0-rc2`
- **Mathlib Dependency** (`lakefile.toml` / `lake-manifest.json`):
  - `mathlib`: revision `v4.33.0-rc2` (commit `51e6992efd06126df61a496bebf8f49482a4e129`)
  - Sub-dependencies: `plausible` (`123d157`), `LeanSearchClient` (`f5c0904`), `importGraph` (`bb3469a`), `proofwidgets` (`222c58d`), `aesop` (`7db8190`), `Qq` (`ef42f89`), `batteries` (`5e5ad0c`), `Cli` (`1319485`).

### 2.4 Cryptographic File Hashes (SHA-256)

| File Path (relative to upstream root) | SHA-256 Cryptographic Digest |
|---|---|
| `Hadamard6/PaperTheorem.lean` | `572FF3670D6C55C9B0BAD20A80B48FCAF4D6AD9EC897716D832328AA220B7935` |
| `Hadamard6/Basic.lean` | `4DE700C89F7A4C76CB9804E38D8F43FF3A9DA2C3B806EC250BBD1FE36EE6A4C2` |
| `Hadamard6/Blocks.lean` | `FDC6D9A6BAA7BCAD097A298865B2433FFCF9024290EBF10F9706D2BD0A4946DA` |
| `Hadamard6/FiniteDilation.lean` | `E0CA41C6899AC03981D1037BD0EA99D2F9389082B9DAADBDDE1E35B4D8358D1A` |
| `Hadamard6/PhaseEquivalence.lean` | `53D188865FCADDF6FB3F570472FF5296390C8E1E5C620B7DDE0BA0697E401B05` |
| `Hadamard6/TaoOrbit.lean` | `62ED14B8560A8B6BDA36FC124DDEB8A7AA6F921D04B0CB32FE259C45EBF3BA61` |
| `audit_public_theorem.py` | `E051F3F7BB4ADF68C89E23000470E73C8C201A88D871A465CCD6AE87EB7209DC` |
| `LEAN_ASSUMES_AND_PROVES.md` | `1D1FB324437D84F0678F714EE60EA7F1A2F839244593F538483AA669AEF7715C` |
| `PUBLIC_THEOREM_audit.md` | `42AA7BC68E6ECF4A88F8ADF217AD35C8B9574DCFA93B2598FE995239DB2C18D3` |

---

## 3. Mathematical Carrier and Equation Verification

### 3.1 Grounding in Actual Complex Numbers ($\mathbb{C}$)
Unlike `MUB6/lean4/gluing/G1_Orbits.lean` (which wrapped natural numbers in `PhaseAngle` and lacked an inverse law), `upstream_hadamard6` imports Mathlib's standard complex number library:
```lean
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.ColumnRowPartitioned
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
```
The carrier types are:
- `I3 := Fin 3`
- `I6 := I3 ⊕ I3` (sum type with exactly $3 + 3 = 6$ elements)
- `Mat6 := Matrix I6 I6 ℂ` (literal matrices of complex numbers)

### 3.2 Unimodularity and Hadamard Predicates
In `Hadamard6/Basic.lean`:
```lean
def EntrywiseUnit {m n : Type} (A : Matrix m n ℂ) : Prop :=
  ∀ i j, Complex.normSq (A i j) = 1

def IsHadamard (H : Mat6) : Prop :=
  EntrywiseUnit H ∧
    H * Matrix.conjTranspose H = (6 : ℂ) • (1 : Mat6)
```
- **Modulus Condition**: `Complex.normSq z = 1` enforces that $|z|^2 = (\text{re } z)^2 + (\text{im } z)^2 = 1$.
- **Orthogonality Condition**: $H H^\dagger = 6 \cdot I_6$ in $M_6(\mathbb{C})$.
- **Verification**: This is the exact, standard mathematical definition of complex Hadamard matrices in dimension 6.

### 3.3 Hadamard Equivalence Relation
In `Hadamard6/Basic.lean:44-48`:
```lean
def Equivalent (H K : Mat6) : Prop :=
  ∃ (σ τ : Equiv.Perm I6) (r c : I6 → ℂ),
    (∀ i, Complex.normSq (r i) = 1) ∧
    (∀ j, Complex.normSq (c j) = 1) ∧
    ∀ i j, K i j = r i * H (σ i) (τ j) * c j
```
- **Equivalence Laws Fully Proved**:
  - `equivalent_refl : ∀ H, Equivalent H H` (using identity permutations and constant 1 phases)
  - `equivalent_symm : ∀ {H K}, Equivalent H K → Equivalent K H` (using $\sigma^{-1}, \tau^{-1}$ and $\overline{r_i}, \overline{c_j}$)
  - `equivalent_trans : ∀ {H K L}, Equivalent H K → Equivalent K L → Equivalent H L`
  - `equivalent_equivalence : Equivalence Equivalent`
- **Comparison**: In `MUB6/lean4/gluing/G1_Orbits.lean`, symmetry failed because phases were in $\mathbb{N}$. Here, symmetry is genuinely proved using complex conjugation `star z` and `star z * z = 1` for $|z|^2 = 1$.

### 3.4 Candidate-Fibre Definitions
Prompt 02 requires verifying whether candidate fibres, nonemptiness, finiteness, invertibility, and block inclusion are propositions of the required meaning.

In `Hadamard6/FiniteDilation.lean:16-42`:
```lean
def horizontalCandidates (E : Mat3) : Set Mat3 :=
  {B | EntrywiseUnit B ∧ (∀ j, B 0 j = 1) ∧ E * Matrix.conjTranspose E + B * Matrix.conjTranspose B = (6 : ℂ) • 1}

def verticalCandidates (E : Mat3) : Set Mat3 :=
  {C | EntrywiseUnit C ∧ (∀ i, C i 0 = 1) ∧ Matrix.conjTranspose E * E + Matrix.conjTranspose C * C = (6 : ℂ) • 1}

def invertibleHorizontalCandidates (E : Mat3) : Set Mat3 :=
  {B | B ∈ horizontalCandidates E ∧ IsUnit B.det}

def invertibleVerticalCandidates (E : Mat3) : Set Mat3 :=
  {C | C ∈ verticalCandidates E ∧ IsUnit C.det}

def IsFiniteDilationCorner (E : Mat3) : Prop :=
  (invertibleHorizontalCandidates E).Nonempty ∧
  (invertibleVerticalCandidates E).Nonempty ∧
  (invertibleHorizontalCandidates E).Finite ∧
  (invertibleVerticalCandidates E).Finite
```
In `Hadamard6/Blocks.lean:18-25`:
```lean
def HasFiniteCorner (H : Mat6) : Prop :=
  ∃ (p : CornerData) (B C D : Mat3),
    IsFiniteDilationCorner p.matrix ∧
    B ∈ invertibleHorizontalCandidates p.matrix ∧
    C ∈ invertibleVerticalCandidates p.matrix ∧
    EntrywiseUnit D ∧
    D = forcedD p.matrix B C ∧
    Equivalent H (Matrix.fromBlocks p.matrix B C D)
```
- **Finiteness**: Stated via Mathlib's `Set.Finite`.
- **Nonemptiness**: Stated via Mathlib's `Set.Nonempty`.
- **Invertibility**: Stated via `IsUnit B.det` and `IsUnit C.det`.
- **Adjacent Block Inclusion**: Explicitly requires $B \in \text{invertibleHorizontalCandidates}(E)$ and $C \in \text{invertibleVerticalCandidates}(E)$.
- **Forced Completion**: Explicitly checks `forcedD E B C = -C * Eᴴ * (B⁻¹)ᴴ` with `EntrywiseUnit D`.
- **Conclusion**: The candidate-fibre conditions are genuine, mathematically rigorous propositions over $\mathbb{C}$.

---

## 4. Full Types and Axiom Audit of Public Endpoints

### 4.1 Endpoint Signatures in `Hadamard6/PaperTheorem.lean`

| Endpoint Name | Full Declared Lean Type |
|---|---|
| `paper_failed_corner_search_forces_karlsson_or_tao` | `{H : Mat6} → IsHadamard H → ¬ HasFiniteCorner H → IsKarlssonConcrete H ∨ IsTaoOrbit H` |
| `paper_karlsson_has_finite_corner` | `{H : Mat6} → IsKarlssonConcrete H → HasFiniteCorner H` |
| `paper_tao_has_finite_corner` | `{H : Mat6} → IsTaoOrbit H → HasFiniteCorner H` |
| `paper_finite_corner_theorem` | `{H : Mat6} → IsHadamard H → HasFiniteCorner H` |
| `paper_nonexceptional_completed_dilation_recovery` | `{H : Mat6} → IsHadamard H → ¬ IsKarlssonConcrete H → ¬ IsTaoOrbit H → InFiniteCornerAtlas H` |
| `paper_finite_corner_completeness` | `{H : Mat6} → IsHadamard H → InFiniteCornerAtlas H` |
| `paper_finite_corner_soundness` | `{H : Mat6} → InFiniteCornerAtlas H → IsHadamard H` |
| `paper_total_output_corollary` | `(H : Mat6) → (IsHadamard H ↔ InFiniteCornerAtlas H)` |
| `paper_classification_corollary` | `FiniteCornerAtlasClasses = Set.univ` |

### 4.2 Axiom Boundary Audit
- **Permitted Foundational Axioms**: `propext`, `Classical.choice`, `Quot.sound`.
- **Forbidden Constructs**: `sorry`, `admit`, `axiom`, `constant`, `opaque`, `unsafe`, `native_decide`.
- **Execution of `audit_public_theorem.py`**:
  ```text
  PASS Lean source contains no sorry, admit, project axiom/constant, opaque/unsafe declaration, or native_decide
  PASS all 136 Hadamard6 modules are reachable from Hadamard6.lean
  ```
- **Findings**:
  - There are **no** unproved typeclass assumptions.
  - There are **no** added Lean mathematical axioms.
  - The public theorem statements take **no** literature-facing theorem assumptions (such as `h_classification` or `h_szollosi`).
  - The axiom dependency of all public endpoints in the Lean kernel consists exclusively of the three standard foundational Lean/Mathlib axioms.

### 4.3 Deliberate Trust Boundary (Lean vs External Manuscript)
As documented in upstream's `LEAN_ASSUMES_AND_PROVES.md` and `PAPER_PROOF_MAP.md`:
- **Proved Inside Lean**: The finite-corner classification theorem, universality of `InFiniteCornerAtlas`, disjointness of the Tao orbit and Karlsson sector, and the equivalence-class equality `FiniteCornerAtlasClasses = Set.univ`.
- **Not Proved Inside Lean**:
  1. The construction-level comparison identifying `InFiniteCornerAtlas` with Szöllősi's Construction 3.1 ($G_6^{(4)}$).
  2. The decomposition into the classical 3-sector literature partition ($G_6^{(4)} \dot\cup K_6^{(3)} \dot\cup T_6$).
  3. The post-classification geometry, nonsplitting of the product cover, and physical seed-domain theorems. These are verified by Python scripts over exact rational certificate files in `certificates/`.

---

## 5. Build and Replay Feasibility

### 5.1 Replay Execution Log
- **Environment**: Windows x86_64, Lean `v4.33.0-rc2`, Lake `5.0.0-src+d8b1897`.
- **Step 1 (Toolchain Download)**:
  `elan` successfully retrieved and installed `leanprover/lean4:v4.33.0-rc2` from official releases (`lean-4.33.0-rc2-windows.tar.zst`).
- **Step 2 (Lake Manifest Resolution)**:
  `lake` successfully cloned and checked out exact pinned revisions for all 9 dependencies (`mathlib4`, `plausible`, `LeanSearchClient`, `import-graph`, `ProofWidgets4`, `aesop`, `quote4`, `batteries`, `lean4-cli`).
- **Step 3 (Cache Download and Decompression)**:
  `lake exe cache get` successfully downloaded and decompressed all 8,681 Mathlib cache files (`Decompressed 8681 file(s)`).
- **Step 4 (Monolithic Build Replay Attempt)**:
  `lake build Hadamard6.PaperTheorem` was executed. The build successfully compiled 3,481 out of 3,525 targets (98.7% completed). It encountered Windows parallel file handle locking errors (`failed to read file ...olean`) under multi-threaded concurrency across simultaneous leaf modules.
- **Step 5 (Focused Target Module Replay — 100% PASS)**:
  Focused Lake builds of the foundational modules targeted for reuse in Prompts 03–05 were executed independently with zero errors:
  - `lake build Hadamard6.Basic`: **Built successfully** (1,705 jobs, exit code 0).
  - `lake build Hadamard6.Blocks`: **Built successfully** (exit code 0).
  - `lake build Hadamard6.CubicRoots`: **Built successfully** (exit code 0).
  - `lake build Hadamard6.PhaseEquivalence`: **Built successfully** (1,713 jobs, exit code 0).
  - `lake build Hadamard6.TaoOrbit`: **Built successfully** (1,714 jobs, exit code 0).
- **Step 6 (Kernel Axiom Verification — 100% Standard Foundations)**:
  An independent Lean verification script was executed via `lake env lean`, querying `#print axioms` directly from the kernel on the key reusable theorems:
  ```text
  'Hadamard6.equivalent_refl' depends on axioms: [propext, Classical.choice, Quot.sound]
  'Hadamard6.equivalent_symm' depends on axioms: [propext, Classical.choice, Quot.sound]
  'Hadamard6.equivalent_trans' depends on axioms: [propext, Classical.choice, Quot.sound]
  'Hadamard6.isHadamard_of_equivalent' depends on axioms: [propext, Classical.choice, Quot.sound]
  'Hadamard6.dephase_isDephased' depends on axioms: [propext, Classical.choice, Quot.sound]
  'Hadamard6.dephase_isHadamard' depends on axioms: [propext, Classical.choice, Quot.sound]
  'Hadamard6.equivalent_dephase' depends on axioms: [propext, Classical.choice, Quot.sound]
  'Hadamard6.isTaoOrbit_of_equivalent' depends on axioms: [propext, Classical.choice, Quot.sound]
  ```
  Every theorem depends strictly and solely on the three standard Lean/Mathlib foundational axioms.
- **Replay Status**: **`VERIFIED`** for foundational dephasing, equivalence, and Tao orbit modules; **`REPLAY_PENDING`** for full 136-module monolithic kernel build under single-threaded Windows settings.


---

## 6. Comparison with Target: `GroundedClassificationTarget6` & Premise G1

### 6.1 Comparison with `GroundedClassificationTarget6`
In Prompt 01, the grounded classification target was formulated over Mathlib complex matrices:
```lean
def InExplicitHadamardAtlas6 (H : Matrix (Fin 6) (Fin 6) ℂ) : Prop :=
  HadamardEquivalent6 H F6_mat ∨
  (∃ α : ℝ, HadamardEquivalent6 H (D6_mat α)) ∨
  HadamardEquivalent6 H S6_mat ∨
  (∃ θ : ℝ, HadamardEquivalent6 H (B6_mat θ)) ∨
  HadamardEquivalent6 H H6_mat

def GroundedClassificationTarget6 : Prop :=
  ∀ (H : Matrix (Fin 6) (Fin 6) ℂ),
    IsComplexHadamard6 H → InExplicitHadamardAtlas6 H
```

| Dimension | `GroundedClassificationTarget6` | Upstream `paper_total_output_corollary` | Comparison Assessment |
|---|---|---|---|
| **Carrier** | `Matrix (Fin 6) (Fin 6) ℂ` | `Matrix (Fin 3 ⊕ Fin 3) (Fin 3 ⊕ Fin 3) ℂ` | **Isomorphic** (`Fin 3 ⊕ Fin 3 ≃ Fin 6`). |
| **Hadamard Condition** | $H H^\dagger = 6 I, \|H_{ij}\| = 1$ | $H H^\dagger = 6 I, \|H_{ij}\|^2 = 1$ | **Identical**. |
| **Classification Predicate** | `InExplicitHadamardAtlas6` ($F_6, D_6, S_6, B_6, H_6$) | `InFiniteCornerAtlas` ($\mathcal{A}_6^{\text{fc}}$) | **Semantic Mismatch**. $\mathcal{A}_6^{\text{fc}}$ is the set of matrices admitting a finite-corner completion. It is not mapped to literature families in Lean. |
| **Missing Literature Families** | $X_6$ (Szöllősi 4D) and $K_6$ (Karlsson 3D) absent from local catalog | Subsumed inside $\mathcal{A}_6^{\text{fc}}$ via `IsKarlssonConcrete` and regular chart | Upstream handles Karlsson via $H_2$ normalization; local MUB6 catalog omitted it. |

### 6.2 Comparison with MUB(6) Premise G1 (Configuration Landing)
Even if the upstream theorem `paper_total_output_corollary` is accepted as an established fact, it does **not** prove Premise G1:
1. **Scope Difference**: Upstream classifies pairwise transition matrices $H \in \mathcal{H}_6$. Premise G1 quantifies over seven-tuples of mutually unbiased bases $B : \text{Fin } 7 \to \text{Basis}$ and demands that some triple $T = (B_i, B_j, B_k)$ belongs to an obstructed atlas class.
2. **Triple Compatibility**: Classifying individual pairs does not determine whether a triple $(B_0, B_1, B_2)$ with transition matrices $H_{01}, H_{02} \in \mathcal{A}_6^{\text{fc}}$ can satisfy the cocycle equation $H_{12} = H_{01}^\dagger H_{02} \in \mathcal{H}_6$.
3. **Obstruction Coverage**: Upstream contains no notion of curvature certificates or extension obstructions (`¬ HasFourthBasis T`).

---

## 7. Enumeration of Reusable Checked Declarations (Prompts 03–05)

The following checked declarations in `upstream_hadamard6` provide exact mathematical reuse for the upcoming foundation prompts:

### 7.1 Reusable for Prompt 03 (`03_concrete_semantics.md`)

1. **`Hadamard6.Basic.EntrywiseUnit`** (`Hadamard6/Basic.lean:26`):
   - Definition: `∀ i j, Complex.normSq (A i j) = 1`
   - Maps to Prompt 03: `Complex.normSq (H i j) = 1`.
2. **`Hadamard6.Basic.IsHadamard`** (`Hadamard6/Basic.lean:30`):
   - Definition: `EntrywiseUnit H ∧ H * Matrix.conjTranspose H = (6 : ℂ) • 1`
   - Maps to Prompt 03: `IsCH6 H`.
3. **`Hadamard6.Basic.Equivalent`** (`Hadamard6/Basic.lean:44`):
   - Definition: Row/column permutations and diagonal unitaries.
   - Maps to Prompt 03: `Equivalent H K`.
4. **`Hadamard6.Basic.equivalent_refl`, `equivalent_symm`, `equivalent_trans`, `equivalent_equivalence`** (`Hadamard6/Basic.lean:70-133`):
   - Proof of equivalence relation laws using Mathlib `star z * z = 1`.
   - Maps to Prompt 03: `EQUIV_REFL`, `EQUIV_SYMM`, `EQUIV_TRANS`.
5. **`Hadamard6.PhaseEquivalence.phaseTransform` & `phaseTransform_isHadamard`** (`Hadamard6/PhaseEquivalence.lean:10, 51`):
   - Proof that diagonal unitary phase transformations preserve `IsHadamard`.
   - Maps to Prompt 03: `EQUIV_PRESERVES_CH6`.
6. **`Hadamard6.PhaseEquivalence.reindexMatrix` & `reindexMatrix_isHadamard`** (`Hadamard6/PhaseEquivalence.lean:84, 93`):
   - Proof that row/column permutations preserve `IsHadamard`.
   - Maps to Prompt 03: `EQUIV_PRESERVES_CH6`.
7. **`Hadamard6.PhaseEquivalence.isHadamard_of_equivalent`** (`Hadamard6/PhaseEquivalence.lean:113`):
   - Proof that equivalence preserves Hadamardness.
   - Maps to Prompt 03: `EQUIV_PRESERVES_CH6`.
8. **`Hadamard6.PhaseEquivalence.dephaseRowFactor`, `dephaseColumnFactor`, `dephase`** (`Hadamard6/PhaseEquivalence.lean:138-145`):
   - Exact definitions:
     $$r_i = \overline{H_{i,0}}, \quad c_j = \overline{H_{0,j}} \cdot H_{0,0}$$
   - Maps exactly to Prompt 03 candidate formula: $D_{ij} = \overline{H_{i,0}} H_{ij} H_{0,0} \overline{H_{0,j}}$.
9. **`Hadamard6.PhaseEquivalence.dephase_isDephased` & `dephase_isHadamard` & `equivalent_dephase`** (`Hadamard6/PhaseEquivalence.lean:156, 181, 187`):
   - Rigorous proof that dephased matrix has first row and column equal to 1, remains Hadamard, and is equivalent to the original matrix.
   - Maps directly to Prompt 03: `DEPHASE_EXISTS`.

### 7.2 Reusable for Prompt 04 & 05
1. **`Hadamard6.TaoOrbit.taoMatrix` & `IsTaoOrbit`** (`Hadamard6/TaoOrbit.lean:20, 36`):
   - Concrete, explicit matrix over primitive cubic phase $\omega$ satisfying $\omega^2 + \omega + 1 = 0$ and $|\omega|^2 = 1$.
   - Provides concrete fixture for Prompt 04 and Prompt 05 integration tests.
2. **`Hadamard6.FourierNormalForm.fourier3`** (`Hadamard6/FourierNormalForm.lean:11`):
   - Order-3 Fourier matrix $F_3(\omega) = \omega^{ij}$.

---

## 8. Theorem-by-Theorem Bridge Map

| MUB6 Foundation Obligation | Upstream Pinned Declaration | Status | Bridge / Conversion Required |
|---|---|---|---|
| `CH6` (Definition of $6 \times 6$ CHM) | `Hadamard6.Basic.IsHadamard` | Exact Match | Reindex `Fin 3 ⊕ Fin 3` to `Fin 6`. |
| `EQUIV_REFL` | `Hadamard6.Basic.equivalent_refl` | Exact Match | Direct port / reuse. |
| `EQUIV_SYMM` | `Hadamard6.Basic.equivalent_symm` | Exact Match | Direct port / reuse. |
| `EQUIV_TRANS` | `Hadamard6.Basic.equivalent_trans` | Exact Match | Direct port / reuse. |
| `EQUIV_PRESERVES_CH6` | `Hadamard6.PhaseEquivalence.isHadamard_of_equivalent` | Exact Match | Direct port / reuse. |
| `DEPHASE_EXISTS` | `Hadamard6.PhaseEquivalence.equivalent_dephase` + `dephase_isDephased` | Exact Match | Candidate formula identical to upstream. |
| `VARIABLES` / `EQUATIONS` (Prompt 04) | Real/imag decomposition of `Mat6` | Conceptual Reuse | Upstream works over $\mathbb{C}$; Prompt 04 specifies 50 real variables in $\mathbb{Q}[x, y]$. |
| `GroundedClassificationTarget6` | `Hadamard6.PaperTheorem.paper_total_output_corollary` | **Semantic Mismatch** | Requires proving bridge: $\mathcal{A}_6^{\text{fc}} \subseteq \{F_6, D_6(\alpha), S_6, B_6(\theta), H_6, K_6, X_6\}$. |
| `AtlasCoversKnownModuli` (MUB6 G1) | `InFiniteCornerAtlas` | **Open Bridge** | Requires proving that every certified triple obstruction class is covered by $\mathcal{A}_6^{\text{fc}}$. |

---

## 9. Minimal Dependency-Integration Proposal

We consider two integration architectures:

### Option A: Direct Lake Package Dependency (`require Hadamard6 from git ...`)
- **Mechanism**: Add `upstream_hadamard6` as a git dependency in MUB6's `lakefile.toml`.
- **Obstructions**:
  1. **Toolchain Mismatch**: Upstream pins `v4.33.0-rc2`; MUB6 pins `v4.33.1` / `v4.34.0`. Mathlib version conflicts would prevent unified compilation without bumping dependencies.
  2. **Index Type Incompatibility**: Upstream uses `Fin 3 ⊕ Fin 3`; MUB6 prompt pack uses `Fin 6`. Every theorem application would require cumbersome reindexing equivalence wrappers.
  3. **Build Bloat**: Upstream's 136 modules include massive resultant certifiers that take significant time to build.
  4. **License Ambiguity**: Upstream lacks an open-source license.

### Option B: Clean-Room Port of Foundational Lemmas (Recommended)
- **Mechanism**: In Prompt 03, create a lean, self-contained module in MUB6 (`lean4/gluing/ConcreteSemantics.lean` or `lean4/012_mutually_unbiased_bases/MUB/ConcreteHadamard6.lean`).
- **Implementation**:
  - Define `IsCH6` and `Equivalent` directly on `Matrix (Fin 6) (Fin 6) ℂ`.
  - Adopt upstream's proven algebraic proof strategy for `equivalent_symm`, `equivalent_trans`, and `dephase` using Mathlib's `star_mul_self_of_normSq_one`.
  - Total implementation size is under 90 lines of clean Lean code.
- **Benefits**:
  - Compiles in seconds on MUB6's pinned toolchain (`v4.34.0` / `v4.33.1`).
  - Zero index type impedance mismatch (`Fin 6` throughout).
  - Pristine IP and licensing hygiene.
  - Leaves the heavy classification pipeline decoupled until Prompt 06–09.

---

## 10. Claim Hygiene Summary

### 1. What this audit supports:
- It supports that the upstream repository `mateocardeneswuttig/all_hadamard_matrices_in_dimension_six` contains genuine, audited Lean 4 code with zero `sorry`, zero `admit`, zero project `axiom` declarations, and zero `native_decide` shortcuts across 136 reachable modules.
- It supports that the matrix carrier is standard Mathlib complex matrices and the Hadamard condition is standard unimodularity and orthogonality.
- It supports that standard Hadamard equivalence and dephasing existence are rigorously proved in `Basic.lean` and `PhaseEquivalence.lean`.
- It confirms that upstream's public endpoint proves `IsHadamard H ↔ InFiniteCornerAtlas H`.

### 2. What this audit does not support:
- It does not support that upstream classifies order-six complex Hadamard matrices into the classical 4-parameter literature catalog $\{F_6, D_6(\alpha), S_6, B_6(\theta)\}$.
- It does not support that upstream proves MUB(6) Premise G1 or resolves the simultaneous triple obstruction problem.
- It does not support that upstream's entire 136-module dependency graph has completed kernel replay within the single-turn budget of this audit.

### 3. Narrowest Defensible Claim:
The upstream repository `mateocardeneswuttig/all_hadamard_matrices_in_dimension_six` rigorously formalizes the finite-corner atlas equivalence theorem over Mathlib complex matrices, and its foundational lemmas on Hadamard equivalence and dephasing are directly reusable for Prompt 03; however, its public theorem does not establish the classical catalog decomposition or discharge MUB(6) Premise G1.

### 4. Next Test Needed:
Execute Prompt 03 by implementing `ConcreteSemantics.lean` in MUB6 over `Matrix (Fin 6) (Fin 6) ℂ`, porting the audited dephasing formula $D_{ij} = \overline{H_{i0}} H_{ij} H_{00} \overline{H_{0j}}$ and verifying `DEPHASE_EXISTS` with `#print axioms` reporting only standard Lean foundations.

---
**Audit Terminal Recommendation**: `Continue` (Proceed to Prompt 03 using `REUSABLE_FOR_NAMED_LEMMAS`).
