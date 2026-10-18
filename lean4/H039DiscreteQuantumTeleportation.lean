

namespace FableHilbertWalk20260819.H039

structure Mat2 where
  a : Int
  b : Int
  c : Int
  d : Int
  deriving DecidableEq, Repr

def mul (m1 m2 : Mat2) : Mat2 :=
  ⟨m1.a * m2.a + m1.b * m2.c,
   m1.a * m2.b + m1.b * m2.d,
   m1.c * m2.a + m1.d * m2.c,
   m1.c * m2.b + m1.d * m2.d⟩

def eye2 : Mat2 := ⟨1, 0, 0, 1⟩
def sigmaX : Mat2 := ⟨0, 1, 1, 0⟩
def sigmaZ : Mat2 := ⟨1, 0, 0, -1⟩
def sigmaXZ : Mat2 := mul sigmaX sigmaZ
def sigmaZX : Mat2 := mul sigmaZ sigmaX

theorem sigma_x_squared : mul sigmaX sigmaX = eye2 := by decide

theorem sigma_z_squared : mul sigmaZ sigmaZ = eye2 := by decide

theorem zx_xz_product : mul sigmaZX sigmaXZ = eye2 := by decide

inductive TeleportOutcome where
  | branch00
  | branch01
  | branch10
  | branch11
  deriving DecidableEq, Repr

def bobChannel : TeleportOutcome → Mat2
  | .branch00 => eye2
  | .branch01 => sigmaX
  | .branch10 => sigmaZ
  | .branch11 => sigmaXZ

def bobRecovery : TeleportOutcome → Mat2
  | .branch00 => eye2
  | .branch01 => sigmaX
  | .branch10 => sigmaZ
  | .branch11 => sigmaZX

theorem branch00_exact_recovery : mul (bobRecovery .branch00) (bobChannel .branch00) = eye2 := by decide

theorem branch01_exact_recovery : mul (bobRecovery .branch01) (bobChannel .branch01) = eye2 := by decide

theorem branch10_exact_recovery : mul (bobRecovery .branch10) (bobChannel .branch10) = eye2 := by decide

theorem branch11_exact_recovery : mul (bobRecovery .branch11) (bobChannel .branch11) = eye2 := by decide

theorem all_branches_teleport_identity :
    (mul (bobRecovery .branch00) (bobChannel .branch00) = eye2) ∧
    (mul (bobRecovery .branch01) (bobChannel .branch01) = eye2) ∧
    (mul (bobRecovery .branch10) (bobChannel .branch10) = eye2) ∧
    (mul (bobRecovery .branch11) (bobChannel .branch11) = eye2) := by decide

theorem classical_bit_capacity : (2 : Int) ^ 2 = 4 := by decide

#print axioms sigma_x_squared
#print axioms sigma_z_squared
#print axioms zx_xz_product
#print axioms all_branches_teleport_identity
#print axioms classical_bit_capacity

end FableHilbertWalk20260819.H039

private def l5aProvenance : String :=
  "Origin: lean4/H039DiscreteQuantumTeleportation.lean Claim: sigma_x_squared AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
