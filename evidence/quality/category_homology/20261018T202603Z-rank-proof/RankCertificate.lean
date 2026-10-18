import Mathlib.LinearAlgebra.Matrix.Rank

/-!
Exact mathematical and explicit-refusal model of the Rust rank checker.
AuthorityEffect: None.

Matrix dimensions and rational values here are already admitted. In Rust that
refinement is performed by checked BasicMatrix storage, admit_coefficients and
check_shapes. Extra fallible admission/allocation operations are represented by
arbitrary Except-valued checks. This file does not claim compiler/MIR equivalence,
allocator totality or machine-checked crash freedom of the Rust implementation.
-/

namespace TFQM.RankCertificate

structure Candidate (m n r : ℕ) where
  image : Matrix (Fin m) (Fin r) ℚ
  coordinates : Matrix (Fin r) (Fin n) ℚ
  imageRetraction : Matrix (Fin r) (Fin m) ℚ
  coordinateSection : Matrix (Fin n) (Fin r) ℚ

def Valid {m n r : ℕ} (M : Matrix (Fin m) (Fin n) ℚ)
    (c : Candidate m n r) : Prop :=
  M = c.image * c.coordinates ∧
  c.imageRetraction * c.image = 1 ∧
  c.coordinates * c.coordinateSection = 1

theorem valid_rank {m n r : ℕ} (M : Matrix (Fin m) (Fin n) ℚ)
    (c : Candidate m n r) (h : Valid M c) : M.rank = r := by
  obtain ⟨hM, hL, hR⟩ := h
  have upper : M.rank ≤ r := by
    rw [hM]
    exact (Matrix.rank_mul_le_left _ _).trans (Matrix.rank_le_width _)
  have split : (c.imageRetraction * M) * c.coordinateSection =
      (1 : Matrix (Fin r) (Fin r) ℚ) := by
    rw [hM]
    simp only [Matrix.mul_assoc, hR, Matrix.mul_one, hL]
  have lower : r ≤ M.rank := by
    calc
      r = (1 : Matrix (Fin r) (Fin r) ℚ).rank := by simp
      _ = ((c.imageRetraction * M) * c.coordinateSection).rank :=
        congrArg Matrix.rank split.symm
      _ ≤ (c.imageRetraction * M).rank := Matrix.rank_mul_le_left _ _
      _ ≤ M.rank := Matrix.rank_mul_le_right _ _
  exact Nat.le_antisymm upper lower

inductive Refusal where
  | domain
  | shape
  | matrix
  | identity
  | producer
  | binding
  deriving DecidableEq, Repr

/-- Each explicit error or failed predicate short-circuits before success. -/
def runChecks : List (Except Refusal Bool) → Except Refusal Unit
  | [] => .ok ()
  | .error e :: _ => .error e
  | .ok false :: _ => .error .identity
  | .ok true :: rest => runChecks rest

theorem runChecks_ok_iff (checks : List (Except Refusal Bool)) :
    runChecks checks = .ok () ↔ ∀ check ∈ checks, check = .ok true := by
  induction checks with
  | nil => simp [runChecks]
  | cons check rest ih =>
    cases check with
    | error e => simp [runChecks]
    | ok value => cases value <;> simp [runChecks, ih]

noncomputable def identityChecks {m n r : ℕ}
    (M : Matrix (Fin m) (Fin n) ℚ) (c : Candidate m n r) :
    List (Except Refusal Bool) := by
  classical
  exact [.ok (decide (M = c.image * c.coordinates)),
    .ok (decide (c.imageRetraction * c.image = 1)),
    .ok (decide (c.coordinates * c.coordinateSection = 1))]

/-- Producer results remain untrusted; success occurs only after all checks. -/
noncomputable def admit {m n r : ℕ} (M : Matrix (Fin m) (Fin n) ℚ)
    (candidate : Except Refusal (Candidate m n r))
    (extraChecks : List (Except Refusal Bool)) : Except Refusal (Candidate m n r) :=
  match candidate with
  | .error e => .error e
  | .ok c => match runChecks (extraChecks ++ identityChecks M c) with
    | .error e => .error e
    | .ok () => .ok c

theorem identityChecks_ok_iff {m n r : ℕ}
    (M : Matrix (Fin m) (Fin n) ℚ) (c : Candidate m n r) :
    runChecks (identityChecks M c) = .ok () ↔ Valid M c := by
  classical
  rw [runChecks_ok_iff]
  simp [identityChecks, Valid]

theorem admit_success {m n r : ℕ} (M : Matrix (Fin m) (Fin n) ℚ)
    (candidate : Except Refusal (Candidate m n r))
    (extraChecks : List (Except Refusal Bool)) (out : Candidate m n r)
    (h : admit M candidate extraChecks = .ok out) : Valid M out := by
  cases candidate with
  | error e => simp [admit] at h
  | ok c =>
    cases hc : runChecks (extraChecks ++ identityChecks M c) with
    | error e => simp [admit, hc] at h
    | ok u =>
      cases u
      have eq : c = out := by simpa [admit, hc] using h
      subst out
      apply (identityChecks_ok_iff M c).mp
      apply (runChecks_ok_iff _).mpr
      intro check member
      exact (runChecks_ok_iff _).mp hc check (List.mem_append_right _ member)

theorem admit_success_rank {m n r : ℕ} (M : Matrix (Fin m) (Fin n) ℚ)
    (candidate : Except Refusal (Candidate m n r))
    (extraChecks : List (Except Refusal Bool)) (out : Candidate m n r)
    (h : admit M candidate extraChecks = .ok out) : M.rank = r :=
  valid_rank M out (admit_success M candidate extraChecks out h)

theorem producer_failure {m n r : ℕ} (M : Matrix (Fin m) (Fin n) ℚ)
    (extraChecks : List (Except Refusal Bool)) (e : Refusal) :
    admit M (.error e : Except Refusal (Candidate m n r)) extraChecks = .error e := rfl

theorem explicit_failure {m n r : ℕ} (M : Matrix (Fin m) (Fin n) ℚ)
    (c out : Candidate m n r) (before after : List (Except Refusal Bool)) (e : Refusal) :
    admit M (.ok c) (before ++ [.error e] ++ after) ≠ .ok out := by
  intro success
  have all := (runChecks_ok_iff
    ((before ++ [.error e] ++ after) ++ identityChecks M c))
  cases hc : runChecks ((before ++ [.error e] ++ after) ++ identityChecks M c) with
  | error err =>
    unfold admit at success
    dsimp only at success
    rw [hc] at success
    cases success
  | ok u =>
    cases u
    have impossible : (.error e : Except Refusal Bool) = .ok true :=
      all.mp hc (.error e) (by simp)
    cases impossible

theorem failed_predicate {m n r : ℕ} (M : Matrix (Fin m) (Fin n) ℚ)
    (c out : Candidate m n r) (before after : List (Except Refusal Bool)) :
    admit M (.ok c) (before ++ [.ok false] ++ after) ≠ .ok out := by
  intro success
  have all := (runChecks_ok_iff
    ((before ++ [.ok false] ++ after) ++ identityChecks M c))
  cases hc : runChecks ((before ++ [.ok false] ++ after) ++ identityChecks M c) with
  | error err =>
    unfold admit at success
    dsimp only at success
    rw [hc] at success
    cases success
  | ok u =>
    cases u
    have impossible : (.ok false : Except Refusal Bool) = .ok true :=
      all.mp hc (.ok false) (by simp)
    cases impossible

/-- This separate propagation model keeps an arbitrary typed error payload,
not just a finite error tag. It corresponds to sequential Rust `?` propagation. -/
def sequence {Error : Type} : List (Except Error Unit) → Except Error Unit
  | [] => .ok ()
  | .error e :: _ => .error e
  | .ok () :: rest => sequence rest

theorem sequence_append {Error : Type} (before after : List (Except Error Unit)) :
    sequence (before ++ after) =
      (match sequence before with
      | .error e => .error e
      | .ok () => sequence after) := by
  induction before with
  | nil => rfl
  | cons first rest ih =>
    cases first with
    | error e => rfl
    | ok u => cases u; simpa [sequence] using ih

def returnAfterChecks {Error Value : Type} (checks : List (Except Error Unit))
    (value : Value) : Except Error Value :=
  match sequence checks with
  | .error e => .error e
  | .ok () => .ok value

theorem first_error_preserved {Error Value : Type}
    (before after : List (Except Error Unit)) (e : Error) (value : Value)
    (h : sequence before = .ok ()) :
    returnAfterChecks (before ++ [.error e] ++ after) value = .error e := by
  simp [returnAfterChecks, sequence_append, h, sequence]

#print axioms valid_rank
#print axioms runChecks_ok_iff
#print axioms admit_success
#print axioms admit_success_rank
#print axioms producer_failure
#print axioms explicit_failure
#print axioms failed_predicate
#print axioms first_error_preserved

end TFQM.RankCertificate
