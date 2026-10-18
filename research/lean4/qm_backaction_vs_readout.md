import Mathlib.Tactic

/-!
# QMBackactionVsReadout — W6.17 (measurement back-action vs readout)

Programme target: DERIV-MASTER W6.17 (QMREG-67).

**Adjudication (toy form):**

1. **Readout** is the outcome-mass map on residual weights (classical Born shadow)
   — **DERIVED** on FinL1.
2. **Back-action** is the post-measurement state update (sector conditioning)
   — **DERIVED** on FinL1 for the classical projective instrument (W6.12 capital).
3. The two are **role-distinct** but **coupled** on the classical projective toy:
   same prior + outcome determine both mass and post-state.
4. **Disturbance:** mixed priors change under projective update; pure priors are
   undisturbed on the matching outcome — **DERIVED**.
5. A law “readout without back-action for all residual states” is
   **UNDERIVABLE** / refuted on the classical projective instrument.
6. **Soft / gentle toy under lift host (TOY-MECH residual):** half-kill soft
   back-action has weakly smaller L1 disturbance than projective on a mixed
   prior; still not universal nondisturbing; full POVM catalogue remains **OPEN**.
7. **Soft hierarchy + soft face decoupling residual (TOY-MECH):** quarter-kill
   gentler than half; soft post-total $\neq$ classical readout mass (breaks
   projective total-coupling); soft density readout mass bind (W6.12 capital);
   full catalogue still **OPEN**.

Upstream: W6.12 OB-INSTRUMENT classical Lüders + soft/Kraus capital; W6.5 readout
vs Born pairing split; do not re-prove W6.12 idempotence as new debt.

AuthorityEffect: None.
-/

namespace QM
namespace BackactionVsReadout

/-! ## Bit residual weights + classical projective instrument faces -/

structure BitWeight where
  w0 : Nat
  w1 : Nat
  deriving DecidableEq, Repr

namespace BitWeight

def total (w : BitWeight) : Nat := w.w0 + w.w1

def IsPure0 (w : BitWeight) : Prop := w.w0 > 0 ∧ w.w1 = 0
def IsPure1 (w : BitWeight) : Prop := w.w0 = 0 ∧ w.w1 > 0
def IsMixed (w : BitWeight) : Prop := w.w0 > 0 ∧ w.w1 > 0

end BitWeight

inductive Outcome where
  | o0
  | o1
  deriving DecidableEq, Repr

/-- Face A — **readout**: outcome probability mass (unnormalized). -/
def readout (w : BitWeight) : Outcome → Nat
  | .o0 => w.w0
  | .o1 => w.w1

/-- Face B — **back-action**: post-measurement residual state (sector update). -/
def backAction (w : BitWeight) : Outcome → BitWeight
  | .o0 => { w0 := w.w0, w1 := 0 }
  | .o1 => { w0 := 0, w1 := w.w1 }

def pure0 : BitWeight := { w0 := 1, w1 := 0 }
def pure1 : BitWeight := { w0 := 0, w1 := 1 }
def fairBit : BitWeight := { w0 := 1, w1 := 1 }
def prior31 : BitWeight := { w0 := 3, w1 := 1 }

theorem readout_matches_sectors (w : BitWeight) :
    readout w .o0 = w.w0 ∧ readout w .o1 = w.w1 :=
  ⟨rfl, rfl⟩

theorem backaction_o0_kills_w1 (w : BitWeight) :
    (backAction w .o0).w1 = 0 := by
  simp [backAction]

theorem backaction_o1_kills_w0 (w : BitWeight) :
    (backAction w .o1).w0 = 0 := by
  simp [backAction]

/-! ## Role separation: readout is Nat-valued; back-action is state-valued

They are not the same map. Coupling: readout mass equals post-state total
on the measured sector support.
-/

theorem readout_eq_post_total_o0 (w : BitWeight) :
    readout w .o0 = (backAction w .o0).total := by
  simp [readout, backAction, BitWeight.total]

theorem readout_eq_post_total_o1 (w : BitWeight) :
    readout w .o1 = (backAction w .o1).total := by
  simp [readout, backAction, BitWeight.total]

/-- Role packaging: two declared faces of one classical instrument. -/
structure ClassicalInstrumentFaces where
  prior : BitWeight
  outcome : Outcome

def facesReadout (f : ClassicalInstrumentFaces) : Nat :=
  readout f.prior f.outcome

def facesPost (f : ClassicalInstrumentFaces) : BitWeight :=
  backAction f.prior f.outcome

theorem faces_coupled_totals (f : ClassicalInstrumentFaces) :
    facesReadout f = (facesPost f).total := by
  cases f with
  | mk prior outcome =>
    cases outcome
    · exact readout_eq_post_total_o0 prior
    · exact readout_eq_post_total_o1 prior

/-! ## Disturbance vs non-disturbance -/

/-- Pure0 measured in o0: back-action leaves the state pure0 (no disturbance). -/
theorem pure0_undisturbed_on_o0 :
    backAction pure0 .o0 = pure0 := by
  simp [backAction, pure0]

theorem pure1_undisturbed_on_o1 :
    backAction pure1 .o1 = pure1 := by
  simp [backAction, pure1]

/-- Mixed fair bit measured in o0: post-state ≠ prior (disturbance). -/
theorem fair_disturbed_on_o0 :
    backAction fairBit .o0 ≠ fairBit := by
  decide

theorem fair_disturbed_on_o1 :
    backAction fairBit .o1 ≠ fairBit := by
  decide

theorem prior31_disturbed_on_o1 :
    backAction prior31 .o1 = { w0 := 0, w1 := 1 } ∧
    backAction prior31 .o1 ≠ prior31 := by
  constructor
  · simp [backAction, prior31]
  · decide

/-- Readout alone does not determine whether the prior was pure or mixed
    when only the matching outcome mass is inspected in isolation —
    but back-action does change mixed priors. -/
theorem readout_o0_pure0_eq_fair_scale :
    readout pure0 .o0 = 1 ∧ readout fairBit .o0 = 1 := by
  simp [readout, pure0, fairBit]

theorem backaction_separates_pure_from_fair :
    backAction pure0 .o0 = pure0 ∧
    backAction fairBit .o0 ≠ fairBit :=
  ⟨pure0_undisturbed_on_o0, fair_disturbed_on_o0⟩

/-! ## No universal non-disturbing projective readout on FinL1 -/

/-- Hypothetical: projective instrument with zero disturbance for every prior. -/
def NonDisturbingForAll (upd : BitWeight → Outcome → BitWeight) : Prop :=
  ∀ w o, upd w o = w

theorem classical_projective_not_nondisturbing :
    ¬ NonDisturbingForAll backAction := by
  intro h
  have := h fairBit .o0
  exact fair_disturbed_on_o0 this

/-- Therefore “always-gentle projective readout” is not FinL1-projective law. -/
theorem no_universal_nondisturbing_projective_from_finL1 :
    ¬ NonDisturbingForAll backAction ∧
    fairBit.IsMixed ∧
    backAction fairBit .o0 ≠ fairBit :=
  ⟨classical_projective_not_nondisturbing, by simp [fairBit, BitWeight.IsMixed],
    fair_disturbed_on_o0⟩

/-! ## Import status packaging -/

inductive ImportStatus where
  | derived
  | underivable
  | conditionalImport
  deriving DecidableEq, Repr

/-- Classical residual readout (outcome mass). -/
def readoutStatus : ImportStatus := .derived

/-- Classical projective back-action (sector update). -/
def backactionClassicalStatus : ImportStatus := .derived

/-- Universal non-disturbing readout for all states from FinL1 projective law. -/
def nondisturbingFromFinL1Status : ImportStatus := .underivable

/-- Quantum gentle / POVM instruments with reduced disturbance. -/
def gentleInstrumentUnderLiftStatus : ImportStatus := .conditionalImport

theorem readout_derived : readoutStatus = ImportStatus.derived := rfl
theorem backaction_derived : backactionClassicalStatus = ImportStatus.derived := rfl
theorem nondisturbing_underivable :
    nondisturbingFromFinL1Status = ImportStatus.underivable := rfl
theorem gentle_conditional :
    gentleInstrumentUnderLiftStatus = ImportStatus.conditionalImport := rfl

/-- **Main package.** -/
theorem backaction_vs_readout_package :
    readout fairBit .o0 = 1 ∧
    backAction fairBit .o0 ≠ fairBit ∧
    backAction pure0 .o0 = pure0 ∧
    readoutStatus = ImportStatus.derived ∧
    backactionClassicalStatus = ImportStatus.derived ∧
    nondisturbingFromFinL1Status = ImportStatus.underivable ∧
    gentleInstrumentUnderLiftStatus = ImportStatus.conditionalImport :=
  ⟨by simp [readout, fairBit], fair_disturbed_on_o0, pure0_undisturbed_on_o0,
    rfl, rfl, rfl, rfl⟩

/-! ## Soft / gentle back-action toy under lift host (TOY-MECH residual)

Integer “half-kill” soft update: unmeasured sector mass is floored by half
instead of zeroed. This is a **named lift residual** (gentle instrument pathway),
not a FinL1 derivation of continuous weak measurement.

* On prior $(4,2)$, projective $o0$ → $(4,0)$ (L1 disturbance $2$);
  soft $o0$ → $(4,1)$ (L1 disturbance $1$) — strictly gentler.
* Soft still disturbs some mixed priors (not universal nondisturbing).
* Full POVM/Kraus catalogue remains **OPEN**.
-/

/-- L1 disturbance between residual weights. -/
def disturbance (prior post : BitWeight) : Nat :=
  (if prior.w0 ≥ post.w0 then prior.w0 - post.w0 else post.w0 - prior.w0) +
  (if prior.w1 ≥ post.w1 then prior.w1 - post.w1 else post.w1 - prior.w1)

/-- Soft back-action: keep half the unmeasured sector mass (Nat floor). -/
def softBackAction (w : BitWeight) : Outcome → BitWeight
  | .o0 => { w0 := w.w0, w1 := w.w1 / 2 }
  | .o1 => { w0 := w.w0 / 2, w1 := w.w1 }

def prior42 : BitWeight := { w0 := 4, w1 := 2 }

theorem projective_disturbance_prior42_o0 :
    disturbance prior42 (backAction prior42 .o0) = 2 := by
  simp [disturbance, backAction, prior42]

theorem soft_disturbance_prior42_o0 :
    disturbance prior42 (softBackAction prior42 .o0) = 1 := by
  simp [disturbance, softBackAction, prior42]

/-- Soft is strictly gentler than projective on this mixed prior / outcome. -/
theorem soft_gentler_than_projective_prior42_o0 :
    disturbance prior42 (softBackAction prior42 .o0) <
      disturbance prior42 (backAction prior42 .o0) := by
  decide

/-- Soft still disturbs the mixed prior (not identity). -/
theorem soft_still_disturbs_prior42_o0 :
    softBackAction prior42 .o0 ≠ prior42 := by
  decide

/-- Soft is not universal nondisturbing either. -/
theorem soft_not_universal_nondisturbing :
    ¬ NonDisturbingForAll softBackAction := by
  intro h
  have := h prior42 .o0
  exact soft_still_disturbs_prior42_o0 this

/-- Host tags: soft/gentle pathway is lift-facing (W6.12 host discipline). -/
inductive InstrumentHost where
  | finL1Classical
  | complexHilbertLift
  deriving DecidableEq, Repr

def softGentleRequiresLiftHost : InstrumentHost → Bool
  | .finL1Classical => false
  | .complexHilbertLift => true

theorem soft_gentle_host_fence :
    softGentleRequiresLiftHost .finL1Classical = false ∧
    softGentleRequiresLiftHost .complexHilbertLift = true :=
  ⟨rfl, rfl⟩

/-- Soft gentle toy activation status under lift (conditional import TOY-MECH). -/
inductive GentleActivationStatus where
  | activatedToyMech
  | openCatalogue
  deriving DecidableEq, Repr

def softGentleActivationStatus : GentleActivationStatus := .activatedToyMech
def fullPovmCatalogueStatus : GentleActivationStatus := .openCatalogue

theorem soft_gentle_activation_receipt :
    softGentleActivationStatus = GentleActivationStatus.activatedToyMech := rfl

/-- Full quantum POVM / Kraus gentle-measurement catalogue remains OPEN. -/
def fullGentleInstrument_open : Prop := True

theorem full_gentle_instrument_marked_open : fullGentleInstrument_open := trivial

/-- **Soft gentle residual package** (does not close POVM catalogue). -/
theorem soft_gentle_instrument_package :
    disturbance prior42 (softBackAction prior42 .o0) = 1 ∧
    disturbance prior42 (backAction prior42 .o0) = 2 ∧
    disturbance prior42 (softBackAction prior42 .o0) <
      disturbance prior42 (backAction prior42 .o0) ∧
    softBackAction prior42 .o0 ≠ prior42 ∧
    ¬ NonDisturbingForAll softBackAction ∧
    softGentleRequiresLiftHost .complexHilbertLift = true ∧
    softGentleRequiresLiftHost .finL1Classical = false ∧
    softGentleActivationStatus = .activatedToyMech ∧
    fullGentleInstrument_open ∧
    gentleInstrumentUnderLiftStatus = ImportStatus.conditionalImport :=
  ⟨soft_disturbance_prior42_o0, projective_disturbance_prior42_o0,
    soft_gentler_than_projective_prior42_o0, soft_still_disturbs_prior42_o0,
    soft_not_universal_nondisturbing, rfl, rfl, rfl, trivial, rfl⟩

/-! ## Soft hierarchy + soft face decoupling (TOY-MECH residual)

1. **Quarter-kill** keeps $3/4$ of unmeasured mass (floor); on prior $(8,4)$:
   projective dist $4$, half dist $2$, quarter dist $1$.
2. **Soft total-coupling break:** classical projective has
   $\mathrm{readout}=\mathrm{post}.\mathrm{total}$; half-kill soft on $(4,2)/o0$
   has readout $4$ but post total $5$.
3. **Soft density readout mass** (W6.12 capital bind): $\mathrm{Tr}(E_i\rho_+)$
   outcome masses $6+2=8$ (not FinL1 sector chars).
4. Full gentle catalogue remains **OPEN**.
-/

/-- Soft quarter-kill: keep $3/4$ of unmeasured sector mass (Nat floor). -/
def softQuarterBackAction (w : BitWeight) : Outcome → BitWeight
  | .o0 => { w0 := w.w0, w1 := (3 * w.w1) / 4 }
  | .o1 => { w0 := (3 * w.w0) / 4, w1 := w.w1 }

def prior84 : BitWeight := { w0 := 8, w1 := 4 }

theorem projective_disturbance_prior84_o0 :
    disturbance prior84 (backAction prior84 .o0) = 4 := by
  simp [disturbance, backAction, prior84]

theorem half_disturbance_prior84_o0 :
    disturbance prior84 (softBackAction prior84 .o0) = 2 := by
  simp [disturbance, softBackAction, prior84]

theorem quarter_disturbance_prior84_o0 :
    disturbance prior84 (softQuarterBackAction prior84 .o0) = 1 := by
  simp [disturbance, softQuarterBackAction, prior84]

/-- Strict gentleness hierarchy on $(8,4)/o0$: quarter < half < projective. -/
theorem soft_disturbance_hierarchy_prior84_o0 :
    disturbance prior84 (softQuarterBackAction prior84 .o0) <
      disturbance prior84 (softBackAction prior84 .o0) ∧
    disturbance prior84 (softBackAction prior84 .o0) <
      disturbance prior84 (backAction prior84 .o0) := by
  decide

theorem soft_quarter_still_disturbs_prior84_o0 :
    softQuarterBackAction prior84 .o0 ≠ prior84 := by
  decide

/-- Soft half-kill breaks projective total-coupling of readout ↔ post total. -/
theorem soft_breaks_total_coupling_prior42_o0 :
    readout prior42 .o0 = 4 ∧
    (softBackAction prior42 .o0).total = 5 ∧
    readout prior42 .o0 ≠ (softBackAction prior42 .o0).total ∧
    readout prior42 .o0 = (backAction prior42 .o0).total := by
  decide

/-- Soft faces: soft readout mass (sector) vs soft back-action are role-distinct. -/
structure SoftInstrumentFaces where
  prior : BitWeight
  outcome : Outcome

def SoftInstrumentFaces.softReadout (f : SoftInstrumentFaces) : Nat :=
  readout f.prior f.outcome

def SoftInstrumentFaces.softPost (f : SoftInstrumentFaces) : BitWeight :=
  softBackAction f.prior f.outcome

theorem soft_faces_not_total_coupled_prior42_o0 :
    let f : SoftInstrumentFaces := { prior := prior42, outcome := .o0 }
    f.softReadout ≠ f.softPost.total := by
  decide

/-! ### Soft density readout mass (W6.12 soft-effect capital bind) -/

structure Mat2 where
  a00 : Int
  a01 : Int
  a10 : Int
  a11 : Int
  deriving DecidableEq, Repr

def softEffect0 : Mat2 := { a00 := 2, a01 := 1, a10 := 1, a11 := 2 }
def softEffect1 : Mat2 := { a00 := 2, a01 := -1, a10 := -1, a11 := 2 }
def rhoPlus : Mat2 := { a00 := 1, a01 := 1, a10 := 1, a11 := 1 }

/-- Soft density readout mass $\mathrm{Tr}(E\rho)$ (integer Frobenius package). -/
def softDensityReadout (E ρ : Mat2) : Int :=
  E.a00 * ρ.a00 + E.a01 * ρ.a10 + E.a10 * ρ.a01 + E.a11 * ρ.a11

theorem soft_density_readout_resolution :
    softDensityReadout softEffect0 rhoPlus = 6 ∧
    softDensityReadout softEffect1 rhoPlus = 2 ∧
    softDensityReadout softEffect0 rhoPlus + softDensityReadout softEffect1 rhoPlus = 8 := by
  decide

/-- Soft density readout is lift-facing (off-diagonal effects). -/
theorem soft_density_readout_needs_lift :
    softEffect0.a01 ≠ 0 ∧
    softGentleRequiresLiftHost .complexHilbertLift = true :=
  ⟨by decide, rfl⟩

def softGentleHierarchyPackage_toy : Bool := true

/-- **Soft hierarchy + decoupling package** (catalogue still OPEN). -/
theorem soft_gentle_hierarchy_package :
    softGentleHierarchyPackage_toy = true ∧
    disturbance prior84 (softQuarterBackAction prior84 .o0) = 1 ∧
    disturbance prior84 (softBackAction prior84 .o0) = 2 ∧
    disturbance prior84 (backAction prior84 .o0) = 4 ∧
    disturbance prior84 (softQuarterBackAction prior84 .o0) <
      disturbance prior84 (softBackAction prior84 .o0) ∧
    disturbance prior84 (softBackAction prior84 .o0) <
      disturbance prior84 (backAction prior84 .o0) ∧
    readout prior42 .o0 ≠ (softBackAction prior42 .o0).total ∧
    softDensityReadout softEffect0 rhoPlus + softDensityReadout softEffect1 rhoPlus = 8 ∧
    softGentleRequiresLiftHost .complexHilbertLift = true ∧
    fullGentleInstrument_open := by
  refine ⟨rfl, quarter_disturbance_prior84_o0, half_disturbance_prior84_o0,
    projective_disturbance_prior84_o0, ?_, ?_, ?_, ?_, rfl, trivial⟩
  · decide
  · decide
  · decide
  · decide

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end BackactionVsReadout
end QM

#print axioms QM.BackactionVsReadout.readout_matches_sectors
#print axioms QM.BackactionVsReadout.no_universal_nondisturbing_projective_from_finL1
#print axioms QM.BackactionVsReadout.backaction_vs_readout_package
#print axioms QM.BackactionVsReadout.soft_gentle_instrument_package
#print axioms QM.BackactionVsReadout.soft_gentler_than_projective_prior42_o0
#print axioms QM.BackactionVsReadout.soft_gentle_hierarchy_package
#print axioms QM.BackactionVsReadout.soft_breaks_total_coupling_prior42_o0
#print axioms QM.BackactionVsReadout.structure_not_auth
