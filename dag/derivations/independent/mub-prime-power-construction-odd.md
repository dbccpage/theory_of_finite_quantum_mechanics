Status: AI-drafted, awaiting human review.

# MUB-PRIME-POWER-CONSTRUCTION: a complete family of q + 1 mutually unbiased bases for every odd prime power q

Node status stays OPEN. This note records the odd-characteristic construction, kernel-checked for an arbitrary finite field of odd characteristic, and states what is not covered (characteristic two beyond dimension 2, and the construction of the complex character inside Lean).

Lean: `lean4/MubPrimePowerOddCharacteristic.lean` (library `CampaignMubPrimePowerOdd`). Receipt: `dag/research/campaign_mub-prime-power-construction-odd_lean_replay.json`. Independent check: `checks/independent/mub-prime-power-construction-odd.py`.

## 1. Setting

Let F be a finite field with q elements and 2 != 0 in F, i.e. q = p^k with p an odd prime. Let R be a commutative domain with an involution `star` (the intended instance is R = C with complex conjugation). Let psi : F -> R be an additive character (psi(0) = 1, psi(s + t) = psi(s) psi(t)) that is nontrivial and unitary: star(psi(t)) = psi(-t). Over C the character psi(t) = exp(2 pi i Tr(t)/p), with Tr the absolute trace F -> F_p, has both properties; this instance is standard and is *not* constructed in the Lean module, which takes psi as a parameter.

Vectors are functions F -> R and the Hermitian pairing is <u, v> = sum_x star(u(x)) v(x). The q + 1 bases, indexed by Option F, are

- the standard basis e_y(x) = [x = y], y in F;
- for each a in F the quadratic-phase basis v_{a,b}(x) = psi(a x^2 + b x), b in F.

No normalisation is performed: the vectors e_y have norm 1 and the v_{a,b} have norm q, and unbiasedness is stated as |<u, v>|^2 q = ||u||^2 ||v||^2 for u, v in different bases, which is |<u/||u||, v/||v||>|^2 = 1/q.

## 2. Character sums

Lemma 1 (`sum_mulShift_eq_zero`, `sum_mulShift`). For c in F, sum_x psi(c x) equals q if c = 0 and 0 otherwise. Proof: if c != 0 pick b with psi(b) != 1; the substitution x -> x + c^{-1} b shows that the sum S satisfies psi(b) S = S, so (psi(b) - 1) S = 0 and S = 0 in the domain R.

Lemma 2 (`weil_sum_mul_star`). For c != 0 and any d, with S = sum_x psi(c x^2 + d x): S star(S) = q. Proof: star(S) = sum_y psi(-(c y^2 + d y)) by unitarity. In the double sum substitute x = y + t for fixed y: c(y+t)^2 + d(y+t) - c y^2 - d y = (c t^2 + d t) + (2 c t) y. Summing first over y, Lemma 1 gives q when 2 c t = 0, i.e. when t = 0 (this is where 2 != 0 is used), and 0 otherwise. The remaining term is psi(0) q = q.

## 3. The bases

- Within the standard basis: <e_y, e_y'> = [y = y'] (`pair_std`).
- Within a quadratic-phase basis: <v_{a,b}, v_{a,b'}> = sum_x psi((b' - b) x) = q [b = b'] by Lemma 1 (`pair_qvec_same`).
- Standard against quadratic-phase: <e_y, v_{a,b}> = psi(a y^2 + b y), of squared modulus psi(t) psi(-t) = 1 (`pair_std_qvec_mul_star`).
- Two quadratic-phase bases with a != a': <v_{a,b}, v_{a',b'}> = sum_x psi((a' - a) x^2 + (b' - b) x), of squared modulus q by Lemma 2 (`pair_qvec_cross_mul_star`).

Theorem (`mub_family`). For every finite field F with 2 != 0, every commutative domain R with involution, every nontrivial unitary additive character psi : F -> R and q != 0 in R: each of the q + 1 bases is orthogonal with nonzero norms, and any two members u, v of different bases satisfy |<u, v>|^2 q = ||u||^2 ||v||^2. The number of bases is q + 1 (`card_bases`).

All declarations compile with only `propext`, `Classical.choice`, `Quot.sound`.

## 4. Independent check

`checks/independent/mub-prime-power-construction-odd.py` builds GF(q) for q in {3, 5, 7, 9, 11, 13, 25, 27} from explicit irreducible polynomials, represents Z[zeta_p] exactly as integer vectors modulo the p-th cyclotomic polynomial, takes psi(t) = zeta_p^{Tr(t)}, and verifies all pairings of all members of all q + 1 bases: 1,015,112 conditions, 0 failures. No floating point is used.

## What is proved

- A complete family of q + 1 bases with the stated orthogonality and unbiasedness identities, for every finite field of odd characteristic, relative to any nontrivial unitary additive character into a domain with involution.
- The Weil-sum identity |sum_x psi(c x^2 + d x)|^2 = q for c != 0.

## What is assumed

- The existence of a nontrivial unitary additive character psi : F -> R. For R = C this is psi(t) = exp(2 pi i Tr(t)/p); the module does not construct it.
- q != 0 in R (automatic for R = C), used only to state that the norms are nonzero.

## What is open

- Characteristic two: the construction of 2^k + 1 bases for k >= 2 (Galois rings GR(4, k)) is not formalised; dimension 2 remains covered only by the earlier Pauli-basis module.
- The complex instance of psi inside Lean, and normalised (unit) vectors.
- Nothing about dimension six is inferred.
