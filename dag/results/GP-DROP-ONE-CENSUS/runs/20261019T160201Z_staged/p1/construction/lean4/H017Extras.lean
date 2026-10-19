





import HWKernel
import H003ReversibilityGate
import H004FreeLinearization
import H007Complexification
import H011Circle
import H014TensorCompositionBoundary
import H014Interface
import H015IrreversibleFork
import H016ContinuousDynamicsFork
import H017MatrixFiniteRecovery
import H017Fin
import H017Gleason

namespace FableHilbertWalk20260819.H017Extras

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004 (Vec)
open FableHilbertWalk20260819.H017Fin


def IsFieldPack {K : Type} (P : StarRingPack K) : Prop :=
  ∀ a : K, a ≠ P.zero → ∃ b : K, P.mul a b = P.one

theorem one_plus_i_not_unit :
    ¬ ∃ b : GaussInt, GaussInt.gmul ⟨1, 1⟩ b = GaussInt.gone := by
  intro h
  rcases h with ⟨⟨x, y⟩, hxy⟩
  have hre := congrArg GaussInt.re hxy
  have him := congrArg GaussInt.im hxy
  simp [GaussInt.gmul, GaussInt.gone] at hre him
  omega

#print axioms one_plus_i_not_unit

theorem gauss_not_a_field : ¬ IsFieldPack gaussPack := by
  intro h
  have hne : (⟨1, 1⟩ : GaussInt) ≠ gaussPack.zero := by
    intro hz
    have hre := congrArg GaussInt.re hz
    simp [gaussPack, GaussInt.gzero] at hre
  rcases h ⟨1, 1⟩ hne with ⟨b, hb⟩
  exact one_plus_i_not_unit ⟨b, hb⟩

#print axioms gauss_not_a_field


def notSpectral : Mat GaussInt Bool :=
  fun i j =>
    if (i == j) = true then GaussInt.gzero
    else if i then ⟨1, -1⟩ else ⟨1, 1⟩

theorem notSpectral_self_adjoint :
    ∀ i j : Bool, adj gaussPack notSpectral i j = notSpectral i j := by
  intro i j; cases i <;> cases j <;> rfl

#print axioms notSpectral_self_adjoint

theorem sq_ge_four_of_abs_ge_two {x : Int}
    (h : 2 ≤ x ∨ x ≤ -2) : 4 ≤ x * x := by
  rcases h with h | h
  · have hx0 : (0 : Int) ≤ x := by omega
    have : (2 : Int) * 2 ≤ x * x :=
      Int.mul_le_mul h h (by decide : (0 : Int) ≤ 2) hx0
    exact this
  · have hx0 : (0 : Int) ≤ -x := by omega
    have hneg : (2 : Int) ≤ -x := by omega
    have : (2 : Int) * 2 ≤ (-x) * (-x) :=
      Int.mul_le_mul hneg hneg (by decide : (0 : Int) ≤ 2) hx0
    have heq : (-x) * (-x) = x * x := Int.neg_mul_neg x x
    rw [heq] at this
    exact this

#print axioms sq_ge_four_of_abs_ge_two

theorem int_mul_self_ne_two (x : Int) : x * x ≠ 2 := by
  intro h
  rcases Int.le_total x (-2) with hx | hx
  · have : (4 : Int) ≤ x * x := sq_ge_four_of_abs_ge_two (Or.inr hx)
    rw [h] at this
    exact (by decide : ¬ ((4 : Int) ≤ 2)) this
  · rcases Int.le_total 2 x with hy | hy
    · have : (4 : Int) ≤ x * x := sq_ge_four_of_abs_ge_two (Or.inl hy)
      rw [h] at this
      exact (by decide : ¬ ((4 : Int) ≤ 2)) this
    · have : x = -2 ∨ x = -1 ∨ x = 0 ∨ x = 1 ∨ x = 2 := by omega
      rcases this with rfl | rfl | rfl | rfl | rfl
      · cases h
      · cases h
      · cases h
      · cases h
      · cases h

#print axioms int_mul_self_ne_two

theorem int_mul_self_nonneg (x : Int) : (0 : Int) ≤ x * x := by
  rcases Int.le_total x 0 with h | h
  · have hx : (0 : Int) ≤ -x := by omega
    have : (0 : Int) ≤ (-x) * (-x) := Int.mul_nonneg hx hx
    rwa [Int.neg_mul_neg] at this
  · exact Int.mul_nonneg h h

#print axioms int_mul_self_nonneg

theorem int_mul_self_ne_neg_two (y : Int) : y * y ≠ -2 := by
  intro h
  have : (0 : Int) ≤ y * y := int_mul_self_nonneg y
  rw [h] at this
  exact (by decide : ¬ ((0 : Int) ≤ -2)) this

#print axioms int_mul_self_ne_neg_two

theorem no_gauss_sq_two :
    ¬ ∃ z : GaussInt, GaussInt.gmul z z = ⟨2, 0⟩ := by
  intro h
  rcases h with ⟨⟨x, y⟩, hxy⟩
  have hre : x * x - y * y = 2 := by
    have := congrArg GaussInt.re hxy
    simp [GaussInt.gmul] at this
    exact this
  have him : x * y + y * x = 0 := by
    have := congrArg GaussInt.im hxy
    simp [GaussInt.gmul] at this
    exact this
  have him' : x * y + x * y = 0 := by
    rw [Int.mul_comm y x] at him
    exact him
  have h2 : (2 : Int) * (x * y) = 0 := by
    have : x * y + x * y = 2 * (x * y) := (Int.two_mul (x * y)).symm
    rw [this] at him'
    exact him'
  have hxy0 : x * y = 0 := by omega
  rcases Int.mul_eq_zero.mp hxy0 with hx | hy
  · subst hx
    have : y * y = -2 := by omega
    exact int_mul_self_ne_neg_two y this
  · subst hy
    have : x * x = 2 := by omega
    exact int_mul_self_ne_two x this

#print axioms no_gauss_sq_two

def gnormSq (z : GaussInt) : Int :=
  z.re * z.re + z.im * z.im

theorem gnormSq_zero_iff (z : GaussInt) :
    gnormSq z = 0 ↔ z = GaussInt.gzero := by
  constructor
  · intro h
    cases z with
    | mk x y =>
        have hxnn : (0 : Int) ≤ x * x := int_mul_self_nonneg x
        have hynn : (0 : Int) ≤ y * y := int_mul_self_nonneg y
        have hx : x * x = 0 := by
          simp [gnormSq] at h
          omega
        have hy : y * y = 0 := by
          simp [gnormSq] at h
          omega
        have hx0 : x = 0 := by
          rcases Int.mul_eq_zero.mp hx with hx0 | hx0 <;> exact hx0
        have hy0 : y = 0 := by
          rcases Int.mul_eq_zero.mp hy with hy0 | hy0 <;> exact hy0
        simp [GaussInt.gzero, hx0, hy0]
  · intro h
    cases h
    simp [gnormSq, GaussInt.gzero]

#print axioms gnormSq_zero_iff

theorem gnormSq_mul (a b : GaussInt) :
    gnormSq (GaussInt.gmul a b) = gnormSq a * gnormSq b := by
  cases a with
  | mk ar ai =>
      cases b with
      | mk br bi =>
          simp only [GaussInt.gmul, gnormSq, Int.sub_eq_add_neg,
            Int.mul_add, Int.mul_neg,
            Int.neg_neg, Int.mul_comm, Int.mul_left_comm,
            Int.add_assoc, Int.add_comm, Int.add_left_comm]
          have hcan (A B C D t : Int) :
              A + (B + (t + (t + (C + (D + (-t + -t)))))) =
                A + (B + (C + D)) := by omega
          exact hcan _ _ _ _ _

#print axioms gnormSq_mul

theorem gauss_mul_eq_zero {a b : GaussInt}
    (h : GaussInt.gmul a b = GaussInt.gzero) :
    a = GaussInt.gzero ∨ b = GaussInt.gzero := by
  have hn : gnormSq (GaussInt.gmul a b) = 0 := by
    rw [h]
    simp [gnormSq, GaussInt.gzero]
  rw [gnormSq_mul] at hn
  have : gnormSq a = 0 ∨ gnormSq b = 0 :=
    Int.mul_eq_zero.mp hn
  rcases this with ha | hb
  · exact Or.inl ((gnormSq_zero_iff a).mp ha)
  · exact Or.inr ((gnormSq_zero_iff b).mp hb)

#print axioms gauss_mul_eq_zero

theorem notSpectral_apply (v : Vec GaussInt Bool) :
    applyMat gaussPack enumBool notSpectral v false =
      GaussInt.gmul ⟨1, 1⟩ (v true) ∧
    applyMat gaussPack enumBool notSpectral v true =
      GaussInt.gmul ⟨1, -1⟩ (v false) := by
  constructor
  · unfold applyMat enumBool
    simp only [List.map, rsum]
    have h00 : notSpectral false false = GaussInt.gzero := rfl
    have h01 : notSpectral false true = ⟨1, 1⟩ := rfl
    rw [h00, h01]
    simp [gaussPack, GaussInt.gadd, GaussInt.gmul, GaussInt.gzero]
  · unfold applyMat enumBool
    simp only [List.map, rsum]
    have h10 : notSpectral true false = ⟨1, -1⟩ := rfl
    have h11 : notSpectral true true = GaussInt.gzero := rfl
    rw [h10, h11]
    simp [gaussPack, GaussInt.gadd, GaussInt.gmul, GaussInt.gzero]

#print axioms notSpectral_apply

theorem gadd_mul (a b c : GaussInt) :
    GaussInt.gmul (GaussInt.gadd a b) c =
      GaussInt.gadd (GaussInt.gmul a c) (GaussInt.gmul b c) := by
  rw [GaussInt.gmul_comm, GaussInt.gmul_add, GaussInt.gmul_comm a c,
    GaussInt.gmul_comm b c]

#print axioms gadd_mul

theorem gneg_mul (a b : GaussInt) :
    GaussInt.gmul (GaussInt.gneg a) b =
      GaussInt.gneg (GaussInt.gmul a b) := by
  have hL :
      GaussInt.gmul (GaussInt.gadd a (GaussInt.gneg a)) b =
        GaussInt.gzero := by
    rw [GaussInt.gadd_neg, GaussInt.gmul_comm, GaussInt.gmul_zero]
  have hR :
      GaussInt.gmul (GaussInt.gadd a (GaussInt.gneg a)) b =
        GaussInt.gadd (GaussInt.gmul a b)
          (GaussInt.gmul (GaussInt.gneg a) b) :=
    gadd_mul a (GaussInt.gneg a) b
  have hsum :
      GaussInt.gadd (GaussInt.gmul a b)
        (GaussInt.gmul (GaussInt.gneg a) b) =
        GaussInt.gzero :=
    hR.symm.trans hL
  have hcancel :
      GaussInt.gadd
        (GaussInt.gadd (GaussInt.gmul a b)
          (GaussInt.gmul (GaussInt.gneg a) b))
        (GaussInt.gneg (GaussInt.gmul a b)) =
        GaussInt.gadd GaussInt.gzero
          (GaussInt.gneg (GaussInt.gmul a b)) :=
    congrArg (fun z => GaussInt.gadd z
      (GaussInt.gneg (GaussInt.gmul a b))) hsum
  have hL2 :
      GaussInt.gadd
        (GaussInt.gadd (GaussInt.gmul a b)
          (GaussInt.gmul (GaussInt.gneg a) b))
        (GaussInt.gneg (GaussInt.gmul a b)) =
        GaussInt.gmul (GaussInt.gneg a) b := by
    rw [GaussInt.gadd_comm (GaussInt.gmul a b), GaussInt.gadd_assoc,
      GaussInt.gadd_neg, GaussInt.gadd_comm, GaussInt.gzero_add]
  have hR2 :
      GaussInt.gadd GaussInt.gzero
        (GaussInt.gneg (GaussInt.gmul a b)) =
        GaussInt.gneg (GaussInt.gmul a b) :=
    GaussInt.gzero_add _
  exact (hL2.symm.trans hcancel).trans hR2

#print axioms gneg_mul

def SpectralEigenvalueExtra {Q : Type} [DecidableEq Q]
    (E : Enum Q) : Prop :=
  ∀ (A : Mat GaussInt Q),
    (∀ i j, adj gaussPack A i j = A i j) →
      ∃ (lam : GaussInt) (v : Vec GaussInt Q),
        (∃ q, v q ≠ gaussPack.zero) ∧
          ∀ i, applyMat gaussPack E A v i = gaussPack.mul lam (v i)

theorem notSpectral_has_no_gauss_eigenvalue :
    ¬ ∃ (lam : GaussInt) (v : Vec GaussInt Bool),
      (∃ q, v q ≠ gaussPack.zero) ∧
        ∀ i : Bool,
          applyMat gaussPack enumBool notSpectral v i =
            gaussPack.mul lam (v i) := by
  intro h
  rcases h with ⟨lam, v, ⟨q, hq⟩, heig⟩
  have happ := notSpectral_apply v
  have hf := heig false
  have ht := heig true
  rw [happ.1] at hf
  rw [happ.2] at ht
  simp only [gaussPack] at hf ht
  have hlam2 :
      GaussInt.gmul lam (GaussInt.gmul lam (v true)) =
        GaussInt.gmul ⟨2, 0⟩ (v true) := by
    have h1 :
        GaussInt.gmul lam (GaussInt.gmul lam (v true)) =
          GaussInt.gmul lam (GaussInt.gmul ⟨1, -1⟩ (v false)) :=
      congrArg (fun z => GaussInt.gmul lam z) ht.symm
    have h2 :
        GaussInt.gmul lam (GaussInt.gmul ⟨1, -1⟩ (v false)) =
          GaussInt.gmul ⟨1, -1⟩ (GaussInt.gmul lam (v false)) := by
      rw [← GaussInt.gmul_assoc, GaussInt.gmul_comm lam,
        GaussInt.gmul_assoc]
    have h3 :
        GaussInt.gmul ⟨1, -1⟩ (GaussInt.gmul lam (v false)) =
          GaussInt.gmul ⟨1, -1⟩ (GaussInt.gmul ⟨1, 1⟩ (v true)) :=
      congrArg (fun z => GaussInt.gmul ⟨1, -1⟩ z) hf.symm
    have h4 :
        GaussInt.gmul ⟨1, -1⟩ (GaussInt.gmul ⟨1, 1⟩ (v true)) =
          GaussInt.gmul (GaussInt.gmul ⟨1, -1⟩ ⟨1, 1⟩) (v true) :=
      (GaussInt.gmul_assoc _ _ _).symm
    have h5 : GaussInt.gmul ⟨1, -1⟩ ⟨1, 1⟩ = ⟨2, 0⟩ := by decide
    rw [h1, h2, h3, h4, h5]
  have hcancel :
      GaussInt.gmul (GaussInt.gmul lam lam) (v true) =
        GaussInt.gmul ⟨2, 0⟩ (v true) := by
    rw [← GaussInt.gmul_assoc] at hlam2
    exact hlam2
  have hdiff :
      GaussInt.gmul (GaussInt.gadd (GaussInt.gmul lam lam)
          (GaussInt.gneg ⟨2, 0⟩)) (v true) =
        GaussInt.gzero := by
    have hsum :
        GaussInt.gadd (GaussInt.gmul (GaussInt.gmul lam lam) (v true))
          (GaussInt.gneg (GaussInt.gmul ⟨2, 0⟩ (v true))) =
          GaussInt.gzero := by
      rw [hcancel, GaussInt.gadd_neg]
    have hdist := gadd_mul (GaussInt.gmul lam lam)
      (GaussInt.gneg ⟨2, 0⟩) (v true)
    have hneg := gneg_mul ⟨2, 0⟩ (v true)
    rw [hdist, hneg]
    exact hsum
  have hzero := gauss_mul_eq_zero hdiff
  rcases hzero with hlam | hv
  · have hsq : GaussInt.gmul lam lam = ⟨2, 0⟩ := by
      have hcancel' :
          GaussInt.gadd
            (GaussInt.gadd (GaussInt.gmul lam lam) (GaussInt.gneg ⟨2, 0⟩))
            ⟨2, 0⟩ =
          GaussInt.gadd GaussInt.gzero ⟨2, 0⟩ :=
        congrArg (fun z => GaussInt.gadd z ⟨2, 0⟩) hlam
      have hL :
          GaussInt.gadd
            (GaussInt.gadd (GaussInt.gmul lam lam) (GaussInt.gneg ⟨2, 0⟩))
            ⟨2, 0⟩ =
          GaussInt.gmul lam lam := by
        rw [GaussInt.gadd_assoc]
        have hn :
            GaussInt.gadd (GaussInt.gneg ⟨2, 0⟩) ⟨2, 0⟩ =
              GaussInt.gzero := by
          rw [GaussInt.gadd_comm, GaussInt.gadd_neg]
        rw [hn, GaussInt.gadd_comm, GaussInt.gzero_add]
      have hR :
          GaussInt.gadd GaussInt.gzero ⟨2, 0⟩ = ⟨2, 0⟩ :=
        GaussInt.gzero_add _
      exact hL.symm.trans (hcancel'.trans hR)
    exact no_gauss_sq_two ⟨lam, hsq⟩
  · have ht0 : GaussInt.gmul ⟨1, -1⟩ (v false) = GaussInt.gzero := by
      rw [hv, GaussInt.gmul_zero] at ht
      exact ht
    have hvf : v false = GaussInt.gzero := by
      have hone : (⟨1, -1⟩ : GaussInt) ≠ GaussInt.gzero := by
        intro hz
        have him := congrArg GaussInt.im hz
        simp [GaussInt.gzero] at him
      rcases gauss_mul_eq_zero ht0 with h1 | h0
      · exact absurd h1 hone
      · exact h0
    have hvz : ∀ i : Bool, v i = gaussPack.zero := by
      intro i
      cases i
      · exact hvf
      · exact hv
    exact hq (hvz q)

#print axioms notSpectral_has_no_gauss_eigenvalue

theorem spectral_eigenvalue_extra_fails_on_two_label :
    ¬ SpectralEigenvalueExtra enumBool := by
  intro h
  have hs := h notSpectral notSpectral_self_adjoint
  exact notSpectral_has_no_gauss_eigenvalue hs

#print axioms spectral_eigenvalue_extra_fails_on_two_label


theorem remaining_extras_for_ordinary_mnC :
    ¬ IsFieldPack gaussPack ∧
      ¬ SpectralEigenvalueExtra enumBool ∧
      ¬ FableHilbertWalk20260819.H017Gleason.GleasonDimAtLeastThree
          enumBool ∧
      (¬ ∃ σ : Bool → Bool,
        ∀ q : Bool, σ (σ q) = FableHilbertWalk20260819.H003.toggle q) ∧
      FableHilbertWalk20260819.H011Circle.ConnectednessShadow
        FableHilbertWalk20260819.H011Circle.gaussUnitCarrier ∧
      FableHilbertWalk20260819.H011Circle.ConnectednessShadow
        FableHilbertWalk20260819.H011Circle.cyc3Carrier ∧
      (¬ ∀ u v p,
        FableHilbertWalk20260819.H014Interface.dumpRight u v p =
          FableHilbertWalk20260819.H014.tensor u v p) ∧
      (¬ ∃ A : Bool → Bool → Int,
        ∀ i j : Bool,
          FableHilbertWalk20260819.H017Matrix.pauliY i j =
            FableHilbertWalk20260819.H007.embed (A i j)) :=
  ⟨gauss_not_a_field,
    spectral_eigenvalue_extra_fails_on_two_label,
    FableHilbertWalk20260819.H017Gleason.two_label_host_not_gleason_dimension,
    FableHilbertWalk20260819.H016.no_report_half_step,
    FableHilbertWalk20260819.H011Circle.gauss_units_meet_connectedness_shadow,
    FableHilbertWalk20260819.H011Circle.cyc3_meets_connectedness_shadow,
    FableHilbertWalk20260819.H014Interface.dumpRight_not_tensor,
    FableHilbertWalk20260819.H017Matrix.pauliY_not_integer_matrix⟩

#print axioms remaining_extras_for_ordinary_mnC

end FableHilbertWalk20260819.H017Extras

private def l5aProvenance : String :=
  "Origin: lean4/H017Extras.lean Claim: one_plus_i_not_unit AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
