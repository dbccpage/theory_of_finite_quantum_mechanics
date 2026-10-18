/-
  H008 -- phase-blind presentation. AuthorityEffect: None. Candidate
  only. Not PROVEN. Kind: LIFT RUNG.

  Claim identifier: HW-H008
  Source-paper contact: QM_020 C-layer (diagonal weights), QM_060
  (phase content), QM_061 C1-C2 (carrier and phase-blind primitive
  difference), QM_208 (audited as proposal).

  Target proposition
    The coordinatewise map psi_q -> |psi_q|^2 from Gaussian-integer
    amplitude vectors to integer weight vectors is a presentation in
    the H000 sense. It is QUADRATIC BY IMPORT: calling it the Born
    presentation would smuggle the Born rule; here it is named
    phase-blind. Its normalization is carried explicitly as total
    weight.

  Imports added at this rung
    The quadratic readout |.|^2 itself, and the declared sector
    basis in which it is diagonal. Both are choices.

  Theorem or counterexample
    weight_nonneg / weight_real: the presentation lands in honest
    integer weights (via H005 gauss_self_real).
    equal_moduli_diff_phase: (1,1) and (1,-1) have equal weights and
    are unequal vectors -- the countermodel the work order names.
    global_phase_blind: multiplying by i preserves every weight
    (general theorem, any vector).

  Nonclaim boundary
    NOT called Born: no probability interpretation, no uniqueness
    of the quadratic rule (H013 prices that). The sector basis is
    declared, not derived (H005 gram_not_unique already separates
    basis choices).

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import H004FreeLinearization
import H005InnerProductAdmission

namespace FableHilbertWalk20260819.H008

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H005 (gauss_self_real int_sq_nonneg)

/-- Coordinatewise squared modulus: the phase-blind presentation.
    Quadratic BY IMPORT, not by derivation. -/
def phaseBlind {Q : Type} (v : Vec GaussInt Q) : Q → Int :=
  fun q => (GaussInt.gmul (GaussInt.gconj (v q)) (v q)).re

/-- Total weight: the explicit normalization data. -/
def totalWeight {Q : Type} (E : Enum Q) (v : Vec GaussInt Q) : Int :=
  rsum intPack (E.elems.map (phaseBlind v))

theorem weight_nonneg {Q : Type} (v : Vec GaussInt Q) (q : Q) :
    0 ≤ phaseBlind v q :=
  (gauss_self_real (v q)).2

#print axioms weight_nonneg

/-- The presentation forgets nothing off-record: the im-part of
    conj(z)*z is identically zero, so Int weights lose no data. -/
theorem weight_real {Q : Type} (v : Vec GaussInt Q) (q : Q) :
    (GaussInt.gmul (GaussInt.gconj (v q)) (v q)).im = 0 :=
  (gauss_self_real (v q)).1

#print axioms weight_real

/-! ## The named countermodel: equal moduli, different phases. -/

/-- psi1 = (1, 1). -/
def psi1 : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gone else GaussInt.gone

/-- psi2 = (1, -1): same moduli, opposite relative phase. -/
def psi2 : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gneg GaussInt.gone else GaussInt.gone

theorem equal_weights : ∀ q : Bool, phaseBlind psi1 q = phaseBlind psi2 q := by
  intro q; cases q <;> rfl

theorem distinct_vectors : ¬(∀ q : Bool, psi1 q = psi2 q) := by
  intro h
  have h1 := h true
  revert h1
  decide

theorem equal_total :
    totalWeight enumBool psi1 = 2 ∧ totalWeight enumBool psi2 = 2 := by
  refine ⟨by decide, by decide⟩

#print axioms equal_weights
#print axioms distinct_vectors

/-! ## Global phase blindness: a general theorem, not a fixture. -/

theorem global_phase_blind {Q : Type} (v : Vec GaussInt Q) (q : Q) :
    phaseBlind (fun x => GaussInt.gmul GaussInt.gi (v x)) q =
      phaseBlind v q := by
  unfold phaseBlind
  rw [GaussInt.gconj_gi_mul (v q) (v q)]

#print axioms global_phase_blind

/-- H008 punchline: the quadratic presentation is honest (real,
    nonnegative, explicitly normalized), blind to global phase in
    general, and blind to the (1,1)/(1,-1) relative phase. -/
theorem phase_blind_presentation :
    (∀ q : Bool, phaseBlind psi1 q = phaseBlind psi2 q) ∧
      ¬(∀ q : Bool, psi1 q = psi2 q) ∧
      (∀ (v : Vec GaussInt Bool) (q : Bool),
        phaseBlind (fun x => GaussInt.gmul GaussInt.gi (v x)) q =
          phaseBlind v q) ∧
      totalWeight enumBool psi1 = totalWeight enumBool psi2 :=
  ⟨equal_weights, distinct_vectors,
    fun v q => global_phase_blind v q, by decide⟩

#print axioms phase_blind_presentation

end FableHilbertWalk20260819.H008
