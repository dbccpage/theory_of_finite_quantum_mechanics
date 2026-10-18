namespace QM.GOMC08A

structure ProbDist where
  p1 : Nat
  p2 : Nat
  sum_M : p1 + p2 = 100

def LinearReadout : ProbDist where
  p1 := 50
  p2 := 50
  sum_M := by decide

def QuadraticReadout : ProbDist where
  p1 := 20
  p2 := 80
  sum_M := by decide

theorem l1_does_not_uniquely_select_born :
    LinearReadout ≠ QuadraticReadout := by
  intro h
  have h_p1 : LinearReadout.p1 = QuadraticReadout.p1 := congrArg ProbDist.p1 h
  revert h_p1
  decide

end QM.GOMC08A
