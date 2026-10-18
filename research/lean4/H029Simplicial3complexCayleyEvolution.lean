

namespace FableHilbertWalk20260819.H029


theorem tetrahedron_euler_characteristic : (4 : Int) - 6 + 4 = 2 := by decide

structure TetChain1 where
  e01 : Int
  e02 : Int
  e03 : Int
  e12 : Int
  e13 : Int
  e23 : Int
  deriving DecidableEq, Repr

def zeroTet1 : TetChain1 := ⟨0, 0, 0, 0, 0, 0⟩

def addTet1 (c d : TetChain1) : TetChain1 :=
  ⟨c.e01 + d.e01, c.e02 + d.e02, c.e03 + d.e03,
   c.e12 + d.e12, c.e13 + d.e13, c.e23 + d.e23⟩

def subTet1 (c d : TetChain1) : TetChain1 :=
  ⟨c.e01 - d.e01, c.e02 - d.e02, c.e03 - d.e03,
   c.e12 - d.e12, c.e13 - d.e13, c.e23 - d.e23⟩

instance : Zero TetChain1 := ⟨zeroTet1⟩
instance : Add TetChain1 := ⟨addTet1⟩
instance : Sub TetChain1 := ⟨subTet1⟩

structure TetChain2 where
  f0 : Int
  f1 : Int
  f2 : Int
  f3 : Int
  deriving DecidableEq, Repr

structure TetChain3 where
  t0 : Int
  deriving DecidableEq, Repr

def tet_d2 (c : TetChain2) : TetChain1 :=
  ⟨c.f2 + c.f3,
   c.f1 - c.f3,
   -c.f1 - c.f2,
   c.f0 + c.f3,
   -c.f0 + c.f2,
   c.f0 + c.f1⟩

theorem tet_chain1_zero_ext (c : TetChain1)
    (h01 : c.e01 = 0) (h02 : c.e02 = 0) (h03 : c.e03 = 0)
    (h12 : c.e12 = 0) (h13 : c.e13 = 0) (h23 : c.e23 = 0) :
    c = zeroTet1 := by
  rcases c with ⟨e01, e02, e03, e12, e13, e23⟩
  dsimp [zeroTet1]
  congr

def tet_d3 (c : TetChain3) : TetChain2 :=
  ⟨c.t0, -c.t0, c.t0, -c.t0⟩

theorem tet_d2_comp_d3_nilpotent (c : TetChain3) :
    tet_d2 (tet_d3 c) = 0 := by
  apply tet_chain1_zero_ext <;> dsimp [tet_d2, tet_d3] <;> omega

theorem tet_d2_boundary_cancellation :
    tet_d2 (tet_d3 ⟨1⟩) = 0 := by
  apply tet_chain1_zero_ext <;> dsimp [tet_d2, tet_d3] <;> omega


theorem octahedron_euler_characteristic : (6 : Int) - 12 + 8 = 2 := by decide

structure OctChain1 where
  e0 : Int
  e1 : Int
  e2 : Int
  e3 : Int
  e4 : Int
  e5 : Int
  e6 : Int
  e7 : Int
  e8 : Int
  e9 : Int
  e10 : Int
  e11 : Int
  deriving DecidableEq, Repr

def zeroOct1 : OctChain1 := ⟨0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩

def addOct1 (c d : OctChain1) : OctChain1 :=
  ⟨c.e0 + d.e0, c.e1 + d.e1, c.e2 + d.e2, c.e3 + d.e3,
   c.e4 + d.e4, c.e5 + d.e5, c.e6 + d.e6, c.e7 + d.e7,
   c.e8 + d.e8, c.e9 + d.e9, c.e10 + d.e10, c.e11 + d.e11⟩

instance : Zero OctChain1 := ⟨zeroOct1⟩
instance : Add OctChain1 := ⟨addOct1⟩

structure OctChain2 where
  f0 : Int
  f1 : Int
  f2 : Int
  f3 : Int
  f4 : Int
  f5 : Int
  f6 : Int
  f7 : Int
  deriving DecidableEq, Repr

def oct_d2 (c : OctChain2) : OctChain1 :=
  ⟨c.f0 - c.f4,
   c.f1 - c.f5,
   c.f2 - c.f6,
   c.f3 - c.f7,
   -c.f0 + c.f3,
   c.f0 - c.f1,
   c.f1 - c.f2,
   c.f2 - c.f3,
   c.f4 - c.f7,
   -c.f4 + c.f5,
   -c.f5 + c.f6,
   -c.f6 + c.f7⟩

theorem oct_d2_boundary_cancellation :
    oct_d2 ⟨1, 1, 1, 1, 1, 1, 1, 1⟩ = 0 := by rfl


structure Cayley2 where
  m00 : Int
  m01 : Int
  m10 : Int
  m11 : Int
  deriving DecidableEq, Repr

def cayley_step (w : Int) : Cayley2 :=
  ⟨1 - w * w, -2 * w, 2 * w, 1 - w * w⟩

def check_cayley_diag (w : Int) : Bool :=
  let C := cayley_step w
  C.m00 * C.m00 + C.m10 * C.m10 == (1 + w * w) ^ 2

def check_cayley_off_diag (w : Int) : Bool :=
  let C := cayley_step w
  C.m00 * C.m01 + C.m10 * C.m11 == 0

theorem cayley_isometry_w0 :
    check_cayley_diag 0 = true ∧ check_cayley_off_diag 0 = true := by decide

theorem cayley_isometry_w1 :
    check_cayley_diag 1 = true ∧ check_cayley_off_diag 1 = true := by decide

theorem cayley_isometry_w2 :
    check_cayley_diag 2 = true ∧ check_cayley_off_diag 2 = true := by decide

theorem cayley_isometry_w_neg1 :
    check_cayley_diag (-1) = true ∧ check_cayley_off_diag (-1) = true := by decide

theorem cayley_isometry_w_neg2 :
    check_cayley_diag (-2) = true ∧ check_cayley_off_diag (-2) = true := by decide

#print axioms tetrahedron_euler_characteristic
#print axioms tet_d2_comp_d3_nilpotent
#print axioms tet_d2_boundary_cancellation
#print axioms octahedron_euler_characteristic
#print axioms oct_d2_boundary_cancellation
#print axioms cayley_isometry_w0
#print axioms cayley_isometry_w1
#print axioms cayley_isometry_w2
#print axioms cayley_isometry_w_neg1
#print axioms cayley_isometry_w_neg2

end FableHilbertWalk20260819.H029

private def l5aProvenance : String :=
  "Origin: lean4/H029Simplicial3complexCayleyEvolution.lean Claim: tetrahedron_euler_characteristic AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
