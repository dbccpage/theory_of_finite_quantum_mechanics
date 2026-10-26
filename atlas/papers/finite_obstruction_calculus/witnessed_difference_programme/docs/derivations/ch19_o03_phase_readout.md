# Scalar, phase, and readout choices

**Status.** Selected finite derivation for the broader-work column of
`CH19-O03`. The conditional bridge in `WDP-CH19-O03` stays as registered.
This note names the scalar and phase choices of the two implemented branches,
admits the continuous logarithm rather than evaluating it, and shows that
phase invariance does not select the Born readout. It does not retitle the
canonical ledger row.

**Witness.** `ch19-o03-phase-readout`,
`problem_sha256` `8eaccab8f1ca8ca5ce34fb4e973ef81e97e73de2825c14ea7a4ea82ee53c571f`,
receipt
[`evidence/ch19_o03_phase_readout_receipt.json`](../../evidence/ch19_o03_phase_readout_receipt.json).
The checker is
[`code/witnessed_difference/ch19_o03_phase_readout.py`](../../code/witnessed_difference/ch19_o03_phase_readout.py).

## 1. Three scalar choices, and why they are not one choice

The bridge in §19.4 has to name an amplitude carrier. Three hosts appear in
the scoped result. They are not interchangeable.

1. **Anchor host.** Work in \(\mathbb Q(i)\) with the fixed unit
   \[
   u=\frac{3+4i}{5}=\frac{2+i}{2-i}.
   \]
   Its norm is \(1\). Integer powers \(u^n\) are defined. This is the phase
   of CH19-P11 and CH19-P12.
2. **Rational-turn host.** Work in \(\mathbb Q/\mathbb Z\). The declared
   character sends the class of \(q\) to \(\exp(2\pi i q)\). On a common
   conductor this is a root of unity. Every class has an \(n\)th root. The
   character has period \(1\).
3. **Continuous host.** Declare a real angle \(\theta\) with
   \(\exp(i\theta)=u\), and set \(\chi_\theta(t)=\exp(i\theta t)\). This note
   does not compute that exponential. The host is the admission that a
   logarithm of \(u\) has been supplied.

**(Proposition 1.)** No unit-norm element of \(\mathbb Q(i)\) squares to \(u\).
Hence no homomorphism \((\mathbb Q,+)\to U(1)\cap\mathbb Q(i)\) sends \(1\) to
\(u\).

*Proof.* A square root \(x+yi\) would satisfy \(x^2+y^2=1\) and
\(x^2-y^2=3/5\), so \(x^2=4/5\) and \(y^2=1/5\). In lowest terms, \(4/5\) is a
square only if both \(4\) and \(5\) are integer squares. The integer \(5\) is
not a square. The same holds for \(1/5\). A homomorphism sending \(1\) to \(u\)
would send \(1/2\) to such a square root. \(\square\)

**(Proposition 2.)** \(u^n=1\) if and only if \(n=0\). The anchor therefore has
infinite order, while the rational-turn character kills every integer.

*Proof.* The case \(n=0\) is immediate, and negative \(n\) follow by inversion.
Write \((2+i)^n=a_n+b_ni\). Then \(u^n=1\) implies \((2+i)^n=(2-i)^n\), so
\(b_n=0\). The recurrence is \(a_{n+1}=2a_n-b_n\) and \(b_{n+1}=a_n+2b_n\),
with \(a_1=2\), \(b_1=1\). Modulo \(5\),
\[
a_1+3b_1=5\equiv 0,\qquad a_1-3b_1=-1\equiv(-1)^1.
\]
The step expands to
\[
a'+3b'=5(a+b),\qquad a'-3b'+(a-3b)=-10b.
\]
Both corrections are divisible by \(5\), so
\(a_n+3b_n\equiv 0\) and \(a_n-3b_n\equiv(-1)^n\) for every \(n\ge 1\). If
\(b_n\equiv 0\), then \(a_n\equiv 0\) and \(a_n\equiv\pm 1\), which is
impossible modulo \(5\). Thus \(b_n\neq 0\) and \(u^n\neq 1\). \(\square\)

The rational-turn branch makes a different identification. On a triangle,
edges \(1/3\), \(1/4\), and \(1/6\) have loop class
\[
\frac13+\frac14-\frac16=\frac{5}{12}.
\]
Adding a vertex potential changes the edges by a coboundary and leaves the
loop class unchanged: the endpoint corrections cancel. An integer cochain
with cycle sum \(1\) is not a coboundary, because every coboundary has cycle
sum \(0\). The rational-turn character nevertheless sends that cycle to \(1\),
the same value it sends to \(0\). It is a divisible periodic phase. It is not
a root of the infinite-order anchor, and Proposition 1 says the anchor's own
host cannot supply that root.

The continuous character is the third choice: pay a real logarithm of \(u\).
Then \(\chi_\theta(1/2)\) is a square root of \(u\), so Proposition 1 is
escaped by leaving \(\mathbb Q(i)\). No value of that exponential is claimed
in the receipt. The branch is justified as the host that keeps the anchor and
accepts rational exponents, not as a calculation inside the anchor host.

## 2. Readout is a further choice

Phase invariance does not pick a probability. Let \(z=(1,2)\) and let
\(w=uz\). Then \(N(u)=1\), so \(N(w_i)=N(z_i)\). The cross term is unchanged
because
\[
w_1\bar w_2=u z_1\bar u\,\bar z_2=N(u)\,z_1\bar z_2.
\]
Any readout that depends on the two norms and the cross term is therefore
the same for \(z\) and for \(w\).

Two such readouts disagree. The normalized squared norms are
\[
\Bigl(\frac{N(1)}{N(1)+N(2)},\frac{N(2)}{N(1)+N(2)}\Bigr)
=\Bigl(\frac15,\frac45\Bigr).
\]
The normalized fourth powers are
\[
\Bigl(\frac{1}{17},\frac{16}{17}\Bigr).
\]
Both are nonnegative and sum to \(1\). They are not equal. The same split
appears before normalization: for \(z_1=z_2=1\), \(N(z_1+z_2)=4\) and
\(N(z_1+z_2)^2=16\).

The Born pairing is a third declaration, not a consequence of the invariance.
Admit coordinate projectors and the pure state
\(\rho=zz^{\dagger}/(z^{\dagger}z)\). Its outcome probabilities are the
normalized squared norms, hence the quadratic table, not the quartic table.
Gauge invariance of \(\rho\) holds because a common unit phase cancels in
\(zz^{\dagger}\). The invariance is shared with the quartic rule, so it does
not select the projector trace. Selecting Born is selecting the quadratic
pairing after the trace has been admitted.

## 3. What stays outside

The continuous exponential is not evaluated. No faithful continuous character
\(\mathbb R\to U(1)\) is claimed: every continuous character has a period
lattice, as already recorded for the scoped bridge. Empirical identification
of either readout with an apparatus is not inferred. `CH19-O04` is not
addressed. The canonical row `WDP-CH19-O03` remains the conditional result
already registered, and `CH19-N01` stands: phase invariance does not select
the Born rule.
