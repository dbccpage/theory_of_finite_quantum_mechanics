import Mathlib.GroupTheory.OrderOfElement
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Omega

/-! AuthorityEffect: None. Bounded SU(2) index arithmetic, exact quantum-number
recurrence and signed root-table correspondence. No full q-6j/pentagon theorem,
Rust extraction, general level theorem or physical realization is asserted. -/
namespace TFQM.SU2Racah

theorem level_bounds (k : Nat) (hk : 1≤k ∧ k≤6) :
    6≤2*(k+2) ∧ 2*(k+2)≤16 ∧ 24≤8*(k+2) ∧ 8*(k+2)≤64 ∧ k+2≤8 := by omega

theorem triangle_indices (k a b c : Nat)
    (ha : a≤b+c) (hb : b≤a+c) (hc : c≤a+b) (ht : a+b+c≤2*k) :
    a≤(a+b+c)/2 ∧ b≤(a+b+c)/2 ∧ c≤(a+b+c)/2 ∧ (a+b+c)/2+1≤k+1 := by omega

theorem lower_indices (k a b c d e f : Nat)
    (h0 : a+b+e≤2*k) (h1 : e+c+d≤2*k)
    (h2 : b+c+f≤2*k) (h3 : a+f+d≤2*k) :
    (a+b+e)/2≤k ∧ (e+c+d)/2≤k ∧ (b+c+f)/2≤k ∧ (a+f+d)/2≤k := by omega

theorem upper_indices (k a b c d e f z : Nat)
    (hc : c≤k) (hd : d≤k) (hf : f≤k) (hb : b≤k)
    (h0 : (a+b+e)/2≤z) (h1 : (e+c+d)/2≤z) (hz : z≤k) :
    (a+b+c+d)/2-z≤k ∧ (a+c+e+f)/2-z≤k ∧ (b+d+e+f)/2-z≤k ∧ z+1≤k+1 := by omega

theorem casimir_bound (n : Nat) (hn : n≤6) : n*(n+2)≤48 := by
  calc n*(n+2) ≤ 6*(6+2) := Nat.mul_le_mul hn (Nat.add_le_add_right hn 2)
       _ = 48 := rfl

theorem braiding_exponent_bound (a b c : Int)
    (ha : 0≤a ∧ a≤48) (hb : 0≤b ∧ b≤48) (hc : 0≤c ∧ c≤48) :
    -96≤c-a-b ∧ c-a-b≤48 := by omega

theorem braiding_parity (a b c : Nat) (h : c≤a+b) (hp : (a+b+c)%2=0) :
    (a+b-c)/2%2=0 ↔ (a+b+c)/2%2=c%2 := by omega

def phasePower {G : Type*} [Monoid G] (z : G) : Nat → G
  | 0 => 1
  | n+1 => phasePower z n*z

theorem phase_cache_pow {G : Type*} [Monoid G] (z : G) (n : Nat) :
    phasePower z n=z^n := by
  induction n with
  | zero => simp [phasePower]
  | succ n ih => simp [phasePower,ih,pow_succ]

theorem phase_signed_period {G : Type*} [Group G] (z : G) (e : Int) :
    z^(e%(orderOf z : Int))=z^e := zpow_mod_orderOf z e

variable {K : Type*} [Field K]

def quantumNum (q t : K) (n : Nat) : K := (q^n-t^n)/(q-t)

theorem quantum_zero (q t : K) : quantumNum q t 0=0 := by simp [quantumNum]

theorem quantum_one (q t : K) (h : q-t≠0) : quantumNum q t 1=1 := by simp [quantumNum,h]

theorem quantum_recurrence (q t : K) (h : q*t=1) (n : Nat) :
    quantumNum q t (n+2)=(q+t)*quantumNum q t (n+1)-quantumNum q t n := by
  simp only [quantumNum,pow_succ,div_eq_mul_inv]
  linear_combination -((q^n-t^n)*(q-t)⁻¹)*h

theorem quantum_two (q t : K) (h : q-t≠0) (hi : q*t=1) :
    quantumNum q t 2=q+t := by
  simpa [quantum_zero,quantum_one q t h] using quantum_recurrence q t hi 0

end TFQM.SU2Racah

#print axioms TFQM.SU2Racah.level_bounds
#print axioms TFQM.SU2Racah.triangle_indices
#print axioms TFQM.SU2Racah.lower_indices
#print axioms TFQM.SU2Racah.upper_indices
#print axioms TFQM.SU2Racah.casimir_bound
#print axioms TFQM.SU2Racah.braiding_exponent_bound
#print axioms TFQM.SU2Racah.braiding_parity
#print axioms TFQM.SU2Racah.phase_cache_pow
#print axioms TFQM.SU2Racah.phase_signed_period
#print axioms TFQM.SU2Racah.quantum_zero
#print axioms TFQM.SU2Racah.quantum_one
#print axioms TFQM.SU2Racah.quantum_recurrence
#print axioms TFQM.SU2Racah.quantum_two
