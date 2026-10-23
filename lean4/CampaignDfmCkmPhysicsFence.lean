import BornGaussRat
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Prod
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
Counting gap for the CKM physics fence.

`cycleCount` and `cpCount` are rational expressions. Their difference identity
is arithmetic. It does not build a graph, a tree, a unitary matrix, or a
measured angle. Two declared quartets in `Q(i)` have imaginary parts 0 and 1.
-/

namespace CampaignDfmCkmPhysicsFence

def cycleCount (n : ℚ) : ℚ := (n - 1) * (n - 1)

def constraintCount (n : ℚ) : ℚ := n * (n - 1) / 2

def cpCount (n : ℚ) : ℚ := (n - 1) * (n - 2) / 2

theorem cpCount_from_difference (n : ℚ) :
    cycleCount n - constraintCount n = cpCount n := by
  simp only [cycleCount, constraintCount, cpCount, div_eq_mul_inv]
  ring

theorem constraintCount_sum (n : ℚ) :
    cpCount n + (n - 1) = constraintCount n := by
  simp only [cpCount, constraintCount, div_eq_mul_inv]
  ring

theorem count_table :
    cycleCount 1 = 0 ∧ cpCount 1 = 0 ∧
    cycleCount 2 = 1 ∧ cpCount 2 = 0 ∧
    cycleCount 3 = 4 ∧ cpCount 3 = 1 ∧
    cycleCount 4 = 9 ∧ cpCount 4 = 3 ∧
    cycleCount 1 = cpCount 1 ∧
    cycleCount 2 ≠ cpCount 2 ∧
    cycleCount 3 ≠ cpCount 3 ∧
    cycleCount 4 ≠ cpCount 4 := by
  simp only [cycleCount, cpCount]
  norm_num

theorem three_generation_split :
    cycleCount 3 = 4 ∧
    constraintCount 3 = 3 ∧
    cpCount 3 = 1 ∧
    cycleCount 3 - constraintCount 3 = cpCount 3 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp only [cycleCount]; norm_num
  · simp only [constraintCount]; norm_num
  · simp only [cpCount]; norm_num
  · rw [cpCount_from_difference]

@[ext]
structure GR where
  re : ℚ
  im : ℚ
  deriving DecidableEq, Repr

namespace GR

def conj (z : GR) : GR := ⟨z.re, -z.im⟩

def mul (z w : GR) : GR :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩

end GR

def quartet (a b c d : GR) : GR :=
  GR.mul (GR.mul a b) (GR.mul (GR.conj c) (GR.conj d))

def oneGR : GR := ⟨1, 0⟩
def iGR : GR := ⟨0, 1⟩

def quartetReal : GR := quartet oneGR oneGR oneGR oneGR
def quartetImag : GR := quartet oneGR iGR oneGR oneGR

theorem quartet_real_value : quartetReal = ⟨1, 0⟩ := by
  simp only [quartetReal, quartet, oneGR, GR.mul, GR.conj]
  apply GR.ext <;> norm_num

theorem quartet_imag_value : quartetImag = ⟨0, 1⟩ := by
  simp only [quartetImag, quartet, oneGR, iGR, GR.mul, GR.conj]
  apply GR.ext <;> norm_num

theorem quartets_differ : quartetReal ≠ quartetImag := by
  intro h
  have hr := congrArg GR.im h
  simp only [quartet_real_value, quartet_imag_value] at hr
  norm_num at hr

theorem count_misses_one_quartet :
    cpCount 3 = 1 ∧
    quartetReal.im = 0 ∧
    quartetImag.im = 1 ∧
    quartetReal.im ≠ cpCount 3 ∧
    quartetImag.im = cpCount 3 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · simp only [cpCount]; norm_num
  · rw [quartet_real_value]
  · rw [quartet_imag_value]
  · rw [quartet_real_value]
    simp only [cpCount]
    norm_num
  · rw [quartet_imag_value]
    simp only [cpCount]
    norm_num

#print axioms CampaignDfmCkmPhysicsFence.cpCount_from_difference
#print axioms CampaignDfmCkmPhysicsFence.constraintCount_sum
#print axioms CampaignDfmCkmPhysicsFence.count_table
#print axioms CampaignDfmCkmPhysicsFence.three_generation_split
#print axioms CampaignDfmCkmPhysicsFence.quartet_real_value
#print axioms CampaignDfmCkmPhysicsFence.quartet_imag_value
#print axioms CampaignDfmCkmPhysicsFence.quartets_differ
#print axioms CampaignDfmCkmPhysicsFence.count_misses_one_quartet

/-! A supplied multiplicative label group, not a unitarity or Yukawa assumption.
`Option` reserves a base row and column while allowing zero free rows/columns. -/
namespace Rephasing

variable {R C G : Type*} [CommGroup G]
abbrev Table (R C G : Type*) := R → C → G

@[ext] structure Gauge (R C G : Type*) where
  row : R → G
  col : C → G

def act (g : Gauge R C G) (M : Table R C G) : Table R C G :=
  fun i j => g.row i * M i j / g.col j

def identity : Gauge R C G := ⟨fun _ => 1, fun _ => 1⟩
def compose (g h : Gauge R C G) : Gauge R C G :=
  ⟨fun i => g.row i * h.row i, fun j => g.col j * h.col j⟩
def inverse (g : Gauge R C G) : Gauge R C G :=
  ⟨fun i => (g.row i)⁻¹, fun j => (g.col j)⁻¹⟩

theorem act_identity (M : Table R C G) : act identity M = M := by
  funext i j; simp [act, identity]

theorem act_compose (g h : Gauge R C G) (M : Table R C G) :
    act (compose g h) M = act g (act h M) := by
  funext i j
  simp [act, compose, div_eq_mul_inv, mul_comm, mul_left_comm, mul_assoc]

theorem act_inverse (g : Gauge R C G) (M : Table R C G) :
    act (inverse g) (act g M) = M := by
  funext i j
  simp [act, inverse, div_eq_mul_inv, mul_comm, mul_left_comm, mul_assoc]

def normalize (r : R) (c : C) (M : Table R C G) : Table R C G :=
  fun i j => M i j * M r c / (M i c * M r j)

def Normalized (r : R) (c : C) (M : Table R C G) : Prop :=
  (∀ j, M r j = 1) ∧ (∀ i, M i c = 1)

theorem normalize_boundary (r : R) (c : C) (M : Table R C G) :
    Normalized r c (normalize r c M) := by
  constructor <;> intro k <;> simp [normalize, mul_comm]

theorem normalize_fixed {r : R} {c : C} {M : Table R C G}
    (h : Normalized r c M) : normalize r c M = M := by
  funext i j
  simp [normalize, h.1, h.2]

theorem normalize_idempotent (r : R) (c : C) (M : Table R C G) :
    normalize r c (normalize r c M) = normalize r c M :=
  normalize_fixed (normalize_boundary r c M)

theorem normalize_invariant (r : R) (c : C) (g : Gauge R C G)
    (M : Table R C G) : normalize r c (act g M) = normalize r c M := by
  funext i j
  simp [normalize, act, div_eq_mul_inv, mul_comm, mul_left_comm, mul_assoc]

/-- Computed gauge sending M to its canonical representative. -/
def normalizingGauge (r : R) (c : C) (M : Table R C G) : Gauge R C G :=
  ⟨fun i => (M i c)⁻¹, fun j => M r j / M r c⟩

theorem act_normalizingGauge (r : R) (c : C) (M : Table R C G) :
    act (normalizingGauge r c M) M = normalize r c M := by
  funext i j
  simp [act, normalizingGauge, normalize, div_eq_mul_inv, mul_comm, mul_left_comm, mul_assoc]

def Related (M N : Table R C G) : Prop := ∃ g : Gauge R C G, act g M = N

/-- Decisive classification in both directions, with a computed witness. -/
theorem related_iff_normalize (r : R) (c : C) (M N : Table R C G) :
    Related M N ↔ normalize r c M = normalize r c N := by
  constructor
  · rintro ⟨g, rfl⟩
    exact (normalize_invariant r c g M).symm
  · intro h
    refine ⟨compose (inverse (normalizingGauge r c N)) (normalizingGauge r c M), ?_⟩
    rw [act_compose, act_normalizingGauge, h, ← act_normalizingGauge r c N, act_inverse]

/-- All normalized tables are freely determined by their non-base entries. -/
def extend (x : Table R C G) : Table (Option R) (Option C) G
  | some i, some j => x i j
  | _, _ => 1

def restrict (M : Table (Option R) (Option C) G) : Table R C G :=
  fun i j => M (some i) (some j)

theorem extend_normalized (x : Table R C G) : Normalized none none (extend x) := by
  constructor <;> intro k <;> cases k <;> rfl

theorem restrict_extend (x : Table R C G) : restrict (extend x) = x := rfl

theorem extend_restrict {M : Table (Option R) (Option C) G}
    (h : Normalized none none M) : extend (restrict M) = M := by
  funext i j
  cases i with
  | none => exact (h.1 j).symm
  | some i =>
    cases j with
    | none => exact (h.2 (some i)).symm
    | some j => rfl

def coordinatesEquiv : {M : Table (Option R) (Option C) G // Normalized none none M} ≃
    Table R C G where
  toFun M := restrict M.val
  invFun x := ⟨extend x, extend_normalized x⟩
  left_inv M := Subtype.ext (extend_restrict M.property)
  right_inv := restrict_extend

/-- A separating invariant or a constructive witness, using decidable equality. -/
def decideRelated [Fintype R] [Fintype C] [DecidableEq G]
    (M N : Table (Option R) (Option C) G) : Bool :=
  decide (restrict (normalize none none M) = restrict (normalize none none N))

theorem decideRelated_correct [Fintype R] [Fintype C] [DecidableEq G]
    (M N : Table (Option R) (Option C) G) : decideRelated M N = true ↔ Related M N := by
  simp only [decideRelated, decide_eq_true_eq]
  rw [related_iff_normalize none none]
  constructor
  · intro h
    have h' := congrArg extend h
    simpa only [extend_restrict (normalize_boundary none none M),
      extend_restrict (normalize_boundary none none N)] using h'
  · exact congrArg restrict

/-- The number of independent coordinate positions, including the singleton case. -/
theorem free_coordinate_count (n : ℕ) : Fintype.card (Fin n × Fin n) = n * n := by
  simp

/-- Concrete exact carrier; nonzero labels are enforced by Units. -/
abbrev GaussianTable (R C : Type*) := Table (Option R) (Option C) BornFable.GaussRatˣ

/-- Zero is an explicit failed conversion; it is never silently inverted. -/
def checkedLabel (z : BornFable.GaussRat) : Option BornFable.GaussRatˣ :=
  if h : z = 0 then none else some (Units.mk0 z h)

theorem checkedLabel_none_iff (z : BornFable.GaussRat) :
    checkedLabel z = none ↔ z = 0 := by
  by_cases h : z = 0 <;> simp [checkedLabel, h]

theorem checkedLabel_value (z : BornFable.GaussRat) (u : BornFable.GaussRatˣ)
    (h : checkedLabel z = some u) : (u : BornFable.GaussRat) = z := by
  by_cases hz : z = 0
  · simp [checkedLabel, hz] at h
  · simp only [checkedLabel, dite_eq_right hz, Option.some.injEq] at h
    rw [← h]; rfl

end Rephasing

#print axioms Rephasing.act_compose
#print axioms Rephasing.act_inverse
#print axioms Rephasing.normalize_boundary
#print axioms Rephasing.normalize_idempotent
#print axioms Rephasing.normalize_invariant
#print axioms Rephasing.related_iff_normalize
#print axioms Rephasing.coordinatesEquiv
#print axioms Rephasing.decideRelated_correct
#print axioms Rephasing.checkedLabel_none_iff
#print axioms Rephasing.checkedLabel_value
#print axioms Rephasing.free_coordinate_count

end CampaignDfmCkmPhysicsFence
