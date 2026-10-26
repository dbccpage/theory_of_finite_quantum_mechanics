/-!
# Genesis Seed, Admission Events, Regimes, and Candidate Items (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/Basic.lean
- lean4/Derivation/Constitution.lean

Classification: Object-language core and metatheoretic apparatus.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.SeedAndRegime

/-- Presentation Token. Inscriptions visible to metatheory. -/
abbrev Token := String

/-- Argument indices referring to admitted data. -/
abbrev Args := List Nat

/-- Judgment instance: form index and argument indices. -/
abbrev Inst := Nat × Args

/-- Separation requirement on data indices (i, j) with i < j. -/
abbrev ReqPair := Nat × Nat

/-- Admitted state (Regime).
    `data`: list of presentation tokens in admission order.
    `forms`: list of arities (each >= 1) for admitted judgment forms.
    `insts`: list of admitted judgment instances (form, args).
    `rules`: list of form indices carrying the uniform all-tuples rule.
    `reqs`: list of externally imposed persistent separation requirements. -/
structure Regime where
  data : List Token
  forms : List Nat
  insts : List Inst
  rules : List Nat
  reqs : List ReqPair
deriving Repr, DecidableEq

/-- The empty base regime (genesis void). -/
def emptyRegime : Regime :=
  { data := [], forms := [], insts := [], rules := [], reqs := [] }

/-- External and internal admission events. -/
inductive Event where
  | supply (tok : Token)
  | admitDatum (tok : Token)
  | admitForm (arity : Nat)
  | admitInst (form : Nat) (args : Args)
  | admitRuleAll (form : Nat)
  | impose (i j : Nat)
deriving Repr, DecidableEq

/-- Candidate response items to separation requirements. -/
inductive Item where
  | newDatum
  | newForm (arity : Nat)
  | newInst (form : Nat) (args : Args)
  | newRuleAll (form : Nat)
deriving Repr, DecidableEq

/-- A candidate delta is a sequence of items. -/
abbrev Delta := List Item

/-- Context structure for internal observation:
    form index, slot index, argument prefix, argument suffix. -/
structure Ctx where
  form : Nat
  slot : Nat
  «prefix» : Args
  suffix : Args
deriving Repr, DecidableEq

/-- Finite search bounds for candidate responses. -/
structure Bounds where
  max_items : Nat := 2
  max_arity : Nat := 2
deriving Repr, DecidableEq

/-- Step transition relation on regimes under an event.
    Deterministic; ill-formed admissions leave the state unchanged. -/
def step (r : Regime) (e : Event) : Regime :=
  match e with
  | Event.supply _ => r
  | Event.admitDatum tok =>
    if tok ∈ r.data then r
    else { r with data := r.data ++ [tok] }
  | Event.admitForm arity =>
    if arity < 1 then r
    else { r with forms := r.forms ++ [arity] }
  | Event.admitInst form args =>
    match r.forms[form]? with
    | some a =>
      if args.length = a ∧ args.all (· < r.data.length) then
        if (form, args) ∈ r.insts then r
        else { r with insts := (form, args) :: r.insts }
      else r
    | none => r
  | Event.admitRuleAll form =>
    if form < r.forms.length then
      if form ∈ r.rules then r
      else { r with rules := form :: r.rules }
    else r
  | Event.impose i j =>
    if i < j ∧ j < r.data.length then
      if (i, j) ∈ r.reqs then r
      else { r with reqs := (i, j) :: r.reqs }
    else r

/-- Replay of a recorded history from a base regime. -/
def replay (history : List Event) (base : Regime := emptyRegime) : Regime :=
  history.foldl step base

end GenesisPrimitives.SeedAndRegime
