import Mathlib.Combinatorics.Enumerative.Partition.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-! AuthorityEffect: None. Exact gauge-factor cancellation and pentagon transport,
bounded finite path extension, and admitted machine indices. Runtime vector,
callback, ordered diagnostic and provider correspondence remain source/native
obligations. No extracted Rust, general realizability or physical theorem. -/
namespace TFQM.CategoryReplay
open scoped BigOperators

theorem bounded_cube (r : Nat) (hr : r≤32) : r*r*r≤32768 := by
  exact Nat.le_trans (Nat.mul_le_mul (Nat.mul_le_mul hr hr) hr) (by decide)

theorem bounded_fourth (r : Nat) (hr : r≤32) : r*r*r*r≤1048576 := by
  exact Nat.le_trans (Nat.mul_le_mul (Nat.mul_le_mul (Nat.mul_le_mul hr hr) hr) hr) (by decide)

theorem admitted_index (i dimension rank : Nat) (hi : i<dimension)
    (hd : dimension≤rank) (hr : rank≤32) : i<32 := by omega

def charge (amount limit : Nat) : Bool := decide (amount≤limit)

theorem charge_exact (amount limit : Nat) : charge amount limit=true ↔ amount≤limit := by simp [charge]

theorem charge_refused (amount limit : Nat) (h : limit<amount) : charge amount limit=false := by
  simp [charge,Nat.not_le_of_lt h]

theorem extension_bound (r bound : Nat) (count edge : Fin r → Nat)
    (hc : ∀ i,count i≤bound) (he : ∀ i,edge i≤1) :
    (∑ i, count i*edge i)≤r*bound := by
  calc
    (∑ i, count i*edge i) ≤ ∑ _i : Fin r, bound := by
      exact Finset.sum_le_sum (fun i _ => by simpa using Nat.mul_le_mul (hc i) (he i))
    _ = r*bound := by simp

variable {K : Type*} [Field K]

def gaugeFactor (a b c d : K) : K := (a*b)/(c*d)

theorem gauge_nonzero (a b c d : K) (ha:a≠0) (hb:b≠0) (hc:c≠0) (hd:d≠0) :
    gaugeFactor a b c d≠0 := div_ne_zero (mul_ne_zero ha hb) (mul_ne_zero hc hd)

theorem gauge_undo (a b c d x : K) (ha:a≠0) (hb:b≠0) (hc:c≠0) (hd:d≠0) :
    gaugeFactor c d a b*(gaugeFactor a b c d*x)=x := by
  unfold gaugeFactor
  field_simp

theorem gauge_composition (a b c d e f g h : K)
    (hc:c≠0) (hd:d≠0) (hg:g≠0) (hh:h≠0) :
    gaugeFactor (a*e) (b*f) (c*g) (d*h)=gaugeFactor a b c d*gaugeFactor e f g h := by
  unfold gaugeFactor
  field_simp

-- Ten vertex weights in the actual two-term/three-term pentagon formula.
theorem pentagon_transport (u1 u2 u3 u4 u5 u6 u7 u8 u9 u10 : K)
    (h4:u4≠0) (h5:u5≠0) (h6:u6≠0) (h7:u7≠0) (h8:u8≠0) (h9:u9≠0) (h10:u10≠0) :
    gaugeFactor u2 u3 u4 u10*gaugeFactor u1 u10 u5 u6 =
    gaugeFactor u1 u2 u7 u9*gaugeFactor u9 u3 u8 u6*gaugeFactor u7 u8 u4 u5 := by
  unfold gaugeFactor
  field_simp

theorem common_factor_sum {ι : Type*} (s : Finset ι) (factor : K) (terms : ι→K) :
    (∑ i ∈ s, factor*terms i)=factor*(∑ i ∈ s, terms i) := by
  simp only [Finset.mul_sum]

-- A product of the two unit-channel F entries is preserved under a
-- unit-compatible gauge. Arbitrary raw gauges need not preserve unit laws.
theorem dimension_product_transport (a b left right x y : K)
    (ha:a≠0) (hb:b≠0) (hl:left≠0) (hr:right≠0) :
    (gaugeFactor a left b left*x)*(gaugeFactor b right a right*y)=x*y := by
  unfold gaugeFactor
  field_simp

end TFQM.CategoryReplay

#print axioms TFQM.CategoryReplay.bounded_cube
#print axioms TFQM.CategoryReplay.bounded_fourth
#print axioms TFQM.CategoryReplay.admitted_index
#print axioms TFQM.CategoryReplay.charge_exact
#print axioms TFQM.CategoryReplay.charge_refused
#print axioms TFQM.CategoryReplay.extension_bound
#print axioms TFQM.CategoryReplay.gauge_nonzero
#print axioms TFQM.CategoryReplay.gauge_undo
#print axioms TFQM.CategoryReplay.gauge_composition
#print axioms TFQM.CategoryReplay.pentagon_transport
#print axioms TFQM.CategoryReplay.common_factor_sum
#print axioms TFQM.CategoryReplay.dimension_product_transport
