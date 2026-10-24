import Imported.Genesis19l57g1.Derivation.Minimality
import Imported.Genesis19l57g1.PaperSearch

open Derivation GenesisPaper.Orbit GenesisPaper.Search

/-
Narrowed boundary for PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN.
U0 and U1 are the two-datum unary regimes. BL is the binary regime.
The exhaustive key lists both datum permutations and the one form permutation.
This module does not read a Python key or an exported run.
-/

def pgwIso_U0_U1 : Iso U0 U1 where
  dmap := swap01
  dinv := swap01
  fmap := id
  finv := id
  dmap_lt := by decide
  dinv_lt := by decide
  dinv_dmap := by decide
  dmap_dinv := by decide
  fmap_lt := by decide
  finv_lt := by decide
  finv_fmap := by decide
  fmap_finv := by decide
  arity := by decide
  insts_fwd := by decide
  insts_bwd := by decide
  rules_fwd := by decide
  rules_bwd := by decide
  reqs_fwd := by decide
  reqs_bwd := by decide

theorem pgwIso_U0_wf : U0.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro p hp
    simp [U0] at hp
    subst hp
    decide
  · intro f hf
    simp [U0] at hf
  · intro q hq
    simp [U0] at hq
    subst hq
    decide
  · intro a ha
    simp [U0] at ha
    subst ha
    decide

theorem pgwIso_U1_wf : U1.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro p hp
    simp [U1] at hp
    subst hp
    decide
  · intro f hf
    simp [U1] at hf
  · intro q hq
    simp [U1] at hq
    subst hq
    decide
  · intro a ha
    simp [U1] at ha
    subst ha
    decide

theorem pgwIso_BL_wf : BL.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro p hp
    simp [BL] at hp
    subst hp
    decide
  · intro f hf
    simp [BL] at hf
  · intro q hq
    simp [BL] at hq
    subst hq
    decide
  · intro a ha
    simp [BL] at ha
    subst ha
    decide

theorem pgwIso_set_collections :
    SetCollections U0 ∧ SetCollections U1 ∧ SetCollections BL := by
  refine ⟨⟨?_, ?_, ?_⟩, ⟨?_, ?_, ?_⟩, ⟨?_, ?_, ?_⟩⟩
  all_goals
    first
    | decide
    | simp [U0, U1, BL, List.nodup_cons, List.nodup_nil]

theorem pgwIso_candidate_counts :
    (candidateKeys U0).length = 2 ∧
      (candidateKeys U1).length = 2 ∧
      (candidateKeys BL).length = 2 := by
  decide

theorem pgwIso_keys_eq :
    canonicalKey U0 = canonicalKey U1 :=
  (canonicalKey_classification pgwIso_U0_wf pgwIso_U1_wf
      pgwIso_set_collections.1 pgwIso_set_collections.2.1).mpr ⟨pgwIso_U0_U1⟩

theorem pgwIso_U0_not_BL (h : Iso U0 BL) : False :=
  U0_not_iso_BL h

theorem pgwIso_keys_ne :
    canonicalKey U0 ≠ canonicalKey BL := by
  intro h
  rcases (canonicalKey_classification pgwIso_U0_wf pgwIso_BL_wf
      pgwIso_set_collections.1 pgwIso_set_collections.2.2).mp h with ⟨iso⟩
  exact pgwIso_U0_not_BL iso

#print axioms pgwIso_U0_U1
#print axioms pgwIso_U0_wf
#print axioms pgwIso_U1_wf
#print axioms pgwIso_BL_wf
#print axioms pgwIso_set_collections
#print axioms pgwIso_candidate_counts
#print axioms pgwIso_keys_eq
#print axioms pgwIso_keys_ne
#print axioms pgwIso_U0_not_BL
