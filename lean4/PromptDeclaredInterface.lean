import Mathlib.Tactic.NormNum

/- Operations and laws below are supplied assumptions. They do not select
   quantum mechanics from primitive difference. Exact examples use real-rational
   entries in the admitted complex framework. AuthorityEffect: None. -/
namespace QuantumMechanics.PromptDeclaredInterface
structure Inputs (K V State Effect : Type) where
  inner : V → V → K
  positiveState : State → Prop
  admissibleEffect : Effect → Prop
  pairing : State → Effect → ℚ
  unit : Effect
  tensor : State → State → State
  channel : State → State
  step : State → State
  record : State → Type
  normalized : ∀ s, positiveState s → pairing s unit = 1
  channel_positive : ∀ s, positiveState s → positiveState (channel s)

theorem normalization_consumes_supplied_law {K V S E : Type}
    (i : Inputs K V S E) (s : S) (hs : i.positiveState s) :
    i.pairing s i.unit = 1 := i.normalized s hs
theorem admitted_channel_composes {K V S E : Type}
    (i : Inputs K V S E) (s : S) (hs : i.positiveState s) :
    i.positiveState (i.channel (i.channel s)) :=
  i.channel_positive _ (i.channel_positive _ hs)
theorem concrete_density_trace_and_Born :
    (9/25 : ℚ) + 16/25 = 1 ∧
    (9/25 : ℚ)*1 + (12/25)*0 + (12/25)*0 + (16/25)*0 = 9/25 := by norm_num
theorem concrete_pinching_preserves_trace :
    (9/25 : ℚ) + 16/25 = 1 ∧ (9/25 : ℚ)*(16/25)-(12/25)^2 = 0 := by norm_num
theorem supplied_rotation_is_orthogonal :
    (3/5 : ℚ)^2+(4/5)^2=1 ∧ (3/5 : ℚ)*(-4/5)+(4/5)*(3/5)=0 := by norm_num
end QuantumMechanics.PromptDeclaredInterface
#print axioms QuantumMechanics.PromptDeclaredInterface.normalization_consumes_supplied_law
#print axioms QuantumMechanics.PromptDeclaredInterface.admitted_channel_composes
#print axioms QuantumMechanics.PromptDeclaredInterface.concrete_density_trace_and_Born
#print axioms QuantumMechanics.PromptDeclaredInterface.concrete_pinching_preserves_trace
#print axioms QuantumMechanics.PromptDeclaredInterface.supplied_rotation_is_orthogonal
