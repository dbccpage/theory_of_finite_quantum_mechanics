/-!
LT-K / LT-Q — pairing non-selection: the compatibility skeleton does not single out
Born, and no probability exists without the imported pairing.

Paper: `08_state_effect_pairing_audit.md` (O024); `11_…` T4; `01_…` §2.

Two finite firewalls about the state/effect pairing:

* **LT-K (O024 non-uniqueness).** A probability pairing is modelled as outcome
  weights `(ℕ × ℕ)`; the declared compatibility slice is normalization to a fixed
  total (positivity is free over `ℕ`). The slice admits two distinct pairings, so
  it does **not** uniquely select one — in particular it does not single out a
  designated Born pairing.
* **LT-Q (no Born without pairing).** Outcome probability is the operational pairing
  `⟨E, ρ⟩` of an effect with a state. For a fixed state it varies with the effect,
  so there is **no** map assigning a probability to a state independently of the
  effect: the amplitude/state carries no probability content without the imported
  pairing.

No Born rule is derived; no authority minted. Mathlib-free (core `Nat`/`Prod`).
-/

namespace QM

/-! ## LT-K — the compatibility skeleton does not uniquely select Born -/

/-- A probability pairing over two outcomes: `(weight₀, weight₁)`. -/
abbrev Pairing := Nat × Nat

/-- The declared compatibility slice: normalization to a fixed total (positivity is
free over `ℕ`). A finite model of the O024 state/effect compatibility skeleton. -/
def Compatible (total : Nat) (p : Pairing) : Prop := p.1 + p.2 = total

/-- A designated Born-like (uniform) pairing, normalized to `2`. -/
def bornUniform : Pairing := (1, 1)

/-- **O024 non-uniqueness.** The compatibility slice admits two distinct pairings —
normalization does not single out one pairing. -/
theorem compatible_not_unique :
    ∃ p1 p2 : Pairing, Compatible 2 p1 ∧ Compatible 2 p2 ∧ p1 ≠ p2 := by
  refine ⟨(1, 1), (2, 0), ?_, ?_, ?_⟩
  · unfold Compatible; decide
  · unfold Compatible; decide
  · decide

/-- The designated Born pairing is not forced: another compatible pairing exists. -/
theorem born_not_selected :
    ∃ p : Pairing, Compatible 2 p ∧ p ≠ bornUniform := by
  refine ⟨(2, 0), ?_, ?_⟩
  · unfold Compatible; decide
  · decide

/-! ## LT-Q — no Born probability without the imported pairing -/

/-- The operational pairing `⟨E, ρ⟩` of an effect with a state (its bilinear shadow). -/
def pairing (state effect : Nat) : Nat := state * effect

/-- Outcome probability is effect-relative: a fixed state yields different outcome
weights under different effects. -/
theorem probability_is_pairing_relative :
    ∃ state e1 e2 : Nat, pairing state e1 ≠ pairing state e2 := by
  refine ⟨1, 1, 2, ?_⟩
  unfold pairing; decide

/-- **No Born without pairing.** There is no map assigning a probability to a state
independently of the effect — the pairing genuinely depends on the effect, so the
amplitude/state alone carries no probability content. -/
theorem no_probability_without_pairing :
    ¬ ∃ prob : Nat → Nat, ∀ state effect : Nat, pairing state effect = prob state := by
  rintro ⟨prob, h⟩
  have h1 : pairing 1 1 = prob 1 := h 1 1
  have h2 : pairing 1 2 = prob 1 := h 1 2
  unfold pairing at h1 h2
  omega

end QM

#print axioms QM.compatible_not_unique
#print axioms QM.born_not_selected
#print axioms QM.probability_is_pairing_relative
#print axioms QM.no_probability_without_pairing
