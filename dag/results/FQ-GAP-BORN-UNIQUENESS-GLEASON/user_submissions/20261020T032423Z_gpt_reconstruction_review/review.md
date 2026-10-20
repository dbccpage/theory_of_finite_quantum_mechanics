# Verdict

Keep the Jordan reconstruction route and the conditional trace-pairing explanation. Reject the claimed full monoidal isomorphism as proved by the present argument. In particular, A0--A4 do not force every finite Hilbert-space dimension to occur as a system. The original finite-QM reconstruction row remains OPEN IN THIS PROJECT.

## 1. What the literature actually supplies

[Barnum--Hilgert, Theorem 1.1](https://arxiv.org/html/1904.03753) classifies finite-dimensional spectral, strongly symmetric compact convex state spaces as simple EJA state spaces or simplices. This already includes the simple-or-classical conclusion. Their proof uses classification of regular convex bodies through polar representations; calling Koecher--Vinberg alone the engine omits the difficult implication to the needed cone structure. Affine frame symmetry does not itself identify the physically allowed transformation set.

The no-restriction issue should not be invented as a separate obstruction without checking definitions. [Barnum--Mueller--Ududec, Proposition 1](https://arxiv.org/html/1403.4147) derives all effects from the two operational postulates under its effect/measurement/transformation closure framework. Barnum--Hilgert explicitly discusses this restricted-effects extension in its framework section. Therefore either match those operational assumptions and import the saturation theorem, or distinguish geometric frames from operational frames. The manuscript's residual claim that effects remain merely embedded is too weak if it intends the complete cited operational framework. Arbitrary restriction of effects need not preserve its A1 and A2.

[Barnum--Wilce, Proposition 1 and its composite definitions](https://arxiv.org/html/1202.4513) require more than a vector-space dimension equality: Jordan/HSD model structure, a suitable composite with product tests and independent local processes, and factorizable self-duality. Their Lemma 8 can derive trace-form factorization for the appropriate Jordan composites, so this need not be an extra independent axiom if its premises are verified. Hanche-Olsen's unit-leg Jordan identities are explicit compatibility conditions. The short A0 does not specify all of these data. Their categorical result also assumes the stated dagger/HSD framework; it is not a theorem about arbitrary bilinear product maps.

These are source-checked theorem imports, not fresh proofs or Lean certificates in this bundle.

## 2. Decisive counterexample to the target as stated

Let T_2 be ordinary complex quantum theory restricted to system dimensions S={2^k:k>=0}, with all density matrices, all POVMs, all CPTP maps between those systems, standard unitary reversibles, and the usual tensor product. It is a coherent monoidal subtheory since 2^j 2^k=2^(j+k).

A0 holds on every system and composite. A1 is matrix spectral decomposition. A2 is transitivity on ordered orthogonal pure-state frames, by extending frames to orthonormal bases and applying a unitary. A3 is standard local tomography: the real unnormalized space has dimension n². A4 is the qubit at n=2.

Nevertheless T_2 has no qutrit system. Every system dimension is 1 or even, so none is 3. Nor can an affine state isomorphism hide one: a qutrit state space has affine dimension 8, while D(C^(2^k)) has affine dimension 4^k-1, never 8. Thus the theory is not essentially surjective onto the target with all positive integer dimensions. An encoded qutrit face in a two-qubit system is not a qutrit object unless a face/subsystem-closure principle is supplied. This is a general written countermodel, not an inference from a finite search.

The displayed family phi_A can at best identify the realized systems unless system availability and essential surjectivity are addressed. A monoidal equivalence onto a realized subtheory is distinct from an isomorphism with the entire stated target. Use n>=1 for normalized systems; n=0 has no trace-one state and needs a separate empty/zero-system convention.

## 3. Dimension arithmetic: useful diagnostics, incomplete reconstruction

K is the real dimension of the unnormalized ordered vector space, not the affine dimension of normalized states. For the standard matrix families,

    K_R(n)=n(n+1)/2, K_C(n)=n², K_H(n)=n(2n-1).

The standard real composite has dimension excess nm(n-1)(m-1)/4 over the product, while the standard quaternionic one has defect -2nm(n-1)(m-1). These refute local tomography for those standard tensor candidates when n,m>1. But K_classical(n)=n is also multiplicative. A3 alone neither gives capacity multiplication nor a universal function K depending only on capacity.

A dimension-only alternative even passes qubit-composite counts: a rank-two spin factor with unnormalized dimension 7 times a qubit has dimension 28 and product rank 4, matching Herm_4(H). No such compatible GPT composite is constructed or asserted here; the coincidence demonstrates why dimension counts alone cannot replace the tensor-compatibility theorem.

The classical-system exclusion can be retained with explicit premises. For a classical capacity-m system and a qubit, product tests give capacity at least 2m and local tomography gives dimension 4m. For m>=2, the smallest dimension of a simple real matrix EJA of rank at least 2m is m(2m+1)>4m; the complex and quaternionic minima are larger. Spin factors and the exceptional EJA have insufficient rank. A classical composite would be a finite simplex. The inverse image of a fixed pure classical marginal is a face; its qubit marginal maps onto the entire qubit ball by the product-state assumption. An affine image of a simplex face is a polytope, which the ball is not. Thus it too is excluded. The product-test and marginal assumptions are needed for this argument.

'No composites' for spin or octonionic systems is too broad. The conclusion concerns the specified locally tomographic compatible composite class. We do not classify every Jordan tensor construction here.

## 4. Reversibility, time evolution and channels

The affine automorphisms of a complex matrix state space include unitary conjugation and conjugation followed by transpose. That describes geometry, not the physical reversible group of complex QM with arbitrary entangled ancillas. A local transpose fails positivity on half of a Bell state: its partial transpose has eigenvalues (-1/2,1/2,1/2,1/2). Unitary conjugation of this counterexample preserves the negative eigenvalue, excluding every local antiunitary-conjugation branch under standard complete positivity. The submission's target initially permits unitary reversibles but its equivalence definition later admits antiunitaries; those categories must be aligned.

Strong symmetry supplies a transitive allowed subgroup. Identifying the whole PU(n) requires an actual subgroup theorem with its closedness/continuity premises matched; an orbit-dimension number alone is not that proof. The cited operational framework imposes topological closure, but short A0 does not. We do not claim a proper closed transitive full-frame subgroup exists; the step is a missing proof/import, not a fabricated counterexample.

Once continuous one-parameter unitary dynamics is available, finite-dimensional generators give the von Neumann equation. The density evolution determines H only up to an added scalar identity. It does not select a physical Hamiltonian, time scale, hbar convention, or continuous interpolation from discrete samples.

Ancilla-stable positivity with all complex matrix ancillas is the CP criterion. This establishes a necessary admissibility condition for local processes. It does not by that sentence establish that every CP/TP map is an allowed process. A full transformation reconstruction must prove availability, for example from a stated dilation and operational-closure argument. The target must say whether it contains all CPTP arrows, CP instruments, or only the listed reversible maps.

A POVM specifies outcome probabilities, not a unique state update. Our exact two-outcome instruments share effects P0,P1; one dephases and the other resets both outcomes to |0>. Their postmeasurement states differ. This is an additional boundary if the intended GPT includes instruments.

## 5. Effects, Born pairing and tensor coherence

After a full affine state isomorphism into complex density matrices, every mathematical affine effect is uniquely Tr(E rho), with 0<=E<=I. This finite-dimensional duality is a valid point and requires no projective Gleason theorem at this stage. The normalization of a measurement gives sum E_i=I. Physical availability of those effects is supplied by the correctly matched saturation theorem or an explicitly stated alternative assumption.

Dimension equality does not by itself identify the positive composite cone or its product embedding. In the usual Hermitian tensor vector space, the separable cone, quantum PSD cone and maximal product-positive cone have the same ambient dimension and differ in order. A quantum reconstruction needs the cited compatibility theorem or an independent equivalent proof. In particular, a Jordan tensor product is not the rule (a tensor v) bullet (b tensor w)=(a bullet b) tensor (v bullet w); the Pauli counterexample in the controls refutes that naive rule.

Once compatible identifications on product states and local tomography are proved, linear extension makes the composite identification unique relative to them. Coherent units, associators and swaps must still be supplied by the actual monoidal framework and shown to be intertwined. Single-system affine bijections carrying structures 'into' target structures do not constitute a full monoidal isomorphism by themselves.

## 6. Independence and the physical boundary

The bullet-point 'independence audit' is motivation, not a proof of logical independence of the axioms. A2 transports arbitrary ordered distinguishable frames, which is stronger than merely permuting outcomes within one fixed measurement. Stokes-polarization geometry can motivate a ball model but does not by itself establish a quantum two-level operational system, its full effects or composites. A0 already imports compact real convex state spaces and real mixture coefficients; it is not obtained here from finite data. All of A0--A4 need an explicit boundary realization in the finite-QM program, even if some are derived from others or imported through reconstruction results.

Contextuality statements require dimensions, measurement classes and composite availability. Kochen--Specker and a two-qubit CHSH value are distinct scoped consequences, not interchangeable claims that every spin or Jordan model is contextual and has no composites. The table is retained only as an informal motivation, not a proved classification of rival theories. No blanket assertion about all infinite-dimensional reconstruction routes is imported.

The correct residual is a dependency ledger: match the operational framework, discharge the composite/compatibility and dynamics arguments, fix the realized-object scope, and prove the finite-QM boundary hypotheses. It is not 'only A2 remains'.
