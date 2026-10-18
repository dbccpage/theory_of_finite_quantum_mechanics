
import PhaseBlindPresentation

namespace SuperpositionQuotientFiber

def phaseRel {Q : Type} (u v : Vec GaussInt Q) : Prop :=
  ∀ q : Q, phaseBlind u q = phaseBlind v q

theorem phaseRel_refl {Q : Type} (v : Vec GaussInt Q) : phaseRel v v :=
  fun _ => rfl

theorem phaseRel_symm {Q : Type} {u v : Vec GaussInt Q} (h : phaseRel u v) : phaseRel v u :=
  fun q => (h q).symm

theorem phaseRel_trans {Q : Type} {u v w : Vec GaussInt Q} (h1 : phaseRel u v) (h2 : phaseRel v w) : phaseRel u w :=
  fun q => (h1 q).trans (h2 q)

def phaseSetoid (Q : Type) : Setoid (Vec GaussInt Q) where
  r := phaseRel
  iseqv := {
    refl := phaseRel_refl
    symm := phaseRel_symm
    trans := phaseRel_trans
  }

def SuperpositionQuotient (Q : Type) := Quotient (phaseSetoid Q)

def toQuotient {Q : Type} (v : Vec GaussInt Q) : SuperpositionQuotient Q :=
  Quotient.mk (phaseSetoid Q) v

def toBaseWeights {Q : Type} : SuperpositionQuotient Q → (Q → Int) :=
  Quotient.lift phaseBlind (fun _ _ h => funext (fun q => h q))

theorem toBaseWeights_comm {Q : Type} (v : Vec GaussInt Q) :
    toBaseWeights (toQuotient v) = phaseBlind v :=
  rfl

def Fiber {Q : Type} (w : Q → Int) := { v : Vec GaussInt Q // phaseBlind v = w }

def psi1 : Vec GaussInt Bool := fun _ => GaussInt.one
def psi2 : Vec GaussInt Bool := fun q => if q then GaussInt.neg GaussInt.one else GaussInt.one

theorem psi1_psi2_in_same_fiber : phaseRel psi1 psi2 := by
  intro q
  cases q <;> rfl

theorem psi1_psi2_distinct : psi1 ≠ psi2 := by
  intro h
  have h_val := congrFun h true
  revert h_val
  decide

theorem fiber_exceeds_global_gauge_orbit :
    ¬ ∃ (u : GaussInt), ∀ q : Bool, psi2 q = GaussInt.mul u (psi1 q) := by
  intro ⟨u, hu⟩
  have h_false := hu false
  have h_true := hu true
  dsimp [psi1, psi2, GaussInt.one, GaussInt.neg, GaussInt.mul] at h_false h_true
  injection h_false with hr1 _
  injection h_true with hr2 _
  simp only [Int.mul_zero, Int.sub_zero, Int.mul_one] at hr1 hr2
  omega

end SuperpositionQuotientFiber

private def l5aProvenance : String :=
  "Origin: lean4/QuotientFiber.lean Claim: phaseRel_refl AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
