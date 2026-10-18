# Campaign C750 Block 01: Formal Reduction Proof & Negative Controls

AuthorityEffect: None.
Citation: `sealed-derivation-v1` (`3100c4e`)

This document provides the formal mathematical reduction for Campaign C750 Block 01 (Targets C750-T556 through C750-T560).
It establishes that for any finite-dimensional density operator $\rho$ with algebraic spectrum:
1. The von Neumann entropy $S(\rho)$ reduces to a linear form in logarithms of algebraic numbers with algebraic coefficients.
2. Reduction to a $\mathbb{Q}$-linearly independent basis produces a non-vanishing form for any mixed state.
3. By Baker's theorem (Anchor A1), $S(\rho)$ is transcendental for all mixed states.
4. $S(\rho) \in \mathbb{Q}(\zeta_n) \iff S(\rho) = 0 \iff \rho$ is pure ($\mathrm{Tr}(\rho^2) = 1$).
5. Integer-order Rényi invariants $P_m = \mathrm{Tr}(\rho^m)$ are carrier-internal algebraic quantities.

---

## 1. Domain, Definitions, and Carriers

### 1.1 Carrier and Hilbert Space
Let $K = \mathbb{Q}(\zeta_n)$ be the cyclotomic carrier field of conductor $n \ge 1$, where $\zeta_n = e^{2\pi i / n}$.
Let $\mathcal{H}$ be a finite-dimensional Hilbert space of dimension $d \ge 2$ over $K$.
A system declares a single real embedding $\iota \colon K^+ \hookrightarrow \mathbb{R}$ of the maximal totally real subfield $K^+ = \mathbb{Q}(\zeta_n + \zeta_n^{-1}) = \mathbb{Q}(\cos(2\pi/n))$.

### 1.2 Density Operators
A density operator $\rho$ is an endomorphism $\rho \in \mathrm{Herm}_d(K)$ satisfying:
1. Positive semi-definiteness under $\iota$: $\langle v, \rho v \rangle \ge 0$ for all $v \in \mathcal{H}$;
2. Normalization: $\mathrm{Tr}(\rho) = 1$.

### 1.3 Spectrum and Splitting Field
The characteristic polynomial $\chi_\rho(t) = \det(t I_d - \rho) \in K[t]$ has degree $d$.
Let $L / K$ be the splitting field of $\chi_\rho(t)$. The extension degree $[L : K]$ is finite ($[L : K] \le d!$).
Because $\rho$ is Hermitian and positive semi-definite under $\iota$, all roots of $\chi_\rho(t)$ are real under $\iota$.
We denote the multiset of eigenvalues as $\mathrm{spec}(\rho) = \{\lambda_1, \lambda_2, \dots, \lambda_d\} \subset L$, where under $\iota$:
$$\lambda_j \ge 0 \quad \text{for all } j \in \{1, \dots, d\}, \qquad \sum_{j=1}^d \lambda_j = 1.$$
Every eigenvalue $\lambda_j$ is an algebraic number over $\mathbb{Q}$.

### 1.4 Purity and Collision Invariant
The purity (or order-2 Rényi purity) of $\rho$ is defined by:
$$P_2(\rho) = \mathrm{Tr}(\rho^2) = \sum_{j=1}^d \lambda_j^2.$$
More generally, for any integer $m \ge 1$, the integer-order Rényi trace invariant is:
$$P_m(\rho) = \mathrm{Tr}(\rho^m) = \sum_{j=1}^d \lambda_j^m.$$

### 1.5 Von Neumann Entropy
The von Neumann entropy of $\rho$ is defined by functional calculus:
$$S(\rho) = -\mathrm{Tr}(\rho \log \rho) = -\sum_{j=1}^d \eta(\lambda_j),$$
where the function $\eta \colon [0, 1] \to \mathbb{R}_{\ge 0}$ is defined by:
$$\eta(x) = \begin{cases} x \log x, & x \in (0, 1], \\ 0, & x = 0. \end{cases}$$
The branch of the logarithm is the real natural logarithm $\log \colon \mathbb{R}_{>0} \to \mathbb{R}$.
The convention $\eta(0) = 0$ is the unique continuous extension, since $\lim_{x \to 0^+} x \log x = 0$.

---

## 2. Cited Inputs: Transcendence Theorems

In strict adherence to the Campaign C750 Operating Contract (§2), classical transcendence theorems are cited inputs and are not proved or verified by numerical sampling.

### Anchor A1: Baker's Theorem on Linear Forms in Logarithms
**Source:** A. Baker, *Transcendental Number Theory*, Cambridge University Press, 1975, Chapters 1–3.  
**Classification:** `CITED_INPUT`.  
**Statement:** Let $\alpha_1, \dots, \alpha_r$ be non-zero algebraic numbers such that $\log \alpha_1, \dots, \log \alpha_r$ are linearly independent over $\mathbb{Q}$. Let $\beta_0, \beta_1, \dots, \beta_r$ be algebraic numbers, not all zero. Then:
$$\Lambda = \beta_0 + \sum_{i=1}^r \beta_i \log \alpha_i \neq 0$$
and $\Lambda$ is transcendental.  
In particular, for $\beta_0 = 0$, if $\beta_1, \dots, \beta_r$ are algebraic numbers with at least one $\beta_i \neq 0$, the linear form $\sum_{i=1}^r \beta_i \log \alpha_i$ is transcendental.

### Anchor A2: Lindemann–Weierstrass Theorem
**Source:** Baker (1975), Chapter 1.  
**Classification:** `CITED_INPUT`.  
**Statement:** For any non-zero algebraic number $\alpha$, $e^\alpha$ is transcendental. Equivalently, for any algebraic number $\alpha \notin \{0, 1\}$, $\log \alpha$ is transcendental.

---

## 3. Reduction Step 1: Linear Form in Logarithms (Target C750-T557)

Let $\rho$ be a density operator with spectrum $\mathrm{spec}(\rho) = \{\lambda_1, \dots, \lambda_d\} \subset L$.
Let $\{q_1, q_2, \dots, q_m\}$ denote the distinct strictly positive eigenvalues of $\rho$, where $1 \le m \le d$, and let $k_j \ge 1$ denote the multiplicity of $q_j$, so that:
$$\sum_{j=1}^m k_j q_j = 1, \qquad q_j \in (0, 1] \cap L.$$
By the convention $\eta(0) = 0$, all zero eigenvalues contribute zero to the entropy. Therefore:
$$S(\rho) = -\sum_{j=1}^m k_j q_j \log q_j = \sum_{j=1}^m c_j \log q_j,$$
where:
$$c_j = -k_j q_j \in L \setminus \{0\}.$$
Because $k_j \in \mathbb{Z}_{\ge 1}$ and $q_j \in L$, each coefficient $c_j$ is a non-zero algebraic number.
This represents $S(\rho)$ as an exact linear form in logarithms of non-zero algebraic numbers with algebraic coefficients.

---

## 4. Reduction Step 2: Multiplicative Dependence Reduction (Target C750-T558)

The non-zero algebraic numbers $\{q_1, \dots, q_m\}$ may be multiplicatively dependent.

### Definition: Multiplicative Dependence
A set of non-zero algebraic numbers $\{q_1, \dots, q_m\} \subset L^*$ is multiplicatively dependent if there exists a non-zero integer vector $(e_1, \dots, e_m) \in \mathbb{Z}^m \setminus \{\mathbf{0}\}$ such that:
$$\prod_{j=1}^m q_j^{e_j} = 1.$$
Otherwise, $\{q_1, \dots, q_m\}$ is multiplicatively independent.

### Lemma 1: Factorization and $\mathbb{Q}$-Linearly Independent Logarithm Basis
Let $G = \langle q_1, \dots, q_m \rangle$ be the multiplicative subgroup of $L^*$ generated by the positive eigenvalues $\{q_1, \dots, q_m\}$.
Under the embedding $\iota$, each $q_j > 0$ is a positive real number.
Because any root of unity $\zeta \in L^*$ with $\iota(\zeta) > 0$ must satisfy $\iota(\zeta) = 1$, the torsion subgroup of $G$ is trivial: $\mathrm{Tors}(G) = \{1\}$.
Therefore, $G$ is a finitely generated free abelian group of rank $r \ge 1$.
There exists a basis of multiplicatively independent positive algebraic numbers $\{\gamma_1, \dots, \gamma_r\} \subset L^*$ such that each eigenvalue factors uniquely as:
$$q_j = \prod_{i=1}^r \gamma_i^{E_{ji}}, \qquad E_{ji} \in \mathbb{Z}.$$

For the rational spectral case ($q_j \in \mathbb{Q}_{>0}$), the basis $\{\gamma_1, \dots, \gamma_r\}$ is given by the prime factors of the numerators and denominators of $\{q_1, \dots, q_m\}$, and $E_{ji} = v_{p_i}(q_j) \in \mathbb{Z}$ are standard $p$-adic valuations.

### Lemma 2: $\mathbb{Q}$-Linear Independence of Logarithms
The logarithms $\{\log \gamma_1, \dots, \log \gamma_r\}$ are linearly independent over $\mathbb{Q}$.

*Proof.* Suppose there exist rational numbers $a_1, \dots, a_r \in \mathbb{Q}$ such that:
$$\sum_{i=1}^r a_i \log \gamma_i = 0.$$
Clearing denominators yields integers $n_1, \dots, n_r \in \mathbb{Z}$, not all zero unless all $a_i = 0$, such that:
$$\sum_{i=1}^r n_i \log \gamma_i = 0 \iff \log\left(\prod_{i=1}^r \gamma_i^{n_i}\right) = 0 \iff \prod_{i=1}^r \gamma_i^{n_i} = 1.$$
Since $\{\gamma_1, \dots, \gamma_r\}$ are multiplicatively independent, we must have $n_1 = n_2 = \dots = n_r = 0$.
Hence $a_1 = a_2 = \dots = a_r = 0$. $\blacksquare$

### Reduction of the Linear Form
Substituting $\log q_j = \sum_{i=1}^r E_{ji} \log \gamma_i$ into $S(\rho)$:
$$S(\rho) = \sum_{j=1}^m c_j \left(\sum_{i=1}^r E_{ji} \log \gamma_i\right) = \sum_{i=1}^r \left(\sum_{j=1}^m c_j E_{ji}\right) \log \gamma_i = \sum_{i=1}^r \Gamma_i \log \gamma_i,$$
where:
$$\Gamma_i = \sum_{j=1}^m c_j E_{ji} = -\sum_{j=1}^m k_j q_j E_{ji} \in L.$$
Each $\Gamma_i$ is an algebraic number, explicitly computed via exact rational matrix-vector arithmetic.

---

## 5. Reduction Step 3: Purity Corollary & Non-Vanishing Form (Target C750-T559)

### Lemma 3: Non-negativity and Purity Characterization of $S(\rho)$
Let $\rho$ be a density operator on $\mathcal{H}_d$ with algebraic spectrum.
1. $S(\rho) \ge 0$.
2. $S(\rho) = 0 \iff \rho$ is pure ($\mathrm{Tr}(\rho^2) = 1$, spectrum $\{1, 0, \dots, 0\}$).
3. If $\rho$ is mixed ($\mathrm{Tr}(\rho^2) < 1$), then $S(\rho) > 0$.

*Proof.*
Consider the real-valued function $f(x) = -\eta(x)$ on $[0, 1]$:
- For $x = 0$, $f(0) = 0$.
- For $x = 1$, $f(1) = -1 \log 1 = 0$.
- For $x \in (0, 1)$, $\log x < 0$, so $f(x) = -x \log x > 0$.

Thus $f(x) \ge 0$ for all $x \in [0, 1]$, and $f(x) = 0 \iff x \in \{0, 1\}$.
Since the spectrum $\{\lambda_1, \dots, \lambda_d\}$ satisfies $\lambda_j \in [0, 1]$ and $\sum_{j=1}^d \lambda_j = 1$:
$$S(\rho) = \sum_{j=1}^d f(\lambda_j) \ge 0.$$

Equality $S(\rho) = 0$ holds if and only if each term $f(\lambda_j) = 0$.
By the characterization above, this occurs if and only if $\lambda_j \in \{0, 1\}$ for every $j \in \{1, \dots, d\}$.
Combined with $\sum_{j=1}^d \lambda_j = 1$, exactly one eigenvalue is 1 and the remaining $d-1$ eigenvalues are 0.
This corresponds to a spectrum of $\{1, 0, \dots, 0\}$, which means $\rho = |v\rangle\langle v|$ is a rank-1 projection, or equivalently $\mathrm{Tr}(\rho^2) = 1^2 + 0 + \dots + 0 = 1$.

Conversely, if $\rho$ is mixed, $\mathrm{Tr}(\rho^2) = \sum_{j=1}^d \lambda_j^2 < 1$.
Because $\sum \lambda_j = 1$, no single eigenvalue can equal 1.
Therefore, at least two eigenvalues $\lambda_a, \lambda_b$ satisfy $0 < \lambda_a, \lambda_b < 1$.
Consequently, $f(\lambda_a) > 0$ and $f(\lambda_b) > 0$, implying $S(\rho) \ge f(\lambda_a) + f(\lambda_b) > 0$. $\blacksquare$

### Lemma 4: Non-Vanishing of the Reduced Linear Form for Mixed States
Let $\rho$ be a mixed state with algebraic spectrum. In the reduced linear form:
$$S(\rho) = \sum_{i=1}^r \Gamma_i \log \gamma_i,$$
the coefficients $(\Gamma_1, \dots, \Gamma_r)$ do not all vanish:
$$\exists i \in \{1, \dots, r\} \quad \text{such that } \Gamma_i \neq 0.$$

*Proof.* Suppose for contradiction that $\Gamma_i = 0$ for all $i \in \{1, \dots, r\}$.
Then:
$$S(\rho) = \sum_{i=1}^r 0 \cdot \log \gamma_i = 0.$$
However, by Lemma 3, $\rho$ being mixed implies $S(\rho) > 0$.
The equality $0 = S(\rho) > 0$ is a direct contradiction.
Hence at least one coefficient $\Gamma_i$ is non-zero. $\blacksquare$

---

## 6. Reduction Step 4: Application of Baker's Theorem and Transcendence

### Theorem 1 (Entropy Transcendence for Mixed States)
Let $\rho$ be any mixed density operator on a finite-dimensional Hilbert space $\mathcal{H}_d$ whose spectrum consists of algebraic numbers.
Then the von Neumann entropy $S(\rho)$ is transcendental.

*Proof.*
1. By Section 4, $S(\rho)$ is expressed as:
   $$S(\rho) = \sum_{i=1}^r \Gamma_i \log \gamma_i,$$
   where $\gamma_1, \dots, \gamma_r$ are non-zero algebraic numbers, and $\Gamma_1, \dots, \Gamma_r$ are algebraic numbers.
2. By Lemma 2, $\{\log \gamma_1, \dots, \log \gamma_r\}$ are linearly independent over $\mathbb{Q}$.
3. By Lemma 4, because $\rho$ is mixed, the linear form is non-vanishing ($\exists i, \Gamma_i \neq 0$).
4. The hypotheses of Baker's Theorem (Anchor A1) are completely satisfied:
   - $\gamma_i \in \overline{\mathbb{Q}} \setminus \{0\}$,
   - $\log \gamma_i$ are $\mathbb{Q}$-linearly independent,
   - $\Gamma_i \in \overline{\mathbb{Q}}$,
   - at least one $\Gamma_i \neq 0$.
5. By Anchor A1, the linear form $\sum_{i=1}^r \Gamma_i \log \gamma_i$ is transcendental.
6. Therefore, $S(\rho)$ is transcendental. $\blacksquare$

---

## 7. Equality Case Characterization & Terminal Verdict

### Theorem 2 (Entropy Dichotomy & Carrier Equality Case)
Let $K = \mathbb{Q}(\zeta_n)$ be any cyclotomic carrier field. Let $\rho$ be a density operator on $\mathcal{H}_d$ with spectrum in $\overline{\mathbb{Q}}$.
Then:
$$S(\rho) \in \mathbb{Q}(\zeta_n) \iff S(\rho) = 0 \iff \rho \text{ is pure } (\mathrm{Tr}(\rho^2) = 1).$$

*Proof.*
- $(\Leftarrow)$ If $\rho$ is pure, $S(\rho) = 0 \in \mathbb{Q} \subset \mathbb{Q}(\zeta_n)$.
- $(\Rightarrow)$ Suppose $S(\rho) \in \mathbb{Q}(\zeta_n)$.
  Every element of $\mathbb{Q}(\zeta_n)$ is an algebraic number of degree at most $\phi(n)$ over $\mathbb{Q}$.
  If $\rho$ were mixed, Theorem 1 establishes that $S(\rho)$ is transcendental over $\mathbb{Q}$, meaning $S(\rho) \notin \overline{\mathbb{Q}}$.
  This would contradict $S(\rho) \in \mathbb{Q}(\zeta_n) \subset \overline{\mathbb{Q}}$.
  Therefore, $\rho$ cannot be mixed; it must be pure.
  By Lemma 3, $\rho$ being pure implies $S(\rho) = 0$. $\blacksquare$

### Mapping to Campaign Terminal Fields
Target C750-T559 formally establishes the following terminal field bindings for `apps/finite_qm/campaigns/c750/block_01/result.json`:
- `terminal_outcome`: `"ENTROPY_REFUSED_EXCEPT_AT_PURITY"`
- `equality_case`: `"PURE_STATES_ONLY"`
- `entropy_dichotomy_proved`: `true`
- `algebraic_mixed_entropy_found`: `false`
- `baker_used_as`: `"CITED_INPUT"`
- `classical_choice_declarations`: `0`
- `open_fields`: `{}`

---

## 8. Target C750-T560: Exhibition of Negative Controls

Target C750-T560 requires two explicit negative controls:
1. A non-trivial vanishing linear form in logarithms with algebraic coefficients, proving that $\mathbb{Q}$-linear independence is load-bearing;
2. A mixed quantum state exhibiting carrier-internal Rényi-2 purity alongside transcendental von Neumann entropy.

### Negative Control 1: Non-Trivial Vanishing Linear Form
Consider the non-zero algebraic numbers $\alpha_1 = 2, \alpha_2 = 3, \alpha_3 = 6 \in \mathbb{Q}_{>0}$.
Consider the integer coefficients $\beta_1 = 1, \beta_2 = 1, \beta_3 = -1 \in \mathbb{Z} \setminus \{0\}$.
The linear form evaluates to:
$$\Lambda = 1 \cdot \log 2 + 1 \cdot \log 3 - 1 \cdot \log 6 = \log\left(\frac{2 \cdot 3}{6}\right) = \log(1) = 0.$$
Similarly:
$$\Lambda' = 1 \cdot \log 4 - 2 \cdot \log 2 = \log\left(\frac{4}{2^2}\right) = \log(1) = 0.$$

**Load-Bearing Significance:**
- Both $\Lambda$ and $\Lambda'$ are linear forms in logarithms of algebraic numbers with non-zero algebraic coefficients.
- The value $0$ is an algebraic number ($0 \in \mathbb{Q}$), NOT transcendental.
- This demonstrates why reduction to a $\mathbb{Q}$-linearly independent basis (Target C750-T558) and the proof of non-vanishing $S(\rho) > 0$ (Target C750-T559) are strictly load-bearing:
  Without reduction, the linear form could vanish identically, violating Baker's non-vanishing requirement and rendering any transcendence claim invalid.

### Negative Control 2: Carrier-Internal Rényi Purity vs Transcendental Entropy

#### Instance 2A: Frozen Class Witness S6
Witness S6 from `class/fqmi1_class.json` is the commensurable ladder state at conductor 1:
$$\rho_{S6} = \mathrm{diag}\left(\frac{8}{15}, \frac{4}{15}, \frac{2}{15}, \frac{1}{15}\right) \in \mathrm{Herm}_4(\mathbb{Q}).$$

1. **Carrier Membership and Purity:**
   $$\mathrm{Tr}(\rho_{S6}) = \frac{8 + 4 + 2 + 1}{15} = 1.$$
   The integer-order Rényi purity ($m = 2$) evaluates to:
   $$P_2(\rho_{S6}) = \mathrm{Tr}(\rho_{S6}^2) = \left(\frac{8}{15}\right)^2 + \left(\frac{4}{15}\right)^2 + \left(\frac{2}{15}\right)^2 + \left(\frac{1}{15}\right)^2 = \frac{64 + 16 + 4 + 1}{225} = \frac{85}{225} = \frac{17}{45} \in \mathbb{Q}.$$
   The purity $P_2(\rho_{S6}) = \frac{17}{45}$ is an exact rational number, strictly contained in the carrier field $\mathbb{Q} \subset \mathbb{Q}(\zeta_n)$.
   Similarly, all higher integer-order Rényi purities $P_m = \mathrm{Tr}(\rho^m) \in \mathbb{Q}$.

2. **Von Neumann Entropy:**
   The eigenvalues factor over the primes $\{2, 3, 5\}$:
   $$\lambda_1 = \frac{2^3}{15} \implies \log \lambda_1 = 3\log 2 - \log 3 - \log 5,$$
   $$\lambda_2 = \frac{2^2}{15} \implies \log \lambda_2 = 2\log 2 - \log 3 - \log 5,$$
   $$\lambda_3 = \frac{2^1}{15} \implies \log \lambda_3 = \log 2 - \log 3 - \log 5,$$
   $$\lambda_4 = \frac{2^0}{15} \implies \log \lambda_4 = -\log 3 - \log 5.$$
   Weighting by $-\lambda_j$:
   $$S(\rho_{S6}) = -\sum_{j=1}^4 \lambda_j \log \lambda_j = -\left(\frac{8 \cdot 3 + 4 \cdot 2 + 2 \cdot 1 + 1 \cdot 0}{15}\right)\log 2 + \left(\sum_{j=1}^4 \lambda_j\right)\log 3 + \left(\sum_{j=1}^4 \lambda_j\right)\log 5$$
   $$= -\frac{34}{15}\log 2 + 1\log 3 + 1\log 5 = \log 3 + \log 5 - \frac{34}{15}\log 2.$$

   Because $\{2, 3, 5\}$ are distinct primes, $\{\log 2, \log 3, \log 5\}$ are linearly independent over $\mathbb{Q}$.
   The coefficients $(1, 1, -34/15)$ are non-zero rationals.
   By Baker's Theorem (Anchor A1), $S(\rho_{S6})$ is transcendental!

#### Instance 2B: Maximally Mixed Qubit ($I_2 / 2$)
Consider the maximally mixed qubit state:
$$\rho_{\mathrm{mix}} = \frac{1}{2} I_2 = \mathrm{diag}\left(\frac{1}{2}, \frac{1}{2}\right) \in \mathrm{Herm}_2(\mathbb{Q}).$$
1. Rényi-2 purity:
   $$P_2(\rho_{\mathrm{mix}}) = \mathrm{Tr}\left(\left(\frac{1}{2}I_2\right)^2\right) = \left(\frac{1}{2}\right)^2 + \left(\frac{1}{2}\right)^2 = \frac{1}{4} + \frac{1}{4} = \frac{1}{2} \in \mathbb{Q}.$$
2. Von Neumann entropy:
   $$S(\rho_{\mathrm{mix}}) = -\left(\frac{1}{2}\log\frac{1}{2} + \frac{1}{2}\log\frac{1}{2}\right) = -\log\frac{1}{2} = \log 2.$$
   By Lindemann–Weierstrass (Anchor A2) or Baker (Anchor A1), $\log 2$ is transcendental!

**Comparative Significance:**
- Rényi integer-order purities $P_m = \mathrm{Tr}(\rho^m)$ are polynomial trace invariants computed by rational matrix multiplications and additions. They never leave the ground carrier field $K$:
  $$\text{renyi\_integer\_order\_carrier\_internal} = \mathrm{true}.$$
- In sharp contrast, von Neumann entropy $S(\rho)$ forces logarithmic evaluation across the spectrum. For every mixed state, it exits the carrier field entirely and lands in the transcendental numbers.
- Entropy and Rényi purity are structurally distinct mathematical objects: one is carrier-internal, the other is transcendental and must be refused or externally interfaced.

---

## 9. Claim Discipline Summary

| Item | Status / Finding | Evidence Anchor |
|---|---|---|
| $S(\rho) = 0 \iff \rho$ is pure | PROVED THEOREM | Elementary calculus & convexity on $[0, 1]$ |
| $S(\rho) > 0$ for all mixed $\rho$ | PROVED THEOREM | Non-negativity of $-\lambda \log \lambda$ |
| Reduction to $\mathbb{Q}$-independent logarithms | PROVED THEOREM | Prime valuation / abelian rank reduction |
| Non-vanishing of reduced form | PROVED THEOREM | $S(\rho) > 0$ prevents all $\Gamma_i = 0$ |
| $S(\rho)$ transcendental for mixed $\rho$ | PROVED THEOREM (CONDITIONAL) | Reduced form + Anchor A1 (Baker 1975) |
| Equality case $S(\rho) \in \mathbb{Q}(\zeta_n)$ | PURE_STATES_ONLY | Intersection of $\mathbb{Q}(\zeta_n)$ and transcendental set is $\emptyset$ |
| Vanishing linear form control | COUNTERMODEL | $\log 2 + \log 3 - \log 6 = 0$ |
| Rényi-2 purity of witness S6 | CARRIER-INTERNAL | $P_2 = 17/45 \in \mathbb{Q}$ |
| Entropy of witness S6 | TRANSCENDENTAL | $S(\rho) = \log 3 + \log 5 - (34/15)\log 2$ |

### What this artifact supports:
- Rigorous mathematical reduction connecting finite-dimensional density operators with algebraic spectra to Baker's theorem (Anchor A1).
- Unambiguous characterization of the equality case: entropy is carried if and only if the state is pure.
- Mathematical foundation for the exact 16-key result schema in Campaign C750 Block 01.

### What this artifact does not support:
- Does not prove Baker's theorem, Lindemann-Weierstrass, or Gelfond-Schneider (these are cited classical inputs).
- Does not claim that physical entropy cannot exist or that thermodynamics cannot be modeled; it shows that within the exact algebraic carrier $\mathbb{Q}(\zeta_n)$, entropy is not a carrier quantity for mixed states.
- Does not make any empirical assertions about physical laboratory systems.

### Narrowest Defensible Claim:
For any density operator $\rho$ on finite-dimensional Hilbert space whose spectrum consists of algebraic numbers, $S(\rho) = 0$ if and only if $\rho$ is pure ($\mathrm{Tr}(\rho^2) = 1$), and $S(\rho)$ is transcendental whenever $\rho$ is mixed. Consequently, $S(\rho) \in \mathbb{Q}(\zeta_n) \iff S(\rho) = 0 \iff \rho$ is pure.

### Next Test Needed:
Polyglot implementation and validation in Milestone M3:
- Python exact rational modules (`c750_b01_exact_solver.py`, `c750_b01_entropy_verdict.py`);
- Rust native BigRational implementation (`code_rs/src/c750_b01_entropy.rs`);
- Lean 4 formal reduction theorem with 0 sorry and 0 axioms (`C750B01Reduction.lean`).

