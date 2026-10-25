/-!
TFQ-0313, narrowed finite case. AuthorityEffect: None.

Carrier: the 16-element module (Z/4Z)^2.
Endomorphisms are 2×2 matrices with entries in Fin 4.
A = [[0, 1], [0, 0]], B = [[0, 0], [1, 0]].
AB = [[1, 0], [0, 0]], BA = [[0, 0], [0, 1]],
AB - BA = [[1, 0], [0, 3]].
The diagonal pair diag(1, 2) and diag(3, 1) commute, with product diag(3, 2).
A is not a scalar matrix. The coefficient ring satisfies 1+1+1+1 = 0 and 1 ≠ 0.

This file does not fill the QM_202 stub, does not treat a continuum operator
algebra, and does not identify the carrier with the Gaussian integers.
-/

namespace CampaignTfq0313OperatorAlgebraShadow

structure M where
  a : Fin 4
  b : Fin 4
  c : Fin 4
  d : Fin 4
  deriving DecidableEq, Repr

@[ext]
structure V where
  x : Fin 4
  y : Fin 4
  deriving DecidableEq, Repr

def vadd (v w : V) : V := ⟨v.x + w.x, v.y + w.y⟩

def vsmul (s : Fin 4) (v : V) : V := ⟨s * v.x, s * v.y⟩

def vsub (v w : V) : V := ⟨v.x - w.x, v.y - w.y⟩

def apply (m : M) (v : V) : V :=
  ⟨m.a * v.x + m.b * v.y, m.c * v.x + m.d * v.y⟩

def mmul (p q : M) : M where
  a := p.a * q.a + p.b * q.c
  b := p.a * q.b + p.b * q.d
  c := p.c * q.a + p.d * q.c
  d := p.c * q.b + p.d * q.d

def msub (p q : M) : M where
  a := p.a - q.a
  b := p.b - q.b
  c := p.c - q.c
  d := p.d - q.d

def A : M := ⟨0, 1, 0, 0⟩

def B : M := ⟨0, 0, 1, 0⟩

def D : M := ⟨1, 0, 0, 2⟩

def E : M := ⟨3, 0, 0, 1⟩

def scalar (s : Fin 4) : M := ⟨s, 0, 0, s⟩

def e0 : V := ⟨1, 0⟩

theorem A_on (v : V) : apply A v = ⟨v.y, 0⟩ := by
  cases v with
  | mk x y =>
    ext <;> decide +revert

theorem B_on (v : V) : apply B v = ⟨0, v.x⟩ := by
  cases v with
  | mk x y =>
    ext <;> decide +revert

theorem A_additive (v w : V) : apply A (vadd v w) = vadd (apply A v) (apply A w) := by
  cases v with
  | mk x y =>
    cases w with
    | mk x' y' =>
      ext <;> decide +revert

theorem B_additive (v w : V) : apply B (vadd v w) = vadd (apply B v) (apply B w) := by
  cases v with
  | mk x y =>
    cases w with
    | mk x' y' =>
      ext <;> decide +revert

theorem A_homogeneous (s : Fin 4) (v : V) : apply A (vsmul s v) = vsmul s (apply A v) := by
  cases v with
  | mk x y =>
    ext <;> decide +revert

theorem B_homogeneous (s : Fin 4) (v : V) : apply B (vsmul s v) = vsmul s (apply B v) := by
  cases v with
  | mk x y =>
    ext <;> decide +revert

theorem ab_matrix : mmul A B = ⟨1, 0, 0, 0⟩ := by
  rfl

theorem ba_matrix : mmul B A = ⟨0, 0, 0, 1⟩ := by
  rfl

theorem commutator_matrix : msub (mmul A B) (mmul B A) = ⟨1, 0, 0, 3⟩ := by
  rfl

theorem ab_ne_ba : mmul A B ≠ mmul B A := by
  decide

theorem ab_matches_composition (v : V) : apply (mmul A B) v = apply A (apply B v) := by
  cases v with
  | mk x y =>
    ext <;> decide +revert

theorem ba_matches_composition (v : V) : apply (mmul B A) v = apply B (apply A v) := by
  cases v with
  | mk x y =>
    ext <;> decide +revert

theorem actions_differ_on_e0 : apply A (apply B e0) ≠ apply B (apply A e0) := by
  decide

theorem left_action_e0 : apply A (apply B e0) = ⟨1, 0⟩ := by
  decide

theorem right_action_e0 : apply B (apply A e0) = ⟨0, 0⟩ := by
  decide

theorem commutator_on_e0 :
    vsub (apply A (apply B e0)) (apply B (apply A e0)) = ⟨1, 0⟩ := by
  decide

theorem diagonals_commute : mmul D E = mmul E D := by
  rfl

theorem diagonal_product : mmul D E = ⟨3, 0, 0, 2⟩ := by
  rfl

theorem A_not_scalar (s : Fin 4) : A ≠ scalar s := by
  decide +revert

theorem coeff_char_four : (1 : Fin 4) + 1 + 1 + 1 = 0 ∧ (1 : Fin 4) ≠ 0 := by
  decide

def allV : List V :=
  [⟨0, 0⟩, ⟨0, 1⟩, ⟨0, 2⟩, ⟨0, 3⟩,
   ⟨1, 0⟩, ⟨1, 1⟩, ⟨1, 2⟩, ⟨1, 3⟩,
   ⟨2, 0⟩, ⟨2, 1⟩, ⟨2, 2⟩, ⟨2, 3⟩,
   ⟨3, 0⟩, ⟨3, 1⟩, ⟨3, 2⟩, ⟨3, 3⟩]

theorem module_has_sixteen_vectors : allV.length = 16 ∧ allV.Nodup := by
  constructor
  · rfl
  · decide

theorem module_lists_every_vector (v : V) : v ∈ allV := by
  cases v with
  | mk x y =>
    match x, y with
    | 0, 0 => decide
    | 0, 1 => decide
    | 0, 2 => decide
    | 0, 3 => decide
    | 1, 0 => decide
    | 1, 1 => decide
    | 1, 2 => decide
    | 1, 3 => decide
    | 2, 0 => decide
    | 2, 1 => decide
    | 2, 2 => decide
    | 2, 3 => decide
    | 3, 0 => decide
    | 3, 1 => decide
    | 3, 2 => decide
    | 3, 3 => decide

#print axioms A_on
#print axioms B_on
#print axioms A_additive
#print axioms B_additive
#print axioms A_homogeneous
#print axioms B_homogeneous
#print axioms ab_matrix
#print axioms ba_matrix
#print axioms commutator_matrix
#print axioms ab_ne_ba
#print axioms ab_matches_composition
#print axioms ba_matches_composition
#print axioms actions_differ_on_e0
#print axioms left_action_e0
#print axioms right_action_e0
#print axioms commutator_on_e0
#print axioms diagonals_commute
#print axioms diagonal_product
#print axioms A_not_scalar
#print axioms coeff_char_four
#print axioms module_has_sixteen_vectors
#print axioms module_lists_every_vector

end CampaignTfq0313OperatorAlgebraShadow
