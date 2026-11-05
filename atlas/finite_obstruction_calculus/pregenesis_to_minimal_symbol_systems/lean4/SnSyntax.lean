/-!
# S(n) Presentation Syntax & Inductive Wire Tokens (Lean 4)

AuthorityEffect: None. GenesisEffect: None.
Typed syntax corresponding to the flat S(n) presentation grammar `sn.ebnf`.
No wire parser or Python/Lean equivalence theorem is supplied here.
All types are constructive and Mathlib-free.
-/

namespace SnPresentation

/-- Primitive character tokens: lowercase ASCII letter or decimal digit. -/
inductive Glyph where
  | latin (c : Fin 26)
  | digit (d : Fin 10)
  deriving Repr, DecidableEq

/-- Render a Glyph as a string. -/
def Glyph.toString : Glyph → String
  | .latin c => String.singleton (Char.ofNat ('a'.toNat + c.val))
  | .digit d => s!"{d.val}"

instance : ToString Glyph := ⟨Glyph.toString⟩

/-- Stage S(0): The Ground presentation token `<>`.
    Note: presentation token length is 1, while carrier cardinality is 0. -/
structure GroundToken where
  raw : Unit := ()
  deriving Repr, DecidableEq

def GroundToken.toWire (_ : GroundToken) : String := "<>"

/-- Supplied mark syntax `<a>`; construction of syntax is not admission. -/
structure SuppliedToken where
  mark : Glyph
  deriving Repr, DecidableEq

def SuppliedToken.toWire (s : SuppliedToken) : String :=
  s!"<{s.mark}>"

/-- Stage S(2): Retained pair token `<ab>`. -/
structure RetainedPair where
  first : Glyph
  second : Glyph
  deriving Repr, DecidableEq

def RetainedPair.toWire (p : RetainedPair) : String :=
  s!"<{p.first}{p.second}>"

/-- Directed cut syntax `<a->b>`; endpoint inequality is a separate premise. -/
structure DirectedCut where
  src : Glyph
  tgt : Glyph
  deriving Repr, DecidableEq

def DirectedCut.toWire (c : DirectedCut) : String :=
  s!"<{c.src}->{c.tgt}>"

/-- Stage S(3): Abstract 1-simplex cut `[a,b]`. -/
structure SimplexCut where
  v0 : Glyph
  v1 : Glyph
  deriving Repr, DecidableEq

def SimplexCut.toWire (s : SimplexCut) : String :=
  s!"[{s.v0},{s.v1}]"

/-- Relational token alternatives covering S(2) and S(3). -/
inductive RelationToken where
  | pair (p : RetainedPair)
  | cut (c : DirectedCut)
  | simplex (s : SimplexCut)
  deriving Repr, DecidableEq

def RelationToken.toWire : RelationToken → String
  | .pair p => p.toWire
  | .cut c => c.toWire
  | .simplex s => s.toWire

/-- Inner body enclosure for section lifts and retractions. -/
inductive InnerBody where
  | arrow (src : Glyph) (tgt : Glyph)
  | pair (first : Glyph) (second : Glyph)
  | glyphs (gs : List Glyph)
  deriving Repr, DecidableEq

def InnerBody.toWire : InnerBody → String
  | .arrow src tgt => s!"{src}->{tgt}"
  | .pair f s => s!"{f},{s}"
  | .glyphs gs => String.join (gs.map Glyph.toString)

/-- Stage S(6): Section lift `u_N<inner_body>`. -/
structure SectionLift where
  stage : Nat
  body : InnerBody
  deriving Repr, DecidableEq

def SectionLift.toWire (l : SectionLift) : String :=
  s!"u_{l.stage}<{l.body.toWire}>"

/-- Stage S(6): Retraction down-map `r_N<inner_body>`. -/
structure RetractionMap where
  stage : Nat
  body : InnerBody
  deriving Repr, DecidableEq

def RetractionMap.toWire (r : RetractionMap) : String :=
  s!"r_{r.stage}<{r.body.toWire}>"

/-- Stage S(6): Explicit typed refusal token `NON_DESCENT`. -/
structure NonDescent where
  raw : Unit := ()
  deriving Repr, DecidableEq

def NonDescent.toWire (_ : NonDescent) : String := "NON_DESCENT"

/-- Master S(n) presentation grammar inductive type aligning with `sn_presentation` in `sn.ebnf`. -/
inductive SnPresentation where
  | ground (g : GroundToken)
  | supplied (s : SuppliedToken)
  | relation (r : RelationToken)
  | lift (l : SectionLift)
  | retraction (r : RetractionMap)
  | nonDescent (nd : NonDescent)
  deriving Repr, DecidableEq

def SnPresentation.toWire : SnPresentation → String
  | .ground g => g.toWire
  | .supplied s => s.toWire
  | .relation r => r.toWire
  | .lift l => l.toWire
  | .retraction r => r.toWire
  | .nonDescent nd => nd.toWire

instance : ToString SnPresentation := ⟨SnPresentation.toWire⟩

end SnPresentation
