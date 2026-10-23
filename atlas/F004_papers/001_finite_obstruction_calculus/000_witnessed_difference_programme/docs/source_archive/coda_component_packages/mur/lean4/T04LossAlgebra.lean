import T03T04T05LossNoCreation

/-!
Lean 4 proof kernel for the abstract GTMUR-T04 loss-algebra law.

AuthorityEffect: None.

`GTMUR_T03_T04_T05_LossNoCreation.lean` proves a concrete finite Boolean
ledger. This file factors out the theorem actually used by the paper: any
declared loss algebra with associative accumulation, empty ledger units, and
pushforward laws has unital and associative composite loss accounting.
-/

namespace CODA_MUR

universe u

/-- Abstract loss-ledger algebra used by GTMUR-T04. -/
structure LossAlgebra (Loss : Type u) where
  empty : Loss
  sum : Loss -> Loss -> Loss
  sum_assoc : ∀ L M N, sum (sum L M) N = sum L (sum M N)
  empty_sum : ∀ L, sum empty L = L
  sum_empty : ∀ L, sum L empty = L

/-- Pushforward distributes over the declared loss accumulation law. -/
def GenericPushDistributes {Loss : Type u}
    (A : LossAlgebra Loss) (push : Loss -> Loss) : Prop :=
  ∀ L M, push (A.sum L M) = A.sum (push L) (push M)

/-- Pushforward preserves the declared empty ledger. -/
def GenericPushPreservesEmpty {Loss : Type u}
    (A : LossAlgebra Loss) (push : Loss -> Loss) : Prop :=
  push A.empty = A.empty

/-- Generic composite loss: push earlier loss into the codomain, then accumulate. -/
def genericComposeLoss {Loss : Type u}
    (A : LossAlgebra Loss)
    (push : Loss -> Loss)
    (lossF lossG : Loss) : Loss :=
  A.sum (push lossF) lossG

/-- GTMUR-T04 abstract composition formula. -/
theorem generic_loss_composition_formula {Loss : Type u}
    (A : LossAlgebra Loss)
    (push : Loss -> Loss)
    (lossF lossG : Loss) :
    genericComposeLoss A push lossF lossG = A.sum (push lossF) lossG :=
  rfl

/-- Left identity law for generic loss composition. -/
theorem generic_loss_identity_left {Loss : Type u}
    (A : LossAlgebra Loss)
    (push : Loss -> Loss)
    (hEmpty : GenericPushPreservesEmpty A push)
    (lossF : Loss) :
    genericComposeLoss A push A.empty lossF = lossF := by
  unfold genericComposeLoss
  unfold GenericPushPreservesEmpty at hEmpty
  rw [hEmpty]
  exact A.empty_sum lossF

/-- Right identity law for generic loss composition. -/
theorem generic_loss_identity_right {Loss : Type u}
    (A : LossAlgebra Loss)
    (lossF : Loss) :
    genericComposeLoss A (fun L => L) lossF A.empty = lossF := by
  unfold genericComposeLoss
  exact A.sum_empty lossF

/-- Associativity of three-step generic loss accumulation under declared push laws. -/
theorem generic_loss_chain_assoc {Loss : Type u}
    (A : LossAlgebra Loss)
    (pushH pushG pushHG : Loss -> Loss)
    (hComp : ∀ L, pushH (pushG L) = pushHG L)
    (hDistrib : GenericPushDistributes A pushH)
    (lossF lossG lossH : Loss) :
    genericComposeLoss A pushH (genericComposeLoss A pushG lossF lossG) lossH =
      A.sum (pushHG lossF) (A.sum (pushH lossG) lossH) := by
  unfold genericComposeLoss
  rw [hDistrib]
  rw [hComp]
  exact A.sum_assoc (pushHG lossF) (pushH lossG) lossH

/-- The finite Boolean ledger from the T03/T04/T05 file is an instance. -/
def booleanLossAlgebra : LossAlgebra LossLedger where
  empty := LossLedger.empty
  sum := LossLedger.sum
  sum_assoc := loss_sum_assoc
  empty_sum := loss_sum_left_unit
  sum_empty := loss_sum_right_unit

end CODA_MUR

#print axioms CODA_MUR.generic_loss_composition_formula
#print axioms CODA_MUR.generic_loss_identity_left
#print axioms CODA_MUR.generic_loss_identity_right
#print axioms CODA_MUR.generic_loss_chain_assoc
#print axioms CODA_MUR.booleanLossAlgebra
