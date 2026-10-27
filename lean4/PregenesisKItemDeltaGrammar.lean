/-
Narrow case for PGW-K-ITEM-DELTA-GRAMMAR.
One empty base: two data, no forms, no instances, no rules.
Each admitted form has arity one. The census is the well-formed
sequences of one or two items over a ten-atom universe, plus two
named three-item histories. AuthorityEffect: None.
-/

namespace PregenesisKItemDeltaGrammar

inductive Arg where
  | t0
  | t1
  | fresh
deriving DecidableEq, Repr

inductive Atom where
  | datum
  | form1
  | rule0
  | rule1
  | i0t0
  | i0t1
  | i0fr
  | i1t0
  | i1t1
  | i1fr
deriving DecidableEq, Repr

structure Inst where
  form : Nat
  arg : Arg
deriving DecidableEq, Repr

structure State where
  dataCount : Nat
  forms : Nat
  insts : List Inst
  rules : List Nat
deriving DecidableEq, Repr

def base : State :=
  { dataCount := 2, forms := 0, insts := [], rules := [] }

def step (s : State) : Atom → Option State
  | .datum => some { s with dataCount := s.dataCount + 1 }
  | .form1 => some { s with forms := s.forms + 1 }
  | .rule0 =>
      if 0 < s.forms then some { s with rules := s.rules ++ [0] } else none
  | .rule1 =>
      if 1 < s.forms then some { s with rules := s.rules ++ [1] } else none
  | .i0t0 =>
      if 0 < s.forms then
        if 0 < s.dataCount then
          some { s with insts := s.insts ++ [⟨0, .t0⟩] }
        else none
      else none
  | .i0t1 =>
      if 0 < s.forms then
        if 1 < s.dataCount then
          some { s with insts := s.insts ++ [⟨0, .t1⟩] }
        else none
      else none
  | .i0fr =>
      if 0 < s.forms then
        if 2 < s.dataCount then
          some { s with insts := s.insts ++ [⟨0, .fresh⟩] }
        else none
      else none
  | .i1t0 =>
      if 1 < s.forms then
        if 0 < s.dataCount then
          some { s with insts := s.insts ++ [⟨1, .t0⟩] }
        else none
      else none
  | .i1t1 =>
      if 1 < s.forms then
        if 1 < s.dataCount then
          some { s with insts := s.insts ++ [⟨1, .t1⟩] }
        else none
      else none
  | .i1fr =>
      if 1 < s.forms then
        if 2 < s.dataCount then
          some { s with insts := s.insts ++ [⟨1, .fresh⟩] }
        else none
      else none

/-- Hole-plug bit of one argument on one form. A missing form contributes false. -/
def profileAt (s : State) (form : Nat) (a : Arg) : Bool :=
  if form < s.forms then
    s.rules.contains form || s.insts.contains ⟨form, a⟩
  else
    false

/-- Unequal target bits on form 0, or on form 1 when that form exists. -/
def separates (s : State) : Bool :=
  ((profileAt s 0 .t0) != (profileAt s 0 .t1)) ||
    ((decide (1 < s.forms)) && ((profileAt s 1 .t0) != (profileAt s 1 .t1)))

def separatesOf : Option State → Bool
  | none => false
  | some s => separates s

def run2 (a b : Atom) : Option State :=
  match step base a with
  | none => none
  | some s => step s b

def run3 (a b c : Atom) : Option State :=
  match run2 a b with
  | none => none
  | some s => step s c

def atoms : List Atom :=
  [ .datum, .form1, .rule0, .rule1
  , .i0t0, .i0t1, .i0fr
  , .i1t0, .i1t1, .i1fr ]

def pairs : List (Atom × Atom) :=
  atoms.flatMap (fun a => atoms.map (fun b => (a, b)))

def wellFormedSingles : List Atom :=
  atoms.filter (fun a => (step base a).isSome)

def wellFormedPairs : List (Atom × Atom) :=
  pairs.filter (fun p => (run2 p.1 p.2).isSome)

def separatingSingles : List Atom :=
  atoms.filter (fun a => separatesOf (step base a))

def separatingPairs : List (Atom × Atom) :=
  pairs.filter (fun p => separatesOf (run2 p.1 p.2))

def ruleBits : Bool × Bool × Bool :=
  match run2 .form1 .rule0 with
  | some s => (profileAt s 0 .t0, profileAt s 0 .t1, separates s)
  | none => (false, false, true)

def extBits : Bool × Bool × Bool × Bool × Bool × Bool :=
  match run2 .form1 .i0t0, run3 .form1 .i0t0 .rule0 with
  | some s, some t =>
      ( profileAt s 0 .t0, profileAt s 0 .t1, separates s
      , profileAt t 0 .t0, profileAt t 0 .t1, separates t)
  | _, _ => (false, false, false, false, false, false)

def offBits : Bool × Bool × Bool × Bool :=
  match run3 .datum .form1 .i0fr with
  | some s =>
      ( s.insts.contains ⟨0, .fresh⟩
      , profileAt s 0 .t0
      , profileAt s 0 .t1
      , separates s)
  | none => (false, true, true, true)

theorem well_formed_singles_are :
    wellFormedSingles = [.datum, .form1] := by
  decide

theorem well_formed_pairs_are :
    wellFormedPairs = [
      (.datum, .datum),
      (.datum, .form1),
      (.form1, .datum),
      (.form1, .form1),
      (.form1, .rule0),
      (.form1, .i0t0),
      (.form1, .i0t1)
    ] := by
  decide

theorem no_single_item_separates : separatingSingles = [] := by
  decide

theorem separating_pairs_are_two :
    separatingPairs = [(.form1, .i0t0), (.form1, .i0t1)] := by
  decide

theorem ten_atoms : atoms.length = 10 := by
  decide

theorem one_hundred_pairs : pairs.length = 100 := by
  decide

theorem nine_well_formed :
    wellFormedSingles.length + wellFormedPairs.length = 9 := by
  decide

theorem seven_leave_bits_equal :
    (wellFormedSingles.length + wellFormedPairs.length) - separatingPairs.length = 7 := by
  decide

theorem fresh_datum_pairs_do_not_separate :
    separatesOf (run2 .datum .datum) = false ∧
    separatesOf (run2 .datum .form1) = false ∧
    separatesOf (run2 .form1 .datum) = false := by
  decide

theorem form_rule_both_true : ruleBits = (true, true, false) := by
  decide

theorem rule_extension_equalizes :
    extBits = (true, false, true, true, true, false) := by
  decide

theorem rule_extension_is_longer :
    [Atom.form1, Atom.i0t0].length = 2 ∧
    [Atom.form1, Atom.i0t0, Atom.rule0].length = 3 := by
  decide

theorem off_target_instance_keeps_bits :
    offBits = (true, false, false, false) := by
  decide

#print axioms well_formed_singles_are
#print axioms well_formed_pairs_are
#print axioms no_single_item_separates
#print axioms separating_pairs_are_two
#print axioms ten_atoms
#print axioms one_hundred_pairs
#print axioms nine_well_formed
#print axioms seven_leave_bits_equal
#print axioms fresh_datum_pairs_do_not_separate
#print axioms form_rule_both_true
#print axioms rule_extension_equalizes
#print axioms rule_extension_is_longer
#print axioms off_target_instance_keeps_bits

end PregenesisKItemDeltaGrammar
