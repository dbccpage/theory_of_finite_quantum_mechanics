import Init
import Init.Data.List.Perm

/-!
Local exact laws for bounded native continuation reports. Counts are natural
numbers, signed totals are integers, and the combined count bound is four.
The reconstruction theorem derives injectivity; it does not assume it.

The layered model accepts an arbitrary supplied deterministic transition table
with three separate offer outcomes. It supports either terminal observation
profile by a supplied terminal readout. These declarations do not verify the
Rust or Python programs, their enumeration, the original source, the concrete
result-mark orbit computation, or the numeric raw-carrier class count. Binding
their tables and readouts to this model is a separate replay obligation.

Only core Lean is imported. The declared permitted axioms are `propext`,
`Quot.sound`, and `Classical.choice`. The printed audit reports choice in the
count and guard proofs; the layered lifting and composition proofs do not use
it. No custom axioms are introduced.
-/

namespace WitnessedDifference.NativeFutureCompression

def sumOn {I : Type} (indices : List I) (f : I → Int) : Int :=
  (indices.map f).sum

theorem sumOn_add {I : Type} (indices : List I) (f g : I → Int) :
    sumOn indices (fun i => f i + g i) = sumOn indices f + sumOn indices g := by
  induction indices with
  | nil => rfl
  | cons i is ih =>
    simp only [sumOn, List.map_cons, List.sum_cons] at ih ⊢
    omega

theorem sumOn_sub {I : Type} (indices : List I) (f g : I → Int) :
    sumOn indices (fun i => f i - g i) = sumOn indices f - sumOn indices g := by
  induction indices with
  | nil => rfl
  | cons i is ih =>
    simp only [sumOn, List.map_cons, List.sum_cons] at ih ⊢
    omega

theorem sumOn_zero {I : Type} (indices : List I) : sumOn indices (fun _ => 0) = 0 := by
  induction indices with
  | nil => rfl
  | cons i is ih => simpa [sumOn] using ih

theorem sumOn_swap {I J : Type} (is : List I) (js : List J) (f : I → J → Int) :
    sumOn is (fun i => sumOn js (f i)) = sumOn js (fun j => sumOn is (fun i => f i j)) := by
  induction is with
  | nil => exact (sumOn_zero js).symm
  | cons i is ih =>
    change sumOn js (f i) + sumOn is (fun x => sumOn js (f x)) =
      sumOn js (fun j => f i j + sumOn is (fun x => f x j))
    rw [sumOn_add, ih]

/-- Row subtraction and column addition preserve the complete signed total. -/
theorem normalization_preserves_signed_sum {I : Type} (is : List I)
    (table : I → I → Int) (potential : I → Int) :
    sumOn is (fun i => sumOn is (fun j => table i j - potential i + potential j)) =
      sumOn is (fun i => sumOn is (table i)) := by
  have potential_swap := sumOn_swap is is (fun i _ => potential i)
  simp only [sumOn_add, sumOn_sub]
  rw [potential_swap]
  exact Int.sub_add_cancel _ _

theorem sumOn_permutation {I : Type} {xs ys : List I} (permutation : xs.Perm ys)
    (f : I → Int) : sumOn xs f = sumOn ys f := by
  induction permutation with
  | nil => rfl
  | cons x same ih => simpa [sumOn] using congrArg (fun total => f x + total) ih
  | swap x y rest => simp only [sumOn, List.map_cons, List.sum_cons]; omega
  | trans first second ihFirst ihSecond => exact ihFirst.trans ihSecond

/-- A common permutation of the two complete index lists preserves the total. -/
theorem square_sum_permutation {I : Type} {xs ys : List I} (permutation : xs.Perm ys)
    (table : I → I → Int) :
    sumOn xs (fun i => sumOn xs (table i)) = sumOn ys (fun i => sumOn ys (table i)) := by
  calc
    _ = sumOn ys (fun i => sumOn xs (table i)) := sumOn_permutation permutation _
    _ = _ := congrArg (sumOn ys) (funext (fun i => sumOn_permutation permutation (table i)))

def signedSum : List Bool → List Nat → Int
  | [], _ => 0
  | _, [] => 0
  | sign :: signs, count :: counts =>
    (if sign then (count : Int) else -(count : Int)) + signedSum signs counts

def clipped (counts : List Nat) : List Nat := counts.map (fun count => min count 2)

theorem clipped_eq_self_of_sum_le_two (counts : List Nat) (bound : counts.sum ≤ 2) :
    clipped counts = counts := by
  induction counts with
  | nil => rfl
  | cons c cs ih =>
    have head : c ≤ 2 := by simp only [List.sum_cons] at bound; omega
    have tail : cs.sum ≤ 2 := by simp only [List.sum_cons] at bound; omega
    simp only [clipped, List.map_cons]
    rw [Nat.min_eq_left head]
    exact congrArg (List.cons c) (ih tail)

/-- Exact count reconstruction at total bound four, for any fixed sign list. -/
theorem clipped_signed_counts_unique (signs : List Bool) (xs ys : List Nat)
    (xlength : xs.length = signs.length) (ylength : ys.length = signs.length)
    (xbound : xs.sum ≤ 4) (ybound : ys.sum ≤ 4)
    (caps : clipped xs = clipped ys) (total : signedSum signs xs = signedSum signs ys) :
    xs = ys := by
  induction signs generalizing xs ys with
  | nil =>
    have hx : xs = [] := List.length_eq_zero_iff.mp xlength
    have hy : ys = [] := List.length_eq_zero_iff.mp ylength
    exact hx.trans hy.symm
  | cons sign signs ih =>
    cases xs with
    | nil => simp at xlength
    | cons x xs =>
      cases ys with
      | nil => simp at ylength
      | cons y ys =>
        have lensx : xs.length = signs.length := by simpa using xlength
        have lensy : ys.length = signs.length := by simpa using ylength
        have boundsx : x + xs.sum ≤ 4 := by simpa using xbound
        have boundsy : y + ys.sum ≤ 4 := by simpa using ybound
        have cap_parts : min x 2 = min y 2 ∧ clipped xs = clipped ys :=
          List.cons.inj caps
        by_cases small : x < 2
        · have heads : x = y := by have := cap_parts.1; omega
          subst y
          have totals : signedSum signs xs = signedSum signs ys := by
            cases sign <;> simp only [signedSum, Bool.false_eq_true, if_false, if_true] at total <;>
              omega
          have tails := ih xs ys lensx lensy (by omega) (by omega) cap_parts.2 totals
          exact congrArg (List.cons x) tails
        · have bigy : 2 ≤ y := by have := cap_parts.1; omega
          have tailx : xs.sum ≤ 2 := by omega
          have taily : ys.sum ≤ 2 := by omega
          have tails : xs = ys := by
            have h := cap_parts.2
            rw [clipped_eq_self_of_sum_le_two xs tailx,
              clipped_eq_self_of_sum_le_two ys taily] at h
            exact h
          subst ys
          have heads : x = y := by
            cases sign <;> simp only [signedSum, Bool.false_eq_true, if_false, if_true] at total <;>
              omega
          exact congrArg (fun z => z :: xs) heads

/-- The second answer is the positive-count guard after one removal. -/
def removalAnswers (count : Nat) : Bool × Bool :=
  (decide (0 < count), decide (0 < count - 1))

theorem two_removal_answers_determine_clip (x y : Nat)
    (answers : removalAnswers x = removalAnswers y) : min x 2 = min y 2 := by
  have first := congrArg Prod.fst answers
  have second := congrArg Prod.snd answers
  simp only [removalAnswers, decide_eq_decide] at first second
  omega

theorem removal_answers_determine_clips (xs ys : List Nat)
    (answers : xs.map removalAnswers = ys.map removalAnswers) : clipped xs = clipped ys := by
  induction xs generalizing ys with
  | nil => cases ys <;> simp_all [clipped]
  | cons x xs ih =>
    cases ys with
    | nil => simp at answers
    | cons y ys =>
      obtain ⟨head, tail⟩ := List.cons.inj answers
      change min x 2 :: clipped xs = min y 2 :: clipped ys
      rw [two_removal_answers_determine_clip x y head, ih ys tail]

def BoundedCounts (signs : List Bool) :=
  { counts : List Nat // counts.length = signs.length ∧ counts.sum ≤ 4 }

def countReport (signs : List Bool) (counts : BoundedCounts signs) :
    Int × List (Bool × Bool) :=
  (signedSum signs counts.val, counts.val.map removalAnswers)

theorem count_report_injective (signs : List Bool) : Function.Injective (countReport signs) := by
  intro xs ys same
  apply Subtype.ext
  apply clipped_signed_counts_unique signs xs.val ys.val xs.property.1 ys.property.1
    xs.property.2 ys.property.2
  · exact removal_answers_determine_clips _ _ (congrArg Prod.snd same)
  · exact congrArg Prod.fst same

/-- Every unequal admitted pair differs in a signed total or a removal answer. -/
theorem unequal_counts_have_separating_observation (signs : List Bool)
    (xs ys : BoundedCounts signs) (different : xs ≠ ys) :
    countReport signs xs ≠ countReport signs ys := by
  intro same
  exact different (count_report_injective signs same)

/-- Any report retaining the two stated observations has only singleton fibres. -/
theorem adequate_report_is_injective {Q : Type} (signs : List Bool)
    (report : BoundedCounts signs → Q)
    (retains : ∀ xs ys, report xs = report ys → countReport signs xs = countReport signs ys) :
    Function.Injective report := by
  intro xs ys same
  exact count_report_injective signs (retains xs ys same)

/-- A count of five admits a collision, so the theorem's numerical bound matters. -/
theorem bound_five_clipped_collision :
    clipped [2, 3] = clipped [3, 2] ∧
      signedSum [true, true] [2, 3] = signedSum [true, true] [3, 2] ∧
      ([2, 3] : List Nat) ≠ [3, 2] := by decide

abbrev Price := Nat × Nat

def priceAdd (p q : Price) : Price := (p.1 + q.1, p.2 + q.2)

theorem priceAdd_zero (p : Price) : priceAdd p (0, 0) = p := by
  cases p; simp [priceAdd]

theorem zero_priceAdd (p : Price) : priceAdd (0, 0) p = p := by
  cases p; simp [priceAdd]

theorem priceAdd_assoc (p q r : Price) : priceAdd (priceAdd p q) r = priceAdd p (priceAdd q r) := by
  apply Prod.ext <;> simp [priceAdd, Nat.add_assoc]

/-- Refusal outcomes retain different data and have no successor. -/
inductive Offer (S : Type) where
  | disabled
  | excluded (price : Price)
  | admitted (price : Price) (next : S)

def Offer.map {S Q : Type} (f : S → Q) : Offer S → Offer Q
  | .disabled => .disabled
  | .excluded p => .excluded p
  | .admitted p s => .admitted p (f s)

def Signature (Terminal Present Action : Type) : Nat → Type
  | 0 => Terminal
  | h + 1 => Present × (Action → Offer (Signature Terminal Present Action h))

/-- The terminal readout can contain only present answers or also offer statuses. -/
def signature {S Terminal Present Action : Type} (terminal : S → Terminal)
    (present : S → Present) (step : S → Action → Offer S) :
    (h : Nat) → S → Signature Terminal Present Action h
  | 0, s => terminal s
  | h + 1, s => (present s, fun a => Offer.map (signature terminal present step h) (step s a))

theorem step_projection {S Terminal Present Action : Type} (terminal : S → Terminal)
    (present : S → Present) (step : S → Action → Offer S) (h : Nat) (s t : S)
    (a : Action) (p : Price) (edge : step s a = .admitted p t) :
    (signature terminal present step (h + 1) s).2 a =
      .admitted p (signature terminal present step h t) := by
  simp [signature, edge, Offer.map]

/-- Every admitted signature edge lifts from its supplied original state. -/
theorem step_reflection {S Terminal Present Action : Type} (terminal : S → Terminal)
    (present : S → Present) (step : S → Action → Offer S) (h : Nat) (s : S)
    (a : Action) (p : Price) (target : Signature Terminal Present Action h)
    (edge : (signature terminal present step (h + 1) s).2 a = .admitted p target) :
    ∃ t, step s a = .admitted p t ∧ signature terminal present step h t = target := by
  cases native : step s a with
  | disabled => simp [signature, native, Offer.map] at edge
  | excluded cost => simp [signature, native, Offer.map] at edge
  | admitted cost t =>
    have parts : cost = p ∧ signature terminal present step h t = target := by
      simpa [signature, native, Offer.map] using edge
    exact ⟨t, by rw [parts.1], parts.2⟩

/-- A successful path retains every action occurrence, including zero-price ones. -/
inductive FinePath {S Action : Type} (step : S → Action → Offer S) :
    S → List Action → Price → S → Prop where
  | nil (s : S) : FinePath step s [] (0, 0) s
  | cons {s t u : S} {a : Action} {actions : List Action} {p q : Price}
      (edge : step s a = .admitted p t) (rest : FinePath step t actions q u) :
      FinePath step s (a :: actions) (priceAdd p q) u

/-- The remaining horizon is a type index, so a suffix cannot reset it. -/
inductive LayerPath {Terminal Present Action : Type} :
    {h k : Nat} → Signature Terminal Present Action h → List Action → Price →
      Signature Terminal Present Action k → Prop where
  | nil {h : Nat} (q : Signature Terminal Present Action h) : LayerPath q [] (0, 0) q
  | cons {h k : Nat} {q : Signature Terminal Present Action (h + 1)}
      {child : Signature Terminal Present Action h} {target : Signature Terminal Present Action k}
      {a : Action} {actions : List Action} {p r : Price}
      (edge : q.2 a = .admitted p child) (rest : LayerPath child actions r target) :
      LayerPath q (a :: actions) (priceAdd p r) target

theorem layer_path_length {Terminal Present Action : Type} {h k : Nat}
    {source : Signature Terminal Present Action h} {target : Signature Terminal Present Action k}
    {actions : List Action} {price : Price} (path : LayerPath source actions price target) :
    h = k + actions.length := by
  induction path with
  | nil => simp
  | cons edge rest ih => simp only [List.length_cons]; omega

theorem fine_path_append {S Action : Type} {step : S → Action → Offer S}
    {s t u : S} {left right : List Action} {p q : Price}
    (first : FinePath step s left p t) (second : FinePath step t right q u) :
    FinePath step s (left ++ right) (priceAdd p q) u := by
  induction first with
  | nil => simpa [zero_priceAdd] using second
  | cons edge rest ih =>
    simpa only [List.cons_append, priceAdd_assoc] using FinePath.cons edge (ih second)

theorem fine_path_deterministic {S Action : Type} {step : S → Action → Offer S}
    {s t u : S} {actions : List Action} {p q : Price}
    (first : FinePath step s actions p t) (second : FinePath step s actions q u) :
    p = q ∧ t = u := by
  induction first generalizing q u with
  | nil => cases second; exact ⟨rfl, rfl⟩
  | cons edge rest ih =>
    cases second with
    | cons otherEdge otherRest =>
      obtain ⟨samePrice, sameState⟩ := Offer.admitted.inj (edge.symm.trans otherEdge)
      cases samePrice
      cases sameState
      obtain ⟨rfl, rfl⟩ := ih otherRest
      exact ⟨rfl, rfl⟩

theorem layer_path_append {Terminal Present Action : Type} {h k j : Nat}
    {s : Signature Terminal Present Action h} {t : Signature Terminal Present Action k}
    {u : Signature Terminal Present Action j} {left right : List Action} {p q : Price}
    (first : LayerPath s left p t) (second : LayerPath t right q u) :
    LayerPath s (left ++ right) (priceAdd p q) u := by
  induction first with
  | nil => simpa [zero_priceAdd] using second
  | cons edge rest ih =>
    simpa only [List.cons_append, priceAdd_assoc] using LayerPath.cons edge (ih second)

theorem project_fine_path {S Terminal Present Action : Type} (terminal : S → Terminal)
    (present : S → Present) (step : S → Action → Offer S)
    {s t : S} {actions : List Action} {price : Price}
    (path : FinePath step s actions price t) (remaining : Nat) :
    LayerPath (signature terminal present step (remaining + actions.length) s) actions price
      (signature terminal present step remaining t) := by
  induction path with
  | nil s => exact LayerPath.nil _
  | @cons s t u a actions p q edge rest ih =>
    simpa only [List.length_cons, Nat.add_succ] using
      LayerPath.cons (step_projection terminal present step _ s t a p edge) ih

/-- This constructive lift starts with the retained source, not a chosen representative. -/
theorem lift_layer_path {S Terminal Present Action : Type} (terminal : S → Terminal)
    (present : S → Present) (step : S → Action → Offer S)
    {h k : Nat} {source : Signature Terminal Present Action h}
    {target : Signature Terminal Present Action k} {actions : List Action} {price : Price}
    (path : LayerPath source actions price target) :
    ∀ s, signature terminal present step h s = source →
      ∃ t, FinePath step s actions price t ∧ signature terminal present step k t = target := by
  induction path with
  | nil source =>
    intro s same
    exact ⟨s, FinePath.nil s, same⟩
  | cons edge rest ih =>
    intro s same
    have edge' := edge
    rw [← same] at edge'
    obtain ⟨t, native, projected⟩ := step_reflection terminal present step _ s _ _ _ edge'
    obtain ⟨u, nativeRest, endpoint⟩ := ih t projected
    exact ⟨u, FinePath.cons native nativeRest, endpoint⟩

theorem lifted_empty_path_is_identity {S Action : Type} {step : S → Action → Offer S}
    {s t : S} {p : Price} (path : FinePath step s [] p t) : t = s ∧ p = (0, 0) := by
  cases path
  exact ⟨rfl, rfl⟩

theorem zero_price_step_retains_occurrence {S Action : Type} {step : S → Action → Offer S}
    {s t : S} {a : Action} (edge : step s a = .admitted (0, 0) t) :
    FinePath step s [a] (0, 0) t ∧ ([a] : List Action).length = 1 := by
  exact ⟨FinePath.cons edge (FinePath.nil t), rfl⟩

/-- The path alphabet supplies occurrence counts independently of its prices. -/
theorem occurrence_count_composes {Action : Type} (left right : List Action) :
    (left ++ right).length = left.length + right.length := List.length_append

theorem horizon_two_composition_bound {Terminal Present Action : Type}
    {s : Signature Terminal Present Action 2} {k j : Nat}
    {t : Signature Terminal Present Action k} {u : Signature Terminal Present Action j}
    {left right : List Action} {p q : Price}
    (first : LayerPath s left p t) (second : LayerPath t right q u) :
    left.length + right.length ≤ 2 := by
  have h := layer_path_length (layer_path_append first second)
  rw [List.length_append] at h
  omega

end WitnessedDifference.NativeFutureCompression

#print axioms WitnessedDifference.NativeFutureCompression.normalization_preserves_signed_sum
#print axioms WitnessedDifference.NativeFutureCompression.square_sum_permutation
#print axioms WitnessedDifference.NativeFutureCompression.clipped_signed_counts_unique
#print axioms WitnessedDifference.NativeFutureCompression.two_removal_answers_determine_clip
#print axioms WitnessedDifference.NativeFutureCompression.removal_answers_determine_clips
#print axioms WitnessedDifference.NativeFutureCompression.count_report_injective
#print axioms WitnessedDifference.NativeFutureCompression.unequal_counts_have_separating_observation
#print axioms WitnessedDifference.NativeFutureCompression.adequate_report_is_injective
#print axioms WitnessedDifference.NativeFutureCompression.bound_five_clipped_collision
#print axioms WitnessedDifference.NativeFutureCompression.step_projection
#print axioms WitnessedDifference.NativeFutureCompression.step_reflection
#print axioms WitnessedDifference.NativeFutureCompression.layer_path_length
#print axioms WitnessedDifference.NativeFutureCompression.fine_path_append
#print axioms WitnessedDifference.NativeFutureCompression.fine_path_deterministic
#print axioms WitnessedDifference.NativeFutureCompression.layer_path_append
#print axioms WitnessedDifference.NativeFutureCompression.project_fine_path
#print axioms WitnessedDifference.NativeFutureCompression.lift_layer_path
#print axioms WitnessedDifference.NativeFutureCompression.lifted_empty_path_is_identity
#print axioms WitnessedDifference.NativeFutureCompression.zero_price_step_retains_occurrence
#print axioms WitnessedDifference.NativeFutureCompression.occurrence_count_composes
#print axioms WitnessedDifference.NativeFutureCompression.horizon_two_composition_bound
