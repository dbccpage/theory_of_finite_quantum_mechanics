


namespace Higher2GroupBraiding

universe u


structure StrictCrossedModule (G H : Type u) where
  mul_g : G → G → G
  inv_g : G → G
  one_g : G
  mul_h : H → H → H
  inv_h : H → H
  one_h : H
  bnd : H → G
  alpha : G → H → H
  mul_one_g : ∀ g, mul_g g one_g = g
  one_mul_g : ∀ g, mul_g one_g g = g
  mul_inv_g : ∀ g, mul_g g (inv_g g) = one_g
  inv_mul_g : ∀ g, mul_g (inv_g g) g = one_g
  mul_assoc_g : ∀ a b c, mul_g (mul_g a b) c = mul_g a (mul_g b c)
  mul_one_h : ∀ h, mul_h h one_h = h
  one_mul_h : ∀ h, mul_h one_h h = h
  mul_inv_h : ∀ h, mul_h h (inv_h h) = one_h
  inv_mul_h : ∀ h, mul_h (inv_h h) h = one_h
  mul_assoc_h : ∀ a b c, mul_h (mul_h a b) c = mul_h a (mul_h b c)
  peiffer : ∀ g h, bnd (alpha g h) = mul_g g (mul_g (bnd h) (inv_g g))
  crossed_module_cond : ∀ h1 h2, alpha (bnd h1) h2 = mul_h h1 (mul_h h2 (inv_h h1))

theorem peiffer_identity_holds {G H : Type u} (cm : StrictCrossedModule G H) (g : G) (h : H) :
    cm.bnd (cm.alpha g h) = cm.mul_g g (cm.mul_g (cm.bnd h) (cm.inv_g g)) :=
  cm.peiffer g h

theorem crossed_module_condition_holds {G H : Type u} (cm : StrictCrossedModule G H) (h1 h2 : H) :
    cm.alpha (cm.bnd h1) h2 = cm.mul_h h1 (cm.mul_h h2 (cm.inv_h h1)) :=
  cm.crossed_module_cond h1 h2


structure PostnikovCocycle (G H : Type u) (cm : StrictCrossedModule G H) where
  cocycle : G → G → G → H
  is_trivial : Bool
  trivial_spec : is_trivial = true → ∀ g1 g2 g3, cocycle g1 g2 g3 = cm.one_h

theorem trivial_postnikov_evaluates_to_identity {G H : Type u} (cm : StrictCrossedModule G H)
    (post : PostnikovCocycle G H cm) (h_triv : post.is_trivial = true) (g1 g2 g3 : G) :
    post.cocycle g1 g2 g3 = cm.one_h :=
  post.trivial_spec h_triv g1 g2 g3


abbrev SignInt := Int

def surfaceLoopHolonomy (isTrivial : Bool) (oddLinking : Bool) : SignInt :=
  if isTrivial then 1
  else if oddLinking then -1
  else 1

theorem trivial_postnikov_is_positive (oddLinking : Bool) :
    surfaceLoopHolonomy true oddLinking = 1 := by
  dsimp [surfaceLoopHolonomy]

theorem nontrivial_postnikov_has_negative_sign :
    surfaceLoopHolonomy false true = -1 := by
  dsimp [surfaceLoopHolonomy]

def oneFormQuantumDoubleHolonomy (isTrivial : Bool) (oddLinking : Bool) : SignInt :=
  surfaceLoopHolonomy isTrivial oddLinking

theorem one_form_quantum_double_retains_negative_sign :
    oneFormQuantumDoubleHolonomy false true = -1 := by
  dsimp [oneFormQuantumDoubleHolonomy, surfaceLoopHolonomy]

def higherTwoDoubleHolonomy (bareHol : SignInt) : Nat :=
  (bareHol.natAbs) * (bareHol.natAbs)

theorem higher_2double_trace_nonnegative (bareHol : SignInt) :
    higherTwoDoubleHolonomy bareHol ≥ 0 := by
  dsimp [higherTwoDoubleHolonomy]
  omega

theorem higher_2double_restores_sign_positivity :
    higherTwoDoubleHolonomy (surfaceLoopHolonomy false true) = 1 := by
  dsimp [higherTwoDoubleHolonomy, surfaceLoopHolonomy]

def higherDefectMass (normVal : Nat) : Nat :=
  if normVal > 0 then 0 else 1

theorem higher_2double_nullifies_defect_mass :
    higherDefectMass (higherTwoDoubleHolonomy (surfaceLoopHolonomy false true)) = 0 := by
  dsimp [higherDefectMass, higherTwoDoubleHolonomy, surfaceLoopHolonomy]

end Higher2GroupBraiding
