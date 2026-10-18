


namespace IsingMajoranaBraiding

universe u

inductive PauliBasis : Type
  | I : PauliBasis
  | X : PauliBasis
  | Y : PauliBasis
  | Z : PauliBasis
deriving DecidableEq, Repr

inductive QuantumStateSector : Type
  | Stabilizer   : QuantumStateSector
  | MagicTState  : QuantumStateSector
deriving DecidableEq, Repr

def blochL1NormScaled : QuantumStateSector → Nat
  | QuantumStateSector.Stabilizer  => 1000
  | QuantumStateSector.MagicTState => 1414

def wignerNegativityScaled : QuantumStateSector → Nat
  | QuantumStateSector.Stabilizer  => 0
  | QuantumStateSector.MagicTState => 207

def nonStabilizerCurvatureScaled : QuantumStateSector → Nat
  | QuantumStateSector.Stabilizer  => 0
  | QuantumStateSector.MagicTState => 765

theorem stabilizer_sector_wigner_nonnegative :
    wignerNegativityScaled QuantumStateSector.Stabilizer = 0 := rfl

theorem stabilizer_sector_cochain_closed :
    nonStabilizerCurvatureScaled QuantumStateSector.Stabilizer = 0 := rfl

theorem stabilizer_octahedron_boundary :
    blochL1NormScaled QuantumStateSector.Stabilizer = 1000 := rfl

theorem magic_state_punctures_octahedron :
    blochL1NormScaled QuantumStateSector.MagicTState > 1000 := by
  dsimp [blochL1NormScaled]
  decide

theorem magic_state_wigner_negative :
    wignerNegativityScaled QuantumStateSector.MagicTState > 0 := by
  dsimp [wignerNegativityScaled]
  decide

theorem magic_state_curvature_positive :
    nonStabilizerCurvatureScaled QuantumStateSector.MagicTState > 0 := by
  dsimp [nonStabilizerCurvatureScaled]
  decide

def totalMagicDefectMass : QuantumStateSector → Nat
  | s => wignerNegativityScaled s + nonStabilizerCurvatureScaled s

theorem magic_defect_mass_positive :
    totalMagicDefectMass QuantumStateSector.MagicTState > 0 := by
  dsimp [totalMagicDefectMass, wignerNegativityScaled, nonStabilizerCurvatureScaled]
  decide

end IsingMajoranaBraiding
