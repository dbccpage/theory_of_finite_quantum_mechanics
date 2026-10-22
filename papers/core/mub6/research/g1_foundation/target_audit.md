# Target and Premise Audit Report: MUB(6) G1 and Moduli Foundations

**Packet**: Prompt 01 (Target & Premise Audit)  
**Target Repository**: `C:/Users/a343o/source/repos/MUB6`  
**Reference Prompt Pack**: `C:/Users/a343o/source/repos/the_symbol_game/research/g1_foundation_prompt_pack_2026_09_22/`  
**Auditor**: `worker_prompt01` (Target and Premise Auditor)  
**Date**: 2026-09-22  
**AuthorityEffect**: None  
**Firewall Line**: `stated region only; mints no authority`  

---

## 1. Environment and File Hash Integrity

### 1.1 Repository State
- **Git HEAD**: `b2f5b318d0a1a793e47429f6b53a13e429ae1941`
- **Working Tree**: Clean (0 modified tracked files, 0 untracked files in target source tree)
- **Lean Toolchain Versions**:
  - `lean4/gluing/lean-toolchain`: `leanprover/lean4:v4.34.0`
  - `lean4/012_mutually_unbiased_bases/lean-toolchain`: `leanprover/lean4:v4.33.1`
  - Host Installed Lean: `Lean (version 4.34.0, x86_64-w64-windows-gnu, commit 293d5d0c0c3f3dded4688b3ccd6a33939ac5102b, Release)`

### 1.2 Cryptographic Digests (SHA-256)

| Relative Path | SHA-256 Digest |
|---|---|
| `lean4/gluing/lean-toolchain` | `744874093261C1854638246B978F088EAE15414B0F636AC08481A088A7AAA867` |
| `lean4/gluing/lakefile.toml` | `784BB10D23F1735497B0FA8A5A417B67800F1BD1EF9815AC027734E72F1F8119` |
| `lean4/G1_Orbits.lean` | `32B2924C2E12C75CB69D3B887D5115E98E67B8DD76844FABA791549FDA953EDE` |
| `lean4/Gluing.lean` | `586BC339DDE9B850437633225ED95FD91540A81A04D6EC8B8E09288334369823` |
| `lean4/ModuliReduction.lean` | `3533389BC4AE821CDF57E8FF1617B52D3614422AD42DBFB176C33AB1A9D4FC0F` |
| `lean4/TargetA11OrbitExhaustiveness.lean` | `86B659770EA980E4695D368935FC2B243E9D4244F5118F6895EB872E17AEE313` |
| `lean4/TargetA10GlobalCover.lean` | `8610B4905614CE369E5F2BCFD31D73E6BCD16D259D8CBEEAE586D7C216996443` |
| `lean4/TargetA9Haagerup.lean` | `D3E980F5A252B93319C2A2C8C45849EE7C23C1D33D6B8F67DF2CDDD2DE9678CC` |
| `lean4/SzollosiDeltoid.lean` | `950E662BCA86BB065A31DCFF42411327607EB354D1F0A44C8C053DE58EBA5270` |
| `lean4/KarlssonManifold.lean` | `FF0B6B4A67AA40EC57D1E4E7DEE818867AA06627355681E45FF39C6A62BB69D6` |
| `lean4/WallTransport.lean` | `8A7CAC87BF636EFBC8A1F6C511BBF5B6F1C34866D74F6A811DB8DA9795F44D46` |
| `lean4/ZeroRelVariety.lean` | `446450C192CF575F0E71C125C037C3ADA8AEAC35F2B7CDD901028F7B86C6FC05` |
| `lean4/012_mutually_unbiased_bases/lean-toolchain` | `A0ADA3782CD088719516BBFDF37B9E7032230E211BF424B85D952EE650C51091` |

---

## 2. Type and Constructor Audit: Syntactic vs Concrete Semantics

Inspection of `lean4/gluing/` reveals two disconnected sub-models with non-standard algebraic behavior.

### 2.1 The Eight Audited Declarations

#### 1. `PhaseAngle`
- **Location**: `lean4/G1_Orbits.lean:25-36`
- **Definition**:
  ```lean
  structure PhaseAngle where
    val : Nat
  deriving Inhabited, DecidableEq, Repr

  def PhaseAngle.zero : PhaseAngle := ⟨0⟩
  def PhaseAngle.add (a b : PhaseAngle) : PhaseAngle := ⟨a.val + b.val⟩
  def PhaseAngle.neg (a : PhaseAngle) : PhaseAngle := ⟨a.val⟩
  ```
- **Semantic Audit**:
  - `PhaseAngle` is an unreduced wrapper around `Nat`.
  - There is no quotient by $2\pi$ or modulo reduction (e.g. mod 6 or mod 24).
  - Addition is standard addition of natural numbers in $\mathbb{N}$.
  - `neg` is defined as `⟨a.val⟩`, returning the exact input.
  - Group inverse law fails: $a + (-a) = \langle 2 \cdot a.\text{val} \rangle \ne 0$ whenever $a.\text{val} > 0$.
  - It does not represent the circle group $U(1)$ or $\mathbb{R}/2\pi\mathbb{Z}$.

#### 2. `ComplexMatrix6`
- **Location**: `lean4/G1_Orbits.lean:39-42`
- **Definition**:
  ```lean
  structure ComplexMatrix6 where
    entry : Fin 6 -> Fin 6 -> PhaseAngle
  deriving Inhabited
  ```
- **Semantic Audit**:
  - A $6 \times 6$ grid of natural number wrappers (`Fin 6 -> Fin 6 -> PhaseAngle`).
  - No complex numbers $\mathbb{C}$, no real/imaginary parts, no modulus constraint ($|z| = 1$), and no matrix multiplication algebra are defined on this type.

#### 3. `is_complex_hadamard`
- **Location**: `lean4/G1_Orbits.lean:45`
- **Definition**:
  ```lean
  opaque is_complex_hadamard : ComplexMatrix6 -> Prop
  ```
- **Semantic Audit**:
  - Completely opaque.
  - Carries zero mathematical axioms, zero definitional reduction, and no condition linking it to unitarity ($H H^\dagger = 6 I$) or unimodularity.
  - In the Lean kernel, it behaves as an uninterpretable atomic predicate.

#### 4. `HadamardEquivalent`
- **Location**: `lean4/G1_Orbits.lean:59-83`
- **Definition**:
  ```lean
  structure PhaseGauge6 where
    phase : Fin 6 -> PhaseAngle

  structure Permutation6 where
    perm : Fin 6 -> Fin 6
    inv : Fin 6 -> Fin 6
    left_inv : ∀ i, inv (perm i) = i
    right_inv : ∀ i, perm (inv i) = i

  def applyHadamardGauge
      (D1 : PhaseGauge6) (P1 : Permutation6)
      (H : ComplexMatrix6)
      (P2 : Permutation6) (D2 : PhaseGauge6) : ComplexMatrix6 where
    entry j k :=
      PhaseAngle.add (D1.phase j)
        (PhaseAngle.add (H.entry (P1.perm j) (P2.perm k)) (D2.phase k))

  def HadamardEquivalent (H1 H2 : ComplexMatrix6) : Prop :=
    ∃ (D1 D2 : PhaseGauge6) (P1 P2 : Permutation6),
      H2 = applyHadamardGauge D1 P1 H1 P2 D2
  ```
- **Equivalence Law Audit**:
  - The relation evaluates entrywise as $(H_2)_{jk} = D_{1, j} + (H_1)_{P_1(j), P_2(k)} + D_{2, k}$ in $\mathbb{N}$.
  - **Reflexivity**: Holds definitionally at $D_1 = 0, D_2 = 0, P_1 = P_2 = \text{id}$.
  - **Symmetry**: **FAILS**. If $H_2$ is obtained from $H_1$ by setting $D_1.\text{phase}(0) = \langle 1 \rangle$, all entries of row 0 strictly increase in `val`. Since all gauge phases are in `Nat`, there exist no non-negative integers $D_1', D_2'$ such that $H_1 = D_1' + H_2 + D_2'$.
  - **Transitivity**: Unproved in the model.
  - Consequently, `G1_Orbits.lean` lines 95-103 is forced to declare reflexivity, symmetry, and transitivity as pending external variables:
    ```lean
    variable (hadamard_equiv_refl : ∀ (H : ComplexMatrix6), HadamardEquivalent H H)
    variable (hadamard_equiv_symm : ∀ {H1 H2 : ComplexMatrix6}, HadamardEquivalent H1 H2 -> HadamardEquivalent H2 H1)
    variable (hadamard_equiv_trans : ∀ {H1 H2 H3 : ComplexMatrix6}, HadamardEquivalent H1 H2 -> HadamardEquivalent H2 H3 -> HadamardEquivalent H1 H3)
    ```

#### 5. `InKnownHadamardModuli`
- **Location**: `lean4/G1_Orbits.lean:227-229`
- **Definition**:
  ```lean
  def InKnownHadamardModuli (H : ComplexMatrix6) : Prop :=
    FourierOrbit H ∨ DitaOrbit H ∨ ChernyavskyTaoOrbit H ∨ SzollosiOrbit H
  ```
  where:
  - `FourierOrbit H := HadamardEquivalent H F6_matrix` (`opaque F6_matrix : ComplexMatrix6`)
  - `DitaOrbit H := ∃ (alpha : PhaseAngle), HadamardEquivalent H (D6_family alpha)` (`opaque D6_family : PhaseAngle -> ComplexMatrix6`)
  - `ChernyavskyTaoOrbit H := HadamardEquivalent H Tao_S6_matrix` (`opaque Tao_S6_matrix : ComplexMatrix6`)
  - `SzollosiOrbit H := ∃ (theta : PhaseAngle), HadamardEquivalent H (Szollosi_B6_family theta)` (`opaque Szollosi_B6_family : PhaseAngle -> ComplexMatrix6`)
- **Semantic Audit**:
  - The continuous parameters $\alpha \in [0, \pi)$ and $\theta \in [0, \pi]$ are typed as `PhaseAngle` (natural numbers).
  - The references `F6_matrix` and `Tao_S6_matrix` are opaque constants, disconnected from `F6_concrete` and `Tao_S6_concrete`.

#### 6. `ClassificationExhaustivenessPremise`
- **Location**: `lean4/TargetA11OrbitExhaustiveness.lean:71-72`
- **Definition**:
  ```lean
  def ClassificationExhaustivenessPremise : Prop :=
    ∀ (H : ComplexMatrix6), is_complex_hadamard H → InKnownHadamardModuli H
  ```
- **Semantic Audit**:
  - A proposition asserting that any syntactic array of natural numbers satisfying the opaque predicate `is_complex_hadamard` lands in `InKnownHadamardModuli`.
  - It carries no connection to matrices over $\mathbb{C}$.

#### 7. `OrbitCatalogExhaustive`
- **Location**: `lean4/ModuliReduction.lean:34-35`
- **Definition**:
  ```lean
  def OrbitCatalogExhaustive : Prop :=
    ∀ (H : ComplexMatrix6), is_complex_hadamard H → InKnownHadamardModuli H
  ```
- **Semantic Audit**:
  - Definitionally identical to `ClassificationExhaustivenessPremise`.

#### 8. `G1`
- **Location**: `lean4/Gluing.lean:88-91`
- **Definition**:
  ```lean
  def G1 : Prop :=
    ∀ (B : Fin 7 → Basis),
      PairwiseMU B →
      ∃ (T : MUTriple), InConfig T B ∧ ∃ (c : TripleClass), CoveredClasses c ∧ belongs_to_class T c
  ```
- **Semantic Audit**:
  - States that in every 7-basis pairwise MU configuration, some constituent triple lands in a covered atlas class.
  - Operates over opaque types `Basis`, `TripleClass`, `belongs_to_class`, and `CoveredClasses`.

---

### 2.2 Second Disjoint Model: Section 8 Rational Arithmetic
In `lean4/G1_Orbits.lean:353-565`, a separate complex model is defined:
```lean
structure ℂ where
  re : Rat
  im : Rat

structure IsHadamard (H : Matrix (Fin 6) (Fin 6) ℂ) : Prop where
  ortho_left : Hᴴ * H = 1
  ortho_right : H * Hᴴ = 1
  entry_mod : ∀ j k : Fin 6, (H j k).normSq = 1 / 6
```
- **Arithmetic Inhabitation Failure**:
  For $z = \langle x, y \rangle \in \mathbb{Q} \times \mathbb{Q}$, `normSq z = x^2 + y^2 = 1/6`.
  This requires $6(x^2 + y^2) = 1$, or $6(a^2 + b^2) = c^2$ for integers $a, b, c$.
  In the 3-adic field $\mathbb{Q}_3$:
  - $v_3(c^2) = 2 v_3(c)$ is even.
  - Since $-1$ is not a quadratic residue mod 3, $v_3(a^2 + b^2) = 2 \min(v_3(a), v_3(b))$ is even.
  - $v_3(6(a^2 + b^2)) = 1 + v_3(a^2 + b^2)$ is odd.
  - Odd = even has no integer solutions.
  Therefore, no element of $\mathbb{Q} \times \mathbb{Q}$ has squared norm $1/6$.
  `IsHadamard` is empty over `ℂ = Rat × Rat`.
  Any theorem conditioned on `IsHadamard H` (such as `mu_triple_hadamard_transition`) has vacuous hypotheses over this type.

---

## 3. Opaque Objects and Missing Interpretations

| Opaque Constant | Declaring File & Line | Declared Type | Intended Mathematical Object | Status in Kernel |
|---|---|---|---|---|
| `Basis` | `Gluing.lean:30` | `Type` | Orthonormal basis of $\mathbb{C}^6$ | Uninterpreted type |
| `is_mutually_unbiased` | `Gluing.lean:34` | `Basis → Basis → Prop` | $\|\langle v_i, w_j \rangle\|^2 = 1/6$ for all $i, j$ | Uninterpreted predicate |
| `TripleClass` | `Gluing.lean:72` | `Type` | Moduli space of MU triples under unitary gauge | Uninterpreted type |
| `belongs_to_class` | `Gluing.lean:75` | `MUTriple → TripleClass → Prop` | Projection into orbit class | Uninterpreted relation |
| `CoveredClasses` | `Gluing.lean:79` | `TripleClass → Prop` | Covered region of certified atlas | Uninterpreted predicate |
| `is_complex_hadamard` | `G1_Orbits.lean:45` | `ComplexMatrix6 → Prop` | $H \in M_6(\mathbb{C}), \|H_{jk}\| = 1, H H^\dagger = 6 I$ | Uninterpreted predicate |
| `F6_matrix` | `G1_Orbits.lean:129` | `ComplexMatrix6` | Standard Fourier matrix $F_6$ | Uninterpreted constant |
| `D6_family` | `G1_Orbits.lean:146` | `PhaseAngle → ComplexMatrix6` | Diță 1-parameter family $D_6(\alpha)$ | Uninterpreted function |
| `Tao_S6_matrix` | `G1_Orbits.lean:195` | `ComplexMatrix6` | Tao isolated matrix $S_6$ | Uninterpreted constant |
| `Szollosi_B6_family` | `G1_Orbits.lean:212` | `PhaseAngle → ComplexMatrix6` | Szöllősi 1-parameter family $B_6(\theta)$ | Uninterpreted function |
| `triple_transition_hadamard` | `G1_Orbits.lean:240` | `MUTriple → ComplexMatrix6` | Transition matrix $U_{01} = B_0^\dagger B_1$ | Uninterpreted function |

---

## 4. Hadamard Orbit Exhaustiveness vs Configuration-Landing Proposition G1

The project structure demonstrates a fundamental gap between the classification of complex Hadamard matrices and the resolution of Premise G1:

```
+--------------------------------------------------------------------+
|                CLASSIFICATION EXHAUSTIVENESS PREMISE               |
|   Every 6x6 complex Hadamard matrix lies in {F6, D6, S6, B6, H6}   |
+--------------------------------------------------------------------+
                                 |
                                 v (unproved bridge: TransitionHadamardProperty)
+--------------------------------------------------------------------+
|                     PAIR MODULI COVERAGE                          |
|    Transition matrix of every MU pair/triple lies in the catalog   |
+--------------------------------------------------------------------+
                                 |
                                 v (unproved bridge: AtlasCoversKnownModuli)
+--------------------------------------------------------------------+
|                TRIPLE-LEVEL MODULI COVERAGE                        |
|       Every MU triple lands in a covered certified atlas class     |
+--------------------------------------------------------------------+
                                 |
                                 v (unproved bridge: GaugeInvariantClassMembership)
+--------------------------------------------------------------------+
|                     PREMISE G1 (CONFIGURATION LANDING)              |
|  Every 7-basis configuration B contains a triple T in covered class |
+--------------------------------------------------------------------+
                                 |
                                 v (unproved bridge: Premise G2 / Extension Obstruction)
+--------------------------------------------------------------------+
|                         NO COMPLETE MUB(6)                         |
+--------------------------------------------------------------------+
```

### 4.1 Structural Differences

1. **Quantifier Scope**:
   - **Classification Exhaustiveness**: Quantifies over isolated matrices $H \in \mathcal{H}_6$ (representing a pair of mutually unbiased bases).
   - **Premise G1**: Quantifies over complete families of seven bases $B : \text{Fin } 7 \to \text{Basis}$ and asserts that at least one of the $\binom{7}{3} = 35$ constituent triples belongs to an atlas class that admits no fourth basis.

2. **Simultaneous Realizability (The Triple Obstruction)**:
   - Knowing that every pair $(B_0, B_1)$ has transition matrix in $\mathcal{M}_6$ does not classify the simultaneous geometry of triples $(B_0, B_1, B_2)$.
   - A triple requires three pairwise Hadamard transition matrices $H_{01}, H_{02}, H_{12}$ satisfying the cocycle relation $H_{12} = H_{01}^\dagger H_{02}$. Pair classification does not resolve which pairs of orbits can form an MU triple.

3. **Required Downstream Bridges for A11/G1**:
   To deduce `NoCompleteMUB6` via `TargetA11OrbitExhaustiveness.lean`, the theorem `target_a11_canonical_grand_synthesis` explicitly demands:
   - `ClassificationExhaustivenessPremise` (Pair classification)
   - `TransitionHadamardProperty` (Transition matrices are Hadamard)
   - `AtlasCoversKnownModuli` (Atlas covers all catalog orbits)
   - `GaugeInvariantClassMembership` (Gauge invariance)
   - `G2_Variety` (Extension obstruction across all covered classes)
   - `G3` (Combinatorial basis selection — proved in `Gluing.lean`)

---

## 5. Audit of the "Classification is the Sole Remaining Frontier" Assertion

The assertion that "classification of $6 \times 6$ complex Hadamard matrices is the sole remaining frontier" is **demonstrably unsupported**. 

Even if a verified proof of `ClassificationExhaustivenessPremise` were supplied today, the following obligations remain open in the repository:

1. **Bridge 1: Transition Hadamardness on Concrete Bases (`TransitionHadamardProperty`)**:
   - Status: **DECLARED / OPEN**.
   - Lean body: `triple_transition_hadamard` is opaque. Section 8 proves `mu_triple_hadamard_transition` only for `Matrix (Fin 6) (Fin 6) ℂ` where `normSq = 1/6` is empty. No proof exists connecting orthonormal bases in $\mathbb{C}^6$ to Hadamard transition matrices.

2. **Bridge 2: Atlas Coverage of Moduli (`AtlasCoversKnownModuli`)**:
   - Status: **DECLARED / OPEN**.
   - Lean body: An unproved parameter in `g1_of_moduli_coverage`. Assumes that the certified classes in `Gluing.lean` cover all points in the continuous families $D_6(\alpha)$ and $B_6(\theta)$.

3. **Bridge 3: Gauge Invariance of Class Membership (`GaugeInvariantClassMembership`)**:
   - Status: **DECLARED / OPEN**.
   - Lean body: An unproved parameter in `ModuliReduction.lean:66`.

4. **Bridge 4: Premise G2 Extension Obstruction (`G2` / `G2_Variety`)**:
   - Status: **DECLARED / OPEN**.
   - Lean body: Requires showing that no triple in any covered class admits a 4th basis. In `TargetA10GlobalCover.lean:352`, the soundness theorem `checkGlobalUnifiedCover_sound` achieves `¬ HasFourthBasis pt.triple` solely because `has_cert : HasCurvatureCertificate triple` is an explicit input field of `GlobalPoint`! The extension obstruction across the continuous manifold is assumed point by point.

5. **Bridge 5: Global Cover Bridge (`TransitionMatrixGlobalCoverBridge`)**:
   - Status: **DECLARED / OPEN**.
   - Lean body: In `TargetA11OrbitExhaustiveness.lean:238`, it explicitly assumes that for every triple with transition matrix in known moduli, there exists a `GlobalPoint` (which internally contains `has_cert`).

6. **Bridge 6: Domain and Phase Arithmetic Mismatch**:
   - Status: **STRUCTURAL DEFECT**.
   - `PhaseAngle` is in `Nat`; continuous parameters are not represented.

---

## 6. Concrete Proposed Target over Mathlib Complex Matrices

To formulate a mathematically rigorous, checkable endpoint, the target must be grounded in Mathlib's complex analysis library (`Mathlib.Data.Complex.Basic`, `Mathlib.Data.Matrix.Basic`).

### 6.1 Original Target (in `TargetA11OrbitExhaustiveness.lean`)
```lean
def ClassificationExhaustivenessPremise : Prop :=
  ∀ (H : ComplexMatrix6), is_complex_hadamard H → InKnownHadamardModuli H
```

### 6.2 Proposed Grounded Target
```lean
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basic

open Matrix Complex

/-- Standard Complex Hadamard Matrix in dimension 6 over Mathlib Complex field. -/
def IsComplexHadamard6 (H : Matrix (Fin 6) (Fin 6) ℂ) : Prop :=
  (∀ i j : Fin 6, ‖H i j‖ = 1) ∧
  H * H.conjTranspose = (6 : ℂ) • (1 : Matrix (Fin 6) (Fin 6) ℂ)

/-- Standard Hadamard Equivalence over Complex Matrices. -/
def HadamardEquivalent6 (H1 H2 : Matrix (Fin 6) (Fin 6) ℂ) : Prop :=
  ∃ (D1 D2 : Fin 6 → ℂ) (P1 P2 : Equiv.Perm (Fin 6)),
    (∀ i, ‖D1 i‖ = 1) ∧ (∀ j, ‖D2 j‖ = 1) ∧
    H2 = diagonal D1 * P1.toMatrix * H1 * P2.toMatrix * diagonal D2

/-- Explicit Parameterized Atlas of Dimension 6 Complex Hadamard Matrices. -/
def InExplicitHadamardAtlas6 (H : Matrix (Fin 6) (Fin 6) ℂ) : Prop :=
  HadamardEquivalent6 H F6_mat ∨
  (∃ α : ℝ, HadamardEquivalent6 H (D6_mat α)) ∨
  HadamardEquivalent6 H S6_mat ∨
  (∃ θ : ℝ, HadamardEquivalent6 H (B6_mat θ)) ∨
  HadamardEquivalent6 H H6_mat

/-- Grounded Target Theorem: Exhaustive Classification of Order-6 Complex Hadamard Matrices. -/
def GroundedClassificationTarget6 : Prop :=
  ∀ (H : Matrix (Fin 6) (Fin 6) ℂ),
    IsComplexHadamard6 H → InExplicitHadamardAtlas6 H
```

### 6.3 Exact Differences
1. **Scalars**: `ComplexMatrix6` uses `PhaseAngle` (wrapper around `Nat`); proposed target uses Mathlib's `ℂ`.
2. **Hadamard Condition**: Original uses uninterpreted `opaque is_complex_hadamard`; proposed target uses explicit norm condition `‖H i j‖ = 1` and orthogonality `H * H.conjTranspose = 6 • 1`.
3. **Equivalence Group**: Original adds raw `Nat` values without group inverses; proposed target uses diagonal unitaries in $U(1)^6$ and permutations $S_6$.
4. **Parameter Space**: Original indexes families by `Nat`; proposed target indexes continuous families by $\mathbb{R}$.

---

## 7. Claim Hygiene Summary

1. **What this audit supports**:
   - It supports that the four Lean 4 files assemble conditional reduction implications (e.g., $G1 \wedge G2 \wedge G3 \to \text{NoCompleteMUB6}$).
   - It supports that combinatorial lemma G3 is proved in `Gluing.lean`.
   - It demonstrates that `PhaseAngle.neg` is the identity and `HadamardEquivalent` is not symmetric in the abstract model.
   - It shows that Section 8's `IsHadamard` predicate over $\mathbb{Q} \times \mathbb{Q}$ is uninhabited.

2. **What this audit does not support**:
   - It does not support that classification of complex Hadamard matrices is complete in Lean 4.
   - It does not support that classification is the sole remaining open bridge to resolving MUB(6).
   - It does not support that `InKnownHadamardModuli` covers the true moduli space of complex Hadamard matrices.

3. **Narrowest Defensible Claim**:
   The current MUB(6) gluing code in `lean4/gluing/` is an abstract propositional reduction scaffold over uninterpreted types and a discrete natural-number phase toy model; it does not formalize continuous complex Hadamard matrix classification or complete the G1/G2 geometric bridges.

4. **Next Test Needed**:
   Audit the external Cárdenes Wuttig–Tindall repository (`all_hadamard_matrices_in_dimension_six`) at a pinned commit to test whether its certificates can be translated to Mathlib's `Matrix (Fin 6) (Fin 6) ℂ` and whether its finite-corner atlas can discharge `GroundedClassificationTarget6`.

---
**Audit Terminal Recommendation**: `Repair` (The formal target requires semantic grounding over Mathlib complex matrices).
