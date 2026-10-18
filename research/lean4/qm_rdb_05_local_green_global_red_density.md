import «residual_density_bridge»
import «l010_01_born_redundancy»

/-!
RDB-05: local-green/global-red density bridge.

This file packages the observer-forgetting theorem in density language and
adds the existing PaperQF002 finite sign-flip witness as a concrete model.
-/

namespace QM

namespace RDB05

universe u v w z

open ResidualDensityBridge

theorem localGreen_globalRed_marginal_density
    {Alpha : Type u} {Beta : Type v} {Rho : Type w} {Hidden : Type z}
    (P : OmegaCore.PrimitiveDifference Alpha Beta)
    (joint : Alpha -> Rho × Hidden)
    (hMarginal : QuotientCompatible P (fun x : Alpha => (joint x).1))
    {x y : Alpha} (hxy : P.ZeroRel x y)
    (hHidden : (joint x).2 ≠ (joint y).2) :
    FactorsThroughResidual P (fun x : Alpha => (joint x).1) ∧
      ¬ FactorsThroughResidual P joint := by
  exact
    marginal_factor_not_joint_factor_of_hidden_witness
      P joint hMarginal hxy hHidden

theorem pairPhaseBlind_localGreen_globalRed_witness :
    (∃ F : PaperQF002.pairPhaseBlindPrimitiveDifference.ResidualQuotient -> ℚ × ℚ,
        ∀ p : ℚ × ℚ,
          F (PaperQF002.pairPhaseBlindPrimitiveDifference.classOf p) =
            (PaperQF002.pairLocalGlobalDiagnostic p).1) ∧
      ¬ (∃ F :
          PaperQF002.pairPhaseBlindPrimitiveDifference.ResidualQuotient ->
            (ℚ × ℚ) × (ℚ × ℚ),
          ∀ p : ℚ × ℚ,
            F (PaperQF002.pairPhaseBlindPrimitiveDifference.classOf p) =
              PaperQF002.pairLocalGlobalDiagnostic p) := by
  exact PaperQF002.pairLocalGlobalDiagnostic_lggr_quotient_obstruction

end RDB05

end QM

#print axioms QM.RDB05.localGreen_globalRed_marginal_density
#print axioms QM.RDB05.pairPhaseBlind_localGreen_globalRed_witness
