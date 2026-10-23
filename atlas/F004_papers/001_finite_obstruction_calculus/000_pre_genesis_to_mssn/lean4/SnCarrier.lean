import SnSyntax

/-!
# S(n) Inductive Carrier Types, Survivor Dynamics & Retraction Maps (Lean 4)

AuthorityEffect: None. GenesisEffect: None.
Formalizes:
1. Declared finite example carriers, not cardinalities inferred from 19L57G1.
2. The epistemic distinction between presentation length and carrier cardinality.
3. Decoupling of active obstruction count (s_n) from cumulative history ledger (|H_n|).
4. Section lifts u_N and retraction down-maps r_N obeying the Old-Image Law.
-/

namespace SnCarrier

open SnPresentation

/-- Declared cardinalities for finite examples; not source-derived stage counts. -/
def carrierCard : Nat → Nat
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 2
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | n => n

/-- An actual finite carrier with the declared cardinality, empty at index zero. -/
abbrev Carrier (n : Nat) := Fin (carrierCard n)

/-- Active obstruction count sequence s_n = (0, 1, 1, 1, 0, 1, 1).
    Notice s_4 = 0 under terminal orbit closure, and s_0 = 0 under ground inertia. -/
def activeObstructions : Nat → Nat
  | 0 => 0
  | 1 => 1
  | 2 => 1
  | 3 => 1
  | 4 => 0
  | 5 => 1
  | 6 => 1
  | _ => 1

/-- Cumulative history ledger count |H_n|.
    Unlike s_n, cumulative history is monotonically non-decreasing. -/
def cumulativeHistory : Nat → Nat
  | 0 => 1  -- {receipt_ground_inertia}
  | 1 => 2  -- + {receipt_lone_mark}
  | 2 => 3  -- + {receipt_retained_pair}
  | 3 => 4  -- + {cert_cost_2_floor}
  | 4 => 5  -- + {cert_orbit_closure}
  | 5 => 6  -- + {receipt_continuation_demand}
  | 6 => 7  -- + {cert_section_retraction}
  | n => n + 1

/-- The flat grammar can lift these base constructors without losing their tags.
    Nested lift/retraction/refusal terms are not members of this source type. -/
inductive BasePresentation where
  | ground (g : GroundToken)
  | supplied (s : SuppliedToken)
  | relation (r : RelationToken)
  deriving Repr, DecidableEq

def BasePresentation.toPresentation : BasePresentation → SnPresentation
  | .ground g => .ground g
  | .supplied s => .supplied s
  | .relation r => .relation r

/-- Section on base presentations, with an explicit source type. -/
def sectionLift (stage : Nat) (p : BasePresentation) : SnPresentation :=
  match p with
  | .ground _ =>
    .lift ⟨stage, .glyphs []⟩
  | .supplied s =>
    .lift ⟨stage, .glyphs [s.mark]⟩
  | .relation (.pair p) =>
    .lift ⟨stage, .glyphs [p.first, p.second]⟩
  | .relation (.cut c) =>
    .lift ⟨stage, .arrow c.src c.tgt⟩
  | .relation (.simplex s) =>
    .lift ⟨stage, .pair s.v0 s.v1⟩

/-- Retraction down-map outcome: either an accepted lower-stage presentation, or typed NON_DESCENT. -/
inductive RetractOutcome where
  | accepted (p : SnPresentation)
  | nonDescent
  deriving Repr, DecidableEq

/-- Retraction down-map r_N: evaluates an input presentation down to stage N. -/
def retractionDownMap (stage : Nat) (p : SnPresentation) : RetractOutcome :=
  match p with
  | .lift l =>
    if l.stage == stage then
      match l.body with
      | .glyphs [] => .accepted (.ground ⟨()⟩)
      | .glyphs [m] => .accepted (.supplied ⟨m⟩)
      | .glyphs [f, s] => .accepted (.relation (.pair ⟨f, s⟩))
      | .arrow src tgt => .accepted (.relation (.cut ⟨src, tgt⟩))
      | .pair v0 v1 => .accepted (.relation (.simplex ⟨v0, v1⟩))
      | _ => .nonDescent
    else
      .nonDescent
  | _ =>
    .nonDescent

end SnCarrier
