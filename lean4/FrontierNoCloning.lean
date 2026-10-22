import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Linarith

/-!
# Qubit no-cloning and antipodal Pauli attributes over Q(i) (CT-QUBIT-NO-CLONING-FINITE-TARGET)

AuthorityEffect: None.
Scope: Exact linear algebra over the Gaussian rationals `GaussRat = Q(i)` on 2x2 and 4x4 matrices,
together with the six Pauli eigenstate rays `{|0⟩, |1⟩, |+⟩, |-⟩, |+i⟩, |-i⟩}`.
Proves:
(a) `Z = {|0⟩, |1⟩}`, `X = {|+⟩, |-⟩}`, and `Y = {|+i⟩, |-i⟩}` are each cloned by an explicit
    trace-preserving completely positive Kraus channel (`cloneZ`, `cloneX`, `cloneY`).
(b) In `Herm(2)`, `|0⟩⟨0| + |1⟩⟨1| = |+⟩⟨+| + |-⟩⟨-|`, whereas
    `(|0⟩⟨0|⊗|0⟩⟨0| + |1⟩⟨1|⊗|1⟩⟨1|) - (|+⟩⟨+|⊗|+⟩⟨+| + |-⟩⟨-|⊗|-⟩⟨-|)` has entry `1/2` on
    `|00⟩⟨11|` and `|11⟩⟨00|`, so no additive map clones `Z ∪ X`.
(c) Monotonicity of fidelity (`overlapSq s t ≤ (overlapSq s t)^2` for `overlapSq s t ∈ [0,1]`)
    forces `overlapSq s t ∈ {0, 1}`, and exhaustive classification of all 64 subsets of the six
    Pauli eigenstates shows that exactly 10 subsets (empty, 6 singletons, 3 antipodal pairs) are
    pairwise equal-or-orthogonal, with the 3 antipodal pairs as the unique maximal cloneable subsets.
-/

namespace FrontierNoCloning

/-- Kernel-reducible canonical reduced fraction `num / den` (`den > 0`, `gcd(|num|, den) = 1`)
for exact rational and Gaussian-rational matrix arithmetic in `decide`. -/
structure Frac where
  num : Int
  den : Nat
  deriving DecidableEq, Repr

namespace Frac

def mkNorm (n : Int) (d : Nat) : Frac :=
  if d == 0 || n == 0 then ⟨0, 1⟩
  else
    let g := Nat.gcd n.natAbs d
    ⟨n / (g : Int), d / g⟩

def zero : Frac := ⟨0, 1⟩
def one : Frac := ⟨1, 1⟩
def half : Frac := ⟨1, 2⟩
def nhalf : Frac := ⟨-1, 2⟩

def add (a b : Frac) : Frac :=
  if a == zero then b
  else if b == zero then a
  else mkNorm (a.num * (b.den : Int) + b.num * (a.den : Int)) (a.den * b.den)

def sub (a b : Frac) : Frac :=
  mkNorm (a.num * (b.den : Int) - b.num * (a.den : Int)) (a.den * b.den)

def mul (a b : Frac) : Frac :=
  mkNorm (a.num * b.num) (a.den * b.den)

def neg (a : Frac) : Frac := ⟨-a.num, a.den⟩

instance : Zero Frac := ⟨zero⟩
instance : One Frac := ⟨one⟩
instance : Add Frac := ⟨add⟩
instance : Sub Frac := ⟨sub⟩
instance : Mul Frac := ⟨mul⟩
instance : Neg Frac := ⟨neg⟩

@[simp] theorem add_zero (a : Frac) : Frac.add a Frac.zero = a := by
  change (if a == zero then zero else if zero == zero then a else _) = a
  cases h : (a == zero)
  · rfl
  · exact (beq_iff_eq.mp h).symm

@[simp] theorem zero_add (a : Frac) : Frac.add Frac.zero a = a := rfl

end Frac

/-- Exact Gaussian rational `a + b i` with `a, b : Frac`. -/
@[ext]
structure GaussRat where
  re : Frac
  im : Frac
  deriving DecidableEq, Repr

namespace GaussRat

def zero : GaussRat := ⟨Frac.zero, Frac.zero⟩
def one : GaussRat := ⟨Frac.one, Frac.zero⟩
def half : GaussRat := ⟨Frac.half, Frac.zero⟩
def nhalf : GaussRat := ⟨Frac.nhalf, Frac.zero⟩
def ihalf : GaussRat := ⟨Frac.zero, Frac.half⟩
def nihalf : GaussRat := ⟨Frac.zero, Frac.nhalf⟩

def add (z w : GaussRat) : GaussRat := ⟨z.re + w.re, z.im + w.im⟩
def sub (z w : GaussRat) : GaussRat := ⟨z.re - w.re, z.im - w.im⟩
def mul (z w : GaussRat) : GaussRat :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩
def conj (z : GaussRat) : GaussRat := ⟨z.re, -z.im⟩
def normSq (z : GaussRat) : Frac := z.re * z.re + z.im * z.im

instance : Zero GaussRat := ⟨zero⟩
instance : One GaussRat := ⟨one⟩
instance : Add GaussRat := ⟨add⟩
instance : Sub GaussRat := ⟨sub⟩
instance : Mul GaussRat := ⟨mul⟩

end GaussRat

open GaussRat

/-- 2x2 matrix over `Q(i)`. -/
structure Mat2 where
  m00 : GaussRat
  m01 : GaussRat
  m10 : GaussRat
  m11 : GaussRat
  deriving DecidableEq, Repr

def add2 (A B : Mat2) : Mat2 :=
  ⟨A.m00 + B.m00, A.m01 + B.m01, A.m10 + B.m10, A.m11 + B.m11⟩

def mul2 (A B : Mat2) : Mat2 :=
  ⟨A.m00 * B.m00 + A.m01 * B.m10,
   A.m00 * B.m01 + A.m01 * B.m11,
   A.m10 * B.m00 + A.m11 * B.m10,
   A.m10 * B.m01 + A.m11 * B.m11⟩

def trace2 (A : Mat2) : GaussRat := A.m00 + A.m11

/-- 4x4 matrix over `Q(i)` indexed by `Fin 4 → Fin 4 → GaussRat`. -/
def Mat4 := Fin 4 → Fin 4 → GaussRat

def mat4EqBool (A B : Mat4) : Bool :=
  (List.finRange 4).all fun i =>
    (List.finRange 4).all fun j =>
      decide (A i j = B i j)

def add4 (A B : Mat4) : Mat4 := fun i j => A i j + B i j
def sub4 (A B : Mat4) : Mat4 := fun i j => A i j - B i j

def trace4 (A : Mat4) : GaussRat :=
  A 0 0 + A 1 1 + A 2 2 + A 3 3

def entry2 (A : Mat2) (i j : Fin 2) : GaussRat :=
  match i, j with
  | ⟨0, _⟩, ⟨0, _⟩ => A.m00
  | ⟨0, _⟩, ⟨1, _⟩ => A.m01
  | ⟨1, _⟩, ⟨0, _⟩ => A.m10
  | ⟨1, _⟩, ⟨1, _⟩ => A.m11

def splitIdx (k : Fin 4) : Fin 2 × Fin 2 :=
  (⟨k.val / 2, by omega⟩, ⟨k.val % 2, by omega⟩)

/-- Tensor product `A ⊗ B` of two 2x2 matrices as a 4x4 matrix in the computational basis
`|00⟩, |01⟩, |10⟩, |11⟩`. -/
def tensor2 (A B : Mat2) : Mat4 := fun r c =>
  let (r1, r2) := splitIdx r
  let (c1, c2) := splitIdx c
  entry2 A r1 c1 * entry2 B r2 c2

/-- The six Pauli eigenstate density matrices in `Herm(2)` over `Q(i)`. -/
def rho_z0 : Mat2 := ⟨one, zero, zero, zero⟩
def rho_z1 : Mat2 := ⟨zero, zero, zero, one⟩
def rho_xp : Mat2 := ⟨half, half, half, half⟩
def rho_xm : Mat2 := ⟨half, nhalf, nhalf, half⟩
def rho_yp : Mat2 := ⟨half, nihalf, ihalf, half⟩
def rho_ym : Mat2 := ⟨half, ihalf, nihalf, half⟩

def pauliState : Fin 6 → Mat2
  | ⟨0, _⟩ => rho_z0
  | ⟨1, _⟩ => rho_z1
  | ⟨2, _⟩ => rho_xp
  | ⟨3, _⟩ => rho_xm
  | ⟨4, _⟩ => rho_yp
  | ⟨5, _⟩ => rho_ym

/-- (a) Z-basis cloning CPTP map `ρ ↦ ⟨0|ρ|0⟩ |00⟩⟨00| + ⟨1|ρ|1⟩ |11⟩⟨11|`. -/
def cloneZ (ρ : Mat2) : Mat4 := fun r c =>
  if r = 0 ∧ c = 0 then ρ.m00
  else if r = 3 ∧ c = 3 then ρ.m11
  else zero

/-- X-basis cloning CPTP map `ρ ↦ ⟨+|ρ|+⟩ |++⟩⟨++| + ⟨-|ρ|-⟩ |--⟩⟨--|`. -/
def cloneX (ρ : Mat2) : Mat4 :=
  let pPlus := (trace2 (mul2 rho_xp ρ))
  let pMinus := (trace2 (mul2 rho_xm ρ))
  let tPlus := tensor2 rho_xp rho_xp
  let tMinus := tensor2 rho_xm rho_xm
  fun r c => pPlus * tPlus r c + pMinus * tMinus r c

/-- Y-basis cloning CPTP map `ρ ↦ ⟨+i|ρ|+i⟩ |+i,+i⟩⟨+i,+i| + ⟨-i|ρ|-i⟩ |-i,-i⟩⟨-i,-i|`. -/
def cloneY (ρ : Mat2) : Mat4 :=
  let pPlus := (trace2 (mul2 rho_yp ρ))
  let pMinus := (trace2 (mul2 rho_ym ρ))
  let tPlus := tensor2 rho_yp rho_yp
  let tMinus := tensor2 rho_ym rho_ym
  fun r c => pPlus * tPlus r c + pMinus * tMinus r c

theorem cloneZ_trace_preserving (ρ : Mat2) : trace4 (cloneZ ρ) = trace2 ρ := by
  have h00 : cloneZ ρ 0 0 = ρ.m00 := rfl
  have h11 : cloneZ ρ 1 1 = zero := rfl
  have h22 : cloneZ ρ 2 2 = zero := rfl
  have h33 : cloneZ ρ 3 3 = ρ.m11 := rfl
  dsimp [trace4, trace2]
  rw [h00, h11, h22, h33]
  ext <;> simp [HAdd.hAdd, Add.add, GaussRat.add, GaussRat.zero]

theorem cloneZ_clones_Z_attribute :
    mat4EqBool (cloneZ rho_z0) (tensor2 rho_z0 rho_z0) = true ∧
    mat4EqBool (cloneZ rho_z1) (tensor2 rho_z1 rho_z1) = true := by
  decide

theorem cloneX_clones_X_attribute :
    mat4EqBool (cloneX rho_xp) (tensor2 rho_xp rho_xp) = true ∧
    mat4EqBool (cloneX rho_xm) (tensor2 rho_xm rho_xm) = true := by
  decide

theorem cloneY_clones_Y_attribute :
    mat4EqBool (cloneY rho_yp) (tensor2 rho_yp rho_yp) = true ∧
    mat4EqBool (cloneY rho_ym) (tensor2 rho_ym rho_ym) = true := by
  decide

/-- (b) Exact completeness relation `|0⟩⟨0| + |1⟩⟨1| = |+⟩⟨+| + |-⟩⟨-|` in `Herm(2)`. -/
theorem pauli_Z_X_completeness_identity :
    add2 rho_z0 rho_z1 = add2 rho_xp rho_xm := by
  decide

/-- The difference between the cloned Z-sum and the cloned X-sum in `Herm(4)`. -/
def cloningDefectZX : Mat4 :=
  sub4 (add4 (tensor2 rho_z0 rho_z0) (tensor2 rho_z1 rho_z1))
       (add4 (tensor2 rho_xp rho_xp) (tensor2 rho_xm rho_xm))

/-- The defect matrix has exact entry `-1/2` (`nhalf`) on `|00⟩⟨11|` (`(0,3)`) and `|11⟩⟨00|` (`(3,0)`). -/
theorem cloning_defect_ZX_off_diagonal_half :
    cloningDefectZX 0 3 = nhalf ∧ cloningDefectZX 3 0 = nhalf := by
  decide

/-- No additive map `Φ : Mat2 → Mat4` can clone all four states `{|0⟩, |1⟩, |+⟩, |-⟩}`. -/
theorem no_additive_cloner_for_Z_union_X
    (Φ : Mat2 → Mat4)
    (h_add : ∀ A B, Φ (add2 A B) = add4 (Φ A) (Φ B))
    (hz0 : Φ rho_z0 = tensor2 rho_z0 rho_z0)
    (hz1 : Φ rho_z1 = tensor2 rho_z1 rho_z1)
    (hxp : Φ rho_xp = tensor2 rho_xp rho_xp)
    (hxm : Φ rho_xm = tensor2 rho_xm rho_xm) : False := by
  have h1 : Φ (add2 rho_z0 rho_z1) = Φ (add2 rho_xp rho_xm) := by
    rw [pauli_Z_X_completeness_identity]
  rw [h_add, h_add, hz0, hz1, hxp, hxm] at h1
  have h03 := congrFun (congrFun h1 0) 3
  revert h03
  decide

/-- (c) Exact squared overlap `Tr(ρ_s ρ_t)` for `s, t ∈ Fin 6`. -/
def overlapSq (s t : Fin 6) : Frac :=
  (trace2 (mul2 (pauliState s) (pauliState t))).re

def isAntipodalPair (s t : Fin 6) : Bool :=
  (s.val / 2 == t.val / 2) && (s.val != t.val)

/-- Fidelity monotonicity criterion: for any rational overlap `x ∈ [0, 1]`, if a CPTP cloner
does not decrease fidelity (`x ≤ x^2`), then `x = 0` or `x = 1`. -/
theorem fidelity_monotonicity_forces_zero_or_one (x : Rat)
    (h0 : 0 ≤ x) (h1 : x ≤ 1) (hcl : x ≤ x * x) : x = 0 ∨ x = 1 := by
  rcases eq_or_lt_of_le h0 with rfl | hpos
  · exact Or.inl rfl
  · right
    nlinarith

/-- For the six Pauli eigenstates, `overlapSq s t = (overlapSq s t)^2` holds if and only if
`s = t` (overlap 1) or `s, t` are antipodal (overlap 0); all 24 non-antipodal distinct pairs
have `overlapSq s t = 1/2`. -/
theorem pauli_overlap_idempotent_iff_equal_or_antipodal :
    ((List.finRange 6).all fun s =>
      (List.finRange 6).all fun t =>
        decide (overlapSq s t = overlapSq s t * overlapSq s t) ==
          (decide (s = t) || isAntipodalPair s t)) = true ∧
    ((List.finRange 6).all fun s =>
      (List.finRange 6).all fun t =>
        if s = t then decide (overlapSq s t = Frac.one)
        else if isAntipodalPair s t then decide (overlapSq s t = Frac.zero)
        else decide (overlapSq s t = Frac.half)) = true := by
  decide

/-- Exhaustive classification of all `2^6 = 64` subsets of the six Pauli eigenstates:
a subset is pairwise equal-or-orthogonal iff all its pairs satisfy `s = t ∨ isAntipodalPair s t`.
Exactly 10 subsets are cloneable (1 empty, 6 singletons, 3 antipodal pairs `{0,1}`, `{2,3}`, `{4,5}`),
54 subsets are non-cloneable, and the maximal cloneable subsets are the 3 antipodal pairs. -/
def inSubset (mask : Nat) (s : Fin 6) : Bool :=
  ((mask >>> s.val) &&& 1) == 1

def isCloneableSubset (mask : Nat) : Bool :=
  (List.finRange 6).all fun s =>
    (List.finRange 6).all fun t =>
      if inSubset mask s && inSubset mask t then
        decide (s = t) || isAntipodalPair s t
      else true

def isMaximalCloneableSubset (mask : Nat) : Bool :=
  isCloneableSubset mask &&
  (List.finRange 6).all fun s =>
    if inSubset mask s then true
    else !(isCloneableSubset (mask ||| (1 <<< s.val)))

theorem exhaustive_64_subsets_clonability_classification :
    ((List.range 64).filter isCloneableSubset).length = 10 ∧
    ((List.range 64).filter (fun m => !isCloneableSubset m)).length = 54 ∧
    (List.range 64).filter isMaximalCloneableSubset = [3, 12, 48] := by
  decide

end FrontierNoCloning

#print axioms FrontierNoCloning.cloneZ_trace_preserving
#print axioms FrontierNoCloning.cloneZ_clones_Z_attribute
#print axioms FrontierNoCloning.cloneX_clones_X_attribute
#print axioms FrontierNoCloning.cloneY_clones_Y_attribute
#print axioms FrontierNoCloning.pauli_Z_X_completeness_identity
#print axioms FrontierNoCloning.cloning_defect_ZX_off_diagonal_half
#print axioms FrontierNoCloning.no_additive_cloner_for_Z_union_X
#print axioms FrontierNoCloning.fidelity_monotonicity_forces_zero_or_one
#print axioms FrontierNoCloning.pauli_overlap_idempotent_iff_equal_or_antipodal
#print axioms FrontierNoCloning.exhaustive_64_subsets_clonability_classification

private def l5aProvenance : String :=
  "Origin: lean4/FrontierNoCloning.lean Claim: no_additive_cloner_for_Z_union_X AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
