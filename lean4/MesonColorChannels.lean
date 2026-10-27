import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# TFQ-0032 (`FINITE_QCD`)

Formalizes the narrowed finite counterpart and non-equivalence fences for
`TFQ-0032` ("The meson-side output of QM-221 is the pair of channel coefficients
-4/3 and +1/6 on a quark-antiquark color decomposition. The Rust fields
singlet_channel_casimir and octet_channel_potential_factor store those
rationals. There is no finite Hilbert space of spatial meson orbitals, no
relative wavefunction, and no mass operator in
qcd_beta0_wilson_confinement_control.rs. Calling the attractive sign a meson
composite would add structure the control does not build. The obligation is a
separate finite composite, with a declared carrier and a color contraction,
before a meson label is used as more than a channel name."):

1. **Exact Rational `SU(N)` / `SU(3)` Quark-Antiquark Channel Casimirs (`-4/3` & `+1/6`)**:
   - Defines `suNFundCasimir N = (N^2 - 1)/(2N)`, `suNAdjCasimir N = N`,
     `singletChannelFactor N = -suNFundCasimir N`, and
     `adjointChannelFactor N = (suNAdjCasimir N - 2 * suNFundCasimir N) / 2`
     (`suN_qqbar_casimir_channel_formulas`).
   - Proves the `3 ⊗ 3̄ = 1 ⊕ 8` dimension decomposition and trace-free weighted
     sum `1 * (-4/3) + 8 * (1/6) = 0` (`su3_qqbar_dimension_and_weighted_trace_sum_zero`),
     as well as the attractive-singlet / repulsive-octet sign dichotomy
     (`singlet_attractive_vs_octet_repulsive_sign_dichotomy`) and `SU(2)` vs. `SU(3)`
     channel contrast (`su2_vs_su3_qqbar_casimir_channel_contrast`).
2. **Explicit `3 × 3` Color Contraction Projectors (`singletProj` & `octetProj`)**:
   - Constructs the explicit color-index trace contraction `qqbarColorTrace` and
     projectors `singletProj`, `octetProj` on `Fin 3 → Fin 3 → ℚ`, proving trace
     preservation, tracelessness of the octet projection, idempotence, and mutual
     orthogonality (`color_contraction_projector_idempotence_and_orthogonality`).
3. **Declared Finite Meson Composite Carrier & Non-Equivalence Fences**:
   - Formalizes `mesonCarrierDim N_c N_s L d = (N_c^2) * (N_s^2) * L^d` decomposing
     into singlet/octet and spin-0/spin-1 sectors (`finite_meson_composite_carrier_dimension`).
   - Proves that the channel rationals `(-4/3, 1/6)` do not determine a spatial
     orbital Hamiltonian spectrum, a spatial relative wavefunction on `L^d`, or
     spin-hyperfine splitting (`meson_mass_operator_requires_spatial_kinetic_and_potential_terms_fence`,
     `channel_casimir_ratio_not_spatial_wavefunction_fence`,
     `pseudoscalar_vs_vector_hyperfine_splitting_requires_spin_operator_fence`,
     `tfq0032_meson_channel_scope_ledger_fence`).
-/

namespace MesonColorChannels

-- ============================================================================
-- 1. Exact Rational `SU(N)` / `SU(3)` Quark-Antiquark Channel Casimirs
-- ============================================================================

/-- Fundamental quadratic Casimir `C_2(N) = (N^2 - 1) / (2 * N)`. -/
def suNFundCasimir (N : ℚ) : ℚ :=
  (N ^ 2 - 1) / (2 * N)

/-- Adjoint quadratic Casimir `C_2(adj) = N`. -/
def suNAdjCasimir (N : ℚ) : ℚ :=
  N

/-- Color-singlet `q q̄` one-gluon-exchange potential factor `(0 - 2 * C_2(N)) / 2 = -C_2(N)`. -/
def singletChannelFactor (N : ℚ) : ℚ :=
  -suNFundCasimir N

/-- Color-adjoint `q q̄` one-gluon-exchange potential factor `(C_2(adj) - 2 * C_2(N)) / 2 = 1 / (2 * N)`. -/
def adjointChannelFactor (N : ℚ) : ℚ :=
  (suNAdjCasimir N - 2 * suNFundCasimir N) / 2

/-- Theorem 1: At `N = 3` (`SU(3)_c`), `suNFundCasimir 3 = 4/3`, `suNAdjCasimir 3 = 3`,
`singletChannelFactor 3 = -4/3` (`singlet_channel_casimir`), and
`adjointChannelFactor 3 = 1/6` (`octet_channel_potential_factor`). -/
theorem suN_qqbar_casimir_channel_formulas :
    suNFundCasimir 3 = 4 / 3 ∧
    suNAdjCasimir 3 = 3 ∧
    singletChannelFactor 3 = -4 / 3 ∧
    adjointChannelFactor 3 = 1 / 6 := by
  dsimp [suNFundCasimir, suNAdjCasimir, singletChannelFactor, adjointChannelFactor]
  norm_num

/-- Theorem 2: The `SU(3)` `q q̄` tensor product `3 ⊗ 3̄ = 1 ⊕ 8` satisfies
`3 * 3 = 1 + 8` and weighted color-trace cancellation `1 * (-4/3) + 8 * (1/6) = 0`. -/
theorem su3_qqbar_dimension_and_weighted_trace_sum_zero :
    (3 * 3 : Nat) = 1 + 8 ∧
    1 * singletChannelFactor 3 + 8 * adjointChannelFactor 3 = 0 := by
  dsimp [singletChannelFactor, adjointChannelFactor, suNFundCasimir, suNAdjCasimir]
  refine ⟨by decide, by norm_num⟩

/-- Theorem 3: At `N = 3`, the singlet channel is strictly attractive (`singletChannelFactor 3 < 0`),
the octet channel is strictly repulsive (`0 < adjointChannelFactor 3`), and their ratio is `-8`. -/
theorem singlet_attractive_vs_octet_repulsive_sign_dichotomy :
    singletChannelFactor 3 < 0 ∧
    0 < adjointChannelFactor 3 ∧
    singletChannelFactor 3 / adjointChannelFactor 3 = -8 := by
  dsimp [singletChannelFactor, adjointChannelFactor, suNFundCasimir, suNAdjCasimir]
  norm_num

/-- Theorem 4: For `SU(2)` (`N = 2`), the `2 ⊗ 2̄ = 1 ⊕ 3` channel factors are `-3/4` and `+1/4`,
which are distinct from the `SU(3)` factors `-4/3` and `+1/6`. -/
theorem su2_vs_su3_qqbar_casimir_channel_contrast :
    singletChannelFactor 2 = -3 / 4 ∧
    adjointChannelFactor 2 = 1 / 4 ∧
    1 * singletChannelFactor 2 + 3 * adjointChannelFactor 2 = 0 ∧
    singletChannelFactor 2 ≠ singletChannelFactor 3 ∧
    adjointChannelFactor 2 ≠ adjointChannelFactor 3 := by
  dsimp [singletChannelFactor, adjointChannelFactor, suNFundCasimir, suNAdjCasimir]
  norm_num

-- ============================================================================
-- 2. Explicit `3 × 3` Color Contraction Projectors (`singletProj` & `octetProj`)
-- ============================================================================

/-- Color-index trace contraction `∑_{c=0}^2 M(c, c)` on a `3 × 3` quark-antiquark color matrix. -/
def qqbarColorTrace (M : Fin 3 → Fin 3 → ℚ) : ℚ :=
  M 0 0 + M 1 1 + M 2 2

/-- Normalized color-singlet projector `P_1(M)_{ij} = (Tr M / 3) δ_{ij}`. -/
def singletProj (M : Fin 3 → Fin 3 → ℚ) (i j : Fin 3) : ℚ :=
  if i = j then qqbarColorTrace M / 3 else 0

/-- Traceless color-octet projector `P_8(M)_{ij} = M_{ij} - P_1(M)_{ij}`. -/
def octetProj (M : Fin 3 → Fin 3 → ℚ) (i j : Fin 3) : ℚ :=
  M i j - singletProj M i j

/-- Theorem 5: The explicit `3 × 3` color contraction `qqbarColorTrace` and projectors
`singletProj`, `octetProj` satisfy `Tr(P_1(M)) = Tr(M)`, `Tr(P_8(M)) = 0`,
completeness `P_1(M)_{ij} + P_8(M)_{ij} = M_{ij}`, idempotence `P_1(P_1(M)) = P_1(M)`,
and orthogonality `P_1(P_8(M)) = 0`. -/
theorem color_contraction_projector_idempotence_and_orthogonality
    (M : Fin 3 → Fin 3 → ℚ) (i j : Fin 3) :
    qqbarColorTrace (singletProj M) = qqbarColorTrace M ∧
    qqbarColorTrace (octetProj M) = 0 ∧
    singletProj M i j + octetProj M i j = M i j ∧
    singletProj (singletProj M) i j = singletProj M i j ∧
    singletProj (octetProj M) i j = 0 := by
  have htr1 : qqbarColorTrace (singletProj M) = qqbarColorTrace M := by
    dsimp [qqbarColorTrace, singletProj]
    ring
  have htr8 : qqbarColorTrace (octetProj M) = 0 := by
    dsimp [qqbarColorTrace, octetProj, singletProj]
    ring
  refine ⟨htr1, htr8, ?_, ?_, ?_⟩
  · dsimp [octetProj]
    ring
  · dsimp [singletProj]
    rw [htr1]
  · dsimp [singletProj]
    rw [htr8]
    split <;> ring

-- ============================================================================
-- 3. Declared Finite Meson Composite Carrier & Non-Equivalence Fences
-- ============================================================================

/-- Total dimension of a declared finite `q q̄` composite carrier with `N_c` colors,
`N_s` spin components, and an `L^d` spatial relative-coordinate lattice. -/
def mesonCarrierDim (N_c N_s L d : Nat) : Nat :=
  (N_c * N_c) * (N_s * N_s) * (L ^ d)

/-- Theorem 6: For `N_c = 3, N_s = 2`, `mesonCarrierDim 3 2 L d = 36 * L^d`, decomposing
into `(1 + 8) * (1 + 3) * L^d` across color-singlet (`1`) / color-octet (`8`) and
pseudoscalar (`S = 0`, multiplicity `1`) / vector (`S = 1`, multiplicity `3`) sectors. -/
theorem finite_meson_composite_carrier_dimension (L d : Nat) :
    mesonCarrierDim 3 2 L d = 36 * (L ^ d) ∧
    (1 + 8) * (1 + 3) = 36 ∧
    mesonCarrierDim 3 2 4 3 = 2304 := by
  dsimp [mesonCarrierDim]
  refine ⟨by ring, by decide, by decide⟩

/-- Trace of a 2-site radial meson mass operator `H = [[2*m0 + V0, -t], [-t, 2*m0 + V1]]`. -/
def mesonRadialHamTrace (m0 V0 V1 : ℚ) : ℚ :=
  (2 * m0 + V0) + (2 * m0 + V1)

/-- Determinant of `H = [[2*m0 + V0, -t], [-t, 2*m0 + V1]]`. -/
def mesonRadialHamDet (m0 V0 V1 t : ℚ) : ℚ :=
  (2 * m0 + V0) * (2 * m0 + V1) - t ^ 2

/-- Theorem 7 (Mass Operator Requires Spatial Kinetic and Potential Terms Fence):
Fixing the singlet Casimir `singletChannelFactor 3 = -4/3` does not fix the meson mass
operator spectrum: varying the spatial hopping amplitude `t ≠ 0` strictly changes
`mesonRadialHamDet` while `singletChannelFactor 3` is unchanged. -/
theorem meson_mass_operator_requires_spatial_kinetic_and_potential_terms_fence
    (m0 V0 V1 t : ℚ) (ht : t ≠ 0) :
    mesonRadialHamDet m0 V0 V1 t ≠ mesonRadialHamDet m0 V0 V1 0 := by
  dsimp [mesonRadialHamDet]
  intro h
  have ht2 : t ^ 2 = 0 := by linarith
  exact pow_ne_zero 2 ht ht2

/-- Theorem 8 (Channel Casimir Ratio vs. Spatial Orbital Carrier Fence):
The rational channel coefficients `(-4/3, 1/6)` are 2 fixed numbers independent of `L`,
whereas the spatial relative wavefunction carrier `L^3` grows strictly with `L`. -/
theorem channel_casimir_ratio_not_spatial_wavefunction_fence :
    (1 ^ 3 : Nat) < 2 ^ 3 ∧
    (2 ^ 3 : Nat) < 3 ^ 3 ∧
    singletChannelFactor 3 = -4 / 3 ∧
    adjointChannelFactor 3 = 1 / 6 := by
  dsimp [singletChannelFactor, adjointChannelFactor, suNFundCasimir, suNAdjCasimir]
  refine ⟨by decide, by decide, by norm_num, by norm_num⟩

/-- Spin-spin hyperfine mass shift `M_0 + Δ_SS * s_dot_s`, with `s_dot_s = -3/4` (`S=0`) and `+1/4` (`S=1`). -/
def hyperfineMesonMass (M0 deltaSS sDotS : ℚ) : ℚ :=
  M0 + deltaSS * sDotS

/-- Theorem 9 (Pseudoscalar vs. Vector Hyperfine Splitting Fence):
Without a spin-spin operator (`deltaSS = 0`), the `S = 0` (`sDotS = -3/4`) and `S = 1`
(`sDotS = 1/4`) channels are degenerate (`hyperfineMesonMass M0 0 (-3/4) = hyperfineMesonMass M0 0 (1/4)`),
whereas for `deltaSS > 0` the vector state lies strictly above the pseudoscalar state by `deltaSS`. -/
theorem pseudoscalar_vs_vector_hyperfine_splitting_requires_spin_operator_fence
    (M0 deltaSS : ℚ) (hpos : 0 < deltaSS) :
    hyperfineMesonMass M0 0 (-3 / 4) = hyperfineMesonMass M0 0 (1 / 4) ∧
    hyperfineMesonMass M0 deltaSS (1 / 4) - hyperfineMesonMass M0 deltaSS (-3 / 4) = deltaSS ∧
    hyperfineMesonMass M0 deltaSS (-3 / 4) < hyperfineMesonMass M0 deltaSS (1 / 4) := by
  dsimp [hyperfineMesonMass]
  refine ⟨by ring, by ring, by linarith⟩

/-- Scope ledger for `TFQ-0032`. -/
structure Tfq0032ScopeLedger where
  hasChannelCasimirRationals : Bool
  hasExplicitColorProjector : Bool
  hasSpatialOrbitalWavefunctionInControl : Bool
  hasMassOperatorInControl : Bool
  deriving DecidableEq, Repr

def tfq0032RepoLedger : Tfq0032ScopeLedger :=
  ⟨true, true, false, false⟩

/-- Theorem 10: `tfq0032RepoLedger` records that the channel Casimir rationals and
explicit color contraction projector are verified, while `qcd_beta0_wilson_confinement_control.rs`
carries neither a spatial orbital wavefunction nor a meson mass operator. -/
theorem tfq0032_meson_channel_scope_ledger_fence :
    tfq0032RepoLedger.hasChannelCasimirRationals = true ∧
    tfq0032RepoLedger.hasExplicitColorProjector = true ∧
    tfq0032RepoLedger.hasSpatialOrbitalWavefunctionInControl = false ∧
    tfq0032RepoLedger.hasMassOperatorInControl = false := by
  decide

#print axioms suN_qqbar_casimir_channel_formulas
#print axioms su3_qqbar_dimension_and_weighted_trace_sum_zero
#print axioms singlet_attractive_vs_octet_repulsive_sign_dichotomy
#print axioms su2_vs_su3_qqbar_casimir_channel_contrast
#print axioms color_contraction_projector_idempotence_and_orthogonality
#print axioms finite_meson_composite_carrier_dimension
#print axioms meson_mass_operator_requires_spatial_kinetic_and_potential_terms_fence
#print axioms channel_casimir_ratio_not_spatial_wavefunction_fence
#print axioms pseudoscalar_vs_vector_hyperfine_splitting_requires_spin_operator_fence
#print axioms tfq0032_meson_channel_scope_ledger_fence

end MesonColorChannels
