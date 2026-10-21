import Mathlib.Basic.Real.Basic
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith

/-!
Finite real operational systems with an involutive symmetry. All processes
are nonnegative equivariant matrices; events have column sums at most one.
Parallel composition uses the diagonal symmetry, not separate local symmetries.
This gives a coherent operational countermodel to local tomography, not a
reconstruction of quantum systems or a model of unspecified stronger primitives.
-/
noncomputable section
open Matrix
open scoped BigOperators Kronecker
namespace OperationalIndependence

structure System where
  Point : Type
  finite : Fintype Point
  nonempty : Nonempty Point
  flip : Point ≃ Point
  involutive : Function.Involutive flip

instance : CoeSort System Type := ⟨System.Point⟩
instance (A : System) : Fintype A := A.finite
instance (A : System) : Nonempty A := A.nonempty
instance (A : System) : DecidableEq A := Classical.decEq A

@[simp] theorem flip_flip (A : System) (x : A) : A.flip (A.flip x) = x := A.involutive x

abbrev tensor (A B : System) : System where
  Point := A × B
  finite := inferInstance
  nonempty := inferInstance
  flip := A.flip.prodCongr B.flip
  involutive := by rintro ⟨a,b⟩; simp

infixr:35 " ⊗ₛ " => tensor

abbrev classical (X : Type) [Fintype X] [Nonempty X] : System where
  Point := X
  finite := inferInstance
  nonempty := inferInstance
  flip := Equiv.refl X
  involutive := fun _ => rfl

abbrev unit : System := classical PUnit

abbrev Vec (A : System) := A → ℝ
def Invariant (A : System) (v : Vec A) : Prop := ∀ x, v (A.flip x) = v x
def Positive {A : System} (v : Vec A) : Prop := ∀ x, 0 ≤ v x
def mass {A : System} (v : Vec A) : ℝ := ∑ x, v x
def State (A : System) (v : Vec A) : Prop := Invariant A v ∧ Positive v ∧ mass v = 1
def Effect (A : System) (e : Vec A) : Prop := Invariant A e ∧ ∀ x, 0 ≤ e x ∧ e x ≤ 1
def probability {A : System} (e v : Vec A) : ℝ := ∑ x, e x * v x

def product {A B : System} (p : Vec A) (q : Vec B) : Vec (A ⊗ₛ B) :=
  fun x => p x.1 * q x.2

@[simp] theorem sum_flip (A : System) (f : A → ℝ) : (∑ x, f (A.flip x)) = ∑ x, f x :=
  Equiv.sum_comp A.flip f

theorem product_invariant {A B : System} {p : Vec A} {q : Vec B}
    (hp : Invariant A p) (hq : Invariant B q) : Invariant (A ⊗ₛ B) (product p q) := by
  rintro ⟨a,b⟩
  exact congrArg₂ (· * ·) (hp a) (hq b)

theorem product_mass {A B : System} (p : Vec A) (q : Vec B) :
    mass (product p q) = mass p * mass q := by
  change (∑ x : A × B, p x.1 * q x.2) = _
  rw [Fintype.sum_prod_type]
  simp only [mass, Finset.sum_mul, Finset.mul_sum]
  exact Finset.sum_comm

theorem product_state {A B : System} {p : Vec A} {q : Vec B}
    (hp : State A p) (hq : State B q) : State (A ⊗ₛ B) (product p q) := by
  exact ⟨product_invariant hp.1 hq.1, fun x => mul_nonneg (hp.2.1 x.1) (hq.2.1 x.2),
    by rw [product_mass, hp.2.2, hq.2.2]; norm_num⟩

theorem product_effect {A B : System} {e : Vec A} {f : Vec B}
    (he : Effect A e) (hf : Effect B f) : Effect (A ⊗ₛ B) (product e f) := by
  refine ⟨product_invariant he.1 hf.1, fun x => ⟨mul_nonneg (he.2 x.1).1 (hf.2 x.2).1, ?_⟩⟩
  calc
    _ ≤ 1 * f x.2 := mul_le_mul_of_nonneg_right (he.2 x.1).2 (hf.2 x.2).1
    _ ≤ 1 := by simpa using (hf.2 x.2).2

theorem independent_probabilities {A B : System} (e p : Vec A) (f q : Vec B) :
    probability (product e f) (product p q) = probability e p * probability f q := by
  change (∑ x : A × B, (e x.1 * f x.2) * (p x.1 * q x.2)) = _
  rw [Fintype.sum_prod_type]
  simp only [probability]
  simp_rw [show ∀ a b, (e a * f b) * (p a * q b) = (e a * p a) * (f b * q b) by intros; ring]
  simp only [Finset.sum_mul, Finset.mul_sum]
  exact Finset.sum_comm

structure Process (A B : System) where
  matrix : Matrix B A ℝ
  nonneg : ∀ y x, 0 ≤ matrix y x
  equivariant : ∀ y x, matrix (B.flip y) (A.flip x) = matrix y x

def act {A B : System} (T : Process A B) (p : Vec A) : Vec B := T.matrix *ᵥ p
def column {A B : System} (T : Process A B) (x : A) : ℝ := ∑ y, T.matrix y x
def Event {A B : System} (T : Process A B) : Prop := ∀ x, column T x ≤ 1
def Channel {A B : System} (T : Process A B) : Prop := ∀ x, column T x = 1

def identity (A : System) : Process A A where
  matrix := 1
  nonneg := by intro y x; simp only [Matrix.one_apply]; split_ifs <;> norm_num
  equivariant := by intro y x; simp [Matrix.one_apply]

def comp {A B C : System} (S : Process B C) (T : Process A B) : Process A C where
  matrix := S.matrix * T.matrix
  nonneg := fun z x => Finset.sum_nonneg fun y _ => mul_nonneg (S.nonneg z y) (T.nonneg y x)
  equivariant := by
    intro z x
    change (∑ y, S.matrix (C.flip z) y * T.matrix y (A.flip x)) = _
    rw [← sum_flip B (fun y => S.matrix (C.flip z) y * T.matrix y (A.flip x))]
    simp_rw [S.equivariant, T.equivariant]
    rfl

def parallel {A B C D : System} (T : Process A B) (S : Process C D) :
    Process (A ⊗ₛ C) (B ⊗ₛ D) where
  matrix := T.matrix ⊗ₖ S.matrix
  nonneg := fun y x => mul_nonneg (T.nonneg y.1 x.1) (S.nonneg y.2 x.2)
  equivariant := by rintro ⟨y,z⟩ ⟨x,w⟩; exact congrArg₂ (· * ·) (T.equivariant y x) (S.equivariant z w)

theorem act_invariant {A B : System} (T : Process A B) {p : Vec A}
    (hp : Invariant A p) : Invariant B (act T p) := by
  intro y
  change ∀ x, p (A.flip x) = p x at hp
  change (∑ x, T.matrix (B.flip y) x * p x) = _
  rw [← sum_flip A (fun x => T.matrix (B.flip y) x * p x)]
  simp_rw [T.equivariant, hp]
  rfl

theorem act_positive {A B : System} (T : Process A B) {p : Vec A}
    (hp : Positive p) : Positive (act T p) :=
  fun y => Finset.sum_nonneg fun x _ => mul_nonneg (T.nonneg y x) (hp x)

theorem column_nonneg {A B : System} (T : Process A B) (x : A) : 0 ≤ column T x :=
  Finset.sum_nonneg fun y _ => T.nonneg y x

theorem mass_act {A B : System} (T : Process A B) (p : Vec A) :
    mass (act T p) = ∑ x, column T x * p x := by
  simp only [mass, act, Matrix.mulVec, dotProduct, column, Finset.sum_mul]
  exact Finset.sum_comm

theorem event_mass {A B : System} (T : Process A B) (hT : Event T) {p : Vec A}
    (hp : Positive p) : mass (act T p) ≤ mass p := by
  rw [mass_act]
  exact Finset.sum_le_sum fun x _ => by simpa using mul_le_mul_of_nonneg_right (hT x) (hp x)

theorem channel_mass {A B : System} (T : Process A B) (hT : Channel T) (p : Vec A) :
    mass (act T p) = mass p := by
  rw [mass_act]
  simp only [Channel] at hT
  simp [hT, mass]

theorem channel_state {A B : System} (T : Process A B) (hT : Channel T) {p : Vec A}
    (hp : State A p) : State B (act T p) :=
  ⟨act_invariant T hp.1, act_positive T hp.2.1, (channel_mass T hT p).trans hp.2.2⟩

theorem column_comp {A B C : System} (S : Process B C) (T : Process A B) (x : A) :
    column (comp S T) x = ∑ y, column S y * T.matrix y x := by
  simp only [column, comp, Matrix.mul_apply, Finset.sum_mul]
  exact Finset.sum_comm

theorem event_comp {A B C : System} (S : Process B C) (T : Process A B)
    (hS : Event S) (hT : Event T) : Event (comp S T) := by
  intro x; rw [column_comp]
  calc
    _ ≤ ∑ y, T.matrix y x := Finset.sum_le_sum fun y _ => by
      simpa using mul_le_mul_of_nonneg_right (hS y) (T.nonneg y x)
    _ ≤ 1 := hT x

theorem channel_comp {A B C : System} (S : Process B C) (T : Process A B)
    (hS : Channel S) (hT : Channel T) : Channel (comp S T) := by
  intro x
  rw [column_comp]
  simp only [Channel] at hS hT
  simp only [hS, one_mul]
  exact hT x

theorem column_parallel {A B C D : System} (T : Process A B) (S : Process C D)
    (x : A ⊗ₛ C) : column (parallel T S) x = column T x.1 * column S x.2 := by
  change (∑ y : B × D, T.matrix y.1 x.1 * S.matrix y.2 x.2) = _
  rw [Fintype.sum_prod_type]
  simp only [column, Finset.sum_mul, Finset.mul_sum]
  exact Finset.sum_comm

theorem event_parallel {A B C D : System} (T : Process A B) (S : Process C D)
    (hT : Event T) (hS : Event S) : Event (parallel T S) := by
  intro x; rw [column_parallel]
  calc
    _ ≤ 1 * column S x.2 := mul_le_mul_of_nonneg_right (hT _) (column_nonneg S _)
    _ ≤ 1 := by simpa using hS x.2

theorem channel_parallel {A B C D : System} (T : Process A B) (S : Process C D)
    (hT : Channel T) (hS : Channel S) : Channel (parallel T S) := by
  intro x
  rw [column_parallel, hT _, hS _]
  norm_num

theorem identity_channel (A : System) : Channel (identity A) := by
  intro x; simp [column, identity, Matrix.one_apply]

theorem act_comp {A B C : System} (S : Process B C) (T : Process A B) (p : Vec A) :
    act (comp S T) p = act S (act T p) := (Matrix.mulVec_mulVec p S.matrix T.matrix).symm

theorem comp_assoc {A B C D : System} (R : Process C D) (S : Process B C) (T : Process A B) :
    (comp (comp R S) T).matrix = (comp R (comp S T)).matrix := Matrix.mul_assoc _ _ _

theorem interchange {A B C D E F : System} (T : Process A B) (S : Process B C)
    (U : Process D E) (V : Process E F) :
    (parallel (comp S T) (comp V U)).matrix = (comp (parallel S V) (parallel T U)).matrix :=
  Matrix.mul_kronecker_mul _ _ _ _

/-- Classical randomization is admitted; its weights and total bound are explicit. -/
def weighted {A B : System} {I : Type*} [Fintype I] (w : I → ℝ)
    (hw : ∀ i, 0 ≤ w i) (T : I → Process A B) : Process A B where
  matrix := fun y x => ∑ i, w i * (T i).matrix y x
  nonneg := fun y x => Finset.sum_nonneg fun i _ => mul_nonneg (hw i) ((T i).nonneg y x)
  equivariant := by intro y x; simp_rw [Process.equivariant]

theorem column_weighted {A B : System} {I : Type*} [Fintype I] (w : I → ℝ)
    (hw : ∀ i, 0 ≤ w i) (T : I → Process A B) (x : A) :
    column (weighted w hw T) x = ∑ i, w i * column (T i) x := by
  simp only [column, weighted, Finset.mul_sum]
  exact Finset.sum_comm

theorem event_weighted {A B : System} {I : Type*} [Fintype I] (w : I → ℝ)
    (hw : ∀ i, 0 ≤ w i) (hbound : ∑ i, w i ≤ 1) (T : I → Process A B)
    (hT : ∀ i, Event (T i)) : Event (weighted w hw T) := by
  intro x; rw [column_weighted]
  calc
    _ ≤ ∑ i, w i := Finset.sum_le_sum fun i _ => by
      simpa using mul_le_mul_of_nonneg_left (hT i x) (hw i)
    _ ≤ 1 := hbound

def prepare {A : System} (p : Vec A) (hi : Invariant A p) (hp : Positive p) : Process unit A where
  matrix := fun y _ => p y
  nonneg := fun y _ => hp y
  equivariant := fun y _ => hi y

def test {A : System} (e : Vec A) (hi : Invariant A e) (he : Positive e) : Process A unit where
  matrix := fun _ x => e x
  nonneg := fun _ x => he x
  equivariant := fun _ x => hi x

theorem prepare_channel {A : System} {p : Vec A} (hp : State A p) :
    Channel (prepare p hp.1 hp.2.1) := by intro x; exact hp.2.2

theorem test_event {A : System} {e : Vec A} (he : Effect A e) :
    Event (test e he.1 (fun x => (he.2 x).1)) := by
  intro x
  change (∑ _ : PUnit, e x) ≤ 1
  simpa using (he.2 x).2

def discard (A : System) : Process A unit := test (fun _ => 1) (fun _ => rfl) (fun _ => by norm_num)

theorem discard_channel (A : System) : Channel (discard A) := by
  intro x; change (∑ _ : PUnit, (1 : ℝ)) = 1; simp

theorem discard_unique {A : System} (T : Process A unit) (hT : Channel T) :
    T.matrix = (discard A).matrix := by
  funext y x
  have hy : y = PUnit.unit := Subsingleton.elim _ _
  subst y
  have h := hT x
  change (∑ z : PUnit, T.matrix z x) = 1 at h
  simpa [discard, test] using h

theorem discard_comp {A B : System} (T : Process A B) (hT : Channel T) :
    (comp (discard B) T).matrix = (discard A).matrix := by
  apply discard_unique
  exact channel_comp _ _ (discard_channel B) hT

theorem prepare_test_reset {A B : System} {p : Vec B} {e : Vec A}
    (hp : State B p) (he : Effect A e) (y : B) (x : A) :
    (comp (prepare p hp.1 hp.2.1) (test e he.1 (fun z => (he.2 z).1))).matrix y x = p y * e x := by
  change (∑ _ : PUnit, p y * e x) = _
  simp

theorem reset_event {A B : System} {p : Vec B} {e : Vec A}
    (hp : State B p) (he : Effect A e) :
    Event (comp (prepare p hp.1 hp.2.1) (test e he.1 (fun z => (he.2 z).1))) :=
  event_comp _ _ (fun x => le_of_eq (prepare_channel hp x)) (test_event he)

/-- An orbit-averaged point indicator is both a normalized preparation and a
bounded effect. It reads exactly one coordinate of every invariant vector. -/
def orbit (A : System) (a : A) : Vec A :=
  fun x => ((if x = a then 1 else 0) + (if x = A.flip a then 1 else 0)) / 2

theorem orbit_invariant (A : System) (a : A) : Invariant A (orbit A a) := by
  intro x
  have h : A.flip x = a ↔ x = A.flip a := by
    constructor
    · intro he; simpa using congrArg A.flip he
    · intro he; rw [he, flip_flip]
  simp only [orbit, h, Equiv.apply_eq_iff_eq]
  ring

theorem orbit_positive (A : System) (a : A) : Positive (orbit A a) := by
  intro x; unfold orbit; split_ifs <;> norm_num

theorem orbit_state (A : System) (a : A) : State A (orbit A a) := by
  refine ⟨orbit_invariant A a, orbit_positive A a, ?_⟩
  change (∑ x : A, ((if x = a then (1 : ℝ) else 0) + (if x = A.flip a then 1 else 0)) / 2) = 1
  simp_rw [div_eq_mul_inv]
  rw [← Finset.sum_mul, Finset.sum_add_distrib]
  norm_num

theorem orbit_effect (A : System) (a : A) : Effect A (orbit A a) := by
  refine ⟨orbit_invariant A a, fun x => ⟨orbit_positive A a x, ?_⟩⟩
  unfold orbit; split_ifs <;> norm_num

theorem orbit_reads {A : System} (a : A) {v : Vec A} (hv : Invariant A v) :
    probability (orbit A a) v = v a := by
  have h : v (A.flip a) = v a := hv a
  change (∑ x : A, (((if x = a then (1 : ℝ) else 0) + (if x = A.flip a then 1 else 0)) / 2) * v x) = v a
  simp_rw [div_mul_eq_mul_div, add_mul, ite_mul, one_mul, zero_mul]
  simp_rw [div_eq_mul_inv]
  rw [← Finset.sum_mul, Finset.sum_add_distrib]
  simp [h]; ring

theorem global_effects_separate {A : System} {v w : Vec A}
    (hv : Invariant A v) (hw : Invariant A w)
    (h : ∀ e, Effect A e → probability e v = probability e w) : v = w := by
  funext a
  simpa only [orbit_reads a hv, orbit_reads a hw] using h (orbit A a) (orbit_effect A a)

theorem probability_interval {A : System} {e p : Vec A} (he : Effect A e) (hp : State A p) :
    0 ≤ probability e p ∧ probability e p ≤ 1 := by
  constructor
  · exact Finset.sum_nonneg fun x _ => mul_nonneg (he.2 x).1 (hp.2.1 x)
  · calc
      _ ≤ mass p := Finset.sum_le_sum fun x _ => by
        simpa using mul_le_mul_of_nonneg_right (he.2 x).2 (hp.2.1 x)
      _ = 1 := hp.2.2

/-- The positive cone generates the invariant real carrier; no extra span axiom. -/
theorem cone_generating {A : System} {v : Vec A} (hv : Invariant A v) :
    ∃ p q : Vec A, Invariant A p ∧ Positive p ∧ Invariant A q ∧ Positive q ∧ v = p - q := by
  refine ⟨fun x => max (v x) 0, fun x => max (-v x) 0,
    fun x => by dsimp; rw [hv x], fun x => le_max_right _ _,
    fun x => by dsimp; rw [hv x], fun x => le_max_right _ _, ?_⟩
  funext x
  change v x = max (v x) 0 - max (-v x) 0
  by_cases h : 0 ≤ v x
  · rw [max_eq_left h, max_eq_right (neg_nonpos.mpr h)]; ring
  · have h' : v x ≤ 0 := le_of_not_ge h
    rw [max_eq_right h', max_eq_left (neg_nonneg.mpr h')]; ring

def Instrument {A B : System} {I : Type*} [Fintype I] (T : I → Process A B) : Prop :=
  ∀ x, ∑ i, column (T i) x = 1

theorem instrument_event {A B : System} {I : Type*} [Fintype I]
    (T : I → Process A B) (hT : Instrument T) (i : I) : Event (T i) := by
  intro x
  calc
    _ ≤ ∑ j, column (T j) x := Finset.single_le_sum (fun j _ => column_nonneg (T j) x) (Finset.mem_univ i)
    _ = 1 := hT x

theorem instrument_probability {A B : System} {I : Type*} [Fintype I]
    (T : I → Process A B) (hT : Instrument T) (p : Vec A) :
    (∑ i, mass (act (T i) p)) = mass p := by
  change ∀ x, ∑ i, column (T i) x = 1 at hT
  simp_rw [mass_act]
  rw [Finset.sum_comm]
  simp_rw [← Finset.sum_mul, hT]
  simp [mass]

theorem instrument_adaptive {A B C : System} {I J : Type*} [Fintype I] [Fintype J]
    (T : I → Process A B) (S : I → J → Process B C)
    (hT : Instrument T) (hS : ∀ i, Instrument (S i)) :
    Instrument (fun ij : I × J => comp (S ij.1 ij.2) (T ij.1)) := by
  intro x
  change ∀ i x, ∑ j, column (S i j) x = 1 at hS
  simp only [Fintype.sum_prod_type, column_comp]
  have step : ∀ i, (∑ j, ∑ y, column (S i j) y * (T i).matrix y x) = column (T i) x := by
    intro i
    rw [Finset.sum_comm]
    simp_rw [← Finset.sum_mul, hS i]
    simp [column]
  simp_rw [step]
  exact hT x

theorem instrument_parallel {A B C D : System} {I J : Type*} [Fintype I] [Fintype J]
    (T : I → Process A B) (S : J → Process C D)
    (hT : Instrument T) (hS : Instrument S) :
    Instrument (fun ij : I × J => parallel (T ij.1) (S ij.2)) := by
  intro x
  change ∀ x, ∑ j, column (S j) x = 1 at hS
  simp only [Fintype.sum_prod_type, column_parallel]
  simp_rw [← Finset.mul_sum, hS, mul_one]
  exact hT x.1

/-- Normalized randomization preserves channels. -/
theorem channel_weighted {A B : System} {I : Type*} [Fintype I] (w : I → ℝ)
    (hw : ∀ i, 0 ≤ w i) (htotal : ∑ i, w i = 1) (T : I → Process A B)
    (hT : ∀ i, Channel (T i)) : Channel (weighted w hw T) := by
  intro x
  rw [column_weighted]
  simp only [Channel] at hT
  simpa only [hT, mul_one] using htotal

/-- Normalization vanishes on a positive vector only at zero. -/
theorem normalization_faithful {A : System} {p : Vec A} (hp : Positive p)
    (hm : mass p = 0) : p = 0 := by
  funext x
  have hle : p x ≤ mass p := Finset.single_le_sum (fun y _ => hp y) (Finset.mem_univ x)
  change p x = 0
  rw [hm] at hle
  exact le_antisymm hle (hp x)

theorem orbit_symmetric (A : System) (a x : A) : orbit A a x = orbit A x a := by
  have h : x = A.flip a ↔ a = A.flip x := by
    constructor
    · intro he; simpa using (congrArg A.flip he).symm
    · intro he; simpa using (congrArg A.flip he).symm
  simp only [orbit, h, eq_comm]

/-- Every invariant vector is an explicit real linear combination of normalized
orbit preparations; spanning is proved, not supplied as an extra assumption. -/
theorem normalized_preparations_span {A : System} {v : Vec A} (hv : Invariant A v) :
    ∀ x, v x = ∑ a, v a * orbit A a x := by
  intro x
  simp_rw [orbit_symmetric A _ x, mul_comm (v _)]
  exact (orbit_reads x hv).symm

end OperationalIndependence
