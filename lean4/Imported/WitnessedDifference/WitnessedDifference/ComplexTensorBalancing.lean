/- Imported so that this repository carries its own Lean evidence.
   Original sha256: b360164d3aeef595ac9beb087a5e3ee5f54a65f58f1e5953229e045462030dfe (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.WitnessedDifference.WitnessedDifference.ComplexTensorBalancing
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-!
# Integer coefficient laws of the declared complex tensor balance

These are the two-component and four-component coefficient identities.
They do not formalize real positivity, density matrices, arbitrary matrix
dimensions, tensor universal properties or selection of complex scalars.
Division by two and ordered-field arguments are written separately.
-/
namespace WitnessedDifference.ComplexTensorBalancing

structure Pair where
  re : Int
  im : Int
  deriving DecidableEq

structure Quad where
  rr : Int
  ri : Int
  ir : Int
  ii : Int
  deriving DecidableEq

def balance (v : Quad) : Pair := ⟨v.rr-v.ii, v.ri+v.ir⟩
def sectionMap (z : Pair) : Quad := ⟨z.re,z.im,z.im,-z.re⟩
def twiceProject (v : Quad) : Quad := sectionMap (balance v)
def doublePair (z : Pair) : Pair := ⟨2*z.re,2*z.im⟩
def doubleQuad (v : Quad) : Quad := ⟨2*v.rr,2*v.ri,2*v.ir,2*v.ii⟩
def j (z : Pair) : Pair := ⟨-z.im,z.re⟩
def jLeft (v : Quad) : Quad := ⟨-v.ir,-v.ii,v.rr,v.ri⟩
def jRight (v : Quad) : Quad := ⟨-v.ri,v.rr,-v.ii,v.ir⟩
def negative (v : Quad) : Quad := ⟨-v.rr,-v.ri,-v.ir,-v.ii⟩
def subtract (v w : Quad) : Quad := ⟨v.rr-w.rr,v.ri-w.ri,v.ir-w.ir,v.ii-w.ii⟩
def mul (z w : Pair) : Pair := ⟨z.re*w.re-z.im*w.im,z.re*w.im+z.im*w.re⟩
def leftAction (z : Pair) (v : Quad) : Quad :=
  ⟨z.re*v.rr-z.im*v.ir,z.re*v.ri-z.im*v.ii,
   z.im*v.rr+z.re*v.ir,z.im*v.ri+z.re*v.ii⟩
def rightAction (z : Pair) (v : Quad) : Quad :=
  ⟨z.re*v.rr-z.im*v.ri,z.im*v.rr+z.re*v.ri,
   z.re*v.ir-z.im*v.ii,z.im*v.ir+z.re*v.ii⟩

theorem balance_section (z : Pair) : balance (sectionMap z) = doublePair z := by
  cases z
  simp only [balance,sectionMap,doublePair]
  congr 1 <;> omega

theorem twice_project_square (v : Quad) :
    twiceProject (twiceProject v) = doubleQuad (twiceProject v) := by
  cases v
  simp only [twiceProject,sectionMap,balance,doubleQuad]
  congr 1 <;> omega

theorem balance_kernel_iff (v : Quad) :
    balance v = ⟨0,0⟩ ↔ v.rr=v.ii ∧ v.ri = -v.ir := by
  constructor
  · intro h
    have hr := congrArg Pair.re h
    have hi := congrArg Pair.im h
    simp only [balance] at hr hi
    constructor <;> omega
  · rintro ⟨hr,hi⟩
    simp only [balance]
    congr 1 <;> omega

theorem j_left_square (v : Quad) : jLeft (jLeft v) = negative v := by
  cases v
  simp [jLeft,negative]

theorem j_right_square (v : Quad) : jRight (jRight v) = negative v := by
  cases v
  simp [jRight,negative]

theorem local_structures_commute (v : Quad) :
    jLeft (jRight v) = jRight (jLeft v) := by
  cases v
  simp [jLeft,jRight]

theorem balance_intertwines_left (v : Quad) : balance (jLeft v) = j (balance v) := by
  cases v
  simp only [balance,jLeft,j]
  congr 1 <;> omega

theorem balance_intertwines_right (v : Quad) : balance (jRight v) = j (balance v) := by
  cases v
  simp only [balance,jRight,j]
  congr 1 <;> omega

theorem twice_project_formula (v : Quad) :
    twiceProject v = subtract v (jLeft (jRight v)) := by
  cases v
  simp only [twiceProject,sectionMap,balance,subtract,jLeft,jRight]
  congr 1 <;> omega

theorem balance_annihilates_relation (v : Quad) :
    balance (subtract (jLeft v) (jRight v)) = ⟨0,0⟩ := by
  cases v
  simp only [balance,subtract,jLeft,jRight]
  congr 1 <;> omega

theorem kernel_is_relation_image (v : Quad) (h : balance v = ⟨0,0⟩) :
    ∃ w, subtract (jLeft w) (jRight w) = v := by
  rcases (balance_kernel_iff v).mp h with ⟨hr,hi⟩
  refine ⟨⟨0,0,-v.rr,-v.ri⟩,?_⟩
  cases v
  dsimp at hr hi
  simp only [subtract,jLeft,jRight]
  congr 1 <;> omega

theorem balance_left_action (z : Pair) (v : Quad) :
    balance (leftAction z v) = mul z (balance v) := by
  cases z
  cases v
  simp only [balance,leftAction,mul,Int.mul_add,Int.mul_sub]
  congr 1 <;> omega

theorem balance_right_action (z : Pair) (v : Quad) :
    balance (rightAction z v) = mul z (balance v) := by
  cases z
  cases v
  simp only [balance,rightAction,mul,Int.mul_add,Int.mul_sub]
  congr 1 <;> omega

theorem balance_associativity (a b c d e f g h : Int) :
    balance ⟨a-g,b-h,c+e,d+f⟩ = balance ⟨a-d,b+c,e-h,f+g⟩ := by
  simp only [balance]
  congr 1 <;> omega

end WitnessedDifference.ComplexTensorBalancing

#print axioms WitnessedDifference.ComplexTensorBalancing.balance_section
#print axioms WitnessedDifference.ComplexTensorBalancing.twice_project_square
#print axioms WitnessedDifference.ComplexTensorBalancing.balance_kernel_iff
#print axioms WitnessedDifference.ComplexTensorBalancing.j_left_square
#print axioms WitnessedDifference.ComplexTensorBalancing.j_right_square
#print axioms WitnessedDifference.ComplexTensorBalancing.local_structures_commute
#print axioms WitnessedDifference.ComplexTensorBalancing.balance_intertwines_left
#print axioms WitnessedDifference.ComplexTensorBalancing.balance_intertwines_right
#print axioms WitnessedDifference.ComplexTensorBalancing.twice_project_formula
#print axioms WitnessedDifference.ComplexTensorBalancing.balance_annihilates_relation
#print axioms WitnessedDifference.ComplexTensorBalancing.kernel_is_relation_image
#print axioms WitnessedDifference.ComplexTensorBalancing.balance_left_action
#print axioms WitnessedDifference.ComplexTensorBalancing.balance_right_action
#print axioms WitnessedDifference.ComplexTensorBalancing.balance_associativity
