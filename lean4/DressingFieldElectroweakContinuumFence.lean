import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
Residual covariance of the algebraic electroweak dressing over `Q(i)`.

`U` is un-normalized. Dividing by one supplied rational `s` preserves
`U(z Φ) = U(Φ) diag(conj z, z)` for every `z`. The doublet's own norm root
is that same `s` when `norm2 z = 1` and `s * s` equals the squared norm.
-/

namespace DressingFieldElectroweakContinuumFence

@[ext]
structure GR where
  re : ℚ
  im : ℚ
  deriving DecidableEq, Repr

namespace GR

def conj (z : GR) : GR := ⟨z.re, -z.im⟩

def mul (z w : GR) : GR :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩

def norm2 (z : GR) : ℚ := z.re * z.re + z.im * z.im

def negConj (z : GR) : GR := ⟨-z.re, z.im⟩

def div (z : GR) (s : ℚ) : GR := ⟨z.re / s, z.im / s⟩

theorem mul_comm (z w : GR) : mul z w = mul w z := by
  rcases z with ⟨zr, zi⟩
  rcases w with ⟨wr, wi⟩
  apply GR.ext
  · simp only [mul]; ring
  · simp only [mul]; ring

theorem conj_mul (z w : GR) : conj (mul z w) = mul (conj z) (conj w) := by
  rcases z with ⟨zr, zi⟩
  rcases w with ⟨wr, wi⟩
  apply GR.ext
  · simp only [conj, mul]; ring
  · simp only [conj, mul]; ring

theorem norm2_mul (z w : GR) : norm2 (mul z w) = norm2 z * norm2 w := by
  rcases z with ⟨zr, zi⟩
  rcases w with ⟨wr, wi⟩
  simp only [norm2, mul]
  ring

theorem negConj_mul_conj (z p : GR) : negConj (mul z p) = mul (negConj p) (conj z) := by
  rcases z with ⟨zr, zi⟩
  rcases p with ⟨pr, pi⟩
  apply GR.ext
  · simp only [negConj, mul, conj]; ring
  · simp only [negConj, mul, conj]; ring

theorem div_mul (a b : GR) (s : ℚ) : div (mul a b) s = mul (div a s) b := by
  rcases a with ⟨ar, ai⟩
  rcases b with ⟨br, bi⟩
  apply GR.ext
  · simp only [div, mul]
    rw [div_eq_mul_inv, div_eq_mul_inv, div_eq_mul_inv]
    ring
  · simp only [div, mul]
    rw [div_eq_mul_inv, div_eq_mul_inv, div_eq_mul_inv]
    ring

end GR

@[ext]
structure Dub where
  p : GR
  q : GR
  deriving DecidableEq, Repr

namespace Dub

def v2 (Φ : Dub) : ℚ := GR.norm2 Φ.p + GR.norm2 Φ.q

def scale (z : GR) (Φ : Dub) : Dub := ⟨GR.mul z Φ.p, GR.mul z Φ.q⟩

theorem v2_scale (z : GR) (Φ : Dub) : v2 (scale z Φ) = GR.norm2 z * v2 Φ := by
  rcases Φ with ⟨p, q⟩
  simp only [v2, scale, GR.norm2_mul]
  ring

end Dub

def u00 (Φ : Dub) : GR := GR.conj Φ.q
def u01 (Φ : Dub) : GR := Φ.p
def u10 (Φ : Dub) : GR := GR.negConj Φ.p
def u11 (Φ : Dub) : GR := Φ.q

@[ext]
structure Mat2 where
  e00 : GR
  e01 : GR
  e10 : GR
  e11 : GR
  deriving DecidableEq, Repr

def U (Φ : Dub) : Mat2 := ⟨u00 Φ, u01 Φ, u10 Φ, u11 Φ⟩

/-- Column 0 times `c0`, column 1 times `c1`. -/
def rightDiag (M : Mat2) (c0 c1 : GR) : Mat2 :=
  ⟨GR.mul M.e00 c0, GR.mul M.e01 c1, GR.mul M.e10 c0, GR.mul M.e11 c1⟩

def scaleMat (M : Mat2) (s : ℚ) : Mat2 :=
  ⟨GR.div M.e00 s, GR.div M.e01 s, GR.div M.e10 s, GR.div M.e11 s⟩

theorem unnormalized_covariance (z : GR) (Φ : Dub) :
    U (Dub.scale z Φ) = rightDiag (U Φ) (GR.conj z) z := by
  rcases Φ with ⟨p, q⟩
  apply Mat2.ext
  · simp only [U, u00, Dub.scale, rightDiag]
    rw [GR.conj_mul]
    exact GR.mul_comm (GR.conj z) (GR.conj q)
  · simp only [U, u01, Dub.scale, rightDiag]
    exact GR.mul_comm z p
  · simp only [U, u10, Dub.scale, rightDiag]
    exact GR.negConj_mul_conj z p
  · simp only [U, u11, Dub.scale, rightDiag]
    exact GR.mul_comm z q

theorem div_rightDiag (M : Mat2) (c0 c1 : GR) (s : ℚ) :
    scaleMat (rightDiag M c0 c1) s = rightDiag (scaleMat M s) c0 c1 := by
  apply Mat2.ext
  · simpa [scaleMat, rightDiag] using GR.div_mul M.e00 c0 s
  · simpa [scaleMat, rightDiag] using GR.div_mul M.e01 c1 s
  · simpa [scaleMat, rightDiag] using GR.div_mul M.e10 c0 s
  · simpa [scaleMat, rightDiag] using GR.div_mul M.e11 c1 s

theorem unit_shares_norm (z : GR) (Φ : Dub) (s : ℚ)
    (hz : GR.norm2 z = 1) (hs : s * s = Dub.v2 Φ) :
    s * s = Dub.v2 (Dub.scale z Φ) := by
  rw [Dub.v2_scale, hz, one_mul]
  exact hs

theorem unit_normalized_covariance (z : GR) (Φ : Dub) (s : ℚ)
    (hz : GR.norm2 z = 1) (hs : s * s = Dub.v2 Φ) :
    scaleMat (U (Dub.scale z Φ)) s =
      rightDiag (scaleMat (U Φ) s) (GR.conj z) z ∧
      s * s = Dub.v2 (Dub.scale z Φ) := by
  constructor
  · rw [unnormalized_covariance, div_rightDiag]
  · exact unit_shares_norm z Φ s hz hs

/-! Checked normalization and unit-phase action. Rational roots are supplied,
validated and never inferred to exist for every Gaussian-rational doublet. -/
namespace Normalization

structure Input where
  phi : Dub
  scale : ℚ
  positive : 0 < scale
  square : scale * scale = Dub.v2 phi

structure UnitDoublet where
  value : Dub
  unit : Dub.v2 value = 1

structure UnitPhase where
  value : GR
  unit : GR.norm2 value = 1

inductive Error
  | zeroNorm
  | nonpositiveScale
  | mismatchedSquare
  deriving DecidableEq, Repr

def check (phi : Dub) (s : ℚ) : Except Error Input :=
  if hn : Dub.v2 phi = 0 then .error .zeroNorm
  else if hp : 0 < s then
    if hs : s * s = Dub.v2 phi then .ok ⟨phi, s, hp, hs⟩
    else .error .mismatchedSquare
  else .error .nonpositiveScale

theorem check_accepts (phi : Dub) (s : ℚ) (hp : 0 < s)
    (hs : s * s = Dub.v2 phi) : check phi s = .ok ⟨phi, s, hp, hs⟩ := by
  have hn : Dub.v2 phi ≠ 0 := by rw [← hs]; exact mul_ne_zero (ne_of_gt hp) (ne_of_gt hp)
  simp [check, hn, hp, hs]

theorem check_preserves (phi : Dub) (s : ℚ) (n : Input)
    (h : check phi s = .ok n) : n.phi = phi ∧ n.scale = s := by
  unfold check at h
  split at h
  · cases h
  · split at h
    · split at h
      · cases h; exact ⟨rfl, rfl⟩
      · cases h
    · cases h

theorem check_success_iff (phi : Dub) (s : ℚ) :
    (∃ n, check phi s = .ok n) ↔ 0 < s ∧ s * s = Dub.v2 phi := by
  constructor
  · rintro ⟨n, hn⟩
    obtain ⟨hphi, hs⟩ := check_preserves phi s n hn
    simpa [← hphi, ← hs] using And.intro n.positive n.square
  · rintro ⟨hp, hs⟩
    exact ⟨⟨phi, s, hp, hs⟩, check_accepts phi s hp hs⟩

def divide (phi : Dub) (s : ℚ) : Dub := ⟨GR.div phi.p s, GR.div phi.q s⟩

theorem divide_norm (phi : Dub) (s : ℚ) :
    Dub.v2 (divide phi s) = Dub.v2 phi / (s * s) := by
  simp only [Dub.v2, divide, GR.norm2, GR.div]
  ring

def Input.normalize (n : Input) : UnitDoublet where
  value := divide n.phi n.scale
  unit := by
    rw [divide_norm, ← n.square]
    exact div_self (mul_ne_zero (ne_of_gt n.positive) (ne_of_gt n.positive))

def UnitPhase.act (z : UnitPhase) (phi : UnitDoublet) : UnitDoublet where
  value := Dub.scale z.value phi.value
  unit := by rw [Dub.v2_scale, z.unit, phi.unit, one_mul]

def UnitPhase.compose (z w : UnitPhase) : UnitPhase where
  value := GR.mul z.value w.value
  unit := by rw [GR.norm2_mul, z.unit, w.unit, one_mul]

def Input.act (n : Input) (z : UnitPhase) : Input where
  phi := Dub.scale z.value n.phi
  scale := n.scale
  positive := n.positive
  square := unit_shares_norm z.value n.phi n.scale z.unit n.square

theorem action_composes (z w : UnitPhase) (phi : UnitDoublet) :
    (z.act (w.act phi)).value = ((z.compose w).act phi).value := by
  apply Dub.ext <;> apply GR.ext <;>
    simp [UnitPhase.act, UnitPhase.compose, Dub.scale, GR.mul] <;> ring

theorem normalize_covariant (z : UnitPhase) (n : Input) :
    ((n.act z).normalize).value = (z.act n.normalize).value := by
  apply Dub.ext <;> apply GR.ext <;>
    simp [Input.normalize, Input.act, UnitPhase.act, divide, Dub.scale, GR.div, GR.mul] <;> ring

theorem matrix_covariant (z : UnitPhase) (n : Input) :
    scaleMat (U (n.act z).phi) (n.act z).scale =
      rightDiag (scaleMat (U n.phi) n.scale) (GR.conj z.value) z.value := by
  exact (unit_normalized_covariance z.value n.phi n.scale z.unit n.square).1

end Normalization

def zUnit : GR := ⟨3 / 5, 4 / 5⟩
def phiAxis : Dub := ⟨⟨1, 0⟩, ⟨0, 0⟩⟩
def zTwo : GR := ⟨2, 0⟩

theorem witness_three_fifths :
    GR.norm2 zUnit = 1 ∧
    Dub.v2 phiAxis = 1 ∧
    (1 : ℚ) * 1 = Dub.v2 phiAxis ∧
    (scaleMat (U (Dub.scale zUnit phiAxis)) 1).e01 = zUnit := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp only [zUnit, GR.norm2]
    norm_num
  · simp only [phiAxis, Dub.v2, GR.norm2]
    norm_num
  · simp only [phiAxis, Dub.v2, GR.norm2]
    norm_num
  · simp only [scaleMat, U, u01, Dub.scale, phiAxis, zUnit, GR.mul, GR.div]
    apply GR.ext <;> norm_num

theorem nonunit_normalized_entries_differ :
    GR.norm2 zTwo = 4 ∧
    Dub.v2 phiAxis = 1 ∧
    Dub.v2 (Dub.scale zTwo phiAxis) = 4 ∧
    (1 : ℚ) * 1 = Dub.v2 phiAxis ∧
    (2 : ℚ) * 2 = Dub.v2 (Dub.scale zTwo phiAxis) ∧
    (scaleMat (U (Dub.scale zTwo phiAxis)) 2).e01 = ⟨1, 0⟩ ∧
    (rightDiag (scaleMat (U phiAxis) 1) (GR.conj zTwo) zTwo).e01 = ⟨2, 0⟩ ∧
    (scaleMat (U (Dub.scale zTwo phiAxis)) 2).e01 ≠
      (rightDiag (scaleMat (U phiAxis) 1) (GR.conj zTwo) zTwo).e01 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp only [zTwo, GR.norm2]; norm_num
  · simp only [phiAxis, Dub.v2, GR.norm2]; norm_num
  · simp only [zTwo, phiAxis, Dub.v2, Dub.scale, GR.norm2, GR.mul]; norm_num
  · simp only [phiAxis, Dub.v2, GR.norm2]; norm_num
  · simp only [zTwo, phiAxis, Dub.v2, Dub.scale, GR.norm2, GR.mul]; norm_num
  · simp only [scaleMat, U, u01, Dub.scale, phiAxis, zTwo, GR.mul, GR.div]
    apply GR.ext <;> norm_num
  · simp only [rightDiag, scaleMat, U, u01, phiAxis, zTwo, GR.conj, GR.mul, GR.div]
    apply GR.ext <;> norm_num
  · intro h
    have hr := congrArg GR.re h
    simp only [scaleMat, rightDiag, U, u01, Dub.scale, phiAxis, zTwo, GR.conj, GR.mul, GR.div] at hr
    norm_num at hr

#print axioms Normalization.check_accepts
#print axioms Normalization.check_preserves
#print axioms Normalization.check_success_iff
#print axioms Normalization.Input.normalize
#print axioms Normalization.UnitPhase.act
#print axioms Normalization.UnitPhase.compose
#print axioms Normalization.Input.act
#print axioms Normalization.action_composes
#print axioms Normalization.normalize_covariant
#print axioms Normalization.matrix_covariant
#print axioms DressingFieldElectroweakContinuumFence.GR.mul_comm
#print axioms DressingFieldElectroweakContinuumFence.GR.conj_mul
#print axioms DressingFieldElectroweakContinuumFence.GR.norm2_mul
#print axioms DressingFieldElectroweakContinuumFence.GR.negConj_mul_conj
#print axioms DressingFieldElectroweakContinuumFence.GR.div_mul
#print axioms DressingFieldElectroweakContinuumFence.Dub.v2_scale
#print axioms DressingFieldElectroweakContinuumFence.unnormalized_covariance
#print axioms DressingFieldElectroweakContinuumFence.div_rightDiag
#print axioms DressingFieldElectroweakContinuumFence.unit_shares_norm
#print axioms DressingFieldElectroweakContinuumFence.unit_normalized_covariance
#print axioms DressingFieldElectroweakContinuumFence.witness_three_fifths
#print axioms DressingFieldElectroweakContinuumFence.nonunit_normalized_entries_differ

end DressingFieldElectroweakContinuumFence
