/- Imported so that this repository carries its own Lean evidence.
   Original sha256: eb8e353420d8a745725b8fa22fbdccb6f27e78f8fbb1efba02f08f7932f3f62a (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.LegacyTopLevel.GrammarDepthCeiling
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
/-!
PaperER007's narrow fixed-alphabet nesting lemma.

This file models only unary terms built from an already declared symbol type and
an already declared operator type.  It proves that repeatedly applying one
declared unary operator cannot introduce an undeclared symbol or operator.  It
does not formalize the monograph's full grammar ceiling, parser, typed operad,
or denotational semantics.
-/

namespace LggrFiniteConsequences

universe u v

inductive FixedAlphabetTerm (Symbol : Type u) (Operator : Type v) where
  | atom : Symbol → FixedAlphabetTerm Symbol Operator
  | unary : Operator → FixedAlphabetTerm Symbol Operator →
      FixedAlphabetTerm Symbol Operator

namespace FixedAlphabetTerm

variable {Symbol : Type u} {Operator : Type v}

def symbolsDeclared
    (allowedSymbol : Symbol → Prop) :
    FixedAlphabetTerm Symbol Operator → Prop
  | .atom symbol => allowedSymbol symbol
  | .unary _ body => symbolsDeclared allowedSymbol body

def operatorsDeclared
    (allowedOperator : Operator → Prop) :
    FixedAlphabetTerm Symbol Operator → Prop
  | .atom _ => True
  | .unary op body => allowedOperator op ∧ operatorsDeclared allowedOperator body

def declarationsPreserved
    (allowedSymbol : Symbol → Prop) (allowedOperator : Operator → Prop)
    (term : FixedAlphabetTerm Symbol Operator) : Prop :=
  symbolsDeclared allowedSymbol term ∧ operatorsDeclared allowedOperator term

def nest
    (op : Operator) : Nat → FixedAlphabetTerm Symbol Operator →
      FixedAlphabetTerm Symbol Operator
  | 0, term => term
  | depth + 1, term => .unary op (nest op depth term)

theorem fixed_alphabet_nesting_introduces_no_undeclared_symbols
    (allowedSymbol : Symbol → Prop) (op : Operator) (depth : Nat)
    (term : FixedAlphabetTerm Symbol Operator)
    (hTerm : symbolsDeclared allowedSymbol term) :
    symbolsDeclared allowedSymbol (nest op depth term) := by
  induction depth with
  | zero => exact hTerm
  | succ depth ih => exact ih

theorem fixed_alphabet_nesting_introduces_no_undeclared_operators
    (allowedOperator : Operator → Prop) (op : Operator) (depth : Nat)
    (term : FixedAlphabetTerm Symbol Operator)
    (hOp : allowedOperator op)
    (hTerm : operatorsDeclared allowedOperator term) :
    operatorsDeclared allowedOperator (nest op depth term) := by
  induction depth with
  | zero => exact hTerm
  | succ depth ih => exact ⟨hOp, ih⟩

/--
Internal fixed-alphabet closure for unary nesting.  The conclusion is only
about the two supplied declaration predicates; it is not the full LggrFiniteConsequences
grammar-ceiling claim.
-/
theorem fixed_alphabet_nesting_preserves_declarations
    (allowedSymbol : Symbol → Prop) (allowedOperator : Operator → Prop)
    (op : Operator) (depth : Nat) (term : FixedAlphabetTerm Symbol Operator)
    (hOp : allowedOperator op)
    (hTerm : declarationsPreserved allowedSymbol allowedOperator term) :
    declarationsPreserved allowedSymbol allowedOperator (nest op depth term) := by
  exact ⟨
    fixed_alphabet_nesting_introduces_no_undeclared_symbols
      allowedSymbol op depth term hTerm.1,
    fixed_alphabet_nesting_introduces_no_undeclared_operators
      allowedOperator op depth term hOp hTerm.2⟩

end FixedAlphabetTerm

#print axioms LggrFiniteConsequences.FixedAlphabetTerm.fixed_alphabet_nesting_introduces_no_undeclared_symbols
#print axioms LggrFiniteConsequences.FixedAlphabetTerm.fixed_alphabet_nesting_introduces_no_undeclared_operators
#print axioms LggrFiniteConsequences.FixedAlphabetTerm.fixed_alphabet_nesting_preserves_declarations

end LggrFiniteConsequences
