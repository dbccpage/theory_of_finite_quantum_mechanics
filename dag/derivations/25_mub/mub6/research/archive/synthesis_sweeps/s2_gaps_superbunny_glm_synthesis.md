# MUB(6) Subgraph S2 Gap Evaluation Synthesis

**Date:** 2026-09-29 03:23:56 UTC  
**Epistemic Firewall:** `stated region only; mints no authority`  
**Queried Models:** Super Bunny Alpha (`stealth/space-bunny-alpha`), GLM 5.3 (`z-ai/glm-5.3`)  

> [!WARNING]
> **EPISTEMIC AUDIT NOTICE & DEFECT REMEDIATION:**
> All 10 model calls in this evaluation run returned `finish_reason: "length"` at `max_tokens=8192` with `message.content == null`.
> The models exhausted their output budgets entirely within their internal reasoning scratchpads before generating any completion response.
> These truncated reasoning traces are untrusted proposals (`AuthorityEffect: None`) and do NOT constitute completed evaluations or formal proofs.
> They support no registry status change. No model evaluated or discharged any gap.

---

## Canonical Gap Status Reference

Authoritative gap statuses, dependency bounds, and open residuals are maintained in [mub6_gap_registry.json](mub6_gap_registry.json):

- **G1 (Full Moduli Variety Classification)**: `OPEN` (Priority 1). Subgaps R6 (claimed unverified, artifact missing) and R7 (ENC-1147 real spectrum exhaustion on $I_{55}$) open.
- **G2 (Candidate Representation Bridge)**: `DISCHARGED_CONDITIONAL` on G1.
- **G3 (Analytic Parameter Variation Enclosures)**: `PARTIAL`. Linear interpolation bounds endpoint margins only; does not bound parameter variation across CHM moduli.
- **G4 (Genuine Simplicial 1-Cochains)**: `DISCHARGED_CONDITIONAL` on G1. $\Phi_1 \ge \Gamma = 12133/5000 > 0$ is a fixed rational circulation over the declared 5-chart nerve, not derived from continuous chart geometry.
- **G5 (Projector-Moment Positivity)**: `PARTIAL` (Q5/Q6 generic operator gap open).

---

## Gap G1: Full Moduli Classification & Subgap R7 (ENC-1147) Exhaustion

### Model: GLM 5.3

- **Status:** TRUNCATED (finish_reason: `length`, content: null)
- **Latency:** 37.52s | **Tokens:** 8796
- **Notice:** Call exhausted token limit during internal reasoning; no completion content was emitted.

<details><summary>Truncated Reasoning Trace (26909 chars)</summary>

```
The user is asking me to provide a rigorous algebraic geometry / real algebraic geometry formulation for discharging "Subgap R7" in a MUB(6) program. This is a highly technical question about:

1. The variety of 6×6 complex Hadamard matrices (unitary matrices with unimodular entries — i.e., complex Hadamard matrices that are also unitary, which is automatic for Hadamard matrices scaled by 1/√6).

2. The ideal I_55 of 55 polynomials in 50 real variables defining 6×6 unitary matrices with unimodular entries.

3. Using Positivstellensatz certificates (Stengle, Putinar) to certify that real solutions must lie in the closure of 5 known families: F(x,y) (Fourier family / Tao's family?), B_6(θ) (dephased B_6 family — the "B_6" family from Karlsson, i.e., a one-parameter family), K_6^(3) (Karlsson's 3-parameter family?), S_6 (Sylvester?), H_6 (probably the "H_6" family — maybe the Haagerup-like or the "H_6" from some classification).

Let me think about the actual mathematics here, because I need to be careful and honest.

**Background on complex Hadamard matrices of order 6:**

The classification of 6×6 complex Hadamard matrices is a famous open problem. Known facts:
- The set H(6) of complex Hadamard matrices of order 6 is a real algebraic variety (defined by orthogonality of rows: |entries| = 1 and rows pairwise orthogonal).
- After dephasing (normalizing first row and column to 1), the dephased variety H_6^dephased is cut out by polynomial equations in the (6-1)² = 25 complex entries = 50 real variables.
- The number of equations: orthogonality of rows i,j (i<j, 5·4/2 = 10 pairs) gives 2 real equations each (real and imaginary parts of the Hermitian inner product), so 20 equations; plus unimodularity of the 25 free entries gives 25 equations (|z|² = 1). Total 45. Hmm, but the problem says 55 polynomials in 50 real variables. Let me recount: unitary 6×6 with unimodular entries. Full matrix: 36 entries, 72 real variables. Unimodularity: 36 equations |z_ij|² = 1. Unitarity: U*U = I gives 36 equations (21 real: 6 real diagonal + 15 complex off-diagonal = 6 + 30 = 36 real equations). Total 72 equations in 72 variables. After dephasing (fixing first row and column to 1), we remove 11 entries (11 complex = 22 real variables), leaving 25 complex = 50 real variables. The equations: unimodularity of 25 free entries (25 equations), orthogonality of rows: 10 pairs × 2 = 20 equations, orthogonality of columns: 10 pairs × 2 = 20 equations. But wait — for Hadamard matrices, if all entries are unimodular and rows are orthogonal, columns are automatically orthogonal (since a square matrix with unimodular entries and orthogonal rows is unitary up to scaling, hence columns are orthogonal too). Actually: if H has unimodular entries and HH* = 6I, then H is invertible, H* = 6H⁻¹, and H*H = 6I follows. So column orthogonality is implied. So the dephased variety is cut out by 25 + 20 = 45 equations in 50 real variables. Hmm, the problem says 55. Maybe they include both row and column orthogonality redundantly: 25 + 20 + 20 = 65? No. Or maybe they don't dephase fully. Or maybe 55 = 25 (unimodular) + 30 (row orthogonality for 10 pairs... no, 10 pairs × 2 = 20). Hmm, 55 = 25 + 30? 30 = 15 pairs × 2? If they consider all pairs (i,j) with i≠j: 30 ordered pairs × 2 = 60. Hmm.

Alternatively: 55 could come from: 36 unimodularity equations minus... no. Let me not worry too much about the exact count; the problem statement says "55 polynomials in 50 real variables defining 6×6 unitary matrices with unimodular entries." I should accept this as given (it's their encoding) but I can note the standard count. Actually, maybe: 50 real variables = 25 complex dephased entries. Equations: |z|² = 1 for 25 entries (25 equations), row orthogonality: 10 pairs, each Hermitian inner product = 0 gives 2 real equations (20), column orthogonality: 10 pairs × 2 = 20. Total 65. If we drop column orthogonality (redundant): 45. Hmm, 55 = 45 + 10? Maybe they add 10 more for something. Or maybe they don't dephase the first row: 30 free complex entries = 60 real variables... no, they say 50.

Alternatively, maybe they parametrize differently. I shouldn't get bogged down; I'll accept I_55 ⊂ ℝ[x₁,...,x₅₀] as given, and note that the standard dephased encoding yields 45 essential equations with 10 possibly redundant (e.g., including both row and column orthogonality partially, or including normalization). Actually, one plausible count: dephased 6×6, free entries 25 complex = 50 real. Equations: unimodularity 25; row orthogonality 10 pairs × 2 = 20; that's 45. Add 10 equations for... hmm, maybe they include the "first column" or some extra constraints. Or maybe they use a different parametrization with 55 = 25 + 20 + 10 where 10 are the imaginary parts of something. I'll just note that the exact count depends on encoding and that redundancy is harmless for the Nullstellensatz/Satz arguments (adding redundant generators doesn't change the variety or the real radical).

**Known classification status of 6×6 complex Hadamards:**

This is genuinely open. Known families:
- F(6) = Fourier family F₆ (all entries 6th roots of unity), isolated? No — F₆ is part of a positive-dimensional family? Actually, the Fourier matrix F₆ is known to belong to a one-parameter family? Hmm. Let me recall: For n=6, the known dephased families include:
  - The "generic" family: it's known that the set of 6×6 complex Hadamard matrices contains a 4-parameter family (after dephasing, the "manifold" dimension is 4). Actually, the known result: H(6) contains a 4-dimensional family (the "Fourier-type" family F(x,y)? Hmm).
  
Let me recall the literature: The classification of complex Hadamard matrices of order 6 is open. Known:
- F₆: the Fourier matrix (entries ω^jk, ω = e^{2πi/6}).
- B₆(θ): a one-parameter family containing... hmm, actually I recall "B_6^{(0)}" and "B_6^{(1)}" from Karlsson? There's a family found by Beauchamp? Let me think.

Known 6×6 families (from the catalog of Szöllősi, from the paper "Complex Hadamard matrices of order 6" by various authors):
- The Fourier family F₆.
- The family S₆ (Sylvester-type? Actually S₆ might denote the "S_6" family from Szöllősi's catalog — a 2-parameter family?).
- K₆ (Karlsson's family, 3-parameter? "K_6^{(3)}" suggests a 3-parameter family).
- The "Dita" family? Dita's construction gives a 2-parameter family for n = (a)(b)? Dita's construction: for n = ab, gives families. For 6 = 2·3, Dita gives a 2-parameter family? Hmm.
- H₆: maybe the "Haagerup" — no, Haagerup is order 7? Haagerup's matrix is 7×7? No wait, Haagerup found a 5×5? Hmm: Haagerup's famous matrix is order 5? No — Haagerup's matrix is the 5×5? Let me recall: Haagerup 1997 constructed an infinite family of complex Hadamard matrices of "Circulant" type? The famous Haagerup matrix is 5×5? Hmm, actually I recall Haagerup's matrix is of order 5? No... The famous sporadic complex Hadamard matrices: order 5 (Haagerup? no, order 5 has a 1-parameter family? hmm), order 6 (several sporadic), order 7 (Petracca–? no). 

Let me recall properly: Complex Hadamard classification status:
- n ≤ 5: classified (n=5 has the Fourier F₅ and a 1-parameter family? Actually n=5: F₅ and the "Haagerup"? no). Hmm: n=1,2,3,4 classified; n=4 has a 1-parameter family (F₄(a)); n=5: classified (F₅ and a 1-parameter family? I think n=5 is classified: F₅ plus a one-parameter family? Actually I recall n=5 classification: F₅ and the family? Hmm, I believe n=5 is classified with F₅ and a 1-parameter family "F₅(a)"? No wait — I think for n=5, the dephased set consists of F₅ and a 1-parameter family? Let me not worry.)
- n=6: open. Known: F₆, the 2-parameter family? Actually the known components of H(6):
  - A 4-parameter family? Hmm. Let me recall the dimension: The "manifold" of dephased 6×6 complex Hadamards — the known families have up to 4 parameters? I recall that the set of 6×6 complex Hadamard matrices, after dephasing, contains a 4-dimensional family? Hmm, actually I recall the "generic" 6×6 complex Hadamard matrices form a 4-parameter family? Let me think: the "Fourier" F₆ has deformation space of dimension... The tangent space dimension at F₆ (dephased) is 4? I recall that at F₆, the tangent space has dimension 4, and there's a known 4-parameter family through F₆? Hmm, but I also recall that the known families of 6×6 are: F₆ (isolated? no), B₆ (1-param), S₆ (2-param?), K₆ (3-param), and the "generic" family? 

From Szöllősi's catalog (hadamard matrices up to order 6? the "catalog" goes to order 6? I think the online catalog by Szöllősi lists all known matrices up to order 6? Hmm, actually the catalog lists up to order 6? I recall the catalog covers n ≤ 6? No — I think it covers n ≤ 6? Hmm, I believe the catalog covers up to order 6? Let me just recall the known 6×6 families from the literature (e.g., the paper "Complex Hadamard matrices and the construction of mutually unbiased bases" or Karlsson's thesis):

Known 6×6 dephased complex Hadamard families:
1. F₆ — the Fourier matrix, which is isolated? No — F₆ is not isolated; it's contained in families.
2. F(x, y)? Hmm — maybe "F(x,y)" denotes a 2-parameter family? Hmm, but the problem says "F(x, y)" as one of the 5 literature families. Hmm, maybe F(x,y) is the "Fourier-type" 2-parameter family? Hmm.
3. B₆(θ) — 1-parameter family (this is likely the family from Karlsson's paper "Hadamard matrices from complex Hadamard matrices"? or the "B_6" family in the catalog: B₆^{(0)}? Hmm).
4. K₆^{(3)} — Karlsson's 3-parameter family? Hmm, I recall Karlsson constructed a 3-parameter family of 6×6 complex Hadamards? Actually I recall "K_6^{(3)}" might be from the paper by Karlsson? Hmm.
5. S₆ — 2-parameter family? "S_6" might be from Szöllősi? Hmm.
6. H₆ — hmm.

Actually, I now recall more concretely: In the study of MUBs of size 6 (e.g., work by Brierley–Weigert, and the "Hadamard matrices and MUB(6)" literature), the known 6×6 complex Hadamard matrices include:
- The Fourier family F₆ (with the "Fourier" being part of a family? F₆ itself is isolated within the "circulant" class but sits inside bigger families).
- The "Dita" family D(6)? Dita's construction for 6 = 2×3 gives a 2-parameter family? Hmm, Dita's construction: H = [A B; B* A*]? For n = ab with a,b, gives families with (a-1)(b-1)? parameters? For 6 = 2·3: (2-1)(3-1) = 2 parameters? So Dita's family for n=6 is 2-parameter? Hmm.
- The "B_6" family: I recall from the paper by Karlsson? Hmm, actually "B_6" might refer to the family found by "Beauchamp"? Hmm.

OK here's the thing: I don't need to precisely identify the 5 families; the problem gives them: F(x,y), B₆(θ), K₆^{(3)}, S₆, H₆. These look like: F(x,y) — 2-parameter "Fourier-type" family (maybe the family containing F₆, parametrized by x,y on the torus); B₆(θ) — 1-parameter family (the "B_6" family, maybe from the catalog, containing the "B_6^{(0)}" matrix?); K₆^{(3)} — 3-parameter family (Karlsson's?); S₆ — maybe the "Sylvester"/"Szöllősi" 2-parameter? Hmm, or S₆ could be a single matrix? And H₆ — maybe a single sporadic matrix? Hmm.

Actually, I recall now: the known 6×6 complex Hadamard matrices in the catalog include: F₆, S₆ (a "Sylvester-like"?), K₆ (Karlsson), B₆ (from "Björck"? no, Björck is for cyclic n=7...). Hmm, "B_6" might be from the paper of "Björck"? No. Let me think about "B_6(θ)": There's a known 1-parameter family of 6×6 complex Hadamards sometimes denoted B₆(θ)? Hmm, hmm. There's the family "B_6" in Szöllősi's catalog? I don't remember exactly.

Anyway — the key point: the problem is asking me to formulate (not solve!) the algebraic geometry approach to prove that the real variety of I_55 is exactly the union of the closures of these 5 families. This is the "classification" of 6×6 complex Hadamards, which is a genuinely open problem in mathematics. So I must be very careful: I cannot claim to discharge it; I can only provide the formulation, the certificate structure, the bounds, and the next computational test. The constitutional rules require me to:
- Never claim MUB(6)=3 or ≤3.
- Avoid hype verbs.
- For each gap: what it supports, what it does not support, narrowest defensible claim, next test.
- Provide precise algebraic, geometric, and formal Lean 4 insights.

So my answer should be a rigorous mathematical formulation document. Let me now actually do the mathematics carefully.

**Setup: the real algebraic variety of dephased 6×6 complex Hadamard matrices.**

Let me set up notation. Dephased matrix: first row and column all 1. Free entries: z_ij for 2 ≤ i,j ≤ 6, i.e., 25 complex unknowns. Write z_ij = x_ij + i y_ij, 50 real unknowns.

Equations:
(a) Unimodularity: x_ij² + y_ij² = 1 for each of 25 entries. (25 equations)
(b) Row orthogonality: for 1 ≤ i < j ≤ 6, Σ_k conj(z_ik) z_jk = 0. With first row = 1s: for pairs (1,j): Σ_k z_jk = 0 (complex) → 2 real equations each, 5 pairs → 10 equations. For pairs (i,j), 2 ≤ i < j ≤ 6: Σ_k conj(z_ik) z_jk = 0 → 2 real each, 10 pairs → 20 equations. Total row orthogonality: 30 real equations.
(c) Column orthogonality: similarly 30 real equations, but redundant given (a)+(b) (since a square unimodular-entry matrix with orthogonal rows is unitary up to scale).

Total essential: 25 + 30 = 55. Ah — there we go! 55 = 25 (unimodularity) + 30 (row orthogonality: 15 pairs × 2 real equations). Yes! 15 pairs of rows (6 choose 2 = 15), each orthogonality is one complex equation = 2 real equations → 30. Plus 25 unimodularity = 55. And column orthogonality is a consequence. So I_55 = ⟨ x_ij² + y_ij² − 1 (25), Re Σ_k z̄_ik z_jk (15), Im Σ_k z̄_ik z_jk (15) ⟩ ⊂ ℝ[x₂₂, y₂₂, ..., x₆₆, y₆₆] (50 variables). 

So the variety X = V(I_55) ⊂ ℝ⁵⁰ (or ℂ⁵⁰) is the dephased complex Hadamard variety H(6)₀. Known: it's a compact real variety (subset of the torus T²⁵ ⊂ ℝ⁵⁰), of real dimension 4 (the known families are 4-dimensional? hmm — actually what's the expected dimension?).

Dimension count: The full unitary group U(6) has real dimension 36. The set of unitary matrices with unimodular entries: cut out by 36 conditions |u_ij| = 1 inside U(6) (36-dim), so expected dimension 0, but actual: the Hadamard set H(6) = U(6) ∩ (torus) — hmm, the set of complex Hadamard matrices of order 6 up to left unitary multiplication: H(6)/U(6)? The standard count: the "manifold" of complex Hadamard matrices of order n, after quotienting by U(n) and dephasing, has expected dimension (n−1)² − (number of independent constraints). For n=6: dephased free entries 25 complex = 50 real; constraints: 25 unimodularity + 30 row orthogonality = 55; but they're not independent; the actual dimension of the dephased variety is known to be 4 at generic points? Hmm, I recall that the 6×6 complex Hadamard "manifold" has dimension 4 (i.e., there's a 4-parameter family of dephased 6×6 complex Hadamards — the "generic" family). Hmm, is that right? Let me think: known result (Tao? no). I recall that for n=6, the dephased Hadamard variety has a component of dimension 4? Hmm, hmm.

Actually, I recall: "It is known that the set of equivalence classes of 6×6 complex Hadamard matrices contains a 4-parameter family" — hmm, I'm not 100% sure. Let me think about the "Fourier" F₆: its deformation theory. There's a classical result that F₆ admits a 4-dimensional deformation? Hmm. Alternatively, the known families: F(x,y) is 2-parameter? B₆(θ) 1-parameter? K₆^{(3)} 3-parameter? S₆? H₆? If the max known family is 3-parameter (K₆^{(3)}), then the variety's dimension is at least 3. Hmm.

Hold on. Let me recall the actual literature on 6×6 complex Hadamards more carefully:

From the paper "Complex Hadamard matrices of order 6" — hmm, there isn't a complete classification paper. Known results:
- The catalog (Szöllősi's "Hadamard matrices up to order 6"? no, the catalog is up to order 6? I believe the online catalog lists all known complex Hadamard matrices up to order 6? Hmm, no — I think it's up to order 6? Let me just go with known families.)

Known 6×6 complex Hadamard matrices (up to equivalence):
1. F₆ (Fourier).
2. The "Dita" family? Dita's construction with 6 = 2·3 gives a family with 2 parameters? Hmm, Dita's construction: for n = ab, H = [H₁ H₂; H₃ H₄]-type block construction gives (a−1)(b−1)? parameters? For 6 = 2·3: 1·2 = 2 parameters. So there's a 2-parameter family containing F₆? Hmm, actually Dita's construction for n=6: I recall the "Dita" family D₆ has 2 parameters? Hmm.
3. Karlsson's family: Karlsson (in "On a class of complex Hadamard matrices"? or his thesis) found a 3-parameter family of 6×6? Hmm, I recall "K_6^{(3)}" — hmm, maybe from the paper by Karlsson? Hmm.
4. The "S_6" family: from Szöllősi's construction? Hmm.
5. "B_6": hmm.

Alternatively, from the MUB(6) literature (Brierley–Weigert "All mutually unbiased bases in dimension 6"? no, that's not complete either): The known 6×6 complex Hadamards relevant to MUBs: F₆, the "Dita" family, "B_6" (from the paper by "Björck"? no...). 

Hmm, I recall the paper "Mutually unbiased bases and complex Hadamard matrices of order 6" or the thesis work: the known families of 6×6 complex Hadamards include:
- F₆
- F₆-like: the family "F(x,y)"? Hmm, maybe "F(x,y)" is the 2-parameter family from the paper by "Tadej–Życzkowski"? Hmm.

Actually! I remember now: There's a well-known 2-parameter family of 6×6 complex Hadamard matrices, sometimes written with parameters x, y ∈ T (the "Fourier-type" family), constructed via the "tensor product deformation" or via "Hadamard 3×3 blocks": the family F(x,y) might be the one from the construction: H = F₂ ⊗ F₃ deformed? The tensor product F₂ ⊗ F₃ is equivalent to F₆? No — F₂ ⊗ F₃ is a 6×6 complex Hadamard not equivalent to F₆ (F₆ = F₆, and F₂⊗F₃ ≇ F₆ as complex Hadamards? Actually F₂ ⊗ F₃ is equivalent to F₆? Hmm: F₆ has entries ω^{jk} with ω = e^{2πi/6}; F₂⊗F₃ has entries e^{2πi jk/2} e^{2πi lm/3} — these are different matrices; are they equivalent? I believe F₂⊗F₃ is NOT equivalent to F₆ (they're distinguished by... hmm, actually I recall that F₂⊗F₃ IS equivalent to F₆? Let me think: the character group of ℤ₆ vs ℤ₂×ℤ₃ — they're isomorphic groups! ℤ₆ ≅ ℤ₂ × ℤ₃. So the Fourier matrices are the same up to permutation of rows/columns. Yes! F₆ is equivalent to F₂⊗F₃.) OK so that's the same matrix.

The known 2-parameter family: I recall the family from "Diţă's construction" gives for n=6 a 2-parameter family? Hmm, hmm. Also there's the family "S_6" from Szöllősi? And "K_6" from Karlsson with 3 parameters? And "B_6" from... hmm, "B_6" might be from the paper "Complex Hadamard matrices of order 6: a computer search"? 

Hmm, let me think about what I actually remember from the literature:

1. **Karlsson's families**: Björn Karlsson, "Hadamard matrices and mutually unbiased bases" (thesis / paper). He found a 3-parameter family of 6×6 complex Hadamards? Hmm, I recall Karlsson found "K_6" — hmm.

2. **The "B_6" family**: I'm fairly confident there's a 1-parameter family denoted B₆(θ) or similar in the literature — possibly from the paper by "Beauchamp"? Hmm, or from "Bengtsson"? Hmm. Actually — I recall in the context of MUB(6), there's the family of "B_6" matrices from the paper by "Brierley"? Hmm.

3. **"S_6"**: possibly the "Sylvester-type"? Or from "Szöllősi"?

4. **"H_6"**: possibly from "Haagerup"? Haagerup's construction? Hmm.

Actually, you know what — I recall the specific known result: **the 6×6 complex Hadamard matrices known include a 4-parameter family**? Hmm no. Let me think about the dimension of the deformation space at F₆. 

There's a classical computation: the tangent space to the dephased Hadamard variety at F_n. For F_n, deformations correspond to "skew" matrices: the tangent space at dephased F₆ has dimension... The known result (from "On the structure of the set of complex Hadamard matrices" or Tadej–Życzkowski "Slater" paper): at F₆, the tangent space dimension is 4? Hmm, I genuinely recall that for n=6, the local dimension at F₆ is 4, and there's a 4-parameter family through F₆? Hmm, but wait — I also recall that the "generic" 6×6 complex Hadamard is isolated? No, that can't be.

Hmm, let me think about it via the "affine" deformation theory: A dephased complex Hadamard H is a point of the variety; the tangent space at H: matrices dH (with dH in the tangent directions) such that H + εdH stays Hadamard to first order: conditions: rows of H+εdH orthogonal to first order: dH_i H_j* + H_i dH_j* = 0, and unimodularity: Re(conj(h_ij) dh_ij) = 0. The dimension of the solution space at F₆: known to be 4? I recall for F₆ the tangent dimension is 4 (and F₆ is a "smooth" point? or singular?). Hmm, and I recall the statement "the set of 6×6 complex Hadamard matrices contains a 4-dimensional family" — hmm, actually now I strongly recall: **the known 6×6 complex Hadamards form families of up to 4 parameters**? Hmm, no wait.

Let me approach from the MUB(6) literature: In the search for MUBs in dimension 6, people search for triples of complex Hadamards. The known 6×6 complex Hadamard families used: F₆, the "Dita" family (2-param), the "B_6" family? Hmm, and "K_6"? 

OK here's another angle: I recall the paper by **Szöllősi, "All complex Hadamard matrices of order 6 up to... "?** no. There's the paper **"Complex Hadamard matrices of order 6" by Wojciech Tadej?** Hmm. And there's the recent arXiv paper claiming classification? I don't recall a complete classification being published — it's a well-known open problem, part of the reason MUB(6) is open.

Known components (from the literature, e.g., the survey "Complex Hadamard matrices and their applications" or the catalog):
- **F₆**: Fourier. 
- **S₆**: I'm now fairly confident "S₆" is a known 6×6 complex Hadamard from the catalog — possibly a 2-parameter family? Hmm, "S_6" — Szöllősi? 
- **K₆^{(3)}**: Karlsson's 3-parameter family — I'm fairly confident Karlsson constructed a 3-parameter family of 6×6 complex Hadamards in his thesis (Björn Karlsson, Lund). Hmm.
- **B₆(θ)**: 1-parameter family — hmm, this could be the family from "Björck–? " no... Could be from the paper "B_6" in the catalog by Szöllősi? Hmm. Or "B" for "Beauchamp"? Hmm.
- **F(x,y)**: 2-parameter family — this might be the family from "Diţă"? Or the "Fourier-type" family F(x,y)? Hmm.

Actually — I remember! There's a known **2-parameter family of 6×6 complex Hadamards** often parametrized as F(x, y)? Hmm, hmm. Or maybe F(x,y) refers to the "Fourier family" F₆ with its deformations parametrized by (x,y)? 

You know, the exact provenance doesn't matter that much for my answer. The problem statement declares the 5 literature families: F(x, y), B₆(θ), K₆^{(3)}, S₆, H₆. I'll take these as: a 2-parameter family F(x,y) (x,y ∈ T), a 1-parameter family B₆(θ), a 3-parameter family K₆^{(3)}, and possibly 0-parameter (isolated/sporadic) matrices or families S₆ and H₆. Hmm, wait — actually I recall now: in the catalog of complex Hadamard matrices of order 6, there are exactly these known inequivalent members: F₆, S₆ (a "sporadic"?), K₆ (Karlsson, 3-param), B₆ (1-param? or the "B_6^{(0)}" and "B_6^{(1)}"?), H₆ (hmm). 

Hmm, actually here's a cleaner memory: In some papers on MUB(6) (e.g., by "Jaffali, Bengtsson, et al."? or the "Hadamard matrices of order 6" section of the Tadej–Życzkowski catalog paper "On the structure of complex Hadamard matrices"?), the known order-6 families are listed as:
1. The **Fourier family** F₆ — but F₆ is isolated in the dephased variety? No...

Ugh. Let me just try to recall the actual state of knowledge about H(6):

**Fact (known)**: The dephased 6×6 complex Hadamard variety contains:
- A **4-parameter family**? or is the max 3? 

I found it: I'm now recalling the paper **"Complex Hadamard matrices and mutually unbiased bases in dimension 6"** hmm. And **Karlsson's thesis** constructs a 3-parameter family. And there's the classical result that **F₆ sits in a 4-parameter family**? Hmm, hmm. 

Actually, here's a cleaner recollection: **The set of 6×6 complex Hadamard matrices, up to equivalence, is known to contain a 4-dimensional "manifold"** — no wait. Let me think about the "Butson" constraint: F₆ is a Butson matrix BH(6,6). Deformations of F₆: the tangent space computation. Let me actually do a quick dimension count for the tangent space at F₆.

Dephased F₆: entries h_ij = ω^{(i−1)(j−1)}, ω = e^{2πi/6}. Free entries: i,j ∈ {2,...,6} (using 1-indexed with first row/col = 1). Tangent vector: d_ij (complex) for free entries, 0 for the dephased entries. Conditions:
1. Unimodularity to first order: Re(conj(h_ij) d_ij) = 0 for each free entry: 25 real conditions.
2. Row orthogonality to first order: for each pair (i,j), Σ_k conj(d_ik) h_jk + conj(h_ik) d_jk = 0? Let me write: rows r_i, r_j orthogonal: ⟨r_i, r_j⟩ = Σ_k r̄_ik r_jk = 0. First-order: Σ_k (d̄_ik h_jk + h̄_ik d_jk) = 0. For pairs involving row 1 (all-ones): Σ_k d_jk = 0 (5 complex conditions). For pairs (i,j) both ≥ 2: Σ_k (d̄_ik h_jk + h̄_ik d_jk) = 0 (10 complex conditions).

Unknowns: 25 complex = 50 real. Conditions: 25 real (unimodularity) + 15 complex = 30 real (orthogonality) = 55 real conditions on 50 real unknowns. The tangent space dimension = 50 − rank(Jacobian at F₆). If the rank is 46, tangent dim = 4. I do recall the number 4 for F₆ — i.e., **the tangent space at dephased F₆ has real dimension 4**? Hmm, but is the tangent space at F₆ actually realized by honest deformations (i.e., is F₆ a smooth point of a 4-dim component, or is the tangent space bigger than the component due to singularities)? I recall that F₆ is a **singular point** of the dephased Hadamard variety? Hmm, and that there's a known 4-parameter family through F₆? Hmm.

Hmm, I now recall more specifically: **the "generic" 6×6 complex Hadamard matrices form a 4-parameter family** — this is stated in some papers as "the set of equivalence classes of complex Hadamard matrices of order 6 contains a 4-parameter family, and it is conjectured that all 6×6 complex Hadamards belong to finitely many families of dimension ≤ 4"? Hmm. Hmm, wait — actually I recall the opposite: that the known families have dimension ≤ 3 and it's open whether there's a 4-dim family? 

Let me think about the "Dita" construction: Dita's construction for n = ab: gives a family with (a−1)(b−1) parameters? For 6 = 2·3: 2 parameters. And there's the "tensor product" deformations. And Karlsson's 3-parameter family. Hmm, and I recall a statement in Karlsson's thesis: "we present a three-parameter family of complex Hadamard matrices of order 6, which we conjecture to be maximal"? Hmm.

Hmm, actually here's a much more solid memory: **In dimension 6, the known complex Hadamard matrices form families of dimension at most 4, and the "manifold" of 6×6 complex Hadamards (the set of equivalence classes) is 4-dimensional at the Fourier matrix**? Hmm no.

OK here's another approach: the problem statement itself says "the 5 literature families (F(x,y), B
```
</details>


---

### Model: Super Bunny Alpha

- **Status:** TRUNCATED (finish_reason: `length`, content: null)
- **Latency:** 138.58s | **Tokens:** 8910
- **Notice:** Call exhausted token limit during internal reasoning; no completion content was emitted.

<details><summary>Truncated Reasoning Trace (29533 chars)</summary>

```
We need craft answer. Need deeply assess mathematical issue. User asks exact formulation to discharge R7 via degree/dimension/Sperner and Positivstellensatz certificates showing any real solution belongs algebraic closure of 5 charts. Need respect no forbidden hype words, especially "proves", "guarantees", "mathematically verifies", "fundamentally", "true intelligence", "impossible", "universal", "flawless", "perfectly", "clearly", "obviously", "simply", "merely", "weaponized". Must avoid those words perhaps inflected? Need not claim MUB bound. Need identify likely conceptual flaw: ideal of complex Hadamard matrices 6x6 perhaps finite set? Classification known: complex Hadamard matrices of order 6: 5 equivalence families? Let’s recall. 6x6 complex Hadamard matrices classified by de Launey/Levin? There are five families, continuous parameters. "I_55 consists 55 polynomials in 50 real variables defining 6x6 unitary matrices with unimodular entries." But ideal? The set of complex Hadamard matrices dimension? Family Diţă: two real params. H_6 family dimension 3? Other families? Need understand.

Question requests exact AG / Positivstellensatz formulation. Key issue: a real radical ideal's real variety may include multiple irreducible components/algebraic charts. Degree/dimension alone cannot exclude detached components; lower-dimensional components can exist. Membership in algebraic closure of one chart cannot generally be certified by polynomial identity/Positivstellensatz in way excluding other components. Positivstellensatz handles infeasibility or strict positivity and semialgebraic constraints, not direct finite component classification. To prove union of closed sets Z(g_j)=0, can use product ideal identity: ∏ g_j ∈ I + Σ? In R[x], if real variety is finite union of algebraic subsets, Nullstellensatz can establish via product polynomial vanishing on V(I), perhaps product in real radical I. But "algebraic closure of one of charts" ambiguously Zariski closure; any real point lies in some? If charts are semialgebraic/constructible families, closures. A Positivstellensatz refutation certificate could encode exclusions with chart-selection inequalities, and derive contradiction. To show implication for every chart? Need formulate exact.

They ask "What exact Stengle/Putinar Positivstellensatz refutation certificate structure can be computed over Q or Q(zeta_24) to certify that any real solution satisfying I_55=0 must belong to algebraic closure of one of canonical charts?" Need explain no single Positivstellensatz certificate merely from ideal unless include selector/guard polynomials. We can provide theorem structure.

Need parse context. Variables x1..x25,y25 corresponding real/imag of 25? 6x6 has 36 entries, but Hadamard condition perhaps first row/column normalized, 5x5 residual, hence 25 complex = 50 reals. I_55 55 polynomial equations. Literature families five. Need likely answer generic parameterized.

Need answer numbered.

First exact AG formulation:
Let A=Q[z_1,...,z_25,\bar z_1,...,\bar z_25]? Identify with R[x,y] via conjugation. I_55. Coordinate ring B=A_R/I. To classify V_R(I), real spectrum points are systems of prime ideals p in B with p+p^σ=p and fraction field formally real (Artin-Lang? real spectrum prime). Detached components are real zero-dimensional/minimal primes p of real radical √[R]{I} with A/p formally real, whose real loci not contained in Zariski closures C_j. There is no finite "degree and dimension" exclusion: any finite collection of points or curves can have small Hilbert function/dim yet detached. Need compute Gröbner/real radical, primary/minimal decomposition, primary/real decomposition. Dimensions of irreducible components only constrain possible count if nonemptiness plus degree/chart intersection. If B reduced equidimensional and all known chart irreducible components have same dimension, and all known components accounted? Degree bound could exclude if chart union degree D and B degree ≤D plus every known chart component is a component and no multiplicity—but this only works with hypotheses, and if degree equals saturation perhaps. Need articulate rigorous sufficient test:
- Let C = ∪ closures of five chart images.
- If C algebraic, ideal J(C)=√? over C/R.
- B maybe projective/affine. Establish I(C)=I(V_R(I)) (real radical).
- C contains V_R(I)? Actually classification means V_R(I)= C_real. To show reverse V_R(I) ⊆ C algebraic, an algebraic identity product of chart ideal generators g_j lies in I. If V(I) ⊆ V(g) for g=∏g_j, real Nullstellensatz says g∈√_R I, certificate g = h_1^2+... + h? General real Nullstellensatz allows h_0? For basic closed semialgebraic no inequalities, V_R(I) subset V(g) iff -? g vanishes. Real radical √_R I = {f: f vanishes on V_R(I)}. Membership has sums of squares representation possibly f^{2m+1}∈I + sums squares (Scheiderer). More generally certificate -? Stengle. Putinar can certify nonvanishing absence with g? To show g=0 on all, use g? Positivstellensatz.
- To exclude component outside, find f in √_R(I +? chart?). If selector p has p>0 on all V(I), then exclude V(I)∩{p≤0} using Positivstellensatz infeasibility: σ0 + ∑ p_j σ_j + Σ squares = -1 (assuming p_j>0; sign details). This is exact.

"belong to algebraic closure of one chart" likely closures C_j. If C_j are algebraic varieties, show V_R(I) ⊆ ∪ C_j. Define g=∏ g_j if each C_j=V(g_j) affine principal—not generally. For arbitrary ideals J_j, product of ideals? To witness union V(I)⊂∪V(J_j), need for every tuple? If f∈J_j all j, product f_1...f_m vanishes union. If each point each has some f_j=0, f=∏ f_j vanishes, so f ∈ I(V_R(I)) = √_R I. This yields real radical inclusion. Exact certificate via sums of squares. But it certifies union containment, not "detached components outside closures" if closures not equal zero loci? Zariski closure is algebraic and can be represented.

However if V_R(I) infinite union of curves. If C_j Zariski closures, all chart points in V(I) by equations. So C_j real loci subset V(I) if I vanishes on charts; desired V(I) subset ∪C_j. Equality. Then product identity.

But Positivstellensatz asks any real solution "must belong to algebraic closure". Algebraic closure is too weak perhaps. If detached points lie inside Zariski closure accidentally, degree/dim not distinguish branch/chart label. Need track real branches and inequalities.

Could formulate branch certificate:
Charts U_α = V(I) ∩ basic semialgebraic set with guard q_α > 0 and chart equations/inequalities. To prove V_R(I)=∪U_α, for each complement disjunct? Since finite union, cover proof can use indicator. A master selector/disjunctive Positivstellensatz. E.g. choose signs/normalization. For every x∈V_R(I), some q_{α,k}>0 or polynomial equalities. If closures algebraic represented by s_{α,k}=0. To refute existence outside:
V_R(I) ⊆ ∪_{α} {s_{α,k}=0}. Introduce disjunction via product. If select inequalities.

Can make Putinar certificate separately for each "outside" local sign cell. Semialgebraic decomposition by signs of guard polynomials. If V(I)∩D_β outside chart, need strict selector >0 there and nonpositive on cell, or guard positive. Stengle handles arbitrary signs p≥0. Standard form:
If K=V(I)∩{σ_j f_j ≥0} empty, then
-1 = s_0 + s_1 + ∑_{f_i>0} s_i f_i + ∑_{f_i<0} s_i(-f_i) + Σ h_k^2
with s_i sums of squares, perhaps s0 and all s_i SOS (Stengle). Putinar only if all constraints p_i≥0, p_i strictly positive, not non-strict general:
-1 = σ_0 + ∑ σ_i p_i + ∑ squares, σ SOS. Strictly positive constraints p>0 can be represented as {p≥0,-p? not}. Putinar theorem: S={x | f_i≥0}={x | f_i>0, sums?} closure? Putinar: S = {f_i≥0 and f>0 on S} maybe f SOS under interior. If K empty, -1 = σ0 + Σ σ_i f_i + sum squares if f_i≥0. Stengle general exact.

Over Q or Q(ζ24): Coefficients? Variables real; if I has complex coefficients, need real and imaginary parts or Galois-invariant norm. Positivstellensatz over base field. Q(ζ24) is not formally real and cannot be ordered as real field. Key important point. Positivstellensatz SOS requires a real closed field/order; Q(ζ24) has no ordering because contains sqrt? ζ24 includes sqrt3? ζ_8, indeed ζ8^3+ζ8^-? Q(ζ8) contains √2, so nonreal. No sums of squares order. You can formulate coefficients in Q(ζ24) and ask real solutions interpreted with conjugate equations, but SOS certificates must be in an ordered/formally real coefficient field such as Q or a real Galois-invariant field, e.g. Q(ζ24+ζ24^{-1}) = real cyclotomic subfield, and Galois norms for complex certificates. Cannot run Putinar over Q(ζ24) directly. This likely essential. User specifically asks over Q or Q(ζ24). We should say direct Putinar over Q(ζ24) invalid; use base change to R? If polynomial coefficients cyclotomic, real/imag splitting over K^+ or take all conjugates. We need be precise.

Also "I_55 subset R[x...]" coefficients real, so Q likely. Phases roots of unity might rational complex field after encoding. If equations in Q(ζ24), impose I and all Galois conjugates? To define real x,y, each complex equation = 0, real and imaginary coefficients in real subfield perhaps. ζ24 real/imag lives Q(√2,√3)? sin π/12 etc; tan? Fine.

Need discuss exact degree/dimension. Coordinate ring B=R[X]/I_55 (they call R maybe real numbers, confusing use \mathbb R and ring R). 50 variables. 55 equations. The ideal of all 6x6 complex Hadamard matrices perhaps not complete intersection, and number equations irrelevant. Need compute Hilbert series, degree. Dimension likely 2? Let's recall five families dimensions. Families:
- F_6(x,y) de Launey? continuous 2 params.
- B_6(θ) one parameter?
- K_6^(3) maybe orbit family 3? "K_6^(3)" maybe isolated? H_6? Classification.
MUB literature families perhaps five families in Matolcsi-Weiner? Let's research from memory.

Complex Hadamard order 6 classification:
Equivalent classes form five families: \mathcal F_6 (2 params), \mathcal B_6 (1 param), \mathcal H_6 (3 params?), \mathcal K_6 (1? exceptional?), and isolated matrices? Notation H_6(z), K_6? There are exactly five: F_6(x,y), H_6(z), K_6(z), T_6, maybe? The user specifies K_6^(3), S_6, H_6. Assume canonical charts.

Known "Classification of complex Hadamard matrices of order 6": five families, including de Launey's \mathcal F_6, \mathcal B_6, \mathcal H_6, \mathcal K_6 and isolated? There are 12 sporadic classes? They claim all excluded R6.

For degree/dim:
Affine coordinate ring degree not finite if positive dimensional. Degree of projective closure. Hilbert polynomial. If all irreducible components of V_R(I) have dimension d, then any chart closure lower dimension can't contain all? Detached components could be same d. A bound on d says no high-dimensional components, but detached 0D/1D remain. Number and degree bounds, if all known charts collectively supply maximal degree and chart ideals are components, could use Bézout. But if B degree > D maybe excludes additional components only under containment and no multiplicity. More exact: If C_j⊂V(I) are irreducible components and B coordinate degree D_B. If union degree D_C = sum degrees C_j, and B reduced with no embedded? Hilbert leading coefficient. If D_B=D_C and each C_j is component, then no others (if positive-dimensional degree accounting). But to know C_j are components, injection ideals etc. If B not radical, multiplicity makes D_B ≥ D_C, equality sufficient; if B radical and C_j distinct. If affine unbounded, degree in projective closure / homogenized ideal. If degree D_B &lt; D_C impossible if C_j subsets? Multiplicities. To use D_B≤ D? Given C_j subset, D_B ≥ union degree (under projective proper conditions). Degree bound D_B maybe known. To exclude extra if D_B=D_union and known chart components included. Lower-dimensional components contribute degree 0 in Hilbert polynomial, so exact next test must primary decomposition or zero-dimensional degree after slicing.

Dimension bound alone: if B Krull dim 2 and known chart closures have dimensions maybe max 2, an extra curve possible same dim; isolated points not visible. Even if all 5 chart components and total Hilbert polynomial matches, embedded/nilpotent/reduced issues and lower-dimensional comps.

"on Sper(R[X]/I_55)" They want perhaps real spectrum. Real spectrum of finitely generated real algebra is not just real points; it includes orderings of residue fields, points over extensions and infinitesimals? A real spectrum comprises prime cones corresponding to orderings of real closed residue fields. A rational real point gives homomorphism to R. A detached component is a minimal prime p of real radical with fraction field formally real. A real closed field with ordering. To classify "all real solutions" in R^50, rational real spectrum V_R(B) is homeomorphic to real zero set? Usually real spectrum includes points corresponding to real closed extensions; for an algebraically closed real field, points correspond to real zeros? There can be nonarchimedean points but topology? Rational real spectrum perhaps yes. We can state conservative.

Exact real algebraic classification:
Let S = R[x_1..x_50]/I. Let I^{rr}=√_R I.
Compute minimal primes over I^{rr}; retract to A. For each p, A/p formally real yields real points? A real prime p with fraction field formally real corresponds to an ordering, but does it ensure real solution in R? No, e.g. x^2+y^2+1? real radical itself? Prime with formally real fraction maybe variety may have no R point? E.g. x^2+y^2+3? fraction formally real (Q(x,y)/(sum squares+3) formally real) but no real zero. Real spectrum nonempty perhaps x^2+y^2+3 positive by sum squares? In formally real field -1 no sum squares; quotient could be formally real. Real spectrum may have orderings but order at x,y requires x^2+y^2+3≥0 possible, yes no rational point but real spectrum point extension. "Real solutions in R" correspond real points; existence of order on residue field may not guarantee R-rational due to model theory? Real spectrum nonempty likely can exist for x^2+1? not formally. x^2+y^2+1 has orderings, yes. So real components of real algebraic set generally V(I) may be empty despite real spectrum? Definition real spectrum nonempty iff ideal is weakly satisfiable over real closed extension. x²+y²+1 has no R zero but has non-Archimedean? In RRCF, x²+y²+1 cannot equal 0 because positive, but order cone could invert signs? A preordering for positivity -f=-(x²+y²+1); choose x,y with huge? SOS x²+y²+1 is sum squares, must ≥0, can't equal 0 in ordered field. So no. It is not weakly satisfiable because f is SOS. Fraction field x²+y²+1 maybe -1=sum squares? f=0 gives -1=x²+y², no. Not formally real indeed. x²+y²+3=0 gives -3 sum squares, could imply sqrt3? -1=(x/√3)^2... extension with √3 not sum? In ordered field containing? sqrt(-3) no, fraction likely formally real; at zero x²+y²=-3 can be negative, possible, so nonarchimedean real closed extension point. Thus no R point. So distinguish real spectrum and R-rational points. User explicitly Sper and real solution perhaps likely wants real points. We should mention.

For real Nullstellensatz, define √_R I = {f | f vanishes on V_R(I)}; over real closed field. "Real radical" yes. Minimal primes of real radical correspond irreducible components that have R points? Let's check x²+y²+3 real radical ideal itself (irreducible and zero set? It has no R points, vacuously all polys vanish, so real radical of whole ring would be (1), contradiction! Real Nullstellensatz formula √_R(I) = I + sums? If V_R(I)=empty over R, real radical is &lt;1&gt;. Indeed real radical computed by sums of squares likely 1. So minimal primes of real radical correspond components with real points, not just formally real primes? Real spectrum points may be non-rational but if component has real closed extension point then perhaps real radical doesn't eliminate. But over real closed K, real points = K points. Real radical ideal? I=(x²+y²+3) in R[x,y], does it contain a representation yielding 1? f=0 doesn't conflict with SOS due 3. Could real Nullstellensatz says f is in real radical iff f=0 on K points. It has no K points, so 1 should. Is 1 in real radical of (f)? Real radical definition I+Σsquares? f? 1 =? Since f=0, can we derive SOS=1 using f and square h²? Need h maybe polynomial linear? f itself is SOS plus 3, not 1. If ideal plus SOS: 1=s+h f? Maybe 3 is positive constant, no polynomial SOS expression 1-h f? Could choose h=1/3, s=1-(1/3)(x²+y²+3)= -(1/3)(x²+y²), not SOS. Other h. Real Nullstellensatz indeed says V_R(I) empty iff -1 ∈ I + Σ[a_i²+b_i²]? Here -1 =? f itself x²+y²+3=0 means x²+y²=-3, can -1 be sum rational squares? multiply? 1/3 not square. But 1=(1/3)*3 and 3=-x²-y², not sum squares due negative. No.

Wait real Nullstellensatz: √[R]{I} = {f | ∃ m, -f^{2m} ∈ I+Σ squares?} perhaps. If V empty, 1 in. Is I+(x²+y²+3) already real prime? Quotient R[x,y]/f. Is fraction field formally real? If f=0, -3=x²+y². Could -1 become sum squares? Since 3 positive in any ordering, x²+y²=-3 &lt;0 impossible under usual order on rational 3, so no ordering. So fraction not formally real, but ideal not real prime due no ordering. Real radical likely contains 1 via something. Can find -1 = a f + SOS? Let a constant c. -1-cf = (-1+3c)-c(x²+y²). Choose c&gt;0, constant 3c-1≥0 and coefficient -c means subtract c squares, not SOS. no.

Maybe x²+y²+3 actually has complex zeros but no R zeros; ideal's real radical should 1. Formula real radical uses f^{2m+1}, and Positivstellensatz: if f≥0 no zeros, 1-f? Since f is positive, f = x²+y²+3; 1 = (1/3)(? cannot SOS constant 1/3 not square in polynomial ring but can sum? 1/3 not square polynomial with rational coefficients, but over R, constant 1/3 = (1/√3)^2, coefficients allowed R! I=R coefficients, h=1/√3. 1 = (1/3) f +? (1/3) f = 1 +(1/3)(x²+y²), subtract SOS; not. Need 1 =? -1 = a f + SOS, choose a? c negative perhaps: c=-1/3 => -1+ f/3=x²+y² SOS. Yes -1=(-1/3)f+x²+y². Thus 1 in real radical. Over Q coefficients, 3 SOS? 3=1²+1²+1², -3 = -1²-... Then 1=(1/3)f -(1/3)(x²+y²) no SOS. But can scale 3: -3=(-1/3)f+x²+y² is SOS representation RHS but 3 positive; To get 1, -? multiply by square 1/3 which is square of 1/√3 not Q. Over Q, 1/3 not SOS rational. Maybe -1? formula. Yet real closed field coefficients can √3. Context R coefficients, so fine. Empty real set.

Minimal primes of real radical over R indeed components with real points perhaps.

For real spectrum Spec_r, orderings correspond to preorderings, and x²+y²+3 cannot zero due sum positive, so no real spectrum. Thus formally real quotient condition for prime plus f relation? In quotient f, f itself is sum squares +3, but 3=sum squares (1²+1²+1²) in any ordered field, so f=0 is sum squares, forcing all x,y and each 1 zero, contradiction. Thus f is sum squares in quotient! Although 3 is sum 1²+1²+1², yes x²+y²+1²+1²+1²=0. So ideal contains sum squares, violates -1 not sum? In ordered field sum squares zero means each zero, including 1. So no order. Fraction not formally real indeed. Good. So condition works.

Real points of a prime with formal reality? A prime quotient domain formally real has some ordering by Artin-Schreier, yielding real spectrum point but perhaps residue field not real closed. A real closure gives RRCF extension and point. So V_R(I) over R? An extension solution not coordinate point. Real spectrum nonempty. But if I is real radical, any order point. Thus real radical can include prime no R-rational points but real spectrum point over real closure. Does minimal prime of real radical correspond extension components. Real Nullstellensatz over R? If p has ordering, does V_R(p) necessarily have R point for a finitely generated algebra? Not necessarily: conic x²+y²=3z² has real points yes. Some anisotropic varieties? Real closed field R is real closed; an ordering extension may not be archimedean, polynomial may no archimedean solution. Example p from an isolated real closed extension with polynomial positive? e.g. p minimal polynomial? R is real closed, every odd poly has root. Multivariate maybe ordering but no R point likely yes. So real spectrum captures more.

Question says "real solution" likely coordinate over R. Strict answer can distinguish.

Second part certificate. Let's design a robust framework.

Definitions:
A = \mathbb R[\mathbf x,\mathbf y].
f_1,...,f_55 generate I.
Let chart parameter maps:
φ_α: \mathbb R[t_{α1},...,t_{αr_α}] → A,
possibly after normalizations, image Γ_α. Let C_α = \overline{Γ_α}^{Zar} = V_A(J_α), where J_α=(φ_α(t_\alpha)-v_i(v)): if source independent variables then J=0. More generally elimination ideal J_α=I(Γ_α). Need ensure J_α real and C components.

Desired containment:
V_\mathbb R(I) ⊆ C = ∪ V_\mathbb R(J_α).
Equivalent chart sets cover actual real variety if Γ are dense in C and C components. Algebraically, if J_α are real radical, select finite g_{αk} with V(J_α)=V(g_{αk}) only if affine variety principal; not all algebraic sets principal. But to create a polynomial g vanishing on C, choose a polynomial in J_α nonzero on C. For positive-dimensional irreducible component, generic linear form g_{αk} ∈ J_α may vanish on C; affine coordinate with scaling. Projective closure ideal generated by multiple homogeneous forms; choose sufficiently many/generic linear forms g_{αk} whose common zero C. We need a selector. Could use product of one polynomial per chart if find g_α∈J_α with C_α=V(g_α). Is every affine variety hypersurface? no. Instead can form product of sums? If J_α generated j_{α1},..., j_{αr}, common zero union. To ensure point in one chart, all j_{αk}=0. A disjunction of conjunctions. Product-of-ideals membership characterization: ∏_α J_α ⊆ I? In commutative rings, if x∈J_α for each α, then product x_1...x_m ∈ ∏J_α⊂I. For membership, choose generators. But I(C) (ideal of union) equals J_1⋯J_m for algebraic sets over algebraically closed field (ideal of finite union is product of ideals). For real sets, real ideal I(V_R union) may be real radical of product. Thus if show product ideal subset I maybe C⊂V(I), opposite. We already know C⊂V(I). To show V(I)⊂C, need I(C)⊂I perhaps. Since C⊂V(I), I(V(I))⊂I(C), opposite. Equality needed.

We can state exact criterion: V_R(I)⊂C iff I(C)⊂I (where I(S) all polys vanish on S). Compute I(C)=√_R(J_1⋯J_m). Need certificates for generators h_l∈I(C) represented in I + SOS. Real radical membership. For finitely generated ideal product (known finite Hilbert basis), can check Gröbner basis. This is an exact algebraic geometry route, not necessarily Positivstellensatz.

But user specifically asks Stengle/Putinar refutation certificate. We can formulate local branch exclusion:
For each sign cell σ ∈ {−,0,+}^k for finite chart guards g_i, define:
K_σ = V_R(I) ∩ {ε_i g_i ≥ 0? exact sign}. If K_σ∩C =∅, produce a Positivstellensatz identity.

Stengle's Positivstellensatz for infeasibility:
Given p_j and signs:
-1 = σ_0 + ∑_{j} σ_j a_j p_j + ∑ h_l²,
where σ_j SOS and a_j=0,1,−1 for p_j=0,p_j≥0,p_j≤0, perhaps indexing. Is this always enough? Need verify Stengle form. Stengle says for empty basic semialgebraic S={f=0, f>0, f≥0}, there exist SOS σ_i such that
-1 = σ_0 + ∑ σ_i f_i + σ_{sos}, where multipliers positive/negative adjusted. Yes. For equality constraints, σ=0. We can write:
-1 = σ_{\rm eq? maybe σ_0} + Σ_{positive} σ_i g_i + Σ_{negative} σ_i(-g_i) + Σ h²
with strict constraints? If K uses g_i≥0, p_i=g_i. For ≥ constraints, yes. For ≤, use -g. Equality ideal terms. Putinar form is special all p_i≥0:
-1 = σ_0 + ∑ σ_i p_i + ∑ h², σ_i SOS. Putinar applies to empty K with non-strict p≥0 under its theorem? Classic Putinar: S={f_i≥0}; if f (SOS) strictly positive on S, f ∈ quadratic module; setting f=1 empty yields representation. Yes. Stengle handles strict/disjunctive general? User says Stengle/Putinar. We can give both.

For "outside C" with multiple charts and strict chart guards:
If a chart is Zariski closure C_α=V(J_α), no inequalities needed. To refute V(I)∪_{k}V(j_{αk}):
S = V(I) ∪ ⋃_{α,k}{j_{αk}≠0}? Want no point with all chart equations nonzero. A point outside C means for every α,k j_{αk}≠0. Finite strict disjunction. Convert to {−j_{αk}>0} plus I. If empty, Stengle cert. But Putinar can't represent ≠ as polynomial ≥0 directly; split sign cells: for each sign vector ε_{αk} ∈{±1}, K_ε = {I=0, ε_{αk} j_{αk} ≥ 0} and require at least one strict? If all nonzero, choose either signs and all >0. Could use ≥ includes zeros on C, so K includes points already in C, not empty. Need enforce nonzero via strict >0. Stengle can handle strict. Or use open cover and local real radical certificates: for each x outside C, p_α? finite open covers. There is no global polynomial strictly positive on V(I)\C if complement open? Could use sign cells with a "selector" that vanishes on C and positive outside? Product etc.

Alternative use algebraic union identity avoids strict selectors: pick polynomial P=∏_{α,k} j_{αk}? A point outside all C has all j≠0 so P≠0, but C points P=0. To show no outside, show P vanishes on V(I), i.e. P∈√_R I. Real radical certificate can be expressed as -? Putinar: If -P? To show P=0 on V(I), assume nonzero and split signs. A real Nullstellensatz certificate:
P^{2m+1} = Σ h_i f_i + Σ s_j
? If P^{odd} in I + SOS, then on V(I), P^{odd}=SOS≥0, does not force P=0 unless odd exponent? If P&lt;0 then negative; if P&gt;0 positive, no contradiction. If use -P? Need both P and -P certificates:
P^{2m+1} = a + Σsquares, and -P^{2n+1}=b+Σsquares. On V, if P&gt;0 first is ≥0 no issue, second LHS negative must ≥0 contradiction; if P&lt;0 first contradiction. Thus P=0. Membership in real radical has -P^{2m+1} ∈ I+Σsquares for some m; this alone says P cannot be &lt;0 or zero? At P=0 okay. On V, RHS SOS, -P^{odd}≥0 =&gt; P≤0. Another exponent/sign gives P≥0. Real Nullstellensatz definition often f∈√_R I iff -f^{2m+1}∈ I+Σ SOS for some m. This only says no f&gt;0, not equality. If f vanishes, indeed. If f negative somewhere, no. If f positive somewhere, no. But to force f=0, need rule out f≠0 both signs: perhaps apply to f? Rules out positive, and apply to? real radical closed under multiplication not negation. Apply -f? -(-f) = f, not same. Need -(-f)^{odd}=f^{odd} ∈ preordering. So both. Maybe real Nullstellensatz formula f∈√[R]I iff ∃m, -f^{2m+1} ∈ I+Σ squares. Why would this force f≤0 on V, not zero. Example f=x on V={x≤0}? But V(I) zeros of equations, not inequalities; x may be negative on an algebraic component e.g. V(x²+1) empty, f? If V empty all. For V(x+1), f=x+1=0. General polynomial vanishing iff both? It can be ≤0 without zero: V(x²-1), f=x-1 ≤0 and no positive, yet not vanish at x=-1. Is x²-1 real radical and - (x-1)^{odd} in I+Σsquares? Test maybe x-1≤0 on {-1,1}, can SOS represent -(x-1)^3 modulo x²-1? At x=-1 =8 positive, x=1=0, polynomial SOS modulo I. Could be? Let 2? -(x-1)^3 modulo: x³= x, (x-1)^3=x³-3x²+3x-1 ≡ x-3+3x-1=4x-4; negative =4-4x values 8,0, linear nonnegative on finite set; can represent SOS modulo x²-1 e.g. (2?); likely yes. So formula perhaps real radical in ordered field sense is f≥? Let's recall:
Real Nullstellensatz: √_R(I) = {f | f^{2m+1} ∈ I + Σ squares?} maybe with sign? If f≤0 on V, -f≥0, then (-f)^{odd} = -f^{odd} nonnegative and could be SOS modulo I for finite set. So -f^{odd} membership. Thus indeed membership means f≤0? This can't equal vanishing ideal. Maybe definition of real radical ideal is {f | f^{2m+1} ∈ I+ΣS²}? x-1 on ±1: f values -2,0, not all signs; f itself nonpositive, odd f nonpositive, cannot SOS, so f not. -f^{odd} positive, so membership but ideal not closed under negation. Thus not ideal? Real radical should be ideal. Formula likely:
√_R I = { f | ∃m, f^{2m+1} = g + h_1^2+... } and also? For x-1 fails (negative at -1). For f? x+1 values 0,2 positive fails. Vanishing works. So f^{odd} ∈ I+Σ squares, no minus. But for f=-x-1? values 0,-2, odd negative, fails. Why no sign? If f positive, also fails. Thus both signs. This is plausible. Some definitions use -f^{2m+1} ∈ I + preordering? Let's look up real radical: f^m ∈ I+Σ[i?]? In real algebraic geometry, f in real radical iff ∃m such that f^{2m+1} = -s_1 - h_1²... (negative SOS), not positive. Since on V, f^odd=-SOS≤0. Again only f≤0. But ideal perhaps intersection? Hmm.

Real Nullstellensatz: I(V_R(I)) = { f | ∃m, - f^{2m+1} ∈ I + Σ h²}. If f=x-1 on ±1, -f positive at both (8,0), can be SOS modulo. So membership, contradict ideal. Maybe real radical is defined as f that is either ≥0 or ≤0? Let's retrieve exact theorem.

There are two notions:
- real radical √[R]{I} = {f | ∃ odd m, f^m ∈ I + Σ a_i²}
- weak real radical? 
If f vanishes, yes f^m=0. If f has fixed negative sign, cannot positive SOS, so not. If fixed positive sign, f^m positive may potentially be SOS modulo I even without vanishing. Example V(x²-1), f=x+1 values 0,2. Is x+1 odd positive; can represent SOS modulo? f=0 at -1, 2 at 1. SOS h(x) matching values 0 at -1 forces h(-1)=0; possible h=(x+1)g, at 1 value 2g(1)=2, g(1)=1, yes h=x+1 exactly! Then h² - f? h²-(x+1) = (x+1)x = x²+x? modulo x²-1 gives? h² - f = (x+1)^2-(x+1)=(x+1)x=x²+x ≡1+x=f, so f = h² - (x²-1), SOS. Thus positive nonvanishing f is in I+ΣSOS. So x+1 would be in real radical, impossible if real radical an ideal? Wait ideal I=(x²-1) itself is real (all points real), so x+1 obviously belongs I? Is x+1 divisible by x²-1? no. But I is real radical as ideal? If I is real ideal, contains I and for any f in I membership. x+1 isn't I. Formula
```
</details>


---

## Gap G2: Candidate Representation Bridge Unconditional Discharge

### Model: GLM 5.3

- **Status:** TRUNCATED (finish_reason: `length`, content: null)
- **Latency:** 40.35s | **Tokens:** 8677
- **Notice:** Call exhausted token limit during internal reasoning; no completion content was emitted.

<details><summary>Truncated Reasoning Trace (28873 chars)</summary>

```
The user is asking me to explain, under strict epistemic governance rules, how the Candidate Representation Bridge becomes unconditional once G1/R7 is discharged. This is about the MUB(6) program — mutually unbiased bases in dimension 6 — and a formal verification effort in Lean 4. The context mentions:

- Gap G2 is DISCHARGED_CONDITIONAL on G1
- Mechanized in TargetA7ZeroRelVariety.lean (CurvatureWallCertifiedAtlas)
- Establishes that every candidate quadruple built from the declared catalog representatives exhibits a certified curvature wall obstruction Ψ² > 0

The task has three parts:
1. Detail the exact quotient map from the affine variety V(I_55) to the dephased orbit space M_6 = V(I_55) / (T^5 × T^5 ⋊ S_6 × S_6)
2. How is PSD of the Gramian block matrices and dual SDP witness matrices W = LDL† preserved under continuous gauge transport along each Hadamard orbit?
3. What explicit theorem specification in Lean 4 connects the real spectrum gluing of G1 directly to TargetA7ZeroRelVariety.lean without circular dependencies, respecting the firewall?

Important constraints:
- Strict Firewall: NEVER claim or imply MUB(6)=3 or MUB(6)≤3. All findings apply strictly to the declared region/moduli and mint no authority.
- Claim Hygiene: no hype verbs.
- For each gap analysis: what it supports, what it does not support, narrowest defensible claim, next test needed.

Let me think about the actual mathematics here to give a substantive, precise answer.

Background on MUB(6): In dimension 6, it's unknown whether there exists a complete set of 7 mutually unbiased bases. The program appears to be a formal verification effort that decomposes the problem into gaps G1–G5. The structure suggests:

- G1/R7: something about "real spectrum gluing" — likely a result that the relevant variety/spectrum can be reduced to real points, or that spectral data glues across charts. "R7" might refer to a reduction step. The phrase "real spectrum gluing" suggests gluing local real spectra (perhaps of the curvature/obstruction functional) into a global statement.

- G2: Candidate Representation Bridge — the claim that it suffices to check candidate quadruples built from declared catalog representatives (e.g., known families of complex Hadamard matrices in dimension 6, like the Fourier family F(6), the spectral family F(2)⊗F(3) with parameterization, the "self-dual" family, etc.). The catalog of 6×6 complex Hadamard matrices: at present, infinitely many families are known; the classification is complete only up to certain equivalences for some subclasses. The "declared catalog" is a finite/explicit list of parameterized families.

- TargetA7ZeroRelVariety.lean: a Lean file mechanizing something about the target A7 (perhaps the 7th basis in a putative complete set, or an "A7" structure) and the "zero-rel variety" — the variety defined by the relations that must vanish for a candidate to extend. The CurvatureWallCertifiedAtlas: an atlas of charts each certifying a "curvature wall" Ψ² > 0 — a second-order obstruction. Ψ² > 0 likely means the curvature of some functional at a critical point is positive, so the point is a strict local minimum / isolated, or the obstruction functional is bounded away from zero, preventing the existence of a solution in that chart.

So the Candidate Representation Bridge (G2) says: every candidate quadruple (perhaps every putative extension of a triple/quadruple of MUBs) is equivalent, up to the symmetry group, to one built from the declared catalog representatives. This is conditional on G1 because G1 presumably establishes that the relevant moduli/spectrum reduces to the catalog region — e.g., that any solution would have to lie in the region covered by the atlas, or that the real spectrum gluing covers all boundary strata.

Now the three questions:

**Question 1: The exact quotient map from V(I_55) to M_6.**

V(I_55): an affine variety cut out by an ideal I_55 — presumably 55 relations (or an ideal in 55 variables?). In the MUB problem, one can set up the problem as: fix the first basis to be the standard basis (dephasing), then the other bases are given by complex Hadamard matrices (unitary matrices with all entries of modulus 1/√6). Dephasing: multiply rows/columns by phases to make first row and first column all real positive (equal to 1/√6, or after normalization, the matrix is a "dephased Hadamard" with first row and column all 1s).

The symmetry group: T^5 × T^5 ⋊ S_6 × S_6. Hmm — actually the full symmetry group of the MUB problem in dimension 6: left and right diagonal unitaries (phases) — dephasing uses U(1)^6 × U(1)^6 modulo overall phase, so effectively T^5 × T^5 (the 5-torus in each factor after quotienting the diagonal U(1)), and permutation matrices S_6 × S_6 (row and column permutations). Actually the full equivalence group of complex Hadamard matrices is (permutation × monomial unitary) on each side: the "Hadamard equivalence" group. After dephasing, the residual symmetry is smaller, but the orbit space of dephased matrices under the residual group is what's usually considered.

Wait — the question says "dephased orbit space M_6 = V(I_55) / (T^5 × T^5 ⋊ S_6 × S_6)". So V(I_55) is presumably the variety of (not-yet-fully-dephased?) candidate configurations — maybe the variety of quadruples of Hadamards satisfying MUB relations, cut out by 55 polynomial relations (e.g., the orthogonality relations among rows across bases, plus Hadamard constraints). The quotient by T^5 × T^5 (row/column phase rephasings, having fixed one row/column as anchor — hence 5-dimensional tori, since one row and one column are pinned by dephasing) and by S_6 × S_6 (row and column permutations) gives the dephased orbit space.

Actually, let me think more carefully. A 6×6 complex Hadamard matrix H: entries |H_ij| = 1/√6 (or 1 after normalization), rows orthogonal. Equivalence: H ~ D_1 P_1 H P_2 D_2 where D_i diagonal unitary (phases), P_i permutation. Dephasing: use D_1, D_2 to make first row and first column all 1s (real). The dephasing freedom remaining: phases that preserve the dephased form — diagonal matrices with phases only in rows/columns 2..6 that cancel: actually residual symmetry of dephased matrices is generated by: simultaneous conjugation... Let me recall: for dephased Hadamards, the residual equivalence is by "gauge" transformations: multiply row i and column j by phases such that first row/column stay real — i.e., D_L = diag(1, e^{iθ_2}, ..., e^{iθ_6}), D_R = diag(1, e^{-iθ_2}, ..., e^{-iθ_6})? No wait, that's for preserving H_{1j} = H_{i1} = 1: D_L H D_R has (1,1) entry e^{iα}·1·e^{iβ}... Let me not over-derive; the point is the torus T^5 × T^5 acts, and the semidirect product with S_6 × S_6 (permutations that then require re-dephasing) generates the full equivalence.

Hmm, but actually the question states the quotient map explicitly: M_6 = V(I_55) / (T^5 × T^5 ⋊ S_6 × S_6). So I should describe:

- V(I_55) ⊂ A^N (affine space over ℂ, or over ℝ after G1's real spectrum gluing) — the incidence/compatibility variety defined by the ideal I_55 of 55 relations. What are the 55 relations? Possibly: for a quadruple of bases (B_1, B_2, B_3, B_4) with B_1 fixed to the standard basis after dephasing, the MUB conditions |⟨b_i^{(k)} | b_j^{(l)}⟩|² = 1/6 for all i,j and k≠l give polynomial relations in the phase variables. If we write each Hadamard entry as e^{iθ}/√6, the MUB conditions are sums of cosines equal to zero — trigonometric polynomial relations. Converting via z = e^{iθ} to polynomial relations in torus variables: |Σ_k z_k|² = 0 type relations. The number 55 could be the count of independent relations after symmetry reduction for the specific ansatz (e.g., the "zero-rel variety" — the variety where certain relations vanish).

Alternatively, I_55 might be the ideal of the "zero relations" — TargetA7ZeroRelVariety suggests "A7 zero-rel variety": the variety where the relations that must be zero for the A7 (7-basis) structure to exist... Actually "TargetA7" might mean the target of extending to 7 bases (a complete set of 7 MUBs in d=6). The "ZeroRel" variety: the subvariety where the obstruction relations vanish identically — i.e., the locus of candidate solutions.

I don't need to know the exact 55; I can describe the structure: I_55 is generated by 55 explicit polynomial relations (given in the file), V(I_55) is the affine variety of candidate configurations (e.g., quadruples of dephased Hadamards satisfying the pairwise MUB relations up to the catalog ansatz), and the quotient map π: V(I_55) → M_6 quotients by the rephasing torus and the row/column permutation group.

The quotient map details:
- The group G = (T^5 × T^5) ⋊ (S_6 × S_6) acts on V(I_55) by (D_L, D_R; σ, τ): H ↦ D_L P_σ H P_τ D_R (with appropriate re-dephasing normalization to land back in the dephased slice — i.e., the action is a "gauge transport": apply the monomial equivalence, then apply the unique dephasing gauge to restore first row/column to 1s).
- Actually more precisely: the full monomial group (U(1)^6 ⋊ S_6) × (U(1)^6 ⋊ S_6) acts on the space of Hadamards; the dephasing map δ: H ↦ D_L(H) H D_R(H) is a section onto the dephased slice; the residual action on the slice is by the subgroup that commutes appropriately — the T^5 × T^5 ⋊ S_6 × S_6 as stated, where T^5 = {diag(1, e^{iθ_2},...,e^{iθ_6})} acting as D_L H D_R with D_R = D_L^{-1} restricted appropriately... Hmm.

Let me set it up cleanly. Let H be 6×6 with |H_ij| = 1 (normalized Hadamard, entries unit modulus, HH† = 6I). Equivalence group: G_full = (Mon_6 × Mon_6) where Mon_6 = U(1)^6 ⋊ S_6 (complex monomial matrices). Action: (M_L, M_R)·H = M_L H M_R† (or M_L H M_R). Dephased slice: H_{1j} = H_{i1} = 1 for all i,j. Every orbit meets the slice: dephasing uses the phases of first row and first column. The stabilizer-like residual: the subgroup of G_full preserving the slice is: M_L = diag(e^{iα_1},...,e^{iα_6}) P_σ, M_R = diag(e^{iβ_1},...,e^{iβ_6}) P_τ with constraints... For the slice to be preserved we need (M_L H M_R)_{1j} = 1 and (M_L H M_R)_{i1} = 1 for all H in the slice — that forces σ(1)=1... no wait, permutations move the first row. Hmm, actually the standard treatment: the dephased Hadamard is a canonical form; two Hadamards are equivalent iff their dephased forms are related by an element of the "dephased equivalence group" which includes permutations that fix... no — actually two dephased Hadamards H, H' are equivalent iff H' = D_L P_σ H P_τ D_R for some phases and permutations, and then H' dephased equals... The standard result: equivalence classes of Hadamards ↔ orbits of dephased Hadamards under the group generated by: (a) "gauge" phase moves: H ↦ D_L H D_R where D_L = diag(1, e^{iθ_2},...,), D_R = diag(1, e^{-iθ_2}, ...) — wait that doesn't preserve dephased form in general.

Let me just do it: dephased H: H_{1j} = 1 ∀j, H_{i1} = 1 ∀i. Apply D_L = diag(e^{iα_i}), D_R = diag(e^{iβ_j}): (D_L H D_R)_{ij} = e^{iα_i} e^{iβ_j} H_{ij}. First row: e^{iα_1} e^{iβ_j} · 1 — to be 1 for all j need β_j = -α_1 ∀j, so D_R = e^{-iα_1} I. First column: e^{iα_i} e^{-iα_1} · 1 = 1 need α_i = α_1 ∀i, so D_L = e^{iα_1} I. So pure diagonal phase moves act trivially on the dephased slice (they move off the slice and dephasing brings you back). The residual symmetry on the slice: permutations. P_σ H P_τ: first row becomes row σ^{-1}... (P_σ H)_{1j} = H_{σ^{-1}(1), j}. To stay dephased need σ(1)=1 and τ(1)=1? No: (P_σ H P_τ)_{1j} = H_{σ^{-1}(1), τ^{-1}(j)}. For this to be 1 for all j need σ^{-1}(1) = 1 (i.e., σ fixes 1) and τ^{-1}(j) arbitrary — H_{1,τ^{-1}(j)} = 1 ✓ since first row all 1. So need σ(1) = 1. Similarly first column: (P_σ H P_τ)_{i1} = H_{σ^{-1}(i), τ^{-1}(1)} = 1 need τ(1) = 1. So permutations fixing the first index preserve the slice: S_5 × S_5 acting on indices {2..6}. But then after permutation, the entries are still unit modulus but the matrix may no longer be... wait it is still dephased. Hmm, but the standard "Hadamard equivalence" of dephased matrices: H ~ H' iff H' = P_σ H P_τ (dephased both) up to... no. Actually the correct statement: two Hadamards H, H' are equivalent iff their dephasings are related by H'_dep = P_σ H_dep P_τ for permutations σ, τ with... no, that's not right either because dephasing after permutation gives extra phases.

Standard fact (e.g., from Tadej–Życzkowski / Brierley): the set of dephased Hadamards H_n (first row and column = 1) parametrizes equivalence classes, but with residual identifications: H ~ H' if H' = P H Q for P, Q permutation matrices — but then H' might not be dephased... P H Q has first row = row of H (all ones in first row? (PHQ)_{1j} = H_{σ^{-1}(1), τ^{-1}(j)}). Hmm, if σ, τ don't fix 1, the first row of PHQ is a permuted row of H, which is not all-ones. Then dephasing PHQ gives a different dephased matrix. So the equivalence on dephased matrices is: H_dep ~ H'_dep iff ∃ monomial M_L, M_R: H' = M_L H M_R. This is a complicated action on the slice.

But the question tells us the group: T^5 × T^5 ⋊ S_6 × S_6. So the setup must be: V(I_55) is NOT the dephased slice; it's the full variety of configurations (with phases), and M_6 is the orbit space under the full rephasing + permutation group, called "dephased orbit space" because it's identified with orbits of dephased representatives. So the quotient map π: V(I_55) → M_6 := V(I_55)/G where G = (T^5 × T^5) ⋊ (S_6 × S_6).

Why T^5 × T^5 rather than T^6 × T^6? Because the overall phase (diagonal U(1) acting as scalar) acts trivially on the relevant objects (projective/quantum states are up to phase), or because one phase per side is fixed by normalization. In the MUB problem: bases are orthonormal bases; each basis vector has a phase freedom (6 phases per basis, but one per basis is trivial → 5 per basis... hmm). Actually for a set of 7 bases: each basis B_k = {v_1^{(k)},...,v_6^{(k)}}; rephasing each vector: v_i^{(k)} ↦ e^{iθ_i^{(k)}} v_i^{(k)} — that's U(1)^6 per basis, U(1)^{42} total; but MUB relations |⟨v,w⟩|² are invariant under all of these. Fixing the first basis to the standard basis and dephasing the others: each Hadamard matrix H_k (k=2..7) has row phases (6) and column phases (6); dephasing kills 11 of the 12 (first row and first column), leaving... the dephased matrix has no residual phase freedom except the "gauge" transformations that preserve dephased form — which we showed are trivial for pure phases. Hmm, so where does T^5 × T^5 come from?

Alternative: the "quadruple" — candidate quadruple of Hadamards (H_2, H_3, H_4, H_5?) — and the torus T^5 × T^5 acts by rephasing rows and columns of... one designated Hadamard? Or: the variety V(I_55) parametrizes a single Hadamard plus data, and T^5 × T^5 is the row/column phase group with the (1,1) anchor removed: row phases (θ_1,...,θ_6) with θ_1 = 0 → T^5; column phases similarly → T^5. That makes sense: the dephasing gauge has been partially fixed (first row and column of the designated matrix pinned), leaving T^5 × T^5 as the residual rephasing that moves within... no wait, if first row and column are pinned, residual phases are trivial as shown.

Hmm, let me reconsider: maybe V(I_55) is the variety of "candidate quadruples" where the quadruple is (H_1, H_2, H_3, H_4) — four bases beyond the standard one? Or the problem is about quadruples of MUBs (4 bases), and the bridge says: to rule out extendability to 7, it suffices to check quadruples from the catalog.

Actually, let me think about what's known in the literature: The MUB(6) problem. Known results: complete sets of MUBs in dimension 6 are unknown; the best known is 3 MUBs (many triples exist). There are results like "any complete set would contain a quadruple equivalent to one from a finite list" — e.g., work by Brierley, Weigert, D'Ariano et al. on classifying pairs/triples of MUBs in d=6. Also "Hadamard matrices in d=6": infinitely many equivalence classes (e.g., the one-parameter Fourier family F(6) ⊗ ... no, F(2)⊗F(3) is a one-parameter family F_{2}⊗F_{3}(a) — actually the family F(2)⊗F(3) with parameter, and the "Fourier" F(6), and sporadic ones like the "Tao" matrix... In d=6, known: a one-parameter family containing F(6) and F(2)⊗F(3) (the "spectral" family), plus isolated classes (e.g., from the classification of Butson/other). The full classification of 6×6 Hadamards is open — infinitely many? Actually it's known there are infinitely many equivalence classes? Hmm — in d=6, I recall it's not known whether there are finitely or infinitely many equivalence classes... Actually I believe it's known that there are infinitely many (families with parameters)? Let me recall: 6×6 complex Hadamard matrices: known families include the 1-parameter family F(6)∼F(2)⊗F(3) (they're in the same family — the "Fourier family" F_{6}^{(1)}(a)), plus isolated matrices like the "Dită" matrices? Hmm. The classification is complete for n=5 and below; for n=6 there's a known list of families but completeness is open. Recent work (e.g., by Óstereich, or the "Hadamard" databases like the catalogue of Đoković) lists many 6×6 families. I recall that for 6×6, there are known: F(6) family (1-param), plus several isolated/sporadic classes, and it's an open question whether the list is complete. Actually I recall a result: "all 6×6 Hadamards with a certain symmetry" classified. The "declared catalog" in this program is presumably an explicit finite list of parameterized families that the program declares as its region.

Given the firewall rules, I don't need to assert the catalog is complete — indeed the whole point of the governance is that the catalog is a declared region, and G1 (real spectrum gluing) presumably establishes that the region covered by the atlas (charts from catalog representatives) exhausts the relevant locus — e.g., that any point of the real spectrum of the relevant quotient lies in the image of the atlas. Hmm, but G1 discharged would give: the real spectrum gluing — a statement that the real points of some structure are covered by gluing local pieces.

Let me now think about what "R7" is: "G1/R7" — G1 is the gap, R7 might be the requirement/step R7 in a roadmap. "Real spectrum gluing": In real algebraic geometry, the real spectrum of a ring (real prime cones/orderings) is a topological space; "gluing" suggests a sheaf/covering argument: the real spectrum of the coordinate ring of the orbit space is obtained by gluing real spectra of chart rings. This is like: M_6 is covered by finitely many "charts" (from catalog representatives), each chart being a semi-algebraic set parametrized by the catalog family parameters; G1 establishes that the real spectrum of the relevant coordinate ring is covered/glued by these charts — i.e., a completeness-of-coverage statement within the declared region.

So the logic: G2 (Candidate Representation Bridge) says "every candidate quadruple is equivalent to one built from catalog representatives" — this is exactly a coverage statement, and it's conditional on G1 because G1's real spectrum gluing provides the coverage. Once G1 is discharged (unconditionally), G2 becomes unconditional: the bridge from "arbitrary candidate" to "catalog representative + gauge transport" no longer depends on an unproven assumption.

Now the three questions in detail:

**Q1: The exact quotient map.**

I should describe:
- The ambient space: A^N_ℂ (or the torus (C*)^m × A^k) with coordinates: the entries of the quadruple (H^{(2)}, H^{(3)}, H^{(4)}, H^{(5)})? Or phases θ_ij^{(k)}. The ideal I_55: generated by 55 explicit polynomial relations — presumably the MUB compatibility relations (|⟨h_i^{(a)}, h_j^{(b)}⟩|² = 1/6) expressed as polynomials in the phase variables z = e^{iθ} and their conjugates, plus Hadamard orthogonality relations, restricted to the ansatz. Since it's called "ZeroRel" — the variety where the relations vanish.

Hmm, "TargetA7ZeroRelVariety" — "Target A7": the target of the program is A7 = a complete set of 7 MUBs? Or "A7" is an algebraic structure (A_7 the alternating group? Coxeter group A_7?). Hmm. Could be: the "A7" is the 7th basis (the target to construct). "ZeroRel variety": the variety on which the defining relations of the target vanish. So V(I_55) = locus where the 55 relations (obstruction relations?) vanish — the candidate locus.

Alternatively, in these formal-verification MUB programs (this looks like it could be from a specific research program — possibly the "MUB(6) program" with gaps G1–G5, SDP witnesses, curvature walls — this resembles a synthetic/constructed scenario), the details are internally defined. I should answer with mathematically coherent content consistent with the given context, being careful to hedge on specifics I can't know (like the exact 55 generators) while giving the precise structural description.

Actually, the instruction says "Provide precise algebraic, geometric, and formal Lean 4 insights." So I should construct a coherent, precise mathematical account. Since this is a hypothetical/internal program, I'll describe the quotient map in standard, defensible terms:

Setup: Let the candidate space be the set of ordered quadruples of 6×6 unit-modulus matrices (H_1,...,H_4) — hmm, or maybe the quadruple is (H_2,...,H_5) with H_1 = I (standard basis fixed by dephasing the first basis). Actually with 7 bases: fix B_1 = standard; then B_2,...,B_7 are Hadamards; a "quadruple" might be 4 of them, e.g., (B_2, B_3, B_4, B_5), and the bridge reduces to catalog representatives for one designated Hadamard (say B_2) since any pair of MUBs is equivalent to (I, H) with H dephased Hadamard, and the catalog of Hadamards gives representatives for B_2; then the quadruple structure constrains the rest.

The known reduction: any pair of MUBs in d=6 ≡ (standard, dephased Hadamard H). Any triple ≡ (I, H, U) with H dephased Hadamard and U unitary with |U_ij|² and MUB conditions. The "candidate quadruple" would be (I, H, U, V). The catalog: representatives of Hadamard equivalence classes (parameterized families). The bridge: every candidate quadruple is gauge-equivalent to one with H in the catalog region.

Quotient map: π: V(I_55) → M_6, [x] = orbit of x under G = (T^5 × T^5) ⋊ (S_6 × S_6).

Concretely: coordinates on V(I_55): for the designated Hadamard H ∈ (S^1)^{36} (entries of modulus 1) — actually as an affine variety: H ∈ (C*)^{36} with relations H H† = 6 I (row orthogonality: 15 relations for pairs of rows, each giving 2 real equations... 6 rows, C(6,2)=15 pairs, each orthogonality Σ_k H_ik conj(H_jk) = 0 — one complex equation each = 30 real; plus moduli |H_ik|=1 — but if we work in the torus (C*)^{36} with |z|=1 that's a real semi-algebraic set). Hmm, "affine variety V(I_55)" — over ℂ? With 55 generators. The MUB relations for a quadruple: |⟨u_i, v_j⟩|² = 1/6 for all i,j across each pair of the 4 Hadamards: 3 pairs × 36 = 108 relations, minus those implied... 55 could be a symmetry-reduced count.

I think the honest approach: describe the quotient map structurally and precisely, noting where the specific counts (55) enter as the declared generating set of the ideal, without inventing false specifics. I can say: I_55 = ⟨f_1,...,f_55⟩ the declared ideal (the 55 zero-relations mechanized in the file), V(I_55) ⊂ A^{N}_ℂ the candidate locus; the group G = (T^5 × T^5) ⋊ (S_6 × S_6) acts by:

(D_L, D_R; σ, τ) · (H^{(2)},...,H^{(5)}) = (D_L P_σ H^{(2)} P_τ D_R, ... gauge-transported partners...)

Hmm wait — the torus T^5 × T^5: row-rephasing torus T^5 = {diag(1, e^{iθ_2},...,e^{iθ_6})} (first row anchored by dephasing) and column-rephasing torus T^5 similarly. These act on the designated Hadamard H: H ↦ D_L H D_R. But as computed, this doesn't preserve dephased form unless compensated. In the orbit-space picture, we don't need to preserve the dephased slice: V(I_55) is the pre-dephased variety (all rephasings allowed), and M_6 is the orbit space; the "dephased orbit space" name comes from the fact that each orbit has a dephased representative (a slice), so M_6 ≅ dephased slice / residual discrete symmetry. The residual symmetry on the dephased slice: permutations combined with re-dephasing — the "Hadamard equivalence" restricted: for dephased H, H', H ~ H' iff H' = P_σ H P_τ dephased — the action of S_6 × S_6 on the slice is: (σ,τ)·H := dephase(P_σ H P_τ). This is a well-defined action of S_6 × S_6 on the dephased slice (since dephasing is a canonical retraction). And the torus part acts trivially on the slice but is needed to describe the full pre-slice variety. So:

M_6 = V(I_55)/G ≅ S_slice / (S_6 × S_6) where S_slice = V(I_55) ∩ {dephased} — provided every orbit meets the slice (dephasing lemma: yes, since entries are unit modulus, first row/column phases can always be gauged away; the subtlety: the torus action must be free/transitive enough — the dephasing map δ: V(I_55) → S_slice, δ(x) = D_L(x) x D_R(x), is a morphism (where phases are extracted via entries: e^{iα_j} = x_{1j}, etc. — algebraic since we can use the entries themselves as the phase units: D_R = diag(conj(x_{1j})) — polynomial in x and conj(x), i.e., a regular map on the real points / or on the ℂ-points with conjugates as extra coordinates).

So the exact quotient map: π = q ∘ δ where δ is the dephasing retraction and q: S_slice → S_slice/(S_6 × S_6) is the quotient by the residual finite group. Or intrinsically: π: V(I_55) → M_6, x ↦ G·x, with M_6 given the quotient topology/structure sheaf (or as a real semi-algebraic quotient / invariant-theoretic quotient Spec R^G where R = ℝ[V(I_55)] — since G has a non-reductive torus part, the invariant ring might be small; better: use the slice description).

Hmm — actually for the formal Lean development, the cleanest: M_6 as a quotient type (orbit relation), with the atlas providing charts. The "CurvatureWallCertifiedAtlas" — an atlas: a finite family of charts (U_c, φ_c) indexed by catalog representatives c, each with certified obstruction Ψ² > 0 on U_c. G1's real spectrum gluing: the real spectrum of the coordinate ring of M_6 (or of the relevant open/region) is covered by the charts — i.e., every real point of the declared region lies in some chart's domain.

Let me now also address: "How does the Candidate Representation Bridge become unconditional once G1/R7 is discharged?" — The bridge (G2) states: every candidate quadruple (point of V(I_55)(ℝ) in the declared region) is G-equivalent to one built from a catalog representative — i.e., lies in the G-saturation of the atlas charts. Conditional discharge: the Lean theorem is of the form `theorem bridge : G1_hypothesis → CandidateRepresentation` — i.e., an implication whose hypothesis is the G1 statement (real spectrum gluing). Once G1 is discharged (proved unconditionally as a theorem in the development, or derived from previously discharged results), the implication can be composed: `G2_unconditional := G2_conditional (G1_discharged)` — modus ponens — and the bridge no longer carries a hypothesis. The key formal point: the dependency graph must be acyclic — G1's proof must not use G2 (no circularity). The question asks to spell out the theorem spec that connects them without circular dependency.

**Q2: PSD preservation under continuous gauge transport.**

The setting: Gramian block matrices — for a candidate configuration, the Gram matrix of the stacked vectors (e.g., the 24×24 or 36×36 Gram matrix of the quadruple's vectors, or block matrices G_{ab} = H_a† H_b with entries ⟨u_i^{(a)}, u_j^{(b)}⟩). PSD: Gram matrices are always PSD (they're Gram matrices of vectors — PSD by definition: v† G v = ||Σ...||² ≥ 0). The relevant PSD objects: the Gramian blocks of the SDP relaxation — the MUB existence problem can be relaxed to an SDP (as in the work on "SDP relaxations of MUB problems", e.g., by D. A. et al. or the "MUB semidefinite relaxation" literature). The dual SDP witness matrices W = L D L† — a Cholesky-type factorization: W = L D L† with D diagonal ≥ 0 (or D PSD) certifies W ⪰ 0 (PSD), since congruence preserves PSD: for any v, v† W v = (L†v)† D (L†v) ≥ 0 if D ⪰ 0. So W ⪰ 0 iff (given L invertible) D ⪰ 0.

Gauge transport: along each Hadamard orbit, the group element g = (D_L, D_R; σ, τ) acts; the Gramian blocks transform by congruence: G_{ab} ↦ (D_L P_σ) G_{ab} (D_L P_σ)† or similar — i.e., G ↦ M G M† with M unitary/monomial. Congruence by invertible matrices preserves PSD: x†(M G M†)x = (M†x)† G (M†x) ≥ 0. So PSD is preserved exactly, not just approximately. The subtlety: "continuous gauge transport" — the orbit is connected (torus part is connected; the S_6 × S_6 part is finite, so orbits have up to (6!)² components... hmm, actually the group G has identity component T^5 × T^5, and the orbit of a point under G is a finite union of torus orbits). "Continuous gauge transport along each Hadamard orbit": transporting the witness W along a continuous path g(t) in the
```
</details>


---

### Model: Super Bunny Alpha

- **Status:** TRUNCATED (finish_reason: `length`, content: null)
- **Latency:** 163.25s | **Tokens:** 8804
- **Notice:** Call exhausted token limit during internal reasoning; no completion content was emitted.

<details><summary>Truncated Reasoning Trace (31231 chars)</summary>

```
We need craft answer. Need analyze request/context. Need likely explain exact quotient map affine variety V(I55) to dephased orbit space M6 = V(I55)/(T5 x T5 ⋊ S6 x S6) perhaps notation malformed. Need be careful: V(I55), I_55? Need infer MUB program. Need perhaps identify issue: cannot honestly detail without definitions. Need reason. They want theorem specification connecting G1 real spectrum gluing to Lean file. Need mention conditional becomes unconditional once G1/R7 discharged, but not claim MUB. Need explain PSD preservation under continuous gauge transport along Hadamard orbit, dual SDP witness W=L D L^\dagger. Need distinguish PSD under congruence/unitary transport versus active gauge? Need quotient quotient group action and invariant polynomials/symmetric product quotient. Exact quotient map q.

Let's parse terminology. MUB(6) MUB bases? I_55 perhaps ideal for moment polytope? 55 = n choose 2? n=6, 15+? 55 perhaps bases/order? M_6. Group T^5 x T^5 \rtimes S_6 x S_6 perhaps T^5 × T^5 ⋊ (S6 × S6), dephased orbit. Candidate quadruple built catalog reps. Curvature wall Psi²>0 certified. Need explain bridge.

Potential trap: The requested conclusion may be mathematically invalid. Quotient of V(I55) by group? Exact map needs invariant/descended ideal. If V affine closed and G compact, categorical affine quotient Spec coordinate ring invariants may only be variety, not necessarily set quotient if invariant ring not finitely generated? For compact reductive group finite generated yes. But group T^5 x T^5 ⋊ S6xS6 possibly semidirect? Need exact action. They wrote "(T^5 x T^5 rtimes S_6 x S_6)" missing "\rtimes". Could mean \((T^5 \times T^5)\rtimes(S_6 \times S_6)\). Need spell.

"Dephased orbit space M_6 = V(I_55) / (T^5 x T^5 rtimes S_6 x S_6)." If V(I55) is union of orbits? q(x)=G·x. But exact group action and map. Need not claim quotient is affine unless closed orbits. The orbits under compact group in affine variety may not be closed unless? Compact group orbit not always closed in arbitrary affine? For complex reductive G closed orbits theorem, compact real torus/wreath? likely. But quotient coordinate ring A^G and map finite if all orbits closed and finite. However T^5 factors might act with stabilizers.

Need understand Gramian block matrices and dual SDP witness matrices W=L D L^\dag. PSD under continuous gauge transport along each Hadamard orbit. They may envision gauge transport U matrices. Need formulate: If block Gramian B and witness W are unitarily conjugated B' = U B U^\dagger, PSD iff eigenvalues nonnegative. But quotient generally identifies points under unitary orbit. If gauge is phase/diagonal, B'(θ)=D_g B D_g^*, W similarly. Duality pairing tr(BW) invariant if simultaneous transport. If a factor/reference L also transforms, W=L D L^\dag where L is isometry and D⪰0, then automatically PSD. But under gauge, L' = U L (if columns change), D remains, W'=U L D L^\dag U^\dag. If D diagonal and certificate positivity d_i≥0. Gramian B maybe L^\dag L? Then B'=U L^\dag L U^\dag. But continuous Hadamard orbit gauge not necessarily unitary on matrix block; perhaps local diffeomorphism and congruence by Jacobian. General PSD covariance under congruence: B'=J B J^T with invertible real J; W'=? If dual witness perhaps inverse congruence J^{-\top} W J^{-1}. Both PSD. If W=L D L^\dag form uses L as factor matrix, L maybe Cholesky, changes via unitary only. Need explain alternatives and not conflate.

Positive semidefiniteness is preserved by unitary similarity/congruence, not arbitrary "continuous gauge transport." A continuous path alone does not preserve PSD. This may be key strict epistemic answer. User asks "How is ... preserved under continuous gauge transport along each Hadamard orbit?" We must state only if transport is implemented by congruence/unitary map preserving Hermitian cone, and same operation on primal/dual. Mere continuity doesn't. Need perhaps correct premise.

Third: explicit Lean theorem specification connecting real spectrum gluing of G1 directly to TargetA7... without circular dependencies, firewall. We cannot edit file or know exact definitions. Can suggest theorem declaration/interface. Need perhaps provide Lean 4 skeleton using types. Need avoid unsupported exact theorem name. They mention file and declaration. We can write spec theorem e.g.:

structure CandidateBridgeResult where
  /-- ... -/
  spectrumGluing : ...
  catalogCompleteness : ...
  quotientCorrect : ...
  obstruction : ∀ c ∈ candidates, 0 < c.psiSq
  firewall : ...

theorem curvatureWall_of_realSpectrumGluing
    (hG1 : RealSpectrumGluing R7) :
    ∀ q : CandidateQuadruple, 0 < q.psiSq := by
  exact TargetA7ZeroRelVariety.CurvatureWallCertifiedAtlas
    (bridge := CandidateRepresentationBridge.fromSpectrumGluing hG1)

But they say mechanized in TargetA7ZeroRelVariary.lean (CurvatureWallCertifiedAtlas), establishing every candidate quadruple built from catalog reps. Need likely actual theorem signature unknown. We can define abstract interface and exact construction. Ensure no circular dependencies: G1 module imported by bridge/target, but target doesn't import G1? Better architecture:
- `G1Spectrum.lean`: proves real spectrum gluing from R7.
- `CandidateRepresentationBridge.lean`: imports `G1Spectrum`, theorem raw seed space = V(I55), all candidate quadruples arise, map quotient and property equivariance.
- `TargetA7ZeroRelVariety.lean`: maybe generic analytic obstruction theorem, imports bridge? User asks connects G1 directly to Target... Could have `G1ToA7.lean` imports both and applies.
No circularity: G1 should not import A7 or bridge; A7 should not import G1; final theorem imports both. Or if Target file currently conditional on bridge, bridge theorem takes G1 proof. Need state.

Maybe target theorem itself is a structure taking `CandidateRepresentationBridge` parameter. Once G1 discharged, theorem produces bridge and applies. If proof irrelevance allows no modification? In Lean theorem is universally quantified over hypothesis; instantiate.

Need distinguish G1 "DISCHARGED_CONDITIONAL on G1" and "G1/R7" perhaps R7 assumptions. An implication theorem \(A7 \leftarrow G1/R7\) only becomes unconditional relative to foundational/ambient axioms, not absolute. In strict governance, say unconditional in kernel under those assumptions, not blanket unconditional. If G1/R7 has residual assumptions, retain. We should mention. They ask "becomes unconditional once G1/R7 is discharged" so answer yes logically: if hG1 is closed/theorem with no open hypotheses, specialization removes condition. But no conclusion about MUB(6) max count or &lt;=3.

Need detail exact quotient map. Need define V(I55) likely complex affine. Let K=C. \(V_{55}(I):= \operatorname{Spec}_{\mathbb C} A_{55}\), A=C[x]/I. Group \(G=(U(1)^5\times U(1)^5)\rtimes(S_6\times S_6)\). Since complex points, T^5=(U(1))^5 = (\mathbb C^\times)^5 perhaps acts. Dephased: projective/dephasing equivalence mod U(1) global. Wait group is T5×T5 not U1^6. 6x6 MUBs. Dephasing usually mod global phase gives torus of dim 5. Two MUBs =&gt; T^5×T^5. Permutations within each basis: S6×S6. Semidirect product \((T^5\times T^5)\rtimes(S_6\times S_6)\). Good.

\(V(I_{55})\) maybe equations independent of phases? 55? The exact quotient action:
\[
((\lambda,\mu),(\sigma,\tau))\cdot X = P_\sigma X P_\tau^\top \,\operatorname{diag}(\lambda_1\dots\lambda_5,1) \operatorname{diag}(\mu_1\dots\mu_5,1)
\]
or order. But dephased means perhaps representatives with one fixed entry/row, so residual T5; could phase columns and rows? We can give generic formula contingent on convention. Need be exact. If each MUB is 6x6 unitary, row and column permutations, and dephasing removes one phase per unitary. The residual torus action is diagonal left and right:
\(D_{\bar\lambda} X D_{\bar\mu}\) with \(\lambda_6=\mu_6=1\). Depending left/right orientation. Then semidirect S6×S6. Formula:
\( [(\lambda,\mu),(\sigma,\tau)]\cdot X =
D_{\lambda} P_\sigma X P_\tau^T D_{\mu}^{-1}\)
or Dλ X Dμ? If MUB has row and column gauges, each side. The action must be specified. The exact quotient map is q(X)=[X]. If coordinate ring invariants:
\[
q^\#:\mathbb C[V/G] \to A,\quad [f]\mapsto f,\quad
\mathbb C[V/G]\simeq A^G
\]
and \(q:\operatorname{Spec}A\to\operatorname{Spec}A^G\), contravariant. On k-points q_K([x])=[x]. The "exact quotient" also requires map induced by inclusion invariants \(A^G \hookrightarrow A\) and equality of orbit fibers. This is exact iff closed-orbit/finite quotient conditions. We need state that. They ask exact map; can explain q and q*. Need perhaps define the dephased orbit space as set quotient, no need affine quotient. But precise formalization.

Candidate representation bridge: G1 real spectrum gluing likely proves all real spectrum points/candidate quadruples admit representatives in V(I55), or catalog exhaustive. Need articulate:
- G1 gluing is not just spectral equations; needs representation theorem: each glued branch/real cell has a complex point in V(I55), gauge equivalent to one represented by catalog data.
- map `rep : glued spectrum -> V(I55)` with:
  1. equations `idealMembership`
  2. fiber surjectivity: any candidate quadruple's seed \(x\) arises as `rep y` after G action, or candidate orbits correspond.
  3. quotient representative: if spectrum identifies under group, reps do too.
  4. obstruction function \(Ψ^2\) invariant/equivariant: Ψ²(g·x)=Ψ²(x).
Then bridge yields \(\forall y, 0&lt;Ψ²(rep y)\), and A7 applies.
"every candidate quadruple built from declared catalog representatives" is not enough for all points of V(I55) unless G1 establishes exhaustive coverage and closure. Need make this firewall/next test. The bridge's burden is surjective/exhaustive.

Could define candidate quadruple c = \((x_1,x_2,x_3,x_4)\)? Gramian blocks. They may have matrices. Need not know exact definitions. Could use abstract `Quadruple`. On V(I55)? Maybe candidate quadruple built from reps, not points. We can say exact.

PSD under gauge:
Let \(B\) Hermitian Gramian and \(W\) Hermitian SDP witness. For \(g\) represented by unitary \(U_g\) or block diagonal \(D_g\):
\[
B_g=U_g B U_g^\dagger,\quad W_g=U_g W U_g^\dagger.
\]
If all block matrices are transformed simultaneously by \(\mathcal U_g=\oplus_j U_{g,j}\), then:
\[
B_g^*B_g = \mathcal U_g B^*B \mathcal U_g^\dagger
\]
and
\[
W_g=L_g D L_g^\dagger,\quad L_g=\mathcal U_g L,
\]
so eigenvalues unchanged. Or if Gramian \(B=L^\dag L\). If each block perhaps B = B0^* B0. Thus PSD.

For real congruence under local chart \(J\):
\[
B_g=J_g^*B J_g
\]
and dual \(W_g=J_g^{-\dagger} W J_g^{-1}\), pairing:
\[
\langle B,W\rangle = \operatorname{tr}(BW)
\]
is invariant:
check. If B' = J^* B J; W'=J^{-*} W J^{-1}. Then tr(B'W') = tr(J^* B J J^{-*} W J^{-1}) = tr(J^* B J (J^*)^{-1} W J^{-1}); \(J J^{-*}=I\), leaving J^* B W J^{-1}; trace=tr(BW). Good. Both PSD if B,W PSD. If W=L D L†, congruence transform factor \(L' = L J^\dagger?\):
Want W'=J^{-*} W J^{-1}. If W=L D L†, choose L'=J^{-*} L? Then L' D L'† = J^{-*} L D L† (J^{-*})†. \((J^{-*})† = J^{-1}\). yes. So W'=(J^{-*}L)D(J^{-*}L)†. If J real, J^{-T} L. For B'=J^* B J if B perhaps L†L? choose L'=J^*L. Fine. Under unitary U:
W'=U W U†, L'=U L.
Thus continuous path U(t) or J(t) preserves at each t. A path in GL/ U with derivative etc. "continuous gauge transport along each Hadamard orbit" likely group maps unitary. But the quotient may identify matrices under nonunitary row/column gauges? Row/column diagonal unitary, yes. Permutations are unitary. So U_g is unitary. If real block Gramian perhaps not complex? Dagger handles.

Important nuance: SDP witness W = L D L^\dag. If L changes by arbitrary gauge not preserving inner product, factor doesn't remain isometry. But if U unitary, yes. If gauge acts on vectors, U. If arbitrary differentiable gauge on coefficient coordinates, use congruence and dual inverse. If path only continuous \(g(t)\), each g(t) unitary means all t. If only orbit map continuous and endpoint gauge not unitary, no general preservation. We should explicitly reject general assertion. Need perhaps say PSD is closed but continuity only means if positive definite at t0, nearby remains positive for sufficiently small t, whereas semidefinite may develop negative eigenvalues? Eigenvalues continuous; at t0 zeros could turn negative, so not preserved. If strictly positive definite, there is local neighborhood but not entire path unless controlled. Here group unitary guarantees global. State this.

W=L D L† automatically PSD if D diagonal with \(d_i≥0\), independent of L (any L), actually yes, not need L isometry. The factorization is sufficient. Under U, D unchanged. If D entries real and L complex. Dual SDP witness might be "W" and Gramian blocks. Pairing invariance. If D is from equality constraints? Fine.

The quotient action at block level: Candidate data might consist matrices \(A_i\) and Gramian. Let group g induced blockdiag. Define pullback. Need invariance means q∘g=q, so any function on quotient is G-invariant. Curvature \(\Psi²\) needs \(G\)-invariance. If obstruction theorem works on raw reps, transport gives orbit-wide result. Quotient map exact and PSD property descends because PSD is orbit-invariant under unitary orbit. But to define property on quotient, use existential/conjunction:
\[
[B]\in \mathrm{PSD} \iff U_g B U_g^\dagger\succeq0\ \forall g
\]
which holds if one rep. Or choice-independent. Dual pair.

Need address affine quotient nuance:
- Set quotient \(V/\!/G := \operatorname{Spec} A^G\).
- Natural map q. If orbits not closed or fibers not exactly orbits, q isn't "exact orbit map." For a compact linear algebraic group, closed orbit theorem often all orbits closed? Let's inspect. For complex reductive group acting on affine variety, closed orbits theorem maybe all orbits closed if G connected? Borel theorem. T^5 connected, finite permutations; likely closed. But if V reducible/non-normal? Closed orbit theorem may hold for affine schemes and complex reductive G? Need not overclaim. Could say q is set-theoretic orbit map by definition. It descends to affine categorical quotient only under verified hypotheses; G1/R7 or bridge must certify closedness/finite fibers. The group compact over real, but over C \(T=(G_m)^5\) not compact. Orbits may not be closed. If M6 notation explicitly set quotient, q exact by definition. If formalizing as affine variety, need `quotientMap` with equality fibers. The next test needed is formal orbit-closure/fiber theorem. Since user asks "exact quotient map from affine variety to dephased orbit space", likely expect formal map. We can state coordinate ideal and saturation. Exact quotient:
\[
I_G = \{ f\in A : G\cdot f=f\},\quad q: V(I)\to V(I_G)
\]
since \(A^G = A/I_G\) when I radical (Hilbert basis finite gen for torus⋊finite? yes invariants finitely generated for reductive linear algebraic G; semidirect finite extension). But is kernel of A→A^G equal ideal generated by f-u f? Under reductivity and exactness of invariants? For affine algebraic action, kernel map A→A^G may include orbit closure ideal. Reynolds if linearly reductive gives A→A^G surjective and kernel generated by differences perhaps. Torus ⋊ finite is linearly reductive if finite extension, yes. Could say \(I_G=\ker(A\to A^G)\), and no simplistic generator claim unless action assumptions certified. If all orbits closed, V(I_G)=set quotient. Formal q*: A^G→A.

"Exact quotient map" might mean:
\[
q: V(I_{55}) \to V(I_{55}^{G}),\quad p\mapsto [p],
\]
with \(I_{55}^{G} = \sqrt{\langle g f-f : f\in\mathbb C[x],g\in G\rangle}\) and equality fibers \(q^{-1}(q(p))=G\cdot p\). Need be cautious semidirect group.

Can detail invariant ring under phases/permutations if V(I55) defined? Maybe they expect exact formula. Could derive action in entries. Let X=(x_{ij}) for candidate? Two matrices maybe a quadruple. If there are two 6x6 MUB matrices U,V, group action separately:
\[
((\lambda,\mu),(\sigma,\tau))\cdot (U_1,U_2)
=
(D_\lambda P_\sigma U_1 P_\tau^\top D_{\mu_1}^{-1}, ...?)
\]
But group T5×T5 likely dephasing one MUB? Let's understand notation M6 = V(I55)/(T5 x T5 ⋊ S6 x S6). Maybe \(V(I_{55})\) consists 6x6 MUB? 55 perhaps degree count. M6 maybe moduli for a single MUB pair? Group T^5×T^5 and S6×S6. Dephased orbit of ordered pair? In MUB classification, two orthonormal bases (U,V), relative phases. Dephase V? Permutations both. A "Hadamard orbit" perhaps candidate basis and Gramian.

Could be G1 relates "real spectrum gluing" to 55 charts? I_55 maybe vanishing ideal of "MUB(6) seed variety"? They give M_6 explicitly. We can avoid pretending unknown action by stipulate using program's phase conventions. But task asks exact. We need provide a canonical formula, with orientation clearly defined. We can define the action ourselves in symbols and say if source file uses transpose/inverse, adjust convention consistently; mathematically same. This is an exact formula once conventions fixed. Need not know coordinate equations. The group action is central.

Let's formulate: Let \(U_1,U_2\) be the two 6×6 component matrices of a point (if `V(I55)` is represented by quadruple, apply componentwise). For \(\lambda,\mu\in\mathbb C^5\), extend \(\bar\lambda=(\lambda_1,\dots,\lambda_5,1)\), etc. Let \(D(\lambda)=\mathrm{diag}(\bar\lambda)\), \(P_\sigma\) permutation matrix satisfying \((P_\sigma z)_i=z_{\sigma(i)}\). Define:
\[
((\lambda,\mu),(\sigma,\tau))\cdot(U_1,U_2)
=\left(D(\lambda)P_\sigma U_1P_\tau^{\mathsf T}D(\mu^{-1}),
D(\lambda)P_\sigma U_2P_\tau^{\mathsf T}D(\mu^{-1})\right)
\]
But if two T5 correspond one per basis, should be λ for U1 and μ for U2, not both applied each. Maybe "T5 x T5" likely phases of two bases, so action:
\[
U_1\mapsto D_\lambda P_{\sigma_1} U_1 P_{\tau_1}^T,\quad
U_2\mapsto D_\mu P_{\sigma_2}U_2P_{\tau_2}^T
\]
with S6×S6. Dephased each has one coordinate fixed, so no inverse needed. Better.

What does dephasing mean: Fix last row/column to standard by diagonal unitaries. Residual action is right diagonal phase. If point is dephased, left residual might trivial; why T5×T5 then? Could be two matrices each has 5 relative column phases, hence T5×T5. Permutations each. Formula:
\[
((\lambda,\mu),(\sigma,\tau))\cdot (U,V)
=(D(\lambda)P_\sigma U P_\tau^T,\; D(\mu)P_\sigma V P_\tau^T)
\]
if same permutation pair applies each? S6×S6 can separately permute U and V. The notation likely `(T^5 x T^5) rtimes S_6 x S_6`: first T5 for? two MUBs, S6 x S6 for bases? Could be. We can phrase generally: on component j, \(X_j\mapsto D_j(a_j)P_{\sigma_j}X_jP_{\tau_j}^T\), with \(a_1=\lambda,a_2=\mu,(\sigma_1,\sigma_2)=(\sigma,\tau)\). This is exact and flexible. Fix last phase 1. If actual convention uses inverse, replacing a_j by a_j^-1 is coordinate reparametrization. State must match G1's action lemma; quotient object only meaningful once convention fixed. That is perhaps best.

But "affine variety V(I55)" singular matrix? We can say if a point is quadruple \(x=(X^{(1)},...,X^{(r)})\), action is componentwise. That gives exact map without relying on representation.

Semidirect product action: finite S6×S6 normalizes torus, possibly permutes coordinates and swaps components. Define:
\[
(a,s)\cdot x = a\,(s\cdot x)
\]
and multiplication \((a,s)(b,t)=(a\,s\cdot b,st)\). Need write.

At matrix level phase action is unitary over R/unitary points. Over complex, Dλ isn't unitary unless |λ|=1, but on real/unitary locus yes. T^5 as real torus. Formal Lean likely uses `Complex` phases constrained norm=1 or `Unitary` structures. Mention distinction. The affine variety likely complex. Group as real compact torus acts; algebraic T5=(C*)^5 complexifies. Formal q in Lean may be on real spectrum or complex points. Need be precise.

"real spectrum gluing of G1" suggests Lean types maybe `RealSpectrum`. We can propose structure.

Need not claim actual implementation. State cannot infer source definitions; here is exact theorem contract. The user asks explicit theorem specification in Lean 4. We can provide pseudocode/valid-ish Lean 4. Need make it syntactically plausible. Avoid fake `TargetA7ZeroRelVariety` namespace? The file likely namespace. We can write a module skeleton with abstract variables and theorem type. Need perhaps use theorem `CurvatureWallCertifiedAtlas` name conflicts: they say declaration. Could have:
```
theorem curvatureWall_of_g1
    (h : G1.RealSpectrumGluing R7) :
    CandidateRepresentationBridge := ...
```
Then:
```
theorem g1_curvature_wall
    (hG1 : RealSpectrumGluing R7) :
    ∀ q, q ∈ declaredCatalog → 0 < q.psiSq := by
  have hBridge := CandidateRepresentationBridge.mk ... hG1
  exact curvatureWallCertifiedAtlas hBridge
```
But "connects ... directly to TargetA7...lean" maybe theorem in final module imports file:
```
import TargetA7ZeroRelVariary
import G1RealSpectrumGluing
open ...
theorem R7_g1_to_A7 (hG1...) ...
```
No circular dependencies.

Need include firewall as proposition? A Lean theorem cannot prove negative claim "NOT MUB(6)=3" unless define a restricted proposition and prove it from context, which likely not possible. The firewall should be documentation and theorem scope, not a hypothesis. We can encode:
```
/-- Scope: ... This result is not an upper-bound theorem. -/
structure StatedRegion where ...
```
and result type has only `StatedRegion`. No definitions of global max. Add theorem:
```
theorem noGlobalBoundAuthority :
  ¬ (∀ ... global property ...) := ...
```
But cannot prove no implication in logic generally unless definitions. Better governance: make module no `Mub6Max` or `Mub6Le` constants imported; theorem's conclusion only obstruction on stated region. The string firewall can be `axiom`? An `axiom Firewall : ...` undesirable. Could encode a typed erased scope:
```
structure A7Scope where
  seed : V I55
  catalog ...
```
and no global count. Comments. "respecting firewall: 'NOT MUB...'" means answer must explicitly state. We must never say MUB=3 or <=3; can repeat their literal firewall? Developer says MUST NEVER claim or imply MUB(6)=3 or MUB(6)<=3. User asks respecting phrase `stated region only; mints no authority`; we can state exact phrase as prohibition. Is repeating "NOT MUB(6)=3" itself not claiming equality. Fine, but perhaps developer says never claim or imply, negation is okay. Need avoid hype verbs listed. Don't use "proves", "guarantees", "mathematically verifies", "fundamentally", "true intelligence", "impossible", "universal", "flawless", "perfectly", "clearly", "obviously", "simply", "merely", "weaponized". Also avoid "proved/proves" in Lean discussion? "proof" is okay, banned verb 'proves' exactly maybe avoid. We can say theorem. "established" maybe okay. Avoid "guarantee". "certified" is in declaration and context; allowed. Need use careful.

Need for each gap analysis always include four bullets. This is G2 analysis. We must include:
- What it supports
- What it does not support
- Narrowest defensible claim
- Next test needed
Could structure at end and perhaps throughout. Also perhaps S2 means 5 gaps, but only G2 task. We apply to G2.

Need discuss exact quotient map more rigorously.

Let's set field and rings:
- Let \(A_{55}:=\mathbb C[x_1,\ldots,x_N]/I_{55}\). If Lean is real, \(\mathbb R\) analog.
- \(X=V(I_{55})=\operatorname{Spec}A_{55}\).
- \(G_\mathbb C=(\mathbb G_m^5\times\mathbb G_m^5)\rtimes(S_6\times S_6)\). On real points, T phases \(S^1\).
- On coordinates, action. Dephased gauges: \(\bar a=(a,1)\), \(\bar b=(b,1)\). If matrices \(X^{(1)},X^{(2)}\):
\[
\rho(a,b;\sigma,\tau)(X^{(j)})
= D(a_j) P_{\sigma_j} X^{(j)}P_{\tau_j}^{T}
\]
where \((a_1,a_2)=(a,b)\), \((σ_1,σ_2)=(σ,τ)\). If program uses right gauges, use \(P X D\), but need exact source convention. Maybe choose likely action. We can state this formula *is* convention; the source theorem must instantiate exactly it. No ambiguity after definitions.

But if dephasing means quotient by `T^5 x T^5` and each MUB's global phase removed, perhaps each component gets one T5. This formula works.

- Semidirect: \(S_6×S_6\) may act by permuting phase coordinates; \(\rho(h,k)x=\rho_T(h)\rho_G(k)x\). Composition:
\[
\rho((a,b),(\sigma,\tau))\rho((a',b'),(\sigma',\tau')) =
\rho((a,b)(\sigma,\tau)\cdot(a',b'),(\sigma\sigma',\tau\tau'))
\]
This ensures semidirect.

- Dephased orbit:
\[
M_6(k)=X(k)/G(k),\quad q_k(x)=[x].
\]
If "variety quotient":
\[
A_{55}^G=\{f∈A: f(gx)=f(x)\}, \quad
M_6^{aff}=\operatorname{Spec}A_{55}^G,
\]
and
\[
q^\#:A_{55}^G\hookrightarrow A_{55}, f\mapsto f,\quad M_6^{aff}\to X.
\]
- `exact` if \(q(x)=q(y)\iff y\in Gx\), and q surjective. This follows definition on closed orbits; for categorical quotient need orbit closure. State a Lean theorem `quotientMap_eq_iff_orbit` with membership relation. This is likely next formal test.

- If quotient is by pseudo-reflection? finite? Could formal exact finite quotient. Need not.

"Every candidate quadruple built from declared catalog representatives" q? Perhaps candidate catalog is finite reps of orbits. To conclude every orbit in M6, need catalog orbits cover X/G. G1 real spectrum gluing may provide this. The bridge:
  - Let \(\Sigma_R\) glued real spectrum.
  - `glueRep : SigmaReal -> X` maybe.
  - `orbit_surj : ∀ x, ∃ y, q y = q x ∧ CatalogRep?`? Or if candidate quadruple is in catalog, A7 gives each.
  - Need a theorem:
```
theorem bridge (h : RealSpectrumGluing R7) :
  ∀ x : X, ∃ c : CatalogCandidate,
    QuotientCandidate c = q x ∧ 0 < c.psi2
```
But if A7 obstruction is then for c. Better separation:
```
CandidateRepresentationBridge:
  (∀ c ∈ catalog, 0 < psi2 c) →
  (∀ x ∈ X, 0 < psi2 x)
```
with invariance and coverage.
A7 provides first, G1 second. Direct final theorem.

Maybe G1 is "real spectrum gluing" and bridge map. We can define:
```
structure RepresentationBridge where
  toImage : RealSpectrum → X
  coverage : ∀ x, ∃ z, q (toImage z)=q x
  respectsGluing : ...
  psiEq : ∀ z, psi2 (toImage z)=...
```
Then A7:
```
CurvatureWallCertifiedAtlas :
  RepresentationBridge → ∀ c : CatalogQuadruple, c.declared → 0 < c.psi2
```
But if coverage maps spectrum to catalog candidates, not arbitrary X. Maybe:
```
structure CandidateRepresentationBridge where
  encode : X → CandidateQuadruple
  encode_eq_on_orbits : ...
  declared : ∀ x, ...
  psi2_eq : ...
```
Then A7's theorem can be applied.

Let's articulate two possible directions:
1. G1 yields map from every relevant candidate orbit to a catalog representative: \(\rho:\mathcal C\to \mathrm{Cat}\), \(\rho(c)=c'\), q(c)=q(c'). It is not enough to map real spectrum points to V; bridge needs `orbit coverage`.
2. A7 says obstruction for catalog c'. Then invariance yields for c.

This is likely more exact. Let \(\mathcal C\) domain of all candidate quadruples satisfying G1. For each c, there is catalog rep r(c) and \(g(c)\) with \(c=g(c)\cdot r(c)\). Then:
\[
0<Ψ²(r(c))=Ψ²(c).
\]
If q is quotient, equality q(c)=q(r) means c and r same orbit under assumptions. That's bridge. `q` maybe seed quotient, not candidate quadruple quotient.

Need connect "real spectrum gluing" directly. G1 likely shows cells correspond to catalog. The bridge can be formalized as:
```
def orbitRepresentative (c : Candidate) : CatalogRep :=
  RealSpectrumGluing.representative hG1 c.spectrum

theorem orbitRepresentative_eq (c) :
  q c = q (orbitRepresentative hG1 c) := ...
```
But if q to M6, both are points. Then final:
```
theorem obstruction_on_g1_region
 (hG1) (c) (hc : c.property hG1) :
  0 < c.psiSq :=
  CurvatureWallCertifiedAtlas hG1.repBridge hc
```

Need mention proof dependencies:
Layer 0: `R7Axioms` (whatever R7) and algebraic foundations.
Layer 1: `G1RealSpectrumGluing`: imports R7 only; conclusion `G1Result`.
Layer 2: `CandidateRepresentationBridge`: imports G1 and seed action; no A7.
Layer 3: `TargetA7ZeroRelVariety`: generic curvature theorem; ideally imports bridge interface but not G1. It has:
```
theorem CurvatureWallCertifiedAtlas
  (B : CandidateRepresentationBridge) :
  ∀ c, c.declared → 0 < c.psi2
```
Layer 4:
`G1A7Final`: imports G1 and A7; constructs B and specializes. No cycles.

If current target file has theorem that already takes bridge. The final theorem:
```
theorem curvatureWall_on_statedRegion
    (hG1 : G1.RealSpectrumGluing R7) :
    ∀ c : CandidateQuadruple,
      c.IsFrom hG1 →
      DeclaredRegion c →
      0 < c.psiSq := by
  let B := CandidateRepresentationBridge.ofG1 hG1
  exact TargetA7ZeroRelVariety.CurvatureWallCertifiedAtlas B
```
If `CurvatureWallCertifiedAtlas` already no bridge argument because it established catalog reps only:
```
exact fun c hc => ... via B
```
We can present both signature alignment. User specifically says "mechanized ... (CurvatureWallCertifiedAtlas), establishing that every candidate quadruple built from declared catalog representatives..." So likely theorem takes no h? It might be unconditional on catalog. Then final adapter:
```
theorem G1R7_to_A7
 (h : RealSpectrumGluing R7) :
 ∀ c, G1Candidate c -> 0 < c.psiSq := by
  have hb := CandidateRepresentationBridge.of_realSpectrumGluing h
  intro c hc
  have hc' := hb.map_to_catalog hc
  exact curvatureWallCertifiedAtlas hc'
```
No circular.

"Once G1/R7 discharged" In Lean, if hG1 becomes theorem:
```
theorem realSpectrumGluing : RealSpectrumGluing R7 := ...
```
then:
```
theorem g1A7 : ... := G1R7_to_A7 realSpectrumGluing
```
No assumptions if R7 discharged. But if file has axioms, theorem is only axiom-relative. Need explicitly call "unconditional in theorem kernel" not absolute. "Unconditional" means no variable hG1 remains. Lean kernel checks dependencies. If R7 remains as axioms, not unconditional. The user says G1/R7 discharged, so assume closed. State.

Could offer code with `noncomputable def`? Need Lean syntax. Let's construct robust pseudo-Lean 4.

First module:
```
import Mathlib.Ring.Finite.Invariants
import G1.RealSpectrumGluing
import M6.SeedVariety
import M6.PhasePermutationAction

namespace M6G2

open M6 Seed

structure CandidateRepresentationBridge where
  rep : CandidateQuadruple → CatalogRepresentative
  declared : ∀ c, IsG1Candidate c → DeclaredRepresentative (rep c)
  orbit_eq : ∀ c, IsG1Candidate c →
    Quotient.liftOn? ...
  psi2_eq : ...
```
Represent quotient equality simply use `OrbitRel`:
```
def SameOrbit (x y : X) : Prop := ∃ g : G, y = ρ g x
```
q equality less computable. Bridge theorem:
```
theorem mk_of_realSpectrumGluing
  (hG1 : RealSpectrumGluing R7) :
  CandidateRepresentationBridge where ...
```
No circular.

PSD:
Maybe in code:
```
def transportBlock (U : ...) (B : Matrix n n ℂ) := U * B * Uᴴ
theorem psd_transport ... := ...
```
Matrix n n ℂ` is PSD if `hB : B.IsHermitian` and `0 ≤ B` in quadratic order. Mathlib matrix PSD APIs uncertain. We can state theorem signatures abstractly to avoid invalid syntax. But "explicit theorem specification in Lean 4" wants precise. We can define own `IsPSD`:
```
def IsPSD (n : Type) (B : Matrix n n ℂ) : Prop :=
  B.IsHermitian ∧ ∀ x : n → ℂ, 0 ≤ dotProduct (star x) (B * x)
```
Syntax uncertain. Better use `Matrix.IsPosDef` APIs? Mathlib has `Matrix.IsPosDef`? I recall definitions in Mathlib:
- `Matrix.IsHermitian`
- `Matrix.IsPosDef` likely `Is
```
</details>


---

## Gap G3: Analytic Variation Enclosures Global Certification

### Model: GLM 5.3

- **Status:** TRUNCATED (finish_reason: `length`, content: null)
- **Latency:** 39.49s | **Tokens:** 8706
- **Notice:** Call exhausted token limit during internal reasoning; no completion content was emitted.

<details><summary>Truncated Reasoning Trace (26691 chars)</summary>

```
Let me carefully parse this task. The user is asking about Gap G3 in a MUB(6) program — this appears to be related to the mutually unbiased bases problem in dimension 6 (the famous problem of whether there exist 3 MUBs in dimension 6, or whether MUB(6) = 3). The context mentions:

- Gap G3 is "DISCHARGED on chart interfaces via continuous boundary homotopies" in a Lean 4 file `ContinuousBoundaryHomotopyPositivstellensatz.lean`
- It proves convex margin positivity μ(t) ≥ 12133/30000 > 0 across 6 interface homotopies connecting 5 canonical charts: B_6(θ), K_6^(3), cusps, H_6, S_6
- The task asks to explain:
  1. How the 6 interface convex combinations μ(t) = (1-t)μ_A + t·μ_B ≥ 12133/30000 > 0 for t ∈ [0,1] ensure no uncertified zero-curvature gap opens during continuous homotopy deformations between adjacent chart closures.
  2. Formulate the uniform Lipschitz continuity bound L = 85/9 and its interaction with certified bisection mesh step δ = 1/1000 to ensure strict gap propagation ε − L·δ > 0.
  3. State the narrowest defensible claim regarding global enclosure over the certified charts, respecting the firewall: stated region only; mints no authority.

The constitutional rules are strict:
1. Never claim or imply MUB(6)=3 or MUB(6)≤3. All findings apply strictly to the declared region/moduli and mint no authority.
2. No hype verbs.
3. For each gap analysis, include: what it supports, what it does not support, the narrowest defensible claim, the next test needed.
4. Provide precise algebraic, geometric, and formal Lean 4 insights.

So I need to write a careful, epistemically disciplined analysis of Gap G3's discharge mechanism. Let me think about the mathematics here.

**Setting the scene:**

The MUB(6) problem concerns mutually unbiased bases in dimension 6. The program apparently decomposes the relevant parameter space (some moduli of complex Hadamard matrices or MUB configurations) into charts — 5 canonical charts: B_6(θ) (probably a one-parameter family of complex Hadamard matrices in dimension 6, like the B_6 family from the classification of 6×6 complex Hadamard matrices), K_6^(3) (perhaps a Karlsson family?), cusps (boundary strata), H_6 (some transversal/symmetric family), S_6 (perhaps the self-adjoint or symmetric sector).

Actually, in the literature on 6×6 complex Hadamard matrices, there are families: F_6^(2) (Fourier), B_6(θ) (a one-parameter family found by Brierley/Hayden? Actually B_6 is a known one-parameter family), K_6^(3) (Karlsson's 3-parameter family? Actually Karlsson found K_6^(2) and K_6^(3) families), etc. The classification of 6×6 complex Hadamard matrices includes F_6, B_6(θ), K_6^(2), K_6^(3), and isolated matrices like P_6, S_6... Hmm, actually there's a known "S_6" isolated matrix? There's the "Sicilian" family? Let me recall: The known 6×6 complex Hadamard matrices: F_6 = F_2 ⊗ F_3, B_6(θ) (one-parameter), K_6^(2) (two-parameter), K_6^(3) (three-parameter), plus isolated ones: P_6 (a "Phantom"?), S_6 (a "sporadic"?), X_6, etc. Actually the known isolated 6×6 complex Hadamard matrices include P_6 and S_6 (found by computer search, e.g., by Szöllősi). And "cusps" might refer to boundary strata of the moduli space.

Anyway, the exact identity of the charts matters less than the logical structure. The program apparently:

- Covers a declared region of the parameter space (moduli of MUB-relevant configurations, e.g., Fourier families of order 6, or the space of pairs (Hadamard, eigenbasis) relevant to MUB triples) by 5 charts.
- Each chart has been certified (presumably via Positivstellensatz-type certificates in Lean, i.e., sums-of-squares / semialgebraic certificates over the quotient ring Sper(R[X]/I_55) — the real spectrum of a coordinate ring modulo an ideal I_55, presumably the ideal of the variety cut out by 55 polynomial constraints, e.g., MUB-defining equations).
- Gap G3 concerns the interfaces between charts: the "gaps" between chart closures where the certification might fail — i.e., whether an uncertified region (a "zero-curvature gap" — presumably a point where some curvature/margin functional degenerates to zero, indicating a potential transition point where the MUB structure could break down or where the certification's positivity fails) could open during homotopy deformation between adjacent charts.

The discharge mechanism: continuous boundary homotopies. For each pair of adjacent charts (A, B), consider the convex combination of the margin functionals μ_A and μ_B: μ(t) = (1−t)μ_A + t·μ_B. If both μ_A ≥ m and μ_B ≥ m with m = 12133/30000 ≈ 0.404433..., then trivially μ(t) ≥ m for all t ∈ [0,1] by convexity. Wait — but that's only if μ_A and μ_B are both bounded below by the same constant. Actually the claim is that the Lean file proves μ(t) ≥ 12133/30000 > 0 across all 6 interface homotopies. The number 12133/30000 ≈ 0.40443333...

Hmm, but actually the point of the homotopy is subtler: the charts are adjacent, their closures overlap or abut along an interface (a shared boundary stratum). The margin functional μ measures something like the "curvature margin" or "positivity margin" of the certification — e.g., the minimum of some polynomial (or its SOS certificate value) over the chart. During a homotopy deformation from chart A's certificate to chart B's certificate, the intermediate objects μ(t) must remain positive; if at some t the margin hit zero, there'd be an "uncertified zero-curvature gap" — a point where the certification degenerates.

The convexity argument: if μ_A ≥ m and μ_B ≥ m pointwise (as functions on the interface, or as certified constants), then μ(t) = (1−t)μ_A + tμ_B ≥ (1−t)m + t·m = m > 0 for all t ∈ [0,1]. So the homotopy path stays uniformly bounded away from zero — the margin never degenerates. This is the "convex margin positivity" argument. The key insight: positivity with a uniform lower bound is preserved under convex combination, so the straight-line homotopy in the space of margin functionals never crosses zero. Hence no zero-curvature gap opens on the interface.

But wait — there's a subtlety. The homotopy is between chart closures, and the margin functionals μ_A, μ_B might be defined on different domains (chart A and chart B respectively). On the interface (the intersection of closures, or a connecting region), both are defined, and the convex combination makes sense there. The 6 interfaces: 5 charts, and the interface graph presumably has 6 edges (e.g., a tree on 5 vertices has 4 edges; 6 edges suggests a specific adjacency structure — maybe a cycle plus chords, or the interface complex is 1-dimensional with 6 edges). Actually with 5 charts, 6 interfaces could be: B_6–K_6^(3), K_6^(3)–cusps, cusps–H_6, H_6–S_6, S_6–B_6, and maybe B_6–H_6 or similar. The exact combinatorics: 5 charts, 6 pairwise interfaces — like a graph on 5 vertices with 6 edges (e.g., K_5 minus 4 edges, or a specific adjacency graph). The user says "all 6 interface homotopies connecting the 5 canonical charts", so the interface graph has 6 edges.

**Part 1: The convex combination argument.**

Let me formalize. Let the ambient space be the real spectrum Sper(R[X]/I_55) — the real spectrum of the coordinate ring R[X]/I_55, where I_55 is presumably the ideal generated by the 55 polynomial equations defining the MUB-relevant variety (e.g., for a 6×6 problem, the number of real equations after symmetries might be 55). Sper is the set of prime cones/orderings — points of the real spectrum, which includes both classical real points and "points at infinity"/boundary/infinitesimal points. Working over Sper is the natural setting for Positivstellensatz certificates: a polynomial f is strictly positive on the real spectrum of a ring given sign conditions iff there exist s, and sums of squares etc. with f·s ≡ ... The classical Positivstellensatz: f > 0 on {g ≥ 0} ∩ Sper(A) iff ∃ s ∈ ΣA², m ∈ cone(g) with f·s = 1 + m (or f·s − m ∈ 1 + ...). Actually: f ≥ 0 on the constructible set iff f ∈ the preordering generated... Let me recall precisely:

- Krivine–Stengle Positivstellensatz: For f ∈ A = R[X]/I, and S a semialgebraic subset of Sper(A) defined by sign conditions g_i ≥ 0:
  - f > 0 on S iff ∃ s ∈ ΣA² (sum of squares), t ∈ the preordering generated by g_i, such that f·s = 1 + t in A. (Actually f·s·t = ... hmm.)
  
  Standard statement: f ≥ 0 on S iff ∃ s ∈ multiplicative module... Let me be careful:
  - f ≥ 0 on S ⟺ ∃ s ∈ ΣA², t ∈ preorder cone(g_i) with f·s = t... no.
  
  The Stengle Positivstellensatz: Let A be a ring, T the preordering generated by g_1,...,g_s. Then:
  - f vanishes on {T ≥ 0} iff ∃ n, f^{2n+1} + t·f = 0... (Nullstellensatz)
  - f ≥ 0 on {T ≥ 0} iff ∃ t ∈ T, s ∈ ΣA²: f·s = t... hmm, actually: f ≥ 0 iff f·s ∈ T for some s ∈ ΣA²? No wait.
  
  Correct statements:
  - f > 0 on S^A(T) := {α ∈ Sper A : g ≥_α 0 ∀g ∈ T} iff ∃ t ∈ T such that f·t = 1 (mod the ideal)... Hmm, that's not right either. Let me recall properly.
  
  Stengle's Positivstellensatz (1974): Let A be a commutative ring with 1 (or R-algebra), T ⊂ A a preordering (contains squares, closed under +, ·). Let S = {α ∈ Sper A : f(α) ≥ 0 ∀ f ∈ T}. Then:
  1. f ≥ 0 on S ⟺ ∃ s ∈ ΣA², t ∈ T: f·s = t... no. Hmm. Actually: f ≥ 0 on S ⟺ ∃ s ∈ ΣA² and t ∈ T with f·s + t = 0? No...
  
  Let me just recall the three statements:
  - **Positivstellensatz**: f > 0 on S ⟺ ∃ t ∈ T, s ∈ ΣA² : f·s = 1 + t. (i.e., f·s − t = 1.) Hmm, I think it's: f > 0 on S iff f·s = 1 + t for some s ∈ ΣA², t ∈ T? Wait, that would make f·s − 1 ∈ T, i.e., f·s − 1 ≥ 0 on S, so f·s ≥ 1 > 0 on S, hence f > 0 on S (since s ≥ 0). Conversely if f > 0 on S... by compactness arguments (with Sper compactness), yes: f·s − 1 ∈ T for some s ∈ ΣA². Hmm, but actually I recall it as: f·s·t = 1 + (something in T)? Let me think again.
  
  Standard formulation (e.g., from Marshall's book "Positive Polynomials and Sums of Squares", or Bochnak–Coste–Roy):
  For A = R[X], T a preordering, S_T = {x ∈ R^n : g(x) ≥ 0 ∀ g ∈ T}:
  - f > 0 on S_T ⟺ ∃ s ∈ Σ², t ∈ T: f·s = 1 + t. ✓ (This is right: f·s − t = 1, so f·s − t ∈ 1 + T... hmm, f·s = 1 + t means f·s − t = 1.)
  - f ≥ 0 on S_T ⟺ ∃ s ∈ Σ², t ∈ T: f·s = t... no wait: f·t = f^{2k} + s? Hmm. I recall: f ≥ 0 on S_T ⟺ ∃ s ∈ Σ², t ∈ T, m ∈ N: f·t = f^{2m} + s? Hmm, or f^{2m} + f·t + s = 0? Let me think: f ≥ 0 on S_T iff ∃ t ∈ T, s ∈ Σ², k ≥ 1: f^{2k} + f·t = s? Hmm.
  
  Actually the standard: 
  - **Nichtnegativstellensatz**: f ≥ 0 on S_T ⟺ ∃ t ∈ T, s ∈ ΣA², and odd positive integer... : f·t = f²·s + ... I'll just state: f ≥ 0 on S_T iff there exist s ∈ Σ², t ∈ T with f·s = t? Check: if f·s = t ∈ T then on S_T, f·s ≥ 0 and s ≥ 0 so f ≥ 0. ✓. Conversely, this is the theorem (with possibly f·s = t needing f·s ∈ T). Hmm, but I recall the Nichtnegativstellensatz involves f^{2n+1}: f ≥ 0 on S_T ⟺ ∃ n, t ∈ T, s ∈ Σ²: f^{2n+1}·... hmm no: f^{2n} + t·f + s = 0? Let's check: if f^{2n} + t·f + s = 0, then on S_T: f^{2n} + s = −t·f, so −t·f ≥ 0 (LHS ≥ 0), t ≥ 0, so f ≤ 0? That gives f ≤ 0. Hmm, sign conventions. If f^{2n} + s + t·f = 0 then t·f = −(f^{2n}+s) ≤ 0, and t ≥ 0 on S_T, so f ≤ 0 on S_T. So that's the Negativstellensatz for −f. OK so:
  - f ≤ 0 on S_T ⟺ ∃ n ≥ 1, s ∈ Σ², t ∈ T: f^{2n} + s + t·f = 0.
  - f ≥ 0 on S_T ⟺ ∃ n ≥ 1, s ∈ Σ², t ∈ T: f^{2n} + s − t·f = 0? Hmm wait: apply the above to −f: (−f)^{2n} + s + t·(−f) = 0 ⟹ f^{2n} + s − t·f = 0 ⟹ t·f = f^{2n} + s ≥ 0 on S_T ⟹ f ≥ 0 on S_T (where t > 0... hmm, t could vanish). OK, roughly.
  - f = 0 on S_T ⟺ ∃ n, s, t: f^{2n} + s + t·f = 0 AND f^{2n} + s − t'·f = 0, or combined: f^{2n+1} + s + t·f = 0? Hmm: Real Nullstellensatz: f vanishes on S_T ⟺ ∃ n, s ∈ Σ², t ∈ T: f^{2n} + s + t·f = 0? Check: on S_T, f^{2n} + s = −t·f; if f(x) ≠ 0... hmm, this shows f^{2n} + s + t·f = 0 forces... at a point where f > 0: LHS > 0, contradiction; where f < 0: f^{2n} + s ≥ 0 and t·f ≤ 0, could sum to zero? t·f ≤ 0 and f^{2n}+s ≥ 0, sum zero possible. Hmm, so that identity alone gives f ≥ 0? No wait: if f(x) < 0, then t(x)f(x) ≤ 0, f^{2n}(x) + s(x) ≥ 0, sum could be 0. So that's not enough. The real Nullstellensatz: f ∈ I(real radical) ⟺ ∃ n, s ∈ Σ²: f^{2n} + s ∈ (ideal). With preorderings: f vanishes on S_T iff ∃ n, s, t: f^{2n} + s + t·f = 0? Hmm, I think for the Nullstellensatz it's f^{2n} + s + Σ t_i g_i·(stuff)... I'm overcomplicating. 

For the answer, I don't need the full Stengle machinery in complete precision; I need to reference it correctly at the level of: strict positivity on the real spectrum is certified by an identity f·s = 1 + t with s a sum of squares and t in the preordering/cone generated by the chart constraints. That's the Positivstellensatz certificate. The key point for the firewall: such certificates are algebraic identities in the ring, checkable in Lean by ring normalization / sos decomposition, and they certify positivity on ALL of Sper(R[X]/I_55) restricted to the sign conditions — i.e., on the declared region only.

Now the "margin" μ: presumably each chart comes with a margin functional — maybe μ is the certified lower bound of some curvature-like quantity (e.g., the determinant of a Gram/Hessian, or the minimum eigenvalue margin of the MUB-defining map, or the "gap" in a spectral sense). The number 12133/30000 ≈ 0.4044333. Interesting: 12133/30000. Hmm, 12133 = ? 12133 = 11 × 1103 = 11 × 1103. 1103 is prime? 1103: not divisible by 2,3,5,7 (7×157=1099), 11 (11×100=1100, 11×100.3 no), 13 (13×84=1092, 13×85=1105), 17 (17×64=1088, 17×65=1105), 19 (19×58=1102), 23 (23×47=1081, 23×48=1104), 29 (29×38=1102), 31 (31×35=1085, 31×36=1116), sqrt(1103)≈33.2, so check 31: no. So 1103 prime. So 12133 = 11·1103. And 30000 = 2^4·3·5^4... = 16·1875 = 30000. Fine, it's just a rational constant from a bisection/certification computation. ≈ 0.404433.

**Part 1 details:**

The interface homotopy: for adjacent charts A, B with closures cl(A), cl(B) meeting along interface ∂A ∩ ∂B (or connected via a homotopy region), the certification on A gives margin μ_A ≥ m_A and on B gives μ_B ≥ m_B, with min(m_A, m_B) ≥ 12133/30000 (or the interface-specific combined bound). The homotopy H(x, t) = (1−t)·μ_A(x) + t·μ_B(x) for x in the interface region, t ∈ [0,1]. Since for each fixed x, t ↦ H(x,t) is affine in t, and H(x,0) = μ_A(x) ≥ m, H(x,1) = μ_B(x) ≥ m, we get H(x,t) ≥ (1−t)m + t·m = m = 12133/30000 > 0 for all t ∈ [0,1]. 

Key structural points:
- Affinity in t means no interior minimum can dip below the endpoint values: min over t of an affine function on [0,1] is attained at an endpoint. So the homotopy margin is bounded below by min(μ_A(x), μ_B(x)) ≥ m. This is the "convex margin positivity" — the straight-line (linear) homotopy in margin space cannot create zeros because the zero set of H is avoided: {H = 0} ∩ (interface × [0,1]) = ∅ since H ≥ m > 0.
- "No uncertified zero-curvature gap opens": a "zero-curvature gap" would be a point (x, t) where the margin vanishes — i.e., where the certification's positivity degenerates, corresponding to a point where the curvature/regularity functional controlling the chart's validity hits zero, opening an uncontrolled region. Since H ≥ m > 0 uniformly, the margin stays bounded away from zero along the entire deformation; the certified region is closed under the homotopy. Formally: the set C = {(x,t) : H(x,t) ≥ m} contains interface × [0,1], and since positivity is certified by a Positivstellensatz identity that is stable under the convex combination (the certificate itself can be interpolated: s(t) = (1−t)s_A + t·s_B, t-cert = (1−t)t_A + t·t_B, giving f·s(t) = 1 + t(t) identities... wait, does the certificate interpolate linearly? If f_A·s_A = 1 + t_A and f_B·s_B = 1 + t_B, then for the interpolated margin functional... hmm, actually the margin functionals μ_A, μ_B are presumably the same underlying polynomial f restricted to different charts, or chart-specific. The convex combination of certificates: (1−t)(f·s_A) + t(f·s_B) = f·((1−t)s_A + t s_B) = 1 + ((1−t)t_A + t·t_B), and since Σ² and the preordering T are convex cones (closed under convex combination: (1−t)s_A + t·s_B ∈ Σ² as sums of squares are a convex cone — yes, Σ² is a convex cone; preorderings are also closed under addition and multiplication by nonneg scalars, so convex), the interpolated certificate is again a valid certificate. This is a nice point: the certificate space is convex, so the linear interpolation of certificates is a certificate, matching the linear interpolation of margins. This gives a "certificate-level homotopy," not just a value-level one. That's a strong structural point to make: the discharge is not merely numerical evaluation along a path but an algebraic identity valid over the ring, hence valid at every point of Sper(R[X]/I_55) satisfying the sign conditions — including non-closed points, infinitesimal thickenings, and boundary points of the real spectrum. This matters because Sper includes limit points that a naive numerical mesh might miss.

- Why 6 interfaces for 5 charts: the interface graph. Presumably the adjacency structure of the chart cover of the declared region: e.g., B_6(θ) ↔ K_6^(3) (B_6 is a boundary/degenerate member of the K_6^(3) family at specific parameter values), K_6^(3) ↔ cusps (cusp strata as parameters degenerate), cusps ↔ H_6, H_6 ↔ S_6, S_6 ↔ B_6, and one more, maybe K_6^(3) ↔ H_6 or cusps ↔ S_6. I shouldn't overclaim the exact combinatorics; I can note that the interface graph on 5 vertices has 6 edges and that the discharge covers each edge with one homotopy. Actually, I could present it as: the 6 interfaces form the 1-skeleton of the chart-cover nerve restricted to pairwise adjacencies; G3's discharge requires every edge of this skeleton to be certified. If the nerve is not a tree (6 edges > 4 = tree edges for 5 vertices), there are 2 independent cycles; the homotopy discharge must be consistent around cycles — but since each edge discharge is a standalone positivity certificate, cycle-consistency is automatic (no monodromy/orientation issue for positivity margins). That's a nice point: positivity margins are scalar and orientation-free, so unlike gluing problems with signs or phases (where holonomy around cycles could obstruct), the convex-combination discharge composes freely around cycles.

**Part 2: Lipschitz bound and mesh.**

L = 85/9 ≈ 9.4444... δ = 1/1000 = 0.001. ε = the margin 12133/30000 ≈ 0.404433. Then ε − L·δ = 12133/30000 − 85/9000. Compute: 85/9 × 1/1000 = 85/9000 = 17/1800 ≈ 0.0094444. So ε − Lδ = 12133/30000 − 85/9000. Common denominator 90000: 12133/30000 = 36399/90000; 85/9000 = 850/90000. Difference = 35549/90000 ≈ 0.394989 > 0. ✓. So strict gap propagation holds with slack ≈ 0.395.

The logic: the margin functional μ (or the family μ(t)) is Lipschitz in the chart/interface parameters with constant L = 85/9 (presumably a certified bound: |μ(x) − μ(y)| ≤ L·‖x−y‖ for the relevant parameter metric, derived from bounding the gradient of the polynomial margin over the compact certified region — e.g., via interval arithmetic / Bernstein coefficients / mean value theorem with certified derivative bounds). The bisection mesh: the parameter domain is subdivided by certified bisection into cells of diameter ≤ δ = 1/1000 (mesh step). On each cell, μ is evaluated at the cell center (or a sample point) with certified value ≥ ε (the certified margin at sample points). Then by Lipschitz continuity, for any point x in a cell with sample point x_0: μ(x) ≥ μ(x_0) − L·‖x − x_0‖ ≥ ε − L·(δ/2 or δ) > 0. The condition ε − L·δ > 0 ensures that the pointwise certified value at mesh nodes propagates to strict positivity on the whole cell — "strict gap propagation": the gap (margin) cannot close within a mesh cell because the maximal possible decrease L·δ is strictly less than the certified margin ε.

The interaction: 
- L·δ = 85/9000 ≈ 0.00944 is the worst-case margin erosion over one mesh step.
- ε = 12133/30000 ≈ 0.40443 is the certified margin at mesh nodes (or the homotopy margin).
- ε − L·δ = 35549/90000 ≈ 0.39499 > 0: uniform slack. So even at the worst point of any cell, the margin is ≥ 35549/90000 > 0. Actually, careful: is ε the same as the homotopy margin m = 12133/30000? The problem says "convex margin positivity μ(t) ≥ 12133/30000" and then "strict gap propagation ε − L·δ > 0". Presumably ε = 12133/30000 (or ε is the certified node margin and the homotopy bound is the same constant). I'll take ε = 12133/30000 and compute ε − Lδ = 12133/30000 − 85/9000 = (36399 − 850)/90000 = 35549/90000 ≈ 0.39499 > 0. Let me double check: 12133/30000 = 0.4044333..., 85/9000 = 0.0094444..., difference = 0.3949889. And 35549/90000 = 0.39498888... ✓.

Also note: the Lipschitz bound must be uniform across the homotopy: sup over t ∈ [0,1] of the Lipschitz constant of μ(·, t) — since μ(t) = (1−t)μ_A + tμ_B, Lip(μ(t)) ≤ (1−t)Lip(μ_A) + t·Lip(μ_B) ≤ max(Lip(μ_A), Lip(μ_B)) = L = 85/9. So the convex structure again helps: the Lipschitz constant of the interpolated functional is bounded by the max of endpoint constants — the homotopy does not amplify gradients. This is the "uniform" in "uniform Lipschitz continuity bound": L is uniform over t ∈ [0,1] and over all 6 interfaces (a single global constant works for all interfaces, presumably because the charts share a common polynomial degree/derivative bound structure over the compact region).

Formal Lean 4 aspects: 
- The Lipschitz bound would be proven via `LipschitzWith` in Mathlib: `LipschitzWith (85/9) μ` on the metric space of parameters (e.g., a product of intervals with the sup metric), derived from `ContDiff` + bounded derivative, or via interval arithmetic on polynomial derivatives (`Polynomial.derivative` bounds, or `intervalArithmetic`/`Interval` computations certified by `norm_num` / `native_decide` on rationals — better: exact rational arithmetic).
- The mesh: a bisection procedure producing a `Finset` of cells with certified diameter ≤ 1/1000; each cell carries a certificate (SOS identity) or a rational interval evaluation of μ at its center.
- The propagation lemma: `∀ x ∈ cell, μ x ≥ ε − L * δ`, proven by combining `LipschitzWith` with the triangle inequality: `|μ x − μ x₀| ≤ L * dist x x₀ ≤ L * δ`.
- The final positivity: `ε − L * δ = 35549 / 90000 > 0` by `norm_num` / `rat` arithmetic — decidable, exact.
- The homotopy: `μ t x = (1 - t) * μA x + t * μB x`, with `Continuous`, and the convexity lemma `μ t x ≥ min (μA x) (μB x)` via `add_mul`/`mul_le` manipulations — actually the cleanest: since 0 ≤ t ≤ 1, (1−t)·μA + t·μB ≥ (1−t)·m + t·m = m. In Lean: `convexity` lemmas or direct `nlinarith` after establishing bounds. The key: everything is over ℚ (rationals), so positivity checks are decidable by `decide`/`norm_num` — no floating point.

Also the real-spectrum unification: Sper(R[X]/I_55) is the space of orderings; the charts correspond to constructible subsets defined by sign conditions on the chart-defining polynomials; the interfaces are where sign conditions flip between adjacent charts. The Positivstellensatz certificates are ring identities, hence hold at every ordering. The homotopy margin μ(t) ≥ m is likewise a statement about all orderings satisfying the combined sign conditions. The "global unification" across Sper: the 5 charts + 6 interfaces cover the declared region D ⊂ Sper(R[X]/I_55) (the declared region being the intersection of the constructible cover with the sign conditions defining the moduli under study). G3's discharge ensures the cover is not just a union of certified islands but a connected certified region with no interstitial uncertified gaps: chart interiors certified (by G1/G2 presumably), interfaces certified by G3's homotopies, hence by a nerve/covering argument the entire declared region is enclosed. The Lipschitz–mesh argument handles the residual concern that the homotopy positivity is certified on a discrete mesh: uniform Lipschitz continuity propagates the node certificates to the continuum between nodes, and ε − Lδ > 0 gives the uniform strict slack.

Wait — I should be careful about the logical division of labor: 
- The convex combination argument (Part 1) is exact/analytic: μ(t) ≥ m for all t ∈ [0,1] — this is an exact statement if μ_A, μ_B ≥ m pointwise. But how do we know μ_A ≥ m pointwise on the interface? Presumably via the mesh + Lipschitz argument: μ_A is certified ≥ m at mesh nodes, and Lipschitz + mesh step propagates to the whole interface with slack ε − Lδ. Hmm, but then the margin at general points is ≥ ε − Lδ = 35549/90000, not ≥ ε. Let me re-read the task.

"Formulate the uniform Lipschitz continuity bound L = 85/9 and its interaction with the certified bisection mesh step δ = 1/1000 to ensure strict gap propagation ε − L*δ > 0."

So ε here is presumably the certified margin at mesh nodes = 12133/30000 (the same constant as the homotopy bound, or the homotopy bound is derived from node margins). The structure is likely:

1. On each chart, the margin functional is certified at bisection mesh nodes with value ≥ ε = 12133/30000 (via exact rational/SOS evaluation).
2. Lipschitz continuity with constant L = 85/9 propagates: any point within distance δ of a node has margin ≥ ε − Lδ = 35549/90000 > 0.
3. The mesh with step δ covers the chart (and interfaces), so the whole declared region has margin ≥ 35549/90000 > 0 — strict positivity, no zero-curvature gap.
4. On interfaces, the homotopy μ(t) = (1−t)μ_A + tμ_B inherits: node values ≥ ε on both sides ⟹ μ(t) ≥ ε at nodes ⟹ (Lipschitz in (x,t)? or in x for each t) μ(t, x) ≥ ε − Lδ for all x within δ of nodes. Additionally, the convexity in t gives the uniform-in-t bound μ(t) ≥ min(μ_A, μ_B) ≥ ε − Lδ, so no t-sampling is needed — the t-direction is handled exactly by convexity, and only the x-direction needs the mesh. That's an important structural point: the homotopy parameter t is handled exactly (no meshing in t needed) because of affinity/convexity; the spatial parameters are handled by mesh + Lipschitz. This division of labor is what makes the enclosure both rigorous and tractable.

Hmm, but the problem statement says "proves convex margin positivity μ(t) ≥ 12133/30000 > 0 across all 6 interface homotopies" — so the Lean file proves μ(t) ≥ 12133/30000 directly (perhaps the interface margins are certified pointwise via the certificates, and the convex combination preserves the bound exactly). Then the Lipschitz–mesh argument is the mechanism by which the pointwise/node certification extends, or the mechanism for the chart interiors. Either way, I can present both layers coherently:

- Layer 1 (exact, algebraic): Positivstellensatz certificates on charts give μ ≥ m on chart regions (as Sper statements). Interface hom
```
</details>


---

### Model: Super Bunny Alpha

- **Status:** TRUNCATED (finish_reason: `length`, content: null)
- **Latency:** 128.01s | **Tokens:** 8824
- **Notice:** Call exhausted token limit during internal reasoning; no completion content was emitted.

<details><summary>Truncated Reasoning Trace (34338 chars)</summary>

```
We need craft answer. Need understand context. Need explain globally across Sper(R[X]/I55), interfaces, six convex combos lower bound, Lipschitz L 85/9 and delta 1/1000, strict epsilon - L delta >0. Need likely calculate L delta = 85/9000 =17/1800 ≈ .009444. Need say condition epsilon >17/1800, or if certified epsilon maybe value not supplied. Need avoid hype terms including "proves", "guarantees", "mathematically verifies", "fundamentally", "true intelligence", "impossible", "universal", "flawless", "perfectly", "clearly", "obviously", "simply", "merely", "weaponized". We can use establishes? Claim hygiene only hype verbs specified. Need perhaps explain graph/tree covering 5 charts and six interfaces, connected adjacency. Each edge parameter t. Convex affine interpolation positivity. At endpoints, same. Uniform min = c. Open cover? "global across Sper..." Need be precise: If chart closures cover certified region, and interiors have base epsilon perhaps. G3 discharged only interfaces. Uniform continuity between mesh nodes via Lipschitz. But potential issue: Lipschitz variation bound: |mu(s)-mu(t)| ≤ L|s-t|. Then mu(t) ≥ mu(t_k)-Lδ. If node margin ≥ epsilon, then ≥ epsilon - Lδ. Strict if epsilon > 17/1800. Uniform bisection. Need perhaps ε is certified minimum over mesh nodes. Six homotopy margins alone don't define ε across full charts; need finite certified mesh and perhaps each cell. We should distinguish Sper quotient algebraic semantics: charts pullbacks to representatives? I_55 ideal? We shouldn't overclaim global all algebraic variety unless chart atlas coverage and certificates. They say certified charts. Need formulate.

Could mention μ_A, μ_B endpoint margins along relevant common overlap/closures. A convex combination of two positive margins is positive. Numerical exact rational 12133/30000 ≈ 0.4044333. Therefore each edge has no zero. The six edges forming connected chart adjacency graph (5 vertices, likely K5? Canonical charts? Six interface homotopies maybe graph connected). Every path/deformation that factors through adjacent edges avoids interface zero. But arbitrary global homotopy not necessarily; "during continuous homotopy deformations between adjacent chart closures." Need limit to monotone traversals or path composed of these six edge homotopies. Continuity alone doesn't prevent zeros in interior absent bound. Emphasize.

Interaction with mesh: On each edge t, sample t_k = k/1000, k 0..1000. Lipschitz in t. For t in interval, choose endpoint/nearest node, difference ≤δ perhaps if half spacing, or ≤δ conservative. If μ values satisfy curvature relation? They call mu(t) margin. L=85/9. Then μ(t) ≥ μ(t_k)-17/1800. If node min ε. Strict positivity if ε>17/1800. If equality, lower bound zero and doesn't certify strict. Important. If certified epsilon might be known from file/context, not stated. Could say provided ε is certified with strict >. The user wording "ensure strict gap propagation epsilon - L*delta >0." State exact condition. If ε known maybe 1? But no. Could infer perhaps margin positivity and Lipschitz. Need perhaps calculate if epsilon e.g. what? We cannot invent. Say define ε = min over certified mesh nodes. To obtain strict positivity, need ε > 17/1800. If source gives ε rational, compare exact. The question might expect formula. "Formulate uniform Lipschitz continuity bound L=85/9 and its interaction with certified bisection mesh step delta=1/1000 to ensure..." So calculate.

Potential issue Lipschitz applies to what? "analytic parameter variation enclosure unified globally" likely family of witness/margin. Need explain pullback to quotient. In Sper(R[X]/I_55), scalar functions are equivalence classes modulo I55. Chart inequalities need descend/are interpreted modulo ideal. A uniform certificate could be finite atlas: chart functions q_i and overlap transition maps. Each interface has pullbacks A/B. On quotient, same algebraic element represented differently. μ(t) certificate is chart-invariant in the sense its pullbacks on overlap? Need avoid assuming. Perhaps explain global enclosure as atlas-local certificates whose overlap compatibility has been checked. The six interface bounds glue due to connected graph. But lower bounds on overlaps alone don't give compactness or uniformity over interiors? Mesh handles parameter variation.

Let's parse exact ask:

"### CONTEXT:
Gap G3 is DISCHARGED on chart interfaces via continuous boundary homotopies in ContinuousBoundaryHomotopyPositivstellensatz.lean, which proves convex margin positivity mu(t) >= 12133/30000 > 0 across all 6 interface homotopies connecting the 5 canonical charts (B_6(theta), K_6^(3), cusps, H_6, S_6).

### TASK:
Explain how the analytic parameter variation enclosure is unified globally across Sper(R[X]/I_55):
1. Explain how the 6 interface convex combinations mu(t) = (1-t)mu_A + t mu_B >= 12133/30000 > 0 for t in [0, 1] ensure that no uncertified zero-curvature gap opens during continuous homotopy deformations between adjacent chart closures.
2. Formulate the uniform Lipschitz continuity bound L = 85/9 and its interaction with the certified bisection mesh step delta = 1/1000 to ensure strict gap propagation epsilon - L*delta > 0.
3. State the narrowest defensible claim regarding global enclosure over the certified charts, respecting: 'stated region only; mints no authority'."

We need likely accept context, explain. Need perhaps structure required fields: what supports, does not support, narrowest claim, next test. Must always include for each gap analysis. We can organize one G3 analysis with all four explicit. Need mention "supports", "does not support", "narrowest", "next test."

No forbidden words. Ensure not accidentally use "clearly"/"simply"/"merely"/"proves" etc. We can say theorem certifies. "uniform" is not forbidden (universal is). "global" as scoped. "ensure" user uses; not forbidden but maybe epistemic. We can state condition.

Need think mathematical rigor.

Part 1:
Let G=(V,E), |V|=5, |E|=6, vertices chart closures C_i, edge e=(i,j) common interface. Let h_e:[0,1]→? continuous path within C_i∪C_j or overlap. Pullbacks of margin functional: m_i etc. On edge, endpoint functions μ_A, μ_B. Certificate says
μ_e(t) = (1-t)μ_A + t μ_B.
If μ_A, μ_B ≥ c, then μ_e(t) ≥ [(1-t)+t]c=c, exact c=12133/30000. If actual endpoint bounds perhaps c. Strict. Thus no zero at interface, for every t. At t endpoints too. The min lies c. Since 6 edges cover all pairwise adjacency and graph connected, any chart path crosses edges and remains positive at crossings. But what does "zero-curvature gap" mean? A zero of curvature-related margin on boundary. Avoid if margin &gt;0. Need say this only precludes zeros detected by this scalar margin on interfaces. It doesn't say curvature itself positive, unless margin is Positivstellensatz witness certifying it. A positive witness can establish nonvanishing/positivity depending theorem. "Uncertified zero-curvature gap" means no point with μ=0, so no loss via that certificate. It doesn't exclude singularities not represented by μ or paths not covered.

Part 2:
Need define analytic map perhaps m_e(t) on t parameter. Uniform Lipschitz:
|μ_e(t)-μ_e(s)| ≤ 85/9 |t-s| for all e and s,t ∈[0,1].
Potential concern convex affine function is Lipschitz with |μ_B-μ_A|, but given L. Fine.
Mesh Tδ={k/1000}. For each t pick mesh t_k same edge. If arbitrary point, nearest sample distance ≤1/2000, but conservative endpoint/cell bound ≤δ. State use δ (safe). Then:
μ_e(t)≥μ_e(t_k)-Lδ.
Define ε perhaps minimum over all chart-interior certification points and mesh nodes:
ε := min_{e,k} μ_e(t_k) (or includes chart cores). If every node has μ ≥ ε, then uniform lower bound ε - 17/1800.
Compute 85/9*1/1000=85/9000=17/1800. Strict &gt;0 iff ε&gt;17/1800.
If using interface c only, can we derive full interval min from c and Lipschitz? c -17/1800 = 12133/30000 -17/1800. Calculate common denominator 90000: 36399/90000 -850/90000=35549/90000 ≈ .3949889 &gt;0. Interesting! If c is lower bound across continuous t already, no mesh needed. But perhaps c only endpoint? Context says c across all. Yet they ask mesh interaction. Could mention two independent layers: exact convex interface bound already continuous and gives c. For other analytic chart parameter functions covered by Lipschitz mesh, need ε &gt;17/1800. If ε can be bounded below by c? If node μ≥c then c-Lδ &gt;0. But Lipschitz-based enclosure likely interior. Need be cautious.

Maybe ε is initial strict margin. We can formulate global enclosure:
- chart core certificate: minimum epsilon on certified mesh points.
- Lipschitz controls unsampled.
- interface convexity is exact and no subdivision required.
Then global lower bound min{12133/30000, ε-17/1800}, perhaps if other cells use Lipschitz. This is useful. If node minima include endpoints, perhaps ε≥? But formula.
Calculate c - Lδ:
12133/30000 = denominator lcm? 30000=2^4*3*5^4? 1800=2^3*3^2*5^2. lcm 90000. c=36399/90000, 17/1800=850/90000 => 35549/90000 >0. This offers an explicit robust bound if ε≥c. But don't infer epsilon. Could state if mesh-node certificate inherits μ_A,μ_B≥c at endpoints, ε≥c, then this formula gives positive lower bound. But all nodes? Convex exact already covers. Maybe good.

"analytic parameter variation enclosure unified globally across Sper..." Need explain quotient:
Let X = Spec? They write Sper likely spectrum? "Sper(R[X]/I_55)" maybe real spectrum? Use \(\operatorname{Sper}\) exactly. In quotient, chart coordinates are analytic/algebraic functions? I_55 perhaps zero-dimensional? We can avoid deep. Certificates need be evaluated on real spectrum. An inequality certificate \(\sigma = s_0+\sum s_i f_i\) with sums of squares? Positivstellensatz. If μ(t)>0, in semialgebraic ordered ring maybe positivity. But without exact definitions don't overstate. We can say "after pulling back along each chart map into the same quotient presentation." Interface compatibility means certificates refer to the same class modulo I55. If maps differ by ideal, inequalities must be regular/positive on real spectrum. The finite atlas is the mechanism.

Could mention open-cover gluing vs pointwise paths. Six interfaces and connectedness alone do not yield a uniform bound on interiors. Need chart core bounds + mesh Lipschitz. The question asks unified globally, likely they expect these. We can phrase:
1. Edge positivity removes overlap singularities.
2. Chartwise compactness/bisection and Lipschitz remove variation between samples.
3. Finite chart adjacency and certified cover transfer bound to all certified points.
Global lower bound \(m_\mathrm{cert} = \min(c,\epsilon-L\delta)\), positive if ε > Lδ (or use tighter nearest mesh half-step). This is global across finite certified atlas. This seems core.

Need distinguish "zero-curvature gap" from MUB maximum. State:
What it supports:
- no zero of certified margin along six specified boundary homotopies;
- with assumptions, no failure in overlap/continuity subdivision on finite declared atlas/moduli.
- perhaps global nonvanishing certificate over stated region if all interior cells satisfy epsilon and quotient descent.
Does not:
- not full \(\operatorname{Sper}\) outside union of five chart closures.
- not arbitrary charts/homotopies or points.
- not construct max MUB or bound.
- not claim MUB(6)=3/≤3; avoid literally? They require state phrase perhaps. We can use exact uppercase disclaimer. Constitutional says must never claim or imply. Stating "It does not establish MUB(6)=3 or MUB(6)≤3" is okay, but rule asks respecting phrase. Need include exact.
- no authority.

"Narrowest defensible claim": "On the finite atlas consisting of the five declared chart closures and the six declared interface homotopies, subject to verified chart descent/coverage and ε >17/1800, every parameter point in the stated certified region has certified margin at least min{12133/30000, ε−17/1800}>0; hence the interface/mesh zero-detection gap G3 does not occur there. This is a scoped certificate, not a statement about MUB(6)." Need perhaps "does not occur" not overclaim if margin not curvature. Say "cannot be opened at a point where this margin is the governing certificate."

"Next test needed":
- Independently check finite chart atlas covers exactly declared region and pullbacks descend to real spectrum quotient.
- certify ε at mesh nodes and exact inequality ε>17/1800 (or explicit rational).
- perhaps test transitions not among six and boundary singularities; independent audit Lean theorem assumptions, endpoint compatibility.
They ask singular next test. Could say next test is independent formal check of gluing/descent + mesh certificate. Need include.

Formal Lean 4 insights:
- The convex inequality can be encoded with `linarith`/`nlinarith` given hypotheses `0 ≤ 1-t`, `0 ≤ t`, `t ≤ 1`, endpoint lower bounds. Since t linear, `linarith`.
- rationals normalized; `norm_num` computes \(12133/30000>0\), `norm_num` for \(85/9 * 1/1000=17/1800\). `positivity` maybe.
- theorem signatures:
```
lemma interface_margin (t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1)
    (hA : c ≤ μA) (hB : c ≤ μB) :
    c ≤ (1-t)*μA+t*μB := by nlinarith
```
Actually linear arithmetic handles products t*μA as variables, coefficients with t variable? `linarith` treats nonlinear monomials as atoms but expression expanded and assumptions; can reason? `(1-t)*muA + t*muB - c`; if hA c≤muA, multiply inequality by nonnegative t isn't linear tactic unless Positivstellensatz. Algebra:
(1-t)μA + t μB = μA + t(μB-μA). Given μA≥c and μB≥c, can show using t nonnegative and 1-t nonnegative. `nlinarith` may derive products. `positivity` not with comparisons. We can show `have : 0 ≤ (1-t)*(μA-c) := mul_nonneg (sub_nonneg.mpr ...) ...`; similarly. Then `nlinarith`. Good.
- Lipschitz:
```
lemma mesh_lip (hk : δ = 1/1000) ... :
  L*δ = 17/1800 := by norm_num [hk]
```
and positivity via `lt_of_lt_of_le hε ...`.
- Need distinguish strict `>` in ordered field.
- For quotient `R[X]/I₅₅`, formalization uses `Ideal.Quotient` and mappings; if ring not ordered because quotient, inequalities are on representatives or maps to real spectrum, not quotient ring itself. This is an important formal Lean insight. The real spectrum has an order cone; positivity should be interpreted there, or via pullback to ordered rings. In Lean, `Ring` quotient does not inherit `LinearOrder`/positivity straightforwardly; a positive polynomial modulo ideal means its class has nonnegative image under every real homomorphism \(\operatorname{Spec}_R A \to \mathbb R\). We should mention. This is precise and perhaps expected. "Sper" likely specialized real spectrum. Formalizing positivity in quotient requires `RealSpectrum` or cone. The user asks global across Sper. We can say certificates are statements under all orderings, not direct `/` inequalities unless representation chosen.

Maybe I_55 denotes ideal in MUB program. Do not assume. The finite chart maps likely to real algebraic settings. State "provided each chart certificate is pulled back to the real spectrum of the quotient (or an ordered coordinate ring)." This condition is needed for narrow claim.

Let's think if the lower bound `c` follows from μ_A, μ_B each ≥ c. User says "6 interface convex combinations ... >= c." Could write:
\[
(1-t)\mu_A+t\mu_B\ge (1-t)c+t c=c.
\]
If endpoint lower bounds may differ but both at least c. Strict. Therefore no sign change by IVT. A continuous scalar function with positive margin cannot cross zero. This addresses zero-curvature gap. However "curvature" may be represented as square? Positivstellensatz. We can say a zero of certified expression would force μ=0 if μ=1-K? If margin μ = 1-λ? Need no details. If curvature gap \(g=\mu\), then. If Positivstellensatz witness margin positive, theorem maps that to desired inequality, not direct geometric curvature perhaps. Phrase scoped.

Connectivity:
V = {B,K,Cusps,H,S}, E six. Any sequence of adjacent chart changes is a path in finite graph. But six edges connecting all charts. At switches margin positive. Does it "unify globally"? Need interior cover. A connected graph lets avoid interface zeros, but not uniform interior. We combine mesh.

Uniform Lipschitz and ε:
Could define each chart's scalar parameter \(r\), functions \(m_i(r)\). Uniform `L` across all charts and interfaces:
\[
|m_i(r)-m_i(s)| \le L|r-s|,\quad \forall i,r,s.
\]
But transition coordinate Lipschitz may need account Jacobian. Given L 85/9. On mesh. Define:
\[
\epsilon = \min_{i,0\le k\le1000} m_i(r_{i,k})
\]
over certified bisection nodes. If exact rational values are machine certified, positivity. For any \(r\) in [r_k,r_{k+1}], choose endpoint; \(|r-r_k|\leδ\):
\[
m_i(r)\ge m_i(r_k)-Lδ\ge ε-Lδ.
\]
Actually if using right endpoint, yes \(r-r_k≤δ\). No issue. If endpoint chosen whichever, one lower. This establishes over chart parameter domain. At chart transitions, exact interface c. Combined:
\[
m_{\rm atlas}\ge \min\left(c,\epsilon-\frac{17}{1800}\right).
\]
If ε&gt;17/1800. This is precise global finite atlas bound. If chart covers all actual points and margins are appropriate, no zero.

Should epsilon perhaps be margin on nodes before Lipschitz. We can define all certified sample points. If min &gt; threshold. The interface c could itself be used to get endpoint nodes but exact. If ε≥c, combined bound as computed. We should state this optional:
If mesh endpoints are included among the interface certificate, ε≥c, then:
\[
c-\frac{17}{1800}=\frac{35549}{90000}&gt;0.
\]
Check arithmetic:
12133*3 = 36399. 17/1800*50=850/90000. difference 35549. gcd? 35549 maybe no. approx .3949889. Correct.
But if μ values can be &gt; c etc. This explicit calculation meets "strict gap propagation." Yet condition could be simply epsilon &gt; 17/1800. We can show both.

Potential conceptual issue: A convex combination of positive endpoint functions stays positive, but if μ_A and μ_B are not themselves same scalar under transition? Homotopy linear combination creates margin. The theorem says it. Explain coordinate consistency / endpoint pullbacks. If endpoints correspond to two charts and use same underlying quotient class, then convex blend is valid. If they are just arbitrary positive quantities, no. Need state assumption: endpoint functions are positive representations of the same Positivstellensatz functional after pullback. This is part of interface theorem. "Certified chart maps" and overlap.

What are five canonical charts B6(theta), K6^(3), cusps, H6, S6? Could mention chart labels only, no claims. Cusps maybe singular; interface positivity. Need no specific geometry.

"Sper(R[X]/I55)" maybe \(\mathbb R[X]/I_{55}\). We can denote \(X_{\mathrm{cer}} = \bigcup_i \pi_i(\dots)\). On real spectrum, finite chart cover. Need explain topological gluing:
- A finite cover by chart closures; each real point assigned at least one chart (assuming certificate).
- Over overlaps, transition maps.
- Interfaces form codimension-one seam. Exact convex certificates control seam.
- Within each chart, bisection nodes plus Lipschitz control all unsampled points.
- The finite min is global because finite min. This is the unification. No need compactness if mesh certificates given.
- If charts have multiple local parameters, L must apply in each and transition metric; uniform L 85/9. If not, global fails. Mention.

"analytic parameter variation enclosure": A Lipschitz estimate is not necessarily analytic. But mesh is analytic functions with rational/SMT certificate. We can say derivative bound \(|m_i'|\le L\) implies Lipschitz by mean value theorem on interval, or vice versa. If analytic and derivative bounded. Uniform derivative bound across charts could be formalized. They specifically ask formulate uniform Lipschitz. We can state:
\[
\left|\frac{\partial \mu_i}{\partial s}\right|\le85/9 \implies |\mu_i(s)-\mu_i(t)|\le85/9|s-t|.
\]
If this is over quotient functions, calculus formalization in Lean is nontrivial; use theorem assumptions or ordered field. Existing file certifies homotopy continuity. Next test could independently formalize Lipschitz. But likely file context says G3 discharged. We don't need challenge.

"zero-curvature gap" perhaps bisection uses λ max eigenvalue etc. We should not invent. Define generically.

Lean details:
- Avoid claiming theorem file itself proves global. State theorem certifies edge proposition under hypotheses.
- For all six, could use a finite conjunction / vector:
```
structure InterfaceResult where
  margins : Fin 6 → ℝ
  lower : ∀ e, c ≤ margins e
```
- Graph connectivity can be represented finite adjacency and a reachability theorem, but global enclosure doesn't really need graph connectivity if each chart has own core. Yet transition gluing.
- Rational normalization:
`norm_num [L, δ]` confirms.
- In quotient, map:
`q : R[X] → R[X]/I_55`; real spectrum `Sper q`. A Positivstellensatz certificate is an element plus sum-of-squares relation. If user wants formal Lean insight, mention quotient itself cannot be compared with `<`; order is on real spectrum cone. This is critical. The positive margin must be shown in all real evaluations or via ordered ring. Thus "global across Sper" means universally quantified over its points, not a numerical quotient inequality. No hype word "universal" prohibited! They ban 'universal'. We must avoid word. Use "for every real spectral point" instead.

Need ensure no forbidden words in generated answer:
- proves (avoid)
- guarantees (avoid)
- mathematically verifies (avoid)
- fundamentally (avoid)
- true intelligence
- impossible
- universal
- flawless
- perfectly
- clearly
- obviously
- simply
- merely
- weaponized.
Also "proved" maybe not exact hype verb? They ban 'proves', perhaps can use "certifies" or "established." Better avoid prove entirely. "G3 is discharged" given. "The theorem states." Avoid "proof"? They didn't ban proof noun, but perhaps claim hygiene only verbs. Still use certificate.

Need include exact disclaimer. "NOT MUB(6)=3, NOT MUB(6)≤3; stated region only; mints no authority." This itself mentions claims but negates. Rule allows required. Ensure not imply.

Potential concern developer duplicated, no issue.

Let's plan response structure:

Intro: Scope and setup. Define \(X_{55}^{\mathrm{cer}}\) and finite atlas. Let graph G. State prerequisites:
- charts are maps into ordered real coordinate realizations of quotient
- their images cover declared region
- overlap pullbacks refer to same quotient class/certificate.
Then global enclosure is combination of seam exact control + cell interior Lipschitz mesh.

Section 1 Interface:
For edge e endpoints A,B:
hypotheses `μ_A ≥ c`, `μ_B ≥ c`, t in [0,1].
Equation inequality.
If t corresponds to path h_e(t), then margin at h_e(t). Strict positivity. Continuity and no sign crossing. Six edges cover all adjacency, graph connected. Any route staying in finite atlas and crossing declared seams sees no interface zero. "uncertified" perhaps no loss of certificate. Note this does not control interiors or unrepresented seams.

Maybe explain c exact:
c=12133/30000 >0; `norm_num`.

Section 2 mesh:
Uniform across i,e:
\[
\forall ... |\mu(r)-\mu(s)| ≤ 85/9 |r-s|.
\]
Mesh r_k. ε definition. For t:
\[
\mu(t) \ge \mu(t_k)-L|t-t_k|
\ge \epsilon - 85/9000
=\epsilon-17/1800.
\]
Strict positivity condition. If choose nearest, δ/2 and stronger; but use certified δ. No need mention maybe.
Combined lower:
\[
m_* = \min(c, ε-17/1800).
\]
Finite. If ε> threshold then >0. If ε≥c:
c-Lδ=35549/90000.
Need check if `epsilon` over all nodes and chart interiors. If c exact seam, maybe global.
Also transition parameter compatibility: same L in normalized chart parameter; transition maps themselves certified. We can phrase "assuming stated L is with respect to the parameter used by mesh and covers chart cells." Without, no global conclusion.

Could mention if ε is certified strict e.g. rational compare:
```
example : 17/1800 < ε := by norm_num [ε_spec]
```
No value.

Section 3 Lean representation:
- quotient order.
- lemmas and tactics.
Pseudo Lean:
```
def c : ℚ := 12133/30000
...
lemma convex_lower ... := by
 have h1 : 0 ≤ (1-t)*(μA-c) := mul_nonneg ...
 have h2 ...
 nlinarith [h1,h2]
```
Need account t as ℝ and c ℝ.
- rational calc.
- quotient:
```
q : R[X] →+* R[X]/I_55
```
and positivity on `Sper`; avoid direct order. Maybe mention `I₅₅` isn't syntactically Lean name; `Ideal.I₅₅` etc. Formal theorem should map certificates to `RealSpectrum` order. The `Sper` order is not a `LinearOrder` on quotient. Good.
- `norm_num` for constants, `nlinarith` for convex bound, `linarith` only after products nonneg. `exact_mod_cast I_55` for ideal membership/descent.

Section 4 governance:
Explicit bullets:
What it supports.
What not.
Narrowest defensible claim.
Next test.

Need avoid repetitive and ensure all four.

Narrow claim exact:
"Subject to (i) finite atlas coverage of declared real region, (ii) interface pullbacks descend/are compatible on real spectrum, and (iii) mesh-node certificate ε>17/1800, every point in the declared region has a positive certified margin, with lower bound min(...). Consequently, G3's zero-margin failure mode is excluded on those chart closures and six homotopies." Is that too broad? "every point" within chart parameters if mesh covers each. Fine conditional.

Does interface exact bound c mean no "uncertified zero-curvature gap" between adjacent chart closures. Need say if μ is the margin used to certify curvature, then zero of margin cannot occur. The term "zero-curvature" could require link. We can qualify.

What not:
- not all Sper if atlas not full.
- not arbitrary analytic variation outside certified ranges or new charts.
- not excludes a geometric zero that doesn't force this certificate nonpositive.
- not MUB cardinality.
- no authority.
Maybe "Does not establish" okay.

Next test:
"Independently check the cover/descent predicate and obtain exact lower bound for ε at all 5 chart meshes; then recompute m_* in Lean. Following that, test unrepresented boundary/cusp strata and any chart adjacency absent from six." They ask next test singular; make primary. "The immediate next test is..." Fine.

Need perhaps mention topological issue: connected interface graph not enough for all regions. If chart interiors each certified, yes. If no mesh, seam bound alone only controls interfaces. The narrow claim must not overstate. We can emphasize.

Let's think if exact global lower bound c - Lδ can be claimed across interface. Since convex exact lower c, no need Lipschitz. Combined min if chart core bound. If only edge c, global enclosure over chart interiors cannot be inferred. User says "unified globally across Sper" maybe expects state. We can say the unification is conditional and exact.

Potential issue they may expect \(ε - Lδ >0\) with some ε perhaps from margin. They didn't specify ε. We should state conditional. Maybe `ε` could be lower bound at all mesh nodes. To "ensure" strict, require `ε > 17/1800`. If epsilon likely e.g. 1/30? Compare 17/1800=.00944, 1/30=.0333. Could infer maybe they expect \(\epsilon >17/1800\). No need invent. Could mention if ε is any certified positive margin, not enough; must exceed threshold. This is an important precision.

Let's calculate c and potential values:
12133/30000 = .404433333. Lδ=.00944444. Difference .3949889. If epsilon=1/100 maybe works. But no value. If ε=c, lower bound 35549/90000.

Could formulate derivative version:
\[
\left\|\nabla m\right\|? 
\]
No, scalar parameter. If local coordinates multiple dimensions, L 85/9 operator norm. Define one-dimensional. If transitions, parameter variation could be multiple. The user says analytic parameter variation, likely scalar. We can state for each local parameter and normalized transition coordinate. Uniform in chart index.

"bisection mesh step δ=1/1000" includes 1001 nodes. Could mention exact rational. On each closed interval [r_k,r_{k+1}], right endpoint difference ≤δ. To cover final endpoint, k 0..999. Fine.

Use of IVT:
Since μ_e continuous and μ_e(t)≥c, no t has μ=0. "No sign-change zero can open." We can mention this is pointwise and exact, not sampling artifact. If a path traverses edge non-monotonically, t is still in [0,1] and bound holds. If arbitrary path leaves edge, not covered.
"Continuous homotopy" h_e(t) may not be injective; all points image satisfy. Good.

Sper:
A positive polynomial certificate in ordered quotient. Maybe `Sper(R[X]/I55)` is likely a set of real points. The real spectrum has strict order? In Lean Mathlib, `RealSpectrum` order is partial? Positivity `0 ≤ᵣ a`. There may be `IsPos`? We can avoid exact API names. Mention cone membership `0 ≤ a` or all real evaluations. The quotient algebra itself may have zero divisors and no field order. Thus a claim "`μ>0` in quotient" is shorthand for ordered-real-spectrum positivity, not direct `<` in ring. This adds precision. The six edge charts likely analytic not polynomial? Real spectrum only polynomial ring. Chart analytic functions may not belong. Could require localizing/rational functions or real spectrum of localized coordinate ring. But context says Sper quotient. We can say pullbacks and admissible denominators. Do not overcomplicate. Yet as formal verification expert, note this.

Lean pseudo:
```
variable {A B t : ℝ}
lemma interface_lower
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1)
    (hA : c ≤ μA) (hB : c ≤ μB) :
    c ≤ (1-t)*μA + t*μB := by
  have hA' : 0 ≤ (1-t)*(μA-c) :=
    mul_nonneg (sub_nonneg.mpr.mpr (sub_nonneg.mpr ht1)) (sub_nonneg.mpr hA)
...
  nlinarith
```
Check sub_nonneg:
1 - t ≥0 from ht1.
μA-c≥0 hA.
```
have h1 : 0 ≤ (1-t)*(μA-c) :=
  mul_nonneg (by linarith) (by linarith)
```
Likewise.
Then expansion.
For strict:
c positive:
```
have hc : 0 < c := by norm_num [c]
exact lt_of_lt_of_le hc hconv
```
Lipschitz:
```
lemma lip_step : (85/9)*(1/1000)=17/1800 := by norm_num
```
Lean parser `(85 / 9 : ℚ)`. Real division tactic norm_num.
Then:
```
exact sub_pos.mpr hε |> lt_of_lt_of_eq? 
```
No need exact code.

For quotient descent, ideal membership:
If representative differs by element `I₅₅`, same class. But inequalities on real spectrum insensitive. Formal certificate should have `μA = μB`? Actually endpoint functions correspond. We can say compatibility represented by equality modulo ideal:
\[
p_A-p_B \in I_{55}
\]
when expected to be same class, and denominators invertible in localization. Interface homotopy must act on class. This is a useful algebraic insight. If charts use distinct functions, inequality certificate is same underlying form modulo ideal. The theorem should state.
Potential issue sum of squares Positivstellensatz: Strict positivity of a margin \(\mu\) over semialgebraic set means \(1/\mu\) lies in quadratic module generated by constraints: there is a certificate. Lean file named Positivstellensatz likely proves. We can mention:
At each chart, \(\mu\in \mathcal Q(g)\), i.e.
\[
1 = \mu_0+\sum_i \sigma_i g_i
\]
with \(\mu_0>0\) and \(\sigma_i\) sums of squares (or corresponding quadratic module). Then μ>0 implies no vanishing of denominator in inversion. But context only says margin positivity. "zero-curvature gap" could stem from inability to invert margin. We can articulate condition. Need not know exact theorem. A Positivstellensatz certificate often form \(1 = \tau_0+\sum \tau_i f_i\). If μ is a positive coefficient? The margin may be lower bound. Avoid overclaim exact algebra.
Could say "Whatever the file's Positivstellensatz predicate is, its strict-positive hypothesis must be instantiated by this same μ; the seam calculation alone does not create an interior SOS certificate." This is precise governance.

Need maybe explain "uncertified zero-curvature gap" in algebraic terms:
If curvature expression is rational with denominator controlled by μ, a zero of μ could make certificate undefined, not actual curvature zero. The positive margin prevents a singular denominator. But user phrase says zero-curvature gap. We can write "it prevents a zero of the margin that would open the stated zero-gap exception." Avoid equating.

Let's consider whether `μ_A, μ_B` endpoint margins ≥ c or only convex combination theorem lower c. User says "mu(t)... >= c across all 6." It might not state each endpoint ≥ c? Convex positivity at t=0/1 implies yes if formula and bound for all t. We can state that.

Could use graph adjacency matrix? Five charts, six interfaces. Maybe chart graph is K5 minus four edges. Not needed. A connected graph with 5 vertices and 6 edges. There can be cycles. Edge-wise bounds ensure any path. For global pointwise cover, graph connectivity irrelevant; but gluing route. We can say connected finite graph allows transfer, not compactness.

"uniform Lipschitz continuity bound L=85/9 and its interaction with certified bisection mesh step..." The uniform bound must include all chart functions. Need phrase:
\[
\forall i,\; \forall s,t\in I_i,\quad |\mu_i(s)-\mu_i(t)|\le \frac{85}{9}|s-t|.
\]
If overlaps are reparametrized, transition maps also need Lipschitz constants and composition. Given theorem declares uniform maybe. We can make condition explicit. A uniform L over all cells is what makes one global finite min. If constants chart-specific, use max. L 85/9 likely already max.

"analytic parameter variation enclosure" perhaps error propagation formula:
\[
M(t) \ge M(t_k) - L\delta
\]
and if curvature λ? We can call margin. "strict gap propagation ε - Lδ >0." Exactly.

We can mention if the bisection mesh is adaptive, δ maximum interval length. Here fixed 1/1000. If at every node ε is lower bound, all. If node intervals cross chart boundary, handle separately with c.

No hype terms. "exact" okay. "uniform" okay. "finite" okay.

Let's draft in detailed but moderate length. Need not quote full user context. Start:

"Let \(X_{55}^{cer}\subset Sper(...)\) be union of five declared chart closures, and assume chart pullbacks are ordered-real-spectrum certificates. Let G..." This is conditional and scoped.

"Because quotient ring generally isn't ordered, notation μ>0 means positive under every real ordering/evaluation after pullback." This addresses.

Then interface.

Potential concern word "every" okay, banned "universal." Fine.

Use "
```
</details>


---

## Gap G4: Genuine Simplicial 1-Cochains Topological Invariance

### Model: GLM 5.3

- **Status:** TRUNCATED (finish_reason: `length`, content: null)
- **Latency:** 32.65s | **Tokens:** 8686
- **Notice:** Call exhausted token limit during internal reasoning; no completion content was emitted.

<details><summary>Truncated Reasoning Trace (27554 chars)</summary>

```
Let me carefully work through this problem. The context is the MUB(6) program — a research program studying mutually unbiased bases in dimension 6, with 5 "gaps" (G1–G5) being analyzed under strict epistemic governance. The constitutional rules are strict: I must never claim or imply MUB(6)=3 or MUB(6)≤3, must avoid hype verbs, and for each gap analysis must include what it supports, what it does not support, the narrowest defensible claim, and the next test needed.

The specific task concerns Gap G4, which is described as "DISCHARGED on chart intersections with exact cycle circulation Phi_1 >= Gamma = 12133/5000 > 0 certified by Network Simplex with zero rational duality gap." The task asks me to explain the topological invariance of genuine alternating simplicial 1-cochains derived from the Čech nerve of the 5-chart cover:

1. Formulate the nerve simplicial complex N(U) of the 5 charts (B_6, K_6^(3), cusps, H_6, S_6).
2. Prove that the coboundary operator δ_0: C^0 → C^1 satisfies Σ_{e∈C} (δ_0 α)_e = 0 for every 0-cochain potential α on every closed 1-cycle C in Z_1(N(U)).
3. Explain how this proves that the circulation obstruction Φ_1 ≥ Γ > 0 represents a genuine non-trivial cohomology class in H^1(N(U); ℝ) that cannot be eliminated by any local gauge transformation, while respecting the firewall: "NOT MUB(6)=3, NOT MUB(6)≤3; stated region only; mints no authority."

Let me think about the mathematics here carefully.

**Setup: The nerve of a cover.**

Given a cover U = {U_i}_{i∈I} of a space X, the Čech nerve N(U) is the abstract simplicial complex whose k-simplices are ordered (k+1)-tuples (i_0, ..., i_k) of distinct indices such that the intersection U_{i_0} ∩ ... ∩ U_{i_k} ≠ ∅. So:
- 0-simplices (vertices): charts U_i with U_i ≠ ∅.
- 1-simplices (edges): pairs {i, j} with U_i ∩ U_j ≠ ∅.
- 2-simplices (triangles): triples {i, j, k} with U_i ∩ U_j ∩ U_k ≠ ∅.
- etc.

Here we have 5 charts: B_6, K_6^(3), cusps, H_6, S_6. Let me index them, say:
- 0: B_6
- 1: K_6^(3)
- 2: cusps (call it C_6 or the cusp chart)
- 3: H_6
- 4: S_6

The nerve N(U) is then a simplicial complex on the vertex set {0,1,2,3,4}, with an edge {i,j} whenever the corresponding charts intersect, a 2-simplex {i,j,k} whenever the triple intersection is nonempty, etc.

**Simplicial cochains and the coboundary.**

For an abstract simplicial complex K, the simplicial cochain complex with coefficients in an abelian group A (here ℝ or ℚ) is:
- C^k(K; A) = functions from oriented k-simplices to A, alternating with respect to orientation (i.e., a cochain evaluated on a simplex changes sign when the orientation is flipped).

Actually, let me be careful. There are two common conventions:

(a) Ordered simplicial cochains: C^k is the free abelian group on ordered (k+1)-tuples, and the coboundary is δf(i_0,...,i_{k+1}) = Σ_{j=0}^{k+1} (-1)^j f(i_0, ..., î_j, ..., i_{k+1}).

(b) Alternating cochains: cochains that vanish on degenerate simplices and change sign under permutation of vertices. The normalized subcomplex of the ordered one.

For the nerve of a cover, the natural object is the ordered simplicial complex (the nerve is often taken as the simplicial complex whose k-simplices are ordered tuples, or as a poset). The alternating cochains are the normalized ones.

The task says "genuine alternating simplicial 1-cochains", so we should work with alternating cochains: a 1-cochain φ assigns to each ordered pair (i,j) with U_i ∩ U_j ≠ ∅ a value φ(i,j) ∈ ℝ with φ(j,i) = -φ(i,j). This is the standard setup for Čech cohomology with constant coefficients: Čech 1-cochains are alternating functions on pairs of indices with nonempty intersection.

The coboundary δ_0: C^0 → C^1: a 0-cochain α assigns to each vertex i a value α_i ∈ ℝ. Then (δ_0 α)(i,j) = α_j - α_i. This is alternating: (δ_0 α)(j,i) = α_i - α_j = -(δ_0 α)(i,j). Good.

**Cycles and circulation.**

A 1-cycle C in Z_1(N(U)) is a formal sum C = Σ_e n_e · e (n_e ∈ ℤ, or we can think of it as a closed edge path) with ∂C = 0, i.e., at every vertex the net flow is zero. For a closed edge path v_0 → v_1 → ... → v_m = v_0, the circulation of a 1-cochain φ along C is Σ_{k=0}^{m-1} φ(v_k, v_{k+1}).

**Key claim (part 2):** For every 0-cochain α and every closed 1-cycle C, Σ_{e∈C} (δ_0 α)_e = 0.

Proof: This is the fundamental fact that coboundaries pair trivially with cycles — it's the statement ⟨δ_0 α, C⟩ = ⟨α, ∂C⟩ = 0 since ∂C = 0. Let me spell it out.

For a closed edge path v_0 → v_1 → ... → v_m = v_0 (with m ≥ 1, and edges (v_k, v_{k+1}) in N(U)):

Σ_{k=0}^{m-1} (δ_0 α)(v_k, v_{k+1}) = Σ_{k=0}^{m-1} (α_{v_{k+1}} - α_{v_k}) = (α_{v_1} - α_{v_0}) + (α_{v_2} - α_{v_1}) + ... + (α_{v_0} - α_{v_{m-1}}) = 0 by telescoping.

For a general integral 1-cycle C = Σ_e n_e e with ∂C = 0: Σ_e n_e (δ_0 α)(e) = ⟨δ_0 α, C⟩ = ⟨α, ∂C⟩ = ⟨α, 0⟩ = 0. Here the pairing ⟨·,·⟩ is the natural pairing between cochains and chains, and δ is the adjoint of ∂: ⟨δ α, C⟩ = ⟨α, ∂C⟩. This is a standard fact from simplicial homology/cohomology.

Alternatively, directly: write C as a sum of closed paths (every 1-cycle in a graph decomposes into closed edge walks), and apply the telescoping argument to each.

Actually, let me be careful about the general case. A 1-cycle in a simplicial complex is supported on the 1-skeleton, which is a graph. In a graph, H_1 is generated by cycles (simple closed paths), and every 1-cycle is a sum of simple cycles. So the telescoping argument on closed paths suffices, plus linearity.

Also, I should verify the adjointness ⟨δ α, C⟩ = ⟨α, ∂ C⟩ explicitly for the simplicial setting. With ordered cochains: (δ_0 α)(i,j) = α(j) - α(i). ∂(i,j) = j - i. Then ⟨δ_0 α, (i,j)⟩ = α(j) - α(i) = ⟨α, j - i⟩ = ⟨α, ∂(i,j)⟩. Extending linearly gives the general identity. 

**Part 3: The cohomology class.**

Now the circulation obstruction. The setup: on the chart intersections, there's some 1-cochain Φ (the "circulation" data — presumably derived from the Network Simplex certification: the flow/circulation on the 1-skeleton of the nerve, or a 1-cochain measuring obstruction). The claim is Φ_1 ≥ Γ = 12133/5000 > 0 on some distinguished cycle (or: the circulation of Φ around every cycle in some class is at least Γ, or the total circulation is at least Γ).

Hmm, let me think about what Φ_1 is. "exact cycle circulation Phi_1 >= Gamma = 12133/5000 > 0 certified by Network Simplex with zero rational duality gap." So presumably there's a linear program: minimize circulation subject to constraints, and the Network Simplex method certifies the optimum is Γ = 12133/5000 with zero duality gap (i.e., the LP optimum equals the dual optimum, certified exactly over ℚ). So Φ_1 is the exact (rational) value of the circulation on some cycle, and it's ≥ Γ > 0.

The topological point: if Φ were a coboundary, i.e., Φ = δ_0 α for some 0-cochain α (a "local gauge transformation" — gauge potentials on charts, with transition functions on overlaps), then the circulation of Φ around every closed cycle would be zero. Since there's a cycle C* with circulation Φ(C*) = Φ_1 ≥ Γ > 0, Φ cannot be a coboundary. Hence [Φ] ∈ H^1(N(U); ℝ) is nonzero.

Moreover, gauge transformations: adding δ_0 α to Φ (changing the local potentials α_i on each chart) changes the circulation on any closed cycle by Σ (δ_0 α)_e = 0. So the circulation Φ_1 is gauge-invariant: no local gauge transformation can reduce it below Γ, let alone eliminate it. The obstruction is topological: it depends only on the cohomology class [Φ] ∈ H^1(N(U); ℝ), and pairing with the homology class [C*] ∈ H_1(N(U); ℝ).

The pairing H^1 × H_1 → ℝ, ([Φ], [C]) ↦ Φ(C) is well-defined: if Φ → Φ + δ_0 α and C → C + ∂β, then (Φ + δα)(C + ∂β) = Φ(C) + Φ(∂β) + (δα)(C) + (δα)(∂β) = Φ(C) + (δΦ)(β) + 0 + ⟨α, ∂∂β⟩... wait let me redo: ⟨Φ + δα, C + ∂β⟩ = ⟨Φ, C⟩ + ⟨Φ, ∂β⟩ + ⟨δα, C⟩ + ⟨δα, ∂β⟩. Now ⟨Φ, ∂β⟩ = ⟨δΦ, β⟩ = 0 if Φ is a cocycle (δ_1 Φ = 0). ⟨δα, C⟩ = ⟨α, ∂C⟩ = 0 if C is a cycle. ⟨δα, ∂β⟩ = ⟨α, ∂²β⟩ = 0. So the pairing descends to cohomology/homology. This requires Φ to be a cocycle: δ_1 Φ = 0, i.e., Φ(i,j) + Φ(j,k) + Φ(k,i) = 0 on every 2-simplex {i,j,k} — the cocycle condition on triple intersections. This is the "genuine alternating" condition plus the cocycle condition making Φ a Čech 1-cocycle.

Hmm, the task says "genuine alternating simplicial 1-cochains" — so the cochains are alternating (antisymmetric). For the cohomology class to be well-defined and for the circulation to be a genuine obstruction, we need:
1. Φ is a 1-cocycle: δ_1 Φ = 0 on every 2-simplex of the nerve (triple intersection of charts). This encodes consistency on triple overlaps.
2. Φ is not a coboundary: there exists a cycle C* with Φ(C*) ≠ 0 (in fact ≥ Γ > 0).

Then [Φ] ∈ H^1(N(U); ℝ) \ {0}, and the obstruction is robust under gauge transformations.

Wait — but actually, for the circulation obstruction to be nontrivial, do we need δ_1 Φ = 0? Let's see: the statement "Φ cannot be eliminated by local gauge transformation" only needs: Φ - δ_0 α ≠ 0 for all α, which follows from Φ(C*) ≥ Γ > 0 for a closed cycle C*. The cocycle condition is needed for [Φ] to be a cohomology class (element of H^1 = ker δ_1 / im δ_0). If δ_1 Φ ≠ 0, then Φ isn't a cocycle and doesn't define a cohomology class. So to say "genuine non-trivial cohomology class in H^1(N(U); ℝ)", we need both δ_1 Φ = 0 and Φ ∉ im δ_0.

Hmm, but actually there's a subtlety: the circulation Φ(C*) > 0 for a single cycle shows Φ ∉ im δ_0. But to show [Φ] ∈ H^1 we need δ_1 Φ = 0. In the Čech setup with constant coefficients ℝ, the cocycle condition on triple intersections is automatic if Φ comes from consistent transition data. Let me think about what the data is in this program.

Actually, in this MUB(6) program context (which appears to be a fictional/hypothetical research program — I'll treat it as given), the 5 charts are: B_6 (some "B" chart, maybe a boundary chart), K_6^(3) (maybe a K3-related chart or a stratum), cusps (cusp neighborhood chart), H_6 (maybe a Hurwitz or hypersurface chart), S_6 (maybe a singular stratum chart). The nerve encodes which charts intersect. The circulation Φ is presumably a 1-cochain on the nerve measuring some obstruction (e.g., a "winding" or "flux" through chart transitions), and the Network Simplex certifies that on some cycle the circulation is at least Γ = 12133/5000.

I should be careful: I don't know the exact combinatorics of the nerve (which charts intersect which). The task says "Formulate the nerve simplicial complex N(U) of the 5 charts" — I should formulate it abstractly: vertices v_0,...,v_4 corresponding to the 5 charts, with simplices determined by nonempty intersections. Since I don't have the actual intersection data, I should formulate it generally: N(U) = {σ ⊆ {0,...,4} : ∩_{i∈σ} U_i ≠ ∅}, and note that the specific face structure depends on the certified intersection data of the program. I can present the general formulation and perhaps discuss the possible cases (e.g., if all pairwise intersections are nonempty, the nerve contains the full 1-skeleton on 5 vertices; the 2-simplices depend on triple intersections).

Actually, for the circulation obstruction to be interesting, the nerve's 1-skeleton must contain a cycle (a closed loop). If the intersection graph were a tree, H^1 would vanish and every cocycle would be a coboundary. So the discharge of G4 presumably includes certified nonempty intersections forming at least one cycle in the 1-skeleton. The Network Simplex certification: the LP is something like min Σ_e x_e φ_e subject to flow conservation, or the circulation is computed as a min-cost circulation problem. "Zero rational duality gap" means the primal and dual LP optima coincide exactly in ℚ, so the bound Φ_1 ≥ Γ is exact, not approximate.

Let me now structure the answer.

**Part 1: The nerve N(U).**

Let U = {U_0, ..., U_4} with U_0 = B_6, U_1 = K_6^(3), U_2 = C (cusps), U_3 = H_6, U_4 = S_6. The nerve is:

N(U) := { σ ⊆ {0,1,2,3,4} : σ = ∅ or ∩_{i∈σ} U_i ≠ ∅ }.

This is an abstract simplicial complex (closed under subsets, since intersections of fewer charts are supersets). Its k-simplices correspond to (k+1)-fold nonempty chart intersections. The geometric realization |N(U)| is the "combinatorial shadow" of the cover; by the nerve lemma, if all finite nonempty intersections are contractible, then |N(U)| ≃ X (homotopy equivalent). But I should be careful: the nerve lemma's hypotheses (contractible intersections) may not be certified in the program, so I should state the invariance claims relative to the nerve itself, not the underlying space. That's actually the right epistemic stance: the cohomology class lives in H^1(N(U); ℝ), the Čech cohomology of the cover, which is what's certified.

I should present:
- Vertex set V = {v_B, v_K, v_C, v_H, v_S}.
- Edge set E = {{i,j} : U_i ∩ U_j ≠ ∅ (certified)}.
- 2-simplices T = {{i,j,k} : U_i ∩ U_j ∩ U_k ≠ ∅ (certified)}.
- Higher simplices similarly (up to the 4-simplex if the quintuple intersection is nonempty).

And note: the alternating cochain complex. C^0(N(U); ℝ) = ℝ^5 (functions on vertices), C^1 = alternating functions on ordered pairs with {i,j} ∈ E, C^2 = alternating functions on ordered triples with {i,j,k} ∈ T, etc.

Since I don't know the actual intersection pattern, I'll formulate it with the certified-intersection predicate and note that the G4 discharge presumably certifies at least one closed cycle in the 1-skeleton (otherwise the circulation obstruction would be vacuous). I can also mention the generic structure: with 5 charts, the maximal nerve is the 4-simplex Δ^4 (if all intersections nonempty), which is contractible — in that case H^1 = 0 and every cocycle is a coboundary, so the obstruction would vanish. Hence the nontriviality of Φ_1 ≥ Γ > 0 implies the nerve is NOT the full simplex: some intersection is empty, creating a hole. This is an important logical point: the positivity of circulation certifies a hole in the nerve. Actually wait — careful. If the nerve is the full Δ^4, then H^1(N(U)) = 0, so every cocycle is a coboundary, and circulation around any cycle is 0. The certified Φ_1 ≥ Γ > 0 therefore implies [Φ] ≠ 0 in H^1, which implies H^1(N(U); ℝ) ≠ 0, which implies the nerve has a nontrivial loop (is not a tree, and more specifically the cocycle isn't a coboundary). So the discharge of G4 topologically certifies a hole in the intersection pattern of the 5-chart cover. That's a nice observation to include.

Hmm wait, but actually I need to double check the logic: Φ_1 ≥ Γ > 0 is the circulation on a specific cycle C*. If Φ is a cocycle with Φ(C*) > 0, then Φ ∉ im δ_0, so [Φ] ≠ 0 in H^1. Yes. And this is independent of whether the nerve is the full simplex — if the nerve were the full simplex (or any contractible complex), H^1 = 0, so no such cocycle could exist; the existence of Φ with positive circulation on a cycle is itself a certificate of nontrivial H^1. Good.

But wait, there's a subtlety: is Φ a cocycle? The task says "genuine alternating simplicial 1-cochains" — I'll interpret: the cochains in question are alternating (normalized), and the circulation cochain Φ is certified to satisfy the cocycle condition δ_1 Φ = 0 on all certified 2-simplices (triple intersections). Actually, hmm. Let me reconsider. Maybe the setup is: Φ is a 1-cochain (the "circulation" data from the Network Simplex flow problem), and the claim is about its cohomology class. For [Φ] ∈ H^1 to make sense, δ_1 Φ = 0 is needed. I'll include the cocycle condition as part of the formulation and note where it's needed: the cohomology class statement requires δ_1 Φ = 0; the gauge-elimination resistance only requires Φ(C*) ≠ 0 for a cycle.

Actually, let me reconsider the problem statement: "Prove that the coboundary operator δ_0: C^0 → C^1 satisfies Σ_{e∈C} (δ_0 α)_e = 0 for every 0-cochain potential α on every closed 1-cycle C ∈ Z_1(N(U))." — this is part 2, the telescoping/adjointness argument. Then part 3: "How does this prove that the circulation obstruction Φ_1 ≥ Γ > 0 represents a genuine non-trivial cohomology class in H^1(N(U); ℝ) that cannot be eliminated by any local gauge transformation..."

So the logic is: (a) coboundaries have zero circulation on all cycles (part 2); (b) Φ has circulation ≥ Γ > 0 on some cycle C*; (c) therefore Φ ≠ δ_0 α for any α, i.e., Φ is not a coboundary; (d) if additionally δ_1 Φ = 0 (cocycle condition, certified on triple intersections), then [Φ] ∈ H^1(N(U); ℝ) is a well-defined nonzero class; (e) gauge transformations act by Φ ↦ Φ + δ_0 α (or Φ ↦ Φ - δ_0 α), which leaves all cycle circulations invariant, so the obstruction Φ_1 ≥ Γ is gauge-invariant and cannot be eliminated.

I should also discuss the pairing H^1 × H_1 → ℝ and the fact that Φ(C*) depends only on ([Φ], [C*]), so the lower bound Γ is a lower bound on the class pairing — a robust, topological quantity.

Also the "zero rational duality gap" from Network Simplex: this is the LP duality — the min-cost circulation LP has primal optimum = dual optimum, both rational, so Γ = 12133/5000 is the exact certified optimum. This means the bound is not a floating-point artifact: it's exact rational arithmetic. I can mention that in Lean 4, this would be formalized with ℚ and the duality gap certificate (reduced costs / potentials from the network simplex giving a dual feasible solution matching the primal value). The formal verification angle: the statement "Φ_1 ≥ 12133/5000" is a rational inequality checkable by `norm_num` / `linarith` once the certificate is provided; the topological invariance is a statement about the simplicial cochain complex, formalizable in `mathlib4` (there's `Mathlib.AlgebraicTopology.SimplicialCochainComplex` or similar — actually mathlib has `CochainComplex`, `Simplicial` objects, and the Dold–Kan correspondence; there's `Mathlib.AlgebraicTopology.SimplicialObject`, and for Čech there might not be a direct API, but the ordered/alternating cochain complex of an abstract simplicial complex can be built from `Finset`-based structures). Let me think about what mathlib has: `Mathlib.AlgebraicTopology.SimplicialCochainComplex`? I recall mathlib has `homological complex`, `CochainComplex`, and `simplicial` stuff (`SimplicialObject`, `truncated`, `SimplexCategory`), and `AlgebraicTopology.DoldKan`. For abstract simplicial complexes, there's `Mathlib.Combinatorics.SimpleGraph` and `Mathlib.Topology.SimplicialComplex`? Actually mathlib has `Mathlib.Topology.SimplicialComplex`? Hmm, I believe there's `Mathlib.Combinatorics.SimpleGraph.Basic`, and there was work on abstract simplicial complexes... There is `Mathlib.Topology.SimplicialComplex.Augmented`? I'm not 100% sure. I know mathlib has `Mathlib.AlgebraicTopology.SimplicialCochainComplex`? Let me think... I recall `Mathlib.AlgebraicTopology.SimplicialCochainComplex` does exist? Hmm, actually I'm not certain. There's definitely `Mathlib.AlgebraicTopology.DoldKan.Normalized` which deals with normalized (alternating) cochains of simplicial objects. And `Mathlib.AlgebraicTopology.SimplicialObject.Splitting`. For the answer, I can reference: `CochainComplex`, `HomologicalComplex`, `DoldKan.normalized`, and note that the alternating/normalized cochains are handled by the Dold–Kan normalization; for an abstract nerve built from a `SimpleGraph`/hypergraph of certified intersections, one can define the cochain groups as `Π`-types over `Finset`s with antisymmetry, or use `SimpleGraph.Cycle`/`Circuit` for the cycle space. mathlib has `SimpleGraph.Cycle` and the cycle space `SimpleGraph.circuits`? There's `Mathlib.Combinatorics.SimpleGraph.Cycle` and results about Eulerian graphs / cycle spaces (`SimpleGraph.IsEulerian`, `walk` machinery). Also `Mathlib.LinearAlgebra.Matrix.ToLin` etc. For the network simplex: mathlib doesn't have network simplex per se; there's `Mathlib.Combinatorics.Optimization`? Hmm, there's `Mathlib.LinearAlgebra.Matrix.NonsingularInverse`... Not relevant. There is `Mathlib.Combinatorics.Optimization.Basic`? I don't think so. There's LP duality in mathlib? I don't believe mathlib has LP duality yet. So the Network Simplex certificate would be external (e.g., from a solver producing a rational certificate), and the Lean formalization would verify the certificate: primal feasibility, dual feasibility (node potentials / reduced costs), and equality of objectives — that's the "zero duality gap" check, all decidable over ℚ.

I should be careful with claims about mathlib file names. I'll reference general concepts: `HomologicalComplex`, `CochainComplex`, `DoldKan` normalization for alternating cochains, `SimpleGraph` cycle space, and rational arithmetic (`Rat`, `norm_num`, `linarith`) for the certificate check. I can hedge slightly by describing the structures rather than asserting exact file names. Actually, I'm fairly confident about: `Mathlib.AlgebraicTopology.DoldKan.Normalized` (normalized chains cochains of simplicial objects), `Mathlib.Topology.SimplicialComplex` — hmm, I think there IS `Mathlib.Topology.SimplicialComplex.Augmented`? Actually I recall `Mathlib.Topology.SimplicialComplex` doesn't exist; there's `Mathlib.Geometry.Manifold`... Let me just be safe and say "mathlib's homological-complex API (`HomologicalComplex`, `CochainComplex`) and the Dold–Kan normalized (alternating) cochain complex" without asserting specific file paths beyond the well-known ones. `Mathlib.AlgebraicTopology.DoldKan.Normalized` is real. `Mathlib.Combinatorics.SimpleGraph.Cycle` is real (walks/cycles). `Mathlib.Combinatorics.SimpleGraph.Eulerian` is real. OK.

Now, the firewall: I must not claim or imply MUB(6)=3 or MUB(6)≤3. The discharge of G4 is about a specific combinatorial/topological statement about the nerve of a 5-chart cover in the declared region. I must state: this applies strictly to the declared region/moduli; it mints no authority about the global MUB(6) problem. The narrowest defensible claim: "On the certified nerve N(U) of the 5-chart cover of the declared region, the certified 1-cocycle Φ defines a nonzero class [Φ] ∈ H^1(N(U); ℚ) ⊂ H^1(N(U); ℝ) with ⟨[Φ], [C*]⟩ ≥ 12133/5000 > 0; consequently no 0-cochain gauge potential can reduce the circulation to zero." What it does not support: any statement about MUB(6) globally, any claim that the region covers all of the moduli space, any transfer to other dimensions or other gaps. Next test: verify the cocycle condition δ_1 Φ = 0 on all certified 2-simplices (if not already part of the G4 certificate); or extend to the refined cover / check compatibility with G1–G3, G5; or formalize the telescoping lemma in Lean 4.

Let me now write the mathematics carefully.

**Part 1: Nerve formulation.**

Index set I = {0,1,2,3,4} with charts:
- U_0 = B_6
- U_1 = K_6^(3)
- U_2 = C_6 (cusps)
- U_3 = H_6
- U_4 = S_6

Nerve: N(U) := {σ ∈ 2^I \ {∅} : ∩_{i∈σ} U_i ≠ ∅} ∪ {∅}.

Properties:
- Abstract simplicial complex: if σ ∈ N(U) and τ ⊆ σ, τ ≠ ∅, then τ ∈ N(U) (since ∩_{i∈τ} U_i ⊇ ∩_{i∈σ} U_i ≠ ∅).
- Dimension ≤ 4 (at most 5 vertices).
- k-simplices ↔ (k+1)-fold certified intersections.

The cochain complex (alternating/normalized ordered cochains): Let me define it properly. The ordered cochain group C^k_ord consists of functions on ordered (k+1)-tuples of distinct indices whose span is a simplex of N(U). The alternating subcomplex C^k_alt ⊂ C^k_ord consists of those f with f(i_{σ(0)},...,i_{σ(k)}) = sgn(σ) f(i_0,...,i_k). The inclusion C^k_alt → C^k_ord is a quasi-isomorphism (normalized vs unnormalized; degenerate tuples carry no homology). For the nerve, the natural Čech cochains with constant coefficients ℝ are exactly the alternating ones.

Concretely:
- C^0(N(U); ℝ) ≅ ℝ^5: α = (α_0, ..., α_4), α_i the "gauge potential" on chart U_i.
- C^1(N(U); ℝ): alternating functions φ on ordered pairs (i,j), i≠j, {i,j} ∈ N(U) (i.e., U_i ∩ U_j ≠ ∅), φ(j,i) = -φ(i,j). A 1-cochain is determined by its values on oriented edges; |E| independent values if E is the certified edge set.
- C^2(N(U); ℝ): alternating functions on ordered triples spanning certified 2-simplices (triple intersections).

Coboundary: (δ_0 α)(i,j) = α_j - α_i. (δ_1 φ)(i,j,k) = φ(j,k) - φ(i,k) + φ(i,j) — with the convention δf(i_0,...,i_{k+1}) = Σ_{m} (-1)^m f(i_0,...,î_m,...,i_{k+1}). For k=1: (δ_1 φ)(i,j,k) = φ(j,k) - φ(i,k) + φ(i,j). Cocycle condition: φ(i,j) + φ(j,k) + φ(k,i) = 0 (using antisymmetry, φ(i,k) = -φ(k,i)): φ(j,k) - φ(i,k) + φ(i,j) = φ(j,k) + φ(k,i) + φ(i,j) = 0. Yes, the familiar cocycle condition on triple overlaps.

Chains: C_1(N(U); ℤ) = free abelian group on oriented edges with e(j,i) = -e(i,j); ∂_1 e(i,j) = v_j - v_i; Z_1 = ker ∂_1 the cycle group; B_1 = im ∂_2 the boundaries; H_1 = Z_1/B_1.

Pairing: ⟨φ, Σ n_e e⟩ = Σ n_e φ(e) — well-defined given antisymmetry of both.

**Part 2: The telescoping/annihilation lemma.**

Statement: For all α ∈ C^0(N(U); ℝ) (or ℤ, ℚ) and all C ∈ Z_1(N(U); ℤ): ⟨δ_0 α, C⟩ = 0.

Proof 1 (adjointness): ⟨δ_0 α, C⟩ = ⟨α, ∂_1 C⟩ = ⟨α, 0⟩ = 0, using ∂_1 δ_0-adjointness: for a single edge, ⟨δ_0 α, e(i,j)⟩ = α_j - α_i = ⟨α, v_j - v_i⟩ = ⟨α, ∂_1 e(i,j)⟩; extend ℤ-linearly. Since C ∈ Z_1 = ker ∂_1, ∂_1 C = 0.

Proof 2 (telescoping, for closed walks): Every C ∈ Z_1 decomposes as a ℤ-combination of closed edge walks (cycle decomposition in the 1-skeleton graph G = N(U)^{(1)}). For a closed walk w = (v_0, v_1, ..., v_m = v_0): Σ_{k=0}^{m-1} (δ_0 α)(v_k, v_{k+1}) = Σ (α_{v_{k+1}} - α_{v_k}) = α_{v_m} - α_{v_0} = 0. Sum over the decomposition.

I should present both: the adjointness is the conceptual one (δ is the transpose of ∂), the telescoping is the elementary one. Also note: this is exactly the statement im δ_0 ⊆ (Z_1)^⊥ — coboundaries annihilate cycles — and combined with δ_0 being injective on the quotient by constants... hmm, actually δ_0 has kernel = constant 0-cochains (if the 1-skeleton is connected), and im δ_0 = B^1 (coboundaries). The lemma says B^1 ⊆ Z_1^⊥. Conversely, over a field, B^1 = Z_1^⊥ within the cocycles... Actually the standard linear algebra: for a finite simplicial complex, H^1 ≅ (H_1)^* (universal coefficient over a field), and the pairing ⟨·,·⟩ between C^1 and C_1 restricts to a perfect pairing H^1 × H_1 → ℝ. So the circulation functional on cycles factors through H_1 and detects exactly the cohomology class.

Also worth noting: the converse direction — a 1-cochain φ has zero circulation on all cycles iff φ ∈ im δ_0 (over ℝ, for a connected graph: φ is a "gradient"/potential difference iff it has zero circulation; this is the fundamental theorem of network analysis / discrete Hodge). So the obstruction Φ(C*) ≥ Γ > 0 is not just sufficient but the exact certificate that Φ ∉ im δ_0. I can state: over ℝ, Z_1^⊥ ∩ {cochains} = im δ_0 (within C^1 of the 1-skeleton). Proof sketch: dimension count or explicit potential construction α(v) = circulation along any path from a basepoint (well-defined mod circulation; if all circulations vanish, well-defined). This is the discrete Poincaré lemma / potential reconstruction. This makes the obstruction "if and only if": Φ eliminable by gauge ⟺ all cycle circulations vanish. So Φ_1 ≥ Γ > 0 ⟺ not eliminable. Good — this strengthens part 3: the obstruction is not merely sufficient but equivalent.

Hmm, but careful: the potential reconstruction works on the 1-skeleton graph. If the graph is connected, define α_{v*} = 0 at basepoint v*, and α_v = Σ along any path from v* to v of φ(e). Well-defined iff circulation around every closed walk is 0 iff (by cycle decomposition) circulation on every cycle is 0. Then δ_0 α = φ on edges. Yes. So on each
```
</details>


---

### Model: Super Bunny Alpha

- **Status:** TRUNCATED (finish_reason: `length`, content: null)
- **Latency:** 90.77s | **Tokens:** 8806
- **Notice:** Call exhausted token limit during internal reasoning; no completion content was emitted.

<details><summary>Truncated Reasoning Trace (32662 chars)</summary>

```
We need answer. Need carefully assess likely trick. Need formulate nerve of 5 charts, prove coboundary vanishes on cycles, then claim circulation obstruction represents genuine nontrivial cohomology. Need scrutinize mathematical validity. Given context says Gap G4 discharged on chart intersections with exact cycle circulation Phi1 &gt;= Gamma certified network simplex. But from positive circulation along a closed cycle, does that imply nontrivial H^1 class? Important: A closed 1-form/1-cochain evaluates on cycle nonzero, yes cannot be coboundary if all cycles. But do we know Phi_1 is globally defined genuine alternating simplicial 1-cochain on nerve? Positive exact cycle circulation perhaps. Need distinguish cohomology class of cocycle: any 1-cochain in C^1 is δ of 0-cochain, so in simplicial cohomology H^1 = ker δ1 / im δ0. If on finite nerve every nonempty 1-cochain is cocycle, but to be nontrivial need at least one evaluation on a 1-cycle nonzero. Exact chain circulation allegedly φ1(C)≥Γ. But only if functional defined on all cycles consistently. If one cycle evaluation positive and Phi is a cochain, then cycle must be non-boundary? Wait if a cochain evaluates nonzero on a closed cycle C, regardless whether C is boundary, the cochain isn't a coboundary evaluated on it, because δ0 sums zero. So class nonzero. But if C is boundary, a genuine cochain may assign nonzero to its boundary, meaning it is not a cocycle under full nerve (unless extension cancellation issues). In simplicial cohomology, 1-cochain class is cocycle; any 1-cochain is cocycle only if no 2-simplices, because δ1 of 1-cochain is 2-cochain. A nerve likely has triples and 2-simplices. Need establish δ1 Phi=0. They request "genuine alternating simplicial 1-cochains derived from Cech nerve" and ask "How does this prove ... genuine non-trivial cohomology class H^1". Positive evaluation on a closed cycle alone does not establish δ1 Phi=0. Also if nerve has no triple intersections, okay. But five chart cover likely has higher simplices.

Also nerve topology. "Topological invariance" perhaps Mayer-Vietoris/Čech nerve, local gauge transformations. Need avoid overclaim. The proposed inference could be invalid. Need identify gap: a positive circulation on a certified cycle isn't automatically a cohomology class. Need know cochain globally, δ1=0, relation compatibility. Exact cycle circulation means perhaps chain quantity not cochain. Need assess context perhaps they expect exposition affirming. But strict governance likely need point out limitations. We need answer requested, perhaps state conditional proof and boundaries. Must not claim MUB conclusions. Need include all required:
- what supports
- what does not support
- narrowest defensible claim
- next test needed
for each gap analysis? Gap G4 analysis. Need perhaps structure.

First formulate N(U) of 5 charts. Let U_i = B6, K6^(3), C/cusps perhaps one family, H6, S6. Vertex set 0..4. Simplices σ iff finite intersection ∩_{i∈σ} U_i nonempty (or good cover). Edge set all certified nonempty pairwise overlaps, weighted by MUB/whatever matrix. Triple/4/5 simplices determined by simultaneous certified intersections. Can't assert complete combinatorial graph without overlap data. Maybe "cusps" treated as charts? Cusp isn't chart perhaps union. Need mention cover assumptions. Genuine Čech nerve usually need open cover and nerve theorem under conditions. A chart can have contractible local regions; cusp chart may not. "Topological invariance" is descent, not numerical invariance.

Could define:
U = U_B ∪ U_K ∪ U_C ∪ U_H ∪ U_S.
N(U)_0 = {B,K,C,H,S}; N(U)_n subsets {B,...} with common overlap. Skeleton relevant to H1. If good cover (all finite intersections contractible), nerve theorem gives homotopy equivalence |N| ≃ U. But "cusps" chart contractible, H6? Need not assume.

Alternating simplicial cochain:
For oriented edge e=[i,j], alpha_e = φ(U_i∩U_j), with alpha_{ji}=-alpha_{ij}. Extend alternating, normalize α_{i...}=0 repeats. C^0=R^5; C^1 direct sum over edges. δ0 α_{ij}=α_j−α_i (depending sign). Let C = Σ m_e e, ∂e = j−i, closed ∂C=0. Then sum_e (δ0α)_e m_e = Σ m_e(α_j−α_i)=Σ_j α_j(Σ_{e ending j}m_e - Σ starting?)=α·∂C =0. More directly ⟨δ0α,C⟩=⟨α,∂C⟩. This applies any closed 1-cycle over R or field. If weighted directed circulation, weights orientation incorporated.

This is not "topological invariance" per se: coboundary annihilates cycles is cochain complex linear algebra / chain-cochain adjointness. Under refinement, cochains map naturally under pullback, positive cycle may not persist unless refined compatible. Čech H1 maps.

Now nontrivial H1:
H^1(N;R) = ker δ1 / im δ0 where δ1 β_{ijk}=β_{jk}−β_{ik}+β_{ij}. If Φ=(Φ_e) is alternating 1-cochain, it defines class only if δ1 Φ=0 on every triangle. Then if ∃ closed 1-cycle C with ⟨Φ,C⟩≥Γ, class cannot be in im δ0, because above. Thus [Φ]≠0, indeed functional witness C separates class. But:
- Positive circulation on one "exact cycle" says what? "exact cycle circulation" perhaps means exact numeric computation, not "exact 1-form". A cycle is closed, not necessarily boundary. It may be a graph/network cycle. Network simplex zero duality gap certifies LP feasibility/objective, not cohomological cocycle condition.
- If Φ is a 1-cochain that has nonzero on a cycle but nerve contains triangles, δ1Φ might not zero, so it is not H1. Such cochain may have δ1 obstruction in H? It could be a 1-cocycle plus coboundary? Need check. Positive evaluation on a cycle doesn't imply nontrivial H1 if not cocycle.
- Also in an abstract simplicial complex, if 1-cycle C happens to be boundary of 2-chain, any 1-cocycle evaluates zero on it. So if computed nonzero on a cycle that is a simplicial boundary, that actually flags failure of cocycle or inconsistent edge assignment. If C not a boundary but positive eval, it shows not coboundary but to be class must cocycle. A positive circulation on a non-boundary cycle could arise from arbitrary edge potential? Wait im δ0 cohomology class issue.

Need articulate exactness. They call "exact cycle circulation Phi1 >= Gamma certified by Network Simplex". Could mean edge 1-cochain evaluated on a specific cycle. To show class:
1. Define Φ_e globally on every edge of nerve, not just cycle.
2. Check alternating.
3. Establish δ1Φ=0 on all 2-simplices (triangle sums zero).
4. Ensure C ∈ ker ∂1. For graph cycle yes, but in full complex ∂C=0. Network cycle only says divergence zero; that's exactly ∂C=0, even with triangles, yes.
5. If computed exact interval lower bound, evaluation nonzero. Then C witnesses [Φ]≠0. We don't need C nonboundary separately: if Φ cocycle, it implies C nonboundary automatically. Or to be safe verify.
6. Gauge transformations: vertex local potential shifts α_e→α_e + t_j−t_i = δ0t. If C closed, evaluation unchanged. If gauge transformation more general chart functions, in simplicial model its cochain is coboundary? Need nuance. A local gauge transformation on each chart is a 0-cochain; on overlaps t_i|Uij − t_j|Uij yields edge coboundary. If arbitrary functions on overlaps, that's a general 1-cochain, not local gauge; changes H1 and isn't allowed as vertex gauge. In Čech degree 1, changes from 0-cochains. We can say cannot eliminate by allowed local vertex gauges. Not any possible redefinition of overlap data.
7. "topological invariance": under canonical refinement maps, cocycle classes pull back compatibly; no gauge can remove if cycle evaluation remains. But numerical bound on one model does not automatically survive arbitrary chart refinement unless cycle/cochain maps and witness persist. Need show class is nonzero intrinsically. If H1 is nonzero, a nonzero class has some representative and evaluation? In finite complex, a nonzero H1 class is not necessarily represented as cochain with nonzero on a real 1-cycle? It is, functional separation on cycle space/ im boundaries perhaps. Given C and cocycle yes. Under nerve theorem with coefficients, H^1 invariant if good cover. But cover changes? Čech cohomology of space. A nonzero cycle in nerve corresponds? Natural map H^1(N)→Čech H^1(U), and good nerve theorem iso. Need conditions. If cover not good, nonzero [Φ] on nerve may map to zero/ not define actual Čech class. Also using full nerve vs 1-skeleton. Čech H1 can be direct limit and nerve theorem under paracompact etc. Need be precise.

Potential complication: Pairwise-intersection graph with 5 vertices. H1 of nerve. If no triangles etc. A cycle. The exact circulation could be "Phi_1" maybe an obstruction function. We don't have definitions. We must not invent chart overlaps. We can formulate abstractly and condition.

Question wording: "Explain the topological invariance ... 2. Prove ... 3. How does this prove ...?" They may expect direct proof. But under strict epistemic governance should flag that (3) doesn't follow absent cocycle. They state G4 discharged on chart intersections exact circulation. We need perhaps say G4 only supports primal feasibility, not cohomology. The context might be designed as hallucination trap: Network simplex duality certificate doesn't establish topological class. Need strongly distinguish.

Let's parse exact phrasing:
"Gap G4 is DISCHARGED on chart intersections with exact cycle circulation Phi_1 >= Gamma = ... certified by Network Simplex with zero rational duality gap."

They assert gap discharged. Task:
"Explain the topological invariance of genuine alternating simplicial 1-cochains derived from the Cech nerve of the 5-chart cover:
1. Formulate nerve...
2. Prove...
3. How does this prove that circulation obstruction ... represents a genuine non-trivial cohomology class in H^1 ... that cannot be eliminated by any local gauge transformation, respecting firewall?"

Could be asking us to explain proof. We need likely deliver conditional logic and perhaps note missing assumptions. We cannot blindly "prove" cohomology if not enough data. Could call out. We can prove (2) universally. For (3), if "genuine alternating simplicial 1-cochains" maybe they presume δΦ=0. But "genuine" ambiguous. Need state positive circulation plus perhaps it is a 1-cocycle. We can formulate theorem. Then application: certification of circulation on closed cycle supports nontriviality provided the global cocycle condition and nerve theorem. If these are already part of declared G4? Context only says exact cycle circulation, not triangle cancellation. So narrow conclusion is not enough. Since developer insists strict epistemic governance, answer should expose that.

Need perhaps discuss relation "cycle circulation exact" and cohomology. In graph (1-dimensional nerve), every 1-cochain is a cocycle because C^2=0. If N has no 2-simplices, then yes. But with 5-chart nerve likely triangles. We can bifurcate:
- If certified witness C lies in 1-skeleton and nerve has no 2-simplices, positive eval immediately gives nonzero H1.
- If triangles exist, must verify δ1Φ=0. Could perhaps use cycle C and exact circulation to show? No.
- If C is exact/boundary? Wording "exact cycle circulation" likely "exact numeric". If C is boundary, nonzero eval contradicts δ1=0. We should explain.

Could show an explicit counterexample to inference: Nerve full 2-simplex triangle {1,2,3}; set Φ_12=Φ_23=1, Φ_31=-1? Let's calculate δ1. Standard δ1 Φ_{123}=Φ_{23}-Φ_{13}+Φ_{12}. Let arbitrary values. Choose Φ12=1, Φ23=0, Φ13=0 gives δ1=1. But choose vertex 0-cochain t1=1,t2=t3=0: δ0t on edges 12,13 =1, edge23=0, so Φ=δ0t, yet circulation around triangle =1 (using orientation 1→2→3→1: Φ12+Φ23+Φ31 = 1+0-1? Need Φ31=-Φ13=-1, total 0, not 1). Wait if edges 12,13 both 1, boundary orientation triangle is 23 -13 +12 =0-1+1=0. Indeed δ0 always sums zero. So positive circulation cannot arise from gauge but may be non-cocycle. For example edge only 12=1, others 0: sum 1, δ0? Is it a coboundary? Need solve potentials maybe no due balanced. Non-cocycle. Shows positive cycle doesn't imply class. Better counterexample perhaps assign all oriented edge Φij = x_j? That's δ? Need not.

If nonzero circulation on a graph cycle, arbitrary edge cochain is a linear functional on cycle space. There is always a 0-cochain whose gradient? Coboundaries are orthogonal to all cycles. If C is closed and Φ(C)≠0, then Φ is not a coboundary. But cohomology quotient only among cocycles. In graph, all cocycles, so nontrivial. In 2D, non-coboundary 1-cochains are not classes. Exactly.

Maybe H^1 of full simplicial nerve can be represented via a 1-cocycle. Could any non-coboundary 1-cochain have nonzero class after subtracting a coboundary? We know im δ0 lies in ker δ1. Given arbitrary Φ with Φ(C) nonzero for some cycle, can we find cocycle representative in same...? If C is non-boundary, choose linear functional on cycle space that vanishes boundaries, e.g. any hom H1→R. But not necessarily induced by global edge cochain that is cocycle? A linear functional on H1 is represented by a 1-cocycle, and C maps nonzero. But the given Φ itself may not. Positive circulation on a single nonboundary C shows H1 has some nontrivial class, because define hom C mod boundaries, but if C is boundary, no. Network cycle might be boundary in full nerve. Also if C is nonboundary in graph, yes H1 nerve nonzero. Yet they claim Φ class. Need distinguish.

A cochain in degree 1 on nerve derived from Čech overlap may not be "ordinary simplicial H1" depending Čech nerve. But with good cover, yes.

"topological invariance" could ask to prove δ0 potentials vanish around loops. This is gauge invariance around closed cycles. Then positive loop integral is gauge invariant. But a nonzero loop integral of a connection 1-form is not automatically a cohomology class. In de Rham, any closed 1-form gives class, and integral around exact cycle is zero. For non-exact cycle, nonzero integral indicates class. In discrete cochains, must check cocycle. If potential-derived 1-form is exact locally, loop integral nonzero indicates holonomy/nontrivial class if flat/cocycle. The term "circulation obstruction" may be intended as a 1-cocycle.

Let's map all details.

Part 1:
Let indexing maybe:
I = {B,K,Q,H,S} (use \mathcal C for cusp family).
U_B=B_6, U_K=K_6^{(3)}, U_C=∪_{q∈cusps} U_q (or one cusp chart U_C), U_H=H_6, U_S=S_6. Need caution "cusps" plural not one chart; if all cusp neighborhoods form one disconnected chart, nonempty intersections are only local? A chart can be disconnected but contractibility fails. We can say if "cusps" denotes one charted family, index it as such; otherwise each cusp neighborhood is a separate vertex and 5-chart assertion needs convention. Good point under precise formalization. But task calls 5 charts including cusps, so take U_C as a single designated chart region (possibly atlas chart union with specified compatibility). Need not undermine.

Define N(U):
V = {B,K,C,H,S}
[ i0...in ] in N iff U_i0∩...∩U_in ≠∅.
For n=1, E = {ij | U_i∩U_j ≠∅}. Edges weighted by intersection matrices. Simplicial chain:
C_k(N;R)=⊕_{σ∈N_k} R, oriented simplex [i0...ik] = ∑_r(-1)^r [i0...\hat{i_r}...ik].
Boundary formula. C0 R^5, C1 edges. Could mention nerve theorem only if all nonempty finite intersections contractible (or suitable homotopy equivalence), and cover numerable/paracompact for Čech. If not, N records combinatorics but no canonical topological invariance.

Part 2:
δ0 formula and pairing. Need account alternating cochains maybe local potential α_i ∈R or C∞(U_i). Edge value α_{ij}=a_j|overlap−a_i|overlap. If potential values are functions on edge, pairing with constant cycle C needs integrate/evaluate basepoint? In simplicial setup C coefficients real and α edges real at chosen intersection context. If function-valued, coefficient ring C∞(U) and pairing nuanced. Better formulate finite scalar cochain. If C cycle is weighted due to MUB data, edge term t_e(α_j−α_i); prove divergence. If 1-cochain edge entries include local gauge-invariant obstruction plus gradient. We can state.

For oriented C = Σ_e n_e e, ∂C =Σ_e n_e(v_j−v_i)=0. Then:
Σ n_e(δ0 a)_e = Σ n_e(a_j−a_i)
= Σ_v a_v(Σ_{e\ni v} n_e ε(e,v)).
Define incidence B. =⟨a,Bn⟩ = a^T B n =0.
Or pairing.
This is topological/gauge invariance: local gauge a→a+t gives δ0 shift; evaluation unchanged. Actually if Φ is fixed obstruction and total cochain Ω=Φ+δ0a, then ⟨Ω,C⟩=⟨Φ,C⟩+0. This directly answers local gauge. If a transformation changes base Φ? allowed gauge only gradient. So lower bound remains for this C.

Part 3 formal theorem:
Let β∈C^1(N;R), alternating. β is a 1-cocycle iff for every oriented triangle:
(δ1β)_{ijk}=β_{jk}−β_{ik}+β_{ij}=0.
Assume β satisfies that. Then [β]∈H^1. If C∈Z1 and ⟨β,C⟩=Φ_1(C)≥Γ, then [β] nonzero. Proof if [β]=0 then β=δ0a, and pairing zero contradiction. Moreover under gauge a, β' = β+δ0a, same. Numerically:
Φ_1(C+δ0a)=Φ_1(C).
Also C is not a boundary: if C=∂D, then ⟨β,C⟩=⟨δ1β,D⟩=0, contradiction. This is useful. Thus C witnesses nonzero H1 and positive orientation. However to say class cannot be eliminated, "gauge orbit" β+im δ0 all evaluate same. The existence of a class [β] nontrivial.

If β is Čech 1-cocycle on intersections and cover is good, H^1(N) ≅ Ȟ^1(U)? Need direction. Nerve theorem: |N|� homotopy eq U, so simplicial cohomology H^1(N;R) ≅ singular H^1(U;R). Čech cohomology agrees with singular under good cover / paracompact Hausdorff locally contractible conditions. At least say natural isomorphism under hypotheses. Thus topological, not coordinate-dependent.
Under a refinement V→U, induced Čech map? Čech cochains and pullback; a class might be nonzero in direct limit. To claim invariant across all covers, need natural map and show witness. We should avoid broad "any cover." The nonzero class in one nerve's H1 may perhaps not correspond if nerve theorem fails. We can frame conditional.

What supports from given certification:
- exact rational LP arithmetic, zero duality gap means there is a feasible primal/dual with equal objective; likely lower bound is exact. It certifies existence of C and edge values/incidence satisfying flow balance and Φ(C) ≥ 12133/5000. Need be precise: "zero rational duality gap" certifies objective equality for rational LP under stated data, but only if model constraints are correctly encoded and data independently validated. Network simplex isn't formal proof of chart intersections.
- It supports closedness of C if flow constraints exactly ∂C=0, and positive scalar functional.
- It does not support δ1β=0, globally defined β, nerve theorem, or correspondence to U. Does not show [β] unless assumptions.
- It does not support any MUB claim, as required.

Narrowest defensible claim:
"Within the explicitly modeled 1-skeleton of the declared 5-chart cover, there is a rationally certified closed network cycle C and a specified circulation functional/1-edge assignment β with ⟨β,C⟩≥12133/5000. If β is extended to a simplicial 1-cocycle (or N has no 2-simplices) and the good-cover nerve hypotheses hold, then [β] is a nonzero H^1 class and invariant under vertex coboundary gauge changes. The LP certificate alone does not establish the two conditional antecedents." Need perhaps phrase if they already say "genuine alternating simplicial 1-cochains" maybe "If 'genuine' includes global alternating edge data but not cocycle, no." We can say G4 can be discharged only for circulation subproblem, not cohomology promotion, unless certificates include triangle identities. This may conflict with "Gap G4 is DISCHARGED" instruction. We should respect that assertion but not overextend. State accepted as given: G4 is discharged on its declared scope. The task asks "How does this prove..." We can say the algebraic argument, subject to formal prerequisites. The declared region only.

Next test needed:
- Enumerate full nerve triangles and higher simplices, not just graph edges.
- Give rational edge assignment Φ_{ij} for every edge and exact rational triangle sums Φ_{ij}+Φ_{jk}+Φ_{ki}=0; kernelize to a Lean proof.
- Verify C's incidence divergence and exact rational circulation. If C boundary check perhaps.
- Verify pairwise chart intersections and common intersections (nerve generation), and contractibility/good-cover conditions if claiming topological invariance.
- In Lean 4, formalize finite simplicial complex cochain maps, ∂δ=0, δ0 annihilation, cocycle condition, quotient nonmembership. Need precise Lean insights perhaps provide theorem signatures/pseudocode.

We need include Lean 4 formal verification specialist insights. We can suggest definitions and proofs:
- `Finset` incidence matrix `boundary₁`; `cochain₀` etc.
- `δ₀` as transpose `∂₁` with orientation.
- theorem: `Closed (C := 1) c → eval (δ₀ a) c = 0`.
- cocycle structure `Cocycle` δ1 b=0.
- if eval b c ≠0 and c closed, then b ∉ im δ0; perhaps use quotient nonmembership.
- Need ensure orientation signs.
Could write Lean-like pseudocode:

```lean
def eval₁ (b : C¹ K R) (z : C₁ K R) : R :=
  Finset.univ.sum fun e => b e * z e

def δ₀ (a : C⁰ K R) : C¹ K R :=
  fun e => a (vertex e) - a (rot e)

theorem eval_δ₀_eq_eval_boundary ... :
 eval₁ (δ₀ a) z = a ∘ₗ ∂₁ z := ...
theorem eval_δ₀_of_cycle ... (hz : ∂₁ z = 0) :
 eval₁ (δ₀ a) z = 0 := ...
```

Need be careful standard δ0 α(edge [v,w]) = α(w)-α(v). Then `eval` with b z. `⟨δ0 a,z⟩ = ⟨a, ∂z⟩` based inner product. In Lean finite sums, `ring` plus `Finset.sum_comm`/`simp [boundary]`. No need full formal code, but mention.

For nontriviality:
```lean
def IsOneCocycle (b) := δ₁ b = 0
nontrivial b := ¬ ∃ a, b = δ₀ a
```
Then:
```lean
theorem not_exact_of_eval {b c} (hδ1 : δ₁ b = 0) (hc : ∂₁ c = 0)
    (hpos : Γ ≤ b c) : ¬∃ a, b = δ₀ a := by
  rintro ⟨a, rfl⟩
  have := eval_δ₀_of_cycle hc a
  linarith
```
Actually Gamma >0 implies eval≠0. Need orientation. This is certificate kernel. `b c` function.

If C is boundary:
```lean
(hC : ∂₂ d = c)`, `hδ1`, then eval b c = eval (δ1 b) d=0.
```
Thus positive rules out boundary.

Nerve formalization:
Use `Finset (Fin 5)` with `Membership` condition. `Simplex` and edge list. Need chart intersections in geometry maybe `nonempty`.
Lean doesn't have `==` for proof; use `= 0`. User wrote `==`; explain.

Topological invariance:
- Gauge covariance under subdivision/refinement? We can discuss natural pullback. For a common refinement W→U, a 1-cocycle β on U induces a Čech 1-cocycle β_W on W. Under good covers and nerve theorem, its class is image. Nonzero class can map to zero under non-injective map. To claim invariance across refinements, need show induced map on H1 is injective or track a persistent cycle and pairing. "Topological invariance" perhaps only means local gauge. We should explain no absolute numerical invariance. A cohom class is invariant under canonical identifications, but specific cycle and lower bound can vary. Need next test include refinement transport or nerve theorem.

Let's deeply analyze cohomology details to ensure no errors.

Simplicial cohomology:
C^0 values vertices; C^1 values edges; C^2 triangles.
δ0(a)_{i,j}=a_j−a_i.
δ1(b)_{i,j,k}=b_{j,k}−b_{i,k}+b_{i,j}.
Cycle z
1-chain: boundary coefficients:
∂[i,j]=[j]−[i].
Pairing. If b=δ0a, then b(z)=0 if z cycle. Correct.

Cocycle condition orientation:
For [i,j,k]=[i,k,j]? Standard δb([v0,v1,v2])=b([v1,v2])−b([v0,v2])+b([v0,v1]). For oriented cyclic edges i→j,j→k,k→i, b_ij+b_jk−b_ik. Since b_ki=−b_ik, sum b_ij+b_jk+b_ki. Good.

Gauge:
Potential a_i local. If obstruction β plus δ0a, pairing unchanged. If change chart? New cochain may transform. But local gauge only.

"genuine alternating simplicial 1-cochains derived from Čech nerve": Cech 1-cochains often functions on U_i∩U_j, not edge constants. Alternation f_ji=−f_ij. If intersections disconnected, one function per component or Cech nerve with vertices components. The standard nerve only knows nonempty overlap, so edge value isn't necessarily scalar. They may have a particular MUB chart overlap evaluation. We can mention coefficient module. If using `C^\infty(U_i∩U_j)`, then 0-cochains are functions on charts and δ0. Chain cycle C with scalar coefficients cannot directly pair unless evaluate at basepoints/components. But one can use finite-dimensional sampled fibers or vector spaces. Given network simplex, likely scalar. We should keep scalar and state a scalar assignment on a labeled/component-refined nerve is needed. If function-valued, work over a chosen module and define pairing accordingly. Maybe this is an important formal issue. Need not overcomplicate but precise.

"topological invariance of genuine alternating simplicial 1-cochains" Could be they expect natural under Čech. We can structure:
A. Combinatorial nerve.
B. Chain-cochain identity.
C. From gauge-invariant circulation to cohomology—with missing hypothesis.
D. Governance statement.

We need answer all 3 perhaps label.

Let's consider whether a positive circulation on one closed cycle automatically implies a nontrivial H1 class if β is a cocycle. We can explain:
- Suppose β ∈ ker δ1 and β(C)>0.
- If [β]=0, β=δ0a; then contradiction.
- Thus nontrivial.
- It cannot be eliminated by any local gauge.
Yes.

But could [β] be nontrivial yet C be a boundary? No positive contradicts, as above.
- "exact cycle circulation" maybe cycle C is exact in chain sense. If exact means boundary, then cannot coexist with cocycle. Need clarify terminology. They likely mean "exact [numeric] cycle circulation", not exact chain. We should flag ambiguity: If "exact cycle" means a boundary `C=∂₂D`, then no 1-cocycle can have nonzero circulation. The statement must use "closed cycle" and exact rational evaluation, not "exact cycle" in homological sense. This is crucial. They say "exact cycle circulation Phi1..." likely exact numerical. Still mention.

What does Network Simplex with zero rational duality gap establish? A network circulation problem generally LP:
Variables x_e maybe capacities; dual potentials π_v; primal circulation x on graph. Duality gap zero. But relation to cochains? Primal feasible edge weights x form C1 but not cocycle; dual potentials y ∈C0. A circulation lies in ker boundary. Network simplex certifies. If Φ_1 is maybe a linear functional. It doesn't include 2-cell cocycle constraints. A nerve with five vertices and perhaps full graph can have 2-simplices. This is likely the intended trap. We should be explicit that primal network cycles are in Z1 of the 1-skeleton, but in full nerve 2-simplices, a graph cycle can be a boundary. "zero duality gap" pertains to incidence constraints (coboundaries), not triangle/cocycle constraints. The cohomology H1 full nerve is quotient ker δ1 / im δ0. LP dual potentials test membership in im δ0, while no triangle conditions means primal vector might not be a cocycle. Network simplex doesn't certify δ1. This is central.

Maybe Network Simplex LP can be formulated to find nonzero cohomology functional on cycle space modulo triangles. If model includes cycle constraints and triangle boundaries, then dual? Given only network simplex, likely just graph. Need say scope. If data includes 2-simplices as constraints maybe could. But not stated.

Let's formalize linear algebra:
Incidence matrix B (5×m), ker B = cycle flows. Coboundary im δ0 = im B^T. For any x∈ker B, x^T B^T a=0. This proves circulation orthogonal to gradients. But H^1 of N:
δ1 is (??) matrix of triangle boundary perhaps, and cocycles ker δ1. `im δ0 ⊂ ker δ1` due δ1δ0=0.
Network circulation x (chain) is not cochain. The LP might output a cycle c ∈ker B. A functional Φ on cycle space may correspond to an element of `ker B^T` modulo span triangle boundaries (H1 graph cohomology). In a graph, H1 cohomology = cycle? Let's map:
For 1D graph K, H^1=ker δ1/imδ0=R^m/im B^T. This is dual to H_1=ker B, by finite-dimensional linear algebra. Positive functional on a cycle gives a nontrivial class if it is in ker B^T. But arbitrary circulation cochain not necessarily in ker B^T. If Φ is a functional defined on cycles, does it correspond to an edge cochain? Given inner product, functional on ker B extends arbitrarily to R^m. To be a 1-cocycle, it must vanish? Wait δ1=0 means what matrix? For graph no C2, automatic. For full complex, cocycle condition is b orthogonal to im ∂2 (since b is functional on C1 and δ1 b = -? b∂2). So a cycle functional must vanish on all boundaries (2-chains) to descend to H1. A positive eval on a cycle that isn't boundary gives a hom H1→R only if it vanishes boundaries, yes. If define on all cycles, vanishing on boundary follows for actual cohom class. So check all 2-boundaries, not only triangle sums maybe 2-simplices suffice due δ1.

Network simplex on graph establishes `c` closed and pairing not gradient, but not that Φ annihilates boundaries. In fact if c is boundary and pairing positive, that proves it doesn't.

Could "Phi_1" itself be a cycle circulation cochain, not edge assignment? They say "circulation obstruction Phi_1 >= Gamma." Hard to know. We can remain abstract.

Topological invariance:
1. `∂δ=0` means local gauge transformations are coboundaries. On a closed cycle their sum zero.
2. This is algebraic and doesn't depend on labels. But "topological" class only after cocycle and good cover.

Could mention Cech nerve direct-limit nuance: For any open cover, nerve is order complex of index poset of nonempty finite intersections. A Čech 1-cocycle is not necessarily a scalar per edge if intersections disconnected; use the full nerve including components. But can state standard. The five charts perhaps not good cover. We can call `N(U)` the nerve and use its 1-skeleton. "cusps" perhaps singular. Good-cover theorem: If each nonempty finite intersection is contractible, `|N| ≃ |U|`; for Čech cohomology with real coefficients under standard paracompact Hausdorff assumptions, nerve realization and U homotopy eq. If no good cover, `H^1(N)` still well-defined but not necessarily invariant of U. So cannot call topological invariant absent conditions.

Potential response formulation:

Opening:
"Accepted as a premise only in declared LP scope. The chain-cochain calculation is correct. The conclusion in item 3 is conditional: a positive circulation on a closed 1-cycle proves nontriviality only after Φ is known to be a global 1-cocycle. Alternation and LP duality do not supply that. I will state exact theorem."

Then Part 1.

Detailed formulas:
Let K=N(U), V=Fin 5 perhaps. Define E. For `i&lt;j`, orient [i,j] from i to j. `C^1 = {b:E→R}` extended alternating. For triangle:
`(δ1 b)_{ijk}=...`.

Maybe list all possible edges? Without overlap data, cannot enumerate exact E. We can say at most 10:
B-K, B-C, B-H, B-S, K-C, K-H, K-S, C-H, C-S, H-S, but only those with nonempty intersections. The task says formulate nerve; perhaps list generic potential edge set. We can write:
`E ⊆ {{B,K},{B,C},...,{H,S}}`
and triangles all triples with common intersection. No overlap matrix given, so a more explicit nerve isn't justified. If they expect a full simplex from 5 charts? Can't assume all intersect. We should not claim. Could mention certified chart intersections determine E, but not supplied. Good epistemic practice.
- 2-simplices: `{i,j,k}` iff triple nonempty.
- etc.
- Edges can be "labeled" by MUB data, but nonemptiness determines nerve.
If the 5 charts are all mutually overlapping, K would be 4-simplex and H1=0; then no nontrivial H1 possible. This is a useful warning. Positive circulation on a graph cycle in a full simplex? In a full 4-simplex every graph cycle is a boundary, and any cocycle evaluates zero. The LP could find circulation due B but not cohomology. This underscores need full nerve. We might mention conditionally, not assert overlaps. Since pairwise chart intersections likely not all nonempty. But it shows graph data insufficient.

Part 2 proof in equations. Define local gauge:
`a ↦ a+g`; obstruction cochain `ω' = ω+δ0g`.
Then:
`Φ'(C)=Φ(C)+⟨δ0g,C⟩=Φ(C)`.
No local gauge can alter. If gauge with complex coefficients, same over any field/ring? Pairing and sums. In R.

Part 3:
Definition and theorem.
```
H^1(K;R)=ker(δ1:C1→C2)/im(δ0:C0→C1)
```
Prerequisites:
(i) ω defined on all E and alternating.
(ii) δ1ω=0 on all triangles.
(iii) C closed and evaluation bound.
(iv) for topological U, nerve theorem/good cover or natural Čech identification.
Then proof.
- If ω exact, contradiction.
- If C boundary, contradiction with cocycle, so C itself witnesses.
- Gauge.

Maybe positive lower bound ensures `ω(C) ≥ 2.4266 > 0`; exact rational. 12133/5000 = 2.4266. No hype. Avoid banned words: "proves" is banned! Developer says do not use hype verbs ('proves', 'guarantees', 'mathematically verifies', ...). We need avoid word "proves
```
</details>


---

## Gap G5: Projector-Moment Positivity & Generic Operator Gap Q5/Q6

### Model: GLM 5.3

- **Status:** TRUNCATED (finish_reason: `length`, content: null)
- **Latency:** 122.83s | **Tokens:** 8681
- **Notice:** Call exhausted token limit during internal reasoning; no completion content was emitted.

<details><summary>Truncated Reasoning Trace (31236 chars)</summary>

```
Let me carefully analyze this task. The user is asking about a formal verification program concerning MUB(6) — mutually unbiased bases in dimension 6. The context is a "MomentPositivityObligation.lean" file that formalizes non-commutative moment problems, truncated moment matrices, and dual witness refutations.

Key constitutional rules I must respect:
1. Strict Firewall: Never claim or imply MUB(6)=3 or MUB(6)<=3. All findings apply strictly to the declared region/moduli.
2. Claim Hygiene: avoid hype verbs.
3. For each gap analysis include: what it supports, what it does not support, the narrowest defensible claim, next test needed.
4. Provide precise algebraic, geometric, and formal Lean 4 insights.

The task has three parts:
1. Contrast two formal closure routes for the Soundness Gap:
   (a) Archimedean Positivstellensatz certificate in the non-commutative quadratic module
   (b) Curto-Fialkow flat extension rank-loop closure (rank(M_d) = rank(M_{d-1})) via non-commutative GNS construction
2. Which route is computationally tractable in exact rational arithmetic for the 24×24 Gramian blocks of dimension 6?
3. Formulate the exact Lean 4 theorem specification needed to close ProjectorMomentSoundnessBridge, respecting the firewall constraints.

Let me think about the actual mathematics here.

**Background: MUB(6) and the moment problem formulation**

The MUB problem in dimension 6 asks whether there exist 3 (or more) mutually unbiased bases. The known result: MUB(d) exists with d+1 bases when d is a prime power. For d=6, it's open whether 3 MUBs exist (the "MUB(6)=3" question — whether the maximum number of MUBs in dimension 6 is 3, i.e., whether 3 exist, and whether more than 3 don't exist). Actually the notation MUB(6)=3 would mean the maximal number of MUBs in dimension 6 is exactly 3. The firewall says I must never claim or imply MUB(6)=3 or MUB(6)≤3. So the program presumably is searching for certificates that would rule out triples in some region, or something like that — but the governance says findings apply strictly to a declared region/moduli and mint no authority. So the program seems to be: formalize moment relaxations for the MUB(6) existence problem, and the gaps G1–G5 are epistemic gaps in the program. G5 is partial: the "generic operator gap" (Q5/Q6) is open.

The setup: MUB existence can be formulated as a polynomial optimization problem over non-commuting variables (the projector entries or the unitary matrix entries). Specifically, a set of d+1 (or 3) MUBs corresponds to a set of rank-1 projector-valued measures: projectors P_i^(k) = |v_k^(i)⟩⟨v_k^(i)| satisfying:
- Σ_k P^(i)_k = I for each basis i (completeness)
- Tr(P^(i)_k P^(j)_l) = δ_kl / d for i ≠ j (unbiasedness: |⟨v^(i)_k | v^(j)_l⟩|² = 1/d)

These are polynomial equations in the entries of the projectors (which are Hermitian matrices). One can phrase this as a commutative polynomial system in the real and imaginary parts of entries, or as a non-commutative problem in the projector variables themselves.

The "moment approach": consider the free *-algebra generated by symbols for the projectors, with the relations. A truncated moment matrix M_d(E) of a linear functional E on words of degree ≤ 2d. The question of whether a candidate "solution" or "refutation" at finite degree d extends to an actual state (a positive functional coming from an actual configuration of projectors) is the Soundness Gap: finite truncation positivity does not imply realizability by physical states.

Dual side: a refutation is a linear functional W = L D L^T (a sum of squares-type certificate) that separates: if E(W) < 0 for all physical states but the truncated moment data is positive, etc. Actually the dual witness: to show infeasibility of the moment relaxation at level d, one exhibits a certificate that the moment matrix cannot be PSD, i.e., an element of the quadratic module that is negative on the candidate. Hmm.

Let me think about the two closure routes:

**Route (a): Non-commutative Archimedean Positivstellensatz**

The classical Helton's theorem (Helton 2002, "Positive noncommutative polynomials"), and the non-commutative Positivstellensatz: A symmetric non-commutative polynomial p is positive on all tuples of matrices (all sizes) iff it is a sum of hermitian squares (SOHS). For positivity on a semialgebraic set defined by symmetric nc polynomials g_1,...,g_k, the relevant object is the quadratic module Q(g) = {Σ s_i^* s_i + Σ_j Σ_i h_{ij}^* g_j h_{ij}}. The nc Archimedean Positivstellensatz (due to Helton-McCullough, and in the "state" version due to ... hmm) says: if the quadratic module is archimedean (i.e., contains N - Σ x_i^* x_i for some N, or in the matrix-valued setting, is closed and contains bounding elements), then a symmetric polynomial p positive on the set has a certificate p = q + ε with q in the closure of the quadratic module. Actually the precise statement: For the free skew field... Let me recall.

Helton's 2002 theorem: p ⪰ 0 on all matrix tuples ⟺ p is SOHS. This is an exact algebraic certificate, no archimedeanity needed because the domain is all tuples (unconstrained). With constraints g_j ⪰ 0, positivity on the constrained set: p = Σ s_i^* s_i + Σ_j Σ h_{ij}^* g_j h_{ij} + small error, under archimedeanity (Helton-McCullough 2004? "Positivstellensätze for noncommutative polynomials"). There's also the "matrix-valued" version and the "state" version relevant to C*-algebras: e.g., the results of Cimpric, Helton, McCullough, Nelson, and the "noncommutative real algebraic geometry" school.

For the MUB problem: the variables are projector-like operators; constraints include P² = P (idempotence), P = P*, Σ_k P_k = I (completeness), and unbiasedness Tr conditions. But wait — unbiasedness is a trace condition, not an operator inequality. In the nc formulation, one might use the normalized trace as part of the functional: the moment functional E is a tracial state (E(AB) = E(BA)), and unbiasedness is E(P^(i)_k P^(j)_l) = δ_kl/6.

So the setting is: free *-algebra with generators p^(i)_k (i = basis index, k = vector index), relations: p* = p, p² = p, Σ_k p^(i)_k = 1 (central unit), and the functional E is a tracial positive functional with E(1) = 1. The moment matrix M_d(E) has rows/columns indexed by words of degree ≤ d, entries E(w* w'). Positivity of E on all words: M_d(E) ⪰ 0 for all d ⟺ E extends to a positive functional on the free algebra (by nc GNS / Haviland-type theorem). But positivity on the free algebra does NOT imply the functional comes from an actual finite-dimensional representation with the relations — that's the Soundness Gap. The physical states are those E arising from actual configurations: E(w) = Tr(ρ w(P)) where P is a tuple of 6×6 matrices satisfying the relations (or more precisely, E(w) = (1/6)Tr(w(P)) with P actual projectors). The gap: a positive tracial functional on the abstract algebra need not be a convex combination of "evaluation states" at finite-dimensional representations. This is exactly the distinction between the cone of all positive functionals and the cone of functionals coming from finite-dimensional representations — the moment relaxation is sound only if we can bridge from "M_d ⪰ 0 for all d" (or flat extension) to "E is an evaluation/convex combination of evaluations."

**Route (b): Curto-Fialków flat extension**

In the commutative truncated moment problem, Curto-Fialków theory: given a truncated moment functional L on polynomials of degree ≤ 2d with moment matrix M_d ⪰ 0, if rank(M_d) = rank(M_{d-1}) (flatness), then L extends uniquely to a full moment functional represented by a positive Borel measure supported on rank(M_d) many points, and the extension is "flat" forever; moreover the support points can be extracted (they're the joint eigenvalues / solutions of a system from the column relations). This is the "flat extension theorem" (Curto–Fialków 1996, 2000; also related to Bayer–Teichmann, Henrion–Lasserre's extraction).

In the non-commutative setting, the analogue: given a truncated nc moment functional on words of degree ≤ 2d, with M_d(E) ⪰ 0 and flatness rank(M_d) = rank(M_{d-1}), one can build the GNS representation: define an inner product space from the quotient of words by the kernel relations (columns of M_d that are linear combinations of lower-degree columns), and the multiplication operators give a *-representation of the free algebra on a Hilbert space of dimension rank(M_d). Flatness ensures the representing space is finite-dimensional and the representation is well-defined at degree d (the "flat" condition ensures the relations propagate). This is the nc flat extension / GNS construction — related to results by ... hmm, in nc real algebraic geometry: "Noncommutative moment problems" — there's work by J. W. Helton, I. Klep, S. McCullough, C. Nelson, and also "the free moment problem" by ... Also relevant: the "Procesi–Schacher" type settings, and the C*-algebraic GNS. For tracial functionals and finite-dimensional representations: the flat extension gives a finite-dimensional *-representation π with E(w) = Tr(ρ π(w)) — actually if E is tracial and the GNS space is finite-dimensional, then E(w) = ⟨v, π(w)v⟩ for a cyclic vector; traciality plus flatness can force ρ to be a multiple of trace on each irreducible block... Hmm, need care.

The key point for the MUB problem: if we can show flat extension at some degree d for the moment data of a candidate, then the candidate is realized by an actual finite-dimensional representation — closing the soundness gap for that candidate. Conversely, if the relaxation is infeasible at level d with a dual certificate (a W = L D L^T in the quadratic module that is negative somewhere), then... wait, the dual witness refutation: W = L D L^T is a sum-of-squares-type element; if E(W) < 0 for the truncated data but W ⪰ 0 on all physical states, then no physical state matches the truncated data — that's a refutation of the candidate's moment data. But to refute the existence of MUB triples in a region, one wants: for all physical states, some certificate is positive, but the relaxation says negative... Let me re-read the context.

"defines the non-commutative polynomial algebra, truncated moment matrices M_d(E_tilde), and dual witness refutations W = L D L^T. It identifies the Soundness Gap between finite truncation and universal physical state realization."

So E_tilde is presumably a candidate moment functional (maybe an extension of partial data, "tilde" suggesting an extension or a hypothetical). The dual witness W = L D L^T: L is a matrix of nc polynomials (linear forms in words?), D a PSD (diagonal?) matrix, so W is a sum of hermitian squares: W = Σ_j (Σ_i L_ij w_i)^* d_j (Σ_i L_ij w_i) — an element of the free quadratic module. If W is a certificate that E_tilde cannot be positive (E_tilde(W) < 0), then E_tilde is not a state — refuting the candidate moment data. But the Soundness Gap: even if M_d(E_tilde) ⪰ 0 for all d up to some bound, E_tilde might not come from a physical state (a 6-dimensional representation with the MUB relations). Conversely, a refutation at finite d is sound (if E_tilde(W) < 0 with W SOHS then E_tilde is not positive — that direction is fine), but the completeness direction — that every non-physical candidate is eventually refuted — is the gap. Hmm, actually let me think about which direction is "soundness."

Soundness Gap between finite truncation and universal physical state realization: The relaxation hierarchy at level d has feasible set = {truncated moment data of degree ≤ 2d satisfying constraints, M_d ⪰ 0}. Every physical state gives feasible truncated data (soundness of relaxation in one direction: physical ⟹ feasible). The gap: feasible truncated data need not come from a physical state. So "soundness" here = the converse: does feasibility at level d imply existence of a physical state? For the MUB problem, if we want to prove non-existence in a region, we need: infeasibility at level d ⟹ no physical state in the region. That direction is automatic (contrapositive of physical ⟹ feasible). Wait, that's the easy direction. Hmm.

Actually for non-existence results: to show no MUB triple exists in region R, we show the relaxation restricted to R is infeasible at level d. Since every physical configuration in R would yield feasible moment data, infeasibility ⟹ no physical configuration in R. That's sound and needs no flat extension. The dual witness W = L D L^T certifies infeasibility: W is a non-negative combination of the constraint polynomials plus SOHS, and evaluating on any feasible data gives ≥ 0, but the constant term is negative — a Positivstellensatz certificate of infeasibility. This is sound at any finite level (assuming the certificate is a valid element of the quadratic module — which is checkable in exact arithmetic).

The Soundness Gap is the other direction: if the relaxation is feasible at all levels (or at level d), does a physical state exist? This matters if the program is trying to *construct* or *confirm existence* — or if the program's logic is: "the relaxation at level d is feasible, therefore we cannot refute, therefore..." Hmm. Or the gap could be about the refutation of *specific candidate moment functionals* E_tilde: the program enumerates candidate truncated moment data (e.g., from symmetry reductions, the "24×24 Gramian blocks"), and needs to decide whether each candidate extends to a physical state. If a candidate E_tilde has M_d ⪰ 0 but no physical realization, then treating it as "not refuted" is unsound for existence claims; conversely, refuting it requires either a W with E_tilde(W) < 0 (works at any level, sound) or showing no extension exists (hard).

Given "Gap G5 is PARTIAL (Q5/Q6 generic operator gap open)" — the generic operator gap: for generic (non-symmetric?) operator candidates, the question of whether truncated positivity implies realizability is open. The two closure routes:

(a) Archimedean Positivstellensatz: if the quadratic module generated by the constraints is archimedean, then every positive functional on the constrained algebra is approximable by / is a limit of quadratic module functionals... The relevant theorem: For a unital *-algebra A with archimedean quadratic module Q, states (positive unital functionals) are exactly the functionals non-negative on Q... Hmm, more precisely: the nc Positivstellensatz in the state setting (Cimpric–Helton–McCullough–Nelson? or the "Haviland theorem for free algebras"): A linear functional L is positive on the free algebra iff L(q) ≥ 0 for all q in the quadratic module of SOHS. For constrained positivity: L positive on the constrained set of representations iff L ≥ 0 on the quadratic module generated by constraints — under archimedeanity, by the nc Kadison–Dubois / Jacobi representation theorem. The Archimedean route closes the gap by showing: the cone of functionals non-negative on the archimedean quadratic module equals the cone of functionals positive on all representations (finite-dimensional, bounded). But then one still needs finite-dimensionality (dimension ≤ 6) — the representations could be infinite-dimensional or higher-dimensional. Hmm, but for the MUB problem, the relations P² = P, Σ P_k = I with 6 projectors per basis... Actually a representation of the free algebra with these relations on a Hilbert space: the projectors decompose the space; the trace condition Tr(P_i P_j) = 1/6 with normalized trace forces... In finite dimension n, Σ_k Tr(P_k) = n, and unbiasedness Tr(P^(i)_k P^(j)_l) = n/6? Wait: |⟨v|w⟩|² = 1/6 for unbiased vectors in dimension 6. In a representation of dimension n ≠ 6, the relations would scale differently. The moment formulation fixes E(P^(i)_k) = Tr(P_k)/n = 1/6 (each projector has rank 1 in dimension 6, so normalized trace 1/6). So the moment data includes E(p_k) = 1/6, and E(p_k p_l) = δ_kl/6 for same basis (orthogonality: distinct vectors in the same basis are orthogonal, so P_k P_l = 0), and E(p^(i)_k p^(j)_l) = 1/6 for i ≠ j (unbiasedness). These trace conditions pin the "dimension" to 6 in a suitable sense: a finite-dimensional representation with a tracial state realizing these moments would have dimension 6 (since Σ_k E(p_k) = 1 and each p_k ≠ 0 minimal...). Hmm, actually the relations p_k p_l = 0 (k≠l), Σ p_k = 1, p_k² = p_k force the p_k to be complementary rank-1-ish projections in any representation where they're nonzero: the corner algebras p_k A p_k... In a finite-dimensional representation, Σ_k p_k = I with p_k p_l = 0 means the p_k are pairwise orthogonal projections summing to I; if additionally each p_k ≠ 0, then dim ≥ 6 (6 projections). The trace conditions E(p_k) = 1/6 with E tracial: E(p_k) = Tr(ρ p_k)... if E is the normalized trace on a representation of dimension n, E(p_k) = rank(p_k)/n = 1/6 forces rank(p_k) = n/6, so n = 6m and ranks = m. Hmm, so representations of dimension 6m with each p_k of rank m also satisfy the moment conditions. So the moment problem's "physical states" might need to be defined as dimension-6 representations specifically, or the trace conditions might force it via flatness rank. Interesting — the flat extension route: rank(M_d) = rank(M_{d-1}) = r gives a representation of dimension r; if r = 6 (or r relates to 6), we get a 6-dimensional realization. Hmm, but with 3 bases × 6 projectors = 18 generators, the GNS dimension from flatness would be the rank of the moment matrix, which could be large.

Wait — the "24×24 Gramian blocks of dimension 6": 24 = 4·6 or 24 = number of... In dimension 6, a basis has 6 vectors; Gram matrices between two bases are 6×6. 24×24: maybe the Gramian of 4 bases? 4×6 = 24 vectors. Or the Gram matrix of the 24 vectors of 4 bases (the question of 4 MUBs?). Hmm, or 24 = dimension of some symmetry-adapted block. The task says "the 24×24 Gramian blocks of dimension 6" — so blocks of size 24×24, in the dimension-6 problem. Perhaps: the Gram matrix of the 24 vectors from 4 hypothetical bases (testing whether 4 MUBs exist would imply... no wait, firewall says don't claim MUB(6)=3 or ≤3, so the program is about... hmm, if the program is trying to establish MUB(6) = 3, it would need both existence of 3 (open? no — existence of 3 MUBs in dimension 6 is open! Actually: it's known that MUBs exist in pairs (d+1 ≥ 2 always? no...). Let me recall: in dimension 6, it's known that at least 3 MUBs exist? Hmm. The MUB(6) problem: the maximum number of MUBs in dimension 6 is unknown; it's known that 3 ≤ MUB(6) ≤ ... hmm, actually I recall that the existence of 3 MUBs in dimension 6 was open for a while; there are numerical constructions of 3 MUBs (found by computer search, e.g., by Grassl, or the "MUBs in dimension 6" numerical solutions), and it's known that 7 MUBs don't exist? No wait. Let me recall the state of the art: For d=6, it's known that MUB(6) ≥ 3 (three MUBs were constructed numerically and verified to high precision? or rigorously?). I believe: pairs of MUBs always exist (trivially, any basis is unbiased to the Fourier basis of it? no — a basis and its Fourier transform are not always unbiased... actually for any prime power d, d+1 MUBs exist; for general d, at least 2 MUBs exist? Hmm, it's known that in any dimension, at least 2 MUBs exist? I think yes: the computational basis and the Fourier basis are unbiased only when... |F_{jk}| = 1/√d always for the Fourier matrix, so yes, any orthonormal basis and its image under the Fourier transform (defined via any orthonormal basis) are unbiased. So ≥ 2 always. For d=6: 3 MUBs — I recall numerical evidence and constructions of triples (e.g., by Brierley–Weigert, or "3 MUBs in d=6 exist" — actually I believe it's established that 3 MUBs exist in dimension 6? Hmm, there's a known result: "there exist 3 MUBs in dimension 6" — yes, I'm fairly confident triples of MUBs in dimension 6 have been constructed (e.g., via computer search with rigorous verification, by Grassl or others; also "MUBs in dimension 6: a computer-assisted construction"?). And whether 4 exist is open? Hmm, actually I recall the open question is whether MUB(6) = 3 (i.e., whether the max is exactly 3, requiring both ≥3 and ≤3). The ≤3 direction (no 4 MUBs) is wide open. The program "MUB(6) program" with gaps G1–G5 seems to be a formal verification program attempting to establish... something, with strict governance that it must NOT claim MUB(6)=3 or ≤3 — i.e., the governance is preventing overclaiming; the program's results are region-limited (e.g., ruling out 4 MUBs in some symmetric region/moduli).

Given the firewall, I should not speculate too much about the program's ultimate goal; I should analyze the technical question as posed.

So the task: analyze the resolution of the Soundness Gap for generic operator candidates in MomentPositivityObligation.lean.

**Part 1: Contrast the two closure routes**

Route (a): Archimedean Positivstellensatz certificate in the nc quadratic module.

Setting: free *-algebra A = ℝ⟨x_1,...,x_n⟩ (or ℂ with *), symmetric constraint polynomials g_1,...,g_m (the MUB relations: p_k² - p_k, p_k - p_k*, Σ_k p_k - 1, p_k p_l (k≠l), and the trace/unbiasedness conditions — though trace conditions are linear conditions on the functional E, not constraints on the operators; the operator-level constraints are the projector relations). The quadratic module Q = SOHS cone + Σ_j SOHS·g_j·SOHS. Archimedeanity: Q is archimedean if for each generator x, some N - x* x ∈ Q (or N·1 - Σ x_i² ∈ Q). With the constraint p² - p ⪯ 0... hmm, p² = p gives p² - p = 0, which bounds: p = p² ≤ ... From p² = p and p = p*, we get spectra ⊆ {0,1}, so p is a projection, bounded by 1: 1 - p² = 1 - p ∈ Q (since p² - p = 0 ∈ Q trivially as constraint, 1 - p = -(p² - p) + (1 - p²)... wait: 1 - p = (1 - p²) + (p² - p) = (1-p*)(1-p) + ... let me compute: (1-p)² = 1 - 2p + p² = 1 - 2p + p = 1 - p. So 1 - p = (1-p)² ∈ SOHS. And p = p² ∈ SOHS. So the quadratic module with the idempotence constraints is automatically archimedean in each generator: N - p*p = N - p² = N - p = (N-1)(1-p) + (1-p)... hmm, N - p = (N-1)·1 + (1 - p) hmm need 1 ∈ Q (yes, 1 = 1*1) and (1-p) ∈ Q, so N - p ∈ Q for N ≥ 1. Yes! So the quadratic module generated by the projector relations is archimedean (each generator is bounded: p* p = p² = p ⪯ 1 in the Q-order). Great — so archimedeanity holds for the projector-constrained nc algebra. This is a nice observation: idempotent Hermitian generators are automatically archimedean.

Then the nc Archimedean Positivstellensatz (Helton–McCullough 2004? "A Positivstellensatz for semialgebraic sets in free variables"? Actually the relevant one: Helton, McCullough, "Positivstellensätze for noncommutative polynomials", Bull LMS 2004?; also the "state version" by Cimpric–Helton–McCullough–Nelson? and the tracial version by Klep–Schweighofer "Pure states, matrix convexity..."? Hmm, there are several:

1. Helton 2002: p ⪰ 0 on all tuples ⟺ SOHS. (Unconstrained.)
2. Helton–McCullough 2004-ish: for constrained sets, with archimedean Q: p strictly positive on the constrained set ⟹ p ∈ Q (or p + ε ∈ Q for all ε > 0? or p in the closure). Actually I recall: if Q is archimedean and p is strictly positive on the set, then p ∈ Q. Hmm, there's a subtlety: for nc, "strictly positive" means bounded below by ε·1 uniformly over all sizes — that's a strong condition. The theorem: p ⪰ ε·1 on the free set S ⟺ p - ε ∈ Q when Q archimedean? I think the correct statement (Helton–McCullough, "A noncommutative Positivstellensatz"): if Q archimedean, then p strictly positive on S (i.e., ∃ε>0 with p ⪰ ε on all of S at all sizes) implies p ∈ Q. Hmm wait, I think it's: p ∈ Q ⟹ p ⪰ 0 on S; conversely with archimedeanity, p strictly positive on S ⟹ p ∈ Q. Yes.

3. The "state" / moment side: the dual. Haviland-type: L is a state nonnegative on Q ⟺ ... The dual of Q-cone is the cone of Q-positive functionals; the question of whether every Q-positive functional is a limit/integral of evaluation states at representations — this is the nc moment problem. For archimedean Q, the answer: the Q-positive functionals are exactly the states on the "free C*-algebra" quotient... Hmm. Actually there's a clean statement: For archimedean quadratic module Q in free algebra, a unital functional L with L(Q) ≥ 0 extends to a state on the universal C*-algebra C*(⟨x⟩ | g_j ⪰ 0), and by GNS gives a *-representation π (possibly infinite-dimensional) with L(w) = ⟨v, π(w)v⟩. So the archimedean route closes the gap to "representation of the universal C*-algebra" but NOT to finite-dimensional 6-dimensional representations. The remaining gap: infinite-dimensional representations of the projector relations exist (e.g., infinite-dimensional Hilbert space with 6 orthogonal projections summing to I — sure, take any Hilbert space H = ⊕_6 H, p_k = projection onto k-th summand; then the trace conditions E(p_k) = 1/6 hold with normalized trace if dim H = ∞? Traces on B(H)... normalized trace doesn't exist on B(∞-dim); but there are tracial states on some C*-algebras with these relations). So the archimedean route gives: positivity on the quadratic module ⟺ state on the universal C*-algebra ⟹ GNS representation (infinite-dim possible). To get down to dimension 6, need extra arguments (e.g., the trace conditions + finite-dimensionality of the moment matrix / flatness, or algebraic arguments that the universal C*-algebra's states satisfying the trace conditions are limits of 6-dim ones...). Hmm, but actually for the MUB problem, maybe the relevant claim is weaker: the soundness bridge needed is "if the relaxation is feasible at level d (with flatness or not), then physical states exist" — for *refutation* purposes one needs the contrapositive only for the direction: physical ⟹ feasible (always true). Let me reconsider what "ProjectorMomentSoundnessBridge" might be.

Given the name: "ProjectorMomentSoundnessBridge" — a theorem bridging projector-level (physical) statements and moment-level (relaxation) statements. Likely: "If the level-d moment relaxation (with the projector relations and trace conditions) is feasible with a flat extension, then there exists a physical configuration (actual 6-dim projectors) realizing it" — i.e., the soundness of using relaxation feasibility to conclude physical existence. OR: "If a dual witness W = L D L^T is found with E_tilde(W) < 0, then E_tilde is not a physical state" — that's the easy direction. The "Soundness Gap between finite truncation and universal physical state realization" — the gap is that finite truncation positivity does not imply physical realization. Closing it = proving that (under conditions X) finite truncation data IS realized physically. The two routes: (a) archimedean certificate — show the candidate's positivity extends via Positivstellensatz to a state on the universal C*-algebra, then argue dimension ≤ 6; (b) flat extension — rank condition gives finite-dim GNS representation directly of dimension rank(M_d), then argue the trace conditions force the representation to decompose into 6-dim MUB blocks.

Hmm wait, but actually maybe the bridge goes the other way for the program's purpose: the program wants to REFUTE candidates (generic operator candidates — Q5/Q6 generic operator gap open). A candidate operator tuple (generic operators, not necessarily satisfying symmetry) is proposed; the question: does the moment data of the candidate satisfy the relaxation? If the relaxation at level d is infeasible, the candidate is refuted (soundly, since physical ⟹ feasible). If feasible, the candidate is "not refuted at level d" — and the soundness question is whether feasibility at level d (or all d) implies the candidate (or some candidate) is physical. For the program to claim "candidate C is consistent/not excluded," it needs the bridge: feasibility ⟹ physical realizability. Without the bridge, feasibility at all finite levels is necessary but not sufficient for physical realizability — the gap.

So closing the Soundness Gap = proving: truncated moment data satisfying (i) M_d ⪰ 0, (ii) constraints, (iii) [flatness or archimedean certificate] ⟹ realized by physical state (6-dim projectors satisfying MUB relations in the stated region).

Route (a) details: The Archimedean Positivstellensatz route. To use it for the bridge: given the candidate E_tilde positive on M_d for all d... hmm, the archimedean route would go: E_tilde is positive on the quadratic module Q (checkable? not finitely checkable in general — that's the issue: L(Q) ≥ 0 is an infinite condition; but if E_tilde is given by an explicit formula/extension, maybe checkable). Then by archimedeanity, E_tilde is a state of the universal C*-algebra A_univ = C*(p^(i)_k | relations). Then GNS: representation π, cyclic vector v. Then need: π finite-dimensional, and the trace conditions force dimension 6. The trace conditions E(p^(i)_k p^(j)_l) = 1/6 etc. are conditions on E, hence on ⟨v, π(·)v⟩. Hmm, to get dimension 6: consider the projections q^(i)_k = π(p^(i)_k): 18 projections, within each basis pairwise orthogonal summing to 1. The vector v has ⟨v, q^(i)_k v⟩ = 1/6 for all i,k. Unbiasedness: ⟨v, q^(i)_k q^(j)_l q^(i)_k v⟩ = 1/6 for i≠j. Does this force dim ≤ ...? Not obviously; infinite-dimensional examples: take H = K^{⊗6}? Hmm, consider H infinite-dim with a "MUB-like" structure... Actually here's a thought: the universal C*-algebra generated by 18 projections with Σ_k p^(i)_k = 1, p p' = 0 within basis — this is a "projection grid"/"commuting square"-like algebra; its representations include infinite-dimensional ones (e.g., tensor the 6-dim MUB rep with any Hilbert space K: p_k ↦ P_k ⊗ 1_K — then normalized trace doesn't exist but vector states do: v = v_0 ⊗ w with ‖v_0‖... ⟨v, (P_k⊗1) v⟩ = |⟨v_0, P_k v_0⟩|... to get 1/6 for all k need v_0 = (1/√6)Σ e_k — the maximally mixed vector state: ⟨v_0, P^(i)_k v_0⟩ = 1/6 ✓. And unbiasedness: ⟨v, P^(i)_k P^(j)_l P^(i)_k v⟩ = |⟨v^(i)_k, v^(j)_l⟩|² = 1/6 ✓. So the "amplified" representations (MUB rep) ⊗ (any rep of anything) with the maximally mixed vector realize the same moment data! So the moment data does NOT pin dimension 6 — the GNS representation could be 6·dim(K). But that's fine for the bridge: if the moment data is realized by SOME representation of the form (6-dim MUB)⊗K with mixed vector, then in particular a 6-dim MUB exists (the tensor factor). But the bridge needs: E_tilde realized ⟹ 6-dim MUB in the region exists. The amplified representations still contain the 6-dim MUB as a tensor factor — but does every representation realizing the moment data contain a 6-dim MUB block? Not necessarily — there might be "exotic" representations (e.g., on C*-algebras like free products, or the C*-algebra of the "MUB relations" might have non-product representations). Hmm, this is exactly the subtlety of the soundness gap: the universal C*-algebra of the MUB relations (without unbiasedness, which is a state condition) — its representations are "6 projection-valued partitions"; the universal algebra is like a free product amalgamated... The unbiasedness conditions are conditions on the state, not the algebra. So the bridge via route (a): E_tilde Q-positive
```
</details>


---

### Model: Super Bunny Alpha

- **Status:** TRUNCATED (finish_reason: `length`, content: null)
- **Latency:** 140.83s | **Tokens:** 8801
- **Notice:** Call exhausted token limit during internal reasoning; no completion content was emitted.

<details><summary>Truncated Reasoning Trace (37445 chars)</summary>

```
We need craft answer. Need understand context deeply. Need likely inspect? No actual files supplied. Need analyze G5, Lean spec. Need avoid forbidden claims/hype and strict firewall. Need perhaps identify conceptual issue: two routes Archimedean Positivstellensatz in noncommutative quadratic module vs Curto-Fialkow flat extension rank-loop closure via noncommutative GNS. Need contrast. Computational tractability exact rational 24x24 Gramian blocks dim6. Need formulate exact Lean theorem spec for ProjectorMomentSoundnessBridge with epistemic qualifiers.

Need reason details.

MUB(6), M_d(E_tilde), dual witness refutations W=L D L^T. Moment matrices perhaps blocks 24x24 because symmetric projector? Need understand variables/dim. Noncomm polynomial algebra. Generic operator candidates. Finite moments versus physical state realization. Soundness gap: truncated positivity tests accept algebra but no commuting/GNS state? Curto-Fialkow applies commutative polynomial algebras and Hamburger moment problem perhaps flat-extension theorem. In noncomm setting GNS? Need be precise: A generic noncommutative operator algebra truncated representation may have positive semidefinite moment matrix. Does NSDP imply GNS/state on algebra? For one operator, perhaps finite truncation not necessarily extend to positive functional on noncommutative polynomials. Archimedean NCP can certify via sums of squares if strict Archimedean. For matrices/noncomm, Positivstellensatz caveats. Need distinguish.

Question wording asks "Analyze resolution ... 1. Contrast two formal closure routes: (a) Archimedean Positivstellensatz certificate in non-commutative quadratic module, versus (b) Curto-Fialkow flat-extension rank-loop closure (rank...) via non-commutative GNS construction. 2. Which route computationally tractable in exact rational arithmetic for 24x24 Gramian blocks dimension 6? 3. Formulate exact Lean 4 theorem specification needed to close bridge..." Likely expect explain route a SDP exact cert and route b rank/SOS perhaps computationally hard. Need establish what can computationally tractably do. Exact rational arithmetic on 24x24 blocks: matrix ranks via exact LDL/rational Gaussian elimination feasible; linear algebra tractable. But generic rank-loop all d infinite closure cannot be achieved finite unless rank stabilization theorem/certificate. Curto-Fialkow in commutative setting: once rank condition and consistency, extension exists; noncomm GNS? Need maybe use one route as theorem. Exact rational SDP for Archimedean Positivstellensatz can be difficult due unknown denominators/SOS multipliers, but for fixed 24x24 rational certificate it is exact rational linear algebra plus PSD exact certification. Search isn't tractable in general. If dimension 6 projective state variables lead Gramian 24 block. Need parse 24 arises M_d? Six-dimensional subspace of traceless Hermitian 3x3 projectors dimension 8, not 24. 24 basis for M_3? Full matrix units 9 gives 81. 24? Maybe M_d blocks from six variables degree d? d=2 gives number monomials maybe? M_d Etilde dimension 24. Could be M_2 of degree? E tilde 3x3 basis? 6^2? 24 distinct trace-free Hermitian? Let's not assume.

Question perhaps intentionally asks specialist challenge: identify route mismatch. Curto-Fialkow flat extension rank condition only valid commutative moment problem, and "via non-commutative GNS" potentially invalid. Need state that. The right resolution perhaps route (a), if an Archimedean certificate gives a positive trace on universal noncommutative algebra. Yet a finite algebraic identity? Need exact Lean theorem.

We need formulate Lean theorem signatures with assumptions including state map. "ProjectorMomentSoundnessBridge" likely theorem connecting finite moment feasibility to physical state? Need define abstract predicates rather than claim actual projector's MUB. Need include NOT labels. We can give code skeleton using finite types, PosMulDef, StarOrdered? Lean 4 mathlib details. Need be exact enough. We can formulate theorem spec perhaps pseudocode / Lean code, mark definitions placeholders. They ask exact specification. Need make sound logical shape: cannot close soundness from rank loop alone. Need theorem assumptions corresponding certificate or extension and conclusions restricted region. "Mint no authority." Need maybe theorem itself says within declared region and candidate, existence finite moments -> state.

Let's formalize.

Set:
- F = Q maybe Rat
- Hilbert space H maybe finite dimensional C^6
- A = free noncomm algebra over Q/C generated by Etilde elements.
- evaluation ν: A -> C? A positive normalized linear functional.
- truncation map ev_d.
- M_d(ν)_{ij} = ν(x_i^* x_j)
- admissible Gramian X ≥0, linear equations, normalization.
- physical state: positive unital trace τ: NC algebra generated by candidate Etilde -> M? A GNS positive trace, and τ(E_i^*E_j)=M_d entries. Perhaps "state realization" for finite-dimensional operator algebra. If candidate subspace includes commutativity? Generic noncomm operators in fixed 6x6 Hermitian space can span full M6; universal C*-algebra finite. Positive functional on full M6 corresponds density matrix, easy if closure. But physical state likely state on free product? Etilde maybe operators. Physical means positive state on algebra, no need commuting if noncomm candidate? The declared gap finite truncation/universal physical state realization.

Archimedean Positivstellensatz certificate:
Given polynomial f? To show existence of state satisfying linear constraints, one can formulate Riesz-Haviland: finite-dimensional subspace V ⊂ A is positive iff for every q with q*? positivity etc. Archimedean quadratic module allows dual certificates. W=LDL refutes. A certificate perhaps
1 - ||?||? = σ0 + sum σ_i q_i
with SOS. If module Archimedean, emptiness of module yields certificate. But which polynomial encodes all moments? Feasibility of truncated NMP. There are known NMP algorithms (Nie: Archimedean quadratic module). For noncommutative polynomials, Helton? Noncomm Positivstellensatz. Need be cautious.

A Positivstellensatz certificate typically proves infeasibility of a system, not realizes moments. If strict certificate? For moment feasibility, duality: a positive functional on V represented by integral over representation; separating dual can refute. A primal feasible moment matrix can itself yield representation on V? A PSD Hankel matrix gives GNS representation of V? For noncomm finite-dimensional subspace, perhaps. Extension to whole A not guaranteed. An Archimedean certificate for "1 belongs to module" establishes something about noncompactness, not arbitrary moment feasibility. Need articulate exact logical role.

Route (a) could furnish a positive trace by constructing a positive functional from Archimedean dual representation? In commutative real algebraic geometry, saturated quadratic module corresponds to K-moment functionals on quotient. Archimedean Putinar certificate yields representation. In matrix/noncomm, quadratic module of completely positive elements? Maybe exact.

Route b: Curto-Fialkow theorem for commutative bivariate (and multivariate extensions) moment matrices: if flat M_d, there is representing measure. For noncomm, rank condition alone generally not enough. "via non-commutative GNS construction" perhaps a proposed adaptation: represent algebra A by GNS from truncated moment matrix and recursively ensure consistency. But GNS from a truncated functional is not enough. Need flag. If all rank loops and consistency, can extend positive functional? In a unital C* algebra, any truncated N-sequence of moments satisfying positivity maybe? Need extension requires full sequence, not just flatness. Curto-Fialkow for classical commuting variables gets it. For noncomm one operator? The algebra generated by one selfadjoint is commutative. For multiple noncomm, no.

The task perhaps expects choose route computationally tractable. Could say:
(a) is the appropriate semantic route but finding a complete Archimedean/SOS certificate may invoke semidefinite feasibility/optimization; exact rational verification of a proposed certificate at 24x24 is tractable (linear solves, Gram matrix construction, exact LDL or principal-minor/polynomial methods), but complete rational Positivstellensatz search is not polynomial-time guaranteed and positivity over C/R needs exact real-algebraic tests.
(b) rank loop is computationally cheapest at each d: exact rank of 24x24 rational matrix via fraction-free Gaussian elimination, then M_{d+1}; however the noncomm rank-loop theorem needed is absent/unavailable. If valid CF hypothesis (commutative) included, rank closure and representing measure, but generic noncomm not within theorem. Thus among routes in current formal setting, only (a) can be intended as finite exact certificate if assumptions supply theorem; (b) cannot close soundness merely via rank. Question asks "Which route is computationally tractable in exact rational arithmetic for the 24x24 Gramian blocks?" They might expect b because rank computations easy, while Positivstellensatz SDP expensive. But need parse wording: "versus (b) Curto-Fialkow flat extension rank-loop closure ... via non-commutative GNS construction." Maybe answer: exact rational rank computations are tractable, so route b; Archimedean Positivstellensatz involves SDP/SOS not tractable in general. But can route b legitimately close? Curto-Fialkow only commutative. They may want point out mismatch and say rank route tractable diagnostically, not sufficient for generic noncomm. Maybe use route a as semantically correct but computational? Let's infer intent from context. They call G5 PARTIAL, generic operator gap open. Asked "Analyze the resolution ...". They likely want discuss both, determine tractable route, formulate theorem. Strict governance means no overclaim. The answer should likely say no resolution yet absent certificate/theorem; formal bridge can only be closed conditionally.

Could formulate theorem where rank stabilization for all d plus "noncomm CF extension property" assumption gives state. Then exact Lean spec. But to resolve actual gap need prove that property, which is the gap. Or use Archimedean representation theorem as assumption, similarly. Need distinguish formalization of theorem vs actual instantiation.

Let's define two routes logically:

(a) Certificate route:
- Candidate moment data X = (X_0,...,X_D) rational.
- Need establish X is restrictions of a positive linear functional τ on A? SOS/Positivstellensatz can show infeasibility for extension constraints, perhaps a "dual refutation" W. Wait W=LDL refutations identify finite constraints incompatible with positive matrices. For soundness, if all finite W refute candidate, then no physical state by Hahn-Banach? If a physical state exists, all W should be PSD, so W refutes state. This is safety/necessity, not sufficiency. To establish a state from finite moments, need completeness.
- Archimedean NCP theorem says under Archimedeanness, truncated extension feasibility can be dual characterized? If one has a certificate for a polynomial strictly positive on moment variety, construct measure/state. A certificate can be checked. But not just W=LDL.

Maybe define "quadratic module" Q = sums σ0+Σσ_i q_i. If 1 ∈ Q + I, infeasible. That certificate is a dual refutation, not a state. For candidate feasibility, a primal rational Gramian plus a representation theorem could close. What certificate "Archimedean Positivstellensatz certificate" supports? If certificate is a separating function, it refutes. The task perhaps calls route a closure route; likely they envision certificate proving existence. Need state exact distinction.

A positive functional τ on A is itself infinite data generally, though for finite-dimensional matrix algebra can represent by density matrix. An Archimedean certificate at truncation may establish extension? Noncomm Positivstellensatz gives dual certificates for NMP feasibility. For a feasible system, the theorem yields existence of representing measure/state (in a commutative or matrix polynomial setting), with explicit rational? Archimedean condition essential for duality and measures.

Question's exact wording: "Analyze the resolution of the Soundness Gap for generic operator candidates in MomentPositivityObligation.lean:
1. Contrast the two formal closure routes: (a) Archimedean Positividelensatz certificate in the non-commutative quadratic module, versus (b) Curto-Fialkow flat extension rank-loop closure (rank(M_d) = rank(M_{d-1})) via non-commutative GNS construction.
2. Which route is computationally tractable in exact rational arithmetic for the 24x24 Gramian blocks of dimension 6?
3. Formulate the exact Lean 4 theorem specification needed to close ProjectorMomentSoundnessBridge, respecting: 'stated region only; mints no authority'."

Likely generated from a project. They may expect a direct answer selecting route. Need possibly say neither is currently complete; (a) semantically robust, (b) invalid unless commutation; rank computations tractable. We should phrase.

Let's delve computational complexity exact rational.

24x24 rational symmetric PSD:
- Multiplication O(n^3)=13,824 basic rational ops approximately (24^3), elimination O(24^3), storage O(576). Fraction-free / modular algorithms.
- Exact PSD can be checked by exact LDL^T with pivoting / Sturm sequence or characteristic coefficients. But rational LDL without square roots can have 2x2 pivots; semidefinite exact. Principal minors are combinatorial if naive. Use exact rational LDL with symmetric pivoting and PSD conditions. Matrix rank computed fraction-free Gaussian elimination.
- 24 blocks may be entries polynomials/rational functions due normalization denominators. Clear denominators with positive factors; check projective chart and denominators.
- Positivstellensatz search: fixed-degree multipliers introduce larger Gram matrices; rational exact feasibility is existential theory of reals (∃R), often NP_hard; bit complexity can explode. Positivstellensatz degree bounds exist but not small. An explicitly supplied rational Gram/SOS certificate is easy to verify. But SOS of noncomm polynomial: Gram matrix size equal to basis of degree. If directly 24x24, verification uses matrix products and equality of coefficients, still polynomial. Finding denominators and certificate not guaranteed tractable.
- Rank loop: each d exact rank cheap, and comparing M_{d+1} range/inclusion. Yet "all d" infinite cannot be certified by finite computation unless a finite-degree extension/rank theorem applies. For finite-dimensional candidate algebra perhaps recurrence/determinantal representation can yield bound; not generic. A stabilized rank over two levels does not necessarily establish all future ranks. CF theorem gives finite flat condition under classical assumptions. In noncomm generic setting no.
- Noncomm GNS: To construct GNS, need a global positive functional τ on A. A finite sequence X_d does not define τ on A, because words of degree >d unresolved. GNS of quotient/V_d yields representation of V_d (or relations) but not A unless A is generated/quotiented at that level and relations certified. Extending reps to each d coherently is another task. Rank flatness controls kernels of Hankel matrices in classical setting, not generic operator relations.

Archimedean condition:
- Need define noncomm quadratic module. For real *-algebra? Q = σ0 + ∑ σ_i q_i, with σ_i = q_i^* q_i? In real * algebra sums of hermitian squares. Complete positivity? In noncomm, ordering has matrix-valued subtleties; scalar polynomials positive pointwise aren't necessarily completely positive. If physical state on operator algebra, use completely positive cone, not just positive cone. A real quadratic module may support commutative-like order but not C*-positivity.
- Archimedean: if 1 - ε Σ? belongs module then ε large; or ∃N, Σ z_i^*z_i - N1 ∈ module. This compactifies feasible spectra. Exact certificate should include an explicit N and identity.
- However 1∈module indicates infeasibility, not a state. An "Archimedean Positivstellensatz representation theorem" can establish equality between dual state cone and moment cone under a separator dual cone. Need require both.
- In noncomm algebra, standard Archimedean Positivstellensatz may not hold merely due Archimedean quadratic module. Need theorem assumptions: real closed base, finite-dimensional *-subalgebra, Archimedean and closed, or matrix Positivstellensatz. Generic free noncomm algebra on multiple symmetric generators is non-Archimedean if generators unbounded; imposing finite operator norm bounds may restore compactness but those bounds become physical/state-specific. Thus explicit N needed.

Could propose route (a):
Candidate defined by linear equalities L(E_i)=0 and inequalities. To show existence of state τ realizing X, need check τ? Perhaps an Archimedean certificate for a strictly positive polynomial p on the moment data? Let's frame generic abstract interface: `ArchimedeanNCRepresentability` predicate packages theorem that certificate + exact rational primal data yields a positive trace. Lean doesn't need derive from raw module unless formalized. But "exact theorem specification" should not hide central gap. We can formulate assumptions explicit enough.

Maybe:
```
theorem ProjectorMomentSoundnessBridge
  (harch : IsArchimedean Q)
  (hmom : CompleteMomentDatum R 6 candidate D)
  (hcert : NCPositivstellensatzCertificate Q ...)
  (hreal : DualRepresentation hcert ...) :
  CompletePositiveTrace A candidate
```
Conclusion with restricted candidate. But a certificate alone might be infeasibility. Need use correct direction.

Could have theorem:
```
theorem ProjectorMomentSoundnessBridge
  (hRegion : Candidate ∈ declaredRegion)
  (hData : RationalMomentDatum ...)
  (hArch : Archimedean ...)
  (hCert : NCArchimedeanExtensionCertificate Q hData) :
  ∃ τ, PositiveTrace ... ∧ ...
```
Then what assumptions exactly? Need define certificate as data containing τ? If it contains τ, circular. Better define a representation certificate in terms of finite Gram matrices and archimedean multipliers that theorem maps to state. But difficult actual code.

Alternative conditional theorem for route b:
```
theorem ProjectorMomentSoundnessBridge
 (hcomm : IsCommutative A)
 (hflat : ∀ d≥D, rank M_d = rank M_{d-1})
 (hCF : CFExtensionTheorem A hcomm hflat) :
 ∃ τ, ...
```
But CF theorem for multivariate commuting finite tuples requires more conditions, e.g. consistency, singular? Standard Curto-Fialkow flat extension theorem: For bivariate, M_1 flat suffices; in general multivariate there are variants/conditions. Don't overstate. For univariate Hamburger, rank stabilization. Generic noncomm no. So not valid unless commutation. Could formulate a `NoncommFlatExtension` premise, but that's exactly missing theorem and circular. The question explicitly wants exact theorem needed "via non-commutative GNS construction" perhaps they expect assumption rank loop. We should point out rank loop isn't enough and theorem cannot be stated/proven as desired from it.

Maybe formulate two theorem variants and recommend one:
A. Sound conditional bridge from explicit state extension / Archimedean representation.
B. Candidate flat-loop bridge rejected absent extension theorem.
Then provide Lean code for valid A.

Need include no MUB authority. In code namespace and comments; theorem conclusion should not mention number of mutually unbiased bases or maximal cardinality. "stated region only" encoded by parameter `R` and hypothesis. "mints no authority" can't be mathematical hypothesis, but metadata:
```
/-- Scope certificate: ... -/
theorem ... (R : DeclaredRegion) (hR : Candidate c ∈ R) ...
```
Maybe use structure `ScopeNoAuthority`? Can't formalize governance string as logical proposition. We can include theorem docstring and ensure conclusion only says trace for candidate. In final explain firewall labels are governance metadata, not mathematical assumptions unless encoded as scope datatype. Could define:
```
structure DeclaredRegion where
  name : String
  contains : Candidate -> Prop
```
and conclusion no global count.

What does "physical state" mean? We can formalize GNS positive trace:
- A `StarAlgebra` over ℂ.
- `PositiveFunctional τ` if τ 1=1 and for all a, τ (a* a) ≥ 0. A linear functional on C*-algebra automatically completely positive in C* context.
- For candidate tuple `x : Fin 6 → A`? Etilde maybe `Fin n → H → H`.
- finite moment datum `μ : List?`.
- Consistency `M_d`.
- `τ (x_i * x_j)` equals specified block.
Could say `τ` positive unital on algebra generated by candidate. GNS construction from τ gives a Hilbert space and cyclic representation. Thus soundness conclusion is a GNS trace, not that tuple is a projector set or MUB.

If candidate is actual operators `e : Fin 6 → H → H` on dimension six Hilbert space, any normalized density matrix yields a state and is a GNS state. If moments specify a density matrix on M6, bridge straightforward. But projector's linear relations and traces. Yet use abstract.

Could formalize exact rational moments:
```
def Block (X : Matrix (Fin 24) (Fin 24) ℚ) := ...
```
M_d maybe a rational symmetric matrix. `M_d X` already computed. Need relation between blocks. Define data as:
```
structure RationalGramian where
  blocks : Fin (D+1) → Matrix (Fin 24) (Fin 24) ℚ
  hermitian : ...
  consistency : ...
  nonneg : PSDℚ ...
```
24 block dimension given. Maybe blocks differ dimensions; prompt says "24x24 Gramian blocks of dimension 6" perhaps all. Use fixed 24.

Archimedean certificate:
Could define `NCArchCertificate Q datum` as:
- polynomial h strictly positive on something and identity
`h = σ0 + Σ σ_i q_i`? For infeasibility, Putinar:
If `-p` etc. Need not spell full module? Task asks exact theorem spec. Could state abstract certificate type, then define its fields.

Let's understand moment feasibility Positivstellensatz:
A system `L(y)=b, g_i(y)≥0`. Dual module generated by `g_i`; an infeasibility certificate is `-1 = σ0 + Σ σ_i g_i` (for normalized g, perhaps `1`). This certifies no moments. A state existence cannot be certified by this. A separation theorem says if infeasible, such certificate under Archimedean assumptions. If feasible, not a finite certificate in same module generally. Thus route (a) is actually a completeness route for refutations, not closure of accepted finite candidates. The context says "W = L D L^T" refutations and soundness gap. Maybe they want an Archimedean certificate as sufficient to refute? If candidate has W, no physical state. But soundness gap "finite truncation and universal physical state realization" likely they need prove if no W then physical state. Positivstellensatz completeness can ensure if extension impossible there is a finite W/certificate. Then all finite W absent yields state. Yet no termination bound.

Could be:
- Given a moment sequence, physical state must make all W PSD. This is necessity. Strong duality can show no state -> W. But to close soundness for a concrete candidate, one can produce Positivstellensatz certificate? Wait to show a candidate does possess state, cannot.
- Maybe "resolution" means either certify finite moments are physical or refute. Archimedean certificate in module is exact dual and semidefinite. But still no guarantee candidate accepted.
- Flat rank closure can establish state from finite moments.

Need explicitly state semantic asymmetry:
- A Positivstellensatz identity `1 ∈ Q + I` is a refutation, same direction as W. It can certify rejection. It does not produce τ.
- A representation theorem (not identity alone) can establish that no separator exists and hence primal state exists, but invoking it is the central completeness theorem. In noncomm settings, needs archimedean/CP cone hypotheses.
- Curto-Fialkow rank closure can produce a measure/state if valid, but classical theorem not generic noncomm.

This is likely valued.

Need perhaps mention exact rational arithmetic vs physical matrices complex. Gramian entries may be rational due symmetry, but PSD can be certified over ℚ. A rational positive semidefinite matrix is okay. A GNS state can be complex extension. If use real *-algebra, rational Gram factorization may not exist (e.g., PSD rational matrix can require irrational vectors), but GNS completion can be over R/ℂ; don't need rational factor. This is a subtle exact arithmetic point. Rational PSD certificates: Gaussian/LDL exact. For Gram matrix SOS, `G ⪰ 0`; factorization may be irrational, no need to produce rational Cholesky. If Lean theorem asks rational Cholesky, false: `[1 0;0 1]` fine, but rational PSD 2x2? x²+y² matrix diag; factor rational yes. Some rational PSD forms can require irrational square roots but can have sum of rational square Gram? E.g. [[2,1],[1,1]] = sum v_i v_i^T rational? rank2 det1, LDL gives factor with sqrt2; maybe two rational rank1 forms perhaps [[1,1],[1,1]] + [[1,0],[0,1?]] sum [[2,1],[1,2]] no. Can choose multiple. Not relevant. State existence over ℝ can be certified algebraically.

Noncomm GNS and rank:
Define Hankel/Moment matrix. For a positive functional τ, kernel relation at degree d can reduce representation. A flat matrix indicates no new kernel? In univariate moments, if rank M_d = rank M_{d-1}, extension. In noncomm, dimensions of word subspaces and relations may need "jointly flat" all states, and rank equality may not ensure compatible kernels. There can be noncomm flat extensions? Research "flat extension theorem for noncommutative moment problem" maybe. Need avoid categorical invalidity if specialized theorem. State "not supplied by Curto-Fialkow; one must prove a noncommutative analogue with compatibility. Rank equality alone is not a theorem for generic free *-algebra." Good.

Maybe dimension 6/24:
- 24x24 rank is easy exact.
- Number of variables 6 doesn't reduce existential complexity enough.
- Rational bit complexity depends coefficients/degrees. At each block O(n^3) field ops and O(n^2) memory. Modular methods can handle large rationals.
- An archimedean certificate can perhaps be checked by 24x24 Gram matrices if same degree. But complete Positivstellensatz search has unknown degree. Exact rational output may not exist even if real solution exists; rational certificate isn't automatic. The theorem would need existential real coefficients or specify rational certificate. For Lean, ℚ is preferable: assume explicit rational certificate. If physical data algebraic, can use number fields/ordered fields; not just ℚ.
- Search for rational SOS decomposition is also nonconvex if decomposition unknown, but Gram linear matrix inequality. Exact feasibility over rationals is ETR complete in general.
- If all 24x24 blocks already supplied and only ranks requested, route b computational layer tractable, but closure layer not.
- Thus answer to "which route computationally tractable": distinguish verification from discovery. Rank loop at fixed d is the most tractable exact task; explicit arch certificate verification also tractable. If forced for end-to-end rational route, no route is presently both semantically valid and computationally guaranteed. Under added commutative/finite-matrix hypotheses, (b) is tractable and finite; under a supplied bounded-degree Archimedean certificate, (a)'s checking is tractable but discovery not. For generic noncomm, (a) is conceptually appropriate conditional representation route, but not computational blanket. Need perhaps answer clear.

Let's lay answer structure:

1. Scope and current status.
- G5 remains partial. Finite PSD + W tests are local necessary conditions. `W = LDL^T` PSD iff conditions etc (if exact field), not state.
- Define `A_* = Alg(Etilde)` abstract *-algebra / `A_6` free NC polynomial algebra modulo linear constraints.
- A state τ unital positive. Soundness target:
`∃ τ, τ∘ev_d = X_d` all d (or required region) plus candidate equations; GNS then follows.
- no count conclusion.

2. Route a:
- Module Q_A.
- Archimedean witness N and identity.
- Positivstellensatz separation/dual.
- Exact certificate forms and what it certifies.
- For a *primal* feasible state, need representation side/dual alternative; certificate itself likely refutes. If `1 = ...`, no state. If using arch theorem to show no separator and extension, need hypotheses.
- Noncomm requires correct cone: hermitian squares only gives positivity; physical state may require cp/completely positive sums. If A is C*-algebra and τ positive functional, okay, but module dual should be appropriate. Matrix variables need cp module.
- Archimedean due bounded generators. Generic free algebra isn't archimedean; can have unbounded spectra, e.g. powers. Thus certificate unavailable without normalization/bounds.
- Supports refutation/completeness under conditions; not automatic global extension.

3. Route b:
- Classical CF conditions: commutative polynomial tuple, positive Hankel, consistency, flatness. Then represent measure and positive functional.
- In generic noncomm, rank equality doesn't ensure all word order relations or coherent GNS. Need representation of kernels / `ker M_d ⊗ ...`; compatibility.
- GNS requires τ on whole A, not just finite truncation. Finite matrix can create a GNS for V_d but not A.
- If commutativity absent, add `FlatExtensionTheorem` with proof. Without, cannot invoke CF.
- all-d rank loop not finite unless D and theorem.
- supports conditional extension; not MUB claims.

4. Computational:
Table perhaps:
- fixed 24x24 rational PSD/rank/equality: tractable O(24³), exact.
- verify supplied arch certificate of fixed degree/block: tractable (multiplications, coefficient equalities, exact PSD), but if multiple blocks.
- search cert: ETR, not generally tractable, denominator/degree unknown.
- rank loop: each d easy; global infinite no.
- GNS: after τ/state matrix exists, linear algebra; constructing global τ not resolved.
Conclude:
  - Current implementation: use rank checks as diagnostics/certificate, not closure.
  - For accepted generic noncomm candidate, need arch representation theorem and explicit arch bound/certificate or direct finite-dimensional state. If certificate is a refutation, use to reject.
  - If a proved noncomm flat extension theorem plus finite stabilization bound, (b) is cheaper.
Question asks singular "Which route is computationally tractable ...?" Answer likely: fixed-block rank route b is computationally tractable, but not logically sufficient. We can state exact nuanced answer in bold:
"At the level of 24x24 exact rational linear algebra, (b) is the tractable one. This does not make (b) a valid proof for generic noncommutativity. (a) is easy only to verify a supplied certificate, not to discover one. Therefore neither supplies an unconditional end-to-end closure in current file."
This directly answers.

5. Lean theorem specification.

Need decide exact theorem shape. We can give two conditional lemmas:
- `archimedean_refutation_bridge`: candidate violates? `W` etc.
- `projector_moment_soundness_bridge`: from a noncomm representability certificate (not just arch identity).
But user asks exact theorem needed "to close ProjectorMomentSoundnessBridge". We can formulate target and assumptions.

Let's design code in Lean 4 style, perhaps not compile due placeholder definitions. We can explicitly say signatures schematic around existing namespace but logically exact. Need maybe use `ℂ` and `Matrix`. Lean mathlib supports `StarRing`, `StarOrdered`? Better avoid uncertain names. Define abstract interface structures to be implemented. We can write a paper specification with `NCAlgebra`, etc. They ask Lean 4 theorem specification, likely code block accepted. We can define minimal classes and theorem.

Potential:
```
namespace MUB6
namespace MomentPositivityObligation

structure Candidate where
  n : Nat
  -- generator tags ...
inhabited ...

structure Scope where
  Candidate : Type
  mem : Candidate → Prop

structure RationalMomentSystem (C : Scope) where
  D : Nat
  eval : Fin (D+1) → Matrix (Fin 24) (Fin 24) ℚ
  archm : ...
...
def Represents (S : ...) (τ : A C → ℂ) : Prop :=
  ∀ d, ...
def PositiveUnitalTrace (τ : A → ℂ) : Prop := τ 1 = 1 ∧ ∀ a, 0 ≤ τ (a * a)
```
Lean order on `ℂ` no order. Use Hermitian and `0 ≤` star order notation, or use `PosMulDef`:
- mathlib has `PosMulDef` for ordered ring? For complex C*-algebra, `starRing` and `StarOrdered?` C*? There is `CStarAlgebra`, `StarOrdered`? We can abstract `PositiveFunctional` as a Prop assumed, avoiding compile dependencies. But "precise formal Lean insight" can define:
```
class PositiveTrace (A : Type*) [StarRing A] [AddCommMonoid A] where
  pos : ...
```
Yet positivity on a complex * algebra isn't scalar complex order. Could use `0 ≤ₛ` from `StarOrdered` in mathlib (notation maybe `≤ₛ`). I recall mathlib:
- `PosMulDef` for `OrderedSemiring`
- `StarOrdered` module? In C* algebra, `star_ordered`? 
Lean code need not compile if placeholders clearly identified.

Could formulate via `CStarAlgebra` and `Complex`? Define abstract `PositiveUnitalFunctional`:
```
structure NCPFunctional (A : Type*) [StarRing A] [AddCommMonoid A] [Module ℂ A] where
  toFun : A → ℂ
  map_one' : ...
  positivity' : ∀ a, IsHermitian (τ (a * a))
  nonneg' : ∀ a r : ℝ, 0 ≤ r → IsHermitian (τ ((a* a) * r)) ...
```
Better: In C*-algebra scalar order for Hermitian: `IsHermitian x` and spectrum nonnegative, hard.

Use abstract `PositiveState` predicate already formalized in file:
```
def PositiveTrace (τ : A → ℂ) : Prop :=
 τ 1 = 1 ∧ ∀ a, τ (a* a) = 0 ∨ ... 
```
Cannot define positivity over complex. Could represent A concretely as `H → H` with H inner-product and use `0 ≤` operators. In concrete finite matrices, there is canonical positive operator preorder:
```
def Pos (T : H → H) := ∀ x, 0 ≤ inner ... 
```
If H=Euclidean finite, inner product ℝ or ℂ and real part. Define `IsPSD`.

Could use matrices and `StarRing` plus theorem `[∀ T, 0 ≤ T ↔ ...]`, but no global order.

Abstract theorem interface is acceptable:
```
def PositiveUnitalTrace (A : Type*) (τ : A → ℂ) : Prop
```
declared in existing file and required to unfold to positivity. Specify semantic expansion in prose.

Arch certificate exact:
```
structure ArchNC certificate (Q : NCQuadraticModule A) where
  bound : ℚ
  hbound : bound > 0 ∧
    Q.sumHermitianSquares? ... = ...
```
For representability, what identity? Could avoid pretending module identity constructs τ. Define:
```
structure ArchimedeanRepresentationCertificate ... where
  archN : ...
  archWitness : ...
  separationAlternative : ...
```
Need make exact enough.

Maybe theorem can take actual `τ` as assumption:
```
(hτ : PositiveUnitalTrace ...)
(hmom : Realizes τ X)
```
Then conclusion is GNS, trivial and doesn't resolve finite-to-global. Not acceptable.

We need assumption that is a genuine finite certificate and representation theorem. We could state an abstract theorem `NoncommArchimedeanRepresentation` as a premise, but then central work hidden. Better show required result:
```
(hrep : ∀ X, Q.ArchimedeanAt X → Q.Represents ...)
```
No.

Let's reason what a valid arch certificate for existence could be. In moment problem, to prove primal feasibility, a certificate isn't usually SOS; one gives rational moment matrix. If matrix PSD and all constraints, it is primal feasible. A theorem says under NMP conditions, there is measure. Archimedean module Positivstellensatz can provide this via duality: feasibility of SDP means no separating dual element. A finite primal matrix plus equality constraints is already the state on finite V, but extension theorem gives state. Could state an Archimedean **representation condition**, not refutation:
- moment data satisfies linear constraints
- for every polynomial q in an appropriate finite set? A dual separation condition? To conclude state, need all d.
Maybe module is quotient dual cone and certificate means a strictly positive element? Krivine Positivstellensatz.

For commutative real quotient K, a linear functional L has K-moment functional iff `L(f²)≥0` for all f in K (Riesz-Haviland). Archimedean quadratic module can test? A quadratic module representation:
`L(f) ≥ 0` for f ∈ Q(K) iff L is moment functional. To verify for all Q elements, enough generators due sums? For all σ, check Gram matrices.
In noncomm, state positivity requires `τ(a*a)≥0` all a. A finite basis cone may need closure.

Could use a certificate consisting of a **positive trace on the finite-dimensional operator span** that exactly matches all monomial moments. If candidate operators are actual finite matrices and block is a density matrix ρ, then this is enough and computational. For free noncomm algebra, not.

Maybe declared region includes actual 6x6 projectors. Then `Etilde` is concrete matrices, and a state on `M_6(C)` is density matrix. If all algebra/moments are represented by ρ, state realization immediate. But context says noncomm polynomial algebra universal, likely lifts finite matrices. A positive functional on `M_6(C)` is physical.

Let's perhaps formulate theorem abstractly at correct logical level and state exact missing premise. Lean closure can be:
```
theorem ProjectorMomentSoundnessBridge
    (R : DeclaredRegion)
    (c : Candidate R)
    (X : NCMoment
```
</details>


---
