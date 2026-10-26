/-!
Finite Bool-by-Bool slice of the imported tensor-product target.
AuthorityEffect: None.
The module has no import.
-/

namespace CampaignGpImportTensorProduct

def delta {α : Type} [DecidableEq α] (i q : α) : Int :=
  if i = q then 1 else 0

def tensor (u v : Bool → Int) : Bool × Bool → Int
  | (a, b) => u a * v b

def dumpRight (u v : Bool → Int) : Bool × Bool → Int
  | (a, false) => u a * (v false + v true)
  | (_, true) => 0

structure BilinearKroneckerEmbed where
  embed : (Bool → Int) → (Bool → Int) → (Bool × Bool → Int)
  add_left :
    ∀ u1 u2 v p,
      embed (fun q => u1 q + u2 q) v p = embed u1 v p + embed u2 v p
  add_right :
    ∀ u v1 v2 p,
      embed u (fun q => v1 q + v2 q) p = embed u v1 p + embed u v2 p
  smul_left :
    ∀ (c : Int) u v p,
      embed (fun q => c * u q) v p = c * embed u v p
  smul_right :
    ∀ (c : Int) u v p,
      embed u (fun q => c * v q) p = c * embed u v p
  kronecker :
    ∀ i j p,
      embed (delta i) (delta j) p = delta (i, j) p

theorem tensor_pointwise (u v : Bool → Int) (a b : Bool) :
    tensor u v (a, b) = u a * v b := rfl

theorem bool_expand (u : Bool → Int) (q : Bool) :
    u q = u false * delta false q + u true * delta true q := by
  cases q <;> simp [delta]

theorem tensor_on_deltas (i j a b : Bool) :
    tensor (delta i) (delta j) (a, b) = delta (i, j) (a, b) := by
  cases i <;> cases j <;> cases a <;> cases b <;> simp [tensor, delta]

theorem tensor_add_left (u1 u2 v : Bool → Int) (p : Bool × Bool) :
    tensor (fun q => u1 q + u2 q) v p = tensor u1 v p + tensor u2 v p := by
  rcases p with ⟨a, b⟩
  simp only [tensor]
  exact Int.add_mul (u1 a) (u2 a) (v b)

theorem tensor_add_right (u v1 v2 : Bool → Int) (p : Bool × Bool) :
    tensor u (fun q => v1 q + v2 q) p = tensor u v1 p + tensor u v2 p := by
  rcases p with ⟨a, b⟩
  simp only [tensor]
  exact Int.mul_add (u a) (v1 b) (v2 b)

theorem tensor_smul_left (c : Int) (u v : Bool → Int) (p : Bool × Bool) :
    tensor (fun q => c * u q) v p = c * tensor u v p := by
  rcases p with ⟨a, b⟩
  simp only [tensor]
  exact Int.mul_assoc c (u a) (v b)

theorem tensor_smul_right (c : Int) (u v : Bool → Int) (p : Bool × Bool) :
    tensor u (fun q => c * v q) p = c * tensor u v p := by
  rcases p with ⟨a, b⟩
  simp only [tensor]
  rw [← Int.mul_assoc, Int.mul_comm (u a) c, Int.mul_assoc]

def tensorEmbed : BilinearKroneckerEmbed where
  embed := tensor
  add_left := tensor_add_left
  add_right := tensor_add_right
  smul_left := tensor_smul_left
  smul_right := tensor_smul_right
  kronecker := fun i j p => by
    rcases p with ⟨a, b⟩
    exact tensor_on_deltas i j a b

theorem embed_eq_tensor (E : BilinearKroneckerEmbed) (u v : Bool → Int) (p : Bool × Bool) :
    E.embed u v p = tensor u v p := by
  rcases p with ⟨a, b⟩
  have hu : u = fun q =>
      u false * delta false q + u true * delta true q :=
    funext (bool_expand u)
  have hv : v = fun q =>
      v false * delta false q + v true * delta true q :=
    funext (bool_expand v)
  rw [hu, hv]
  have hL :=
    E.add_left
      (fun q => u false * delta false q)
      (fun q => u true * delta true q)
      (fun q => v false * delta false q + v true * delta true q) (a, b)
  rw [hL]
  have hf :=
    E.smul_left (u false) (delta false)
      (fun q => v false * delta false q + v true * delta true q) (a, b)
  have ht :=
    E.smul_left (u true) (delta true)
      (fun q => v false * delta false q + v true * delta true q) (a, b)
  rw [hf, ht]
  have hfR :=
    E.add_right (delta false)
      (fun q => v false * delta false q)
      (fun q => v true * delta true q) (a, b)
  have htR :=
    E.add_right (delta true)
      (fun q => v false * delta false q)
      (fun q => v true * delta true q) (a, b)
  rw [hfR, htR]
  have hf0 := E.smul_right (v false) (delta false) (delta false) (a, b)
  have hf1 := E.smul_right (v true) (delta false) (delta true) (a, b)
  have ht0 := E.smul_right (v false) (delta true) (delta false) (a, b)
  have ht1 := E.smul_right (v true) (delta true) (delta true) (a, b)
  rw [hf0, hf1, ht0, ht1]
  rw [E.kronecker false false (a, b), E.kronecker false true (a, b),
    E.kronecker true false (a, b), E.kronecker true true (a, b)]
  cases a <;> cases b <;> simp [tensor, delta, Int.mul_zero, Int.mul_one, Int.add_zero, Int.zero_add]

theorem dumpRight_false_coord (u v : Bool → Int) (a : Bool) :
    dumpRight u v (a, false) = u a * (v false + v true) := rfl

theorem dumpRight_true_coord (u v : Bool → Int) (a : Bool) :
    dumpRight u v (a, true) = 0 := rfl

theorem dumpRight_add_left (u1 u2 v : Bool → Int) (p : Bool × Bool) :
    dumpRight (fun q => u1 q + u2 q) v p = dumpRight u1 v p + dumpRight u2 v p := by
  rcases p with ⟨a, b⟩
  cases b
  · exact Int.add_mul (u1 a) (u2 a) (v false + v true)
  · rfl

theorem dumpRight_add_right (u v1 v2 : Bool → Int) (p : Bool × Bool) :
    dumpRight u (fun q => v1 q + v2 q) p = dumpRight u v1 p + dumpRight u v2 p := by
  rcases p with ⟨a, b⟩
  cases b
  · have hsum :
        (v1 false + v2 false) + (v1 true + v2 true) =
          (v1 false + v1 true) + (v2 false + v2 true) := by
      omega
    change u a * ((v1 false + v2 false) + (v1 true + v2 true)) =
      u a * (v1 false + v1 true) + u a * (v2 false + v2 true)
    rw [hsum, Int.mul_add]
  · rfl

theorem dumpRight_smul_left (c : Int) (u v : Bool → Int) (p : Bool × Bool) :
    dumpRight (fun q => c * u q) v p = c * dumpRight u v p := by
  rcases p with ⟨a, b⟩
  cases b
  · exact Int.mul_assoc c (u a) (v false + v true)
  · exact (Int.mul_zero c).symm

theorem dumpRight_smul_right (c : Int) (u v : Bool → Int) (p : Bool × Bool) :
    dumpRight u (fun q => c * v q) p = c * dumpRight u v p := by
  rcases p with ⟨a, b⟩
  cases b
  · change u a * (c * v false + c * v true) = c * (u a * (v false + v true))
    rw [← Int.mul_add, ← Int.mul_assoc, Int.mul_comm (u a) c, Int.mul_assoc]
  · exact (Int.mul_zero c).symm

theorem dumpRight_collapsed_tag (i j : Bool) (p : Bool × Bool) :
    dumpRight (delta i) (delta j) p = delta (i, false) p := by
  rcases p with ⟨a, b⟩
  cases b
  · have hsum : delta j false + delta j true = 1 := by
      cases j <;> simp [delta]
    change delta i a * (delta j false + delta j true) = delta (i, false) (a, false)
    rw [hsum, Int.mul_one]
    cases i <;> cases a <;> simp [delta]
  · change (0 : Int) = delta (i, false) (a, true)
    cases i <;> cases a <;> simp [delta]

theorem witness_tensor_one :
    tensor (delta false) (delta true) (false, true) = 1 := by
  simp [tensor, delta]

theorem witness_dump_zero :
    dumpRight (delta false) (delta true) (false, true) = 0 := rfl

theorem dumpRight_ne_tensor :
    dumpRight (delta false) (delta true) (false, true) ≠
      tensor (delta false) (delta true) (false, true) := by
  rw [witness_dump_zero, witness_tensor_one]
  decide

theorem dumpRight_not_always_tensor :
    ¬ ∀ u v p, dumpRight u v p = tensor u v p := by
  intro h
  exact dumpRight_ne_tensor (h (delta false) (delta true) (false, true))

#print axioms tensor_pointwise
#print axioms bool_expand
#print axioms tensor_on_deltas
#print axioms embed_eq_tensor
#print axioms dumpRight_false_coord
#print axioms dumpRight_true_coord
#print axioms dumpRight_add_left
#print axioms dumpRight_add_right
#print axioms dumpRight_smul_left
#print axioms dumpRight_smul_right
#print axioms dumpRight_collapsed_tag
#print axioms witness_tensor_one
#print axioms witness_dump_zero
#print axioms dumpRight_ne_tensor
#print axioms dumpRight_not_always_tensor

end CampaignGpImportTensorProduct
