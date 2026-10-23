import D01D02D03Records
import L01FiniteCoreAction

/-!
Lean 4 proof kernel for the L01/live-core case of GTMUR-T01.

AuthorityEffect: None.

For finite-core actions induced in the GTMUR-L01 sense, the descent-square
certificate is the `spec` field of `FiniteCoreAction`. Pasting two such
certificates is exactly the `spec` field of the composite action constructed by
`FiniteCoreAction.comp`.

This mechanizes the pointwise certificate-pasting law for live-core actions.
It also mechanizes the generic exact commuting-square pasting law for D03
descent-square certificates.
The full bicategorical coherence of arbitrary certified 2-cells remains the
GTMUR-T02 coherence-data problem.
-/

namespace CODA_MUR

universe uA uB uC vA vB vC

/-- The pointwise pasted certificate for L01-induced finite-core actions. -/
def PastedCertificate
    {RepA : Type uA} {RepB : Type uB} {RepC : Type uC}
    {CoreA : Type vA} {CoreB : Type vB} {CoreC : Type vC}
    {D_A : RepA -> Option CoreA}
    {D_B : RepB -> Option CoreB}
    {D_C : RepC -> Option CoreC}
    {F : RepA -> RepB} {G : RepB -> RepC}
    (FAction : FiniteCoreAction D_A D_B F)
    (GAction : FiniteCoreAction D_B D_C G) : Prop :=
  ∀ x cA, (hx : D_A x = some cA) ->
    D_C (G (F x)) =
      some ((GAction.comp FAction).act ⟨cA, ⟨x, hx⟩⟩)

/-- GTMUR-T01, exact D03 form: commuting descent-square certificates paste. -/
theorem descentSquareCertificate_paste
    {RepA : Type uA} {RepB : Type uB} {RepC : Type uC}
    {CoreA : Type vA} {CoreB : Type vB} {CoreC : Type vC}
    {D_A : RepA -> CoreA}
    {D_B : RepB -> CoreB}
    {D_C : RepC -> CoreC}
    {F : RepA -> RepB} {G : RepB -> RepC}
    {barF : CoreA -> CoreB} {barG : CoreB -> CoreC}
    (chiF : DescentSquareCertificate F barF D_A D_B)
    (chiG : DescentSquareCertificate G barG D_B D_C) :
    DescentSquareCertificate
      (fun x => G (F x))
      (fun c => barG (barF c))
      D_A
      D_C := by
  constructor
  intro x
  calc
    D_C (G (F x)) = barG (D_B (F x)) := chiG.commutes (F x)
    _ = barG (barF (D_A x)) := by rw [chiF.commutes x]

/-- GTMUR-T01, L01/live-core form: induced certificates paste pointwise. -/
theorem certificate_pasting_from_induced_actions
    {RepA : Type uA} {RepB : Type uB} {RepC : Type uC}
    {CoreA : Type vA} {CoreB : Type vB} {CoreC : Type vC}
    {D_A : RepA -> Option CoreA}
    {D_B : RepB -> Option CoreB}
    {D_C : RepC -> Option CoreC}
    {F : RepA -> RepB} {G : RepB -> RepC}
    (FAction : FiniteCoreAction D_A D_B F)
    (GAction : FiniteCoreAction D_B D_C G) :
    PastedCertificate FAction GAction := by
  intro x cA hx
  exact (GAction.comp FAction).spec x cA hx

/--
Any separately supplied composite certificate agrees, on its finite-core action,
with the pasted certificate derived from the two component certificates.
-/
theorem certificate_pasting_agrees_with_composite_action
    {RepA : Type uA} {RepB : Type uB} {RepC : Type uC}
    {CoreA : Type vA} {CoreB : Type vB} {CoreC : Type vC}
    {D_A : RepA -> Option CoreA}
    {D_B : RepB -> Option CoreB}
    {D_C : RepC -> Option CoreC}
    {F : RepA -> RepB} {G : RepB -> RepC}
    (FAction : FiniteCoreAction D_A D_B F)
    (GAction : FiniteCoreAction D_B D_C G)
    (GFAction : FiniteCoreAction D_A D_C (fun x => G (F x))) :
    GFAction.act = (GAction.comp FAction).act :=
  finiteCoreAction_functoriality FAction GAction GFAction

end CODA_MUR

#print axioms CODA_MUR.certificate_pasting_from_induced_actions
#print axioms CODA_MUR.certificate_pasting_agrees_with_composite_action
#print axioms CODA_MUR.descentSquareCertificate_paste
