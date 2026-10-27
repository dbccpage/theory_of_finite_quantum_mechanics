/-!
Rational arithmetic for the imported EPRL label formulas.

`jPlus` and `jMinus` are the absolute values `(1 + gamma).abs * k / 2`
and `(1 - gamma).abs * k / 2`.
`nLorentz` and `rhoLorentz` are `2 * k` and `2 * gamma * k`.
No 15j symbol, booster, continuum representation, spin sum,
continuum limit, semiclassical limit, or cosmological constant
is constructed.

This module imports only the Lean core. The pinned Mathlib checkout
is not required for these identities.
-/

namespace LqgEprlVertexImport

def jPlus (gamma k : Rat) : Rat := (1 + gamma).abs * k / 2

def jMinus (gamma k : Rat) : Rat := (1 - gamma).abs * k / 2

def nLorentz (k : Rat) : Rat := 2 * k

def rhoLorentz (gamma k : Rat) : Rat := 2 * gamma * k

theorem euclidean_below (gamma k : Rat) (h0 : 0 < gamma) (h1 : gamma < 1) :
    jPlus gamma k = (1 + gamma) * k / 2 ∧
      jMinus gamma k = (1 - gamma) * k / 2 ∧
        jPlus gamma k + jMinus gamma k = k ∧
          jPlus gamma k - jMinus gamma k = gamma * k := by
  have hone : (0 : Rat) ≤ 1 := Rat.le_of_lt (by decide)
  have hp : 0 ≤ 1 + gamma := Rat.add_nonneg hone (Rat.le_of_lt h0)
  have hm : 0 ≤ 1 - gamma := (Rat.le_iff_sub_nonneg gamma 1).mp (Rat.le_of_lt h1)
  unfold jPlus jMinus
  rw [Rat.abs_of_nonneg hp, Rat.abs_of_nonneg hm]
  refine ⟨rfl, rfl, ?_, ?_⟩
  · grind
  · grind

theorem euclidean_above (gamma k : Rat) (h1 : 1 < gamma) :
    jPlus gamma k = (1 + gamma) * k / 2 ∧
      jMinus gamma k = (gamma - 1) * k / 2 ∧
        jPlus gamma k - jMinus gamma k = k ∧
          jPlus gamma k + jMinus gamma k = gamma * k := by
  have hone : (0 : Rat) ≤ 1 := Rat.le_of_lt (by decide)
  have hge : (1 : Rat) ≤ gamma := Rat.le_of_lt h1
  have hp : 0 ≤ 1 + gamma := Rat.add_nonneg hone (Rat.le_trans hone hge)
  have hm : 0 ≤ gamma - 1 := (Rat.le_iff_sub_nonneg 1 gamma).mp hge
  have hsub : (1 : Rat) - gamma = -(gamma - 1) := by grind
  unfold jPlus jMinus
  rw [Rat.abs_of_nonneg hp, hsub, Rat.abs_neg, Rat.abs_of_nonneg hm]
  refine ⟨rfl, rfl, ?_, ?_⟩
  · grind
  · grind

theorem recorded_euclidean_points :
    jPlus (1 / 2) 2 = 3 / 2 ∧
      jMinus (1 / 2) 2 = 1 / 2 ∧
        jPlus (1 / 2) 2 + jMinus (1 / 2) 2 = 2 ∧
          jPlus (1 / 2) 2 - jMinus (1 / 2) 2 = 1 ∧
            jPlus (1 / 2) 2 - jMinus (1 / 2) 2 ≠ (2 : Rat) ∧
              jPlus (3 : Rat) 2 = 4 ∧
                jMinus (3 : Rat) 2 = 2 ∧
                  jPlus (3 : Rat) 2 - jMinus (3 : Rat) 2 = 2 ∧
                    jPlus (3 : Rat) 2 + jMinus (3 : Rat) 2 = 6 ∧
                      jPlus (3 : Rat) 2 + jMinus (3 : Rat) 2 ≠ (2 : Rat) ∧
                        jPlus 1 2 = 2 ∧
                          jMinus 1 2 = 0 ∧
                            jPlus 1 2 + jMinus 1 2 = 2 ∧
                              jPlus 1 2 - jMinus 1 2 = 2 := by
  have hhalf0 : (0 : Rat) < 1 / 2 := by grind
  have hhalf1 : (1 : Rat) / 2 < 1 := by grind
  have habove : (1 : Rat) < 3 := by grind
  have hlow := euclidean_below (1 / 2) 2 hhalf0 hhalf1
  have hhigh := euclidean_above 3 2 habove
  have hlowPlus : jPlus (1 / 2) 2 = 3 / 2 := by
    rw [hlow.1]
    grind
  have hlowMinus : jMinus (1 / 2) 2 = 1 / 2 := by
    rw [hlow.2.1]
    grind
  have hhighPlus : jPlus 3 2 = 4 := by
    rw [hhigh.1]
    grind
  have hhighMinus : jMinus 3 2 = 2 := by
    rw [hhigh.2.1]
    grind
  have hone : (0 : Rat) ≤ 1 := Rat.le_of_lt (by decide)
  have hboundaryPos : 0 ≤ (1 : Rat) + 1 := Rat.add_nonneg hone hone
  have hboundaryNeg : 0 ≤ (1 : Rat) - 1 := by
    rw [Rat.sub_self]
    exact Rat.le_refl (a := 0)
  have hboundaryPlus : jPlus 1 2 = 2 := by
    unfold jPlus
    rw [Rat.abs_of_nonneg hboundaryPos]
    grind
  have hboundaryMinus : jMinus 1 2 = 0 := by
    unfold jMinus
    rw [Rat.abs_of_nonneg hboundaryNeg]
    grind
  refine ⟨hlowPlus, hlowMinus, ?_, ?_, ?_, hhighPlus, hhighMinus, ?_, ?_, ?_,
      hboundaryPlus, hboundaryMinus, ?_, ?_⟩
  · rw [hlow.2.2.1]
  · have hdiff : jPlus (1 / 2) 2 - jMinus (1 / 2) 2 = (1 : Rat) / 2 * 2 := hlow.2.2.2
    rw [hdiff]
    grind
  · rw [hlow.2.2.2]
    grind
  · rw [hhigh.2.2.1]
  · rw [hhigh.2.2.2]
    grind
  · rw [hhigh.2.2.2]
    grind
  · rw [hboundaryPlus, hboundaryMinus]
    grind
  · rw [hboundaryPlus, hboundaryMinus]
    grind

theorem lorentzian_embedding (gamma k : Rat) :
    nLorentz k = 2 * k ∧
      rhoLorentz gamma k = 2 * gamma * k ∧
        nLorentz k / 2 = k ∧
          rhoLorentz gamma k = gamma * nLorentz k ∧
            rhoLorentz gamma k = 2 * gamma * (nLorentz k / 2) := by
  unfold nLorentz rhoLorentz
  refine ⟨rfl, rfl, ?_, ?_, ?_⟩
  · grind
  · grind
  · grind

theorem lorentzian_half_two :
    nLorentz 2 = 4 ∧
      rhoLorentz (1 / 2) 2 = 2 ∧
        nLorentz 2 / 2 = 2 ∧
          (1 / 2 : Rat) * (nLorentz 2 / 2) = 1 ∧
            rhoLorentz (1 / 2) 2 = 2 * ((1 / 2 : Rat) * (nLorentz 2 / 2)) := by
  unfold nLorentz rhoLorentz
  grind

theorem five_tetrahedron_pairs : 5 * (5 - 1) / 2 = 10 := by
  decide

#print axioms LqgEprlVertexImport.euclidean_below
#print axioms LqgEprlVertexImport.euclidean_above
#print axioms LqgEprlVertexImport.recorded_euclidean_points
#print axioms LqgEprlVertexImport.lorentzian_embedding
#print axioms LqgEprlVertexImport.lorentzian_half_two
#print axioms LqgEprlVertexImport.five_tetrahedron_pairs

end LqgEprlVertexImport
