import WitnessedDifference.PresentationDuality
import Mathlib.Topology.Algebra.Group.Quotient
import Mathlib.Topology.Algebra.ContinuousMonoidHom

/-!
# Protected subgroups and continuous circle characters

The quotient carries its quotient topology. Character separation is an explicit
mathematical hypothesis, not a consequence of completeness. The source theorem
uses the stated PC/extension correspondence; no LCA theorem is asserted here.
-/

noncomputable section

namespace WitnessedDifference.ProtectedCharacterQuotient

open Topology
open ContinuousMonoidHom
open PresentationCompletion

abbrev Character (H : Type*) [AddGroup H] [TopologicalSpace H] :=
  ContinuousAddMonoidHom H (Additive Circle)

variable {H : Type*} [AddCommGroup H] [TopologicalSpace H] [IsTopologicalAddGroup H]

def doubleAnnihilator (N : AddSubgroup H) : AddSubgroup H where
  carrier := {x | ∀ χ : Character H, N ≤ χ.toAddMonoidHom.ker → χ x = 0}
  zero_mem' := by intro χ _; exact map_zero χ
  add_mem' := by
    intro x y hx hy χ hχ
    simp only [map_add, hx χ hχ, hy χ hχ, add_zero]
  neg_mem' := by
    intro x hx χ hχ
    simp only [map_neg, hx χ hχ, neg_zero]

def CharactersSeparate (H : Type*) [AddGroup H] [TopologicalSpace H] : Prop :=
  ∀ x : H, (∀ χ : Character H, χ x = 0) → x = 0

omit [IsTopologicalAddGroup H] in
theorem subgroup_le_doubleAnnihilator (N : AddSubgroup H) :
    N ≤ doubleAnnihilator N := by
  intro x hx χ hχ
  exact hχ hx

theorem character_vanishes_closure_iff (N : AddSubgroup H) (χ : Character H) :
    N.topologicalClosure ≤ χ.toAddMonoidHom.ker ↔ N ≤ χ.toAddMonoidHom.ker := by
  constructor
  · exact fun h => N.le_topologicalClosure.trans h
  · intro h
    exact N.topologicalClosure_minimal h (isClosed_eq χ.continuous continuous_const)

def quotientCharacter (N : AddSubgroup H) (χ : Character H)
    (hχ : N ≤ χ.toAddMonoidHom.ker) : Character (H ⧸ N) where
  toAddMonoidHom := QuotientAddGroup.lift N χ.toAddMonoidHom hχ
  continuous_toFun := (QuotientAddGroup.isQuotientMap_mk N).continuous_iff.mpr
    χ.continuous

omit [IsTopologicalAddGroup H] in
@[simp] theorem quotientCharacter_mk (N : AddSubgroup H) (χ : Character H)
    (hχ : N ≤ χ.toAddMonoidHom.ker) (x : H) :
    quotientCharacter N χ hχ (QuotientAddGroup.mk x) = χ x := rfl

def pullbackCharacter (N : AddSubgroup H) (ψ : Character (H ⧸ N)) : Character H where
  toAddMonoidHom := ψ.toAddMonoidHom.comp (QuotientAddGroup.mk' N)
  continuous_toFun := ψ.continuous.comp QuotientAddGroup.continuous_mk

omit [IsTopologicalAddGroup H] in
theorem pullbackCharacter_vanishes (N : AddSubgroup H) (ψ : Character (H ⧸ N)) :
    N ≤ (pullbackCharacter N ψ).toAddMonoidHom.ker := by
  intro x hx
  change ψ (QuotientAddGroup.mk x) = 0
  rw [(QuotientAddGroup.eq_zero_iff x).mpr hx, map_zero]

omit [IsTopologicalAddGroup H] in
theorem quotientCharacter_unique (N : AddSubgroup H) (χ : Character H)
    (hχ : N ≤ χ.toAddMonoidHom.ker) (ψ : Character (H ⧸ N))
    (hψ : ∀ x : H, ψ (QuotientAddGroup.mk x) = χ x) :
    ψ = quotientCharacter N χ hχ := by
  apply ContinuousAddMonoidHom.ext
  intro x
  obtain ⟨x, rfl⟩ := QuotientAddGroup.mk_surjective x
  exact hψ x

omit [IsTopologicalAddGroup H] in
theorem mem_doubleAnnihilator_iff_quotient (N : AddSubgroup H) (x : H) :
    x ∈ doubleAnnihilator N ↔
      ∀ ψ : Character (H ⧸ N), ψ (QuotientAddGroup.mk x) = 0 := by
  constructor
  · intro hx ψ
    exact hx (pullbackCharacter N ψ) (pullbackCharacter_vanishes N ψ)
  · intro hx χ hχ
    exact hx (quotientCharacter N χ hχ)

omit [IsTopologicalAddGroup H] in
theorem doubleAnnihilator_eq_iff_quotient_separates (N : AddSubgroup H) :
    doubleAnnihilator N = N ↔ CharactersSeparate (H ⧸ N) := by
  constructor
  · intro h x hx
    obtain ⟨y, rfl⟩ := QuotientAddGroup.mk_surjective x
    apply (QuotientAddGroup.eq_zero_iff y).mpr
    rw [← h]
    exact (mem_doubleAnnihilator_iff_quotient N y).mpr hx
  · intro h
    apply le_antisymm _ (subgroup_le_doubleAnnihilator N)
    intro x hx
    apply (QuotientAddGroup.eq_zero_iff x).mp
    exact h _ ((mem_doubleAnnihilator_iff_quotient N x).mp hx)

section Source

variable {G : Type*} [AddCommGroup G]

def restrictedDoubleAnnihilator (p : G →+ H) (A : AddSubgroup G) : AddSubgroup G :=
  (doubleAnnihilator (A.map p).topologicalClosure).comap p

theorem protected_closure_le (p : G →+ H) (A : AddSubgroup G) :
    (A.map p).topologicalClosure.comap p ≤ restrictedDoubleAnnihilator p A := by
  exact AddSubgroup.comap_mono (subgroup_le_doubleAnnihilator _)

theorem source_exact_iff_image_separated (p : G →+ H) (A : AddSubgroup G) :
    restrictedDoubleAnnihilator p A = (A.map p).topologicalClosure.comap p ↔
      ∀ g : G,
        (∀ ψ : Character (H ⧸ (A.map p).topologicalClosure),
          ψ (QuotientAddGroup.mk (p g)) = 0) →
        p g ∈ (A.map p).topologicalClosure := by
  constructor
  · intro h g hg
    have hmem : g ∈ restrictedDoubleAnnihilator p A :=
      (mem_doubleAnnihilator_iff_quotient _ _).mpr hg
    rwa [h] at hmem
  · intro h
    apply le_antisymm _ (protected_closure_le p A)
    intro g hg
    exact h g ((mem_doubleAnnihilator_iff_quotient _ _).mp hg)

theorem source_exact_of_quotient_separates (p : G →+ H) (A : AddSubgroup G)
    (h : CharactersSeparate (H ⧸ (A.map p).topologicalClosure)) :
    restrictedDoubleAnnihilator p A = (A.map p).topologicalClosure.comap p := by
  unfold restrictedDoubleAnnihilator
  rw [(doubleAnnihilator_eq_iff_quotient_separates _).mpr h]

theorem source_recovery_iff (p : G →+ H) (A : AddSubgroup G)
    (h : CharactersSeparate (H ⧸ (A.map p).topologicalClosure)) :
    restrictedDoubleAnnihilator p A = A ↔ (A.map p).topologicalClosure.comap p = A := by
  rw [source_exact_of_quotient_separates p A h]

theorem protected_closure_recovery_iff (p : G →+ H) (A : AddSubgroup G) :
    (A.map p).topologicalClosure.comap p = A ↔
      p.ker ≤ A ∧ ∀ g : G, p g ∈ (A.map p).topologicalClosure → p g ∈ A.map p := by
  constructor
  · intro h
    constructor
    · intro g hg
      rw [← h]
      change p g ∈ (A.map p).topologicalClosure
      change p g = 0 at hg
      rw [hg]
      exact (A.map p).topologicalClosure.zero_mem
    · intro g hg
      have ha : g ∈ A := by rw [← h]; exact hg
      exact AddSubgroup.mem_map.mpr ⟨g, ha, rfl⟩
  · rintro ⟨hker, hclosed⟩
    apply le_antisymm
    · intro g hg
      obtain ⟨a, ha, hag⟩ := hclosed g hg
      have hk : g - a ∈ p.ker := by
        change p (g - a) = 0
        rw [map_sub, hag, sub_self]
      simpa using A.add_mem (hker hk) ha
    · intro a ha
      exact (A.map p).le_topologicalClosure (AddSubgroup.mem_map.mpr ⟨a, ha, rfl⟩)

end Source
end WitnessedDifference.ProtectedCharacterQuotient

namespace WitnessedDifference.ProtectedCharacterQuotient

open PresentationCompletion

variable {G H : Type*} [AddCommGroup G] [AddCommGroup H]
variable [MetricSpace H] [IsTopologicalAddGroup H]

def pcDoubleAnnihilator (p : G →+ H) (A : AddSubgroup G) : Set G :=
  {g | ∀ χ : G →+ Additive Circle,
    RelativeControl p χ → A ≤ χ.ker → χ g = 0}

theorem pcDoubleAnnihilator_eq (p : G →+ H) (A : AddSubgroup G)
    (extension : ∀ χ : G →+ Additive Circle,
      RelativeControl p χ ↔ ∃ ψ : Character H, ∀ g, ψ (p g) = χ g) :
    pcDoubleAnnihilator p A = (restrictedDoubleAnnihilator p A : Set G) := by
  ext g
  constructor
  · intro hg ψ hψ
    let χ := ψ.toAddMonoidHom.comp p
    have hc : RelativeControl p χ := (extension χ).mpr ⟨ψ, fun _ => rfl⟩
    apply hg χ hc
    intro a ha
    exact hψ ((A.map p).le_topologicalClosure (AddSubgroup.mem_map.mpr ⟨a, ha, rfl⟩))
  · intro hg χ hc hA
    obtain ⟨ψ, hψ⟩ := (extension χ).mp hc
    rw [← hψ g]
    apply hg ψ
    apply (character_vanishes_closure_iff (A.map p) ψ).mpr
    rintro _ ⟨a, ha, rfl⟩
    change ψ (p a) = 0
    rw [hψ a]
    exact hA ha

end WitnessedDifference.ProtectedCharacterQuotient
