import Cochain

/-! Chain homotopies induce equal homology homomorphisms. Consequently a chain
map split up to homotopy is still injective on homology. These results concern
the same actual kernel/image quotients as the strict retraction theorem. -/
namespace PreMssn.ChainHomotopy
open Homology
open Lean.Grind AddCommMonoid AddCommGroup
universe u

def identity (C : Complex.{u}) : Morphism C C where
  upper := AddHom.identity _
  middle := AddHom.identity _
  lower := AddHom.identity _
  boundary_commutes _ := rfl
  differential_commutes _ := rfl

def compose {C D E : Complex.{u}} (g : Morphism D E) (f : Morphism C D) : Morphism C E where
  upper := g.upper.comp f.upper
  middle := g.middle.comp f.middle
  lower := g.lower.comp f.lower
  boundary_commutes a := by
    change g.middle (f.middle (C.boundary a)) = E.boundary (g.upper (f.upper a))
    rw [f.boundary_commutes, g.boundary_commutes]
  differential_commutes a := by
    change g.lower (f.lower (C.differential a)) = E.differential (g.middle (f.middle a))
    rw [f.differential_commutes, g.differential_commutes]

theorem homology_identity (C : Complex.{u}) (q : Homology C) : homologyMap (identity C) q = q := by
  induction q using Quotient.inductionOn with
  | _ z => rfl

theorem homology_compose {C D E : Complex.{u}} (g : Morphism D E) (f : Morphism C D)
    (q : Homology C) : homologyMap (compose g f) q = homologyMap g (homologyMap f q) := by
  induction q using Quotient.inductionOn with
  | _ z => rfl

structure Homotopy {C D : Complex.{u}} (f g : Morphism C D) where
  raiseMiddle : AddHom C.middle D.upper
  raiseLower : AddHom C.lower D.middle
  equation : ∀ a, f.middle a =
    g.middle a + D.boundary (raiseMiddle a) + raiseLower (C.differential a)

/-- The boundary term is exactly a witness for equality in quotient homology. -/
theorem homotopy_induces_equal_maps {C D : Complex.{u}} {f g : Morphism C D}
    (h : Homotopy f g) (q : Homology C) : homologyMap f q = homologyMap g q := by
  induction q using Quotient.inductionOn with
  | _ z =>
    apply Quotient.sound
    refine ⟨h.raiseMiddle z.val, ?_⟩
    apply Subtype.ext
    change f.middle z.val = g.middle z.val + D.boundary (h.raiseMiddle z.val)
    have hz := h.equation z.val
    rw [z.property, h.raiseLower.map_zero, add_zero] at hz
    exact hz

theorem homotopy_retraction {C D : Complex.{u}} (i : Morphism C D) (r : Morphism D C)
    (h : Homotopy (compose r i) (identity C)) (q : Homology C) :
    homologyMap r (homologyMap i q) = q := by
  rw [← homology_compose, homotopy_induces_equal_maps h, homology_identity]

theorem homotopy_retraction_injective {C D : Complex.{u}}
    (i : Morphism C D) (r : Morphism D C)
    (h : Homotopy (compose r i) (identity C)) (x y : Homology C)
    (same : homologyMap i x = homologyMap i y) : x=y := by
  have back := congrArg (homologyMap r) same
  simpa only [homotopy_retraction i r h] using back

theorem triangle_has_no_homotopy_retraction :
    ¬∃ r : Morphism TriangleHomology.filledComplex TriangleHomology.unfilledComplex,
      Nonempty (Homotopy (compose r TriangleHomology.attachment)
        (identity TriangleHomology.unfilledComplex)) := by
  rintro ⟨r,⟨h⟩⟩
  apply TriangleHomology.unfilled_generator_nonzero
  apply homotopy_retraction_injective TriangleHomology.attachment r h
  rw [TriangleHomology.attachment_kills_h1, (homologyMap TriangleHomology.attachment).map_zero]

end PreMssn.ChainHomotopy
