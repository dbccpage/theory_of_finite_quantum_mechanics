# Corrected reconstruction contract

Status: conditional dependency statement, NOT A PROVED RECONSTRUCTION OF THE FINITE-QM PROGRAM. Source imports are explicit and not kernel-checked here.

## RC-1. Choose the target and its object scope

For normalized systems use positive integers n, state cones Herm_n(C)_+, normalized states Tr rho=1, effects 0<=E<=I, and explicitly specified transformations (for full deterministic quantum theory, all CPTP maps). Tensor dimension is nm, unit is 1. Physical local reversibles are unitary conjugations. Transpose is an affine state symmetry but is not a CP local transformation for n>=2.

Either reconstruct onto the realized dimension set S, or add/prove object completeness. Tensor closure and a qubit alone permit S={2^k}. One sufficient object-completeness principle is that each exposed quantum face is represented as a system: once 2^k-dimensional systems exist, every rank-n face in some 2^k-dimensional system realizes D(C^n). This principle is not in A0--A4 as written.

## RC-2. Single-system Jordan classification

Match the operational framework of Barnum--Mueller--Ududec, including closed allowed effect cones, effect pullback by allowed transformations, mixture/coarse-graining structure and the relevant transformation closure. Under operational spectrality and ordered-frame strong symmetry, their Proposition 1 derives no-restriction. With this match, import Barnum--Hilgert's finite-dimensional classification: the state space is a simple EJA state space or a simplex. Alternatively, use geometric frames and explicitly keep physical effect availability separate. Do not switch between these conventions mid-proof.

No derivation of these postulates from the finite packet data is supplied by citing the classification theorem.

## RC-3. Complex selection needs a compatible composite

For each system A and the declared qubit Q, verify the precise Jordan-model composite assumptions in Barnum--Wilce. These include product tests/effects and product states with factorized probabilities, independent local-process extensions, local tomography and the appropriate self-dual/HSD structure. If using their Lemma 8 to obtain factorized trace forms, prove that its input is a Jordan composite in their sense.

A clear algebraic checkpoint is the Hanche-Olsen unit-leg identities on J_A tensor Herm_2(C):

    (a tensor 1) bullet (b tensor v)=(a bullet b) tensor v,
    (1 tensor v) bullet (a tensor w)=a tensor (v bullet w).

They imply that J_A is the self-adjoint part of a complex C*-algebra. This may initially allow direct sums. With the strong-symmetry classification and the classical/qubit composite exclusion (whose dimension and simplex-face argument is in review.md), one obtains simple complex matrix state spaces or the trivial system. The equation dim V_AB=dim V_A dim V_B alone is not a substitute for this checkpoint.

## RC-4. State/effect duality

Given an affine isomorphism phi_A:Omega_A->D(C^n), extend it to a normalization-preserving order isomorphism on unnormalized real spaces. An affine effect e pulls back to a unique linear functional on Herm_n(C), hence uniquely to E via Tr(E rho). Evaluating on every rank-one projector gives 0<=E<=I iff e takes values in [0,1]. A normalized measurement has sum E_i=I. To conclude surjectivity of physically allowed POVMs, invoke the matched operational saturation and measurement-closure result; do not infer availability from positivity alone.

This establishes the Born pairing in the conditional operational representation, not a new primitive derivation of probabilities or a projective frame-function uniqueness theorem.

## RC-5. Dynamics and process completeness

A reversible physical map is an affine state automorphism, but every affine automorphism need not have been admitted as a physical map. To identify the allowed reversible group with PU(n), supply the correct closed-subgroup/full-frame-transitivity result and verify its premises, or state universal unitary control as an additional import. The antiunitary branch is excluded by the standard entangled-ancilla positivity test.

For full deterministic arrows, prove both directions: every allowed local arrow is CPTP; every CPTP arrow is realizable. The first follows from positivity on all standard matrix ancillas and normalization. The second may be derived from universal unitary control on appropriate composites, ancillary preparations, discarding and dilation, but requires its own argument and operational closure. Instruments require similarly explicit CP-outcome and sum-TP availability. No uniqueness of state update follows from a POVM.

Continuous unitary one-parameter groups give Hamiltonian commutators. H and H+cI induce the same density evolution; a physical choice of dynamics/time remains declared data.

## RC-6. Tensor and categorical conclusion

Use the full compatible composite theorem, or prove that the identifications satisfy

    phi_AB(omega tensor sigma)=phi_A(omega) tensor phi_B(sigma)

for all product states. Product states span the locally tomographic unnormalized space, so this fixes the linear composite map on every state. Prove its positivity, inverse positivity and the corresponding effect/process transport, not just a dimension match. Intertwine the unit, swap and associator diagrams from the coherent operational framework; equality on spanning product states is a useful verification method.

With all these obligations discharged, obtain a strong symmetric monoidal equivalence onto the realized quantum subtheory. Fullness on effects and transformations requires the saturation/availability results above. Essential surjectivity onto all positive integer dimensions requires RC-1 object completeness. An equivalence of operationally identified systems is generally the right invariant claim; a literal isomorphism of arbitrary system labels is stronger.

This contract makes the required work explicit. It does not assert that these are independent new axioms: some may follow from a fully specified version of the original framework and the cited theorems. It rejects the claim that the short proposal has already discharged them all.
