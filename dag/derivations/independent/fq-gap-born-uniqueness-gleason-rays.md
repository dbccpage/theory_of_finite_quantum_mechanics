Status: AI-drafted, awaiting human review.

# FQ-GAP-BORN-UNIQUENESS-GLEASON: frame functions on all rational rays of Q^3, and the residue-mod-2 ansatz on Q(i)^3

Node status stays CONDITIONAL. This note records two kernel-checked results on the projection-only (frame-function) route and states precisely what remains open.

Lean: `lean4/CampaignBornRationalRayObstruction.lean`, `lean4/CampaignBornGaussianMod2ClassRigidity.lean` (library `CampaignFqGapBornGleasonRays`). Receipt: `dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json`. Independent checks: `checks/independent/fq-gap-born-uniqueness-gleason-rational-rays.py`, `checks/independent/fq-gap-born-uniqueness-gleason-mod2.py`.

## 1. Setting

A *frame* in Q^3 is a triple of nonzero pairwise orthogonal vectors; a *frame function* is a function on rays with f(u) + f(v) + f(w) = 1 on every frame. A frame function is *quadratic* (Born) if there is a rational symmetric 3 x 3 form Q with f(v) = Q(v) / (v . v) for every nonzero v.

Every rational ray contains an integer vector not all of whose coordinates are even; two such representatives differ by an odd rational factor. So a function on integer vectors not all even that is invariant under negation and under scaling by odd integers is a function on rational rays.

The repository already has a two-valued non-quadratic frame function on the rational *unit sphere* (`BornRationalSphereObstruction`, rays with square norm). The question treated here is the larger carrier of *all* rational rays.

## 2. The exotic function on Q^3

For an integer vector v = (a, b, c) not all even, call its *pattern* the triple of parities. Exactly one, two, or three coordinates are odd.

- If exactly two coordinates x, y are odd, put pairSign(x, y) = -1 if x = y (mod 4) and +1 otherwise, and sgn v = pairSign(x, y).
- Otherwise sgn v = 0.

Define exotic(v) = (1 + sgn v) / 3. Its values are 0, 1/3, 2/3 (`exotic_values`, `exotic_nonneg`). It is invariant under negation and odd scalings (`exotic_neg`, `exotic_odd_smul`): odd scalings preserve parities and congruence modulo 4.

**Theorem A** (`exotic_frame_function`). For every frame (u, v, w) of integer vectors not all even, exotic(u) + exotic(v) + exotic(w) = 1.

*Proof.* It suffices to show sgn u + sgn v + sgn w = 0 (`sgn_frame_sum`).

Step 1 (patterns). Reducing u . v = 0 modulo 2 shows that the patterns of u and v are orthogonal in F_2^3. The nonzero vectors of F_2^3 are e_1, e_2, e_3 (weight one), e_k + e_l (weight two) and (1,1,1) (weight three). Checking the F_2 pairings: a weight-one pattern is orthogonal only to the other two weight-one patterns and to the weight-two pattern on the complementary pair; a weight-two pattern is orthogonal to itself, to the complementary weight-one pattern, and to (1,1,1); (1,1,1) is orthogonal only to weight-two patterns. Hence the pattern multiset of a frame is one of: {e_1, e_2, e_3}; {e_k, e_l + e_m, e_l + e_m}; {(1,1,1), e_k + e_l, e_k + e_l}; {e_k + e_l, e_k + e_l, e_k + e_l}. In particular a weight-two pattern never occurs exactly once in a frame, and two different weight-two patterns never occur together.

Step 2 (cancellation). Let v, w be orthogonal with the same weight-two pattern, odd coordinates in positions l, m and even third coordinates v_n, w_n. Write v_l = a, v_m = b, w_l = c, w_m = d (all odd) and e = v_n, f = w_n (both even). Then ac + bd + ef = 0 and ef = 0 (mod 4), so ac + bd = 0 (mod 4). Modulo 4 the odd residues are +-1, and for signs a, b, c, d in {+-1} the identity ac + bd = 0 holds exactly when precisely one of a = b, c = d holds. Therefore pairSign(a, b) + pairSign(c, d) = 0 (`pairSign_add_eq_zero`, proved by a 64-case residue check).

Step 3. In the pattern types with exactly two weight-two vectors, the third vector has sgn 0 and the two weight-two vectors cancel by Step 2. In the type with three weight-two vectors of the same pattern, Step 2 applied to the three pairs gives s_1 + s_2 = s_2 + s_3 = s_1 + s_3 = 0, hence s_1 + s_2 + s_3 = 0. (Over Z this type cannot occur at all, but the proof does not need that.) In the type {e_1, e_2, e_3} all signs are 0. The Lean proof runs over the 2^9 parity patterns of the nine coordinates, discharging impossible patterns with the dot products modulo 2 and the possible ones with Step 2.

**Theorem B** (`exotic_not_quadratic`). No rational symmetric form Q satisfies Q(v) = exotic(v) (a^2 + b^2 + c^2) on all rays.

*Proof.* On e_1, e_2, e_3 the values are 1/3, forcing the diagonal entries r_00 = r_11 = r_22 = 1/3. On (1,1,0), (1,0,1), (0,1,1) the value is 0 (the two odd coordinates are 1 and 1, congruent mod 4), forcing r_01 = r_02 = r_12 = -1/3. Then Q(1,1,1) = 1 - 2 = -1, while exotic(1,1,1) . 3 = 1. Contradiction. The independent check recomputes the 7 x 6 system exactly and finds it inconsistent (rank 6).

Consequently, on all rational rays of Q^3, frame additivity on orthogonal triples does not force the quadratic form, even for nonnegative frame functions with values in {0, 1/3, 2/3}.

## 3. The residue-mod-2 ansatz on Q(i)^3 is rigid

The existing module `BornGaussianRationalFrameObstruction` shows that a frame function on Q(i)^3 whose value on Gaussian-integer vectors not divisible by 1 + i depends only on the (1+i)-parity class ((a+b) mod 2, (c+d) mod 2, (e+g) mod 2) is the constant 1/3, and names residues modulo 2 as the next untested ansatz.

**Theorem C** (`mod2_class_function_is_third`). Let f be a frame function on Q(i)^3 and suppose f(a+bi, c+di, e+gi) = col(a mod 2, b mod 2, c mod 2, d mod 2, e mod 2, g mod 2) whenever some component is not divisible by 1 + i. Then f = 1/3 on all such vectors.

*Proof.* There are 4^3 - 2^3 = 56 admissible residue classes. The module lists 56 explicit frames of Gaussian-integer vectors with coordinates of modulus at most 3, found by an exact search; each is verified by the kernel. The 56 x 56 matrix A whose (frame, class) entry counts how often the class occurs in the frame is invertible over Q, and the frame equations read A col = (1, ..., 1). Each class value is therefore the rational combination of the frame equations given by the corresponding row of A^{-1}; the entries of A^{-1} have modulus at most 1 and denominators dividing 12, and every row sums to 1/3. The Lean proof discharges each of the 56 class equations with `linear_combination` using those coefficients, then evaluates the given vector's class by a case split on the six parities. The independent check recomputes the orthogonality of all 56 frames, the admissibility of the 168 vectors, the coverage of the 56 classes, the invertibility of A, and A^{-1}(1, ..., 1) = (1/3, ..., 1/3), with exact fractions.

Exact probes (not formalised, not claimed): the same elimination over frames with coordinates in a box of radius 3 forces the constant 1/3 also for class functions modulo (1+i)^3 = 2+2i, modulo 4, modulo the inert prime 3 and modulo the split prime 2+i. These are leads only.

## 4. Relation between the two carriers

Every real frame is a Q(i)-frame, so a frame function on Q(i)^3 restricts to one on Q^3. The exotic function of Section 2 is a class function modulo 4 on Z^3, whereas by Theorem C (and the mod-4 probe) no non-constant class function modulo 4 exists on Z[i]^3. So if the exotic function extends to Q(i)^3 at all, the extension is not a residue class function modulo 4. Exact linear algebra over Gaussian boxes of radius 2, with the real rays fixed to the exotic values and permutation/conjugation symmetry imposed, found no inconsistency and determined 60 non-real ray values (among them 1/2 on (1, -1-i, -1)); this is finite evidence only and decides nothing.

## What is proved

- `exotic_frame_function`: exotic is a frame function on all rational rays of Q^3 (integer vectors not all even; invariance under negation and odd scalings is proved).
- `exotic_not_quadratic`: it is not of the form Q(v)/(v . v) for any rational symmetric form Q.
- `exotic_values`, `exotic_nonneg`: its values are 0, 1/3, 2/3.
- `mod2_class_function_is_third`: on Q(i)^3, every frame function that is a residue-mod-2 class function on (1+i)-primitive Gaussian-integer vectors is 1/3 there.

All declarations compile with only `propext`, `Classical.choice`, `Quot.sound`.

## What is assumed

Nothing beyond the definitions: frames are pairwise orthogonal triples of nonzero vectors for the stated inner products; the class hypothesis in Theorem C is an explicit ansatz, not a derived fact. The carrier and effect additivity of the node remain supplied, as before.

## What is open

- Whether every frame function on Q(i)^3 rays is quadratic (variants: signed, nonnegative, {0,1}-valued). Not decided.
- Whether the exotic Q^3 function extends to a frame function on Q(i)^3. Not decided.
- Class ansatzes modulo (1+i)^k for k >= 3 and modulo odd primes: closed only by unformalised exact probes.
- Over Q^3, whether a {0,1}-valued frame function exists on all rational rays (a Kochen-Specker colouring of P^2(Q)); the exotic function is three-valued.
