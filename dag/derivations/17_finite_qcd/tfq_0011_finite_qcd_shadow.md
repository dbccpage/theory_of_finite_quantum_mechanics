# [TFQ-0011] Finite QCD shadow

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `171bfea4-4046-5794-a9e5-ae2e8572b427`  
> **Parent Derivation**: [TFQ-0009](../14_finite_gauge/tfq_0009_finite_gauge_cochain.md)

---

## 1. Abstract & Formal Statement

In any group, the gauged four-edge product (a inverse, g, b) (b inverse, h, c) (c inverse, k, d) (d inverse, m, a) equals a inverse times (g h k m) times a. In S3 the transpositions of 0 with 1 and of 1 with 2 do not commute, and the product of the first transposition, the second, and two identity factors is not the identity. At color count 3 the channel formulae are C_F = 4/3, C_A = 3, singlet = -4/3, octet = 1/6, sextet = 1/3 and antitriplet = -2/3, the singlet is negative, and the octet is positive. The gluon split 4 C_A - C_A/3 equals 11, one Dirac flavor contributes -2/3, and the recorded abelian coefficient -4/3 is negative. With beta0(n_c, n_f) = (11/3) n_c - (2/3) n_f, the values beta0(3, n_f) at n_f = 0, 3, 5, 6, 16, 17 are 11, 9, 23/3, 7, 1/3, -1/3. For every rational n_f, beta0(3, n_f) > 0 if and only if n_f < 33/2, and beta0(3, n) > 0 for every natural n ≤ 16, while beta0(3, 17) < 0. With beta1(3, n_f) = 102 - (38/3) n_f, the values at n_f = 0, 5, 16 are 102, 116/3, -302/3, and (-beta0(3, 16)) / beta1(3, 16) = 1/302. For a nonzero rational b and natural numbers r, t at least 1, the Creutz ratio of the area monomials b^(r t) equals b, and the Creutz ratio of the perimeter monomials b^(2 (r + t)) equals 1. At b = 1/9 the area ratios on the pairs (2, 2) and (3, 3) equal 1/9, the perimeter ratios equal 1, and 1/9 is distinct from 1. The declared counts 9 and 12 satisfy 9 - 1 = 8, 12 - 9 + 1 = 4 and 12 - 8 = 4.

### Governing Obligation
Outside this certificate: continuum confinement, a string tension, the 12-decimal alpha_s and ln(9) strings, lattice Dirac doubling, an SU(3) matrix representation of the plaquette, and a constructed 3x3 complex with these counts. The route from TFQ-0009 stays a gap. Status stays OPEN.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
The finite certificate is `lean4/CampaignTfq0011FiniteQcd.lean`. It is not a continuum confinement theorem. The node stays OPEN.

### Sovereign Rust Certifiers
No Rust certifier is cited for this certificate.

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F002_continuum/floor.yaml`
