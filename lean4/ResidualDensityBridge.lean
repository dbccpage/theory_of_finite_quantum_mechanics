
import PrimitiveDifference





namespace QM

namespace ResidualDensityBridge

universe u v w z

def QuotientCompatible {Alpha : Type u} {Beta : Type v} {Rho : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta) (lift : Alpha -> Rho) : Prop :=
  P.InvariantCongruent lift

def FactorsThroughResidual {Alpha : Type u} {Beta : Type v} {Rho : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta) (lift : Alpha -> Rho) : Prop :=
  ∃ F : P.ResidualQuotient -> Rho, ∀ x : Alpha, F (P.classOf x) = lift x

def QuotientCompatibleMod {Alpha : Type u} {Beta : Type v} {Rho : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta) (lift : Alpha -> Rho)
    (RhoSetoid : Setoid Rho) : Prop :=
  P.InvariantCongruentMod lift RhoSetoid

def FactorsThroughResidualMod {Alpha : Type u} {Beta : Type v} {Rho : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta) (lift : Alpha -> Rho)
    (RhoSetoid : Setoid Rho) : Prop :=
  ∃ F : P.ResidualQuotient -> Quotient RhoSetoid,
    ∀ x : Alpha, F (P.classOf x) = Quotient.mk RhoSetoid (lift x)

theorem quotientCompatible_iff_factorsThroughResidual
    {Alpha : Type u} {Beta : Type v} {Rho : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta) (lift : Alpha -> Rho) :
    FactorsThroughResidual P lift ↔ QuotientCompatible P lift := by
  exact
    ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      P lift

theorem quotientCompatibleMod_iff_factorsThroughResidualMod
    {Alpha : Type u} {Beta : Type v} {Rho : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta) (lift : Alpha -> Rho)
    (RhoSetoid : Setoid Rho) :
    FactorsThroughResidualMod P lift RhoSetoid ↔
      QuotientCompatibleMod P lift RhoSetoid := by
  exact
    ObstructionCore.PrimitiveDifference.invariantFactorMod_exists_iff_invariantCongruentMod
      P lift RhoSetoid

theorem quotientCompatibleMod_preserved_by_coarser_output
    {Alpha : Type u} {Beta : Type v} {Rho : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta) (lift : Alpha -> Rho)
    (FineSetoid : Setoid Rho) (CoarseSetoid : Setoid Rho)
    (hFineToCoarse :
      ∀ x y : Rho, FineSetoid.r x y -> CoarseSetoid.r x y)
    (hLift : QuotientCompatibleMod P lift FineSetoid) :
    QuotientCompatibleMod P lift CoarseSetoid := by
  exact
    ObstructionCore.PrimitiveDifference.invariantCongruentMod_of_setoid_imp
      P lift FineSetoid CoarseSetoid hFineToCoarse hLift

theorem factorsThroughResidualMod_preserved_by_coarser_output
    {Alpha : Type u} {Beta : Type v} {Rho : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta) (lift : Alpha -> Rho)
    (FineSetoid : Setoid Rho) (CoarseSetoid : Setoid Rho)
    (hFineToCoarse :
      ∀ x y : Rho, FineSetoid.r x y -> CoarseSetoid.r x y)
    (hDescends : FactorsThroughResidualMod P lift FineSetoid) :
    FactorsThroughResidualMod P lift CoarseSetoid := by
  exact
    ObstructionCore.PrimitiveDifference.invariantFactorMod_exists_of_setoid_imp
      P lift FineSetoid CoarseSetoid hFineToCoarse hDescends

theorem quotientCompatible_pair
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (hLeft : QuotientCompatible P left)
    (hRight : QuotientCompatible P right) :
    QuotientCompatible P (fun x : Alpha => (left x, right x)) := by
  exact
    (ObstructionCore.PrimitiveDifference.invariantCongruent_pair_iff
      P left right).mpr ⟨hLeft, hRight⟩

theorem factorsThroughResidual_pair
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (hLeft : FactorsThroughResidual P left)
    (hRight : FactorsThroughResidual P right) :
    FactorsThroughResidual P (fun x : Alpha => (left x, right x)) := by
  have hLeftCompat : QuotientCompatible P left :=
    (quotientCompatible_iff_factorsThroughResidual P left).mp hLeft
  have hRightCompat : QuotientCompatible P right :=
    (quotientCompatible_iff_factorsThroughResidual P right).mp hRight
  exact
    (quotientCompatible_iff_factorsThroughResidual
      P (fun x : Alpha => (left x, right x))).mpr
      (quotientCompatible_pair P left right hLeftCompat hRightCompat)

theorem factorsThroughResidual_pair_iff_component_factors
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma) :
    FactorsThroughResidual P (fun x : Alpha => (left x, right x)) ↔
      FactorsThroughResidual P left ∧ FactorsThroughResidual P right := by
  exact
    ObstructionCore.PrimitiveDifference.invariantFactor_pair_exists_iff_component_factors
      P left right

theorem pair_no_factor_of_left_not_factor
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (hLeft : ¬ FactorsThroughResidual P left) :
    ¬ FactorsThroughResidual P (fun x : Alpha => (left x, right x)) := by
  intro hPair
  exact hLeft ((factorsThroughResidual_pair_iff_component_factors
    P left right).mp hPair).1

theorem pair_no_factor_of_right_not_factor
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (hRight : ¬ FactorsThroughResidual P right) :
    ¬ FactorsThroughResidual P (fun x : Alpha => (left x, right x)) := by
  intro hPair
  exact hRight ((factorsThroughResidual_pair_iff_component_factors
    P left right).mp hPair).2
theorem factorsThroughResidual_triple_iff_component_factors
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Tau : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (middle : Alpha -> Sigma) (right : Alpha -> Tau) :
    FactorsThroughResidual P
        (fun x : Alpha => ((left x, middle x), right x)) ↔
      FactorsThroughResidual P left ∧
        FactorsThroughResidual P middle ∧
        FactorsThroughResidual P right := by
  constructor
  · intro hTriple
    have hPairRight :
        FactorsThroughResidual P (fun x : Alpha => (left x, middle x)) ∧
          FactorsThroughResidual P right :=
      (factorsThroughResidual_pair_iff_component_factors
        P (fun x : Alpha => (left x, middle x)) right).mp hTriple
    have hLeftMiddle :
        FactorsThroughResidual P left ∧ FactorsThroughResidual P middle :=
      (factorsThroughResidual_pair_iff_component_factors
        P left middle).mp hPairRight.1
    exact ⟨hLeftMiddle.1, hLeftMiddle.2, hPairRight.2⟩
  · intro hComponents
    exact
      factorsThroughResidual_pair
        P (fun x : Alpha => (left x, middle x)) right
        (factorsThroughResidual_pair
          P left middle hComponents.1 hComponents.2.1)
        hComponents.2.2

theorem triple_no_factor_of_left_not_factor
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Tau : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (middle : Alpha -> Sigma) (right : Alpha -> Tau)
    (hLeft : ¬ FactorsThroughResidual P left) :
    ¬ FactorsThroughResidual P
      (fun x : Alpha => ((left x, middle x), right x)) := by
  intro hTriple
  exact hLeft ((factorsThroughResidual_triple_iff_component_factors
    P left middle right).mp hTriple).1

theorem triple_no_factor_of_middle_not_factor
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Tau : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (middle : Alpha -> Sigma) (right : Alpha -> Tau)
    (hMiddle : ¬ FactorsThroughResidual P middle) :
    ¬ FactorsThroughResidual P
      (fun x : Alpha => ((left x, middle x), right x)) := by
  intro hTriple
  exact hMiddle ((factorsThroughResidual_triple_iff_component_factors
    P left middle right).mp hTriple).2.1

theorem triple_no_factor_of_right_not_factor
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Tau : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (middle : Alpha -> Sigma) (right : Alpha -> Tau)
    (hRight : ¬ FactorsThroughResidual P right) :
    ¬ FactorsThroughResidual P
      (fun x : Alpha => ((left x, middle x), right x)) := by
  intro hTriple
  exact hRight ((factorsThroughResidual_triple_iff_component_factors
    P left middle right).mp hTriple).2.2

theorem quotientCompatibleMod_pair
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (LeftSetoid : Setoid Rho) (RightSetoid : Setoid Sigma)
    (hLeft : QuotientCompatibleMod P left LeftSetoid)
    (hRight : QuotientCompatibleMod P right RightSetoid) :
    QuotientCompatibleMod P (fun x : Alpha => (left x, right x))
      (ObstructionCore.PrimitiveDifference.productSetoid LeftSetoid RightSetoid) := by
  exact
    (ObstructionCore.PrimitiveDifference.invariantCongruentMod_pair_iff
      P left right LeftSetoid RightSetoid).mpr ⟨hLeft, hRight⟩

theorem factorsThroughResidualMod_pair
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (LeftSetoid : Setoid Rho) (RightSetoid : Setoid Sigma)
    (hLeft : FactorsThroughResidualMod P left LeftSetoid)
    (hRight : FactorsThroughResidualMod P right RightSetoid) :
    FactorsThroughResidualMod P (fun x : Alpha => (left x, right x))
      (ObstructionCore.PrimitiveDifference.productSetoid LeftSetoid RightSetoid) := by
  have hLeftCompat : QuotientCompatibleMod P left LeftSetoid :=
    (quotientCompatibleMod_iff_factorsThroughResidualMod
      P left LeftSetoid).mp hLeft
  have hRightCompat : QuotientCompatibleMod P right RightSetoid :=
    (quotientCompatibleMod_iff_factorsThroughResidualMod
      P right RightSetoid).mp hRight
  exact
    (quotientCompatibleMod_iff_factorsThroughResidualMod
      P (fun x : Alpha => (left x, right x))
        (ObstructionCore.PrimitiveDifference.productSetoid
          LeftSetoid RightSetoid)).mpr
      (quotientCompatibleMod_pair
        P left right LeftSetoid RightSetoid hLeftCompat hRightCompat)
theorem factorsThroughResidualMod_pair_iff_component_factors
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (LeftSetoid : Setoid Rho) (RightSetoid : Setoid Sigma) :
    FactorsThroughResidualMod P (fun x : Alpha => (left x, right x))
      (ObstructionCore.PrimitiveDifference.productSetoid LeftSetoid RightSetoid) ↔
      FactorsThroughResidualMod P left LeftSetoid ∧
      FactorsThroughResidualMod P right RightSetoid := by
  exact
    ObstructionCore.PrimitiveDifference.invariantFactorMod_pair_exists_iff_component_factors
      P left right LeftSetoid RightSetoid

theorem pair_mod_no_factor_of_left_not_factor
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (LeftSetoid : Setoid Rho) (RightSetoid : Setoid Sigma)
    (hLeft : ¬ FactorsThroughResidualMod P left LeftSetoid) :
    ¬ FactorsThroughResidualMod P (fun x : Alpha => (left x, right x))
      (ObstructionCore.PrimitiveDifference.productSetoid LeftSetoid RightSetoid) := by
  intro hPair
  exact hLeft ((factorsThroughResidualMod_pair_iff_component_factors
    P left right LeftSetoid RightSetoid).mp hPair).1

theorem pair_mod_no_factor_of_right_not_factor
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (LeftSetoid : Setoid Rho) (RightSetoid : Setoid Sigma)
    (hRight : ¬ FactorsThroughResidualMod P right RightSetoid) :
    ¬ FactorsThroughResidualMod P (fun x : Alpha => (left x, right x))
      (ObstructionCore.PrimitiveDifference.productSetoid LeftSetoid RightSetoid) := by
  intro hPair
  exact hRight ((factorsThroughResidualMod_pair_iff_component_factors
    P left right LeftSetoid RightSetoid).mp hPair).2
theorem factorsThroughResidualMod_triple_iff_component_factors
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Tau : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (middle : Alpha -> Sigma) (right : Alpha -> Tau)
    (LeftSetoid : Setoid Rho) (MiddleSetoid : Setoid Sigma)
    (RightSetoid : Setoid Tau) :
    FactorsThroughResidualMod P
      (fun x : Alpha => ((left x, middle x), right x))
      (ObstructionCore.PrimitiveDifference.productSetoid
        (ObstructionCore.PrimitiveDifference.productSetoid
          LeftSetoid MiddleSetoid)
        RightSetoid) ↔
      FactorsThroughResidualMod P left LeftSetoid ∧
        FactorsThroughResidualMod P middle MiddleSetoid ∧
        FactorsThroughResidualMod P right RightSetoid := by
  constructor
  · intro hTriple
    have hPairRight :
        FactorsThroughResidualMod P (fun x : Alpha => (left x, middle x))
            (ObstructionCore.PrimitiveDifference.productSetoid
              LeftSetoid MiddleSetoid) ∧
          FactorsThroughResidualMod P right RightSetoid :=
      (factorsThroughResidualMod_pair_iff_component_factors
        P (fun x : Alpha => (left x, middle x)) right
        (ObstructionCore.PrimitiveDifference.productSetoid
          LeftSetoid MiddleSetoid)
        RightSetoid).mp hTriple
    have hLeftMiddle :
        FactorsThroughResidualMod P left LeftSetoid ∧
          FactorsThroughResidualMod P middle MiddleSetoid :=
      (factorsThroughResidualMod_pair_iff_component_factors
        P left middle LeftSetoid MiddleSetoid).mp hPairRight.1
    exact ⟨hLeftMiddle.1, hLeftMiddle.2, hPairRight.2⟩
  · intro hComponents
    exact
      factorsThroughResidualMod_pair
        P (fun x : Alpha => (left x, middle x)) right
        (ObstructionCore.PrimitiveDifference.productSetoid
          LeftSetoid MiddleSetoid)
        RightSetoid
        (factorsThroughResidualMod_pair
          P left middle LeftSetoid MiddleSetoid
          hComponents.1 hComponents.2.1)
        hComponents.2.2

theorem triple_mod_no_factor_of_left_not_factor
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Tau : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (middle : Alpha -> Sigma) (right : Alpha -> Tau)
    (LeftSetoid : Setoid Rho) (MiddleSetoid : Setoid Sigma)
    (RightSetoid : Setoid Tau)
    (hLeft : ¬ FactorsThroughResidualMod P left LeftSetoid) :
    ¬ FactorsThroughResidualMod P
      (fun x : Alpha => ((left x, middle x), right x))
      (ObstructionCore.PrimitiveDifference.productSetoid
        (ObstructionCore.PrimitiveDifference.productSetoid
          LeftSetoid MiddleSetoid)
        RightSetoid) := by
  intro hTriple
  exact hLeft ((factorsThroughResidualMod_triple_iff_component_factors
    P left middle right LeftSetoid MiddleSetoid RightSetoid).mp hTriple).1

theorem triple_mod_no_factor_of_middle_not_factor
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Tau : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (middle : Alpha -> Sigma) (right : Alpha -> Tau)
    (LeftSetoid : Setoid Rho) (MiddleSetoid : Setoid Sigma)
    (RightSetoid : Setoid Tau)
    (hMiddle : ¬ FactorsThroughResidualMod P middle MiddleSetoid) :
    ¬ FactorsThroughResidualMod P
      (fun x : Alpha => ((left x, middle x), right x))
      (ObstructionCore.PrimitiveDifference.productSetoid
        (ObstructionCore.PrimitiveDifference.productSetoid
          LeftSetoid MiddleSetoid)
        RightSetoid) := by
  intro hTriple
  exact hMiddle ((factorsThroughResidualMod_triple_iff_component_factors
    P left middle right LeftSetoid MiddleSetoid RightSetoid).mp hTriple).2.1

theorem triple_mod_no_factor_of_right_not_factor
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Tau : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (middle : Alpha -> Sigma) (right : Alpha -> Tau)
    (LeftSetoid : Setoid Rho) (MiddleSetoid : Setoid Sigma)
    (RightSetoid : Setoid Tau)
    (hRight : ¬ FactorsThroughResidualMod P right RightSetoid) :
    ¬ FactorsThroughResidualMod P
      (fun x : Alpha => ((left x, middle x), right x))
      (ObstructionCore.PrimitiveDifference.productSetoid
        (ObstructionCore.PrimitiveDifference.productSetoid
          LeftSetoid MiddleSetoid)
        RightSetoid) := by
  intro hTriple
  exact hRight ((factorsThroughResidualMod_triple_iff_component_factors
    P left middle right LeftSetoid MiddleSetoid RightSetoid).mp hTriple).2.2

theorem quotientCompatible_postprocess
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (readout : Rho -> Sigma)
    (hDensity : QuotientCompatible P density) :
    QuotientCompatible P (fun x : Alpha => readout (density x)) := by
  intro x y hxy
  exact congrArg readout (hDensity x y hxy)

theorem factorsThroughResidual_postprocess
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (readout : Rho -> Sigma)
    (hDensity : FactorsThroughResidual P density) :
    FactorsThroughResidual P (fun x : Alpha => readout (density x)) := by
  rcases hDensity with ⟨F, hF⟩
  exact ⟨fun q => readout (F q), fun x => congrArg readout (hF x)⟩

theorem quotientCompatibleMod_postprocess
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (readout : Rho -> Sigma)
    (DensitySetoid : Setoid Rho) (ReadoutSetoid : Setoid Sigma)
    (hRespect :
      ∀ x y : Rho, DensitySetoid.r x y ->
        ReadoutSetoid.r (readout x) (readout y))
    (hDensity : QuotientCompatibleMod P density DensitySetoid) :
    QuotientCompatibleMod P
      (fun x : Alpha => readout (density x)) ReadoutSetoid := by
  intro x y hxy
  exact hRespect (density x) (density y) (hDensity x y hxy)

theorem factorsThroughResidualMod_postprocess
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (readout : Rho -> Sigma)
    (DensitySetoid : Setoid Rho) (ReadoutSetoid : Setoid Sigma)
    (hRespect :
      ∀ x y : Rho, DensitySetoid.r x y ->
        ReadoutSetoid.r (readout x) (readout y))
    (hDensity : FactorsThroughResidualMod P density DensitySetoid) :
    FactorsThroughResidualMod P
      (fun x : Alpha => readout (density x)) ReadoutSetoid := by
  have hDensityCompat :
      QuotientCompatibleMod P density DensitySetoid :=
    (quotientCompatibleMod_iff_factorsThroughResidualMod
      P density DensitySetoid).mp hDensity
  exact
    (quotientCompatibleMod_iff_factorsThroughResidualMod
      P (fun x : Alpha => readout (density x)) ReadoutSetoid).mpr
      (quotientCompatibleMod_postprocess
        P density readout DensitySetoid ReadoutSetoid hRespect hDensityCompat)

def GlobalJointRed {Alpha : Type u} {Beta : Type v} {Rho : Type w}
    {Hidden : Type z} (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden) : Prop :=
  ¬ FactorsThroughResidual P (fun x : Alpha => (density x, hidden x))



theorem density_factor_not_joint_factor_of_hidden_witness
    {Alpha : Type u} {Beta : Type v} {Rho : Type w} {Hidden : Type z}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (hDensity : QuotientCompatible P density)
    {x y : Alpha} (hxy : P.ZeroRel x y) (hHidden : hidden x ≠ hidden y) :
    FactorsThroughResidual P density ∧ GlobalJointRed P density hidden := by
  constructor
  · exact (quotientCompatible_iff_factorsThroughResidual P density).mpr hDensity
  · intro hJoint
    have hJointCompat :
        P.InvariantCongruent (fun x : Alpha => (density x, hidden x)) :=
      (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
        P (fun x : Alpha => (density x, hidden x))).mp hJoint
    have hPair : (density x, hidden x) = (density y, hidden y) :=
      hJointCompat x y hxy
    exact hHidden (congrArg Prod.snd hPair)


theorem marginal_factor_not_joint_factor_of_hidden_witness
    {Alpha : Type u} {Beta : Type v} {Rho : Type w} {Hidden : Type z}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (joint : Alpha -> Rho × Hidden)
    (hMarginal : QuotientCompatible P (fun x : Alpha => (joint x).1))
    {x y : Alpha} (hxy : P.ZeroRel x y) (hHidden : (joint x).2 ≠ (joint y).2) :
    FactorsThroughResidual P (fun x : Alpha => (joint x).1) ∧
      ¬ FactorsThroughResidual P joint := by
  constructor
  · exact
      (quotientCompatible_iff_factorsThroughResidual
        P (fun x : Alpha => (joint x).1)).mpr hMarginal
  · intro hJoint
    have hJointCompat : P.InvariantCongruent joint :=
      (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
        P joint).mp hJoint
    have hPair : joint x = joint y := hJointCompat x y hxy
    exact hHidden (congrArg Prod.snd hPair)


theorem density_diagnostic_not_authority_certificate
    {Alpha : Type u} {Beta : Type v} {Rho : Type w} {Authority : Type z}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (authority : Alpha -> Authority)
    (hDensity : QuotientCompatible P density)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hAuthority : authority x ≠ authority y) :
    FactorsThroughResidual P density ∧
      ¬ FactorsThroughResidual P (fun x : Alpha => (density x, authority x)) :=
  density_factor_not_joint_factor_of_hidden_witness
    P density authority hDensity hxy hAuthority


theorem local_pair_factor_not_joint_factor_of_hidden_witness
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w} {Hidden : Type z}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (hidden : Alpha -> Hidden)
    (hLeft : QuotientCompatible P left)
    (hRight : QuotientCompatible P right)
    {x y : Alpha} (hxy : P.ZeroRel x y) (hHidden : hidden x ≠ hidden y) :
    FactorsThroughResidual P (fun a : Alpha => (left a, right a)) ∧
      ¬ FactorsThroughResidual P
        (fun a : Alpha => ((left a, right a), hidden a)) := by
  exact
    density_factor_not_joint_factor_of_hidden_witness
      P (fun a : Alpha => (left a, right a)) hidden
      (quotientCompatible_pair P left right hLeft hRight) hxy hHidden



theorem diagnostic_readout_factor_not_joint_factor_of_hidden_witness
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w} {Hidden : Type z}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (readout : Rho -> Sigma)
    (hidden : Alpha -> Hidden)
    (hDensity : QuotientCompatible P density)
    {x y : Alpha} (hxy : P.ZeroRel x y) (hHidden : hidden x ≠ hidden y) :
    FactorsThroughResidual P (fun a : Alpha => readout (density a)) ∧
      ¬ FactorsThroughResidual P
        (fun a : Alpha => (readout (density a), hidden a)) := by
  exact
    density_factor_not_joint_factor_of_hidden_witness
      P (fun a : Alpha => readout (density a)) hidden
      (quotientCompatible_postprocess P density readout hDensity)
      hxy hHidden


theorem density_factor_not_hidden_readout_factor_of_witness
    {Alpha : Type u} {Beta : Type v} {Rho : Type w}
    {Hidden : Type z} {Readout : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (readout : Hidden -> Readout)
    (hDensity : QuotientCompatible P density)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hReadout : readout (hidden x) ≠ readout (hidden y)) :
    FactorsThroughResidual P density ∧
      ¬ FactorsThroughResidual P
        (fun a : Alpha => (density a, readout (hidden a))) := by
  exact
    density_factor_not_joint_factor_of_hidden_witness
      P density (fun a : Alpha => readout (hidden a))
      hDensity hxy hReadout


theorem density_mod_factor_not_joint_mod_factor_of_hidden_witness
    {Alpha : Type u} {Beta : Type v} {Rho Hidden : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (DensitySetoid : Setoid Rho) (HiddenSetoid : Setoid Hidden)
    (hDensity : QuotientCompatibleMod P density DensitySetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hHidden : ¬ HiddenSetoid.r (hidden x) (hidden y)) :
    FactorsThroughResidualMod P density DensitySetoid ∧
      ¬ (∃ F : P.ResidualQuotient ->
          Quotient (ObstructionCore.PrimitiveDifference.productSetoid
            DensitySetoid HiddenSetoid),
        ∀ a : Alpha,
          F (P.classOf a) =
            @Quotient.mk (Rho × Hidden)
              (ObstructionCore.PrimitiveDifference.productSetoid
                DensitySetoid HiddenSetoid)
              (density a, hidden a)) := by
  exact
    ObstructionCore.PrimitiveDifference.localGreenGlobalRed_pair_mod_obstruction_of_witness
      P density hidden DensitySetoid HiddenSetoid hDensity hxy hHidden

theorem density_mod_diagnostic_not_authority_certificate
    {Alpha : Type u} {Beta : Type v} {Rho Authority : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (authority : Alpha -> Authority)
    (DensitySetoid : Setoid Rho) (AuthoritySetoid : Setoid Authority)
    (hDensity : QuotientCompatibleMod P density DensitySetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hAuthority : ¬ AuthoritySetoid.r (authority x) (authority y)) :
    FactorsThroughResidualMod P density DensitySetoid ∧
      ¬ (∃ F : P.ResidualQuotient ->
          Quotient (ObstructionCore.PrimitiveDifference.productSetoid
            DensitySetoid AuthoritySetoid),
        ∀ a : Alpha,
          F (P.classOf a) =
            @Quotient.mk (Rho × Authority)
              (ObstructionCore.PrimitiveDifference.productSetoid
                DensitySetoid AuthoritySetoid)
              (density a, authority a)) := by
  exact
    density_mod_factor_not_joint_mod_factor_of_hidden_witness
      P density authority DensitySetoid AuthoritySetoid hDensity hxy hAuthority


theorem local_pair_mod_factor_not_joint_mod_factor_of_hidden_witness
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Hidden : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (hidden : Alpha -> Hidden)
    (LeftSetoid : Setoid Rho) (RightSetoid : Setoid Sigma)
    (HiddenSetoid : Setoid Hidden)
    (hLeft : QuotientCompatibleMod P left LeftSetoid)
    (hRight : QuotientCompatibleMod P right RightSetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hHidden : ¬ HiddenSetoid.r (hidden x) (hidden y)) :
    FactorsThroughResidualMod P (fun a : Alpha => (left a, right a))
      (ObstructionCore.PrimitiveDifference.productSetoid LeftSetoid RightSetoid) ∧
      ¬ (∃ F : P.ResidualQuotient ->
          Quotient (ObstructionCore.PrimitiveDifference.productSetoid
            (ObstructionCore.PrimitiveDifference.productSetoid
              LeftSetoid RightSetoid)
            HiddenSetoid),
        ∀ a : Alpha,
          F (P.classOf a) =
            @Quotient.mk ((Rho × Sigma) × Hidden)
              (ObstructionCore.PrimitiveDifference.productSetoid
                (ObstructionCore.PrimitiveDifference.productSetoid
                  LeftSetoid RightSetoid)
                HiddenSetoid)
              ((left a, right a), hidden a)) := by
  have hPair :
      QuotientCompatibleMod P (fun a : Alpha => (left a, right a))
        (ObstructionCore.PrimitiveDifference.productSetoid
          LeftSetoid RightSetoid) :=
    quotientCompatibleMod_pair
      P left right LeftSetoid RightSetoid hLeft hRight
  exact
    density_mod_factor_not_joint_mod_factor_of_hidden_witness
      P (fun a : Alpha => (left a, right a)) hidden
      (ObstructionCore.PrimitiveDifference.productSetoid LeftSetoid RightSetoid)
      HiddenSetoid hPair hxy hHidden

theorem local_pair_mod_diagnostic_not_authority_certificate
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Authority : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (authority : Alpha -> Authority)
    (LeftSetoid : Setoid Rho) (RightSetoid : Setoid Sigma)
    (AuthoritySetoid : Setoid Authority)
    (hLeft : QuotientCompatibleMod P left LeftSetoid)
    (hRight : QuotientCompatibleMod P right RightSetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hAuthority : ¬ AuthoritySetoid.r (authority x) (authority y)) :
    FactorsThroughResidualMod P (fun a : Alpha => (left a, right a))
      (ObstructionCore.PrimitiveDifference.productSetoid LeftSetoid RightSetoid) ∧
      ¬ (∃ F : P.ResidualQuotient ->
          Quotient (ObstructionCore.PrimitiveDifference.productSetoid
            (ObstructionCore.PrimitiveDifference.productSetoid
              LeftSetoid RightSetoid)
            AuthoritySetoid),
        ∀ a : Alpha,
          F (P.classOf a) =
            @Quotient.mk ((Rho × Sigma) × Authority)
              (ObstructionCore.PrimitiveDifference.productSetoid
                (ObstructionCore.PrimitiveDifference.productSetoid
                  LeftSetoid RightSetoid)
                AuthoritySetoid)
              ((left a, right a), authority a)) := by
  exact
    local_pair_mod_factor_not_joint_mod_factor_of_hidden_witness
      P left right authority LeftSetoid RightSetoid AuthoritySetoid
      hLeft hRight hxy hAuthority



theorem diagnostic_readout_mod_factor_not_joint_mod_factor_of_hidden_witness
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Hidden : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (readout : Rho -> Sigma)
    (hidden : Alpha -> Hidden)
    (DensitySetoid : Setoid Rho) (ReadoutSetoid : Setoid Sigma)
    (HiddenSetoid : Setoid Hidden)
    (hRespect :
      ∀ x y : Rho, DensitySetoid.r x y ->
        ReadoutSetoid.r (readout x) (readout y))
    (hDensity : QuotientCompatibleMod P density DensitySetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hHidden : ¬ HiddenSetoid.r (hidden x) (hidden y)) :
    FactorsThroughResidualMod P
      (fun a : Alpha => readout (density a)) ReadoutSetoid ∧
      ¬ (∃ F : P.ResidualQuotient ->
          Quotient (ObstructionCore.PrimitiveDifference.productSetoid
            ReadoutSetoid HiddenSetoid),
        ∀ a : Alpha,
          F (P.classOf a) =
            @Quotient.mk (Sigma × Hidden)
              (ObstructionCore.PrimitiveDifference.productSetoid
                ReadoutSetoid HiddenSetoid)
              (readout (density a), hidden a)) := by
  exact
    density_mod_factor_not_joint_mod_factor_of_hidden_witness
      P (fun a : Alpha => readout (density a)) hidden
      ReadoutSetoid HiddenSetoid
      (quotientCompatibleMod_postprocess
        P density readout DensitySetoid ReadoutSetoid hRespect hDensity)
      hxy hHidden


theorem density_mod_factor_not_hidden_readout_mod_factor_of_witness
    {Alpha : Type u} {Beta : Type v} {Rho Hidden Readout : Type w}
    (P : ObstructionCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (readout : Hidden -> Readout)
    (DensitySetoid : Setoid Rho) (ReadoutSetoid : Setoid Readout)
    (hDensity : QuotientCompatibleMod P density DensitySetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hReadout : ¬ ReadoutSetoid.r (readout (hidden x)) (readout (hidden y))) :
    FactorsThroughResidualMod P density DensitySetoid ∧
      ¬ (∃ F : P.ResidualQuotient ->
          Quotient (ObstructionCore.PrimitiveDifference.productSetoid
            DensitySetoid ReadoutSetoid),
        ∀ a : Alpha,
          F (P.classOf a) =
            @Quotient.mk (Rho × Readout)
              (ObstructionCore.PrimitiveDifference.productSetoid
                DensitySetoid ReadoutSetoid)
              (density a, readout (hidden a))) := by
  exact
    density_mod_factor_not_joint_mod_factor_of_hidden_witness
      P density (fun a : Alpha => readout (hidden a))
      DensitySetoid ReadoutSetoid hDensity hxy hReadout

end ResidualDensityBridge

end QM

#print axioms QM.ResidualDensityBridge.quotientCompatible_iff_factorsThroughResidual
#print axioms QM.ResidualDensityBridge.quotientCompatibleMod_iff_factorsThroughResidualMod
#print axioms QM.ResidualDensityBridge.quotientCompatibleMod_preserved_by_coarser_output
#print axioms QM.ResidualDensityBridge.factorsThroughResidualMod_preserved_by_coarser_output
#print axioms QM.ResidualDensityBridge.quotientCompatible_pair
#print axioms QM.ResidualDensityBridge.factorsThroughResidual_pair
#print axioms QM.ResidualDensityBridge.quotientCompatibleMod_pair
#print axioms QM.ResidualDensityBridge.factorsThroughResidualMod_pair
#print axioms QM.ResidualDensityBridge.factorsThroughResidual_pair_iff_component_factors
#print axioms QM.ResidualDensityBridge.factorsThroughResidualMod_pair_iff_component_factors
#print axioms QM.ResidualDensityBridge.pair_no_factor_of_left_not_factor
#print axioms QM.ResidualDensityBridge.pair_no_factor_of_right_not_factor
#print axioms QM.ResidualDensityBridge.factorsThroughResidual_triple_iff_component_factors
#print axioms QM.ResidualDensityBridge.triple_no_factor_of_left_not_factor
#print axioms QM.ResidualDensityBridge.triple_no_factor_of_middle_not_factor
#print axioms QM.ResidualDensityBridge.triple_no_factor_of_right_not_factor
#print axioms QM.ResidualDensityBridge.pair_mod_no_factor_of_left_not_factor
#print axioms QM.ResidualDensityBridge.pair_mod_no_factor_of_right_not_factor
#print axioms QM.ResidualDensityBridge.factorsThroughResidualMod_triple_iff_component_factors
#print axioms QM.ResidualDensityBridge.triple_mod_no_factor_of_left_not_factor
#print axioms QM.ResidualDensityBridge.triple_mod_no_factor_of_middle_not_factor
#print axioms QM.ResidualDensityBridge.triple_mod_no_factor_of_right_not_factor
#print axioms QM.ResidualDensityBridge.quotientCompatible_postprocess
#print axioms QM.ResidualDensityBridge.factorsThroughResidual_postprocess
#print axioms QM.ResidualDensityBridge.quotientCompatibleMod_postprocess
#print axioms QM.ResidualDensityBridge.factorsThroughResidualMod_postprocess
#print axioms QM.ResidualDensityBridge.density_factor_not_joint_factor_of_hidden_witness
#print axioms QM.ResidualDensityBridge.marginal_factor_not_joint_factor_of_hidden_witness
#print axioms QM.ResidualDensityBridge.density_diagnostic_not_authority_certificate
#print axioms QM.ResidualDensityBridge.local_pair_factor_not_joint_factor_of_hidden_witness
#print axioms QM.ResidualDensityBridge.diagnostic_readout_factor_not_joint_factor_of_hidden_witness
#print axioms QM.ResidualDensityBridge.density_factor_not_hidden_readout_factor_of_witness
#print axioms QM.ResidualDensityBridge.density_mod_factor_not_joint_mod_factor_of_hidden_witness
#print axioms QM.ResidualDensityBridge.density_mod_diagnostic_not_authority_certificate
#print axioms QM.ResidualDensityBridge.local_pair_mod_factor_not_joint_mod_factor_of_hidden_witness
#print axioms QM.ResidualDensityBridge.local_pair_mod_diagnostic_not_authority_certificate
#print axioms QM.ResidualDensityBridge.diagnostic_readout_mod_factor_not_joint_mod_factor_of_hidden_witness
#print axioms QM.ResidualDensityBridge.density_mod_factor_not_hidden_readout_mod_factor_of_witness

private def l5aProvenance : String :=
  "Origin: lean4/ResidualDensityBridge.lean Claim: quotientCompatible_iff_factorsThroughResidual AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
