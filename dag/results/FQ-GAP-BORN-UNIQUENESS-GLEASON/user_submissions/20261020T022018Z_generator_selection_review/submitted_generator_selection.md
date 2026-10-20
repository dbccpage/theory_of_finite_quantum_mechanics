Step 6 is the one rung where the discrete data genuinely underdetermine the continuous object, so it pays to separate what is forced from what is chosen.

**Forced.** Given a Hilbert space and a group homomorphism t ↦ U(t) into the unitaries that is merely weakly measurable, von Neumann gives strong continuity for free (separable ℋ), and Stone gives a unique self-adjoint H with U(t) = e^{−itH}. Norm continuity is too strong (it forces H bounded); weak measurability is enough. So once you *have* the continuous group, the generator is a theorem, not a selection.

**Not forced.** If step 5 only delivers U = U(τ), you are solving e^{−iτH} = U. Existence is free (every unitary has a skew-adjoint log). Uniqueness fails by exactly the kernel of exp: H and H + (2π/τ)·N agree stroboscopically for any integer-valued function N of H. The spectrum is known only modulo 2π/τ — a Floquet/Brillouin zone — which is Nyquist aliasing in the literal sense. Every branch is a strongly continuous group through the same sample points, so strong continuity does not discriminate between them.

Qubit, τ = 1, U = Z: H = π|1⟩⟨1| and H = −π|1⟩⟨1| both work, as does π|1⟩⟨1| + 2π·(any integer diagonal). The discrete data cannot even fix the sense of rotation.

Contrast case worth having in the row: the Markov embedding problem. Not every stochastic matrix is e^{τQ} for a rate matrix Q (Kingman), and when it is, Q can be non-unique (Cuthbert). Unitary: always embeddable, never unique. Stochastic: sometimes embeddable, sometimes non-unique. Same aliasing, different obstruction.

"Multiple interpolations" also splits into two ambiguity classes the row currently conflates:

- Among groups — the kernel of exp; countable per spectral component; killed by a branch choice.
- Among arbitrary paths — uncountable; killed only by imposing the group law U(s+t) = U(s)U(t), which is itself a commitment (memorylessness) the ladder should state explicitly, not inherit.

**Selection data that actually fixes H** — the "justify the generator" clause has to name one:

- Band limit: spec(H) ⊂ (−π/τ, π/τ]. The principal log; equivalent to a Nyquist assumption on the dynamics.
- Energy bounded below plus minimality. Physically natural; still fails if the spectral width exceeds 2π/τ.
- Refinement: a consistent family U(τ/2ⁿ) with U(τ/2ⁿ)² = U(τ/2ⁿ⁻¹). The generator is the inverse limit; aliasing is removed by halving rather than by fiat. This is the only option that stays inside "discrete evolution."
- Locality: on a lattice, demand H quasi-local. The generic Floquet log is nonlocal, so locality selects — when a local branch exists at all.
- Symmetry: H in the commutant of the given symmetry group. Restricts the branch per sector, rarely to one.

Pithy version: strong continuity buys the generator *given* the group; it buys nothing toward choosing the group from its samples. The justification in the row is a selection datum, not a continuity argument.

Tightened cell, if useful:

> Impose the group law and a topology (strong continuity suffices; norm continuity over-constrains). Stone/Hille–Yosida then yields H uniquely. From a discrete U(τ) alone, H is fixed only modulo 2π/τ on each spectral component (aliasing); the continuous group is a branch choice and must be justified by a declared selection datum — band limit, refinement family, locality, or minimal energy.
