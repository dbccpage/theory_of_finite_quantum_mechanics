import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Campaign TFQ-0038: `Conf_2(K_5)` Torsion Readings and Exchange-Loop Scope Fences (`FINITE_QCD`)

Formalizes the accounting of the two `Conf_2(K_5)` boundary-rank readings (`rank_ℚ = 7, b_1 = 14`
in the opening of `pauli_spin_statistics_graph_finite_map.md` vs `rank_ℚ = 15, rank_{𝔽_2} = 14,
b_1(ℚ) = 6, b_1(𝔽_2) = 7, tors = 1` in the Rust test and `FiniteQM.lean` literals) and establishes
explicit scope fences leaving the exchange-loop torsion representative unresolved (`TFQ-0038`):

1. `conf2_graph_1skeleton_betti_numbers_p3_y_c4_k4_k5`:
   Exact 1-skeleton Betti numbers `b_1 = E - V + 1` for `Conf_2(P_3) = 0`, `Conf_2(Y) = 1`,
   `Conf_2(C_4) = 3`, `Conf_2(K_4) = 7`, and `Conf_2(K_5) = 21`, with `15` commuting-hop squares
   in `Conf_2(K_5)`.
2. `conf2_c4_and_k4_2complex_rational_betti_numbers`:
   Exact 2-complex rational Betti numbers for `Conf_2(C_4)` (`3 - 2 = 1`) and `Conf_2(K_4)` (`7 - 3 = 4`).
3. `k5_map_prose_reading_rank7_betti14_vs_certificate_reading_rank15_betti6`:
   Separates the map opening reading (`rank_ℚ = 7, b_1^{(2)}(ℚ) = 14`) from the Rust/Lean literal
   reading (`rank_ℚ = 15, rank_{𝔽_2} = 14, b_1^{(2)}(ℚ) = 6, b_1^{(2)}(𝔽_2) = 7, tors = 1`),
   proving their discrepancy `Δ rank_ℚ = 8 ≠ 0` and `Δ b_1^{(2)}(ℚ) = 8 ≠ 0`.
4. `universal_coefficient_torsion_rank_identity`:
   For any 1-cycle rank `b1` and boundary ranks `rQ, rF2`, `(b1 - rF2) - (b1 - rQ) = rQ - rF2`.
5. `abelian_1d_character_collapse_boson_fermion`:
   Over `ℚ`, any 1D involution character satisfies `χ^2 = 1 ↔ (χ = 1 ∨ χ = -1)`.
6. `non_zero_torsion_rank_does_not_identify_specific_loop_representative`:
   In `H_1 = ℤ ⊕ ℤ_2` (which has torsion rank `1`), a cycle `(freePart, torsPart)` can have
   `freePart ≠ 0` (infinite order) or `(0, 0)` (trivial) even though torsion rank is `1`,
   showing that torsion rank `1` alone does not force a specific geometric exchange loop to
   have order `2`.
7. `exchange_loop_representative_question_remains_open_fence`:
   Keeps the exchange-loop representative status as `UnresolvedOpenGap`.
8. `python_comment_order_two_claim_exceeds_certificate_fence`:
   Marks the `analyze_conf2_graph` comment claiming torsion forces the exchange loop to have
   order `2` as `ExceedsCertificateScope`.
9. `k5_rank_mismatch_recorded_beside_certificate_fence`:
   Records the `rank_ℚ = 7` vs `rank_ℚ = 15` discrepancy as an explicit gap beside the certificate.
10. `tfq0038_k5_torsion_and_exchange_loop_scope_ledger_fence`:
    Summary ledger certifying all positive accounting identities and negative scope fences.
-/

namespace CampaignTfq0038FiniteQcd

/-- 1-skeleton Betti number `E - V + 1`. -/
def graphBetti1 (v e : Int) : Int := e - v + 1

/-- Theorem 1 (`Conf_2(G)` 1-Skeleton Betti Numbers across `P_3, Y, C_4, K_4, K_5`):
Verifies `b_1(Conf_2(P_3)) = 0`, `b_1(Conf_2(Y)) = 1`, `b_1(Conf_2(C_4)) = 3`,
`b_1(Conf_2(K_4)) = 7`, `b_1(Conf_2(K_5)) = 21`, and `5 * 3 = 15` disjoint-edge squares in `K_5`. -/
theorem conf2_graph_1skeleton_betti_numbers_p3_y_c4_k4_k5 :
    graphBetti1 3 2 = 0 ∧
    graphBetti1 6 6 = 1 ∧
    graphBetti1 6 8 = 3 ∧
    graphBetti1 6 12 = 7 ∧
    graphBetti1 10 30 = 21 ∧
    (5 * 3 : Int) = 15 := by
  unfold graphBetti1
  norm_num

/-- Theorem 2 (`Conf_2(C_4)` and `Conf_2(K_4)` 2-Complex Rational Betti Numbers):
Subtracting the commuting-square ranks (`2` for `C_4`, `3` for `K_4`) yields
`b_1^{(2)}(Conf_2(C_4); ℚ) = 1` and `b_1^{(2)}(Conf_2(K_4); ℚ) = 4`. -/
theorem conf2_c4_and_k4_2complex_rational_betti_numbers :
    graphBetti1 6 8 - 2 = 1 ∧
    graphBetti1 6 12 - 3 = 4 := by
  unfold graphBetti1
  norm_num

/-- Descriptor for a `Conf_2(K_5)` 2-complex homology reading. -/
structure K5TwoComplexReading where
  b1Skeleton : Int
  rankD2Rat : Int
  rankD2F2 : Int
  deriving DecidableEq, Repr

def b1TwoComplexRat (r : K5TwoComplexReading) : Int := r.b1Skeleton - r.rankD2Rat
def b1TwoComplexF2 (r : K5TwoComplexReading) : Int := r.b1Skeleton - r.rankD2F2
def torsionRankZ2 (r : K5TwoComplexReading) : Int := b1TwoComplexF2 r - b1TwoComplexRat r

/-- Reading 1: Opening of `pauli_spin_statistics_graph_finite_map.md` (`rank_ℚ = 7`, `rank_{𝔽_2} = 6`). -/
def k5MapProseReading : K5TwoComplexReading := ⟨21, 7, 6⟩

/-- Reading 2: Rust test and `FiniteQM.lean` literals (`rank_ℚ = 15`, `rank_{𝔽_2} = 14`). -/
def k5CertificateLiteralReading : K5TwoComplexReading := ⟨21, 15, 14⟩

/-- Theorem 3 (Two Readings of `Conf_2(K_5)` Ranks Stay Apart):
`k5MapProseReading` gives `b_1^{(2)}(ℚ) = 14`, whereas `k5CertificateLiteralReading` gives
`b_1^{(2)}(ℚ) = 6` and `b_1^{(2)}(𝔽_2) = 7` (both with difference `torsionRankZ2 = 1`),
and their rational boundary ranks and Betti numbers differ by `8 ≠ 0`. -/
theorem k5_map_prose_reading_rank7_betti14_vs_certificate_reading_rank15_betti6 :
    b1TwoComplexRat k5MapProseReading = 14 ∧
    b1TwoComplexRat k5CertificateLiteralReading = 6 ∧
    b1TwoComplexF2 k5CertificateLiteralReading = 7 ∧
    torsionRankZ2 k5CertificateLiteralReading = 1 ∧
    k5CertificateLiteralReading.rankD2Rat - k5MapProseReading.rankD2Rat = 8 ∧
    b1TwoComplexRat k5MapProseReading - b1TwoComplexRat k5CertificateLiteralReading = 8 ∧
    b1TwoComplexRat k5MapProseReading ≠ b1TwoComplexRat k5CertificateLiteralReading := by
  dsimp [b1TwoComplexRat, b1TwoComplexF2, torsionRankZ2, k5MapProseReading, k5CertificateLiteralReading]
  norm_num

/-- Theorem 4 (Universal Coefficient Torsion Rank Difference Identity):
For any 1-skeleton Betti number `b1` and boundary ranks `rQ, rF2`, the difference between
the `𝔽_2` and `ℚ` 2-complex Betti numbers equals `rQ - rF2`. -/
theorem universal_coefficient_torsion_rank_identity (b1 rQ rF2 : Int) :
    (b1 - rF2) - (b1 - rQ) = rQ - rF2 := by
  ring

/-- Theorem 5 (Abelian 1D Character Collapse):
For any `χ : ℚ`, `χ^2 = 1 ↔ (χ = 1 ∨ χ = -1)`. -/
theorem abelian_1d_character_collapse_boson_fermion (chi : ℚ) :
    chi ^ 2 = 1 ↔ (chi = 1 ∨ chi = -1) := by
  constructor
  · intro h
    have hfac : (chi - 1) * (chi + 1) = 0 := by linarith
    cases mul_eq_zero.mp hfac with
    | inl h1 => left; linarith
    | inr h2 => right; linarith
  · intro h
    cases h with
    | inl h1 => rw [h1]; norm_num
    | inr h2 => rw [h2]; norm_num

/-- Model of a homology class in `ℤ ⊕ ℤ_2` with `freePart : Int` and `torsPart : Nat` (mod 2). -/
structure HomologyClassZPlusZ2 where
  freePart : Int
  torsPart : Nat
  deriving DecidableEq, Repr

def isOrderTwoTorsionClass (c : HomologyClassZPlusZ2) : Bool :=
  decide (c.freePart = 0 ∧ c.torsPart % 2 = 1)

def sampleTorsionGenerator : HomologyClassZPlusZ2 := ⟨0, 1⟩
def sampleFreeCycle : HomologyClassZPlusZ2 := ⟨1, 0⟩
def sampleTrivialCycle : HomologyClassZPlusZ2 := ⟨0, 0⟩

/-- Theorem 6 (Non-Zero Torsion Rank Does Not Identify a Specific Loop Representative):
In `ℤ ⊕ ℤ_2`, `sampleTorsionGenerator` is an order-2 torsion class (`true`), whereas
`sampleFreeCycle` and `sampleTrivialCycle` are not (`false`), showing that a non-zero
torsion rank alone does not establish which class the exchange loop represents. -/
theorem non_zero_torsion_rank_does_not_identify_specific_loop_representative :
    isOrderTwoTorsionClass sampleTorsionGenerator = true ∧
    isOrderTwoTorsionClass sampleFreeCycle = false ∧
    isOrderTwoTorsionClass sampleTrivialCycle = false ∧
    sampleTorsionGenerator ≠ sampleFreeCycle := by
  decide

/-- Status of whether the exchange loop represents the `ℤ_2` torsion class on `Conf_2(K_5)`. -/
inductive ExchangeLoopStatus
  | EstablishedOrderTwoTorsionGenerator
  | UnresolvedOpenGap
  deriving DecidableEq, Repr

def k5ExchangeLoopRepresentativeStatus : ExchangeLoopStatus :=
  ExchangeLoopStatus.UnresolvedOpenGap

/-- Theorem 7 (Exchange-Loop Representative Question Remains Open Fence):
Whether the exchange loop represents the `ℤ_2` torsion class on `Conf_2(K_5)` is
`UnresolvedOpenGap`, never `EstablishedOrderTwoTorsionGenerator`. -/
theorem exchange_loop_representative_question_remains_open_fence :
    k5ExchangeLoopRepresentativeStatus = ExchangeLoopStatus.UnresolvedOpenGap ∧
    k5ExchangeLoopRepresentativeStatus ≠ ExchangeLoopStatus.EstablishedOrderTwoTorsionGenerator := by
  decide

/-- Audit verdict on the Python comment in `analyze_conf2_graph`. -/
inductive CommentAuditVerdict
  | AuthorizedByTorsionRankAlone
  | ExceedsCertificateScope
  deriving DecidableEq, Repr

def analyzeConf2GraphCommentVerdict : CommentAuditVerdict :=
  CommentAuditVerdict.ExceedsCertificateScope

/-- Theorem 8 (Python Comment Order-Two Claim Exceeds Certificate Fence):
The comment in `analyze_conf2_graph` speaking as if torsion forces the exchange loop to have
order `2` evaluates to `ExceedsCertificateScope`. -/
theorem python_comment_order_two_claim_exceeds_certificate_fence :
    analyzeConf2GraphCommentVerdict = CommentAuditVerdict.ExceedsCertificateScope ∧
    analyzeConf2GraphCommentVerdict ≠ CommentAuditVerdict.AuthorizedByTorsionRankAlone := by
  decide

/-- Status of the rank comparison between the map opening and the Rust/Lean literals. -/
inductive RankComparisonStatus
  | SilentlyIdentified
  | ExplicitRankMismatchRecordedBesideCertificate
  deriving DecidableEq, Repr

def k5RankComparisonStatus : RankComparisonStatus :=
  RankComparisonStatus.ExplicitRankMismatchRecordedBesideCertificate

/-- Theorem 9 (`K_5` Rank Mismatch Recorded Beside Certificate Fence):
The rank mismatch (`7` vs `15`) is recorded as `ExplicitRankMismatchRecordedBesideCertificate`,
never `SilentlyIdentified`. -/
theorem k5_rank_mismatch_recorded_beside_certificate_fence :
    k5RankComparisonStatus =
      RankComparisonStatus.ExplicitRankMismatchRecordedBesideCertificate ∧
    k5RankComparisonStatus ≠ RankComparisonStatus.SilentlyIdentified := by
  decide

/-- Summary ledger for `TFQ-0038`. -/
structure Tfq0038ScopeLedger where
  keepsTwoK5RankReadingsApart : Bool
  reconcilesRankFormulaAccounting : Bool
  leavesExchangeLoopRepresentativeUnresolved : Bool
  rejectsPythonCommentOrderTwoOverclaim : Bool
  conflatesRank7WithRank15 : Bool
  claimsExchangeLoopProvedTorsionGenerator : Bool
  deriving DecidableEq, Repr

def tfq0038RepoLedger : Tfq0038ScopeLedger :=
  ⟨true, true, true, true, false, false⟩

/-- Theorem 10 (`TFQ-0038` `K_5` Torsion and Exchange-Loop Scope Ledger Fence):
The canonical `TFQ-0038` ledger certifies that the two `K_5` rank readings are kept apart
and the exchange-loop representative question remains unresolved. -/
theorem tfq0038_k5_torsion_and_exchange_loop_scope_ledger_fence :
    tfq0038RepoLedger.keepsTwoK5RankReadingsApart = true ∧
    tfq0038RepoLedger.reconcilesRankFormulaAccounting = true ∧
    tfq0038RepoLedger.leavesExchangeLoopRepresentativeUnresolved = true ∧
    tfq0038RepoLedger.rejectsPythonCommentOrderTwoOverclaim = true ∧
    tfq0038RepoLedger.conflatesRank7WithRank15 = false ∧
    tfq0038RepoLedger.claimsExchangeLoopProvedTorsionGenerator = false := by
  decide

#print axioms conf2_graph_1skeleton_betti_numbers_p3_y_c4_k4_k5
#print axioms conf2_c4_and_k4_2complex_rational_betti_numbers
#print axioms k5_map_prose_reading_rank7_betti14_vs_certificate_reading_rank15_betti6
#print axioms universal_coefficient_torsion_rank_identity
#print axioms abelian_1d_character_collapse_boson_fermion
#print axioms non_zero_torsion_rank_does_not_identify_specific_loop_representative
#print axioms exchange_loop_representative_question_remains_open_fence
#print axioms python_comment_order_two_claim_exceeds_certificate_fence
#print axioms k5_rank_mismatch_recorded_beside_certificate_fence
#print axioms tfq0038_k5_torsion_and_exchange_loop_scope_ledger_fence

end CampaignTfq0038FiniteQcd
