/-!
  # HigherCell.Core — Abstract Additive Trace/Embedding Assumptions
  Explicit hypotheses for k-site additive perturbation spaces, trace maps,
  and tangent embeddings. This is not a concrete density-matrix model.
  AuthorityEffect: None.
-/

namespace HigherCell

/-- Abstract operator space representing perturbations on a k-simplex. -/
structure SimplexOperatorSpace where
  k : Nat
  E : Type
  add : E → E → E
  zero : E
  neg : E → E
  sub : E → E → E

  -- Group axioms
  add_assoc : ∀ a b c : E, add (add a b) c = add a (add b c)
  zero_add : ∀ a : E, add zero a = a
  add_zero : ∀ a : E, add a zero = a
  add_left_neg : ∀ a : E, add (neg a) a = zero
  sub_eq_add_neg : ∀ a b : E, sub a b = add a (neg b)
  add_comm : ∀ a b : E, add a b = add b a
  sub_self : ∀ a : E, sub a a = zero

  -- Local single-site perturbation spaces and maps for each site j < k
  Ej : Nat → Type
  tau : (j : Nat) → E → Ej j
  iota : (j : Nat) → Ej j → E
  zero_Ej : (j : Nat) → Ej j
  add_Ej : (j : Nat) → Ej j → Ej j → Ej j
  zero_add_Ej : ∀ (j : Nat) (a : Ej j), add_Ej j (zero_Ej j) a = a
  add_zero_Ej : ∀ (j : Nat) (a : Ej j), add_Ej j a (zero_Ej j) = a

  -- Additivity of partial traces and embeddings
  tau_add : ∀ (j : Nat) (x y : E), tau j (add x y) = add_Ej j (tau j x) (tau j y)
  tau_zero : ∀ (j : Nat), tau j zero = zero_Ej j
  iota_add : ∀ (j : Nat) (u v : Ej j), iota j (add_Ej j u v) = add (iota j u) (iota j v)
  iota_zero : ∀ (j : Nat), iota j (zero_Ej j) = zero

  -- Fundamental trace-embedding commutation on product states:
  -- Tr_j(iota_j(u)) = u, while Tr_l(iota_j(u)) = 0 for l ≠ j
  tau_iota_same : ∀ (j : Nat) (u : Ej j), tau j (iota j u) = u
  tau_iota_diff : ∀ (j l : Nat) (u : Ej j), j ≠ l → tau l (iota j u) = zero_Ej l

namespace SimplexOperatorSpace

variable (V : SimplexOperatorSpace)

/-- Infix notation helpers for readability. -/
instance : Add V.E where add := V.add
instance : Zero V.E where zero := V.zero
instance : Neg V.E where neg := V.neg
instance : Sub V.E where sub := V.sub

/-- Partial sum of tangent components up to index m: ∑_{j=0}^{m-1} iota_j(tau_j(Z)). -/
def sumTangent (m : Nat) (Z : V.E) : V.E :=
  match m with
  | 0 => V.zero
  | n + 1 => V.add (sumTangent n Z) (V.iota n (V.tau n Z))

/-- The k-cell oblique tangent projector P_sigma(Z) = ∑_{j=0}^{k-1} iota_j(tau_j(Z)). -/
def P_sigma (Z : V.E) : V.E :=
  V.sumTangent V.k Z

/-- The complementary normal projector Q_sigma(Z) = Z - P_sigma(Z). -/
def Q_sigma (Z : V.E) : V.E :=
  V.sub Z (V.P_sigma Z)

end SimplexOperatorSpace

end HigherCell
