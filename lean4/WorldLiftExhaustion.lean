
import WorldPresentation



namespace OmegaWorld

def Exhausted {State Move : Type} (score : State -> Nat)
    (applyMove : Move -> State -> State) (moves : List Move) (state : State) : Prop :=
  forall move, move ∈ moves -> score state ≤ score (applyMove move state)

theorem not_exhausted_of_improving {State Move : Type}
    (score : State -> Nat) (applyMove : Move -> State -> State)
    (moves : List Move) (state : State) (move : Move)
    (member : move ∈ moves)
    (improves : score (applyMove move state) < score state) :
    Not (Exhausted score applyMove moves state) := by
  intro exhausted
  have noDecrease := exhausted move member
  exact (Nat.not_lt_of_ge noDecrease) improves

structure ExhaustionReceipt (State Move : Type) where
  score : State -> Nat
  applyMove : Move -> State -> State
  moveUniverse : List Move
  state : State
  replay : forall move, move ∈ moveUniverse ->
    score state ≤ score (applyMove move state)

namespace ExhaustionReceipt

theorem exhausted {State Move : Type} (receipt : ExhaustionReceipt State Move) :
    Exhausted receipt.score receipt.applyMove receipt.moveUniverse receipt.state :=
  receipt.replay

end ExhaustionReceipt

inductive LiftRefusal where
  | missingExhaustion
  deriving DecidableEq

def requireExhaustion {State Move : Type}
    (receipt : Option (ExhaustionReceipt State Move)) :
    Except LiftRefusal (ExhaustionReceipt State Move) :=
  match receipt with
  | none => .error .missingExhaustion
  | some value => .ok value

theorem survivor_without_exhaustion_refuses {State Move : Type} :
    requireExhaustion (State := State) (Move := Move) none =
      .error .missingExhaustion := by
  rfl

structure VerifiedOneGeneratorLift (source target : Presentation) where
  generatorId : String
  generator_nonempty : generatorId ≠ ""
  encodeRepair : target.Repair -> Sum source.Repair Unit
  decodeRepair : Sum source.Repair Unit -> target.Repair
  encode_decode : forall repair, encodeRepair (decodeRepair repair) = repair
  decode_encode : forall repair, decodeRepair (encodeRepair repair) = repair
  generator : target.Repair
  generator_is_new : encodeRepair generator = Sum.inr ()
  exhaustion : ExhaustionReceipt (Fin source.carrierSize) source.Repair
  exhaustion_uses_source_repairs : exhaustion.applyMove = source.applyRepair
  stageAdjacent : target.stage = source.stage + 1
  embedding : Fin source.carrierSize -> Fin target.carrierSize
  downMap : Fin target.carrierSize -> Fin source.carrierSize
  roundTrip : forall x, downMap (embedding x) = x
  differenceEmbedding : Fin source.differenceSize -> Fin target.differenceSize
  preservesDelta : forall x y,
    target.primitive.δ (embedding x) (embedding y) =
      differenceEmbedding (source.primitive.δ x y)
  preservesZero : forall residual,
    source.primitive.Zero residual ↔
      target.primitive.Zero (differenceEmbedding residual)
  SourceJudgment : Fin source.carrierSize -> Prop
  TargetJudgment : Fin target.carrierSize -> Prop
  preservesJudgment : forall x,
    SourceJudgment x ↔ TargetJudgment (embedding x)
  resolvesSurvivor : Prop
  resolutionWitness : resolvesSurvivor
  removalRestoresSurvivor : Prop
  minimalityWitness : removalRestoresSurvivor
  authorityEffect : AuthorityEffect
  authority_none : authorityEffect = .none

namespace VerifiedOneGeneratorLift

theorem has_exhaustion {source target : Presentation}
    (lift : VerifiedOneGeneratorLift source target) :
    Exhausted lift.exhaustion.score lift.exhaustion.applyMove
      lift.exhaustion.moveUniverse lift.exhaustion.state :=
  lift.exhaustion.exhausted

theorem old_judgments_are_conservative
    {source target : Presentation}
    (lift : VerifiedOneGeneratorLift source target)
    (x : Fin source.carrierSize) :
    lift.SourceJudgment x ↔ lift.TargetJudgment (lift.embedding x) :=
  lift.preservesJudgment x

theorem generator_is_minimal
    {source target : Presentation}
    (lift : VerifiedOneGeneratorLift source target) :
    lift.removalRestoresSurvivor :=
  lift.minimalityWitness

theorem authority_is_none
    {source target : Presentation}
    (lift : VerifiedOneGeneratorLift source target) :
    lift.authorityEffect = .none :=
  lift.authority_none

theorem preserves_zero_rel
    {source target : Presentation}
    (lift : VerifiedOneGeneratorLift source target)
    (x y : Fin source.carrierSize) :
    source.primitive.ZeroRel x y ↔
      target.primitive.ZeroRel (lift.embedding x) (lift.embedding y) := by
  change source.primitive.Zero (source.primitive.δ x y) ↔
    target.primitive.Zero (target.primitive.δ (lift.embedding x) (lift.embedding y))
  rw [lift.preservesDelta]
  exact lift.preservesZero (source.primitive.δ x y)

end VerifiedOneGeneratorLift
end OmegaWorld

private def l5aProvenance : String :=
  "Origin: lean4/WorldLiftExhaustion.lean Claim: not_exhausted_of_improving AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
