# L1, signed mixing, Hilbert structure: source map for the pictures

Read on 2026-11-03. No source was edited. This is a bounded reading of the supplied papers and selected foundations chapters, not a rebuild of their formal evidence.

**Later-source addendum:** the subsequently supplied finite-QM core explicitly resolves the two Paper 080 issues, and WDP strengthens the earlier alpha aggregation hypotheses. See [the newer source connections, section 6](09_finite_qm_and_wdp_source_connections.md#6-later-sources-resolve-earlier-review-findings). The earlier review remains a record of the specific older files examined.

## The most useful strip: a report can discard what the next move needs

Use two pairs of equal-length directed strokes. The first pair points the same way. The second pair points opposite ways. A report retaining only each length gives the same answer for both pairs. Apply the same head-to-tail construction: one pair extends, the other returns.

Candidate captions:

1. **“Same lengths. Different directions.”**
2. **“Join each pair the same way.”**
3. **“One advances. One returns.”**

This is a sign-only version of the report/mixing witness, not a physical experiment or derivation of a unique complex carrier. It can precede the naming of phase, Hilbert space, or complex amplitude. It demonstrates that a report discarding direction is insufficient for predicting that operation. The sign/direction model, report and addition rule are still supplied.

The information loss belongs to the chosen report, not to an l1 norm by itself. A signed vector equipped with an l1 norm still retains its signs and supports addition. The strip therefore challenges a direction-discarding description; it does not prove that all l1 geometry cannot represent mixing.

The precise two-output witness in the supplied [QM_122, §3.2 and §4](C:/.ana/coda_university/coda_research/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md:137) is:

\[
r(a,b)=(a^2,b^2),\quad M(a,b)=(a+b,a-b).
\]

Then

\[
r(1,1)=r(1,-1)=(1,1),
\]

but

\[
r(M(1,1))=(4,0),\qquad r(M(1,-1))=(0,4).
\]

No function F of the old report can satisfy r∘M=F∘r on both inputs. The next visible result requires information the old report discarded. This is the same conceptual hinge as the alpha paper's failure of contextual congruence.

Important scale boundary: this integer mixing matrix satisfies MᵀM=2I. It is not itself a norm-preserving quantum time evolution. A normalized Hadamard uses an additional 1/√2 factor in a host admitting that scalar. The diagram should call this an addition/mixing construction, not silently identify it with unitary dynamics. The square report is declared here, not proved to be uniquely Born's rule.

## What each source supplies

| Source | Usable result | Extra structure that stays explicit |
|---|---|---|
| Alpha finite obstruction paper | Allowed reference changes, residual classes, closure tests, invariant detector pairing | Carrier, comparison/repair class, cochain maps and observer gauge |
| [QM_020: conditional Hilbert lift](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/foundations/qm_020_born_normalization_and_conditional_hilbert_lift.md) | Nonnegative weights normalize directly; square-root encoding reproduces that same normalized profile | Phases, Hilbert representation and Born-uniqueness assumptions; normalization alone does not supply them |
| [QM_003 redirect and retained boundary](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/foundations/qm_003_residual_density_calculus_l1_l2_boundary.md) | Diagonal density embedding and information-loss examples | A chosen residual representative: minimizing l1 norm need not select a unique coordinatewise density |
| Supplied QM_122 | Same-report pairs can separate after mixing, already over integers; finite permutation isometries under a supplied orthonormal pairing | Coefficient pack, pairing, report, mixing rule; complex field, circle, unique Born law, tensor uniqueness, channels and continuous time remain named extras |
| [QM_062 selector](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/foundations/qm_062_the_u1_selector.md) | A declared quarter-turn J with J²=−I gives the familiar two-component multiplication rule | Real scalar extension and continuous reversible pairing-preserving transport; finite Gaussian-integer algebra is not by itself a completed complex Hilbert theory |
| Supplied QM_080 | Obstruction geometry and bounded dual witnesses inside a chosen operator/trace-distance representation | Hilbert space, Hermitian operators, channels, operational metric selection; this is not the construction of the Hilbert host |
| [QM_035 Hamiltonian admission](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/foundations/qm_035_hamiltonian_generator_admission.md) | A reserved boundary slot | The body is still an internal stub with open obligations, despite a RELEASED banner above it. It does not supply the missing generator derivation. |

## The quarter-turn is a useful later picture, with a precise boundary

In QM_062, J is the supplied two-component move J(x,y)=(-y,x), so two applications reverse both components and four return them. Combining a copy of the identity move with a copy of J gives

\[
(aI+bJ)(cI+dJ)=(ac-bd)I+(ad+bc)J.
\]

The multiplication law can be taught by repeated moves before naming complex numbers. Over integers this constructs Gaussian-integer algebra; over an admitted real scalar plane it represents complex multiplication. It does not show that nature uniquely uses this host. Continuous time, a preferred generator, and a physical interpretation remain additional obligations. The quarter-turn itself must be given or independently derived; displaying it is not a uniqueness proof.

## Holonomy: a relevant passage, but not a free identification

[QM_061, §6](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/foundations/qm_061_interference_as_the_non_l1_resource.md:155) contains the requested “holonomy bridge.” The firm algebraic statement is that an exact phase cochain telescopes to zero around a closed walk. The connection from phase transport to interference is marked interpretive/imported in that chapter.

Do not draw loop holonomy and detected intensity as the same quantity. Zero relative phase can yield constructive interference; intensity also depends on the supplied magnitudes, mixing and readout. To turn the holonomy wording into a derivation, specify those maps and prove the relationship. This chapter may help locate the remembered argument, but it is not a Noether theorem.

## Version custody

The user-described older foundations folder is not a uniform frozen older copy. Its QM_122 file identifies itself as v0.2.0, consolidated 2026-10-17; the supplied coda-university file identifies itself as v0.1.16, dated 2026-08-20. They have different bodies and scope descriptions. Folder location alone does not determine which result supersedes another.

- Supplied QM_122 SHA-256: `f4ef85f405ba846ddf92fd6bbd8fc7aaa86d658c4678b4b841989f2cb97ee004`.
- Foundations QM_122 SHA-256: `b9fbb3fe96d51eeffa65d4b5fb4bab27ab1a390b0b10a8e11058112f39683938`.

The supplied QM_122 abstract should be read with §3.1's hypothesis of an orthonormal report basis. An arbitrary inner product is not preserved by every report permutation: a swap fails for unequal diagonal Gram weights. The body names the required supplied structure; the abstract's shorter phrasing should not be promoted to the stronger arbitrary-pairing claim.

## What this changes about the teaching plan

The [independent Paper 080 review](08_adversary_quantum_sources_verbatim.md) is retained in full. It finds the two copies' mathematical bodies unchanged and identifies two specific issues for later source repair: (1) the dual balance law for trace-zero repairs is a condition modulo scalar identity, and centered witness matrices need not literally balance; (2) contractivity under the stated all-dimensions, all-CPTP-channel family, together with homogeneity, already forces trace-norm shape up to a common scale. The scalar normalization remains unselected. The reviewer supplies explicit arguments and a three-dimensional balance counterexample. No source repair or Lean verification was performed.

The strongest source-led entry is now:

**comparison → allowed reference changes → invariant remainder → a report loses direction → the same operation exposes that loss → repeated turning → explicitly supplied dynamics.**

This provides material for revising the opening of the classical v3 sheets. Those sheets have already been reviewed as a conditional construction, and remain preserved as such. Neither these reading notes nor their captions silently upgrade them to a derivation from the papers. Born, Everett and Bell still need their own constructions; they cannot be obtained merely by renaming a leftover.
