import Mathlib.Tactic.NormNum
import Mathlib.Algebra.Group.Action.Defs
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Tactic.Group
import Lean.Elab.Tactic.Omega

/-!
Finite-clock transport, closure validation and a rational order-4 client.

`step` is the real matrix `[[0, -1], [1, 0]]`. Each block
`(step^{t+1})^T step step^t` equals `I` for `t = 0, 1, 2, 3`.
The Clock API handles arbitrary supplied group-valued schedules and group actions.
No continuous-time generator is constructed.
-/

namespace DressingFieldRelationalTimeFence

@[ext]
structure M2 where
  a00 : Rat
  a01 : Rat
  a10 : Rat
  a11 : Rat

@[ext]
structure V2 where
  x : Rat
  y : Rat

def mmul (A B : M2) : M2 where
  a00 := A.a00 * B.a00 + A.a01 * B.a10
  a01 := A.a00 * B.a01 + A.a01 * B.a11
  a10 := A.a10 * B.a00 + A.a11 * B.a10
  a11 := A.a10 * B.a01 + A.a11 * B.a11

def transp (A : M2) : M2 where
  a00 := A.a00
  a01 := A.a10
  a10 := A.a01
  a11 := A.a11

def apply (A : M2) (v : V2) : V2 where
  x := A.a00 * v.x + A.a01 * v.y
  y := A.a10 * v.x + A.a11 * v.y

def eye : M2 where
  a00 := 1
  a01 := 0
  a10 := 0
  a11 := 1

def minusEye : M2 where
  a00 := -1
  a01 := 0
  a10 := 0
  a11 := -1

def step : M2 where
  a00 := 0
  a01 := -1
  a10 := 1
  a11 := 0

def u0 : M2 := eye
def u1 : M2 := step
def u2 : M2 := mmul u1 step
def u3 : M2 := mmul u2 step
def u4 : M2 := mmul u3 step

def psi : V2 where
  x := 3 / 5
  y := 4 / 5

def block (tNext tCur : M2) : M2 := mmul (mmul (transp tNext) step) tCur

theorem step_square_and_order :
    u2 = minusEye ∧
    u4 = eye ∧
    mmul (transp step) step = eye := by
  refine ⟨?_, ?_, ?_⟩
  all_goals apply M2.ext
  all_goals simp only [u2, u4, u3, u1, mmul, transp, step, eye, minusEye]
  all_goals norm_num

theorem four_blocks :
    block u1 u0 = eye ∧
    block u2 u1 = eye ∧
    block u3 u2 = eye ∧
    block u4 u3 = eye := by
  refine ⟨?_, ?_, ?_, ?_⟩
  all_goals apply M2.ext
  all_goals simp only [block, u0, u1, u2, u3, u4, mmul, transp, step, eye]
  all_goals norm_num

theorem psi_recover :
    psi.x ^ 2 + psi.y ^ 2 = 1 ∧
    apply (transp u0) (apply u0 psi) = psi ∧
    apply (transp u1) (apply u1 psi) = psi ∧
    apply (transp u2) (apply u2 psi) = psi ∧
    apply (transp u3) (apply u3 psi) = psi ∧
    (apply u1 psi).x ≠ psi.x ∧
    (apply u2 psi).x ≠ psi.x := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp only [psi]; norm_num
  · apply V2.ext
    all_goals simp only [apply, transp, u0, eye, psi]
    all_goals norm_num
  · apply V2.ext
    all_goals simp only [apply, transp, u1, step, psi]
    all_goals norm_num
  · apply V2.ext
    all_goals simp only [apply, transp, u2, u1, mmul, step, psi]
    all_goals norm_num
  · apply V2.ext
    all_goals simp only [apply, transp, u3, u2, u1, mmul, step, psi]
    all_goals norm_num
  · simp only [apply, u1, step, psi]; norm_num
  · simp only [apply, u2, u1, mmul, step, psi]; norm_num


/-! A reusable finite-clock interface. The group and its action are supplied.
The seam obstruction is computed from the links, never assumed by normalization. -/
namespace Clock

variable {G : Type*} [Group G]

/-- Chronological transport: the latest link multiplies on the left. -/
def frame (link : ℕ → G) : ℕ → G
  | 0 => 1
  | t + 1 => link t * frame link t

/-- Change frame at both endpoints of an edge. -/
def dress (g : ℕ → G) (link : ℕ → G) (t : ℕ) : G :=
  (g (t + 1))⁻¹ * link t * g t

@[simp] theorem frame_zero (link : ℕ → G) : frame link 0 = 1 := rfl

@[simp] theorem frame_succ (link : ℕ → G) (t : ℕ) :
    frame link (t + 1) = link t * frame link t := rfl

/-- General transport under a frame change, including the initial frame. -/
theorem frame_dress (g link : ℕ → G) (t : ℕ) :
    frame (dress g link) t = (g t)⁻¹ * frame link t * g 0 := by
  induction t with
  | zero => simp
  | succ t ih => rw [frame_succ, ih, frame_succ]; simp only [dress]; group

theorem interior (link : ℕ → G) (t : ℕ) : dress (frame link) link t = 1 := by
  simp [dress, mul_assoc]

/-- The closing edge returns to frame zero, rather than frame period. -/
def seam (link : ℕ → G) (last : ℕ) : G :=
  (frame link 0)⁻¹ * link last * frame link last

@[simp] theorem seam_eq (link : ℕ → G) (last : ℕ) :
    seam link last = frame link (last + 1) := by simp [seam]

/-- A frame which cancels every edge must recur by transport. -/
theorem trivial_iff_recurrence (g link : ℕ → G) (t : ℕ) :
    dress g link t = 1 ↔ g (t + 1) = link t * g t := by
  simp only [dress, mul_assoc, inv_mul_eq_one]

/-- No periodic change of frame can remove a nonidentity holonomy. -/
theorem periodic_trivialization_iff (link : ℕ → G) (n : ℕ) :
    (∃ g : ℕ → G, g n = g 0 ∧ ∀ t, t < n → dress g link t = 1) ↔
      frame link n = 1 := by
  constructor
  · rintro ⟨g, periodic, trivial⟩
    have h : ∀ t, t ≤ n → frame (dress g link) t = 1 := by
      intro t ht
      induction t with
      | zero => rfl
      | succ t ih => rw [frame_succ, trivial t (by omega), ih (by omega), one_mul]
    have hn := h n (le_refl n)
    rw [frame_dress, periodic] at hn
    have he := congrArg (fun x => g 0 * x * (g 0)⁻¹) hn
    simpa only [mul_assoc, mul_inv_cancel, mul_one, mul_inv_cancel_left,
      mul_inv_cancel_right, mul_inv_cancel_left] using he
  · intro closed
    exact ⟨frame link, by simpa using closed, fun t _ => interior link t⟩

inductive ClosureError
  | emptyPeriod
  | nontrivialHolonomy
  deriving DecidableEq, Repr

/-- Validated nonempty period. The links remain supplied, not inferred. -/
structure ClosedCycle (link : ℕ → G) where
  period : ℕ
  positive : 0 < period
  closes : frame link period = 1

/-- Reject zero periods and nonclosing schedules with distinct failures. -/
def validate [DecidableEq G] (link : ℕ → G) (n : ℕ) :
    Except ClosureError (ClosedCycle link) :=
  if hp : 0 < n then
    if hc : frame link n = 1 then .ok ⟨n, hp, hc⟩
    else .error .nontrivialHolonomy
  else .error .emptyPeriod

@[simp] theorem validate_zero [DecidableEq G] (link : ℕ → G) :
    validate link 0 = .error .emptyPeriod := by simp [validate]

theorem validate_success_iff [DecidableEq G] (link : ℕ → G) (n : ℕ) :
    (∃ c, validate link n = .ok c) ↔ 0 < n ∧ frame link n = 1 := by
  unfold validate
  split_ifs <;> simp_all

theorem validate_period [DecidableEq G] (link : ℕ → G) (n : ℕ)
    (c : ClosedCycle link) (h : validate link n = .ok c) : c.period = n := by
  unfold validate at h
  split_ifs at h with hp hc
  · cases h; rfl

theorem validate_roundtrip [DecidableEq G] (link : ℕ → G) (c : ClosedCycle link) :
    validate link c.period = .ok c := by
  cases c with
  | mk n hp hc => simp [validate, hp, hc]

theorem validate_nonclosing [DecidableEq G] (link : ℕ → G) (n : ℕ)
    (hp : 0 < n) (hc : frame link n ≠ 1) :
    validate link n = .error .nontrivialHolonomy := by simp [validate, hp, hc]

/-- Finite clock successor, including the wrap to zero. -/
def next (n : ℕ) (t : Fin n) : ℕ := if t.val + 1 < n then t.val + 1 else 0

def cycleBlock (link : ℕ → G) (n : ℕ) (t : Fin n) : G :=
  (frame link (next n t))⁻¹ * link t.val * frame link t.val

/-- Every interior block is identity; the closing block is the holonomy. -/
theorem cycleBlock_normal_form (link : ℕ → G) (n : ℕ) (t : Fin n) :
    cycleBlock link n t = if t.val + 1 < n then 1 else frame link n := by
  unfold cycleBlock next
  split_ifs with h
  · exact interior link t.val
  · have hn : t.val + 1 = n := by omega
    simp [← frame_succ, hn]

theorem ClosedCycle.blocks (link : ℕ → G) (c : ClosedCycle link) (t : Fin c.period) :
    cycleBlock link c.period t = 1 := by rw [cycleBlock_normal_form, c.closes]; split <;> rfl

variable {X : Type*} [MulAction G X]

/-- A history is re-expressed reversibly at each time; no information is erased. -/
def historyEquiv (g : ℕ → G) : (ℕ → X) ≃ (ℕ → X) where
  toFun h t := (g t)⁻¹ • h t
  invFun h t := g t • h t
  left_inv h := by funext t; simp
  right_inv h := by funext t; simp

def Evolves (link : ℕ → G) (h : ℕ → X) : Prop :=
  ∀ t, h (t + 1) = link t • h t

/-- Evolution is covariant under a reversible history transformation. -/
theorem evolves_iff (g link : ℕ → G) (h : ℕ → X) :
    Evolves (dress g link) (historyEquiv g h) ↔ Evolves link h := by
  unfold Evolves
  constructor
  · intro hd t
    have he := congrArg (fun x => g (t + 1) • x) (hd t)
    simpa [historyEquiv, dress, mul_smul] using he
  · intro he t
    simp [historyEquiv, dress, mul_smul, he t]

/-- Frame coordinates turn transported histories into constant histories. -/
theorem stationary_iff (link : ℕ → G) (h : ℕ → X) :
    (∀ t, historyEquiv (frame link) h (t + 1) = historyEquiv (frame link) h t) ↔
      Evolves link h := by
  have he := evolves_iff (frame link) link h
  simpa only [Evolves, interior, one_smul] using he

/-- Constant steps specialize to ordinary powers, for every natural period. -/
theorem frame_constant (u : G) (n : ℕ) : frame (fun _ => u) n = u ^ n := by
  induction n with
  | zero => simp
  | succ n ih => rw [frame_succ, ih, pow_succ'];

end Clock

/-- The supplied matrix acts as a genuinely reversible rational-vector map. -/
def rotation : Equiv.Perm V2 where
  toFun v := ⟨-v.y, v.x⟩
  invFun v := ⟨v.y, -v.x⟩
  left_inv v := by cases v; simp
  right_inv v := by cases v; simp

theorem rotation_apply (v : V2) : rotation v = apply step v := by
  apply V2.ext <;> simp [rotation, apply, step]

theorem rotation_four : Clock.frame (fun _ => rotation) 4 = 1 := by
  ext v <;> simp [Clock.frame, rotation, Equiv.Perm.mul_apply]

def rationalClock : Clock.ClosedCycle (fun _ => rotation) := ⟨4, by decide, rotation_four⟩

theorem rationalClock_blocks (t : Fin 4) :
    Clock.cycleBlock (fun _ => rotation) 4 t = 1 :=
  Clock.ClosedCycle.blocks _ rationalClock t

#print axioms DressingFieldRelationalTimeFence.step_square_and_order
#print axioms DressingFieldRelationalTimeFence.four_blocks
#print axioms DressingFieldRelationalTimeFence.psi_recover

#print axioms DressingFieldRelationalTimeFence.Clock.frame_dress
#print axioms DressingFieldRelationalTimeFence.Clock.interior
#print axioms DressingFieldRelationalTimeFence.Clock.seam_eq
#print axioms DressingFieldRelationalTimeFence.Clock.trivial_iff_recurrence
#print axioms DressingFieldRelationalTimeFence.Clock.periodic_trivialization_iff
#print axioms DressingFieldRelationalTimeFence.Clock.validate_zero
#print axioms DressingFieldRelationalTimeFence.Clock.validate_success_iff
#print axioms DressingFieldRelationalTimeFence.Clock.validate_period
#print axioms DressingFieldRelationalTimeFence.Clock.validate_roundtrip
#print axioms DressingFieldRelationalTimeFence.Clock.validate_nonclosing
#print axioms DressingFieldRelationalTimeFence.Clock.cycleBlock_normal_form
#print axioms DressingFieldRelationalTimeFence.Clock.ClosedCycle.blocks
#print axioms DressingFieldRelationalTimeFence.Clock.evolves_iff
#print axioms DressingFieldRelationalTimeFence.Clock.stationary_iff
#print axioms DressingFieldRelationalTimeFence.Clock.frame_constant
#print axioms DressingFieldRelationalTimeFence.rotation_apply
#print axioms DressingFieldRelationalTimeFence.rotation_four
#print axioms DressingFieldRelationalTimeFence.rationalClock_blocks

end DressingFieldRelationalTimeFence
