

namespace FableHilbertWalk20260819.H052

def is_cyclotomic_subfield (m n : Nat) : Prop :=
  m ∣ n

theorem subfield_inclusion_trans {m k n : Nat} (h1 : m ∣ k) (h2 : k ∣ n) : m ∣ n :=
  Nat.dvd_trans h1 h2

theorem subfield_inclusion_refl (n : Nat) : n ∣ n :=
  Nat.dvd_refl n

theorem cyclotomic_tower_is_directed (m1 m2 : Nat) (h1 : m1 ≥ 1) (h2 : m2 ≥ 1) :
    ∃ n : Nat, n ≥ 1 ∧ m1 ∣ n ∧ m2 ∣ n :=
  ⟨m1 * m2, Nat.mul_pos h1 h2, ⟨m2, rfl⟩, ⟨m1, Nat.mul_comm m1 m2⟩⟩

structure CyclotomicDirectedSystem where
  conductors : Nat → Nat
  directed_witness : ∀ i j, ∃ k, (conductors i ∣ conductors k) ∧ (conductors j ∣ conductors k)

def identityCyclotomicSystem : CyclotomicDirectedSystem where
  conductors := id
  directed_witness := fun i j => ⟨i * j, ⟨j, rfl⟩, ⟨i, Nat.mul_comm i j⟩⟩

def targetConductors : List Nat := [1, 2, 3, 4, 5, 8, 12]

def targetLcmConductor : Nat := 120

theorem target_c1_div_120 : 1 ∣ targetLcmConductor := by decide

theorem target_c2_div_120 : 2 ∣ targetLcmConductor := by decide

theorem target_c3_div_120 : 3 ∣ targetLcmConductor := by decide

theorem target_c4_div_120 : 4 ∣ targetLcmConductor := by decide

theorem target_c5_div_120 : 5 ∣ targetLcmConductor := by decide

theorem target_c8_div_120 : 8 ∣ targetLcmConductor := by decide

theorem target_c12_div_120 : 12 ∣ targetLcmConductor := by decide

theorem all_targets_embed_in_lcm_conductor :
    ∀ c ∈ targetConductors, c ∣ targetLcmConductor := by
  decide

structure KroneckerWeberDirectedFamily where
  conductors : List Nat
  conductor_divisibility : ∀ c ∈ conductors, c ∣ targetLcmConductor

def foundationalKroneckerWeberFamily : KroneckerWeberDirectedFamily := {
  conductors := targetConductors,
  conductor_divisibility := all_targets_embed_in_lcm_conductor
}

theorem foundational_family_embeds :
    ∀ c ∈ foundationalKroneckerWeberFamily.conductors, c ∣ targetLcmConductor :=
  foundationalKroneckerWeberFamily.conductor_divisibility

structure CyclotomicAmplitude where
  re : Int
  im : Int
  denom : Nat

def conj_amp (a : CyclotomicAmplitude) : CyclotomicAmplitude :=
  { re := a.re, im := -a.im, denom := a.denom }

theorem conj_amp_involutive (a : CyclotomicAmplitude) : conj_amp (conj_amp a) = a := by
  cases a
  dsimp [conj_amp]
  rw [Int.neg_neg]

def in_real_subfield (a : CyclotomicAmplitude) : Prop :=
  a.im = 0

def born_weight_numer (a : CyclotomicAmplitude) : Int :=
  a.re * a.re + a.im * a.im

def born_weight (a : CyclotomicAmplitude) : CyclotomicAmplitude :=
  { re := born_weight_numer a,
    im := 0,
    denom := a.denom * a.denom }

theorem born_weight_in_real_subfield (a : CyclotomicAmplitude) :
    in_real_subfield (born_weight a) := by
  dsimp [in_real_subfield, born_weight]

theorem born_weight_conj_invariant (a : CyclotomicAmplitude) :
    conj_amp (born_weight a) = born_weight a := by
  rfl

#print axioms subfield_inclusion_trans
#print axioms subfield_inclusion_refl
#print axioms cyclotomic_tower_is_directed
#print axioms identityCyclotomicSystem
#print axioms foundational_family_embeds
#print axioms all_targets_embed_in_lcm_conductor
#print axioms conj_amp_involutive
#print axioms born_weight_in_real_subfield
#print axioms born_weight_conj_invariant

end FableHilbertWalk20260819.H052

private def l5aProvenance : String :=
  "Origin: lean4/H052CyclotomicTowerDirected.lean Claim: subfield_inclusion_trans AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
