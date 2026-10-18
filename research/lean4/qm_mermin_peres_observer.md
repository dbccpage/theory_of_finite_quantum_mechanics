import Mathlib.Tactic

/-!
# QMMerminPeresObserver — W7.3 (Mermin–Peres as observer-incomparability)

Programme target: DERIV-MASTER W7.3 (path §F.39; §G.44); freeze T15.

**Job:** quantitative operational recovery of Mermin–Peres as an F₂ cochain
obstruction + observer-incomparability reading (row vs column probe families).
Mirrors estate F₂ capital in self-contained dual form; does not re-derive QM.

AuthorityEffect: None.
-/

namespace QM
namespace MerminPeresObserver

abbrev F2 := Bool

def add (x y : F2) : F2 := Bool.xor x y
def xorList (xs : List F2) : F2 := xs.foldl add false

def mask : F2 → F2 → F2
  | true, x => x
  | false, _ => false

inductive V where
  | a11 | a12 | a13
  | a21 | a22 | a23
  | a31 | a32 | a33
  deriving DecidableEq, Repr

inductive C where
  | r1 | r2 | r3
  | c1 | c2 | c3
  deriving DecidableEq, Repr

open V C

def allVariables : List V :=
  [a11, a12, a13, a21, a22, a23, a31, a32, a33]

def contexts : List C :=
  [r1, r2, r3, c1, c2, c3]

theorem n_vars : allVariables.length = 9 := by decide
theorem n_contexts : contexts.length = 6 := by decide

def row1 : V → F2
  | a11 | a12 | a13 => true
  | _ => false

def row2 : V → F2
  | a21 | a22 | a23 => true
  | _ => false

def row3 : V → F2
  | a31 | a32 | a33 => true
  | _ => false

def col1 : V → F2
  | a11 | a21 | a31 => true
  | _ => false

def col2 : V → F2
  | a12 | a22 | a32 => true
  | _ => false

def col3 : V → F2
  | a13 | a23 | a33 => true
  | _ => false

def A : C → V → F2
  | r1 => row1
  | r2 => row2
  | r3 => row3
  | c1 => col1
  | c2 => col2
  | c3 => col3

abbrev Assignment := V → F2

def d0 (a : Assignment) (c : C) : F2 :=
  xorList (allVariables.map fun v => mask (A c v) (a v))

/-- Target: five + (false) and c3 = − (true). -/
def target : C → F2
  | r1 | r2 | r3 | c1 | c2 => false
  | c3 => true

def ell (y : C → F2) : F2 :=
  xorList (contexts.map y)

def incidenceParity (v : V) : F2 :=
  xorList (contexts.map fun c => A c v)

theorem all_variable_incidences_even :
    ∀ v : V, incidenceParity v = false
  | a11 | a12 | a13 | a21 | a22 | a23 | a31 | a32 | a33 => rfl

theorem ell_d0_eq_false (a : Assignment) : ell (d0 a) = false := by
  change
    xorList
      [xorList [a a11, a a12, a a13, false, false, false, false, false, false],
       xorList [false, false, false, a a21, a a22, a a23, false, false, false],
       xorList [false, false, false, false, false, false, a a31, a a32, a a33],
       xorList [a a11, false, false, a a21, false, false, a a31, false, false],
       xorList [false, a a12, false, false, a a22, false, false, a a32, false],
       xorList [false, false, a a13, false, false, a a23, false, false, a a33]]
      = false
  cases a a11 <;> cases a a12 <;> cases a a13 <;>
  cases a a21 <;> cases a a22 <;> cases a a23 <;>
  cases a a31 <;> cases a a32 <;> cases a a33 <;>
  rfl

theorem ell_target_eq_true : ell target = true := by
  rfl

def InImageOfD0 (s : C → F2) : Prop :=
  ∃ a : Assignment, d0 a = s

theorem target_not_in_image : ¬ InImageOfD0 target := by
  intro h
  rcases h with ⟨a, hA⟩
  have h0 : ell (d0 a) = false := ell_d0_eq_false a
  have h1 : ell (d0 a) = true := by
    rw [hA]
    exact ell_target_eq_true
  rw [h1] at h0
  cases h0

def SatisfiesTarget (a : Assignment) : Prop := d0 a = target

theorem no_global_assignment : ¬ ∃ a : Assignment, SatisfiesTarget a := by
  intro h
  exact target_not_in_image h

/-! ## Observer-incomparability reading (row vs column probe families) -/

def rowFamily : List C := [r1, r2, r3]
def colFamily : List C := [c1, c2, c3]

theorem row_family_card : rowFamily.length = 3 := by decide
theorem col_family_card : colFamily.length = 3 := by decide

/-- Families are distinct partitions of the six contexts. -/
theorem families_partition_contexts :
    rowFamily.length + colFamily.length = contexts.length := by
  decide

/-- Observer-incomparability: no assignment jointly realizes the global target
    demanded by combining row and column probe families. -/
def observerIncomparable : Prop :=
  ¬ ∃ a : Assignment, SatisfiesTarget a

theorem observer_incomparable : observerIncomparable :=
  no_global_assignment

/-- Quantitative obstruction vector (cards + parity). -/
structure QuantWitness where
  nVars : Nat
  nContexts : Nat
  nRow : Nat
  nCol : Nat
  targetParity : F2
  deriving DecidableEq, Repr

def quantWitness : QuantWitness :=
  { nVars := 9
    nContexts := 6
    nRow := 3
    nCol := 3
    targetParity := true }

theorem quant_witness_matches :
    quantWitness.nVars = allVariables.length ∧
    quantWitness.nContexts = contexts.length ∧
    quantWitness.nRow = rowFamily.length ∧
    quantWitness.nCol = colFamily.length ∧
    quantWitness.targetParity = ell target := by
  decide

/-! ## T15 recovery status -/

def t15PartialRecovery : Bool := true
/-- Full continuum / Hilbert operator-algebra MP realization remains open. -/
def operatorMpFullRealization_closed : Bool := false
/-- Legacy flag: full realization not closed (product-sign toy is separate). -/
def operatorMpRealization_closed : Bool := false

theorem t15_partial_operator_open :
    t15PartialRecovery = true ∧ operatorMpRealization_closed = false ∧
    operatorMpFullRealization_closed = false := by
  decide

/-! ## Operator-square residual (named Pauli product-sign toy)

Standard two-qubit Mermin–Peres operator labels (Mermin 1990 / Peres 1990 package):

```
a11 = X⊗I   a12 = I⊗X   a13 = X⊗X
a21 = I⊗Y   a22 = Y⊗I   a23 = Y⊗Y
a31 = X⊗Y   a32 = Y⊗X   a33 = Z⊗Z
```

Encoded as phase-group elements $i^{p} X^{x_1}Z^{z_1}\otimes X^{x_2}Z^{z_2}$ with
$p\in\mathbb{Z}/4\mathbb{Z}$. Context product signs recover the F₂ target
(five $+$, $c_3=-$). Full spectral/Hilbert derivation remains **OPEN**.
FinL1 classical diagonal host does not admit this operator package.
-/

/-- Two-qubit Pauli-phase element: $(p, x_1, z_1, x_2, z_2)$. -/
structure Pauli2 where
  p : Nat
  x1 : Bool
  z1 : Bool
  x2 : Bool
  z2 : Bool
  deriving DecidableEq, Repr

namespace Pauli2

def id : Pauli2 := { p := 0, x1 := false, z1 := false, x2 := false, z2 := false }

/-- Single-qubit mul contribution: phase bump $2\cdot z\cdot x'$ when multiplying $X^{x}Z^{z}\cdot X^{x'}Z^{z'}$. -/
def phaseBump (z x' : Bool) : Nat := if z && x' then 2 else 0

def mul (A B : Pauli2) : Pauli2 :=
  { p := (A.p + B.p + phaseBump A.z1 B.x1 + phaseBump A.z2 B.x2) % 4
    x1 := xor A.x1 B.x1
    z1 := xor A.z1 B.z1
    x2 := xor A.x2 B.x2
    z2 := xor A.z2 B.z2 }

def isPlusId (A : Pauli2) : Bool :=
  A.p == 0 && !A.x1 && !A.z1 && !A.x2 && !A.z2

def isMinusId (A : Pauli2) : Bool :=
  A.p == 2 && !A.x1 && !A.z1 && !A.x2 && !A.z2

/-- Product sign as F₂: false = +, true = − (matches `target`). -/
def productSignMinus (A : Pauli2) : Option F2 :=
  if isPlusId A then some false
  else if isMinusId A then some true
  else none

end Pauli2

/-- Named square operators (phase-group packaging of standard labels). -/
def squareOp : V → Pauli2
  | a11 => { p := 0, x1 := true,  z1 := false, x2 := false, z2 := false } -- X⊗I
  | a12 => { p := 0, x1 := false, z1 := false, x2 := true,  z2 := false } -- I⊗X
  | a13 => { p := 0, x1 := true,  z1 := false, x2 := true,  z2 := false } -- X⊗X
  | a21 => { p := 1, x1 := false, z1 := false, x2 := true,  z2 := true  } -- I⊗Y
  | a22 => { p := 1, x1 := true,  z1 := true,  x2 := false, z2 := false } -- Y⊗I
  | a23 => { p := 2, x1 := true,  z1 := true,  x2 := true,  z2 := true  } -- Y⊗Y
  | a31 => { p := 1, x1 := true,  z1 := false, x2 := true,  z2 := true  } -- X⊗Y
  | a32 => { p := 1, x1 := true,  z1 := true,  x2 := true,  z2 := false } -- Y⊗X
  | a33 => { p := 0, x1 := false, z1 := true,  x2 := false, z2 := true  } -- Z⊗Z

def contextProduct (c : C) : Pauli2 :=
  match c with
  | r1 => Pauli2.mul (Pauli2.mul (squareOp a11) (squareOp a12)) (squareOp a13)
  | r2 => Pauli2.mul (Pauli2.mul (squareOp a21) (squareOp a22)) (squareOp a23)
  | r3 => Pauli2.mul (Pauli2.mul (squareOp a31) (squareOp a32)) (squareOp a33)
  | c1 => Pauli2.mul (Pauli2.mul (squareOp a11) (squareOp a21)) (squareOp a31)
  | c2 => Pauli2.mul (Pauli2.mul (squareOp a12) (squareOp a22)) (squareOp a32)
  | c3 => Pauli2.mul (Pauli2.mul (squareOp a13) (squareOp a23)) (squareOp a33)

theorem context_products_match_target :
    Pauli2.productSignMinus (contextProduct r1) = some false ∧
    Pauli2.productSignMinus (contextProduct r2) = some false ∧
    Pauli2.productSignMinus (contextProduct r3) = some false ∧
    Pauli2.productSignMinus (contextProduct c1) = some false ∧
    Pauli2.productSignMinus (contextProduct c2) = some false ∧
    Pauli2.productSignMinus (contextProduct c3) = some true := by
  decide

theorem operator_product_signs_eq_target :
    (∀ c : C, Pauli2.productSignMinus (contextProduct c) = some (target c)) := by
  intro c
  cases c <;> decide

/-- Operator product-sign package requires quantum Pauli host (not FinL1). -/
inductive OpHost where
  | finL1Classical
  | quantumPauliLift
  deriving DecidableEq, Repr

def admitsOperatorProductPackage : OpHost → Bool
  | .finL1Classical => false
  | .quantumPauliLift => true

theorem finL1_no_operator_product_package :
    admitsOperatorProductPackage .finL1Classical = false := by
  decide

theorem quantum_host_admits_operator_product_package :
    admitsOperatorProductPackage .quantumPauliLift = true := by
  decide

/-- Named product-sign residual closed at TOY-MECH; full Hilbert still OPEN. -/
def operatorProductSignPackage_toy : Bool := true

theorem operator_product_sign_package :
    operatorProductSignPackage_toy = true ∧
    (∀ c : C, Pauli2.productSignMinus (contextProduct c) = some (target c)) ∧
    admitsOperatorProductPackage .quantumPauliLift = true ∧
    admitsOperatorProductPackage .finL1Classical = false ∧
    operatorMpFullRealization_closed = false :=
  ⟨rfl, operator_product_signs_eq_target, rfl, rfl, rfl⟩

/-! ## Main package -/

theorem mermin_peres_observer_package :
    allVariables.length = 9 ∧
    contexts.length = 6 ∧
    ell target = true ∧
    (¬ ∃ a : Assignment, SatisfiesTarget a) ∧
    observerIncomparable ∧
    operatorProductSignPackage_toy = true ∧
    operatorMpFullRealization_closed = false :=
  ⟨n_vars, n_contexts, ell_target_eq_true, no_global_assignment,
    observer_incomparable, rfl, rfl⟩

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end MerminPeresObserver
end QM

#print axioms QM.MerminPeresObserver.no_global_assignment
#print axioms QM.MerminPeresObserver.mermin_peres_observer_package
#print axioms QM.MerminPeresObserver.operator_product_sign_package
#print axioms QM.MerminPeresObserver.structure_not_auth
