import Mathlib.Data.Set.Lattice

/-! AuthorityEffect: None. Relation lookup preserves genuine unavailability
and refuses missing defined targets; local coordinate updates, profile fibers
and collision/factor boundaries. Supplied interactions are premises. Rust
ordered admission, usize costs, first witness and provider refinement separate. -/
namespace TFQM.JointDynamics
variable {X L R P C : Type}

def resolve (lookup : X → Option Nat) (next : Option X) : Except X (Option Nat) :=
  match next with
  | none => .ok none
  | some x => match lookup x with
    | none => .error x
    | some row => .ok (some row)
theorem unavailable (lookup : X → Option Nat) : resolve lookup none = .ok none := rfl
theorem defined_found (lookup : X → Option Nat) (x : X) (row : Nat) (h : lookup x = some row) :
    resolve lookup (some x) = .ok (some row) := by simp only [resolve, h]
theorem defined_missing (lookup : X → Option Nat) (x : X) (h : lookup x = none) :
    resolve lookup (some x) = .error x := by simp only [resolve, h]
theorem no_missing_as_unavailable (lookup : X → Option Nat) (next : Option X) :
    resolve lookup next = .ok none ↔ next = none := by
  cases next with
  | none => simp only [resolve]
  | some x => cases h : lookup x <;> simp [resolve, h]
theorem success_found (lookup : X → Option Nat) (next : Option X) (row : Nat) :
    resolve lookup next = .ok (some row) ↔ ∃ x, next = some x ∧ lookup x = some row := by
  cases next with
  | none => simp [resolve]
  | some x => cases h : lookup x <;> simp [resolve, h]
theorem refusal_missing (lookup : X → Option Nat) (next : Option X) (x : X) :
    resolve lookup next = .error x ↔ next = some x ∧ lookup x = none := by
  cases next with
  | none => simp [resolve]
  | some y => cases h : lookup y <;> simp [resolve, h, eq_comm]

def leftTarget (step : L → Option L) (pair : L × R) : Option (L × R) :=
  (step pair.1).map (fun l => (l, pair.2))
def rightTarget (step : R → Option R) (pair : L × R) : Option (L × R) :=
  (step pair.2).map (fun r => (pair.1, r))
theorem left_none (step : L → Option L) (pair : L × R) (h : step pair.1 = none) :
    leftTarget step pair = none := by simp [leftTarget, h]
theorem left_some (step : L → Option L) (pair : L × R) (l : L) (h : step pair.1 = some l) :
    leftTarget step pair = some (l, pair.2) := by simp [leftTarget, h]
theorem right_none (step : R → Option R) (pair : L × R) (h : step pair.2 = none) :
    rightTarget step pair = none := by simp [rightTarget, h]
theorem right_some (step : R → Option R) (pair : L × R) (r : R) (h : step pair.2 = some r) :
    rightTarget step pair = some (pair.1, r) := by simp [rightTarget, h]
theorem left_closure (step : L → Option L) (relation : Set (L × R))
    (closed : ∀ pair ∈ relation, ∀ l, step pair.1 = some l → (l, pair.2) ∈ relation)
    (pair : L × R) (member : pair ∈ relation) (target : L × R)
    (found : leftTarget step pair = some target) : target ∈ relation := by
  cases h : step pair.1 with
  | none => simp [leftTarget, h] at found
  | some l =>
    have same : (l, pair.2) = target := by simpa [leftTarget, h] using found
    exact same ▸ closed pair member l h

def FiberConstant (profile : X → P) (classes : X → C) : Prop :=
  ∀ x y, profile x = profile y → classes x = classes y
theorem no_collision_iff (profile : X → P) (classes : X → C) :
    (¬∃ x y, profile x = profile y ∧ classes x ≠ classes y) ↔ FiberConstant profile classes := by
  constructor
  · intro absent x y same
    by_contra different
    exact absent ⟨x, y, same, different⟩
  · rintro constant ⟨x, y, same, different⟩
    exact different (constant x y same)
theorem collision_no_factor (profile : X → P) (classes : X → C) (x y : X)
    (same : profile x = profile y) (different : classes x ≠ classes y) :
    ¬∃ decoder : P → C, ∀ z, decoder (profile z) = classes z := by
  rintro ⟨decoder, law⟩
  exact different ((law x).symm.trans ((congrArg decoder same).trans (law y)))
noncomputable def factor (profile : X → P) (classes : X → C) (p : Set.range profile) : C :=
  classes (Classical.choose p.property)
theorem factor_spec (profile : X → P) (classes : X → C)
    (constant : FiberConstant profile classes) (x : X) :
    factor profile classes ⟨profile x, ⟨x, rfl⟩⟩ = classes x :=
  constant _ _ (Classical.choose_spec (show ∃ a, profile a = profile x from ⟨x, rfl⟩))
theorem factor_unique (profile : X → P) (classes : X → C) (f g : Set.range profile → C)
    (hf : ∀ x, f ⟨profile x, ⟨x, rfl⟩⟩ = classes x)
    (hg : ∀ x, g ⟨profile x, ⟨x, rfl⟩⟩ = classes x) : f = g := by
  funext p
  obtain ⟨x, hx⟩ := p.property
  have same : (⟨profile x, ⟨x, rfl⟩⟩ : Set.range profile) = p := Subtype.ext hx
  rw [← same]
  exact (hf x).trans (hg x).symm
theorem paired_profile {Q S : Type} (left : L → Q) (right : R → S) (a b : L × R) :
    (left a.1, right a.2) = (left b.1, right b.2) ↔ left a.1 = left b.1 ∧ right a.2 = right b.2 :=
  Prod.mk.injEq
theorem defined_observably_distinct (value : C) : (none : Option C) ≠ some value := by simp
end TFQM.JointDynamics

#print axioms TFQM.JointDynamics.unavailable
#print axioms TFQM.JointDynamics.defined_found
#print axioms TFQM.JointDynamics.defined_missing
#print axioms TFQM.JointDynamics.no_missing_as_unavailable
#print axioms TFQM.JointDynamics.success_found
#print axioms TFQM.JointDynamics.refusal_missing
#print axioms TFQM.JointDynamics.left_none
#print axioms TFQM.JointDynamics.left_some
#print axioms TFQM.JointDynamics.right_none
#print axioms TFQM.JointDynamics.right_some
#print axioms TFQM.JointDynamics.left_closure
#print axioms TFQM.JointDynamics.no_collision_iff
#print axioms TFQM.JointDynamics.collision_no_factor
#print axioms TFQM.JointDynamics.factor_spec
#print axioms TFQM.JointDynamics.factor_unique
#print axioms TFQM.JointDynamics.paired_profile
#print axioms TFQM.JointDynamics.defined_observably_distinct
