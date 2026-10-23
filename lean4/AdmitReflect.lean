import AdmitCore

/-!
# Admit reflection

AuthorityEffect: None.

Quotation of the core syntax (expressions, events, judgments, regimes).
Soundness here is a round trip of that syntax and transport of `AdmitCore.Step`.
There is no truth predicate and no biconditional for judgments.
-/

namespace AdmitReflect

inductive QExpr where
  | qToken : Nat → QExpr
  | qDatum : Nat → QExpr
  | qForm : Nat → List Nat → QExpr
  | qCut : Nat → Nat → QExpr

inductive QEvent where
  | qSupply : Nat → QEvent
  | qAdmitData : Nat → QEvent
  | qAdmitForm : Nat → Nat → QEvent
  | qAdmitCut : Nat → Nat → QEvent
  | qImpose : QEvent

inductive QJudg where
  | qTyped : QExpr → AdmitCore.Kind → QJudg
  | qAdmittedData : Nat → QJudg
  | qAdmittedForm : Nat → Nat → QJudg
  | qAdmittedCut : Nat → Nat → QJudg
  | qApart : Nat → Nat → QJudg

structure QRegime where
  data : List Nat
  forms : List (Nat × Nat)
  cuts : List (Nat × Nat)

def quoteExpr : AdmitCore.Expr → QExpr
  | .token n => .qToken n
  | .datum n => .qDatum n
  | .form i idx => .qForm i idx
  | .cut a b => .qCut a b

def unquoteExpr : QExpr → AdmitCore.Expr
  | .qToken n => .token n
  | .qDatum n => .datum n
  | .qForm i idx => .form i idx
  | .qCut a b => .cut a b

theorem unquote_quote_expr (e : AdmitCore.Expr) : unquoteExpr (quoteExpr e) = e := by
  cases e <;> rfl

theorem quote_unquote_expr (q : QExpr) : quoteExpr (unquoteExpr q) = q := by
  cases q <;> rfl

def quoteEvent : AdmitCore.Event → QEvent
  | .supply n => .qSupply n
  | .admitData n => .qAdmitData n
  | .admitForm i k => .qAdmitForm i k
  | .admitCut a b => .qAdmitCut a b
  | .impose => .qImpose

def unquoteEvent : QEvent → AdmitCore.Event
  | .qSupply n => .supply n
  | .qAdmitData n => .admitData n
  | .qAdmitForm i k => .admitForm i k
  | .qAdmitCut a b => .admitCut a b
  | .qImpose => .impose

theorem unquote_quote_event (e : AdmitCore.Event) : unquoteEvent (quoteEvent e) = e := by
  cases e <;> rfl

theorem quote_unquote_event (q : QEvent) : quoteEvent (unquoteEvent q) = q := by
  cases q <;> rfl

def quoteJudg : AdmitCore.Judg → QJudg
  | .typed e k => .qTyped (quoteExpr e) k
  | .admittedData n => .qAdmittedData n
  | .admittedForm i k => .qAdmittedForm i k
  | .admittedCut a b => .qAdmittedCut a b
  | .apart a b => .qApart a b

def unquoteJudg : QJudg → AdmitCore.Judg
  | .qTyped q k => .typed (unquoteExpr q) k
  | .qAdmittedData n => .admittedData n
  | .qAdmittedForm i k => .admittedForm i k
  | .qAdmittedCut a b => .admittedCut a b
  | .qApart a b => .apart a b

theorem unquote_quote_judg (J : AdmitCore.Judg) : unquoteJudg (quoteJudg J) = J := by
  cases J with
  | typed e k =>
    show AdmitCore.Judg.typed (unquoteExpr (quoteExpr e)) k = AdmitCore.Judg.typed e k
    rw [unquote_quote_expr e]
  | admittedData _ => rfl
  | admittedForm _ _ => rfl
  | admittedCut _ _ => rfl
  | apart _ _ => rfl

theorem quote_unquote_judg (q : QJudg) : quoteJudg (unquoteJudg q) = q := by
  cases q with
  | qTyped e k =>
    show QJudg.qTyped (quoteExpr (unquoteExpr e)) k = QJudg.qTyped e k
    rw [quote_unquote_expr e]
  | qAdmittedData _ => rfl
  | qAdmittedForm _ _ => rfl
  | qAdmittedCut _ _ => rfl
  | qApart _ _ => rfl

def quoteRegime (Γ : AdmitCore.Regime) : QRegime where
  data := Γ.data
  forms := Γ.forms
  cuts := Γ.cuts

def unquoteRegime (q : QRegime) : AdmitCore.Regime where
  data := q.data
  forms := q.forms
  cuts := q.cuts

theorem unquote_quote_regime (Γ : AdmitCore.Regime) :
    unquoteRegime (quoteRegime Γ) = Γ := rfl

theorem quote_unquote_regime (q : QRegime) : quoteRegime (unquoteRegime q) = q := rfl

theorem unquoteRegime_inj {q q' : QRegime} (h : unquoteRegime q = unquoteRegime q') : q = q' := by
  rw [← quote_unquote_regime q, ← quote_unquote_regime q', h]

/-- The step relation read on quoted syntax. It is transport, not a truth predicate. -/
abbrev QStep (qΓ : QRegime) (qe : QEvent) (qΓ' : QRegime) : Prop :=
  AdmitCore.Step (unquoteRegime qΓ) (unquoteEvent qe) (unquoteRegime qΓ')

theorem qstep_sound (Γ : AdmitCore.Regime) (e : AdmitCore.Event) (Γ' : AdmitCore.Regime) :
    QStep (quoteRegime Γ) (quoteEvent e) (quoteRegime Γ') ↔ AdmitCore.Step Γ e Γ' := by
  unfold QStep
  rw [unquote_quote_regime Γ, unquote_quote_event e, unquote_quote_regime Γ']

theorem quoted_supply_noop (qΓ : QRegime) (n : Nat) (qΓ' : QRegime)
    (h : QStep qΓ (.qSupply n) qΓ') : qΓ' = qΓ :=
  unquoteRegime_inj (AdmitCore.supply_noop h)

theorem quoted_self_cut_refused (qΓ : QRegime) (n : Nat) (qΓ' : QRegime) :
    ¬ QStep qΓ (.qAdmitCut n n) qΓ' := by
  intro h
  exact AdmitCore.self_cut_refused h

theorem quoted_impose_no_step (qΓ qΓ' : QRegime) : ¬ QStep qΓ .qImpose qΓ' := by
  intro h
  exact AdmitCore.impose_no_step _ _ h

/-- Unquoting a quoted token does not type it as data. -/
theorem quoted_token_not_data (Γ : AdmitCore.Regime) (n : Nat) :
    ¬ AdmitCore.Typed Γ (unquoteExpr (.qToken n)) .dataK := by
  intro h
  cases h

end AdmitReflect

#print axioms AdmitReflect.unquote_quote_expr
#print axioms AdmitReflect.quote_unquote_expr
#print axioms AdmitReflect.unquote_quote_event
#print axioms AdmitReflect.quote_unquote_event
#print axioms AdmitReflect.unquote_quote_judg
#print axioms AdmitReflect.quote_unquote_judg
#print axioms AdmitReflect.unquote_quote_regime
#print axioms AdmitReflect.quote_unquote_regime
#print axioms AdmitReflect.unquoteRegime_inj
#print axioms AdmitReflect.qstep_sound
#print axioms AdmitReflect.quoted_supply_noop
#print axioms AdmitReflect.quoted_self_cut_refused
#print axioms AdmitReflect.quoted_impose_no_step
#print axioms AdmitReflect.quoted_token_not_data
