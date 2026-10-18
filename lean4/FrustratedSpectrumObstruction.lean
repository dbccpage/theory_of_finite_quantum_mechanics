


namespace FrustratedSpectrumObstruction

universe u

inductive JwSign : Type
  | Plus  : JwSign
  | Minus : JwSign
deriving DecidableEq, Repr

def toInt : JwSign → Int
  | JwSign.Plus  => 1
  | JwSign.Minus => -1

structure TrotterPath (P : Type u) where
  weight : P → Nat
  sign : P → JwSign

structure BipartiteInvolution {P : Type u} (T : TrotterPath P) where
  xi : P → P
  xi_involutive : ∀ p, xi (xi p) = p
  weight_preserving : ∀ p, T.weight (xi p) = T.weight p
  sign_reversing : ∀ p, T.sign (xi p) = match T.sign p with
    | JwSign.Plus  => JwSign.Minus
    | JwSign.Minus => JwSign.Plus

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

def DisjointWeightSpectra {P : Type u} (T : TrotterPath P) : Prop :=
  ∀ (p_pos p_neg : P),
    T.sign p_pos = JwSign.Plus →
    T.sign p_neg = JwSign.Minus →
    T.weight p_pos ≠ T.weight p_neg

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

theorem disjoint_pair_residual_nonzero (w_pos w_neg : Nat) (h_ne : w_pos ≠ w_neg) :
    (w_pos : Int) * toInt JwSign.Plus + (w_neg : Int) * toInt JwSign.Minus ≠ 0 := by
  dsimp [toInt]
  intro h_zero
  have h_eq : (w_pos : Int) = (w_neg : Int) := by omega
  exact h_ne (Int.ofNat_inj.mp h_eq)

end FrustratedSpectrumObstruction
