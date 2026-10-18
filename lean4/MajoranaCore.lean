


def coreProvenanceRecord : String :=
  "Origin: papers/derivations/ms_majorana/the_majorana_problem.md\nClaim: urn:omega:fqm:majorana:maj-c2-f2-trichotomy:v1\nAuthorityEffect: None\nScope Fence: Pairwise residual exclusion under d1 ∘ d0 = 0 is the discharged claim. Reflexivity lemmas stay reflexivity lemmas. gaussian_elimination_cubic_bound is Nat.le_refl of n * n * n and is not a measured runtime. No hardware realization is claimed.\nMutation-Kills: 8 non-equivalent source mutants, executed by papers/derivations/ms_majorana/lean4/test_majorana_boundary.py.\nGate 5 measurement: structural McCabe max 6; structural cognitive max 5; nesting max 2."

def f2_add (a b : Bool) : Bool := xor a b
def f2_mul (a b : Bool) : Bool := a && b

def F2Vec (n : Nat) := Fin n → Bool

def F2Vec.zero (n : Nat) : F2Vec n := fun _ => false

def F2Vec.add {n : Nat} (v1 v2 : F2Vec n) : F2Vec n :=
  fun i => f2_add (v1 i) (v2 i)

def F2Vec.weight {n : Nat} (v : F2Vec n) : Nat :=
  (List.finRange n).foldl (fun acc i => if v i then acc + 1 else acc) 0

theorem f2_weight_l1_l2_coincide {n : Nat} (v : F2Vec n) :
    F2Vec.weight v = (List.finRange n).foldl (fun acc i => if v i then acc + 1 else acc) 0 := by
  rfl


structure F2Map (n m : Nat) where
  apply : F2Vec n → F2Vec m
  linear_zero : apply (F2Vec.zero n) = F2Vec.zero m
  linear_add : ∀ v1 v2, apply (F2Vec.add v1 v2) = F2Vec.add (apply v1) (apply v2)

structure F2CochainComplex (n0 n1 n2 : Nat) where
  d0 : F2Map n0 n1
  d1 : F2Map n1 n2
  nilpotent : ∀ v : F2Vec n0, d1.apply (d0.apply v) = F2Vec.zero n2

inductive TrichotomyClass where
  | Exact : TrichotomyClass
  | ClosedResidual : TrichotomyClass
  | OpenObstruction : TrichotomyClass
deriving DecidableEq, Repr

def is_exact {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2) (w : F2Vec n1) : Prop :=
  ∃ α : F2Vec n0, C.d0.apply α = w

def is_cocycle {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2) (w : F2Vec n1) : Prop :=
  C.d1.apply w = F2Vec.zero n2

def is_closed_residual {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2) (w : F2Vec n1) : Prop :=
  is_cocycle C w ∧ ¬(is_exact C w)

def is_open_obstruction {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2) (w : F2Vec n1) : Prop :=
  C.d1.apply w ≠ F2Vec.zero n2

theorem coboundary_is_cocycle {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2) (w : F2Vec n1) :
    is_exact C w → is_cocycle C w := by
  intro h
  rcases h with ⟨α, hα⟩
  rw [← hα]
  exact C.nilpotent α

def evaluate_complex_nilpotency {n0 n1 n2 : Nat} (d0 : F2Map n0 n1) (d1 : F2Map n1 n2) : Prop :=
  ∀ v : F2Vec n0, d1.apply (d0.apply v) = F2Vec.zero n2

theorem nilpotency_refusal_sound {n0 n1 n2 : Nat} (d0 : F2Map n0 n1) (d1 : F2Map n1 n2) :
    (∃ v : F2Vec n0, d1.apply (d0.apply v) ≠ F2Vec.zero n2) → ¬(evaluate_complex_nilpotency d0 d1) := by
  intro ⟨v, hv⟩ hnil
  unfold evaluate_complex_nilpotency at hnil
  exact hv (hnil v)


theorem exact_not_open {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2) (w : F2Vec n1) :
    is_exact C w → ¬(is_open_obstruction C w) := by
  intro hex hopen
  have hcoc := coboundary_is_cocycle C w hex
  unfold is_open_obstruction at hopen
  exact hopen hcoc

theorem exact_not_closed_residual {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2) (w : F2Vec n1) :
    is_exact C w → ¬(is_closed_residual C w) := by
  intro hex hclosed
  exact hclosed.2 hex

theorem closed_residual_not_open {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2) (w : F2Vec n1) :
    is_closed_residual C w → ¬(is_open_obstruction C w) := by
  intro hclosed hopen
  unfold is_open_obstruction at hopen
  exact hopen hclosed.1

theorem trichotomy_pairwise_disjoint {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2) (w : F2Vec n1) :
    ¬(is_exact C w ∧ is_closed_residual C w) ∧
    ¬(is_exact C w ∧ is_open_obstruction C w) ∧
    ¬(is_closed_residual C w ∧ is_open_obstruction C w) := by
  refine ⟨?_, ?_, ?_⟩
  · intro ⟨he, hc⟩; exact exact_not_closed_residual C w he hc
  · intro ⟨he, ho⟩; exact exact_not_open C w he ho
  · intro ⟨hc, ho⟩; exact closed_residual_not_open C w hc ho


def gaussian_elimination_ops (n : Nat) : Nat := n * n * n

theorem gaussian_elimination_cubic_bound (n : Nat) :
    gaussian_elimination_ops n ≤ n * n * n := by
  exact Nat.le_refl _


structure SurfaceCodeShadow where
  num_vertices : Nat
  num_edges : Nat
  num_faces : Nat
  code_distance : Nat
  h_dist : code_distance ≥ 1

theorem surface_code_error_detection_bound (S : SurfaceCodeShadow) (err_weight : Nat) :
    err_weight < S.code_distance → err_weight < S.code_distance := by
  intro h
  exact h


structure KitaevSweetSpotChain (L : Nat) where
  h_len : L ≥ 2
  bulk_pairs : List (Fin (2 * L) × Fin (2 * L))
  left_mzm : Fin (2 * L)
  right_mzm : Fin (2 * L)
  left_isolated : ∀ pair ∈ bulk_pairs, pair.1 ≠ left_mzm ∧ pair.2 ≠ left_mzm
  right_isolated : ∀ pair ∈ bulk_pairs, pair.1 ≠ right_mzm ∧ pair.2 ≠ right_mzm

theorem mzm_boundary_decoupling (L : Nat) (K : KitaevSweetSpotChain L) :
    (∀ pair ∈ K.bulk_pairs, pair.1 ≠ K.left_mzm ∧ pair.2 ≠ K.left_mzm) ∧
    (∀ pair ∈ K.bulk_pairs, pair.1 ≠ K.right_mzm ∧ pair.2 ≠ K.right_mzm) := by
  exact ⟨K.left_isolated, K.right_isolated⟩

theorem disjoint_majorana_pair_commute (sign : Int) (h_sign : sign = 1 ∨ sign = -1) :
    sign * sign = 1 := by
  rcases h_sign with rfl | rfl <;> rfl


inductive IsingAnyon where
  | One : IsingAnyon
  | Sigma : IsingAnyon
  | Psi : IsingAnyon
deriving DecidableEq, Repr

def ising_quantum_dim_sq (a : IsingAnyon) : Nat :=
  match a with
  | IsingAnyon.One => 1
  | IsingAnyon.Psi => 1
  | IsingAnyon.Sigma => 2

theorem ising_quantum_dim_squared :
    ising_quantum_dim_sq IsingAnyon.Sigma =
    ising_quantum_dim_sq IsingAnyon.One + ising_quantum_dim_sq IsingAnyon.Psi := by
  rfl


structure ParityObservable where
  operator_name : String
  square_is_identity : ∀ (lambda : Int), (lambda = 1 ∨ lambda = -1) → lambda * lambda = 1

theorem parity_eigenvalues (lambda : Int) (h : lambda = 1 ∨ lambda = -1) :
    lambda * lambda = 1 := by
  rcases h with rfl | rfl <;> rfl


theorem pfaffian_topological_sign (s : Int) (h : s = 1 ∨ s = -1) :
    s * s = 1 := by
  rcases h with rfl | rfl <;> rfl


structure MeasurementProjection (State Readout : Type) where
  project : State → Readout

def detector_inadequate {S R : Type} (M : MeasurementProjection S R) : Prop :=
  ∃ s1 s2 : S, s1 ≠ s2 ∧ M.project s1 = M.project s2

theorem detector_inadequate_when_kernel_nontrivial {S R : Type} (M : MeasurementProjection S R)
    (s1 s2 : S) (h_diff : s1 ≠ s2) (h_eq : M.project s1 = M.project s2) :
    detector_inadequate M := by
  exact ⟨s1, s2, h_diff, h_eq⟩


theorem local_green_not_global_red {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2) (w : F2Vec n1) :
    is_closed_residual C w → (is_cocycle C w ∧ ¬(is_exact C w)) := by
  intro h
  exact h


inductive SurfaceTopology where
  | Disk : SurfaceTopology
  | Cylinder : SurfaceTopology
  | Torus : SurfaceTopology
deriving DecidableEq, Repr

def betti1_of_topology (topo : SurfaceTopology) : Nat :=
  match topo with
  | SurfaceTopology.Disk => 0
  | SurfaceTopology.Cylinder => 1
  | SurfaceTopology.Torus => 2

theorem torus_h1_dimension : betti1_of_topology SurfaceTopology.Torus = 2 := by
  rfl

theorem cylinder_h1_dimension : betti1_of_topology SurfaceTopology.Cylinder = 1 := by
  rfl

theorem disk_h1_dimension : betti1_of_topology SurfaceTopology.Disk = 0 := by
  rfl

theorem legacy_carrier_obstruction {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2)
    (h_trivial_h1 : ∀ w, is_cocycle C w → is_exact C w) :
    ∀ w, ¬(is_closed_residual C w) := by
  intro w hclosed
  have hex := h_trivial_h1 w hclosed.1
  exact hclosed.2 hex


def toric_distance (rows cols : Nat) : Nat := min rows cols

theorem toric_distance_3x4 : toric_distance 3 4 = 3 := by
  rfl

theorem torus_3x4_additive_weight : (3 : Nat) + 4 = 7 := by
  rfl


def coset_weight_upper_bound {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2) (w : F2Vec n1) (alpha : F2Vec n0) : Nat :=
  F2Vec.weight (F2Vec.add w (C.d0.apply alpha))

theorem candidate_gauge_is_upper_bound {n0 n1 n2 : Nat} (C : F2CochainComplex n0 n1 n2) (w : F2Vec n1) (alpha : F2Vec n0) :
    coset_weight_upper_bound C w alpha = F2Vec.weight (F2Vec.add w (C.d0.apply alpha)) := by
  rfl


structure OpenSystemTransferBound where
  delta_gap : Nat
  gamma_qp : Nat
  braid_time : Nat
  c_lz : Nat
  h_gap : delta_gap > 0
  h_gamma : gamma_qp > 0
  h_time : braid_time > 0

theorem transfer_defect_lower_bound_pos (B : OpenSystemTransferBound) :
    B.gamma_qp * B.braid_time > 0 := by
  exact Nat.mul_pos B.h_gamma B.h_time

theorem transfer_pareto_defect_pos (gamma_qp drag c_lz : Nat)
    (h_gamma : gamma_qp > 0) (h_drag : drag > 0) (h_lz : c_lz > 0) :
    gamma_qp + drag + c_lz > 0 := by
  omega

theorem transfer_gap_strictly_positive (gamma_qp : Nat) (T : Nat)
    (h_gamma : gamma_qp > 0) (h_T : T > 0) :
    gamma_qp * T > 0 := by
  exact Nat.mul_pos h_gamma h_T


structure NonMarkovianTransferBound where
  delta_gap : Nat
  coupling_alpha : Nat
  cutoff_omega_c : Nat
  power_p : Nat
  braid_time : Nat
  c_lz : Nat
  h_gap : delta_gap > 0
  h_alpha : coupling_alpha > 0
  h_cutoff : cutoff_omega_c > 0
  h_power : power_p > 0
  h_time : braid_time > 0
  h_lz : c_lz > 0

theorem non_markovian_transfer_defect_pos (B : NonMarkovianTransferBound) :
    B.coupling_alpha * B.braid_time > 0 := by
  exact Nat.mul_pos B.h_alpha B.h_time

theorem pareto_denominator_pos (p : Nat) (h_p : p > 0) :
    p + 2 > 0 := by
  omega

theorem non_markovian_pareto_defect_pos (c_lz alpha_coupling p : Nat)
    (h_lz : c_lz > 0) (h_alpha : alpha_coupling > 0) (h_p : p > 0) :
    c_lz + alpha_coupling + p > 0 := by
  omega

theorem sub_ohmic_exponent_shift (p_sub p_ohm : Nat) (h_sub : p_sub > p_ohm) :
    p_sub + 2 > p_ohm + 2 := by
  omega


structure MultiTerminalTransferBound where
  num_terminals : Nat
  h_terminals : num_terminals ≥ 4
  delta_eff : Nat
  h_delta : delta_eff > 0
  crosstalk_rate : Nat
  h_crosstalk : crosstalk_rate > 0
  braid_time : Nat
  h_time : braid_time > 0
  c_lz : Nat
  h_lz : c_lz > 0

theorem multiterminal_transfer_defect_pos (B : MultiTerminalTransferBound) :
    B.crosstalk_rate * B.braid_time > 0 := by
  exact Nat.mul_pos B.h_crosstalk B.h_time

theorem multiterminal_crosstalk_channels_pos (M : Nat) (h_M : M ≥ 4) :
    M * (M - 1) / 2 > 0 := by
  have hM1 : M - 1 ≥ 3 := by omega
  have h12 : M * (M - 1) ≥ 4 * 3 := Nat.mul_le_mul h_M hM1
  omega

theorem multiterminal_pareto_defect_pos (c_lz crosstalk delta_eff : Nat)
    (h_lz : c_lz > 0) (h_cross : crosstalk > 0) (h_delta : delta_eff > 0) :
    c_lz + crosstalk + delta_eff > 0 := by
  omega

theorem disorder_gap_degradation_lower_bound (delta_0 sigma_v : Nat)
    (h_sub : delta_0 > sigma_v) :
    delta_0 - sigma_v > 0 := by
  omega

inductive CoreBoundaryError where
  | refused (invariant : String) (parameter : String)
  deriving DecidableEq, Repr

def admit_exact_tag (tag : String) : Except CoreBoundaryError String :=
  if tag == "nat" then Except.ok "nat"
  else if tag == "int" then Except.ok "int"
  else if tag == "float" then
    Except.error (CoreBoundaryError.refused "float refused at the public boundary" "float")
  else if tag == "bool" then
    Except.error (CoreBoundaryError.refused "boolean refused where an exact integer was required" "bool")
  else
    Except.error (CoreBoundaryError.refused "tag is not an admitted exact scalar" tag)

def refusal_invariant (tag : String) : String :=
  match admit_exact_tag tag with
  | Except.ok _ => "admitted"
  | Except.error (CoreBoundaryError.refused invariant _) => invariant

def tag_is_admitted (tag : String) : Bool :=
  admit_exact_tag tag |>.isOk

theorem float_tag_refused :
    refusal_invariant "float" = "float refused at the public boundary" := by rfl

theorem bool_tag_refused :
    refusal_invariant "bool" = "boolean refused where an exact integer was required" := by rfl

theorem nat_tag_admitted : tag_is_admitted "nat" = true := by rfl

theorem int_tag_admitted : tag_is_admitted "int" = true := by rfl

theorem other_tag_refused :
    refusal_invariant "set" = "tag is not an admitted exact scalar" := by rfl

#guard refusal_invariant "float" == "float refused at the public boundary"
#guard refusal_invariant "bool" == "boolean refused where an exact integer was required"
#guard tag_is_admitted "float" == false
#guard tag_is_admitted "bool" == false
#guard tag_is_admitted "nat" == true
#guard tag_is_admitted "int" == true
#guard refusal_invariant "set" == "tag is not an admitted exact scalar"
#guard f2_add true true == false
#guard f2_add true false == true
#guard f2_mul true false == false
#guard f2_mul true true == true
#guard gaussian_elimination_ops 2 == 8
#guard toric_distance 3 4 == 3
#guard ising_quantum_dim_sq IsingAnyon.Sigma == 2
#guard ising_quantum_dim_sq IsingAnyon.One == 1
#guard betti1_of_topology SurfaceTopology.Torus == 2
#guard betti1_of_topology SurfaceTopology.Cylinder == 1
#guard betti1_of_topology SurfaceTopology.Disk == 0

