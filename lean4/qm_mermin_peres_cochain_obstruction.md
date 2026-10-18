import «qm_parity_context_obstruction»

/-!
# Mermin-Peres square as a finite parity cochain obstruction

This is the concrete QM_047 finite witness.  The Mermin-Peres square is encoded
as a parity-context packet: nine Boolean signs, six row/column contexts, five
declared +1 products, and one declared -1 product.  Every variable occurs twice,
so every assignment has total left context product +1, while the declared target
sign vector multiplies to -1.  Hence no global noncontextual assignment exists.

Scope: this is a known contextuality proof translated into the Omega finite
PrimitiveDifference/cochain/LGGR vocabulary.  It does not derive quantum
mechanics, Hilbert space, measurement, or authority.
-/

namespace QM
namespace MerminPeres

open ParityContext

inductive Variable where
  | a11 | a12 | a13
  | a21 | a22 | a23
  | a31 | a32 | a33
deriving DecidableEq, Repr

inductive Context where
  | r1 | r2 | r3
  | c1 | c2 | c3
deriving DecidableEq, Repr

open Variable
open Context

def allVariables : List Variable :=
  [a11, a12, a13, a21, a22, a23, a31, a32, a33]

def contexts : List Context :=
  [r1, r2, r3, c1, c2, c3]

def members : Context -> List Variable
  | r1 => [a11, a12, a13]
  | r2 => [a21, a22, a23]
  | r3 => [a31, a32, a33]
  | c1 => [a11, a21, a31]
  | c2 => [a12, a22, a32]
  | c3 => [a13, a23, a33]

def declaredSign : Context -> Sign
  | r1 => pos
  | r2 => pos
  | r3 => pos
  | c1 => pos
  | c2 => pos
  | c3 => neg

def packet : Packet Variable Context where
  vars := allVariables
  contexts := contexts
  members := members
  declaredSign := declaredSign

def allPositiveAssignment : Assignment Variable := fun _ => pos

def onlyA13Neg : Assignment Variable
  | a11 => pos
  | a12 => pos
  | a13 => neg
  | a21 => pos
  | a22 => pos
  | a23 => pos
  | a31 => pos
  | a32 => pos
  | a33 => pos

def onlyA23Neg : Assignment Variable
  | a11 => pos
  | a12 => pos
  | a13 => pos
  | a21 => pos
  | a22 => pos
  | a23 => neg
  | a31 => pos
  | a32 => pos
  | a33 => pos

def onlyA33Neg : Assignment Variable
  | a11 => pos
  | a12 => pos
  | a13 => pos
  | a21 => pos
  | a22 => pos
  | a23 => pos
  | a31 => pos
  | a32 => pos
  | a33 => neg

def a11A13Neg : Assignment Variable
  | a11 => neg
  | a12 => pos
  | a13 => neg
  | a21 => pos
  | a22 => pos
  | a23 => pos
  | a31 => pos
  | a32 => pos
  | a33 => pos

def a12A13Neg : Assignment Variable
  | a11 => pos
  | a12 => neg
  | a13 => neg
  | a21 => pos
  | a22 => pos
  | a23 => pos
  | a31 => pos
  | a32 => pos
  | a33 => pos

def witnessForContext : Context -> Assignment Variable
  | r1 => allPositiveAssignment
  | r2 => allPositiveAssignment
  | r3 => allPositiveAssignment
  | c1 => allPositiveAssignment
  | c2 => allPositiveAssignment
  | c3 =>
      onlyA13Neg

theorem local_context_witness (ctx : Context) :
    contextProduct packet (witnessForContext ctx) ctx =
      packet.declaredSign ctx := by
  cases ctx <;> rfl

theorem local_contexts_individually_satisfiable :
    LocallySatisfiable packet := by
  intro ctx _hMem
  exact ⟨witnessForContext ctx, local_context_witness ctx⟩

theorem left_global_product_for_any_assignment (a : Assignment Variable) :
    sprod (contextProducts packet a) = pos := by
  change
    sprod
      [sprod [a a11, a a12, a a13],
       sprod [a a21, a a22, a a23],
       sprod [a a31, a a32, a a33],
       sprod [a a11, a a21, a a31],
       sprod [a a12, a a22, a a32],
       sprod [a a13, a a23, a a33]] = pos
  cases a a11 <;>
  cases a a12 <;>
  cases a a13 <;>
  cases a a21 <;>
  cases a a22 <;>
  cases a a23 <;>
  cases a a31 <;>
  cases a a32 <;>
  cases a a33 <;>
  rfl

theorem mermin_peres_even_incidence_closure :
    EvenIncidenceClosure packet := by
  intro a
  exact left_global_product_for_any_assignment a

theorem declared_sign_product_neg :
    DeclaredProductOdd packet := by
  rfl

theorem mermin_peres_no_global_assignment :
    GlobalObstructed packet :=
  odd_declared_sign_product_blocks_assignment packet
    mermin_peres_even_incidence_closure
    declared_sign_product_neg

theorem local_green_global_red :
    LocalGreenGlobalRed packet := by
  exact ⟨local_contexts_individually_satisfiable,
    mermin_peres_no_global_assignment⟩

def SatisfiesExcept (dropCtx : Context) (a : Assignment Variable) : Prop :=
  forall ctx : Context, ctx ≠ dropCtx ->
    contextProduct packet a ctx = declaredSign ctx

def witnessExcept : Context -> Assignment Variable
  | r1 => onlyA13Neg
  | r2 => onlyA23Neg
  | r3 => onlyA33Neg
  | c1 => a11A13Neg
  | c2 => a12A13Neg
  | c3 => allPositiveAssignment

theorem every_five_context_subset_satisfiable (dropCtx : Context) :
    exists a : Assignment Variable, SatisfiesExcept dropCtx a := by
  refine ⟨witnessExcept dropCtx, ?_⟩
  intro ctx hCtx
  cases dropCtx <;> cases ctx <;>
    first | exact (hCtx rfl).elim | rfl

end MerminPeres
end QM

#print axioms QM.MerminPeres.left_global_product_for_any_assignment
#print axioms QM.MerminPeres.local_contexts_individually_satisfiable
#print axioms QM.MerminPeres.mermin_peres_no_global_assignment
#print axioms QM.MerminPeres.local_green_global_red
#print axioms QM.MerminPeres.every_five_context_subset_satisfiable
