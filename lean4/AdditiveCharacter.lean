import SharedKernelAdditiveCharacter

/-!
MUB compatibility shim: additive-character cancellation now lives in
`SharedKernelAdditiveCharacter`. Re-exported here under `namespace MUB` so
existing MUB modules keep compiling unchanged.
-/

namespace MUB

export SharedKernel (
  finite_sum_eq_scaled_sum_from_translation
  finite_character_sum_vanishes_from_nontrivial_translation
)

end MUB

#print axioms MUB.finite_sum_eq_scaled_sum_from_translation
#print axioms MUB.finite_character_sum_vanishes_from_nontrivial_translation
