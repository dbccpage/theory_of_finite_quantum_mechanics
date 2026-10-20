import Mathlib.Algebra.Group.Submonoid.Membership
import Mathlib.Data.Fintype.Card
import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.Combinatorics.Enumerative.Partition.Basic
import Mathlib.Tactic.Ring

/-! AuthorityEffect: None. Word reachability and finite closure in an arbitrary
group, projective coordinate normalization, and actual matrix conjugation for
the outer tensor pair. Rust refinement and allocator/bit costs are separate. -/
namespace TFQM.BraidTensorActions

variable {G : Type*} [Group G]

def run (x : G) : List G → G
  | [] => x
  | a::w => run (x*a) w

theorem run_append (x : G) (u v : List G) : run x (u++v)=run (run x u) v := by
  induction u generalizing x with
  | nil => rfl
  | cons a u ih => simp only [List.cons_append,run,ih]

theorem run_mul_left (a x : G) (w : List G) : run (a*x) w=a*run x w := by
  induction w generalizing x with
  | nil => rfl
  | cons b w ih => simpa only [run,mul_assoc] using ih (x*b)

def reachable (generators : Set G) (x : G) : Prop :=
  ∃ w : List G, (∀ a ∈ w, a ∈ generators) ∧ run 1 w=x

theorem reachable_one (generators : Set G) : reachable generators 1 := by
  exact ⟨[],by simp, rfl⟩

theorem reachable_step (generators : Set G) {x a : G}
    (hx : reachable generators x) (ha : a ∈ generators) : reachable generators (x*a) := by
  obtain ⟨w,hw,rfl⟩ := hx
  refine ⟨w++[a],?_,?_⟩
  · simpa only [List.mem_append,List.mem_singleton] using fun b h => h.elim (hw b) (fun h => h ▸ ha)
  · simp [run_append,run]

theorem reachable_mul (generators : Set G) {x y : G}
    (hx : reachable generators x) (hy : reachable generators y) : reachable generators (x*y) := by
  obtain ⟨u,hu,rfl⟩ := hx
  obtain ⟨v,hv,rfl⟩ := hy
  refine ⟨u++v,?_,?_⟩
  · simpa only [List.mem_append] using fun a h => h.elim (hu a) (hv a)
  · rw [run_append]
    simpa using run_mul_left (run 1 u) 1 v

theorem closed_run (generators S : Set G)
    (step : ∀ x ∈ S, ∀ a ∈ generators, x*a ∈ S)
    (x : G) (hx : x ∈ S) (w : List G) (hw : ∀ a ∈ w, a ∈ generators) : run x w ∈ S := by
  induction w generalizing x with
  | nil => exact hx
  | cons a w ih =>
      exact ih (fun b hb => hw b (List.mem_cons_of_mem a hb)) (x*a)
        (step x hx a (hw a (by simp)))

theorem closed_exploration_exact (generators S : Set G) (one : (1:G) ∈ S)
    (step : ∀ x ∈ S, ∀ a ∈ generators, x*a ∈ S)
    (sound : ∀ x ∈ S, reachable generators x) : S={x | reachable generators x} := by
  ext x
  constructor
  · exact sound x
  · rintro ⟨w,hw,rfl⟩
    exact closed_run generators S step 1 one w hw

theorem finite_inverse (S : Submonoid G) [Finite S] {x : G} (hx : x ∈ S) : x⁻¹ ∈ S := by
  let f : S → S := fun y => ⟨x*y,S.mul_mem hx y.property⟩
  have hi : Function.Injective f := by
    intro a b h
    apply Subtype.ext
    exact mul_left_cancel (congrArg Subtype.val h)
  obtain ⟨y,hy⟩ := Finite.surjective_of_injective hi (1:S)
  have h : x*(y:G)=1 := congrArg Subtype.val hy
  have he : (y:G)=x⁻¹ := by
    calc (y:G)=x⁻¹*(x*(y:G)) := by simp
         _=x⁻¹ := by rw [h,mul_one]
  exact he ▸ y.property

theorem frontier_step (next count : Nat) (h : next<count) : next+1≤count := by omega

theorem retained_and_scratch (states entries : Nat) :
    2*states*entries+2*entries=2*(states+1)*entries := by ring

variable {I K : Type*} [Field K]

def normal (v : I → K) (pivot : K) : I → K := fun i => v i / pivot

theorem normalize_reconstruct (v : I → K) (p : K) (hp : p≠0) (i : I) :
    normal v p i*p=v i := div_mul_cancel₀ (v i) hp

theorem normalize_pivot (v : I → K) (i : I) (p : K) (hp : p≠0) (h : v i=p) :
    normal v p i=1 := by simp [normal,h,hp]

theorem normalize_scale (v : I → K) (p t : K) (ht : t≠0) :
    normal (fun i => t*v i) (t*p)=normal v p := by
  ext i
  exact mul_div_mul_left (v i) p ht

abbrev Triple (I : Type*) := I × I × I
def flip23 (x : Triple I) : Triple I := (x.1,x.2.2,x.2.1)

theorem flip_involutive (x : Triple I) : flip23 (flip23 x)=x := by cases x; rfl

theorem flipped_eq (x y : Triple I) : x=flip23 y ↔ y=flip23 x := by
  constructor
  · intro h; rw [h,flip_involutive]
  · intro h; rw [h,flip_involutive]

variable [Fintype I] [DecidableEq I]
def flipMatrix : Matrix (Triple I) (Triple I) K := fun x y => if x=flip23 y then 1 else 0
def firstPair (r : Matrix (I×I) (I×I) K) : Matrix (Triple I) (Triple I) K :=
  fun x y => if x.2.2=y.2.2 then r (x.1,x.2.1) (y.1,y.2.1) else 0
def outerPair (r : Matrix (I×I) (I×I) K) : Matrix (Triple I) (Triple I) K :=
  fun x y => if x.2.1=y.2.1 then r (x.1,x.2.2) (y.1,y.2.2) else 0

theorem conjugation_apply (m : Matrix (Triple I) (Triple I) K) (x y : Triple I) :
    (flipMatrix*m*flipMatrix) x y=m (flip23 x) (flip23 y) := by
  simp [Matrix.mul_apply,flipMatrix,flipped_eq,mul_ite,ite_mul]

theorem outer_pair_conjugation (r : Matrix (I×I) (I×I) K) :
    flipMatrix*firstPair r*flipMatrix=outerPair r := by
  ext x y
  rw [conjugation_apply]
  rfl

end TFQM.BraidTensorActions

#print axioms TFQM.BraidTensorActions.run_append
#print axioms TFQM.BraidTensorActions.run_mul_left
#print axioms TFQM.BraidTensorActions.reachable_one
#print axioms TFQM.BraidTensorActions.reachable_step
#print axioms TFQM.BraidTensorActions.reachable_mul
#print axioms TFQM.BraidTensorActions.closed_run
#print axioms TFQM.BraidTensorActions.closed_exploration_exact
#print axioms TFQM.BraidTensorActions.finite_inverse
#print axioms TFQM.BraidTensorActions.frontier_step
#print axioms TFQM.BraidTensorActions.retained_and_scratch
#print axioms TFQM.BraidTensorActions.normalize_reconstruct
#print axioms TFQM.BraidTensorActions.normalize_pivot
#print axioms TFQM.BraidTensorActions.normalize_scale
#print axioms TFQM.BraidTensorActions.flip_involutive
#print axioms TFQM.BraidTensorActions.flipped_eq
#print axioms TFQM.BraidTensorActions.conjugation_apply
#print axioms TFQM.BraidTensorActions.outer_pair_conjugation
