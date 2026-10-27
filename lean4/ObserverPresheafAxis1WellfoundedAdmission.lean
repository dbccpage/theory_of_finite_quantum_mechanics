-- OPS-AXIS1-WELLFOUNDED-ADMISSION. Not a default target.
-- Three-candidate admission chain. The Genesis theorem collapsed_of_no_insts is not re-run.

namespace ObserverPresheafAxis1WellfoundedAdmission

def pred : Fin 3 → Option (Fin 3)
  | 0 => none
  | 1 => some 0
  | 2 => some 1

/-- Admission along the predecessor chain. Candidate 0 reads its base bit.
Candidate 1 reads its base bit or admission of 0. Candidate 2 reads its base bit or admission of 1. -/
def admitted (b : Fin 3 → Bool) : Fin 3 → Bool
  | 0 => b 0
  | 1 => b 1 || b 0
  | 2 => b 2 || (b 1 || b 0)

def noneBase : Fin 3 → Bool := fun _ => false

def zeroBase : Fin 3 → Bool
  | 0 => true
  | 1 => false
  | 2 => false

theorem pred0 : pred 0 = none := rfl
theorem pred1 : pred 1 = some 0 := rfl
theorem pred2 : pred 2 = some 1 := rfl

theorem adm0 (b : Fin 3 → Bool) : admitted b 0 = b 0 := rfl
theorem adm1 (b : Fin 3 → Bool) : admitted b 1 = (b 1 || admitted b 0) := rfl
theorem adm2 (b : Fin 3 → Bool) : admitted b 2 = (b 2 || admitted b 1) := rfl

theorem none0 : admitted noneBase 0 = false := rfl
theorem none1 : admitted noneBase 1 = false := rfl
theorem none2 : admitted noneBase 2 = false := rfl

theorem zb0 : zeroBase 0 = true := rfl
theorem zb1 : zeroBase 1 = false := rfl
theorem zb2 : zeroBase 2 = false := rfl

theorem zero0 : admitted zeroBase 0 = true := rfl
theorem zero1 : admitted zeroBase 1 = true := rfl
theorem zero2 : admitted zeroBase 2 = true := rfl

#print axioms pred0
#print axioms pred1
#print axioms pred2
#print axioms adm0
#print axioms adm1
#print axioms adm2
#print axioms none0
#print axioms none1
#print axioms none2
#print axioms zb0
#print axioms zb1
#print axioms zb2
#print axioms zero0
#print axioms zero1
#print axioms zero2

end ObserverPresheafAxis1WellfoundedAdmission
