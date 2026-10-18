import «superposition_cochain»

/-!
# H¹-rank of the superposition complex — `dim H¹ = b₁`, `card H¹ = pᵇ¹` (entanglement resource)

Slice 3: the linear-algebra layer over a field. The slice-2 identity `ker hol = im d₀`
(`holonomy_zero_iff_gauge`) does the heavy lifting — for the single `n`-cycle it gives
`dim H¹ = E − V + 1 = 1` (`finrank_H1_eq_one`) by rank-nullity, with **no** general graph theory.
Over `F_p` the resource count is then `card H¹ = p^(dim H¹) = p` (`card_H1_cycle`), via the general
`resource_card : card W = p^(rank W)`.

The single loop is `b₁ = 1`. The general graph — arbitrary `b₁ =` number of independent loops `=`
the entanglement rank, with `card H¹ = pᵇ¹` — is the *same* computation once `rank d₀ = V − C`
(the connected-components lemma) is in hand; that is the remaining generalization. This ties the
resource count directly to `holonomy_resource_injective` (`2^rank` distinct configs at fixed L1).

No authority minted (GTOC-5); finite, carrier-declared.
-/

namespace QM.SuperpositionH1Rank

open QM.SuperpositionCochain

variable {n : ℕ} [NeZero n] {𝕜 : Type*} [Field 𝕜]

/-- The coboundary `d₀` as a `𝕜`-linear map. -/
def d0L : (ZMod n → 𝕜) →ₗ[𝕜] (ZMod n → 𝕜) where
  toFun := d0
  map_add' φ ψ := by funext x; simp only [d0, Pi.add_apply]; ring
  map_smul' c φ := by
    funext x; simp only [d0, Pi.smul_apply, RingHom.id_apply, smul_eq_mul]; ring

/-- The holonomy `hol` as a `𝕜`-linear map. -/
def holL : (ZMod n → 𝕜) →ₗ[𝕜] 𝕜 where
  toFun := hol
  map_add' a b := by simp only [hol, Pi.add_apply]; exact Finset.sum_add_distrib
  map_smul' c a := by
    simp only [hol, Pi.smul_apply, RingHom.id_apply, smul_eq_mul]
    exact (Finset.mul_sum _ _ _).symm

theorem holL_surjective : Function.Surjective (holL (n := n) (𝕜 := 𝕜)) := by
  intro c
  obtain ⟨a, ha⟩ := hol_surjective (n := n) (A := 𝕜) c
  exact ⟨a, ha⟩

/-- **`im d₀ = ker hol`** as submodules — the linear form of the slice-2 classification. -/
theorem range_d0L_eq_ker_holL :
    LinearMap.range (d0L (n := n) (𝕜 := 𝕜)) = LinearMap.ker (holL (n := n) (𝕜 := 𝕜)) := by
  ext a
  rw [LinearMap.mem_range, LinearMap.mem_ker]
  exact (holonomy_zero_iff_gauge a).symm

/-- **`dim H¹ = 1`** for the single `n`-cycle (`= E − V + 1 = b₁`), by rank-nullity from
`ker hol = im d₀` and surjectivity of `hol`. -/
theorem finrank_H1_eq_one :
    Module.finrank 𝕜 ((ZMod n → 𝕜) ⧸ LinearMap.range (d0L (n := n) (𝕜 := 𝕜))) = 1 := by
  have hC : Module.finrank 𝕜 (ZMod n → 𝕜) = n := by rw [Module.finrank_pi, ZMod.card]
  have hrange_hol : Module.finrank 𝕜 (LinearMap.range (holL (n := n) (𝕜 := 𝕜))) = 1 := by
    rw [LinearMap.range_eq_top.2 holL_surjective, finrank_top, Module.finrank_self]
  have hrn := LinearMap.finrank_range_add_finrank_ker (holL (n := n) (𝕜 := 𝕜))
  rw [hrange_hol, hC] at hrn
  have hrd0 : Module.finrank 𝕜 (LinearMap.range (d0L (n := n) (𝕜 := 𝕜))) = n - 1 := by
    rw [range_d0L_eq_ker_holL]; omega
  have hq := Submodule.finrank_quotient_add_finrank (LinearMap.range (d0L (n := n) (𝕜 := 𝕜)))
  rw [hC, hrd0] at hq
  have hn : 1 ≤ n := Nat.one_le_iff_ne_zero.2 (NeZero.ne n)
  omega

/-- **Resource = `p^rank`.** Any finite `F_p`-space has `card = p^(dim)`. The `H¹` instance below
makes this the interference/entanglement resource count. -/
theorem resource_card {p : ℕ} [Fact p.Prime] (W : Type*) [AddCommGroup W] [Module (ZMod p) W]
    [Fintype W] [FiniteDimensional (ZMod p) W] :
    Fintype.card W = p ^ Module.finrank (ZMod p) W := by
  rw [Module.card_eq_pow_finrank (K := ZMod p), ZMod.card]

/-- **`card H¹ = p`** for the single `n`-cycle over `F_p` (`= p^{b₁}`, `b₁ = 1`) — the resource
count of one independent loop. -/
theorem card_H1_cycle {p : ℕ} [Fact p.Prime] :
    Fintype.card ((ZMod n → ZMod p) ⧸ LinearMap.range (d0L (n := n) (𝕜 := ZMod p))) = p := by
  haveI : Finite ((ZMod n → ZMod p) ⧸ LinearMap.range (d0L (n := n) (𝕜 := ZMod p))) :=
    Finite.of_surjective _ (Submodule.Quotient.mk_surjective _)
  haveI : Fintype ((ZMod n → ZMod p) ⧸ LinearMap.range (d0L (n := n) (𝕜 := ZMod p))) :=
    Fintype.ofFinite _
  rw [resource_card (p := p), finrank_H1_eq_one, pow_one]

#print axioms range_d0L_eq_ker_holL
#print axioms finrank_H1_eq_one
#print axioms card_H1_cycle

end QM.SuperpositionH1Rank
