


namespace NonAbelianGaugeSigns

universe u


inductive Su2FluxSector : Type
  | Sector0 : Su2FluxSector
  | Sector1 : Su2FluxSector
deriving DecidableEq, Repr

def su2_sign : Su2FluxSector → Int
  | Su2FluxSector.Sector0 => 1
  | Su2FluxSector.Sector1 => -1

theorem su2_action_gap_forces_weight_inequality (w0 delta_S : Nat) (h_gap : delta_S > 0) :
    w0 ≠ w0 + delta_S := by
  omega

theorem su2_disjoint_weights_nonzero_residual (w0 delta_S : Nat) (h_gap : delta_S > 0) :
    (w0 : Int) * su2_sign Su2FluxSector.Sector0 +
    ((w0 + delta_S : Nat) : Int) * su2_sign Su2FluxSector.Sector1 ≠ 0 := by
  dsimp [su2_sign]
  intro h_zero
  omega


inductive HadronTopology : Type
  | Meson  : HadronTopology
  | Baryon : HadronTopology
deriving DecidableEq, Repr

def hadronCochainCurvature : HadronTopology → Nat
  | HadronTopology.Meson  => 0
  | HadronTopology.Baryon => 5

theorem meson_cochain_is_closed :
    hadronCochainCurvature HadronTopology.Meson = 0 := rfl

theorem baryon_cochain_is_open :
    hadronCochainCurvature HadronTopology.Baryon > 0 := by
  dsimp [hadronCochainCurvature]
  decide


inductive PolyakovCenterSector : Type
  | Trivial  : PolyakovCenterSector
  | Clockwise: PolyakovCenterSector
  | Counter  : PolyakovCenterSector
deriving DecidableEq, Repr

theorem polyakov_deconfinement_action_gap (h P : Nat) (h_field : h > 0) (h_ord : P > 0) :
    18 * h * P > 0 := by
  have h1 : 18 * h > 0 := Nat.mul_pos (by decide) h_field
  exact Nat.mul_pos h1 h_ord

theorem polyakov_sector_weights_distinct (base_weight h P : Nat)
    (h_field : h > 0) (h_ord : P > 0) :
    base_weight ≠ base_weight + (18 * h * P) := by
  have h_gap := polyakov_deconfinement_action_gap h P h_field h_ord
  omega


inductive ColorRepresentation : Type
  | Fundamental : ColorRepresentation
  | Adjoint     : ColorRepresentation
deriving DecidableEq, Repr

def n_ality (N_c : Nat) : ColorRepresentation → Nat
  | ColorRepresentation.Fundamental => 1 % N_c
  | ColorRepresentation.Adjoint     => 0

def fluxTubeCurvature (N_c : Nat) (rep : ColorRepresentation) : Nat :=
  n_ality N_c rep

theorem adjoint_matter_zero_n_ality (N_c : Nat) :
    n_ality N_c ColorRepresentation.Adjoint = 0 := rfl

theorem adjoint_flux_tube_curvature_vanishes (N_c : Nat) :
    fluxTubeCurvature N_c ColorRepresentation.Adjoint = 0 := rfl

theorem fundamental_flux_tube_curvature_nonzero (N_c : Nat) (h_nc : N_c ≥ 2) :
    fluxTubeCurvature N_c ColorRepresentation.Fundamental > 0 := by
  dsimp [fluxTubeCurvature, n_ality]
  have h_lt : 1 < N_c := by omega
  rw [Nat.mod_eq_of_lt h_lt]
  decide

end NonAbelianGaugeSigns
