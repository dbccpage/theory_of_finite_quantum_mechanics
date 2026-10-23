Without tools to compile, I need to settle for Lean 4 code that has a strong chance of working with recent Mathlib, accepting that a full classification of all 48 common rays isn't realistically achievable here.

I'm sketching the key pieces: defining F₆ with explicit entries using ω as a complex number, stating the characterization theorem for CommonRay in terms of unit entries and vanishing shifted overlaps, and possibly including the Gauss family with pairwise exclusion. I'm working out how CommonRay, overlap, and column should be defined in terms of the unknown SixMatrix/Mat abstractions from MonomialTransport, trying to infer their underlying Matrix type so my construction type-checks.

I'll assume `Mat ι = Matrix ι ι ℂ` and define `fourierSix` using `Matrix.of` so it's accepted by defeq regardless of how `Mat` unfolds, with `Matrix.of_apply` handling the simp lemma for entrywise access.

Confirming that defining the matrix with a plain lambda function typechecks fine since Lean unfolds the `Matrix` def during elaboration, even though Mathlib style discourages it.

Not worth overthinking the dot-notation mechanics — I'll just go with `Matrix.of` and open the right namespace with `SixMatrix`. Now I need to pin down ω as a complex number with real part 1/2 and imaginary part √3/2, and verify the key identity ω² = ω - 1.

Writing omega lemmas...

After ring normalization, the product term should become an atom matching the sqrt3_sq hypothesis, so nlinarith should close it fine even if plain linarith might struggle with the nonlinear term.

I'm worried about "no goals" errors if simp closes things unexpectedly, so I should consider a safer route using Complex.ext and explicit simp lemmas for real/imaginary parts followed by nlinarith with the sqrt3 squared fact.

Writing the omega_sq lemma proof...

I need to confirm that `sq` rewrites `ω^2` to `ω*ω` correctly, then verify the cube identity: using `linear_combination (ω + 1) * omega_sq` should work since expanding `(ω+1)(ω²-ω+1)` gives `ω³+1`, matching the goal's difference exactly.

For the sixth power identity, `linear_combination (ω³-1) * omega_cube` works since `(ω³-1)(ω³+1) = ω⁶-1`. Then for reducing exponents mod 6, I'm rewriting `n` using `Nat.mod_add_div` to split it into `n % 6 + 6 * (n / 6)`, then using `pow_add` and `pow_mul` along with the sixth-power fact to simplify away the multiple-of-6 part.

That rewrite only targets the single occurrence of `n`, so there's no looping issue. I'm also considering an alternative approach defining a character function on `Fin 6` and using its additive property instead.

Checking that the rewrite tactic correctly unifies the modular exponent pattern without accidentally matching the right-hand side, confirming the substitution only targets the sum term.

Then I verify that `χ_zero` follows from simplifying the Fin cast of zero with `pow_zero`, and I move to proving `normSq ω = 1` by expanding the complex norm squared formula to show the real and imaginary parts sum to one.

Next I use `map_pow` to extend this to `normSq (ω^n) = (normSq ω)^n`, which collapses to 1, and I start working out `star_χ` using `Complex.mul_conj` to express the unit circle relation.

I'm confirming `Complex.mul_conj` gives the normSq identity and checking how `star` relates to `conj` in Mathlib to make sure the lemma chain type-checks correctly.

Since `Star.star` appears as an applied subterm in the goal, rw should succeed as long as the instance paths match up to defeq, which they typically do since instances are reducible. I'll try `simp only [Complex.star_def]` as a more robust alternative, since simp handles instance matching more flexibly too.

Actually, to avoid relying on `Complex.star_def` entirely, I could instead use `Complex.normSq_eq_conj_mul_self`, which the repo also uses and sidesteps the star-to-conj conversion issue.

Writing the conjugate lemma proof...

I'm reasoning that kabstract should still match the star instance up to defeq even if there are multiple typeclass resolution paths, since it works at the ambient transparency. Given that the codebase already uses this lemma successfully with simp, I'm fairly confident the rewrite will go through.

I'm considering a fallback using `simp only [Complex.star_def]` followed by `rw [mul_comm, Complex.mul_conj]`, but weighing the risk that simp only might fail to make progress, so I'll stick with the `rw` approach for now. I'm also thinking about avoiding star altogether by reframing in terms of character negation, but decide that's extra complexity I don't need yet.

I'm now defining the overlap formula in terms of the matrix entries and sketching the main DFT characterization theorem, stating that a vector lies on a common ray iff it starts at 1, has unimodular entries, and satisfies a cyclic orthogonality condition for nonzero shifts. I'm setting up the proof structure, defining a sum S_k over characters and values of z, aiming toward a key identity under the unimodularity assumption.

Working through the normSq(S k) expansion, I'm substituting indices to rewrite it as a double sum, then using the multiplicative property of characters to factor out terms, pushing toward showing this equals a weighted sum of the cyclic correlation c_j across shifts j.

c_0 equals the sum of squared norms, which comes out to 6 by unimodularity, so normSq(S k) = 6 plus a sum over nonzero j weighted by character values. I'm now setting up the forward direction: assuming all c_j vanish for j≠0 should force normSq(S k) to collapse to just 6.

For the converse, I want to show normSq(S k)=6 for all k forces those nonzero c_j terms to vanish. I'm using orthogonality of characters—multiplying by a character and summing over k should isolate individual d_j coefficients, since the orthogonality relation ∑_k χ(j₀k)·conj(χ(jk)) picks out only the j=j₀ term, giving 6·d_{j₀} = 0.

For proving the orthogonality lemma itself, I'm thinking of a slicker trick: for a ≠ 0, multiply the sum S = ∑_k χ(ak) by χ(a), which just reindexes the sum via a shift and gives back S, so (χ(a) - 1)S = 0, and since χ(a) ≠ 1 when a ≠ 0, S must vanish. This avoids expanding the sum term by term.

I'm working out each inequality by taking the imaginary part of both sides and showing it leads to a contradiction, using that √3 is nonzero (via positivity or √3 ≤ 0 being false) to force the imaginary component argument through.

I can establish the real and imaginary parts of ω by rfl since it's defined as a structure literal that unfolds directly. For showing ω^a ≠ 1 across a = 1..5, I'm considering using fin_cases on a and computing powers directly for each resulting case.

I recall Mathlib's documented example uses `fin_cases p` with hypotheses for each value 0, 1, 2, so the generated goals likely just substitute the literal value directly rather than showing a subtype anonymous constructor.

Maybe I should avoid case analysis entirely and instead prove that ω is a primitive 6th root of unity directly, then use a lemma like `pow_ne_one_of_pos_of_lt` to get that ω^n ≠ 1 for n strictly between 0 and 6.

I realize I can just define ω directly as a complex exponential and get `IsPrimitiveRoot ω 6` straight from `Complex.isPrimitiveRoot_exp`, which immediately gives me the power identities I need, and there's even a built-in geometric sum lemma for primitive roots that could handle the orthogonality argument.

Proving the lemma involving cosine/sine conversion seems risky if it breaks compilation, so I'm weighing whether to skip it. I'm leaning toward defining ω directly with coordinates (1/2, √3/2), proving its key algebraic relations (ω²=ω−1, ω³=−1, ω⁶=1), and showing ω^n≠1 for n=1..5 via case analysis, then handling orthogonality through the shift trick and splitting on `a : Fin 6` with `a ≠ 0`.

I'm considering destructuring the Fin into its underlying natural number and bound, then using interval_cases on that variable directly, since applying interval_cases to an expression like `a.val` feels uncertain compared to working with a plain Nat variable.

I'm working out that the zero element of Fin 6 reduces by computation, so proving the value equality should just go through via `rfl` or `Fin.ext` on the underlying nat values.

Trying the Fin.ext approach instead, checking that the defeq unfolding of the zero coercion reduces properly to make the equality proof typecheck.

Then after splitting into cases with `interval_cases n`, I'll have separate goals for each power of ω from 1 through 5, each needing to show it's not equal to 1.

For the first case, I'm working out that ω itself isn't 1 by comparing imaginary parts—taking the imaginary part of both sides, simplifying with the known value of ω's imaginary part, and reducing to a contradiction about √3/2 equaling zero.

I realize I can just extract the imaginary part directly: rewrite ω^1 using pow_one, then compare imaginary parts of both sides via omega_im and Complex.one_im to get √3/2 = 0, which linarith kills immediately. Same strategy works for ω² ≠ 1, using omega_sq and Complex.sub_im to isolate the imaginary part equation.

For ω³ = -1, I just rewrite with omega_cube and let norm_num finish it. For ω⁴ = -ω, I can verify algebraically with linear_combination using ω times the cube relation, then take imaginary parts via Complex.neg_im to get -√3/2. I'm now working out the linear_combination coefficients needed to prove ω⁵ = 1 - ω by expressing it in terms of ω²·ω³ and the cube identity.

Actually the shift trick is cleaner: I can show χ(a)·S(a) equals S(a) by reindexing the sum via k ↦ k+1, which forces S(a) = 0 whenever χ(a) ≠ 1, avoiding the case-by-case expansion entirely.

Writing the proof...

Still verifying the ring identity and checking that simp_rw correctly rewrites under the summation binder before reindexing the sum via the shift.

Trying "simpa using" with the addRight equiv, but worried simp might normalize the hypothesis and goal differently since they share structure. Considering an alternative approach using Fintype.sum_equiv instead to be safer.

Checking that the underlying unification matches the goal pattern correctly, and that the `simp` call resolves the equivalence shift to close by reflexivity after elaboration — this should work since `exact` unifies against the goal before the tactic block runs.

Next I'm proving `χ a ≠ 1` for nonzero `a`: destructuring `a` into its natural number representative, showing the hypothesis gives a nonzero remainder, rewriting the goal as `ω^n ≠ 1`, then case-splitting on the possible values of `n` via `interval_cases` and discharging each case.

I'm tracing through how `Fin.val` reduces for the `OfNat` instance across Lean core versions, checking that unifying `n = 0` against the Fin equality goal reduces by projection and matches definitionally.

I'll settle on using `simpa [Fin.ext_iff] using ha` to convert the hypothesis into the plain numeric inequality I need, then double check whether the goal after destructuring `a` still matches up properly.

Then I'm checking that `interval_cases n` splits into the six concrete cases for n = 0 through 5, each with the specific disequality hypothesis substituted in, handling the n = 0 case directly since it contradicts itself via `absurd rfl`.

For n = 1 I just unfold `pow_one` and reuse `omega_ne_one`. For n = 2, I rewrite using the squared formula for omega, then take the imaginary part of both sides of a hypothetical equality to derive a contradiction using the positivity of √3, working through `Complex.sub_im` and `Complex.one_im` to simplify.

I realize I should apply `Complex.one_im` just once since `rw` rewrites all matching instances at once, avoiding a "no occurrence" error. A cleaner approach is to use `simp only` with the relevant imaginary-part lemmas in one pass, then close with `linarith` using the positivity of √3. I'm also sketching a helper lemma that shows a complex number isn't equal to 1 whenever its imaginary part is nonzero.

For the specific root ω, I can apply this helper by rewriting with `omega_im` and letting `positivity` handle showing √3/2 is nonzero, since positivity can close strict inequality, nonnegativity, and nonzero goals alike.

For ω - 1 though, since its imaginary part simplifies to the same √3/2 minus zero, positivity isn't equipped for subtraction, so I need to simplify away the subtraction first with simp lemmas before the nonzero goal reduces cleanly.

I'm sorting out the remaining nonequalities similarly: -1 ≠ 1 is trivial via norm_num, and -ω's imaginary part is -(√3/2), so I'm negating the positivity proof to get the nonzero result.

Now I'm moving to the main theorem proofs, starting by defining the Fourier matrix on Fin 6 using the character χ applied to products of indices, building it with Matrix.of.

Since `Matrix.of` is just the identity equivalence under the hood, unfolding it should reduce definitionally to plain function application, so `column fourierSix k i` should just reduce to `χ (i*k)` by `rfl`, since the coercion unfolds cleanly through `Equiv.refl`.

I'll go with `rfl` since it relies on the same underlying proof as `of_apply`. I also realize I need to open the `MUB.SzollosiCommonRays` namespace since `column` and `overlap` live there, while keeping my own definitions in a separate noncomputable section since ω depends on `Real.sqrt`.

Working through the overlap computation, I confirm `overlap (column fourierSix k) z` reduces by `rfl` all the way down since both `overlap` and `column` unfold definitionally. Now I'm setting up an autocorrelation function to use in the key computation.

For unimodular sequences, I'm proving that the squared norm of the overlap expands into a sum involving the character and the autocorrelation, working through the star-sum manipulations carefully since `star_mul` reverses order in general star rings but commutes for ℂ.

I can use the additive character property χ(l+j)k = χ(lk)χ(jk) together with the unimodularity relation χ(lk)star(χ(lk))=1 to simplify each term down to star(χ(jk)) times star(z l) times z(l+j), then plan to swap the order of summation.

I realize this identity doesn't actually require unimodularity at all—the normSq-to-autocorrelation relation holds for any vector z, since unimodularity only matters later for establishing c_0 = 6. I need to carefully expand the double sum using `star_sum` and match terms to get the goal into the autocorrelation form.

Confirming the typeclass instances line up for ℂ, then considering whether to instead prove a pointwise identity for each index and finish with sum_comm, working through the per-term rewriting of the inner sum.

I'm worried the rewrite could match either sum ambiguously since both sides share the same pattern shape, so it's safer to switch to `Fintype.sum_equiv` instead, which lets me specify the bijection and matching function explicitly rather than relying on `rw`'s traversal order.

I'm working out the correct direction for the equivalence: I need to apply it symmetrically, matching the shifted index against the original sum, so I flip to using `.symm` on the sum_equiv application with the addLeft equivalence to get the two sums to line up correctly.

I'm tracing through how `symm` interacts with the metavariable unification in `Fintype.sum_equiv`, confirming the expected type resolves correctly by matching `g` and `f` against the goal's two sums before checking the pointwise obligation holds.

To be safer about expected type propagation, I decide to put the `Eq.symm` as a prefix wrapping the whole refine term rather than using dot notation, so the expected type flows through properly. Then I turn to checking the resulting obligation goal involving the character and star terms after substitution.

Simplifying with the addLeft coercion lemma, beta-reducing to collapse `(Equiv.addLeft l) j` into `l + j`, and then working through `add_mul` and `χ_add` to break apart the product and sum terms into separate star-multiplied factors, though I need to double check which occurrence `add_mul` actually targets first in the goal.

I'm trying to close the gap using `h1 : star(χ(l*k)) * χ(l*k) = 1`, factoring the difference as ABC(1 - D·D̄) and matching coefficients so `linear_combination` can verify it with the right scalar multiple of `h1`.

I need to rewrite that sum using hinner under the outer binder, perhaps via simp_rw or Finset.sum_congr, then swap the summation order with Finset.sum_comm so I can match it against the autocorr definition by unfolding and pushing the sum through the multiplication.

Still tracing the star_mul' rewrite...

Worried simp_rw might not produce the exact associativity I expect, I'm considering a more robust fallback: proving the pointwise equality directly via calc or using Finset.sum_congr with an explicit inner equality, so the proof doesn't depend on simp's exact normal form.

Working through index reordering...

After swapping sums, the two sides match exactly after unfolding autocorr and distributing the product over the sum, so I'm now drafting the full Lean proof combining these reindexing and sum-commutation steps.

Still proving the inner sum identity...

Tracing through the remaining rewrites: applying `χ_add` gives the split product, then two applications of `star_mul'` handle each starred product (order doesn't matter since both are listed), and `star_star` collapses the double star back to `χ (l*k)`, leaving the goal in its simplified form.

Checking the linear_combination coefficient against `star_χ_mul`: the difference reduces to the same factored expression up to the identity `D̄D = 1`, confirming the combination is correct before moving on to rewriting with `star_mul_self`.

Now tracing through the rewrite chain: `star_mul_self` converts the normSq cast into a `star z * z` form, `hS` substitutes in both overlap occurrences, then `star_sum` and `Finset.sum_mul_sum` expand things into a double sum of star products. I'm verifying that `Finset.sum_mul_sum` actually matches this shape in Mathlib.

I'm trying to recall whether `rw` beta-reduces the resulting goal automatically, since the lemma produces lambda applications like `f₁ x₁` that should simplify to plain applications — I believe it does via its internal instantiation step.

Good, that confirms the beta-reduction works. Now checking whether `simp_rw [hinner]` can match the inner sum under the outer binder — with `l` bound to the outer index, the pattern should align correctly since `simp_rw` rewrites under binders using `simp only`, though I should watch for any extra beta/eta normalization simp applies along the way.

That should close by rfl after matching sides, so I just need to double check that the sum manipulations line up correctly and that unfolding autocorr gives the matching double-sum form on both sides.

Now proving autocorr_zero: unfolding autocorr and showing each term star(z l) * z(l+0) equals 1 using the unit-magnitude hypothesis, then simplifying the resulting constant sum over Fin 6 to get 6.

I'm confirming the simp normalization closes the sum to 6=6, and checking that rewriting with add_zero, star_mul_self, and hz collapses the identity to 1=1. Now I'm moving on to tackle the main theorem itself.

I'm stating the biconditional characterization of CommonRay for fourierSix in terms of z 0 = 1, all normSq conditions equal to 1, and autocorrelation vanishing for nonzero indices, then starting the forward direction by extracting the overlap hypothesis and reformulating it as a sum identity involving characters and autocorr.

I'll just use `simp` for that cast equality instead of `norm_num`. Now I'm trying to isolate the nonzero autocorrelation term by splitting the sum using the fact that autocorr vanishes except at zero, so the orthogonality relation reduces to the single j=0 term equaling 6.

For a fixed nonzero j₀, I want to multiply both sides of the key identity by χ(j₀·k) and sum over k: the right side collapses using character sum orthogonality (giving zero since j₀≠0), while the left side, after swapping sums, picks out exactly the j=j₀ term, showing 6 times autocorr at j₀ must vanish.

I'm working through the algebraic identity showing that χ(j₀·k)·star(χ(j·k)) equals χ((j₀-j)·k), using the fact that χ is multiplicative on sums in its argument and star(χ(b)) relates to χ(-b), multiplying through and canceling using star_χ_mul.

I'm trying to find a `linear_combination` shortcut instead, working out coefficients so the two hypotheses algebraically combine to give the goal directly.

Now I'm moving on to proving the orthogonality lemma showing the sum over k of χ(a*k) equals 6 if a=0 and 0 otherwise.

For the a=0 case, I split into cases, substitute, and simplify using χ_zero so zero_mul reduces each term to 1, giving a constant sum equal to 6, while the nonzero case follows from a separate lemma char_sum_eq_zero.

Now I'm verifying that χ 0 = 1 holds by simplification: χ 0 unfolds to ω raised to the value of 0 in Fin 6, which simp handles via Fin.val_zero and pow_zero, so I lean on simp rather than rfl to be safe. Moving on, I start sketching the converse direction of the proof.

For the converse, I take an arbitrary nonzero j₀ and show the double sum over k and j of χ(j₀k) times the conjugate character weighted autocorrelation vanishes, using the orthogonality relation char_sum_eq_zero. Then I begin establishing that swapping the order of summation turns this into 6 times the autocorrelation at j₀, using Finset.sum_comm.

Still verifying the sum identity...

Checking whether the sum commutes correctly and doesn't accidentally rewrite the autocorrelation term since it's not literally a sum. Then I apply the sum swap and verify the next goal, which involves substituting the character sum identity for the index difference to match the indicator function times autocorrelation.

After applying sum_mul and sum_congr, I check whether χ_mul_star applies directly to the goal term, but the pattern doesn't match since the product (j₀-j)*k isn't in the right subtraction form — so I need to distribute with sub_mul first before applying χ_mul_star.

Applying simp_rw with the indicator identity collapses the sum since simp will also rewrite the subtraction-equals-zero condition into an equality form, leaving just the single nonzero term scaled by 6. Then I want to isolate that term using `Finset.sum_eq_single` at j₀, checking its hypothesis requirements.

The main goal after rewriting reduces trivially via `sub_self` and `if_pos`, while the side goal requires showing all other terms vanish—using that j₀ - j is nonzero whenever j ≠ j₀ to force the indicator to zero.

Using `mul_eq_zero` splits the product into two cases, and `norm_num` closes the false case where 6 equals 0. For the reverse direction, I'm proving the forward implication by isolating the j=0 term in the sum and substituting the autocorrelation values for nonzero indices to show the sum reduces to 6.

That simplifies to h equaling 6, and casting from ℂ to ℝ closes the goal via the real/complex numeral equality. I'm also checking whether the side conditions from `Finset.sum_eq_single` appear as separate goals after the rewrite, with the first requiring that terms vanish for indices other than zero.

Then I'm tracing through how the implicit type gets resolved when elaborating `Finset.sum_eq_single 0` — the metavariable for the numeral's type should unify with `Fin 6` once Lean matches it against the sum appearing in `h`.

I realize the final goal, that no two common rays are unbiased, isn't something I can actually prove, so I'll need to be upfront that this remains an open/partial result rather than a complete theorem.

I'm trying to pin down where `HasRawQuartet` actually lives in the namespace hierarchy — whether it's under `MonomialTransport` or nested further under `MUB` — since the file opens `MonomialTransport` at the top level and I need to reference it correctly to compose the characterization with the no-unbiased-pair condition.

Since this should still resolve correctly regardless of which exact root the namespace lives under, I'll place my namespace under `MUB.` and use `open MonomialTransport`, matching the pattern used in the existing file that compiles successfully.

I'm also reconsidering whether I need `HasRawQuartet` stated explicitly in the conditional theorem — yes, I do, since the theorem's conclusion references it directly.

I'm tempted to add a concrete Gauss-vector common-ray example, but that would require heavy exact ζ₁₂ computation with autocorrelation sums expanded term by term over Fin 6, which is risky without being able to compile. Better to stick with what I'm confident will work rather than risk a failed build.

I need ζ to be a primitive 12th root of unity with ζ²=ω, choosing ζ = e^{iπ/6} explicitly as a complex number with real and imaginary parts √3/2 and 1/2, verified to square correctly to ω. Then I'm working through the orthogonality computation for star(g l) times g(l+j), expanding (l+j)² mod the index arithmetic to isolate the cross term.

This simplifies to ζ^{2lj}ζ^{j²}, and since ζ^{2lj} = ω^{lj} = χ(l·j) using the mod-n relation on Fin values, I get star(g l)·g(l+j) = ζ^{j²}·χ(l·j) — now I need to formalize this with Fin.val_add and Fin.val_mul lemmas.

Working through the mod-6 squaring lemma: writing m as r + 6q where r = m%6, q = m/6, the key identity m² = r² + 12(rq + 3q²) should follow from substitution and nlinarith, though substituting m directly is tricky since r and q are defined in terms of it.

I'm worried nlinarith can't derive the needed identity just from squaring the mod-div equation, since it doesn't multiply by arbitrary atoms—I may need to manually supply multiplied hint terms like multiplying the equation by m, r, and q separately to get the right cross terms.

I'm now considering whether linear_combination works for ℕ at all, since it's a semiring without subtraction, and thinking instead about explicitly decomposing m using Nat.mod_add_div to extract a quotient term.

I want to prove a helper lemma showing that ζ raised to the square of (r + 6q) equals ζ raised to the square of r, by expanding (r+6q)² into r² plus a multiple of 12, which should let me cancel the extra term using periodicity.

Now I'm applying this to the Fin 6 addition case, using Nat.mod_add_div to rewrite (l.val + j.val) in terms of its mod-6 remainder plus a multiple of 6, so I can substitute into the squared exponent and reduce it back to the remainder's square.

Finishing the proof confirms the rewrite closes by reflexivity since both sides reduce to the same expression. Now I'm working out the per-term lemma relating star(g l) times g(l+j) to a power of ζ times χ(l·j), expanding g in terms of squared indices modulo 6.

I'm expanding (a+b)² using pow_add to split off the cross term 2ab from a² and b², then canceling star(ζ^(a²)) against ζ^(a²) so only ζ^(2ab+b²) survives. I'm rewriting ζ^(2ab) as (ζ²)^(ab) = ω^(ab), matching it against χ(l*j) which also equals ω^(ab) once I unfold χ via Fin.val_mul.

Still writing proof steps...

I'm confirming `ring` can handle symbolic ℕ exponents consistently across both sides, which should make this normalization work, though I want to double check how `ring` treats `star` applied to a power term as an atom.

Then tracing through the actual rewrite chain: using `Fin.val_mul` to unpack the mod-6 arithmetic in `χ (l*j)`, applying `omega_pow_mod` to simplify away the modulus, and landing on the equation `ω ^ (l.val * j.val) = ζ ^ (2 * (l.val * j.val))`, which I can close via the `zeta_sq` relation.

I realize applying `pow_mul` generically is risky here since the rewrite could match the left side instead of the intended right side, collapsing the exponents wrong. I need to pin down the rewrite to target `ζ` specifically by supplying explicit arguments so it only restructures the right-hand side.

Working through `h2`, rewriting with `← omega_pow_mod` correctly matches the `(l.val * j.val) % 6` pattern on the right. For `h1`, unfolding `g` and applying `Fin.val_add` rewrites both occurrences of `(l+j).val` into the mod-6 sum form, which should align both sides for closing the goal.

Checking that the rhs has no addition pattern to accidentally match, confirming the second `pow_add` rewrite lands correctly, and verifying `l.val` and `↑l` refer to the same underlying coercion so `hsq` applies cleanly.

Now I'm working out the autocorrelation of g: factoring out the constant term and using `mul_comm` to reduce the sum to the character sum, which vanishes for nonzero j. Writing the Lean proof for autocorr_g...

Once that's done, checking g 0 = 1 and that g is unimodular via pow and normSq lemmas, then combining everything with `commonRay_fourierSix_iff` to confirm g is a concrete common ray.

Computing the explicit values gives (1, ζ, ω², -i, ω², ζ), which is nice. I'm also wondering whether I could extend this to a family of twelve Gauss-type vectors parameterized by a ∈ {1,5} and b ∈ Fin 6, and check pairwise overlaps between vectors with the same a but different b.

The same-a overlaps reduce to a character sum that's 6 when b=b' and 0 otherwise, giving norm-squared values of 36 or 0, neither equal to 6, so that case is handled cleanly. The cross-a overlaps between a=1 and a=5 vectors are messier, reducing to sums of the form ω^{2k²+ck}, which require splitting into cases depending on whether c is even or odd and computing each six-term sum explicitly.

I'm weighing whether to include this sub-family exclusion, since it's a nice-to-have but adds compile risk to the file. I could mitigate that by splitting it into a separate imported file instead.

I'll split into two files: one covering the core characterization, no-quartet result, and explicit Gauss ray; the other covering the six modulations, their common rays, and showing pairwise overlaps are never unbiased. I'll likely skip the conjugate-family cross computation to limit risk, though conjugation trivially preserves common rays if I want to include it.

For even c, I compute |T|² using a shift trick, expanding the double sum and isolating when the cross term vanishes mod 6, which collapses nicely to 6 times a factor depending on c mod something, giving 12 as long as c is even.

Expanding this same norm-squared sum into an autocorrelation gives ∑_j ω^{2j²}χ(cj)∑_l χ(4jl), reducing the problem to evaluating that inner character sum over l, which will vanish unless 4j is trivial mod the relevant modulus.

Given the scale of this computation, I'm weighing whether to commit to the full 6-family modulation case for file 2, since it could neatly match the exclusion property I'm after, but it's a sizable chunk of work with real risk of getting bogged down.

I'm instead sketching a general reusable lemma relating the squared norm of a sum to a sum of autocorrelations, which should simplify via star/sum manipulations and reindexing, and could be applied directly to derive the overlap identity I need rather than proving it from scratch each time.

Working through the pairwise overlaps for the 12-family: between two shifted copies of g, the overlap reduces to a character sum over the shift difference, giving either 6 or 0 as required; and between a g-copy and its conjugate family, I'm tracking how the star operation interacts with the modulation to set up the next overlap computation.

Continuing the algebra, I'm simplifying g_l·star(g_{l+j}) using the known Gauss sum relation, pulling out the quadratic phase factor and reducing the sum over l to a character sum that collapses unless 2j is trivial, giving an expression for the autocorrelation purely in terms of χ(cj) and the phase ζ^{2j²}.

Wait, there's a discrepancy with my earlier computation giving c=0 as 12. Rechecking: comparing v_k to the earlier a=5 family, I find ζ^{10k²} = ζ^{4k²}(-1)^k, meaning this family is a modulation by ω^{3k} relative to the earlier one — so it's consistent once I shift c by 3.

So pairwise cross overlaps always land in {0, 12}, never 6, which is what I need. Formalizing this in Lean means handling the character sum manipulations for the cross case — identifying when 2j=0 (i.e., j ∈ {0,3}) and evaluating the sum over j in Fin 6 weighted by that indicator, which is moderately involved but tractable.

I'm weighing time and risk here, and leaning toward structuring this as multiple files: one for the core result, another for the modulation piece.

I want to set up the gauss and conjugate-gauss families as functions parameterized by a shift, so I can compute overlaps between members of each family and check pairwise exclusion, then try to organize the cross-family overlap computation to avoid awkward Fin-literal arithmetic.

Now I need to verify the normSq computation itself: splitting into the case where b'-b is zero giving normSq 6 = 36, versus the nonzero case giving normSq 0 = 0, using the real/imaginary part lemmas for natural number literals in ℂ.

I can then rewrite 6 as a real cast and simplify normSq via norm_num, or alternatively just unfold normSq directly with simp and finish with norm_num to get 36.

I'm trying to establish that the normSq of this overlap expression isn't 6 by splitting into cases and converting the numeral 6 to its real-number cast form so I can apply the normSq-of-real lemma cleanly.

Right, I recall now that Mathlib does define simp lemmas for `re_ofNat` and `im_ofNat` covering exactly this numeral-casting case, so I can rely on those directly.

Maybe I should sidestep this entirely and work with the cross overlap structure directly: expressing the overlap as a sum involving characters evaluated at differences of indices, then computing its norm squared via autocorrelation of that sequence, term by term.

Squaring that term reduces to a character sum over 2j, which vanishes unless 2j=0, giving 6 in that case. So the autocorrelation collapses to a simple expression nonzero only when 2j=0, and now I need to sum this over all j in Fin 6, checking the condition 2j=0 case by case.

For j=0 the contribution is 6, and for j=3 the exponent simplifies since ζ^18 = -1, giving a term proportional to -χ(3c). All other j give zero, so the total is 6 - 6χ(3c), and I'm working out that χ(3c) equals χ(c)³, which reduces to ±1 depending on c.val mod 2.

Now I need to handle the sum over Fin 6 explicitly, where terms involve indicator conditions like whether 2j equals zero modulo 6. I'm thinking through how to discharge these via decide tactics rather than relying on simp to automatically resolve them.

I'm confident `rfl` or `decide` can resolve `(3 : Fin 6).val = 3` since it reduces to a straightforward modular arithmetic computation.

This cross computation is a sizable chunk of the proof. I'm also wondering if restructuring the conjugate family or the file-2 setup could simplify the indexing, though the structure seems inherent to the problem.

I'm leaning toward splitting into three files to isolate compile risk: file 1 for core setup, file 2 for the modulation family plus conjugate membership and within-family exclusion, and file 3 for cross exclusion plus the final theorem combining all twelve families. That's more writing, but each file only risks itself if something fails to compile, so it seems like the safer path. Let me reconsider the exact statement of file 1's main theorem before committing to this split.

I'll prove the general lemma first since it isolates the reindexing argument, then get the specialization as a pointwise computation inside autocorr—fewer total reindexing proofs this way. Writing the normSq_sum_eq lemma now, reindexing the double sum into autocorr terms...

I'm checking that `Equiv.addLeft` unfolds definitionally so the equality holds by `rfl`, but using `simp` is the safer bet in case the coercion doesn't reduce automatically.

After rewriting with `hinner`, swapping the summation order with `Finset.sum_comm` should match the goal with the definition of `autocorr`, closing by `rfl` since both sides unfold to the same double sum.

Now I'm sketching out a new lemma, `normSq_overlap_eq`, relating the squared norm of the overlap between a Fourier basis column and a vector to a sum involving `χ` evaluated at `j * k`.

I'm double-checking whether the rewrite step will actually beta-reduce that lambda application correctly before proceeding, since Lean might leave it unreduced depending on elaboration.

Instead of worrying about that, I realize it's simpler to just let unification solve for the metavariable directly against the sum pattern, since it's a straightforward higher-order pattern match.

Working through the algebra, I verify that unfold beta-reduces correctly, then distribute the sum via mul_sum and reduce the goal to showing each term matches after pulling out the star of the character factor, leaving a per-term equality to establish via conjugate multiplication properties.

Working out the coefficient: since lhs - rhs factors as ABC(DD̄ - 1) and the hypothesis gives D̄D - 1, the coefficient should just be ABC, confirming the linear_combination term is correct. I'm double-checking that the rewrite patterns only match the intended subterms—verifying `add_mul` only applies to the `(l+j)*k` factor and `χ_add` only matches the `χ(l*k + j*k)` pattern, so no unintended rewrites happen elsewhere.

I'm also considering whether `unfold autocorr` properly beta-reduces the resulting lambda application, since core `unfold` relies on simp's equation lemma mechanism which should handle beta reduction automatically, but I want to be extra careful here.

Switching strategy, I decide `simp only [autocorr, Finset.mul_sum]` is safer than `unfold` since simp reliably beta-reduces and also pulls the sum out, distributing the star term across the inner sum.

Checking that the same approach works for autocorr_g: using `simp only [autocorr, g_term]` under the binder should match the body pattern exactly regardless of bound variable names. Now I'm moving to draft the final conditional theorem statement for the first file.

Finishing the conversion using commonRay_fourierSix_iff, I need to verify this lemma's unfolding matches what I expect for CommonRay applied to fourierSix, checking that the components line up correctly.

Actually I think anonymous constructor elaboration uses plain `whnf`, not `whnfR` — that's consistent with how `Set.Nonempty` and similar defs unfold fine with `⟨_, _⟩` in practice, so this should work for `CommonRay` too.

To be safe, I'll just `unfold CommonRay` at the start of the proof to expose the conjunction directly, which is accessible since it's a def I can reference via the open namespace. Then I need to work out what the column overlap condition becomes once unfolded.

Checking the definitional unfolding, `fourierSix` constructed via `Matrix.of` should reduce by `rfl` to the character sum expression I expect, since `Matrix.of` is just the identity equivalence underneath.

I'm weighing whether to define the matrix as a plain lambda versus using `Matrix.of`—both should typecheck if `Mat` is just an abbreviation for `Matrix`, but I'll stick with `Matrix.of` since it's the more idiomatic and robust choice.

Checking if using symbols like `χ` and `ω` as identifiers could clash with existing Mathlib notation, but since `ω` for `Ordinal.omega` is scoped and not opened by default, there shouldn't be a conflict.

Settling on `omega6` to sidestep any clash with the `omega` tactic name, then starting the draft of the first file with its imports, namespace setup, and opening section header.

Now I'm defining `omega6` as the primitive sixth root of unity with its real and imaginary parts given explicitly, then adding basic lemmas about `√3` (its square and positivity) along with accessor lemmas for `omega6`'s components, and beginning a lemma establishing its square.

Proving that lemma, I'm checking real and imaginary parts separately using `Complex.ext`, using `nlinarith` with the square-root identity for the real part and `ring` for the imaginary part—then I pause to double-check that the definitional equality for `omega6.re` actually holds as expected given how the constructor elaborates.

For the imaginary part, the check reduces to a ring identity that holds trivially since the imaginary piece cancels. I verify the simp lemmas correctly rewrite omega6.re and omega6.im before confirming the cube identity holds, then move to drafting the proof of omega6_cube using these facts.

Now I'm proving omega6_six by combining omega6_cube with the factorization of omega6^3 - 1, then establishing the periodicity lemma omega6_pow_mod via mod/div decomposition of exponents using omega6_six. Next I'm computing normSq_omega6 by unfolding Complex.normSq into real and imaginary components and verifying it equals 1 using nlinarith with the sqrt3 multiplication fact.

I'm rewriting the exponent using `Nat.mod_add_div`, confirming that substituting `n` with `n % 6 + 6 * (n/6)` inside `omega6 ^ n` abstracts correctly since the identity matches the expected order of terms.

That confirms `pow_add` applies correctly. Now I'm defining a character function `chi` on `Fin 6` using powers of omega6, proving it sends 0 to 1 via simp lemmas, and starting a proof that it's a homomorphism with respect to addition.

Checking that `normSq_chi` works using `map_pow` since `Complex.normSq` is a monoid-with-zero homomorphism, so normSq of a power equals the power of normSq, which is 1 since omega6 has unit norm.

Now I'm verifying `star_mul_self`, rewriting `star z` to `conj z` via `Complex.star_def`, then using `Complex.mul_conj` after commuting the multiplication to match the expected form `↑(normSq z)`.

I'm also considering an alternative approach using `Complex.normSq_eq_conj_mul_self` directly instead of going through `star_def`.

Since `starRingEnd ℂ z` should unfold definitionally to `star z` through the coercion chain, `rfl` ought to close the goal either way, so I'll go with the `Complex.star_def` version.

Tracing through the definitional unfolding, `star z` should reduce down through the ring hom coercion and the `starRingEnd` definition to just `star z` itself, so `rfl` should close the defeq check between the two sides.

To be safe I'm adding a fallback using `first | rfl | simp [Complex.star_def]` so the proof tries `rfl` first and falls back to simp with the star definition if the defeq check fails for any reason.

For `star_chi_mul`, I rewrite using `star_mul_self` and `normSq_chi` then convert the real one to a complex one via `Complex.ofReal_one` to get the identity.

Now for `chi_mul_star` I'm establishing a helper fact that `chi (a-b) * chi b = chi a` by combining additivity of `chi` with cancellation of subtraction and addition, then combining it with `star_chi_mul b` using `linear_combination` to derive the final equality.

I verify the linear combination coefficients algebraically to confirm the goal matches exactly, then move on to proving `chi_ne_one`, starting with a lemma that any complex number with nonzero imaginary part can't equal one.

Confirming that verifies. Now I'm proving chi_ne_one by case-splitting on the index n from 0 to 5, using omega6's imaginary part being nonzero to rule out n=1, and similarly checking the other cases via the square and cube values to show chi a ≠ 1 whenever a ≠ 0.

I'm trying a fallback tactic combining `Fin.ext`, substitution, and `simp` to handle the case conversion safely, then checking that after `interval_cases n` the n=0 case gives a contradictory hypothesis `0 ≠ 0`.

I'm also confirming that `interval_cases` has the bound it needs from context, that unfolding `chi ⟨n, hn⟩` reduces definitionally to `omega6 ^ n`, and that the inequality hypothesis on `a` correctly rewrites to the tuple form after obtaining its components.

For the cube case, rewriting via `omega6_cube` reduces the goal to `(-1 : ℂ) ≠ 1`, which `norm_num` handles directly.

Now I'm starting the orthogonality lemma, proving that summing `chi (a * k)` over all `k` vanishes when `a ≠ 0`, by multiplying both sides by `chi a` and reindexing the sum...

I'm checking that `ring` works for the algebraic identity over `Fin 6`, since it needs a `CommRing` instance there, and planning a `simp` fallback using `mul_add` and `mul_one` in case `ring` fails.

I'm checking that the equiv-based sum shift matches term by term, confirming the shift function satisfies the required equality on both sides. Then I verify the remaining algebraic identity by substituting h1 and using sub_self to close it.

I'm now splitting into cases: when a=0, simplify directly using chi_zero; otherwise, invoke the lemma showing the sum vanishes.

That confirms the simp chain works out, so I'll use `simp [chi_zero]` with a `norm_num` fallback as backup. For the subst step, since `a` is a local variable, `subst ha` should work fine to replace it with 0. Now I'm setting up the Fourier matrix definition using the character function, and starting to define the autocorrelation function over the vector space.

For the key lemma relating the normSq of a sum to the sum of autocorrelations, I'm expanding the product of sums using star multiplication, then reindexing each inner sum via a shift by `l` using `Equiv.addLeft`, and finally swapping the order of summation to match the target form, closing with `rfl`.

That checks out fine. Now I'm verifying the reindexing via `Fintype.sum_equiv` with the shift equivalence, matching up the two sums term by term using the required equality obligation for each index.

I'm applying sum_comm to swap the order of summation, then checking whether the resulting double sum matches the autocorrelation form on the right-hand side so rfl can close it.

To be extra safe against a "no goals" error if `rw`'s internal rfl check happens to close things, I'm considering using `all_goals rfl` instead of a bare `rfl`, since it's a no-op when no goals remain but still closes any leftover goal.

Moving to the overlap lemma for the six-point Fourier basis, I'm setting up that evaluating a column gives the character function by definition, then computing the overlap sum as a sum of conjugated character values.

For the normSq equality, I'm rewriting through the overlap and normSq_sum lemmas, then matching term-by-term using the autocorrelation definition and character addition identities via linear_combination.

I'm double-checking that the defeq used for column_fourierSix holds under the elaborator's default transparency, and tracing through how simp only with autocorr and mul_sum unfolds the sum on the left side to make sure no unintended distribution occurs.

After confirming that Finset.sum_congr rfl isolates the pointwise term correctly, I verify the resulting equality matches the expected star/chi product form, then proceed with add_mul and chi_add to split the exponent and finish the rewrite.

Good, that confirms the equality holds. I'm double-checking that `star_mul'` is the right Mathlib lemma name for commutative star semigroups, and confirming the rewrite order doesn't matter since both instantiations get handled regardless of which match is hit first. Now I'm moving on to work through the `autocorr_zero` lemma statement.

I should just use plain `simp` as a fallback for closing the sum. Now I'm moving on to stating the main theorem, which characterizes when a vector shares a common ray with the Fourier sixth-root vector in terms of its first entry, normalization, and vanishing autocorrelations for nonzero shifts.

For the forward direction, I'm unfolding the orthogonality relation for each shift k into a sum equal to 6, then using that to derive that the character sum over a nonzero j₀ must vanish by factoring out the sum and applying the known zero-sum identity for characters.

Finishing the orthogonality argument...

For the reverse direction, I provide the remaining component by using the normSq overlap identity and isolating the zero-index term, applying the autocorrelation-at-zero fact with character normalization to conclude the cast equality, then handling the off-diagonal terms via the vanishing hypothesis h2.

Confirming the pattern matches, then working through hsum: rewriting the sum under the binder, pulling out the constant factor via sum_mul, applying the chi_sum_eq_zero lemma to get zero, and collapsing with zero_mul.

Moving to hsum2, I distribute using mul_sum to push the chi factor inside the inner sum, matching it against the right side's scalar multiple.

Swapping the summation order with Finset.sum_comm gives the double sum form I need. Now I'm substituting the character orthogonality relation chi_sum to rewrite the inner sum as an indicator function depending on whether j₀ - j equals zero.

Checking the sub_mul rewrite matches the (j₀-j)*k pattern correctly, then simplifying with the indicator function down to the single term where j equals j₀, using sum_eq_single to isolate it and simp to close the main case via sub_self.

For the side condition that other terms vanish, I'm worried that simp might rewrite `j₀ - j = 0` via sub_eq_zero into `j₀ = j` before it gets a chance to apply the inequality hypothesis, which could break the intended simplification path.

To avoid that ambiguity, I'll switch to the deterministic `rw [if_neg this, zero_mul]` instead of relying on simp. That gets both sides into shape so `hsum` reduces to `6 * autocorr z j₀ = 0`, then `mul_eq_zero.mp` splits it, and `norm_num` closes the false numeric case, finishing the goal.

For the reverse direction, I'm isolating the single nonzero term at `j = 0` in the sum using `Finset.sum_eq_single`, then simplifying `autocorr z 0` to `6`, collapsing `0 * k` to `0` via `zero_mul`, and reducing `chi_zero` with `star_one` and `one_mul` so the hypothesis matches the target form.

I'm a bit unsure about the order the side goals (`h₀`, `h₁`) appear relative to the main goal after that rewrite — if `sum_eq_single` orders them differently than expected, the bullet structure will fail to compile, so I'm considering a safer alternative approach.

To avoid that risk, I'm proving `h'` as an explicit term using `Finset.sum_eq_single`, isolating the `j = 0` case and showing all other terms vanish via `h2`, then rewriting with `autocorr_zero`, `chi_zero`, `star_one`, and `one_mul` to simplify the hypothesis deterministically. I'm planning to use the same term-style approach for the second sum.

I'm trying to work out whether the term elaboration order in `rw` actually postpones the `by tac` blocks until after unification resolves the metavariables, or whether it elaborates them too early and causes failures — this depends on how `rewriteTarget` calls `elabTerm` and whether synthesis is deferred.

Since that approach seems risky here because `f` isn't known yet, I decide instead to use an explicit `have` statement with `Finset.sum_eq_single` so the function is pinned down by the expected type rather than relying on later unification, applying this fix to both `hsum` and `hsum2`. Writing the sum equality proof...

Verifying the elaboration order confirms unification happens correctly, and tracing through `sub_self` and `if_pos` shows the goal collapses to a trivial equality closed by rfl.

Simplifying with `sub_self` and the `if` reduction should close that goal directly, so `rw [hs]; simp` works. I just need to double check the complex number type annotations in `hs` match the ℂ-typed conditional from `hj` so everything unifies properly.

Checking the decidable instances match between the two expressions confirms they're syntactically identical. I'm also verifying the absurd/mem_univ argument in the converse direction works out by type, then starting to check whether `CommonRay` can be unfolded directly with `unfold` depending on its definition.

Moving on, I note a conditional no-quartet theorem still needs `HasRawQuartet` added. Then I'm verifying the Gauss ray construction — checking that ζ = e^(iπ/6) squares to ω by confirming the real and imaginary parts match, and beginning to define `zeta12` and its real part lemma in Lean.

Still proving ζ² = ω and that ζ¹² = 1 via the order-6 relation on ω...

I'm checking the norm-squared computation to confirm ζ12 lies on the unit circle, verifying the real and imaginary parts reduce correctly through nlinarith, then thinking about how to handle the numeral rewrite for the exponent 12 in the power expression.

Rewriting the exponent as 2*6 and splitting into a nested square...

Now I'm defining the Gauss sum vector using zeta12 raised to k squared, then proving a periodicity lemma showing the exponent squared is invariant mod 12 by factoring the difference as a multiple of 12 and applying the twelfth-power identity.

I realize generic `pow_mul` rewriting is ambiguous since both sides have the form `base ^ (m * n)`, so I need to specify the exact arguments like `pow_mul zeta12 12` to force it to match the term with the 12 factor rather than accidentally rewriting the r*r term.

Now I'm working on the gauss_term lemma, expanding `(l.val + j.val)^2` algebraically to separate out the cross term, setting up the identity needed to relate the shifted Gauss sum to the original one scaled by a power of zeta12.

I establish that the star-product term equals one using the norm-square identity, then combine h1 and h2 via linear_combination to close the goal, unfolding gauss to verify both sides match after substitution.

That matches the rhs, confirming the equality holds by reflexivity. I'm now double-checking that Fin.val_add behaves as expected under the coercion, then moving to verify h2, unfolding chi and applying Fin.val_mul to handle the omega6 power expression.

For h3, I'm simplifying the norm-squared expression down to 1 using the star-mul-self identity, the power map, and the known norm-squared value of zeta12. Then in the main goal, I'm substituting h1 and h2 and unfolding the Gauss sum to reduce the equation to matching powers of zeta12 on both sides.

I'm applying `linear_combination` with the appropriate coefficient to reduce the goal using h3, factoring the difference as a product times (SZ - 1), and then checking whether `ring` can normalize the exponents since they're polynomial expressions in the atoms l and j.

I'm checking the rewrite step, confirming `chi (l * j)` appears in the goal so `rw [h1, h2]` applies, and sketching out the `gauss` lemmas I'll need — `gauss_zero` and `normSq_gauss`, the latter using `map_pow` and `normSq_zeta12` to show the norm squared is always 1.

Now I'm proving the autocorrelation of `gauss` vanishes for nonzero shifts: pulling the sum factor out, showing the inner sum over `chi (l * j)` is zero by commutativity and `chi_sum_eq_zero`, then closing with `mul_zero`. From there I establish `gauss_commonRay` by applying `commonRay_fourierSix_iff` with `gauss_zero` and `normSq_gauss`.

Finishing that simplification confirms the autocorrelation vanishes. I'm also considering whether to document the explicit Gauss sum values and whether an explicit formula lemma for fourierSix in terms of omega6 and the modular product would be useful to add.

Since the RawHadamard connection is undefined in this context, I'll skip proving that relationship and move on to defining the Gauss family in the second file, starting with a modular Gauss sum definition.

I'm sketching the key ray proofs: showing the sum starts at 1 via simp lemmas for gauss_zero and chi_zero, then establishing the norm-squared identity using map_mul and the known normSq lemmas for gauss and chi.

For autocorrelation, I'm working out that the autocorrelation of the modulated sequence factors into a character twist times the original autocorrelation, which vanishes—using the algebraic identity that splits the star-multiplied term into a chi(b*j) factor times the conjugate-shifted gauss product, provable via rewriting with mul_add, chi_add, and star_mul' followed by a linear combination argument.

Still writing proof script...

Now I'm checking how `chi_add` and `star_mul'` apply to the rewritten expression, confirming the rewrite matches `b*(l+j)` splitting into `b*l + b*j` correctly, then moving to verify the overlap identity between `gaussMod b` and `gaussMod b'`.

Using linear_combination with that star-gauss identity confirms the coefficient works out, so the overlap sum collapses to chi_sum(b'-b), which is 6 when b=b' and 0 otherwise. Now I'm setting up the theorem statement showing the normSq of the overlap can't equal 6 for general b, b'.

I split on whether b'-b equals zero: in that case normSq of 6 is 36, which isn't 6, and otherwise normSq of 0 is 0, also not 6 — both handled by norm_num. I'm proving the helper lemma that normSq(6:ℂ) = 36 by casting 6 to a real number first, then applying the real-to-complex normSq formula.

Still tracing through whether these numeral casts are definitionally equal...

Tracing through how both literal representations unfold at the `Nat.cast`/`OfNat` level, they do seem to reduce to the same normal form, so `rfl` should close the goal.

Let me try a hedge with `first`, trying alternative tactics in case `rfl` doesn't fire directly. One backup path is computing `normSq 6 = 36` via `Complex.normSq_apply` and `norm_num`, sidestepping the defeq question entirely by case-splitting on whether the overlap equals 6 or 0.

Similarly I'd handle the 12-squared case for cross terms. Then for the conjugate Gauss sum family, I want to show gaussConj at 0 equals 1 using simp with gaussConj, gauss_zero, and chi_zero, and figure out the right normSq lemma for star versus conj since Complex.normSq_conj exists but I'm unsure about an analogous star version.

Actually working through the star approach, the autocorrelation of the conjugated Gauss sum telescopes nicely: each term splits into a chi(bj) factor times the star of the original autocorrelation term, so the whole sum collapses to chi(bj) times star of the original autocorrelation, which vanishes since the original does.

Working through the algebra, I close the goal with a linear_combination step using the star_chi_mul identity. Then I move to proving the autocorrelation property for gaussConj, unfolding definitions and distributing the star and sum operations.

Expanding the overlap term for gaussConj with the shifted character, I work through the per-term identity using star_mul', star_star, and sub_mul to reduce it to a character difference, then finish with a linear combination using the unitarity relation gauss k * star (gauss k) = 1.

Now I'm working through the autocorrelation of the vector built from squared conjugated Gauss sums times a character, trying to show it collapses via the Gauss sum shift identity so the sum over l of the squared conjugate terms picks up a χ(cj) factor times a root-of-unity correction, reducing the cross-term computation to something tractable.

I'm then noting the sum over l vanishes unless j+j=0, so the whole expression reduces to evaluating over the finite type Fin 6 term by term, checking j=0 gives a contribution of 6.

For j=3, j+j=0 holds, and the squared star term simplifies through repeated powers of zeta12 down to -1, while all the other residues (1,2,4,5) fail the j+j=0 condition and contribute nothing, leaving the total as 6 plus the j=3 term.

Working out χ(c·3) = χ(c)³ = (-1)^{c.val}, so the normSq expression reduces to either 0 or 144 depending on parity of c.val — never 6, which is the contradiction I need. I'm now figuring out how to formally handle the (-1)^{c.val} parity case split in Lean.

Now I'm carefully planning the final evaluation of the sum over Fin 6, worrying about edge cases like the if-conditions and val computations evaluating correctly, and starting to define a term T summing chi(c*j) times a conjugated root-of-unity power.

Since the sum is real-valued (either 6 or 0), I realize I can just split on the if-condition and use conjugate-fixed-point lemmas for numeric literals to show the star of the sum equals itself, checking whether Mathlib has the right simp lemma for star fixing OfNat values.

I realize I can derive star(χ(a)) = χ(-a) directly from chi_mul_star by plugging in 0, which gives a cleaner path: then the sum over l of star(χ(al)) becomes a sum of χ((-a)l), reducing to chi_sum(-a), which simplifies via neg_eq_zero to the a=0 case.

Now I'm trying to restructure the per-term correlation identity involving star(gauss)² and χ(c·k) to stay as mechanical as possible, likely favoring a linear_combination-style approach for the cross terms.

So T_c becomes a pure character sum over a quadratic form in Fin 6, and I can compute its norm squared via an autocorrelation expression that factors into a term depending only on j times a linear character in l, which should be verifiable by `ring` in Fin 6 arithmetic.

The sum over l of that linear character collapses to 6 only when the coefficient -(j+j) vanishes, giving nonzero contributions only at j=0 (worth 6) and j=3 (worth χ(3c-3)·6, since 9 reduces to 3 mod 6). I'm now working out that χ(3c-3) = χ(3c)·χ(-3), and since χ(-3)=χ(3)=ω³=-1, I need to carefully evaluate χ(3c) for general c in Fin 6.

Splitting 3c as c+c+c lets me write χ(3c) = χ(c)³ = ω^(3c.val) = (-1)^c.val, which seems like a cleaner, more direct path through pure character identities than chasing individual Fin 6 arithmetic facts.

Now I'm working through the autocorrelation lemma for v using star_chi and chi_add to combine character products into a single exponent, then closing the arithmetic with ring over Fin 6.

`ring` works formally since it's a polynomial identity, independent of characteristic. Now I need to show the cross-term equals `chi ((b' - b) * k - k * k)`, which reduces to proving the squared Gauss sum relation `star(gauss k)^2 = chi(-(k*k))` by unfolding `gauss` as a power of `zeta12` and relating `zeta12^2` to `omega6` via `pow_mul` and `omega6_pow_mod`.

Still working through the rewrite chain...

Now I'm working out the cross-term expansion for the Gauss sum product, breaking it down using conjugation and character multiplicativity to express it as a character evaluated at a linear combination of indices, then starting to formalize this as a lemma in Lean.

Tracing through the rewrites step by step, matching both sides so the star and chi terms align into the target expression, confirming the algebra closes out correctly with h1 and h2 substituted in.

Verifying h1's chain of rewrites step by step: converting the product of conjugates into a squared term, applying the Gauss sum squared identity, then using the conjugation property of chi to land on the negated argument.

I then prove star_chi by specializing the cross-multiplication identity at zero and simplifying away the trivial terms, then use this to build overlap_cross, which unfolds overlap into a sum and matches each term via the cross_term lemma.

Now I define a quadratic character vector and try to prove a shift identity for it, rewriting the star and product via chi_add -- trying to combine the exponents algebraically so they match the target expression after a ring normalization.

For the quadratic autocorrelation lemma, I factor out the constant chi term using the sum pullout, then apply the chi_sum identity to collapse the geometric sum into the indicator form, which closes the goal by rfl.

That checks out, so the ring identity holds. Now I'm working out the normSq of the cross overlap term, which reduces to a sum over j of chi(cj-j²) times an indicator that's 6 when -(j+j)=0 and 0 otherwise, and I'm expanding that Fin 6 sum explicitly term by term.

Checking each indicator case: j=0 and j=3 give true (since 3+3=6≡0 mod 6), while j=1,2,4,5 give false, and `decide` should settle each of these Fin equalities by kernel computation.

I'm second-guessing whether `rw` actually delays elaboration of the `by decide` tactic blocks until after it unifies the `ite` pattern, since that ordering is crucial for this to work at all — I'm not confident it does, and I recall seeing similar `if_pos (by simp)` patterns elsewhere that might offer a safer alternative.

Given that risk, I'm considering instead proving the individual equalities and inequalities as separate hypotheses via `decide`, then feeding those into `simp only` to discharge the `if_pos`/`if_neg` conditions directly rather than relying on `rw` to unify through the tactic block.

Actually a full `simp` could be risky since Fin numeral normalization might simplify both sides unpredictably, like reducing `(3 : Fin 6) * 3` to `3` on both the lhs and rhs — I need to check whether that normalization applies consistently so the equation still holds after simp.

I'm also considering a cleaner approach: using a sum lemma like `Finset.sum_eq_add` to isolate just the two nonzero terms at j=0 and j=3, rather than evaluating the sum over all six indices.

Still working out the decidability proofs...

Working through the rewrite order carefully, I confirm the simplification reduces to normSq(6 + chi(c*3-3*3)*6) with c = b'-b, and now I'm expanding chi(c*3-3*3) via sub_eq_add_neg and chi_add into chi(c*3)*chi(-(3*3)).

I'm verifying that -(3*3) equals 3 in Fin 6, giving chi(3) = omega6^3 = -1, and that chi(c*3) reduces to chi(c)^3 by rewriting c*3 as c+c+c.

So the total sum works out to 6 - 6·(-1)^(c.val), and I'm checking the case where this power equals 1, making the total zero and normSq zero.

Still writing the Lean proof...

Still tracing the rewrite steps, making sure the associativity of the power multiplication matches correctly so the final cube identity applies cleanly.

I could also fall back to `decide` as a backup tactic if the rewrite approach fails. Now I'm working through some small lemmas about negation and sums in Fin 6 arithmetic, verifying each by decidability, building toward a general claim that for nonzero, non-three elements the negated sum behaves in a particular way.

Defining sum_quad lemma...

Checking that the two trivial side conditions close via membership in the finite universe, and double-checking the signature of `Finset.sum_eq_add` matches how I'm applying it, particularly that the `(by decide)` proof obligation for the inequality of the two chosen indices actually goes through.

Writing the have statement...

Checking that the beta-reduced sum matches the stated form, confirming `key_ne` lines up with the `if` condition for the `if_neg` rewrite, and verifying the `if_pos` rewrites apply correctly for the zero and three cases.

Good, that confirms the instance match works. Now simplifying the goal further: using `mul_zero` twice to clear the zero terms, then `sub_zero`, `chi_zero`, and `one_mul` to reduce the left side down to just 6, matching the right side's leading term.

Still writing lemma proof...

I'm establishing that the normSq equals 6 plus a chi term using overlap_cross and quadratic autocorrelation lemmas, then substituting the chi_cross_value to derive a contradiction assuming the normSq equals 6, and starting to case on the possible values of the sign term.

Checking that `hq` unfolds correctly by definitional equality, since `quad c k` is literally defined as `chi (c*k - k*k)`, so the sum matches `normSq_sum_eq` by rfl without needing an explicit rewrite.

Then I verify `rw [hq]` applies cleanly since its left side matches the goal exactly from `overlap_cross`, and I continue into rewriting `chi_cross_value` at `h1`, matching the pattern `chi (?c * 3 - 3 * 3)` to simplify it to `-((-1) ^ (b' - b).val)`.

For the two sign cases of `(-1)^n`, I substitute into `h1` and use `norm_num` to reduce each to a false numeric equation (`6 = 0` or a contradiction from `12`), closing both branches — relying on `norm_num` handling the real-to-complex coercion via `Complex.ofReal_ofNat`.

Good, that lemma exists with the right signature, and rewriting with it should match the term in h1 since both use the same val expression. Now I'm thinking about defining the overall family membership predicate as a disjunction over the two orbit types, mod and conjugate forms.

For proving every pair has distinct overlap, I need to handle the conj-mod and conj-conj cases by showing overlap is conjugate-symmetric: overlap z w equals the star of overlap w z, which follows from distributing star over the sum and using commutativity on each term. Since normSq is invariant under star, this symmetry lets me reduce these cases to the already-proven mod-mod case.

Actually, there's a simpler existing lemma `Complex.normSq_conj` that handles conjugate normSq directly, so I can just rewrite star into conj and apply it, with a fallback chain of tactics in case the defeq doesn't line up cleanly.

I also need to handle the analogous overlap computation between two conjugated Gauss sum families, which follows the same structure as before but with an extra `star_star` simplification layer. Then I'm assembling the final theorem statement that no pair from the Gauss family can have overlap normSq equal to 6, starting the proof by case-splitting on how z and w arise in the family.

I finish the case split with `rcases` producing four goals covering mod-mod, mod-conj, conj-mod, and conj-conj combinations, dispatching each with the corresponding lemma (using `overlap_star`/`normSq_star` to reduce the conj-mod case to the mod-conj case). I briefly consider whether I should also prove these twelve vectors are pairwise distinct, but decide that's not necessary for this theorem and can be skipped.

I double-check that gaussConj b 0 = 1 holds since star(gauss 0) times chi(b*0) simplifies to star 1 times chi 0, which equals 1, confirming it as a common ray.

Working out the autocorrelation at j≠0 gives zero since star 0 is 0. Then I notice something interesting: the overlap between gaussMod b and gaussMod b' is chi_sum(b'-b), which is 6 when b=b' and 0 otherwise -- meaning the six gaussMod vectors are mutually orthogonal, forming a basis. This is actually the known MUB triple structure {I, F₆, G}, though I won't try to formalize that broader fact here.

Now I'm reviewing the first file's conditional theorem and checking compile risks: I plan to import only SzollosiCommonRays rather than also SzollosiQuartetSystem, to avoid unnecessary name clashes since I don't actually need the latter module.

I'm worried some tactics like `interval_cases`, `linear_combination`, and `positivity` may not come in transitively, so I might just import all of Mathlib to be safe despite the compile cost.

Checking that each specific tactic module name is still valid in current Mathlib before relying on targeted imports instead of the full `import Mathlib`.

I'm trying to recall exactly which Mathlib file defines `Real.sqrt` and `NNReal.sqrt`, since I need the correct import path.

Since `Complex.abs` likely needs `Real.sqrt`, and I'm not certain all the needed imports are covered individually, I think just importing all of Mathlib is the safer choice here, even though it costs build time — that way name resolution won't be an issue regardless of the exact Mathlib version being used.

To avoid name clashes I'll rename them `gaussRay` and `quadRay`. I'm also checking that the `MonomialTransport` namespace resolves correctly given the file's actual namespace nesting, and double-checking whether `HasRawQuartet` is defined where I expect.

I'm structuring the file with `noncomputable section` followed by the namespace, mirroring how the existing repo file closes sections without an explicit `end` for the unnamed section.

I'll also print axioms inside the namespace before closing it. Checking that `Complex.ext` splits into real and imaginary goals correctly for `apply`, and verifying `linear_combination` and `Finset.sum_mul_sum` are available in the current Mathlib form I'm relying on.

I'm unsure which form is current given the version string, so to be safe I should avoid relying on that exact lemma name and instead manually rewrite the double sum using more basic, stable sum lemmas.

I'm also double-checking other lemma names I'm using like `star_sum` and confirming I'm no longer relying on `Fin.sum_univ_six`.

I need `interval_cases n` which requires importing the right tactic, and I'm checking the `conv` rewrite for `omega6 ^ n` using the mod-div identity to make sure the motive only abstracts the exponent correctly.

Thinking about alternatives: directly rewriting `n` everywhere with `h` would cause the substitution to also hit the `n % 6` on the right side, creating a messier nested expression, so the conv-based approach is cleaner. Considering a `calc` proof instead that splits the exponent into its mod and div parts explicitly.

Finishing the calc proof: the first step closes via `Nat.mod_add_div` which directly rewrites the sum back to `n`, and the second step uses `pow_add`, `pow_mul`, and the fact that `omega6^6 = 1` to collapse the extra factor, leaving just `omega6^(n%6)` — this is the cleaner version to use. For the `chi_add` lemma, I'm unfolding `chi`, rewriting the coercion of `Fin` addition, applying the periodicity lemma, and splitting the exponent with `pow_add`.

For `chi_sum`, I'm tracing through the `split_ifs`/`subst` logic for the `a = 0` case, then checking that `simp` can reduce the constant sum over `Fin 6` down to `6` via the chain of `Finset.sum_const`, `Fintype.card_fin`, and `nsmul_eq_mul` simplifications — I'm fairly confident this chain closes the goal.

For `commonRay_fourierSix_iff`, I'm deciding whether `unfold CommonRay` or `simp only [CommonRay]` is the right way to unfold the `CommonRay` definition, leaning toward `unfold CommonRay`.

For the next step, I'm rewriting the normSq overlap equality backward using `normSq_overlap_eq` and `h2 k`, then checking that `norm_num` handles the coercion of 6 to a complex number, with `first | norm_num | simp | rfl` as a fallback if the pattern match fails.

Checking that `simp_rw [hk]` correctly rewrites the inner sum under the outer binder since `hk` holds for all k, then confirming that splitting the zero-product case with `mul_eq_zero.mp` and discharging the false branch where 6 equals 0 via `norm_num at h` closes that case cleanly. Moving to the reverse direction, I'm now rewriting with `hs`, `autocorr_zero`, `zero_mul`, and `chi_zero`.

The `ne_one_of_im` proof unfolds the equality and extracts the imaginary part contradiction. I verify the `chi_ne_one` cases work by rewriting `omega6^2` and `omega6^5` expressions, checking the imaginary parts come out nonzero via `positivity` after simplifying with `Complex.sub_im` and `omega6_im`.

Next, `gaussRay_zero` simplifies the Gaussian ray at zero using `Fin.val_zero`, `mul_zero`, and `pow_zero` to collapse the exponent to zero, giving `1`. I'm checking `autocorr_gaussRay` next, which unfolds `autocorr` and `gaussRay` together.

Then for `normSq_overlap_eq`, I rewrite with `overlap_fourierSix` and `normSq_sum_eq`, matching the sum pattern so the weight function unifies correctly, then apply `Finset.sum_congr rfl` to reduce to checking the autocorrelation pointwise against the conjugated character term.

Unfolding `autocorr` via `simp` on both sides and distributing the sum with `Finset.mul_sum`, both the shifted sum and the right-hand side reduce to matching per-term expressions after another `sum_congr`, leaving a final `linear_combination` step relying on a character multiplicativity hypothesis.

I'm checking that `star_mul'` applies since ℂ is a commutative semigroup with star-multiplication structure, then verifying the reindexing via `Fintype.sum_equiv` with `Equiv.addLeft` works out through a `simp` call that should unfold the coercion of `Equiv.addLeft` into addition.

For `normSq_sum_eq`, I apply the same equiv-sum shift trick with `Equiv.addLeft l`, matching the required equality by direct computation. Similarly for `chi_sum_eq_zero`, I use `Equiv.addRight 1` to shift the sum index, with the per-term equality closed by `rfl` or `simp`.

For the mod-mod normSq inequality, I think I can avoid introducing `normSq_twelve` by casing on the if-condition directly: splitting into cases, rewriting with `normSq_six` or `Complex.normSq_zero`, then closing each branch with `norm_num`.

I'm confirming `Complex.normSq_ofReal` and `neg_one_pow_eq_or` as usable lemmas for the parity argument.

Checking the signature of `Finset.prod_eq_mul` (and its additive counterpart) — it requires distinct elements `a` and `b` with the rest of the function equal to 1, giving the product as `f a * f b`. This looks correctly matched with the decidable equality instance.

Now I'm verifying a `decide`-based claim about `Fin 6`: that for all `j`, if `j ≠ 0` and `j ≠ 3` then `-(j+j) ≠ 0`. This should be decidable since the universal quantifier over a fintype with a decidable predicate reduces via `Fintype.decidableForallFintype`, which unwinds through the finset and multiset machinery down to quotient recursion over the underlying list for `Fin 6`.

I'm now checking whether a specific rewrite using a lemma about `-(0+0) = 0` lines up syntactically with the goal that appears after unfolding the sum at index 0, since the rewrite only works if the stated hypothesis matches the term produced by that unfolding exactly.

Now checking the cross_term step: unfolding gaussMod and gaussConj should beta-reduce properly to give gaussRay times chi, and I'm considering whether redefining gaussMod to take both arguments directly would sidestep any unfold/beta issues.

I'm proving this by unfolding overlap into a sum, pushing star through with star_sum, then for each term applying star_mul' and star_star to flip the conjugate-multiply order, finishing with mul_comm to match sides.

For normSq_star, I try normSq_conj directly, or fall back to unfolding via star_def. Then for gaussMod_term, I'm unfolding the Gaussian character, applying star_mul' and distributing the subtraction over multiplication, then using chi_mul_star and a linear combination to close the identity relating chi at the difference to the product of conjugate terms.

Proving overlap_gaussMod by unfolding the overlap definition, simplifying with gaussMod_term, then applying chi_sum to the difference b' - b — the sum collapses to the character sum formula. Now I'm moving to the conjugate analog, setting up a lemma about the product of conjugated gaussConj terms...

I'm verifying the lemma holds by unfolding gaussConj and manipulating star and multiplication identities, using a linear combination involving the ray relation G·Ḡ = 1 to close the gap between both sides, confirming the difference vanishes by ring arithmetic. Next I'll set up autocorr_gaussMod and autocorr_gaussConj as planned design items.

Now I'm proving that gaussMod satisfies the CommonRay property for fourierSix: checking the base case equals one via gaussRay_zero and chi_zero, verifying the norm-squared condition using normSq_gaussRay and normSq_chi, and showing orthogonality for other indices by reducing autocorr_gaussMod to autocorr_gaussRay which vanishes.

I can add a cheap corollary stating orthogonality of distinct gaussMod vectors, following directly from the overlap formula with a nonzero difference argument. I'm also double-checking there are no naming collisions in Mathlib for identifiers like `autocorr`, `chi`, or `omega6` within the namespace.

Checking that `Matrix.of`, `Fin.val_mul`, `Fin.val_add`, `Fin.ext`, and `Fin.ext_iff` are all available as expected, then working out the proof that `n ≠ 0` inside `chi_ne_one` by deriving a contradiction from the hypothesis.

I'm confirming the Fin arithmetic reduces correctly through the kernel's literal evaluation, then hedging with a fallback tactic sequence combining `Fin.ext`, `subst`, and `simp` in case one approach fails on the substitution direction.

Checking that the `interval_cases` split handles the n=0 case properly with the inequality hypothesis, and that `show` correctly unfolds the goal after destructuring through definitional equality. I'm also verifying the `linear_combination` call with `ring1` closes the algebraic identity involving the star/conjugate atoms.

For `omega6_sq`, I'm tracing through the real/imaginary part lemmas to expand `(omega6^2).re` down to `omega6.re * omega6.re - omega6.im * omega6.im` using the known values for omega6's real and imaginary components, confirming it matches `(omega6 - 1).re`.

Checking the imaginary part computation also reduces cleanly with `ring`. For `normSq_omega6`, rewriting with the real/imaginary component lemmas gives an equation that `nlinarith` closes, and the same pattern verifies `zeta12_sq`'s real and imaginary parts via `ring`.

I'm also confirming the Complex anonymous constructor usage is valid since `Complex` is a structure with `re`/`im` fields, and that `Real.sqrt` remains the correct name in current Mathlib alongside the relevant square-root identity lemma.

I'm checking that the `fourierSix_apply` proof correctly unfolds `chi` and applies `Fin.val_mul` to match the exponent on both sides, verifying `show chi (i * j) = _` unifies properly with the goal.

If `Mat` is just a `def` wrapping `Matrix`, the elaborator should still unfold it via whnf to recognize it as a function type, so applying `fourierSix` to indices should typecheck fine.

Now I need to check the `BigOperators` scoped namespace usage and whether `Equiv.addLeft`/`addRight` on `Fin 6` will require specific additive group structure.

After rewriting the inner sum identity, I'm checking whether swapping the summation order with `Finset.sum_comm` followed by `rfl` actually closes the goal, since `autocorr w j` should unfold definitionally to the swapped sum expression.

I realize `all_goals rfl` is safe even if there are zero remaining goals, so I'll use that as a safety net rather than relying on a bare `rfl` that could fail if nothing's left to close.

Let me reconsider whether `simp_rw [hinner]` could loop or misfire: since the pattern is `l`-dependent and the rewritten term doesn't match the same shape again, it shouldn't try to rewrite recursively, but I want to double-check the unification carefully before trusting it.

Writing lemma statement...

I'm double-checking that each rewrite step actually makes progress and matches correctly, verifying the sum-splitting lemma applies to both sides as expected, and considering whether a more direct nested-sum lemma from Mathlib might simplify this further.

For the equiv-sum obligation, I'm confirming the `first | rfl | simp` tactic parses correctly in term mode and that unification with metavariables happens before the tactic blocks elaborate, so the goal should resolve properly.

Rechecking `hsum2`: rewriting `← chi_sum (j₀ - j)` replaces the indicator term with the character sum, then applying `Finset.sum_mul` distributes the multiplication across that sum to match the target expression.

The congruence step then handles each term by expanding the subtraction in the character argument and using multiplicativity, closing with `ring`. I'm also verifying `hj`'s substitution lines up the inner sums correctly against the `6 * autocorr z j₀` target, and now checking that `hsum` after the rewrite matches what the forward direction expects.

Moving on, I'm confirming the quartet conditional theorem applies cleanly given the pairwise overlap condition, and noting that file 2's final result, `gaussFamily_no_unbiased_pair`, doesn't actually need the no-quartet conclusion.

Now I'm checking that `gaussRay_commonRay` follows from the common-ray characterization, with the three conjuncts—zero mean, correct norm, and vanishing autocorrelation at nonzero lags—all matching up correctly against `autocorr_gaussRay`.

