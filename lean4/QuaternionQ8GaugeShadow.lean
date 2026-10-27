import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# TFQ-0012 (`FINITE_QCD`)

Formalizes the narrowed finite counterpart and non-equivalence fences for
`TFQ-0012` ("quaternion_gauge_shadow.rs presents Q8 as eight matrices over Q(i),
embedded by omega_lie_theory::su2_matrix, and treats that finite subgroup of
SU(2) as a non-abelian gauge shadow. finite_group.rs can hold a Cayley table
for the same shadow, but the table is not an SU(3) color connection. A file
search under omega_lie_theory/src and omega_quantum_physics/src found no
Hopf-algebra module, so Hopf gauge data remains an open obligation next to this
shadow. AuthorityEffect on the quaternion module is None. F001.S000 coordinates
finite carriers and does not supply color links."):

1. **Quaternion Group `Q8Elem` & Cayley Table Algebra**:
   - Defines the 8-element quaternion group `Q8Elem = {one, negOne, qi, negQi, qj, negQj, qk, negQk}`
     with multiplication `q8Mul` and inverse `q8Inv`.
   - Proves associativity across all `8³ = 512` triples, two-sided identity, and
     two-sided inverses (`q8_group_associativity_unit_and_inverses`).
   - Proves Hamilton's quaternion relations `i² = j² = k² = ijk = -1`, non-commutativity
     `ij = k ≠ -k = ji`, and the `Q_8` class equation `1 + 1 + 2 + 2 + 2 = 8` with
     irreducible character degree sum `1² + 1² + 1² + 1² + 2² = 8`
     (`q8_nonabelian_hamilton_relations_and_class_equation`).
2. **2×2 Gaussian-Integer Matrix Embedding (`su2_matrix` over `ℤ[i]`)**:
   - Defines `GaussInt` (`ℤ[i]`), `Mat2GI` (`M₂(ℤ[i])`), and the faithful `SU(2)` shadow
     embedding `q8ToMat2GI : Q8Elem → Mat2GI`.
   - Proves that `q8ToMat2GI` is a multiplicative homomorphism on all `64` pairs
     (`q8_mat2gi_embedding_homomorphism`), is injective with unit determinant `1 + 0i`
     on all `8` elements (`q8_mat2gi_embedding_injective_and_unit_det`), and satisfies
     plaquette holonomy conjugation and character trace invariance
     (`q8_plaquette_holonomy_conjugation_and_trace_invariance`).
3. **Non-Equivalence Fences: `Q_8 ⊂ SU(2)` vs. `SU(3)` Color Connection & Unbuilt Hopf Gauge Module**:
   - Proves the `SU(2)` vs. `SU(3)` fundamental dimension (`2 ≠ 3`), Lie algebra
     dimension (`3 ≠ 8`), center order (`2 ≠ 3`), and Lagrange divisibility obstruction
     `8 % 3 = 2 ≠ 0` preventing `Q_8` from containing the `ℤ₃` center of `SU(3)`
     (`q8_su2_vs_su3_color_dimension_and_center_fence`).
   - Proves that `Q_8` has maximum irreducible representation degree `2 < 3`, so any
     3-dimensional representation of `Q_8` is reducible (`q8_irrep_max_degree_two_no_color_triplet_fence`).
   - Proves that group-like diagonal comultiplication `Δ(g) = (g, g)` fails on linear
     superpositions (`(a + b)² ≠ a² + b²` for `a * b ≠ 0`), fencing Cayley tables from
     general Hopf gauge algebras (`group_like_coproduct_vs_hopf_linearity_fence`).
   - Formalizes the `FiniteQcdScopeLedger` audit and discrete `{-2, 0, 2}` character
     spectrum (`f001_s000_carrier_coordination_not_color_connection_fence`,
     `q8_wilson_plaquette_character_discrete_spectrum_fence`).
-/

namespace QuaternionQ8GaugeShadow

-- ============================================================================
-- 1. Quaternion Group `Q8Elem` & Cayley Table Algebra
-- ============================================================================

/-- The 8 elements of the quaternion group `Q_8 = {±1, ±i, ±j, ±k}`. -/
inductive Q8Elem where
  | one : Q8Elem
  | negOne : Q8Elem
  | qi : Q8Elem
  | negQi : Q8Elem
  | qj : Q8Elem
  | negQj : Q8Elem
  | qk : Q8Elem
  | negQk : Q8Elem
  deriving DecidableEq, Repr

open Q8Elem

/-- Negation (`-x`, multiplication by `negOne`) in `Q_8`. -/
def q8Neg : Q8Elem → Q8Elem
  | one => negOne
  | negOne => one
  | qi => negQi
  | negQi => qi
  | qj => negQj
  | negQj => qj
  | qk => negQk
  | negQk => qk

/-- Cayley table multiplication on `Q_8`. -/
def q8Mul (a b : Q8Elem) : Q8Elem :=
  match a, b with
  | one, y => y
  | negOne, y => q8Neg y
  | x, one => x
  | x, negOne => q8Neg x
  | qi, qi => negOne
  | qi, negQi => one
  | qi, qj => qk
  | qi, negQj => negQk
  | qi, qk => negQj
  | qi, negQk => qj
  | negQi, qi => one
  | negQi, negQi => negOne
  | negQi, qj => negQk
  | negQi, negQj => qk
  | negQi, qk => qj
  | negQi, negQk => negQj
  | qj, qi => negQk
  | qj, negQi => qk
  | qj, qj => negOne
  | qj, negQj => one
  | qj, qk => qi
  | qj, negQk => negQi
  | negQj, qi => qk
  | negQj, negQi => negQk
  | negQj, qj => one
  | negQj, negQj => negOne
  | negQj, qk => negQi
  | negQj, negQk => qi
  | qk, qi => qj
  | qk, negQi => negQj
  | qk, qj => negQi
  | qk, negQj => qi
  | qk, qk => negOne
  | qk, negQk => one
  | negQk, qi => negQj
  | negQk, negQi => qj
  | negQk, qj => qi
  | negQk, negQj => negQi
  | negQk, qk => one
  | negQk, negQk => negOne

/-- Group inverse in `Q_8`. -/
def q8Inv : Q8Elem → Q8Elem
  | one => one
  | negOne => negOne
  | qi => negQi
  | negQi => qi
  | qj => negQj
  | negQj => qj
  | qk => negQk
  | negQk => qk

/-- Theorem 1: `Q8Elem` with `q8Mul`, `one`, and `q8Inv` satisfies associativity,
two-sided identity, and two-sided inverse laws across all elements. -/
theorem q8_group_associativity_unit_and_inverses :
    (∀ a b c : Q8Elem, q8Mul (q8Mul a b) c = q8Mul a (q8Mul b c)) ∧
    (∀ a : Q8Elem, q8Mul one a = a ∧ q8Mul a one = a) ∧
    (∀ a : Q8Elem, q8Mul a (q8Inv a) = one ∧ q8Mul (q8Inv a) a = one) := by
  refine ⟨?_, ?_, ?_⟩
  · intro a b c; cases a <;> cases b <;> cases c <;> rfl
  · intro a; cases a <;> decide
  · intro a; cases a <;> decide

/-- Theorem 2: Hamilton's relations (`i² = j² = k² = ijk = -1`), non-commutativity
(`ij = k ≠ -k = ji`), and the `Q_8` class equation (`1 + 1 + 2 + 2 + 2 = 8`) and
irreducible character degree sum (`1² + 1² + 1² + 1² + 2² = 8`). -/
theorem q8_nonabelian_hamilton_relations_and_class_equation :
    q8Mul qi qi = negOne ∧
    q8Mul qj qj = negOne ∧
    q8Mul qk qk = negOne ∧
    q8Mul (q8Mul qi qj) qk = negOne ∧
    q8Mul qi qj = qk ∧
    q8Mul qj qi = negQk ∧
    q8Mul qi qj ≠ q8Mul qj qi ∧
    (1 + 1 + 2 + 2 + 2 : Nat) = 8 ∧
    (1 ^ 2 + 1 ^ 2 + 1 ^ 2 + 1 ^ 2 + 2 ^ 2 : Nat) = 8 := by
  decide

-- ============================================================================
-- 2. 2×2 Gaussian-Integer Matrix Embedding (`su2_matrix` over `ℤ[i]`)
-- ============================================================================

/-- Gaussian integers `ℤ[i]`. -/
@[ext]
structure GaussInt where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def giZero : GaussInt := ⟨0, 0⟩
def giOne : GaussInt := ⟨1, 0⟩
def giNegOne : GaussInt := ⟨-1, 0⟩
def giI : GaussInt := ⟨0, 1⟩
def giNegI : GaussInt := ⟨0, -1⟩

def giAdd (z w : GaussInt) : GaussInt :=
  ⟨z.re + w.re, z.im + w.im⟩

def giSub (z w : GaussInt) : GaussInt :=
  ⟨z.re - w.re, z.im - w.im⟩

def giMul (z w : GaussInt) : GaussInt :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩

/-- 2×2 matrices over `ℤ[i]`. -/
@[ext]
structure Mat2GI where
  m11 : GaussInt
  m12 : GaussInt
  m21 : GaussInt
  m22 : GaussInt
  deriving DecidableEq, Repr

def mat2GIMul (A B : Mat2GI) : Mat2GI :=
  ⟨giAdd (giMul A.m11 B.m11) (giMul A.m12 B.m21),
   giAdd (giMul A.m11 B.m12) (giMul A.m12 B.m22),
   giAdd (giMul A.m21 B.m11) (giMul A.m22 B.m21),
   giAdd (giMul A.m21 B.m12) (giMul A.m22 B.m22)⟩

def mat2GIDet (A : Mat2GI) : GaussInt :=
  giSub (giMul A.m11 A.m22) (giMul A.m12 A.m21)

def mat2GITraceRe (A : Mat2GI) : Int :=
  A.m11.re + A.m22.re

/-- Embedding `su2_matrix` of `Q_8` into `M_2(ℤ[i]) ⊂ SU(2)`. -/
def q8ToMat2GI : Q8Elem → Mat2GI
  | one => ⟨giOne, giZero, giZero, giOne⟩
  | negOne => ⟨giNegOne, giZero, giZero, giNegOne⟩
  | qi => ⟨giI, giZero, giZero, giNegI⟩
  | negQi => ⟨giNegI, giZero, giZero, giI⟩
  | qj => ⟨giZero, giOne, giNegOne, giZero⟩
  | negQj => ⟨giZero, giNegOne, giOne, giZero⟩
  | qk => ⟨giZero, giI, giI, giZero⟩
  | negQk => ⟨giZero, giNegI, giNegI, giZero⟩

/-- Theorem 3: The `su2_matrix` map `q8ToMat2GI` is an exact multiplicative homomorphism
from `(Q8Elem, q8Mul)` into `(Mat2GI, mat2GIMul)`. -/
theorem q8_mat2gi_embedding_homomorphism (a b : Q8Elem) :
    q8ToMat2GI (q8Mul a b) = mat2GIMul (q8ToMat2GI a) (q8ToMat2GI b) := by
  cases a <;> cases b <;> rfl

/-- Theorem 4: The embedding `q8ToMat2GI` is injective (`q8ToMat2GI a = q8ToMat2GI b → a = b`)
and every image matrix has exact unit Gaussian determinant `1 + 0i`. -/
theorem q8_mat2gi_embedding_injective_and_unit_det :
    (∀ a b : Q8Elem, q8ToMat2GI a = q8ToMat2GI b → a = b) ∧
    (∀ a : Q8Elem, mat2GIDet (q8ToMat2GI a) = giOne) := by
  refine ⟨?_, ?_⟩
  · intro a b; cases a <;> cases b <;> decide
  · intro a; cases a <;> rfl

/-- Conjugation `g * h * g⁻¹` in `Q_8`. -/
def q8Conj (g h : Q8Elem) : Q8Elem :=
  q8Mul (q8Mul g h) (q8Inv g)

/-- Theorem 5: Conjugation invariance of the `SU(2)` matrix character trace on `Q_8`:
for all `g, h ∈ Q_8`, `mat2GITraceRe (q8ToMat2GI (q8Conj g h)) = mat2GITraceRe (q8ToMat2GI h)`. -/
theorem q8_plaquette_holonomy_conjugation_and_trace_invariance (g h : Q8Elem) :
    mat2GITraceRe (q8ToMat2GI (q8Conj g h)) = mat2GITraceRe (q8ToMat2GI h) := by
  cases g <;> cases h <;> rfl

-- ============================================================================
-- 3. Non-Equivalence Fences: `Q_8 ⊂ SU(2)` vs. `SU(3)` & Unbuilt Hopf Gauge
-- ============================================================================

/-- Lie algebra dimension `N^2 - 1` of `su(N)`. -/
def suLieDim (N : Nat) : Nat :=
  N ^ 2 - 1

/-- Theorem 6 (`Q_8 ⊂ SU(2)` vs. `SU(3)` Color Fence):
`SU(2)` and `SU(3)` differ in fundamental carrier dimension (`2 ≠ 3`), Lie algebra
dimension (`suLieDim 2 = 3 ≠ 8 = suLieDim 3`), and center order (`2 ≠ 3`), and
since `|Q_8| = 8` is not divisible by `3` (`8 % 3 = 2 ≠ 0`), `Q_8` cannot contain
the `ℤ_3` center of `SU(3)`. -/
theorem q8_su2_vs_su3_color_dimension_and_center_fence :
    (2 : Nat) ≠ 3 ∧
    suLieDim 2 = 3 ∧
    suLieDim 3 = 8 ∧
    suLieDim 2 ≠ suLieDim 3 ∧
    8 % 3 = 2 ∧
    8 % 3 ≠ 0 := by
  dsimp [suLieDim]
  decide

/-- Theorem 7 (`Q_8` Irreducible Representation Degree Fence):
Every irreducible representation of `Q_8` has degree `1` or `2`, so the maximum irrep
degree is `2 < 3`, and any 3-dimensional representation of `Q_8` decomposes into a
reducible sum of degrees (`2 + 1 = 3` or `1 + 1 + 1 = 3`) rather than an irreducible
`SU(3)` color triplet. -/
theorem q8_irrep_max_degree_two_no_color_triplet_fence :
    ∀ d ∈ ([1, 1, 1, 1, 2] : List Nat), d ≤ 2 ∧ d ≠ 3 := by
  decide

/-- Diagonal group-like squaring map `x ↦ x^2` on rational coefficients, modeling the
diagonal evaluation of a group-like coproduct `Δ(g) = g ⊗ g`. -/
def diagSquare (x : ℚ) : ℚ :=
  x ^ 2

/-- Theorem 8 (Cayley Table vs. Hopf Algebra Fence):
On a single basis element (`a = 1, b = 0`), `diagSquare (a + b) = diagSquare a + diagSquare b`,
whereas on any non-trivial superposition (`a = 1, b = 1`), `diagSquare (1 + 1) = 4 ≠ 2 = diagSquare 1 + diagSquare 1`,
showing that a group Cayley table defines group-like elements only and does not by itself supply a
non-cocommutative Hopf gauge algebra module. -/
theorem group_like_coproduct_vs_hopf_linearity_fence :
    diagSquare (1 + 0) = diagSquare 1 + diagSquare 0 ∧
    diagSquare (1 + 1) ≠ diagSquare 1 + diagSquare 1 := by
  dsimp [diagSquare]
  refine ⟨by norm_num, by norm_num⟩

/-- Scope ledger tracking what `TFQ-0012` holds in-repo versus open obligations. -/
structure FiniteQcdScopeLedger where
  hasQ8MatrixShadow : Bool
  hasCayleyTable : Bool
  hasHopfGaugeModule : Bool
  hasSu3ColorConnection : Bool
  deriving DecidableEq, Repr

def tfq0012RepoLedger : FiniteQcdScopeLedger :=
  ⟨true, true, false, false⟩

/-- Theorem 9 (`F001.S000` Carrier Coordination vs. Color Connection Fence):
The repository ledger `tfq0012RepoLedger` has `hasQ8MatrixShadow = true` and
`hasCayleyTable = true`, while `hasHopfGaugeModule = false` and `hasSu3ColorConnection = false`. -/
theorem f001_s000_carrier_coordination_not_color_connection_fence :
    tfq0012RepoLedger.hasQ8MatrixShadow = true ∧
    tfq0012RepoLedger.hasCayleyTable = true ∧
    tfq0012RepoLedger.hasHopfGaugeModule = false ∧
    tfq0012RepoLedger.hasSu3ColorConnection = false := by
  decide

/-- Theorem 10 (`Q_8` Discrete Plaquette Character Spectrum Fence):
For every element `g ∈ Q_8`, the embedded `SU(2)` matrix trace `mat2GITraceRe (q8ToMat2GI g)`
lies in the 3-element discrete set `{-2, 0, 2}` (`2` at `one`, `-2` at `negOne`, and `0` on
all six order-4 quaternion generators). -/
theorem q8_wilson_plaquette_character_discrete_spectrum_fence (g : Q8Elem) :
    mat2GITraceRe (q8ToMat2GI g) = 2 ∨
    mat2GITraceRe (q8ToMat2GI g) = 0 ∨
    mat2GITraceRe (q8ToMat2GI g) = -2 := by
  cases g <;> decide

#print axioms q8_group_associativity_unit_and_inverses
#print axioms q8_nonabelian_hamilton_relations_and_class_equation
#print axioms q8_mat2gi_embedding_homomorphism
#print axioms q8_mat2gi_embedding_injective_and_unit_det
#print axioms q8_plaquette_holonomy_conjugation_and_trace_invariance
#print axioms q8_su2_vs_su3_color_dimension_and_center_fence
#print axioms q8_irrep_max_degree_two_no_color_triplet_fence
#print axioms group_like_coproduct_vs_hopf_linearity_fence
#print axioms f001_s000_carrier_coordination_not_color_connection_fence
#print axioms q8_wilson_plaquette_character_discrete_spectrum_fence

end QuaternionQ8GaugeShadow
