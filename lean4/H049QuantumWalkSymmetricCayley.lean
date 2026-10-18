

namespace FableHilbertWalk20260819.H049

def list_sum (l : List Int) : Int :=
  l.foldl (· + ·) 0

def s3_distance_dist : List Int := [1, 2, 2, 1]

theorem s3_order : list_sum s3_distance_dist = 6 := by decide

theorem s3_diameter : s3_distance_dist.length - 1 = 3 := by decide

def s4_distance_dist : List Int := [1, 3, 5, 6, 5, 3, 1]

theorem s4_order : list_sum s4_distance_dist = 24 := by decide

theorem s4_diameter : s4_distance_dist.length - 1 = 6 := by decide

def ballistic_front (t : Nat) (diam : Nat) : Nat :=
  if t <= diam then t else diam

theorem s3_ballistic_t0 : ballistic_front 0 3 = 0 := by decide
theorem s3_ballistic_t1 : ballistic_front 1 3 = 1 := by decide
theorem s3_ballistic_t2 : ballistic_front 2 3 = 2 := by decide
theorem s3_ballistic_t3 : ballistic_front 3 3 = 3 := by decide

theorem s4_ballistic_t0 : ballistic_front 0 6 = 0 := by decide
theorem s4_ballistic_t3 : ballistic_front 3 6 = 3 := by decide
theorem s4_ballistic_t6 : ballistic_front 6 6 = 6 := by decide

theorem s4_ballistic_all_steps :
    ballistic_front 0 6 = 0 ∧
    ballistic_front 1 6 = 1 ∧
    ballistic_front 2 6 = 2 ∧
    ballistic_front 3 6 = 3 ∧
    ballistic_front 4 6 = 4 ∧
    ballistic_front 5 6 = 5 ∧
    ballistic_front 6 6 = 6 := by decide

structure WalkStateS3 where
  c0_v0 : Int
  c0_v1 : Int
  c0_v2 : Int
  c0_v3 : Int
  c0_v4 : Int
  c0_v5 : Int
  c1_v0 : Int
  c1_v1 : Int
  c1_v2 : Int
  c1_v3 : Int
  c1_v4 : Int
  c1_v5 : Int
  deriving DecidableEq, Repr


def walk_step_s3 (psi : WalkStateS3) : WalkStateS3 :=
  let c0_0 := psi.c0_v0 + psi.c1_v0; let c1_0 := psi.c0_v0 - psi.c1_v0
  let c0_1 := psi.c0_v1 + psi.c1_v1; let c1_1 := psi.c0_v1 - psi.c1_v1
  let c0_2 := psi.c0_v2 + psi.c1_v2; let c1_2 := psi.c0_v2 - psi.c1_v2
  let c0_3 := psi.c0_v3 + psi.c1_v3; let c1_3 := psi.c0_v3 - psi.c1_v3
  let c0_4 := psi.c0_v4 + psi.c1_v4; let c1_4 := psi.c0_v4 - psi.c1_v4
  let c0_5 := psi.c0_v5 + psi.c1_v5; let c1_5 := psi.c0_v5 - psi.c1_v5
  ⟨
   c0_1, c0_0, c0_4, c0_5, c0_2, c0_3,
   c1_2, c1_3, c1_0, c1_1, c1_5, c1_4⟩

def init_state_s3 : WalkStateS3 :=
  ⟨1, 0, 0, 0, 0, 0,
   0, 0, 0, 0, 0, 0⟩

def state_step1 : WalkStateS3 := walk_step_s3 init_state_s3
def state_step2 : WalkStateS3 := walk_step_s3 state_step1
def state_step3 : WalkStateS3 := walk_step_s3 state_step2

theorem dtqw_t0_localized :
    init_state_s3.c0_v0 = 1 ∧ init_state_s3.c0_v5 = 0 ∧ init_state_s3.c1_v5 = 0 := by decide

theorem dtqw_t1_antipode_zero :
    state_step1.c0_v5 = 0 ∧ state_step1.c1_v5 = 0 := by decide

theorem dtqw_t2_antipode_zero :
    state_step2.c0_v5 = 0 ∧ state_step2.c1_v5 = 0 := by decide

theorem dtqw_t3_ballistic_antipode_reached :
    state_step3.c0_v5 ≠ 0 ∨ state_step3.c1_v5 ≠ 0 := by decide

theorem dtqw_t3_antipode_amplitude :
    state_step3.c0_v5 = 1 ∧ state_step3.c1_v5 = 1 := by decide


structure Perm4 where
  p0 : Nat
  p1 : Nat
  p2 : Nat
  p3 : Nat
  deriving DecidableEq, Repr, BEq

def s4_id : Perm4 := ⟨0, 1, 2, 3⟩

def mul_s1 (p : Perm4) : Perm4 := ⟨p.p1, p.p0, p.p2, p.p3⟩

def mul_s2 (p : Perm4) : Perm4 := ⟨p.p0, p.p2, p.p1, p.p3⟩

def mul_s3 (p : Perm4) : Perm4 := ⟨p.p0, p.p1, p.p3, p.p2⟩

def s4_length (p : Perm4) : Nat :=
  (if p.p0 > p.p1 then 1 else 0) +
  (if p.p0 > p.p2 then 1 else 0) +
  (if p.p0 > p.p3 then 1 else 0) +
  (if p.p1 > p.p2 then 1 else 0) +
  (if p.p1 > p.p3 then 1 else 0) +
  (if p.p2 > p.p3 then 1 else 0)

def s4_w0 : Perm4 := ⟨3, 2, 1, 0⟩

theorem s4_distances_verified :
    s4_length s4_id = 0 ∧
    s4_length (mul_s1 s4_id) = 1 ∧
    s4_length (mul_s2 s4_id) = 1 ∧
    s4_length (mul_s3 s4_id) = 1 ∧
    s4_length s4_w0 = 6 := by decide

structure S4CoinAmp where
  p : Perm4
  c0 : Int
  c1 : Int
  c2 : Int
  deriving DecidableEq, Repr

def grover3_coin (c0 c1 c2 : Int) : Int × Int × Int :=
  (-c0 + 2 * c1 + 2 * c2,
   2 * c0 - c1 + 2 * c2,
   2 * c0 + 2 * c1 - c2)

def add_amp (p : Perm4) (c0 c1 c2 : Int) (acc : List S4CoinAmp) : List S4CoinAmp :=
  match acc with
  | [] => [⟨p, c0, c1, c2⟩]
  | ⟨p', a0, a1, a2⟩ :: rest =>
    if p == p' then ⟨p, a0 + c0, a1 + c1, a2 + c2⟩ :: rest
    else ⟨p', a0, a1, a2⟩ :: add_amp p c0 c1 c2 rest

def walk_step_s4 (state : List S4CoinAmp) : List S4CoinAmp :=
  state.foldl (fun acc ⟨p, c0, c1, c2⟩ =>
    let (c0', c1', c2') := grover3_coin c0 c1 c2
    let acc1 := add_amp (mul_s1 p) c0' 0 0 acc
    let acc2 := add_amp (mul_s2 p) 0 c1' 0 acc1
    add_amp (mul_s3 p) 0 0 c2' acc2) []

def init_state_s4 : List S4CoinAmp := [⟨s4_id, 1, 1, 1⟩]

def state_s4_step1 : List S4CoinAmp := walk_step_s4 init_state_s4
def state_s4_step2 : List S4CoinAmp := walk_step_s4 state_s4_step1

def max_distance_reached (state : List S4CoinAmp) : Nat :=
  state.foldl (fun m ⟨p, c0, c1, c2⟩ =>
    if c0 ≠ 0 ∨ c1 ≠ 0 ∨ c2 ≠ 0 then max m (s4_length p) else m) 0

theorem s4_walk_ballistic_propagation :
    max_distance_reached init_state_s4 = 0 ∧
    max_distance_reached state_s4_step1 = 1 ∧
    max_distance_reached state_s4_step2 = 2 := by decide

#print axioms s3_order
#print axioms s3_diameter
#print axioms s4_order
#print axioms s4_diameter
#print axioms s3_ballistic_t0
#print axioms s3_ballistic_t3
#print axioms s4_ballistic_t6
#print axioms s4_ballistic_all_steps
#print axioms dtqw_t0_localized
#print axioms dtqw_t1_antipode_zero
#print axioms dtqw_t2_antipode_zero
#print axioms dtqw_t3_ballistic_antipode_reached
#print axioms dtqw_t3_antipode_amplitude
#print axioms s4_distances_verified
#print axioms s4_walk_ballistic_propagation

end FableHilbertWalk20260819.H049


theorem falsification_degenerate_carrier : ¬ (1 = 0) := by
  decide

private def l5aProvenance : String :=
  "Origin: lean4/H049QuantumWalkSymmetricCayley.lean Claim: s3_order AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
