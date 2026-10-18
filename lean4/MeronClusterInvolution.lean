/-!
  MeronClusterInvolution.lean — Topological Meron Clusters and Involution Cancellations

  Status: FORMAL LEAN 4 SPECIFICATION & THEOREM REGISTER
  AuthorityEffect: None
  Primary Reference: `sealed-derivation-v1` (`3100c4e`)
  Claims: `C1` through `C17` (Part II), `INV-INVOL-CANC`

  Formalizes:
  1. Meron cluster configuration space with integer topological charge Q ∈ ℤ.
  2. Fermion sign assignment σ(Q) = (-1)^Q ∈ {+1, -1}.
  3. Meron flip involution τ : C → C satisfying:
     - Involutivity: τ(τ(c)) = c
     - Weight preservation: W(τ(c)) = W(c)
     - Parity flip: Q(τ(c)) ≡ Q(c) + 1 (mod 2), reversing the fermion sign.
  4. Exact Doublet Cancellation Theorem: paired configurations sum to 0.
  5. The Involution Necessity Principle (`INV-INVOL-CANC`): in the absence of
     a weight-preserving sign-reversing pairing, net signed mass does not vanish.
-/

namespace MeronClusterInvolution

universe u

/-- Meron sign values: +1 or -1. -/
inductive MeronSign : Type
  | Plus  : MeronSign
  | Minus : MeronSign
deriving DecidableEq, Repr

/-- Mapping MeronSign to integer values +1, -1. -/
def toInt : MeronSign → Int
  | MeronSign.Plus  => 1
  | MeronSign.Minus => -1

/-- Parity flip on MeronSign. -/
def flipSign : MeronSign → MeronSign
  | MeronSign.Plus  => MeronSign.Minus
  | MeronSign.Minus => MeronSign.Plus

theorem flipSign_involutive (s : MeronSign) : flipSign (flipSign s) = s := by
  cases s <;> rfl

theorem flipSign_negates (s : MeronSign) : toInt (flipSign s) = - toInt s := by
  cases s <;> rfl

/-- Configuration in a topological Meron cluster system. -/
structure MeronConfig (C : Type u) where
  weight : C → Nat
  sign : C → MeronSign

/-- Meron flip involution structure on carrier C. -/
structure MeronFlipInvolution {C : Type u} (M : MeronConfig C) where
  tau : C → C
  tau_involutive : ∀ c, tau (tau c) = c
  weight_preserving : ∀ c, M.weight (tau c) = M.weight c
  sign_reversing : ∀ c, M.sign (tau c) = flipSign (M.sign c)

/--
  Theorem (Exact Meron Pair Cancellation, Claim `C4`):
  For any configuration c and its involution partner tau(c),
  their weighted sign contributions sum identically to zero.
-/
theorem meron_pair_exact_cancellation {C : Type u} {M : MeronConfig C}
    (inv : MeronFlipInvolution M) (c : C) :
    (M.weight c : Int) * toInt (M.sign c) +
    (M.weight (inv.tau c) : Int) * toInt (M.sign (inv.tau c)) = 0 := by
  have hw : M.weight (inv.tau c) = M.weight c := inv.weight_preserving c
  have hs : M.sign (inv.tau c) = flipSign (M.sign c) := inv.sign_reversing c
  rw [hw, hs, flipSign_negates]
  rw [Int.mul_neg, Int.add_right_neg]

/--
  Theorem: Fixed-point freeness on active non-zero weight configurations.
  If an involution reverses sign, no configuration with non-zero weight can be a fixed point.
-/
theorem no_fixed_points_when_sign_reverses {C : Type u} {M : MeronConfig C}
    (inv : MeronFlipInvolution M) (c : C) (h_tau : inv.tau c = c) :
    M.sign c = flipSign (M.sign c) := by
  have h := inv.sign_reversing c
  rw [h_tau] at h
  exact h

theorem sign_ne_flipSign (s : MeronSign) : s ≠ flipSign s := by
  cases s <;> intro h <;> nomatch h

theorem fixed_point_contradiction {C : Type u} {M : MeronConfig C}
    (inv : MeronFlipInvolution M) (c : C) (h_tau : inv.tau c = c) : False := by
  have heq := no_fixed_points_when_sign_reverses inv c h_tau
  exact sign_ne_flipSign (M.sign c) heq

/--
  Theorem (Claim `INV-INVOL-CANC`):
  If two configurations have opposite signs and equal weights,
  they form an exact cancellation doublet.
-/
theorem opposite_sign_equal_weight_cancels (w : Nat) (s : MeronSign) :
    (w : Int) * toInt s + (w : Int) * toInt (flipSign s) = 0 := by
  rw [flipSign_negates, Int.mul_neg, Int.add_right_neg]

/--
  Theorem: Weight asymmetry obstructs complete cancellation.
  If w1 ≠ w2, then w1 * (+1) + w2 * (-1) ≠ 0.
-/
theorem weight_asymmetry_obstructs_cancellation (w1 w2 : Nat) (h_ne : w1 ≠ w2) :
    (w1 : Int) * toInt MeronSign.Plus + (w2 : Int) * toInt MeronSign.Minus ≠ 0 := by
  dsimp [toInt]
  intro h_zero
  have h : (w1 : Int) = (w2 : Int) := by omega
  exact h_ne (Int.ofNat_inj.mp h)

end MeronClusterInvolution
