import CandidateGramPositivity
import TargetA4Gramian

/-!
# Target A5: Finite Partition and Cover Semantics in Lean 4

AuthorityEffect: None

This module formalizes Target A5 of the MUB(6) formalization program:
1. 5D Rational Interval Boxes and Point Membership:
   - Exact 5D rational interval boxes `RationalBox5` with lower bounds `u : Fin 5 → Rat`
     and upper bounds `v : Fin 5 → Rat`.
   - Validity predicate `RationalBox5.valid`: lower bounds do not exceed upper bounds.
   - Point membership: `in_box b x ↔ ∀ i : Fin 5, b.u i ≤ x i ∧ x i ≤ b.v i`.
   - Canonical embedding to `ParameterBox (Fin 5 → Rat)`.
2. Inductive Bisection Tree and Leaf Extraction:
   - `BisectionTree` inductive data structure representing recursive adaptive hyper-rectangle
     domain partitioning.
   - Leaf extraction `leaves : BisectionTree → List RationalBox5`.
3. Executable Boolean Partition Verification:
   - Executable boolean equality `eqBox` and `BEq RationalBox5` instance.
   - Child domain constructors `splitLeft` and `splitRight`.
   - Executable boolean verification function `checkPartitionCover : BisectionTree → RationalBox5 → Bool`.
   - Preservation lemmas: `in_box_splitLeft`, `in_box_splitRight`, `splitLeft_valid`, `splitRight_valid`.
4. Formal Soundness / Reflection Theorem:
   - `theorem checkPartitionCover_sound`:
     `checkPartitionCover tree domain = true → (∀ x, in_box domain x → ∃ B ∈ tree.leaves, in_box B x)`.
     Proven constructively by structural induction on `tree` with ZERO axioms outside standard Lean foundations.
5. Definitional Kernel Reflection:
   - Concrete 5D unit box `unitBox5 = [0, 1]^5`.
   - Concrete bisection tree `sampleBisectionTree` bisecting on dimension 0 and dimension 1 at 1/2.
   - Kernel reflection theorem:
     `theorem concrete_partition_cover_verified : checkPartitionCover sampleBisectionTree unitBox5 = true := by rfl`.
6. Global Cover Obstruction Theorems:
   - `global_cover_obstruction`: Abstract cover obstruction lifting per-cell obstruction to the entire domain.
   - `global_cover_sdp_obstruction`: Concrete integration with Target A4 SDP dual certificates W_B (D >= 0)
     with strictly negative trace Tr(W_B · G(q)) < 0 across each leaf box B.
   - `global_cover_non_extendibility`: Certifies non-extendibility of candidate configurations across the domain.
   - `global_cover_realizes_gram_family_obstruction`: Parameterized candidate vector families cannot realize
     the Gram family on the aggregated domain.
7. Axiom Audit:
   - Verification that all theorems depend solely on standard foundational axioms `[propext, Classical.choice, Quot.sound]`.
-/

namespace MUB6.Gluing.TargetA5

open MUB6.Gluing
open MUB6.Gluing.CandidateGram
open MUB6.Gluing.TargetA4

/-!
### 1. 5D Rational Interval Boxes and Point Membership
-/

/-- A 5-dimensional rational interval box B = ∏_{j=0}^4 [u_j, v_j] ⊂ ℚ^5
parameterized by coordinate lower bounds `u` and upper bounds `v`. -/
structure RationalBox5 where
  u : Fin 5 → Rat
  v : Fin 5 → Rat

/-- Mathematical validity predicate: for every dimension `i ∈ Fin 5`,
the lower bound does not exceed the upper bound (`u i ≤ v i`). -/
def RationalBox5.valid (b : RationalBox5) : Prop :=
  ∀ i : Fin 5, b.u i ≤ b.v i

/-- Point membership predicate: a rational parameter vector `x : Fin 5 → Rat`
lies in box `b` if and only if `b.u i ≤ x i ≤ b.v i` for all `i ∈ Fin 5`. -/
def in_box (b : RationalBox5) (x : Fin 5 → Rat) : Prop :=
  ∀ i : Fin 5, b.u i ≤ x i ∧ x i ≤ b.v i

/-- Canonical embedding of a `RationalBox5` into a generic `ParameterBox (Fin 5 → Rat)`. -/
def box5ToParameterBox (b : RationalBox5) : ParameterBox (Fin 5 → Rat) :=
  ⟨fun x => in_box b x⟩

/-!
### 2. Inductive Bisection Tree and Leaf Extraction
-/

/-- Inductive bisection tree representing hierarchical subdivision of a parameter domain:
- `leaf b`: a terminal cell labeled by rational box `b`;
- `split dim cut left right`: an internal node splitting coordinate `dim` at rational threshold `cut`,
  with subtrees `left` and `right`. -/
inductive BisectionTree where
  | leaf (b : RationalBox5) : BisectionTree
  | split (dim : Fin 5) (cut : Rat) (left right : BisectionTree) : BisectionTree

/-- Extracts the list of terminal leaf boxes from a bisection tree. -/
def BisectionTree.leaves : BisectionTree → List RationalBox5
  | .leaf b => [b]
  | .split _ _ left right => leaves left ++ leaves right

export BisectionTree (leaves)

/-!
### 3. Executable Boolean Box Equality and Partition Cover Verification
-/

/-- Exact boolean equality for 5D rational interval boxes.
Checks coordinate-wise equality of all lower and upper bounds. -/
def eqBox (b1 b2 : RationalBox5) : Bool :=
  (b1.u 0 == b2.u 0) && (b1.v 0 == b2.v 0) &&
  (b1.u 1 == b2.u 1) && (b1.v 1 == b2.v 1) &&
  (b1.u 2 == b2.u 2) && (b1.v 2 == b2.v 2) &&
  (b1.u 3 == b2.u 3) && (b1.v 3 == b2.v 3) &&
  (b1.u 4 == b2.u 4) && (b1.v 4 == b2.v 4)

instance : BEq RationalBox5 where
  beq := eqBox

/-- Left child box formed by updating the upper bound at dimension `dim` to `cut`. -/
def splitLeft (domain : RationalBox5) (dim : Fin 5) (cut : Rat) : RationalBox5 :=
  { u := domain.u, v := fun i => if i = dim then cut else domain.v i }

/-- Right child box formed by updating the lower bound at dimension `dim` to `cut`. -/
def splitRight (domain : RationalBox5) (dim : Fin 5) (cut : Rat) : RationalBox5 :=
  { u := fun i => if i = dim then cut else domain.u i, v := domain.v }

/-- Executable boolean verification function for bisection cover validity:
- At a `leaf b domain`: checks `b == domain` (exact equality of interval bounds).
- At a `split dim cut left right domain`:
  1. Checks `domain.u dim < cut` and `cut < domain.v dim` (strictly interior cut);
  2. Recursively verifies that `left` covers `splitLeft domain dim cut`;
  3. Recursively verifies that `right` covers `splitRight domain dim cut`. -/
def checkPartitionCover : BisectionTree → RationalBox5 → Bool
  | .leaf b, domain => b == domain
  | .split dim cut left right, domain =>
    (domain.u dim).blt cut &&
    cut.blt (domain.v dim) &&
    checkPartitionCover left (splitLeft domain dim cut) &&
    checkPartitionCover right (splitRight domain dim cut)

/-- Elimination helper for boolean conjunction. -/
theorem bool_and_elim {a b : Bool} (h : (a && b) = true) : a = true ∧ b = true := by
  cases a <;> cases b <;> simp at h ⊢

/-- **Soundness of Box Equality**:
If `(b1 == b2) = true`, then lower and upper bounds coincide on all dimensions `i ∈ Fin 5`. -/
theorem eqBox_sound {b1 b2 : RationalBox5} (h : (b1 == b2) = true) (i : Fin 5) :
    b1.u i = b2.u i ∧ b1.v i = b2.v i := by
  change eqBox b1 b2 = true at h
  dsimp [eqBox] at h
  have h10 := bool_and_elim h
  have h9 := bool_and_elim h10.1
  have h8 := bool_and_elim h9.1
  have h7 := bool_and_elim h8.1
  have h6 := bool_and_elim h7.1
  have h5 := bool_and_elim h6.1
  have h4 := bool_and_elim h5.1
  have h3 := bool_and_elim h4.1
  have h2 := bool_and_elim h3.1
  have eq_u0 : b1.u 0 = b2.u 0 := beq_iff_eq.mp h2.1
  have eq_v0 : b1.v 0 = b2.v 0 := beq_iff_eq.mp h2.2
  have eq_u1 : b1.u 1 = b2.u 1 := beq_iff_eq.mp h3.2
  have eq_v1 : b1.v 1 = b2.v 1 := beq_iff_eq.mp h4.2
  have eq_u2 : b1.u 2 = b2.u 2 := beq_iff_eq.mp h5.2
  have eq_v2 : b1.v 2 = b2.v 2 := beq_iff_eq.mp h6.2
  have eq_u3 : b1.u 3 = b2.u 3 := beq_iff_eq.mp h7.2
  have eq_v3 : b1.v 3 = b2.v 3 := beq_iff_eq.mp h8.2
  have eq_u4 : b1.u 4 = b2.u 4 := beq_iff_eq.mp h9.2
  have eq_v4 : b1.v 4 = b2.v 4 := beq_iff_eq.mp h10.2
  rcases i with ⟨ival, hi⟩
  have hcases : ival = 0 ∨ ival = 1 ∨ ival = 2 ∨ ival = 3 ∨ ival = 4 := by omega
  rcases hcases with h0 | h1 | h2 | h3 | h4
  · have hi0 : (⟨ival, hi⟩ : Fin 5) = 0 := by ext; exact h0
    rw [hi0]; exact ⟨eq_u0, eq_v0⟩
  · have hi1 : (⟨ival, hi⟩ : Fin 5) = 1 := by ext; exact h1
    rw [hi1]; exact ⟨eq_u1, eq_v1⟩
  · have hi2 : (⟨ival, hi⟩ : Fin 5) = 2 := by ext; exact h2
    rw [hi2]; exact ⟨eq_u2, eq_v2⟩
  · have hi3 : (⟨ival, hi⟩ : Fin 5) = 3 := by ext; exact h3
    rw [hi3]; exact ⟨eq_u3, eq_v3⟩
  · have hi4 : (⟨ival, hi⟩ : Fin 5) = 4 := by ext; exact h4
    rw [hi4]; exact ⟨eq_u4, eq_v4⟩

/-- Point membership in left child box when coordinate satisfies `x dim ≤ cut`. -/
theorem in_box_splitLeft (domain : RationalBox5) (dim : Fin 5) (cut : Rat)
    (x : Fin 5 → Rat) (hx : in_box domain x) (hcut : x dim ≤ cut) :
    in_box (splitLeft domain dim cut) x := by
  intro i
  dsimp [splitLeft]
  split
  · rename_i h_eq
    subst h_eq
    exact ⟨(hx i).1, hcut⟩
  · exact hx i

/-- Point membership in right child box when coordinate satisfies `cut ≤ x dim`. -/
theorem in_box_splitRight (domain : RationalBox5) (dim : Fin 5) (cut : Rat)
    (x : Fin 5 → Rat) (hx : in_box domain x) (hcut : cut ≤ x dim) :
    in_box (splitRight domain dim cut) x := by
  intro i
  dsimp [splitRight]
  split
  · rename_i h_eq
    subst h_eq
    exact ⟨hcut, (hx i).2⟩
  · exact hx i

/-- Validity preservation for left child box. -/
theorem splitLeft_valid (domain : RationalBox5) (dim : Fin 5) (cut : Rat)
    (h_valid : domain.valid) (h_cut : domain.u dim ≤ cut) :
    (splitLeft domain dim cut).valid := by
  intro i
  dsimp [splitLeft]
  split
  · rename_i h_eq
    subst h_eq
    exact h_cut
  · exact h_valid i

/-- Validity preservation for right child box. -/
theorem splitRight_valid (domain : RationalBox5) (dim : Fin 5) (cut : Rat)
    (h_valid : domain.valid) (h_cut : cut ≤ domain.v dim) :
    (splitRight domain dim cut).valid := by
  intro i
  dsimp [splitRight]
  split
  · rename_i h_eq
    subst h_eq
    exact h_cut
  · exact h_valid i

/-!
### 4. Formal Soundness / Reflection Theorem
-/

/-- **THE PARTITION COVER SOUNDNESS THEOREM**:
If `checkPartitionCover tree domain = true`, then for any point `x : Fin 5 → Rat`
in `domain`, there exists a leaf box `B ∈ tree.leaves` containing `x`.

Proven constructively by structural induction on `tree`:
- Base case (`leaf b`): `eqBox` soundly forces interval equality `b = domain`.
- Inductive step (`split dim cut left right`): By rational linearity `Rat.le_total`,
  either `x dim ≤ cut` (landing in `splitLeft`, covered by `ih_left`)
  or `cut ≤ x dim` (landing in `splitRight`, covered by `ih_right`).
Zero sorry. -/
theorem checkPartitionCover_sound (tree : BisectionTree) (domain : RationalBox5) :
    checkPartitionCover tree domain = true →
    (∀ x : Fin 5 → Rat, in_box domain x → ∃ B ∈ tree.leaves, in_box B x) := by
  induction tree generalizing domain with
  | leaf b =>
    intro h_check x hx
    dsimp [checkPartitionCover] at h_check
    dsimp [BisectionTree.leaves]
    refine ⟨b, List.Mem.head _, ?_⟩
    intro i
    have h_eq := eqBox_sound h_check i
    have hxi := hx i
    rw [h_eq.1, h_eq.2]
    exact hxi
  | split dim cut left right ih_left ih_right =>
    intro h_check x hx
    dsimp [checkPartitionCover] at h_check
    have h4 := bool_and_elim h_check
    have h3 := bool_and_elim h4.1
    have h2 := bool_and_elim h3.1
    have h_check_left := h3.2
    have h_check_right := h4.2
    dsimp [BisectionTree.leaves]
    cases Rat.le_total (a := x dim) (b := cut) with
    | inl h_le =>
      have hx_left := in_box_splitLeft domain dim cut x hx h_le
      have ⟨B, hB_mem, hB_box⟩ := ih_left (splitLeft domain dim cut) h_check_left x hx_left
      refine ⟨B, List.mem_append.mpr (Or.inl hB_mem), hB_box⟩
    | inr h_ge =>
      have hx_right := in_box_splitRight domain dim cut x hx h_ge
      have ⟨B, hB_mem, hB_box⟩ := ih_right (splitRight domain dim cut) h_check_right x hx_right
      refine ⟨B, List.mem_append.mpr (Or.inr hB_mem), hB_box⟩

/-!
### 5. Definitional Kernel Reflection on Concrete Partition
-/

/-- Non-zero proof for denominator 1 (axiom-free). -/
theorem nz1 : 1 ≠ 0 := by intro h; cases h

/-- Coprime proof for 0 / 1 (axiom-free). -/
theorem red0 : (Int.ofNat 0).natAbs.Coprime 1 := rfl

/-- Coprime proof for 1 / 1 (axiom-free). -/
theorem red1 : (Int.ofNat 1).natAbs.Coprime 1 := rfl

/-- Non-zero proof for denominator 2 (axiom-free). -/
theorem nz2 : 2 ≠ 0 := by intro h; cases h

/-- Coprime proof for 1 / 2 (axiom-free). -/
theorem redHalf : (Int.ofNat 1).natAbs.Coprime 2 := rfl

/-- Exact rational 0 constructed definitionally without non-constructive axioms. -/
def qZero : Rat := Rat.mk' 0 1 nz1 red0

/-- Exact rational 1 constructed definitionally without non-constructive axioms. -/
def qOne : Rat := Rat.mk' 1 1 nz1 red1

/-- Exact rational 1/2 constructed definitionally without non-constructive axioms. -/
def qHalf : Rat := Rat.mk' 1 2 nz2 redHalf

/-- The canonical 5D unit box [0, 1]^5 in ℚ^5. -/
def unitBox5 : RationalBox5 :=
  { u := fun _ => qZero, v := fun _ => qOne }

/-- Verification of mathematical validity for `unitBox5`. -/
theorem unitBox5_valid : unitBox5.valid := by
  intro i
  change qOne.blt qZero = false
  rfl

/-- Concrete 4-cell partition of `unitBox5`:
Dimension 0 is split at 1/2, and each child domain is split on dimension 1 at 1/2. -/
def boxLL : RationalBox5 := splitLeft (splitLeft unitBox5 0 qHalf) 1 qHalf
def boxLR : RationalBox5 := splitRight (splitLeft unitBox5 0 qHalf) 1 qHalf
def boxRL : RationalBox5 := splitLeft (splitRight unitBox5 0 qHalf) 1 qHalf
def boxRR : RationalBox5 := splitRight (splitRight unitBox5 0 qHalf) 1 qHalf

/-- Concrete bisection tree representing the 4-cell partition of `unitBox5`. -/
def sampleBisectionTree : BisectionTree :=
  .split 0 qHalf
    (.split 1 qHalf (.leaf boxLL) (.leaf boxLR))
    (.split 1 qHalf (.leaf boxRL) (.leaf boxRR))

/-- **Definitional Kernel Reflection Theorem**:
The Lean 4 kernel definitionally certifies that `sampleBisectionTree` is a valid
partition cover of `unitBox5` via `rfl`. -/
theorem concrete_partition_cover_verified :
    checkPartitionCover sampleBisectionTree unitBox5 = true := by
  rfl

/-!
### 6. Global Cover Obstruction Theorems
-/

/-- **Global Cover Obstruction (General Realization Predicate)**:
If a bisection tree certifies a partition cover of `domain`, and every leaf box `B ∈ tree.leaves`
is certified obstructed for a realization predicate `Realization`, then no realization exists for
any parameter `p` in the aggregated domain. -/
theorem global_cover_obstruction
    (tree : BisectionTree) (domain : RationalBox5)
    (h_cover : checkPartitionCover tree domain = true)
    (Realization : (Fin 5 → Rat) → Prop)
    (h_leaf_obstructed : ∀ B ∈ tree.leaves, ∀ p, in_box B p → ¬ Realization p)
    (p : Fin 5 → Rat) (hp : in_box domain p) :
    ¬ Realization p := by
  intro h_real
  have ⟨B, hB_mem, hB_box⟩ := checkPartitionCover_sound tree domain h_cover p hp
  have h_obst := h_leaf_obstructed B hB_mem p hB_box
  exact h_obst h_real

/-- **Global Cover Obstruction for Quadruple Candidate Realizations (Target A4 SDP)**:
If each leaf box `B ∈ tree.leaves` has a certified SDP dual witness `W_B` whose trace evaluation
is strictly negative across `B`, then no candidate quadruple realization `Q` in `PreHilbertSpace V`
can realize `G(p)` for any parameter `p` in the aggregated `domain`. -/
theorem global_cover_sdp_obstruction
    {V : Type} (H : PreHilbertSpace V)
    (tree : BisectionTree) (domain : RationalBox5)
    (h_cover : checkPartitionCover tree domain = true)
    (G : QuadGramFamily (Fin 5 → Rat))
    (eval_trace : {m : Nat} → QuadDualWitness m → (Fin 24 → Fin 24 → Rat) → Rat)
    (h_eval_eq : ∀ {m : Nat} (W : QuadDualWitness m) (v : Fin 24 → V),
      eval_trace W (gramMatrix H v) = traceInnerFactored W H v)
    (h_leaf_witness : ∀ B ∈ tree.leaves,
      ∃ (m : Nat) (W : QuadDualWitness m), ∀ q, in_box B q → eval_trace W (G q) < 0)
    (p : Fin 5 → Rat) (hp : in_box domain p) :
    ¬ ∃ (Q : QuadCandidateSystem V H), quadGramianRat H Q = G p := by
  apply global_cover_obstruction tree domain h_cover (fun p => ∃ Q : QuadCandidateSystem V H, quadGramianRat H Q = G p)
  · intro B hB q hq ⟨Q, hQ⟩
    rcases h_leaf_witness B hB with ⟨m, W, hW_neg⟩
    have h_obst := quad_regional_dual_obstruction H W G (eval_trace W) (h_eval_eq W) (box5ToParameterBox B) hW_neg q hq
    exact h_obst ⟨Q, hQ⟩
  · exact hp

/-- **Global Non-Extendibility of Candidate Quadruple across Aggregated Domain**:
Under certified per-cell SDP dual certificates across the bisection cover,
no quadruple candidate system exists that realizes `G(p)` for any parameter in `domain`. -/
theorem global_cover_non_extendibility
    {V : Type} (H : PreHilbertSpace V)
    (tree : BisectionTree) (domain : RationalBox5)
    (h_cover : checkPartitionCover tree domain = true)
    (G : QuadGramFamily (Fin 5 → Rat))
    (eval_trace : {m : Nat} → QuadDualWitness m → (Fin 24 → Fin 24 → Rat) → Rat)
    (h_eval_eq : ∀ {m : Nat} (W : QuadDualWitness m) (v : Fin 24 → V),
      eval_trace W (gramMatrix H v) = traceInnerFactored W H v)
    (h_leaf_witness : ∀ B ∈ tree.leaves,
      ∃ (m : Nat) (W : QuadDualWitness m), ∀ q, in_box B q → eval_trace W (G q) < 0)
    (p : Fin 5 → Rat) (hp : in_box domain p) :
    ∀ (Q : QuadCandidateSystem V H), quadGramianRat H Q = G p → False := by
  intro Q hQ
  have h_obst := global_cover_sdp_obstruction H tree domain h_cover G eval_trace h_eval_eq h_leaf_witness p hp
  exact h_obst ⟨Q, hQ⟩

/-- **Global Realization Obstruction for Parameterized Vector Families**:
A parameterized candidate vector family `v : QuadVectorFamily (Fin 5 → Rat) V` cannot realize
the Gram family `G` on the aggregated `domain`. -/
theorem global_cover_realizes_gram_family_obstruction
    {V : Type} (H : PreHilbertSpace V)
    (tree : BisectionTree) (domain : RationalBox5)
    (h_cover : checkPartitionCover tree domain = true)
    (G : QuadGramFamily (Fin 5 → Rat))
    (eval_trace : {m : Nat} → QuadDualWitness m → (Fin 24 → Fin 24 → Rat) → Rat)
    (h_eval_eq : ∀ {m : Nat} (W : QuadDualWitness m) (v : Fin 24 → V),
      eval_trace W (gramMatrix H v) = traceInnerFactored W H v)
    (h_leaf_witness : ∀ B ∈ tree.leaves,
      ∃ (m : Nat) (W : QuadDualWitness m), ∀ q, in_box B q → eval_trace W (G q) < 0)
    (p : Fin 5 → Rat) (hp : in_box domain p)
    (v : QuadVectorFamily (Fin 5 → Rat) V) :
    RealizesGramFamily H (box5ToParameterBox domain) G v → False := by
  intro h_real
  have hp_box : (box5ToParameterBox domain).in_box p := hp
  have hv := h_real p hp_box
  have ⟨B, hB_mem, hB_box⟩ := checkPartitionCover_sound tree domain h_cover p hp
  rcases h_leaf_witness B hB_mem with ⟨m, W, hW_neg⟩
  have h_sdp := regional_dual_obstruction H W G (eval_trace W) (h_eval_eq W) (box5ToParameterBox B) hW_neg p hB_box
  exact h_sdp ⟨v p, hv⟩

/-!
### 7. Axiom Audits
-/

#print axioms bool_and_elim
#print axioms eqBox_sound
#print axioms in_box_splitLeft
#print axioms in_box_splitRight
#print axioms splitLeft_valid
#print axioms splitRight_valid
#print axioms checkPartitionCover_sound
#print axioms nz1
#print axioms red0
#print axioms red1
#print axioms nz2
#print axioms redHalf
#print axioms unitBox5_valid
#print axioms concrete_partition_cover_verified
#print axioms global_cover_obstruction
#print axioms global_cover_sdp_obstruction
#print axioms global_cover_non_extendibility
#print axioms global_cover_realizes_gram_family_obstruction

end MUB6.Gluing.TargetA5
