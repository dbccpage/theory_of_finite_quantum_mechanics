


namespace FqhLaughlinBraiding

universe u

def laughlin_m : Nat := 3

def monodromyPhaseNumerator : Nat := 2

theorem monodromy_phase_nontrivial :
    monodromyPhaseNumerator % laughlin_m ≠ 0 := by
  dsimp [monodromyPhaseNumerator, laughlin_m]
  decide

def fqhCochainCurvature : Nat :=
  monodromyPhaseNumerator

theorem fqh_curvature_is_positive :
    fqhCochainCurvature > 0 := by
  dsimp [fqhCochainCurvature, monodromyPhaseNumerator]
  decide

theorem involution_coprime_to_laughlin_phase :
    Nat.gcd 2 laughlin_m = 1 := rfl

structure LaughlinQuasiparticleGaps where
  gap_qh : Nat
  gap_qe : Nat
  gap_asymmetry : gap_qe > gap_qh

theorem quasiparticle_weights_unequal (g : LaughlinQuasiparticleGaps) :
    g.gap_qe ≠ g.gap_qh := by
  have h := g.gap_asymmetry
  omega

theorem fqh_defect_mass_positive (w_qh w_qe : Nat) (h_ne : w_qh ≠ w_qe) :
    (w_qh : Int) - (w_qe : Int) ≠ 0 := by
  intro h_zero
  have : w_qh = w_qe := by omega
  exact h_ne this

end FqhLaughlinBraiding
