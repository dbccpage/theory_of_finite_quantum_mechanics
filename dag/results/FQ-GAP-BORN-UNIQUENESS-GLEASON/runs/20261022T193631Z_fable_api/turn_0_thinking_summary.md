I need something concrete and compilable rather than another unresolved attempt. I recall that over ℚ(i), there's a triangle of pairwise orthogonal vectors all in the E_3 class, with two odd coordinates and one even, using vectors like (1,1,0), (1,-1,1+i), and (1,-1,-1-i).

Settling whether a global obstruction exists for all orthogonal frames seems hard without restricting to a subfamily, and proving the opposite direction looks even harder. I'm trying to recall whether the Hrushovski–Pitowsky work on effective Gleason theorems offers a route, since they established results about finite sets of rays and quantitative versions of Gleason's theorem for finite-dimensional Hilbert spaces.

This doesn't translate well to my situation since those frame functions are bounded and nonnegative, unlike the unbounded rational-valued ones I'm working with. I'm also recalling Pitowsky's and Meyer's work on rational rays and Kochen-Specker colorability, plus Clifton-Kent nullification results, wondering if any of these extend to Gaussian-rational vectors in the ℚ(i) case.

Actually, the Peres-Mermin 24 rays in ℝ⁴ are purely rational, with entries 0, ±1 — that's a clean example. But in dimension 3 over ℚ, Godsil-Zaks shows no KS set exists on the rational unit sphere; the question is whether a 0/1 coloring exists for all rational directions in ℚ³ more generally, not just unit-sphere ones, which I'm less sure about.

I recall Havlicek et al.'s work on coloring the rational quantum sphere, discussing orthogonal triples with non-square norms, but I can't pin down whether a full 2-coloring exists. Given the lack of tools and the difficulty here, I should focus on producing the largest honest, verifiable piece I can rather than guessing at unresolved results.

One promising direction: formalizing the exotic frame function on all primitive integer vectors in ℤ³ without the square-norm restriction, which strengthens what's already in the repo by showing frame additivity on real orthogonal frames alone doesn't force a quadratic function, though it leaves the extension field case open. Another option is proving the Gaussian triangle fact about the relevant exceptional set.

Working through all the type cases confirms that forcing f to factor through reduction mod (1+i) pins every value to 1/3, matching the quadratic solution exactly. This gives a clean, finite, kernel-checkable result: the parity/Meyer route collapses to the trivial constant function over ℚ(i), closing off that avenue rigorously.

Now I need to formalize this properly in Lean — setting up Gaussian rational vectors, the Hermitian inner product, orthogonal frames, and frame functions as ray-invariant additive functions on nonzero vectors. The trickier part is encoding the "mod (1+i) class" hypothesis cleanly for Gaussian-integer vectors so the statement captures exactly what I proved by hand.

I realize I don't need the full rays framework—just defining a frame as three pairwise orthogonal nonzero vectors and frame additivity as the sum over any frame equaling 1 suffices. Scale invariance isn't a separate requirement either, since f(λv)=f(v) actually follows from frame additivity itself.

Given any nonzero v, I can complete it to a frame (v,w,x) using a vector orthogonal to v in its 2-dimensional orthogonal complement plus a conjugate cross product, and since (λv,w,x) is also a valid frame, additivity forces f(λv)=f(v) automatically. This means I could define everything directly on vectors and prove scale invariance as a derived lemma, though constructing the completion explicitly in Lean (showing w and x are nonzero) would take extra work, so I'm weighing whether to include that lemma or skip it.

That works — w = (-conj b, conj a, 0) satisfies the orthogonality condition, and taking x as the cross product of conjugates of v and w gives x = (-a·conj c, -b·conj c, |a|²+|b|²), which I verify is indeed orthogonal to v.

Checking ⟨w,x⟩ gives zero too, and x is nonzero whenever (a,b)≠0; the remaining degenerate case (a,b)=0, c≠0 just uses the standard basis. Given the compile risk of each added lemma, I'm leaning toward keeping the Lean proof minimal and robust rather than adding scale invariance as an extra feature.

I have to be honest that neither direction (A) nor (B) is fully resolved. The best path forward is presenting a genuine strengthening: an exotic frame function defined on all primitive integer rays of ℤ³ (full ℚP², without the square-norm restriction) that's frame-additive and non-quadratic, since this naturally extends the real-valued exotic function relevant to the K-question. Now I'm weighing how difficult the Lean proof of frame-additivity would actually be for this ℚP² function.

I verify this against the frame (1,1,0),(1,-1,0),(0,0,1): the values 0, 2/3, 1/3 sum to 1 as expected, confirming the formula. But proving additivity in general requires more than just the mod-2 structure — I recall the real case needed a cross-product valuation argument to rule out all three vectors lying in the same class, so I need to check whether that same obstruction applies here.

I'm worried the mod-4 case analysis could blow up combinatorially if done naively—9 products each needing a 16-way split would be way too many cases for omega to handle directly. I need a smarter way to linearize each product, maybe by attaching derived facts about each product's residue rather than brute-forcing every combination.

Right, so if both even product is 0 mod 4, one even one odd gives the even one's residue mod 4, and for both odd the product mod 4 depends on whether their mod-4 residues match (1 or 3) versus differ, giving a case-split lemma characterizing x*y mod 4 based on x,y mod 2 and mod 4.

Now with nine such instantiated lemmas combined with the dot product equations and primitivity condition, I'm trying to see if omega alone can close the goal, but since the conclusion involves rational f-values, I probably need to reduce to a finite case structure by defining an integer-valued code function on vectors that captures the relevant parity pattern.

I verify the s(x,y) rule works on test cases like (1,1,0) and (1,-1,0), confirming consistency with the frame values. For the Lean proof, I realize omega can't handle if-then-else directly, so I'll need split_ifs to break the nested conditions into many separate goals before applying arithmetic reasoning.

With 343 branches each requiring omega on several seven-way disjunctions, the worst-case blowup is way too large to be practical. Instead I should isolate the real structural facts — a mod 2 lemma about orthogonal parity vectors having an even count of shared-odd positions, and a mod 4 lemma pinning down when the sign terms cancel for vectors sharing the same odd-position pattern.

Working through the parity patterns by weight (single positions, pairs, and the all-odd triple), I can classify exactly which pattern pairs are compatible with orthogonality — they must share zero or two odd positions, ruling out same-singleton pairs and singleton-pair mismatches.

Building possible frame triples from these patterns, I find candidates like {e1,e2,e3}, {e_i,ε_i,ε_i}, and {τ,ε_i,ε_i}, but the all-same-pair triple {ε_i,ε_i,ε_i} fails due to a sign pigeonhole argument — three values in {−1,1} can't pairwise sum to zero.

Now I'm considering how to encode this robustly in Lean. A single massive omega call seems unwieldy, so I'm thinking about introducing residues mod 4 for each coordinate and treating nonlinear products as fresh atoms, then supplying facts relating each product's residue to its factors' residues.

But worry is combinatorial blowup: nine products each needing a seven-way case split leads to a huge number of combined cases for omega to explore, and I'm not sure it prunes efficiently enough to stay tractable.

A safer route is to hand-structure the proof using parity lemmas instead of brute-force omega. I'm sketching a parity helper that expresses the dot product mod 2 in terms of the residues of each component, then building pairwise lemmas following the repository's existing style for this kind of argument.

For the mod-4 case, I'm working through the specific pattern where two vectors both have form (odd, odd, even) — since the even component contributes a multiple of 4, I need to relate the products of the odd components mod 4 to whether (u.a-u.b) or (v.a-v.b) vanishes mod 4, aiming for a lemma capturing odd*odd mod 4 behavior based on residues.

For the frame theorem I'm thinking through how omega can close the sum-of-three-residues case given the mod-4 constraints on each pair. Then I need a robust case split strategy for the main proof — likely deriving mod-2 pattern facts for each vector pair and using rcases across the possible residue patterns, though that could blow up combinatorially.

Alternatively, I'm considering encoding the function arithmetically rather than with if-then-else, using parity indicators and a sign function based on x*y mod 4 to replace the explicit odd/even branching.

Since omega can't handle the `if` conditions directly, I'm thinking I'd need to establish parity hypotheses first, then use simp to resolve conditions on mod-2 before split_ifs and omega tackle the remaining mod-4 cases—though this chain of automation steps is hard to verify without actually compiling it.

Given the fragility of running 512 cases through simp, split_ifs, and omega without compilation to check it, I'm reconsidering whether there's a cleaner formalization approach for this exotic function on ℚP² that avoids this much automation risk.

One idea is to classify vertices by their residue pattern mod 2 into a finite type, so orthogonality mod 2 becomes a decidable finite relation I can check with `decide`. The complication is that the g-value for patterns with weight 2 depends not just on the pattern but also on the sign of the s-value for the odd coordinates, so I'd need to split into that case separately.

The third shape contradicts via pigeonhole, the second gives sval sum zero, and the first forces all g to zero. But I'm wary that translating between vector residues and the Pat encoding for `decide` adds bridging lemmas, each one another compile risk.

A more manageable path: split each vector into one of 7 residue patterns via omega, then case-split all three vectors (343 goals total), followed by a uniform closing tactic like `first | omega | (simp; omega)` that uses product residue facts supplied beforehand for all nine coordinates.

I'm wondering whether omega's preprocessing actually handles conditional implications and biconditionals correctly for these mod-4 product facts, since that determines whether this approach will even work.

I'm trying to recall the actual source implementation of the omega frontend, specifically how it handles propositional connectives like negation, conjunction, disjunction, biconditional, and implication when processing facts during preprocessing.

Now I'm more confident omega converts implications into a disjunction form using decidability lemmas, and since the repo's own proofs feed it biconditionals directly, I'll favor using ↔ and ∨ rather than → to be safe, stating the mod-4 fact as an unconditional disjunction covering all parity combinations.

I tried checking orthogonality for the e_3/ε_3 frame pair but mislabeled the parity pattern initially—working through it again, the products end up all even, so it actually holds fine once I match up the correct component types.

Now I'm working out which facts I need: mod-2 parity suffices for most pairwise products, but the ε_i–ε_i case needs mod-4 facts since it involves two odd·odd products plus one even·even product. I'm formulating the mod-4 lemma as a disjunction rather than an implication to keep things in a form that avoids conditional reasoning.

Rather than defining g directly with an if-expression, which the goal still carries, I'm thinking I should instead prove a specification lemma characterizing g's output value based on the parity and mod-4 relationships between the components of v, structured as a disjunction over the different parity cases.

Then I worry that feeding all three such specifications plus the 27 product facts, dot equations, and primitivity constraints into a single omega call could cause an explosion of case splits, since each spec has multiple branches and omega might need to combine them combinatorially. I'm reconsidering whether omega actually defers splitting on disjunctions until the non-disjunctive facts alone fail to resolve the problem, which would make this much more tractable than a naive worst case.

To tame this, I think it's safer to structure the proof manually: split on g_spec of u, v, w via rcases first to get 343 concrete cases, then in each case call omega with just the parity facts to close it quickly.

I'm reconsidering g_spec to explicitly enumerate all 8 parity patterns instead of using negation of a conjunction for the "not exactly two odd" case — weight 0, 1, 3, and 2 (with subcases) — giving 11 leaves total, so the case product across u,v,w becomes 11³ = 1331, which is a lot but each case should close trivially.

So omega can indeed derive the contradiction since x*y%4=1 forces x*y%2=1, confirming those branches die. That caps things at roughly 1331 omega calls, likely 5-10 minutes total — borderline but workable, though I could cut this down by using rcases only on u and v (121 cases) and letting omega handle w separately.

Actually a better approach: split only on parity patterns across all 9 components (512 cases), with a helper lemma determining g from the pattern, then let omega resolve mod-4 subcases internally — primitivity should kill weight-zero cases trivially too, so this seems tractable via nested parity splits using emod_two_eq_zero_or_one on each component.

Writing the mul_emod_four proof...

Right, since the RHS has a nonlinear product of two non-literal terms, omega treats it as an opaque atom and won't substitute using the hypothesis unless I explicitly rewrite first — so the rw step really is necessary, matching what the repo does. I just need to confirm the rewrite only touches the intended subterm without accidentally affecting the LHS, since x and y are distinct variables here.

For the final piece, I want to define a rational-valued function f(v) = (1 + g(v))/3, then show f(u) + f(v) + f(w) = 1 follows from g(u) + g(v) + g(w) = 0, probably by unfolding f, pushing casts, and finishing with linarith.

Now I'm thinking about the non-quadratic case, where I'll need explicit ray vectors with concrete values — starting with the standard basis vectors and their pairwise sums.

Checking the candidate quadratic form against these seven vectors shows a contradiction: the value forced by (1,1,1) disagrees with the required f-value, confirming no quadratic form can fit. So I need all seven vectors to derive the contradiction properly.

Now I'm working on the proof mechanics — I need to compute the mod-based function g on concrete integer literals, relying on simp's modular arithmetic simplification to reduce each conditional to True or False so the if-then-else collapses to a concrete value.

I think `decide` should handle this fine since kernel reduction works through Int literals and emod evaluation, though there's some risk it fails on well-founded recursion edge cases—`norm_num [g]` might be a safer fallback.

I'm considering hedging the decidability tactic with a fallback chain trying `decide`, `norm_num`, and `simp` in sequence, since the mod equalities should reduce via simprocs. Then I shift to checking the quadratic obstruction statement mirroring the repo, starting to work through the primitive vector hypothesis values.

Rewriting the linarith setup for the seven equations...

I think importing the repo's `Vec3` makes more sense than redefining types, since I can reuse `normSq`, `dot`, `sq_emod_eight`, and `mul_emod_two_eq_one` directly. I'd define primitivity as the negation of all three components being even, matching the first conjunct of `IsRay`, and convert `Even` to mod-2 arithmetic via `Int.even_iff` for simp, following the repo's existing pattern.

Now I'm turning to the Gaussian integer case, setting up a `GVec` structure over `GaussRat` with an inner product defined using conjugation, and formulating what it means for three vectors to form an orthogonal frame with none of them zero.

I want to state a theorem showing that if a frame function's value depends only on the parity pattern of each vector's components mod divisibility by (1+i), then the function must be constant at 1/3 on all such Gaussian integer vectors not uniformly divisible by (1+i) -- essentially a parity-obstruction route analogous to the earlier arguments.

Now I'm working out the actual values using the explicit frame constraints: setting up equations across the 7 parity classes, I find that symmetric triangle frames force each two-coordinate class (like 110, 101, 011) to equal 1/3, and substituting back into the basis-frame equation forces each single-coordinate class (100, 010, 001) to also equal 1/3.

Checking a Type III frame with vectors (1,1,1), (1,-1,0), (1,1,-2) confirms orthogonality and gives class 111 the same value, so all seven classes equal 1/3 — meaning the density f of primitive Gaussian vectors landing in any fixed nonzero class is exactly 1/3.

Normalizing that gives `col 1 1 0`, so I can rewrite the final goal using the hypothesis equalities for `(a+b)%2`, `(c+d)%2`, `(e+g)%2` to reduce it to that same expression equaling 1/3, which closes via linarith with the earlier derived equations. Now I need to check how to verify orthogonality of the explicit Gaussian rational vectors in Lean, likely via extensionality and simp/norm_num.

Trying the combination of `ext` with `simp` then `norm_num` as fallback, since `<;>` only applies the next tactic to goals actually produced. I'm weighing whether `norm_num` alone (which includes simp lemmas) might suffice, versus risking a leftover goal neither tactic can close.

Now I'm figuring out how to express nonzero-ness for GVec — either giving it a Zero instance and using `u ≠ 0`, or defining it explicitly as a disjunction over the components, possibly decidable via GaussRat's DecidableEq.

I'm reconsidering whether `decide` can actually reduce this inequality given the derived DecidableEq instance, and thinking a safer approach might be extracting the real-component equality via `congrArg` and simplifying from there instead.

That projection reduction should work cleanly, giving me the component equality I need. For each explicit vector I'm using, I can just pick whichever component is nonzero and apply Or.inl or Or.inr accordingly. Now I want to make sure the frame function theorem statement is genuinely formulated over K rather than something weaker.

This captures the point that the parity route is closed over ℚ(i): any frame-additive function respecting (1+i)-parity classes must equal the constant 1/3, matching the Born value of the maximally mixed state, and I should note that the constant 1/3 function is trivially quadratic since it corresponds to ρ = I/3 — probably worth stating as a brief remark rather than a full lemma. I'm also thinking about including the fact that the ℚ-exotic function's restriction doesn't extend in the way one might hope.

I want to formalize the triangle frame as a standalone theorem showing three vectors all lying in the same (1+i)-parity class form a valid orthogonal frame — this is a genuinely new phenomenon compared to ℚ, where no such triangle can exist since three ε₃ vectors can't be pairwise orthogonal mod 4; I could state that non-existence as a corollary but it may not be necessary. Now I need to carefully recheck the ℚP² exotic function construction, since that's the central new theorem, making sure the math holds for every primitive orthogonal triple.

I'm defining a function g on primitive integer vectors that outputs -1, 0, or +1 based on the parity pattern of coordinates: it looks at which two coordinates are odd, then checks whether they're congruent or anti-congruent mod 4. My claim is that for any three pairwise orthogonal primitive vectors, these g-values sum to zero, and I'm working through the proof by tracking which coordinate positions are odd for each vector and using orthogonality to show the overlap in odd positions between any two vectors must be even.

I'm now casing out the possible combinations of weight patterns (number of odd coordinates: 1, 2, or 3) across the three vectors, checking which overlaps are forced to be disjoint, equal, or impossible, and starting to verify the sum condition for each case like {1,1,1} and {1,1,2}.

Checking the {1,1,3} case next: since 1 and 3 overlap, it's automatically impossible, and I'm verifying the {1,2,2} case parallels the parity contradiction found in the previous pattern.

Checking both cases confirms the condition holds either way, so the orthogonality works out. Testing {1,2,3} fails since 1 and 3 can't pair, and {2,2,2} leads to a contradiction where each sum would need to equal both its negative and itself, so that case is impossible too.

Continuing through remaining cases: {2,2,3} works since the pair lemma only needs the two weight-2 vectors orthogonal, while {2,3,3}, {3,3,3}, {1,3,3}, and {1,1,3} all fail. With all cases checked, the theorem holds, confirming non-quadratic behavior with the seven vectors shown, and I'm now verifying scale invariance under multiplication by odd integers since the parity pattern stays unchanged.

Next I need the negation symmetry g(-v) = g(v), which follows directly from the symmetry of the mod-4 condition under sign flip. I'm considering proving this via the spec lemma since both sides satisfy the same specification, letting omega close the gap, and thinking through how splitting on the if-conditions would expose the right hypotheses to make the disjunction goal provable automatically.

Now I'm setting up the Lean file with the necessary imports and opening the Vec3 namespace from the rational sphere module, then defining primitivity of a vector as not having all three components even.

Actually I realize dot-notation would break since defining `Vec3.IsPrimitive` inside the new namespace would create a different qualified name than the original `Vec3` type's namespace, so I should just define `IsPrimitive` as a plain function and call it directly rather than relying on dot notation.

Now I'm proving that `IsRay` implies `IsPrimitive`: if a vector isn't primitive, all three components are even, but `IsRay` already asserts the negation of that evenness condition, so I can derive a contradiction directly using `Int.even_iff` to convert between evenness and the mod-2 characterization.

I'm defining a sign function for pairs of odd integers based on their congruence mod 4, then building `g` as a piecewise function that picks which pair of coordinates to apply the sign to depending on which two components are odd and which is even.

Still writing specification cases...

I'm finishing the proof by unfolding the sign function definition and letting `split_ifs` combined with `omega` handle all the parity case splits automatically.

For the multiplication mod four lemma, I'm setting up a case split based on parity, reducing products modulo 4 via the mod-of-mod identity to establish the four disjuncts.

I'm checking that rewriting with the mod-4 hypothesis doesn't accidentally match inside the multiplication term, then verifying a mixed case example where x%4=0 and y%4=1 to confirm omega can derive the mod-2 facts needed for the final arithmetic, since omega handles the linear relationship between mod-4 and mod-2 remainders correctly.

Now I'm moving on to sketch the frame theorem for primitive vectors u, v, w.

Still case-splitting on parities...

I'm now branching through all the mod-2 cases for each coordinate and closing each with omega, though I'm worried about whether 512 omega calls with all these nested disjunctions and equations will actually be feasible to verify.

Worst case comes to roughly 9 binary splits giving up to 512 leaves, each a small LP, so compilation probably stays around a few minutes even accounting for this. The dead-branch pruning relies on omega deriving contradictions quickly from the known parity facts, which should kill most branches almost immediately when a parity conflict is detected.

Since omega adds all equality/inequality facts before splitting any disjunction, the parity hypotheses from rcases are already known when branching begins — so splitting on the first disjunction immediately kills most branches via parity contradictions, since each branch gets a fresh feasibility check before recursing further.

The `≠` facts on `(x-y) % 4` similarly split into `<`/`>` but since the remainder is bounded between 0 and 3 with the equality excluded, only one branch survives. This all seems fine.

Now I'm moving to the ℚ-valued frame theorem statement.

Writing the conversion proof...

The `linarith` call should close the fractional sum equation since it reduces to simple linear arithmetic over ℚ. I'm also verifying the lemma that `g` only ever takes values -1, 0, or 1 via `omega`, and starting to think about how `g` behaves under negation of the vector.

Now I'm worried whether `omega` can actually simplify `g_spec` applied to the negated vector's constructor projections, since omega needs to treat those field accesses as matching atoms, and I'm uncertain whether its atom-matching handles defeq reduction through anonymous constructors properly.

I'm worried `simp only` might fail with "no progress" if it doesn't reduce the projections, so I'm considering alternatives — stating a lemma directly over an explicit vector, or unfolding `g` and `pairSign` and splitting on the if-conditions before calling omega.

I'll plan `g_neg` with a proof that unfolds `g` and `pairSign`, then splits on all the if-conditions so omega can close each case, expecting many goals but all trivial. Checking for edge cases where simp might oversimplify conditions, but with only those two lemmas it should stay safe.

As an alternative, I consider proving `g_neg` via `g_spec` applied to the negated triple, then using `dsimp only` to reduce the structure projections directly to `-a`, `-b`, `-c` without needing a full simp call.

Now for the concrete value lemmas like `f ⟨1,0,0⟩ = 1/3`, I'm thinking of just using `decide` or unfolding directly since these are fixed numeric evaluations.

This should reduce cleanly through kernel evaluation of Nat mod and Int subtraction, so `decide` ought to handle the small integer arithmetic in `pairSign` without issue, consistent with how the repo already uses `decide` for similar Even/parity checks on Int.

I'm planning to prove the value lemmas for g using `decide`, then derive f's values by rewriting with the definitional equations and g's computed values, finishing with `norm_num` on the resulting rational arithmetic.

Next I'm formulating the main theorem stating that f cannot be expressed as a quadratic form in the components of v — asserting no coefficients exist such that a symmetric quadratic expression in v.a, v.b, v.c matches f v for all primitive vectors.

Running norm_num on each equation should clear the casts and projections, leaving linear equations I can feed into linarith to pin down r00=r11=r22=1/3 and r01=-1/3.

I realize each hypothesis does have casts or projections that norm_num can simplify, so none will fail with "no progress." I could also just fold the f_e1, f_e2, etc. rewrites directly into the norm_num simp set rather than doing separate rw steps, though I need to make sure simp doesn't accidentally touch the literal vector arguments before applying those rewrites.

Since Int has reduceEq simprocs in Lean core, norm_num with the relevant definitions unfolded should handle these equalities fine. Given I can't actually compile this, I'm building in redundancy by trying decide first, then falling back to norm_num with the definitions unfolded for each lemma.

Now I'm shifting to defining the Gaussian integer vector space structure in Lean: a GVec structure with three GaussRat components, plus an inner product function and a nonzero predicate for vectors.

I'm defining what counts as an orthogonal frame (three mutually orthogonal nonzero vectors) and what it means for a function to be a "frame function" satisfying additivity across such frames, then setting up a helper constructor for building Gaussian integer vectors from integer coordinate pairs.

I'm also formalizing the hypothesis that a frame function's value is determined by the parities of coordinate sums, and stating the theorem that this forces the function to equal 1/3 whenever the parity condition excludes the all-even case—then enumerating explicit orthogonal frames (standard basis, and several "type II" frames mixing basis vectors with diagonal combinations) to use as test cases in the proof.

Now checking orthogonality between the two complex vectors, verifying their inner product also vanishes.

Then I verify the parity classes for each pair match the (1,1,0) pattern before moving to the next triangle class F7, where I'm permuting components and checking pairwise orthogonality across its three vectors.

Checking orthogonality for F8's vectors confirms both inner products vanish. Now I'm setting up the system of equations relating the coefficients c100, c010, c001, c110, c011, c101, c111 from each face constraint, building toward solving for their values.

I'm checking that the integer-to-rational casts simplify cleanly for the gv literals, and that the parity checks on expressions like (1+0)%2 and (-1+0)%2 evaluate correctly via norm_num.

Now I'm verifying the inner product computation for two orthogonal vectors by unfolding the definition and checking the star-multiplication terms cancel.

Working through whether simp will fully close both goals after the cast pushes and sign arithmetic, confirming there's no branch left unsimplified, and double-checking that the `gv` definition unfolds cleanly under simp without leaving stray terms.

For the nonzero proofs, I'm reasoning that proving `(gv ...).NonZero` reduces to showing a component like `.x ≠ 0`, which after unfolding via congrArg and simp collapses to a false numeral equation like `1 = 0`, closing the goal by contradiction.

I'm sketching a helper lemma that derives `GVec.NonZero` from a hypothesis on the real part, using `Or.inl` with a rewrite step that turns the assumption into the definitional fact that zero's real part is zero.

I'll similarly define `nonZero_of_y` and `nonZero_of_z`, then apply these to specific vectors like `gv 1 0 (-1) 0 1 1` by simplifying `gv` and reducing the integer cast inequality down to `one_ne_zero` or the negative-one case.

Now I'm applying the frame function hypothesis to the specific triple from frame6, then using the parity lemma hP to compute each term's value by normalizing the mod-2 arithmetic for each coordinate combination.

I should double check that instantiating hP with specific literals like negative numbers will syntactically match the frame equation's term, since elaboration needs to produce identical normal forms on both sides for the substitution to go through cleanly.

For the final step, I'm worried that using `rw` with multiple lemmas at a hypothesis will fail if any single lemma's left-hand side doesn't actually appear there, since `rw` errors on an unused rewrite—so I should switch to `simp only` instead, which tolerates lemmas that don't apply.

Linarith should treat those function applications as atoms since it recognizes syntactically matching terms up to defeq. So my plan is to collect all the frame equations and the roughly fifteen class-value equations across the distinct vectors and feed them together into linarith.

For the main goal, given arbitrary residues with the hypothesis that they're not all equal, I rewrite using the key equation to reduce the goal to a statement about the mod-2 classes, then case-split on each residue being 0 or 1. The all-zero case is ruled out directly by contradiction with the hypothesis.

I'm checking that the rewrite correctly substitutes the parity conditions into the goal expression, confirming linarith can close each remaining case from the linear frame equations—deriving c110, c101, c011 each from their respective three-term sum equaling 1.

Now I'm considering whether to add a scale-invariance lemma showing a frame function only depends on rays, which would require proving that any vector can be completed into a frame and defining scalar multiplication on GVec to formalize it.

For showing u nonzero, I need to use that its last component equals the sum of norm-squares of the first two coordinates, which is positive since v is nonzero, relying on lemmas like `re_star_mul_self` and `normSq_eq_zero_iff`. This is doable but fiddly — roughly twenty lines — and then I still need to verify the inner product orthogonality conditions between v, w, and u.

Working through the orthogonality computations, I can get inner(v,w) and inner(v,u) to vanish by treating star v.x, star v.y as atoms and letting `ring` close them out algebraically. The inner(w,u) case is trickier since it needs simp lemmas like `star_star`, `star_neg`, `star_zero` to clean up before `ring` can finish.

Now I'm turning to how scaling interacts with inner products: proving that inner(λ•v, w) pulls out star λ times inner(v, w) by unfolding smul and star_mul, which should let me establish the key lemma for scaled frames.

For the nonzero case, scaling preserves nonzero coordinates via mul_ne_zero, so f(λv) must equal f(v) by comparing the sum-to-one equations. Then I move to case B, where v.x = v.y = 0 forces v.z ≠ 0, and I need to build a frame using e1, e2, v while verifying orthogonality against v's vanishing first two components.

This addition adds roughly 60 lines with moderate compile risk, so I'm weighing whether to isolate it in a separate file to protect the main proof from a cascading failure if the host audits and rejects on any error.

So my plan is to split things into separate files — one for the exotic ℚP² frame function, one for the Gaussian parity/triangle obstruction, and possibly one for ray-invariance — so a failure in one doesn't sink the others. Then I'm thinking through how to state the main theorem: an exotic frame function exists on every orthogonal frame of primitive integer vectors in ℤ³, without any square-norm restriction, taking multiple values and not reducible to a quadratic form.

For the Gaussian case, I want to show that any frame function on K³ depending only on parity class is forced to be constant 1/3, meaning the natural parity-based route to a counterexample is closed off — a clean negative result. I'll note as a remark that restricting a K-frame function to real rays gives back a ℚ-frame function, so whether the exotic ℚ-function extends to all of K remains an open question.

I'm also considering a third theorem: over ℚ there's no "epsilon-triangle" of three pairwise orthogonal primitive integer vectors sharing the same odd-odd-even parity pattern, which follows cheaply from the pair lemma since the sum of three odd numbers can't be zero — this contrasts sharply with what's possible over K.

I should state precisely what's proved, and I need to verify that `Int.emod_two_eq_zero_or_one` is available in Mathlib under the right import path for this repo.

To avoid depending on an uncertain name, I'll just prove the mod-2 case split directly with `omega` instead. I also confirm `Int.mul_emod` is already used correctly in the repo, so I just need to finalize which two repo imports to bring in.

On the rational sphere where exactly one coordinate is odd, the new function f reduces to the constant 1/3, which is distinct from the parity-based construction — worth a remark but not a problem for the argument.

I'm now drafting the Lean file for the rational plane obstruction, setting up the namespace and defining what it means for an integer vector to be primitive at 2 (not all coordinates even), since every rational ray reduces to such a primitive representative.

I'm checking that the dot notation resolves correctly within the namespace, confirming `h.1` gives the needed non-all-even property. I'm also reconsidering the "exactly two representatives" claim—primitivity (gcd 1) is distinct from just being odd-primitive (not all-even), since non-primitive vectors like (3,3,0) still qualify as odd-primitive, and I need invariance of the function under odd scalar multiples for the ray to be well-defined.

I'm working through why that invariance holds: showing the mod-2 and mod-4 parity conditions reduce correctly under multiplication by an odd integer, but `omega` struggles to relate product terms like `k*a` and `k*b` without more explicit algebraic facts connecting them.

I'm weighing whether odd-scaling invariance is actually necessary here — since vectors like (3,3,0) and (1,1,0) represent the same ray, the function needs to agree on odd multiples, not just sign flips. Restricting the domain to gcd-primitive representatives might be simpler than proving the full odd-scaling lemma.

I'm leaning toward splitting this into a third file for the invariance lemmas (g_neg, g_odd_smul), importing from the core file, to isolate the risk if the proof turns out harder than expected. For the odd scaling case, I'm trying to reduce it to g_spec applied to the scaled vector plus some modular arithmetic facts about products.

I'm planning to prove g_spec' by unfolding g and pairSign, relying on simp's projection reduction to simplify the constructor application down to plain components, then closing with split_ifs followed by omega.

For g_frame, I'll destructure u, v, w into their explicit coordinates so that Vec3.dot and IsPrimitive unfold cleanly via simp only, reducing everything to a purely variable-based arithmetic statement that I can then feed into g_spec'.

Checking that `simp only [g]` properly unfolds the definition through the projections and `pairSign`, and confirming `split_ifs` leaves hypotheses that `omega` can still use even if inaccessible.

I'm locating `mul_emod_two_eq_one` as the accessible lemma relating `x*y % 2 = 1` to both factors being odd, then sketching the `g_frame` theorem statement for a frame of three pairwise-orthogonal primitive vectors.

Still writing proof...

Chaining all nine parity rcases together before a final omega call, letting it brute-force all 512 resulting cases—though I wonder if omega alone could handle the disjunctive facts without the explicit case split at all.

Continuing the linear cases confirms those also work fine. Checking the dot product terms, I verify that the `mul_emod_four` facts match the exact atom ordering used in `Vec3.dot`, like `a₁ * a₂` rather than the reversed order, since omega treats multiplication atoms as order-sensitive.

Now I'm drafting individual decidability lemmas for specific unit vector inputs.

I trace through the kernel reduction manually: negating -1 gives 1, so 1+1=2, and 2%4=2≠0, landing in the else branch giving 1 as expected. I also note a potential concern about whether `decide` will efficiently reduce the `Decidable` instance for this equality.

For the integer mod check, decidable equality on Int reduces fine through Nat's decEq, and `decide` proving simple mod facts is standard practice in Mathlib, so I plan a fallback using `first | decide | norm_num [g, pairSign]` for robustness. Then I check that `rw [f]` correctly unfolds the definition to rewrite the first matching occurrence before applying `norm_num` to finish the arithmetic.

I realize combining everything into a single `norm_num [f, g_100]` call is cleaner since it avoids the "no goals" error that would occur if `simp` already closed the goal before a separate `norm_num` call. For the non-quadratic theorem, I'm checking whether `IsPrimitive` instances can be discharged by `decide` since the predicate reduces to decidable equalities on integers.

I'm weighing whether `intro h; omega` would work versus just unfolding first — safer to unfold `IsPrimitive` so the projection reduces properly before `decide` evaluates it, since all the needed decidability instances (negation, conjunction, integer equality) are available.

As a fallback, I'm setting up a `first` combinator trying the unfold-decide approach then `norm_num [IsPrimitive]`, and starting to sketch the main theorem statement that no rational quadratic form matches the target function.

Finishing the statement, I then begin the proof by introducing the hypothesis and instantiating it with specific primitive vectors to derive constraints on the coefficients.

Checking that h7's normalized form gives sum=1, then combining h4, h5, h6 with the diagonal values yields S=-1 while h7 forces S=0 — a clean contradiction that linarith should close. I'm just double-checking norm_num produces forms linarith can actually use directly.

Also sketching a corollary stating no real triangle can satisfy that parity pattern across u, v, w simultaneously.

I'm reasoning that g_spec extends naturally to Vec3 by destructuring components, and then omega should close the goal using the disjunctive facts from g_spec for each vector plus the frame equation g(u)+g(v)+g(w)=0, since the parity pattern forces each g-value to be ±1, making the sum odd and nonzero—a contradiction.

Moving to the invariance file, I'm now proving a lemma that for odd k, k*m mod 4 equals 0 iff m mod 4 equals 0, working through the modular arithmetic by splitting on whether k mod 4 is 1 or 3.

Then I'm building the proof that g is invariant under scaling by an odd integer k, using the spec equation for both scaled and unscaled triples.

I'm checking that omega can treat the term involving g as an opaque atom, since it's a non-arithmetic expression, and confirming that the linking lemmas tie the k-scaled atoms back to the original variables so omega can close the goal.

For g_neg, the same approach works directly since everything reduces to linear conditions omega can handle. Then f_neg and f_odd_smul follow as straightforward corollaries by unfolding f and rewriting with g_odd_smul. I'm now moving on to checking the Gaussian integer file.

Setting up the GVec structure...

Now I'm completing orthogonality conditions for pairwise frame vectors, defining a frame function as one summing to 1 over any orthogonal frame, and adding a helper constructor for building Gaussian-integer vectors from integer components.

I'm noting that the Gaussian-rational pair needs integer-to-rational coercion, then working out that divisibility by (1+i) corresponds to matching parity between the real and imaginary parts, which I can express via a mod-2 condition. I'm now defining a property capturing when a frame function is fully determined by this parity class across coordinates.

Writing helper lemma proofs...

Using `Or.inl fun e => h (by simp [e])` resolves that case cleanly, and I'll apply the same pattern for y and z. Now I'm setting up explicit standard basis vectors using `gv` literals to build the frames directly, and working through how `simp` handles the inner product expansion with `norm_num` to verify the numeric computations.

Working through the arithmetic, I get 1 + 1 - 2 = 0, confirming the identity holds, though I need norm_num or simp to fully close the numeric evaluation.

I'm confirming that `(1 : ℤ)` always elaborates to the same `OfNat` instance regardless of context, since instance resolution is deterministic, so `Int.cast_one` applies cleanly and `norm_num` should handle these casts fine.

So I'll try `ext <;> simp [GVec.inner, gv] <;> norm_num` as a plan — simp should always unfold things enough to avoid a "no progress" error, and the relevant lemmas like `re_mul` are already tagged simp, so this should close the goal.

Each non-zero obligation reduces to a numeral inequality after unfolding `gv`, which `norm_num` closes directly. Now I'm writing the frame theorem for F6, building the `IsFrame` term using `nonZero_of_x` with `norm_num [gv]` for each component...

I should wrap each tactic block in parentheses to be safe, and consider factoring out the repetition by proving a reusable lemma computing the inner product formula for general gv components, then applying it in each case.

I realize I need GaussRat.ext_iff to handle the zero-equality goal properly, since simp alone may not unfold it. Weighing whether to prove a single inner_gv lemma versus directly doing `ext <;> simp [GVec.inner, gv] <;> norm_num` per frame instance -- the direct approach seems more robust since each resulting numeric equation is elementary and norm_num should close it easily across all 21 cases.

Now I'm drafting the main theorem statement establishing that under the non-parity condition, f equals 1/3, and starting to work out the specific class values for explicit vectors needed to build the proof.

I'm confirming the arithmetic simplification reduces both sides to the same literal values, so `norm_num` should close the goal via `rfl` after evaluating the mod operations, including checking that negative literal cases also reduce correctly.

Actually I realize different vectors with the same class would produce syntactically distinct mod-expressions, so linarith couldn't match them as the same atom. I need to normalize each instance with `norm_num` right after extracting it, so each hypothesis reduces to a clean literal form like `col 1 1 0` that can be compared directly.

Writing proof tactics...

The rewrite only touches the goal, leaving `hne` untouched, which should be fine. Now I'm moving to a separate file for the scale-invariance lemma, proving that scaling a vector distributes over the inner product by unfolding the definitions and applying conjugation and ring arithmetic.

Still writing proofs...

Now I'm working on the case where v has zero x and y components, meaning v is purely along the z-axis with z nonzero, and I'm constructing the frame using the standard basis vectors e1 and e2.

Still proving the scaled version with inner product smul lemmas, then moving on to the case analysis where (x,y) isn't zero.

Now I'm checking that w is nonzero in each branch, using `star_eq_zero` to tie nonvanishing of v.x or v.y to nonvanishing of w's components, and setting up `neg_ne_zero` for the corresponding case.

For u nonzero, I'm reasoning that u.z's real part equals the sum of normSq of v.x and v.y, which must be positive since at least one of v.x, v.y is nonzero, giving positivity via `normSq_nonneg` plus a strict inequality argument.

Still working out the positivity proof...

Still working out the nonzero argument...

Now I'm verifying the two inner product identities algebraically — checking that inner v w reduces to zero by simple cancellation, and that inner v u also cancels to zero by expanding the star terms.

That smul case follows similarly using inner_smul_left. Now I'm proving frameFunction_smul: given a frame function f and nonzero v scaled by nonzero l, I obtain the frame vectors, apply the frame function property to both v and the scaled version, then close the goal with linarith since both evaluate to the same value.

I'm considering whether to add a trivial Lean theorem about the constant 1/3 being quadratic-like, but decide to skip it since it's not needed. I should double check that the "WHAT IS PROVED" summary is precise, and mentally verify that omega can handle at least one nontrivial case among the 512 possibilities in File 1's main theorem.

Tracing through a specific case with u, v, w parities (1,1,0), (1,1,0), (0,0,1), I check that the branch logic for g correctly resolves each vector's value and confirm the modular arithmetic constraints line up for the omega solver to close.

I'm checking whether omega can actually handle this modular case split, since it needs to introduce quotient variables to track b₁-b₂ mod 4 and confirm it lands on residue 2 given the parity and non-zero constraints.

Omega is complete for Presburger arithmetic with these case splits, so this should be derivable through its exact divisibility reasoning (dark shadows and such). This confirms the problem is a legitimately linear integer arithmetic case that omega should solve correctly.

Double checking the g_spec' pattern for (0,0,1) w, specifically that the 4th disjunct's structure negates the right conjunction of parity conditions, and that omega's preprocessing correctly turns negated conjunctions into disjunctions of negations during fact addition.

To be safer, I'm considering rewriting that disjunct positively instead, listing out the remaining weight-0, weight-1, and weight-3 parity cases explicitly rather than relying on the negation.

I'm checking that split_ifs correctly splits all nested if-conditions in the goal after unfolding g and pairSign, keeping the goal count manageable, and worrying whether the simp step might collapse branches in a way that breaks the structure.

Then I'm double-checking decide can evaluate the integer mod arithmetic kernel-side for a specific case like g ⟨1, -1, 0⟩ = 1.

literals and modular arithmetic correctly. I'm satisfied the kernel can reduce all of this via `decide`, so no issues with decidability synthesis. Now I'm checking the explicit primitivity proof for a specific triple, planning to unfold `IsPrimitive` and verify it directly.

I should also run `#print axioms` on the main theorems, and double-check that opening the `BornFable.RationalSphere` namespace doesn't cause naming collisions between my new lemma names and existing ones like `parity`.

To avoid clashes, I'll rename my functions more distinctively—using `sgn` for the sign function and `exotic` for the rational-valued function, plus `pairSign`, while checking these don't collide with `Vec3.normSq` or other existing definitions in the opened namespace.

Now I'm writing out the full first file, starting with imports and setting up the `BornFable.RationalPlane` namespace, defining `IsPrimitive` for vectors and beginning a theorem about primitivity...

Still writing sign definitions...

Still writing the specification cases...

I'm finishing the lemma by unfolding the sign definitions and letting `split_ifs` with `omega` handle the case split, double-checking that simp correctly reduces the struct field projections like `.a`, `.b`, `.c` down to the plain variables before the tactic closes the goal.

Writing frame theorem proof...

Deriving more mod-four multiplication facts...

Now I'm setting up parity cases for each variable and splitting into all combinations via rcases to check the sum of squares mod 4 exhaustively.

Checking that the primitivity and dot-product hypotheses unfold correctly after destructuring the vectors into components confirms the equations I need hold.

Checking the atoms line up with sgn_spec, and confirming the four-way rcases pattern for the mod-four disjunction destructures correctly. I'm also verifying the left-associated `<;>` chain correctly applies each subsequent tactic to all remaining goals, then moving on to check exotic_frame_function, its values, the non-quadratic property, no_real_triangle, and exotic_eq_third_of_isRay.

For rays with exactly one odd coordinate, I want to show sgn equals zero by pulling in the repo's `ray_exactly_one_odd` lemma, converting its odd/even disjunction through parity simp lemmas, then closing with sgn_spec and omega — this gives the nice fact that the exotic function is constant 1/3 on the rational sphere despite being globally non-quadratic. I'm drafting this proof now.

Still writing proof tactics...

Actually, I realize it'd be cleaner to avoid destructuring entirely and state `sgn_spec'` directly in terms of `v.a`, `v.b`, `v.c` so the atoms in `h` and `hs` match up naturally without needing simp to reduce projections.

For sgn_odd_smul I can unfold sgn and pairSign on both sides and split_ifs with the parity facts already in context, letting omega close each branch — though that could generate up to 49 case splits since both sides have nested conditionals, each should still resolve fine with omega.

Similarly sgn_neg should follow the same unfold-then-split_ifs-then-omega pattern, since the negated coordinates' parity and difference conditions remain linear and omega-friendly.

For sgn_spec, I'm confident simp can reduce the projections of explicit vectors so decide handles concrete cases at the kernel level. Then exotic_three_valued follows by case-splitting on sgn_mem into the three possible values and simplifying exotic in each branch.

Working through the remaining case confirms norm_num handles all three values correctly. I should also verify exotic's values land in [0,1], and double-check the destructuring pattern matches the repo's approach before moving to the axioms check and reconsidering File 2's normalization strategy, starting to write a have-statement for the color function evaluation.

I should double check that `decide` handles negative literals correctly too, tracing through how `(-1 + 0) % 2` reduces via the integer arithmetic rules in the kernel to make sure the disjointness condition still evaluates properly.

Now I'm moving on to setting up explicit vector and frame definitions for File 2, starting with each class vector like E1 for (1,0,0).

Continuing to build out more vectors and checking their classes — including T, S, and complex-valued cases like A, B, C, D, verifying parity conditions on each coordinate.

Now I'm verifying orthogonality across several coordinate frames, checking dot products between vector pairs like E3/P/M, E1/Q/Qm, E2/R/Rm, and T/M/S to confirm each frame forms a valid orthogonal set.

After confirming fr8 also checks out orthogonally, I'm now setting up the coefficient equations from each frame condition, finding that fr2 gives c001 + 2c110 = 1, fr3 gives c100 + 2c011 = 1, fr4 gives c010 + 2c101 = 1, and fr5-fr8 each reduce to 3 times a single coefficient equaling 1, pinning down c110 and c101.

Solving the system gives every class coefficient equal to 1/3, satisfying all seven equations consistently across the 17 classes I need to check, including E1, E2, E3, P, M, Q, Qm, R, Rm, T, S, A, B, C, D, F, G. I'm now verifying the inner products component-by-component, double-checking that pairs like C and D remain orthogonal using their explicit coordinate values.

Checking that each vector's nonzero component unfolds correctly via `gv` and reduces to a simple integer cast inequality that `norm_num` can close, with the right component (x, y, or other) chosen for each case.

Now I'm reasoning through whether anonymous constructor notation `⟨...⟩` can work directly for `IsFrame`, since it's a def unfolding to a conjunction — the elaborator should unfold it via whnf to find the underlying And structure, which is a common pattern for such definitions.

Good, confirmed—whnf with default transparency unfolds defs for anonymous constructors and rcases alike, so that pattern should work fine for IsFrame and NonZero. Now checking whether applying a def-wrapped hypothesis like IsFrameFunction directly to arguments also triggers the necessary unfolding.

Writing GaussianFrames file...

Defining more structures...

I'm realizing `PiPrimitive` as a plain def might block `decide` from working since instance search won't unfold it, so I'm considering making it reducible or just inlining the negation condition directly to sidestep the issue.

I'm also writing small helper lemmas showing a vector is nonzero when one of its components has nonzero real part, each proved by case analysis and simp.

If simp leaves leftover goals norm_num should mop up the numerals, and I've already double-checked the arithmetic so I'm not worried about simp reducing things to False. Actually a cleaner approach might be using norm_num directly with the ext_iff lemma generated by @[ext] so one tactic call handles both components at once.

Checking that simp's default lemmas won't mangle a star of a basic vector since re_mul/im_star split things properly, I'm now setting up the frame theorem statement...

Still writing proof...

I'm also double-checking that norm_num leaves no stray arithmetic in the function application itself, and that the numeral representation it produces for the literal matches what `exact h` expects for the integer type, so there's no mismatch from differing `OfNat` instances.

To sidestep potential atom-matching mismatches between linarith's instance representations, I'm considering avoiding the `rw [ha, hc, he]` approach entirely and instead using `simp only` with the hypotheses directly on the original goal, keeping all `col` references from the same elaboration source.

The numeral elaborates deterministically the same way across both occurrences, so that's consistent. I need linarith to pick up all the k-lemmas and t-equations using my own atom representations, and I'm checking that the rewrite with ha, hc, he correctly transforms the goal after applying hP. For the disjunction case, I'm considering using `first | exact absurd ⟨ha, hc, he⟩ hne | linarith` to close it, or alternatively handling hne more directly.

Now I'm thinking through file organization: I want to keep File 2 as the core, with File 3 handling ray invariance for K (importing File 2), and File 4 handling ℚ invariance like sgn_neg and sgn_odd_smul (importing File 1). Since a compile failure in one file would cost all its theorems, I'm leaning toward keeping these separate even though it means four files total, since combining File 3 and 4 risks losing both if either fails.

For the sgn_odd_smul proof specifically, I'm weighing whether to use split_ifs on both sides -- which generates many goals needing omega with product facts, moderate risk -- versus instantiating sgn_spec at the scaled triple and the original triple to derive the result more directly.

I can derive `sgn_spec'` for general `Vec3` by destructuring into components and applying `sgn_spec`, which then lets `sgn_odd_smul`/`sgn_neg` go through cleanly with omega since they avoid projection issues. That suggests packaging `sgn_spec` and `sgn_spec'` together in File 1, and I'm weighing whether the low-risk ℚ-invariance lemmas should join them there too, contingent on whether the `simp only` projection reduction actually holds up.

Since the host rejects a file on any compile error too, not just forbidden content, I want to balance risk carefully: File 1 gets the invariance lemmas since they're simple omega facts, File 2 holds the core Gaussian material, and File 3 covers Gaussian ray invariance. I'm now double-checking that omega can correctly linearize expressions like `k * a - k * b = k * (a - b)` by treating products like `k*a` and `k*b` as atoms.

Checking that sgn_spec applied to the scaled triple matches the goal through the same parity and mod-4 conditions, so omega should close it by linking the specs via the iff hypotheses. I'm now considering whether the exotic_neg and exotic_odd_smul corollaries follow as straightforward consequences of this result.

For the ray invariance statement, I'm noting that primitive integer representatives of a rational ray are unique up to sign, so I should just state invariance under negation and odd scalars and explain this in prose rather than formalizing the full uniqueness argument.

Now I'm setting up the plane obstruction file, starting with imports and the definition of a primitive vector as one not having all coordinates even.

Writing primitivity lemma and sign functions...

For the spec proof, I can unfold the definitions with simp and then split on all the if-conditions, closing everything with omega since split_ifs handles repeated conditions correctly. I'm now checking the remaining supporting lemmas—sgn_spec', mul_emod_four, odd_mul_emod_four, and sgn_frame—to make sure each holds up.

For the primitivity hypotheses I unfold IsPrimitive and the dot product, which turns each into a negated parity condition. Then for exotic_frame_function I just need explicit sign values at standard basis vectors, using decide as the primary tactic with norm_num as a fallback in case decide struggles.

Tracing through decide's evaluation, it needs to walk through the decidable instance chain, reducing sgn via its ite-based definition down to checking Int.emod values on the components, which should reduce cleanly for small inputs like (1,0,0).

I'm confirming that decide should work for checking IsPrimitive on simple cases, with norm_num as a fallback, and now I'm working through verifying the exotic function's value on the (1,0,0) input by rewriting with its definition.

Checking that the final norm_num call actually closes the arithmetic goal after the rewrite, confirming the result isn't quadratic, and verifying the sign/parity lemmas using Int.odd_iff and Int.even_iff to handle the ray case.

I'm also double-checking there's no namespace collision from opening RationalSphere inside RationalPlane, since Vec3 and the mod-2 lemmas need to resolve correctly, and moving on to the no_real_triangle theorem's parity statement.

With that file nailed down, I'm moving to File 3, BornGaussianFrameRays.lean, starting with lemmas about inner products under scalar multiplication for Gaussian vector frames.

I'm now proving that scaling a nonzero vector by a nonzero scalar preserves its nonzero property, by case-splitting on which component is nonzero and checking each case unfolds correctly with `rcases`.

Writing the theorem proof...

Still building the proof...

That checks out for the i3 case too. Now for the second branch I'm establishing positivity of the sum of norm squares by splitting on which coordinate is nonzero and using strict inequality from the nonvanishing norm square.

Then I'm defining orthogonal vectors w and u using conjugates and cross-product-like constructions to build the rest of the orthonormal frame.

Working out the nonzero-component proof...

Checking the defeq works out so `ne_of_gt hpos` gives `S ≠ 0`, or equivalently I could just use `hpos.ne'` for the same result.

Now I'm verifying that `nonZero_of_z hz` matches the expected goal by definitional unfolding. I'm also setting up several orthogonality lemmas showing various inner products of constructed vectors vanish, proving each by unfolding the inner product definition and closing with `ring`.

Verifying i3 reduces correctly with star_neg, star_star, and star_zero so ring can close it, confirming the required instances are satisfied. Then I'm assembling the final tuple with the three identities and moving into the uniqueness argument, starting with the nonzero witness.

The metavariable unification should work, but I'll be safe and provide explicit terms in the refine. The inner_smul_left rewrite chain reduces the goal to 0=0 by rfl, confirming frameFunction_smul works. Now I need to handle the case split on whether v.x and v.y are both zero, which requires decidability.

OK, so by_cases falls back to classical, which is fine since equality of Gaussian rationals is decidable anyway, and the axioms involved should be acceptable. I'm confirming the triangle theorem file is in place and considering whether to add a small lemma about the (1+i)-divisibility in the second file.

Since I don't have an actual Gaussian integer type, I'll just explain in prose that (a+bi)/(1+i) is a Gaussian integer exactly when a and b have the same parity, rather than trying to formalize it. Now I'm drafting the "what is proved" section and thinking about compile time for File 1—with 512 omega calls each handling around 45 hypotheses, including parity equalities, dot product equations, and negated conjunctions that introduce disjunctions.

Each contradictory conjunction splits into a disjunction of negations, and since the parities are already fixed in each case, most branches die off quickly, leaving omega to close them fast; factoring in the four-way splits from mul_emod_four and the nested specs, I'm estimating something like 0.2 to 1 second per call, putting total runtime in a reasonable range across all 512 cases.

Acceptable, though I wonder if I could trim the branching further; still, 512 cases is manageable. I'm also double-checking that the simp call correctly unfolds IsPrimitive and Vec3.dot given the opened namespace, which it should.

Verifying `u.dot v` resolves correctly to `Vec3.dot u v` through the opened namespace, and that the case splits reuse hypothesis names safely. I'm also confirming the signature of `Int.mul_emod` matches how the repo uses it in `mul_emod_four`, checking for any issue after the case split there.

I'm double-checking that rewriting `hx` and `hy` into `h` won't hit a "motive is not type correct" error since there are no dependent types involved, and that `x % 4` and `y % 4` still appear correctly in `h` after each rewrite. I'm also confirming the operator precedence so `x * y % 4` parses as `(x * y) % 4` given multiplication and modulo share precedence 70 and are left-associative.

I'm verifying `Int.mul_emod` matches this form, then sketching the proof of `odd_mul_emod_four` using a case split on `k % 4` being 1 or 3 derived via omega, and starting the `sgn_odd_smul` theorem for how scaling coordinates by an odd integer affects the sign function.

I need to be clear-eyed that we haven't settled options (A) or (B), but we've established three things: an exotic frame function over ℚ on all of ℚP², the fact that the parity route over ℚ(i) is closed since any frame function constant on parity classes of Gaussian-integer vectors must equal 1/3 there (with an explicit non-real triangle example), and the ray invariance lemmas needed to support this.

What's still missing is either a finer invariant than (1+i)-parity on Gaussian-integer rays that's compatible with all K-frames, or a Gleason-type rigidity proof over ℚ(i). Since restricting a K-frame function to real vectors always yields a ℚ-frame function, option (B) would require showing the exotic ℚ-function can't extend to K-rays, while (A) would follow if some exotic ℚ-function does extend — and I should note the extra constraint that non-real frames introduce through their unique real perpendicular ray.

Checking my Lean setup: IsFrameFunction is defined on vectors, but frameFunction_smul confirms it behaves as a function of rays, and exists_frame_completion guarantees every nonzero vector sits in some frame. For the ℚ case, every rational ray has a primitive integer representative with not all coordinates even, and two such representatives differ by an odd rational factor — I'm working through how this invariant interacts with that.

Still writing out the sign-invariance proof...

Finishing the proof by rewriting with the hypotheses to align both sides, then closing with the two sign equalities to conclude sgn u = sgn u'.

Actually simpler: just use `exact e1.symm.trans e2` to chain the two equalities directly, rather than doing the rewrite dance. Though I need to double check the structure types line up exactly between the anonymous constructor forms used in e1 and e2.

Confirmed Lean 4's structure eta handles the equality between the anonymous constructor and the structure instance, so the ray well-definedness proof should go through, and the rational cast for sgn into the exotic definition works automatically too. Now I'm carefully writing out the final Lean theorem statements and proofs.

Still writing the spec...

Finishing the remaining parity cases and proving the sign-zero equivalence by unfolding the definitions and splitting on conditionals, then checking whether simp's rewriting of the if-then-else could interfere with the equality goal.

I should double check that omega can actually decompose negated conjunctions into disjunctions internally, which is the key mechanism making this work — I recall its frontend handles `Not` over `And` by distributing via De Morgan's, so this should be fine.

For the exotic_not_quadratic case, I'm tracing through how norm_num should simplify the vector projections down to concrete integer casts, which should let it evaluate the polynomial identity directly.

I'm checking that none of the hypotheses collapse trivially after norm_num, then confirming linarith closes the False goal. Now I'm moving on to proving exotic_frame_function from sgn_frame, starting to set up that proof.

Now I'm proving sgn only takes values -1, 0, 1 via omega from the spec, then using that to show exotic always evaluates to 0, 1/3, or 2/3 by case splitting and using norm_num to verify each arithmetic case after substitution.

Now I'm moving on to proving that sgn equals zero whenever the vector is a ray.

I'm considering an optional example verifying that the exotic values sum to 1 for a specific frame, deciding it's not essential to include. Then I'm defining a Lean tactic macro `gauss_arith` that tries extensionality with simplification and norm_num first, falling back to other normalization tactics for verifying Gaussian-rational inner product identities.

Checking the `macro` needs no extra imports, and verifying the nonzero side goals resolve via `norm_num` after unfolding `gv` through the coercion chain down to a nonzero rational.

Now I'm defining the seven frame theorems, each asserting `IsFrame` for a different combination of `gv` triples covering the e1, e2, e3 directions with their sign variants.

Adding more frame theorems and verifying the orthogonality conditions for each, checking that the dot products between vectors work out to zero as required.

Continuing through remaining nonzero cases for tri_110, tri_101, and tri_011, confirming each representative value checks out, then I start building a class-value lookup table mapping each class label (k100, k010, etc.) to its corresponding column vector for the main theorem's 17 lemmas.

Still computing column parities...

I'm also sketching a generic helper lemma that would take the normalization hypotheses as parameters and derive the result automatically, rather than proving each case by hand.

Checking the rewrite step closes by rfl since the two expressions become syntactically identical after substitution, and confirming variable distinctness avoids collisions. Now I'm applying the same class_value pattern to compute each coefficient in the main theorem...

Still writing proof steps...

Refining the tactic to use `have := class_value ...` followed by `linarith` instead of rewriting, which should handle the underscore arguments for p, q, r inferred from the hypothesis correctly.

I'm double-checking that the anonymous constructor elaborates against `absurd`'s expected type correctly, since the argument type comes from `hne`'s negated proposition being processed during elaboration.

To be safe, I'll just construct the conjunction explicitly with `And.intro` nested calls rather than relying on the anonymous constructor to infer correctly. I also confirm variable naming doesn't collide between the two files, and that the `decide` tactic handles the integer modular arithmetic side conditions fine, including the negation case. Now I need to make sure the negation hypothesis in `class_value`'s statement matches the one from `ParityDetermined` exactly.

Rather than defining a separate predicate for the negation condition, I'll just inline it directly so `absurd` unifies without needing to unfold a definition. With that settled, I'm moving on to checking the third file's `frameFunction_smul` content and starting to think through the documentation for the `frame_tri_110` theorem, which is the key new result.

I considered adding a trivial lemma making explicit that the constant 1/3 corresponds to the Born rule value, but it's not essential enough to include formally — I'll just mention this connection in prose instead. Now I'm ready to write out the full prose argument.

Before finalizing, I'm double-checking compile details in File 1: verifying the import and namespace match the repo's module structure, confirming the `Vec3` constructor usage is consistent with existing definitions, and checking that the `sgn` function's decidability instance resolves correctly given its conjunction of parity conditions.

Looking at `sgn_frame` and `sgn_spec'`, I'm tracing through how `IsPrimitive` and `Vec3.dot` unfold under `simp only`, and confirming that destructuring `v` into its components and applying `sgn_spec` produces a definitionally equal goal.

For `mul_mod_four`, I'm checking that rewriting with `hx` and `hy` hypotheses correctly simplifies `h` since neither rewrite target overlaps unexpectedly, and that `omega` can close the resulting case where the product reduces to a literal zero mod four. I'm then moving into verifying the large case split over parity conditions on `u.a`, `u.b`, `u.c`.

I'm estimating worst-case branching for `omega`: for the pattern where each vector has one even component, each of three "odd-odd" product pairs per coordinate contributes a free binary choice for whether their difference is divisible by four, giving up to six such pairs and roughly 64 branches to consider in the worst case.

Combined with the specification branches that multiplies out to about 512 leaves, each resolving a small integer linear problem quickly, so total runtime across all cases should stay within a couple minutes. I'm also checking that the `≠` fact splitting in omega doesn't add real cost since infeasible branches get pruned immediately.

Now I'm reviewing the second file for issues, confirming the GVec structure and inner product definition use the right Star instance correctly.

I'm tracing through whether simp can unfold GVec.inner applied to gv via its equation lemma, and confirming integer casts like negative two to rational get simplified correctly by norm_num. Now I'm verifying the imaginary component arithmetic for one of the frame computations.

Checking the triangle inner products for tri_110 in GaussRat, computing each pairwise product by hand (star(1)·1 terms, etc.) and confirming they all cancel to zero as expected, including the (1-i)(-1-i) expansion giving -2 for the real part and 0 overall.

Moving to tri_101 with R, C, D: verifying R·C, R·D, and C·D all vanish through direct computation (1 - 2 + 1 = 0).

For tri_011 with Q, F, G: confirming Q·F and Q·G vanish, and working through F·G's expansion involving (1-i)(-1-i).

Continuing the checks: D, F, G, and S all verify correctly against their expected columns. Now I'm setting up the linear system from the t1, t4, and t5 constraints, substituting the computed column values for each term.

I'm checking that the numeral types elaborate correctly and tracing through the rewrite chain for `class_value`, confirming the `hP` rewrite correctly reduces the goal to matching `col` arguments via the hypotheses `h1`, `h2`, `h3`.

Now I'm moving to the third file to verify `exists_frame_completion`, checking that unfolding `GVec.inner` with `hx : v.x = 0` correctly simplifies the inner product expression for the basis vector case.

That second inner product also simplifies cleanly to zero, so File 3 checks out. I'm confirming the case split on v.x = 0 ∧ v.y = 0 works fine, and that the negation uses the standard not_and_or lemma from Mathlib's basic logic file, which is already available transitively.

In the contradiction branch, I derive v.x = 0 from the hypothesis via normSq_eq_zero_iff, contradicting hx, and separately use lt_of_le_of_ne with normSq_nonneg to establish the strict positivity needed there.

Then with linarith I combine normSq_nonneg for v.y to get the sum of norms strictly positive, and for the hz goal I rewrite using re_add and re_star_mul_self twice to unfold the real part of the sum into normSq v.x plus the real part of star v.y * v.y.

I'll confirm `normSq` is the right name, then construct the witness vectors satisfying the orthogonality and independence conditions, finishing with a scaling argument that preserves the inner product conditions under nonzero multiplication.

I'm also checking that `frameFunction_smul` handles the negation case since scaling by -1 already covers it, and there are no universe or implicit argument issues to worry about. For the sign parity lemma, I'm drafting `sgn_odd_smul` using the mod-2 hypothesis on k along with the integers a, b, c...

Still writing proof steps...

With the remaining algebraic identities established, I'm hoping omega can close the goal by combining these facts, though I'm second-guessing whether it will correctly treat terms like `k * a` and `k * (a - b)` as atoms rather than trying to distribute them.

I'm now checking the sgn_neg lemma, which should follow directly from symmetry via sgn_spec applied to both the negated and original triples, closed by omega.

Similarly, `exotic_neg` and `exotic_odd_smul` reduce to unfolding `exotic` and rewriting with `sgn_neg`, and the eq-of-odd-scalings lemmas follow the same pattern. I'm also noting the relevant module file paths for the final answer and need to double-check the axioms used.

Now I'm drafting the full Lean file, starting with imports, module doc comments, and the `BornFable.RationalPlane` namespace opening with `BornFable.RationalSphere`, then defining what it means for a vector to be odd-primitive.

I'm defining `IsPrimitive`, proving that any ray vector is primitive, and introducing a `pairSign` helper based on mod-4 differences, leading into a `sgn` function definition for vectors.

Still writing sgn function... then defining `exotic` as `(1 + sgn v) / 3`, but I notice there's a type coercion issue—I need to make sure `1` is treated as a rational number, not an integer.

Omega should handle sgn u as an atomic integer fine. I need to write out Files 2 and 3 fully, including the prose argument covering both parts, the mod-4 pair lemma, the classification, the Gaussian triangle construction, and clearly flagging the open status — stating plainly in "WHAT IS PROVED" that neither (A) nor (B) was established, with precise theorem names. I'm also considering a subtlety: pairwise orthogonal nonzero vectors in dimension 3 forming a frame.

One important detail I'm adding is a heartbeat limit — since the 512-case omega check could exceed Lean's default heartbeat budget, I'll set a higher `maxHeartbeats` option before the relevant theorem to avoid timeouts.

I'm also double-checking that unfolding `IsPrimitive` via `simp only` works correctly against the hypotheses, since definitions can be unfolded via their equation lemmas, though `unfold` at the hypotheses could be a safer alternative if `simp only` runs into trouble.

Verifying the nested `rcases` structure for splitting all nine sign cases with the chained `<;>` syntax before closing out with `omega`.

I'm confirming the lemma names `Int.even_iff` and `Int.odd_iff` are correct, and checking how the evenness/oddity components get supplied as a conjunction in the primitivity proof.

Then I verify `exotic_not_quadratic`'s norm_num call correctly rewrites each `exotic` literal before linarith closes it, and I move on to checking the `prim_*` lemmas proved by unfolding `IsPrimitive` and using `decide`.

