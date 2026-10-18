import Mathlib.Data.Fintype.Basic

/-!
# GHZ all-or-nothing: no local-realist assignment (cycle 011, QM_029 neighborhood)

A finite, recognizable nonlocality brick (distinct from the Mermin–Peres square of QM_029). The
three-party GHZ correlations are `⟨XYY⟩ = ⟨YXY⟩ = ⟨YYX⟩ = +1` and `⟨XXX⟩ = −1`. No deterministic
±1 local assignment of the X- and Y-outcomes can reproduce all four — multiplying the three `+1`
constraints forces `x₁x₂x₃ = +1`, contradicting the fourth (`= −1`).

This is the **classical / local-realism** impossibility (an all-or-nothing GHZ contradiction). It is
not a claim about the quantum state, nor a derivation of QM. No authority minted (LGGR). `decide`.
-/

namespace QM.GHZ

/-- Sign of a bit: `true ↦ +1`, `false ↦ −1`. -/
def s (b : Bool) : ℤ := if b then 1 else -1

/-- **GHZ all-or-nothing.** No deterministic ±1 local assignment `(x₁,x₂,x₃,y₁,y₂,y₃)` satisfies all
four GHZ correlations simultaneously — they are jointly unsatisfiable. -/
theorem ghz_no_local :
    ∀ x₁ x₂ x₃ y₁ y₂ y₃ : Bool,
      ¬ (s x₁ * s y₂ * s y₃ = 1 ∧
         s y₁ * s x₂ * s y₃ = 1 ∧
         s y₁ * s y₂ * s x₃ = 1 ∧
         s x₁ * s x₂ * s x₃ = -1) := by decide

end QM.GHZ

#print axioms QM.GHZ.ghz_no_local
