/-
Provenance (NEW, NOT RECOVERED, 2026-10-21)
  This file is not part of the recovered folder
  C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\formal.
  It was written during recovery to test the audit finding that the recovered `GlobalLift`
  transport can be instantiated with Mathlib's computability library.
  module : AuthIncompleteness.MathlibBridge
  build  : checked with `lean` v4.35.0 against the Mathlib v4.35.0 build; NOT a lakefile root
           (the isolated recovery Lake environment carries no Mathlib build).
-/
import Mathlib.Computability.Halting
import AuthIncompleteness.GlobalLift

/-!
# Instantiating the class-relative transport with Mathlib computability

`NoTotalDecider allowed predicate` is relative to an arbitrary class `allowed`. Taking
`allowed := Computable` and the predicate "program `c` halts on input `n`" yields exactly
Mathlib's `ComputablePred.halting_problem`. The transport theorem of the recovered
`GlobalLift` module then pushes that no-decider fact along any reduction closed under the
chosen class.

AuthorityEffect: None.
-/

namespace AuthorizationIncompleteness.MathlibBridge

open AuthorizationIncompleteness.GlobalComputabilityLift Nat.Partrec

/-- The halting predicate has no computable total Boolean decider (Mathlib's halting problem,
restated in the recovered `NoTotalDecider` vocabulary). -/
theorem halting_has_no_computable_decider (n : Nat) :
    NoTotalDecider (fun d : Code → Bool => Computable d) (fun c : Code => (Code.eval c n).Dom) := by
  rintro ⟨d, hd, hdecides⟩
  apply ComputablePred.halting_problem n
  rw [ComputablePred.computable_iff]
  refine ⟨d, hd, ?_⟩
  funext c
  exact propext (hdecides c).symm

/-- Computable proposal authorizers pull back along a computable reduction map. -/
theorem computable_closed_under_computable_reduction {H P : Type} [Primcodable H] [Primcodable P]
    {hard : H → Prop} {valid : P → Prop} (reduction : ValidityReduction hard valid)
    (hmap : Computable reduction.map) :
    ClosedUnderReduction (fun d : H → Bool => Computable d) (fun a : P → Bool => Computable a)
      reduction :=
  fun _ hauth => hauth.comp hmap

/-- The recovered transport with `Computable` on both sides: if the source predicate has no
computable total decider and the reduction map is computable, neither does proposal validity. -/
theorem no_computable_authorizer_of_computable_reduction {H P : Type} [Primcodable H]
    [Primcodable P] {hard : H → Prop} {valid : P → Prop} (reduction : ValidityReduction hard valid)
    (hmap : Computable reduction.map)
    (noSourceDecider : NoTotalDecider (fun d : H → Bool => Computable d) hard) :
    NoTotalDecider (fun a : P → Bool => Computable a) valid :=
  no_source_decider_blocks_total_authorizer reduction
    (computable_closed_under_computable_reduction reduction hmap) noSourceDecider

/-- The identity reduction from halting to itself, used to exercise the transport theorem. -/
def haltingIdentityReduction (n : Nat) :
    ValidityReduction (fun c : Code => (Code.eval c n).Dom) (fun c : Code => (Code.eval c n).Dom) where
  map := id
  preserves := fun _ => Iff.rfl

/-- Halting pulled back along the identity reduction, through the instantiated transport. -/
theorem halting_transport_instance (n : Nat) :
    NoTotalDecider (fun d : Code → Bool => Computable d) (fun c : Code => (Code.eval c n).Dom) :=
  no_computable_authorizer_of_computable_reduction (haltingIdentityReduction n) Computable.id
    (halting_has_no_computable_decider n)

end AuthorizationIncompleteness.MathlibBridge

#print axioms AuthorizationIncompleteness.MathlibBridge.halting_has_no_computable_decider
#print axioms AuthorizationIncompleteness.MathlibBridge.computable_closed_under_computable_reduction
#print axioms AuthorizationIncompleteness.MathlibBridge.no_computable_authorizer_of_computable_reduction
#print axioms AuthorizationIncompleteness.MathlibBridge.halting_transport_instance
