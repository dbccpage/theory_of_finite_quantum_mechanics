import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. The concrete Maybe value model and finite observed
clone/law flags. Passing finite samples is not universal verification of a generic
Monad, arbitrary callbacks or exhaustive domain coverage. Rust callback/Eq/Clone
semantics and usize/Vec correspondence require separate source/native evidence.
-/
namespace TFQM.EMSamples

def bind (x : Option A) (f : A → Option B) : Option B :=
  match x with | none => none | some a => f a
def join (x : Option (Option A)) : Option A := bind x id

theorem bind_left (a : A) (f : A → Option B) : bind (some a) f = f a := rfl
theorem bind_right (x : Option A) : bind x some = x := by cases x <;> rfl
theorem bind_associative (x : Option A) (f : A → Option B) (g : B → Option C) :
    bind (bind x f) g = bind x (fun a => bind (f a) g) := by cases x <;> rfl
theorem map_identity (x : Option A) : Option.map id x = x := by cases x <;> rfl
theorem map_composition (x : Option A) (f : A → B) (g : B → C) :
    Option.map g (Option.map f x) = Option.map (fun a => g (f a)) x := by cases x <;> rfl
theorem join_spec (x : Option (Option A)) : join x = bind x id := rfl
theorem free_unit (x : Option A) : join (some x) = x := rfl
theorem free_associativity (x : Option (Option (Option A))) :
    join (Option.map join x) = join (join x) := by
  cases x with
  | none => rfl
  | some value => cases value <;> rfl

inductive Law where | unit | associativity | morphism deriving DecidableEq
inductive Refusal where
  | clone (law : Law) (index : Nat)
  | violated (law : Law) (index : Nat)
  deriving DecidableEq

def step (law : Law) (index : Nat) (copyOK lawOK : Bool) : Except Refusal Unit :=
  if copyOK then
    if lawOK then .ok () else .error (.violated law index)
  else .error (.clone law index)
theorem clone_first (law : Law) (index : Nat) (lawOK : Bool) :
    step law index false lawOK = .error (.clone law index) := rfl
theorem law_after_clone (law : Law) (index : Nat) :
    step law index true false = .error (.violated law index) := rfl
theorem step_pass (law : Law) (index : Nat) : step law index true true = .ok () := rfl

def scan (law : Law) : List (Bool × Bool) → Nat → Except Refusal Unit
  | [], _ => .ok ()
  | (copyOK,lawOK)::tail, index => match step law index copyOK lawOK with
    | .error e => .error e
    | .ok () => scan law tail (index+1)
theorem scan_empty (law : Law) (index : Nat) : scan law [] index = .ok () := rfl
theorem scan_ok_iff (law : Law) (samples : List (Bool × Bool)) (index : Nat) :
    scan law samples index = .ok () ↔ ∀ p ∈ samples, p.1 = true ∧ p.2 = true := by
  induction samples generalizing index with
  | nil => simp [scan]
  | cons head tail ih =>
    rcases head with ⟨a,b⟩
    cases a <;> cases b <;> simp [scan,step,ih]

def algebra (units assocs : List (Bool × Bool)) : Except Refusal (Nat × Nat) :=
  match scan .unit units 0 with
  | .error e => .error e
  | .ok () => match scan .associativity assocs 0 with
    | .error e => .error e
    | .ok () => .ok (units.length,assocs.length)
theorem algebra_empty : algebra [] [] = .ok (0,0) := rfl
theorem unit_before_associativity (units assocs : List (Bool × Bool)) (e : Refusal)
    (h : scan .unit units 0 = .error e) : algebra units assocs = .error e := by simp [algebra,h]
theorem observed_counts (units assocs : List (Bool × Bool))
    (hu : scan .unit units 0 = .ok ()) (ha : scan .associativity assocs 0 = .ok ()) :
    algebra units assocs = .ok (units.length,assocs.length) := by simp [algebra,hu,ha]

end TFQM.EMSamples

#print axioms TFQM.EMSamples.bind_left
#print axioms TFQM.EMSamples.bind_right
#print axioms TFQM.EMSamples.bind_associative
#print axioms TFQM.EMSamples.map_identity
#print axioms TFQM.EMSamples.map_composition
#print axioms TFQM.EMSamples.join_spec
#print axioms TFQM.EMSamples.free_unit
#print axioms TFQM.EMSamples.free_associativity
#print axioms TFQM.EMSamples.clone_first
#print axioms TFQM.EMSamples.law_after_clone
#print axioms TFQM.EMSamples.step_pass
#print axioms TFQM.EMSamples.scan_empty
#print axioms TFQM.EMSamples.scan_ok_iff
#print axioms TFQM.EMSamples.algebra_empty
#print axioms TFQM.EMSamples.unit_before_associativity
#print axioms TFQM.EMSamples.observed_counts
