/-!
# Pure-gauge triangle cancellation and determinant-sign fixtures

AuthorityEffect: None. GenesisEffect: None.
The group-law theorem proves cancellation for links g(x) g(y)^{-1}.
The determinant records below check signs of supplied integers; they do not
compute a Cayley-Menger matrix, establish Euclidean embeddability, or prove
a Regge/Bianchi identity. Curved hinge holonomy need not be the identity.
-/

namespace MssnSimplicialGauge

/-- Generic discrete group structure for link holonomies. -/
structure GroupCarrier (α : Type) where
  one : α
  mul : α → α → α
  inv : α → α
  mul_assoc : ∀ a b c : α, mul (mul a b) c = mul a (mul b c)
  one_mul : ∀ a : α, mul one a = a
  mul_one : ∀ a : α, mul a one = a
  mul_inv : ∀ a : α, mul a (inv a) = one
  inv_mul : ∀ a : α, mul (inv a) a = one

/-- Link assignment on natural-number vertex labels, with an inverse-link law. -/
structure LinkAssignment (α : Type) (G : GroupCarrier α) where
  U : Nat → Nat → α
  inv_link : ∀ x y : Nat, U y x = G.inv (U x y)

/-- Local face holonomy around oriented triangle (a, b, c):
    R(a, b, c) = U(a, b) * U(b, c) * U(c, a). -/
def faceHolonomy {α : Type} (G : GroupCarrier α) (bundle : LinkAssignment α G) (a b c : Nat) : α :=
  G.mul (G.mul (bundle.U a b) (bundle.U b c)) (bundle.U c a)

/-- Exact cancellation identity for pure gauge links:
    U(x, y) = g_x * g_y^{-1}.
    Any pure gauge face holonomy identically evaluates to the group identity. -/
theorem pure_gauge_triangle_is_identity
    {α : Type} (G : GroupCarrier α) (g : Nat → α) (a b c : Nat) :
    let U (x y : Nat) := G.mul (g x) (G.inv (g y))
    let r := G.mul (G.mul (U a b) (U b c)) (U c a)
    r = G.one := by
  have cancel (x y z : α) :
      G.mul (G.mul x (G.inv y)) (G.mul y z) = G.mul x z := by
    rw [G.mul_assoc, ← G.mul_assoc (G.inv y) y z, G.inv_mul, G.one_mul]
  dsimp
  rw [cancel (g a) (g b) (G.inv (g c)), cancel (g a) (g c) (G.inv (g a)), G.mul_inv]

/-- 4-Simplex Cayley-Menger Determinant Record.
    In dimension D=4:
    V_4^2 = (-det(C)) / 9216. -/
structure CayleyMenger4D where
  detC : Int

/-- Necessary determinant-sign test for positive 4-volume: requires (-det(C)) > 0, i.e. det(C) < 0. -/
def CayleyMenger4D.isRealVolume (cm : CayleyMenger4D) : Prop :=
  cm.detC < 0

/-- Supplied determinant fixture for a regular unit 4-simplex: det(C) = -5. -/
def regularUnit4Simplex : CayleyMenger4D :=
  ⟨-5⟩

/-- Sign check on the supplied determinant: regular unit 4-simplex satisfies positive 4-volume reality. -/
theorem regular_4simplex_volume_reality : regularUnit4Simplex.isRealVolume := by
  dsimp [CayleyMenger4D.isRealVolume, regularUnit4Simplex]
  decide

/-- Supplied determinant fixture for the standard orthogonal 4-simplex: -16. -/
def orthogonalEuclidean4Simplex : CayleyMenger4D :=
  ⟨-16⟩

/-- Sign check on the supplied determinant: orthogonal 4-simplex satisfies positive 4-volume reality. -/
theorem orthogonal_4simplex_volume_reality : orthogonalEuclidean4Simplex.isRealVolume := by
  dsimp [CayleyMenger4D.isRealVolume, orthogonalEuclidean4Simplex]
  decide

/-- Degenerate flattened 4-simplex with det(C) = 0. -/
def degenerate4Simplex : CayleyMenger4D :=
  ⟨0⟩

/-- Sign check on the supplied determinant: degenerate 4-simplex fails volume reality (fail-closed). -/
theorem degenerate_4simplex_fails_volume_reality : ¬ degenerate4Simplex.isRealVolume := by
  dsimp [CayleyMenger4D.isRealVolume, degenerate4Simplex]
  decide

end MssnSimplicialGauge
