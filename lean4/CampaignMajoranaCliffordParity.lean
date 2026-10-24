module

public import Mathlib.LinearAlgebra.Matrix.ConjTranspose
public import Mathlib.LinearAlgebra.Matrix.PosDef
public import Mathlib.Analysis.Complex.Order
public import Mathlib.Algebra.Algebra.Subalgebra.Basic
public import Mathlib.Tactic

/-!
# CAR-to-Majorana algebra with explicit assumptions

AuthorityEffect: None.
CAR and the complex star-algebra are inputs. Equality of generated subalgebras
is not a proof of an abstract Clifford-algebra isomorphism. No physical parity
superselection principle is inferred.
-/

@[expose] public section

open Complex
open scoped ComplexOrder
namespace CampaignMajoranaCliffordParity
noncomputable section

variable {A K : Type*} [Ring A]

def ac (x y : A) : A := x * y + y * x

theorem ac_comm (x y : A) : ac x y = ac y x := add_comm _ _
theorem ac_add_left (x y z : A) : ac (x + y) z = ac x z + ac y z := by
  unfold ac; noncomm_ring
theorem ac_sub_left (x y z : A) : ac (x - y) z = ac x z - ac y z := by
  unfold ac; noncomm_ring
theorem ac_add_right (x y z : A) : ac x (y + z) = ac x y + ac x z := by
  unfold ac; noncomm_ring
theorem ac_sub_right (x y z : A) : ac x (y - z) = ac x y - ac x z := by
  unfold ac; noncomm_ring

variable [Algebra ℂ A]
theorem ac_smul_left (r : ℂ) (x y : A) : ac (r • x) y = r • ac x y := by
  simp [ac, smul_add]
theorem ac_smul_right (r : ℂ) (x y : A) : ac x (r • y) = r • ac x y := by
  simp [ac, smul_add]

variable [StarRing A] [StarModule ℂ A] [DecidableEq K]

/-- CAR is supplied as a hypothesis, rather than claimed from finite primitives. -/
structure CARFamily (K A : Type*) [DecidableEq K] [Ring A] [StarRing A]
    [Algebra ℂ A] [StarModule ℂ A] where
  c : K → A
  aa : ∀ i j, ac (c i) (c j) = 0
  mixed : ∀ i j, ac (c i) (star (c j)) = if i = j then 1 else 0

namespace CARFamily
variable (F : CARFamily K A)

def gamma (a : K × Bool) : A :=
  if a.2 then (-I) • (F.c a.1 - star (F.c a.1))
  else F.c a.1 + star (F.c a.1)

theorem dd (i j : K) : ac (star (F.c i)) (star (F.c j)) = 0 := by
  have h := congrArg star (F.aa j i)
  simpa [ac] using h

theorem mixed_rev (i j : K) :
    ac (star (F.c i)) (F.c j) = if i = j then 1 else 0 := by
  rw [ac_comm, F.mixed]
  simp [eq_comm]

theorem gamma_star (a : K × Bool) : star (F.gamma a) = F.gamma a := by
  rcases a with ⟨i, b⟩
  cases b <;> simp [gamma, star_smul, sub_eq_add_neg, add_comm]

theorem gamma_ac (a b : K × Bool) :
    ac (F.gamma a) (F.gamma b) = if a = b then 2 else 0 := by
  rcases a with ⟨i, x⟩
  rcases b with ⟨j, y⟩
  cases x <;> cases y <;>
    simp only [gamma, Bool.false_eq_true, ↓reduceIte, ac_add_left, ac_add_right,
      ac_sub_left, ac_sub_right, ac_smul_left, ac_smul_right, F.aa,
      F.mixed, F.mixed_rev, F.dd] <;>
    by_cases h : i = j <;> simp [h, smul_smul] <;> norm_num

theorem recover_c (i : K) :
    F.c i = (1 / 2 : ℂ) • (F.gamma (i, false) + I • F.gamma (i, true)) := by
  simp only [gamma, ↓reduceIte, Bool.false_eq_true, smul_smul]
  norm_num
  module

theorem recover_star_c (i : K) :
    star (F.c i) = (1 / 2 : ℂ) • (F.gamma (i, false) - I • F.gamma (i, true)) := by
  simp only [gamma, ↓reduceIte, Bool.false_eq_true, smul_smul]
  norm_num
  module

/-- The two sets generate the same concrete operator subalgebra. This does not
identify that subalgebra with the abstract Clifford algebra. -/
theorem generated_algebra :
    Algebra.adjoin ℂ (Set.range F.c ∪ Set.range (fun i => star (F.c i))) =
      Algebra.adjoin ℂ (Set.range F.gamma) := by
  have hg (a : K × Bool) : F.gamma a ∈ Algebra.adjoin ℂ (Set.range F.gamma) :=
    Algebra.subset_adjoin ⟨a, rfl⟩
  apply le_antisymm
  · apply Algebra.adjoin_le
    intro x hx
    rcases hx with ⟨i, rfl⟩ | ⟨i, rfl⟩
    · rw [F.recover_c i]
      exact Subalgebra.smul_mem _ (Subalgebra.add_mem _
        (hg (i, false)) (Subalgebra.smul_mem _ (hg (i, true)) _)) _
    · change star (F.c i) ∈ Algebra.adjoin ℂ (Set.range F.gamma)
      rw [F.recover_star_c i]
      exact Subalgebra.smul_mem _ (Subalgebra.sub_mem _
        (hg (i, false)) (Subalgebra.smul_mem _ (hg (i, true)) _)) _
  · apply Algebra.adjoin_le
    rintro x ⟨⟨i, b⟩, rfl⟩
    have hc : F.c i ∈ Algebra.adjoin ℂ
        (Set.range F.c ∪ Set.range (fun i => star (F.c i))) :=
      Algebra.subset_adjoin (Or.inl ⟨i, rfl⟩)
    have hd : star (F.c i) ∈ Algebra.adjoin ℂ
        (Set.range F.c ∪ Set.range (fun i => star (F.c i))) :=
      Algebra.subset_adjoin (Or.inr ⟨i, rfl⟩)
    cases b
    · exact Subalgebra.add_mem _ hc hd
    · exact Subalgebra.smul_mem _ (Subalgebra.sub_mem _ hc hd) _

def occupation (i : K) : A := star (F.c i) * F.c i
def localParity (i : K) : A := 1 - 2 * F.occupation i

theorem annihilate_sq (i : K) : F.c i * F.c i = 0 := by
  have h : (2 : ℂ) • (F.c i * F.c i) = 0 := by
    simpa [ac, two_smul ℂ] using F.aa i i
  exact (smul_eq_zero.mp h).resolve_left (by norm_num)

theorem occupation_star (i : K) : star (F.occupation i) = F.occupation i := by
  simp [occupation]

theorem occupation_sq (i : K) : F.occupation i * F.occupation i = F.occupation i := by
  have hm : F.c i * star (F.c i) = 1 - star (F.c i) * F.c i := by
    apply eq_sub_of_add_eq
    simpa [ac] using F.mixed i i
  unfold occupation
  calc
    star (F.c i) * F.c i * (star (F.c i) * F.c i) =
        star (F.c i) * (F.c i * star (F.c i)) * F.c i := by noncomm_ring
    _ = star (F.c i) * (1 - star (F.c i) * F.c i) * F.c i := by rw [hm]
    _ = star (F.c i) * F.c i - (star (F.c i) * star (F.c i)) * (F.c i * F.c i) := by
      noncomm_ring
    _ = star (F.c i) * F.c i := by rw [F.annihilate_sq]; simp

theorem localParity_pair (i : K) :
    (-I) • (F.gamma (i, false) * F.gamma (i, true)) = F.localParity i := by
  have hm : F.c i * star (F.c i) = 1 - star (F.c i) * F.c i := by
    apply eq_sub_of_add_eq
    simpa [ac] using F.mixed i i
  have hd : star (F.c i) * star (F.c i) = 0 := by
    simpa using congrArg star (F.annihilate_sq i)
  simp only [gamma, Bool.false_eq_true, ↓reduceIte, mul_smul_comm, smul_smul]
  norm_num
  rw [show (F.c i + star (F.c i)) * (F.c i - star (F.c i)) =
      F.c i * F.c i - F.c i * star (F.c i) + star (F.c i) * F.c i -
      star (F.c i) * star (F.c i) by noncomm_ring,
    F.annihilate_sq, hd, hm]
  unfold localParity occupation
  noncomm_ring

theorem localParity_star (i : K) : star (F.localParity i) = F.localParity i := by
  simp [localParity, F.occupation_star, two_mul]

theorem localParity_sq (i : K) : F.localParity i * F.localParity i = 1 := by
  unfold localParity
  calc
    (1 - 2 * F.occupation i) * (1 - 2 * F.occupation i) =
        1 - 4 * F.occupation i + 4 * (F.occupation i * F.occupation i) := by noncomm_ring
    _ = 1 := by rw [F.occupation_sq]; noncomm_ring

/-- Ordered products require no implicit choice of a noncommutative Finset product. -/
theorem parity_product (modes : List K) :
    (modes.map (fun i => (-I) • (F.gamma (i, false) * F.gamma (i, true)))).prod =
      (modes.map F.localParity).prod := by
  simp only [F.localParity_pair]

/-- Conditional action on a supplied common occupation eigenvector. Existence
and completeness of such a basis are not asserted. -/
theorem localParity_action {V : Type*} [AddCommGroup V] [Module A V]
    (v : V) (bits : K → Bool)
    (hv : ∀ i, F.occupation i • v = if bits i then v else 0) (i : K) :
    F.localParity i • v = if bits i then -v else v := by
  simp only [localParity, sub_smul, one_smul, mul_smul, hv]
  cases bits i <;> simp [two_smul A]

theorem parity_action {V : Type*} [AddCommGroup V] [Module A V]
    (v : V) (bits : K → Bool)
    (hv : ∀ i, F.occupation i • v = if bits i then v else 0) (modes : List K) :
    (modes.map F.localParity).prod • v = ((-1 : ℤ) ^ modes.countP bits) • v := by
  induction modes with
  | nil => simp
  | cons i tail ih =>
    rw [List.map_cons, List.prod_cons, mul_smul, ih, smul_comm,
      F.localParity_action v bits hv i]
    cases h : bits i <;> simp [h, pow_succ]

end CARFamily

omit [DecidableEq K] in
theorem gamma_index_count [Fintype K] : Fintype.card (K × Bool) = 2 * Fintype.card K := by
  simp [Fintype.card_prod, Nat.mul_comm]

open Matrix

/-- One-mode CAR is instantiated, so the algebraic hypotheses are nonvacuous. -/
def oneC : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 0, 0]

def oneCAR : CARFamily (Fin 1) (Matrix (Fin 2) (Fin 2) ℂ) where
  c := fun _ => oneC
  aa := by
    intro i j
    ext p q
    fin_cases p <;> fin_cases q <;> norm_num [ac, oneC, Matrix.mul_apply, Fin.sum_univ_two]
  mixed := by
    intro i j
    have h : i = j := Subsingleton.elim _ _
    subst j
    ext p q
    fin_cases p <;> fin_cases q <;>
      norm_num [ac, oneC, Matrix.star_eq_conjTranspose, Matrix.conjTranspose,
        Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_two]

def oneRho : Matrix (Fin 2) (Fin 2) ℂ := !![1/2, 1/2; 1/2, 1/2]
def oneGram : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 1, 0]

theorem oneRho_star : star oneRho = oneRho := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [oneRho]

theorem oneRho_trace : Matrix.trace oneRho = 1 := by
  norm_num [Matrix.trace, oneRho, Fin.sum_univ_two]

theorem oneRho_gram : oneRho = (1/2 : ℂ) • (oneGram * star oneGram) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [oneRho, oneGram, Matrix.star_eq_conjTranspose, Matrix.conjTranspose,
      Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_two]

theorem oneRho_idempotent : oneRho * oneRho = oneRho := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [oneRho, Matrix.mul_apply, Fin.sum_univ_two]

theorem oneRho_posSemidef : oneRho.PosSemidef := by
  have h : oneRho * oneRhoᴴ = oneRho := by
    change oneRho * star oneRho = oneRho
    rw [oneRho_star, oneRho_idempotent]
  rw [← h]
  exact Matrix.posSemidef_self_mul_conjTranspose oneRho

theorem one_parity : oneCAR.localParity 0 = !![(1 : ℂ), 0; 0, -1] := by
  change 1 - 2 * (star oneC * oneC) = _
  rw [two_mul]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [oneC, Matrix.star_eq_conjTranspose, Matrix.conjTranspose,
      Matrix.mul_apply, Fin.sum_univ_two]

/-- A rational Hermitian trace-one Gram matrix can fail to commute with parity.
Restricting allowed states to the commuting ones is an additional postulate. -/
theorem parity_superselection_not_forced :
    oneCAR.localParity 0 * oneRho ≠ oneRho * oneCAR.localParity 0 := by
  intro h
  rw [one_parity] at h
  have he := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℂ => M 0 1) h
  norm_num [oneRho, Matrix.mul_apply, Fin.sum_univ_two] at he
end
end CampaignMajoranaCliffordParity

#print axioms CampaignMajoranaCliffordParity.CARFamily.gamma_star
#print axioms CampaignMajoranaCliffordParity.CARFamily.gamma_ac
#print axioms CampaignMajoranaCliffordParity.CARFamily.recover_c
#print axioms CampaignMajoranaCliffordParity.CARFamily.recover_star_c
#print axioms CampaignMajoranaCliffordParity.CARFamily.generated_algebra
#print axioms CampaignMajoranaCliffordParity.CARFamily.annihilate_sq
#print axioms CampaignMajoranaCliffordParity.CARFamily.occupation_star
#print axioms CampaignMajoranaCliffordParity.CARFamily.occupation_sq
#print axioms CampaignMajoranaCliffordParity.CARFamily.localParity_pair
#print axioms CampaignMajoranaCliffordParity.CARFamily.localParity_star
#print axioms CampaignMajoranaCliffordParity.CARFamily.localParity_sq
#print axioms CampaignMajoranaCliffordParity.CARFamily.parity_product
#print axioms CampaignMajoranaCliffordParity.CARFamily.localParity_action
#print axioms CampaignMajoranaCliffordParity.CARFamily.parity_action
#print axioms CampaignMajoranaCliffordParity.gamma_index_count
#print axioms CampaignMajoranaCliffordParity.oneCAR
#print axioms CampaignMajoranaCliffordParity.oneRho_star
#print axioms CampaignMajoranaCliffordParity.oneRho_trace
#print axioms CampaignMajoranaCliffordParity.oneRho_gram
#print axioms CampaignMajoranaCliffordParity.oneRho_idempotent
#print axioms CampaignMajoranaCliffordParity.oneRho_posSemidef
#print axioms CampaignMajoranaCliffordParity.one_parity
#print axioms CampaignMajoranaCliffordParity.parity_superselection_not_forced
#print axioms CampaignMajoranaCliffordParity.ac_comm
#print axioms CampaignMajoranaCliffordParity.ac_add_left
#print axioms CampaignMajoranaCliffordParity.ac_sub_left
#print axioms CampaignMajoranaCliffordParity.ac_add_right
#print axioms CampaignMajoranaCliffordParity.ac_sub_right
#print axioms CampaignMajoranaCliffordParity.ac_smul_left
#print axioms CampaignMajoranaCliffordParity.ac_smul_right
#print axioms CampaignMajoranaCliffordParity.CARFamily.dd
#print axioms CampaignMajoranaCliffordParity.CARFamily.mixed_rev
