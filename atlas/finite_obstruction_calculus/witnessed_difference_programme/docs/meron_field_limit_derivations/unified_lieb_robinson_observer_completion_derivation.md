# Locality, sufficient observation, and faithful recovery

Corrected derivation, 2026-10-05. AuthorityEffect: None.
The submitted draft is preserved byte for byte in
[`docs/source_archive/locality_and_smearing/source_manifest.json`](../source_archive/locality_and_smearing/source_manifest.json) in `docs/source_archive/locality_and_smearing/`.
Its statements are not inherited as proved propositions.

## 1. The precise bridge

There are two different restrictions: information discarded by an observer,
and operations excluded by physical locality. They meet at a declared readout
map; neither restriction supplies the missing physical adapter for the other.
The theorem below gives exact finite recovery conditions, then bounds the
conditioning of a physical readout under explicit locality hypotheses.
It does not identify a positive error upper bound with an error floor.

Fix a nonempty finite set E of admitted errors in V = F₂ⁿ, a repair subspace
B ≤ V, and a linear syndrome map Q:V→F₂ᵐ with B ≤ ker Q. Repair success
means e+r∈B. An error in B has zero quotient obstruction; an error outside B
does not become zero by selecting another representative. These are
algebraic declarations. An actual decoder operation realizing r must still
be supplied to use this model for a device or a PFP repair.

**Theorem L1 (sharp admitted-error recovery).** A syndrome-only decoder
r:Q(E)→V succeeds for every e∈E if and only if

\[
 Qe=Qf\quad\Longrightarrow\quad e+f\in B \qquad(e,f\in E).
\]

**Proof.** If r succeeds, add e+r(Qe)∈B and f+r(Qf)∈B; the common repair
cancels. Conversely select one admitted representative e_s from each nonempty
fiber Q⁻¹(s)∩E and set r(s)=e_s. The hypothesis gives e+e_s∈B.
Both selection and verification terminate by finite enumeration. A positive
certificate lists every used syndrome and its repair. A negative certificate
is a pair e,f in the same fiber with e+f∉B. The checker replays the supplied
repair or pair; it does not replace an incorrect decoder with a new one. ∎

This is not a left inverse of Q, RQ=id_V. That equation is impossible for a
noninjective Q. Recovery is only required on E, modulo the declared B.
For a full Hamming ball E={e:wt(e)≤t}, define
d=min{wt(v):v∈ker Q\B}, with d=∞ when this set is empty. Then L1 is
equivalent to 2t<d: a forbidden vector of weight at most 2t splits into two
vectors of weight at most t, and the sum of any two admitted errors has
weight at most 2t. For a restricted admitted family, L1 is the criterion;
the distance inequality is sufficient but need not be necessary.

**Theorem L2 (minimum linear observer completion).** Additional binary rows
must annihilate B. A row suite C permits recovery precisely when every
forbidden difference

\[
 F=\{e+f:e,f\in E,\ Qe=Qf,\ e+f\notin B\}
\]

has a nonzero value under at least one row of C. Thus its minimum size is
the minimum finite hitting suite among the rows in Bᵖᵉʳᵖ. There is an
exhaustive terminating procedure: enumerate row subsets by increasing size,
discard rows that do not annihilate B, and test all forbidden differences.
A lower certificate must cover every smaller admitted suite with a retained
collision. Merely displaying a successful suite is only an upper bound.

If E is itself a linear subspace containing B, the minimum is
dim(ker(Q|E)/B). Necessity follows from injectivity of the added map on that
quotient. Sufficiency follows by choosing dual coordinate functionals there,
extending them to E/B and then V/B. This dimension formula is not asserted
for an arbitrary restricted E.

The retained example has n=3, Q(x,y,z)=x+y, B={000,110}, E=F₂³.
The original syndrome collides on 000 and 001. One extra row z produces
(x+y,z), with repair (0,x+y,z). Zero extra rows fail and one succeeds, so
the exact minimum is one. `LocalObservationCompletion.lean` proves this
concrete decoder separately from its abstract fiber criterion.

## 2. Conditional physical locality theorem

Let a finite tensor-product quantum system have a declared region R. Let
ρ,σ be density matrices. Let O be a Hermitian evolved readout and O_R a
Hermitian operator supported on the **joint** region R. Assume

\[
 \operatorname{Tr}_{R^c}\rho=\operatorname{Tr}_{R^c}\sigma,
 \qquad \|O-O_R\|_\infty\le\beta.
\]

**Theorem L3 (local readout bound).**

\[
 |\operatorname{Tr}((\rho-\sigma)O)|
 \le\|\rho-\sigma\|_1\,\beta\le2\beta.
\]

**Proof.** Equal joint marginals give
Tr((ρ−σ)O_R)=0. Subtract this identity and apply trace/operator norm
duality. The trace distance bound follows from positivity and unit trace:
∥ρ−σ∥₁≤∥ρ∥₁+∥σ∥₁=2. ∎

With approximate marginals at trace-norm distance d_R, the bound is instead
d_R∥O_R∥∞+∥ρ−σ∥₁β. No correlation-decay assumption is needed for equal
joint marginals. Equal **single-site** marginals do not give equal joint
marginals on a multi-site region.

Here is an explicit way to obtain O_R from finite commutator estimates.
For a qubit y outside R let E_y be the average of conjugation by I,X,Y,Z
on y. It is a norm contraction and removes dependence on that qubit.
Composing these maps gives E_R, the conditional expectation onto operators
supported on R. If ∥[O,P_y]∥∞≤η_y for each of the three nonidentity
Paulis, then

\[
 \|O-E_R O\|_\infty\le\tfrac34\sum_{y\notin R}\eta_y.
\]

Indeed O−E_yO is the average of the three differences O−P_yOP_y;
each has the commutator norm. A telescoping sum over y, with preceding
conditional expectations contractive, proves the claim. Higher local
dimensions use a declared finite unitary twirl and its corresponding average.

An imported Lieb–Robinson bound can therefore provide a β of the form
C_R exp[−μ(r−v|t|)] after the spatial tail has actually been summed.
C_R includes the geometry, operator norm, and interaction hypotheses.
This derivation does not infer such a bound from the name of a Hamiltonian.
The standard locality results are imported from
[Bravyi–Hastings–Verstraete](https://arxiv.org/abs/quant-ph/0603121) and
[Nachtergaele–Sims–Young](https://arxiv.org/abs/1810.02428).
The finite twirl and the readout deduction above are self-contained.

The equality Tr([ρ,O])=0 holds for every pair of finite square matrices.
It is **not** an expression for Tr((ρ−σ)O). Confusing these two expressions
would wrongly erase every readout difference.

## 3. Conditioning and noisy refusal

Let z=R(ρ) and z'=R(σ) be readout vectors, in a declared norm. Suppose
∥z−z'∥≤η, a decoder F satisfies ∥F(z)−F(z')∥≤κ∥z−z'∥, and its endpoint
errors against the desired targets a,b are at most α.

**Theorem L4.** If ∥a−b∥=δ, then

\[
 \delta\le2\alpha+\kappa\eta.
\]

For exact endpoint decoding and η≤2β, κ must satisfy κ≥δ/(2β) when β>0.
If β=0 and δ>2α, no such decoder exists. This is an obstruction to stable
reconstruction, not a lower bound on the physical error of the device.
For multiple channels their common β and vector norm must be declared;
one cannot silently use a scalar bound for an arbitrary-dimensional norm.

**Proof.** Insert F(z),F(z') between a and b and apply the triangle
inequality. Combining the locality bound uses κ≥0. ∎

If two readouts have distance at most 2ε in a normed real space, their closed
noise balls of radius ε intersect at the midpoint. At the common report,
any reconstruction has error at least δ/2 at one endpoint. Thus β≤ε is
a sufficient indistinguishability condition in the scalar bound of L3.
It is not a necessary physical horizon, nor evidence that the system has
intrinsic error ε. The Lean proof establishes the common-report contradiction
for exact rational targets and errors.

## 4. Retained carrier counterexamples

**Bell marginals.** The rational density matrices of
(|00⟩±|11⟩)/√2 have identical individual marginals I/2. The observable
X⊗X has expectations +1 and −1. Keeping current single-site outputs loses
the joint readout. Setting O_R=Z⊗I and O=O_R+εX⊗X gives readout difference
2ε and tail norm ε: the bound in L3 is sharp on these finite data.
The executable checker checks density positivity, exact marginal equality,
the submitted norm certificates, and the actual readout separately.

**Gauge cycle.** For oriented edges a→b→c→a and α=(0,1,0), the gradient
is (1,−1,0) if dα(edge)=α(head)−α(tail), or (−1,1,0) for the opposite
convention. Its L¹ norm is two, and its circulation is zero. Every gauge
gradient telescopes around a cycle. Translation of the admitted repair set
therefore preserves the quotient obstruction and the infimal repair cost.
It cannot extinguish a nonzero cycle class. Changing the carrier, weights,
or admissible repairs is a different operation requiring a preservation map.

**Star exchange.** Four physical sites 0,1,2,3 form a star centered at 0.
The two-particle configuration loop is
{1,2}→{0,2}→{2,3}→{0,3}→{1,3}→{0,1}→{1,2}.
Its legal directed hops are 1→0,0→3,2→0,0→1,3→0,0→2.
In ascending CAR occupation order their signs are 1,−1,1,1,−1,−1,
with product −1. Six signs all equal to −1 would instead multiply to +1.
The exchange loop lives in the configuration graph, not the physical site
tree. The CAR/exterior-power carrier construction must be declared; it is
not an inclusion of physical site cycles into configuration cycles.

**Upper envelopes.** An inequality 0≤error≤positive_bound does not imply
error>0. Infimizing an upper envelope does not change this fact. A lower
obstruction requires a collision, a separated pair, or another independently
checked witness of the missing capability.

## 5. WDP, CODA and LGGR scope

L1 separates local syndrome satisfaction from global admitted-error recovery,
the LGGR distinction. L2 specifies what an adequate observer must retain.
The quotient ker Q/B connects the raw defect to CODA's repair equivalence.
L3–L4 give a physical readout restriction **only when a real carrier/readout
adapter and locality hypotheses are supplied**. WDP binds those source,
observer, repair and evaluation maps, instead of letting a name substitute
for them. Proposal, independent checking and authorization remain separate.

There is no claim here that MUB6 is resolved, that a Majorana device realizes
these declarations, that every noise model is correctable, or that a physical
error floor follows from a Lieb–Robinson upper bound. The standard quantum
error-correction setting is imported separately from
[Knill–Laflamme](https://arxiv.org/abs/quant-ph/9604034); L1 is a finite
binary admitted-error theorem and is not a proof of that full operator theorem.

## 6. Evidence boundary

The full written theorem uses ordinary finite linear algebra, trace norms,
and conditional imported analytic locality bounds. Python replays finite
binary recovery, exact rational matrices, the star exchange, and rejection
controls. `LocalObservationCompletion.lean` proves the fiber criterion,
the concrete binary decoder, rational locality/conditioning consequences,
and cycle/sign identities. It does not formalize the imported analytic
Lieb–Robinson theorem or verify the Python program. The reference package
and source-bound receipts are described in
[`derivation_evidence.md`](../derivation_evidence.md).
