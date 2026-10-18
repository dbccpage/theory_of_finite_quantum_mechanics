import Mathlib.Tactic

/-!
# Finite parity-context obstruction packet

This file is the reusable finite obstruction surface used by the Mermin-Peres
square certificate.  `Sign = Bool`, with `false` as +1 and `true` as -1, so
sign multiplication is xor and a product is a fold by xor.

The generic theorem is intentionally finite and certificate-shaped: if the
context-product closure is always +1, while the declared signs multiply to -1,
then the declared target sign vector is not in the image of the context-product
map `d0`.
-/

namespace QM
namespace ParityContext

abbrev Sign := Bool

def pos : Sign := false

def neg : Sign := true

def smul (a b : Sign) : Sign := Bool.xor a b

def sprod (xs : List Sign) : Sign := xs.foldl smul pos

theorem smul_assoc (a b c : Sign) :
    smul (smul a b) c = smul a (smul b c) := by
  cases a <;> cases b <;> cases c <;> rfl

theorem smul_comm (a b : Sign) : smul a b = smul b a := by
  cases a <;> cases b <;> rfl

theorem smul_self (a : Sign) : smul a a = pos := by
  cases a <;> rfl

theorem sprod_nil : sprod [] = pos := rfl

theorem sprod_singleton (a : Sign) : sprod [a] = a := by
  cases a <;> rfl

theorem sprod_pair_self (a : Sign) : sprod [a, a] = pos := by
  cases a <;> rfl

abbrev Assignment (Variable : Type) := Variable -> Sign

structure Packet (Variable Context : Type) where
  vars : List Variable
  contexts : List Context
  members : Context -> List Variable
  declaredSign : Context -> Sign

def contextProduct {Variable Context : Type}
    (P : Packet Variable Context) (a : Assignment Variable)
    (c : Context) : Sign :=
  sprod ((P.members c).map a)

def contextProducts {Variable Context : Type}
    (P : Packet Variable Context) (a : Assignment Variable) : List Sign :=
  P.contexts.map (fun c => contextProduct P a c)

def declaredProducts {Variable Context : Type}
    (P : Packet Variable Context) : List Sign :=
  P.contexts.map P.declaredSign

/-- The target sign vector is in the image of `d0` for this assignment. -/
def Satisfies {Variable Context : Type}
    (P : Packet Variable Context) (a : Assignment Variable) : Prop :=
  contextProducts P a = declaredProducts P

/--
Closure certificate for even incidence.  In concrete finite packets this is
proved by reduction over the signed variables: multiplying all context products
cancels duplicated variable occurrences and leaves +1.
-/
def EvenIncidenceClosure {Variable Context : Type}
    (P : Packet Variable Context) : Prop :=
  forall a : Assignment Variable, sprod (contextProducts P a) = pos

def DeclaredProductOdd {Variable Context : Type}
    (P : Packet Variable Context) : Prop :=
  sprod (declaredProducts P) = neg

def LocallySatisfiable {Variable Context : Type}
    (P : Packet Variable Context) : Prop :=
  forall c : Context, c ∈ P.contexts ->
    exists a : Assignment Variable, contextProduct P a c = P.declaredSign c

def GlobalObstructed {Variable Context : Type}
    (P : Packet Variable Context) : Prop :=
  Not (exists a : Assignment Variable, Satisfies P a)

def LocalGreenGlobalRed {Variable Context : Type}
    (P : Packet Variable Context) : Prop :=
  LocallySatisfiable P ∧ GlobalObstructed P

theorem even_incidence_forces_global_product_pos
    {Variable Context : Type} (P : Packet Variable Context)
    (h : EvenIncidenceClosure P) :
    forall a : Assignment Variable, sprod (contextProducts P a) = pos :=
  h

theorem odd_declared_sign_product_blocks_assignment
    {Variable Context : Type} (P : Packet Variable Context)
    (hClosure : EvenIncidenceClosure P)
    (hOdd : DeclaredProductOdd P) :
    GlobalObstructed P := by
  intro hSat
  rcases hSat with ⟨a, hImage⟩
  have hPositive : sprod (contextProducts P a) = pos := hClosure a
  rw [hImage, hOdd] at hPositive
  cases hPositive

end ParityContext
end QM

#print axioms QM.ParityContext.even_incidence_forces_global_product_pos
#print axioms QM.ParityContext.odd_declared_sign_product_blocks_assignment
