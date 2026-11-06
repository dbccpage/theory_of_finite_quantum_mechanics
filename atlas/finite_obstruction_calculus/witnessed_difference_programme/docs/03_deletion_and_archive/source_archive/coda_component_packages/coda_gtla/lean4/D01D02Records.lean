/-!
# CODA-GTLA D01/D02: Records for CODA-GTLA: Layered Authority and the Master Normal Form

Formalizes:
1. Finite Carrier Presentation (V, delta) in CODA_pres.
2. Comparison Spans, diagonal identity spans, and pullback composition.
3. Intensional execution traces in CODA_trace, identity traces, and trace composition.
4. Erasure quotient functor q: CODA_trace -> CODA_pres.
5. Disjoint terminal outcome trichotomy: T_auth \sqcup T_res \sqcup F_term.

AuthorityEffect: None.
-/

namespace CodaGtla

set_option linter.unusedVariables false

/-- Definition 1.1: A finite carrier presentation (V, delta). -/
structure Presentation where
  carrier : Type
  [decEq : DecidableEq carrier]
  diff : carrier → carrier → Nat
  diff_self : ∀ x, diff x x = 0

attribute [instance] Presentation.decEq

/-- Definition 1.2: Concrete comparison span between presentations P1 and P2. -/
structure ComparisonSpan (P1 P2 : Presentation) where
  midCarrier : Type
  [decEqMid : DecidableEq midCarrier]
  leftMap : midCarrier → P1.carrier
  rightMap : midCarrier → P2.carrier
  spanCost : Nat

attribute [instance] ComparisonSpan.decEqMid

/-- Diagonal comparison span on any presentation (Identity morphism in CODA_pres). -/
def diagSpan (P : Presentation) : ComparisonSpan P P where
  midCarrier := P.carrier
  leftMap := id
  rightMap := id
  spanCost := 0

/-- Definition 1.3: Relational pullback composition of comparison spans. -/
def compSpan {P1 P2 P3 : Presentation} (S1 : ComparisonSpan P1 P2) (S2 : ComparisonSpan P2 P3) :
    ComparisonSpan P1 P3 where
  midCarrier := { p : S1.midCarrier × S2.midCarrier // S1.rightMap p.1 = S2.leftMap p.2 }
  leftMap p := S1.leftMap p.val.1
  rightMap p := S2.rightMap p.val.2
  spanCost := S1.spanCost + S2.spanCost

/-- Definition: Intensional execution trace in CODA_trace. -/
structure Trace (P1 P2 : Presentation) where
  steps : Nat
  workCost : Nat
  underlyingSpan : ComparisonSpan P1 P2

/-- Identity trace with zero steps and zero work. -/
def idTrace (P : Presentation) : Trace P P where
  steps := 0
  workCost := 0
  underlyingSpan := diagSpan P

/-- Composition of execution traces in CODA_trace. -/
def compTrace {P1 P2 P3 : Presentation} (T1 : Trace P1 P2) (T2 : Trace P2 P3) : Trace P1 P3 where
  steps := T1.steps + T2.steps
  workCost := T1.workCost + T2.workCost
  underlyingSpan := compSpan T1.underlyingSpan T2.underlyingSpan

/-- Erasure quotient functor q: CODA_trace -> CODA_pres. -/
def eraseTrace {P1 P2 : Presentation} (T : Trace P1 P2) : ComparisonSpan P1 P2 :=
  T.underlyingSpan

/-- Extensional morphism cost diagnostic. -/
def extCost {P1 P2 : Presentation} (S : ComparisonSpan P1 P2) : Nat :=
  S.spanCost

/-- Intensional work cost diagnostic. -/
def traceCost {P1 P2 : Presentation} (T : Trace P1 P2) : Nat :=
  T.workCost

/-- Disjoint terminal outcome type for the Master Normal Form.
    Strict coproduct: T_auth \sqcup T_res \sqcup F_term. -/
inductive TerminalOutcome where
  | authorized (payloadId : String)
  | closedResidual (anomalonId : String) (phi1Distance : Nat)
  | refused (reason : String)
  deriving Repr, DecidableEq

/-- Authority predicate: terminal is in T_auth. -/
def IsAuth : TerminalOutcome → Prop
  | .authorized _ => True
  | _ => False

/-- Anomalon predicate: terminal is in T_res (ClosedResidual). -/
def IsAnomalon : TerminalOutcome → Prop
  | .closedResidual _ _ => True
  | _ => False

/-- Refusal predicate: terminal is in F_term. -/
def IsRefused : TerminalOutcome → Prop
  | .refused _ => True
  | _ => False

end CodaGtla
