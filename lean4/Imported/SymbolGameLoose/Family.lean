/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/Family.lean
   Original sha256: 74f9c49439b847603714a678f498d76494d7438e5fa6f47fdc23021a5e59a3f3 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.Family
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.SymbolGameLoose.Expressivity

/-!
# Inc 4 Q1-B: `expressivity_norm_le_grammar_ceiling`

States and proves
$\|o_n\| \le S(n)$
for the declared `ℓ¹` norm on a chosen finite `C¹_n` representative. The norm
is not claimed to descend to `Q¹_n` under a general gauge shift.

## The grammar ceiling `S(n)`

The packet pins the recurrence

```
S(0) = 0
S(1) = 0
S(n) = n * (n - 1)   for n ≥ 2
```

This is the worst-case discrepancy mass on a level-`n` cycle nerve: up to `n`
overlaps, each carrying up to `n - 1` units of integer discrepancy.

## The bound

`expressivity_norm_le_grammar_ceiling (n : Nat) (h : List Int)`
`(hlen : h.length ≤ n) (hcap : ∀ x ∈ h, x.natAbs ≤ n - 1) :`
`expressivityNorm h ≤ grammarCeiling n`

The hypotheses pin the level: a level-`n` problem has at most `n` overlaps
(`hlen`) and each overlap discrepancy is at most `n - 1` in absolute value
(`hcap`). These are exactly the constraints the Rust family driver enforces
when constructing the saturating family at level `n`.

The proof is by induction on the list, with the key step
`|x| + ‖tail‖ ≤ (n-1) + (length-1)·(n-1) = length·(n-1) ≤ n·(n-1)`.

## Firewall

Authority is not minted here. The `#print axioms` audit (S8) checks the
theorem rests only on standard kernel axioms within the
`SemiringTransportAxiomAudit` set.
-/

namespace OmegaCosmology.SymbolGame

/-- The grammar ceiling `S(n)` — the worst-case norm at level `n`. -/
def grammarCeiling (n : Nat) : Nat :=
  if n < 2 then 0 else n * (n - 1)

theorem grammarCeiling_zero : grammarCeiling 0 = 0 := rfl
theorem grammarCeiling_one  : grammarCeiling 1 = 0 := rfl
theorem grammarCeiling_two  : grammarCeiling 2 = 2 := rfl
theorem grammarCeiling_three : grammarCeiling 3 = 6 := rfl
theorem grammarCeiling_four  : grammarCeiling 4 = 12 := rfl
theorem grammarCeiling_eight : grammarCeiling 8 = 56 := rfl

/-- Length-times-cap bound: the norm of a list is at most `length * cap` when
    every entry is capped by `cap`. The induction step inflates the head's
    `natAbs ≤ cap` bound by `length` to absorb the tail. -/
theorem expressivityNorm_le_length_mul_cap
    (cap : Nat) :
    ∀ (h : List Int), (∀ x ∈ h, x.natAbs ≤ cap) →
      expressivityNorm h ≤ h.length * cap
  | [], _ => by
      simp [expressivityNorm]
  | x :: xs, hcap => by
      have hx : x.natAbs ≤ cap := hcap x (by simp)
      have htail : ∀ y ∈ xs, y.natAbs ≤ cap := fun y hy =>
        hcap y (by simp [hy])
      have ih := expressivityNorm_le_length_mul_cap cap xs htail
      have step :
          expressivityNorm (x :: xs) = x.natAbs + expressivityNorm xs := rfl
      have h_len : (x :: xs).length = xs.length + 1 := rfl
      have h_sum :
          cap + xs.length * cap = (xs.length + 1) * cap := by
        rw [Nat.add_comm, Nat.add_mul, Nat.one_mul]
      calc
        expressivityNorm (x :: xs)
            = x.natAbs + expressivityNorm xs := step
        _ ≤ cap + xs.length * cap := Nat.add_le_add hx ih
        _ = (xs.length + 1) * cap := h_sum
        _ = (x :: xs).length * cap := by rw [h_len]

/--
**Q1-B — the grammar-ceiling bound.**

Under the declared expressivity norm `‖·‖_n` and the level-`n` constraints
(at most `n` overlaps, each with `|discrepancy| ≤ n - 1`), the norm of the
defect cochain is bounded by the grammar ceiling `S(n) = n * (n - 1)`.

This is the packet's primary residual `Q¹-B`, proved here over the explicit
finite carrier `List Int`. The bound is stated on a chosen canonical
representative: the proof depends only on the list-level integer cap
(`|x| ≤ n - 1`) and the length bound (`≤ n`). It does NOT assert that the norm
descends to `Q¹_n`; the `ℓ¹` mass is invariant only under the kernel of `d⁰`
(the constant-potential action of S2), not under a general `δ ∈ im d⁰`. -/
theorem expressivity_norm_le_grammar_ceiling
    (n : Nat) (h : List Int)
    (hlen : h.length ≤ n)
    (hcap : ∀ x ∈ h, x.natAbs ≤ n - 1) :
    expressivityNorm h ≤ grammarCeiling n := by
  by_cases hn : n < 2
  · -- n ∈ {0, 1}: cap is 0 (n - 1 = 0 in Nat for n ≤ 1) so every entry vanishes
    -- and the ceiling is 0.
    have hcap_zero : ∀ x ∈ h, x.natAbs ≤ 0 := by
      intro x hx
      have := hcap x hx
      have hle : n - 1 ≤ 0 := by omega
      exact Nat.le_trans this hle
    have bound := expressivityNorm_le_length_mul_cap 0 h hcap_zero
    have h_mul_zero : h.length * 0 = 0 := Nat.mul_zero _
    have norm_zero : expressivityNorm h ≤ 0 := by
      rw [h_mul_zero] at bound
      exact bound
    have ceil_zero : grammarCeiling n = 0 := by
      unfold grammarCeiling
      simp [hn]
    omega
  · -- n ≥ 2: length * (n - 1) ≤ n * (n - 1) and norm ≤ length * (n - 1).
    have step := expressivityNorm_le_length_mul_cap (n - 1) h hcap
    have len_bound : h.length * (n - 1) ≤ n * (n - 1) :=
      Nat.mul_le_mul_right _ hlen
    have ceil_def : grammarCeiling n = n * (n - 1) := by
      unfold grammarCeiling
      simp [hn]
    have hcomp : expressivityNorm h ≤ n * (n - 1) := Nat.le_trans step len_bound
    rw [ceil_def]
    exact hcomp

end OmegaCosmology.SymbolGame
