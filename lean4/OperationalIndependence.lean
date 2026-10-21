import OperationalCoherence

/-! Two coherent finite operational theories, one locally tomographic and one
not. The independence result concerns the explicit finite operational laws,
not purification, local complex quantum systems, or primitive difference. -/
noncomputable section
open Matrix
open scoped BigOperators Kronecker
namespace OperationalIndependence

/-- Each atom has an observable classical bit and an unreferenced binary flag. -/
abbrev atom : System where
  Point := Bool × Bool
  finite := inferInstance
  nonempty := inferInstance
  flip := {
    toFun := fun x => (x.1, !x.2)
    invFun := fun x => (x.1, !x.2)
    left_inv := by rintro ⟨a,b⟩; cases b <;> rfl
    right_inv := by rintro ⟨a,b⟩; cases b <;> rfl }
  involutive := by rintro ⟨a,b⟩; cases b <;> rfl

def rho : Vec (atom ⊗ₛ atom) := orbit _ ((false,false),(false,false))
def sigma : Vec (atom ⊗ₛ atom) := orbit _ ((false,false),(false,true))
def parity : Vec (atom ⊗ₛ atom) := fun x => if x.1.2 = x.2.2 then 1 else 0

theorem hidden_states_normalized : State (atom ⊗ₛ atom) rho ∧ State (atom ⊗ₛ atom) sigma :=
  ⟨orbit_state _ _, orbit_state _ _⟩

theorem parity_effect : Effect (atom ⊗ₛ atom) parity := by
  constructor
  · rintro ⟨⟨a,b⟩,⟨c,d⟩⟩; cases b <;> cases d <;> rfl
  · intro x; unfold parity; split_ifs <;> norm_num

theorem parity_separates : probability parity rho = 1 ∧ probability parity sigma = 0 := by
  have hr := orbit_reads ((false,false),(false,false)) parity_effect.1
  have hs := orbit_reads ((false,false),(false,true)) parity_effect.1
  constructor
  · simpa [probability, rho, parity, mul_comm] using hr
  · simpa [probability, sigma, parity, mul_comm] using hs

theorem hidden_states_distinct : rho ≠ sigma := by
  intro h
  have hx := parity_separates.1
  rw [h, parity_separates.2] at hx
  norm_num at hx

theorem product_tests_agree (e f : Vec atom) (he : Effect atom e) (hf : Effect atom f) :
    probability (product e f) rho = probability (product e f) sigma := by
  have hE : e (false,true) = e (false,false) := he.1 (false,false)
  have hF : f (false,true) = f (false,false) := hf.1 (false,false)
  simp [probability, product, rho, sigma, orbit, atom, Fintype.sum_prod_type, hE, hF]

/-- Separation on the whole invariant linear carrier. The counterexample also
uses normalized positive states, so it is not merely a signed-vector defect. -/
def ProductSeparated (A B : System) : Prop :=
  ∀ v w : Vec (A ⊗ₛ B), Invariant (A ⊗ₛ B) v → Invariant (A ⊗ₛ B) w →
    (∀ e f, Effect A e → Effect B f → probability (product e f) v = probability (product e f) w) → v = w

theorem atom_not_tomographic : ¬ ProductSeparated atom atom := by
  intro h
  exact hidden_states_distinct (h rho sigma hidden_states_normalized.1.1
    hidden_states_normalized.2.1 product_tests_agree)

def TrivialSymmetry (A : System) : Prop := ∀ x, A.flip x = x

theorem orbit_trivial {A : System} (hA : TrivialSymmetry A) (a x : A) :
    orbit A a x = if x = a then 1 else 0 := by
  simp only [orbit, hA a]
  split_ifs <;> norm_num

theorem classical_product_reads {A B : System} (hA : TrivialSymmetry A) (hB : TrivialSymmetry B)
    (a : A) (b : B) (v : Vec (A ⊗ₛ B)) :
    probability (product (orbit A a) (orbit B b)) v = v (a,b) := by
  change (∑ x : A × B, (orbit A a x.1 * orbit B b x.2) * v x) = _
  simp [Fintype.sum_prod_type, orbit_trivial hA, orbit_trivial hB]

theorem classical_tomography {A B : System} (hA : TrivialSymmetry A) (hB : TrivialSymmetry B) :
    ProductSeparated A B := by
  intro v w _ _ h
  funext x
  have hx := h (orbit A x.1) (orbit B x.2) (orbit_effect A x.1) (orbit_effect B x.2)
  simpa only [classical_product_reads hA hB] using hx

/-- A theory is a collection of systems closed under unit, tensor and reversible
wiring. It has ALL of the specified equivariant processes and finite instruments;
admission is not an additional unverified field of this structure. -/
structure Theory where
  allowed : System → Prop
  unit_allowed : allowed unit
  classical_allowed : ∀ (I : Type) [Fintype I] [Nonempty I], allowed (classical I)
  tensor_allowed : ∀ A B, allowed A → allowed B → allowed (A ⊗ₛ B)
  wire_allowed : ∀ {A B}, allowed A → Wire A B → allowed B

def symmetricTheory : Theory where
  allowed := fun _ => True
  unit_allowed := trivial
  classical_allowed := fun _ => trivial
  tensor_allowed := fun _ _ _ _ => trivial
  wire_allowed := fun _ _ => trivial

def classicalTheory : Theory where
  allowed := TrivialSymmetry
  unit_allowed := fun _ => rfl
  classical_allowed := by intro I _ _ x; rfl
  tensor_allowed := by
    intro A B hA hB x
    exact Prod.ext (hA x.1) (hB x.2)
  wire_allowed := by
    intro A B hA e y
    obtain ⟨x,rfl⟩ := e.toEquiv.surjective y
    have h := e.commute x
    rw [hA x] at h
    exact h.symm

def LocallyTomographic (T : Theory) : Prop :=
  ∀ A B, T.allowed A → T.allowed B → ProductSeparated A B

theorem classicalTheory_tomographic : LocallyTomographic classicalTheory :=
  fun _ _ hA hB => classical_tomography hA hB

theorem symmetricTheory_not_tomographic : ¬ LocallyTomographic symmetricTheory := by
  intro h
  exact atom_not_tomographic (h atom atom trivial trivial)

/-- The explicit operational law package. These are universally proved laws of
our ambient construction and hence hold in both closed subtheories below.
It does not encode purification or a reconstruction from primitive difference. -/
structure OperationalLaws : Prop where
  product_state {A B : System} {p : Vec A} {q : Vec B}
      (hp : State A p) (hq : State B q) : State (A ⊗ₛ B) (product p q)
  product_effect {A B : System} {e : Vec A} {f : Vec B}
      (he : Effect A e) (hf : Effect B f) : Effect (A ⊗ₛ B) (product e f)
  independent_probabilities {A B : System} (e p : Vec A) (f q : Vec B) :
      probability (product e f) (product p q) = probability e p * probability f q
  act_invariant {A B : System} (T : Process A B) {p : Vec A}
      (hp : Invariant A p) : Invariant B (act T p)
  act_positive {A B : System} (T : Process A B) {p : Vec A}
      (hp : Positive p) : Positive (act T p)
  event_mass {A B : System} (T : Process A B) (hT : Event T) {p : Vec A}
      (hp : Positive p) : mass (act T p) ≤ mass p
  channel_state {A B : System} (T : Process A B) (hT : Channel T) {p : Vec A}
      (hp : State A p) : State B (act T p)
  event_comp {A B C : System} (S : Process B C) (T : Process A B)
      (hS : Event S) (hT : Event T) : Event (comp S T)
  channel_comp {A B C : System} (S : Process B C) (T : Process A B)
      (hS : Channel S) (hT : Channel T) : Channel (comp S T)
  event_parallel {A B C D : System} (T : Process A B) (S : Process C D)
      (hT : Event T) (hS : Event S) : Event (parallel T S)
  channel_parallel {A B C D : System} (T : Process A B) (S : Process C D)
      (hT : Channel T) (hS : Channel S) : Channel (parallel T S)
  identity_channel (A : System) : Channel (identity A)
  act_comp {A B C : System} (S : Process B C) (T : Process A B) (p : Vec A) :
      act (comp S T) p = act S (act T p)
  comp_assoc {A B C D : System} (R : Process C D) (S : Process B C) (T : Process A B) :
      (comp (comp R S) T).matrix = (comp R (comp S T)).matrix
  interchange {A B C D E F : System} (T : Process A B) (S : Process B C)
      (U : Process D E) (V : Process E F) :
      (parallel (comp S T) (comp V U)).matrix = (comp (parallel S V) (parallel T U)).matrix
  event_weighted {A B : System} {I : Type} [Fintype I] (w : I → ℝ)
      (hw : ∀ i, 0 ≤ w i) (hbound : ∑ i, w i ≤ 1) (T : I → Process A B)
      (hT : ∀ i, Event (T i)) : Event (weighted w hw T)
  channel_weighted {A B : System} {I : Type} [Fintype I] (w : I → ℝ)
      (hw : ∀ i, 0 ≤ w i) (htotal : ∑ i, w i = 1) (T : I → Process A B)
      (hT : ∀ i, Channel (T i)) : Channel (weighted w hw T)
  prepare_channel {A : System} {p : Vec A} (hp : State A p) :
      Channel (prepare p hp.1 hp.2.1)
  test_event {A : System} {e : Vec A} (he : Effect A e) :
      Event (test e he.1 (fun x => (he.2 x).1))
  discard_channel (A : System) : Channel (discard A)
  discard_unique {A : System} (T : Process A unit) (hT : Channel T) :
      T.matrix = (discard A).matrix
  discard_comp {A B : System} (T : Process A B) (hT : Channel T) :
      (comp (discard B) T).matrix = (discard A).matrix
  reset_event {A B : System} {p : Vec B} {e : Vec A}
      (hp : State B p) (he : Effect A e) :
      Event (comp (prepare p hp.1 hp.2.1) (test e he.1 (fun z => (he.2 z).1)))
  global_effects_separate {A : System} {v w : Vec A}
      (hv : Invariant A v) (hw : Invariant A w)
      (h : ∀ e, Effect A e → probability e v = probability e w) : v = w
  probability_interval {A : System} {e p : Vec A} (he : Effect A e) (hp : State A p) :
      0 ≤ probability e p ∧ probability e p ≤ 1
  cone_generating {A : System} {v : Vec A} (hv : Invariant A v) :
      ∃ p q : Vec A, Invariant A p ∧ Positive p ∧ Invariant A q ∧ Positive q ∧ v = p - q
  normalization_faithful {A : System} {p : Vec A} (hp : Positive p)
      (hm : mass p = 0) : p = 0
  normalized_preparations_span {A : System} {v : Vec A} (hv : Invariant A v) :
      ∀ x, v x = ∑ a, v a * orbit A a x
  instrument_event {A B : System} {I : Type} [Fintype I]
      (T : I → Process A B) (hT : Instrument T) (i : I) : Event (T i)
  instrument_probability {A B : System} {I : Type} [Fintype I]
      (T : I → Process A B) (hT : Instrument T) (p : Vec A) :
      (∑ i, mass (act (T i) p)) = mass p
  instrument_adaptive {A B C : System} {I J : Type} [Fintype I] [Fintype J]
      (T : I → Process A B) (S : I → J → Process B C)
      (hT : Instrument T) (hS : ∀ i, Instrument (S i)) :
      Instrument (fun ij : I × J => comp (S ij.1 ij.2) (T ij.1))
  instrument_parallel {A B C D : System} {I J : Type} [Fintype I] [Fintype J]
      (T : I → Process A B) (S : J → Process C D)
      (hT : Instrument T) (hS : Instrument S) :
      Instrument (fun ij : I × J => parallel (T ij.1) (S ij.2))
  instrument_coarse {A B : System} {I J : Type} [Fintype I] [Fintype J]
      (T : I → Process A B) (hT : Instrument T) (f : I → J) : Instrument (coarse T f)
  event_completion {A B : System} (T : Process A B) (hT : Event T) (b : B) :
      Instrument (fun i : Bool => if i then T else failure T hT b)
  record_channel {A B : System} {I : Type} [Fintype I] [Nonempty I]
      (T : I → Process A B) (hT : Instrument T) : Channel (record T)
  controlled_channel {A B : System} {I : Type} [Fintype I] [Nonempty I]
      (T : I → Process A B) (hT : ∀ i, Channel (T i)) : Channel (controlled T)
  no_signalling {A B C D : System} (T : Process A B) (S : Process C D)
      (hS : Channel S) (p : Vec (A ⊗ₛ C)) :
      marginal (act (parallel T S) p) = act T (marginal p)
  ancillary_process_separation {A B : System} (T S : Process A B)
      (h : ∀ e, Effect (B ⊗ₛ A) e →
        probability e (act (parallel T (identity A)) (correlation A)) =
        probability e (act (parallel S (identity A)) (correlation A))) : T.matrix = S.matrix
  comp_identity {A B : System} (T : Process A B) :
      (comp T (identity A)).matrix = T.matrix ∧ (comp (identity B) T).matrix = T.matrix
  parallel_identity (A B : System) :
      (parallel (identity A) (identity B)).matrix = (identity (A ⊗ₛ B)).matrix
  rename_channel {A B : System} (e : Wire A B) : Channel (rename e)
  rename_then {A B C : System} (e : Wire A B) (f : Wire B C) :
      (comp (rename f) (rename e)).matrix = (rename (e.then f)).matrix
  rename_inverse {A B : System} (e : Wire A B) :
      (comp (rename e.inverse) (rename e)).matrix = (identity A).matrix
  associator_naturality {A B C D E F : System}
      (T : Process A B) (S : Process C D) (R : Process E F) :
      (comp (rename (associator B D F)) (parallel (parallel T S) R)).matrix =
      (comp (parallel T (parallel S R)) (rename (associator A C E))).matrix
  swap_naturality {A B C D : System} (T : Process A B) (S : Process C D) :
      (comp (rename (swap B D)) (parallel T S)).matrix =
      (comp (parallel S T) (rename (swap A C))).matrix
  left_unit_naturality {A B : System} (T : Process A B) :
      (comp (rename (leftUnit B)) (parallel (identity unit) T)).matrix =
      (comp T (rename (leftUnit A))).matrix
  right_unit_naturality {A B : System} (T : Process A B) :
      (comp (rename (rightUnit B)) (parallel T (identity unit))).matrix =
      (comp T (rename (rightUnit A))).matrix
  pentagon (A B C D : System) :
      (rename ((associator (A ⊗ₛ B) C D).then (associator A B (C ⊗ₛ D)))).matrix =
      (rename (((associator A B C).both (wireId D)).then
        ((associator A (B ⊗ₛ C) D).then ((wireId A).both (associator B C D))))).matrix
  triangle (A B : System) :
      (rename ((associator A unit B).then ((wireId A).both (leftUnit B)))).matrix =
      (rename ((rightUnit A).both (wireId B))).matrix
  symmetry (A B : System) :
      (rename ((swap A B).then (swap B A))).matrix = (rename (wireId (A ⊗ₛ B))).matrix
  hexagon (A B C : System) :
      (rename ((associator A B C).then ((swap A (B ⊗ₛ C)).then (associator B C A)))).matrix =
      (rename (((swap A B).both (wireId C)).then
        ((associator B A C).then ((wireId B).both (swap A C))))).matrix

  rename_id (A : System) : (rename (wireId A)).matrix = (identity A).matrix
  rename_both {A B C D : System} (e : Wire A B) (f : Wire C D) :
      (rename (e.both f)).matrix = (parallel (rename e) (rename f)).matrix

theorem operational_laws : OperationalLaws where
  rename_id := @OperationalIndependence.rename_id
  rename_both := @OperationalIndependence.rename_both
  product_state := @OperationalIndependence.product_state
  product_effect := @OperationalIndependence.product_effect
  independent_probabilities := @OperationalIndependence.independent_probabilities
  act_invariant := @OperationalIndependence.act_invariant
  act_positive := @OperationalIndependence.act_positive
  event_mass := @OperationalIndependence.event_mass
  channel_state := @OperationalIndependence.channel_state
  event_comp := @OperationalIndependence.event_comp
  channel_comp := @OperationalIndependence.channel_comp
  event_parallel := @OperationalIndependence.event_parallel
  channel_parallel := @OperationalIndependence.channel_parallel
  identity_channel := @OperationalIndependence.identity_channel
  act_comp := @OperationalIndependence.act_comp
  comp_assoc := @OperationalIndependence.comp_assoc
  interchange := @OperationalIndependence.interchange
  event_weighted := @OperationalIndependence.event_weighted
  channel_weighted := @OperationalIndependence.channel_weighted
  prepare_channel := @OperationalIndependence.prepare_channel
  test_event := @OperationalIndependence.test_event
  discard_channel := @OperationalIndependence.discard_channel
  discard_unique := @OperationalIndependence.discard_unique
  discard_comp := @OperationalIndependence.discard_comp
  reset_event := @OperationalIndependence.reset_event
  global_effects_separate := @OperationalIndependence.global_effects_separate
  probability_interval := @OperationalIndependence.probability_interval
  cone_generating := @OperationalIndependence.cone_generating
  normalization_faithful := @OperationalIndependence.normalization_faithful
  normalized_preparations_span := @OperationalIndependence.normalized_preparations_span
  instrument_event := @OperationalIndependence.instrument_event
  instrument_probability := @OperationalIndependence.instrument_probability
  instrument_adaptive := @OperationalIndependence.instrument_adaptive
  instrument_parallel := @OperationalIndependence.instrument_parallel
  instrument_coarse := @OperationalIndependence.instrument_coarse
  event_completion := @OperationalIndependence.event_completion
  record_channel := @OperationalIndependence.record_channel
  controlled_channel := @OperationalIndependence.controlled_channel
  no_signalling := @OperationalIndependence.no_signalling
  ancillary_process_separation := @OperationalIndependence.ancillary_process_separation
  comp_identity := @OperationalIndependence.comp_identity
  parallel_identity := @OperationalIndependence.parallel_identity
  rename_channel := @OperationalIndependence.rename_channel
  rename_then := @OperationalIndependence.rename_then
  rename_inverse := @OperationalIndependence.rename_inverse
  associator_naturality := @OperationalIndependence.associator_naturality
  swap_naturality := @OperationalIndependence.swap_naturality
  left_unit_naturality := @OperationalIndependence.left_unit_naturality
  right_unit_naturality := @OperationalIndependence.right_unit_naturality
  pentagon := @OperationalIndependence.pentagon
  triangle := @OperationalIndependence.triangle
  symmetry := @OperationalIndependence.symmetry
  hexagon := @OperationalIndependence.hexagon

/-- A closed subtheory with all ambient equivariant events and instruments.
The law certificate has no assumed fields: `operational_laws` constructs it. -/
structure OperationalModel where
  objects : Theory
  laws : OperationalLaws

def classicalModel : OperationalModel := ⟨classicalTheory, operational_laws⟩
def symmetricModel : OperationalModel := ⟨symmetricTheory, operational_laws⟩

/-- Independence relative to the stated finite causal convex operational package:
there are complete models on both sides of local tomography. -/
theorem operational_independence :
    ∃ C D : OperationalModel,
      LocallyTomographic C.objects ∧ ¬ LocallyTomographic D.objects :=
  ⟨classicalModel, symmetricModel, classicalTheory_tomographic, symmetricTheory_not_tomographic⟩

theorem operational_laws_do_not_force_tomography :
    ¬ ∀ M : OperationalModel, LocallyTomographic M.objects := by
  intro h
  exact symmetricTheory_not_tomographic (h symmetricModel)

theorem operational_laws_do_not_forbid_tomography :
    ¬ ∀ M : OperationalModel, ¬ LocallyTomographic M.objects := by
  intro h
  exact h classicalModel classicalTheory_tomographic

/-- The negative witness consists of normalized physical states and an admitted
joint effect, with equality against every pair of admitted local effects. -/
theorem normalized_hidden_witness :
    State (atom ⊗ₛ atom) rho ∧ State (atom ⊗ₛ atom) sigma ∧ rho ≠ sigma ∧
    Effect (atom ⊗ₛ atom) parity ∧
    (∀ e f, Effect atom e → Effect atom f →
      probability (product e f) rho = probability (product e f) sigma) ∧
    probability parity rho = 1 ∧ probability parity sigma = 0 :=
  ⟨hidden_states_normalized.1, hidden_states_normalized.2, hidden_states_distinct,
    parity_effect, product_tests_agree, parity_separates⟩

end OperationalIndependence

#print axioms OperationalIndependence.product_state
#print axioms OperationalIndependence.product_effect
#print axioms OperationalIndependence.independent_probabilities
#print axioms OperationalIndependence.act_invariant
#print axioms OperationalIndependence.act_positive
#print axioms OperationalIndependence.event_mass
#print axioms OperationalIndependence.channel_state
#print axioms OperationalIndependence.event_comp
#print axioms OperationalIndependence.channel_comp
#print axioms OperationalIndependence.event_parallel
#print axioms OperationalIndependence.channel_parallel
#print axioms OperationalIndependence.identity_channel
#print axioms OperationalIndependence.act_comp
#print axioms OperationalIndependence.comp_assoc
#print axioms OperationalIndependence.interchange
#print axioms OperationalIndependence.event_weighted
#print axioms OperationalIndependence.channel_weighted
#print axioms OperationalIndependence.prepare_channel
#print axioms OperationalIndependence.test_event
#print axioms OperationalIndependence.discard_channel
#print axioms OperationalIndependence.discard_unique
#print axioms OperationalIndependence.discard_comp
#print axioms OperationalIndependence.reset_event
#print axioms OperationalIndependence.global_effects_separate
#print axioms OperationalIndependence.probability_interval
#print axioms OperationalIndependence.cone_generating
#print axioms OperationalIndependence.normalization_faithful
#print axioms OperationalIndependence.normalized_preparations_span
#print axioms OperationalIndependence.instrument_event
#print axioms OperationalIndependence.instrument_probability
#print axioms OperationalIndependence.instrument_adaptive
#print axioms OperationalIndependence.instrument_parallel
#print axioms OperationalIndependence.instrument_coarse
#print axioms OperationalIndependence.event_completion
#print axioms OperationalIndependence.record_channel
#print axioms OperationalIndependence.controlled_channel
#print axioms OperationalIndependence.no_signalling
#print axioms OperationalIndependence.ancillary_process_separation
#print axioms OperationalIndependence.comp_identity
#print axioms OperationalIndependence.parallel_identity
#print axioms OperationalIndependence.rename_channel
#print axioms OperationalIndependence.rename_then
#print axioms OperationalIndependence.rename_inverse
#print axioms OperationalIndependence.associator_naturality
#print axioms OperationalIndependence.swap_naturality
#print axioms OperationalIndependence.left_unit_naturality
#print axioms OperationalIndependence.right_unit_naturality
#print axioms OperationalIndependence.pentagon
#print axioms OperationalIndependence.triangle
#print axioms OperationalIndependence.symmetry
#print axioms OperationalIndependence.hexagon
#print axioms OperationalIndependence.correlation_probe
#print axioms OperationalIndependence.operational_laws
#print axioms OperationalIndependence.operational_independence
#print axioms OperationalIndependence.operational_laws_do_not_force_tomography
#print axioms OperationalIndependence.operational_laws_do_not_forbid_tomography
#print axioms OperationalIndependence.normalized_hidden_witness
#print axioms OperationalIndependence.classical_tomography
#print axioms OperationalIndependence.atom_not_tomographic

#print axioms OperationalIndependence.rename_id
#print axioms OperationalIndependence.rename_both
