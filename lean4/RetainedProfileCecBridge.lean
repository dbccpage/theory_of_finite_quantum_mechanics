
import PrimitiveDifference



namespace RetainedProfileCECBridge

open OmegaCore
open OmegaCore.PrimitiveDifference

universe u v w u' v' w' i o o'


def RetainedDiff {X : Type u}
    (retained : X → X → Prop) (x y : X) : Prop :=
  retained x y

def Protected {X : Type u}
    (guarded : X → X → Prop) (x y : X) : Prop :=
  guarded x y

def ProfileDifference {I : Type i} {X : Type u} {O : Type o}
    (profile : I → X → O) (observer : I) (x y : X) : Prop :=
  profile observer x ≠ profile observer y

def ZeroRel_r {I : Type i} {X : Type u} {O : Type o}
    (profile : I → X → O) (observer : I) (x y : X) : Prop :=
  ¬ ProfileDifference profile observer x y

structure ActiveObstruction {I : Type i} {X : Type u} {O : Type o}
    (profile : I → X → O) (observer : I)
    (retained guarded : X → X → Prop) (x y : X) : Prop where
  retained : RetainedDiff retained x y
  zeroRelated : ZeroRel_r profile observer x y
  isProtected : Protected guarded x y

theorem retainedDiff_zeroRel_protected_activeObstruction
    {I : Type i} {X : Type u} {O : Type o}
    {profile : I → X → O} {observer : I}
    {retained guarded : X → X → Prop} {x y : X} :
    RetainedDiff retained x y ∧
        ZeroRel_r profile observer x y ∧ Protected guarded x y →
      ActiveObstruction profile observer retained guarded x y := by
  intro h
  exact ⟨h.1, h.2.1, h.2.2⟩


def boolRetainedDeclaration (x y : Bool) : Prop :=
  x = true ∧ y = false

def boolConstantProfile (_ : Unit) (_ : Bool) : Unit := ()

def boolNeverProtected (_ _ : Bool) : Prop := False

theorem unprotected_collapse_countermodel :
    RetainedDiff boolRetainedDeclaration true false ∧
      ZeroRel_r boolConstantProfile () true false ∧
      ¬ Protected boolNeverProtected true false ∧
      ¬ ActiveObstruction
        boolConstantProfile () boolRetainedDeclaration boolNeverProtected
          true false := by
  refine ⟨⟨rfl, rfl⟩, ?_, ?_, ?_⟩
  · intro hDifference
    exact hDifference rfl
  · intro h
    exact h
  · intro h
    exact h.isProtected


structure Presentation (X : Type u) (Sig : Type v) (R : Type w) where
  difference : PrimitiveDifference X R
  step : Sig → X → X

namespace Presentation

def run {X : Type u} {Sig : Type v} {R : Type w}
    (P : Presentation X Sig R) : List Sig → X → X
  | [], x => x
  | op :: program, x => run P program (P.step op x)

theorem run_append {X : Type u} {Sig : Type v} {R : Type w}
    (P : Presentation X Sig R) (left right : List Sig) (x : X) :
    P.run (left ++ right) x = P.run right (P.run left x) := by
  induction left generalizing x with
  | nil => rfl
  | cons op program ih =>
      simp [run, ih]

end Presentation

structure SameLevelRepair {X : Type u} {Sig : Type v} {R : Type w}
    (P : Presentation X Sig R) (start finish : X) where
  program : List Sig
  reaches : P.run program start = finish

def SameLevelRepair.trans {X : Type u} {Sig : Type v} {R : Type w}
    {P : Presentation X Sig R} {x y z : X}
    (first : SameLevelRepair P x y) (second : SameLevelRepair P y z) :
    SameLevelRepair P x z where
  program := first.program ++ second.program
  reaches := by
    rw [Presentation.run_append, first.reaches, second.reaches]

theorem sameLevelRepair_replays_in_same_carrier_and_signature
    {X : Type u} {Sig : Type v} {R : Type w}
    {P : Presentation X Sig R} {x y : X}
    (repair : SameLevelRepair P x y) :
    ∃ program : List Sig, P.run program x = y :=
  ⟨repair.program, repair.reaches⟩


inductive Terminal where
  | SameLevelRepair
  | TypedRefusal
  | ConservativeExtensionProposal
deriving DecidableEq, Repr

structure TerminalEvidence where
  sameLevelRepairVerified : Bool
  sameLevelSearchExhausted : Bool
  extensionAdmissible : Bool
deriving DecidableEq, Repr

def classifyTerminal : TerminalEvidence → Terminal
  | ⟨true, _, _⟩ => .SameLevelRepair
  | ⟨false, true, true⟩ => .ConservativeExtensionProposal
  | ⟨false, _, _⟩ => .TypedRefusal

theorem classifyTerminal_sameLevelRepair_iff (e : TerminalEvidence) :
    classifyTerminal e = .SameLevelRepair ↔
      e.sameLevelRepairVerified = true := by
  cases e with
  | mk repair exhausted admissible =>
      cases repair <;> cases exhausted <;> cases admissible <;> decide

theorem classifyTerminal_conservativeExtensionProposal_iff
    (e : TerminalEvidence) :
    classifyTerminal e = .ConservativeExtensionProposal ↔
      e.sameLevelRepairVerified = false ∧
      e.sameLevelSearchExhausted = true ∧
      e.extensionAdmissible = true := by
  cases e with
  | mk repair exhausted admissible =>
      cases repair <;> cases exhausted <;> cases admissible <;> decide

theorem classifyTerminal_typedRefusal_iff (e : TerminalEvidence) :
    classifyTerminal e = .TypedRefusal ↔
      e.sameLevelRepairVerified = false ∧
      (e.sameLevelSearchExhausted = false ∨
        e.extensionAdmissible = false) := by
  cases e with
  | mk repair exhausted admissible =>
      cases repair <;> cases exhausted <;> cases admissible <;> decide

theorem classifyTerminal_total (e : TerminalEvidence) :
    classifyTerminal e = .SameLevelRepair ∨
      classifyTerminal e = .TypedRefusal ∨
      classifyTerminal e = .ConservativeExtensionProposal := by
  cases e with
  | mk repair exhausted admissible =>
      cases repair <;> cases exhausted <;> cases admissible <;> decide

theorem classifyTerminal_exclusive (e : TerminalEvidence) :
    (classifyTerminal e = .SameLevelRepair ∧
        classifyTerminal e ≠ .TypedRefusal ∧
        classifyTerminal e ≠ .ConservativeExtensionProposal) ∨
    (classifyTerminal e = .TypedRefusal ∧
        classifyTerminal e ≠ .SameLevelRepair ∧
        classifyTerminal e ≠ .ConservativeExtensionProposal) ∨
    (classifyTerminal e = .ConservativeExtensionProposal ∧
        classifyTerminal e ≠ .SameLevelRepair ∧
        classifyTerminal e ≠ .TypedRefusal) := by
  cases e with
  | mk repair exhausted admissible =>
      cases repair <;> cases exhausted <;> cases admissible <;> decide


structure ConservativeExtensionCertificate
    {X : Type u} {Sig : Type v} {R : Type w}
    {Y : Type u'} {Tau : Type v'} {S : Type w'}
    (oldP : Presentation X Sig R) (newP : Presentation Y Tau S)
    (oldRetained oldProtected : X → X → Prop)
    (newRetained newProtected : Y → Y → Prop) where
  carrierEmbed : X → Y
  carrierRetract : Y → X
  carrierRetract_embed : ∀ x : X, carrierRetract (carrierEmbed x) = x
  signatureEmbed : Sig → Tau
  signatureRetract : Tau → Sig
  signatureRetract_embed : ∀ op : Sig,
    signatureRetract (signatureEmbed op) = op
  transition_preservation : ∀ (op : Sig) (x : X),
    newP.step (signatureEmbed op) (carrierEmbed x) =
      carrierEmbed (oldP.step op x)
  zero_refinement : ∀ {x y : X},
    newP.difference.ZeroRel (carrierEmbed x) (carrierEmbed y) →
      oldP.difference.ZeroRel x y
  retained_preservation : ∀ {x y : X},
    oldRetained x y → newRetained (carrierEmbed x) (carrierEmbed y)
  protected_preservation : ∀ {x y : X},
    oldProtected x y → newProtected (carrierEmbed x) (carrierEmbed y)
  strict_extension :
    (∃ y : Y, ∀ x : X, carrierEmbed x ≠ y) ∨
      (∃ opNew : Tau, ∀ op : Sig, signatureEmbed op ≠ opNew)

namespace ConservativeExtensionCertificate

theorem carrierEmbed_injective
    {X : Type u} {Sig : Type v} {R : Type w}
    {Y : Type u'} {Tau : Type v'} {S : Type w'}
    {oldP : Presentation X Sig R} {newP : Presentation Y Tau S}
    {oldRetained oldProtected : X → X → Prop}
    {newRetained newProtected : Y → Y → Prop}
    (C : ConservativeExtensionCertificate oldP newP
      oldRetained oldProtected newRetained newProtected)
    {x y : X} (h : C.carrierEmbed x = C.carrierEmbed y) : x = y := by
  calc
    x = C.carrierRetract (C.carrierEmbed x) :=
      (C.carrierRetract_embed x).symm
    _ = C.carrierRetract (C.carrierEmbed y) := congrArg C.carrierRetract h
    _ = y := C.carrierRetract_embed y

theorem signatureEmbed_injective
    {X : Type u} {Sig : Type v} {R : Type w}
    {Y : Type u'} {Tau : Type v'} {S : Type w'}
    {oldP : Presentation X Sig R} {newP : Presentation Y Tau S}
    {oldRetained oldProtected : X → X → Prop}
    {newRetained newProtected : Y → Y → Prop}
    (C : ConservativeExtensionCertificate oldP newP
      oldRetained oldProtected newRetained newProtected)
    {a b : Sig} (h : C.signatureEmbed a = C.signatureEmbed b) : a = b := by
  calc
    a = C.signatureRetract (C.signatureEmbed a) :=
      (C.signatureRetract_embed a).symm
    _ = C.signatureRetract (C.signatureEmbed b) :=
      congrArg C.signatureRetract h
    _ = b := C.signatureRetract_embed b

theorem embedded_zeroRel_refines
    {X : Type u} {Sig : Type v} {R : Type w}
    {Y : Type u'} {Tau : Type v'} {S : Type w'}
    {oldP : Presentation X Sig R} {newP : Presentation Y Tau S}
    {oldRetained oldProtected : X → X → Prop}
    {newRetained newProtected : Y → Y → Prop}
    (C : ConservativeExtensionCertificate oldP newP
      oldRetained oldProtected newRetained newProtected)
    {x y : X}
    (h : newP.difference.ZeroRel (C.carrierEmbed x) (C.carrierEmbed y)) :
    oldP.difference.ZeroRel x y :=
  C.zero_refinement h

theorem embedded_nonzero_preserved
    {X : Type u} {Sig : Type v} {R : Type w}
    {Y : Type u'} {Tau : Type v'} {S : Type w'}
    {oldP : Presentation X Sig R} {newP : Presentation Y Tau S}
    {oldRetained oldProtected : X → X → Prop}
    {newRetained newProtected : Y → Y → Prop}
    (C : ConservativeExtensionCertificate oldP newP
      oldRetained oldProtected newRetained newProtected)
    {x y : X} (h : ¬ oldP.difference.ZeroRel x y) :
    ¬ newP.difference.ZeroRel (C.carrierEmbed x) (C.carrierEmbed y) := by
  intro hnew
  exact h (C.zero_refinement hnew)

end ConservativeExtensionCertificate


structure DemandFamily (I : Type i) (X : Type u) (O : Type o) where
  profile : I → X → O
  declared : I → Prop

def DemandOrbitRel {I : Type i} {X : Type u} {Sig : Type v}
    {R : Type w} {O : Type o}
    (P : Presentation X Sig R) (D : DemandFamily I X O) (x y : X) : Prop :=
  ∀ demand : I, D.declared demand → ∀ program : List Sig,
    D.profile demand (P.run program x) =
      D.profile demand (P.run program y)

theorem demandOrbitRel_equivalence
    {I : Type i} {X : Type u} {Sig : Type v} {R : Type w} {O : Type o}
    (P : Presentation X Sig R) (D : DemandFamily I X O) :
    Equivalence (DemandOrbitRel P D) where
  refl := by
    intro x demand hDemand program
    rfl
  symm := by
    intro x y hxy demand hDemand program
    exact (hxy demand hDemand program).symm
  trans := by
    intro x y z hxy hyz demand hDemand program
    exact (hxy demand hDemand program).trans (hyz demand hDemand program)

def demandOrbitSetoid
    {I : Type i} {X : Type u} {Sig : Type v} {R : Type w} {O : Type o}
    (P : Presentation X Sig R) (D : DemandFamily I X O) : Setoid X where
  r := DemandOrbitRel P D
  iseqv := demandOrbitRel_equivalence P D

theorem demandOrbit_step_congruent
    {I : Type i} {X : Type u} {Sig : Type v} {R : Type w} {O : Type o}
    (P : Presentation X Sig R) (D : DemandFamily I X O)
    (op : Sig) {x y : X} (hxy : DemandOrbitRel P D x y) :
    DemandOrbitRel P D (P.step op x) (P.step op y) := by
  intro demand hDemand program
  exact hxy demand hDemand (op :: program)

def DemandOrbitQuotient
    {I : Type i} {X : Type u} {Sig : Type v} {R : Type w} {O : Type o}
    (P : Presentation X Sig R) (D : DemandFamily I X O) : Type u :=
  Quotient (demandOrbitSetoid P D)

def demandOrbitClass
    {I : Type i} {X : Type u} {Sig : Type v} {R : Type w} {O : Type o}
    (P : Presentation X Sig R) (D : DemandFamily I X O) (x : X) :
    DemandOrbitQuotient P D :=
  Quotient.mk (demandOrbitSetoid P D) x

theorem demandOrbitClass_eq_iff
    {I : Type i} {X : Type u} {Sig : Type v} {R : Type w} {O : Type o}
    (P : Presentation X Sig R) (D : DemandFamily I X O) {x y : X} :
    demandOrbitClass P D x = demandOrbitClass P D y ↔
      DemandOrbitRel P D x y := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

def quotientTransition
    {I : Type i} {X : Type u} {Sig : Type v} {R : Type w} {O : Type o}
    (P : Presentation X Sig R) (D : DemandFamily I X O) (op : Sig) :
    DemandOrbitQuotient P D → DemandOrbitQuotient P D :=
  Quotient.lift
    (fun x => demandOrbitClass P D (P.step op x))
    (by
      intro x y hxy
      exact Quotient.sound (demandOrbit_step_congruent P D op hxy))

theorem quotientTransition_carries_demandOrbitClass
    {I : Type i} {X : Type u} {Sig : Type v} {R : Type w} {O : Type o}
    (P : Presentation X Sig R) (D : DemandFamily I X O)
    (op : Sig) (x : X) :
    quotientTransition P D op (demandOrbitClass P D x) =
      demandOrbitClass P D (P.step op x) :=
  rfl


structure ObserverExtension {X : Type u} {O : Type o} (base : X → O)
    (Oplus : Type o') where
  profile : X → Oplus
  forget : Oplus → O
  refines : ∀ x : X, forget (profile x) = base x
  declaredCost : Nat

inductive ThreeState where
  | source
  | target
  | spare
deriving DecidableEq, Repr

def baseProfile (_ : ThreeState) : Unit := ()

def refinementAProfile : ThreeState → Bool
  | .source => false
  | .target => true
  | .spare => false

def refinementBProfile : ThreeState → Bool
  | .source => false
  | .target => true
  | .spare => true

def forgetBool (_ : Bool) : Unit := ()

def refinementA : ObserverExtension baseProfile Bool where
  profile := refinementAProfile
  forget := forgetBool
  refines := by intro x; rfl
  declaredCost := 1

def refinementB : ObserverExtension baseProfile Bool where
  profile := refinementBProfile
  forget := forgetBool
  refines := by intro x; rfl
  declaredCost := 1

theorem refinement_profiles_not_related_by_postmap :
    ¬ ∃ f : Bool → Bool, ∀ x : ThreeState,
      f (refinementA.profile x) = refinementB.profile x := by
  intro h
  rcases h with ⟨f, hf⟩
  have hSource : f false = false := hf .source
  have hSpare : f false = true := hf .spare
  have hFalseTrue : false = true := hSource.symm.trans hSpare
  cases hFalseTrue

theorem nonunique_equalCost_extension_countermodel :
    refinementA.profile .source ≠ refinementA.profile .target ∧
      refinementB.profile .source ≠ refinementB.profile .target ∧
      refinementA.declaredCost = refinementB.declaredCost ∧
      ¬ ∃ f : Bool → Bool, ∀ x : ThreeState,
        f (refinementA.profile x) = refinementB.profile x := by
  refine ⟨?_, ?_, rfl, refinement_profiles_not_related_by_postmap⟩
  · intro h
    cases h
  · intro h
    cases h


structure ScopeFence where
  cochainClaims : Prop
  physicsClaims : Prop
  authorityClaims : Prop

def bridgeScope : ScopeFence where
  cochainClaims := False
  physicsClaims := False
  authorityClaims := False

theorem bridgeScope_hardFalse :
    ¬ bridgeScope.cochainClaims ∧
      ¬ bridgeScope.physicsClaims ∧
      ¬ bridgeScope.authorityClaims := by
  exact ⟨(fun h => h), (fun h => h), (fun h => h)⟩

#print axioms retainedDiff_zeroRel_protected_activeObstruction
#print axioms unprotected_collapse_countermodel
#print axioms Presentation.run_append
#print axioms SameLevelRepair.trans
#print axioms sameLevelRepair_replays_in_same_carrier_and_signature
#print axioms classifyTerminal_sameLevelRepair_iff
#print axioms classifyTerminal_conservativeExtensionProposal_iff
#print axioms classifyTerminal_typedRefusal_iff
#print axioms classifyTerminal_total
#print axioms classifyTerminal_exclusive
#print axioms ConservativeExtensionCertificate.carrierEmbed_injective
#print axioms ConservativeExtensionCertificate.signatureEmbed_injective
#print axioms ConservativeExtensionCertificate.embedded_zeroRel_refines
#print axioms ConservativeExtensionCertificate.embedded_nonzero_preserved
#print axioms demandOrbitRel_equivalence
#print axioms demandOrbit_step_congruent
#print axioms demandOrbitClass_eq_iff
#print axioms quotientTransition_carries_demandOrbitClass
#print axioms refinement_profiles_not_related_by_postmap
#print axioms nonunique_equalCost_extension_countermodel
#print axioms bridgeScope_hardFalse

end RetainedProfileCECBridge

private def l5aProvenance : String :=
  "Origin: lean4/RetainedProfileCecBridge.lean Claim: retainedDiff_zeroRel_protected_activeObstruction AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
