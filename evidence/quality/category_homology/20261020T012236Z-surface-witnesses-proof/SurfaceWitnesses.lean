import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Combinatorics.Enumerative.Partition.Basic

/-! AuthorityEffect: None. Fixed report assembly, exact scalar comparison,
ordered error propagation and independent small arithmetic/list witnesses.
Seven separately reviewed providers discharge the mathematical computations.
This model does not turn a publicly mutable report into an admission token. -/
namespace TFQM.SurfaceWitnesses

structure Report where
  partition : Nat
  factorial : Nat
  mub : Nat
  fano : Nat
  affine : Nat
  deriving DecidableEq

def join (p f m g a : Except String Nat) : Except String Report := do
  let p ← p
  let f ← f
  let m ← m
  let g ← g
  let a ← a
  pure ⟨p,f,m,g,a⟩

theorem assemble_exact (p f m g a : Nat) :
    join (.ok p) (.ok f) (.ok m) (.ok g) (.ok a)=.ok ⟨p,f,m,g,a⟩ := rfl

theorem first_error (e : String) (f m g a : Except String Nat) :
    join (.error e) f m g a=.error e := rfl

theorem factorial_error (p : Nat) (e : String) (m g a : Except String Nat) :
    join (.ok p) (.error e) m g a=.error e := rfl

theorem mub_error (p f : Nat) (e : String) (g a : Except String Nat) :
    join (.ok p) (.ok f) (.error e) g a=.error e := rfl

theorem fano_error (p f m : Nat) (e : String) (a : Except String Nat) :
    join (.ok p) (.ok f) (.ok m) (.error e) a=.error e := rfl

theorem affine_error (p f m g : Nat) (e : String) :
    join (.ok p) (.ok f) (.ok m) (.ok g) (.error e)=.error e := rfl

def checkPartition (w : Nat) : Except String Unit :=
  if w=5 then .ok () else .error "p(4)=5"

theorem partition_acceptance (w : Nat) : checkPartition w=.ok () ↔ w=5 := by
  unfold checkPartition
  split_ifs <;> simp_all

theorem partition_refusal (w : Nat) (h : w≠5) : checkPartition w=.error "p(4)=5" := by
  simp [checkPartition,h]

def fourRows : List (List Nat) := [[4],[3,1],[2,2],[2,1,1],[1,1,1,1]]

theorem listed_partition_count : fourRows.length=5 := rfl

theorem listed_partition_invariants : ∀ row ∈ fourRows,
    row.sum=4 ∧ row.Pairwise (fun x y => y≤x) ∧ ∀ x ∈ row, 0<x := by decide

theorem fixed_factorial : Nat.factorial 5=120 := by decide
theorem prime_bundle_count : 5+1=6 := rfl
theorem fano_pair_count : (7*6)/(3*2)=7 := rfl
theorem affine_pair_count : (3*3*(3*3-1))/(3*(3-1))=12 := rfl

theorem fixed_report : join (.ok 5) (.ok 120) (.ok 6) (.ok 7) (.ok 12)=
    .ok ⟨5,120,6,7,12⟩ := rfl

#print axioms assemble_exact
#print axioms first_error
#print axioms factorial_error
#print axioms mub_error
#print axioms fano_error
#print axioms affine_error
#print axioms partition_acceptance
#print axioms partition_refusal
#print axioms listed_partition_count
#print axioms listed_partition_invariants
#print axioms fixed_factorial
#print axioms prime_bundle_count
#print axioms fano_pair_count
#print axioms affine_pair_count
#print axioms fixed_report
end TFQM.SurfaceWitnesses
