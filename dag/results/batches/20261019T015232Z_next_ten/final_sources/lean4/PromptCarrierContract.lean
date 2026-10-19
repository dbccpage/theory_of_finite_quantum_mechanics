import H052CyclotomicTowerDirected
import Mathlib.Algebra.Star.Basic

/- Declared field/tower inputs versus actual arithmetic and star-ring identities.
   The colimit and Kronecker-Weber theorem are not constructed in this module.
   Origin: FQ-CARRIER-CONTRACT-V2. AuthorityEffect: None. -/
namespace QuantumMechanics.PromptCarrierContract

theorem positive_label_diagram_is_directed (m n : Nat) (hm : 1 ≤ m) (hn : 1 ≤ n) :
    ∃ k : Nat, 1 ≤ k ∧ m ∣ k ∧ n ∣ k :=
  FableHilbertWalk20260819.H052.cyclotomic_tower_is_directed m n hm hn

theorem declared_distinct_label_lcm :
    ([1,2,3,4,5,8,12] : List Nat).foldl Nat.lcm 1 = 120 ∧
    ∀ c ∈ ([1,2,3,4,5,8,12] : List Nat), c ∣ 120 := by decide

theorem raw_label_divisibility_asymmetry :
    ¬ (2 ∣ (1 : Nat)) ∧ (1 ∣ (2 : Nat)) := by decide

theorem norm_is_conjugation_fixed {K : Type} [CommRing K] [StarRing K] (z : K) :
    star (z * star z) = z * star z := by
  simp only [star_mul, star_star]

theorem norm_transport_requires_a_star_compatible_hom
    {K L : Type} [CommRing K] [StarRing K] [CommRing L] [StarRing L]
    (f : K →+* L) (commutes : ∀ z, f (star z) = star (f z)) (z : K) :
    f (z * star z) = f z * star (f z) := by
  rw [f.map_mul, commutes]

end QuantumMechanics.PromptCarrierContract
#print axioms QuantumMechanics.PromptCarrierContract.positive_label_diagram_is_directed
#print axioms QuantumMechanics.PromptCarrierContract.declared_distinct_label_lcm
#print axioms QuantumMechanics.PromptCarrierContract.raw_label_divisibility_asymmetry
#print axioms QuantumMechanics.PromptCarrierContract.norm_is_conjugation_fixed
#print axioms QuantumMechanics.PromptCarrierContract.norm_transport_requires_a_star_compatible_hom
