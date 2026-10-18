/-
  H013 -- Born state-effect pairing boundary. AuthorityEffect:
  None. Candidate only. Not PROVEN. Kind: IMPORT BOUNDARY.

  Claim identifier: HW-H013
  Source-paper contact: QM_020 Theorem 4 (Born redundancy over the
  lift), QM_204 and QM_210 (audited as proposals). Work order hard
  obligation 9.

  Target proposition (corrected 2026-08-19, review round 3)
    A bilinear state-effect pairing EXISTS on the finite host
    (bilinearity proved in both slots). Obligation 9 asks to
    IDENTIFY the Born-uniqueness hypotheses and either bind each to
    a local theorem or MARK IT IMPORTED: done via GleasonPack
    (dimension >= 3, noncontextuality, sigma-additivity,
    continuity), all marked imported/absent from this host.

    What is NOT proved (was overstated before): a same-contract
    Born NON-UNIQUENESS. The quartic rival is positive and
    non-proportional to the quadratic readout, but it normalizes to
    a DIFFERENT total (17 vs 5), so the two do not share one
    normalization contract on a common state/effect domain. It
    therefore shows only that the quadratic rule is not the unique
    positive scale-distinct readout -- NOT that a genuine
    same-normalization effect-bearing rival exists. That is open
    obligation O-6 (born_nonuniqueness_open = false).

  Imports added at this rung
    The pairing form itself. Any uniqueness claim would import the
    Gleason hypothesis package -- named here, proved nowhere.

  Theorem or counterexample
    pairing_exists / pair_linear_state / pair_linear_effect: the
    pairing exists and is bilinear (proved).
    quartic_rival + quartic_not_proportional: a positive readout,
    not a rescaling of the quadratic one, differing pointwise --
    but at a different total (no shared normalization contract).
    born_nonuniqueness_open = false: honest open flag for O-6.

  Nonclaim boundary
    No probability interpretation. No claim Gleason fails: only
    that its hypotheses are imports absent here. No claim of Born
    non-uniqueness under a fixed normalization contract (O-6, open).
    No trace pairing: operators carry no admitted trace here yet.

  AuthorityEffect: None
-/

import HWKernel
import H008PhaseBlindPresentation

namespace FableHilbertWalk20260819.H013

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H008

/-- Bilinear state-effect pairing on integer weight vectors. -/
def pair {Q : Type} (E : Enum Q) (w e : Q → Int) : Int :=
  rsum intPack (E.elems.map (fun q => w q * e q))

/-- Indicator effect at a report state. -/
def indicator (b : Bool) : Bool → Int :=
  fun q => if q == b then 1 else 0

theorem pairing_exists :
    pair enumBool (phaseBlind psi1) (indicator false) = 1 ∧
      pair enumBool (phaseBlind psi1) (fun _ => 1) = 2 := by
  refine ⟨by decide, by decide⟩

#print axioms pairing_exists

/-! ## A positive rival readout that does NOT share a normalization
    contract (it totals 17 vs the quadratic's 5) and is NOT an
    effect-bearing rule on a common effect algebra. It shows only
    that the quadratic rule is not the unique positive scale-distinct
    readout -- not Born non-uniqueness (open O-6). -/

/-- Quartic readout: square of the quadratic weight. -/
def quartic {Q : Type} (v : Q → GaussInt) : Q → Int :=
  fun q => phaseBlind v q * phaseBlind v q

/-- The rival is positive on all inputs, like the quadratic one. -/
theorem quartic_nonneg {Q : Type} (v : Q → GaussInt) (q : Q) :
    0 ≤ quartic v q :=
  FableHilbertWalk20260819.H005.int_sq_nonneg (phaseBlind v q)

/-- Witness where quadratic and quartic disagree: amplitudes (2,1).
    Quadratic weights (4,1), quartic weights (16,1). Both are
    normalized at their own declared scales (5 and 17). -/
def psi21 : Bool → GaussInt :=
  fun q => if q then GaussInt.gone else ⟨2, 0⟩

theorem quartic_rival :
    (∀ q : Bool, 0 ≤ quartic psi21 q) ∧
      totalWeight enumBool psi21 = 5 ∧
      rsum intPack (enumBool.elems.map (quartic psi21)) = 17 ∧
      ¬(∀ q : Bool, phaseBlind psi21 q = quartic psi21 q) := by
  refine ⟨fun q => quartic_nonneg psi21 q, by decide, by decide, by decide⟩

#print axioms quartic_rival

/-- Bilinearity of the pairing, effect slot: proved, not asserted. -/
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

/-- Bilinearity, state slot. -/
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

/-- The pinned witness weights: quadratic (4,1), quartic (16,1). -/
theorem weights_pinned :
    (∀ q : Bool, phaseBlind psi21 q = if q then 1 else 4) ∧
      (∀ q : Bool, quartic psi21 q = if q then 1 else 16) := by
  refine ⟨by decide, by decide⟩

/-- The rival is not even a rescaling of the quadratic readout:
    the disagreement is scale-invariant. -/
theorem quartic_not_proportional :
    ¬ ∃ a b : Int, a ≠ 0 ∧
      (∀ q : Bool, a * quartic psi21 q = b * phaseBlind psi21 q) := by
  intro h
  rcases h with ⟨a, b, ha, hab⟩
  have h1 : a * 1 = b * 1 := hab true
  have h2 : a * 16 = b * 4 := hab false
  omega

#print axioms quartic_not_proportional

/-- Hand-set Bool status metadata naming the Gleason-package imports,
    not a theorem-bound hypothesis interface. The `rfl` result below
    reports these selected flags; it is not a no-go theorem. -/
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

/-- Hand-set status metadata for open O-6, not a theorem-bound gate.
    Same-normalization Born NON-uniqueness would require two effect
    rules on one domain and contract; none is constructed here. The
    quartic readout totals 17 versus 5 and is not an effect rule, so
    both unsupported fields stay false. The `rfl` result below only
    reports those selected flags. -/
structure BornNonUniquenessPack where
  common_domain : Bool
  shared_normalization_contract : Bool
  two_effect_rules_differ : Bool

def bornNonUniquenessHost : BornNonUniquenessPack where
  common_domain := true            -- weights over one Bool report set
  shared_normalization_contract := false  -- quartic totals 17, quadratic 5
  two_effect_rules_differ := false -- NO second effect-bearing RULE
    -- exists: the quartic is a state readout, not an element of a
    -- shared effect algebra. quartic_not_proportional shows two
    -- READOUTS differ, which is weaker than two effect rules.

def BornNonUniquenessDischarged (P : BornNonUniquenessPack) : Bool :=
  P.common_domain && P.shared_normalization_contract &&
    P.two_effect_rules_differ

theorem born_nonuniqueness_open :
    BornNonUniquenessDischarged bornNonUniquenessHost = false :=
  rfl

#print axioms born_nonuniqueness_open

/-- H013 punchline (honest): a bilinear pairing exists; a positive
    non-proportional rival readout exists (but not on a shared
    normalization contract); the Gleason uniqueness hypotheses are
    named as imports; same-contract Born non-uniqueness is OPEN. -/
theorem born_pairing_boundary :
    (pair enumBool (phaseBlind psi1) (indicator false) = 1) ∧
      ¬(∀ q : Bool, phaseBlind psi21 q = quartic psi21 q) ∧
      UniquenessDischarged hostSupplies = false ∧
      BornNonUniquenessDischarged bornNonUniquenessHost = false :=
  ⟨pairing_exists.1, quartic_rival.2.2.2, uniqueness_not_discharged,
    born_nonuniqueness_open⟩

#print axioms born_pairing_boundary

end FableHilbertWalk20260819.H013
