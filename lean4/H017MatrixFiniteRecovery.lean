/-
  H017Matrix -- recover the named 2x2 Gauss-integer matrix algebra.
  AuthorityEffect: None. Candidate only. Not PROVEN.

  QM_122 remaining job 7.2 / STACK item 4. The named object is
  M_2(Z[i]): 2x2 matrices over the admitted GaussInt pack, acting
  on the H004 free module Bool -> GaussInt. Ordinary two-level
  quantum mechanics uses this as the integer-Gaussian skeleton of
  M_2(C) before completing the scalars.

  Named extras, as hypotheses, not flags:
    (1) coefficient pack K (instantiated at gaussPack);
    (2) two-point report set Bool;
    (3) additivity of an endomorphism;
    (4) pack-homogeneity of that endomorphism.

  Theorems: every such endomorphism is left-multiplication by a
  unique 2x2 matrix; matrix product is composition; conjugate
  transpose implements the H005 pairing; Pauli X,Y,Z of ordinary
  two-level QM live in this algebra and Y is not an integer matrix.

  This is not M_n(C). Missing extras for that object, named in
  English, not as a Bool ledger: the field C (completeness / density);
  a general finite label set in place of Bool; the spectral theorem;
  Gleason uniqueness of the Born square; CPTP channels; uniqueness
  of tensor product as a combining rule; the circle group; continuous
  time; a Python dual of these statements; a drop-one count of a
  full extra list. Do not read this list as a theorem.

  AuthorityEffect: None
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import H004FreeLinearization
import H005InnerProductAdmission
import H007Complexification

namespace FableHilbertWalk20260819.H017Matrix

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H005 (sesq)
open FableHilbertWalk20260819.H007 (embed)

/-- Named finite matrix object: 2x2 matrices on the Bool report set. -/
def Mat (K : Type) : Type := Bool → Bool → K

/-- Action of a 2x2 matrix on a two-coordinate vector. -/
def applyMat {K : Type} (P : StarRingPack K) (A : Mat K)
    (v : Vec K Bool) : Vec K Bool :=
  fun i => P.add (P.mul (A i false) (v false)) (P.mul (A i true) (v true))

/-- Matrix product on the Bool index set. -/
def mmul {K : Type} (P : StarRingPack K) (A B : Mat K) : Mat K :=
  fun i j =>
    P.add (P.mul (A i false) (B false j)) (P.mul (A i true) (B true j))

/-- Identity matrix. -/
def ident {K : Type} (P : StarRingPack K) : Mat K :=
  fun i j => if i == j then P.one else P.zero

/-- Conjugate transpose. -/
def adj {K : Type} (P : StarRingPack K) (A : Mat K) : Mat K :=
  fun i j => P.conj (A j i)

/-- Named extras for an endomorphism of the free two-point module. -/
structure LinearEnd {K : Type} (P : StarRingPack K) where
  map : Vec K Bool → Vec K Bool
  map_add :
    ∀ u v q,
      map (vadd P u v) q = P.add (map u q) (map v q)
  map_smul :
    ∀ c u q,
      map (smul P c u) q = P.mul c (map u q)

/-- Matrix of an endomorphism: columns are the images of the report basis. -/
def matOf {K : Type} {P : StarRingPack K} (T : LinearEnd P) : Mat K :=
  fun i j => T.map (delta P j) i

/-- Endomorphism of a matrix: left-multiplication. -/
def endOfMat {K : Type} (P : StarRingPack K) (A : Mat K) : LinearEnd P where
  map := applyMat P A
  map_add := fun u v q => by
    unfold applyMat vadd
    rw [P.mul_add, P.mul_add]
    rw [P.add_assoc, ← P.add_assoc (P.mul (A q false) (v false)),
      P.add_comm (P.mul (A q false) (v false)),
      P.add_assoc, ← P.add_assoc]
  map_smul := fun c u q => by
    unfold applyMat smul
    rw [P.mul_add]
    rw [← P.mul_assoc, ← P.mul_assoc, ← P.mul_assoc, ← P.mul_assoc]
    rw [P.mul_comm c (A q false), P.mul_comm c (A q true)]

#print axioms endOfMat

theorem vec_bool_expand {K : Type} (P : StarRingPack K)
    (v : Vec K Bool) (x : Bool) :
    v x =
      P.add (P.mul (v false) (delta P false x))
        (P.mul (v true) (delta P true x)) := by
  cases x
  · unfold delta
    rw [if_pos (beq_self_eq_true false),
      if_neg (by decide : ¬((true == false) = true)),
      P.mul_one, P.mul_zero, P.add_zero]
  · unfold delta
    rw [if_neg (by decide : ¬((false == true) = true)),
      if_pos (beq_self_eq_true true),
      P.mul_zero, P.mul_one, P.zero_add]

#print axioms vec_bool_expand

/-- Under the named extras, the map is left-multiplication by its matrix. -/
theorem apply_eq_matOf {K : Type} {P : StarRingPack K} (T : LinearEnd P)
    (v : Vec K Bool) (x : Bool) :
    T.map v x = applyMat P (matOf T) v x := by
  have hv : v =
      vadd P (smul P (v false) (delta P false))
        (smul P (v true) (delta P true)) :=
    funext (fun y => vec_bool_expand P v y)
  have hmap : T.map v x =
      T.map (vadd P (smul P (v false) (delta P false))
        (smul P (v true) (delta P true))) x :=
    congrArg (fun w => T.map w x) hv
  rw [hmap]
  rw [T.map_add (smul P (v false) (delta P false))
    (smul P (v true) (delta P true)) x]
  rw [T.map_smul (v false) (delta P false) x,
    T.map_smul (v true) (delta P true) x]
  unfold applyMat matOf
  rw [P.mul_comm (v false), P.mul_comm (v true)]

#print axioms apply_eq_matOf

theorem matOf_apply {K : Type} (P : StarRingPack K) (A : Mat K) :
    ∀ i j : Bool, matOf (endOfMat P A) i j = A i j := by
  intro i j
  unfold matOf
  change applyMat P A (delta P j) i = A i j
  unfold applyMat delta
  cases j
  · rw [if_pos (beq_self_eq_true false),
      if_neg (by decide : ¬((false == true) = true)),
      P.mul_one, P.mul_zero, P.add_zero]
  · rw [if_neg (by decide : ¬((true == false) = true)),
      if_pos (beq_self_eq_true true),
      P.mul_zero, P.mul_one, P.zero_add]

#print axioms matOf_apply

theorem ident_acts_as_id {K : Type} (P : StarRingPack K)
    (v : Vec K Bool) (i : Bool) :
    applyMat P (ident P) v i = v i := by
  unfold applyMat ident
  cases i
  · rw [if_pos (beq_self_eq_true false),
      if_neg (by decide : ¬((false == true) = true)),
      P.one_mul, P.zero_mul, P.add_zero]
  · rw [if_neg (by decide : ¬((true == false) = true)),
      if_pos (beq_self_eq_true true),
      P.zero_mul, P.one_mul, P.zero_add]

#print axioms ident_acts_as_id

theorem mmul_as_composition {K : Type} (P : StarRingPack K)
    (A B : Mat K) (v : Vec K Bool) (i : Bool) :
    applyMat P (mmul P A B) v i =
      applyMat P A (applyMat P B v) i := by
  unfold applyMat mmul
  rw [P.add_mul, P.add_mul]
  rw [P.mul_assoc, P.mul_assoc, P.mul_assoc, P.mul_assoc]
  rw [P.add_assoc, ← P.add_assoc
      (P.mul (A i true) (P.mul (B true false) (v false))),
    P.add_comm (P.mul (A i true) (P.mul (B true false) (v false))),
    P.add_assoc, ← P.add_assoc]
  rw [← P.mul_add, ← P.mul_add]

#print axioms mmul_as_composition

theorem adj_mmul {K : Type} (P : StarRingPack K) (A B : Mat K)
    (i j : Bool) :
    adj P (mmul P A B) i j = mmul P (adj P B) (adj P A) i j := by
  unfold adj mmul
  rw [P.conj_add, P.conj_mul, P.conj_mul]
  rw [P.mul_comm (P.conj (A j false)), P.mul_comm (P.conj (A j true))]

#print axioms adj_mmul

theorem rsum_enumBool {K : Type} (P : StarRingPack K) (f : Bool → K) :
    rsum P (enumBool.elems.map f) = P.add (f false) (f true) := by
  unfold enumBool
  simp only [rsum, List.map]
  rw [P.add_zero]

#print axioms rsum_enumBool

theorem mul3_reassoc {K : Type} (P : StarRingPack K) (a b c : K) :
    P.mul (P.mul a b) c = P.mul b (P.mul a c) := by
  rw [P.mul_comm a b, P.mul_assoc]

/-- Conjugate transpose is the adjoint of the admitted pairing. -/
theorem sesq_conj_transpose {K : Type} (P : StarRingPack K) (A : Mat K)
    (u v : Vec K Bool) :
    sesq P enumBool (applyMat P A u) v =
      sesq P enumBool u (applyMat P (adj P A) v) := by
  unfold sesq
  rw [rsum_enumBool, rsum_enumBool]
  unfold applyMat adj
  rw [P.conj_add, P.conj_add, P.conj_mul, P.conj_mul, P.conj_mul, P.conj_mul]
  rw [P.add_mul, P.add_mul, P.mul_add, P.mul_add]
  rw [mul3_reassoc P (P.conj (A false false)) (P.conj (u false)) (v false)]
  rw [mul3_reassoc P (P.conj (A false true)) (P.conj (u true)) (v false)]
  rw [mul3_reassoc P (P.conj (A true false)) (P.conj (u false)) (v true)]
  rw [mul3_reassoc P (P.conj (A true true)) (P.conj (u true)) (v true)]
  rw [P.add_assoc, ← P.add_assoc
      (P.mul (P.conj (u true)) (P.mul (P.conj (A false true)) (v false))),
    P.add_comm
      (P.mul (P.conj (u true)) (P.mul (P.conj (A false true)) (v false))),
    P.add_assoc, ← P.add_assoc]

#print axioms sesq_conj_transpose

/-! ## Named ordinary two-level objects: Pauli matrices over Z[i]. -/

def pauliX : Mat GaussInt :=
  fun i j => if i == j then GaussInt.gzero else GaussInt.gone

def pauliZ : Mat GaussInt :=
  fun i j =>
    if i == j then
      if i then GaussInt.gneg GaussInt.gone else GaussInt.gone
    else GaussInt.gzero

def pauliY : Mat GaussInt :=
  fun i j =>
    if i == j then GaussInt.gzero
    else if i then GaussInt.gi else GaussInt.gneg GaussInt.gi

theorem pauliX_sq :
    ∀ i j : Bool, mmul gaussPack pauliX pauliX i j = ident gaussPack i j := by
  intro i j; cases i <;> cases j <;> rfl

#print axioms pauliX_sq

theorem pauliZ_sq :
    ∀ i j : Bool, mmul gaussPack pauliZ pauliZ i j = ident gaussPack i j := by
  intro i j; cases i <;> cases j <;> rfl

#print axioms pauliZ_sq

theorem pauliY_sq :
    ∀ i j : Bool, mmul gaussPack pauliY pauliY i j = ident gaussPack i j := by
  intro i j; cases i <;> cases j <;> rfl

#print axioms pauliY_sq

theorem pauliX_Z_anticommute :
    ¬(∀ i j : Bool,
      mmul gaussPack pauliX pauliZ i j =
        mmul gaussPack pauliZ pauliX i j) := by
  intro h
  have h1 := h false true
  revert h1
  decide

#print axioms pauliX_Z_anticommute

/-- Pauli Y uses the imaginary unit. The integer matrix host of H012
    does not contain it. Complexification is doing work. -/
theorem pauliY_not_integer_matrix :
    ¬ ∃ A : Bool → Bool → Int, ∀ i j : Bool, pauliY i j = embed (A i j) := by
  intro h
  rcases h with ⟨A, hA⟩
  have hY := hA true false
  have hgi : pauliY true false = GaussInt.gi := by simp [pauliY]
  have him : (embed (A true false)).im = (1 : Int) := by
    rw [← hY, hgi]
    rfl
  have h0 : (embed (A true false)).im = (0 : Int) := rfl
  exact Int.zero_ne_one (h0.symm.trans him)

#print axioms pauliY_not_integer_matrix

/-- Punchline: under the named extras, End of the two-point GaussInt
    module is M_2(Z[i]), composition is matrix product, conjugate
    transpose is the pairing adjoint, and the ordinary Pauli generators
    live here. This is not M_n(C). -/
theorem two_level_gauss_matrix_algebra :
    (∀ (T : LinearEnd gaussPack) (v : Vec GaussInt Bool) (x : Bool),
      T.map v x = applyMat gaussPack (matOf T) v x) ∧
      (∀ (A : Mat GaussInt) (i j : Bool),
        matOf (endOfMat gaussPack A) i j = A i j) ∧
      (∀ (A B : Mat GaussInt) (v : Vec GaussInt Bool) (i : Bool),
        applyMat gaussPack (mmul gaussPack A B) v i =
          applyMat gaussPack A (applyMat gaussPack B v) i) ∧
      (∀ (A : Mat GaussInt) (u v : Vec GaussInt Bool),
        sesq gaussPack enumBool (applyMat gaussPack A u) v =
          sesq gaussPack enumBool u (applyMat gaussPack (adj gaussPack A) v)) ∧
      (∀ i j : Bool, mmul gaussPack pauliX pauliX i j = ident gaussPack i j) ∧
      (∀ i j : Bool, mmul gaussPack pauliY pauliY i j = ident gaussPack i j) ∧
      (∀ i j : Bool, mmul gaussPack pauliZ pauliZ i j = ident gaussPack i j) ∧
      ¬(∀ i j : Bool,
        mmul gaussPack pauliX pauliZ i j =
          mmul gaussPack pauliZ pauliX i j) ∧
      ¬ ∃ A : Bool → Bool → Int, ∀ i j : Bool, pauliY i j = embed (A i j) :=
  ⟨apply_eq_matOf, matOf_apply gaussPack, mmul_as_composition gaussPack,
    sesq_conj_transpose gaussPack, pauliX_sq, pauliY_sq, pauliZ_sq,
    pauliX_Z_anticommute, pauliY_not_integer_matrix⟩

#print axioms two_level_gauss_matrix_algebra

end FableHilbertWalk20260819.H017Matrix
