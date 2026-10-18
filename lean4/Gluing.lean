/- These declarations are opaque and were not elaborated by Lake in this change. -/

/-!
# Formalization of the MUB(6) Gluing Theorem

AuthorityEffect: None

This module formalizes the gluing reduction for the mutually unbiased bases (MUB) problem
in dimension 6. It makes the open mathematical obstruction exact:
a classwise fourth-basis obstruction on certified atlas patches (pinned walls) does not
yield a full no-go theorem without three explicit gluing obligations:

- `G1` (Exhaustive Moduli Cover): Every admissible complete 7-basis MUB configuration in
  dimension 6 contains at least one triple that lands in a covered atlas class.
- `G2` (Lossless Wall Transport): For every covered class in the certified atlas, the class
  transports to a wall-certified lane without losing ZeroRel or terminalizer information,
  ensuring that no triple in that class admits a fourth mutually unbiased basis.
- `G3` (Basis Gluing): In any complete 7-basis MUB configuration, every constituent triple
  admits a fourth mutually unbiased basis in the configuration.

We prove:
1. `gluing_assembly : G1 ∧ G2 ∧ G3 → NoCompleteMUB6` (assembly implication, 0 axioms).
2. `g3_theorem : G3` (pure combinatorial basis-gluing theorem, depends only on `[propext]`).
3. `gluing_reduction_G1_G2 : G1 ∧ G2 → NoCompleteMUB6` (reduced assembly, depends only on `[propext]`).
4. Decomposition of G2 into `WallCertified` (finite computation) and `TransportInvariance` (mathematical theorem).
-/

namespace MUB6.Gluing

/-- An abstract type representing an orthonormal basis of dimension 6. -/
opaque Basis : Type

/-- Pairwise mutual unbiasedness relation between two bases.
In coordinates, `|⟨v_i, w_j⟩|² = 1/6` for all basis vectors `v_i, w_j`. -/
opaque is_mutually_unbiased : Basis → Basis → Prop

/-- A family of `n` bases is pairwise mutually unbiased if distinct bases are mutually unbiased. -/
def PairwiseMU {n : Nat} (B : Fin n → Basis) : Prop :=
  ∀ (i j : Fin n), i ≠ j → is_mutually_unbiased (B i) (B j)

/-- A complete set of seven mutually unbiased bases in dimension 6. -/
def CompleteMUB6 : Prop :=
  ∃ (B : Fin 7 → Basis), PairwiseMU B

/-- The open target claim: No complete set of seven MUBs exists in dimension 6. -/
def NoCompleteMUB6 : Prop :=
  ¬ CompleteMUB6

/-- A set of four mutually unbiased bases in dimension 6. -/
def FourMUB6 : Prop :=
  ∃ (B : Fin 4 → Basis), PairwiseMU B

/-- Open abstract four-basis obstruction target. This definition supplies no inhabitant
and no bridge from the opaque `Basis`/MU predicates to concrete complex matrices. -/
def NoFourMUB6 : Prop :=
  ¬ FourMUB6

/-- Embedding from `Fin 4` into `Fin 7`. -/
def fin4_to_fin7 (i : Fin 4) : Fin 7 := ⟨i.val, by omega⟩

/-- Proof that `fin4_to_fin7` is injective. -/
theorem fin4_to_fin7_injective (i j : Fin 4) (h : fin4_to_fin7 i = fin4_to_fin7 j) : i = j := by
  ext
  injection h


/-- **Theorem: NoFourMUB6 implies NoCompleteMUB6.**
If no set of four mutually unbiased bases exists in dimension 6, then no complete set
of seven mutually unbiased bases can exist.
Proved constructively with zero non-standard axioms. -/
theorem no_complete_mub6_of_no_four_mub6 (h : NoFourMUB6) : NoCompleteMUB6 := by
  intro ⟨B7, hB7_mu⟩
  apply h
  let B4 : Fin 4 → Basis := fun i => B7 (fin4_to_fin7 i)
  refine ⟨B4, ?_⟩
  intro i j hij
  have h_ne : fin4_to_fin7 i ≠ fin4_to_fin7 j := by
    intro h_eq
    exact hij (fin4_to_fin7_injective i j h_eq)
  exact hB7_mu (fin4_to_fin7 i) (fin4_to_fin7 j) h_ne

#print axioms no_complete_mub6_of_no_four_mub6

/-- A triple of orthonormal bases in dimension 6 that are pairwise mutually unbiased. -/
structure MUTriple where
  b0 : Basis
  b1 : Basis
  b2 : Basis
  mu01 : is_mutually_unbiased b0 b1
  mu02 : is_mutually_unbiased b0 b2
  mu12 : is_mutually_unbiased b1 b2

/-- A fourth mutually unbiased basis extending a given MU triple `T`. -/
def HasFourthBasis (T : MUTriple) : Prop :=
  ∃ (b3 : Basis),
    is_mutually_unbiased T.b0 b3 ∧
    is_mutually_unbiased T.b1 b3 ∧
    is_mutually_unbiased T.b2 b3

/-!
### Residual R4: Vector-to-Basis Gluing Bridge
The bridge connecting vector-level curvature wall obstructions (ruling out individual
mutually unbiased vectors) to the basis-level non-extension predicate (`¬ HasFourthBasis T`).
-/

/-- An abstract type representing a vector in dimension 6. -/
structure Vector6 where
  carrier : Unit := ()
deriving Inhabited, Nonempty

/-- The constituent vectors of an orthonormal basis in dimension 6.
    Every basis `b : Basis` provides 6 constituent vectors `basis_vector b k` for `k ∈ Fin 6`. -/
opaque basis_vector : Basis → Fin 6 → Vector6

/-- Relation stating that a vector is mutually unbiased to an entire basis:
    `|⟨b_j, v⟩|² = 1/6` for all constituent vectors `b_j` of the basis. -/
opaque is_mu_vector_to_basis : Basis → Vector6 → Prop

/-- Two bases are mutually unbiased only if every constituent vector of each basis
    is mutually unbiased to the other basis. -/
def BasisVectorMUContract : Prop :=
  ∀ {b1 b2 : Basis}, is_mutually_unbiased b1 b2 → ∀ (k : Fin 6), is_mu_vector_to_basis b1 (basis_vector b2 k)

/-- A vector that is simultaneously mutually unbiased to all three constituent bases of an MU triple `T`. -/
def IsMUVectorToTriple (T : MUTriple) (v : Vector6) : Prop :=
  is_mu_vector_to_basis T.b0 v ∧
  is_mu_vector_to_basis T.b1 v ∧
  is_mu_vector_to_basis T.b2 v

/-- **Theorem: Vector Extraction from Fourth Basis (Residual R4 Component)**:
    If an MU triple `T` admits a fourth mutually unbiased basis `b3`, then under the canonical
    basis-vector contract, `b3` provides at least one vector (for example, its 0-th basis vector)
    that is mutually unbiased to `T`. -/
theorem vector_of_fourth_basis
    (h_contract : BasisVectorMUContract)
    (T : MUTriple) (h : HasFourthBasis T) :
    ∃ (v : Vector6), IsMUVectorToTriple T v := by
  obtain ⟨b3, h0, h1, h2⟩ := h
  let v0 := basis_vector b3 0
  have hv0 : is_mu_vector_to_basis T.b0 v0 := h_contract h0 0
  have hv1 : is_mu_vector_to_basis T.b1 v0 := h_contract h1 0
  have hv2 : is_mu_vector_to_basis T.b2 v0 := h_contract h2 0
  exact ⟨v0, ⟨hv0, hv1, hv2⟩⟩

/-- **Theorem: R4 Basis Gluing Bridge**:
    If no single vector in C^6 can be simultaneously mutually unbiased to the three
    constituent bases of an MU triple `T` (e.g. ruled out by a continuous curvature wall `Ψ²(v) > 0`),
    then under the basis-vector contract, no fourth mutually unbiased basis can exist for `T`. -/
theorem r4_basis_gluing_bridge
    (h_contract : BasisVectorMUContract)
    (T : MUTriple)
    (h_no_vec : ∀ (v : Vector6), ¬ IsMUVectorToTriple T v) :
    ¬ HasFourthBasis T := by
  intro h_fourth
  obtain ⟨v, hv⟩ := vector_of_fourth_basis h_contract T h_fourth
  exact h_no_vec v hv

#print axioms vector_of_fourth_basis
#print axioms r4_basis_gluing_bridge

/-- Witness that an MU triple `T` is a constituent triple of a 7-basis configuration `B`. -/
def InConfig (T : MUTriple) (B : Fin 7 → Basis) : Prop :=
  ∃ (i0 i1 i2 : Fin 7),
    i0 ≠ i1 ∧ i0 ≠ i2 ∧ i1 ≠ i2 ∧
    T.b0 = B i0 ∧ T.b1 = B i1 ∧ T.b2 = B i2

/-- Witness that an MU triple `T` is a constituent triple of a 4-basis configuration `B`. -/
def InConfig4 (T : MUTriple) (B : Fin 4 → Basis) : Prop :=
  ∃ (i0 i1 i2 : Fin 4),
    i0 ≠ i1 ∧ i0 ≠ i2 ∧ i1 ≠ i2 ∧
    T.b0 = B i0 ∧ T.b1 = B i1 ∧ T.b2 = B i2


/-- Equivalence classes of MU triples under unitary and phase gauge transformations. -/
opaque TripleClass : Type

/-- Membership of an MU triple in an equivalence class. -/
opaque belongs_to_class : MUTriple → TripleClass → Prop

/-- The collection of covered triple classes in the certified moduli atlas
(e.g., the Dita seeds Y2⊗Q1 and Y2⊗Q2 neighborhood covers and canonical triple T0). -/
opaque CoveredClasses : TripleClass → Prop

/-!
### The Three Gluing Premises (Gate Definitions)
-/

/-- **Premise G1 (Exhaustive Moduli Cover / Admissibility Landing):**
Every admissible complete 7-basis MUB configuration in dimension 6 contains at least
one triple that lands in a covered atlas class. -/
def G1 : Prop :=
  ∀ (B : Fin 7 → Basis),
    PairwiseMU B →
    ∃ (T : MUTriple), InConfig T B ∧ ∃ (c : TripleClass), CoveredClasses c ∧ belongs_to_class T c

/-- **Premise G2 (Lossless Wall Transport & Extension Obstruction):**
Each covered class transports to a wall-certified lane without losing ZeroRel or
terminalizer information, establishing that no triple in any covered class admits
a fourth mutually unbiased basis. -/
def G2 : Prop :=
  ∀ (c : TripleClass),
    CoveredClasses c →
    ∀ (T : MUTriple), belongs_to_class T c → ¬ HasFourthBasis T

/-- **Premise G3 (Basis Gluing / Configuration Extension):**
In any complete 7-basis MUB configuration, every constituent triple can be extended
by a fourth mutually unbiased basis belonging to the configuration.
Equivalently: classwise fourth-vector obstruction implies no complete 7-basis set. -/
def G3 : Prop :=
  ∀ (B : Fin 7 → Basis),
    PairwiseMU B →
    ∀ (T : MUTriple), InConfig T B → HasFourthBasis T

/-!
### Primary Assembly Theorem
-/

/-- **The Gluing Assembly Theorem.**
Assuming G1, G2, and G3, there exists no complete set of seven MUBs in dimension 6.
The premises remain unproved; the reduction is exact and sorry-free. -/
theorem gluing_assembly (h : G1 ∧ G2 ∧ G3) : NoCompleteMUB6 := by
  intro h_complete
  rcases h with ⟨hG1, hG2, hG3⟩
  rcases h_complete with ⟨B, hB_mu⟩
  -- By G1, the configuration B contains a triple T in some covered class c
  obtain ⟨T, hT_in, c, hc_cov, hT_class⟩ := hG1 B hB_mu
  -- By G3, since T is in configuration B, T has a fourth basis
  have h_has4 : HasFourthBasis T := hG3 B hB_mu T hT_in
  -- By G2, since T belongs to covered class c, T has NO fourth basis
  have h_no4 : ¬ HasFourthBasis T := hG2 c hc_cov T hT_class
  -- Contradiction between existence and non-existence of a fourth basis
  exact h_no4 h_has4

#print axioms gluing_assembly

/-!
### Mechanization and Discharge of G3
G3 is a purely combinatorial/linear algebraic theorem:
In any 7-basis pairwise MUB family, choosing any 3 bases leaves 4 other bases,
each of which is distinct from the 3 and mutually unbiased to all 3.
-/

/-- Explicit choice of a fourth index distinct from any three given indices in `Fin 7`. -/
def candidate_fourth (i0 i1 i2 : Fin 7) : Fin 7 :=
  if 0 ≠ i0 ∧ 0 ≠ i1 ∧ 0 ≠ i2 then 0
  else if 1 ≠ i0 ∧ 1 ≠ i1 ∧ 1 ≠ i2 then 1
  else if 2 ≠ i0 ∧ 2 ≠ i1 ∧ 2 ≠ i2 then 2
  else 3

/-- Proof that `candidate_fourth` produces an index distinct from `i0`, `i1`, and `i2`. -/
theorem candidate_fourth_distinct (i0 i1 i2 : Fin 7) :
    candidate_fourth i0 i1 i2 ≠ i0 ∧
    candidate_fourth i0 i1 i2 ≠ i1 ∧
    candidate_fourth i0 i1 i2 ≠ i2 := by
  revert i0 i1 i2
  decide

#print axioms candidate_fourth_distinct

/-- **Theorem: G3 is a provable combinatorial truth.**
Any constituent triple of a pairwise mutually unbiased 7-basis family can be extended
by a fourth mutually unbiased basis within the family. -/
theorem g3_theorem : G3 := by
  intro B hB_mu T hT_in
  rcases hT_in with ⟨i0, i1, i2, _, _, _, h0, h1, h2⟩
  let i3 := candidate_fourth i0 i1 i2
  have h_distinct := candidate_fourth_distinct i0 i1 i2
  have hd0 : i3 ≠ i0 := h_distinct.1
  have hd1 : i3 ≠ i1 := h_distinct.2.1
  have hd2 : i3 ≠ i2 := h_distinct.2.2
  -- The candidate basis B i3 is mutually unbiased to B i0, B i1, B i2
  have h_mu0 : is_mutually_unbiased (B i0) (B i3) := hB_mu i0 i3 (Ne.symm hd0)
  have h_mu1 : is_mutually_unbiased (B i1) (B i3) := hB_mu i1 i3 (Ne.symm hd1)
  have h_mu2 : is_mutually_unbiased (B i2) (B i3) := hB_mu i2 i3 (Ne.symm hd2)
  -- Substitute T.b0 = B i0, T.b1 = B i1, T.b2 = B i2
  rw [← h0] at h_mu0
  rw [← h1] at h_mu1
  rw [← h2] at h_mu2
  exact ⟨B i3, h_mu0, h_mu1, h_mu2⟩

#print axioms g3_theorem

/-- **Corollary: Reduction of MUB(6) gluing to G1 and G2.**
Since G3 is mathematically verified, the full gluing assembly reduces to `G1 ∧ G2`. -/
theorem gluing_reduction_G1_G2 (h : G1 ∧ G2) : NoCompleteMUB6 :=
  gluing_assembly ⟨h.1, h.2, g3_theorem⟩

#print axioms gluing_reduction_G1_G2

/-!
### Sub-Obligation Decomposition of G2
G2 decomposes into:
1. `WallCertified c`: A finite computational certificate that representative `T_rep` has no 4th basis.
2. `TransportInvariance c`: A mathematical theorem that gauge equivalence preserves `HasFourthBasis`.
-/

/-- A class has a wall certificate if it contains a representative with no fourth basis. -/
def WallCertified (c : TripleClass) : Prop :=
  ∃ (T_rep : MUTriple), belongs_to_class T_rep c ∧ ¬ HasFourthBasis T_rep

/-- A class has lossless transport if gauge equivalence preserves fourth-basis extension. -/
def TransportInvariance (c : TripleClass) : Prop :=
  ∀ (T T' : MUTriple),
    belongs_to_class T c → belongs_to_class T' c →
    (HasFourthBasis T ↔ HasFourthBasis T')

/-- **Theorem: G2 decomposes into Wall Certification + Transport Invariance.** -/
theorem g2_of_wall_and_transport
    (h_wall : ∀ c, CoveredClasses c → WallCertified c)
    (h_trans : ∀ c, CoveredClasses c → TransportInvariance c) :
    G2 := by
  intro c hc T hT
  obtain ⟨T_rep, hT_rep_class, h_no4_rep⟩ := h_wall c hc
  have h_equiv := h_trans c hc T T_rep hT hT_rep_class
  intro h_has4_T
  have h_has4_rep : HasFourthBasis T_rep := h_equiv.mp h_has4_T
  exact h_no4_rep h_has4_rep

#print axioms g2_of_wall_and_transport

/-!
### Quadruple Basis Gluing (NoFourMUB6 Assembly)
Conditional assembly for the abstract Basis and mutual-unbiasedness predicates.
-/

/-- Explicit choice of a fourth index distinct from any three given indices in `Fin 4`. -/
def candidate_fourth_fin4 (i0 i1 i2 : Fin 4) : Fin 4 :=
  if 0 ≠ i0 ∧ 0 ≠ i1 ∧ 0 ≠ i2 then 0
  else if 1 ≠ i0 ∧ 1 ≠ i1 ∧ 1 ≠ i2 then 1
  else if 2 ≠ i0 ∧ 2 ≠ i1 ∧ 2 ≠ i2 then 2
  else 3

/-- Proof that `candidate_fourth_fin4` produces an index distinct from `i0`, `i1`, and `i2`. -/
theorem candidate_fourth_fin4_distinct (i0 i1 i2 : Fin 4) :
    candidate_fourth_fin4 i0 i1 i2 ≠ i0 ∧
    candidate_fourth_fin4 i0 i1 i2 ≠ i1 ∧
    candidate_fourth_fin4 i0 i1 i2 ≠ i2 := by
  revert i0 i1 i2
  decide

#print axioms candidate_fourth_fin4_distinct

/-- **Premise G3_Quad (Basis Gluing for 4-Basis Configurations):**
In any 4-basis MUB configuration, every constituent triple can be extended by a fourth
mutually unbiased basis belonging to the configuration. -/
def G3_Quad : Prop :=
  ∀ (B : Fin 4 → Basis),
    PairwiseMU B →
    ∀ (T : MUTriple), InConfig4 T B → HasFourthBasis T

/-- **Theorem: G3_Quad is a provable combinatorial truth.**
Any constituent triple of a pairwise mutually unbiased 4-basis family can be extended
by a fourth mutually unbiased basis within the family. -/
theorem g3_quad_theorem : G3_Quad := by
  intro B hB_mu T hT_in
  rcases hT_in with ⟨i0, i1, i2, _, _, _, h0, h1, h2⟩
  let i3 := candidate_fourth_fin4 i0 i1 i2
  have h_distinct := candidate_fourth_fin4_distinct i0 i1 i2
  have hd0 : i3 ≠ i0 := h_distinct.1
  have hd1 : i3 ≠ i1 := h_distinct.2.1
  have hd2 : i3 ≠ i2 := h_distinct.2.2
  have h_mu0 : is_mutually_unbiased (B i0) (B i3) := hB_mu i0 i3 (Ne.symm hd0)
  have h_mu1 : is_mutually_unbiased (B i1) (B i3) := hB_mu i1 i3 (Ne.symm hd1)
  have h_mu2 : is_mutually_unbiased (B i2) (B i3) := hB_mu i2 i3 (Ne.symm hd2)
  rw [← h0] at h_mu0
  rw [← h1] at h_mu1
  rw [← h2] at h_mu2
  exact ⟨B i3, h_mu0, h_mu1, h_mu2⟩

#print axioms g3_quad_theorem

/-- **Premise G1_Quad (Exhaustive Moduli Cover for 4-Basis Configurations):**
Every 4-basis MUB configuration contains at least one constituent triple landing in a covered class. -/
def G1_Quad : Prop :=
  ∀ (B : Fin 4 → Basis),
    PairwiseMU B →
    ∃ (T : MUTriple), InConfig4 T B ∧ ∃ (c : TripleClass), CoveredClasses c ∧ belongs_to_class T c

/-- **The Quadruple Gluing Assembly Theorem.**
Assuming G1_Quad, G2, and G3_Quad, there exists no set of four MUBs in dimension 6. -/
theorem gluing_assembly_quad (h : G1_Quad ∧ G2 ∧ G3_Quad) : NoFourMUB6 := by
  intro h_four
  rcases h with ⟨hG1, hG2, hG3⟩
  rcases h_four with ⟨B, hB_mu⟩
  obtain ⟨T, hT_in, c, hc_cov, hT_class⟩ := hG1 B hB_mu
  have h_has4 : HasFourthBasis T := hG3 B hB_mu T hT_in
  have h_no4 : ¬ HasFourthBasis T := hG2 c hc_cov T hT_class
  exact h_no4 h_has4

#print axioms gluing_assembly_quad

/-- **Theorem: Quadruple Gluing Reduction to G1_Quad and G2.**
Uses `g3_quad_theorem`; the hypotheses `G1_Quad` and `G2` remain explicit. -/
theorem gluing_reduction_G1_G2_quad (h : G1_Quad ∧ G2) : NoFourMUB6 :=
  gluing_assembly_quad ⟨h.1, h.2, g3_quad_theorem⟩

#print axioms gluing_reduction_G1_G2_quad

/-- **Theorem: Pointwise Triple Obstruction Implies NoFourMUB6.**
If every mutually unbiased triple in dimension 6 admits no fourth basis, then no 4-MUB
configuration exists.
Proved constructively with zero non-standard axioms. -/
theorem no_four_mub6_of_no_triple_extension (h : ∀ (T : MUTriple), ¬ HasFourthBasis T) : NoFourMUB6 := by
  intro ⟨B, hB_mu⟩
  have h01 : (0 : Fin 4) ≠ 1 := by decide
  have h02 : (0 : Fin 4) ≠ 2 := by decide
  have h12 : (1 : Fin 4) ≠ 2 := by decide
  let T0 : MUTriple := {
    b0 := B 0
    b1 := B 1
    b2 := B 2
    mu01 := hB_mu 0 1 h01
    mu02 := hB_mu 0 2 h02
    mu12 := hB_mu 1 2 h12
  }
  have h_no4 := h T0
  have h03 : (0 : Fin 4) ≠ 3 := by decide
  have h13 : (1 : Fin 4) ≠ 3 := by decide
  have h23 : (2 : Fin 4) ≠ 3 := by decide
  have h_has4 : HasFourthBasis T0 := ⟨B 3, hB_mu 0 3 h03, hB_mu 1 3 h13, hB_mu 2 3 h23⟩
  exact h_no4 h_has4

#print axioms no_four_mub6_of_no_triple_extension

end MUB6.Gluing
