/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Paper.lean
   Original sha256: 65cae01d6be4e3c085e4bc60297f7fa4f9b730f5b96eb91a3033d25ba89cc3a8 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.Genesis19l57g1.Paper
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.Genesis19l57g1.Derivation
import Imported.Genesis19l57g1.CanonicalMinimizer
import Imported.Genesis19l57g1.SecondRun
import Imported.Genesis19l57g1.PaperWire
import Imported.Genesis19l57g1.PaperSearch

/- Carrier-general manuscript statements, separate from the unchanged source. -/
namespace GenesisPaper

def ReportImage {H V : Type} (report : H → V) :=
  {v : V // ∃ h, report h = v}

theorem history_report_criterion {H V S : Type}
    (report : H → V) (answer : H → S) :
    (∃ factor : ReportImage report → S,
      ∀ h, factor ⟨report h, ⟨h, rfl⟩⟩ = answer h) ↔
    (∀ h h', report h = report h' → answer h = answer h') := by
  constructor
  · rintro ⟨factor, hf⟩ h h' heq
    have hv : (⟨report h, ⟨h, rfl⟩⟩ : ReportImage report) =
        ⟨report h', ⟨h', rfl⟩⟩ := Subtype.ext heq
    rw [← hf h, ← hf h', hv]
  · intro hc
    classical
    refine ⟨fun v => answer (Classical.choose v.property), ?_⟩
    intro h
    exact hc _ _ (Classical.choose_spec (show ∃ h', report h' = report h from ⟨h, rfl⟩))

theorem history_factor_unique {H V S : Type}
    (report : H → V) (answer : H → S)
    (a b : ReportImage report → S)
    (ha : ∀ h, a ⟨report h, ⟨h, rfl⟩⟩ = answer h)
    (hb : ∀ h, b ⟨report h, ⟨h, rfl⟩⟩ = answer h) : a = b := by
  funext v
  obtain ⟨h, hh⟩ := v.property
  have hv : (⟨report h, ⟨h, rfl⟩⟩ : ReportImage report) = v := Subtype.ext hh
  rw [← hv, ha, hb]

theorem collapsed_observation_barrier {A V S : Type}
    (report : A → V) (task : A → S) (x y : A)
    (same : report x = report y) (different : task x ≠ task y) :
    ¬ ∃ factor : V → S, ∀ a, factor (report a) = task a := by
  rintro ⟨factor, hf⟩
  apply different
  rw [← hf x, ← hf y, same]

-- A disjoint grammar partition: words without a hole, and words with a hole.
def fixedWords (n : Nat) : Nat → List (List (Option Nat))
  | 0 => [[]]
  | k + 1 => (List.range n).flatMap fun d => (fixedWords n k).map (some d :: ·)

def contextWords (n : Nat) : Nat → List (List (Option Nat))
  | 0 => []
  | k + 1 =>
      ((fixedWords n k ++ contextWords n k).map (none :: ·)) ++
      (List.range n).flatMap (fun d => (contextWords n k).map (some d :: ·))

def wellFormedWord (n : Nat) : List (Option Nat) → Prop
  | [] => True
  | none :: tail => wellFormedWord n tail
  | some d :: tail => d < n ∧ wellFormedWord n tail

theorem fixedWords_mem (n k : Nat) (word : List (Option Nat)) :
    word ∈ fixedWords n k ↔
      word.length = k ∧ wellFormedWord n word ∧ none ∉ word := by
  induction k generalizing word with
  | zero => cases word <;> simp [fixedWords, wellFormedWord]
  | succ k ih =>
      cases word with
      | nil => simp [fixedWords]
      | cons head tail =>
          cases head <;>
            simp [fixedWords, List.mem_flatMap, List.mem_map, ih, wellFormedWord,
              and_assoc, and_left_comm, and_comm]

theorem contextWords_mem (n k : Nat) (word : List (Option Nat)) :
    word ∈ contextWords n k ↔
      word.length = k ∧ wellFormedWord n word ∧ none ∈ word := by
  induction k generalizing word with
  | zero => cases word <;> simp [contextWords]
  | succ k ih =>
      cases word with
      | nil => simp [contextWords]
      | cons head tail =>
          cases head with
          | none =>
              by_cases hh : none ∈ tail <;>
                simp [contextWords, List.mem_flatMap, List.mem_map, fixedWords_mem,
                  ih, wellFormedWord, hh, and_assoc, and_left_comm, and_comm]
          | some d =>
              simp [contextWords, List.mem_flatMap, List.mem_map, fixedWords_mem,
                ih, wellFormedWord, and_assoc, and_left_comm, and_comm]

theorem prefix_nodup (slot : Option Nat) (words : List (List (Option Nat)))
    (h : words.Nodup) : (words.map (slot :: ·)).Nodup := by
  apply List.pairwise_map.mpr
  exact h.imp fun hne heq => hne (List.cons.inj heq).2

theorem dataPrefixes_nodup (n : Nat) (words : List (List (Option Nat)))
    (h : words.Nodup) :
    ((List.range n).flatMap fun d => words.map (some d :: ·)).Nodup := by
  apply List.pairwise_flatMap.mpr
  constructor
  · intro d _
    exact prefix_nodup (some d) words h
  · apply List.nodup_range.imp
    intro a b hne x hx y hy heq
    obtain ⟨u, _, rfl⟩ := List.mem_map.mp hx
    obtain ⟨v, _, rfl⟩ := List.mem_map.mp hy
    exact hne (Option.some.inj (List.cons.inj heq).1)

theorem fixedWords_nodup (n k : Nat) : (fixedWords n k).Nodup := by
  induction k with
  | zero => simp [fixedWords]
  | succ k ih => exact dataPrefixes_nodup n (fixedWords n k) ih

theorem contextWords_nodup (n k : Nat) : (contextWords n k).Nodup := by
  induction k with
  | zero => simp [contextWords]
  | succ k ih =>
      have hboth : (fixedWords n k ++ contextWords n k).Nodup := by
        apply List.nodup_append.mpr
        refine ⟨fixedWords_nodup n k, ih, ?_⟩
        intro a ha b hb heq
        have hf := (fixedWords_mem n k a).mp ha
        have hc := (contextWords_mem n k b).mp hb
        exact hf.2.2 (heq ▸ hc.2.2)
      apply List.nodup_append.mpr
      refine ⟨prefix_nodup none _ hboth, dataPrefixes_nodup n _ ih, ?_⟩
      intro a ha b hb heq
      obtain ⟨u, _, rfl⟩ := List.mem_map.mp ha
      obtain ⟨d, _, hd⟩ := List.mem_flatMap.mp hb
      obtain ⟨v, _, rfl⟩ := List.mem_map.mp hd
      simp at heq

theorem sum_map_constant {A : Type} (xs : List A) (m : Nat) :
    (xs.map fun _ => m).sum = xs.length * m := by
  induction xs with
  | nil => simp
  | cons a xs ih => simp [ih, Nat.succ_mul, Nat.add_comm]

theorem fixedWords_length (n k : Nat) : (fixedWords n k).length = n ^ k := by
  induction k with
  | zero => simp [fixedWords]
  | succ k ih => simp [fixedWords, List.length_flatMap, ih, sum_map_constant, Nat.pow_succ, Nat.mul_comm]

theorem contextWords_count_partition (n k : Nat) :
    (contextWords n k).length + n ^ k = (n + 1) ^ k := by
  induction k with
  | zero => simp [contextWords]
  | succ k ih =>
      simp only [contextWords, List.length_append, List.length_map, fixedWords_length]
      simp only [List.length_flatMap, List.length_map]
      rw [sum_map_constant, List.length_range]
      rw [Nat.pow_succ, Nat.pow_succ, ← ih]
      simp only [Nat.mul_add, Nat.mul_one, Nat.mul_comm]
      omega

theorem contextWords_length (n k : Nat) :
    (contextWords n k).length = (n + 1) ^ k - n ^ k := by
  have h := contextWords_count_partition n k
  omega

-- A terminal endpoint of the unguarded policy cannot contain an unresolved
-- pair: this discharges the no-dead-end part separately from the run bound.
def PolicyTerminal (r : Derivation.Regime) : Prop :=
  ∀ i j, i < j → j < r.data → ¬ Derivation.separable r i j →
    ¬ ∃ delta, Derivation.validResponse r i j delta

theorem policy_terminal_separates (r : Derivation.Regime) (hwf : r.wf)
    (hreqs : ∀ q ∈ r.reqs, Derivation.separable r q.1 q.2)
    (terminal : PolicyTerminal r) :
    ∀ i j, i < j → j < r.data → Derivation.separable r i j := by
  intro i j hij hj
  classical
  apply Classical.byContradiction
  intro unresolved
  apply terminal i j hij hj unresolved
  exact ⟨_, Derivation.mark_progress r hwf i j (Nat.lt_trans hij hj) hj
    (Nat.ne_of_lt hij) hreqs⟩

end GenesisPaper
