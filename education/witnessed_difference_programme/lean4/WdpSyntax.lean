/-!
# Witnessed Difference Programme (WDP) Syntax & Inductive Wire Tokens (Lean 4)

AuthorityEffect: None. GenesisEffect: None.
Constructive Lean 4 formalization of the WDP presentation grammar `wdp.ebnf`.
All types are Mathlib-free, constructive, and admit decidable equality.
-/

namespace WdpPresentation

/-- Primitive character tokens over Sigma36: lowercase ASCII letter or decimal digit. -/
inductive Glyph where
  | latin (c : Char)
  | digit (d : Nat)
  deriving Repr, DecidableEq

/-- Render a Glyph as a single-character string. -/
def Glyph.toString : Glyph → String
  | .latin c => String.singleton c
  | .digit d => s!"{d}"

instance : ToString Glyph := ⟨Glyph.toString⟩

/-- Parse a character into a Glyph over Sigma36. -/
def Glyph.ofChar? (c : Char) : Option Glyph :=
  if 'a' ≤ c ∧ c ≤ 'z' then
    some (.latin c)
  else if '0' ≤ c ∧ c ≤ '9' then
    some (.digit (c.toNat - '0'.toNat))
  else
    none

/-- Non-empty word of glyphs over Sigma36. -/
structure Word where
  head : Glyph
  tail : List Glyph
  deriving Repr, DecidableEq

/-- Render a Word as a string. -/
def Word.toWire (w : Word) : String :=
  w.head.toString ++ String.join (w.tail.map Glyph.toString)

instance : ToString Word := ⟨Word.toWire⟩

/-- Parse a string into a Word over Sigma36. -/
def Word.ofString? (s : String) : Option Word :=
  match s.toList with
  | [] => none
  | c :: cs =>
    match Glyph.ofChar? c with
    | none => none
    | some g =>
      let rec parseTail : List Char → Option (List Glyph)
        | [] => some []
        | x :: xs =>
          match Glyph.ofChar? x with
          | none => none
          | some gx => (parseTail xs).map (gx :: ·)
      (parseTail cs).map (fun rest => { head := g, tail := rest })


-- ---------------------------------------------------------------------------
-- 1. Witnessed Difference Tokens
-- ---------------------------------------------------------------------------

/-- Witnessed difference cut `<glyph!=glyph>`. -/
structure DistinctCut where
  first : Glyph
  second : Glyph
  deriving Repr, DecidableEq

def DistinctCut.toWire (c : DistinctCut) : String :=
  s!"<{c.first}!={c.second}>"

instance : ToString DistinctCut := ⟨DistinctCut.toWire⟩

/-- Simplex edge pair `<glyph,glyph>`. -/
structure SimplexPair where
  first : Glyph
  second : Glyph
  deriving Repr, DecidableEq

def SimplexPair.toWire (p : SimplexPair) : String :=
  s!"<{p.first},{p.second}>"

instance : ToString SimplexPair := ⟨SimplexPair.toWire⟩

/-- Marked quotient token `quot<glyph/word>`. -/
structure MarkedQuotient where
  numerator : Glyph
  fiber : Word
  deriving Repr, DecidableEq

def MarkedQuotient.toWire (q : MarkedQuotient) : String :=
  s!"quot<{q.numerator}/{q.fiber}>"

instance : ToString MarkedQuotient := ⟨MarkedQuotient.toWire⟩

/-- Difference item union covering cuts, pairs, and marked quotients. -/
inductive DifferenceItem where
  | cut (c : DistinctCut)
  | pair (p : SimplexPair)
  | quotient (q : MarkedQuotient)
  deriving Repr, DecidableEq

def DifferenceItem.toWire : DifferenceItem → String
  | .cut c => c.toWire
  | .pair p => p.toWire
  | .quotient q => q.toWire

instance : ToString DifferenceItem := ⟨DifferenceItem.toWire⟩


-- ---------------------------------------------------------------------------
-- 2. Transport & Homotopy Events
-- ---------------------------------------------------------------------------

/-- Boundary d0 map `d0(glyph)`. -/
structure D0Map where
  target : Glyph
  deriving Repr, DecidableEq

def D0Map.toWire (m : D0Map) : String :=
  s!"d0({m.target})"

instance : ToString D0Map := ⟨D0Map.toWire⟩

/-- Boundary d1 map `d1(glyph,glyph)`. -/
structure D1Map where
  first : Glyph
  second : Glyph
  deriving Repr, DecidableEq

def D1Map.toWire (m : D1Map) : String :=
  s!"d1({m.first},{m.second})"

instance : ToString D1Map := ⟨D1Map.toWire⟩

/-- Homotopy filler operator `H(glyph,glyph)`. -/
structure HHomotopy where
  first : Glyph
  second : Glyph
  deriving Repr, DecidableEq

def HHomotopy.toWire (h : HHomotopy) : String :=
  s!"H({h.first},{h.second})"

instance : ToString HHomotopy := ⟨HHomotopy.toWire⟩

/-- Transport and homotopy events. -/
inductive TransportEvent where
  | d0 (m : D0Map)
  | d1 (m : D1Map)
  | homotopy (h : HHomotopy)
  deriving Repr, DecidableEq

def TransportEvent.toWire : TransportEvent → String
  | .d0 m => m.toWire
  | .d1 m => m.toWire
  | .homotopy h => h.toWire

instance : ToString TransportEvent := ⟨TransportEvent.toWire⟩


-- ---------------------------------------------------------------------------
-- 3. Quotient Witness & Obstruction Profile
-- ---------------------------------------------------------------------------

/-- Status of a quotient witness. -/
inductive WitnessStatus where
  | exactRepair
  | homotopicZero
  | closedClass
  | openObstruction
  deriving Repr, DecidableEq

def WitnessStatus.toWire : WitnessStatus → String
  | .exactRepair => "EXACT_REPAIR"
  | .homotopicZero => "HOMOTOPIC_ZERO"
  | .closedClass => "CLOSED_CLASS"
  | .openObstruction => "OPEN_OBSTRUCTION"

instance : ToString WitnessStatus := ⟨WitnessStatus.toWire⟩

def WitnessStatus.ofString? : String → Option WitnessStatus
  | "EXACT_REPAIR" => some .exactRepair
  | "HOMOTOPIC_ZERO" => some .homotopicZero
  | "CLOSED_CLASS" => some .closedClass
  | "OPEN_OBSTRUCTION" => some .openObstruction
  | _ => none

/-- Quotient witness `witness<fiber:word,status:witness_status>`. -/
structure QuotientWitness where
  fiber : Word
  status : WitnessStatus
  deriving Repr, DecidableEq

def QuotientWitness.toWire (w : QuotientWitness) : String :=
  s!"witness<fiber:{w.fiber},status:{w.status}>"

instance : ToString QuotientWitness := ⟨QuotientWitness.toWire⟩


-- ---------------------------------------------------------------------------
-- 4. Balance Matrix & Complex Composite
-- ---------------------------------------------------------------------------

/-- Balance matrix `balance<sites:digits,trace:digits>`. -/
structure BalanceMatrix where
  sites : Nat
  trace : Nat
  deriving Repr, DecidableEq

def BalanceMatrix.toWire (b : BalanceMatrix) : String :=
  s!"balance<sites:{b.sites},trace:{b.trace}>"

instance : ToString BalanceMatrix := ⟨BalanceMatrix.toWire⟩


-- ---------------------------------------------------------------------------
-- 5. Typed Refusal Codes
-- ---------------------------------------------------------------------------

/-- Standard refusal codes. -/
inductive RefusalCode where
  | fiberNonConstant
  | malformedFiller
  | capacityExhausted
  | dualImbalance
  deriving Repr, DecidableEq

def RefusalCode.toWire : RefusalCode → String
  | .fiberNonConstant => "ERR_FIBER_NON_CONSTANT"
  | .malformedFiller => "ERR_MALFORMED_FILLER"
  | .capacityExhausted => "ERR_CAPACITY_EXHAUSTED"
  | .dualImbalance => "ERR_DUAL_IMBALANCE"

instance : ToString RefusalCode := ⟨RefusalCode.toWire⟩

def RefusalCode.ofString? : String → Option RefusalCode
  | "ERR_FIBER_NON_CONSTANT" => some .fiberNonConstant
  | "ERR_MALFORMED_FILLER" => some .malformedFiller
  | "ERR_CAPACITY_EXHAUSTED" => some .capacityExhausted
  | "ERR_DUAL_IMBALANCE" => some .dualImbalance
  | _ => none

/-- Typed refusal token `refusal<refusal_code>`. -/
structure WdpRefusal where
  code : RefusalCode
  deriving Repr, DecidableEq

def WdpRefusal.toWire (r : WdpRefusal) : String :=
  s!"refusal<{r.code}>"

instance : ToString WdpRefusal := ⟨WdpRefusal.toWire⟩


-- ---------------------------------------------------------------------------
-- Master WDP Statement
-- ---------------------------------------------------------------------------

/-- Master statement type unifying all WDP productions. -/
inductive WdpStatement where
  | diff (d : DifferenceItem)
  | transport (t : TransportEvent)
  | witness (w : QuotientWitness)
  | balance (b : BalanceMatrix)
  | refusal (r : WdpRefusal)
  deriving Repr, DecidableEq

def WdpStatement.toWire : WdpStatement → String
  | .diff d => d.toWire
  | .transport t => t.toWire
  | .witness w => w.toWire
  | .balance b => b.toWire
  | .refusal r => r.toWire

instance : ToString WdpStatement := ⟨WdpStatement.toWire⟩

end WdpPresentation
