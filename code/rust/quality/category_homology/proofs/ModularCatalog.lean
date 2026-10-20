import Mathlib.GroupTheory.OrderOfElement
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.Combinatorics.Enumerative.Partition.Basic
import Mathlib.Tactic.Ring

/-! AuthorityEffect: None. Root phase/order reduction, finite bilinear phases,
actual diagonal matrix multiplication, checked division and exact aggregation.
No categorical realization, physical entropy theorem or Rust extraction. -/
namespace TFQM.ModularCatalog

theorem signed_phase_period {G : Type*} [Group G] (z : G) (b : Int) :
    z^(b % (orderOf z : Int))=z^b := zpow_mod_orderOf z b

theorem reduced_phase_order {G : Type*} [Group G] (z : G) (r : Nat) (h : IsOfFinOrder z) :
    orderOf (z^r)=orderOf z/Nat.gcd r (orderOf z) := by
  simpa [Nat.gcd_comm] using (IsOfFinOrder.orderOf_pow (x:=z) (n:=r) h)

theorem reduced_denominator_divides (g r : Nat) : g/Nat.gcd r g ∣ g :=
  Nat.div_dvd_of_dvd (Nat.gcd_dvd_right r g)

theorem lcm_stays_bounded (a d bound : Nat) (ha : a∣bound) (hd : d∣bound) (hb : 0<bound) :
    Nat.lcm a d ≤ bound := Nat.le_of_dvd hb (Nat.lcm_dvd ha hd)

theorem integer_phase_sum_bound (terms : List Nat) (hl : terms.length≤25)
    (ht : ∀ x∈terms, x≤32767) : terms.sum≤819175 := by
  have bounded : ∀ xs : List Nat, (∀ x∈xs, x≤32767) → xs.sum≤xs.length*32767 := by
    intro xs
    induction xs with
    | nil => intro hx; simp
    | cons a rest ih =>
      intro hx
      have ha := hx a (by simp)
      have hr := ih (fun x hxmem => hx x (by simp [hxmem]))
      simp only [List.sum_cons,List.length_cons]
      omega
  have h := bounded terms ht
  omega

def phase {r L : Nat} (weights : Fin r → Fin r → ZMod L)
    (x y : Fin r → ZMod L) : ZMod L := ∑ i, ∑ j, weights i j*x i*y j

theorem phase_add_left {r L : Nat} (w : Fin r → Fin r → ZMod L) (x x' y : Fin r → ZMod L) :
    phase w (x+x') y=phase w x y+phase w x' y := by
  simp [phase,mul_add,add_mul,Finset.sum_add_distrib]

theorem phase_add_right {r L : Nat} (w : Fin r → Fin r → ZMod L) (x y y' : Fin r → ZMod L) :
    phase w x (y+y')=phase w x y+phase w x y' := by
  simp [phase,mul_add,Finset.sum_add_distrib]

theorem phase_sub_left {r L : Nat} (w : Fin r → Fin r → ZMod L) (x x' y : Fin r → ZMod L) :
    phase w (x-x') y=phase w x y-phase w x' y := by
  simp [phase,mul_sub,sub_mul,Finset.sum_sub_distrib]

theorem phase_sub_right {r L : Nat} (w : Fin r → Fin r → ZMod L) (x y y' : Fin r → ZMod L) :
    phase w x (y-y')=phase w x y-phase w x y' := by
  simp [phase,mul_sub,Finset.sum_sub_distrib]

theorem quadratic_balancing {r L : Nat} (w : Fin r → Fin r → ZMod L) (x y : Fin r → ZMod L) :
    phase w (x-y) (x-y)-phase w x x-phase w y y = -(phase w x y+phase w y x) := by
  rw [phase_sub_left,phase_sub_right,phase_sub_right]
  ring

variable {K : Type*} [Field K]

section Division
variable [DecidableEq K]

def checkedDivide (a b : K) : Option K := if b=0 then none else some (a/b)

theorem zero_divisor_refused (a : K) : checkedDivide a 0=none := by simp [checkedDivide]
theorem admitted_division (a b : K) (hb : b≠0) : checkedDivide a b=some (a/b) := by simp [checkedDivide,hb]

end Division

theorem cached_balancing (total ta tb : K) : total/(ta*tb)=total*ta⁻¹*tb⁻¹ := by
  simp only [div_eq_mul_inv,mul_inv_rev]
  ring

theorem indicator_factorization (db dc tb tc : K) :
    (db*tb^2)*(dc/tc^2)=db*dc*(tb/tc)^2 := by
  simp only [div_eq_mul_inv]
  ring

theorem grouped_genus_sum (groups : List (K×Nat)) (square : K) (exponent : Int) :
    (groups.flatMap (fun g => List.replicate g.2 ((square/g.1)^exponent))).sum =
    (groups.map (fun g => (g.2:K)*((square/g.1)^exponent))).sum := by
  induction groups with
  | nil => simp
  | cons group rest ih => simp [ih,nsmul_eq_mul]

theorem equal_square_ratio (a b square : K) (h : a*a=b*b) : square/(a*a)=square/(b*b) := by rw [h]

theorem phase_angle_bounds (n k scale : Nat) (hn : 0<n) (hk : k<n) (hs : 0<scale) :
    0≤((scale*k:Nat):Rat)/(n:Rat) ∧ ((scale*k:Nat):Rat)/(n:Rat)<(scale:Rat) := by
  constructor
  · exact div_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _)
  · apply (div_lt_iff₀ (Nat.cast_pos.mpr hn)).2
    push_cast
    exact mul_lt_mul_of_pos_left (Nat.cast_lt.mpr hk) (Nat.cast_pos.mpr hs)

theorem genus_exponent_fits (genus : Int) (hg : 0≤genus ∧ genus≤4294967295) :
    -1≤genus-1 ∧ genus-1<9223372036854775807 := by omega

theorem right_diagonal_entry {I : Type*} [Fintype I] [DecidableEq I]
    (s : Matrix I I K) (twists : I → K) (a b : I) :
    (s*Matrix.diagonal twists) a b=s a b*twists b := by
  simp [Matrix.mul_apply,Matrix.diagonal,mul_ite]

end TFQM.ModularCatalog

#print axioms TFQM.ModularCatalog.signed_phase_period
#print axioms TFQM.ModularCatalog.reduced_phase_order
#print axioms TFQM.ModularCatalog.reduced_denominator_divides
#print axioms TFQM.ModularCatalog.lcm_stays_bounded
#print axioms TFQM.ModularCatalog.integer_phase_sum_bound
#print axioms TFQM.ModularCatalog.phase_add_left
#print axioms TFQM.ModularCatalog.phase_add_right
#print axioms TFQM.ModularCatalog.phase_sub_left
#print axioms TFQM.ModularCatalog.phase_sub_right
#print axioms TFQM.ModularCatalog.quadratic_balancing
#print axioms TFQM.ModularCatalog.zero_divisor_refused
#print axioms TFQM.ModularCatalog.admitted_division
#print axioms TFQM.ModularCatalog.cached_balancing
#print axioms TFQM.ModularCatalog.indicator_factorization
#print axioms TFQM.ModularCatalog.grouped_genus_sum
#print axioms TFQM.ModularCatalog.equal_square_ratio
#print axioms TFQM.ModularCatalog.phase_angle_bounds
#print axioms TFQM.ModularCatalog.genus_exponent_fits
#print axioms TFQM.ModularCatalog.right_diagonal_entry
