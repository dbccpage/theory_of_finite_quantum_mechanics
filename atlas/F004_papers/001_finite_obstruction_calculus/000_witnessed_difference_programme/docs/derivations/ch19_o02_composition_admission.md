# Admitted composition package behind the CHSH bound

**Status.** Selected finite derivation for the broader-work column of
`CH19-O02`. The conditional bound \(S^2\le 8\) under a declared Hilbert
package stays where `WDP-CH19-O02` and Appendix J already put it. This note
admits the three commitments that package uses, and it separates them from
the composition principle CP. It does not retitle the canonical ledger row.

**Witness.** `ch19-o02-composition-admission`,
`problem_sha256` `bbe70be895c783a18f00193f882597f57fd129ea890b725e38f60161ee537cc1`,
receipt
[`evidence/ch19_o02_composition_admission_receipt.json`](../../evidence/ch19_o02_composition_admission_receipt.json).
The checker is
[`code/witnessed_difference/ch19_o02_composition_admission.py`](../../code/witnessed_difference/ch19_o02_composition_admission.py).

## 1. The three commitments are admissions

CP, as stated in CH19-P08 through CH19-P10, has three clauses:

- **(T)** injective tagging of a Cartesian composite;
- **(NS)** no-signalling of a local instrument, or compatibility of an
  empirical model on the CHSH product cover;
- **(B)** a bilinear form on classical effects, nonnegative on pairs of
  effects and normalized on the constant effects.

Clause (B) is stated for classical carriers only. None of the three clauses
mentions a density operator, a Hermitian observable, or a trace. The
following are therefore not theorems of CP. They are the inputs named by the
broader-work column.

1. **(H) Density.** On \(\mathbb C^2\otimes\mathbb C^2\), with multiplicity
   \(r=1\), take the rational vector \(v=(1,0,0,1)\) and
   \[
   \rho=\frac{vv^{\dagger}}{v^{\dagger}v}.
   \]
   Then \(v^{\dagger}v=2\), \(\operatorname{tr}\rho=1\), and \(\rho\) is a
   Gram matrix, hence positive semidefinite. The matrix is the Bell
   projector already used for package Q2.
2. **(O) Local observables.** \(A_0=Z\), \(A_1=X\),
   \(B_0=(3Z+4X)/5\), \(B_1=(3Z-4X)/5\). Each is real symmetric and squares
   to \(I_2\), because \(X^2=Z^2=I_2\), \(XZ=-ZX\), and
   \((3/5)^2+(4/5)^2=1\).
3. **(T) Tensor trace pairing.** For outcomes \(a,b\in\{+1,-1\}\),
   \[
   p(a,b\mid x,y)
   =\operatorname{tr}\Bigl(\rho\,
     \tfrac{I+a A_x}{2}\otimes\tfrac{I+b B_y}{2}\Bigr).
   \]
   This pairing is supplied with the tensor product. CP does not contain it.

The integer \(r\) is part of admission (H). CP does not name it.

## 2. What CP does decide

**(Proposition 1.)** For nonempty finite carriers, a tagging has local
decoders if and only if it is injective. On \(\{0,1\}\times\{0,1\}\) the
identity tagging is injective. The tagging \(\mathrm{dumpRight}(a,b)=b\)
sends both \((0,0)\) and \((1,0)\) to \(0\), so it has no decoder for the
left factor.

*Proof.* Decoders force \(c(a,b)=c(a',b')\) to imply \((a,b)=(a',b')\). An
injective tagging has a left inverse on its image. The two images of
\(\mathrm{dumpRight}\) were just named. \(\square\)

This is CH19-P08. It chooses injective reports over lossy ones. It does not
choose a Hilbert tensor: both taggings are functions on a four-element
Cartesian carrier, and only one of them is injective.

**(Proposition 2.)** A bilinear form on classical effects that is nonnegative
on every pair of effects and equals \(1\) on the constant effects is exactly
a joint distribution, and the distribution is the value of the form on
indicator effects.

*Proof.* Set \(p(a,b)=\omega(1_a,1_b)\). Nonnegativity and normalization of
\(\omega\) make \(p\) a joint distribution. Bilinearity gives
\(\omega(e,f)=\sum e_a f_b p(a,b)\). Conversely every joint defines such a
form. \(\square\)

The witness evaluates this on the joints
\(p(0,0)=p(1,1)=1/2\) and \(p(0,1)=p(1,0)=0\). The indicator recipe returns
that same table. Clause (B) therefore emits a probability on the four
Cartesian atoms. It does not emit a \(4\times 4\) density.

**(Proposition 3.)** Every deterministic assignment of signs
\((a_0,a_1,b_0,b_1)\) has CHSH value \(\pm 2\). Every mixture does too, in
absolute value.

*Proof.* The combination is \(a_0(b_0+b_1)+a_1(b_0-b_1)\). If \(b_0=b_1\) the
second summand vanishes and the first is \(\pm 2\). If \(b_0=-b_1\) the first
vanishes and the second is \(\pm 2\). A mixture is a convex combination of
these values, so its absolute value is at most \(2\). The sixteen assignments
were enumerated; the only values are \(-2\) and \(2\). \(\square\)

## 3. PR satisfies (NS) and misses the bound

On outcomes \(\{\pm 1\}\) and settings \(\{0,1\}\), let
\[
p(a,b\mid x,y)=\tfrac12
\]
when \(ab=(-1)^{xy}\), and \(0\) otherwise. Each of the four settings is
normalized. Every single-party marginal equals \(1/2\), so the table does not
signal: it meets (NS). Each context's outcome pair is tagged by the identity
on a four-element set, so (T) holds contextwise. The CHSH value is
\[
E_{00}+E_{01}+E_{10}-E_{11}=1+1+1-(-1)=4.
\]
Then \(4^2=16>8\). By Proposition 3 there is no nonnegative global joint with
this value, so clause (B) does not represent the table. (B) was not stated
for a nonclassical factor. Thus (T) and (NS) admit PR, and (B) excludes it
only by remaining classical. Neither clause selects (H), (O), or the trace
pairing.

## 4. The bound under the admission

Write \(P=B_0+B_1\), \(Q=B_0-B_1\), and
\[
S=A_0\otimes P+A_1\otimes Q.
\]
The local square relations give \(P^2+Q^2=4I\) and \(PQ=-QP\). Expanding
\(S^2\) therefore gives the matrix identity
\[
S^2=4I-C_A\otimes C_B,
\]
where \(C_A=[A_0,A_1]\) and \(C_B=[B_0,B_1]\). The same expansion rearranges
to
\[
8I-S^2
=\frac12\Bigl(
(2I+i C_A)\otimes(2I-i C_B)
+(2I-i C_A)\otimes(2I+i C_B)
\Bigr).
\]
Each factor \(2I\pm i C\) is a Gram matrix of \(A_0\pm i A_1\) or
\(B_0\pm i B_1\), so each tensorand is positive semidefinite, and so is the
average. The witness recomputes the rational matrix \(8I-S^2\) and checks
that every principal minor is nonnegative.

Let \(s=\operatorname{tr}(\rho S)\). Positive semidefiniteness of
\((S-s I)^2\) and of \(\rho\) gives
\[
0\le\operatorname{tr}\bigl(\rho(S-s I)^2\bigr)
=\operatorname{tr}(\rho S^2)-s^2.
\]
Positive semidefiniteness of \(8I-S^2\) gives \(\operatorname{tr}(\rho S^2)\le 8\).
Hence \(s^2\le 8\).

On the admitted tuple the four correlators are \(3/5\), \(3/5\), \(4/5\), and
\(-4/5\). Their CHSH combination is \(14/5\). Then
\[
s^2=\frac{196}{25},\qquad 8-s^2=\frac{4}{25}.
\]
The trace \(\operatorname{tr}(\rho S^2)\) equals \(s^2\), so the variance slack
is zero while the operator slack is not. Since \(14/5>2\), Proposition 3 says
no state produced by clause (B) has these correlators. The admitted package
reaches a correlation that CP's classical clause cannot, and it still obeys
\(s^2\le 8\), which PR does not.

## 5. What stays outside

Nothing here derives (H), (O), or the trace pairing from primitive
difference, from injective tagging, or from no-signalling. Multiplicity
\(r=1\) is part of the admission; a larger multiplicity is a different
admission, and CP still would not name it. Phase invariance and the Born
rule are not at issue (`CH19-O03`). The canonical row `WDP-CH19-O02` remains
the conditional result already registered.
