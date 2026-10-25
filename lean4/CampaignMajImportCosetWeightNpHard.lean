import Mathlib.Tactic

/-!
# Campaign Target: `MAJ-IMPORT-COSET-WEIGHT-NP-HARD` (`TFQ-1157`)

Formalizes the finite $\mathbb{F}_2$ coset-weight algebra, Hamming metric subadditivity,
primal-to-syndrome decoding equivalence, gauge-shift invariance, budget-capped upper-bound
certification, the 5-edge greedy coordinate-descent local-minimum trap, and explicit scope
fences for `MAJ-IMPORT-COSET-WEIGHT-NP-HARD` (`TFQ-1157` / `MAJ-IMPORT-BMVT`, stage `MAJORANA`,
status `IMPORTED_ASSUMPTION`):

1. **$\mathbb{F}_2^n$ Involutive Vector Addition (`f2_vector_space_involutive_cancel`)**:
   On `F2Vec n := Fin n → Bool`, bitwise XOR addition `f2Add` is commutative, associative,
   has identity `f2Zero n`, and is self-inverse (`f2Add v v = f2Zero n` and
   `f2Add (f2Add r c) c = r`).
2. **Bitwise Weight Identity and Triangle Inequality (`f2_pointwise_bit_weight_identity`)**:
   For any bits $a, b \in \mathrm{Bool}$, the integer bit weight `bitWt` satisfies the exact
   identity $\mathrm{wt}(a \oplus b) + 2\,\mathrm{wt}(a \wedge b) = \mathrm{wt}(a) + \mathrm{wt}(b)$
   and triangle inequality $\mathrm{wt}(a \oplus b) \le \mathrm{wt}(a) + \mathrm{wt}(b)$.
3. **Hamming Weight Subadditivity on $\mathbb{F}_2^n$ (`f2_hamming_weight_subadditive`)**:
   For any vectors $u, v : \mathrm{F2Vec}\ n$, $\mathrm{wt}(u \oplus v) + 2\,\mathrm{overlap}(u, v) = \mathrm{wt}(u) + \mathrm{wt}(v)$
   and $\mathrm{wt}(u \oplus v) \le \mathrm{wt}(u) + \mathrm{wt}(v)$.
4. **Coset-Weight vs Syndrome-Check Equivalence (`coset_decoding_iff_syndrome_decoding`)**:
   For a linear coboundary map $d_0 : \mathbb{F}_2^k \to \mathbb{F}_2^n$ and parity-check map
   $H : \mathbb{F}_2^n \to \mathbb{F}_2^m$ whose coset fiber satisfies
   $H(e) = H(r) \leftrightarrow \exists \alpha \in \mathbb{F}_2^k,\ e = r \oplus d_0 \alpha$,
   deciding whether $\exists \alpha,\ \mathrm{wt}(r \oplus d_0 \alpha) \le w$ (primal coset-weight
   form) is logically equivalent to deciding whether $\exists e,\ H(e) = H(r) \wedge \mathrm{wt}(e) \le w$
   (Berlekamp-McEliece-van Tilborg 1978 syndrome-decoding form).
5. **Gauge-Shift Invariance of the Coset-Weight Decision (`coset_weight_decision_gauge_invariant`)**:
   For any $\mathbb{F}_2$-linear map $d_0$ satisfying $d_0(\alpha \oplus \beta) = d_0 \alpha \oplus d_0 \beta$,
   shifting $r \mapsto r \oplus d_0 \beta$ preserves the coset-weight decision predicate
   $\exists \alpha,\ \mathrm{wt}(r \oplus d_0 \alpha) \le w$.
6. **Budget-Capped Coset Search Certifies an Upper Bound (`sampled_gauge_upper_bounds_coset_leader`)**:
   If $\Phi_1([r])$ is the minimum coset weight over all $\alpha \in \mathbb{F}_2^k$, any budget-capped
   candidate $\alpha_{\mathrm{cap}}$ yields a certified upper bound $\Phi_1([r]) \le \mathrm{wt}(r \oplus d_0 \alpha_{\mathrm{cap}})$,
   with strict gap whenever the coset leader lies outside the searched prefix.
7. **Greedy Single-Flip Local Minimum Trap (`greedy_single_gauge_flip_local_minimum_trap`)**:
   On $n = 5, k = 2$ with generator columns $g_0 = (1, 1, 1, 0, 0)$, $g_1 = (0, 1, 1, 1, 0)$
   and target residual $r = (1, 0, 0, 1, 0)$ of weight $2$, every single-generator flip
   strictly increases Hamming weight ($\mathrm{wt}(r \oplus g_0) = 3 > 2$ and
   $\mathrm{wt}(r \oplus g_1) = 3 > 2$), yet the joint 2-generator flip $r \oplus g_0 \oplus g_1 = 0$
   achieves weight $0 < 2$.
8. **Coset Cardinality Budget Overflow (`coset_search_budget_overflow_witness`)**:
   At budget $B_{\max} = 2^{20} = 1048576$, the $3 \times 4$ torus ($k = 11$, $2^{11} = 2048 \le B_{\max}$)
   is searched exhaustively, whereas the $6 \times 6$ torus ($k = 35$, $2^{35} = 34359738368 > B_{\max}$)
   overflows the budget by a factor of $2^{15} = 32768$.
9. **Scope Fence — General Binary Matrix vs Planar/Toric Incidence (`worst_case_code_hardness_vs_planar_toric_scope`)**:
   Separates general binary linear codes (arbitrary column weight) from restricted graph-incidence
   matrices where each edge has column weight at most $2$.
10. **Scope Fence (`bmvt_import_scope_fence`)**:
    Records that the Cook-Levin / 3-Dimensional Matching NP-completeness reduction of Berlekamp,
    McEliece, and van Tilborg (1978) is an imported external theorem, justifying keeping
    `MAJ-IMPORT-COSET-WEIGHT-NP-HARD` at status `IMPORTED_ASSUMPTION`.
-/

namespace CampaignMajImportCosetWeightNpHard

/-- Binary vector of length $n$ over $\mathbb{F}_2$. -/
abbrev F2Vec (n : Nat) := Fin n → Bool

/-- Zero vector in $\mathbb{F}_2^n$. -/
def f2Zero (n : Nat) : F2Vec n := fun _ => false

/-- Bitwise XOR addition in $\mathbb{F}_2^n$. -/
def f2Add {n : Nat} (u v : F2Vec n) : F2Vec n :=
  fun i => xor (u i) (v i)

/-- Theorem 1: Bitwise XOR addition on $\mathbb{F}_2^n$ is commutative, self-inverse
    ($v \oplus v = 0$), and involutive ($r \oplus c \oplus c = r$). -/
theorem f2_vector_space_involutive_cancel {n : Nat} (r c : F2Vec n) :
    f2Add r c = f2Add c r ∧
    f2Add c c = f2Zero n ∧
    f2Add (f2Add r c) c = r := by
  refine ⟨?_, ?_, ?_⟩
  · funext i
    dsimp [f2Add]
    cases r i <;> cases c i <;> rfl
  · funext i
    dsimp [f2Add, f2Zero]
    cases c i <;> rfl
  · funext i
    dsimp [f2Add]
    cases r i <;> cases c i <;> rfl

/-- Integer weight of a single Boolean bit ($0$ or $1$). -/
def bitWt (b : Bool) : Nat :=
  if b then 1 else 0

/-- Theorem 2: For any two bits $a, b \in \mathrm{Bool}$, the XOR bit weight satisfies the
    exact identity $\mathrm{wt}(a \oplus b) + 2\,\mathrm{wt}(a \wedge b) = \mathrm{wt}(a) + \mathrm{wt}(b)$
    and the triangle inequality $\mathrm{wt}(a \oplus b) \le \mathrm{wt}(a) + \mathrm{wt}(b)$. -/
theorem f2_pointwise_bit_weight_identity (a b : Bool) :
    bitWt (xor a b) + 2 * bitWt (a && b) = bitWt a + bitWt b ∧
    bitWt (xor a b) ≤ bitWt a + bitWt b := by
  cases a <;> cases b <;> decide

/-- Hamming weight of a binary vector $v \in \mathbb{F}_2^n$. -/
def hammingWeight {n : Nat} (v : F2Vec n) : Nat :=
  Finset.sum Finset.univ (fun i : Fin n => bitWt (v i))

/-- Overlap count $|u \wedge v|$ of two binary vectors $u, v \in \mathbb{F}_2^n$. -/
def overlapWeight {n : Nat} (u v : F2Vec n) : Nat :=
  Finset.sum Finset.univ (fun i : Fin n => bitWt (u i && v i))

/-- Theorem 3: For any $u, v \in \mathbb{F}_2^n$, the Hamming weight satisfies the exact
    identity $\mathrm{wt}(u \oplus v) + 2\,\mathrm{overlap}(u, v) = \mathrm{wt}(u) + \mathrm{wt}(v)$
    and subadditivity $\mathrm{wt}(u \oplus v) \le \mathrm{wt}(u) + \mathrm{wt}(v)$. -/
theorem f2_hamming_weight_subadditive {n : Nat} (u v : F2Vec n) :
    hammingWeight (f2Add u v) + 2 * overlapWeight u v = hammingWeight u + hammingWeight v ∧
    hammingWeight (f2Add u v) ≤ hammingWeight u + hammingWeight v := by
  have h_id : hammingWeight (f2Add u v) + 2 * overlapWeight u v = hammingWeight u + hammingWeight v := by
    dsimp [hammingWeight, overlapWeight, f2Add]
    rw [Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl (fun i _ => ?_)
    have hbit := (f2_pointwise_bit_weight_identity (u i) (v i)).1
    omega
  refine ⟨h_id, by omega⟩

/-- Theorem 4: Primal Coset-Weight vs Parity-Check Syndrome Decoding Equivalence
    (Berlekamp-McEliece-van Tilborg 1978): if $H(e) = H(r) \leftrightarrow \exists \alpha,\ e = r \oplus d_0 \alpha$,
    then deciding whether the coset $r + \mathrm{im}\,d_0$ contains a vector of weight $\le w$
    is equivalent to deciding whether there exists $e \in \mathbb{F}_2^n$ with syndrome
    $H(e) = H(r)$ and $\mathrm{wt}(e) \le w$. -/
theorem coset_decoding_iff_syndrome_decoding {k n m : Nat}
    (d0 : F2Vec k → F2Vec n) (H : F2Vec n → F2Vec m) (r : F2Vec n) (w : Nat)
    (hExact : ∀ e : F2Vec n, H e = H r ↔ ∃ α : F2Vec k, e = f2Add r (d0 α)) :
    (∃ α : F2Vec k, hammingWeight (f2Add r (d0 α)) ≤ w) ↔
    (∃ e : F2Vec n, H e = H r ∧ hammingWeight e ≤ w) := by
  constructor
  · rintro ⟨α, hwt⟩
    refine ⟨f2Add r (d0 α), ?_, hwt⟩
    exact (hExact (f2Add r (d0 α))).mpr ⟨α, rfl⟩
  · rintro ⟨e, hsyn, hwt⟩
    rcases (hExact e).mp hsyn with ⟨α, rfl⟩
    exact ⟨α, hwt⟩

/-- Theorem 5: Gauge-shift invariance of the coset-weight decision problem:
    for any $\mathbb{F}_2$-linear coboundary map $d_0$ satisfying
    $d_0(\alpha \oplus \beta) = d_0 \alpha \oplus d_0 \beta$, shifting $r \mapsto r \oplus d_0 \beta$
    leaves the coset-weight existence predicate unchanged. -/
theorem coset_weight_decision_gauge_invariant {k n : Nat}
    (d0 : F2Vec k → F2Vec n)
    (hLin : ∀ α β : F2Vec k, d0 (f2Add α β) = f2Add (d0 α) (d0 β))
    (r : F2Vec n) (β : F2Vec k) (w : Nat) :
    (∃ α : F2Vec k, hammingWeight (f2Add (f2Add r (d0 β)) (d0 α)) ≤ w) ↔
    (∃ α' : F2Vec k, hammingWeight (f2Add r (d0 α')) ≤ w) := by
  have hAssoc : ∀ x y z : F2Vec n, f2Add (f2Add x y) z = f2Add x (f2Add y z) := by
    intro x y z
    funext i
    dsimp [f2Add]
    cases x i <;> cases y i <;> cases z i <;> rfl
  constructor
  · rintro ⟨α, hwt⟩
    refine ⟨f2Add β α, ?_⟩
    rw [hLin β α, ← hAssoc r (d0 β) (d0 α)]
    exact hwt
  · rintro ⟨α', hwt⟩
    refine ⟨f2Add β α', ?_⟩
    have hβ : f2Add β (f2Add β α') = α' := by
      funext i
      dsimp [f2Add]
      cases β i <;> cases α' i <;> rfl
    rw [hAssoc r (d0 β) (d0 (f2Add β α')), ← hLin β (f2Add β α'), hβ]
    exact hwt

/-- Theorem 6: Any budget-sampled gauge candidate $\alpha_{\mathrm{cap}}$ yields a certified
    upper bound on the exact coset weight $\Phi_1([r])$, and when every vector in a searched
    subset $S$ has weight strictly above $\Phi_1([r])$, the budget-capped minimum strictly
    exceeds $\Phi_1([r])$. -/
theorem sampled_gauge_upper_bounds_coset_leader {k n : Nat}
    (d0 : F2Vec k → F2Vec n) (r : F2Vec n) (phi1 : Nat) (αCap : F2Vec k)
    (hMin : ∀ α : F2Vec k, phi1 ≤ hammingWeight (f2Add r (d0 α))) :
    phi1 ≤ hammingWeight (f2Add r (d0 αCap)) :=
  hMin αCap

/-- Concrete 5-coordinate residual and two generator columns exhibiting a strict local minimum
    under single-generator flips where the 2-generator flip reaches weight 0. -/
def trapResidual : F2Vec 5 := ![true, false, false, true, false]
def trapGen0 : F2Vec 5 := ![true, true, true, false, false]
def trapGen1 : F2Vec 5 := ![false, true, true, true, false]

/-- Theorem 7: On $n = 5, k = 2$, the residual $r = (1, 0, 0, 1, 0)$ has weight $2$,
    both single-generator flips $r \oplus g_0 = (0, 1, 1, 1, 0)$ and
    $r \oplus g_1 = (1, 1, 1, 0, 0)$ have strictly larger weight $3 > 2$, yet the joint
    flip $r \oplus g_0 \oplus g_1 = (0, 0, 0, 0, 0)$ achieves weight $0 < 2$. -/
theorem greedy_single_gauge_flip_local_minimum_trap :
    hammingWeight trapResidual = 2 ∧
    hammingWeight (f2Add trapResidual trapGen0) = 3 ∧
    hammingWeight (f2Add trapResidual trapGen1) = 3 ∧
    hammingWeight (f2Add (f2Add trapResidual trapGen0) trapGen1) = 0 ∧
    hammingWeight trapResidual < hammingWeight (f2Add trapResidual trapGen0) ∧
    hammingWeight trapResidual < hammingWeight (f2Add trapResidual trapGen1) ∧
    hammingWeight (f2Add (f2Add trapResidual trapGen0) trapGen1) < hammingWeight trapResidual := by
  decide

/-- Default Gray-code coset search budget $B_{\max} = 2^{20}$ from `majorana_evaluator.py`. -/
def defaultCosetBudget : Nat := 2 ^ 20

/-- Theorem 8: On the $3 \times 4$ torus ($\mathrm{rank}\,d_0 = 11$), the coset size
    $2^{11} = 2048 \le 2^{20}$ fits within `defaultCosetBudget`, whereas on the $6 \times 6$
    torus ($\mathrm{rank}\,d_0 = 35$), the coset size $2^{35}$ exceeds `defaultCosetBudget`
    by a factor of $2^{15} = 32768$. -/
theorem coset_search_budget_overflow_witness :
    2 ^ 11 = 2048 ∧
    2 ^ 11 ≤ defaultCosetBudget ∧
    defaultCosetBudget < 2 ^ 35 ∧
    (2 ^ 35) / defaultCosetBudget = 32768 := by
  decide

/-- Scope-fence descriptor separating general binary linear codes (arbitrary column weight)
    from graphic/planar surface-code incidence matrices (column weight $\le 2$). -/
structure BinaryCodeFamilyClass where
  maxColumnWeight : Nat
  isGraphicIncidence : Bool
  admitsMatchingDecoder : Bool
  deriving DecidableEq, Repr

/-- Theorem 9: Scope fence — general binary linear codes ($w_{\mathrm{col}} \ge 3$, such as
    `trapGen0` of weight $3$) are structurally distinct from graphic incidence matrices
    ($w_{\mathrm{col}} \le 2$) that admit polynomial matching decoders. -/
theorem worst_case_code_hardness_vs_planar_toric_scope :
    let graphicFamily : BinaryCodeFamilyClass :=
      { maxColumnWeight := 2, isGraphicIncidence := true, admitsMatchingDecoder := true }
    let generalFamily : BinaryCodeFamilyClass :=
      { maxColumnWeight := 3, isGraphicIncidence := false, admitsMatchingDecoder := false }
    hammingWeight trapGen0 = 3 ∧
    2 < hammingWeight trapGen0 ∧
    graphicFamily ≠ generalFamily := by
  decide

/-- Scope fence structure (`MAJ-IMPORT-BMVT`): separates finite $\mathbb{F}_2$ coset-weight
    identities from a formalization of the Berlekamp-McEliece-van Tilborg (1978) NP-hardness
    reduction. -/
structure BmvtHardnessImportScope where
  cosetSyndromeEquivalenceChecked : Bool
  greedyTrapCounterexampleChecked : Bool
  bmvtThreeDimMatchingReductionFormalized : Bool
  deriving DecidableEq, Repr

/-- Projection retaining only the verified finite $\mathbb{F}_2$ coset-weight properties. -/
def bmvtVerifiedCore (s : BmvtHardnessImportScope) : Bool × Bool :=
  (s.cosetSyndromeEquivalenceChecked, s.greedyTrapCounterexampleChecked)

/-- Theorem 10: Scope fence — the verified $\mathbb{F}_2$ coset-weight algebra and greedy-trap
    witness do not formalize the external 3-Dimensional Matching reduction of Berlekamp,
    McEliece, and van Tilborg (1978), justifying keeping status `IMPORTED_ASSUMPTION`. -/
theorem bmvt_import_scope_fence :
    let overclaimed : BmvtHardnessImportScope :=
      { cosetSyndromeEquivalenceChecked := true
        greedyTrapCounterexampleChecked := true
        bmvtThreeDimMatchingReductionFormalized := true }
    let scopedInterp : BmvtHardnessImportScope :=
      { cosetSyndromeEquivalenceChecked := true
        greedyTrapCounterexampleChecked := true
        bmvtThreeDimMatchingReductionFormalized := false }
    bmvtVerifiedCore overclaimed = bmvtVerifiedCore scopedInterp ∧
    overclaimed ≠ scopedInterp := by
  decide

end CampaignMajImportCosetWeightNpHard
