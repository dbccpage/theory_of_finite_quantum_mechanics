import E003_projection_fiber_primitive_difference

/- New minimal implementation, 2026-10-19. Proves the supplied report-map kernel
   is a setoid; no field or Hilbert structure is inferred. AuthorityEffect: None. -/
namespace GrokPdNight20260814.E005
def fiberSetoid {X Q : Type} (pres : X → Q) : Setoid X where
  r := fun x y => pres x=pres y
  iseqv := ⟨fun _ => rfl,fun h => h.symm,fun h k => h.trans k⟩

theorem quotient_eq_iff_report_eq {X Q : Type} (pres : X → Q) (x y : X) :
    Quotient.mk (fiberSetoid pres) x=Quotient.mk (fiberSetoid pres) y ↔ pres x=pres y := by
  constructor
  · intro h; exact Quotient.exact h
  · intro h; apply Quotient.sound; exact h
#print axioms quotient_eq_iff_report_eq
end GrokPdNight20260814.E005
