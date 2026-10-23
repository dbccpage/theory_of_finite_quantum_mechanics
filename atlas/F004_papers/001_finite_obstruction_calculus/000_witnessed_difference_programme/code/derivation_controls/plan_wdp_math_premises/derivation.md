# PLAN-WDP-MATH-PREMISES

Goal id: PLAN-WDP-MATH-PREMISES

Selected scope for PLAN-WDP-MATH-PREMISES is recorded in this note.

## Selected scope

Three labelled finite carriers, not one sum. R2: L=4 CAR occupation basis (16 states), a_0=n_0-1/2 at Euclidean time 0, theta=-1/96, mu=0; on-site covariance 1/4, signed closed-form factor 0, absolute ratio 1. R3: n=2 sharp projectors and lambda=1/2 give 3/4; the separate n=1 value is not an input. R4: Q(i) identified with Q(i) tensor Q(i) by multiplication; unit pure-tensor squared norms 1 and 2. No volume limit, Born uniqueness, or continuum claim.

The cited 2026-10-08 review member inside `history.zip` was not byte-decoded. Its three anchors are not inputs. The arithmetic below is taken from the opened active paper, the two finite derivations, and the opened Python witnesses. Historical receipts were not rewritten. No fresh test or Lean build was run for this note.

## Hypotheses

The hypotheses are restricted to these three carriers. They are selected inputs, not consequences of a volume limit.

H1. R2 uses the periodic CAR ring of even length L=4. The occupation basis has dimension 2^4=16. The opened builder stores the integer matrix 2 a_x, with a_x=(-1)^x (n_x-1/2). Euclidean time is 0, so the Heisenberg operator at the origin is a_0. The state is any trace-one operator, including the normalized state at theta=-1/96. The weight is mu=0, so the rational stand-in for e^mu is 1.

H2. The signed plug-in uses q=96 theta e^mu. The corrected predicate, as written in (O-14), TL-4, and `tail_bound`, uses q=96|theta| e^mu<1. The separate nonnegative-temperature statement (O-15) and TL-7 keeps 0<=theta<=1/192, mu>=0, and that same strict inequality. It is not an input to the signed endpoint.

H3. R3 uses, for integer n>=1 and rational lambda in [0,1],

p_lambda(rho,E)=lambda Tr(rho E)+(1-lambda) Tr(E)/n,

on a finite POVM. The n=2 carrier is the sharp pair of complementary diagonal projectors with lambda=1/2. The opened n=1 effect e=1/3 is a different carrier. It is not substituted into the n=2 value.

H4. R4 identifies Q(i) tensor_{Q(i)} Q(i) with Q(i) by multiplication. The complex structure is multiplication by i. The two compared forms are h_s(z,w)=s conjugate(z) w for s in {1,2}. Pure-tensor multiplicativity is an extra rule, not part of the balance identity.

## Derivation

### R2. Signed ratio on the length-4 ring

On the opened ring builder, 2 a_x is diagonal in the occupation basis. Its entries are (-1)^x (2 n_x-1), hence lie in {-1,+1}. Therefore (2 a_x)^2=I on every even ring L>=4, including L=4, and a_x^2=I/4. The opened test records this for the origin on the 16-dimensional ring: the square of the stored matrix 2 a_0 is the 16 by 16 identity.

At Euclidean time 0 the Heisenberg operator is a_0. For every trace-one state,

C^L_00(0)=Tr(rho a_0^2)=Tr(rho)/4=1/4.

The identity does not use the sign of theta, so it includes theta=-1/96. The y=0 term of the weighted sum is therefore 1/4.

The omitted-absolute ratio at these parameters is

q=96 theta e^mu=96*(-1/96)*1=-1.

The weighted closed form is (1+q)/(1-q)=0/2=0. The opened test multiplies that factor by M_1=24576/43 and obtains 0. A majorant of 0 cannot upper-bound a sum that contains 1/4. The signed plug-in is false on this carrier.

The corrected ratio uses the absolute value:

q=96|theta|e^mu=96*(1/96)*1=1.

The predicate in (O-14) and TL-4 is q<1. The opened `tail_bound` computes q from `abs(theta)` and raises when q<1 fails. At this endpoint it refuses. The same refusal fires on the positive endpoint theta=1/192 when the rational stand-in for e^mu is 2, because that product is also q=1. The opened `embedding_bound` raises there. Refusal at q=1 is the domain statement. It is not a bound.

For comparison, the same routine accepts both signs of theta=1/192 at e^mu=1. Then q=1/2 and (1+q)/(1-q)=3, so the returned majorant is 3 M_1. That acceptance is a rational evaluation of the corrected formula inside q<1. It is not the signed endpoint, and it is not TL-7.

The separate nonnegative-temperature statement stays as written. (O-15) and TL-7 require 0<=theta<=1/192, mu>=0, and q=96|theta|e^mu<1. On that window the lift comparison uses

128^2/(96*192)=16384/18432=8/9,

because 128^2 theta/96 <= 8/9 when 0<=theta<=1/192. The opened `embedding_bound` gate tests `abs(theta)<=1/192`. That code gate does not prove TL-7 for negative theta. The Kotecký–Preiss criterion imported by the volume-limit argument is not reproved here. The length-4 identity is an operator fact on 16 states.

### R3. Readout family, with the dimension split

For n>=1 and 0<=lambda<=1, define p_lambda as in H3. On a finite POVM summing to I,

sum_o Tr(E_o)/n=Tr(I)/n=1.

Each effect term Tr(E)/n is nonnegative, and the trace readout is nonnegative on effects. Every convex combination therefore stays nonnegative, and the outcome weights sum to 1, for every n>=1. Phase invariance and affinity are the corresponding properties of the two summands. The opened `depolarized_probability` implements this combination and refuses a weight outside [0,1].

At n=1 the only normalized state is [1]. For an effect [e], Tr(rho E)=e and Tr(E)/n=e, so p_lambda=e for every lambda. The opened dimension-one witness uses the state factor [2] and three identical accept rows [1/3]. Its effect value is 1/3 at every opened weight, including 0, 1/2, 3/4, and 1. The complementary value is 2/3. That one-dimensional value is not reused below.

At n=2 the sharp pair has Tr(rho E)=1 and Tr(E)/n=1/2. At lambda=1/2,

p_{1/2}=1/2+(1/2)*(1/2)=3/4.

The undeformed value is 1. The difference is

p_lambda-1=-(1-lambda)(1-1/n).

At n=1 the factor (1-1/n) is 0, so the difference is identically 0. At n=2 and lambda=1/2 the difference is -(1/2)(1/2)=-1/4, and 1-1/4=3/4. For n>=2 the same difference is 0 only at lambda=1. The opened tests state this split for sharp pairs in dimensions n=2, 3, and 4: the value equals lambda+(1-lambda)/n, and it differs from the undeformed value exactly when the weight is not 1. Positivity and normalization therefore survive for n>=1. Sharp-pair nonselection requires n>=2.

The theorem text in the paper and in the readout derivation states that split. The one-line GEN-WDP-65 register gloss says the family is distinct from the undeformed trace pairing and does not name n>=2. The completion-audit sentence that a depolarized family differs on a sharp input likewise does not name n>=2. Neither gloss is a substitute for the n=1 identity. The opened Lean module `FiniteStateEffectReadout` proves the two-by-two sharp identity `probability=1` for its basis fixture. It does not state the dimension split. GEN-WDP-64 remains the conditional exact trace interface after that readout is admitted. This calculation does not select or refute it.

### R4. Balance does not fix the pairing scale

The balance relation is (J_V x) tensor y = x tensor (J_W y). Identify both factors with Q(i) by multiplication, and let J be multiplication by i. Then

(i z) w = z (i w)

for every z, w in Q(i), so this identification satisfies balance.

For s in {1,2} define h_s(z,w)=s conjugate(z) w on the identified tensor. The form is sesquilinear, conjugate-linear in the first argument. It is Hermitian because the conjugate of h_s(z,w) is h_s(w,z). It is positive because

h_s(z,z)=s |z|^2,

which is positive for z nonzero. On the unit pure tensor,

h_s(1 tensor 1, 1 tensor 1)=s.

The product of the two usual unit pairings is conjugate(1)*1*conjugate(1)*1=1. Thus s=2 is balanced and positive, but 2 is not 1, so it fails pure-tensor multiplicativity for those unit pairings. The scale s=1 equals that product. The opened test checks both scales, the balance identity under multiplication by i, positivity on three Gaussian-rational samples, and equality with the unit product only at scale 1.

If multiplicativity on pure tensors is supplied,

h(x tensor u, y tensor v)=h_V(x,y) h_W(u,v),

then pure tensors span the finite tensor product, so there is exactly one sesquilinear extension. The opened Hermitianization derivation records that this rule descends through balance, because h_V(J_V x,y)=-i h_V(x,y) matches the other factor. Uniqueness is conditional on that supplied rule. It is not a consequence of balance alone. The coefficient quotient that enforces balance is a different statement and is not reproved here.

## Claims this note does not make

- It does not decode `wdp_review_2026_10_08.md` inside `history.zip`, and it does not rewrite a historical receipt or the goal record.
- It does not treat the length-4 identity C^L_00(0)=1/4 as an infinite-volume limit, a continuum field, a physical temperature law, or a reproof of the imported Kotecký–Preiss criterion.
- It does not read the code gate `abs(theta)<=1/192` as a proof of TL-7 for negative theta.
- It does not remove the hypothesis q<1 from (O-14), TL-4, (O-15), or TL-7. The value 0 of the signed closed form is not a tail bound.
- It does not derive or refute the Born rule. Positivity, normalization, phase invariance, and affinity do not select the undeformed trace pairing when n>=2. Equality of the family at n=1 is not uniqueness of that pairing.
- It does not use the dimension-one value 1/3 as an input to the dimension-two value 3/4.
- It does not treat the GEN-WDP-65 register gloss, or the completion-audit sharp-input sentence, as a statement of the n>=2 split. Neither line was edited.
- It does not call balance a multiplicativity rule, a physical subsystem law, or a completed infinite tensor product. Scale 2 remains a balanced positive form.
- It does not claim a Rust owner of these three fixtures, a fresh test run, or a Lean proof of the dimension split or of the scale split.
- It does not close a theorem outside the three finite carriers named above.
