/-!
# Primitive Passage Dynamics, Four Gates & Active Obstruction (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/PrimitivePassage.lean
- lean4/Derivation/DiffInterface.lean

Classification: Dynamic passage apparatus & active obstruction calculus.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.PrimitivePassage

/-- Occurrence index and pair abbreviations. -/
abbrev Occ := Nat
abbrev Pair := Nat × Nat
abbrev Col := List Nat

/-- Passage State (PState) carrying separated stores:
    `occ`: occurrences (0-cells)
    `asserted`: positive difference assertions (1-cells)
    `wit`: retained positive difference witnesses
    `prot`: protected-demand store (deontic constraints)
    `obs`: declared observation partition columns (none is pre-observational)
    `budget`: fuel budget
    `licensed`: operational authorization gate
    `refusals`: certificate-bearing refusal records
    `halted`: absorbing terminal flag -/
structure PState where
  occ : List Occ
  asserted : List Pair
  wit : List Pair
  prot : List Pair
  obs : Option (List Col)
  budget : Nat
  licensed : Bool
  refusals : List Pair
  halted : Bool
deriving Repr, DecidableEq

/-- The genesis passage state. -/
def genesisP : PState :=
  { occ := [], asserted := [], wit := [], prot := [], obs := none,
    budget := 0, licensed := true, refusals := [], halted := false }

/-- Passage events (PEvent). -/
inductive PEvent where
  | admitOcc (t : Occ)
  | assertWit (i j : Occ)
  | admitWit (i j : Occ)
  | protect (i j : Occ)
  | declareObs
  | refineCol (v : Col) (p : Occ)
  | addCol (c : Col)
  | refuse (i j : Occ)
  | setBudget (n : Nat)
  | setLicense (b : Bool)
  | halt
deriving Repr, DecidableEq

/-- One column separates two occurrence positions. -/
def sepCol (c : Col) (i j : Occ) : Bool :=
  (decide (i ∈ c)) != (decide (j ∈ c))

/-- Observer separation across declared columns. -/
def sepP (cols : List Col) (i j : Occ) : Bool :=
  cols.any (fun c => sepCol c i j)

/-- The zero relation of a declared observation: no declared column separates. -/
def zeroP (cols : List Col) (i j : Occ) : Bool :=
  !sepP cols i j

/-- Active obstruction: retained, protected, observation declared, and observer-zero. -/
def obstP (s : PState) (i j : Occ) : Bool :=
  (decide ((i, j) ∈ s.wit)) && (decide ((i, j) ∈ s.prot))
    && (match s.obs with
        | none => false
        | some cols => zeroP cols i j)

/-- Gate 1: Retained witness. -/
def retainedP (s : PState) (i j : Occ) : Bool :=
  decide ((i, j) ∈ s.wit)

/-- Gate 2: Protected demand. -/
def protectedP (s : PState) (i j : Occ) : Bool :=
  decide ((i, j) ∈ s.prot)

/-- Gate 3: Observation declared. -/
def declaredP (s : PState) : Bool :=
  s.obs.isSome

/-- Gate 4: Zero relation holds on declared observation. -/
def zeroPGate (s : PState) (i j : Occ) : Bool :=
  match s.obs with
  | none => false
  | some cols => zeroP cols i j

/-- Active obstruction factor theorem: obstP is the exact product of four total gates. -/
theorem obstP_factors (s : PState) (i j : Occ) :
    obstP s i j = (retainedP s i j && protectedP s i j && declaredP s && zeroPGate s i j) := by
  unfold obstP retainedP protectedP declaredP zeroPGate
  cases s.obs with
  | none => simp
  | some cols => simp

end GenesisPrimitives.PrimitivePassage
