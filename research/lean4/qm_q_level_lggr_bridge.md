import «residual_density_bridge»
import «primitive_difference_wrappers_q_primitive_difference_wrappers»

/-!
QM-to-Q bridge for PrimitiveDifference LGGR.

This module names the exact point where the QM residual-density diagnostic
uses the Level-Q PrimitiveDifference non-promotion theorem. A density-like
profile can descend through the residual quotient, while the paired
profile/hidden readout remains blocked by a zero-related separating witness.

It is only a quotient/factorization theorem. It does not derive quantum
mechanics, select the Born rule, license a continuum lift, or mint authority.
-/

namespace QM

namespace QLevelLGGRBridge

universe u v w z

/--
Q-level form of the QM residual-density LGGR witness.

If a density-like diagnostic is invariant on PrimitiveDifference zero classes,
then it factors through the residual quotient. If a hidden/global readout still
separates a zero-related pair, the paired `(density, hidden)` readout cannot
factor through that same quotient. This is the QM-facing instance of
`Paper_Q.primitive_continuum_lggr_nonpromotion`.
-/
theorem density_lggr_is_q_level_primitive_nonpromotion
    {Alpha : Type u} {Beta : Type v} {Rho : Type w} {Hidden : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (hDensity : ResidualDensityBridge.QuotientCompatible P density)
    {x y : Alpha} (hxy : P.ZeroRel x y) (hHidden : hidden x ≠ hidden y) :
    (∃ F : P.ResidualQuotient -> Rho,
      ∀ a : Alpha, F (P.classOf a) = density a) ∧
    ¬ (∃ F : P.ResidualQuotient -> Rho × Hidden,
      ∀ a : Alpha, F (P.classOf a) = (density a, hidden a)) := by
  exact
    Paper_Q.primitive_continuum_lggr_nonpromotion
      P density hidden hDensity hxy hHidden

/--
Authority-coordinate specialization of the Q-level bridge.

A quotient-compatible density diagnostic is not a Q terminal or authority
certificate when an authority/status coordinate separates zero-related
representatives.
-/
theorem density_q_bridge_not_authority_certificate
    {Alpha : Type u} {Beta : Type v} {Rho : Type w} {Authority : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (authority : Alpha -> Authority)
    (hDensity : ResidualDensityBridge.QuotientCompatible P density)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hAuthority : authority x ≠ authority y) :
    (∃ F : P.ResidualQuotient -> Rho,
      ∀ a : Alpha, F (P.classOf a) = density a) ∧
    ¬ (∃ F : P.ResidualQuotient -> Rho × Authority,
      ∀ a : Alpha, F (P.classOf a) = (density a, authority a)) := by
  exact
    density_lggr_is_q_level_primitive_nonpromotion
      P density authority hDensity hxy hAuthority

/--
Declared-equivalence Q-level form of the QM residual-density LGGR witness.

Q packets often descend through declared output equivalences rather than raw
equality. If a density-like diagnostic is invariant only modulo its declared
equivalence, but a hidden/global readout remains separated modulo its own
declared equivalence on a zero-related pair, the paired modulo readout cannot
descend through the PrimitiveDifference residual quotient.
-/
theorem density_mod_lggr_is_q_level_primitive_nonpromotion
    {Alpha : Type u} {Beta : Type v} {Rho Hidden : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (DensitySetoid : Setoid Rho) (HiddenSetoid : Setoid Hidden)
    (hDensity :
      ResidualDensityBridge.QuotientCompatibleMod P density DensitySetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hHidden : ¬ HiddenSetoid.r (hidden x) (hidden y)) :
    (∃ F : P.ResidualQuotient -> Quotient DensitySetoid,
      ∀ a : Alpha, F (P.classOf a) = Quotient.mk DensitySetoid (density a)) ∧
    ¬ (∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          DensitySetoid HiddenSetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk (Rho × Hidden)
            (OmegaCore.PrimitiveDifference.productSetoid
              DensitySetoid HiddenSetoid)
            (density a, hidden a)) := by
  exact
    Paper_Q.primitive_continuum_lggr_mod_nonpromotion
      P density hidden DensitySetoid HiddenSetoid hDensity hxy hHidden

/--
Authority-coordinate specialization of the declared-equivalence Q-level bridge.
Declared equivalences can lower diagnostic resolution; they still do not let a
separated authority/status coordinate ride inside a green density packet.
-/
theorem density_mod_q_bridge_not_authority_certificate
    {Alpha : Type u} {Beta : Type v} {Rho Authority : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (authority : Alpha -> Authority)
    (DensitySetoid : Setoid Rho) (AuthoritySetoid : Setoid Authority)
    (hDensity :
      ResidualDensityBridge.QuotientCompatibleMod P density DensitySetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hAuthority : ¬ AuthoritySetoid.r (authority x) (authority y)) :
    (∃ F : P.ResidualQuotient -> Quotient DensitySetoid,
      ∀ a : Alpha, F (P.classOf a) = Quotient.mk DensitySetoid (density a)) ∧
    ¬ (∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          DensitySetoid AuthoritySetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk (Rho × Authority)
            (OmegaCore.PrimitiveDifference.productSetoid
              DensitySetoid AuthoritySetoid)
            (density a, authority a)) := by
  exact
    density_mod_lggr_is_q_level_primitive_nonpromotion
      P density authority DensitySetoid AuthoritySetoid hDensity hxy hAuthority

/--
Density diagnostic coarsening preserves modulo residual descent.

If a Q packet has already made the density diagnostic descend modulo a fine
output equivalence, it also descends modulo any declared coarser diagnostic
equivalence. This lowers diagnostic resolution only; it does not add any hidden
or authority coordinate.
-/
theorem density_mod_descent_preserved_by_diagnostic_coarsening
    {Alpha : Type u} {Beta : Type v} {Rho : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho)
    (FineDensitySetoid : Setoid Rho) (CoarseDensitySetoid : Setoid Rho)
    (hFineToCoarse :
      ∀ x y : Rho, FineDensitySetoid.r x y -> CoarseDensitySetoid.r x y)
    (hDescends :
      ResidualDensityBridge.FactorsThroughResidualMod
        P density FineDensitySetoid) :
    ResidualDensityBridge.FactorsThroughResidualMod
      P density CoarseDensitySetoid := by
  exact
    ResidualDensityBridge.factorsThroughResidualMod_preserved_by_coarser_output
      P density FineDensitySetoid CoarseDensitySetoid hFineToCoarse hDescends

/--
Q-level LGGR persists under density-side diagnostic coarsening.

Coarsening the density equivalence preserves the local green descent, but it
does not erase a hidden/global readout that is still separated modulo its own
declared equivalence.
-/
theorem density_mod_lggr_persists_under_density_coarsening
    {Alpha : Type u} {Beta : Type v} {Rho Hidden : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (FineDensitySetoid : Setoid Rho) (CoarseDensitySetoid : Setoid Rho)
    (HiddenSetoid : Setoid Hidden)
    (hFineToCoarse :
      ∀ x y : Rho, FineDensitySetoid.r x y -> CoarseDensitySetoid.r x y)
    (hDensity :
      ResidualDensityBridge.QuotientCompatibleMod
        P density FineDensitySetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hHidden : ¬ HiddenSetoid.r (hidden x) (hidden y)) :
    (∃ F : P.ResidualQuotient -> Quotient CoarseDensitySetoid,
      ∀ a : Alpha,
        F (P.classOf a) = Quotient.mk CoarseDensitySetoid (density a)) ∧
    ¬ (∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          CoarseDensitySetoid HiddenSetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk (Rho × Hidden)
            (OmegaCore.PrimitiveDifference.productSetoid
              CoarseDensitySetoid HiddenSetoid)
            (density a, hidden a)) := by
  have hCoarse :
      ResidualDensityBridge.QuotientCompatibleMod
        P density CoarseDensitySetoid :=
    ResidualDensityBridge.quotientCompatibleMod_preserved_by_coarser_output
      P density FineDensitySetoid CoarseDensitySetoid hFineToCoarse hDensity
  exact
    density_mod_lggr_is_q_level_primitive_nonpromotion
      P density hidden CoarseDensitySetoid HiddenSetoid hCoarse hxy hHidden

/--
Authority-coordinate specialization of density-side diagnostic coarsening.
Coarsening the density diagnostic does not convert a still-separated authority
coordinate into a paired quotient factor.
-/
theorem density_mod_authority_firewall_persists_under_density_coarsening
    {Alpha : Type u} {Beta : Type v} {Rho Authority : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (authority : Alpha -> Authority)
    (FineDensitySetoid : Setoid Rho) (CoarseDensitySetoid : Setoid Rho)
    (AuthoritySetoid : Setoid Authority)
    (hFineToCoarse :
      ∀ x y : Rho, FineDensitySetoid.r x y -> CoarseDensitySetoid.r x y)
    (hDensity :
      ResidualDensityBridge.QuotientCompatibleMod
        P density FineDensitySetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hAuthority : ¬ AuthoritySetoid.r (authority x) (authority y)) :
    (∃ F : P.ResidualQuotient -> Quotient CoarseDensitySetoid,
      ∀ a : Alpha,
        F (P.classOf a) = Quotient.mk CoarseDensitySetoid (density a)) ∧
    ¬ (∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          CoarseDensitySetoid AuthoritySetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk (Rho × Authority)
            (OmegaCore.PrimitiveDifference.productSetoid
              CoarseDensitySetoid AuthoritySetoid)
            (density a, authority a)) := by
  exact
    density_mod_lggr_persists_under_density_coarsening
      P density authority FineDensitySetoid CoarseDensitySetoid AuthoritySetoid
      hFineToCoarse hDensity hxy hAuthority


/--
Q-level local-green composition theorem.

Two residual diagnostics that are separately quotient-compatible compose into a
quotient-compatible visible pair. If a hidden/global coordinate still separates
a zero-related witness pair, the augmented visible-pair/hidden readout cannot
factor through the primitive residual quotient. This is the Q-level version of
LGGR composition.
-/
theorem local_pair_lggr_is_q_level_primitive_nonpromotion
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w} {Hidden : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (hidden : Alpha -> Hidden)
    (hLeft : ResidualDensityBridge.QuotientCompatible P left)
    (hRight : ResidualDensityBridge.QuotientCompatible P right)
    {x y : Alpha} (hxy : P.ZeroRel x y) (hHidden : hidden x ≠ hidden y) :
    (∃ F : P.ResidualQuotient -> Rho × Sigma,
      ∀ a : Alpha, F (P.classOf a) = (left a, right a)) ∧
    ¬ (∃ F : P.ResidualQuotient -> (Rho × Sigma) × Hidden,
      ∀ a : Alpha, F (P.classOf a) = ((left a, right a), hidden a)) := by
  exact
    Paper_Q.primitive_continuum_lggr_nonpromotion
      P (fun a : Alpha => (left a, right a)) hidden
      (ResidualDensityBridge.quotientCompatible_pair
        P left right hLeft hRight)
      hxy hHidden

/--
Authority-coordinate specialization of Q-level local-green composition.
Even a paired visible diagnostic is not an authority certificate when the
authority/status coordinate remains separated on a primitive zero witness.
-/
theorem local_pair_q_bridge_not_authority_certificate
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w}
    {Authority : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (authority : Alpha -> Authority)
    (hLeft : ResidualDensityBridge.QuotientCompatible P left)
    (hRight : ResidualDensityBridge.QuotientCompatible P right)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hAuthority : authority x ≠ authority y) :
    (∃ F : P.ResidualQuotient -> Rho × Sigma,
      ∀ a : Alpha, F (P.classOf a) = (left a, right a)) ∧
    ¬ (∃ F : P.ResidualQuotient -> (Rho × Sigma) × Authority,
      ∀ a : Alpha, F (P.classOf a) = ((left a, right a), authority a)) := by
  exact
    local_pair_lggr_is_q_level_primitive_nonpromotion
      P left right authority hLeft hRight hxy hAuthority

/--
Declared-equivalence Q-level local-green composition theorem.

Two visible diagnostics that descend modulo their declared equivalences compose
into a visible product diagnostic that descends modulo the product equivalence.
A hidden/global coordinate that remains separated modulo its own declared
equivalence still blocks descent of the augmented product/hidden readout.
-/
theorem local_pair_mod_lggr_is_q_level_primitive_nonpromotion
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Hidden : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (hidden : Alpha -> Hidden)
    (LeftSetoid : Setoid Rho) (RightSetoid : Setoid Sigma)
    (HiddenSetoid : Setoid Hidden)
    (hLeft :
      ResidualDensityBridge.QuotientCompatibleMod P left LeftSetoid)
    (hRight :
      ResidualDensityBridge.QuotientCompatibleMod P right RightSetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hHidden : ¬ HiddenSetoid.r (hidden x) (hidden y)) :
    (∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          LeftSetoid RightSetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk (Rho × Sigma)
            (OmegaCore.PrimitiveDifference.productSetoid
              LeftSetoid RightSetoid)
            (left a, right a)) ∧
    ¬ (∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          (OmegaCore.PrimitiveDifference.productSetoid
            LeftSetoid RightSetoid)
          HiddenSetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk ((Rho × Sigma) × Hidden)
            (OmegaCore.PrimitiveDifference.productSetoid
              (OmegaCore.PrimitiveDifference.productSetoid
                LeftSetoid RightSetoid)
              HiddenSetoid)
            ((left a, right a), hidden a)) := by
  have hPair :
      ResidualDensityBridge.QuotientCompatibleMod
        P (fun a : Alpha => (left a, right a))
        (OmegaCore.PrimitiveDifference.productSetoid
          LeftSetoid RightSetoid) :=
    ResidualDensityBridge.quotientCompatibleMod_pair
      P left right LeftSetoid RightSetoid hLeft hRight
  exact
    Paper_Q.primitive_continuum_lggr_mod_nonpromotion
      P (fun a : Alpha => (left a, right a)) hidden
      (OmegaCore.PrimitiveDifference.productSetoid LeftSetoid RightSetoid)
      HiddenSetoid hPair hxy hHidden

/--
Authority-coordinate specialization of declared-equivalence local-green
composition. Pairing two green visible diagnostics still does not let a
separated authority/status coordinate descend through the Q residual quotient.
-/
theorem local_pair_mod_q_bridge_not_authority_certificate
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Authority : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (authority : Alpha -> Authority)
    (LeftSetoid : Setoid Rho) (RightSetoid : Setoid Sigma)
    (AuthoritySetoid : Setoid Authority)
    (hLeft :
      ResidualDensityBridge.QuotientCompatibleMod P left LeftSetoid)
    (hRight :
      ResidualDensityBridge.QuotientCompatibleMod P right RightSetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hAuthority : ¬ AuthoritySetoid.r (authority x) (authority y)) :
    (∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          LeftSetoid RightSetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk (Rho × Sigma)
            (OmegaCore.PrimitiveDifference.productSetoid
              LeftSetoid RightSetoid)
            (left a, right a)) ∧
    ¬ (∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          (OmegaCore.PrimitiveDifference.productSetoid
            LeftSetoid RightSetoid)
          AuthoritySetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk ((Rho × Sigma) × Authority)
            (OmegaCore.PrimitiveDifference.productSetoid
              (OmegaCore.PrimitiveDifference.productSetoid
                LeftSetoid RightSetoid)
              AuthoritySetoid)
            ((left a, right a), authority a)) := by
  exact
    local_pair_mod_lggr_is_q_level_primitive_nonpromotion
      P left right authority LeftSetoid RightSetoid AuthoritySetoid
      hLeft hRight hxy hAuthority


/--
Q-level diagnostic-readout closure theorem.

Postprocessing a visible density diagnostic by an ordinary readout preserves
local residual descent. If a hidden/global coordinate still separates a
zero-related witness pair, the paired readout/hidden packet cannot descend.
-/
theorem diagnostic_readout_lggr_is_q_level_primitive_nonpromotion
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w} {Hidden : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (readout : Rho -> Sigma)
    (hidden : Alpha -> Hidden)
    (hDensity : ResidualDensityBridge.QuotientCompatible P density)
    {x y : Alpha} (hxy : P.ZeroRel x y) (hHidden : hidden x ≠ hidden y) :
    (∃ F : P.ResidualQuotient -> Sigma,
      ∀ a : Alpha, F (P.classOf a) = readout (density a)) ∧
    ¬ (∃ F : P.ResidualQuotient -> Sigma × Hidden,
      ∀ a : Alpha, F (P.classOf a) = (readout (density a), hidden a)) := by
  exact
    Paper_Q.primitive_continuum_lggr_nonpromotion
      P (fun a : Alpha => readout (density a)) hidden
      (ResidualDensityBridge.quotientCompatible_postprocess
        P density readout hDensity)
      hxy hHidden

/--
Q-level hidden-readout firewall.

A density diagnostic may descend while any declared readout of the hidden/global
coordinate that still separates a zero-related witness blocks paired descent.
-/
theorem hidden_readout_lggr_is_q_level_primitive_nonpromotion
    {Alpha : Type u} {Beta : Type v} {Rho Readout : Type w}
    {Hidden : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (readout : Hidden -> Readout)
    (hDensity : ResidualDensityBridge.QuotientCompatible P density)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hReadout : readout (hidden x) ≠ readout (hidden y)) :
    (∃ F : P.ResidualQuotient -> Rho,
      ∀ a : Alpha, F (P.classOf a) = density a) ∧
    ¬ (∃ F : P.ResidualQuotient -> Rho × Readout,
      ∀ a : Alpha, F (P.classOf a) = (density a, readout (hidden a))) := by
  exact
    Paper_Q.primitive_continuum_lggr_target_readout_nonpromotion
      P density hidden readout hDensity hxy hReadout

/--
Declared-equivalence Q-level diagnostic-readout closure theorem.

If a visible density diagnostic descends modulo its declared equivalence and a
readout respects that equivalence, the readout diagnostic also descends modulo
its declared readout equivalence. A hidden/global coordinate that remains
separated modulo its own declared equivalence still blocks paired descent.
-/
theorem diagnostic_readout_mod_lggr_is_q_level_primitive_nonpromotion
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Hidden : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (readout : Rho -> Sigma)
    (hidden : Alpha -> Hidden)
    (DensitySetoid : Setoid Rho) (ReadoutSetoid : Setoid Sigma)
    (HiddenSetoid : Setoid Hidden)
    (hRespect :
      ∀ x y : Rho, DensitySetoid.r x y ->
        ReadoutSetoid.r (readout x) (readout y))
    (hDensity :
      ResidualDensityBridge.QuotientCompatibleMod P density DensitySetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hHidden : ¬ HiddenSetoid.r (hidden x) (hidden y)) :
    (∃ F : P.ResidualQuotient -> Quotient ReadoutSetoid,
      ∀ a : Alpha,
        F (P.classOf a) = Quotient.mk ReadoutSetoid (readout (density a))) ∧
    ¬ (∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          ReadoutSetoid HiddenSetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk (Sigma × Hidden)
            (OmegaCore.PrimitiveDifference.productSetoid
              ReadoutSetoid HiddenSetoid)
            (readout (density a), hidden a)) := by
  have hReadoutDensity :
      ResidualDensityBridge.QuotientCompatibleMod P
        (fun a : Alpha => readout (density a)) ReadoutSetoid :=
    ResidualDensityBridge.quotientCompatibleMod_postprocess
      P density readout DensitySetoid ReadoutSetoid hRespect hDensity
  exact
    Paper_Q.primitive_continuum_lggr_mod_nonpromotion
      P (fun a : Alpha => readout (density a)) hidden
      ReadoutSetoid HiddenSetoid hReadoutDensity hxy hHidden

/--
Declared-equivalence Q-level hidden-readout firewall.

A density diagnostic may descend modulo its declared equivalence while any
hidden/global readout that still separates a zero-related witness modulo its own
declared readout equivalence blocks paired modulo descent.
-/
theorem hidden_readout_mod_lggr_is_q_level_primitive_nonpromotion
    {Alpha : Type u} {Beta : Type v} {Rho Readout : Type w}
    {Hidden : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (readout : Hidden -> Readout)
    (DensitySetoid : Setoid Rho) (ReadoutSetoid : Setoid Readout)
    (hDensity :
      ResidualDensityBridge.QuotientCompatibleMod P density DensitySetoid)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hReadout :
      ¬ ReadoutSetoid.r (readout (hidden x)) (readout (hidden y))) :
    (∃ F : P.ResidualQuotient -> Quotient DensitySetoid,
      ∀ a : Alpha,
        F (P.classOf a) = Quotient.mk DensitySetoid (density a)) ∧
    ¬ (∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          DensitySetoid ReadoutSetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk (Rho × Readout)
            (OmegaCore.PrimitiveDifference.productSetoid
              DensitySetoid ReadoutSetoid)
            (density a, readout (hidden a))) := by
  exact
    Paper_Q.primitive_continuum_lggr_mod_target_readout_nonpromotion
      P density hidden readout DensitySetoid ReadoutSetoid hDensity hxy hReadout

/--
A paired quotient factorization forces the hidden coordinate to be quotient
compatible. This is the converse-form firewall: a global certificate through the
residual quotient cannot hide a non-invariant authority/status readout inside a
locally green density profile.
-/
theorem joint_factor_implies_hidden_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho : Type w} {Hidden : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (hJoint : ∃ F : P.ResidualQuotient -> Rho × Hidden,
      ∀ a : Alpha, F (P.classOf a) = (density a, hidden a)) :
    ResidualDensityBridge.QuotientCompatible P hidden := by
  rw [ResidualDensityBridge.QuotientCompatible]
  intro x y hxy
  rcases hJoint with ⟨F, hF⟩
  have hClass : P.classOf x = P.classOf y :=
    OmegaCore.PrimitiveDifference.classOf_eq_of_zero P hxy
  have hPair : (density x, hidden x) = (density y, hidden y) := by
    calc
      (density x, hidden x) = F (P.classOf x) := (hF x).symm
      _ = F (P.classOf y) := by rw [hClass]
      _ = (density y, hidden y) := hF y
  exact congrArg Prod.snd hPair

/--
Authority-coordinate specialization: if a paired density/authority diagnostic
really factors through the primitive residual quotient, the authority/status
readout must already be invariant on zero-related worlds.
-/
theorem joint_density_authority_factor_implies_authority_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho : Type w} {Authority : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (authority : Alpha -> Authority)
    (hJoint : ∃ F : P.ResidualQuotient -> Rho × Authority,
      ∀ a : Alpha, F (P.classOf a) = (density a, authority a)) :
    ResidualDensityBridge.QuotientCompatible P authority := by
  exact joint_factor_implies_hidden_quotient_compatible P density authority hJoint

/--
Modulo converse-form firewall. If the paired density/hidden readout descends
through the residual quotient modulo the product of declared equivalences, then
the hidden coordinate must itself be quotient-compatible modulo its declared
equivalence.
-/
theorem joint_mod_factor_implies_hidden_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Hidden : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (DensitySetoid : Setoid Rho) (HiddenSetoid : Setoid Hidden)
    (hJoint : ∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          DensitySetoid HiddenSetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk (Rho × Hidden)
            (OmegaCore.PrimitiveDifference.productSetoid
              DensitySetoid HiddenSetoid)
            (density a, hidden a)) :
    ResidualDensityBridge.QuotientCompatibleMod P hidden HiddenSetoid := by
  rw [ResidualDensityBridge.QuotientCompatibleMod]
  intro x y hxy
  rcases hJoint with ⟨F, hF⟩
  have hClass : P.classOf x = P.classOf y :=
    OmegaCore.PrimitiveDifference.classOf_eq_of_zero P hxy
  have hQuot :
      @Quotient.mk (Rho × Hidden)
          (OmegaCore.PrimitiveDifference.productSetoid
            DensitySetoid HiddenSetoid)
          (density x, hidden x) =
        @Quotient.mk (Rho × Hidden)
          (OmegaCore.PrimitiveDifference.productSetoid
            DensitySetoid HiddenSetoid)
          (density y, hidden y) := by
    calc
      @Quotient.mk (Rho × Hidden)
          (OmegaCore.PrimitiveDifference.productSetoid
            DensitySetoid HiddenSetoid)
          (density x, hidden x) = F (P.classOf x) := (hF x).symm
      _ = F (P.classOf y) := by rw [hClass]
      _ = @Quotient.mk (Rho × Hidden)
          (OmegaCore.PrimitiveDifference.productSetoid
            DensitySetoid HiddenSetoid)
          (density y, hidden y) := hF y
  have hRel := Quotient.exact hQuot
  exact hRel.2

/--
Authority-coordinate specialization of the modulo converse firewall.
-/
theorem joint_mod_density_authority_factor_implies_authority_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Authority : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (authority : Alpha -> Authority)
    (DensitySetoid : Setoid Rho) (AuthoritySetoid : Setoid Authority)
    (hJoint : ∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          DensitySetoid AuthoritySetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk (Rho × Authority)
            (OmegaCore.PrimitiveDifference.productSetoid
              DensitySetoid AuthoritySetoid)
            (density a, authority a)) :
    ResidualDensityBridge.QuotientCompatibleMod P authority AuthoritySetoid := by
  exact
    joint_mod_factor_implies_hidden_quotient_compatible
      P density authority DensitySetoid AuthoritySetoid hJoint


/--
Exact product-converse firewall. If an augmented visible-product/hidden packet
really factors through the primitive residual quotient, then the hidden/global
coordinate was already quotient-compatible. A global certificate cannot be
hidden inside two local green visible diagnostics.
-/
theorem local_pair_factor_implies_hidden_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w} {Hidden : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (hidden : Alpha -> Hidden)
    (hJoint : ∃ F : P.ResidualQuotient -> (Rho × Sigma) × Hidden,
      ∀ a : Alpha, F (P.classOf a) = ((left a, right a), hidden a)) :
    ResidualDensityBridge.QuotientCompatible P hidden := by
  exact
    joint_factor_implies_hidden_quotient_compatible
      P (fun a : Alpha => (left a, right a)) hidden hJoint

/--
Exact diagnostic-readout converse firewall. If a visible-readout/hidden packet
factors through the residual quotient, the hidden/global coordinate itself must
be quotient-compatible.
-/
theorem diagnostic_readout_factor_implies_hidden_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Sigma : Type w} {Hidden : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (readout : Rho -> Sigma)
    (hidden : Alpha -> Hidden)
    (hJoint : ∃ F : P.ResidualQuotient -> Sigma × Hidden,
      ∀ a : Alpha, F (P.classOf a) = (readout (density a), hidden a)) :
    ResidualDensityBridge.QuotientCompatible P hidden := by
  exact
    joint_factor_implies_hidden_quotient_compatible
      P (fun a : Alpha => readout (density a)) hidden hJoint

/--
Exact hidden-readout converse firewall. If the paired density/hidden-readout
packet factors through the residual quotient, then that hidden readout was
already quotient-compatible.
-/
theorem hidden_readout_factor_implies_readout_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Readout : Type w} {Hidden : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (readout : Hidden -> Readout)
    (hJoint : ∃ F : P.ResidualQuotient -> Rho × Readout,
      ∀ a : Alpha, F (P.classOf a) = (density a, readout (hidden a))) :
    ResidualDensityBridge.QuotientCompatible
      P (fun a : Alpha => readout (hidden a)) := by
  exact
    joint_factor_implies_hidden_quotient_compatible
      P density (fun a : Alpha => readout (hidden a)) hJoint

/--
Modulo product-converse firewall. If an augmented visible-product/hidden packet
descends modulo the product of declared equivalences, then the hidden/global
coordinate must itself be quotient-compatible modulo its declared equivalence.
-/
theorem local_pair_mod_factor_implies_hidden_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Hidden : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (hidden : Alpha -> Hidden)
    (LeftSetoid : Setoid Rho) (RightSetoid : Setoid Sigma)
    (HiddenSetoid : Setoid Hidden)
    (hJoint : ∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          (OmegaCore.PrimitiveDifference.productSetoid
            LeftSetoid RightSetoid)
          HiddenSetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk ((Rho × Sigma) × Hidden)
            (OmegaCore.PrimitiveDifference.productSetoid
              (OmegaCore.PrimitiveDifference.productSetoid
                LeftSetoid RightSetoid)
              HiddenSetoid)
            ((left a, right a), hidden a)) :
    ResidualDensityBridge.QuotientCompatibleMod P hidden HiddenSetoid := by
  exact
    joint_mod_factor_implies_hidden_quotient_compatible
      P (fun a : Alpha => (left a, right a)) hidden
      (OmegaCore.PrimitiveDifference.productSetoid LeftSetoid RightSetoid)
      HiddenSetoid hJoint

/--
Modulo diagnostic-readout converse firewall. If a visible-readout/hidden packet
descends modulo declared equivalences, then the hidden/global coordinate must
itself be quotient-compatible modulo its declared equivalence.
-/
theorem diagnostic_readout_mod_factor_implies_hidden_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Hidden : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (readout : Rho -> Sigma)
    (hidden : Alpha -> Hidden)
    (ReadoutSetoid : Setoid Sigma) (HiddenSetoid : Setoid Hidden)
    (hJoint : ∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          ReadoutSetoid HiddenSetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk (Sigma × Hidden)
            (OmegaCore.PrimitiveDifference.productSetoid
              ReadoutSetoid HiddenSetoid)
            (readout (density a), hidden a)) :
    ResidualDensityBridge.QuotientCompatibleMod P hidden HiddenSetoid := by
  exact
    joint_mod_factor_implies_hidden_quotient_compatible
      P (fun a : Alpha => readout (density a)) hidden
      ReadoutSetoid HiddenSetoid hJoint

/--
Modulo hidden-readout converse firewall. If the paired density/hidden-readout
packet descends modulo declared equivalences, then the hidden readout itself was
quotient-compatible modulo its declared readout equivalence.
-/
theorem hidden_readout_mod_factor_implies_readout_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Hidden Readout : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (readout : Hidden -> Readout)
    (DensitySetoid : Setoid Rho) (ReadoutSetoid : Setoid Readout)
    (hJoint : ∃ F : P.ResidualQuotient ->
        Quotient (OmegaCore.PrimitiveDifference.productSetoid
          DensitySetoid ReadoutSetoid),
      ∀ a : Alpha,
        F (P.classOf a) =
          @Quotient.mk (Rho × Readout)
            (OmegaCore.PrimitiveDifference.productSetoid
              DensitySetoid ReadoutSetoid)
            (density a, readout (hidden a))) :
    ResidualDensityBridge.QuotientCompatibleMod
      P (fun a : Alpha => readout (hidden a)) ReadoutSetoid := by
  exact
    joint_mod_factor_implies_hidden_quotient_compatible
      P density (fun a : Alpha => readout (hidden a))
      DensitySetoid ReadoutSetoid hJoint

/--
Exact visible-product certificate criterion. Once the visible local diagnostics
are quotient-compatible, augmented product descent is equivalent to hidden
quotient compatibility.
-/
theorem local_pair_factor_iff_hidden_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Hidden : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (hidden : Alpha -> Hidden)
    (hLeft : ResidualDensityBridge.QuotientCompatible P left)
    (hRight : ResidualDensityBridge.QuotientCompatible P right) :
    ResidualDensityBridge.FactorsThroughResidual
      P (fun a : Alpha => ((left a, right a), hidden a)) ↔
    ResidualDensityBridge.QuotientCompatible P hidden := by
  constructor
  · intro hJoint
    exact local_pair_factor_implies_hidden_quotient_compatible
      P left right hidden hJoint
  · intro hHidden
    have hVisibleCompat :
        ResidualDensityBridge.QuotientCompatible
          P (fun a : Alpha => (left a, right a)) :=
      ResidualDensityBridge.quotientCompatible_pair
        P left right hLeft hRight
    have hVisibleFactor :
        ResidualDensityBridge.FactorsThroughResidual
          P (fun a : Alpha => (left a, right a)) :=
      (ResidualDensityBridge.quotientCompatible_iff_factorsThroughResidual
        P (fun a : Alpha => (left a, right a))).mpr hVisibleCompat
    have hHiddenFactor :
        ResidualDensityBridge.FactorsThroughResidual P hidden :=
      (ResidualDensityBridge.quotientCompatible_iff_factorsThroughResidual
        P hidden).mpr hHidden
    exact
      ResidualDensityBridge.factorsThroughResidual_pair
        P (fun a : Alpha => (left a, right a)) hidden
        hVisibleFactor hHiddenFactor

/--
Exact diagnostic-readout certificate criterion. Once the source density is
quotient-compatible, descent of a visible readout paired with hidden data is
equivalent to hidden quotient compatibility.
-/
theorem diagnostic_readout_factor_iff_hidden_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Hidden : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (readout : Rho -> Sigma)
    (hidden : Alpha -> Hidden)
    (hDensity : ResidualDensityBridge.QuotientCompatible P density) :
    ResidualDensityBridge.FactorsThroughResidual
      P (fun a : Alpha => (readout (density a), hidden a)) ↔
    ResidualDensityBridge.QuotientCompatible P hidden := by
  constructor
  · intro hJoint
    exact diagnostic_readout_factor_implies_hidden_quotient_compatible
      P density readout hidden hJoint
  · intro hHidden
    have hReadoutCompat :
        ResidualDensityBridge.QuotientCompatible
          P (fun a : Alpha => readout (density a)) :=
      ResidualDensityBridge.quotientCompatible_postprocess
        P density readout hDensity
    have hReadoutFactor :
        ResidualDensityBridge.FactorsThroughResidual
          P (fun a : Alpha => readout (density a)) :=
      (ResidualDensityBridge.quotientCompatible_iff_factorsThroughResidual
        P (fun a : Alpha => readout (density a))).mpr hReadoutCompat
    have hHiddenFactor :
        ResidualDensityBridge.FactorsThroughResidual P hidden :=
      (ResidualDensityBridge.quotientCompatible_iff_factorsThroughResidual
        P hidden).mpr hHidden
    exact
      ResidualDensityBridge.factorsThroughResidual_pair
        P (fun a : Alpha => readout (density a)) hidden
        hReadoutFactor hHiddenFactor

/--
Exact hidden-readout certificate criterion. Once the visible density descends,
descent of the density paired with a hidden readout is equivalent to quotient
compatibility of that hidden readout.
-/
theorem hidden_readout_factor_iff_readout_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Readout : Type w} {Hidden : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (readout : Hidden -> Readout)
    (hDensity : ResidualDensityBridge.QuotientCompatible P density) :
    ResidualDensityBridge.FactorsThroughResidual
      P (fun a : Alpha => (density a, readout (hidden a))) ↔
    ResidualDensityBridge.QuotientCompatible
      P (fun a : Alpha => readout (hidden a)) := by
  constructor
  · intro hJoint
    exact hidden_readout_factor_implies_readout_quotient_compatible
      P density hidden readout hJoint
  · intro hReadout
    have hDensityFactor :
        ResidualDensityBridge.FactorsThroughResidual P density :=
      (ResidualDensityBridge.quotientCompatible_iff_factorsThroughResidual
        P density).mpr hDensity
    have hReadoutFactor :
        ResidualDensityBridge.FactorsThroughResidual
          P (fun a : Alpha => readout (hidden a)) :=
      (ResidualDensityBridge.quotientCompatible_iff_factorsThroughResidual
        P (fun a : Alpha => readout (hidden a))).mpr hReadout
    exact
      ResidualDensityBridge.factorsThroughResidual_pair
        P density (fun a : Alpha => readout (hidden a))
        hDensityFactor hReadoutFactor

/--
Modulo visible-product certificate criterion. Once the visible local diagnostics
are quotient-compatible modulo declared equivalences, augmented product descent
modulo the product equivalence is equivalent to hidden modulo compatibility.
-/
theorem local_pair_mod_factor_iff_hidden_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Hidden : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (left : Alpha -> Rho) (right : Alpha -> Sigma)
    (hidden : Alpha -> Hidden)
    (LeftSetoid : Setoid Rho) (RightSetoid : Setoid Sigma)
    (HiddenSetoid : Setoid Hidden)
    (hLeft : ResidualDensityBridge.QuotientCompatibleMod
      P left LeftSetoid)
    (hRight : ResidualDensityBridge.QuotientCompatibleMod
      P right RightSetoid) :
    ResidualDensityBridge.FactorsThroughResidualMod
      P (fun a : Alpha => ((left a, right a), hidden a))
        (OmegaCore.PrimitiveDifference.productSetoid
          (OmegaCore.PrimitiveDifference.productSetoid
            LeftSetoid RightSetoid)
          HiddenSetoid) ↔
    ResidualDensityBridge.QuotientCompatibleMod P hidden HiddenSetoid := by
  constructor
  · intro hJoint
    exact local_pair_mod_factor_implies_hidden_quotient_compatible
      P left right hidden LeftSetoid RightSetoid HiddenSetoid hJoint
  · intro hHidden
    have hVisibleCompat :
        ResidualDensityBridge.QuotientCompatibleMod
          P (fun a : Alpha => (left a, right a))
          (OmegaCore.PrimitiveDifference.productSetoid
            LeftSetoid RightSetoid) :=
      ResidualDensityBridge.quotientCompatibleMod_pair
        P left right LeftSetoid RightSetoid hLeft hRight
    have hVisibleFactor :
        ResidualDensityBridge.FactorsThroughResidualMod
          P (fun a : Alpha => (left a, right a))
          (OmegaCore.PrimitiveDifference.productSetoid
            LeftSetoid RightSetoid) :=
      (ResidualDensityBridge.quotientCompatibleMod_iff_factorsThroughResidualMod
        P (fun a : Alpha => (left a, right a))
          (OmegaCore.PrimitiveDifference.productSetoid
            LeftSetoid RightSetoid)).mpr hVisibleCompat
    have hHiddenFactor :
        ResidualDensityBridge.FactorsThroughResidualMod
          P hidden HiddenSetoid :=
      (ResidualDensityBridge.quotientCompatibleMod_iff_factorsThroughResidualMod
        P hidden HiddenSetoid).mpr hHidden
    exact
      ResidualDensityBridge.factorsThroughResidualMod_pair
        P (fun a : Alpha => (left a, right a)) hidden
        (OmegaCore.PrimitiveDifference.productSetoid LeftSetoid RightSetoid)
        HiddenSetoid hVisibleFactor hHiddenFactor

/--
Modulo diagnostic-readout certificate criterion. A visible readout that respects
declared equivalences can be paired with hidden data exactly when the hidden
coordinate is quotient-compatible modulo its declared equivalence.
-/
theorem diagnostic_readout_mod_factor_iff_hidden_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Sigma Hidden : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (readout : Rho -> Sigma)
    (hidden : Alpha -> Hidden)
    (DensitySetoid : Setoid Rho) (ReadoutSetoid : Setoid Sigma)
    (HiddenSetoid : Setoid Hidden)
    (hRespect :
      ∀ x y : Rho, DensitySetoid.r x y ->
        ReadoutSetoid.r (readout x) (readout y))
    (hDensity : ResidualDensityBridge.QuotientCompatibleMod
      P density DensitySetoid) :
    ResidualDensityBridge.FactorsThroughResidualMod
      P (fun a : Alpha => (readout (density a), hidden a))
        (OmegaCore.PrimitiveDifference.productSetoid
          ReadoutSetoid HiddenSetoid) ↔
    ResidualDensityBridge.QuotientCompatibleMod P hidden HiddenSetoid := by
  constructor
  · intro hJoint
    exact diagnostic_readout_mod_factor_implies_hidden_quotient_compatible
      P density readout hidden ReadoutSetoid HiddenSetoid hJoint
  · intro hHidden
    have hReadoutCompat :
        ResidualDensityBridge.QuotientCompatibleMod
          P (fun a : Alpha => readout (density a)) ReadoutSetoid :=
      ResidualDensityBridge.quotientCompatibleMod_postprocess
        P density readout DensitySetoid ReadoutSetoid hRespect hDensity
    have hReadoutFactor :
        ResidualDensityBridge.FactorsThroughResidualMod
          P (fun a : Alpha => readout (density a)) ReadoutSetoid :=
      (ResidualDensityBridge.quotientCompatibleMod_iff_factorsThroughResidualMod
        P (fun a : Alpha => readout (density a)) ReadoutSetoid).mpr
        hReadoutCompat
    have hHiddenFactor :
        ResidualDensityBridge.FactorsThroughResidualMod
          P hidden HiddenSetoid :=
      (ResidualDensityBridge.quotientCompatibleMod_iff_factorsThroughResidualMod
        P hidden HiddenSetoid).mpr hHidden
    exact
      ResidualDensityBridge.factorsThroughResidualMod_pair
        P (fun a : Alpha => readout (density a)) hidden
        ReadoutSetoid HiddenSetoid hReadoutFactor hHiddenFactor

/--
Modulo hidden-readout certificate criterion. Once the visible density descends
modulo its declared equivalence, descent of the density paired with a hidden
readout is equivalent to modulo quotient compatibility of that hidden readout.
-/
theorem hidden_readout_mod_factor_iff_readout_quotient_compatible
    {Alpha : Type u} {Beta : Type v} {Rho Hidden Readout : Type w}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (hidden : Alpha -> Hidden)
    (readout : Hidden -> Readout)
    (DensitySetoid : Setoid Rho) (ReadoutSetoid : Setoid Readout)
    (hDensity : ResidualDensityBridge.QuotientCompatibleMod
      P density DensitySetoid) :
    ResidualDensityBridge.FactorsThroughResidualMod
      P (fun a : Alpha => (density a, readout (hidden a)))
        (OmegaCore.PrimitiveDifference.productSetoid
          DensitySetoid ReadoutSetoid) ↔
    ResidualDensityBridge.QuotientCompatibleMod
      P (fun a : Alpha => readout (hidden a)) ReadoutSetoid := by
  constructor
  · intro hJoint
    exact hidden_readout_mod_factor_implies_readout_quotient_compatible
      P density hidden readout DensitySetoid ReadoutSetoid hJoint
  · intro hReadout
    have hDensityFactor :
        ResidualDensityBridge.FactorsThroughResidualMod
          P density DensitySetoid :=
      (ResidualDensityBridge.quotientCompatibleMod_iff_factorsThroughResidualMod
        P density DensitySetoid).mpr hDensity
    have hReadoutFactor :
        ResidualDensityBridge.FactorsThroughResidualMod
          P (fun a : Alpha => readout (hidden a)) ReadoutSetoid :=
      (ResidualDensityBridge.quotientCompatibleMod_iff_factorsThroughResidualMod
        P (fun a : Alpha => readout (hidden a)) ReadoutSetoid).mpr
        hReadout
    exact
      ResidualDensityBridge.factorsThroughResidualMod_pair
        P density (fun a : Alpha => readout (hidden a))
        DensitySetoid ReadoutSetoid hDensityFactor hReadoutFactor

end QLevelLGGRBridge

end QM

#print axioms QM.QLevelLGGRBridge.local_pair_factor_iff_hidden_quotient_compatible
#print axioms QM.QLevelLGGRBridge.diagnostic_readout_factor_iff_hidden_quotient_compatible
#print axioms QM.QLevelLGGRBridge.hidden_readout_factor_iff_readout_quotient_compatible
#print axioms QM.QLevelLGGRBridge.local_pair_mod_factor_iff_hidden_quotient_compatible
#print axioms QM.QLevelLGGRBridge.diagnostic_readout_mod_factor_iff_hidden_quotient_compatible
#print axioms QM.QLevelLGGRBridge.hidden_readout_mod_factor_iff_readout_quotient_compatible
#print axioms QM.QLevelLGGRBridge.local_pair_factor_implies_hidden_quotient_compatible
#print axioms QM.QLevelLGGRBridge.diagnostic_readout_factor_implies_hidden_quotient_compatible
#print axioms QM.QLevelLGGRBridge.hidden_readout_factor_implies_readout_quotient_compatible
#print axioms QM.QLevelLGGRBridge.local_pair_mod_factor_implies_hidden_quotient_compatible
#print axioms QM.QLevelLGGRBridge.diagnostic_readout_mod_factor_implies_hidden_quotient_compatible
#print axioms QM.QLevelLGGRBridge.hidden_readout_mod_factor_implies_readout_quotient_compatible
#print axioms QM.QLevelLGGRBridge.density_lggr_is_q_level_primitive_nonpromotion
#print axioms QM.QLevelLGGRBridge.density_q_bridge_not_authority_certificate
#print axioms QM.QLevelLGGRBridge.density_mod_lggr_is_q_level_primitive_nonpromotion
#print axioms QM.QLevelLGGRBridge.density_mod_q_bridge_not_authority_certificate
#print axioms QM.QLevelLGGRBridge.density_mod_descent_preserved_by_diagnostic_coarsening
#print axioms QM.QLevelLGGRBridge.density_mod_lggr_persists_under_density_coarsening
#print axioms QM.QLevelLGGRBridge.density_mod_authority_firewall_persists_under_density_coarsening
#print axioms QM.QLevelLGGRBridge.local_pair_lggr_is_q_level_primitive_nonpromotion
#print axioms QM.QLevelLGGRBridge.local_pair_q_bridge_not_authority_certificate
#print axioms QM.QLevelLGGRBridge.local_pair_mod_lggr_is_q_level_primitive_nonpromotion
#print axioms QM.QLevelLGGRBridge.local_pair_mod_q_bridge_not_authority_certificate
#print axioms QM.QLevelLGGRBridge.diagnostic_readout_lggr_is_q_level_primitive_nonpromotion
#print axioms QM.QLevelLGGRBridge.hidden_readout_lggr_is_q_level_primitive_nonpromotion
#print axioms QM.QLevelLGGRBridge.diagnostic_readout_mod_lggr_is_q_level_primitive_nonpromotion
#print axioms QM.QLevelLGGRBridge.hidden_readout_mod_lggr_is_q_level_primitive_nonpromotion
#print axioms QM.QLevelLGGRBridge.joint_factor_implies_hidden_quotient_compatible
#print axioms QM.QLevelLGGRBridge.joint_density_authority_factor_implies_authority_quotient_compatible
#print axioms QM.QLevelLGGRBridge.joint_mod_factor_implies_hidden_quotient_compatible
#print axioms QM.QLevelLGGRBridge.joint_mod_density_authority_factor_implies_authority_quotient_compatible