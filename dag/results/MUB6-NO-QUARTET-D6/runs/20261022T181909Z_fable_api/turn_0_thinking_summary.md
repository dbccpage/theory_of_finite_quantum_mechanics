I recall that this relates to known literature on mutually unbiased bases — specifically the Jaming–Matolcsi–Móra–Szöllősi–Weiner work characterizing vectors unbiased to both the standard basis and the Fourier matrix F₆, which bears directly on whether a complete set of 7 MUBs in dimension 6 exists.

I'm also recalling Brierley and Weigert's computational work from 2008 showing F₆ can't extend to a quartet, and related constructions by Matolcsi, Réffy, and Szöllősi. Given the question's instruction to prove the largest honest finite piece if the full result is out of reach, I'm weighing what a realistic Lean formalization would require—classifying all common rays of F₆ amounts to solving a polynomial system in ten real unknowns, which is a substantial undertaking.

I'm connecting this to biunimodular sequences: vectors unbiased to both the identity and F₆ correspond to sequences that are unimodular and whose discrete Fourier transform is also unimodular. I recall the classification of length-6 biunimodular sequences is known to have exactly 48 solutions, tied to work by Björck–Saffari and Haagerup on finite biunimodular sequences.

Björck and Fröberg's 1991 paper found 156 cyclic 6-roots total, with 48 being unimodular, while Haagerup's work covered cyclic p-roots for prime lengths. Classifying common rays of F₆ fully equivalent to classifying these unimodular cyclic 6-roots would require a Gröbner-basis-level polynomial system solve in 5 unimodular unknowns, which is far too ambitious to formalize in Lean 4 from scratch without computational tools.

Instead I should aim for the largest honest finite piece I can actually prove. Deriving the exact parametrization is out of reach, but I could instead establish the clean algebraic characterization: show z is a common ray of F₆ exactly when z_0 = 1, all |z_i| = 1, and the autocorrelations vanish for shifts 1 through 5 — the standard equivalence between the Fourier magnitude condition and the autocorrelation sequence being a delta function.

This would require working through the inverse DFT with explicit sums over Fin 6, which is doable but tedious in Lean. Alternatively, I could instead verify a specific finite list of known common rays directly and check pairwise unbiasedness, though without a computer this verification is risky too.

I'm trying to recall the explicit structure of the 48 biunimodular vectors for F₆ from the Jaming et al. literature, since those form the known family worth checking.

Actually, I should think about the Gauss sequence construction: for n=6, z_k = e^{πik²/6} with ζ₁₂ as a 12th root of unity gives a candidate biunimodular sequence, and I'm working out its values for each k.

Since the sequence is 6-periodic, I recognize this sum as a quadratic Gauss sum with magnitude √6, and I'm trying to recall the exact formula for even moduli to pin down its phase.

This confirms the Gauss sequence works. Now I'm thinking about the symmetry group acting on biunimodular sequences — translations, modulations, reflections, decimations by units coprime to 6, plus global phase and conjugation — and whether the orbit of the Gauss sequence under these operations accounts for all 48 known rays for n=6, trying to recall the Björck–Saffari results on this.

I'm fairly confident about 48 vectors forming 16 mutually non-unbiased bases, with the 48 vectors likely being quadratic-phase sequences whose entries are 12th roots of unity. I'm trying to work out which quadratic-phase sequences of length 6 actually satisfy the biunimodularity condition.

This looks like a generalized Gauss sum, and I'm checking that its modulus stays √6 whenever gcd(a,6)=1, verifying the cases a=1, 5, 7, 11 by completing the square or relating them via sign factors back to the base case.

I'm counting distinct sequences z_k = ζ^{ak²}ω^{bk} by tracking which (a,b) pairs give genuinely different sequences versus just shifts of each other, but the count of 12 I'm getting doesn't match the expected 48, so I still need to account for cyclic shifts as another source of equivalence.

Since there are only 12 quadratic-phase sequences and I need 48 total rays, there must be additional constructions beyond these quadratic phases. I'm thinking about whether F₆ decomposes via CRT into a tensor product of F₂ and F₃ since 6 = 2·3 with gcd(2,3)=1, which could generate more biunimodular sequences.

Testing (1, ω₃, ω₃) by computing each of the three modulus conditions confirms they all equal 3, so this sequence satisfies the biunimodular property.

Applying modulations and conjugation to this base sequence generates six total 3-root-of-unity solutions: (1, ω₃, ω₃), (1, ω₃², ω₃²), (1, ω₃², 1), (1, 1, ω₃²), (1, ω₃, 1), and (1, 1, ω₃). I'm now wondering whether additional biunimodular sequences of this length exist beyond these.

For length 3, Haagerup's theory connects biunimodular sequences to cyclic 3-roots, where the symmetric function conditions force x, y, z to be exactly the three cube roots of unity, giving 6 unimodular solutions total. Combining this with the n=2 case via tensor products should yield 12 sequences for the combined F₂ ⊗ F₃ structure.

For n=6, I recall Björck and Fröberg found 156 cyclic 6-roots overall, and I believe 48 of these turn out to be unimodular — though I want to double-check that number since it's key to counting the actual biunimodular sequences of length 6.

So F₆ can't be extended into a MUB quartet. I'm also recalling that the connection between biunimodular sequences and cyclic n-roots works by taking ratios of consecutive entries in a unimodular sequence to generate a solution to the cyclic n-roots system.

This correspondence means the number of biunimodular sequences of length n with first entry fixed equals the number of unimodular cyclic n-roots, so for n=6 with 48 such roots, that gives 48 common rays total—12 from the quadratic-phase family plus 36 others whose structure I'm still trying to pin down.

For n=6 specifically, I recall Björck–Fröberg's work on cyclic 6-roots involves solutions with coordinates in ℚ(√-3), alongside others tied to more complicated polynomials. I'm also considering whether some biunimodular sequences could arise from a tensor-like construction on F₆ ≅ F₂ ⊗ F₃, combining different length-3 biunimodular sequences.

Working through this, applying F₂⊗F₃ to a pair of length-3 blocks gives conditions requiring the orthogonality of their DFTs and that the squared moduli sum to 6 at each frequency — so I need two length-3 unimodular sequences whose transforms satisfy these constraints.

That ratio isn't real except trivially, so conjugation or shifting doesn't easily give a second solution this way. I'm trying to recall whether there's a more general family where the magnitudes aren't equally split, and whether the JMMSW paper's explicit construction (the Fourier matrix F₆ based MUB-triplets) covers this case directly.

I'm not fully certain whether the entries are 24th roots of unity or something else, so let me try actually deriving the 48 vectors directly: setting up a unimodular vector with zero autocorrelation against the Fourier matrix and working through the constraint equations.

Using symmetry, c₃=0 reduces nicely to a single real-part condition on z₃ and z₁ (with z₅ appearing via conjugation), since c₃ is automatically real due to the pairing structure.

This is getting complex, so I'm stepping back to think about what's realistically provable in Lean given I can't test-compile anything — I need something I can write with high confidence on the first try. I'm considering characterizing common rays of F₆ purely via the autocorrelation conditions: unit magnitude entries with z 0 = 1, plus the vanishing sum conditions for each shift j ≠ 0.

Substituting l=i+j turns the norm into a sum over the autocorrelation coefficients c_j weighted by ω^{-jk}, with c_0=6 fixed. So |ẑ_k|²=6 exactly when all c_j vanish for j≠0, and the converse follows by Fourier inversion since the condition holding for every k forces each c_j to be zero.

The forward direction is a quick expansion, while the converse needing inversion is the harder of the two but both seem tractable with explicit term expansion, though I should question whether this is really the most valuable piece to pursue—the task calls for parametrizing common rays exactly, and autocorrelation characterization gives known structure but not a full parametrization. I'm considering instead isolating a sub-family, like the twelve quadratic-phase Gauss sequences, to show they're common rays and check whether they're pairwise unbiased.

Computing the overlap sums between Gauss sequences with different parameters, I find the same-a case gives norm-squared values of either 0 or 36 which checks out, and now I'm working through the cross terms between a=1 and a=5 sequences, reducing to a sum involving cube roots of unity and working out the individual term values.

Checking the other cases confirms it: odd c gives zero, even nonzero c gives modulus² = 12, never matching the target 6. So none of the 12 Gauss rays are mutually unbiased with each other — makes sense since they stem from an F₂⊗F₃ structure that's really just a sub-family, so this obstruction needs to be checked more broadly.

Since I can't verify all 48 pairs without knowing them explicitly, I'm wondering if a different Hadamard matrix choice would make this easier — maybe the Tao matrix S₆, which has cube-root-of-unity entries and might be known to have no vectors unbiased to both I and itself. I'm trying to recall results from Björck's or related work on this matrix.

I'm not fully certain whether S₆ belongs to no MUB triplet at all, or just can't be extended nicely. Proving a matrix has zero common unbiased rays with any other Hadamard matrix seems like it would be just as hard as the original polynomial-system problem, unless there's special structure like cube-root-of-unity entries that simplifies things.

I'm wondering if there's a structural shortcut—some constraint forcing any two common rays of F₆ to fail the unbiasedness condition—rather than fully classifying them. But I don't recall a slick argument; the known proof that no quartet contains F₆ seems to rely on computational Gröbner basis methods.

One idea: a biunimodular vector z corresponds to a circulant matrix whose normalization is unitary, meaning it's essentially a circulant complex Hadamard matrix, which could give a classification route.

But thinking through the MUB quartet literature, the nonexistence results for extending {I, F₆} seem to all rest on computation rather than a clean argument, so I probably can't find an elegant proof. The honest path forward is to lay out the autocorrelation condition, construct the known explicit common rays (like the Gauss sum family), rule out the sub-family computationally, and be upfront about what remains unresolved.

I'm now wondering whether the CRT decomposition of Z/6 as Z/2×Z/3 could let me factor F₆'s structure through F₂ and F₃ tensor pieces, which might actually enable a full classification of all 48 solutions rather than leaving it to brute enumeration.

1)^{k₂l₂}·ω₃^{2k₃l₃}, which shows F₆ factors as a tensor-like product of F₂ with a permuted/conjugated version of F₃. This means the common rays of F₆ correspond (up to index permutation) to common rays of F₂⊗F₃, so I can analyze the problem by splitting z into a 2×3 array and writing the magnitude conditions in terms of sums over each block.

This reduces to requiring |A_m|²+|B_m|²=6 and the real part of conj(A_m)B_m vanishing for each m. Looking at the length-3 DFT of a unimodular triple, the magnitude squared of each Fourier coefficient depends on the correlation sum c₁ formed from the unimodular entries, so |U_m|² decomposes into 3 plus a cosine-weighted term involving c₁.

Setting |A_m|²+|B_m|²=6 constant for all m forces the combined correlation term s = c₁(z⁽⁰⁾) + c₁(z⁽¹⁾) to vanish entirely, since its real part times each cube root of unity must be zero for all three m simultaneously. That means c₁(z⁽¹⁾) must equal the negative of c₁(z⁽⁰⁾), which is a clean constraint linking the two triples.

Now I still need the orthogonality condition Re(conj(A_m)B_m)=0 for each m. I'm parametrizing z⁽⁰⁾=(1,p,q) and z⁽¹⁾=(r,s,t) as unimodular complex numbers, writing out c₁ for each triple explicitly, and combining these into the two real constraints that must hold together.

By DFT invertibility this gives three equations e_j=0 for j=0,1,2. Setting e_0=0 yields a real-part constraint on 1,p,q,r,s,t, and I'm now working out e_1=d_1+conj(d_2) by expanding the cross-correlation terms involving s, p, t, q, r.

That gives five real equations in five real unknowns, expecting finitely many solutions (48), but still too hard to solve by hand. I consider restricting to 12th roots of unity, but checking 12^5 candidates is computationally infeasible for Lean's kernel. The full classification seems out of reach for a single-shot approach, so I need to settle for delivering a partial result: just the definition of F₆ as a structure.

I'm now working out how to define fourierSix with explicit entries and whether it needs RawHadamard as a wrapper, checking the interfaces of quartet_iff_ray_bases and HasRawQuartet to figure out what hypotheses my final theorem actually requires.

Similarly, RawMU likely encodes the mutual unbiasedness condition via an overlap computation giving normSq 6. Without the full definitions, I realize I can't establish hpair unconditionally, so the final theorem can't be proven outright — I need to figure out what honest partial results are deliverable, starting with defining fourierSix explicitly using an algebraic root of unity ω.

A second useful piece would be a characterization theorem: expressing what it means for a vector z to form a common ray with fourierSix in terms of its first coordinate being 1, unit normalization, and vanishing autocorrelation sums across nonzero shifts.

For the proof, I'm considering explicit setups for ω as a sixth root of unity, deriving its powers and conjugate relations, possibly leveraging Mathlib's primitive root machinery via the exponential form instead of hand-rolled coordinates.

I'm trying to recall the right primitive-root lemma to show that ω² acts as a primitive 3rd root of unity, so I can derive sums like 1 + ω² + ω⁴ = 0 from the general geometric-sum vanishing fact.

Writing the explicit proof...

I work out the algebra confirming `linear_combination (-1/4) * h3` closes the goal, since the difference reduces exactly to a multiple of h3's normalized form, and note `nlinarith [h3]` should similarly succeed once √3·√3 is treated as an atom matching h3's statement.

For the characterization theorem, I'm now thinking through how to expand the sum over Fin 6 into six explicit terms involving powers of ω depending on indices k and i, handling each case of k via fin_cases.

Then normSq of that sum needs expanding into real and imaginary parts across 12 real unknowns, which balloons into a quadratic form with many monomials when relating to the autocorrelation sums—doable by `ring` in principle but risky to set up correctly without testing. I should look for a more structural approach instead of brute-forcing this computation.

A cleaner route is to work directly in ℂ: express the normSq of each transformed value as a product with its conjugate using `Complex.mul_conj`, expand into a double sum, and then reindex that double sum over Fin 6 using modular shifts, since Fin 6 addition is already mod 6.

Still working out exponent reduction mod 6...

To get orderOf ω = 6, I'd need to check ω^6 = 1 and that ω^(6/p) ≠ 1 for each prime divisor p of 6, which there's a Mathlib lemma for directly establishing order from such conditions.

Actually I prefer a self-contained approach: proving ω^n = ω^(n%6) directly using Nat.mod_add_div to split n into its remainder and quotient parts, then simplifying using ω^6 = 1. Writing the periodicity lemma...

Now I'm moving on to the key orthogonality sum: for n : ℕ, the sum over Fin 6 of ω^(nk) should equal 6 if 6 divides n and 0 otherwise.

I'm reducing this using n%6 since ω^(n·k) depends only on (n·k)%6, which via `Nat.mul_mod` reduces to ((n%6)·k)%6. Then I can case split on r = n%6 ranging over 0 through 5, checking each case explicitly (r=0 gives 6, r=1 gives the full root sum which vanishes, and so on using symmetry of the roots of unity).

I realize it's cleaner to compute ω³ = -1 directly, giving ω⁴ = -ω and ω⁵ = -ω², which makes verifying 1 + ω² + ω⁴ = 0 and the full sum identity straightforward by splitting into real and imaginary parts rather than expanding powers via simp.

I can verify these identities using Complex.ext and sqrt facts for the base cases, then chain everything else via linear_combination with those established facts—like deriving ω⁶ = 1 directly from ω³ = -1. For the full DFT theorem, I'm weighing whether to handle the sums over Fin 6 generically through reindexing lemmas or just brute-force expand into all 36 terms.

For the brute-force route, I'm defining S_k as the overlap sum and working out that conj(ω) equals ω⁻¹ which is ω⁵, so normSq(S_k) can be expressed via the mul_conj identity, connecting the overlap values back to the autocorrelation sequence c_j.

Setting j = i - l confirms the sum matches c_j as defined, so the identity checks out. This is really a polynomial identity modulo ω^6 = 1, and finding a clean coefficient for linear_combination feels messy, so I'm considering whether ring_nf could simplify things instead.

Decomposing into real/imaginary parts with √3 also seems unwieldy given the scale of the expression, so I'm leaning toward a more structural approach using Fin arithmetic instead.

I recall Mathlib giving Fin n a CommRing instance for positive n, so I could potentially index things via Fin 6 and get the ring structure for free, making the individual steps simpler.

I can show the multiplicativity property holds using the core `Fin.val_add` and `Fin.val_mul` lemmas combined with the periodicity of ω's powers, confirming χ is a proper character. This lets me define the Fourier matrix entries directly as powers of ω indexed by the product of row and column indices.

Now I'm working out that the conjugate of χ equals χ evaluated at the negation, using the explicit value of conj(ω) as ω⁵ and tracking how negation behaves in Fin 6.

I verify all six remaining cases hold, confirming the uniform identity holds for every value of k, so I try crafting a single rewrite using `star_pow`, `hconj`, and `omega_pow_mod` to match exponents mod 6, then check whether `fin_cases a <;> rfl` closes it by looking up how `Fin.neg` computes `(-a).val`.

I'm reasoning through whether `rfl` can actually close this since the kernel should evaluate the Nat literal arithmetic directly, though I'm worried the `Fin` value after `fin_cases` might be wrapped in a subtype form that blocks definitional reduction.

I'm weighing whether `fin_cases a <;> rfl` will actually close all cases, since `rfl` needs to unfold through the `Fin` negation instance definitionally — that should work since it's just a computation, but I'm considering a fallback using `congr 1` with `decide` on the underlying natural number equation if `rfl` fails on some case.

I'm fairly confident `rfl` handles this numeric reduction, but as a fallback I could use `decide`, since it's just a decidable Nat equality that the kernel can evaluate directly.

That seems to work for the Fin case goals. Rather than wrestling with Fin negation further, I should step back and consider formulating the main theorem directly in terms of the sum S(k) = ∑ i, star(fourierSix i k) · z i, expressed via the character χ(-(i·k)) z i, and think about what's needed to compute its squared norm.

Expanding |S(k)|² as a double sum and reindexing i = l + j, the cross terms collapse into a convolution-type sum c_j = ∑_l star(z_l) z_{l+j}, giving normSq(S k) = ∑_j χ(-(jk)) c_j, with the j=0 term contributing 6 since c_0 is real.

For the converse, I'm using orthogonality of characters: averaging χ(jk) times the assumed identity over all k and swapping summation order shows each c_j for j≠0 must vanish, since the character sum ∑_k χ((j-j')k) picks out only the j'=j term, scaled by 6.

Now I'm outlining the two generic lemmas I'll need: basic character properties (additivity, χ0=1, star relation, inverse), and an orthogonality relation stating the sum over k of χ(a·k) equals 6 when a=0 and 0 otherwise, which I plan to prove by case-splitting on a and computing directly for the nonzero cases.

Verifying the a=1 case checks out algebraically, and for a=2 I'm factoring 1+ω²+ω⁴ using hF2 to confirm the identity holds.

For a=4 and a=5, the pattern matches cases already verified (a=2 and a=1 respectively), so those cases check out too. Now I'm worried about whether simp can actually reduce the modular exponent arithmetic in Fin 6 to literal numerals automatically, since `χ (a * k)` needs `(a * k : Fin 6).val` to simplify properly using something like `Fin.val_mul`.

Rather than fighting with Fin numeral simplification, I think it's cleaner to restate the orthogonality lemma using a natural number exponent instead: summing ω^(n * k.val) over Fin 6, equal to 6 if n is divisible by 6 and 0 otherwise. That avoids needing fin_cases on Fin products entirely.

I'm doubting whether Mathlib has direct simp lemmas like `Fin.val_three` for small numerals, so I'm considering unfolding via `Fin.sum_univ_succ` repeatedly instead, building up the value through `Fin.succ` and `Fin.val_succ` steps.

I'm checking whether Lean's unifier can match `Fin 6` against `Fin (?n+1)` for the successor lemma to apply, and recalling that Mathlib likely has dedicated lemmas like `Fin.sum_univ_six` that would make this simpler than unfolding manually.

I'm trying to recall whether simp has a lemma that unfolds `Fin.val (OfNat.ofNat 3)` down to `3 % 6`, since the `OfNat` instance for `Fin (n+1)` is defined via mod reduction and Lean's `Nat.reduceMod` simproc should handle the arithmetic once unfolded.

Actually, maybe safer to build things up via `Fin.succ` recursion so simp's numeral reduction handles `0+1`, `1+1`, etc. step by step, letting Nat.reduceAdd simplify each val to the literal, though the resulting exponent expressions like `ω^(n*(0+1+1))` will still need further simplification afterward.

Rather than a general reduction lemma that would loop as a simp rule, I'm thinking I should just enumerate specific power identities like ω^8 = ω^2, ω^9 = ω^3, ω^10 = ω^4, and so on up through the powers that actually appear, each reducible via ω^6 = 1.

That checks out since the kernel can reduce Nat.mod on literals directly. As an alternative to enumerating powers individually, I'm considering using linear_combination with the hω6 relation to directly collapse the orthogonality sum, like showing 1 + ω^2 + ω^4 + ω^6 + ω^8 + ω^10 reduces to 0 after simplification.

Let me recheck that factoring attempt—the coefficients aren't canceling cleanly, so I need to verify (1-ω³)(1+ω³) actually equals 1-ω⁶ and recompute the difference term by term.

This checks out algebraically. I should also verify the simp normal form matches what linear_combination expects, since the exponents reduce cleanly via Nat.reduceMul and pow_zero before ring1 normalizes everything.

If simp doesn't fully reduce exponents or Fin values to numerals, ring will treat them as opaque atoms and fail, so the real priority is making sure every Fin coercion resolves to a concrete natural number first. A safer plan is to expand sums over Fin 6 using Fin.sum_univ_six, then separately discharge each Fin.val numeral equality with decide or rfl before feeding things to ring.

I'm confirming that `(2 : Fin 6).val` reduces to `2` definitionally, so either `rfl` or `decide` should close that equality, and I recall Mathlib might also have a simp lemma like `Fin.val_ofNat'` that handles this directly.

To be safe, I'm sketching explicit helper lemmas for each value 0 through 5 proving their `Fin 6` coercion equals the natural number, planned for use with `simp only [Fin.sum_univ_six, ...]`, and considering whether such a simp set will syntactically match numerals appearing in the goal.

I'm confident the family of product lemmas up through eight exist in Mathlib, matching the mathlib3 naming convention. Now I'm considering whether to prove the main identity by brute-force polynomial expansion or find a cleaner structured approach using a reindexing argument with the root-of-unity relation.

Defining the correlation sum and expanding the product of sums into a double sum, using that the conjugate of the Fourier coefficient picks up the opposite character value, so I can apply the standard double-sum expansion lemma to separate the terms.

That confirms the final form matches the target sum. I'm checking Lean lemma names for swapping sums and reindexing via the additive shift equivalence on Fin 6, since it's an additive commutative group these equivalences should apply directly.

Then I verify the ring identity -((l+j)k) + lk = -(jk) holds by `ring` since Fin 6 carries a commutative ring structure.

Right, confirming `Fin.instCommRing` exists for `NeZero n` so `ring` works on `Fin 6`, though Mathlib tends to discourage relying on `Fin`'s ring structure. As an alternative, I'm considering sidestepping `ring` entirely and instead using multiplicativity of χ together with the identity χ(-a)·χ(a) = 1 to manipulate the exponents directly.

Since there are no numerals involved, `ring` should work fine here. I also need the fact that χ(-a)·χ(a) = 1, which follows directly from χ_add and χ_zero. Checking potential pitfalls now: coercions, the `star` operation on ℂ, and showing that star(χ a) equals χ(-a) using the power representation of χ.

I'm verifying that star ω = ω^5 by computing both sides directly — star ω is the conjugate ⟨1/2, -√3/2⟩, and ω^5 simplifies to 1-ω which matches. In Lean, I can establish ω^5 = 1 - ω using linear_combination from the defining equations for ω.

Remainder matches -1 times the second relation, confirming c₂ = -1 works for the linear combination. I verify star ω = 1 - ω by checking real and imaginary parts component-wise, then move to showing star of χ(a) equals χ(-a) using the conjugation property.

I'm uncertain whether omega automatically knows the bound on a.val, so I should add a.isLt explicitly first. Then I need to confirm the Mathlib lemma for negation on Fin, something like Fin.coe_neg giving the value as (n - a) % n.

If I can't pin that down safely, I could sidestep by proving the goal case-by-case with fin_cases and rfl instead of relying on the negation lemma, or alternatively work with ZMod 6, which reduces definitionally to Fin 6 anyway.

Actually, I think avoiding negation entirely by working with star values is cleaner: using the multiplicativity of χ and the fact that star(χ(x)) χ(x) = normSq(χ(x)) = 1, I can rewrite the needed identity purely in terms of products of χ at shifted arguments without introducing any subtraction.

I'm confirming that normSq is multiplicative via map_pow, and that normSq ω = 1/4+3/4 = 1, which avoids needing `-a` in the forward direction. For the converse orthogonality argument, I need to handle the sum ∑_k χ(jk)·star(χ(j'k)) by rewriting it as χ((j-j')k) using properties of star and negation.

Multiplying through by χ(j₀k) and summing over k, the orthogonality relation collapses the sum to 6c_{j₀}, forcing each c_{j₀} to vanish — confirming the converse direction. I'll need `Finset.sum_comm` to swap the order of summation in Lean.

Using `Finset.sum_eq_single` confirms that route works cleanly. Stepping back, I think the DFT characterization theorem is achievable in maybe 150-250 lines with moderate risk, and it's a genuinely valuable deliverable since it's the classical reduction towards parametrizing common rays via cyclic 6-roots and biunimodular sequences, directly relevant to the task's suggested example.

A second useful piece would be exhibiting the 12 explicit Gauss quadratic-phase vectors as common rays and proving none are pairwise unbiased, verifying this via the autocorrelation criterion using 12th roots of unity arithmetic with ζ² = ω.

I verify ζ² = ω using the minimal polynomial Φ₁₂(x) = x⁴ - x² + 1, confirming ζ⁴ = ζ² - 1 and ζ⁶ = -1. Now I'm working out the autocorrelation formula for the Gauss vector by summing conjugate products over shifted indices.

The orthogonality lemma collapses the sum to zero for nonzero shifts, which suggests I could prove the autocorrelation property generically for the whole family g^{(a,b)}_k rather than brute-forcing all 12 vectors against 5 autocorrelations. I need to be careful though, since k² mod 12 behaves differently from k² mod 6 when converting between Fin-indexed arithmetic for ζ and ω.

Writing out m = r + 6q decomposition so m² splits into r² plus a multiple of 12, confirming ζ^{m²} = ζ^{(m%6)²} since ζ¹²=1.

Substituting m = r + 6q, I can verify (r+6q)² = r² + 12(qr+3q²) by ring, and (r+6q) % 6 = r by omega since r < 6, which lets me split the power via pow_add and pow_mul. I'm now wondering whether to handle this generically or just explicitly check the specific case since a only needs to range over {1, 5}.

I'm weighing whether to prove the common-ray invariance under conjugation and modulation as generic lemmas, or just directly verify it for the specific Gauss vector g = (1, ζ, ω², -i, ω², ζ). The modulation invariance proof itself is straightforward algebra using χ being additive and star·χ = 1, but it's comparable effort to just brute-forcing the six-term sum directly with the ζ relations via linear_combination.

For the base-vector check, using g_k = ζ^(k²) the autocorrelation collapses nicely: c_j = ∑_k ζ^(-k²)ζ^((k+j)²), which simplifies using the quadratic expansion to a clean closed form in terms of j.

I'm now considering defining a Gauss sum family directly and checking inner products between its members via orthogonality, confirming the diagonal and cross terms reduce to known sums that avoid the forbidden value 6.

Working through the remaining terms, I get T_c = 1 + ω^{3(1+c)} + ω(ω^c + ω^{5c}) + ω⁴(ω^{2c} + ω^{4c}). I realize this doesn't match my earlier pairing with ζ^{4k²}, since that case involved a different exponent combination (a=1 vs a=5 giving ζ^{4k²}ω^{(b'-b)k}), so I need to track which pairing I'm actually computing.

Checking the conjugate relation, I verify that the conjugate of the a=1 family lands in the a=5 family, since ζ^{11k²} factors as ζ^{5k²} times a sign term absorbed into the ω exponent. That confirms the a=5 family is indeed the correct conjugate family, so I can now go back and recompute the overlap between the a=1 and a=5 families properly.

Checking c=1 and c=5 also give 0 by the same cancellation identity, leaving c=0 as the standout case giving 12. Now checking c=2, the terms don't cancel as cleanly, so I'm working through that sum carefully.

Finishing the c=3 and c=4 cases similarly yields 12 again, confirming the overall pattern: normSq always lands in {0, 12, 36}, never hitting 6, which satisfies the required condition. This points toward a sub-family exclusion theorem governing pairwise overlaps in the 12-element Gauss family.

Proving this formally in Lean would require expanding each of the six cross-term cases with explicit polynomial identities in ω and computing normSq evaluations, which is a substantial amount of risky computation. Given that compilation success and honesty are the key success criteria, I need to weigh how much of this detailed case analysis is worth attempting versus finding a more robust approach.

I think splitting this into two files is the safer strategy: one file with the solid, verifiable core characterization that I'm confident will compile, and a second file importing from the first that attempts the riskier sub-family exclusion. That way if the second file fails, the first result still stands on its own.

Actually, that conditional would have a false hypothesis since there are 48 common rays, not 12 — so the Gauss family can't be the complete answer, and I'd be misleading to frame it as the missing piece. I need to be upfront that this hypothesis doesn't hold rather than let a vacuously true theorem obscure that.

If I could describe all 48 common rays as orbits under a symmetry group, that would give a much stronger partial result — pairwise exclusion proven for the full known family, with only completeness left unproven, matching the literature claim. Let me try working out the 48 biunimodular sequences of length 6 using the F₂⊗F₃ decomposition, starting with the Gauss sequences before searching for the rest, and recalling what's known from Gabidulin's work.

I'm also trying to recall Björck–Fröberg and Haagerup's results on cyclic 6-roots — I remember something about 156 solutions with 48 being unimodular, which could tie directly into this count.

For n=6, the count seems to be 156 cyclic 6-roots total with 48 unimodular ones, matching JMMSW, and for n=5 it's 70 total with 20 unimodular. I want to connect these to circulant complex Hadamard matrices of order 6, since a biunimodular sequence of length 6 corresponds to rows being cyclic shifts of such a matrix, and I'm considering whether there's a known F₂⊗F₃ tensor structure underlying them.

Thinking about splitting z into CRT coordinates (z^(0), z^(1)) with constraints from cyclic sum conditions and cross-correlation terms, I consider the case where both components are individually biunimodular, each drawn from the six solutions with entries in the cube roots of unity, and work out how their cross terms must cancel.

Since X_j can't vanish for every j (the sum of squared magnitudes is clearly nonzero by Parseval), I need r² to equal -conj(X_{-j})/X_j consistently across all j with nonzero X_j. Testing the simplest case where u' = u, so X_j becomes the autocorrelation of u itself.

This forces r to be purely imaginary, r = ±i, giving the tensor product (1, ±i) ⊗ u — 12 solutions total, matching the known Gauss family count. I then check whether shifting u gives new solutions, but the shifted autocorrelation only has one nonzero term, which breaks the required condition, so shifts don't work.

Now I'm trying modulations of u by cube roots of unity, checking cross-correlations between u = (1, ω₃, ω₃) and a modulated version u' = (1, ω₃², 1) to see if they combine into valid solutions.

That fails since the condition forces r to be zero. Trying the conjugate case instead, I'm computing X_0, X_1, X_2 for u' = conj(u), getting values involving combinations of ω₃ and ω₃².

Trying another pairing: with u=(1,ω₃,ω₃) and a shifted u', I find X_0 and X_1 both vanish, leaving only X_2 nonzero at 3ω₃² — so I need to check if that single remaining condition can be satisfied.

Testing u' as the conjugate of the m=1 case instead, I compute X_0, X_1, X_2 and they're all nonzero mixed expressions, so now I need to check the orthogonality conditions against these values.

Setting up the j=0 and j=1 constraint equations, I find from j=0 that r² must equal -(2+ω₃)/(2+ω₃²), and verifying |2+ω₃|²=3 confirms this ratio is unimodular, so this candidate survives.

Continuing the computation, I find r² simplifies to 1, which contradicts the required r² = ω₃² from the j=0 equation, so this case yields no valid solution. I'll move on to check the remaining candidate configuration with u' = (1,1,ω₃).

Continuing the j=1 equation, I find it simplifies down to r² = 1, which conflicts with the earlier result, so this branch is inconsistent — confirming Case A yields exactly 12 solutions. Now I'm turning to Case B, where z^(0) and z^(1) aren't individually biunimodular and their first coefficients are opposite but nonzero, which requires solving the general system and apparently yields 36 solutions.

I want to understand the structure behind these non-root-of-unity solutions better, maybe by thinking about known constructions like Björck–Saffari sequences for composite lengths, or by approaching this through the classification of 6×6 complex Hadamard matrices, since circulant Hadamard viewpoints might reveal the pattern here.

I'm trying to directly solve for the unimodular sequence using the CRT decomposition into Z/2 × Z/3 components, splitting the indices by parity and residue mod 3 to set up the autocorrelation equations.

Computing d_0, d_1, d_2 explicitly confirms the condition reduces to 2Re(d_0)=0 and d_1+conj(d_2)=0, which matches (E3) exactly as derived.

Now I'm trying to find Case B solutions where the first Fourier coefficient is nonzero, and with 5 real unknowns against 5 equations I expect isolated solutions. Rather than brute-forcing 36 more cases by hand, I'm thinking about the symmetry group acting on these biunimodular sequences—cyclic shifts, modulation, reflection, conjugation, and decimation—to cut down the search space.

I'm also considering the Fourier transform symmetry: for n=6, applying the DFT to a biunimodular sequence and renormalizing gives another biunimodular sequence, since the double transform just reflects and scales. But testing this on the Gauss sequence, I notice the transformed entries aren't generally roots of unity, which complicates using this symmetry directly.

So the 48 solutions form a single orbit under shifts, modulations, reflection, conjugation, and Fourier symmetry that's closed within the quadratic-phase Gauss family, leaving the remaining 36 as separate orbits — I'm trying to recall what Björck and Fröberg found about their explicit form.

I'm also wondering if this connects to Haagerup's work on F₆ and the MASA/MUB problem for 6×6 matrices, or to Führ and Rzeszotnik's paper on biunimodular vectors for unitary matrices, which might characterize these remaining solutions more explicitly.

Trying a concrete approach for Case B, I'm considering decomposing the cyclic group of order 6 via CRT as F₃ ⊗ F₂, organizing the vector into three pairs so each pair lives in ℂ², hoping this structure reveals the solution set more directly.

Since |z|=1, each |α_b|²+|β_b|²=4, so I need ∑|α_b|²=6 specifically, plus zero autocorrelation for both sequences at nonzero lags — essentially treating this as three pair-vectors w_b with unimodular entries, where α_b is the sum and β_b the difference across the pair.

Writing |α_b|² in terms of θ_b, the angle between the two unimodular entries, gives ∑cos θ_b = 0 as the condition. Checking the Gauss-type solution where one sequence is i times the other, each θ_b = π/2 automatically satisfies this.

For another family I try angles (0, 2π/3, 2π/3), whose cosines sum to zero, which gives α with norms (2,1,1) and β with norms (0,3,3), and now I need to check the autocorrelation of β.

That's also a dead end — any single zero entry forces a cascade of further zeros that violates the modulus constraint, so all α_b and β_b must be nonzero, meaning none of the angles θ_b can be 0 or π. Now I need to work out the general zero-autocorrelation condition for a triple of nonzero complex numbers, treating it as three complex terms of specific moduli summing to zero.

This confirms the equal-moduli case gives the expected biunimodular triples with a phase shift of one of three values. For the non-equal moduli case, I'm checking whether the triangle inequality holds for the modulus triples of both sequences, and trying a symmetry-based ansatz, like requiring the coefficients to satisfy a conjugate-reflection relation, to search for Case B solutions.

Working through c₂ gives Re(b) + Re(conj(a)c) = -1, and now I'm computing c₃, which simplifies to 2Re(c + conj(a)b + conj(b)a) and needs to equal zero as well.

So I have three real equations constraining the phases of a, b, c — enough to pin down isolated solutions. I'm testing a symmetric Gauss-type configuration with z₁=z₅=ζ and z₂=z₄=ω², checking whether equation (ii) holds by computing Re(b) and Re(conj(a)c) explicitly.

Now I'm parametrizing a, b, c by their angles and trying c = -1 as a special case, which forces β-α = ±π/3 and leads to a relation between cos α and cos β that I'm working through.

Also trying c = 1, this gives cos α + cos β = 1/2, which fails. Then I'm testing c = ±i, taking γ = -π/2 and reducing the equations to expressions in sin α, cos β, and cos α.

I try β = α + π/2, which turns condition (ii) into -2 sin α = -1, giving sin α = 1/2, so α = π/6 or 5π/6. Both satisfy condition (i), and I confirm α = π/6 reproduces the Gauss sum pattern with ζ, ω², while α = 5π/6 gives a related solution involving ζ⁵ and ω⁴.

Checking this second case against the Gauss family form, I verify it matches with a=5, b=0 exactly. I also test β = α - π/2, but this makes condition (ii) require sin α - sin α = -1, which is impossible, ruling out that branch.

Then trying γ = π/2, I work through the resulting cosine equations for conditions (i) and (ii), eventually finding that β = α - π/2 combined with this γ value forces sin α = -1/2, giving α = -π/6 or 7π/6, with the first solution satisfying condition (i) automatically. I start computing the explicit values of a and b for α = -π/6.

For general c, I'm checking the constraint cos γ = -2cos(β-α) requires |cos(β-α)| ≤ 1/2, and trying to work through the remaining equations with δ = β-α to see if non-Gauss solutions exist. I'm also considering imposing conjugate symmetry so z becomes real, which would force the sequence into ±1 values.

Length-6 ±1 sequences with zero autocorrelation turn out not to exist, since c₃ reduces to an odd combination that can't equal zero. Trying an anti-symmetric variant also fails immediately since it forces z₀ to be imaginary, contradicting z₀=1. I'm now thinking about which number fields the 48 unimodular cyclic 6-roots actually live in, trying to recall relevant results from the literature.

I recall Haagerup's result that among the 156 cyclic 6-roots, 48 are unimodular, split between those with entries in ℚ(ζ₁₂) and another subset, though I'm not fully certain of the details. Rather than rely on memory, I'll try to directly solve the symmetric system with unequal moduli, setting up equations relating cos θ_b to the squared magnitudes of the α and β phase pairs.

Substituting u = α and δ = β - α, I'm expanding the three cosine equations into a system in u, δ, and γ, trying to reduce it down to something solvable by eliminating variables one at a time.

I'm parametrizing everything in terms of δ, setting cos γ = -2cos δ and sin γ = σr where r = √(1-4cos²δ), then expressing the two linear equations' coefficients A, B, C, D purely in terms of c = cos δ, s = sin δ, σ, and r in order to solve for cos u and sin u and enforce the Pythagorean identity.

This algebra is getting messy, so I try plugging in special values of δ instead — testing the known Gauss solution with δ = π/2 (which checks out giving cos γ = 0), then trying δ = 0 and δ = π/3 to see what γ values result.

For δ = π/3, equation (I) resolves to u = π/3, but checking it against equation (II) produces an inconsistency, so this value doesn't satisfy both constraints simultaneously. Moving on to δ = 2π/3, which gives γ = 0, I start working through equation (I) again to see if it holds.

That gives γ = ±π/3, but cos δ = -1/4 isn't a clean angle — so e^{iδ} = -1/4 ± i√15/4, which feels algebraic but unusual. I'm trying to recall if √15 actually shows up in the known examples from the literature on unbiased vectors, maybe in Bengtsson et al.'s work.

Let me actually test c = -1/4 directly in the symmetric ansatz, working out sin δ = ±√15/4 and checking the consistency with cos γ = 1/2, sin γ = σ√3/2, computing A, B, C from these values.

Checking this case, the amplitude works out to about 7.25, which exceeds 4, so this doesn't rule it out the way the previous sign choice did — I need to verify more carefully whether equation (I) is actually satisfiable here.

Now solving (I) directly: substituting cos u = x and sin u in terms of x into the Pythagorean identity gives a quadratic, 54.83x² + 8x - 37.83 = 0, which yields x ≈ 0.761 or x ≈ -0.907. Checking the first root, sin u comes out to about 0.649.

Testing this against equation (II), the result is about -0.146, which doesn't match the required 0.25, so I reject this solution; checking the second root similarly fails to satisfy (II). I'll try other sign combinations for s and σ next.

For the amplitude condition to reach at least 1, I need |B| ≥ √15/4, which rules out one sign choice but confirms B = -(√15+2√3)/4 works, pointing to σ = +1. With that, I compute C ≈ 0.0365 and start working out D.

Checking equation (I) under the x→-x symmetry gives two possible cosine values, but plugging both into equation (II) with the computed C and D both fail the target of 0.25, so c = -1/4 doesn't work. Switching to c = +1/4 instead, I get cos γ = -1/2, meaning γ = ±2π/3 and sin γ = ±√15/4.

Trying to solve the quadratic for cos u from equation (I), then checking both candidate roots against equation (II) -- neither satisfies it, so this particular case fails.

I'm working toward a cleverer elimination, treating the two equations as linear in cos u and sin u and solving via determinants, then imposing the unit-circle constraint on that solution to get a relation purely in δ and σ, introducing r and γ to parametrize things.

Simplifying further, the determinant reduces to ρ(1 - c² - s²), which is always zero since c² + s² = 1. That means the system is degenerate — the two equations are either inconsistent or dependent, so for consistency the linear forms must be proportional with ratio λ = -c, giving the conditions C = -cA and D = -cB that I need to check.

Working through those equations, I find either s = 0 or c = 0 with ρ = -s. Testing s = 0 gives cos γ values outside the valid range, so that case fails, but c = 0 with ρ = -s checks out consistently, yielding cos γ = 0 and sin γ = ρ = -s.

Confirming δ = ±π/2 give γ = ∓π/2 consistent with earlier results. Plugging back into equation (I) with A = 0 and B = ±2, I solve ±2 sin u = 1 to get sin u = ±1/2, producing u values at π/6, 5π/6 for one case and -π/6, 7π/6 for the other — four symmetric biunimodular sequences total.

Now I'm wondering about the non-symmetric cases, where z_k ≠ z_{-k}, and considering the unequal-moduli picture for α and β more carefully — looking at whether the pairwise products among the three moduli can form a valid triangle, since that geometric constraint would determine the angles in those solutions.

This translates into needing both α and β to be zero-autocorrelation triples, with the additional constraints that their total energies split as 6 and 4 per index, with α_b perpendicular to β_b. So the construction is: pick a zero-autocorrelation triple α with total energy 6 and each |α_b| ≤ 2, then build β_b as a perpendicular vector scaled to satisfy the energy constraint, with a sign choice ε_b ∈ {±1} at each index, and then check that this resulting β also has zero autocorrelation.

I'm checking the sign patterns of ε_bε_{b+1} products around the triangle — either all positive or exactly two negative. In the all-positive case with β proportional to iα, I note the Gauss case where all |α_b| equal √2 gives μ_b=1 trivially, but otherwise the two linear constraints on T_b force tighter conditions on the μ_b.

