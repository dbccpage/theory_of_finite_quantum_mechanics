/-!
# CODA-MUR: Certified Representation Transport Records (D01, D02, D03)

**AuthorityEffect:** None.

Defines:
1. `MorphismKind`: Exact, quotient, embedding, approximation, unmeasured
2. `LossRequired`: Predicate indicating when representation change demands loss accounting
3. `LossLedger`: Finite Boolean loss ledger (e, i, a, u) with associative monoidal accumulation
4. `DescentSquareCertificate`: Commuting descent square certificates
-/

namespace CODA_MUR

inductive MorphismKind where
  | exact
  | quotient
  | embedding
  | approximation
  | unmeasured
  deriving DecidableEq, Repr

def LossRequired : MorphismKind -> Prop
  | MorphismKind.quotient => True
  | MorphismKind.approximation => True
  | MorphismKind.unmeasured => True
  | _ => False

theorem quotient_loss_required : LossRequired MorphismKind.quotient := by
  trivial

structure LossLedger where
  e : Bool := false
  i : Bool := false
  a : Bool := false
  u : Bool := false
  deriving DecidableEq, Repr

namespace LossLedger

def empty : LossLedger :=
  ⟨false, false, false, false⟩

def sum (L M : LossLedger) : LossLedger :=
  ⟨L.e || M.e, L.i || M.i, L.a || M.a, L.u || M.u⟩

end LossLedger

/-- Exact D03 commuting descent square certificate. -/
structure DescentSquareCertificate
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    (F : RepA -> RepB) (barF : CoreA -> CoreB)
    (D_A : RepA -> CoreA) (D_B : RepB -> CoreB) : Prop where
  commutes : ∀ x : RepA, D_B (F x) = barF (D_A x)

/-- Certified representation morphism record (GTMUR-D02). -/
structure CertifiedMorphismRecord where
  kind : MorphismKind
  lossDefined : Prop
  chiExists : Prop
  lossLedger : Option LossLedger := none

/-- Representation transport certificate structure (GTMUR-D01). -/
structure RepresentationTransportCertificate where
  source : String
  target : String
  chiCertified : Bool
  lossRecorded : Bool

end CODA_MUR
