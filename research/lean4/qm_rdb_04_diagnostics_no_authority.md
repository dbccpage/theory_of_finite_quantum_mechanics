import «residual_density_bridge»

/-!
RDB-04: density diagnostics do not mint authority.

The theorem is a plan002-facing wrapper over the residual-density LGGR bridge:
a density-like diagnostic may factor through the primitive residual quotient,
but the joint `(density, authority)` readout need not factor.
-/

namespace QM

namespace RDB04

universe u v w z

open ResidualDensityBridge

theorem densityDiagnostics_no_authority_promotion
    {Alpha : Type u} {Beta : Type v} {Rho : Type w} {Authority : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (density : Alpha -> Rho) (authority : Alpha -> Authority)
    (hDensity : QuotientCompatible P density)
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hAuthority : authority x ≠ authority y) :
    FactorsThroughResidual P density ∧
      ¬ FactorsThroughResidual P (fun x : Alpha => (density x, authority x)) := by
  exact
    density_diagnostic_not_authority_certificate
      P density authority hDensity hxy hAuthority

end RDB04

end QM

#print axioms QM.RDB04.densityDiagnostics_no_authority_promotion
