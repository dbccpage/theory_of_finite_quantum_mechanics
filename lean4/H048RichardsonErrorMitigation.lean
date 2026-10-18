

namespace FableHilbertWalk20260819.H048

def scales1 : List Int := [1, 2]
def weights1 : List Int := [2, -1]

theorem linear_weight_sum : weights1.foldl (· + ·) 0 = 1 := by decide

theorem linear_moment1_cancelled :
    (List.zipWith (· * ·) weights1 scales1).foldl (· + ·) 0 = 0 := by decide

theorem linear_variance_amplification :
    (List.map (fun w => if w < 0 then -w else w) weights1).foldl (· + ·) 0 = 3 := by decide

def scales2 : List Int := [1, 2, 3]
def weights2 : List Int := [3, -3, 1]

theorem quadratic_weight_sum : weights2.foldl (· + ·) 0 = 1 := by decide

theorem quadratic_moment1_cancelled :
    (List.zipWith (· * ·) weights2 scales2).foldl (· + ·) 0 = 0 := by decide

theorem quadratic_moment2_cancelled :
    (List.zipWith (· * ·) weights2 (List.map (fun x => x * x) scales2)).foldl (· + ·) 0 = 0 := by decide

theorem quadratic_variance_amplification :
    (List.map (fun w => if w < 0 then -w else w) weights2).foldl (· + ·) 0 = 7 := by decide

def scales3 : List Int := [1, 2, 3, 4]
def weights3 : List Int := [4, -6, 4, -1]

theorem cubic_weight_sum : weights3.foldl (· + ·) 0 = 1 := by decide

theorem cubic_moment1_cancelled :
    (List.zipWith (· * ·) weights3 scales3).foldl (· + ·) 0 = 0 := by decide

theorem cubic_moment2_cancelled :
    (List.zipWith (· * ·) weights3 (List.map (fun x => x * x) scales3)).foldl (· + ·) 0 = 0 := by decide

theorem cubic_moment3_cancelled :
    (List.zipWith (· * ·) weights3 (List.map (fun x => x * x * x) scales3)).foldl (· + ·) 0 = 0 := by decide

theorem cubic_variance_amplification :
    (List.map (fun w => if w < 0 then -w else w) weights3).foldl (· + ·) 0 = 15 := by decide

def noisy_eval (E0 c1 c2 c3 : Int) (lam : Int) : Int :=
  E0 + c1 * lam + c2 * lam * lam + c3 * lam * lam * lam

theorem richardson_cubic_exact_recovery (E0 c1 c2 c3 : Int) :
    4 * noisy_eval E0 c1 c2 c3 1 -
    6 * noisy_eval E0 c1 c2 c3 2 +
    4 * noisy_eval E0 c1 c2 c3 3 -
    1 * noisy_eval E0 c1 c2 c3 4 = E0 := by
  dsimp [noisy_eval]
  omega

theorem richardson_linear_exact_recovery (E0 c1 : Int) :
    2 * (E0 + c1 * 1) - 1 * (E0 + c1 * 2) = E0 := by
  omega

theorem richardson_quadratic_exact_recovery (E0 c1 c2 : Int) :
    3 * (E0 + c1 * 1 + c2 * 1) -
    3 * (E0 + c1 * 2 + c2 * 4) +
    1 * (E0 + c1 * 3 + c2 * 9) = E0 := by
  omega

#print axioms linear_weight_sum
#print axioms linear_moment1_cancelled
#print axioms linear_variance_amplification
#print axioms quadratic_weight_sum
#print axioms quadratic_moment1_cancelled
#print axioms quadratic_moment2_cancelled
#print axioms quadratic_variance_amplification
#print axioms cubic_weight_sum
#print axioms cubic_moment1_cancelled
#print axioms cubic_moment2_cancelled
#print axioms cubic_moment3_cancelled
#print axioms cubic_variance_amplification
#print axioms richardson_cubic_exact_recovery
#print axioms richardson_linear_exact_recovery
#print axioms richardson_quadratic_exact_recovery

end FableHilbertWalk20260819.H048

private def l5aProvenance : String :=
  "Origin: lean4/H048RichardsonErrorMitigation.lean Claim: linear_weight_sum AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
