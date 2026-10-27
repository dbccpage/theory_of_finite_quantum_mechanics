/- Imported so that this repository carries its own Lean evidence.
   Original sha256: cdc8d4cea4febffc6c3cb9be455c0b51c476383dc537577199021328d5ef0682 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.GenesisPrimitives.SupplyErasure
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
/-!
# Supply erasure at the replay level (Lean 4, core only)

Replay-level form of Genesis `supply_no_op`: deleting every `supply`
event from a history leaves the replayed regime unchanged, so two
histories with the same non-supply subsequence replay to the same regime.

Source definitions are copied byte for byte from
`dbccpage/19L57G1`, commit `f1d56c010e6ba10a3b9418bd7cc5953c067250f2`
(tag `sealed-derivation-v1`), file `lean4/Derivation/Basic.lean`:
`Inst` line 21, `insertNew` lines 25 to 26, `Regime` lines 53 to 59,
`Event` lines 134 to 141, `stepE` lines 145 to 162, `replayE` lines
166 to 167.  The copy sits between the `BEGIN COPY` and `END COPY`
markers; nothing inside the markers is edited here.  `supply_no_op`
(Inertia.lean line 17) is re-proved, not imported.

Classification: metatheoretic apparatus over the object-language core.
AuthorityEffect: None.  No `sorry`, `admit`, `axiom`, `native_decide`,
no `Classical.choice`, `propext` or `Quot.sound` (see `#print axioms`).
-/

namespace GenesisCopy

-- BEGIN COPY (19L57G1 f1d56c01, lean4/Derivation/Basic.lean)
abbrev Inst := Nat × List Nat

def insertNew {α : Type} [DecidableEq α] (l : List α) (a : α) : List α :=
  if a ∈ l then l else l ++ [a]

structure Regime where
  data  : Nat
  forms : List Nat
  insts : List Inst
  rules : List Nat
  reqs  : List (Nat × Nat)
deriving Repr, DecidableEq

inductive Event where
  | supply       (token : Nat)
  | admitDatum
  | admitForm    (arity : Nat)
  | admitInst    (form : Nat) (args : List Nat)
  | admitRuleAll (form : Nat)
  | impose       (i j : Nat)
deriving Repr, DecidableEq

def stepE (r : Regime) : Event → Option Regime
  | .supply _ => some r
  | .admitDatum => some { r with data := r.data + 1 }
  | .admitForm a =>
      if 1 ≤ a then some { r with forms := r.forms ++ [a] } else none
  | .admitInst f args =>
      if f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
          (∀ x ∈ args, x < r.data) then
        some { r with insts := insertNew r.insts (f, args) }
      else none
  | .admitRuleAll f =>
      if f < r.forms.length then
        some { r with rules := insertNew r.rules f }
      else none
  | .impose i j =>
      if i < j ∧ j < r.data then
        some { r with reqs := insertNew r.reqs (i, j) }
      else none


def replayE (h : List Event) (base : Regime) : Option Regime :=
  h.foldlM stepE base

-- END COPY

end GenesisCopy

namespace GenesisPrimitives.SupplyErasure

open GenesisCopy

/-- True exactly on `supply` events. -/
def isSupply : Event → Bool
  | .supply _ => true
  | _ => false

/-- The predicate that keeps the non-supply events of a history. -/
def notSupply (e : Event) : Bool := !isSupply e

/-- A bare supply changes no admitted state (Inertia.lean line 17,
re-proved by `rfl`). -/
theorem supply_no_op (r : Regime) (t : Nat) :
    stepE r (.supply t) = some r := rfl

/-- Replay of a cons: step once, then replay the tail. -/
theorem replayE_cons (e : Event) (h : List Event) (base : Regime) :
    replayE (e :: h) base = (stepE base e).bind (fun r => replayE h r) := rfl

/-- Replay of the empty history is the base. -/
theorem replayE_nil (base : Regime) : replayE [] base = some base := rfl

/-- Corollary 1.  A leading supply is erasable. -/
theorem replayE_cons_supply (t : Nat) (h : List Event) (base : Regime) :
    replayE (.supply t :: h) base = replayE h base := rfl

/-- One cons step of the main induction for a non-supply head: the
filter keeps the head, and the two replays step identically. -/
theorem replayE_filter_cons_keep (e : Event) (rest : List Event) (base : Regime)
    (hkeep : (e :: rest).filter notSupply = e :: rest.filter notSupply)
    (ih : ∀ b, replayE (rest.filter notSupply) b = replayE rest b) :
    replayE ((e :: rest).filter notSupply) base = replayE (e :: rest) base := by
  rw [hkeep, replayE_cons, replayE_cons]
  cases stepE base e with
  | none => rfl
  | some r => exact ih r

/-- **Main theorem.**  Deleting every supply event from a history leaves
the replayed regime unchanged. -/
theorem replayE_filter_supply (h : List Event) (base : Regime) :
    replayE (h.filter notSupply) base = replayE h base := by
  induction h generalizing base with
  | nil => rfl
  | cons e rest ih =>
    cases e
    case supply t =>
      show replayE (rest.filter notSupply) base = replayE (.supply t :: rest) base
      rw [replayE_cons_supply]
      exact ih base
    all_goals exact replayE_filter_cons_keep _ _ _ rfl ih

/-- The same statement with the filter predicate written out. -/
theorem replayE_filter_not_isSupply (h : List Event) (base : Regime) :
    replayE (h.filter (fun e => !isSupply e)) base = replayE h base :=
  replayE_filter_supply h base

/-- Corollary 2.  A history of supplies alone replays to the base. -/
theorem replayE_supply_only (ts : List Nat) (base : Regime) :
    replayE (ts.map Event.supply) base = some base := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
    show replayE (.supply t :: ts.map Event.supply) base = some base
    rw [replayE_cons_supply]
    exact ih

/-- Corollary 3 (supply-interleaving invariance).  Two histories with the
same non-supply subsequence replay to the same regime: presentations may
be inserted or deleted anywhere without changing what is admitted. -/
theorem replayE_eq_of_filter_eq (h₁ h₂ : List Event) (base : Regime)
    (heq : h₁.filter notSupply = h₂.filter notSupply) :
    replayE h₁ base = replayE h₂ base := by
  rw [← replayE_filter_supply h₁ base, ← replayE_filter_supply h₂ base, heq]

/-! ## Step-level idempotence of the deduplicating admissions

`admitInst`, `admitRuleAll` and `impose` go through `insertNew`, so a
second admission of the same event on the resulting regime returns that
regime.  `admitDatum` and `admitForm` append and are not idempotent; the
two witnesses close the section. -/

/-- The appended element is a member of `l ++ [a]`. -/
theorem mem_append_singleton {α : Type} (l : List α) (a : α) : a ∈ l ++ [a] := by
  induction l with
  | nil => exact List.Mem.head _
  | cons x xs ih => exact List.Mem.tail x ih

/-- The inserted element is a member of the insertion. -/
theorem mem_insertNew_self {α : Type} [DecidableEq α] (l : List α) (a : α) :
    a ∈ insertNew l a := by
  unfold insertNew
  split
  next h => exact h
  next _ => exact mem_append_singleton l a

/-- Inserting the same element twice is inserting it once. -/
theorem insertNew_insertNew {α : Type} [DecidableEq α] (l : List α) (a : α) :
    insertNew (insertNew l a) a = insertNew l a := by
  have hdef : insertNew (insertNew l a) a =
      if a ∈ insertNew l a then insertNew l a else insertNew l a ++ [a] := rfl
  rw [hdef]
  split
  next => rfl
  next h => exact absurd (mem_insertNew_self l a) h

theorem stepE_admitInst_idem (r r' : Regime) (f : Nat) (args : List Nat)
    (hs : stepE r (.admitInst f args) = some r') :
    stepE r' (.admitInst f args) = some r' := by
  dsimp only [stepE] at hs ⊢
  split at hs
  next hguard =>
    cases hs
    split
    next => rw [insertNew_insertNew]
    next hneg => exact absurd hguard hneg
  next => cases hs

theorem stepE_admitRuleAll_idem (r r' : Regime) (f : Nat)
    (hs : stepE r (.admitRuleAll f) = some r') :
    stepE r' (.admitRuleAll f) = some r' := by
  dsimp only [stepE] at hs ⊢
  split at hs
  next hguard =>
    cases hs
    split
    next => rw [insertNew_insertNew]
    next hneg => exact absurd hguard hneg
  next => cases hs

theorem stepE_impose_idem (r r' : Regime) (i j : Nat)
    (hs : stepE r (.impose i j) = some r') :
    stepE r' (.impose i j) = some r' := by
  dsimp only [stepE] at hs ⊢
  split at hs
  next hguard =>
    cases hs
    split
    next => rw [insertNew_insertNew]
    next hneg => exact absurd hguard hneg
  next => cases hs

/-- `admitDatum` is not idempotent: a second admission adds a second datum. -/
theorem stepE_admitDatum_not_idem :
    ¬ (∀ r r' : Regime, stepE r .admitDatum = some r' →
        stepE r' .admitDatum = some r') := by
  intro hall
  have h := hall ⟨0, [], [], [], []⟩ ⟨1, [], [], [], []⟩ rfl
  exact absurd h (by decide)

/-- `admitForm` is not idempotent: a second admission appends the arity again. -/
theorem stepE_admitForm_not_idem :
    ¬ (∀ r r' : Regime, stepE r (.admitForm 1) = some r' →
        stepE r' (.admitForm 1) = some r') := by
  intro hall
  have h := hall ⟨0, [], [], [], []⟩ ⟨0, [1], [], [], []⟩ rfl
  exact absurd h (by decide)

end GenesisPrimitives.SupplyErasure

#print axioms GenesisPrimitives.SupplyErasure.supply_no_op
#print axioms GenesisPrimitives.SupplyErasure.replayE_cons
#print axioms GenesisPrimitives.SupplyErasure.replayE_nil
#print axioms GenesisPrimitives.SupplyErasure.replayE_cons_supply
#print axioms GenesisPrimitives.SupplyErasure.replayE_filter_cons_keep
#print axioms GenesisPrimitives.SupplyErasure.replayE_filter_supply
#print axioms GenesisPrimitives.SupplyErasure.replayE_filter_not_isSupply
#print axioms GenesisPrimitives.SupplyErasure.replayE_supply_only
#print axioms GenesisPrimitives.SupplyErasure.replayE_eq_of_filter_eq
#print axioms GenesisPrimitives.SupplyErasure.mem_append_singleton
#print axioms GenesisPrimitives.SupplyErasure.mem_insertNew_self
#print axioms GenesisPrimitives.SupplyErasure.insertNew_insertNew
#print axioms GenesisPrimitives.SupplyErasure.stepE_admitInst_idem
#print axioms GenesisPrimitives.SupplyErasure.stepE_admitRuleAll_idem
#print axioms GenesisPrimitives.SupplyErasure.stepE_impose_idem
#print axioms GenesisPrimitives.SupplyErasure.stepE_admitDatum_not_idem
#print axioms GenesisPrimitives.SupplyErasure.stepE_admitForm_not_idem

/-! The copied definitions themselves carry `propext` through core Lean's
decidable list membership (used by `insertNew`) and `List.getD` (used by
`stepE`); every theorem above inherits exactly that set from its statement
and adds nothing.  Genesis records the same set for its own `supply_no_op`
(19L57G1 `artifacts/lean_axioms.txt` line 1). -/
#print axioms GenesisCopy.insertNew
#print axioms GenesisCopy.stepE
#print axioms GenesisCopy.replayE
#print axioms List.instDecidableMemOfLawfulBEq
#print axioms List.getD
