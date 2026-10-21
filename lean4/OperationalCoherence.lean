import OperationalSymmetry

/-! Structural coherence, classical control, discard, and ancillary separation.
All laws concern the explicitly defined finite involutive operational model. -/
noncomputable section
open Matrix
open scoped BigOperators Kronecker
namespace OperationalIndependence

structure Wire (A B : System) extends A ≃ B where
  commute : ∀ x, toEquiv (A.flip x) = B.flip (toEquiv x)

instance {A B : System} : CoeFun (Wire A B) (fun _ => A → B) := ⟨fun e => e.toEquiv⟩

def Wire.inverse {A B : System} (e : Wire A B) : Wire B A where
  toEquiv := e.toEquiv.symm
  commute := by
    intro y
    apply e.toEquiv.injective
    simpa using (e.commute (e.toEquiv.symm y)).symm

def Wire.then {A B C : System} (e : Wire A B) (f : Wire B C) : Wire A C where
  toEquiv := e.toEquiv.trans f.toEquiv
  commute := by intro x; change f (e (A.flip x)) = _; rw [e.commute, f.commute]; rfl

def Wire.both {A B C D : System} (e : Wire A B) (f : Wire C D) : Wire (A ⊗ₛ C) (B ⊗ₛ D) where
  toEquiv := e.toEquiv.prodCongr f.toEquiv
  commute := by rintro ⟨a,c⟩; exact Prod.ext (e.commute a) (f.commute c)

def wireId (A : System) : Wire A A := ⟨Equiv.refl A, fun _ => rfl⟩
def associator (A B C : System) : Wire ((A ⊗ₛ B) ⊗ₛ C) (A ⊗ₛ (B ⊗ₛ C)) :=
  ⟨Equiv.prodAssoc A B C, fun _ => rfl⟩
def swap (A B : System) : Wire (A ⊗ₛ B) (B ⊗ₛ A) :=
  ⟨Equiv.prodComm A B, fun _ => rfl⟩
def leftUnit (A : System) : Wire (unit ⊗ₛ A) A :=
  ⟨Equiv.punitProd A, fun _ => rfl⟩
def rightUnit (A : System) : Wire (A ⊗ₛ unit) A :=
  ⟨Equiv.prodPUnit A, fun _ => rfl⟩

def rename {A B : System} (e : Wire A B) : Process A B where
  matrix := fun y x => if y = e x then 1 else 0
  nonneg := by intro y x; split_ifs <;> norm_num
  equivariant := by intro y x; rw [e.commute]; simp

theorem rename_channel {A B : System} (e : Wire A B) : Channel (rename e) := by
  intro x; simp [column, rename]

theorem rename_after {A B C : System} (e : Wire B C) (T : Process A B) (z : C) (x : A) :
    (comp (rename e) T).matrix z x = T.matrix (e.toEquiv.symm z) x := by
  change (∑ y, (if z = e y then (1 : ℝ) else 0) * T.matrix y x) = _
  have he : ∀ y, z = e y ↔ y = e.toEquiv.symm z := fun y => by
    constructor
    · intro h; exact (e.toEquiv.injective (by simpa using h.symm))
    · intro h; subst y; simp
  simp [he]

theorem rename_before {A B C : System} (e : Wire A B) (T : Process B C) (z : C) (x : A) :
    (comp T (rename e)).matrix z x = T.matrix z (e x) := by
  change (∑ y, T.matrix z y * (if y = e x then (1 : ℝ) else 0)) = _
  simp

theorem rename_then {A B C : System} (e : Wire A B) (f : Wire B C) :
    (comp (rename f) (rename e)).matrix = (rename (e.then f)).matrix := by
  funext z x
  rw [rename_before]
  rfl

theorem rename_inverse {A B : System} (e : Wire A B) :
    (comp (rename e.inverse) (rename e)).matrix = (identity A).matrix := by
  funext y x
  rw [rename_before]
  change (if y = e.toEquiv.symm (e x) then (1 : ℝ) else 0) = _
  simp [identity, Matrix.one_apply]

theorem associator_naturality {A B C D E F : System}
    (T : Process A B) (S : Process C D) (R : Process E F) :
    (comp (rename (associator B D F)) (parallel (parallel T S) R)).matrix =
    (comp (parallel T (parallel S R)) (rename (associator A C E))).matrix := by
  funext z x
  rw [rename_after, rename_before]
  change (T.matrix z.1 x.1.1 * S.matrix z.2.1 x.1.2) * R.matrix z.2.2 x.2 =
    T.matrix z.1 x.1.1 * (S.matrix z.2.1 x.1.2 * R.matrix z.2.2 x.2)
  ring

theorem swap_naturality {A B C D : System} (T : Process A B) (S : Process C D) :
    (comp (rename (swap B D)) (parallel T S)).matrix =
    (comp (parallel S T) (rename (swap A C))).matrix := by
  funext z x
  rw [rename_after, rename_before]
  change T.matrix z.2 x.1 * S.matrix z.1 x.2 = S.matrix z.1 x.2 * T.matrix z.2 x.1
  ring

theorem left_unit_naturality {A B : System} (T : Process A B) :
    (comp (rename (leftUnit B)) (parallel (identity unit) T)).matrix =
    (comp T (rename (leftUnit A))).matrix := by
  funext z x
  rw [rename_after, rename_before]
  change (identity unit).matrix PUnit.unit x.1 * T.matrix z x.2 = T.matrix z x.2
  simp [identity, Subsingleton.elim PUnit.unit x.1]

theorem right_unit_naturality {A B : System} (T : Process A B) :
    (comp (rename (rightUnit B)) (parallel T (identity unit))).matrix =
    (comp T (rename (rightUnit A))).matrix := by
  funext z x
  rw [rename_after, rename_before]
  change T.matrix z x.1 * (identity unit).matrix PUnit.unit x.2 = T.matrix z x.1
  simp [identity, Subsingleton.elim PUnit.unit x.2]

/-- Both pentagon routes are the same permutation, hence the same admitted process. -/
theorem pentagon (A B C D : System) :
    (rename ((associator (A ⊗ₛ B) C D).then (associator A B (C ⊗ₛ D)))).matrix =
    (rename (((associator A B C).both (wireId D)).then
      ((associator A (B ⊗ₛ C) D).then ((wireId A).both (associator B C D))))).matrix := rfl

theorem triangle (A B : System) :
    (rename ((associator A unit B).then ((wireId A).both (leftUnit B)))).matrix =
    (rename ((rightUnit A).both (wireId B))).matrix := rfl

theorem symmetry (A B : System) :
    (rename ((swap A B).then (swap B A))).matrix = (rename (wireId (A ⊗ₛ B))).matrix := rfl

theorem hexagon (A B C : System) :
    (rename ((associator A B C).then ((swap A (B ⊗ₛ C)).then (associator B C A)))).matrix =
    (rename (((swap A B).both (wireId C)).then
      ((associator B A C).then ((wireId B).both (swap A C))))).matrix := rfl

/-- Finite coarse-graining preserves the complete instrument, not arbitrary sums of events. -/
def coarse {A B : System} {I J : Type*} [Fintype I] [Fintype J]
    (T : I → Process A B) (f : I → J) (j : J) : Process A B := by
  classical
  exact weighted (fun i => if f i = j then 1 else 0) (fun i => by split_ifs <;> norm_num) T

theorem instrument_coarse {A B : System} {I J : Type*} [Fintype I] [Fintype J]
    (T : I → Process A B) (hT : Instrument T) (f : I → J) : Instrument (coarse T f) := by
  classical
  intro x
  simp only [coarse, column_weighted]
  rw [Finset.sum_comm]
  simpa using hT x

def marginal {A B : System} (p : Vec (A ⊗ₛ B)) : Vec A := fun a => ∑ b, p (a,b)

theorem no_signalling {A B C D : System} (T : Process A B) (S : Process C D)
    (hS : Channel S) (p : Vec (A ⊗ₛ C)) :
    marginal (act (parallel T S) p) = act T (marginal p) := by
  funext b
  change (∑ d : D, ∑ x : A × C, (T.matrix b x.1 * S.matrix d x.2) * p x) = _
  simp only [Fintype.sum_prod_type]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro a _
  rw [Finset.sum_comm]
  change (∑ c, ∑ d, (T.matrix b a * S.matrix d c) * p (a,c)) = T.matrix b a * ∑ c, p (a,c)
  simp_rw [mul_assoc, ← Finset.mul_sum, ← Finset.sum_mul]
  change T.matrix b a * (∑ c, column S c * p (a,c)) = _
  simp only [Channel] at hS
  simp [hS]

/-- A normalized diagonal correlation probes every matrix entry with an ancilla.
Thus equality on isolated states is not used as equality of transformations. -/
def correlation (A : System) : Vec (A ⊗ₛ A) :=
  fun x => if x.1 = x.2 then (Fintype.card A : ℝ)⁻¹ else 0

theorem correlation_state (A : System) : State (A ⊗ₛ A) (correlation A) := by
  refine ⟨?_, ?_, ?_⟩
  · rintro ⟨a,b⟩; simp [correlation]
  · intro x; unfold correlation; split_ifs
    · exact inv_nonneg.mpr (Nat.cast_nonneg _)
    · norm_num
  · change (∑ x : A × A, if x.1 = x.2 then (Fintype.card A : ℝ)⁻¹ else 0) = 1
    simp [Fintype.sum_prod_type, Fintype.card_ne_zero]

theorem correlation_probe {A B : System} (T : Process A B) (y : B) (x : A) :
    act (parallel T (identity A)) (correlation A) (y,x) =
    T.matrix y x / Fintype.card A := by
  change (∑ z : A × A, (T.matrix y z.1 * (identity A).matrix x z.2) * correlation A z) = _
  simp [Fintype.sum_prod_type, identity, Matrix.one_apply, correlation, div_eq_mul_inv]

theorem ancillary_process_separation {A B : System} (T S : Process A B)
    (h : ∀ e, Effect (B ⊗ₛ A) e →
      probability e (act (parallel T (identity A)) (correlation A)) =
      probability e (act (parallel S (identity A)) (correlation A))) : T.matrix = S.matrix := by
  have hp := (correlation_state A).1
  have eqv := global_effects_separate (act_invariant _ hp) (act_invariant _ hp) h
  funext y x
  have hh := congrFun eqv (y,x)
  rw [correlation_probe, correlation_probe] at hh
  exact (div_left_inj' (by exact_mod_cast Fintype.card_ne_zero (α := A))).mp hh

theorem comp_identity {A B : System} (T : Process A B) :
    (comp T (identity A)).matrix = T.matrix ∧ (comp (identity B) T).matrix = T.matrix :=
  ⟨Matrix.mul_one _, Matrix.one_mul _⟩

theorem parallel_identity (A B : System) :
    (parallel (identity A) (identity B)).matrix = (identity (A ⊗ₛ B)).matrix := by
  funext ⟨b,d⟩ ⟨a,c⟩
  by_cases h1 : b = a <;> by_cases h2 : d = c <;>
    simp [parallel, identity, h1, h2]

theorem column_invariant {A B : System} (T : Process A B) : Invariant A (column T) := by
  intro x
  change (∑ y, T.matrix y (A.flip x)) = _
  rw [← sum_flip B (fun y => T.matrix y (A.flip x))]
  simp_rw [T.equivariant]
  rfl

theorem missing_effect {A B : System} (T : Process A B) (hT : Event T) :
    Effect A (fun x => 1 - column T x) := by
  refine ⟨fun x => by dsimp; rw [column_invariant T x], fun x => ?_⟩
  exact ⟨sub_nonneg.mpr (hT x), sub_le_self _ (column_nonneg T x)⟩

def failure {A B : System} (T : Process A B) (hT : Event T) (b : B) : Process A B :=
  comp (prepare (orbit B b) (orbit_invariant B b) (orbit_positive B b))
    (test (fun x => 1 - column T x) (missing_effect T hT).1 (fun x => ((missing_effect T hT).2 x).1))

theorem failure_column {A B : System} (T : Process A B) (hT : Event T) (b : B) (x : A) :
    column (failure T hT b) x = 1 - column T x := by
  change (∑ y : B, ∑ _ : PUnit, orbit B b y * (1 - column T x)) = _
  simp only [Fintype.sum_unique]
  rw [← Finset.sum_mul]
  change mass (orbit B b) * (1 - column T x) = _
  rw [(orbit_state B b).2.2, one_mul]

theorem event_completion {A B : System} (T : Process A B) (hT : Event T) (b : B) :
    Instrument (fun i : Bool => if i then T else failure T hT b) := by
  intro x
  simp only [Fintype.sum_bool, Bool.false_eq_true, ite_false, ite_true, failure_column]
  ring

/-- A finite instrument can be recorded in a classical output register. -/
def record {A B : System} {I : Type} [Fintype I] [Nonempty I]
    (T : I → Process A B) : Process A ((classical I) ⊗ₛ B) where
  matrix := fun y x => (T y.1).matrix y.2 x
  nonneg := fun y x => (T y.1).nonneg y.2 x
  equivariant := fun y x => (T y.1).equivariant y.2 x

theorem record_channel {A B : System} {I : Type} [Fintype I] [Nonempty I]
    (T : I → Process A B) (hT : Instrument T) : Channel (record T) := by
  intro x
  change (∑ y : I × B, (T y.1).matrix y.2 x) = 1
  rw [Fintype.sum_prod_type]
  exact hT x

def controlled {A B : System} {I : Type} [Fintype I] [Nonempty I]
    (T : I → Process A B) : Process ((classical I) ⊗ₛ A) B where
  matrix := fun y x => (T x.1).matrix y x.2
  nonneg := fun y x => (T x.1).nonneg y x.2
  equivariant := fun y x => (T x.1).equivariant y x.2

theorem controlled_channel {A B : System} {I : Type} [Fintype I] [Nonempty I]
    (T : I → Process A B) (hT : ∀ i, Channel (T i)) : Channel (controlled T) :=
  fun x => hT x.1 x.2

theorem rename_id (A : System) : (rename (wireId A)).matrix = (identity A).matrix := by
  funext y x
  by_cases h : y = x <;> simp [rename, wireId, identity, h]

theorem rename_both {A B C D : System} (e : Wire A B) (f : Wire C D) :
    (rename (e.both f)).matrix = (parallel (rename e) (rename f)).matrix := by
  funext ⟨b,d⟩ ⟨a,c⟩
  by_cases h1 : b = e a <;> by_cases h2 : d = f c <;>
    simp [rename, Wire.both, parallel, Matrix.kroneckerMap, h1, h2]

end OperationalIndependence
