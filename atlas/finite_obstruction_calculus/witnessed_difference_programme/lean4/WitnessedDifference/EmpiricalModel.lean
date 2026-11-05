import Mathlib.Algebra.BigOperators.Field
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Fintype.Prod
import Mathlib.Algebra.Ring.Rat
import Mathlib.Algebra.Order.Field.Rat
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity

/-!
# Empirical models from finite run tables

`WDP-CH19-O01` asks for a typed map from finite measurement packets to an
empirical model on a declared measurement cover, with a proof of which observer
and evaluator fields survive the map. This module is the part of that map that
does not depend on the packet type; `PacketAdapter` instantiates it with the
measurement packets of Chapter 13.

A declared cover is a family `ctx : ι → Finset X` of contexts. A run in a
context holds one packet for each measurement of the context. Each packet must
be admissible for its measurement, and a declared readout turns it into an
outcome. A table lists the runs recorded in each context. The adapter
normalizes outcome counts into frequencies. It refuses a table with an empty
context, and it refuses a table whose frequencies disagree on the overlap of
two contexts, naming the overlap section where they differ. Otherwise it returns an
empirical model in the sense of Abramsky and Brandenburger: one distribution
per context, compatible on overlaps.

What survives the map: the support of each context distribution is exactly the
set of recorded outcomes, and two tables have the same image exactly when their
outcome counts in each context are proportional. A packet field reaches the
image only through the outcome it reports; fields the readout never reads, the
order of runs, and absolute counts do not affect it.

Weights are rational throughout. When every outcome of every measurement is
reported by some admissible packet, the image of the adapter is every empirical
model on the cover, so packets neither force nor exclude contextuality, and a
model is noncontextual exactly when one table of global runs, each measuring
every measurement at once, restricts to a table with that image. On the CHSH
cover every global table obeys `CHSH ≤ 2`, while a table whose image is the PR
box reaches `4`; the PR box has a signed global section but no nonnegative
one.
-/

namespace WitnessedDifference.Empirical

open Finset

universe u v w z

/-! ## Sections, marginals and empirical models -/

section Sections

variable {X : Type u} {O : Type v}

/-- Restrict a section over `C` to a subset `D`. -/
def restrict {C D : Finset X} (h : D ⊆ C) (s : C → O) : D → O :=
  fun x => s ⟨x.1, h x.2⟩

/-- Restrict a global assignment to a finite set of measurements. -/
def restrictGlobal (C : Finset X) (g : X → O) : C → O :=
  fun x => g x.1

@[simp] theorem restrict_restrictGlobal {C D : Finset X} (h : D ⊆ C)
    (g : X → O) : restrict h (restrictGlobal C g) = restrictGlobal D g :=
  rfl

end Sections

/-- Push weights on the sections of `C` down to the sections of `D ⊆ C`. -/
def marginal {X : Type u} [DecidableEq X] {O : Type v} [Fintype O]
    [DecidableEq O] {C D : Finset X} (h : D ⊆ C) (p : (C → O) → ℚ)
    (t : D → O) : ℚ :=
  ∑ s ∈ univ.filter (fun s => restrict h s = t), p s

/-- Weights on the contexts of a cover agree on the overlap of every two
contexts. -/
def Compatible {X : Type u} [DecidableEq X] {O : Type v} [Fintype O]
    [DecidableEq O] {ι : Type w} (ctx : ι → Finset X)
    (weight : ∀ i, (ctx i → O) → ℚ) : Prop :=
  ∀ i j (t : ↥(ctx i ∩ ctx j) → O),
    marginal inter_subset_left (weight i) t =
      marginal inter_subset_right (weight j) t

/-- An empirical model on the declared cover `ctx`: a probability distribution
on the sections of each context, compatible on overlaps. -/
@[ext]
structure EmpiricalModel {X : Type u} [DecidableEq X] {ι : Type w}
    (ctx : ι → Finset X) (O : Type v) [Fintype O] [DecidableEq O] where
  weight : ∀ i, (ctx i → O) → ℚ
  nonneg : ∀ i s, 0 ≤ weight i s
  normalized : ∀ i, ∑ s, weight i s = 1
  compatible : Compatible ctx weight

section Global

variable {X : Type u} [DecidableEq X] [Fintype X] {O : Type v} [Fintype O]
  [DecidableEq O] {ι : Type w}

/-- `d` is a global section of `weight`: weights on global assignments, of
total one, whose restriction to each context is `weight`. The weights may be
negative. -/
def IsGlobalSection (ctx : ι → Finset X) (weight : ∀ i, (ctx i → O) → ℚ)
    (d : (X → O) → ℚ) : Prop :=
  ∑ g, d g = 1 ∧
    ∀ i s, weight i s =
      ∑ g ∈ univ.filter (fun g => restrictGlobal (ctx i) g = s), d g

/-- Noncontextual: some nonnegative global section exists. -/
def IsNoncontextual (ctx : ι → Finset X) (weight : ∀ i, (ctx i → O) → ℚ) :
    Prop :=
  ∃ d : (X → O) → ℚ, (∀ g, 0 ≤ d g) ∧ IsGlobalSection ctx weight d

/-- Strongly contextual: no global assignment restricts, in every context, to
a section of positive weight. -/
def IsStronglyContextual (ctx : ι → Finset X)
    (weight : ∀ i, (ctx i → O) → ℚ) : Prop :=
  ¬ ∃ g : X → O, ∀ i, 0 < weight i (restrictGlobal (ctx i) g)

theorem marginal_global {C D : Finset X} (h : D ⊆ C) (d : (X → O) → ℚ)
    (t : D → O) :
    marginal h
        (fun s => ∑ g ∈ univ.filter (fun g => restrictGlobal C g = s), d g) t =
      ∑ g ∈ univ.filter (fun g => restrictGlobal D g = t), d g := by
  unfold marginal
  rw [Finset.sum_comm' (t' := univ.filter (fun g => restrictGlobal D g = t))
    (s' := fun g => {restrictGlobal C g})]
  · simp
  · intro s g
    simp only [mem_filter, mem_univ, true_and, mem_singleton]
    constructor
    · rintro ⟨hs, rfl⟩
      exact ⟨rfl, hs⟩
    · rintro ⟨rfl, hg⟩
      exact ⟨hg, rfl⟩

/-- Any weights obtained by restricting one global function, signed or not,
agree on overlaps. -/
theorem compatible_of_global (ctx : ι → Finset X) (d : (X → O) → ℚ) :
    Compatible ctx
      (fun i s => ∑ g ∈ univ.filter (fun g => restrictGlobal (ctx i) g = s),
        d g) := by
  intro i j t
  simp only
  rw [marginal_global, marginal_global]

theorem sum_global (C : Finset X) (d : (X → O) → ℚ) :
    ∑ s : C → O, ∑ g ∈ univ.filter (fun g => restrictGlobal C g = s), d g =
      ∑ g, d g :=
  Finset.sum_fiberwise univ (restrictGlobal C) d

theorem sum_global_mul (C : Finset X) (d : (X → O) → ℚ) (f : (C → O) → ℚ) :
    ∑ s : C → O,
        (∑ g ∈ univ.filter (fun g => restrictGlobal C g = s), d g) * f s =
      ∑ g, d g * f (restrictGlobal C g) := by
  simp_rw [sum_mul]
  rw [← Finset.sum_fiberwise univ (restrictGlobal C)
    (fun g => d g * f (restrictGlobal C g))]
  refine sum_congr rfl fun s _ => sum_congr rfl fun g hg => ?_
  rw [(mem_filter.1 hg).2]

/-- A global section is determined by its values, so the weights it restricts
to are compatible and normalized. -/
theorem isGlobalSection_iff {ctx : ι → Finset X}
    {weight : ∀ i, (ctx i → O) → ℚ} {d : (X → O) → ℚ} :
    IsGlobalSection ctx weight d ↔
      ∑ g, d g = 1 ∧ weight = fun i s =>
        ∑ g ∈ univ.filter (fun g => restrictGlobal (ctx i) g = s), d g := by
  unfold IsGlobalSection
  constructor
  · rintro ⟨h1, h⟩
    exact ⟨h1, funext fun i => funext fun s => h i s⟩
  · rintro ⟨h1, rfl⟩
    exact ⟨h1, fun _ _ => rfl⟩

/-- Weights with a nonnegative global section form an empirical model. -/
def EmpiricalModel.ofGlobal (ctx : ι → Finset X) (d : (X → O) → ℚ)
    (h0 : ∀ g, 0 ≤ d g) (h1 : ∑ g, d g = 1) : EmpiricalModel ctx O where
  weight i s := ∑ g ∈ univ.filter (fun g => restrictGlobal (ctx i) g = s), d g
  nonneg _ _ := sum_nonneg fun g _ => h0 g
  normalized i := (sum_global (ctx i) d).trans h1
  compatible := compatible_of_global ctx d

/-- Strong contextuality rules out every nonnegative global section. -/
theorem not_noncontextual_of_strongly {ctx : ι → Finset X}
    {weight : ∀ i, (ctx i → O) → ℚ}
    (hstrong : IsStronglyContextual ctx weight) :
    ¬ IsNoncontextual ctx weight := by
  rintro ⟨d, h0, h1, hd⟩
  apply hstrong
  have hpos : ∃ g, 0 < d g := by
    by_contra hcon
    have hle : ∀ g, d g ≤ 0 := fun g => not_lt.1 fun hg => hcon ⟨g, hg⟩
    have : ∑ g, d g ≤ 0 := sum_nonpos fun g _ => hle g
    linarith
  obtain ⟨g, hg⟩ := hpos
  refine ⟨g, fun i => ?_⟩
  rw [hd]
  exact lt_of_lt_of_le hg
    (single_le_sum (f := d) (fun g' _ => h0 g') (by simp))

end Global

/-! ## Runs, tables and frequencies -/

/-- A run in context `C`: one admissible packet for each measurement of `C`. -/
structure Run {X : Type u} (P : Type z) (admissible : X → P → Prop)
    (C : Finset X) where
  packet : C → P
  admissible_packet : ∀ x : C, admissible x.1 (packet x)

/-- A global run: one admissible packet for every measurement. -/
structure GlobalRun {X : Type u} (P : Type z) (admissible : X → P → Prop) where
  packet : X → P
  admissible_packet : ∀ x, admissible x (packet x)

section Lists

/-- Counting a list by the fibres of a map to a finite type. -/
theorem sum_countP_smul {α : Type*} {β : Type*} {M : Type*} [Fintype β]
    [DecidableEq β] [AddCommMonoid M] (l : List α) (o : α → β) (f : β → M) :
    ∑ b, (l.countP fun a => o a = b) • f b = (l.map fun a => f (o a)).sum := by
  induction l with
  | nil => simp
  | cons a l ih =>
    simp only [List.countP_cons, add_nsmul, sum_add_distrib, ih, List.map_cons,
      List.sum_cons]
    rw [add_comm]
    congr 1
    rw [Finset.sum_eq_single (o a)]
    · simp only [decide_true, if_true, one_nsmul]
    · intro b _ hb
      simp [Ne.symm hb]
    · simp

theorem countP_comp_eq_sum {α : Type*} {β : Type*} [Fintype β]
    [DecidableEq β] (l : List α) (o : α → β) (p : β → Prop)
    [DecidablePred p] :
    l.countP (fun a => p (o a)) =
      ∑ b ∈ univ.filter p, l.countP fun a => o a = b := by
  induction l with
  | nil => simp
  | cons a l ih =>
    simp only [List.countP_cons, ih, sum_add_distrib]
    congr 1
    simp only [decide_eq_true_eq]
    rw [Finset.sum_ite_eq]
    simp

theorem exists_nat_eq_mul {q : ℚ} (hq : 0 ≤ q) {N : ℕ} (hN : q.den ∣ N) :
    ∃ k : ℕ, (k : ℚ) = q * N := by
  obtain ⟨c, rfl⟩ := hN
  refine ⟨q.num.toNat * c, ?_⟩
  have hnum : ((q.num.toNat : ℕ) : ℚ) = (q.num : ℚ) := by
    exact_mod_cast Int.toNat_of_nonneg (Rat.num_nonneg.2 hq)
  rw [Nat.cast_mul, hnum, Nat.cast_mul, ← mul_assoc, Rat.mul_den_eq_num]

/-- Every rational distribution on a finite type is the frequency table of some
nonempty finite list. -/
theorem exists_list_of_distribution {β : Type*} [Fintype β] [DecidableEq β]
    (w : β → ℚ) (h0 : ∀ b, 0 ≤ w b) (h1 : ∑ b, w b = 1) :
    ∃ l : List β, l ≠ [] ∧
      ∀ b, ((l.countP fun c => c = b : ℕ) : ℚ) / l.length = w b := by
  set N : ℕ := ∏ b, (w b).den with hN
  have hNpos : 0 < N := Finset.prod_pos fun b _ => (w b).den_pos
  have hk : ∀ b, ∃ k : ℕ, (k : ℚ) = w b * N := fun b =>
    exists_nat_eq_mul (h0 b) (Finset.dvd_prod_of_mem _ (mem_univ b))
  choose k hk using hk
  set l : List β := univ.toList.flatMap fun b => List.replicate (k b) b
  have hcount : ∀ b, (l.countP fun c => c = b) = k b := by
    intro b
    simp only [l, List.countP_flatMap, List.countP_replicate,
      Function.comp_def, Finset.sum_map_toList]
    simp
  have hlen : (l.length : ℚ) = N := by
    have hsum : ∑ b, (l.countP fun c => c = b) = l.length := by
      simpa using sum_countP_smul l id (fun _ => (1 : ℕ))
    rw [← hsum]
    push_cast
    simp_rw [hcount, hk, ← sum_mul, h1, one_mul]
  have hNq : (N : ℚ) ≠ 0 := by exact_mod_cast hNpos.ne'
  refine ⟨l, ?_, fun b => ?_⟩
  · intro hl
    rw [hl] at hlen
    simp at hlen
    exact hNq hlen.symm
  · rw [hcount, hlen, hk, mul_div_cancel_right₀ _ hNq]

end Lists

section Tables

variable {X : Type u} [DecidableEq X] {O : Type v} [Fintype O] [DecidableEq O]
  {ι : Type w} {P : Type z} {admissible : X → P → Prop}
  (readout : X → P → O)

/-- The outcome a run reports: the readout of each of its packets. -/
def Run.outcome {C : Finset X} (r : Run P admissible C) : C → O :=
  fun x => readout x.1 (r.packet x)

/-- How many runs of a table report the section `s`. -/
def count {C : Finset X} (T : List (Run P admissible C)) (s : C → O) : ℕ :=
  T.countP fun r => r.outcome readout = s

/-- The normalized multiplicity of `s` in a table (Chapter 8). -/
def freq {C : Finset X} (T : List (Run P admissible C)) (s : C → O) : ℚ :=
  (count readout T s : ℚ) / T.length

/-- The frequencies of a table on a declared cover. -/
def freqs (ctx : ι → Finset X) (T : ∀ i, List (Run P admissible (ctx i))) :
    ∀ i, (ctx i → O) → ℚ :=
  fun i => freq readout (T i)

theorem sum_count_mul {C : Finset X} (T : List (Run P admissible C))
    (f : (C → O) → ℚ) :
    ∑ s, (count readout T s : ℚ) * f s =
      (T.map fun r => f (r.outcome readout)).sum := by
  simpa [count, nsmul_eq_mul] using sum_countP_smul T (Run.outcome readout) f

theorem sum_count {C : Finset X} (T : List (Run P admissible C)) :
    ∑ s, count readout T s = T.length := by
  simpa [count] using sum_countP_smul T (Run.outcome readout)
    (fun _ => (1 : ℕ))

omit [DecidableEq X] [Fintype O] in
theorem freq_nonneg {C : Finset X} (T : List (Run P admissible C))
    (s : C → O) : 0 ≤ freq readout T s :=
  div_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _)

theorem sum_freq {C : Finset X} (T : List (Run P admissible C)) (hT : T ≠ []) :
    ∑ s, freq readout T s = 1 := by
  have hlen : (T.length : ℚ) ≠ 0 := by
    exact_mod_cast (List.length_pos_iff.2 hT).ne'
  simp only [freq, ← sum_div]
  rw [← Nat.cast_sum, sum_count, div_self hlen]

/-- Expectation under the frequencies is the average over runs. -/
theorem sum_freq_mul {C : Finset X} (T : List (Run P admissible C))
    (f : (C → O) → ℚ) :
    ∑ s, freq readout T s * f s =
      (T.map fun r => f (r.outcome readout)).sum / T.length := by
  simp only [freq, div_mul_eq_mul_div, ← sum_div, sum_count_mul]

omit [DecidableEq X] [Fintype O] in
/-- A section has positive frequency exactly when some recorded run reports
it. -/
theorem freq_pos_iff {C : Finset X} (T : List (Run P admissible C))
    (s : C → O) :
    0 < freq readout T s ↔ ∃ r ∈ T, r.outcome readout = s := by
  have hcount : 0 < count readout T s ↔ ∃ r ∈ T, r.outcome readout = s := by
    simp [count]
  rw [← hcount]
  constructor
  · intro h
    by_contra h0
    have : count readout T s = 0 := by omega
    simp [freq, this] at h
  · intro h
    have hl : 0 < T.length := by
      obtain ⟨r, hr, -⟩ := hcount.1 h
      exact List.length_pos_of_mem hr
    exact div_pos (by exact_mod_cast h) (by exact_mod_cast hl)

omit [DecidableEq X] [Fintype O] in
/-- The frequencies ignore the order of runs. -/
theorem freq_perm {C : Finset X} {T T' : List (Run P admissible C)}
    (h : T.Perm T') : freq readout T = freq readout T' := by
  funext s
  simp only [freq, count, h.countP_eq, h.length_eq]

omit [DecidableEq X] [Fintype O] in
/-- Two nonempty tables have the same frequencies exactly when their outcome
counts are proportional. -/
theorem freq_eq_freq_iff {C : Finset X} {P' : Type*}
    {admissible' : X → P' → Prop} (readout' : X → P' → O)
    {T : List (Run P admissible C)} {T' : List (Run P' admissible' C)}
    (hT : T ≠ []) (hT' : T' ≠ []) :
    freq readout T = freq readout' T' ↔
      ∀ s, count readout T s * T'.length = count readout' T' s * T.length := by
  have h1 : (T.length : ℚ) ≠ 0 := by
    exact_mod_cast (List.length_pos_iff.2 hT).ne'
  have h2 : (T'.length : ℚ) ≠ 0 := by
    exact_mod_cast (List.length_pos_iff.2 hT').ne'
  rw [funext_iff]
  refine forall_congr' fun s => ?_
  rw [freq, freq, div_eq_div_iff h1 h2]
  norm_cast

omit [DecidableEq X] [Fintype O] in
/-- The frequencies of a table depend only on its list of outcomes. -/
theorem freq_eq_of_outcomes {C : Finset X} {P' : Type*}
    {admissible' : X → P' → Prop} (readout' : X → P' → O)
    {T : List (Run P admissible C)} {T' : List (Run P' admissible' C)}
    (h : T.map (Run.outcome readout) = T'.map (Run.outcome readout')) :
    freq readout T = freq readout' T' := by
  funext s
  have hc : count readout T s = count readout' T' s := by
    have := congrArg (List.countP fun o => decide (o = s)) h
    simpa [count, List.countP_map, Function.comp_def] using this
  have hl : T.length = T'.length := by
    simpa using congrArg List.length h
  simp only [freq, hc, hl]

omit [DecidableEq X] [Fintype O] in
/-- Mapping runs without changing their outcomes leaves the frequencies
unchanged. -/
theorem freq_map {C : Finset X} {P' : Type*} {admissible' : X → P' → Prop}
    (readout' : X → P' → O)
    (f : Run P admissible C → Run P' admissible' C)
    (hf : ∀ r, (f r).outcome readout' = r.outcome readout)
    (T : List (Run P admissible C)) :
    freq readout' (T.map f) = freq readout T := by
  funext s
  simp only [freq, count, List.countP_map, List.length_map, Function.comp_def,
    hf]

/-- Replace every packet of a run. -/
def Run.mapPacket {C : Finset X} {P' : Type*} {admissible' : X → P' → Prop}
    (φ : P → P') (hφ : ∀ x p, admissible x p → admissible' x (φ p))
    (r : Run P admissible C) : Run P' admissible' C :=
  ⟨fun x => φ (r.packet x), fun x => hφ x.1 _ (r.admissible_packet x)⟩

omit [DecidableEq X] [Fintype O] in
/-- Replacing packets by packets with the same readout leaves the frequencies
unchanged: every packet field that does not reach the readout is lost. -/
theorem freq_mapPacket {C : Finset X} {P' : Type*}
    {admissible' : X → P' → Prop} (readout' : X → P' → O) (φ : P → P')
    (hφ : ∀ x p, admissible x p → admissible' x (φ p))
    (hread : ∀ x p, admissible x p → readout' x (φ p) = readout x p)
    (T : List (Run P admissible C)) :
    freq readout' (T.map (Run.mapPacket φ hφ)) = freq readout T :=
  freq_map readout readout' (Run.mapPacket φ hφ)
    (fun r => funext fun x => hread x.1 _ (r.admissible_packet x)) T

/-! ## The typed adapter -/

/-- Why the adapter declines a table, with the evidence. -/
inductive Refusal (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i))) : Type (max u v w)
  /-- Context `i` has no runs, so it has no frequencies. -/
  | emptyContext (i : ι) (empty : T i = [])
  /-- The frequencies of contexts `i` and `j` disagree on their overlap. -/
  | signalling (i j : ι) (t : ↥(ctx i ∩ ctx j) → O)
      (differ : marginal inter_subset_left (freq readout (T i)) t ≠
        marginal inter_subset_right (freq readout (T j)) t)

/-- The signalling refusal extracted from a failed compatibility check. -/
noncomputable def Refusal.ofIncompatible (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i)))
    (hc : ¬ Compatible ctx (freqs readout ctx T)) : Refusal readout ctx T :=
  have h : ∃ i j, ∃ t : ↥(ctx i ∩ ctx j) → O,
      marginal inter_subset_left (freq readout (T i)) t ≠
        marginal inter_subset_right (freq readout (T j)) t := by
    simpa [Compatible, freqs] using hc
  .signalling h.choose h.choose_spec.choose h.choose_spec.choose_spec.choose
    h.choose_spec.choose_spec.choose_spec

open Classical in
/-- The typed map from run tables on a declared cover to empirical models. -/
noncomputable def adapt (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i))) :
    Refusal readout ctx T ⊕ EmpiricalModel ctx O :=
  if h : ∃ i, T i = [] then .inl (.emptyContext h.choose h.choose_spec)
  else if hc : Compatible ctx (freqs readout ctx T) then
    .inr
      { weight := freqs readout ctx T
        nonneg := fun i s => freq_nonneg readout (T i) s
        normalized := fun i => sum_freq readout (T i) fun he => h ⟨i, he⟩
        compatible := hc }
  else .inl (Refusal.ofIncompatible readout ctx T hc)

/-- The adapter returns `m` exactly when no context is empty and `m` is the
table of frequencies. -/
theorem adapt_eq_inr_iff (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i))) (m : EmpiricalModel ctx O) :
    adapt readout ctx T = .inr m ↔
      (∀ i, T i ≠ []) ∧ m.weight = freqs readout ctx T := by
  unfold adapt
  split_ifs with h hc
  · simp only [false_iff, not_and]
    obtain ⟨i, hi⟩ := h
    exact fun hne => absurd hi (hne i)
  · simp only [Sum.inr.injEq]
    constructor
    · rintro rfl
      exact ⟨fun i hi => h ⟨i, hi⟩, rfl⟩
    · rintro ⟨-, hw⟩
      ext1
      exact hw.symm
  · simp only [false_iff, not_and]
    intro _ hw
    exact hc (hw ▸ m.compatible)

/-- The adapter succeeds exactly on tables with no empty context whose
frequencies agree on every overlap. -/
theorem adapt_succeeds_iff (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i))) :
    (∃ m, adapt readout ctx T = .inr m) ↔
      (∀ i, T i ≠ []) ∧ Compatible ctx (freqs readout ctx T) := by
  constructor
  · rintro ⟨m, hm⟩
    obtain ⟨hne, hw⟩ := (adapt_eq_inr_iff readout ctx T m).1 hm
    exact ⟨hne, hw ▸ m.compatible⟩
  · rintro ⟨hne, hc⟩
    exact ⟨⟨freqs readout ctx T, fun i s => freq_nonneg readout (T i) s,
      fun i => sum_freq readout (T i) (hne i), hc⟩,
      (adapt_eq_inr_iff readout ctx T _).2 ⟨hne, rfl⟩⟩

/-- The support of the image is exactly the set of recorded outcomes. -/
theorem adapt_support (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i))) {m : EmpiricalModel ctx O}
    (hm : adapt readout ctx T = .inr m) (i : ι) (s : ctx i → O) :
    0 < m.weight i s ↔ ∃ r ∈ T i, r.outcome readout = s := by
  obtain ⟨-, hw⟩ := (adapt_eq_inr_iff readout ctx T m).1 hm
  rw [hw]
  exact freq_pos_iff readout (T i) s

/-! ## The image is every rational empirical model -/

/-- If every outcome of every measurement can be reported by an admissible
packet, every empirical model on the cover is the image of some table. -/
theorem exists_table (ctx : ι → Finset X)
    (realize : ∀ x o, ∃ p, admissible x p ∧ readout x p = o)
    (m : EmpiricalModel ctx O) :
    ∃ T : ∀ i, List (Run P admissible (ctx i)), adapt readout ctx T = .inr m := by
  choose pk hpk using realize
  let mk : ∀ i, (ctx i → O) → Run P admissible (ctx i) := fun _ s =>
    ⟨fun x => pk x.1 (s x), fun x => (hpk x.1 (s x)).1⟩
  have hmk : ∀ i s, (mk i s).outcome readout = s := fun _ s =>
    funext fun x => (hpk x.1 (s x)).2
  have hl : ∀ i, ∃ l : List (ctx i → O), l ≠ [] ∧
      ∀ s, ((l.countP fun c => c = s : ℕ) : ℚ) / l.length = m.weight i s :=
    fun i => exists_list_of_distribution (m.weight i) (m.nonneg i)
      (m.normalized i)
  choose l hne hfreq using hl
  refine ⟨fun i => (l i).map (mk i), ?_⟩
  rw [adapt_eq_inr_iff]
  refine ⟨fun i => by simpa using hne i, ?_⟩
  funext i s
  simp only [freqs, freq, count, List.countP_map, List.length_map,
    Function.comp_def, hmk]
  exact (hfreq i s).symm

/-! ## Global runs and noncontextuality -/

/-- The outcome a global run reports for every measurement. -/
def GlobalRun.outcome (g : GlobalRun P admissible) : X → O :=
  fun x => readout x (g.packet x)

/-- Read a global run in one context only. -/
def GlobalRun.restrictTo (g : GlobalRun P admissible) (C : Finset X) :
    Run P admissible C :=
  ⟨fun x => g.packet x.1, fun x => g.admissible_packet x.1⟩

omit [DecidableEq X] [Fintype O] [DecidableEq O] in
@[simp] theorem GlobalRun.outcome_restrictTo (g : GlobalRun P admissible)
    (C : Finset X) :
    (g.restrictTo C).outcome readout = restrictGlobal C (g.outcome readout) :=
  rfl

/-- The table in which every context reads the same global runs. -/
def restrictTable (ctx : ι → Finset X) (G : List (GlobalRun P admissible)) :
    ∀ i, List (Run P admissible (ctx i)) :=
  fun i => G.map fun g => g.restrictTo (ctx i)

variable [Fintype X]

/-- The normalized multiplicity of a global assignment in a global table. -/
def globalFreq (G : List (GlobalRun P admissible)) (a : X → O) : ℚ :=
  ((G.countP fun g => g.outcome readout = a : ℕ) : ℚ) / G.length

theorem freq_restrictTable (ctx : ι → Finset X)
    (G : List (GlobalRun P admissible)) (i : ι) (s : ctx i → O) :
    freq readout (restrictTable ctx G i) s =
      ∑ a ∈ univ.filter (fun a => restrictGlobal (ctx i) a = s),
        globalFreq readout G a := by
  simp only [freq, count, restrictTable, List.countP_map, List.length_map,
    globalFreq, ← sum_div, Function.comp_def, GlobalRun.outcome_restrictTo]
  congr 1
  exact_mod_cast countP_comp_eq_sum G (GlobalRun.outcome readout)
    (fun a => restrictGlobal (ctx i) a = s)

/-- The frequencies of a restricted global table have a nonnegative global
section, namely the global frequencies. -/
theorem noncontextual_of_global_table (ctx : ι → Finset X)
    (G : List (GlobalRun P admissible)) (hG : G ≠ []) :
    IsNoncontextual ctx (freqs readout ctx (restrictTable ctx G)) := by
  refine ⟨globalFreq readout G, fun a => div_nonneg (Nat.cast_nonneg _)
    (Nat.cast_nonneg _), ?_, fun i s => freq_restrictTable readout ctx G i s⟩
  have hlen : (G.length : ℚ) ≠ 0 := by
    exact_mod_cast (List.length_pos_iff.2 hG).ne'
  have htot : ∑ a, (G.countP fun g => g.outcome readout = a) = G.length := by
    simpa using sum_countP_smul G (GlobalRun.outcome readout)
      (fun _ => (1 : ℕ))
  simp only [globalFreq, ← sum_div]
  rw [← Nat.cast_sum, htot, div_self hlen]

/-- A global table restricts to a table the adapter accepts. -/
theorem adapt_restrictTable (ctx : ι → Finset X)
    (G : List (GlobalRun P admissible)) (hG : G ≠ []) :
    ∃ m, adapt readout ctx (restrictTable ctx G) = .inr m := by
  obtain ⟨d, h0, h1, hd⟩ := noncontextual_of_global_table readout ctx G hG
  refine (adapt_succeeds_iff readout ctx _).2 ⟨fun i => ?_, ?_⟩
  · simpa [restrictTable] using hG
  · have hw : freqs readout ctx (restrictTable ctx G) =
        fun i s => ∑ g ∈ univ.filter (fun g => restrictGlobal (ctx i) g = s),
          d g := funext fun i => funext fun s => hd i s
    rw [hw]
    exact compatible_of_global ctx d

/-- An empirical model is noncontextual exactly when a table of global runs,
each reading every measurement at once, restricts to a table with that
image. -/
theorem noncontextual_iff_global_table (ctx : ι → Finset X)
    (realize : ∀ x o, ∃ p, admissible x p ∧ readout x p = o)
    (m : EmpiricalModel ctx O) :
    IsNoncontextual ctx m.weight ↔
      ∃ G : List (GlobalRun P admissible), G ≠ [] ∧
        adapt readout ctx (restrictTable ctx G) = .inr m := by
  constructor
  · rintro ⟨d, h0, h1, hd⟩
    choose pk hpk using realize
    let mk : (X → O) → GlobalRun P admissible := fun a =>
      ⟨fun x => pk x (a x), fun x => (hpk x (a x)).1⟩
    have hmk : ∀ a, (mk a).outcome readout = a := fun a =>
      funext fun x => (hpk x (a x)).2
    obtain ⟨l, hne, hl⟩ := exists_list_of_distribution d h0 h1
    refine ⟨l.map mk, by simpa using hne, ?_⟩
    rw [adapt_eq_inr_iff]
    refine ⟨fun i => by simpa [restrictTable] using hne, ?_⟩
    funext i s
    rw [hd i s, freqs, freq_restrictTable]
    refine sum_congr rfl fun a _ => ?_
    simp only [globalFreq, List.countP_map, List.length_map, Function.comp_def,
      hmk]
    exact (hl a).symm
  · rintro ⟨G, hG, h⟩
    obtain ⟨-, hw⟩ := (adapt_eq_inr_iff readout ctx _ m).1 h
    rw [hw]
    exact noncontextual_of_global_table readout ctx G hG

end Tables

/-! ## The CHSH cover, the Bell bound and the PR box -/

section Chsh

/-- Measurements of the CHSH scenario: `(false, x)` is Alice's setting `x` and
`(true, y)` is Bob's setting `y`. -/
abbrev ChshMeasurement := Bool × Bool

/-- The CHSH cover: context `(x, y)` holds Alice's setting `x` and Bob's
setting `y`. -/
def chshContext (xy : Bool × Bool) : Finset ChshMeasurement :=
  {(false, xy.1), (true, xy.2)}

/-- Alice's measurement in context `xy`. -/
def alice (xy : Bool × Bool) : chshContext xy :=
  ⟨(false, xy.1), by simp [chshContext]⟩

/-- Bob's measurement in context `xy`. -/
def bob (xy : Bool × Bool) : chshContext xy :=
  ⟨(true, xy.2), by simp [chshContext]⟩

/-- A section of a CHSH context is a pair of outcomes. -/
def sectionEquiv (xy : Bool × Bool) : (chshContext xy → Bool) ≃ Bool × Bool where
  toFun s := (s (alice xy), s (bob xy))
  invFun p m := if m.1.1 then p.2 else p.1
  left_inv s := by
    funext m
    obtain ⟨m, hm⟩ := m
    simp only [chshContext, mem_insert, mem_singleton] at hm
    rcases hm with rfl | rfl <;> rfl
  right_inv _ := rfl

@[simp] theorem sectionEquiv_symm_alice (xy : Bool × Bool) (p : Bool × Bool) :
    (sectionEquiv xy).symm p (alice xy) = p.1 :=
  rfl

@[simp] theorem sectionEquiv_symm_bob (xy : Bool × Bool) (p : Bool × Bool) :
    (sectionEquiv xy).symm p (bob xy) = p.2 :=
  rfl

theorem sum_sections (xy : Bool × Bool) (f : (chshContext xy → Bool) → ℚ) :
    ∑ s, f s = ∑ p : Bool × Bool, f ((sectionEquiv xy).symm p) :=
  (Equiv.sum_comp (sectionEquiv xy).symm f).symm

@[simp] theorem restrictGlobal_alice (xy : Bool × Bool)
    (g : ChshMeasurement → Bool) :
    restrictGlobal (chshContext xy) g (alice xy) = g (false, xy.1) :=
  rfl

@[simp] theorem restrictGlobal_bob (xy : Bool × Bool)
    (g : ChshMeasurement → Bool) :
    restrictGlobal (chshContext xy) g (bob xy) = g (true, xy.2) :=
  rfl

theorem restrictGlobal_eq_iff (xy : Bool × Bool) (g : ChshMeasurement → Bool)
    (s : chshContext xy → Bool) :
    restrictGlobal (chshContext xy) g = s ↔
      g (false, xy.1) = s (alice xy) ∧ g (true, xy.2) = s (bob xy) := by
  constructor
  · rintro rfl
    exact ⟨rfl, rfl⟩
  · rintro ⟨h1, h2⟩
    funext m
    obtain ⟨m, hm⟩ := m
    simp only [chshContext, mem_insert, mem_singleton] at hm
    rcases hm with rfl | rfl
    · exact h1
    · exact h2

/-- A global assignment is four outcomes `(a₀, a₁, b₀, b₁)`. -/
def globalEquiv : (ChshMeasurement → Bool) ≃ Bool × Bool × Bool × Bool where
  toFun g := (g (false, false), g (false, true), g (true, false), g (true, true))
  invFun q m :=
    match m with
    | (false, false) => q.1
    | (false, true) => q.2.1
    | (true, false) => q.2.2.1
    | (true, true) => q.2.2.2
  left_inv g := by
    funext m
    rcases m with ⟨_ | _, _ | _⟩ <;> rfl
  right_inv _ := rfl

/-- `+1` when Alice's and Bob's outcomes agree, `-1` otherwise. -/
def correlation (xy : Bool × Bool) (s : chshContext xy → Bool) : ℚ :=
  if s (alice xy) = s (bob xy) then 1 else -1

/-- The sign of context `xy` in `E₀₀ + E₀₁ + E₁₀ - E₁₁`. -/
def chshSign (xy : Bool × Bool) : ℚ :=
  if xy.1 && xy.2 then -1 else 1

/-- The CHSH value `E₀₀ + E₀₁ + E₁₀ - E₁₁` of weights on the CHSH cover, where
`E` is the expected correlation in a context. -/
def chsh (weight : ∀ xy, (chshContext xy → Bool) → ℚ) : ℚ :=
  ∑ xy : Bool × Bool, chshSign xy * ∑ s, weight xy s * correlation xy s

/-- One global assignment has CHSH value at most two. -/
theorem chsh_deterministic_le (g : ChshMeasurement → Bool) :
    ∑ xy : Bool × Bool,
        chshSign xy * correlation xy (restrictGlobal (chshContext xy) g) ≤ 2 := by
  simp only [Fintype.sum_prod_type, Fintype.sum_bool, chshSign, correlation,
    restrictGlobal_alice, restrictGlobal_bob]
  rcases Bool.eq_false_or_eq_true (g (false, false)) with h1 | h1 <;>
    rcases Bool.eq_false_or_eq_true (g (false, true)) with h2 | h2 <;>
    rcases Bool.eq_false_or_eq_true (g (true, false)) with h3 | h3 <;>
    rcases Bool.eq_false_or_eq_true (g (true, true)) with h4 | h4 <;>
    simp only [h1, h2, h3, h4] <;> norm_num

/-- The Bell bound: every noncontextual model on the CHSH cover has CHSH value
at most two. -/
theorem chsh_le_two_of_noncontextual
    {weight : ∀ xy, (chshContext xy → Bool) → ℚ}
    (h : IsNoncontextual chshContext weight) : chsh weight ≤ 2 := by
  obtain ⟨d, h0, h1, hd⟩ := h
  have hE : ∀ xy, ∑ s, weight xy s * correlation xy s =
      ∑ g, d g * correlation xy (restrictGlobal (chshContext xy) g) := by
    intro xy
    simp_rw [hd xy]
    exact sum_global_mul (chshContext xy) d (correlation xy)
  unfold chsh
  simp_rw [hE, mul_sum]
  rw [Finset.sum_comm]
  calc ∑ g, ∑ xy : Bool × Bool,
          chshSign xy * (d g * correlation xy (restrictGlobal (chshContext xy) g))
      = ∑ g, d g * ∑ xy : Bool × Bool,
          chshSign xy * correlation xy (restrictGlobal (chshContext xy) g) := by
        refine sum_congr rfl fun g _ => ?_
        rw [mul_sum]
        exact sum_congr rfl fun xy _ => by ring
    _ ≤ ∑ g, d g * 2 :=
        sum_le_sum fun g _ =>
          mul_le_mul_of_nonneg_left (chsh_deterministic_le g) (h0 g)
    _ = 2 := by rw [← sum_mul, h1, one_mul]

/-- The PR box: in contexts `(0,0)`, `(0,1)` and `(1,0)` the two outcomes agree,
in `(1,1)` they differ, and each allowed pair has probability one half. -/
def prWeight (xy : Bool × Bool) (s : chshContext xy → Bool) : ℚ :=
  if xor (s (alice xy)) (s (bob xy)) = (xy.1 && xy.2) then 1 / 2 else 0

/-- The signed weights `½(δ₀₀₀₀ - δ₀₀₁₀ + δ₀₁₁₀ + δ₁₀₁₁)` on the assignments
`(a₀, a₁, b₀, b₁)`. -/
def prSigned4 : Bool × Bool × Bool × Bool → ℚ
  | (false, false, false, false) => 1 / 2
  | (false, false, true, false) => -1 / 2
  | (false, true, true, false) => 1 / 2
  | (true, false, true, true) => 1 / 2
  | _ => 0

/-- The signed global section of the PR box. -/
def prSigned (g : ChshMeasurement → Bool) : ℚ :=
  prSigned4 (globalEquiv g)

theorem prWeight_nonneg (xy : Bool × Bool) (s : chshContext xy → Bool) :
    0 ≤ prWeight xy s := by
  unfold prWeight
  split_ifs <;> norm_num

theorem sum_prWeight (xy : Bool × Bool) : ∑ s, prWeight xy s = 1 := by
  rw [sum_sections]
  obtain ⟨x, y⟩ := xy
  cases x <;> cases y <;>
    norm_num [prWeight, Fintype.sum_prod_type]

theorem prWeight_eq_global (xy : Bool × Bool) (s : chshContext xy → Bool) :
    prWeight xy s =
      ∑ g ∈ univ.filter (fun g => restrictGlobal (chshContext xy) g = s),
        prSigned g := by
  obtain ⟨⟨a, b⟩, rfl⟩ := (sectionEquiv xy).symm.surjective s
  rw [Finset.sum_filter, ← Equiv.sum_comp globalEquiv.symm]
  simp only [restrictGlobal_eq_iff, prSigned, Equiv.apply_symm_apply,
    sectionEquiv_symm_alice, sectionEquiv_symm_bob, prWeight]
  obtain ⟨x, y⟩ := xy
  cases x <;> cases y <;> cases a <;> cases b <;>
    simp [Fintype.sum_prod_type, prSigned4, globalEquiv] <;> norm_num

theorem sum_prSigned : ∑ g, prSigned g = 1 := by
  rw [← Equiv.sum_comp globalEquiv.symm]
  simp [prSigned, prSigned4, Fintype.sum_prod_type]
  norm_num

/-- The PR box as an empirical model on the CHSH cover. -/
def prBox : EmpiricalModel chshContext Bool where
  weight := prWeight
  nonneg := prWeight_nonneg
  normalized := sum_prWeight
  compatible := by
    have h : prWeight = fun xy s =>
        ∑ g ∈ univ.filter (fun g => restrictGlobal (chshContext xy) g = s),
          prSigned g :=
      funext fun xy => funext fun s => prWeight_eq_global xy s
    rw [h]
    exact compatible_of_global chshContext prSigned

/-- No global assignment is allowed in all four contexts of the PR box. -/
theorem prBox_stronglyContextual :
    IsStronglyContextual chshContext prWeight := by
  rintro ⟨g, hg⟩
  have h00 := hg (false, false)
  have h01 := hg (false, true)
  have h10 := hg (true, false)
  have h11 := hg (true, true)
  simp only [prWeight, restrictGlobal_alice, restrictGlobal_bob] at h00 h01 h10 h11
  revert h00 h01 h10 h11
  rcases Bool.eq_false_or_eq_true (g (false, false)) with h1 | h1 <;>
    rcases Bool.eq_false_or_eq_true (g (false, true)) with h2 | h2 <;>
    rcases Bool.eq_false_or_eq_true (g (true, false)) with h3 | h3 <;>
    rcases Bool.eq_false_or_eq_true (g (true, true)) with h4 | h4 <;>
    simp only [h1, h2, h3, h4] <;> norm_num

theorem chsh_prBox : chsh prWeight = 4 := by
  unfold chsh
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  simp only [sum_sections, Fintype.sum_prod_type, Fintype.sum_bool, prWeight,
    correlation, chshSign, sectionEquiv_symm_alice, sectionEquiv_symm_bob]
  norm_num

/-- The PR box has a signed global section with a negative weight, and no
nonnegative one. -/
theorem prBox_signed_not_nonneg :
    IsGlobalSection chshContext prWeight prSigned ∧
      prSigned (globalEquiv.symm (false, false, true, false)) < 0 ∧
      ¬ IsNoncontextual chshContext prWeight := by
  refine ⟨⟨sum_prSigned, prWeight_eq_global⟩, ?_,
    not_noncontextual_of_strongly prBox_stronglyContextual⟩
  norm_num [prSigned, prSigned4]

section ChshTables

variable {P : Type z} {admissible : ChshMeasurement → P → Prop}
  (readout : ChshMeasurement → P → Bool)

/-- Every table of global runs obeys the Bell bound. -/
theorem chsh_le_two_of_global_table (G : List (GlobalRun P admissible))
    (hG : G ≠ []) :
    chsh (freqs readout chshContext (restrictTable chshContext G)) ≤ 2 :=
  chsh_le_two_of_noncontextual
    (noncontextual_of_global_table readout chshContext G hG)

/-- If packets can report every outcome, some table has the PR box as its
image. Its CHSH value is four, it is strongly contextual, and no table of
global runs has the same image. -/
theorem pr_box_packet_table
    (realize : ∀ x o, ∃ p, admissible x p ∧ readout x p = o) :
    ∃ T : ∀ xy, List (Run P admissible (chshContext xy)),
      adapt readout chshContext T = .inr prBox ∧
      chsh (freqs readout chshContext T) = 4 ∧
      IsStronglyContextual chshContext (freqs readout chshContext T) ∧
      ¬ ∃ G : List (GlobalRun P admissible), G ≠ [] ∧
        adapt readout chshContext (restrictTable chshContext G) = .inr prBox := by
  obtain ⟨T, hT⟩ := exists_table readout chshContext realize prBox
  obtain ⟨-, hw⟩ := (adapt_eq_inr_iff readout chshContext T prBox).1 hT
  have hfreq : freqs readout chshContext T = prWeight := hw.symm
  refine ⟨T, hT, by rw [hfreq, chsh_prBox], by
    rw [hfreq]; exact prBox_stronglyContextual, ?_⟩
  rintro ⟨G, hG, hGT⟩
  have hnc := (noncontextual_iff_global_table readout chshContext realize
    prBox).2 ⟨G, hG, hGT⟩
  exact not_noncontextual_of_strongly prBox_stronglyContextual hnc

end ChshTables

end Chsh

end WitnessedDifference.Empirical
