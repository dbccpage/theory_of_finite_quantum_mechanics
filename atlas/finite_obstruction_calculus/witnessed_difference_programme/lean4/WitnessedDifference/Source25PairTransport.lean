/-!
# Raw seed-25 pair transport and partial execution

The source loop sums counts over endpoint fibers. The matrix owner computes
`P M Pᵀ`. Their finite-sum formulas agree for every finite vertex list, map
and natural multiplicity table, including loops and empty fibers. This is
not repair-quotient descent. Counts and histories have no numerical bound.

The declared state/edit formulas below expose the five source cases and
retain raw states, every occurrence and both addition prices. Replacing fiber
loops by the matrix formula preserves this partial execution at all lengths.
Correspondence with Python/Rust parsing, ordering and concrete storage is a
separate source audit and finite differential test; Lean does not verify those
programs or the other Genesis seeds.
-/

namespace WitnessedDifference.Source25PairTransport

def sumOn : List Nat → (Nat → Nat) → Nat
  | [], _ => 0
  | x :: xs, f => f x + sumOn xs f

theorem sum_congr (xs : List Nat) (f g : Nat → Nat) (h : ∀ x, f x = g x) :
    sumOn xs f = sumOn xs g := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [sumOn, h, ih]

theorem sum_zero (xs : List Nat) : sumOn xs (fun _ => 0) = 0 := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [sumOn, ih, Nat.zero_add]

theorem sum_add (xs : List Nat) (f g : Nat → Nat) :
    sumOn xs (fun x => f x + g x) = sumOn xs f + sumOn xs g := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [sumOn, ih]; omega

theorem sum_mul_right (xs : List Nat) (f : Nat → Nat) (k : Nat) :
    sumOn xs f * k = sumOn xs (fun x => f x * k) := by
  induction xs with
  | nil => simp only [sumOn, Nat.zero_mul]
  | cons x xs ih => simp only [sumOn, Nat.add_mul, ih]

theorem sum_swap (xs ys : List Nat) (f : Nat → Nat → Nat) :
    sumOn xs (fun x => sumOn ys (f x)) = sumOn ys (fun y => sumOn xs (fun x => f x y)) := by
  induction xs with
  | nil => exact (sum_zero ys).symm
  | cons x xs ih =>
    change sumOn ys (f x) + sumOn xs (fun a => sumOn ys (f a)) =
      sumOn ys (fun y => f x y + sumOn xs (fun a => f a y))
    rw [sum_add, ih]

def incidence (q : Nat → Nat) (target source : Nat) : Nat :=
  if q source = target then 1 else 0

def fiberPush (vertices : List Nat) (q : Nat → Nat) (table : Nat → Nat → Nat)
    (i j : Nat) : Nat :=
  sumOn vertices (fun x => sumOn vertices (fun y =>
    if q x = i then if q y = j then table x y else 0 else 0))

/-- Entry of `(P M) Pᵀ`, in the actual matrix owner's product order. -/
def matrixPush (vertices : List Nat) (q : Nat → Nat) (table : Nat → Nat → Nat)
    (i j : Nat) : Nat :=
  sumOn vertices (fun y =>
    sumOn vertices (fun x => incidence q i x * table x y) * incidence q j y)

theorem incidence_entry (q : Nat → Nat) (table : Nat → Nat → Nat) (i j x y : Nat) :
    (incidence q i x * table x y) * incidence q j y =
      (if q x = i then if q y = j then table x y else 0 else 0) := by
  by_cases hi : q x = i <;> by_cases hj : q y = j <;>
    simp only [incidence, hi, hj, if_true, if_false, Nat.one_mul, Nat.mul_one,
      Nat.zero_mul, Nat.mul_zero]

/-- Exact universal algebraic refinement; no bounded sample or injectivity
of q is assumed. This covers identification as well as vertex injection. -/
theorem matrix_push_is_source_fiber_sum
    (vertices : List Nat) (q : Nat → Nat) (table : Nat → Nat → Nat) (i j : Nat) :
    matrixPush vertices q table i j = fiberPush vertices q table i j := by
  unfold matrixPush fiberPush
  calc
    sumOn vertices (fun y => sumOn vertices (fun x => incidence q i x * table x y) * incidence q j y) =
        sumOn vertices (fun y => sumOn vertices (fun x =>
          (incidence q i x * table x y) * incidence q j y)) := by
      apply sum_congr
      intro y
      exact sum_mul_right vertices _ _
    _ = sumOn vertices (fun x => sumOn vertices (fun y =>
          (incidence q i x * table x y) * incidence q j y)) := sum_swap vertices vertices _
    _ = sumOn vertices (fun x => sumOn vertices (fun y =>
          if q x = i then if q y = j then table x y else 0 else 0)) := by
      apply sum_congr
      intro x
      apply sum_congr
      intro y
      exact incidence_entry q table i j x y

theorem matrix_operator_equals_fiber_operator : matrixPush = fiberPush := by
  funext vertices q table i j
  exact matrix_push_is_source_fiber_sum vertices q table i j

abbrev Triple := Nat × Nat × Nat

structure State where
  n : Nat
  r : Nat → Nat → Nat
  s : Nat → Nat → Nat
  filled : List Triple

inductive Relation where
  | r | s
  deriving DecidableEq

inductive Change where
  | identify (x y : Nat)
  | remove (relation : Relation) (x y : Nat)
  | fill (x y z : Nat)
  | addTerm
  | addAssertion (relation : Relation) (x y : Nat)

def counts (state : State) (relation : Relation) :=
  match relation with | .r => state.r | .s => state.s

def wayRound (x y z : Nat) : Triple :=
  if x < y ∧ x < z then (x,y,z) else if y < z then (y,z,x) else (z,x,y)

def tripleLE (a b : Triple) : Bool :=
  decide (a.1 < b.1 ∨ (a.1 = b.1 ∧ (a.2.1 < b.2.1 ∨
    (a.2.1 = b.2.1 ∧ a.2.2 ≤ b.2.2))))

def normalize (triples : List Triple) : List Triple := triples.eraseDups.mergeSort tripleLE

def enabled (state : State) : Change → Bool
  | .identify x y => decide (x < y ∧ y < state.n)
  | .remove rel x y => decide (x < state.n ∧ y < state.n ∧ 0 < counts state rel x y)
  | .fill x y z => decide (x < y ∧ x < z ∧ y ≠ z ∧ y < state.n ∧ z < state.n ∧
      (x,y,z) ∉ state.filled)
  | .addTerm => true
  | .addAssertion _ x y => decide (x < state.n ∧ y < state.n)

def identificationMap (x y vertex : Nat) : Nat :=
  if vertex = y then x else vertex - (if y < vertex then 1 else 0)

def carry (q : Nat → Nat) (filled : List Triple) : List Triple :=
  normalize (filled.filterMap (fun t =>
    let a := q t.1
    let b := q t.2.1
    let c := q t.2.2
    if a ≠ b ∧ b ≠ c ∧ c ≠ a then some (wayRound a b c) else none))

def changeCount (table : Nat → Nat → Nat) (x y : Nat) (remove : Bool) : Nat → Nat → Nat :=
  fun a b => if a = x ∧ b = y then
    if remove then table a b - 1 else table a b + 1 else table a b

/-- The shared five declared edit cases, exposing only the pair-transport
implementation as a parameter. Source-list ordering is audited separately. -/
def stepWith (push : List Nat → (Nat → Nat) → (Nat → Nat → Nat) → Nat → Nat → Nat)
    (state : State) (change : Change) : Option State :=
  if enabled state change then some (match change with
    | .identify x y =>
      let q := identificationMap x y
      { n := state.n - 1, r := push (List.range state.n) q state.r,
        s := push (List.range state.n) q state.s, filled := carry q state.filled }
    | .addTerm =>
      { n := state.n + 1, r := push (List.range state.n) id state.r,
        s := push (List.range state.n) id state.s, filled := state.filled }
    | .fill x y z => { state with filled := normalize ((x,y,z) :: state.filled) }
    | .remove rel x y => match rel with
      | .r => { state with r := changeCount state.r x y true }
      | .s => { state with s := changeCount state.s x y true }
    | .addAssertion rel x y => match rel with
      | .r => { state with r := changeCount state.r x y false }
      | .s => { state with s := changeCount state.s x y false })
  else none

def sourceStep := stepWith fiberPush
def nativeFormulaStep := stepWith matrixPush

theorem all_declared_steps_preserved_and_reflected : nativeFormulaStep = sourceStep := by
  unfold nativeFormulaStep sourceStep
  rw [matrix_operator_equals_fiber_operator]

def additionPrice : Change → Nat × Nat
  | .addTerm => (1,0)
  | .addAssertion _ _ _ => (0,1)
  | _ => (0,0)

structure Execution where
  final : State
  states : List State
  occurrences : List Change
  termAdditions : Nat
  assertionAdditions : Nat

/-- Refused events abort the partial run; they are never admitted no-ops. -/
def execute (step : State → Change → Option State) (initial : State) : List Change → Option Execution
  | [] => some (Execution.mk initial [initial] [] 0 0)
  | change :: rest => do
      let after ← step initial change
      let tail ← execute step after rest
      let price := additionPrice change
      return Execution.mk tail.final (initial :: tail.states) (change :: tail.occurrences)
        (price.1 + tail.termAdditions) (price.2 + tail.assertionAdditions)

/-- Every finite history, with all raw intermediates, ordered occurrences and
both prices. Equality of Options also reflects every refused prefix. -/
theorem every_partial_run_and_paid_trace_preserved (initial : State) (events : List Change) :
    execute nativeFormulaStep initial events = execute sourceStep initial events := by
  rw [all_declared_steps_preserved_and_reflected]

end WitnessedDifference.Source25PairTransport

#print axioms WitnessedDifference.Source25PairTransport.sum_congr
#print axioms WitnessedDifference.Source25PairTransport.sum_zero
#print axioms WitnessedDifference.Source25PairTransport.sum_add
#print axioms WitnessedDifference.Source25PairTransport.sum_mul_right
#print axioms WitnessedDifference.Source25PairTransport.sum_swap
#print axioms WitnessedDifference.Source25PairTransport.incidence_entry
#print axioms WitnessedDifference.Source25PairTransport.matrix_push_is_source_fiber_sum
#print axioms WitnessedDifference.Source25PairTransport.matrix_operator_equals_fiber_operator
#print axioms WitnessedDifference.Source25PairTransport.all_declared_steps_preserved_and_reflected
#print axioms WitnessedDifference.Source25PairTransport.every_partial_run_and_paid_trace_preserved
