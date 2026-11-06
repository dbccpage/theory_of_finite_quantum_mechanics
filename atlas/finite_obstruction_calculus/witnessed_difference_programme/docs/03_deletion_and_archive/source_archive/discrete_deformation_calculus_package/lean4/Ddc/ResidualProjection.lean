/-
Letter R: residual projection keeps Φ₁, Γ₂ and the carrier. AuthorityEffect: None.
-/
import Ddc.ExactRepair

namespace Ddc

/-- DDC-R: R keeps the carrier and both diagnostics. -/
theorem R_keeps_diagnostics (b a : State) (w : Witness) (h : stepLaw .R b a w = true) :
    a.carrier = b.carrier ∧ a.phi = b.phi ∧ a.gamma = b.gamma := by
  obtain ⟨hc, hp, hg, -⟩ := law_R.1 h
  exact ⟨hc.symm, hp, hg⟩

/-- R keeps the class. -/
theorem R_keeps_class (b a : State) (w : Witness) (h : stepLaw .R b a w = true) : a.cls = b.cls := by
  obtain ⟨-, hp, hg⟩ := R_keeps_diagnostics b a w h
  simp [State.cls, hp, hg]

/-- The canonical R move is a gauge move, so it satisfies R's law on the cochain level:
the face defect and exactness are unchanged. -/
theorem R_gauge_move_is_lawful (K : Complex) (x φ : Nat → Int) :
    K.d1 (gaugeMove K x φ) = K.d1 x ∧ (IsExact K (gaugeMove K x φ) ↔ IsExact K x) :=
  ⟨E_gauge_preserves_closure K x φ, E_gauge_preserves_exactness K x φ⟩

end Ddc
