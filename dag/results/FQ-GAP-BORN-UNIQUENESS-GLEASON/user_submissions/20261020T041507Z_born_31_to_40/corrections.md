# General arguments completing the corrections

Status: written mathematical arguments, not Lean kernel certificates. The exact original attachments are under submission/.

## BR-31: algebra identity and non-isometric merge

The outcome-tagged algebra is A_e=direct_sum_i M_(e_i), represented block diagonally in M_E. Its trace is the sum of block traces. Continuation substitution acts as identity on untouched components and the stated CP instrument on the selected component. Its identity law is the identity of A_e. The submitted CPTP extension to all M_E first pinches the blocks: even for an identity continuation it sends an inter-block matrix unit E_ab to zero. Thus it is not the identity on M_E when there is more than one block.

To merge equal-colour slots i,j, let L_i=J'_merged J_i*, L_j=J'_merged J_j*, and L_k=J'_k J_k* on untouched slots. Then M(Y)=sum_k L_k Y L_k* is TP since sum L_k*L_k=I_E. On tagged states it adds the two same-size blocks. It is not generally an isometry: merging two scalar tags maps both orthogonal pure tags to the same scalar state and decreases dimension from 2 to 1. This is tag-forgetting, not reversible relabeling.

## BR-32: the general adjoint identity

For any K-linear Phi, (Tr_out C_Phi)_(jk)=Tr Phi(E_jk)=conjugate(Phi*(I)_(jk)). Hence Tr_out C_Phi=conjugate(Phi*(I)). Only when Phi*(I) is Hermitian can this be rewritten Phi*(I)=(Tr_out C_Phi)^T. In particular the scalar functional Tr(A X) has Choi A^T and adjoint value A*. For effects A*=A, exactly recovering the submitted correction. Identity normalization is invariant. The older BR-21--30 corrected note is already sealed and is not rewritten; this general-map qualification is recorded here for successors.

## BR-33: kernel inclusion can hold while CP extension fails

Use outer slots K_1=(3/5)I and K_2=(4/5)Z, with continuations Id and Ad_Z. The merged outer map is F=(9/25)Id+(16/25)Ad_Z. It preserves diagonal entries and multiplies off-diagonals by -7/25, so it is bijective: its kernel is zero. Merge-after-continuations is Id. Therefore any common merge-first map must be Theta=F^(-1), multiplying off-diagonals by -25/7. On the plus-state G, the vector (1,1) has quadratic value -18/7 under Theta(G). Thus Theta is not even positive. Kernel inclusion holds, but the CP factorization is impossible.

The rational Choi PSD-feasibility system is the exact condition in the rational carrier. A numerical real SDP feasibility report is not automatically a rational solution certificate. In the surjective case a rational right inverse and the kernel check determine the unique candidate, after which BR-35 decides its rational Choi positivity. Trace preservation follows from surjectivity and the given normalization, as in the submission.

## BR-34: finite convex hull versus closure

Let P=(I+(S_x+Z)/sqrt(2))/2. It is a rank-one orthogonal projection with an irrational real entry. The two-outcome trace instrument with effects P,I-P is an extreme point of the full complex effect/Choi tuple set. Indeed if P=sum_t lambda_t A_t with all positive lambda_t, 0<=A_t<=I and sum lambda_t=1, a vector in ker(P) has zero nonnegative quadratic form under every A_t, so every A_t kills ker(P). Likewise every I-A_t kills ran(P). Hence every A_t=P. It follows that this tuple cannot be a finite real convex combination of rational tuples. The submitted finite-real-convex-hull assertion is false.

The appropriate closure statement can be proved. Stack any finite complex normalized Kraus family into an N-by-d isometry and complete its columns to a complex unitary. Rational unitaries are dense: for Hermitian H over Q(i), the Cayley matrix (I-iH)(I+iH)^(-1) is a rational unitary; rational Hermitian matrices approximate arbitrary Hermitian matrices; and complex unitaries without eigenvalue -1 are dense and have such Cayley coordinates. Approximate the completed unitary, retain its first d columns, and split rows into the original Kraus blocks. These rational Kraus families remain exactly normalized and their Choi tuples converge to the original tuple. Thus the norm closure, and closed real convex hull, of rational instrument tuples equals the ambient complex set for the fixed profile. Finite convex hull and closure must not be conflated.

Partial substitution is affine in BOTH normalized CP-instrument arguments. In the continuation argument, substituted slots are linear in the continuation and untouched slots equal sum_t lambda_t Phi_j=Phi_j. General bilinearity without normalized weights is a different assertion. An irrational state can still have rational statistics for some instruments, for instance probability 1 for the identity outcome; only a guarantee of universal rationality is absent.

## BR-35: algorithm proof versus executable guard scope

The recursive pivot argument is valid on Hermitian Q(i) matrices, including the 0-by-0 case. A negative diagonal gives an immediate witness. In a zero-diagonal nonzero block, v=e_j-conjugate(a_jk)e_k yields -2 abs(a_jk)^2. For a positive pivot, the Schur complement is a rational Hermitian matrix of smaller size; congruence lifts either its certificate or its negative witness. This proves termination and correctness by induction. Permutations must transport a witness y in permuted coordinates to P^T y in the original coordinates.

The raw script guards only some requirements with assert; those disappear under -O. It checks diagonal rationality but not every off-diagonal entry, uses bool coercion, and prints failures without guaranteeing a nonzero exit. Its four-square search bound uses a floating square root. The reviewed derivative uses explicit guards, every-entry Gaussian-rational membership, integer isqrt and nonzero failure exit. A separate fixture checks a rectangular non-symmetric input-first vectorization: the raw vecm uses K[j,a] instead of K[a,j], hidden by its diagonal examples.

## BR-36 and BR-37: accepted identities

The qubit ball equation and sharp q_0 bounds are correct under the stated real probability domain. The inverse is Hermitian trace one and PSD iff its determinant is nonnegative. Cauchy-Schwarz on the radius-1/6 ball gives q_0 extrema (3 +/- sqrt(3))/6; equality in the lower bound fixes the unique irrational endpoint. Rational admissible data cannot attain it. Boundary points are pure; zero branches remain unnormalized zero states.

The input-first Choi composition/link formula is correct. Its positivity follows from complete positivity of the continuation, not from positivity of a partial transpose or an arbitrary product of PSD matrices. Associativity follows either from the displayed index contraction or injectivity of Choi representation. Every colour/dimension match remains mandatory.

## BR-38: full non-norm proof and a sharper optional upper bound

The equal-Gram vector matching proof is valid over Q(i). For distinct equal-norm a,b, w=a-b and c=w*a satisfy c!=0 and w*w=c+conjugate(c), giving a rational unitary I-ww*/c that sends a to b and fixes w-perpendicular vectors. At each row step equal Gram data make w orthogonal to all previously matched vectors. This proves the matching invariant and the padded unitary theorem, including zero and dependent rows.

To prove 1/3 is not a Gaussian-rational norm, suppose x,y,z are integers, z!=0, gcd(x,y,z)=1 and (x/z)^2+(y/z)^2=1/3. Then 3(x^2+y^2)=z^2 implies 3 divides z. Write z=3t; then x^2+y^2=3t^2. Squares mod 3 are 0 or 1, so 3 divides both x and y, contradicting primitivity. A finite search for integer squares adding to 3 alone does not establish this rational claim. The two Gaussian numbers (1+i)/3 and 1/3 have norm sum 1/3, proving that the rank-one example needs exactly two rational vectors.

A useful stronger bound follows from the same four-square import already used by the submission. Every nonnegative rational delta=sum_(j=1)^4 r_j^2 is the sum of TWO Gaussian norms, abs(r_1+i r_2)^2+abs(r_3+i r_4)^2. Apply this to each positive diagonal entry in a rational PSD LDL* certificate. For rank r this yields at most 2r Gaussian-rational Gram vectors. Thus rank(C)<=minimal rational Kraus count<=2 rank(C); the rank-one 1/3 example makes the upper bound sharp at rank one. The submitted 4r bound remains valid but is weaker.

## BR-39: global interchange requires all affected pairs

The corrected manuscript gives the four-region continuation assignment and complete outcome-count proof. The original formula fails even before comparing matrices: for m=n=p=q=2 it asserts an identification between 9 and 7 outcomes. The submitted check tests a true local mixed-product identity only. On its own m=n=p=2,q=1 fixture, the complete profiles would have 6 and 5 outcomes. The corrected independent replay checks the whole 9-outcome grid with a concrete flattening permutation, all representatives and normalization.

Swap requires both colour permutation matrices and outcome relabeling, as the submission correctly says. Parallel Choi descent requires the stated leg permutation. These facts do not repair missing strip substitutions in the original global formula.

## BR-40: typed isometry, completed dynamics and nesting

The rational isometry, pointer projection, block/pointer equality on ran(V) and post-partial-trace state identities are correct. The written unitary formula needs an input embedding: V=U_0 B_0 in K^(ER), not generally U_0(x tensor epsilon_1), whose domain would have dimension dR. A trace channel d=2,E=1,R=2 already demonstrates the mismatch.

For a tensor-factor ancilla, D=lcm(d,ER) and the lifted isometry V tensor eta_1^(D/(ER)) share a D-dimensional codomain with x tensor eta_1^(D/d). Rational unitary matching realizes the lift from that input encoding. Measurement and discard on the lifted environment reproduce the original state updates. Availability of this encoding, unitary, pointer measurement and discard remains declared physical input.

For nesting, first define a controlled continuation isometry C on the typed system: apply V_L on the selected block, and map each untouched block to its new tag tensored with a fixed continuation-pointer vector. Then (C tensor I_R)V_K, after a leg permutation, agrees with the direct nested dilation only after an explicit environment embedding. The direct branch count is (R-r_i)+r_iR', generally smaller than RR'. The embedding sends affected (a,b) to a tensor b and untouched a to a tensor 1. Direct, sequential and padded pointer dimensions must be recorded separately. Parallel dilation likewise needs a system/pointer leg permutation.

Finally branch relabeling in BR-26 and CP equivalence in BR-30 are distinct relations. Partial trace discards auxiliary branch information and is compatible with the CP quotient; it does not make those two equivalence relations identical or imply equal environment states for all presentations.
