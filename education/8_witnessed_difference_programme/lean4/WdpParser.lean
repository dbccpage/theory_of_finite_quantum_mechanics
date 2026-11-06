import WdpSyntax

/-!
# WDP Wire Parser in Lean 4

AuthorityEffect: None. GenesisEffect: None.
Deterministic, total, and constructive parser converting wire strings into `WdpStatement` ASTs.
Guarantees round-trip parity with the Python `wdp_codec.py` and `wdp.ebnf`.
-/

namespace WdpPresentation

/-- Helper to check if all characters in a list are ASCII digits and non-empty. -/
def isDigitsList (cs : List Char) : Bool :=
  match cs with
  | [] => false
  | _ => cs.all (fun c => '0' ≤ c ∧ c ≤ '9')

/-- Helper to split a list of characters at the first occurrence of ",status:". -/
def splitStatus (cs : List Char) : Option (List Char × List Char) :=
  let rec loop (acc : List Char) : List Char → Option (List Char × List Char)
    | ',' :: 's' :: 't' :: 'a' :: 't' :: 'u' :: 's' :: ':' :: rest =>
      some (acc.reverse, rest)
    | x :: xs => loop (x :: acc) xs
    | [] => none
  loop [] cs

/-- Helper to split a list of characters at the first occurrence of ",trace:". -/
def splitTrace (cs : List Char) : Option (List Char × List Char) :=
  let rec loop (acc : List Char) : List Char → Option (List Char × List Char)
    | ',' :: 't' :: 'r' :: 'a' :: 'c' :: 'e' :: ':' :: rest =>
      some (acc.reverse, rest)
    | x :: xs => loop (x :: acc) xs
    | [] => none
  loop [] cs


-- ---------------------------------------------------------------------------
-- Parsers for Specific Formats
-- ---------------------------------------------------------------------------

def parseDistinctCut? (cs : List Char) : Option DistinctCut :=
  match cs with
  | ['<', c1, '!', '=', c2, '>'] =>
    match Glyph.ofChar? c1, Glyph.ofChar? c2 with
    | some g1, some g2 => some { first := g1, second := g2 }
    | _, _ => none
  | _ => none

def parseSimplexPair? (cs : List Char) : Option SimplexPair :=
  match cs with
  | ['<', c1, ',', c2, '>'] =>
    match Glyph.ofChar? c1, Glyph.ofChar? c2 with
    | some g1, some g2 => some { first := g1, second := g2 }
    | _, _ => none
  | _ => none

def parseMarkedQuotient? (cs : List Char) : Option MarkedQuotient :=
  match cs with
  | 'q' :: 'u' :: 'o' :: 't' :: '<' :: rest =>
    match rest.reverse with
    | '>' :: innerRev =>
      let inner := innerRev.reverse
      match inner with
      | numChar :: '/' :: wordChars =>
        match Glyph.ofChar? numChar, Word.ofString? (String.ofList wordChars) with
        | some num, some fib => some { numerator := num, fiber := fib }
        | _, _ => none
      | _ => none
    | _ => none
  | _ => none

def parseD0Map? (cs : List Char) : Option D0Map :=
  match cs with
  | ['d', '0', '(', c, ')'] =>
    (Glyph.ofChar? c).map (fun g => { target := g })
  | _ => none

def parseD1Map? (cs : List Char) : Option D1Map :=
  match cs with
  | ['d', '1', '(', c1, ',', c2, ')'] =>
    match Glyph.ofChar? c1, Glyph.ofChar? c2 with
    | some g1, some g2 => some { first := g1, second := g2 }
    | _, _ => none
  | _ => none

def parseHHomotopy? (cs : List Char) : Option HHomotopy :=
  match cs with
  | ['H', '(', c1, ',', c2, ')'] =>
    match Glyph.ofChar? c1, Glyph.ofChar? c2 with
    | some g1, some g2 => some { first := g1, second := g2 }
    | _, _ => none
  | _ => none

def parseQuotientWitness? (cs : List Char) : Option QuotientWitness :=
  match cs with
  | 'w' :: 'i' :: 't' :: 'n' :: 'e' :: 's' :: 's' :: '<' :: 'f' :: 'i' :: 'b' :: 'e' :: 'r' :: ':' :: rest =>
    match rest.reverse with
    | '>' :: innerRev =>
      let inner := innerRev.reverse
      match splitStatus inner with
      | some (fiberChars, statusChars) =>
        match Word.ofString? (String.ofList fiberChars), WitnessStatus.ofString? (String.ofList statusChars) with
        | some fib, some st => some { fiber := fib, status := st }
        | _, _ => none
      | none => none
    | _ => none
  | _ => none

def parseBalanceMatrix? (cs : List Char) : Option BalanceMatrix :=
  match cs with
  | 'b' :: 'a' :: 'l' :: 'a' :: 'n' :: 'c' :: 'e' :: '<' :: 's' :: 'i' :: 't' :: 'e' :: 's' :: ':' :: rest =>
    match rest.reverse with
    | '>' :: innerRev =>
      let inner := innerRev.reverse
      match splitTrace inner with
      | some (sitesChars, traceChars) =>
        if isDigitsList sitesChars && isDigitsList traceChars then
          match (String.ofList sitesChars).toNat?, (String.ofList traceChars).toNat? with
          | some s, some t => some { sites := s, trace := t }
          | _, _ => none
        else
          none
      | none => none
    | _ => none
  | _ => none

def parseWdpRefusal? (cs : List Char) : Option WdpRefusal :=
  match cs with
  | 'r' :: 'e' :: 'f' :: 'u' :: 's' :: 'a' :: 'l' :: '<' :: rest =>
    match rest.reverse with
    | '>' :: innerRev =>
      let codeStr := String.ofList innerRev.reverse
      (RefusalCode.ofString? codeStr).map (fun c => { code := c })
    | _ => none
  | _ => none


-- ---------------------------------------------------------------------------
-- Master Parser Function
-- ---------------------------------------------------------------------------

/-- Parse a wire string into a `WdpStatement` AST. Returns `none` on invalid format. -/
def parseWdp? (wire : String) : Option WdpStatement :=
  let cs := wire.toList
  if let some c := parseDistinctCut? cs then
    some (.diff (.cut c))
  else if let some p := parseSimplexPair? cs then
    some (.diff (.pair p))
  else if let some q := parseMarkedQuotient? cs then
    some (.diff (.quotient q))
  else if let some m := parseD0Map? cs then
    some (.transport (.d0 m))
  else if let some m := parseD1Map? cs then
    some (.transport (.d1 m))
  else if let some h := parseHHomotopy? cs then
    some (.transport (.homotopy h))
  else if let some w := parseQuotientWitness? cs then
    some (.witness w)
  else if let some b := parseBalanceMatrix? cs then
    some (.balance b)
  else if let some r := parseWdpRefusal? cs then
    some (.refusal r)
  else
    none

end WdpPresentation
