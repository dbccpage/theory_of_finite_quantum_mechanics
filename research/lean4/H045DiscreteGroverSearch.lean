

namespace FableHilbertWalk20260819.H045

structure Quad3 where
  a : Int
  b : Int
  deriving DecidableEq, Repr

def qz : Quad3 := ⟨0, 0⟩
def qone : Quad3 := ⟨1, 0⟩
def qsqrt3 : Quad3 := ⟨0, 1⟩

def qadd (x y : Quad3) : Quad3 :=
  ⟨x.a + y.a, x.b + y.b⟩

def qsub (x y : Quad3) : Quad3 :=
  ⟨x.a - y.a, x.b - y.b⟩

def qmul (x y : Quad3) : Quad3 :=
  ⟨x.a * y.a + 3 * x.b * y.b, x.a * y.b + x.b * y.a⟩

def qsmul (c : Int) (x : Quad3) : Quad3 :=
  ⟨c * x.a, c * x.b⟩

instance : Zero Quad3 := ⟨qz⟩
instance : One Quad3 := ⟨qone⟩
instance : Add Quad3 := ⟨qadd⟩
instance : Sub Quad3 := ⟨qsub⟩
instance : Mul Quad3 := ⟨qmul⟩

structure Vec4 where
  v0 : Int
  v1 : Int
  v2 : Int
  v3 : Int
  deriving DecidableEq, Repr

structure Mat4 where
  r0 : Vec4
  r1 : Vec4
  r2 : Vec4
  r3 : Vec4
  deriving DecidableEq, Repr

def dot4 (u v : Vec4) : Int :=
  u.v0 * v.v0 + u.v1 * v.v1 + u.v2 * v.v2 + u.v3 * v.v3

def mat4_mul_vec (M : Mat4) (v : Vec4) : Vec4 :=
  ⟨dot4 M.r0 v, dot4 M.r1 v, dot4 M.r2 v, dot4 M.r3 v⟩

def v_uniform : Vec4 := ⟨1, 1, 1, 1⟩

def v_target : Vec4 := ⟨1, 0, 0, 0⟩

def R_oracle : Mat4 :=
  ⟨⟨-1, 0, 0, 0⟩,
   ⟨0, 1, 0, 0⟩,
   ⟨0, 0, 1, 0⟩,
   ⟨0, 0, 0, 1⟩⟩

def D_tilde : Mat4 :=
  ⟨⟨-1, 1, 1, 1⟩,
   ⟨1, -1, 1, 1⟩,
   ⟨1, 1, -1, 1⟩,
   ⟨1, 1, 1, -1⟩⟩

def grover_step (v : Vec4) : Vec4 :=
  mat4_mul_vec D_tilde (mat4_mul_vec R_oracle v)

theorem oracle_action :
    mat4_mul_vec R_oracle v_uniform = ⟨-1, 1, 1, 1⟩ := by rfl

theorem grover_one_step_exact :
    grover_step v_uniform = ⟨4, 0, 0, 0⟩ := by rfl

theorem grover_target_isolation :
    (grover_step v_uniform).v0 = 4 ∧
    (grover_step v_uniform).v1 = 0 ∧
    (grover_step v_uniform).v2 = 0 ∧
    (grover_step v_uniform).v3 = 0 := by decide

def eye4 : Mat4 :=
  ⟨⟨1, 0, 0, 0⟩,
   ⟨0, 1, 0, 0⟩,
   ⟨0, 0, 1, 0⟩,
   ⟨0, 0, 0, 1⟩⟩

def mat4_mul (A B : Mat4) : Mat4 :=
  ⟨⟨A.r0.v0 * B.r0.v0 + A.r0.v1 * B.r1.v0 + A.r0.v2 * B.r2.v0 + A.r0.v3 * B.r3.v0,
    A.r0.v0 * B.r0.v1 + A.r0.v1 * B.r1.v1 + A.r0.v2 * B.r2.v1 + A.r0.v3 * B.r3.v1,
    A.r0.v0 * B.r0.v2 + A.r0.v1 * B.r1.v2 + A.r0.v2 * B.r2.v2 + A.r0.v3 * B.r3.v2,
    A.r0.v0 * B.r0.v3 + A.r0.v1 * B.r1.v3 + A.r0.v2 * B.r2.v3 + A.r0.v3 * B.r3.v3⟩,
   ⟨A.r1.v0 * B.r0.v0 + A.r1.v1 * B.r1.v0 + A.r1.v2 * B.r2.v0 + A.r1.v3 * B.r3.v0,
    A.r1.v0 * B.r0.v1 + A.r1.v1 * B.r1.v1 + A.r1.v2 * B.r2.v1 + A.r1.v3 * B.r3.v1,
    A.r1.v0 * B.r0.v2 + A.r1.v1 * B.r1.v2 + A.r1.v2 * B.r2.v2 + A.r1.v3 * B.r3.v2,
    A.r1.v0 * B.r0.v3 + A.r1.v1 * B.r1.v3 + A.r1.v2 * B.r2.v3 + A.r1.v3 * B.r3.v3⟩,
   ⟨A.r2.v0 * B.r0.v0 + A.r2.v1 * B.r1.v0 + A.r2.v2 * B.r2.v0 + A.r2.v3 * B.r3.v0,
    A.r2.v0 * B.r0.v1 + A.r2.v1 * B.r1.v1 + A.r2.v2 * B.r2.v1 + A.r2.v3 * B.r3.v1,
    A.r2.v0 * B.r0.v2 + A.r2.v1 * B.r1.v2 + A.r2.v2 * B.r2.v2 + A.r2.v3 * B.r3.v2,
    A.r2.v0 * B.r0.v3 + A.r2.v1 * B.r1.v3 + A.r2.v2 * B.r2.v3 + A.r2.v3 * B.r3.v3⟩,
   ⟨A.r3.v0 * B.r0.v0 + A.r3.v1 * B.r1.v0 + A.r3.v2 * B.r2.v0 + A.r3.v3 * B.r3.v0,
    A.r3.v0 * B.r0.v1 + A.r3.v1 * B.r1.v1 + A.r3.v2 * B.r2.v1 + A.r3.v3 * B.r3.v1,
    A.r3.v0 * B.r0.v2 + A.r3.v1 * B.r1.v2 + A.r3.v2 * B.r2.v2 + A.r3.v3 * B.r3.v2,
    A.r3.v0 * B.r0.v3 + A.r3.v1 * B.r1.v3 + A.r3.v2 * B.r2.v3 + A.r3.v3 * B.r3.v3⟩⟩

theorem diffusion_squared :
    mat4_mul D_tilde D_tilde =
      ⟨⟨4, 0, 0, 0⟩,
       ⟨0, 4, 0, 0⟩,
       ⟨0, 0, 4, 0⟩,
       ⟨0, 0, 0, 4⟩⟩ := by decide

structure Vec2Q where
  x : Quad3
  y : Quad3
  deriving DecidableEq, Repr

def rot2d (v : Vec2Q) : Vec2Q :=
  ⟨qsub (qmul ⟨1, 0⟩ v.x) (qmul ⟨0, 1⟩ v.y),
   qadd (qmul ⟨0, 1⟩ v.x) (qmul ⟨1, 0⟩ v.y)⟩

def v0_state : Vec2Q := ⟨qsqrt3, qone⟩

theorem rotation_to_target :
    rot2d v0_state = ⟨⟨0, 0⟩, ⟨4, 0⟩⟩ := by decide

def S_rec : Nat → Int
  | 0 => 1
  | 1 => 2
  | n + 2 => S_rec (n + 1) - S_rec n

theorem S_rec_step0 : S_rec 0 = 1 := by rfl
theorem S_rec_step1 : S_rec 1 = 2 := by rfl
theorem S_rec_step2 : S_rec 2 = 1 := by rfl
theorem S_rec_step3 : S_rec 3 = -1 := by rfl
theorem S_rec_step4 : S_rec 4 = -2 := by rfl
theorem S_rec_step5 : S_rec 5 = -1 := by rfl
theorem S_rec_step6 : S_rec 6 = 1 := by rfl

theorem grover_periodicity_six : S_rec 6 = S_rec 0 := by decide

#print axioms oracle_action
#print axioms grover_one_step_exact
#print axioms grover_target_isolation
#print axioms diffusion_squared
#print axioms rotation_to_target
#print axioms S_rec_step0
#print axioms S_rec_step1
#print axioms grover_periodicity_six

end FableHilbertWalk20260819.H045

private def l5aProvenance : String :=
  "Origin: lean4/H045DiscreteGroverSearch.lean Claim: oracle_action AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
