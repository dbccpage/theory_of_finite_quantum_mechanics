

namespace HilbertWalk.DiscretePhaseEstimation

structure GaussInt where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def gz : GaussInt := ⟨0, 0⟩
def gone : GaussInt := ⟨1, 0⟩
def gi : GaussInt := ⟨0, 1⟩

def gadd (x y : GaussInt) : GaussInt :=
  ⟨x.re + y.re, x.im + y.im⟩

def gsub (x y : GaussInt) : GaussInt :=
  ⟨x.re - y.re, x.im - y.im⟩

def gmul (x y : GaussInt) : GaussInt :=
  ⟨x.re * y.re - x.im * y.im, x.re * y.im + x.im * y.re⟩

def gconj (x : GaussInt) : GaussInt :=
  ⟨x.re, -x.im⟩

def normSqG (x : GaussInt) : Int :=
  x.re * x.re + x.im * x.im

instance : Zero GaussInt := ⟨gz⟩
instance : One GaussInt := ⟨gone⟩
instance : Add GaussInt := ⟨gadd⟩
instance : Sub GaussInt := ⟨gsub⟩
instance : Mul GaussInt := ⟨gmul⟩

def ipow (k : Nat) : GaussInt :=
  match k % 4 with
  | 0 => ⟨1, 0⟩
  | 1 => ⟨0, 1⟩
  | 2 => ⟨-1, 0⟩
  | 3 => ⟨0, -1⟩
  | _ => ⟨0, 0⟩

def neg_ipow (k : Nat) : GaussInt :=
  match (4 - (k % 4)) % 4 with
  | 0 => ⟨1, 0⟩
  | 1 => ⟨0, 1⟩
  | 2 => ⟨-1, 0⟩
  | 3 => ⟨0, -1⟩
  | _ => ⟨0, 0⟩

structure Vec4G where
  v0 : GaussInt
  v1 : GaussInt
  v2 : GaussInt
  v3 : GaussInt
  deriving DecidableEq, Repr

def smulG (c : Int) (v : Vec4G) : Vec4G :=
  ⟨⟨v.v0.re * c, v.v0.im * c⟩,
   ⟨v.v1.re * c, v.v1.im * c⟩,
   ⟨v.v2.re * c, v.v2.im * c⟩,
   ⟨v.v3.re * c, v.v3.im * c⟩⟩

def totalNormSq (v : Vec4G) : Int :=
  normSqG v.v0 + normSqG v.v1 + normSqG v.v2 + normSqG v.v3

def e0 : Vec4G := ⟨1, 0, 0, 0⟩
def e1 : Vec4G := ⟨0, 1, 0, 0⟩
def e2 : Vec4G := ⟨0, 0, 1, 0⟩
def e3 : Vec4G := ⟨0, 0, 0, 1⟩

def registerState (k : Nat) : Vec4G :=
  ⟨ipow (k * 0), ipow (k * 1), ipow (k * 2), ipow (k * 3)⟩

def ift_entry (j l : Nat) : GaussInt :=
  neg_ipow (j * l)

def applyIFT (v : Vec4G) : Vec4G :=
  ⟨ift_entry 0 0 * v.v0 + ift_entry 0 1 * v.v1 + ift_entry 0 2 * v.v2 + ift_entry 0 3 * v.v3,
   ift_entry 1 0 * v.v0 + ift_entry 1 1 * v.v1 + ift_entry 1 2 * v.v2 + ift_entry 1 3 * v.v3,
   ift_entry 2 0 * v.v0 + ift_entry 2 1 * v.v1 + ift_entry 2 2 * v.v2 + ift_entry 2 3 * v.v3,
   ift_entry 3 0 * v.v0 + ift_entry 3 1 * v.v1 + ift_entry 3 2 * v.v2 + ift_entry 3 3 * v.v3⟩

theorem phase_est_k0 : applyIFT (registerState 0) = smulG 4 e0 := by decide

theorem phase_est_k1 : applyIFT (registerState 1) = smulG 4 e1 := by decide

theorem phase_est_k2 : applyIFT (registerState 2) = smulG 4 e2 := by decide

theorem phase_est_k3 : applyIFT (registerState 3) = smulG 4 e3 := by decide

theorem prob_one_k0 :
    normSqG (applyIFT (registerState 0)).v0 = 16 ∧
    totalNormSq (applyIFT (registerState 0)) = 16 := by decide

theorem prob_one_k1 :
    normSqG (applyIFT (registerState 1)).v1 = 16 ∧
    totalNormSq (applyIFT (registerState 1)) = 16 := by decide

theorem prob_one_k2 :
    normSqG (applyIFT (registerState 2)).v2 = 16 ∧
    totalNormSq (applyIFT (registerState 2)) = 16 := by decide

theorem prob_one_k3 :
    normSqG (applyIFT (registerState 3)).v3 = 16 ∧
    totalNormSq (applyIFT (registerState 3)) = 16 := by decide

theorem zero_leakage_all_branches :
    (applyIFT (registerState 0)).v1 = 0 ∧
    (applyIFT (registerState 0)).v2 = 0 ∧
    (applyIFT (registerState 0)).v3 = 0 ∧
    (applyIFT (registerState 1)).v0 = 0 ∧
    (applyIFT (registerState 1)).v2 = 0 ∧
    (applyIFT (registerState 1)).v3 = 0 ∧
    (applyIFT (registerState 2)).v0 = 0 ∧
    (applyIFT (registerState 2)).v1 = 0 ∧
    (applyIFT (registerState 2)).v3 = 0 ∧
    (applyIFT (registerState 3)).v0 = 0 ∧
    (applyIFT (registerState 3)).v1 = 0 ∧
    (applyIFT (registerState 3)).v2 = 0 := by decide

def geomSum4 (delta : Nat) : GaussInt :=
  ipow (delta * 0) + ipow (delta * 1) + ipow (delta * 2) + ipow (delta * 3)

theorem geom_sum_4_cancellation :
    geomSum4 1 = 0 ∧
    geomSum4 2 = 0 ∧
    geomSum4 3 = 0 := by decide

theorem geom_sum_4_reinforcement :
    geomSum4 0 = ⟨4, 0⟩ ∧
    geomSum4 4 = ⟨4, 0⟩ := by decide

def binProjectionSum (j k : Nat) : GaussInt :=
  ift_entry j 0 * ipow (k * 0) +
  ift_entry j 1 * ipow (k * 1) +
  ift_entry j 2 * ipow (k * 2) +
  ift_entry j 3 * ipow (k * 3)

theorem dyadic_qft_orthonormality_all_16_pairs :
    binProjectionSum 0 0 = ⟨4, 0⟩ ∧
    binProjectionSum 1 1 = ⟨4, 0⟩ ∧
    binProjectionSum 2 2 = ⟨4, 0⟩ ∧
    binProjectionSum 3 3 = ⟨4, 0⟩ ∧
    binProjectionSum 0 1 = 0 ∧ binProjectionSum 0 2 = 0 ∧ binProjectionSum 0 3 = 0 ∧
    binProjectionSum 1 0 = 0 ∧ binProjectionSum 1 2 = 0 ∧ binProjectionSum 1 3 = 0 ∧
    binProjectionSum 2 0 = 0 ∧ binProjectionSum 2 1 = 0 ∧ binProjectionSum 2 3 = 0 ∧
    binProjectionSum 3 0 = 0 ∧ binProjectionSum 3 1 = 0 ∧ binProjectionSum 3 2 = 0 := by decide

#print axioms phase_est_k0
#print axioms phase_est_k1
#print axioms phase_est_k2
#print axioms phase_est_k3
#print axioms prob_one_k0
#print axioms prob_one_k1
#print axioms prob_one_k2
#print axioms prob_one_k3
#print axioms zero_leakage_all_branches
#print axioms geom_sum_4_cancellation
#print axioms geom_sum_4_reinforcement
#print axioms dyadic_qft_orthonormality_all_16_pairs

end HilbertWalk.DiscretePhaseEstimation


private def l5aProvenance : String :=
  "Origin: lean4/DiscretePhaseEstimation.lean Claim: phase_est_k0 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
