import Mathlib.Data.Set.Lattice

/-! AuthorityEffect: None. Exact finite-word transduction/product semantics,
kernel descent on realized states/profiles, and reachable-state lifting.
Rust finite admission, predecessor ranks, canonical BFS order and memory
allocation remain separate source/native obligations. No arbitrary history
action is replaced by a finite sample table. -/
namespace TFQM.HistoryContext
variable {M T I P V : Type}

def run (d : M → I → M) (state : M) : List I → M
  | [] => state
  | i :: word => run d (d state i) word
theorem run_empty (d : M → I → M) (state : M) : run d state [] = state := rfl
theorem run_append (d : M → I → M) (state : M) (a b : List I) :
    run d state (a ++ b) = run d (run d state a) b := by
  induction a generalizing state with
  | nil => rfl
  | cons i a ih => exact ih (d state i)

def scan (control : T → I → T) (emit : T → I → List I) (state : T) : List I → T × List I
  | [] => (state, [])
  | i :: word =>
    let tail := scan control emit (control state i) word
    (tail.1, emit state i ++ tail.2)
def step (d : M → I → M) (control : T → I → T) (emit : T → I → List I)
    (state : M × T × M) (i : I) : M × T × M :=
  (d state.1 i, control state.2.1 i, run d state.2.2 (emit state.2.1 i))
def productRun (d : M → I → M) (control : T → I → T) (emit : T → I → List I)
    (state : M × T × M) : List I → M × T × M
  | [] => state
  | i :: word => productRun d control emit (step d control emit state i) word
theorem step_source (d : M → I → M) (control : T → I → T) (emit : T → I → List I)
    (state : M × T × M) (i : I) : (step d control emit state i).1 = d state.1 i := rfl
theorem step_control (d : M → I → M) (control : T → I → T) (emit : T → I → List I)
    (state : M × T × M) (i : I) : (step d control emit state i).2.1 = control state.2.1 i := rfl
theorem step_output (d : M → I → M) (control : T → I → T) (emit : T → I → List I)
    (state : M × T × M) (i : I) :
    (step d control emit state i).2.2 = run d state.2.2 (emit state.2.1 i) := rfl
theorem product_correct (d : M → I → M) (control : T → I → T) (emit : T → I → List I)
    (source : M) (state : T) (output : M) (word : List I) :
    productRun d control emit (source, state, output) word =
      (run d source word, (scan control emit state word).1, run d output (scan control emit state word).2) := by
  induction word generalizing source state output with
  | nil => rfl
  | cons i word ih =>
    simp only [productRun, step, scan, run, ih, run_append]
theorem product_append (d : M → I → M) (control : T → I → T) (emit : T → I → List I)
    (state : M × T × M) (a b : List I) :
    productRun d control emit state (a ++ b) =
      productRun d control emit (productRun d control emit state a) b := by
  induction a generalizing state with
  | nil => rfl
  | cons i a ih => exact ih (step d control emit state i)

def transform (control : T → I → T) (emit : T → I → List I) (state : T)
    (initial : List I) (final : T → List I) (word : List I) : List I :=
  initial ++ (scan control emit state word).2 ++ final (scan control emit state word).1
theorem final_correct (d : M → I → M) (control : T → I → T) (emit : T → I → List I)
    (source : M) (state : T) (initial : List I) (final : T → List I) (word : List I) :
    let result := productRun d control emit (source, state, run d source initial) word
    run d result.2.2 (final result.2.1) =
      run d source (transform control emit state initial final word) := by
  simp only [product_correct, transform, run_append]
theorem reachable_successor (d : M → I → M) (control : T → I → T) (emit : T → I → List I)
    (initial state : M × T × M) (h : ∃ word, productRun d control emit initial word = state) (i : I) :
    ∃ word, productRun d control emit initial word = step d control emit state i := by
  obtain ⟨word, rfl⟩ := h
  exact ⟨word ++ [i], by rw [product_append]; rfl⟩
theorem closed_covers_all (d : M → I → M) (control : T → I → T) (emit : T → I → List I)
    (visited : Set (M × T × M))
    (closed : ∀ state ∈ visited, ∀ i, step d control emit state i ∈ visited)
    (state : M × T × M) (root : state ∈ visited) (word : List I) :
    productRun d control emit state word ∈ visited := by
  induction word generalizing state with
  | nil => exact root
  | cons i word ih => exact ih _ (closed state root i)

def FiberConstant (profile : List I → P) (image : List I → V) : Prop :=
  ∀ a b, profile a = profile b → image a = image b
noncomputable def factor (profile : List I → P) (image : List I → V) (p : Set.range profile) : V :=
  image (Classical.choose p.property)
theorem factor_spec (profile : List I → P) (image : List I → V)
    (constant : FiberConstant profile image) (word : List I) :
    factor profile image ⟨profile word, ⟨word, rfl⟩⟩ = image word :=
  constant _ _ (Classical.choose_spec (show ∃ w, profile w = profile word from ⟨word, rfl⟩))
theorem factor_iff (profile : List I → P) (image : List I → V) :
    (∃ f : Set.range profile → V, ∀ word, f ⟨profile word, ⟨word, rfl⟩⟩ = image word) ↔
      FiberConstant profile image := by
  constructor
  · rintro ⟨f, law⟩ a b same
    have h : (⟨profile a, ⟨a, rfl⟩⟩ : Set.range profile) = ⟨profile b, ⟨b, rfl⟩⟩ := Subtype.ext same
    exact (law a).symm.trans ((congrArg f h).trans (law b))
  · intro constant
    exact ⟨factor profile image, factor_spec profile image constant⟩
theorem collision_refuses (profile : List I → P) (image : List I → V) (a b : List I)
    (same : profile a = profile b) (different : image a ≠ image b) : ¬FiberConstant profile image :=
  fun h => different (h a b same)
theorem lifted_action (d : M → I → M) (initial : M) (action : M → M) (representative : M → List I)
    (section : ∀ state ∈ Set.range (run d initial), run d initial (representative (action state)) = action state)
    (word : List I) : run d initial (representative (action (run d initial word))) = action (run d initial word) :=
  section _ ⟨word, rfl⟩
theorem lift_requires_reachable (d : M → I → M) (initial : M) (action : M → M)
    (lift : List I → List I) (law : ∀ word, run d initial (lift word) = action (run d initial word))
    (word : List I) : action (run d initial word) ∈ Set.range (run d initial) :=
  ⟨lift word, law word⟩
theorem lift_exists (d : M → I → M) (initial : M) (action : M → M)
    (closed : ∀ word, action (run d initial word) ∈ Set.range (run d initial)) :
    ∃ lift : List I → List I, ∀ word, run d initial (lift word) = action (run d initial word) := by
  classical
  exact ⟨fun word => Classical.choose (closed word), fun word => Classical.choose_spec (closed word)⟩
end TFQM.HistoryContext

#print axioms TFQM.HistoryContext.run_empty
#print axioms TFQM.HistoryContext.run_append
#print axioms TFQM.HistoryContext.step_source
#print axioms TFQM.HistoryContext.step_control
#print axioms TFQM.HistoryContext.step_output
#print axioms TFQM.HistoryContext.product_correct
#print axioms TFQM.HistoryContext.product_append
#print axioms TFQM.HistoryContext.final_correct
#print axioms TFQM.HistoryContext.reachable_successor
#print axioms TFQM.HistoryContext.closed_covers_all
#print axioms TFQM.HistoryContext.factor_spec
#print axioms TFQM.HistoryContext.factor_iff
#print axioms TFQM.HistoryContext.collision_refuses
#print axioms TFQM.HistoryContext.lifted_action
#print axioms TFQM.HistoryContext.lift_requires_reachable
#print axioms TFQM.HistoryContext.lift_exists
