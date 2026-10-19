import Core

/- New minimal implementation, 2026-10-19. Supplies the interface imported by
   H000FinitePresentedCarrier; this is not a recovered historical source file.
   The report map is an input. AuthorityEffect: None. -/
namespace GrokPdNight20260814.E003
open GrokPdNight20260814.Core

def fiberPD {X Q : Type} (pres : X → Q) : PrimitiveDifference X (Q × Q) where
  δ := fun x y => (pres x,pres y)
  Zero := fun p => p.1=p.2
  zero_refl := fun _ => rfl
  zero_symm := fun _ _ h => h.symm
  zero_trans := fun _ _ _ h k => h.trans k

theorem fiberPD_zeroRel_iff {X Q : Type} (pres : X → Q) (x y : X) :
    ZeroRel (fiberPD pres) x y ↔ pres x=pres y := Iff.rfl

def fstBool (p : Bool × Bool) : Bool := p.1
#print axioms fiberPD_zeroRel_iff
end GrokPdNight20260814.E003
