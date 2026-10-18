/-!
  FrustratedSpectrumObstruction.lean — Jordan-Wigner Fermionic Path Signs and
  Disjoint Weight Spectra Obstruction on Frustrated Geometries

  Status: FORMAL LEAN 4 SPECIFICATION & THEOREM REGISTER
  AuthorityEffect: None
  Primary Reference: `sealed-derivation-v1` (`3100c4e`), `code/hamiltonian_gin_bridge.py`
  Claims: `GIN-C2`, `GIN-C3`, `GIN-C4`, `INV-GIN-PARITY`, `INV-DISJOINT-SPEC`

  Formalizes:
  1. Fermionic imaginary-time Trotter paths with Jordan-Wigner permutation signs.
  2. Bipartite sign cancellation under equal-weight involution pairing (GIN-C3).
  3. Disjoint weight spectra on frustrated geometries (e.g. 3-site triangle cluster).
  4. The Disjoint Weight Incompatibility Theorem (`INV-DISJOINT-SPEC`):
     disjoint positive and negative weight spectra obstruct any weight-preserving
     involution, leaving uncancelled defect mass Φ₁ > 0 and routing to SplitBrainRefusal.
-/

namespace FrustratedSpectrumObstruction

universe u

/-- Jordan-Wigner sign for many-body fermionic Trotter paths: +1 or -1. -/
inductive JwSign : Type
  | Plus  : JwSign
  | Minus : JwSign
deriving DecidableEq, Repr

def toInt : JwSign → Int
  | JwSign.Plus  => 1
  | JwSign.Minus => -1

/-- A fermionic Trotter path with declared Boltzmann weight and Jordan-Wigner sign. -/
structure TrotterPath (P : Type u) where
  weight : P → Nat
  sign : P → JwSign

/--
  Bipartite Lattice Involution Pairing:
  Every negative path p_neg is mapped to an equal-weight positive partner.
-/
structure BipartiteInvolution {P : Type u} (T : TrotterPath P) where
  xi : P → P
  xi_involutive : ∀ p, xi (xi p) = p
  weight_preserving : ∀ p, T.weight (xi p) = T.weight p
  sign_reversing : ∀ p, T.sign (xi p) = match T.sign p with
    | JwSign.Plus  => JwSign.Minus
    | JwSign.Minus => JwSign.Plus

/-- Theorem (Claim `GIN-C3`): Bipartite involution partners cancel identically in signed sum. -/
theorem bipartite_pair_exact_cancellation {P : Type u} {T : TrotterPath P}
    (inv : BipartiteInvolution T) (p : P) :
    (T.weight p : Int) * toInt (T.sign p) +
    (T.weight (inv.xi p) : Int) * toInt (T.sign (inv.xi p)) = 0 := by
  have hw := inv.weight_preserving p
  have hs := inv.sign_reversing p
  rw [hw]
  cases h_sign : T.sign p
  · rw [hs, h_sign]
    dsimp [toInt]
    rw [Int.mul_neg, Int.add_right_neg]
  · rw [hs, h_sign]
    dsimp [toInt]
    rw [Int.mul_neg, Int.add_left_neg]

/--
  Disjoint Weight Spectra Predicate (Claim `GIN-C4` / `INV-DISJOINT-SPEC`):
  On frustrated geometries (such as the 3-site triangle cluster),
  no positive path shares a Boltzmann weight with any negative path.
-/
def DisjointWeightSpectra {P : Type u} (T : TrotterPath P) : Prop :=
  ∀ (p_pos p_neg : P),
    T.sign p_pos = JwSign.Plus →
    T.sign p_neg = JwSign.Minus →
    T.weight p_pos ≠ T.weight p_neg

/--
  The Disjoint Weight Incompatibility Theorem:
  If a fermionic path system has at least one positive path and one negative path,
  and its weight spectra are disjoint, then NO weight-preserving,
  sign-reversing involution can exist.
-/
theorem disjoint_spectra_obstructs_involution {P : Type u} (T : TrotterPath P)
    (h_disj : DisjointWeightSpectra T)
    (p_minus : P) (h_minus : T.sign p_minus = JwSign.Minus) :
    ¬ (∃ (_inv : BipartiteInvolution T), True) := by
  intro ⟨I, _⟩
  have h_sign := I.sign_reversing p_minus
  rw [h_minus] at h_sign
  dsimp at h_sign
  have h_ne := h_disj (I.xi p_minus) p_minus h_sign h_minus
  have h_eq := I.weight_preserving p_minus
  exact h_ne h_eq

/--
  Theorem: Residual Defect Mass Positivity under Disjoint Spectra.
  When weights are disjoint, any candidate paired sum between positive and negative paths
  leaves a strictly non-zero signed residual mass.
-/
theorem disjoint_pair_residual_nonzero (w_pos w_neg : Nat) (h_ne : w_pos ≠ w_neg) :
    (w_pos : Int) * toInt JwSign.Plus + (w_neg : Int) * toInt JwSign.Minus ≠ 0 := by
  dsimp [toInt]
  intro h_zero
  have h_eq : (w_pos : Int) = (w_neg : Int) := by omega
  exact h_ne (Int.ofNat_inj.mp h_eq)

end FrustratedSpectrumObstruction
