import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-! AuthorityEffect: None. Actual alternating form, projective direction
partition over fields, and disjoint finite-bundle counting. Rust representatives,
prime admission, checked bounds and iteration are separately reviewed. Operator
bundles are not eigenbases or a completeness theorem in composite dimensions. -/
namespace TFQM.WeylBundles
open scoped BigOperators

def form {R : Type*} [CommRing R] (u v : R × R) : R := u.1*v.2-u.2*v.1

theorem alternating {R : Type*} [CommRing R] (u : R × R) : form u u=0 := by
  simp [form, mul_comm]
theorem antisymmetric {R : Type*} [CommRing R] (u v : R × R) : form u v= -form v u := by
  simp only [form]; ring
theorem additive {R : Type*} [CommRing R] (u v w : R × R) : form (u+v) w=form u w+form v w := by
  simp only [form, Prod.fst_add, Prod.snd_add]; ring

def onRay {K : Type*} [Field K] (direction : Option K) (point : K × K) : Prop :=
  match direction with
  | none => point.1=0
  | some m => point.2=m*point.1

theorem ray_isotropic {K : Type*} [Field K] (d : Option K) (u v : K × K)
    (hu : onRay d u) (hv : onRay d v) : form u v=0 := by
  cases d with
  | none => simp only [onRay] at hu hv; simp [form, hu, hv]
  | some m => simp only [onRay] at hu hv; simp only [form, hu, hv]; ring

theorem unique_direction {K : Type*} [Field K] (u : K × K) (hne : u ≠ (0,0)) :
    ∃! d : Option K, onRay d u := by
  by_cases hx : u.1=0
  · have hy : u.2≠0 := by
      intro h
      exact hne (Prod.ext hx h)
    refine ⟨none, hx, ?_⟩
    intro d hd
    cases d with
    | none => rfl
    | some m => simp [onRay, hx] at hd; exact (hy hd).elim
  · refine ⟨some (u.2/u.1), ?_, ?_⟩
    · exact (div_mul_cancel₀ u.2 hx).symm
    · intro d hd
      cases d with
      | none => exact (hx hd).elim
      | some m =>
        have hm : m=u.2/u.1 := (eq_div_iff hx).mpr hd.symm
        exact congrArg some hm

theorem distinct_directions_disjoint {K : Type*} [Field K] (d e : Option K) (hde : d≠e)
    (u : K × K) (hne : u≠(0,0)) (hd : onRay d u) : ¬onRay e u := by
  intro he
  obtain ⟨w, _, hw⟩ := unique_direction u hne
  exact hde ((hw d hd).trans (hw e he).symm)

theorem direction_count {K : Type*} [Fintype K] : Fintype.card (Option K)=Fintype.card K+1 := by
  simp

theorem bundle_mass (d k : Nat) (bundles : Fin k → Finset (Fin d × Fin d))
    (sizes : ∀ i, (bundles i).card=d-1)
    (disjoint : Pairwise fun i j => Disjoint (bundles i) (bundles j)) :
    (Finset.univ.biUnion bundles).card=k*(d-1) := by
  classical
  rw [Finset.card_biUnion (by
    intro i _ j _ hij
    exact disjoint hij)]
  simp [sizes]

theorem bundle_mass_bound (d k : Nat) (bundles : Fin k → Finset (Fin d × Fin d))
    (zero : Fin d × Fin d) (excluded : ∀ i, zero ∉ bundles i)
    (sizes : ∀ i, (bundles i).card=d-1)
    (disjoint : Pairwise fun i j => Disjoint (bundles i) (bundles j)) : k*(d-1)≤d*d-1 := by
  classical
  have subset : Finset.univ.biUnion bundles ⊆ Finset.univ.erase zero := by
    intro point hp
    obtain ⟨i, _, hi⟩ := Finset.mem_biUnion.mp hp
    apply Finset.mem_erase.mpr
    refine ⟨?_, Finset.mem_univ _⟩
    intro h
    exact excluded i (h ▸ hi)
  have h := Finset.card_le_card subset
  rw [bundle_mass d k bundles sizes disjoint] at h
  simpa using h

theorem basis_count_bound (d k : Nat) (hd : 2≤d) (hm : k*(d-1)≤d*d-1) : k≤d+1 := by
  have hsub : d-1+1=d := by omega
  have hsquare : d*d-1+1=d*d := by nlinarith
  by_contra h
  have hk : d+2≤k := by omega
  have hp : (d+2)*(d-1)≤k*(d-1) := Nat.mul_le_mul_right (d-1) hk
  nlinarith

theorem bounded_add (d a b : Nat) (hd : d≤256) (ha : a<d) (hb : b<d) : a+b≤510 := by omega

theorem bounded_product (d a b : Nat) (hd : d≤256) (ha : a<d) (hb : b<d) : a*b≤65025 := by
  have h1 : a≤255 := by omega
  have h2 : b≤255 := by omega
  exact Nat.le_trans (Nat.mul_le_mul h1 h2) (by decide)

theorem subtract_representative_safe (d a b : Nat) (hb : b<d) : b≤d+a := by omega

theorem singleton_admission {K : Type*} (admitted : K → Prop) (p : K)
    (h : ∀ x ∈ [p], admitted x) : admitted p := h p (by simp)

theorem bounded_plus_one (d maximum : Nat) : d+1≤maximum ↔ d<maximum := by omega

#print axioms alternating
#print axioms antisymmetric
#print axioms additive
#print axioms ray_isotropic
#print axioms unique_direction
#print axioms distinct_directions_disjoint
#print axioms direction_count
#print axioms bundle_mass
#print axioms bundle_mass_bound
#print axioms basis_count_bound
#print axioms bounded_add
#print axioms bounded_product
#print axioms subtract_representative_safe
#print axioms singleton_admission
#print axioms bounded_plus_one
end TFQM.WeylBundles
