/-!
# MSS-N Presentation Syntax & Inductive Wire Tokens (Lean 4)

AuthorityEffect: None. GenesisEffect: None.
Mathlib-free syntax sketches for 19 of the 22 profiles in `mssn.ebnf`.
These structures are not a grammar recognizer: Char, Nat and String fields
are unrestricted (for example Glyph.digit 12 renders two characters).
No well-formedness, parser correspondence or round-trip theorem is proved here.
The Python codec checks all 22 profiles separately; its tests do not establish
a Lean/Python equivalence. Raw glyphs and both Unicode path profiles are absent.
-/

namespace MssnPresentation

/-- Raw glyph sketch; the intended ASCII and single-digit bounds are not encoded. -/
inductive Glyph where
  | latin (c : Char)
  | digit (d : Nat)
  deriving Repr, DecidableEq

def Glyph.toString : Glyph → String
  | .latin c => String.singleton c
  | .digit d => s!"{d}"

instance : ToString Glyph := ⟨Glyph.toString⟩

/-- Path direction token: forward `>` or backward `<`. -/
inductive Direction where
  | fwd
  | bwd
  deriving Repr, DecidableEq

def Direction.toWire : Direction → String
  | .fwd => ">"
  | .bwd => "<"

instance : ToString Direction := ⟨Direction.toWire⟩

/-- 02: Word over Sigma36. -/
structure Word where
  head : Glyph
  tail : List Glyph
  deriving Repr, DecidableEq

def Word.toWire (w : Word) : String :=
  w.head.toString ++ String.join (w.tail.map Glyph.toString)

instance : ToString Word := ⟨Word.toWire⟩

/-- 03: Glyph path: alternating glyph and direction steps. -/
structure GlyphPath where
  head : Glyph
  steps : List (Direction × Glyph)
  deriving Repr, DecidableEq

def GlyphPath.toWire (p : GlyphPath) : String :=
  p.head.toString ++ String.join (p.steps.map fun (d, g) => d.toWire ++ g.toString)

instance : ToString GlyphPath := ⟨GlyphPath.toWire⟩

/-- 04: Label path: alternating word and direction steps. -/
structure LabelPath where
  head : Word
  steps : List (Direction × Word)
  deriving Repr, DecidableEq

def LabelPath.toWire (p : LabelPath) : String :=
  p.head.toWire ++ String.join (p.steps.map fun (d, w) => d.toWire ++ w.toWire)

instance : ToString LabelPath := ⟨LabelPath.toWire⟩

/-- Suffix vertex: lower latin followed by decimal digits. -/
structure SuffixVertex where
  label : Char
  digits : String
  deriving Repr, DecidableEq

def SuffixVertex.toWire (v : SuffixVertex) : String :=
  String.singleton v.label ++ v.digits

instance : ToString SuffixVertex := ⟨SuffixVertex.toWire⟩

/-- 05: Suffix path. -/
structure SuffixPath where
  head : SuffixVertex
  steps : List (Direction × SuffixVertex)
  deriving Repr, DecidableEq

def SuffixPath.toWire (p : SuffixPath) : String :=
  p.head.toWire ++ String.join (p.steps.map fun (d, v) => d.toWire ++ v.toWire)

instance : ToString SuffixPath := ⟨SuffixPath.toWire⟩

/-- 06: Path list: semicolon-separated glyph paths. -/
structure PathList where
  head : GlyphPath
  tail : List GlyphPath
  deriving Repr, DecidableEq

def PathList.toWire (l : PathList) : String :=
  l.head.toWire ++ String.join (l.tail.map fun p => ";" ++ p.toWire)

/-- 07: Suffix list: semicolon-separated suffix paths. -/
structure SuffixList where
  head : SuffixPath
  tail : List SuffixPath
  deriving Repr, DecidableEq

def SuffixList.toWire (l : SuffixList) : String :=
  l.head.toWire ++ String.join (l.tail.map fun p => ";" ++ p.toWire)

/-- Scalar annotation: optional sign, digits, optional fraction or ratio. -/
structure Scalar where
  sign : Option Char
  whole : String
  fracOrRatio : Option (Char × String)
  deriving Repr, DecidableEq

def Scalar.toWire (s : Scalar) : String :=
  (match s.sign with | some c => String.singleton c | none => "") ++
  s.whole ++
  (match s.fracOrRatio with | some (sep, d) => String.singleton sep ++ d | none => "")

instance : ToString Scalar := ⟨Scalar.toWire⟩

/-- 08: Scalar vertex and path. -/
structure ScalarVertex where
  label : Char
  scalar : Scalar
  deriving Repr, DecidableEq

def ScalarVertex.toWire (v : ScalarVertex) : String :=
  String.singleton v.label ++ ":" ++ v.scalar.toWire

structure ScalarPath where
  head : ScalarVertex
  steps : List (Direction × ScalarVertex)
  deriving Repr, DecidableEq

def ScalarPath.toWire (p : ScalarPath) : String :=
  p.head.toWire ++ String.join (p.steps.map fun (d, v) => d.toWire ++ v.toWire)

/-- 09: Vector vertex and path. -/
structure VectorVertex where
  label : Char
  headCoord : Scalar
  tailCoords : List Scalar
  deriving Repr, DecidableEq

def VectorVertex.toWire (v : VectorVertex) : String :=
  String.singleton v.label ++ "[" ++ v.headCoord.toWire ++
  String.join (v.tailCoords.map fun s => "," ++ s.toWire) ++ "]"

structure VectorPath where
  head : VectorVertex
  steps : List (Direction × VectorVertex)
  deriving Repr, DecidableEq

def VectorPath.toWire (p : VectorPath) : String :=
  p.head.toWire ++ String.join (p.steps.map fun (d, v) => d.toWire ++ v.toWire)

/-- 10: Edge weight path: alternating latin and weighted links. -/
structure WeightedLink where
  dir : Direction
  weight : Scalar
  deriving Repr, DecidableEq

def WeightedLink.toWire (l : WeightedLink) : String :=
  l.dir.toWire ++ l.weight.toWire ++ l.dir.toWire

structure EdgeWeightPath where
  head : Char
  steps : List (WeightedLink × Char)
  deriving Repr, DecidableEq

def EdgeWeightPath.toWire (p : EdgeWeightPath) : String :=
  String.singleton p.head ++ String.join (p.steps.map fun (l, c) => l.toWire ++ String.singleton c)

/-- 11: Labelled path: named relation steps `a-step>b`. -/
structure LabelledPath where
  head : Char
  steps : List (Word × Char)
  deriving Repr, DecidableEq

def LabelledPath.toWire (p : LabelledPath) : String :=
  String.singleton p.head ++ String.join (p.steps.map fun (w, c) => "-" ++ w.toWire ++ ">" ++ String.singleton c)

/-- 12: Binary prefix tree. -/
inductive PrefixTree where
  | leaf (g : Glyph)
  | branch (d : Direction) (left right : PrefixTree)
  deriving Repr, DecidableEq

def PrefixTree.toWire : PrefixTree → String
  | .leaf g => g.toString
  | .branch d l r => d.toWire ++ l.toWire ++ r.toWire

/-- 13: Binary postfix tree: glyph followed by zero or more (child_tree, direction) steps. -/
inductive PostfixTree where
  | node (head : Glyph) (steps : List (PostfixTree × Direction))
  deriving Repr

partial def PostfixTree.toWire : PostfixTree → String
  | .node h steps => h.toString ++ String.join (steps.map fun (t, d) => t.toWire ++ d.toWire)

/-- 14: Sequence: comma-separated glyphs. -/
structure GlyphSequence where
  head : Glyph
  tail : List Glyph
  deriving Repr, DecidableEq

def GlyphSequence.toWire (s : GlyphSequence) : String :=
  s.head.toString ++ String.join (s.tail.map fun g => "," ++ g.toString)

/-- 15: Nested grouping tree. -/
inductive NestedTree where
  | leaf (g : Glyph)
  | group (children : List NestedTree)
  deriving Repr

def NestedTree.toWire : NestedTree → String
  | .leaf g => g.toString
  | .group cs => "(" ++ String.intercalate "," (cs.map NestedTree.toWire) ++ ")"

/-- 16: Head term application: `f(x, g(y))`. -/
inductive HeadTerm where
  | atom (w : Word)
  | app (w : Word) (args : List HeadTerm)
  deriving Repr

def HeadTerm.toWire : HeadTerm → String
  | .atom w => w.toWire
  | .app w args => w.toWire ++ "(" ++ String.intercalate "," (args.map HeadTerm.toWire) ++ ")"

/-- 17: Hypergraph incidence item. -/
structure IncidenceItem where
  srcHead : Glyph
  srcTail : List Glyph
  tgtHead : Glyph
  tgtTail : List Glyph
  deriving Repr, DecidableEq

def IncidenceItem.toWire (it : IncidenceItem) : String :=
  "[" ++ it.srcHead.toString ++ String.join (it.srcTail.map fun g => "," ++ g.toString) ++ "]>" ++
  "[" ++ it.tgtHead.toString ++ String.join (it.tgtTail.map fun g => "," ++ g.toString) ++ "]"

structure IncidenceList where
  head : IncidenceItem
  tail : List IncidenceItem
  deriving Repr, DecidableEq

def IncidenceList.toWire (l : IncidenceList) : String :=
  l.head.toWire ++ String.join (l.tail.map fun it => ";" ++ it.toWire)

/-- 20: Bitstream. -/
structure Bitstream where
  bits : String
  deriving Repr, DecidableEq

def Bitstream.toWire (b : Bitstream) : String := b.bits

/-- 21: Octets. -/
structure Octets where
  hex : String
  deriving Repr, DecidableEq

def Octets.toWire (o : Octets) : String := o.hex

/-- 22: Directed rewrite rule `lhs => rhs`. -/
structure RewriteRule where
  lhs : List Glyph
  rhs : List Glyph
  deriving Repr, DecidableEq

def RewriteRule.toWire (r : RewriteRule) : String :=
  String.join (r.lhs.map Glyph.toString) ++ "=>" ++ String.join (r.rhs.map Glyph.toString)

end MssnPresentation
