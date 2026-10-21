import Mathlib.Logic.Function.Basic

/-!
# Pre-Genesis summary over explicitly listed histories: first-match reconstruction without choice

AuthorityEffect: None.  Scope: a list `hs : List H` of histories, a report `report : H -> V` with
`DecidableEq V`, an answer `answer : H -> S`.  Own re-derivation (structural recursion, not the source's
`List.find?` route) of the listed criterion declared in `ListedHistorySummary.lean`.

What the kernel reports is recorded by the `#print axioms` lines at the end of this file.  Everything about
`recon` itself (reconstruction, converse, refusal, uniqueness on the listed reports, the bridge to the
image-factorization of node PG-HISTORY-REPORT-CRITERION) uses no `Classical.choice`.  The one statement that
does is the explicitly classical variant `reconC` for a report type WITHOUT a decidable equality: there the
decidability instance is manufactured by `Classical.propDecidable`, which is where the choice axiom enters.
The sibling file `HistoryReport.lean` (node 163) is not repeated here.
-/

namespace PregenConstructive

universe u v w
variable {H : Type u} {V : Type v} {S : Type w}

/-- Constant on report fibers, among the listed histories only. -/
def FiberConstantOn (hs : List H) (report : H → V) (answer : H → S) : Prop :=
  ∀ h ∈ hs, ∀ h' ∈ hs, report h = report h' → answer h = answer h'

/-- First-match reconstruction: the answer of the first listed history reporting `x`, else `none`. -/
def recon [DecidableEq V] (report : H → V) (answer : H → S) (x : V) : List H → Option S
  | [] => none
  | h :: t => if report h = x then some (answer h) else recon report answer x t

@[simp] theorem recon_nil [DecidableEq V] (report : H → V) (answer : H → S) (x : V) :
    recon report answer x [] = none := rfl

theorem recon_cons_of_eq [DecidableEq V] {report : H → V} {answer : H → S} {x : V} {a : H} (t : List H)
    (h : report a = x) : recon report answer x (a :: t) = some (answer a) := by
  show (if report a = x then some (answer a) else recon report answer x t) = _
  split
  · rfl
  · contradiction

theorem recon_cons_of_ne [DecidableEq V] {report : H → V} {answer : H → S} {x : V} {a : H} (t : List H)
    (h : report a ≠ x) : recon report answer x (a :: t) = recon report answer x t := by
  show (if report a = x then some (answer a) else recon report answer x t) = _
  split
  · contradiction
  · rfl

theorem fiberConstantOn_tail {hs : List H} {a : H} {report : H → V} {answer : H → S}
    (hc : FiberConstantOn (a :: hs) report answer) : FiberConstantOn hs report answer :=
  fun h hm h' hm' e => hc h (List.mem_cons_of_mem a hm) h' (List.mem_cons_of_mem a hm') e

/-- Reconstruction: fiber constancy on the listing makes first-match return every listed answer. -/
theorem recon_of_fiberConstant [DecidableEq V] (report : H → V) (answer : H → S) :
    ∀ hs : List H, FiberConstantOn hs report answer →
      ∀ h ∈ hs, recon report answer (report h) hs = some (answer h)
  | [], _, _, hm => nomatch hm
  | a :: t, hc, h, hm => by
      by_cases e : report a = report h
      · rw [recon_cons_of_eq t e]
        exact congrArg some (hc a (List.mem_cons_self) h hm e)
      · rw [recon_cons_of_ne t e]
        have hmt : h ∈ t := by
          cases hm with
          | head => exact absurd rfl e
          | tail _ hmt => exact hmt
        exact recon_of_fiberConstant report answer t (fiberConstantOn_tail hc) h hmt

/-- Converse: if first-match returns every listed answer, the answer is constant on the listed fibers. -/
theorem fiberConstantOn_of_recon [DecidableEq V] (hs : List H) (report : H → V) (answer : H → S)
    (hr : ∀ h ∈ hs, recon report answer (report h) hs = some (answer h)) :
    FiberConstantOn hs report answer := by
  intro h hm h' hm' e
  have e1 := hr h hm
  have e2 := hr h' hm'
  rw [← e] at e2
  rw [e1] at e2
  exact Option.some.inj e2

/-- The listed criterion: a genuine equivalence, choice-free. -/
theorem listed_history_report_criterion [DecidableEq V] (hs : List H) (report : H → V) (answer : H → S) :
    (∀ h ∈ hs, recon report answer (report h) hs = some (answer h)) ↔
      FiberConstantOn hs report answer :=
  ⟨fiberConstantOn_of_recon hs report answer, fun hc => recon_of_fiberConstant report answer hs hc⟩

/-- Refusal off the listed image: `recon` is `none` exactly when no listed history reports `x`. -/
theorem recon_eq_none_iff [DecidableEq V] (report : H → V) (answer : H → S) (x : V) :
    ∀ hs : List H, recon report answer x hs = none ↔ ∀ h ∈ hs, report h ≠ x
  | [] => ⟨(fun _ _ hm => nomatch hm), (fun _ => rfl)⟩
  | a :: t => by
      by_cases e : report a = x
      · rw [recon_cons_of_eq t e]
        constructor
        · intro h; cases h
        · intro h; exact absurd e (h a (List.mem_cons_self))
      · rw [recon_cons_of_ne t e]
        constructor
        · intro h b hb
          cases hb with
          | head => exact e
          | tail _ hb => exact (recon_eq_none_iff report answer x t).mp h b hb
        · intro h
          exact (recon_eq_none_iff report answer x t).mpr (fun b hb => h b (List.mem_cons_of_mem a hb))

/-- Uniqueness on the listed reports: any `f` returning every listed answer agrees with `recon` there. -/
theorem recon_unique [DecidableEq V] (report : H → V) (answer : H → S) (f : V → Option S) :
    ∀ hs : List H, (∀ h ∈ hs, f (report h) = some (answer h)) →
      ∀ h ∈ hs, recon report answer (report h) hs = f (report h)
  | [], _, _, hm => nomatch hm
  | a :: t, hf, h, hm => by
      by_cases e : report a = report h
      · rw [recon_cons_of_eq t e, ← e]
        exact (hf a (List.mem_cons_self)).symm
      · rw [recon_cons_of_ne t e]
        have hmt : h ∈ t := by
          cases hm with
          | head => exact absurd rfl e
          | tail _ hmt => exact hmt
        exact recon_unique report answer f t (fun b hb => hf b (List.mem_cons_of_mem a hb)) h hmt

/-- Failure off the listed histories: a listed fiber-constant answer can disagree with an UNLISTED history
of the same report, and `recon` then returns the listed answer, not the unlisted one. -/
theorem recon_wrong_off_list [DecidableEq V] {hs : List H} {report : H → V} {answer : H → S}
    (hc : FiberConstantOn hs report answer) {h0 h : H} (h0m : h0 ∈ hs) (same : report h = report h0)
    (different : answer h ≠ answer h0) : recon report answer (report h) hs ≠ some (answer h) := by
  intro heq
  have := recon_of_fiberConstant report answer hs hc h0 h0m
  rw [← same, heq] at this
  exact different (Option.some.inj this)

/-- Bridge to the image-factorization of node 163, without choice: a complete listing plus global fiber
constancy gives the factor through the report image. -/
theorem listed_factor_exists [DecidableEq V] (hs : List H) (report : H → V) (answer : H → S)
    (complete : ∀ h, h ∈ hs) (hc : ∀ h h', report h = report h' → answer h = answer h') :
    ∃ g : {x : V // ∃ h, report h = x} → S, ∀ h, g ⟨report h, ⟨h, rfl⟩⟩ = answer h := by
  have hcl : FiberConstantOn hs report answer := fun h _ h' _ e => hc h h' e
  have hsome : ∀ x : {x : V // ∃ h, report h = x}, (recon report answer x.1 hs).isSome = true := by
    intro x
    obtain ⟨h, hh⟩ := x.2
    rw [← hh, recon_of_fiberConstant report answer hs hcl h (complete h)]
    rfl
  refine ⟨fun x => (recon report answer x.1 hs).get (hsome x), ?_⟩
  intro h
  have e := recon_of_fiberConstant report answer hs hcl h (complete h)
  apply Option.some.inj
  rw [Option.some_get]
  exact e

/-- Classical variant for a report type with NO decidable equality: the instance is manufactured by
`Classical.propDecidable`, and the choice axiom enters exactly there (see the axiom report). -/
noncomputable def reconC (report : H → V) (answer : H → S) (x : V) (hs : List H) : Option S :=
  @recon H V S (fun a b => Classical.propDecidable (a = b)) report answer x hs

theorem listed_history_report_criterion_classical (hs : List H) (report : H → V) (answer : H → S) :
    (∀ h ∈ hs, reconC report answer (report h) hs = some (answer h)) ↔ FiberConstantOn hs report answer :=
  @listed_history_report_criterion H V S (fun a b => Classical.propDecidable (a = b)) hs report answer

/-! ## Instances (labelled as instances, not general statements) -/

/-- Three histories `0,1,2`, report `h % 2`, answer `h % 2`: fiber constant and reconstructed. -/
theorem instance_reconstructs :
    recon (fun h : Nat => h % 2) (fun h : Nat => h % 2) 0 [0, 1, 2] = some 0 ∧
    recon (fun h : Nat => h % 2) (fun h : Nat => h % 2) 1 [0, 1, 2] = some 1 ∧
    recon (fun h : Nat => h % 2) (fun h : Nat => h % 2) 2 [0, 1, 2] = none := by
  decide

/-- Same listing, answer `h` itself: NOT fiber constant on the listing (0 and 2 share report 0). -/
theorem instance_not_fiberConstant :
    ¬ FiberConstantOn [0, 1, 2] (fun h : Nat => h % 2) (fun h : Nat => h) := by
  intro hc
  exact absurd (hc 0 (by simp) 2 (by simp) (by decide)) (by decide)

/-- Listing `[0]` only: fiber constant, but the unlisted history `2` (same report `0`) is answered wrongly. -/
theorem instance_wrong_off_list :
    FiberConstantOn [0] (fun h : Nat => h % 2) (fun h : Nat => h) ∧
    recon (fun h : Nat => h % 2) (fun h : Nat => h) ((2 : Nat) % 2) [0] ≠ some 2 := by
  refine ⟨?_, by decide⟩
  intro h hm h' hm' _
  simp at hm hm'
  rw [hm, hm']

end PregenConstructive

#print axioms PregenConstructive.recon_of_fiberConstant
#print axioms PregenConstructive.fiberConstantOn_of_recon
#print axioms PregenConstructive.listed_history_report_criterion
#print axioms PregenConstructive.recon_eq_none_iff
#print axioms PregenConstructive.recon_unique
#print axioms PregenConstructive.recon_wrong_off_list
#print axioms PregenConstructive.listed_factor_exists
#print axioms PregenConstructive.listed_history_report_criterion_classical
#print axioms PregenConstructive.instance_reconstructs
#print axioms PregenConstructive.instance_not_fiberConstant
#print axioms PregenConstructive.instance_wrong_off_list
