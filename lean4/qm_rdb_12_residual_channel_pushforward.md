import «rdb_01_normalized_residual_weights»
import «rdb_07_channel_diagnostics_no_authority»

/-!
RDB-12: residual-density channel pushforward.

A finite row-stochastic channel can move residual mass between diagnostic
sectors while preserving total mass. This is a diagnostic learning/update
operator only; it does not create authority.
-/

open scoped BigOperators

namespace QM

namespace RDB12

noncomputable section

variable {Source Target : Type*} [Fintype Source] [Fintype Target]

/-- A finite residual channel is a nonnegative row-stochastic kernel from source
sectors to target sectors. -/
def RowStochasticResidualChannel (K : Source -> Target -> ℚ) : Prop :=
  ∀ s, (∀ t, 0 ≤ K s t) ∧ ∑ t, K s t = 1

/-- Push residual mass forward through a finite stochastic channel. -/
def pushforwardMass (mass : Source -> ℚ) (K : Source -> Target -> ℚ)
    (t : Target) : ℚ :=
  ∑ s, mass s * K s t

/-- Total mass after row-stochastic pushforward equals total mass before the
channel. -/
theorem pushforward_totalMass_eq
    (mass : Source -> ℚ) (K : Source -> Target -> ℚ)
    (hK : RowStochasticResidualChannel K) :
    ∑ t, pushforwardMass mass K t = ∑ s, mass s := by
  calc
    ∑ t, pushforwardMass mass K t
        = ∑ t, ∑ s, mass s * K s t := by
          rfl
    _ = ∑ s, ∑ t, mass s * K s t := by
          rw [Finset.sum_comm]
    _ = ∑ s, mass s := by
          apply Finset.sum_congr rfl
          intro s _
          calc
            ∑ t, mass s * K s t
                = mass s * ∑ t, K s t := by
                  rw [Finset.mul_sum]
            _ = mass s := by
                  rw [(hK s).2, mul_one]

theorem pushforward_nonnegative
    (mass : Source -> ℚ) (K : Source -> Target -> ℚ)
    (hmass : ∀ s, 0 ≤ mass s)
    (hK : RowStochasticResidualChannel K)
    (t : Target) :
    0 ≤ pushforwardMass mass K t := by
  unfold pushforwardMass
  exact Finset.sum_nonneg (fun s _ => mul_nonneg (hmass s) ((hK s).1 t))

/-- Runtime channel reports remain diagnostic-only even when input density,
channel validity, and output density are all valid. -/
theorem channelPushforwardDiagnostic_not_authority :
    ¬ (∀ s : RDB07.ChannelSituation,
      RDB07.ChannelDiagnosticValid s -> RDB07.ChannelAuthorityTerminal s) := by
  exact RDB07.not_channelDiagnosticValid_implies_authority

end

end RDB12

end QM

#print axioms QM.RDB12.pushforward_totalMass_eq
#print axioms QM.RDB12.pushforward_nonnegative
#print axioms QM.RDB12.channelPushforwardDiagnostic_not_authority
