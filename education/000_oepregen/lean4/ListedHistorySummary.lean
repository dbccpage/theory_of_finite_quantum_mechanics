/-!
# Listed-history summary: a choice-free reconstruction

AuthorityEffect: None. This file is a proposal.

The pre-Genesis deposit (`000_pre_genesis_to_mssn/lean4/Paper.lean`) has a
proof of `history_report_criterion`: an answer `σ : H → S` factors through a
report `π : H → V` on the report image exactly when `σ` is constant on the
fibers of `π`. Its existence direction selects a representative with the
choice axiom.

This file states, and gives proofs of, the listed version the teaching text
(`03_results_and_arguments.md`, "Sufficient summaries") describes in prose:
on a listed population `hs : List H` with decidable report equality, the
first history in `hs` with the given report supplies the answer. No choice
axiom is used. Values with no listed history reporting them are refused with
`none`; nothing richer is offered.

Core Lean only: no `import`, no Mathlib.
-/
namespace PreMssnListed

variable {H V S : Type}

/-- Answer `answer` is constant on the fibers of `report`, among the listed
histories only. -/
def FiberConstantOn (hs : List H) (report : H → V) (answer : H → S) : Prop :=
  ∀ h ∈ hs, ∀ h' ∈ hs, report h = report h' → answer h = answer h'

instance [DecidableEq V] [DecidableEq S] (hs : List H) (report : H → V)
    (answer : H → S) : Decidable (FiberConstantOn hs report answer) :=
  inferInstanceAs
    (Decidable (∀ h ∈ hs, ∀ h' ∈ hs, report h = report h' → answer h = answer h'))

/-- First-match reconstruction: the answer of the first listed history whose
report is `v`, or `none` when no listed history reports `v`. -/
def recon [DecidableEq V] (hs : List H) (report : H → V) (answer : H → S)
    (v : V) : Option S :=
  (hs.find? (fun h => decide (report h = v))).map answer

/-- The deposit's report image, restated here so this file imports nothing. -/
def ReportImage (report : H → V) := {v : V // ∃ h, report h = v}

/-! ## List lemmas, by induction -/

/-- `find?` on a cons whose head satisfies `p`. -/
theorem find?_cons_true {p : H → Bool} {a : H} {t : List H} (ha : p a = true) :
    (a :: t).find? p = some a := by
  show (match p a with | true => some a | false => t.find? p) = some a
  rw [ha]

/-- `find?` on a cons whose head fails `p`. -/
theorem find?_cons_false {p : H → Bool} {a : H} {t : List H} (ha : p a = false) :
    (a :: t).find? p = t.find? p := by
  show (match p a with | true => some a | false => t.find? p) = t.find? p
  rw [ha]

/-- If some listed element satisfies `p`, `find?` returns a listed element
satisfying `p`. -/
theorem find?_of_mem {p : H → Bool} :
    ∀ {hs : List H} {h : H}, h ∈ hs → p h = true →
      ∃ h₀, hs.find? p = some h₀ ∧ h₀ ∈ hs ∧ p h₀ = true := by
  intro hs
  induction hs with
  | nil => intro h hmem; exact absurd hmem (List.not_mem_nil)
  | cons a t ih =>
    intro h hmem hp
    cases ha : p a with
    | true => exact ⟨a, find?_cons_true ha, List.mem_cons_self, ha⟩
    | false =>
      have hmem' : h ∈ t := by
        cases hmem with
        | head => exact absurd hp (by rw [ha]; exact Bool.false_ne_true)
        | tail _ ht => exact ht
      obtain ⟨h₀, hfind, hmem₀, hp₀⟩ := ih hmem' hp
      refine ⟨h₀, ?_, List.mem_cons_of_mem a hmem₀, hp₀⟩
      rw [find?_cons_false ha]
      exact hfind

/-- `find?` returns `none` exactly when no listed element satisfies `p`. -/
theorem find?_eq_none_iff' {p : H → Bool} :
    ∀ {hs : List H}, hs.find? p = none ↔ ∀ h ∈ hs, p h = false := by
  intro hs
  induction hs with
  | nil =>
    constructor
    · intro _ h hmem; exact absurd hmem (List.not_mem_nil)
    · intro _; rfl
  | cons a t ih =>
    constructor
    · intro hnone h hmem
      cases ha : p a with
      | true =>
        rw [find?_cons_true ha] at hnone
        exact nomatch hnone
      | false =>
        rw [find?_cons_false ha] at hnone
        cases hmem with
        | head => exact ha
        | tail _ hmem' => exact ih.mp hnone h hmem'
    · intro hall
      have ha : p a = false := hall a List.mem_cons_self
      rw [find?_cons_false ha]
      exact ih.mpr (fun h hmem => hall h (List.mem_cons_of_mem a hmem))

/-- `Option.get` of an option known to be `some a` is `a`. -/
theorem option_get_of_eq_some {α : Type} {o : Option α} {a : α}
    (e : o = some a) (hs : o.isSome = true) : o.get hs = a := by
  subst e
  rfl

/-! ## The five parts -/

/-- Part 1 (reconstruction). Fiber constancy on the listed population makes
first-match reconstruction return the answer of every listed history. -/
theorem recon_of_fiberConstant [DecidableEq V]
    (hs : List H) (report : H → V) (answer : H → S)
    (hc : FiberConstantOn hs report answer) :
    ∀ h ∈ hs, recon hs report answer (report h) = some (answer h) := by
  intro h hmem
  have hp : decide (report h = report h) = true := decide_eq_true rfl
  obtain ⟨h₀, hfind, hmem₀, hp₀⟩ :=
    find?_of_mem (p := fun h' => decide (report h' = report h)) hmem hp
  have heq : report h₀ = report h := of_decide_eq_true hp₀
  unfold recon
  rw [hfind]
  show some (answer h₀) = some (answer h)
  rw [hc h₀ hmem₀ h hmem heq]

/-- Part 2 (converse). If first-match reconstruction returns every listed
history's answer, the answer is constant on the listed fibers. -/
theorem fiberConstant_of_recon [DecidableEq V]
    (hs : List H) (report : H → V) (answer : H → S)
    (hr : ∀ h ∈ hs, recon hs report answer (report h) = some (answer h)) :
    FiberConstantOn hs report answer := by
  intro h hmem h' hmem' heq
  have e1 := hr h hmem
  have e2 := hr h' hmem'
  rw [heq] at e1
  rw [e1] at e2
  exact Option.some.inj e2

/-- Parts 1 and 2 together: the listed criterion is an equivalence. -/
theorem listed_history_report_criterion [DecidableEq V]
    (hs : List H) (report : H → V) (answer : H → S) :
    (∀ h ∈ hs, recon hs report answer (report h) = some (answer h)) ↔
      FiberConstantOn hs report answer :=
  ⟨fiberConstant_of_recon hs report answer, recon_of_fiberConstant hs report answer⟩

/-- Part 3 (refusal off the image). Reconstruction refuses with `none`
exactly when no listed history reports `v`. -/
theorem recon_eq_none_iff [DecidableEq V]
    (hs : List H) (report : H → V) (answer : H → S) (v : V) :
    recon hs report answer v = none ↔ ∀ h ∈ hs, report h ≠ v := by
  unfold recon
  constructor
  · intro hnone h hmem hv
    cases hfind : hs.find? (fun h => decide (report h = v)) with
    | none =>
      have hall := find?_eq_none_iff'.mp hfind h hmem
      have : decide (report h = v) = true := decide_eq_true hv
      rw [this] at hall
      exact Bool.noConfusion hall
    | some h₀ =>
      rw [hfind] at hnone
      exact nomatch hnone
  · intro hne
    have hnone : hs.find? (fun h => decide (report h = v)) = none :=
      find?_eq_none_iff'.mpr (fun h hmem => decide_eq_false (hne h hmem))
    rw [hnone]
    rfl

/-- Part 3, forward direction, as the prompt states it. -/
theorem recon_eq_none_of_off_image [DecidableEq V]
    (hs : List H) (report : H → V) (answer : H → S) (v : V)
    (hne : ∀ h ∈ hs, report h ≠ v) : recon hs report answer v = none :=
  (recon_eq_none_iff hs report answer v).mpr hne

/-- Part 3, converse direction, as the prompt states it. -/
theorem off_image_of_recon_eq_none [DecidableEq V]
    (hs : List H) (report : H → V) (answer : H → S) (v : V)
    (hnone : recon hs report answer v = none) : ∀ h ∈ hs, report h ≠ v :=
  (recon_eq_none_iff hs report answer v).mp hnone

/-- Part 4 (uniqueness on the listed image). Any `f : V → Option S` that
returns every listed history's answer agrees with `recon` on every listed
report. No fiber-constancy hypothesis is needed: `f` supplies it. -/
theorem recon_unique [DecidableEq V]
    (hs : List H) (report : H → V) (answer : H → S)
    (f : V → Option S) (hf : ∀ h ∈ hs, f (report h) = some (answer h)) :
    ∀ h ∈ hs, recon hs report answer (report h) = f (report h) := by
  intro h hmem
  have hp : decide (report h = report h) = true := decide_eq_true rfl
  obtain ⟨h₀, hfind, hmem₀, hp₀⟩ :=
    find?_of_mem (p := fun h' => decide (report h' = report h)) hmem hp
  have heq : report h₀ = report h := of_decide_eq_true hp₀
  unfold recon
  rw [hfind]
  show some (answer h₀) = f (report h)
  rw [← hf h₀ hmem₀, heq]

/-- Part 5 (bridge). With a complete listing and fiber constancy, `recon`
and `Option.get` build the deposit's `factor : ReportImage report → S`
with no choice axiom. -/
theorem listed_factor_exists [DecidableEq V]
    (hs : List H) (report : H → V) (answer : H → S)
    (complete : ∀ h, h ∈ hs)
    (hc : ∀ h h', report h = report h' → answer h = answer h') :
    ∃ factor : ReportImage report → S,
      ∀ h, factor ⟨report h, ⟨h, rfl⟩⟩ = answer h := by
  have hc' : FiberConstantOn hs report answer :=
    fun h _ h' _ heq => hc h h' heq
  have hsome : ∀ v : ReportImage report,
      (recon hs report answer v.val).isSome = true := by
    intro v
    obtain ⟨h, hh⟩ := v.property
    rw [← hh, recon_of_fiberConstant hs report answer hc' h (complete h)]
    rfl
  refine ⟨fun v => (recon hs report answer v.val).get (hsome v), ?_⟩
  intro h
  exact option_get_of_eq_some
    (recon_of_fiberConstant hs report answer hc' h (complete h))
    (hsome ⟨report h, ⟨h, rfl⟩⟩)

/-! ## Instance checks

Three histories `0, 1, 2 : Nat`; report `h % 2`, so histories `0` and `2`
share report `0`. -/

/-- Fiber constancy holds for answer `h % 2`, and `recon` returns the answers. -/
example : recon [0, 1, 2] (fun h : Nat => h % 2) (fun h : Nat => h % 2) 0 = some 0 := by
  decide
example : recon [0, 1, 2] (fun h : Nat => h % 2) (fun h : Nat => h % 2) 1 = some 1 := by
  decide
example : FiberConstantOn [0, 1, 2] (fun h : Nat => h % 2) (fun h : Nat => h % 2) := by
  decide
/-- Report `2` is off the listed image and is refused. -/
example : recon [0, 1, 2] (fun h : Nat => h % 2) (fun h : Nat => h % 2) 2 = none := by
  decide

/-- Fiber constancy fails for answer `h` itself: histories `0` and `2` share
report `0` with answers `0 ≠ 2`. -/
example : ¬ FiberConstantOn [0, 1, 2] (fun h : Nat => h % 2) (fun h : Nat => h) := by
  decide
/-- The concrete pair refuting part 2's hypothesis: history `2` is listed,
but `recon` returns history `0`'s answer. -/
example : recon [0, 1, 2] (fun h : Nat => h % 2) (fun h : Nat => h) 0 = some 0 := by
  decide
example :
    ¬ (∀ h ∈ [0, 1, 2],
        recon [0, 1, 2] (fun h : Nat => h % 2) (fun h : Nat => h) (h % 2) = some h) := by
  intro hyp
  have h2 := hyp 2 (by decide)
  exact absurd h2 (by decide)

end PreMssnListed

#print axioms PreMssnListed.recon_of_fiberConstant
#print axioms PreMssnListed.fiberConstant_of_recon
#print axioms PreMssnListed.listed_history_report_criterion
#print axioms PreMssnListed.recon_eq_none_iff
#print axioms PreMssnListed.recon_eq_none_of_off_image
#print axioms PreMssnListed.off_image_of_recon_eq_none
#print axioms PreMssnListed.recon_unique
#print axioms PreMssnListed.listed_factor_exists
