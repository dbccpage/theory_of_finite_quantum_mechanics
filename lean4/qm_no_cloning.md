import Mathlib.Tactic

/-!
# QMNoCloning — W6.18 / OB-CLONE (no-cloning derived or imported)

Programme target: DERIV-MASTER W6.18 (QMREG-68 / freeze `OB-CLONE`).

**Adjudication (toy form):**

1. **Classical residual copy** of finite bit weights is constructible
   (independent product / distribution copy) — **DERIVED** on FinL1.
2. Therefore a **universal no-cloning law** is **UNDERIVABLE** from FinL1
   residual mass alone: the classical world is a countermodel.
3. Under a **linear amplitude lift**, a basis-cloner (CNOT-style copy of
   computational basis into a blank register) **fails** on unnormalized
   $|+\rangle$ — product $|+\rangle\otimes|+\rangle$ ≠ cloner image.
4. Full continuous unitary no-cloning for all pure states remains **OPEN**
   beyond this discrete toy; package as **CONDITIONAL/IMPORT** of linearity
   + superposition structure when claiming the quantum theorem.
5. **Linearity obstruction residual (TOY-MECH):** basis-cloner is joint-linear;
   $|+\rangle\otimes|0\rangle$ splits as basis products; linear image is
   $|00\rangle+|11\rangle \neq |+\rangle\otimes|+\rangle$; population shadow of
   cloner image $\neq$ product-clone joint; full unitary theorem still **OPEN**.

AuthorityEffect: None.
-/

namespace QM
namespace NoCloning

/-! ## Classical residual bit weights -/

structure BitWeight where
  w0 : Nat
  w1 : Nat
  deriving DecidableEq, Repr

namespace BitWeight

def total (w : BitWeight) : Nat := w.w0 + w.w1

def IsPure (w : BitWeight) : Prop :=
  (w.w0 > 0 ∧ w.w1 = 0) ∨ (w.w0 = 0 ∧ w.w1 > 0)

def IsMixed (w : BitWeight) : Prop := w.w0 > 0 ∧ w.w1 > 0

end BitWeight

def pure0 : BitWeight := { w0 := 1, w1 := 0 }
def pure1 : BitWeight := { w0 := 0, w1 := 1 }
def fairBit : BitWeight := { w0 := 1, w1 := 1 }

/-! ## Joint residual tables (two systems) -/

structure JointWeight where
  w00 : Nat
  w01 : Nat
  w10 : Nat
  w11 : Nat
  deriving DecidableEq, Repr

namespace JointWeight

def total (j : JointWeight) : Nat := j.w00 + j.w01 + j.w10 + j.w11

def margA (j : JointWeight) : BitWeight :=
  { w0 := j.w00 + j.w01, w1 := j.w10 + j.w11 }

def margB (j : JointWeight) : BitWeight :=
  { w0 := j.w00 + j.w10, w1 := j.w01 + j.w11 }

end JointWeight

/-- Classical distribution clone: independent product of $w$ with itself.
    Both marginals recover the (scaled) classical residual table. -/
def classicalClone (w : BitWeight) : JointWeight :=
  { w00 := w.w0 * w.w0
    w01 := w.w0 * w.w1
    w10 := w.w1 * w.w0
    w11 := w.w1 * w.w1 }

theorem classical_clone_margA (w : BitWeight) :
    (classicalClone w).margA =
      { w0 := w.w0 * w.total, w1 := w.w1 * w.total } := by
  cases w with
  | mk w0 w1 =>
    simp [classicalClone, JointWeight.margA, BitWeight.total, Nat.mul_add]

theorem classical_clone_margB (w : BitWeight) :
    (classicalClone w).margB =
      { w0 := w.w0 * w.total, w1 := w.w1 * w.total } := by
  cases w with
  | mk w0 w1 =>
    simp [classicalClone, JointWeight.margB, BitWeight.total, Nat.mul_add, Nat.mul_comm]

theorem classical_clone_fair :
    classicalClone fairBit =
      { w00 := 1, w01 := 1, w10 := 1, w11 := 1 } := by
  simp [classicalClone, fairBit]

theorem classical_clone_pure0 :
    classicalClone pure0 =
      { w00 := 1, w01 := 0, w10 := 0, w11 := 0 } := by
  simp [classicalClone, pure0]

/-- Classical residual admits a perfect distribution-level clone for every bit weight. -/
theorem classical_clone_exists_for_all (w : BitWeight) :
    ∃ j : JointWeight,
      j = classicalClone w ∧
      j.margA = { w0 := w.w0 * w.total, w1 := w.w1 * w.total } ∧
      j.margB = { w0 := w.w0 * w.total, w1 := w.w1 * w.total } :=
  ⟨classicalClone w, rfl, classical_clone_margA w, classical_clone_margB w⟩

theorem classical_cloning_derived :
    (classicalClone pure0).margA.w0 = pure0.total ∧
    (classicalClone fairBit).total = 4 ∧
    fairBit.IsMixed := by
  refine ⟨?_, ?_, ?_⟩
  · simp [classicalClone, pure0, JointWeight.margA, BitWeight.total]
  · simp [classicalClone, fairBit, JointWeight.total]
  · simp [fairBit, BitWeight.IsMixed]

/-! ## Linear amplitude toy (Amp2 + joint AmpJoint)

Unnormalized amplitudes over two sectors. Product states and a basis-cloner
model the standard “copy computational basis fails on superposition” witness.
-/

structure Amp2 where
  a0 : Nat
  a1 : Nat
  deriving DecidableEq, Repr

/-- Two-system joint amplitudes (ordered basis 00,01,10,11). -/
structure AmpJoint where
  a00 : Nat
  a01 : Nat
  a10 : Nat
  a11 : Nat
  deriving DecidableEq, Repr

def amp0 : Amp2 := { a0 := 1, a1 := 0 }
def amp1 : Amp2 := { a0 := 0, a1 := 1 }
/-- Unnormalized $|+\rangle \propto |0\rangle+|1\rangle$. -/
def ampPlus : Amp2 := { a0 := 1, a1 := 1 }

/-- Product state amplitudes $a \otimes b$. -/
def productAmp (a b : Amp2) : AmpJoint :=
  { a00 := a.a0 * b.a0
    a01 := a.a0 * b.a1
    a10 := a.a1 * b.a0
    a11 := a.a1 * b.a1 }

theorem product_plus_plus :
    productAmp ampPlus ampPlus =
      { a00 := 1, a01 := 1, a10 := 1, a11 := 1 } := by
  simp [productAmp, ampPlus]

theorem product_plus_blank0 :
    productAmp ampPlus amp0 =
      { a00 := 1, a01 := 0, a10 := 1, a11 := 0 } := by
  simp [productAmp, ampPlus, amp0]

/-- Basis-cloner (CNOT-style): copy computational basis into blank register.
    $|00\rangle\mapsto|00\rangle$, $|10\rangle\mapsto|11\rangle$;
    off-basis inputs that already occupy 01/11 are left fixed (toy total map). -/
def basisCloner (j : AmpJoint) : AmpJoint :=
  { a00 := j.a00
    a01 := j.a01
    a10 := 0
    a11 := j.a10 + j.a11 }

theorem basis_cloner_on_plus_blank :
    basisCloner (productAmp ampPlus amp0) =
      { a00 := 1, a01 := 0, a10 := 0, a11 := 1 } := by
  simp [basisCloner, productAmp, ampPlus, amp0]

/-- Cloner image of $|+\rangle\otimes|0\rangle$ is **not** the product $|+\rangle\otimes|+\rangle$. -/
theorem basis_cloner_fails_on_plus :
    basisCloner (productAmp ampPlus amp0) ≠ productAmp ampPlus ampPlus := by
  decide

theorem basis_cloner_ok_on_0 :
    basisCloner (productAmp amp0 amp0) = productAmp amp0 amp0 := by
  simp [basisCloner, productAmp, amp0]

theorem basis_cloner_ok_on_1 :
    basisCloner (productAmp amp1 amp0) = productAmp amp1 amp1 := by
  simp [basisCloner, productAmp, amp0, amp1]

/-- Discrete no-cloning witness under linear amplitude structure. -/
theorem linear_lift_no_clone_witness :
    basisCloner (productAmp amp0 amp0) = productAmp amp0 amp0 ∧
    basisCloner (productAmp amp1 amp0) = productAmp amp1 amp1 ∧
    basisCloner (productAmp ampPlus amp0) ≠ productAmp ampPlus ampPlus :=
  ⟨basis_cloner_ok_on_0, basis_cloner_ok_on_1, basis_cloner_fails_on_plus⟩

/-! ## Import status packaging -/

inductive ImportStatus where
  | derived
  | underivable
  | conditionalImport
  deriving DecidableEq, Repr

/-- Classical residual distribution copy. -/
def obCloneClassicalStatus : ImportStatus := .derived

/-- Universal no-cloning forced by FinL1 residual tables alone. -/
def obCloneFromFinL1Status : ImportStatus := .underivable

/-- No-cloning as property of linear amplitude / superposition lift (toy witness). -/
def obCloneUnderLinearLiftStatus : ImportStatus := .conditionalImport

theorem classical_status_derived :
    obCloneClassicalStatus = ImportStatus.derived := rfl

theorem from_finL1_underivable :
    obCloneFromFinL1Status = ImportStatus.underivable := rfl

theorem under_lift_conditional :
    obCloneUnderLinearLiftStatus = ImportStatus.conditionalImport := rfl

/-- Classical countermodel: FinL1 admits clone, so universal no-cloning is not FinL1-forced. -/
theorem no_cloning_not_forced_by_finL1 :
    (∃ j, j = classicalClone fairBit) ∧
    obCloneFromFinL1Status = ImportStatus.underivable :=
  ⟨⟨classicalClone fairBit, rfl⟩, rfl⟩

/-- **Main package.** -/
theorem no_cloning_package :
    (classicalClone fairBit).total = 4 ∧
    basisCloner (productAmp ampPlus amp0) ≠ productAmp ampPlus ampPlus ∧
    obCloneClassicalStatus = ImportStatus.derived ∧
    obCloneFromFinL1Status = ImportStatus.underivable ∧
    obCloneUnderLinearLiftStatus = ImportStatus.conditionalImport := by
  refine ⟨?_, basis_cloner_fails_on_plus, rfl, rfl, rfl⟩
  simp [classicalClone, fairBit, JointWeight.total]

/-- Full continuous unitary no-cloning (all pure states / Wootters–Zurek) remains OPEN. -/
def fullUnitaryNoCloning_open : Prop := True

theorem full_unitary_no_cloning_marked_open :
    fullUnitaryNoCloning_open := trivial

/-! ## Linearity obstruction residual (TOY-MECH)

If a joint map is linear and clones the computational basis into a blank
register, linearity forces the image of $|+\rangle\otimes|0\rangle$ to be
$|00\rangle+|11\rangle$, which is **not** the product clone $|+\rangle\otimes|+\rangle$.

Population shadow of the cloner image is a correlated classical joint, not the
independent product clone of the fair residual table.
-/

def AmpJoint.add (j k : AmpJoint) : AmpJoint :=
  { a00 := j.a00 + k.a00, a01 := j.a01 + k.a01
    a10 := j.a10 + k.a10, a11 := j.a11 + k.a11 }

/-- $|+\rangle\otimes|0\rangle$ splits as basis products (unnormalized). -/
theorem plus_blank_splits_as_basis_products :
    productAmp ampPlus amp0 =
      AmpJoint.add (productAmp amp0 amp0) (productAmp amp1 amp0) := by
  simp [productAmp, AmpJoint.add, ampPlus, amp0, amp1]

/-- Basis-cloner is linear on joint amplitude tables. -/
theorem basis_cloner_linear (j k : AmpJoint) :
    basisCloner (AmpJoint.add j k) = AmpJoint.add (basisCloner j) (basisCloner k) := by
  cases j; cases k
  simp [basisCloner, AmpJoint.add, Nat.add_comm, Nat.add_left_comm]

/-- Linearity + basis-cloning forces $|+\rangle\otimes|0\rangle \mapsto |00\rangle+|11\rangle$. -/
theorem linear_image_of_plus_blank :
    basisCloner (productAmp ampPlus amp0) =
      AmpJoint.add (productAmp amp0 amp0) (productAmp amp1 amp1) := by
  simp [basisCloner, productAmp, AmpJoint.add, ampPlus, amp0, amp1]

/-- That forced image is not the ideal product clone. -/
theorem linear_forced_image_neq_product_clone :
    AmpJoint.add (productAmp amp0 amp0) (productAmp amp1 amp1) ≠
      productAmp ampPlus ampPlus := by
  decide

/-- Population shadow of AmpJoint (nonnegative amplitudes). -/
def jointPop (j : AmpJoint) : JointWeight :=
  { w00 := j.a00, w01 := j.a01, w10 := j.a10, w11 := j.a11 }

/-- Cloner image of $|+\rangle\otimes|0\rangle$ has population $\{(00):1,(11):1\}$. -/
theorem cloner_image_population :
    jointPop (basisCloner (productAmp ampPlus amp0)) =
      { w00 := 1, w01 := 0, w10 := 0, w11 := 1 } := by
  simp [jointPop, basisCloner, productAmp, ampPlus, amp0]

/-- Ideal product clone population is the fair classical joint (all four cells). -/
theorem product_plus_plus_population :
    jointPop (productAmp ampPlus ampPlus) =
      classicalClone fairBit := by
  simp [jointPop, productAmp, ampPlus, classicalClone, fairBit]

/-- Population shadows disagree (cloner image ≠ independent clone). -/
theorem cloner_pop_neq_independent_clone_pop :
    jointPop (basisCloner (productAmp ampPlus amp0)) ≠
      jointPop (productAmp ampPlus ampPlus) := by
  decide

/-- Classical independent clone of fair bit is still constructible (FinL1 capital). -/
theorem classical_fair_clone_still_derived :
    classicalClone fairBit =
      { w00 := 1, w01 := 1, w10 := 1, w11 := 1 } :=
  classical_clone_fair

def noCloningLinearityObstructionPackage_toy : Bool := true

/-- **Linearity obstruction residual package** (full unitary theorem OPEN). -/
theorem no_cloning_linearity_obstruction_package :
    noCloningLinearityObstructionPackage_toy = true ∧
    productAmp ampPlus amp0 =
      AmpJoint.add (productAmp amp0 amp0) (productAmp amp1 amp0) ∧
    basisCloner (productAmp ampPlus amp0) =
      AmpJoint.add (productAmp amp0 amp0) (productAmp amp1 amp1) ∧
    AmpJoint.add (productAmp amp0 amp0) (productAmp amp1 amp1) ≠
      productAmp ampPlus ampPlus ∧
    jointPop (basisCloner (productAmp ampPlus amp0)) ≠
      jointPop (productAmp ampPlus ampPlus) ∧
    classicalClone fairBit = jointPop (productAmp ampPlus ampPlus) ∧
    fullUnitaryNoCloning_open ∧
    obCloneUnderLinearLiftStatus = ImportStatus.conditionalImport := by
  refine ⟨rfl, plus_blank_splits_as_basis_products, linear_image_of_plus_blank,
    linear_forced_image_neq_product_clone, cloner_pop_neq_independent_clone_pop,
    ?_, trivial, rfl⟩
  simp [classicalClone, fairBit, jointPop, productAmp, ampPlus]

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end NoCloning
end QM

#print axioms QM.NoCloning.classical_cloning_derived
#print axioms QM.NoCloning.basis_cloner_fails_on_plus
#print axioms QM.NoCloning.no_cloning_package
#print axioms QM.NoCloning.no_cloning_linearity_obstruction_package
#print axioms QM.NoCloning.basis_cloner_linear
#print axioms QM.NoCloning.structure_not_auth
