-- PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY. Not a default target.
-- Integer triangle slice. A general cost, a real or complex repair space,
-- and weighted duality on an arbitrary complex stay outside this module.


namespace PregenesisWdpPhiWellDefinedL1Duality
def d0 (f0 f1 f2 : Int) : Int × Int × Int :=
  (f1 - f0, f2 - f1, f2 - f0)

def add3 (a b : Int × Int × Int) : Int × Int × Int :=
  (a.1 + b.1, a.2.1 + b.2.1, a.2.2 + b.2.2)

def sub3 (a b : Int × Int × Int) : Int × Int × Int :=
  (a.1 - b.1, a.2.1 - b.2.1, a.2.2 - b.2.2)

def absSum (v : Int × Int × Int) : Nat :=
  v.1.natAbs + v.2.1.natAbs + v.2.2.natAbs

def pair110 (v : Int × Int × Int) : Int :=
  v.1 + v.2.1 - v.2.2

theorem d0_linear (f0 f1 f2 g0 g1 g2 : Int) :
    d0 (f0 + g0) (f1 + g1) (f2 + g2)
      = add3 (d0 f0 f1 f2) (d0 g0 g1 g2) := by
  simp [d0, add3]
  constructor
  · omega
  · constructor
    · omega
    · omega

theorem residual_shift (d0v d1v d2v f0 f1 f2 g0 g1 g2 : Int) :
    sub3 (add3 (d0v, d1v, d2v) (d0 g0 g1 g2))
        (d0 (f0 + g0) (f1 + g1) (f2 + g2))
      = sub3 (d0v, d1v, d2v) (d0 f0 f1 f2) := by
  rw [d0_linear]
  simp [sub3, add3]
  constructor
  · omega
  · constructor
    · omega
    · omega

theorem absSum_shift (d0v d1v d2v f0 f1 f2 g0 g1 g2 : Int) :
    absSum (sub3 (add3 (d0v, d1v, d2v) (d0 g0 g1 g2))
        (d0 (f0 + g0) (f1 + g1) (f2 + g2)))
      = absSum (sub3 (d0v, d1v, d2v) (d0 f0 f1 f2)) := by
  rw [residual_shift]

theorem pair_d0_zero (f0 f1 f2 : Int) : pair110 (d0 f0 f1 f2) = 0 := by
  simp [pair110, d0]
  omega

theorem pair_residual (f0 f1 f2 : Int) :
    pair110 (sub3 (1, 1, 0) (d0 f0 f1 f2)) = 2 := by
  simp [pair110, sub3, d0]
  omega

theorem natAbs_pair_le_absSum (v : Int × Int × Int) :
    (pair110 v).natAbs ≤ absSum v := by
  simp [pair110, absSum]
  have hsub : v.1 + v.2.1 - v.2.2 = v.1 + v.2.1 + -v.2.2 := by omega
  rw [hsub]
  calc
    (v.1 + v.2.1 + -v.2.2).natAbs
        ≤ (v.1 + v.2.1).natAbs + (-v.2.2).natAbs := Int.natAbs_add_le _ _
    _ = (v.1 + v.2.1).natAbs + v.2.2.natAbs := by rw [Int.natAbs_neg]
    _ ≤ v.1.natAbs + v.2.1.natAbs + v.2.2.natAbs := by
          exact Nat.add_le_add (Int.natAbs_add_le _ _) (Nat.le_refl _)

theorem absSum_ge_two (f0 f1 f2 : Int) :
    2 ≤ absSum (sub3 (1, 1, 0) (d0 f0 f1 f2)) := by
  have hle := natAbs_pair_le_absSum (sub3 (1, 1, 0) (d0 f0 f1 f2))
  have hpair := pair_residual f0 f1 f2
  rw [hpair] at hle
  simpa using hle

theorem absSum_attained : absSum (sub3 (1, 1, 0) (d0 0 1 0)) = 2 := by
  simp [absSum, sub3, d0]

theorem shifted_ge (g0 g1 g2 f0 f1 f2 : Int) :
    2 ≤ absSum (sub3 (add3 (1, 1, 0) (d0 g0 g1 g2))
        (d0 (f0 + g0) (f1 + g1) (f2 + g2))) := by
  rw [absSum_shift]
  exact absSum_ge_two f0 f1 f2

theorem shifted_attained (g0 g1 g2 : Int) :
    absSum (sub3 (add3 (1, 1, 0) (d0 g0 g1 g2))
        (d0 (0 + g0) (1 + g1) (0 + g2))) = 2 := by
  rw [absSum_shift]
  exact absSum_attained

#print axioms d0_linear
#print axioms residual_shift
#print axioms absSum_shift
#print axioms pair_d0_zero
#print axioms pair_residual
#print axioms natAbs_pair_le_absSum
#print axioms absSum_ge_two
#print axioms absSum_attained
#print axioms shifted_ge
#print axioms shifted_attained

end PregenesisWdpPhiWellDefinedL1Duality
