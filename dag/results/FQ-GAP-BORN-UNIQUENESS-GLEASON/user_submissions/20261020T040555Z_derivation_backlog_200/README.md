# Derivation backlog: 200 explicit targets

AuthorityEffect: None. This is a research agenda, not 200 newly established results or 200 newly discovered open problems.

Targets 1-140 cover sign-problem representations and the estate families. Targets 141-200 cover the connected scalar, Born, channel, tensor, dynamics, Hilbert, Bell, contextuality, MUB and reconstruction obligations. Some elementary items already have written arguments in the earlier review; independent proof or formalization remains useful.

Kinds: R = proof/counterexample exercise; F = concrete family derivation or exact finite replay; C = conditional theorem/import with declared hypotheses; O = larger research objective.

Start by hand with 1, 2, 11, 15, 17, 18, 21, 22, 61, 62. The first unprotected family sequence is 81-90. These are work suggestions, not execution authorization.

[Machine-readable backlog](derivation_backlog.json), [source inventory](source_inventory.json), [validation](validation.json), [provenance](provenance.json), [seal](manifest.json).

For each result supply the precise statement and assumptions, proof or failed step, and evidence status. Preserve originals separately from review. Collect genuine reusable operation signatures and laws where applicable. Code replay does not replace a general proof; an operation record does not replace operad laws.

## 1. Signed measures and honest phase rates

1. **[R] Phase normalization.** Derive q=abs(w)/W, s=w/abs(w), and E_q s=Z/W for integrable w with Z>0; handle its zero set.

2. **[R] Exact positivity criterion.** Prove Z/W=1 iff w>=0 almost everywhere, assuming positive real Z and finite W.

3. **[R] Complex phase versus real sign.** Derive complex reweighting and exhibit failure of replacing the phase by sign(Re w).

4. **[R] Finite versus limiting severity.** Prove g_N=-log(d_N)/V_N tending to g gives d_N=exp(-V_N*g+o(V_N)).

5. **[R] Zero-rate counterexample.** Prove d_N=2^(-floor(sqrt(N))) has zero exponential rate and superpolynomial inverse-square phase penalty.

6. **[R] Path-dependent asymptotics.** Construct different limiting phase rates along different beta,N paths and state a sufficient path-independence condition.

7. **[R] Polynomial phase bound.** Derive the denominator guarantee from d>=1/P(N,beta), separating remaining observable and algorithm costs.

8. **[F] Complete configuration support.** Prove a finite enumeration exhausts the declared model support; distinguish selected fields from an ensemble.

9. **[R] Continuous configuration identities.** Extend reweighting and blocking to continuous measures under explicit absolute-integrability hypotheses.

10. **[F] Actual target identification.** Specify each L0 model's Hamiltonian or transfer, sector, beta, scalar convention, and observables; prove what is calculated.

## 2. Exact preservation, blocking and operads

Suggested prerequisites: 1, 2, 10.

11. **[R] Inserted-numerator preservation.** Prove Z'=cZ and N'_O=cN_O with c>0 preserve normalized expectations.

12. **[R] Composition of exact maps.** Prove identity and composition for representation changes, scalar factors and observable maps.

13. **[R] Unitary observable transport.** For H'=UHU*, derive the required transformed observables and partition/numerator identities.

14. **[F] HS prefactor accounting.** Derive every global and field-dependent scalar for one exact HS change.

15. **[R] Moment-vector pushforward.** Prove blockwise summation of (w,n_1,...,n_m) preserves partition and every insertion.

16. **[R] Moment operad laws.** Prove arity-zero, identity, associativity and permutation laws for componentwise moment addition.

17. **[R] Zero-weight decoding.** Prove ordinary estimators exist on a zero-weight block exactly when all its inserted numerators vanish.

18. **[R] Absolute-weight contraction.** Prove W'<=W under blocking and characterize equality by common phase in each block.

19. **[R] Phase versus observable variance.** Construct exact blocking that improves average phase but worsens a declared estimator's variance.

20. **[R] Product representations.** Derive tensor weights/local insertions and compatibility with blocking and normalization.

## 3. Observable statistics and confidence

Suggested prerequisites: 1, 3, 11.

21. **[R] Exact denominator variance.** For M iid unit phases of mean d>0, prove relative phase variance (1-d^2)/(M*d^2).

22. **[R] Finite-sample ratio confidence.** For abs(f)<=B, bound additive error of bar(sf)/bar(s) in d,B,epsilon,eta, including small denominators.

23. **[R] Residual covariance formula.** Under a multivariate CLT, derive ratio asymptotic covariance from s(f-mu), including complex observables.

24. **[R] CLT versus MSE.** Give sufficient uniform-integrability conditions or an example separating ratio CLT from MSE convergence.

25. **[R] Identity observable exception.** Prove f=1 yields an exact ratio whenever the sampled denominator is nonzero.

26. **[R] Positive rare-event variance.** Derive mean 1 and variance 2^N-1 for q=(2^-N,1-2^-N), f=(2^N,0), without claiming universal hardness.

27. **[R] Denominator failure control.** Bound P(abs(bar(s))<d/2) and define honest treatment of zero denominators.

28. **[R] Finite-sample ratio bias.** Bound ratio bias under explicit denominator and moment assumptions; separate physical approximation bias.

29. **[R] Control variates.** Derive an optimal control-variate coefficient with a known expectation and its residual-variance guarantee.

30. **[R] Initialization error.** Decompose nonstationary sampling error into initialization, dependence, finite-sample and ratio terms.

## 4. Cost, mixing and complexity accounting

Suggested prerequisites: 21, 22, 23.

31. **[R] Exact arithmetic costs.** Bound operation counts and rational numerator/denominator bit growth for a chosen determinant algorithm.

32. **[R] Confidence-to-cost theorem.** Combine an estimator bound with update, estimator, setup and precision costs under a declared input encoding.

33. **[R] Spectral-gap covariance bound.** For a stationary reversible chain with nontrivial eigenvalue moduli <=rho<1, bound integrated residual covariance.

34. **[R] Autocorrelation versus mixing.** Construct a fast observable on a chain with a slow unobserved mode; refute global mixing from one measured correlation.

35. **[R] Balance versus rapid mixing.** Construct reversible irreducible finite chain families with bottlenecks and slow mixing.

36. **[R] Certified burn-in.** Derive burn-in from a declared gap, conductance or coupling certificate and initial law.

37. **[R] Vanishing determinants.** Prove support and insertion rules at zero determinants; distinguish inverse estimators from cofactor formulations.

38. **[R] Construction and normalization cost.** Price computation and precision of a normalization factor or basis rather than treating closed form as efficiency.

39. **[R] Positive spectral existence.** Derive positive eigenbasis weights for finite Hermitian H and identify the uncontrolled construction/estimator costs.

40. **[R] Accuracy conventions.** Separate additive from relative error near zero observable means and state a valid zero-mean convention.

## 5. Finite Fock-space foundations and free controls

Suggested prerequisites: 10.

41. **[R] Creation/annihilation signs.** Derive (-1)^(occupied earlier modes) from the ordered occupation basis.

42. **[R] Finite CAR proof.** Prove anticommutation, nilpotency and occupation-projector identities in the finite Fock construction.

43. **[F] Hamiltonian reconstruction.** Derive Hubbard hopping and diagonal entries from CAR, orbital order, interaction and chemical-potential conventions.

44. **[R] Sector dimensions.** Prove dimension binomial(L,N_up)*binomial(L,N_down) and number conservation.

45. **[F] Exact coefficient field.** Prove field membership of model and transfer entries; list extensions needed by spectral or normalization operations.

46. **[R] Thermal trace positivity.** Prove Tr(exp(-beta H))>0 for finite Hermitian H and finite real beta.

47. **[F] Free triangle analytics.** Derive the two-identical-fermion triangle spectrum and partition under a fixed hopping convention.

48. **[F] Free ring control.** Derive one-particle/canonical spectra and thermal trace, then compare to the finite-step transfer.

49. **[R] Canonical/grand-canonical relation.** Prove the fugacity generating identity when [H,N]=0; distinguish ensemble observables.

50. **[R] Closed-path enumeration cost.** Count closed paths in a transfer trace and distinguish dense matrix evaluation from explicit path enumeration.

## 6. Meron-chain derivations

Suggested prerequisites: 41, 42, 50.

51. **[F] Meron bond transfer.** Exponentiate the two-site spinless interacting Hamiltonian and derive its four-by-four transfer with CAR signs.

52. **[F] Meron normalization.** Derive the q^(-1/4) factor per plaquette and its total checkerboard power.

53. **[F] Meron breakup identity.** Prove vertical weight 1 and horizontal weight (q-1)/2 reproduce all local normalized entries for q>=1.

54. **[F] Cluster reconstruction.** Prove graph components are exactly admissible clusters, including periodic spacetime identifications.

55. **[F] Orientation sign character.** Derive s_g(f)=(-1)^(m_g dot f) from reconstructed occupations rather than assigned labels.

56. **[F] Orbit completeness.** Prove all 2^k flips are distinct, admissible, equal-magnitude and exhaustive.

57. **[R] Zero-meron positivity.** Sum the Boolean sign character and prove exactly which orbits have nonnegative partition contribution.

58. **[R] Observable Fourier selection.** Derive the signed numerator from the observable's Boolean Fourier coefficient at the meron character.

59. **[F] Squared staggered estimator.** Derive zero-meron and two-meron squared-occupation insertion formulas from cluster sizes.

60. **[F] Observable-carrying zero-weight orbit.** Exhibit a real Meron orbit with zero partition and nonzero squared-observable numerator; retain both moment records.

## 7. Hubbard local identities and normalization

Suggested prerequisites: 43, 45, 49.

61. **[F] Repulsive HS identity.** Prove the centered spin-channel local identity on all four occupations, including common scalar C.

62. **[F] Attractive HS identity.** Prove the charge-channel identity and derive h^(-sum s) after spin factorization.

63. **[R] Interaction conventions.** Derive shifted mu and constant relating U*n_up*n_down to the centered interaction, including the partition factor.

64. **[R] Palindromic kinetic matrix.** Prove reality, symmetry, positive definiteness and determinant one for the declared rational bond palindrome.

65. **[R] Bipartite inverse symmetry.** Derive eta*K*eta=K^(-1) from bipartite bond structure and the exact palindrome schedule.

66. **[F] Half-filled determinant pairing.** Track transposes/time order at z=1 and derive the positive up/down determinant relation.

67. **[F] Attractive square positivity.** Prove spin-matrix equality and nonnegative real square times the full charge-channel scalar.

68. **[F] Full HS reconstruction.** Prove all-field sums reproduce the declared finite Fock transfer with complete normalization.

69. **[F] Particle-number insertion.** Derive N_num=(z/M)*dZ_tilde/dz for the M-slice number-conserving transfer.

70. **[F] Singular-field insertion formula.** Derive product-rule/cofactor numerators valid at zero field determinants and compare to inverse-based estimators.

## 8. Protected determinant sectors and exact controls

Suggested prerequisites: 61, 62, 64, 65.

71. **[R] Generalized eigenvalue pairing.** Prove antiunitary commutation bijects generalized eigenspaces at lambda and conjugate(lambda).

72. **[R] Even real multiplicity.** For T^2=-I, prove real generalized eigenspaces have even complex dimension without diagonalizability.

73. **[R] Non-Hermitian Kramers positivity.** Combine conjugate pairs and even real multiplicities to prove det(I+B)>=0, including eigenvalue -1.

74. **[R] Reality is insufficient.** Give a real B with negative det(I+B), explaining the failure of square-+1 conjugation protection.

75. **[R] Equal versus conjugate factors.** Show conjugate determinants give absolute squares, while equal complex determinants can square negatively.

76. **[F] Protected ring replay.** Independently reconstruct all fields and number insertions for L=4,M=2,r=3/2,h=2,z=1.

77. **[F] Attractive triangle replay.** Independently reconstruct all fields at L=3,M=2,r=3/2,h=2,z=3/2, including charge prefactors.

78. **[F] Two-site reconstruction control.** Match auxiliary and independent Fock transfer sums for both interaction signs and a number insertion.

79. **[F] Finite Meron control.** Match orbit and occupation-transfer partition/squared-observable numerators at L=4,M=2,q=3.

80. **[F] Scaling-driver scope.** Identify omitted scalars and insertions in the determinant-only lane and prove which reported quantities remain valid.

## 9. Doped repulsive ring: a ten-stage program

Suggested prerequisites: 66, 68, 69, 75.

81. **[F] Doped-ring negative witness.** Independently rebuild mask 15721 at L=4,M=4,r=2,h=8,z=2 and certify both spin determinant signs.

82. **[F] Full-ring phase information.** Separate the singleton witness from complete signed/absolute sums; bound or compute the latter before claiming a full mean phase.

83. **[F] Physical ring parameters.** Recover delta_tau*t, delta_tau*abs(U), delta_tau*shifted_mu and the finite-product target from r,h,z.

84. **[F] Broken half-filled protection.** Identify the precise determinant-pairing step that fails at z=2 without inferring all fields are negative.

85. **[F] Nontrivial ring observable.** Derive a total-number or double-occupancy numerator with all derivative and normalization terms.

86. **[F] Field symmetry tests.** Determine actions of spin flip, translation and reflection on ring weights/insertions; prove which are actually sign reversing.

87. **[F] Exact ring blocks.** Construct blocks or a group action preserving every declared insertion, including zero-weight fibres.

88. **[F] Strict finite ring improvement.** Prove W'<W or d'>d for a candidate on its declared full support and include construction cost.

89. **[F] Ring estimator comparison.** Bound before/after residual variance, estimator cost and dependence instead of comparing phase alone.

90. **[O] Growing doped-ring family.** Give a uniform exact construction with proved cost and phase bounds; retain finite-instance status if no extension is established.

## 10. Frustrated repulsive triangle: a ten-stage program

Suggested prerequisites: 61, 64, 68, 75.

91. **[F] Triangle negative witness.** Independently verify mask 1281 at L=3,M=4,r=2,h=8,z=1 and both determinant signs.

92. **[F] Frustration versus doping.** Identify separately the failed protection hypotheses for triangle z=1 and bipartite ring z=2.

93. **[R] Bipartite sign criterion.** Prove a sublattice sign reversing every hopping bond exists iff the graph is bipartite; apply to a triangle.

94. **[R] Gauge versus flux change.** Prove local phase gauges preserve loop flux and determine when flux threading changes the physical model.

95. **[F] Triangle gauge classification.** Classify admitted orbital/occupation diagonal gauges and restrict any obstruction to that class.

96. **[F] Attractive triangle comparison.** Derive charge-channel positivity on the same geometry and show why geometry alone does not decide positivity.

97. **[F] Alternative exact triangle decouplings.** Derive two representations of the same transfer, transporting scalar factors and insertions before phase comparison.

98. **[F] Triangle orbit moments.** Compute symmetry-orbit sums and test absolute-weight contraction without losing insertion moments.

99. **[F] Triangle basis/observable transport.** Derive transformed interactions and insertions for a proposed unitary basis change and price their evaluation.

100. **[O] Growing frustrated family.** Construct a uniform exact reduction or a narrowly specified no-go theorem for a growing triangle-based interacting family.

## 11. Occupation gauges and configuration-space topology

Suggested prerequisites: 41, 43.

101. **[R] Configuration gauge criterion.** Prove a diagonal +/-1 gauge makes all off-diagonal entries nonpositive iff every configuration-cycle edge-sign product is positive.

102. **[R] Signed-cover correctness.** Prove reachability (v,+1) to (v,-1) iff a negative closed walk exists; otherwise reconstruct a consistent gauge.

103. **[F] Ring negative configuration cycle.** Reconstruct the recorded four-site CAR cycle and prove diagonal U cannot change its edge-sign obstruction.

104. **[F] Physical-tree exchange obstruction.** Rebuild the star's negative many-particle cycle and explain why a physical tree can have exchange loops.

105. **[F] Open-chain gauge control.** Derive a consistent gauge for the declared open nearest-neighbor chain and orbital order.

106. **[F] Canonical-sector embedding.** Prove how number-sector projection changes full-Fock partition and insertion comparisons.

107. **[R] Nonnegative Euler conditions.** For stoquastic H, derive step-size/shift conditions making I-delta*H entrywise nonnegative and track target changes.

108. **[R] Stoquastic Gibbs positivity.** Prove exp(-beta*H) is entrywise nonnegative for real Hermitian H with nonpositive off-diagonals and beta>=0.

109. **[F] Reconcile representation-specific signs.** Explain why an occupation gauge obstruction does not contradict auxiliary positivity, tracking ensemble differences explicitly.

110. **[C] Precise restricted hardness.** Specify transformation class, encoding and accuracy before importing hardness; do not infer fermionic-HS hardness from qubit claims.

## 12. Finite-step transfer errors and interacting ladder

Suggested prerequisites: 43, 46.

111. **[R] Euler approximation bound.** Derive an explicit norm bound for (I-beta*H/M)^M-exp(-beta*H) with stated hypotheses and M dependence.

112. **[F] Discretization-induced signs.** Give a concrete finite Euler example whose signs or normalization differ from the Gibbs representation.

113. **[R] Positive Euler trace condition.** Derive a spectral step-size condition making the Euler matrix positive definite and its power trace positive.

114. **[R] Energy-shift accounting.** Prove Gibbs energy shifts give a scalar factor while finite Euler shifts need not do so.

115. **[R] Lie-Trotter error.** Derive an explicit finite bounded-operator product error controlled by commutators and time.

116. **[R] Strang error.** Derive a symmetric-product bound with declared nested-commutator constants rather than only an asymptotic order.

117. **[F] Rational transfer/coupling dictionary.** Identify exact local exponentials represented by r,h,z and the noncommuting global product still approximated.

118. **[R] Observable approximation bound.** Bound normalized-expectation error from partition/numerator errors using a positive denominator lower bound.

119. **[C] Finite-lattice locality.** Prove a Lieb-Robinson bound for declared finite-range interaction norms and certify numerical constant enclosures.

120. **[F] Interacting ladder admission.** For L0-08 reconstruct H, Euler transfer and an insertion; certify denominator admissibility or retain the failed parameter choice.

## 13. CT-AUX correctness before scaling

Suggested prerequisites: 43, 49.

121. **[F] CT-AUX expansion identity.** Derive the exact shifted-Hubbard expansion used by the sampler, including K-dependent normalization.

122. **[F] Thermal Green function.** Derive both imaginary-time branches, equal-time convention and antiperiodicity from the one-particle spectrum.

123. **[F] Scalar/vectorized kernel parity.** Prove agreement with the derived Green function at negative eigenvalues and time boundaries, not merely agreement between implementations.

124. **[F] Vertex integration measure.** Derive order factorials, site/time/spin measures and proposal-volume factors in CT-AUX weights.

125. **[F] Insertion/removal balance.** Derive detailed-balance acceptance ratios from the actual target and proposal, including zero weights.

126. **[F] Fast update correctness.** Prove Schur-complement/rank-one determinant and inverse updates, with invertibility and fallback conditions.

127. **[F] Numerical drift control.** Derive residual/interval certificates for determinant signs and inverse updates; distinguish exact identities from floating stabilization.

128. **[C] Expansion-tail control.** If an order cutoff is used, bound omitted weight from operator norms; otherwise prove absence of a hidden cutoff.

129. **[F] Physical CT-AUX observables.** Derive particle-number and double-occupancy estimators from the expansion, including singular configurations.

130. **[F] CT-AUX correctness gate.** Establish stationary-law correctness and independent small-model agreement before any phase, speedup or mixing scaling claim.

## 14. GIN/CDT custody, streaming and obstruction scope

Suggested prerequisites: 15, 17, 21, 125.

131. **[R] Complete cancellation consequence.** Prove a fixed-point-free sign-reversing equal-magnitude involution on full support gives Z=0; identify needed unpaired sectors.

132. **[F] GIN query soundness.** Prove every returned partner satisfies the full involution and weight constraints, not just shared index keys.

133. **[F] Sliding-window preservation.** Derive unmatched-moment bookkeeping needed when configurations are evicted from a streaming window.

134. **[R] Unique pair ownership.** Prove insertion/deletion/query rules count every configuration and cancellation exactly once.

135. **[F] Streaming normalization.** Prove the quotiented estimator targets the original quantity; identify any changed window distribution instead.

136. **[F] Synthetic generator boundary.** Trace GIN configuration generation and prove exactly which indexing claims, rather than Gibbs-measure claims, it supports.

137. **[F] Complex CDT determinant phase.** Derive determinant/abs(determinant) and quantify the error from substituting sign(Re determinant).

138. **[F] Simplicial Dirac adjoints.** Prove kinetic adjoint relations and track mass, mu, orientation and boundary effects on the full matrix.

139. **[C] Topological obstruction admission.** For one concrete family establish the gapped phase, invariants and locality/design hypotheses before importing an intrinsic-sign theorem.

140. **[R] Homotopy scope.** Construct continuous signed-to-positive weights crossing zero while preserving moments; state hypotheses protecting a chosen invariant.

## 15. Scalar fields, phases and completion

Suggested prerequisites: 10.

141. **[R] Rational effect homogeneity.** Prove p(qA)=q*p(A) on E=[0,u] from partial additivity, checking that every evaluated effect remains in E.

142. **[R] Effect monotonicity.** Derive p(A)<=p(B) from A<=B, nonnegative effect values and partial additivity.

143. **[C] Order-unit extension.** Under declared order-unit and decomposition assumptions, extend an effect state uniquely and rational-linearly to its generated space.

144. **[C] Real-place selection.** Specify the archimedean embedding/order and determine which coherent root choices fix weight comparisons; distinguish this from mere orientation.

145. **[R] Torsion phase skeleton.** From phase subgroups of every finite order, derive characteristic zero, the directed root union and its abstract Q/Z structure.

146. **[C] Cyclotomic rational-weight witnesses.** Derive square roots of nonnegative rationals in the cyclotomic union, distinguishing Gauss-sum proof from an imported theorem.

147. **[C] Finite algebraic-witness ceiling.** State the exact equation/inequality language and prove the algebraic-to-complex witness transfer using a pinned real-closed-field result.

148. **[F] Coefficient closure audit.** For one actual construction prove closure under inverses, required roots, spectral factors and tensor operations; declare extensions.

149. **[C] Declared scalar completion.** Construct and characterize completion from a specified place and metric instead of inferring it from finitely many witnesses.

150. **[C] Local-tomography scalar test.** For declared real/complex/quaternionic matrix and composite models derive dimensions and test the proposed multiplicativity requirement.

## 16. Born-rule uniqueness and its missing premises

Suggested prerequisites: 141, 142, 143, 149.

151. **[C] Real effect homogeneity.** On the full real effect interval, use positivity and rational squeezing; never evaluate absent algebraic-carrier effects.

152. **[C] Full-effect linear extension.** Derive a positive real-linear functional from normalized additive finite-Hermitian effect probabilities with explicit effect availability.

153. **[R] Trace duality.** Prove each real-linear Hermitian-matrix functional has a unique Hermitian rho with L(A)=Tr(rho*A).

154. **[R] Density positivity and trace.** Derive rho>=0 and Tr(rho)=1 from nonnegative normalized effect probabilities, including dimension one.

155. **[C] Reconstructed coefficient field.** Determine whether rho lies in the original field or its completion from the probability codomain and input assumptions.

156. **[R] Qubit projective exception.** Construct a continuous normalized nonquadratic qubit frame function; distinguish projective from full-effect additivity.

157. **[C] Exact Gleason interface.** Pin the full-complex dimension-at-least-three theorem's hypotheses and separate that import from a finite-carrier proof.

158. **[C] Dense-carrier extension theorem.** Assume uniform continuity and frame density, then prove extension to all complex frames before applying a full-space theorem.

159. **[R] Algebraic frame density.** Prove algebraic complex orthonormal frames approximate arbitrary complex frames, tracking exact roots and normalization.

160. **[C] Born missing-premise discharge.** For the actual carrier prove the required extension/regularity principle or supply a countermodel; finite agreement is insufficient.

## 17. Channels, tensor products and available systems

Suggested prerequisites: 148, 153, 154.

161. **[R] Kraus normalization.** Prove complete positivity and trace preservation from sum K_j* K_j=I, including rectangular dimensions.

162. **[C] Choi factorization field.** Over a declared real-closed field and complexification derive Gram/Kraus factors, tracking rank and scalar closure.

163. **[R] Finite Choi criterion.** Prove CP iff the convention-fixed Choi matrix is PSD and derive its trace-preserving partial-trace constraint.

164. **[R] Positive versus CP.** Prove transpose is positive and trace preserving but not CP using an exact Bell partial-transpose witness.

165. **[C] Available-ancilla Stinespring.** Construct the dilation/isometry and unitary extension while stating ancillary dimensions and physical availability.

166. **[C] Rational Kraus descent.** Determine when Q(i) channel data admit Q(i) Kraus factors; distinguish Gram factorization from individual square roots.

167. **[R] POVM/instrument nonuniqueness.** Exhibit distinct CP instruments for the same effects and state what selects one state update.

168. **[R] Kraus representation coherence.** Prove isometric mixing invariance and the converse with correct padding/rank/partial-isometry hypotheses.

169. **[C] Physical tensor selection.** Separate the tensor universal property from operational positivity, local tomography and system-availability assumptions.

170. **[C] Object completeness.** Show why qubit tensor powers alone miss dimensions and prove how available projection faces recover all finite sizes.

## 18. Continuous time and Hilbert-space limits

Suggested prerequisites: 145, 149.

171. **[R] Generator aliasing.** Construct different Hermitian logarithms with the same sampled unitary, including branch freedom in degenerate eigenspaces.

172. **[R] Dyadic continuity gap.** Construct compatible dyadic roots not continuous at zero, or derive an exact continuity criterion; compatibility alone does not suffice.

173. **[C] Dyadic-to-real evolution.** Extend a dyadic-time unitary homomorphism continuous at zero to real time, then invoke Stone with its stated hypotheses.

174. **[C] Band-limited logarithm uniqueness.** Prove uniqueness in a declared half-open spectral band of width 2pi/tau and handle the endpoint.

175. **[R] Parallelogram and polarization.** Derive the complex inner product and characterize compatibility with a previously declared quadratic form.

176. **[F] Graph-growth compatibility.** Determine separately when zero extension commutes with incidence and adjoint divergence; include boundary counterexamples.

177. **[R] Subdivision isometry.** Derive weights and refinement maps for function versus density cochains and prove the correct additivity requirements.

178. **[C] Stone-space Hilbert limit.** Construct measure and dense locally constant functions from countable refinements; require atomlessness before a Cantor conclusion.

179. **[C] Galerkin resolvents.** From a closed positive form and dense stage form core prove projected resolvent convergence without false operator-domain assumptions.

180. **[C] Evolution convergence.** Under the correct self-adjoint/resolvent hypotheses prove strong unitary convergence, tracking projections and time uniformity.

## 19. Bell, contextuality and MUB targets

Suggested prerequisites: 141, 148.

181. **[R] Bell inequalities from a joint table.** Derive all CHSH inequalities and marginal consistency from a nonnegative joint law on four binary variables.

182. **[C] Fine converse.** From valid binary pair marginals, consistency and the full inequality system construct a nonnegative joint table.

183. **[R] Rational joint witnesses.** Prove rational feasible Bell marginal data admit a rational joint table with exactly checkable entries.

184. **[R] Exact Bell separators.** Derive a rational dual/Farkas witness for an infeasible joint-extension LP.

185. **[C] CHSH supremum versus attainment.** For an explicit field and state/measurement class determine the supremum, attainment and effects of scalar extension.

186. **[R] Contextuality obstruction scope.** Prove the sound obstruction-to-no-global-section implication for a declared cover and test unsupported converses.

187. **[F] Coefficient-sensitive contextuality.** Compute one cover with integer and cyclotomic coefficients and prove the operational meaning of the difference.

188. **[R] Exact MUB equations.** Derive orthonormality and unbiasedness polynomial constraints, scalar requirements and allowed symmetries.

189. **[R] Sound MUB enclosure pruning.** Prove residual bounds and pruning invariants that preserve every feasible assignment, including seams and repeated-box occupancy.

190. **[O] Global d=6 MUB target.** Construct four exact bases or a rigorously covered global exclusion certificate; local rejected boxes are insufficient.

## 20. Optimization, reconstruction and verified transport

Suggested prerequisites: 11, 12, 16.

191. **[R] Exact cochain optimization duality.** Derive rational primal/dual certificates for a declared finite L1 boundary problem and prove the optimum check.

192. **[R] Local closure versus global exactness.** Exhibit d1*r=0 with r outside im(d0), and prove the required homology-sensitive classifier distinction.

193. **[C] Physical effect availability.** After effect/trace representation, prove or explicitly declare which mathematical effects the theory physically realizes.

194. **[C] Reconstruction product hypotheses.** State Jordan/composite assumptions and prove the product/trace identities before importing any classification result.

195. **[F] Certified entropy enclosures.** For an algebraic density matrix derive rational entropy bounds with a proved remainder, zero-eigenvalue handling and fixed log base.

196. **[C] Controlled CCR limit.** Prove finite trace obstruction and specify embeddings, scaling and domains for a genuine Weyl/CCR continuum limit.

197. **[C] Controlled continuum equation.** Derive one specified lattice-to-Schrodinger or Dirac limit with explicit errors, geometry, dispersion and boundary assumptions.

198. **[R] Collected-operation law proofs.** Prove typed domains, admissibility, identity and composition; distinguish an operation record from a verified operad.

199. **[F] Independent native/formal transport.** Implement exact Rust/Python instances and formalize the actual Lean statement, binding sources, fixtures and rejected mutations.

200. **[O] Integrated conditional reconstruction.** Assemble a coherent QM reconstruction/equivalence with every imported assumption and remaining obligation explicit.
