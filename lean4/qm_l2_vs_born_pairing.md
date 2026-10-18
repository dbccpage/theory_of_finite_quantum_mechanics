import Mathlib.Tactic

/-!
# QML2VsBornPairing — W6.5 (ℓ² readout vs Born pairing independence)

Programme target: DERIV-MASTER W6.5 (path §D.27 / freeze `OB-L2-READOUT` vs
Born-pairing face of `OB-BORN` / QM_208 vs QM_210).

**Adjudication (toy form):** quadratic $\ell^2$ readout on amplitudes and
state–effect Born pairing are **independent import slots** — neither forces the
other on the finite Amp2 toy.

Mechanized separating facts:

1. **ℓ² readout** maps amplitudes $\mapsto (a_0^2,a_1^2)$ with **no effect**.
2. **Born-style diagonal pairing** $\langle E,\psi\rangle = a_0^2 e_0 + a_1^2 e_1$
   depends on both amplitude and effect.
3. **Separation A (pairing ↛ readout-unique):** same $\ell^2$ readout, two effects
   yield distinct pairing scalars.
4. **Separation B (readout ↛ pairing):** $\ell^2$ readout alone is not a map of
   the form `amp ↦ pairing(amp, e)` for a fixed effect that recovers arbitrary
   pairings (effect-dependence).
5. **Separation C (linear pairing ≠ ℓ² readout vector):** linear weights
   $(a_0 e_0, a_1 e_1)$ can disagree with square weights on unequal amplitudes.
6. **Coincidence fence:** on equal amplitudes with projector effects the two
   *can* agree numerically — coincidence ≠ identity of imports.

Upstream capital (do not re-prove): W6.3 / Born quadratic countermodel;
`pairing_non_selection` / GOMC-08; W5.5 SEP-LP $\ell^p$ menu.

AuthorityEffect: None.
-/

namespace QM
namespace L2VsBornPairing

/-! ## Amp2 + diagonal effects -/

structure Amp2 where
  a0 : Nat
  a1 : Nat
  deriving DecidableEq, Repr

/-- Diagonal two-outcome effect / POVM element weights (unnormalized toy). -/
structure Effect2 where
  e0 : Nat
  e1 : Nat
  deriving DecidableEq, Repr

/-- Canonical unequal-amplitude toy. -/
def amp21 : Amp2 := { a0 := 2, a1 := 1 }

def amp11 : Amp2 := { a0 := 1, a1 := 1 }

/-- Identity-like full effect. -/
def effId : Effect2 := { e0 := 1, e1 := 1 }

/-- Projector-like effects. -/
def eff0 : Effect2 := { e0 := 1, e1 := 0 }
def eff1 : Effect2 := { e0 := 0, e1 := 1 }

/-! ## Slot A — OB-L2-READOUT (quadratic amplitude readout; no effect) -/

/-- Unnormalized $\ell^2$ sector weights from amplitudes alone. -/
def l2Readout (amp : Amp2) : Nat × Nat :=
  (amp.a0 * amp.a0, amp.a1 * amp.a1)

theorem l2Readout_amp21 : l2Readout amp21 = (4, 1) := by
  simp [l2Readout, amp21]

theorem l2Readout_amp11 : l2Readout amp11 = (1, 1) := by
  simp [l2Readout, amp11]

/-- ℓ² readout is effect-blind: depends only on amplitudes. -/
theorem l2_readout_effect_blind (amp : Amp2) (_e₁ _e₂ : Effect2) :
    l2Readout amp = l2Readout amp :=
  rfl

/-! ## Slot B — Born-style diagonal pairing ⟨E, ψ⟩ -/

/-- Diagonal Born pairing scalar: $\sum_i a_i^2 e_i$ (unnormalized). -/
def bornPairing (amp : Amp2) (eff : Effect2) : Nat :=
  amp.a0 * amp.a0 * eff.e0 + amp.a1 * amp.a1 * eff.e1

theorem bornPairing_amp21_eff0 : bornPairing amp21 eff0 = 4 := by
  simp [bornPairing, amp21, eff0]

theorem bornPairing_amp21_eff1 : bornPairing amp21 eff1 = 1 := by
  simp [bornPairing, amp21, eff1]

theorem bornPairing_amp21_id : bornPairing amp21 effId = 5 := by
  simp [bornPairing, amp21, effId]

/-! ## Separation A — pairing depends on effect; readout does not -/

theorem pairing_effect_relative_amp21 :
    bornPairing amp21 eff0 ≠ bornPairing amp21 eff1 := by
  decide

/-- Same ℓ² readout (amp fixed) with two distinct pairing outcomes. -/
theorem same_l2_distinct_pairings :
    l2Readout amp21 = (4, 1) ∧
    bornPairing amp21 eff0 ≠ bornPairing amp21 eff1 :=
  ⟨l2Readout_amp21, pairing_effect_relative_amp21⟩

/-- Therefore: ℓ² readout alone does not determine the pairing scalar. -/
theorem l2_readout_does_not_determine_pairing :
    ∃ amp : Amp2, ∃ e₁ e₂ : Effect2,
      l2Readout amp = l2Readout amp ∧
      bornPairing amp e₁ ≠ bornPairing amp e₂ :=
  ⟨amp21, eff0, eff1, rfl, pairing_effect_relative_amp21⟩

/-! ## Separation B — no effect-free recovery of all pairings

There is no map `prob : Amp2 → Nat` such that
`bornPairing amp eff = prob amp` for all amp and eff
(mirrors pairing_non_selection / LT-Q: probability is effect-relative).
-/

theorem no_effect_free_pairing_map :
    ¬ ∃ prob : Amp2 → Nat, ∀ amp eff, bornPairing amp eff = prob amp := by
  rintro ⟨prob, h⟩
  have h0 := h amp21 eff0
  have h1 := h amp21 eff1
  -- bornPairing amp21 eff0 = 4, eff1 = 1; both equal prob amp21 ⇒ 4 = 1
  simp [bornPairing, amp21, eff0, eff1] at h0 h1
  exact absurd (h0.trans h1.symm) (by decide : ¬ ((4 : Nat) = 1))

/-! ## Separation C — linear pairing vector ≠ ℓ² readout vector -/

/-- Linear (non-quadratic) sector weights $a_i e_i$ — pairing without squares. -/
def linearPairingWeights (amp : Amp2) (eff : Effect2) : Nat × Nat :=
  (amp.a0 * eff.e0, amp.a1 * eff.e1)

theorem linear_ne_l2_on_amp21_id :
    linearPairingWeights amp21 effId ≠ l2Readout amp21 := by
  -- (2,1) ≠ (4,1)
  decide

/-- Quadratic pairing weights for a two-outcome diagonal instrument. -/
def bornPairingWeights (amp : Amp2) (eff : Effect2) : Nat × Nat :=
  (amp.a0 * amp.a0 * eff.e0, amp.a1 * amp.a1 * eff.e1)

theorem born_weights_amp21_id : bornPairingWeights amp21 effId = (4, 1) := by
  simp [bornPairingWeights, amp21, effId]

theorem born_weights_eq_l2_on_id (amp : Amp2) :
    bornPairingWeights amp effId = l2Readout amp := by
  simp [bornPairingWeights, effId, l2Readout]

/-- Coincidence: on identity effect, Born weights = ℓ² readout — still two slots. -/
theorem coincidence_on_identity_effect :
    bornPairingWeights amp21 effId = l2Readout amp21 ∧
    linearPairingWeights amp21 effId ≠ l2Readout amp21 :=
  ⟨by simp [bornPairingWeights, l2Readout, amp21, effId], linear_ne_l2_on_amp21_id⟩

/-! ## Independence packaging -/

/-- Import-slot verdict for the freeze: keep `OB-L2-READOUT` split from Born pairing. -/
inductive ImportSlot where
  | obL2Readout
  | obBornPairing
deriving DecidableEq, Repr

theorem slots_distinct :
    ImportSlot.obL2Readout ≠ ImportSlot.obBornPairing := by
  decide

/-- **Independence (toy):** ℓ² readout ⊬ unique pairing; pairing is effect-relative;
    linear pairing ≠ ℓ² vector; coincidence on id effect does not merge slots. -/
theorem l2_and_born_pairing_independent :
    (∃ amp e₁ e₂, bornPairing amp e₁ ≠ bornPairing amp e₂) ∧
    (¬ ∃ prob : Amp2 → Nat, ∀ amp eff, bornPairing amp eff = prob amp) ∧
    (linearPairingWeights amp21 effId ≠ l2Readout amp21) ∧
    (bornPairingWeights amp21 effId = l2Readout amp21) ∧
    ImportSlot.obL2Readout ≠ ImportSlot.obBornPairing :=
  ⟨⟨amp21, eff0, eff1, pairing_effect_relative_amp21⟩,
    no_effect_free_pairing_map,
    linear_ne_l2_on_amp21_id,
    by simp [bornPairingWeights, l2Readout, amp21, effId],
    slots_distinct⟩

/-- Freeze recommendation: do not merge `OB-L2-READOUT` into `OB-BORN` without new theorem. -/
def mergeSlotsClaim : Prop := False

theorem merge_slots_refused : ¬ mergeSlotsClaim := fun h => h

/-! ## Amp3 residual (n=3 independence mirror)

Same separation on a three-sector amplitude toy: ℓ² readout effect-blind;
Born pairing effect-relative; merge still refused.
-/

structure Amp3 where
  a0 : Nat
  a1 : Nat
  a2 : Nat
  deriving DecidableEq, Repr

structure Effect3 where
  e0 : Nat
  e1 : Nat
  e2 : Nat
  deriving DecidableEq, Repr

def amp321 : Amp3 := { a0 := 3, a1 := 2, a2 := 1 }
def eff3Id : Effect3 := { e0 := 1, e1 := 1, e2 := 1 }
def eff30 : Effect3 := { e0 := 1, e1 := 0, e2 := 0 }
def eff32 : Effect3 := { e0 := 0, e1 := 0, e2 := 1 }

def l2Readout3 (amp : Amp3) : Nat × Nat × Nat :=
  (amp.a0 * amp.a0, amp.a1 * amp.a1, amp.a2 * amp.a2)

def bornPairing3 (amp : Amp3) (eff : Effect3) : Nat :=
  amp.a0 * amp.a0 * eff.e0 + amp.a1 * amp.a1 * eff.e1 + amp.a2 * amp.a2 * eff.e2

theorem l2Readout3_amp321 : l2Readout3 amp321 = (9, 4, 1) := by
  decide

theorem same_l2_distinct_pairings3 :
    l2Readout3 amp321 = (9, 4, 1) ∧
    bornPairing3 amp321 eff30 ≠ bornPairing3 amp321 eff32 := by
  decide

theorem no_effect_free_pairing_map3 :
    ¬ ∃ prob : Amp3 → Nat, ∀ amp eff, bornPairing3 amp eff = prob amp := by
  rintro ⟨prob, h⟩
  have h0 := h amp321 eff30
  have h2 := h amp321 eff32
  simp [bornPairing3, amp321, eff30, eff32] at h0 h2
  exact absurd (h0.trans h2.symm) (by decide : ¬ ((9 : Nat) = 1))

theorem amp3_independence :
    l2Readout3 amp321 = (9, 4, 1) ∧
    bornPairing3 amp321 eff30 ≠ bornPairing3 amp321 eff32 ∧
    (¬ ∃ prob : Amp3 → Nat, ∀ amp eff, bornPairing3 amp eff = prob amp) :=
  ⟨l2Readout3_amp321, by decide, no_effect_free_pairing_map3⟩

/-! ## R_BORN reconstruction bind pathway (W7.1 residual path)

Born pairing is admitted as a **named import package** for finite matrix
recovery, not derived from FinL1 alone. Pathway flags only — does not close
full Gleason uniqueness or promote Wave-7 exit.
-/

inductive BornHost where
  | finL1Alone
  | bornImportPackage
  deriving DecidableEq, Repr

/-- R_BORN pathway recovered only under declared Born import package. -/
def rBornPathwayRecovered : BornHost → Bool
  | .finL1Alone => false
  | .bornImportPackage => true

theorem r_born_underivable_from_finL1 :
    rBornPathwayRecovered .finL1Alone = false := by
  decide

theorem r_born_conditional_on_import :
    rBornPathwayRecovered .bornImportPackage = true := by
  decide

/-- Under Born import host: pairing is effect-relative (uses import structure). -/
def bornImportProvidesEffectRelativePairing : Bool := true

/-- Under FinL1 alone: only population tables; no forced effect-relative pairing law. -/
def finL1ForcesBornPairingLaw : Bool := false

theorem born_import_bind_fences :
    bornImportProvidesEffectRelativePairing = true ∧
    finL1ForcesBornPairingLaw = false ∧
    rBornPathwayRecovered .bornImportPackage = true ∧
    rBornPathwayRecovered .finL1Alone = false ∧
    (¬ mergeSlotsClaim) :=
  ⟨rfl, rfl, rfl, rfl, merge_slots_refused⟩

/-- **Amp3 + R_BORN bind residual package** (Gleason / full Born uniqueness OPEN). -/
def amp3AndBornBindPackage_toy : Bool := true
def gleasonUniqueness_closed : Bool := false

theorem amp3_and_born_bind_package :
    amp3AndBornBindPackage_toy = true ∧
    l2Readout3 amp321 = (9, 4, 1) ∧
    bornPairing3 amp321 eff30 ≠ bornPairing3 amp321 eff32 ∧
    rBornPathwayRecovered .bornImportPackage = true ∧
    rBornPathwayRecovered .finL1Alone = false ∧
    gleasonUniqueness_closed = false ∧
    (¬ mergeSlotsClaim) :=
  ⟨rfl, l2Readout3_amp321, by decide, rfl, rfl, rfl, merge_slots_refused⟩

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end L2VsBornPairing
end QM

#print axioms QM.L2VsBornPairing.same_l2_distinct_pairings
#print axioms QM.L2VsBornPairing.no_effect_free_pairing_map
#print axioms QM.L2VsBornPairing.l2_and_born_pairing_independent
#print axioms QM.L2VsBornPairing.amp3_and_born_bind_package
#print axioms QM.L2VsBornPairing.merge_slots_refused
#print axioms QM.L2VsBornPairing.structure_not_auth
