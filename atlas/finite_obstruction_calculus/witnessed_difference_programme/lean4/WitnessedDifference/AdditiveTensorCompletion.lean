/-!
# Free alternatives, signed completion, and algebraic tensor composition

This module starts only after a type `X` of admitted generators has been
supplied.  Finite lists are quotiented by equality under every commutative
monoid interpretation.  The resulting carrier is the free commutative monoid
of finite alternatives.  Signed list pairs are quotiented by equality under
every abelian-group interpretation.  The resulting carrier is the free
abelian group and is the Grothendieck completion of the alternative carrier by
its universal extension property.

For two generator types, the free abelian group on pairs is then proved to be
the tensor object for biadditive maps between the two free abelian groups.
This is an algebraic construction.  It does not select complex scalars, a
norm, an involution, positivity, Hilbert completion, probabilities, or quantum
readout.

Lean core only.  The quotients use semantic equality, so their universal
properties are definitions followed by uniqueness proofs rather than imported
algebraic machinery.
-/

namespace WitnessedDifference.AdditiveTensorCompletion

universe u

set_option linter.checkUnivs false

/-! ## Explicit algebraic targets -/

/-- A commutative monoid, with every law carried explicitly. -/
structure CommMonoid where
  Carrier : Type u
  zero : Carrier
  add : Carrier → Carrier → Carrier
  zero_add : ∀ x, add zero x = x
  add_zero : ∀ x, add x zero = x
  add_assoc : ∀ x y z, add (add x y) z = add x (add y z)
  add_comm : ∀ x y, add x y = add y x

/-- An abelian group.  The inverse-distribution laws are included explicitly
so that the file remains independent of a typeclass library. -/
structure AbelianGroup extends CommMonoid where
  neg : Carrier → Carrier
  add_neg : ∀ x, add x (neg x) = zero
  neg_zero : neg zero = zero
  neg_add : ∀ x y, neg (add x y) = add (neg x) (neg y)
  neg_neg : ∀ x, neg (neg x) = x

namespace CommMonoid

/-- Four-term interchange follows from associativity and commutativity. -/
theorem interchange (M : CommMonoid) (a b c d : M.Carrier) :
    M.add (M.add a b) (M.add c d) = M.add (M.add a c) (M.add b d) := by
  calc
    M.add (M.add a b) (M.add c d) = M.add a (M.add b (M.add c d)) :=
      M.add_assoc a b (M.add c d)
    _ = M.add a (M.add (M.add b c) d) :=
      congrArg (M.add a) (M.add_assoc b c d).symm
    _ = M.add a (M.add (M.add c b) d) :=
      congrArg (fun x => M.add a (M.add x d)) (M.add_comm b c)
    _ = M.add a (M.add c (M.add b d)) :=
      congrArg (M.add a) (M.add_assoc c b d)
    _ = M.add (M.add a c) (M.add b d) :=
      (M.add_assoc a c (M.add b d)).symm

end CommMonoid

/-! ## Free finite alternatives -/

/-- Evaluation of a finite word in a commutative monoid. -/
def evalList {X : Type u} (M : CommMonoid.{u}) (f : X → M.Carrier) :
    List X → M.Carrier
  | [] => M.zero
  | x :: xs => M.add (f x) (evalList M f xs)

theorem evalList_append {X : Type u} (M : CommMonoid.{u}) (f : X → M.Carrier)
    (xs ys : List X) :
    evalList M f (xs ++ ys) = M.add (evalList M f xs) (evalList M f ys) := by
  induction xs with
  | nil => exact (M.zero_add (evalList M f ys)).symm
  | cons x xs ih =>
      change M.add (f x) (evalList M f (xs ++ ys)) =
        M.add (M.add (f x) (evalList M f xs)) (evalList M f ys)
      rw [ih]
      exact (M.add_assoc (f x) (evalList M f xs) (evalList M f ys)).symm

/-- Two finite words represent the same alternative exactly when every
commutative-monoid interpretation gives them the same value. -/
def AlternativeEq {X : Type u} (xs ys : List X) : Prop :=
  ∀ (M : CommMonoid.{u}) (f : X → M.Carrier), evalList M f xs = evalList M f ys

theorem alternativeEq_refl {X : Type u} (xs : List X) : AlternativeEq xs xs := by
  intro M f
  rfl

theorem alternativeEq_symm {X : Type u} {xs ys : List X}
    (h : AlternativeEq xs ys) : AlternativeEq ys xs := by
  intro M f
  exact (h M f).symm

theorem alternativeEq_trans {X : Type u} {xs ys zs : List X}
    (h₁ : AlternativeEq xs ys) (h₂ : AlternativeEq ys zs) : AlternativeEq xs zs := by
  intro M f
  exact (h₁ M f).trans (h₂ M f)

theorem alternativeEq_append {X : Type u} {xs xs' ys ys' : List X}
    (hx : AlternativeEq xs xs') (hy : AlternativeEq ys ys') :
    AlternativeEq (xs ++ ys) (xs' ++ ys') := by
  intro M f
  rw [evalList_append, evalList_append, hx M f, hy M f]

def alternativeSetoid (X : Type u) : Setoid (List X) where
  r := AlternativeEq
  iseqv := {
    refl := alternativeEq_refl
    symm := alternativeEq_symm
    trans := alternativeEq_trans
  }

/-- The free commutative monoid of finite alternatives. -/
abbrev Alternative (X : Type u) := Quotient (alternativeSetoid X)

def alternativeMk {X : Type u} (xs : List X) : Alternative X :=
  Quotient.mk (alternativeSetoid X) xs

def alternativeZero {X : Type u} : Alternative X := alternativeMk []

def alternativeUnit {X : Type u} (x : X) : Alternative X := alternativeMk [x]

def alternativeAdd {X : Type u} : Alternative X → Alternative X → Alternative X :=
  Quotient.lift₂
    (fun xs ys => alternativeMk (xs ++ ys))
    (fun _ _ _ _ hx hy => Quotient.sound (alternativeEq_append hx hy))

theorem alternative_add_zero {X : Type u} (a : Alternative X) :
    alternativeAdd a alternativeZero = a := by
  refine Quotient.inductionOn a ?_
  intro xs
  change alternativeMk (xs ++ []) = alternativeMk xs
  rw [List.append_nil]

theorem alternative_zero_add {X : Type u} (a : Alternative X) :
    alternativeAdd alternativeZero a = a := by
  refine Quotient.inductionOn a ?_
  intro xs
  rfl

theorem alternative_add_assoc {X : Type u} (a b c : Alternative X) :
    alternativeAdd (alternativeAdd a b) c = alternativeAdd a (alternativeAdd b c) := by
  refine Quotient.inductionOn a ?_
  intro xs
  refine Quotient.inductionOn b ?_
  intro ys
  refine Quotient.inductionOn c ?_
  intro zs
  change alternativeMk ((xs ++ ys) ++ zs) = alternativeMk (xs ++ (ys ++ zs))
  rw [List.append_assoc]

theorem alternative_add_comm {X : Type u} (a b : Alternative X) :
    alternativeAdd a b = alternativeAdd b a := by
  refine Quotient.inductionOn a ?_
  intro xs
  refine Quotient.inductionOn b ?_
  intro ys
  apply Quotient.sound
  intro M f
  rw [evalList_append, evalList_append]
  exact M.add_comm (evalList M f xs) (evalList M f ys)

/-- The canonical fold from alternatives to a declared commutative monoid. -/
def alternativeLift {X : Type u} (M : CommMonoid.{u}) (f : X → M.Carrier) :
    Alternative X → M.Carrier :=
  Quotient.lift (evalList M f) (fun _ _ h => h M f)

theorem alternativeLift_zero {X : Type u} (M : CommMonoid.{u}) (f : X → M.Carrier) :
    alternativeLift M f alternativeZero = M.zero := rfl

theorem alternativeLift_unit {X : Type u} (M : CommMonoid.{u}) (f : X → M.Carrier)
    (x : X) : alternativeLift M f (alternativeUnit x) = f x := by
  exact M.add_zero (f x)

theorem alternativeLift_add {X : Type u} (M : CommMonoid.{u}) (f : X → M.Carrier)
    (a b : Alternative X) :
    alternativeLift M f (alternativeAdd a b) =
      M.add (alternativeLift M f a) (alternativeLift M f b) := by
  refine Quotient.inductionOn a ?_
  intro xs
  refine Quotient.inductionOn b ?_
  intro ys
  exact evalList_append M f xs ys

/-- The free-alternative fold is the unique map preserving zero, addition,
and every admitted generator. -/
theorem alternativeLift_unique {X : Type u} (M : CommMonoid.{u}) (f : X → M.Carrier)
    (h : Alternative X → M.Carrier)
    (hzero : h alternativeZero = M.zero)
    (hadd : ∀ a b, h (alternativeAdd a b) = M.add (h a) (h b))
    (hunit : ∀ x, h (alternativeUnit x) = f x) :
    ∀ a, h a = alternativeLift M f a := by
  intro a
  refine Quotient.inductionOn a ?_
  intro xs
  induction xs with
  | nil => exact hzero
  | cons x xs ih =>
      change h (alternativeMk (x :: xs)) = evalList M f (x :: xs)
      have hdecomp : alternativeMk (x :: xs) =
          alternativeAdd (alternativeUnit x) (alternativeMk xs) := rfl
      have ih' : h (alternativeMk xs) = evalList M f xs := ih
      rw [hdecomp, hadd, hunit, ih']
      rfl

/-! ## Free signed completion -/

/-- Evaluation of a positive/negative word pair in an abelian group. -/
def evalSigned {X : Type u} (G : AbelianGroup.{u}) (f : X → G.Carrier)
    (pair : List X × List X) : G.Carrier :=
  G.add (evalList G.toCommMonoid f pair.1)
    (G.neg (evalList G.toCommMonoid f pair.2))

/-- Semantic equality of signed expressions. -/
def SignedEq {X : Type u} (p q : List X × List X) : Prop :=
  ∀ (G : AbelianGroup.{u}) (f : X → G.Carrier), evalSigned G f p = evalSigned G f q

theorem signedEq_refl {X : Type u} (p : List X × List X) : SignedEq p p := by
  intro G f
  rfl

theorem signedEq_symm {X : Type u} {p q : List X × List X}
    (h : SignedEq p q) : SignedEq q p := by
  intro G f
  exact (h G f).symm

theorem signedEq_trans {X : Type u} {p q r : List X × List X}
    (h₁ : SignedEq p q) (h₂ : SignedEq q r) : SignedEq p r := by
  intro G f
  exact (h₁ G f).trans (h₂ G f)

def signedSetoid (X : Type u) : Setoid (List X × List X) where
  r := SignedEq
  iseqv := {
    refl := signedEq_refl
    symm := signedEq_symm
    trans := signedEq_trans
  }

/-- The free abelian group on the admitted generators. -/
abbrev Signed (X : Type u) := Quotient (signedSetoid X)

def signedMk {X : Type u} (p : List X × List X) : Signed X :=
  Quotient.mk (signedSetoid X) p

def signedZero {X : Type u} : Signed X := signedMk ([], [])

def signedUnit {X : Type u} (x : X) : Signed X := signedMk ([x], [])

theorem evalSigned_add_pair {X : Type u} (G : AbelianGroup.{u})
    (f : X → G.Carrier) (p q : List X × List X) :
    evalSigned G f (p.1 ++ q.1, p.2 ++ q.2) =
      G.add (evalSigned G f p) (evalSigned G f q) := by
  simp only [evalSigned, evalList_append, G.neg_add]
  exact G.toCommMonoid.interchange _ _ _ _

theorem evalSigned_neg_pair {X : Type u} (G : AbelianGroup.{u})
    (f : X → G.Carrier) (p : List X × List X) :
    evalSigned G f (p.2, p.1) = G.neg (evalSigned G f p) := by
  simp only [evalSigned, G.neg_add, G.neg_neg]
  exact G.add_comm _ _

theorem signedEq_add {X : Type u} {p p' q q' : List X × List X}
    (hp : SignedEq p p') (hq : SignedEq q q') :
    SignedEq (p.1 ++ q.1, p.2 ++ q.2) (p'.1 ++ q'.1, p'.2 ++ q'.2) := by
  intro G f
  rw [evalSigned_add_pair, evalSigned_add_pair, hp G f, hq G f]

theorem signedEq_neg {X : Type u} {p q : List X × List X}
    (h : SignedEq p q) : SignedEq (p.2, p.1) (q.2, q.1) := by
  intro G f
  rw [evalSigned_neg_pair, evalSigned_neg_pair, h G f]

def signedAdd {X : Type u} : Signed X → Signed X → Signed X :=
  Quotient.lift₂
    (fun p q => signedMk (p.1 ++ q.1, p.2 ++ q.2))
    (fun _ _ _ _ hp hq => Quotient.sound (signedEq_add hp hq))

def signedNeg {X : Type u} : Signed X → Signed X :=
  Quotient.lift (fun p => signedMk (p.2, p.1))
    (fun _ _ h => Quotient.sound (signedEq_neg h))

theorem signed_zero_add {X : Type u} (a : Signed X) :
    signedAdd signedZero a = a := by
  refine Quotient.inductionOn a ?_
  intro p
  cases p
  rfl

theorem signed_add_zero {X : Type u} (a : Signed X) :
    signedAdd a signedZero = a := by
  refine Quotient.inductionOn a ?_
  intro p
  cases p with
  | mk ps ns =>
      change signedMk (ps ++ [], ns ++ []) = signedMk (ps, ns)
      rw [List.append_nil, List.append_nil]

theorem signed_add_assoc {X : Type u} (a b c : Signed X) :
    signedAdd (signedAdd a b) c = signedAdd a (signedAdd b c) := by
  refine Quotient.inductionOn a ?_
  intro p
  refine Quotient.inductionOn b ?_
  intro q
  refine Quotient.inductionOn c ?_
  intro r
  cases p with
  | mk ps ns =>
    cases q with
    | mk qs ms =>
      cases r with
      | mk rs ls =>
        change signedMk ((ps ++ qs) ++ rs, (ns ++ ms) ++ ls) =
          signedMk (ps ++ (qs ++ rs), ns ++ (ms ++ ls))
        rw [List.append_assoc, List.append_assoc]

theorem signed_add_comm {X : Type u} (a b : Signed X) :
    signedAdd a b = signedAdd b a := by
  refine Quotient.inductionOn a ?_
  intro p
  refine Quotient.inductionOn b ?_
  intro q
  apply Quotient.sound
  intro G f
  rw [evalSigned_add_pair, evalSigned_add_pair]
  exact G.add_comm _ _

theorem signed_neg_zero {X : Type u} : signedNeg (signedZero : Signed X) = signedZero := rfl

theorem signed_neg_add {X : Type u} (a b : Signed X) :
    signedNeg (signedAdd a b) = signedAdd (signedNeg a) (signedNeg b) := by
  refine Quotient.inductionOn a ?_
  intro p
  refine Quotient.inductionOn b ?_
  intro q
  apply Quotient.sound
  intro G f
  rw [evalSigned_neg_pair, evalSigned_add_pair, G.neg_add]

theorem signed_neg_neg {X : Type u} (a : Signed X) : signedNeg (signedNeg a) = a := by
  refine Quotient.inductionOn a ?_
  intro p
  cases p
  rfl

theorem signed_add_neg {X : Type u} (a : Signed X) :
    signedAdd a (signedNeg a) = signedZero := by
  refine Quotient.inductionOn a ?_
  intro p
  apply Quotient.sound
  intro G f
  change evalSigned G f (p.1 ++ p.2, p.2 ++ p.1) = evalSigned G f ([], [])
  simp only [evalSigned, evalList_append, evalList, G.neg_zero, G.add_zero]
  rw [G.add_comm (evalList G.toCommMonoid f p.2)
    (evalList G.toCommMonoid f p.1), G.add_neg]

/-- The quotient carries the required abelian-group structure. -/
abbrev signedGroup (X : Type u) : AbelianGroup.{u} where
  Carrier := Signed X
  zero := signedZero
  add := signedAdd
  zero_add := signed_zero_add
  add_zero := signed_add_zero
  add_assoc := signed_add_assoc
  add_comm := signed_add_comm
  neg := signedNeg
  add_neg := signed_add_neg
  neg_zero := signed_neg_zero
  neg_add := signed_neg_add
  neg_neg := signed_neg_neg

/-- The canonical homomorphism from alternatives to their signed completion. -/
def alternativeToSigned {X : Type u} : Alternative X → Signed X :=
  Quotient.lift (fun xs => signedMk (xs, [])) (by
    intro xs ys h
    apply Quotient.sound
    intro G f
    simp only [evalSigned, evalList, G.neg_zero, G.add_zero]
    exact h G.toCommMonoid f)

theorem alternativeToSigned_zero {X : Type u} :
    alternativeToSigned (alternativeZero : Alternative X) = signedZero := rfl

theorem alternativeToSigned_unit {X : Type u} (x : X) :
    alternativeToSigned (alternativeUnit x) = signedUnit x := rfl

theorem alternativeToSigned_add {X : Type u} (a b : Alternative X) :
    alternativeToSigned (alternativeAdd a b) =
      signedAdd (alternativeToSigned a) (alternativeToSigned b) := by
  refine Quotient.inductionOn a ?_
  intro xs
  refine Quotient.inductionOn b ?_
  intro ys
  rfl

/-- Every signed expression is a difference of two finite alternatives. -/
theorem signed_is_difference {X : Type u} (s : Signed X) :
    ∃ p n : Alternative X,
      s = signedAdd (alternativeToSigned p) (signedNeg (alternativeToSigned n)) := by
  refine Quotient.inductionOn s ?_
  intro pair
  refine ⟨alternativeMk pair.1, alternativeMk pair.2, ?_⟩
  cases pair with
  | mk ps ns =>
      change signedMk (ps, ns) = signedMk (ps ++ [], [] ++ ns)
      rw [List.append_nil, List.nil_append]

/-! ## Universal property of the signed completion -/

/-- A homomorphism between explicit abelian groups. -/
structure GroupHom (A B : AbelianGroup.{u}) where
  toFun : A.Carrier → B.Carrier
  map_zero : toFun A.zero = B.zero
  map_add : ∀ x y, toFun (A.add x y) = B.add (toFun x) (toFun y)
  map_neg : ∀ x, toFun (A.neg x) = B.neg (toFun x)

theorem GroupHom.ext {A B : AbelianGroup} (h k : GroupHom A B)
    (pointwise : ∀ x, h.toFun x = k.toFun x) : h = k := by
  cases h with
  | mk hf h0 ha hn =>
      cases k with
      | mk kf k0 ka kn =>
          have hfun : hf = kf := funext pointwise
          cases hfun
          rfl

/-- The canonical signed fold into any abelian group. -/
def signedLift {X : Type u} (G : AbelianGroup.{u}) (f : X → G.Carrier) :
    Signed X → G.Carrier :=
  Quotient.lift (evalSigned G f) (fun _ _ h => h G f)

theorem signedLift_zero {X : Type u} (G : AbelianGroup.{u}) (f : X → G.Carrier) :
    signedLift G f signedZero = G.zero := by
  change evalSigned G f ([], []) = G.zero
  simp only [evalSigned, evalList, G.neg_zero, G.add_zero]

theorem signedLift_unit {X : Type u} (G : AbelianGroup.{u}) (f : X → G.Carrier)
    (x : X) : signedLift G f (signedUnit x) = f x := by
  change evalSigned G f ([x], []) = f x
  simp only [evalSigned, evalList, G.neg_zero, G.add_zero]

theorem signedLift_add {X : Type u} (G : AbelianGroup.{u}) (f : X → G.Carrier)
    (a b : Signed X) :
    signedLift G f (signedAdd a b) = G.add (signedLift G f a) (signedLift G f b) := by
  refine Quotient.inductionOn a ?_
  intro p
  refine Quotient.inductionOn b ?_
  intro q
  exact evalSigned_add_pair G f p q

theorem signedLift_neg {X : Type u} (G : AbelianGroup.{u}) (f : X → G.Carrier)
    (a : Signed X) : signedLift G f (signedNeg a) = G.neg (signedLift G f a) := by
  refine Quotient.inductionOn a ?_
  intro p
  exact evalSigned_neg_pair G f p

def signedLiftHom {X : Type u} (G : AbelianGroup.{u}) (f : X → G.Carrier) :
    GroupHom (signedGroup X) G where
  toFun := signedLift G f
  map_zero := signedLift_zero G f
  map_add := signedLift_add G f
  map_neg := signedLift_neg G f

theorem signedLift_positive_list {X : Type u} (G : AbelianGroup.{u})
    (f : X → G.Carrier) (xs : List X) :
    signedLift G f (signedMk (xs, [])) = evalList G.toCommMonoid f xs := by
  change evalSigned G f (xs, []) = evalList G.toCommMonoid f xs
  simp only [evalSigned, evalList, G.neg_zero, G.add_zero]

/-- Every group homomorphism out of the signed carrier is determined by its
values on admitted generators. -/
theorem signedHom_eq_lift {X : Type u} (G : AbelianGroup.{u})
    (h : GroupHom (signedGroup X) G) :
    h = signedLiftHom G (fun x => h.toFun (signedUnit x)) := by
  apply GroupHom.ext
  intro s
  refine Quotient.inductionOn s ?_
  intro pair
  change h.toFun (signedMk pair) =
    evalSigned G (fun x => h.toFun (signedUnit x)) pair
  have positive : ∀ xs : List X,
      h.toFun (signedMk (xs, [])) =
        evalList G.toCommMonoid (fun x => h.toFun (signedUnit x)) xs := by
    intro xs
    induction xs with
    | nil => exact h.map_zero
    | cons x xs ih =>
        have decomp : signedMk (x :: xs, []) =
            signedAdd (signedUnit x) (signedMk (xs, [])) := rfl
        rw [decomp, h.map_add, ih]
        rfl
  have decomp : signedMk pair = signedAdd (signedMk (pair.1, []))
      (signedNeg (signedMk (pair.2, []))) := by
    cases pair with
    | mk ps ns =>
        change signedMk (ps, ns) = signedMk (ps ++ [], [] ++ ns)
        rw [List.append_nil, List.nil_append]
  rw [decomp, h.map_add, h.map_neg, positive, positive]
  rfl

/-- Grothendieck extension: every alternative-monoid map into an abelian group
extends uniquely to the signed carrier. -/
theorem grothendieck_extension {X : Type u} (G : AbelianGroup.{u})
    (h : Alternative X → G.Carrier)
    (hzero : h alternativeZero = G.zero)
    (hadd : ∀ a b, h (alternativeAdd a b) = G.add (h a) (h b)) :
    ∃ k : GroupHom (signedGroup X) G,
      (∀ a, k.toFun (alternativeToSigned a) = h a) ∧
      ∀ k' : GroupHom (signedGroup X) G,
        (∀ a, k'.toFun (alternativeToSigned a) = h a) → k' = k := by
  let f : X → G.Carrier := fun x => h (alternativeUnit x)
  let k : GroupHom (signedGroup X) G := signedLiftHom G f
  refine ⟨k, ?_, ?_⟩
  · intro a
    refine Quotient.inductionOn a ?_
    intro xs
    change signedLift G f (signedMk (xs, [])) = h (alternativeMk xs)
    rw [signedLift_positive_list]
    symm
    exact alternativeLift_unique G.toCommMonoid f h hzero hadd (fun _ => rfl)
      (alternativeMk xs)
  · intro k' hk'
    have generators : ∀ x, k'.toFun (signedUnit x) = f x := by
      intro x
      exact hk' (alternativeUnit x)
    calc
      k' = signedLiftHom G (fun x => k'.toFun (signedUnit x)) := signedHom_eq_lift G k'
      _ = signedLiftHom G f := by
        apply GroupHom.ext
        intro s
        apply congrArg (fun g => signedLift G g s)
        funext x
        exact generators x
      _ = k := rfl

/-! ## Tensor object for independent biadditive composition -/

/-- Pointwise abelian-group structure on homomorphisms. -/
def zeroHom (A B : AbelianGroup.{u}) : GroupHom A B where
  toFun := fun _ => B.zero
  map_zero := rfl
  map_add := fun _ _ => (B.zero_add B.zero).symm
  map_neg := fun _ => B.neg_zero.symm

def addHom {A B : AbelianGroup.{u}} (h k : GroupHom A B) : GroupHom A B where
  toFun := fun x => B.add (h.toFun x) (k.toFun x)
  map_zero := by rw [h.map_zero, k.map_zero, B.zero_add]
  map_add := by
    intro x y
    rw [h.map_add, k.map_add]
    exact B.toCommMonoid.interchange _ _ _ _
  map_neg := by intro x; rw [h.map_neg, k.map_neg, B.neg_add]

def negHom {A B : AbelianGroup.{u}} (h : GroupHom A B) : GroupHom A B where
  toFun := fun x => B.neg (h.toFun x)
  map_zero := by rw [h.map_zero, B.neg_zero]
  map_add := by intro x y; rw [h.map_add, B.neg_add]
  map_neg := by intro x; rw [h.map_neg, B.neg_neg]

abbrev homGroup (A B : AbelianGroup.{u}) : AbelianGroup.{u} where
  Carrier := GroupHom A B
  zero := zeroHom A B
  add := addHom
  zero_add := by
    intro h
    apply GroupHom.ext
    intro x
    exact B.zero_add _
  add_zero := by
    intro h
    apply GroupHom.ext
    intro x
    exact B.add_zero _
  add_assoc := by
    intro h k l
    apply GroupHom.ext
    intro x
    exact B.add_assoc _ _ _
  add_comm := by
    intro h k
    apply GroupHom.ext
    intro x
    exact B.add_comm _ _
  neg := negHom
  add_neg := by
    intro h
    apply GroupHom.ext
    intro x
    exact B.add_neg _
  neg_zero := by
    apply GroupHom.ext
    intro x
    exact B.neg_zero
  neg_add := by
    intro h k
    apply GroupHom.ext
    intro x
    exact B.neg_add _ _
  neg_neg := by
    intro h
    apply GroupHom.ext
    intro x
    exact B.neg_neg _

/-- Algebraic tensor carrier for the two free signed systems. -/
abbrev Tensor (X Y : Type u) := Signed (X × Y)

/-- For one generator on the left, extend paired generators over the whole
right signed carrier. -/
def tensorRightGenerator {X Y : Type u} (x : X) :
    GroupHom (signedGroup Y) (signedGroup (X × Y)) :=
  signedLiftHom (signedGroup (X × Y)) (fun y => signedUnit (x, y))

/-- Extend the preceding right homomorphisms over the left signed carrier. -/
def tensorCurried {X Y : Type u} :
    GroupHom (signedGroup X) (homGroup (signedGroup Y) (signedGroup (X × Y))) :=
  signedLiftHom (homGroup (signedGroup Y) (signedGroup (X × Y))) tensorRightGenerator

/-- Canonical biadditive independent composition. -/
def tensor {X Y : Type u} (a : Signed X) (b : Signed Y) : Tensor X Y :=
  (tensorCurried.toFun a).toFun b

theorem tensor_unit_unit {X Y : Type u} (x : X) (y : Y) :
    tensor (signedUnit x) (signedUnit y) = signedUnit (x, y) := by
  change (signedLift (homGroup (signedGroup Y) (signedGroup (X × Y)))
    tensorRightGenerator (signedUnit x)).toFun (signedUnit y) = signedUnit (x, y)
  rw [signedLift_unit]
  change signedLift (signedGroup (X × Y)) (fun y => signedUnit (x, y))
    (signedUnit y) = signedUnit (x, y)
  rw [signedLift_unit]

theorem tensor_zero_left {X Y : Type u} (b : Signed Y) :
    tensor (signedZero : Signed X) b = signedZero := by
  rw [tensor, tensorCurried.map_zero]
  rfl

theorem tensor_add_left {X Y : Type u} (a a' : Signed X) (b : Signed Y) :
    tensor (signedAdd a a') b = signedAdd (tensor a b) (tensor a' b) := by
  rw [tensor, tensorCurried.map_add]
  rfl

theorem tensor_neg_left {X Y : Type u} (a : Signed X) (b : Signed Y) :
    tensor (signedNeg a) b = signedNeg (tensor a b) := by
  rw [tensor, tensorCurried.map_neg]
  rfl

theorem tensor_zero_right {X Y : Type u} (a : Signed X) :
    tensor a (signedZero : Signed Y) = signedZero := by
  exact (tensorCurried.toFun a).map_zero

theorem tensor_add_right {X Y : Type u} (a : Signed X) (b b' : Signed Y) :
    tensor a (signedAdd b b') = signedAdd (tensor a b) (tensor a b') := by
  exact (tensorCurried.toFun a).map_add b b'

theorem tensor_neg_right {X Y : Type u} (a : Signed X) (b : Signed Y) :
    tensor a (signedNeg b) = signedNeg (tensor a b) := by
  exact (tensorCurried.toFun a).map_neg b

/-- Any declared operation on generators has a canonical biadditive extension.
For contextual histories, the generator operation can be compatible sequential
composition on fixed source/middle/target hom-sets. -/
def extendBinary {X Y Z : Type u} (operation : X → Y → Z)
    (a : Signed X) (b : Signed Y) : Signed Z :=
  (signedLiftHom (signedGroup Z) (fun xy => signedUnit (operation xy.1 xy.2))).toFun
    (tensor a b)

theorem extendBinary_unit_unit {X Y Z : Type u} (operation : X → Y → Z)
    (x : X) (y : Y) :
    extendBinary operation (signedUnit x) (signedUnit y) =
      signedUnit (operation x y) := by
  rw [extendBinary, tensor_unit_unit]
  change signedLift (signedGroup Z) (fun xy => signedUnit (operation xy.1 xy.2))
    (signedUnit (x, y)) = signedUnit (operation x y)
  rw [signedLift_unit]

theorem extendBinary_add_left {X Y Z : Type u} (operation : X → Y → Z)
    (a a' : Signed X) (b : Signed Y) :
    extendBinary operation (signedAdd a a') b =
      signedAdd (extendBinary operation a b) (extendBinary operation a' b) := by
  rw [extendBinary, tensor_add_left, GroupHom.map_add]
  rfl

theorem extendBinary_add_right {X Y Z : Type u} (operation : X → Y → Z)
    (a : Signed X) (b b' : Signed Y) :
    extendBinary operation a (signedAdd b b') =
      signedAdd (extendBinary operation a b) (extendBinary operation a b') := by
  rw [extendBinary, tensor_add_right, GroupHom.map_add]
  rfl

/-- A submitted biadditive map out of two signed systems. -/
structure BiadditiveMap (X Y : Type u) (G : AbelianGroup.{u}) where
  toFun : Signed X → Signed Y → G.Carrier
  left_zero : ∀ b, toFun signedZero b = G.zero
  left_add : ∀ a a' b, toFun (signedAdd a a') b = G.add (toFun a b) (toFun a' b)
  left_neg : ∀ a b, toFun (signedNeg a) b = G.neg (toFun a b)
  right_zero : ∀ a, toFun a signedZero = G.zero
  right_add : ∀ a b b', toFun a (signedAdd b b') = G.add (toFun a b) (toFun a b')
  right_neg : ∀ a b, toFun a (signedNeg b) = G.neg (toFun a b)

def BiadditiveMap.leftHom {X Y : Type u} {G : AbelianGroup.{u}}
    (B : BiadditiveMap X Y G) (b : Signed Y) : GroupHom (signedGroup X) G where
  toFun := fun a => B.toFun a b
  map_zero := B.left_zero b
  map_add := fun a a' => B.left_add a a' b
  map_neg := fun a => B.left_neg a b

def BiadditiveMap.rightHom {X Y : Type u} {G : AbelianGroup.{u}}
    (B : BiadditiveMap X Y G) (a : Signed X) : GroupHom (signedGroup Y) G where
  toFun := B.toFun a
  map_zero := B.right_zero a
  map_add := B.right_add a
  map_neg := B.right_neg a

/-- The factor induced by a biadditive map, defined on pair generators. -/
def tensorFactor {X Y : Type u} {G : AbelianGroup.{u}} (B : BiadditiveMap X Y G) :
    GroupHom (signedGroup (X × Y)) G :=
  signedLiftHom G (fun xy => B.toFun (signedUnit xy.1) (signedUnit xy.2))

theorem tensorFactor_right_generator {X Y : Type u} {G : AbelianGroup.{u}}
    (B : BiadditiveMap X Y G) (x : X) (b : Signed Y) :
    (tensorFactor B).toFun (tensor (signedUnit x) b) =
      B.toFun (signedUnit x) b := by
  let h : GroupHom (signedGroup Y) G := {
    toFun := fun b => (tensorFactor B).toFun (tensor (signedUnit x) b)
    map_zero := by rw [tensor_zero_right, (tensorFactor B).map_zero]
    map_add := by
      intro b b'
      rw [tensor_add_right, (tensorFactor B).map_add]
    map_neg := by
      intro b
      rw [tensor_neg_right, (tensorFactor B).map_neg]
  }
  have hh := signedHom_eq_lift G h
  have hk := signedHom_eq_lift G (B.rightHom (signedUnit x))
  have generators : ∀ y,
      h.toFun (signedUnit y) = (B.rightHom (signedUnit x)).toFun (signedUnit y) := by
    intro y
    change (tensorFactor B).toFun (tensor (signedUnit x) (signedUnit y)) =
      B.toFun (signedUnit x) (signedUnit y)
    rw [tensor_unit_unit]
    exact signedLift_unit G
      (fun xy => B.toFun (signedUnit xy.1) (signedUnit xy.2)) (x, y)
  have equal : h = B.rightHom (signedUnit x) := by
    calc
      h = signedLiftHom G (fun y => h.toFun (signedUnit y)) := hh
      _ = signedLiftHom G
          (fun y => (B.rightHom (signedUnit x)).toFun (signedUnit y)) := by
        apply GroupHom.ext
        intro s
        apply congrArg (fun g => signedLift G g s)
        funext y
        exact generators y
      _ = B.rightHom (signedUnit x) := hk.symm
  exact congrArg (fun k => k.toFun b) equal

/-- Every biadditive map factors through the tensor carrier. -/
theorem tensorFactor_factors {X Y : Type u} {G : AbelianGroup.{u}}
    (B : BiadditiveMap X Y G) (a : Signed X) (b : Signed Y) :
    (tensorFactor B).toFun (tensor a b) = B.toFun a b := by
  let h : GroupHom (signedGroup X) G := {
    toFun := fun a => (tensorFactor B).toFun (tensor a b)
    map_zero := by rw [tensor_zero_left, (tensorFactor B).map_zero]
    map_add := by
      intro a a'
      rw [tensor_add_left, (tensorFactor B).map_add]
    map_neg := by
      intro a
      rw [tensor_neg_left, (tensorFactor B).map_neg]
  }
  have hh := signedHom_eq_lift G h
  have hk := signedHom_eq_lift G (B.leftHom b)
  have generators : ∀ x,
      h.toFun (signedUnit x) = (B.leftHom b).toFun (signedUnit x) := by
    intro x
    exact tensorFactor_right_generator B x b
  have equal : h = B.leftHom b := by
    calc
      h = signedLiftHom G (fun x => h.toFun (signedUnit x)) := hh
      _ = signedLiftHom G (fun x => (B.leftHom b).toFun (signedUnit x)) := by
        apply GroupHom.ext
        intro s
        apply congrArg (fun g => signedLift G g s)
        funext x
        exact generators x
      _ = B.leftHom b := hk.symm
  exact congrArg (fun k => k.toFun a) equal

/-- The factor through the tensor carrier is unique. -/
theorem tensorFactor_unique {X Y : Type u} {G : AbelianGroup.{u}}
    (B : BiadditiveMap X Y G) (h : GroupHom (signedGroup (X × Y)) G)
    (onPure : ∀ x y, h.toFun (tensor (signedUnit x) (signedUnit y)) =
      B.toFun (signedUnit x) (signedUnit y)) :
    h = tensorFactor B := by
  calc
    h = signedLiftHom G (fun xy => h.toFun (signedUnit xy)) := signedHom_eq_lift G h
    _ = signedLiftHom G
        (fun xy => B.toFun (signedUnit xy.1) (signedUnit xy.2)) := by
      apply GroupHom.ext
      intro s
      apply congrArg (fun g => signedLift G g s)
      funext xy
      rw [← tensor_unit_unit]
      exact onPure xy.1 xy.2
    _ = tensorFactor B := rfl

end WitnessedDifference.AdditiveTensorCompletion

#print axioms WitnessedDifference.AdditiveTensorCompletion.alternativeLift_unique
#print axioms WitnessedDifference.AdditiveTensorCompletion.signed_is_difference
#print axioms WitnessedDifference.AdditiveTensorCompletion.signedHom_eq_lift
#print axioms WitnessedDifference.AdditiveTensorCompletion.grothendieck_extension
#print axioms WitnessedDifference.AdditiveTensorCompletion.tensor_unit_unit
#print axioms WitnessedDifference.AdditiveTensorCompletion.tensor_add_left
#print axioms WitnessedDifference.AdditiveTensorCompletion.tensor_add_right
#print axioms WitnessedDifference.AdditiveTensorCompletion.extendBinary_unit_unit
#print axioms WitnessedDifference.AdditiveTensorCompletion.extendBinary_add_left
#print axioms WitnessedDifference.AdditiveTensorCompletion.extendBinary_add_right
#print axioms WitnessedDifference.AdditiveTensorCompletion.tensorFactor_factors
#print axioms WitnessedDifference.AdditiveTensorCompletion.tensorFactor_unique
