







import HWKernel
import HilbertWalkPhaseBlindPresentation

namespace HilbertWalk.BornPairingBoundary

open HilbertWalk.HWKernel
open HilbertWalk.PhaseBlindPresentation

def pair {Q : Type} (E : Enum Q) (w e : Q → Int) : Int :=
  rsum intPack (E.elems.map (fun q => w q * e q))

def indicator (b : Bool) : Bool → Int :=
  fun q => if q == b then 1 else 0

theorem pairing_exists :
    pair enumBool (phaseBlind psi1) (indicator false) = 1 ∧
      pair enumBool (phaseBlind psi1) (fun _ => 1) = 2 := by
  refine ⟨by decide, by decide⟩

#print axioms pairing_exists


def quartic {Q : Type} (v : Q → GaussInt) : Q → Int :=
  fun q => phaseBlind v q * phaseBlind v q

theorem quartic_nonneg {Q : Type} (v : Q → GaussInt) (q : Q) :
    0 ≤ quartic v q :=
  HilbertWalk.InnerProductAdmission.int_sq_nonneg (phaseBlind v q)

def psi21 : Bool → GaussInt :=
  fun q => if q then GaussInt.gone else ⟨2, 0⟩

theorem quartic_rival :
    (∀ q : Bool, 0 ≤ quartic psi21 q) ∧
      totalWeight enumBool psi21 = 5 ∧
      rsum intPack (enumBool.elems.map (quartic psi21)) = 17 ∧
      ¬(∀ q : Bool, phaseBlind psi21 q = quartic psi21 q) := by
  refine ⟨fun q => quartic_nonneg psi21 q, by decide, by decide, by decide⟩

#print axioms quartic_rival

theorem pair_linear_effect {Q : Type} (E : Enum Q)
    (w e1 e2 : Q → Int) :
    pair E w (fun q => e1 q + e2 q) = pair E w e1 + pair E w e2 := by
  unfold pair
  have h : E.elems.map (fun q => w q * (e1 q + e2 q)) =
      E.elems.map (fun q =>
        intPack.add (w q * e1 q) (w q * e2 q)) :=
    map_congr_mem (fun q _ => Int.mul_add (w q) (e1 q) (e2 q))
  rw [h]
  exact rsum_map_add intPack (fun q => w q * e1 q)
    (fun q => w q * e2 q) E.elems

theorem pair_linear_state {Q : Type} (E : Enum Q)
    (w1 w2 e : Q → Int) :
    pair E (fun q => w1 q + w2 q) e = pair E w1 e + pair E w2 e := by
  unfold pair
  have h : E.elems.map (fun q => (w1 q + w2 q) * e q) =
      E.elems.map (fun q =>
        intPack.add (w1 q * e q) (w2 q * e q)) :=
    map_congr_mem (fun q _ => Int.add_mul (w1 q) (w2 q) (e q))
  rw [h]
  exact rsum_map_add intPack (fun q => w1 q * e q)
    (fun q => w2 q * e q) E.elems

#print axioms pair_linear_effect
#print axioms pair_linear_state

theorem weights_pinned :
    (∀ q : Bool, phaseBlind psi21 q = if q then 1 else 4) ∧
      (∀ q : Bool, quartic psi21 q = if q then 1 else 16) := by
  refine ⟨by decide, by decide⟩

theorem quartic_not_proportional :
    ¬ ∃ a b : Int, a ≠ 0 ∧
      (∀ q : Bool, a * quartic psi21 q = b * phaseBlind psi21 q) := by
  intro h
  rcases h with ⟨a, b, ha, hab⟩
  have h1 : a * 1 = b * 1 := hab true
  have h2 : a * 16 = b * 4 := hab false
  omega

#print axioms quartic_not_proportional

structure GleasonPack where
  dimension_ge_three : Bool
  noncontextuality : Bool
  sigma_additivity : Bool
  continuity_of_measure : Bool

def UniquenessDischarged (G : GleasonPack) : Bool :=
  G.dimension_ge_three && G.noncontextuality &&
    G.sigma_additivity && G.continuity_of_measure

def hostSupplies : GleasonPack where
  dimension_ge_three := false
  noncontextuality := false
  sigma_additivity := false
  continuity_of_measure := false

theorem uniqueness_not_discharged :
    UniquenessDischarged hostSupplies = false :=
  rfl

#print axioms uniqueness_not_discharged

structure BornNonUniquenessPack where
  common_domain : Bool
  shared_normalization_contract : Bool
  two_effect_rules_differ : Bool

def bornNonUniquenessHost : BornNonUniquenessPack where
  common_domain := true
  shared_normalization_contract := false
  two_effect_rules_differ := false

def BornNonUniquenessDischarged (P : BornNonUniquenessPack) : Bool :=
  P.common_domain && P.shared_normalization_contract &&
    P.two_effect_rules_differ

theorem born_nonuniqueness_open :
    BornNonUniquenessDischarged bornNonUniquenessHost = false :=
  rfl

#print axioms born_nonuniqueness_open

theorem born_pairing_boundary :
    (pair enumBool (phaseBlind psi1) (indicator false) = 1) ∧
      ¬(∀ q : Bool, phaseBlind psi21 q = quartic psi21 q) ∧
      UniquenessDischarged hostSupplies = false ∧
      BornNonUniquenessDischarged bornNonUniquenessHost = false :=
  ⟨pairing_exists.1, quartic_rival.2.2.2, uniqueness_not_discharged,
    born_nonuniqueness_open⟩

#print axioms born_pairing_boundary

end HilbertWalk.BornPairingBoundary

private def l5aProvenance : String :=
  "Origin: lean4/BornPairingBoundary.lean Claim: pairing_exists AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
