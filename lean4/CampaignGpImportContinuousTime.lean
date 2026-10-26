-- Campaign GP-IMPORT-CONTINUOUS-TIME.
-- Boolean toggle and two Gaussian-integer interpolants at scale 4.
-- AuthorityEffect: None.

namespace CampaignGpImportContinuousTime

def toggle (q : Bool) : Bool := !q

theorem toggle_images : toggle false = true ∧ toggle true = false :=
  ⟨rfl, rfl⟩

theorem no_toggle_square_root :
    ¬ ∃ σ : Bool → Bool, ∀ q : Bool, σ (σ q) = toggle q := by
  intro h
  rcases h with ⟨σ, hσ⟩
  cases hff : σ false with
  | false =>
      have h1 := hσ false
      rw [hff, hff] at h1
      cases h1
  | true =>
      cases hft : σ true with
      | false =>
          have h1 := hσ false
          rw [hff, hft] at h1
          cases h1
      | true =>
          have h1 := hσ true
          rw [hft, hft] at h1
          cases h1

abbrev G := Int × Int

def gAdd (x y : G) : G := (x.1 + y.1, x.2 + y.2)

def gMul (x y : G) : G := (x.1 * y.1 - x.2 * y.2, x.1 * y.2 + x.2 * y.1)

def gNeg (x : G) : G := (-x.1, -x.2)

theorem gAdd_coords (a b c d : Int) :
    gAdd (a, b) (c, d) = (a + c, b + d) := rfl

theorem gMul_coords (a b c d : Int) :
    gMul (a, b) (c, d) = (a * c - b * d, a * d + b * c) := rfl

abbrev Amp := G × G

def swapAmp (v : Amp) : Amp := (v.2, v.1)

theorem swap_exchanges (x y : G) : swapAmp (x, y) = (y, x) := rfl

def scale4 (v : Amp) : Amp := (gMul (4, 0) v.1, gMul (4, 0) v.2)

def interp (v : Amp) : Amp :=
  (gAdd (gMul (1, 1) v.1) (gMul (1, -1) v.2),
    gAdd (gMul (1, -1) v.1) (gMul (1, 1) v.2))

def interpNeg (v : Amp) : Amp := (gNeg (interp v).1, gNeg (interp v).2)

theorem scale4_swap (v : Amp) :
    swapAmp (scale4 v) = (gMul (4, 0) v.2, gMul (4, 0) v.1) := rfl

theorem interp_twice_is_scaled_swap (af bf aT bT : Int) :
    interp (interp ((af, bf), (aT, bT))) = swapAmp (scale4 ((af, bf), (aT, bT))) := by
  simp [interp, scale4, swapAmp, gAdd, gMul]
  constructor
  · constructor <;> omega
  · constructor <;> omega

theorem interpNeg_twice_is_scaled_swap (af bf aT bT : Int) :
    interpNeg (interpNeg ((af, bf), (aT, bT))) = swapAmp (scale4 ((af, bf), (aT, bT))) := by
  simp [interpNeg, interp, scale4, swapAmp, gAdd, gMul, gNeg]
  constructor
  · constructor <;> omega
  · constructor <;> omega

theorem witness_interp : interp ((1, 0), (0, 0)) = ((1, 1), (1, -1)) := by
  unfold interp gAdd gMul
  decide

theorem witness_neg : interpNeg ((1, 0), (0, 0)) = ((-1, -1), (-1, 1)) := by
  unfold interpNeg interp gNeg gAdd gMul
  decide

theorem interpolants_differ :
    interp ((1, 0), (0, 0)) ≠ interpNeg ((1, 0), (0, 0)) := by
  rw [witness_interp, witness_neg]
  decide

#print axioms toggle_images
#print axioms no_toggle_square_root
#print axioms gAdd_coords
#print axioms gMul_coords
#print axioms swap_exchanges
#print axioms scale4_swap
#print axioms interp_twice_is_scaled_swap
#print axioms interpNeg_twice_is_scaled_swap
#print axioms witness_interp
#print axioms witness_neg
#print axioms interpolants_differ

end CampaignGpImportContinuousTime
