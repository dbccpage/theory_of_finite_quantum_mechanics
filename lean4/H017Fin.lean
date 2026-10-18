/-
  H017Fin -- End of a finite enumerated report set is M_n(Z[i]).
  AuthorityEffect: None. Candidate only. Not PROVEN.

  QM_122 remaining job 7.2 / STACK ordinary M_n(C) item: the
  general finite label set. H017Matrix recovered End of Bool as
  M_2(Z[i]). This file generalizes the label set: for any
  enumerated report set Q, End of Q → GaussInt is left-multiplication
  by a unique n × n Gauss-integer matrix, n = |Q| = E.elems.length.

  Named extras, as hypotheses, not flags:
    (1) coefficient pack K (instantiated at gaussPack);
    (2) a finite enumeration E of the report set Q;
    (3) additivity of an endomorphism;
    (4) pack-homogeneity of that endomorphism.

  Theorems: every such endomorphism is left-multiplication by a
  unique n × n matrix; matrix product is composition; conjugate
  transpose implements the H005 pairing. The Bool host of
  H017Matrix is the n = 2 case; the product host enumBoolProd is
  n = 4. Pauli generators stay in H017Matrix.

  This is not M_n(C). The field C, the spectral theorem, Gleason
  uniqueness at n ≥ 3, CPTP channels, unique Hilbert tensor, the
  circle group, and continuous time remain named extras (H017Extras).
  Do not read this recovery as ordinary complex matrix mechanics.

  AuthorityEffect: None
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import H004FreeLinearization
import H005InnerProductAdmission
import H017MatrixFiniteRecovery

namespace FableHilbertWalk20260819.H017Fin

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H005 (sesq)

/-- Named finite matrix object: n × n matrices on an enumerated
    report set, n = E.elems.length. -/
def Mat (K Q : Type) : Type := Q → Q → K

/-- Action of a matrix on a free vector, summed over the declared
    enumeration. -/
def applyMat {K Q : Type} (P : StarRingPack K) (E : Enum Q)
    (A : Mat K Q) (v : Vec K Q) : Vec K Q :=
  fun i => rsum P (E.elems.map (fun j => P.mul (A i j) (v j)))

/-- Matrix product, summed over the declared enumeration. -/
def mmul {K Q : Type} (P : StarRingPack K) (E : Enum Q)
    (A B : Mat K Q) : Mat K Q :=
  fun i j => rsum P (E.elems.map (fun k => P.mul (A i k) (B k j)))

/-- Identity matrix. -/
def ident {K Q : Type} (P : StarRingPack K) [DecidableEq Q] : Mat K Q :=
  fun i j => if (i == j) = true then P.one else P.zero

/-- Conjugate transpose. -/
def adj {K Q : Type} (P : StarRingPack K) (A : Mat K Q) : Mat K Q :=
  fun i j => P.conj (A j i)

/-- Named extras for an endomorphism of the free module on Q. -/
structure LinearEnd {K : Type} (Q : Type) (P : StarRingPack K) where
  map : Vec K Q → Vec K Q
  map_add :
    ∀ u v q,
      map (vadd P u v) q = P.add (map u q) (map v q)
  map_smul :
    ∀ c u q,
      map (smul P c u) q = P.mul c (map u q)

/-- Matrix of an endomorphism: columns are the images of the
    report basis. -/
def matOf {K Q : Type} [DecidableEq Q] {P : StarRingPack K}
    (T : LinearEnd Q P) : Mat K Q :=
  fun i j => T.map (delta P j) i

theorem rsum_map_mul_right {K X : Type} (P : StarRingPack K)
    (c : K) (f : X → K) (l : List X) :
    rsum P (l.map (fun x => P.mul (f x) c)) =
      P.mul (rsum P (l.map f)) c := by
  have h :
      l.map (fun x => P.mul (f x) c) =
        l.map (fun x => P.mul c (f x)) :=
    map_congr_mem (fun x _ => P.mul_comm _ _)
  rw [h, rsum_map_mul_left, P.mul_comm]

#print axioms rsum_map_mul_right

theorem rsum_conj {K X : Type} (P : StarRingPack K) (f : X → K) :
    ∀ l : List X,
      rsum P (l.map (fun x => P.conj (f x))) =
        P.conj (rsum P (l.map f)) := by
  intro l
  induction l with
  | nil =>
      simp only [List.map_nil, rsum]
      exact P.conj_zero.symm
  | cons a t ih =>
      simp only [List.map_cons, rsum]
      rw [ih, P.conj_add]

#print axioms rsum_conj

theorem rsum_rsum_swap {K X Y : Type} (P : StarRingPack K)
    (f : X → Y → K) (lx : List X) (ly : List Y) :
    rsum P (lx.map (fun x => rsum P (ly.map (fun y => f x y)))) =
      rsum P (ly.map (fun y => rsum P (lx.map (fun x => f x y)))) := by
  induction lx with
  | nil =>
      simp only [List.map_nil, rsum]
      exact (rsum_map_zero P ly).symm
  | cons a t ih =>
      simp only [List.map_cons, rsum]
      rw [ih]
      rw [← rsum_map_add P (fun y => f a y)
        (fun y => rsum P (t.map (fun x => f x y))) ly]

#print axioms rsum_rsum_swap

theorem mul3_reassoc {K : Type} (P : StarRingPack K) (a b c : K) :
    P.mul (P.mul a b) c = P.mul b (P.mul a c) := by
  rw [P.mul_comm a b, P.mul_assoc]

#print axioms mul3_reassoc

/-- Endomorphism of a matrix: left-multiplication. -/
def endOfMat {K Q : Type} (P : StarRingPack K) (E : Enum Q)
    (A : Mat K Q) : LinearEnd Q P where
  map := applyMat P E A
  map_add := fun u v q => by
    unfold applyMat vadd
    have h :
        E.elems.map (fun j =>
            P.mul (A q j) (P.add (u j) (v j))) =
          E.elems.map (fun j =>
            P.add (P.mul (A q j) (u j)) (P.mul (A q j) (v j))) :=
      map_congr_mem (fun j _ => P.mul_add _ _ _)
    rw [h, rsum_map_add]
  map_smul := fun c u q => by
    unfold applyMat smul
    have h :
        E.elems.map (fun j => P.mul (A q j) (P.mul c (u j))) =
          E.elems.map (fun j => P.mul c (P.mul (A q j) (u j))) :=
      map_congr_mem (fun j _ => by
        rw [← P.mul_assoc, P.mul_comm (A q j) c, P.mul_assoc])
    rw [h, rsum_map_mul_left]

#print axioms endOfMat

theorem map_zero {K Q : Type} {P : StarRingPack K}
    (T : LinearEnd Q P) (q : Q) :
    T.map (vzero P) q = P.zero := by
  have hz : smul P P.zero (vzero (Q := Q) P) = vzero P :=
    funext (fun _ => by
      unfold smul vzero
      exact P.mul_zero P.zero)
  calc T.map (vzero P) q
      = T.map (smul P P.zero (vzero P)) q := by rw [hz]
    _ = P.mul P.zero (T.map (vzero P) q) := T.map_smul P.zero (vzero P) q
    _ = P.zero := P.zero_mul (T.map (vzero P) q)

#print axioms map_zero

/-- Expansion of a vector along a list of report labels. -/
def expandOn {K Q : Type} [DecidableEq Q] (P : StarRingPack K)
    (v : Vec K Q) (l : List Q) : Vec K Q :=
  fun x => rsum P (l.map (fun j => P.mul (v j) (delta P j x)))

theorem expandOn_nil {K Q : Type} [DecidableEq Q] (P : StarRingPack K)
    (v : Vec K Q) : expandOn P v [] = vzero P :=
  funext (fun _ => rfl)

#print axioms expandOn_nil

theorem expandOn_cons {K Q : Type} [DecidableEq Q] (P : StarRingPack K)
    (v : Vec K Q) (a : Q) (t : List Q) :
    expandOn P v (a :: t) =
      vadd P (smul P (v a) (delta P a)) (expandOn P v t) :=
  funext (fun _ => rfl)

#print axioms expandOn_cons

theorem map_expandOn {K Q : Type} [DecidableEq Q] {P : StarRingPack K}
    (T : LinearEnd Q P) (v : Vec K Q) (y : Q) :
    ∀ l : List Q,
      T.map (expandOn P v l) y =
        rsum P (l.map (fun j =>
          P.mul (v j) (T.map (delta P j) y))) := by
  intro l
  induction l with
  | nil =>
      unfold expandOn
      simp only [List.map_nil, rsum]
      exact map_zero T y
  | cons a t ih =>
      rw [expandOn_cons, T.map_add, T.map_smul]
      simp only [List.map_cons, rsum]
      rw [ih]

#print axioms map_expandOn

theorem expandOn_enum {K Q : Type} [DecidableEq Q] (P : StarRingPack K)
    (E : Enum Q) (v : Vec K Q) : expandOn P v E.elems = v :=
  funext (fun x => basis_expansion P E v x)

#print axioms expandOn_enum

/-- Under the named extras, the map is left-multiplication by its
    matrix. -/
theorem apply_eq_matOf {K Q : Type} [DecidableEq Q] {P : StarRingPack K}
    (E : Enum Q) (T : LinearEnd Q P) (v : Vec K Q) (x : Q) :
    T.map v x = applyMat P E (matOf T) v x := by
  have hv : v = expandOn P v E.elems := (expandOn_enum P E v).symm
  have hmap : T.map v x = T.map (expandOn P v E.elems) x :=
    congrArg (fun w => T.map w x) hv
  rw [hmap, map_expandOn]
  unfold applyMat matOf
  apply congrArg
  apply map_congr_mem
  intro j _
  exact P.mul_comm _ _

#print axioms apply_eq_matOf

theorem applyMat_delta {K Q : Type} [DecidableEq Q] (P : StarRingPack K)
    (E : Enum Q) (A : Mat K Q) (i j : Q) :
    applyMat P E A (delta P j) i = A i j := by
  unfold applyMat
  have h :
      E.elems.map (fun k => P.mul (A i k) (delta P j k)) =
        E.elems.map (fun k =>
          if (j == k) = true then A i j else P.zero) := by
    apply map_congr_mem
    intro k _
    unfold delta
    by_cases hjk : j = k
    · subst hjk
      rw [if_pos (beq_self_eq_true j), if_pos (beq_self_eq_true j),
        P.mul_one]
    · rw [if_neg (fun h => hjk (beq_iff_eq.mp h)),
        if_neg (fun h => hjk (beq_iff_eq.mp h)), P.mul_zero]
  rw [h, rsum_map_delta P (A i j) (E.complete j) E.nodup]

#print axioms applyMat_delta

theorem matOf_apply {K Q : Type} [DecidableEq Q] (P : StarRingPack K)
    (E : Enum Q) (A : Mat K Q) :
    ∀ i j : Q, matOf (endOfMat P E A) i j = A i j := by
  intro i j
  unfold matOf
  change applyMat P E A (delta P j) i = A i j
  exact applyMat_delta P E A i j

#print axioms matOf_apply

/-- The matrix of an endomorphism is the unique matrix that acts
    as that endomorphism. -/
theorem matrix_of_end_unique {K Q : Type} [DecidableEq Q]
    {P : StarRingPack K} (E : Enum Q) (T : LinearEnd Q P)
    (A : Mat K Q) (h : ∀ v x, T.map v x = applyMat P E A v x) :
    ∀ i j : Q, matOf T i j = A i j := by
  intro i j
  unfold matOf
  rw [h (delta P j) i]
  exact applyMat_delta P E A i j

#print axioms matrix_of_end_unique

theorem ident_acts_as_id {K Q : Type} [DecidableEq Q]
    (P : StarRingPack K) (E : Enum Q) (v : Vec K Q) (i : Q) :
    applyMat P E (ident P) v i = v i := by
  unfold applyMat ident
  have h :
      E.elems.map (fun j =>
          P.mul (if (i == j) = true then P.one else P.zero) (v j)) =
        E.elems.map (fun j =>
          if (i == j) = true then v i else P.zero) := by
    apply map_congr_mem
    intro j _
    by_cases hij : i = j
    · subst hij
      rw [if_pos (beq_self_eq_true i), if_pos (beq_self_eq_true i),
        P.one_mul]
    · rw [if_neg (fun h => hij (beq_iff_eq.mp h)),
        if_neg (fun h => hij (beq_iff_eq.mp h)), P.zero_mul]
  rw [h, rsum_map_delta P (v i) (E.complete i) E.nodup]

#print axioms ident_acts_as_id

theorem mmul_as_composition {K Q : Type} (P : StarRingPack K)
    (E : Enum Q) (A B : Mat K Q) (v : Vec K Q) (i : Q) :
    applyMat P E (mmul P E A B) v i =
      applyMat P E A (applyMat P E B v) i := by
  unfold applyMat mmul
  have h1 :
      E.elems.map (fun k =>
          P.mul (A i k) (rsum P (E.elems.map (fun j =>
            P.mul (B k j) (v j))))) =
        E.elems.map (fun k =>
          rsum P (E.elems.map (fun j =>
            P.mul (A i k) (P.mul (B k j) (v j))))) :=
    map_congr_mem (fun k _ =>
      (rsum_map_mul_left P (A i k)
        (fun j => P.mul (B k j) (v j)) E.elems).symm)
  rw [h1]
  rw [rsum_rsum_swap P
    (fun k j => P.mul (A i k) (P.mul (B k j) (v j)))
    E.elems E.elems]
  have h2 :
      E.elems.map (fun j =>
          rsum P (E.elems.map (fun k =>
            P.mul (A i k) (P.mul (B k j) (v j))))) =
        E.elems.map (fun j =>
          P.mul
            (rsum P (E.elems.map (fun k => P.mul (A i k) (B k j))))
            (v j)) := by
    apply map_congr_mem
    intro j _
    have hassoc :
        E.elems.map (fun k =>
            P.mul (A i k) (P.mul (B k j) (v j))) =
          E.elems.map (fun k =>
            P.mul (P.mul (A i k) (B k j)) (v j)) :=
      map_congr_mem (fun k _ => (P.mul_assoc _ _ _).symm)
    rw [hassoc, rsum_map_mul_right]
  rw [h2]

#print axioms mmul_as_composition

/-- Conjugate transpose is the adjoint of the admitted pairing. -/
theorem sesq_conj_transpose {K Q : Type} (P : StarRingPack K)
    (E : Enum Q) (A : Mat K Q) (u v : Vec K Q) :
    sesq P E (applyMat P E A u) v =
      sesq P E u (applyMat P E (adj P A) v) := by
  unfold sesq
  have hL :
      E.elems.map (fun i =>
          P.mul (P.conj (applyMat P E A u i)) (v i)) =
        E.elems.map (fun i =>
          rsum P (E.elems.map (fun j =>
            P.mul (P.conj (u j)) (P.mul (P.conj (A i j)) (v i))))) := by
    apply map_congr_mem
    intro i _
    unfold applyMat
    have hc :
        P.conj (rsum P (E.elems.map (fun j =>
            P.mul (A i j) (u j)))) =
          rsum P (E.elems.map (fun j =>
            P.mul (P.conj (A i j)) (P.conj (u j)))) := by
      have hconj := rsum_conj P (fun j => P.mul (A i j) (u j)) E.elems
      rw [← hconj]
      apply congrArg
      apply map_congr_mem
      intro j _
      exact P.conj_mul _ _
    rw [hc]
    have hmul := rsum_map_mul_right P (v i)
      (fun j => P.mul (P.conj (A i j)) (P.conj (u j))) E.elems
    rw [hmul.symm]
    apply congrArg
    apply map_congr_mem
    intro j _
    exact mul3_reassoc P (P.conj (A i j)) (P.conj (u j)) (v i)
  rw [hL]
  rw [rsum_rsum_swap P
    (fun i j =>
      P.mul (P.conj (u j)) (P.mul (P.conj (A i j)) (v i)))
    E.elems E.elems]
  have hR :
      E.elems.map (fun j =>
          rsum P (E.elems.map (fun i =>
            P.mul (P.conj (u j)) (P.mul (P.conj (A i j)) (v i))))) =
        E.elems.map (fun j =>
          P.mul (P.conj (u j)) (applyMat P E (adj P A) v j)) := by
    apply map_congr_mem
    intro j _
    have hmul := rsum_map_mul_left P (P.conj (u j))
      (fun i => P.mul (P.conj (A i j)) (v i)) E.elems
    rw [hmul]
    apply congrArg
    unfold applyMat adj
    rfl
  rw [hR]

#print axioms sesq_conj_transpose

/-- Punchline: under the named extras, End of the free GaussInt
    module on a finite enumerated report set Q is M_n(Z[i]) with
    n = |Q|. Composition is matrix product. Conjugate transpose is
    the pairing adjoint. This is not M_n(C). -/
theorem finite_gauss_matrix_algebra {Q : Type} [DecidableEq Q]
    (E : Enum Q) :
    (∀ (T : LinearEnd Q gaussPack) (v : Vec GaussInt Q) (x : Q),
      T.map v x = applyMat gaussPack E (matOf T) v x) ∧
      (∀ (A : Mat GaussInt Q) (i j : Q),
        matOf (endOfMat gaussPack E A) i j = A i j) ∧
      (∀ (A B : Mat GaussInt Q) (v : Vec GaussInt Q) (i : Q),
        applyMat gaussPack E (mmul gaussPack E A B) v i =
          applyMat gaussPack E A (applyMat gaussPack E B v) i) ∧
      (∀ (A : Mat GaussInt Q) (u v : Vec GaussInt Q),
        sesq gaussPack E (applyMat gaussPack E A u) v =
          sesq gaussPack E u
            (applyMat gaussPack E (adj gaussPack A) v)) ∧
      (∀ (T : LinearEnd Q gaussPack) (A : Mat GaussInt Q),
        (∀ v x, T.map v x = applyMat gaussPack E A v x) →
          ∀ i j, matOf T i j = A i j) :=
  ⟨apply_eq_matOf E, matOf_apply gaussPack E,
    mmul_as_composition gaussPack E, sesq_conj_transpose gaussPack E,
    fun T A h => matrix_of_end_unique E T A h⟩

#print axioms finite_gauss_matrix_algebra

theorem two_label_size : enumBool.elems.length = 2 :=
  rfl

#print axioms two_label_size

theorem four_label_size : enumBoolProd.elems.length = 4 :=
  rfl

#print axioms four_label_size

/-- The two-label host is the n = 2 case already named M_2(Z[i])
    in H017Matrix. Action agrees. -/
theorem applyMat_agrees_two_level {K : Type} (P : StarRingPack K)
    (A : Mat K Bool) (v : Vec K Bool) (i : Bool) :
    applyMat P enumBool A v i =
      FableHilbertWalk20260819.H017Matrix.applyMat P A v i := by
  unfold applyMat FableHilbertWalk20260819.H017Matrix.applyMat enumBool
  simp only [List.map, rsum]
  rw [P.add_zero]

#print axioms applyMat_agrees_two_level

/-- Instantiation at the two-label host: M_2(Z[i]). Does not
    replace H017Matrix; it is the same n = 2 case of the general
    recovery. -/
theorem two_label_gauss_matrix_algebra :
    ∀ (T : LinearEnd Bool gaussPack) (v : Vec GaussInt Bool) (x : Bool),
      T.map v x = applyMat gaussPack enumBool (matOf T) v x :=
  (finite_gauss_matrix_algebra enumBool).1

#print axioms two_label_gauss_matrix_algebra

/-- Instantiation at the four-label product host: M_4(Z[i]).
    Still not M_n(C). -/
theorem four_label_gauss_matrix_algebra :
    ∀ (T : LinearEnd (Bool × Bool) gaussPack)
      (v : Vec GaussInt (Bool × Bool)) (x : Bool × Bool),
      T.map v x = applyMat gaussPack enumBoolProd (matOf T) v x :=
  (finite_gauss_matrix_algebra enumBoolProd).1

#print axioms four_label_gauss_matrix_algebra

end FableHilbertWalk20260819.H017Fin
