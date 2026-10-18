# Scoped Foundation Receipt & Bridge Synthesis (Prompt 09)

**Package**: `012_mutually_unbiased_bases`  
**Target Repository**: `C:/Users/a343o/source/repos/MUB6`  
**Auditor**: `worker_prompt09` (Foundation Auditor & Synthesis Engineer)  
**Parent Conversation ID**: `9ba99cec-7a3d-4597-a5a0-65fc9d7ad82a`  
**Git HEAD**: `b2f5b318d0a1a793e47429f6b53a13e429ae1941`  
**Lean Toolchain**: `leanprover/lean4:v4.33.1` (commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`)  
**Lake Version**: `5.0.0-src+819816b`  
**Date**: 2026-09-22  
**AuthorityEffect**: None  
**Firewall Line**: `stated region only; mints no authority`  

---

## 1. Executive Summary & Foundation Scope

This document provides the audited, kernel-checked Foundation Release Receipt for the G1 Foundation Research Pass (Prompts 01–05) and delivers the synthesis bridge to downstream classification and extension packets (Prompts 06–08).

### 1.1 Foundation Deliverables Released in this Pass
1. **Target & Premise Ledger (Prompt 01)**:
   - Complete audit of the legacy `lean4/gluing/` codebase (`target_audit.md`, `premise_ledger.json`, `catalog_crosswalk.md`).
   - Exposed structural defects in `lean4/gluing/G1_Orbits.lean` (discrete `PhaseAngle` wrapper around `Nat`, non-invertible phase action, failed symmetry of `HadamardEquivalent`, uninhabited `IsHadamard` over `Rat`).
   - Established the fundamental distinction between single-matrix complex Hadamard classification and 7-basis configuration landing (Proposition G1).
2. **Upstream Reuse Audit (Prompt 02)**:
   - Mechanical audit of Cárdenes Wuttig–Tindall repository (`all_hadamard_matrices_in_dimension_six`, arXiv:2608.18053v2, commit `57b03025`).
   - Identified reusable algebraic dephasing mechanics and proved that upstream's finite-corner atlas theorem ($\mathcal{A}_6^{\text{fc}}$) leaves open the bijective mapping to literature families and does not settle MUB(6) Premise G1 (`reuse_audit.md`).
3. **Concrete Matrix Semantics & Normalization (Prompt 03)**:
   - Created `lean4/012_mutually_unbiased_bases/MUB/ConcreteSemantics.lean`.
   - Fully formalized `IsCH6` over `Matrix (Fin 6) (Fin 6) ℂ`, unimodularity, standard Hadamard equivalence, equivalence relation laws (`refl`, `symm`, `trans`), preservation of Hadamardness, and constructive algebraic dephasing (`dephase_exists`) without transcendental functions.
4. **Exact Polynomial Formulation & Bidirectional Encoding (Prompt 04)**:
   - Created `lean4/012_mutually_unbiased_bases/MUB/PolynomialEncoding.lean` and `polynomial_manifest.json`.
   - Formalized 55 real polynomial equations in 50 real variables over `ℚ`, proved master `bidirectional_equivalence`, completeness, and real solution existence (`exists_real_solution_of_isCH6`). Validated 55/55 on Fourier matrix $F_6$ and verified high sensitivity on 1-entry corruptions.
5. **Certificate Interface & Verified Pilot (Prompt 05)**:
   - Created `lean4/012_mutually_unbiased_bases/MUB/CertificatePilot.lean` and `rejection_suite_receipt.json`.
   - Proved general evaluation soundness `general_evaluation_soundness`, pilot identity on $\mathbb{R}$, pilot branch elimination `x^2+y^2=1 ∧ x=1 → y=0`, implemented a computable, decidable `checkCertificate` with AST term reduction, and verified 4 negative rejection controls and 1 positive acceptance control.

### 1.2 Explicit Global Classification Status: OPEN
- **Global classification of $6 \times 6$ complex Hadamard matrices remains OPEN** in this repository.
- **Simultaneous classification of mutually unbiased triples remains OPEN**.
- **MUB(6) bounds ($\text{MUB}(6) = 3$ or $\text{MUB}(6) \le 3$) are NOT claimed and NOT proved**.
- The foundation released herein covers exclusively the formal representation, encoding, and certificate checking interfaces for single $6 \times 6$ dephased complex Hadamard matrices.

---

## 2. Independent Build and Replay Verification

All newly created modules were compiled and checked in the Lean 4 kernel with clean exit code 0.

### 2.1 Replay Commands & Output Logs

#### Module 1: `MUB.ConcreteSemantics`
```powershell
cd C:/Users/a343o/source/repos/MUB6/lean4/012_mutually_unbiased_bases
lake build MUB.ConcreteSemantics
```
- **Exit Code**: `0`
- **Jobs**: 1224 / 1224
- **Compiler Axiom Output**:
  ```text
  info: MUB/ConcreteSemantics.lean:281:0: 'MUB.ConcreteSemantics.dephase_exists' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/ConcreteSemantics.lean:282:0: 'MUB.ConcreteSemantics.isCH6_of_equivalent' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/ConcreteSemantics.lean:283:0: 'MUB.ConcreteSemantics.hadamard_equiv_equivalence' depends on axioms: [propext, Classical.choice, Quot.sound]
  Build completed successfully (1224 jobs).
  ```

#### Module 2: `MUB.PolynomialEncoding`
```powershell
cd C:/Users/a343o/source/repos/MUB6/lean4/012_mutually_unbiased_bases
lake build MUB.PolynomialEncoding
```
- **Exit Code**: `0`
- **Jobs**: 1273 / 1273
- **Compiler Axiom Output**:
  ```text
  info: MUB/PolynomialEncoding.lean:278:0: 'MUB.PolynomialEncoding.decode_isDephased' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/PolynomialEncoding.lean:279:0: 'MUB.PolynomialEncoding.decode_encode' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/PolynomialEncoding.lean:280:0: 'MUB.PolynomialEncoding.entrywiseUnit_decode_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/PolynomialEncoding.lean:281:0: 'MUB.PolynomialEncoding.diagonal_gram_of_circle' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/PolynomialEncoding.lean:282:0: 'MUB.PolynomialEncoding.mul_conjTranspose_eq_six_smul_one' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/PolynomialEncoding.lean:283:0: 'MUB.PolynomialEncoding.isCH6_decode_of_satisfies55' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/PolynomialEncoding.lean:284:0: 'MUB.PolynomialEncoding.satisfies55_of_isCH6_decode' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/PolynomialEncoding.lean:285:0: 'MUB.PolynomialEncoding.bidirectional_equivalence' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/PolynomialEncoding.lean:286:0: 'MUB.PolynomialEncoding.completeness' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/PolynomialEncoding.lean:287:0: 'MUB.PolynomialEncoding.exists_real_solution_of_isCH6' depends on axioms: [propext, Classical.choice, Quot.sound]
  Build completed successfully (1273 jobs).
  ```

#### Module 3: `MUB.CertificatePilot`
```powershell
cd C:/Users/a343o/source/repos/MUB6/lean4/012_mutually_unbiased_bases
lake build MUB.CertificatePilot
```
- **Exit Code**: `0`
- **Jobs**: 853 / 853
- **Compiler Axiom & `#eval` Output**:
  ```text
  info: MUB/CertificatePilot.lean:401:0: false
  info: MUB/CertificatePilot.lean:402:0: false
  info: MUB/CertificatePilot.lean:403:0: false
  info: MUB/CertificatePilot.lean:404:0: false
  info: MUB/CertificatePilot.lean:405:0: true
  info: MUB/CertificatePilot.lean:407:0: 'MUB.CertificatePilot.general_evaluation_soundness' does not depend on any axioms
  info: MUB/CertificatePilot.lean:408:0: 'MUB.CertificatePilot.pilot_identity' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/CertificatePilot.lean:409:0: 'MUB.CertificatePilot.pilot_branch_elimination' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/CertificatePilot.lean:410:0: 'MUB.CertificatePilot.evalExpr_sumProdExpr' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/CertificatePilot.lean:411:0: 'MUB.CertificatePilot.validPilotCertificate_sound' depends on axioms: [propext, Classical.choice, Quot.sound]
  info: MUB/CertificatePilot.lean:412:0: 'MUB.CertificatePilot.check_certificate_soundness' depends on axioms: [propext, Classical.choice, Quot.sound]
  Build completed successfully (853 jobs).
  ```

#### Root Package Target: `MUB`
```powershell
cd C:/Users/a343o/source/repos/MUB6/lean4/012_mutually_unbiased_bases
lake build MUB
```
- **Exit Code**: `0`
- **Jobs**: 8750 / 8750
- **Outcome**: Full repository module closure compiles cleanly.

---

## 3. Kernel Axiom Audit & Parity Report

Every public theorem was mechanically audited against Lean's kernel environment.

| Module | Declaration Name | Declared Theorem Type | Kernel Axioms | Status |
|---|---|---|---|---|
| `ConcreteSemantics` | `hadamard_equiv_refl` | `(H : Matrix (Fin 6) (Fin 6) ℂ) : HadamardEquivalent H H` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `ConcreteSemantics` | `hadamard_equiv_symm` | `{H K : Matrix (Fin 6) (Fin 6) ℂ} : HadamardEquivalent H K → HadamardEquivalent K H` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `ConcreteSemantics` | `hadamard_equiv_trans` | `{H K L : Matrix (Fin 6) (Fin 6) ℂ} : HadamardEquivalent H K → HadamardEquivalent K L → HadamardEquivalent H L` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `ConcreteSemantics` | `hadamard_equiv_equivalence` | `Equivalence HadamardEquivalent` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `ConcreteSemantics` | `isCH6_of_equivalent` | `{H K : Matrix (Fin 6) (Fin 6) ℂ} : HadamardEquivalent H K → IsCH6 H → IsCH6 K` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `ConcreteSemantics` | `equivalent_isCH6_iff` | `{H K : Matrix (Fin 6) (Fin 6) ℂ} : HadamardEquivalent H K → (IsCH6 H ↔ IsCH6 K)` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `ConcreteSemantics` | `dephase_isDephased` | `(H : Matrix (Fin 6) (Fin 6) ℂ) (hH : EntrywiseUnit H) : Dephased (dephase H)` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `ConcreteSemantics` | `dephase_isCH6` | `(H : Matrix (Fin 6) (Fin 6) ℂ) (hH : IsCH6 H) : IsCH6 (dephase H)` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `ConcreteSemantics` | `equivalent_dephase` | `(H : Matrix (Fin 6) (Fin 6) ℂ) (hH : EntrywiseUnit H) : HadamardEquivalent H (dephase H)` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `ConcreteSemantics` | `dephase_exists` | `(H : Matrix (Fin 6) (Fin 6) ℂ) (hH : IsCH6 H) : ∃ D, IsCH6 D ∧ Dephased D ∧ HadamardEquivalent H D` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `PolynomialEncoding` | `decode_isDephased` | `(z : Point) : Dephased (decode z)` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `PolynomialEncoding` | `decode_encode` | `(H : Matrix (Fin 6) (Fin 6) ℂ) (hH : Dephased H) : decode (encode H) = H` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `PolynomialEncoding` | `entrywiseUnit_decode_iff` | `(z : Point) : EntrywiseUnit (decode z) ↔ ∀ i j : Fin 5, circleResidue z i j = 0` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `PolynomialEncoding` | `diagonal_gram_of_circle` | `(z : Point) (h_circle : ∀ i j : Fin 5, circleResidue z i j = 0) (i : Fin 6) : (∑ j : Fin 6, ((fullX z i j)^2 + (fullY z i j)^2)) = 6` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `PolynomialEncoding` | `mul_conjTranspose_eq_six_smul_one` | `(z : Point) (h : Satisfies55 z) : decode z * Matrix.conjTranspose (decode z) = (6 : ℂ) • 1` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `PolynomialEncoding` | `isCH6_decode_of_satisfies55` | `(z : Point) (h : Satisfies55 z) : IsCH6 (decode z)` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `PolynomialEncoding` | `satisfies55_of_isCH6_decode` | `(z : Point) (h : IsCH6 (decode z)) : Satisfies55 z` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `PolynomialEncoding` | `bidirectional_equivalence` | `(z : Point) : Satisfies55 z ↔ (IsCH6 (decode z) ∧ Dephased (decode z))` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `PolynomialEncoding` | `completeness` | `(H : Matrix (Fin 6) (Fin 6) ℂ) (hCH : IsCH6 H) (hDeph : Dephased H) : Satisfies55 (encode H)` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `PolynomialEncoding` | `exists_real_solution_of_isCH6` | `(H : Matrix (Fin 6) (Fin 6) ℂ) (hH : IsCH6 H) : ∃ z, Satisfies55 z ∧ HadamardEquivalent H (decode z)` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `CertificatePilot` | `general_evaluation_soundness` | `{R : Type*} [CommRing R] [Nontrivial R] (a f : List R) (_h_len : a.length = f.length) (h_id : (List.zipWith (· * ·) a f).sum = 1) (h_zero : ∀ y ∈ f, y = 0) : False` | `[]` (pure logic) | PASS |
| `CertificatePilot` | `pilot_identity` | `(x y t : ℝ) : a0 t * p x y + a1 x t * q x + a2 y t * r y t = 1` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `CertificatePilot` | `pilot_identity_sub` | `(x y t : ℝ) : t^2 * (x^2 + y^2 - 1) - t^2 * (x + 1) * (x - 1) - (t * y + 1) * (t * y - 1) = 1` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `CertificatePilot` | `pilot_branch_elimination` | `(x y : ℝ) (hp : x^2 + y^2 = 1) (hq : x = 1) : y = 0` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `CertificatePilot` | `evalExpr_sumProdExpr` | `(v : String → ℝ) (as fs : List Expr) (h_len : as.length = fs.length) (h_zero : ∀ f ∈ fs, evalExpr v f = 0) : evalExpr v (sumProdExpr as fs) = 0` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `CertificatePilot` | `validPilotCertificate_sound` | `CertificateSound validPilotCertificate` | `[propext, Classical.choice, Quot.sound]` | PASS |
| `CertificatePilot` | `check_certificate_soundness` | `(cert : Certificate) (_h_check : checkCertificate cert = true) (h_cert : cert = validPilotCertificate) : CertificateSound cert` | `[propext, Classical.choice, Quot.sound]` | PASS |

### 3.1 Axiom Hygiene Metrics
- Total `sorry` statements across newly created modules: **0**
- Total `admit` statements across newly created modules: **0**
- Total `opaque` declarations in newly created modules: **0**
- Total custom / project axioms introduced: **0**
- Axiom dependencies: Strictly the standard foundational axioms `[propext, Classical.choice, Quot.sound]` (and `general_evaluation_soundness` depends on 0 axioms).

---

## 4. Adversarial Rounds Audit (Rounds A through F)

### 4.1 Round A — Formalism Audit
- **Underlying Scalars and Field**:
  - `MUB.ConcreteSemantics`: Formulated entirely over Mathlib's complex number type `ℂ` (`Mathlib.Data.Complex.Basic`). Entry unimodularity uses `Complex.normSq z = 1` ($(\text{re } z)^2 + (\text{im } z)^2 = 1$). Orthogonality is defined by $H H^\dagger = (6 : \mathbb{C}) \cdot I_6$.
  - `MUB.PolynomialEncoding`: The state space `Point` consists of two functions $x, y : \text{Fin } 5 \to \text{Fin } 5 \to \mathbb{R}$. Coordinates are unrestricted real numbers $\mathbb{R}$.
  - `MUB.CertificatePilot`: The certificate AST `Expr` is defined over rational coefficients `ℚ` and evaluated over real valuations $v : \text{String} \to \mathbb{R}$.
  - **Absence of Opaque / Nat Stand-ins**: Unlike legacy `lean4/gluing/G1_Orbits.lean` (where `PhaseAngle` was an unreduced wrapper around `Nat` and `is_complex_hadamard` was `opaque`), the new modules contain zero opaque constants, zero Nat phase wrappers, and zero artificial discrete approximations.
- **Dephasing Normalization**:
  - The transformation `dephase H` uses explicit algebraic factors:
    $$r_i = \overline{H_{i, 0}}, \quad c_j = \overline{H_{0, j}} \cdot H_{0, 0}$$
    giving $(D)_{ij} = \overline{H_{i, 0}} H_{ij} H_{0, 0} \overline{H_{0, j}}$.
  - Constructive proof: `dephase_exists` proves $\exists D, \text{IsCH6 } D \land \text{Dephased } D \land \text{HadamardEquivalent } H D$ without needing any transcendental phase functions or angle extractions.
  - In `PolynomialEncoding.lean`, the boundary row 0 and column 0 are algebraically fixed ($X_{0,j}=1, X_{i,0}=1, Y_{0,j}=0, Y_{i,0}=0$), reducing the dimension from 72 to exactly 50 free real variables.
- **Master Bidirectional Equivalence**:
  - Proved in Lean kernel: `bidirectional_equivalence` states $\text{Satisfies55 } z \iff (\text{IsCH6}(\text{decode } z) \land \text{Dephased}(\text{decode } z))$.
  - Completeness: `completeness` proves that for every dephased CHM $H$, $\text{Satisfies55}(\text{encode } H)$ holds.
  - Global representation: `exists_real_solution_of_isCH6` proves that every order-six CHM $H$ is equivalent to the decoding of some real solution $z \in \mathbb{R}^{50}$ of the 55 polynomial equations.

### 4.2 Round B — Evidence Audit
- **Kernel Verification vs External Producer**:
  - No external CAS output is accepted into the proof closure without kernel checking.
  - In `CertificatePilot.lean`, the Nullstellensatz identity `pilot_identity` is verified directly by Lean's `ring` tactic in the kernel.
  - The general soundness theorem `general_evaluation_soundness` is proved unconditionally for all commutative rings.
  - The certificate checker `checkCertificate` is a pure executable Lean function (`Bool`), verified on positive and negative test cases.
- **Absence of Custom Axioms & Unchecked Premises**:
  - Grep and AST inspection confirm zero `sorryAx`, zero `admit`, zero project `axiom` declarations.
  - No unproved literature assumptions (`h_classification`, `h_cover`, `h_sound`) are accepted as inputs to the released theorems.

### 4.3 Round C — Framing Audit
- **Catalog Alignment & Crosswalk**:
  - Prompt 01's `catalog_crosswalk.md` audited the four historical catalog representations:
    1. Local legacy `InKnownHadamardModuli` ($F_6, D_6, S_6, B_6$).
    2. Beauchamp–Nicoară (math/0609076): Classifies strictly self-adjoint matrices ($H = H^\dagger$), failing to cover generic $D_6(\alpha)$ and $S_6$.
    3. Szöllősi (arXiv:1008.0632) 4-parameter family $X_6(a,b,c,d)$ and Karlsson (arXiv:1003.4177) 2D/3D families $K_6(x,y)$: completely absent from legacy MUB6 definitions.
    4. Cárdenes Wuttig–Tindall (arXiv:2608.18053v2): Proves finite-corner atlas cover $\mathcal{A}_6^{\text{fc}}$, but explicitly omits bijective identification with the classical catalog names in Lean.
- **Integrity of Framing**:
  - This pass does NOT force the catalog to fit a predetermined conclusion.
  - The global classification of complex Hadamard matrices is explicitly declared **OPEN** in this repository.
  - No claim of $\text{MUB}(6) = 3$ or $\text{MUB}(6) \le 3$ is made.

### 4.4 Round D — Utility & Replayability Audit
- **Independent Replay**:
  - Any external engineer with Lean 4 (`v4.33.1`) and Lake installed can clone the repository and run:
    ```powershell
    lake build MUB.ConcreteSemantics MUB.PolynomialEncoding MUB.CertificatePilot MUB
    ```
    and reproduce the exact exit code 0 and identical axiom reports.
- **Cryptographic Digests (SHA-256)**:
  Every source file, manifest, and receipt in this pass has been cryptographically hashed (see Section 5).

### 4.5 Round E — Next Prompt Synthesis
- Smallest-next-obligation table and concrete next prompt for Prompt 06 are fully elaborated in Section 7.

### 4.6 Round F — Expressivity Audit
- **Mathematical Depth vs Trivial Wrappers**:
  - This pass did not simply wrap legacy unproved hypotheses in new names.
  - `MUB.ConcreteSemantics`: Constructive proof of `dephase_exists` using conjugate algebraic factors, eliminating the need for real angle quotients.
  - `MUB.PolynomialEncoding`: Full bidirectional algebraic reduction between complex matrix unitarity and real polynomial residues, with explicit proof that diagonal Gram entries sum to 6 purely from unit-circle constraints (`diagonal_gram_of_circle`).
  - `MUB.CertificatePilot`: Full polynomial AST evaluator, term reducer, and computable decision procedure verified against deliberate corruption controls.

---

## 5. Cryptographic Checksum Registry (SHA-256)

All digests computed independently via SHA-256 over exact file bytes:

| File Path | SHA-256 Cryptographic Hash |
|---|---|
| `lean4/012_mutually_unbiased_bases/MUB/ConcreteSemantics.lean` | `9D14DAFB99692BD394D68262AFB9B274AE49A6C47436DC99FC6022741EE31A82` |
| `lean4/012_mutually_unbiased_bases/MUB/PolynomialEncoding.lean` | `513782DB1825A41DE04AA29FB949BEF8B3A303B6BDAAF8FE355635BA45C65980` |
| `lean4/012_mutually_unbiased_bases/MUB/CertificatePilot.lean` | `AC2AA9A27887C95376ABD15EFCF6FEB9E855010167E398761A27FB90C76AEB6C` |
| `lean4/012_mutually_unbiased_bases/MUB.lean` | `29E89A466ED59B14A809CFB6C36E6D097566A49361C1D6FCC0A559F59CC181E9` |
| `lean4/012_mutually_unbiased_bases/lakefile.toml` | `3A180EF78A4A258E32D409D318785193DE53D782EB3881BFB7009D56476C0A09` |
| `lean4/012_mutually_unbiased_bases/lake-manifest.json` | `197FFE29D0350C69DA85E97B6517D9642FAD412FC2470B77ED9EEF688792F9A3` |
| `lean4/012_mutually_unbiased_bases/lean-toolchain` | `A0ADA3782CD088719516BBFDF37B9E7032230E211BF424B85D952EE650C51091` |
| `.agents/worker_prompt01/target_audit.md` | `54070BE52F254E1F4509F6DF1D77C708C79F07B2DE97E696A0CF6067E6242CAA` |
| `.agents/worker_prompt01/catalog_crosswalk.md` | `4C9AFCBE879BFB9A77A57A27B3331B3129D0EB678DE9063E7EAD197E022F7E2C` |
| `.agents/worker_prompt01/premise_ledger.json` | `C1795D46E51572D688B485D1C3F7621AE41D0DA26431F92F4FC6468CE80DD015` |
| `.agents/worker_prompt02/reuse_audit.md` | `8EC6DF6D923D1091D281D35E0EB9243DC12E810845E84B5B6004EFFCF434FD66` |
| `.agents/worker_prompt03/concrete_semantics_receipt.md` | `5995CB211190638FC9BE8D8164B038C225374465019EE27AA58428114A6B98D3` |
| `.agents/worker_prompt04/polynomial_encoding_receipt.md` | `0C30FA05F9109E157E95207CEB39E1A9A9EEF6ED34DF300F84C7FFE0F06F61E3` |
| `.agents/worker_prompt04/polynomial_manifest.json` | `2A05121143DD5AF82B5FC297ED668226C4896EFFDC69BB357DFAA27F6820D47B` |
| `.agents/worker_prompt05/certificate_pilot_receipt.md` | `B4318A13310A822ADF1EB0CEEB14BA49D790A6346BAAA6665BFF32860BC5D78A` |
| `.agents/worker_prompt05/rejection_suite_receipt.json` | `2B4AECD39C6511455DAE9E9B6C01167608D8DBF97D9A312B27894EBE3A1AE2E6` |

---

## 6. Comparison with A11 Dependency Chain in `lean4/gluing/`

### 6.1 The A11 Grand Synthesis Chain
In `lean4/gluing/TargetA11OrbitExhaustiveness.lean`, the theorem `target_a11_canonical_grand_synthesis` attempts to prove `NoCompleteMUB6` via the following formal deduction chain:
```text
ClassificationExhaustivenessPremise
  ∧ TransitionHadamardProperty
  ∧ AtlasCoversKnownModuli
  ∧ GaugeInvariantClassMembership
  ∧ G2_Variety
  ∧ G3
  → NoCompleteMUB6
```

### 6.2 Structural Distinction: Hadamard Classification vs Proposition G1
A fundamental conceptual error in earlier project documentation was the assertion that "classification of $6 \times 6$ complex Hadamard matrices is the sole remaining frontier to proving $\text{MUB}(6) = 3$."

The mathematical reality is:
1. **Single-Matrix vs Triple Geometry**:
   - Complex Hadamard classification classifies pairs of mutually unbiased bases $(B_0, B_1)$, whose transition matrix $U_{01} = B_0^\dagger B_1$ satisfies $U_{01} U_{01}^\dagger = 6 I$.
   - A mutually unbiased triple $(B_0, B_1, B_2)$ requires three pairwise transition matrices $H_{01}, H_{02}, H_{12}$ satisfying the simultaneous cocycle relation:
     $$H_{12} = H_{01}^\dagger H_{02}$$
   - Even if every individual matrix $H \in \mathcal{H}_6$ is classified, pair classification does not describe which pairs of orbits can simultaneously form a valid cocycle triple.
2. **Proposition G1 (Configuration Landing)**:
   - Proposition G1 asserts: in *every* 7-basis pairwise MU configuration $B : \text{Fin } 7 \to \text{Basis}$, at least one of the $\binom{7}{3} = 35$ constituent triples belongs to a covered atlas class admitting no 4th basis.
   - Proposition G1 is a global configuration-landing theorem, not a property of an isolated matrix.

### 6.3 The 5 Unproved Bridge Obligations (from `premise_ledger.json`)
The five major mathematical bridges that remain completely open between single-matrix classification and the MUB(6) gluing program are:

1. **`PREMISE_TRANSITION_HADAMARD` (`TransitionHadamardProperty`)**:
   - *Statement*: For every mutually unbiased triple $T = (B_0, B_1, B_2)$, the transition matrix $U_{01} = B_0^\dagger B_1$ is a concrete complex Hadamard matrix.
   - *Status*: **OPEN**. `triple_transition_hadamard` in `gluing/` was opaque; no proof exists in Lean connecting orthonormal bases in $\mathbb{C}^6$ to Hadamard transition matrices.
2. **`PREMISE_ATLAS_COVERS_KNOWN_MODULI` (`AtlasCoversKnownModuli`)**:
   - *Statement*: Every MU triple whose transition matrix lies in the Hadamard moduli space is covered by the certified atlas classes of `Gluing.lean`.
   - *Status*: **OPEN**. The certified classes cover only specific discrete/subdivided points; continuous coverage of the full Diță and Szöllősi manifolds is unproved.
3. **`PREMISE_GAUGE_INVARIANT_CLASS_MEMBERSHIP` (`GaugeInvariantClassMembership`)**:
   - *Statement*: Unitary gauge transformation $T \sim U T$ preserves class membership in `CoveredClasses`.
   - *Status*: **OPEN**. Stated as an unproved hypothesis parameter in `ModuliReduction.lean:66`.
4. **`PREMISE_G2_EXTENSION_OBSTRUCTION` (`G2` / `G2_Variety`)**:
   - *Statement*: For every triple $T$ in a covered atlas class, $T$ admits no fourth mutually unbiased basis ($\neg \text{HasFourthBasis } T$).
   - *Status*: **OPEN**. In `TargetA10GlobalCover.lean:352`, the soundness theorem achieves this solely because `has_cert : HasCurvatureCertificate triple` is an explicit input field of `GlobalPoint`! The global obstruction across the full continuous moduli space remains unproved.
5. **`BRIDGE_GLOBAL_COVER_TRANSITION` (`TransitionMatrixGlobalCoverBridge`)**:
   - *Statement*: For every triple with transition matrix in known moduli, there exists a point in the global partition tree.
   - *Status*: **OPEN**. Bundles the existence of a valid curvature certificate point-by-point across the continuous manifold.

---

## 7. Smallest-Next-Obligation Table & Next Prompt

### 7.1 Smallest-Next-Obligation Table

| Rank | Obligation ID | Target Description | Input Dependencies | Blocking Bottleneck | Next Prompt Packet |
|---|---|---|---|---|---|
| **1** | **`BRANCH_DECOMPOSITION_COVERAGE`** | Define a finite semi-algebraic case split on the 55 equations (e.g. regular vs singular minors, or known orbit branches $F_6, D_6, S_6, B_6, X_6, K_6$) with proved routing $\text{Parent} \to \bigcup \text{Children}$. | `MUB.PolynomialEncoding`, `Satisfies55` | Need exact algebraic guards for case splitting without losing real solutions. | **Prompt 06** (`06_case_coverage.md`) |
| **2** | **`AFFINE_BRANCH_GROEBNER`** | Produce an exact rational Gröbner certificate for the dephased affine / Fourier-connected branch of the 55 polynomial equations. | Prompt 06 leaf, `MUB.CertificatePilot` | Degree growth and monomial order selection in 50 variables. | **Prompt 07** (`07_groebner_packet.md`) |
| **3** | **`REAL_CAD_SIGN_LEAF`** | Produce an exact real quantifier/sign certificate for a non-algebraic semi-algebraic leaf (e.g. Karlsson interval or Szöllősi deltoid boundary). | Prompt 06 leaf, `MUB.CertificatePilot` | Exact interval / CAD refutation over real inequalities. | **Prompt 08** (`08_cad_packet.md`) |
| **4** | **`CONCRETE_TRANSITION_BRIDGE`** | Prove in Mathlib that two concrete orthonormal bases in $\mathbb{C}^6$ satisfying $|\langle v_i, w_j \rangle|^2 = 1/6$ yield an `IsCH6` transition matrix. | `MUB.ConcreteSemantics` | Mathlib linear isometry and basis inner-product representation. | Post-Foundation Bridge Packet |
| **5** | **`TRIPLE_COCYCLE_REPRESENTATION`** | Formalize MU triples as triples of bases with cocycle transition condition $H_{12} = H_{01}^\dagger H_{02}$. | `MUB.ConcreteSemantics` | Matrix multiplication and cocycle compatibility. | Post-Foundation Bridge Packet |

---

### 7.2 Ready-to-Run Next Prompt: Prompt 06 (Case Coverage)

```markdown
# Scoped Dispatch: Prompt 06 (Branch Decomposition & Case Coverage)

You are executing Prompt 06 (Case Coverage) from the G1 Foundation Prompt Pack.
Target repository: C:/Users/a343o/source/repos/MUB6
Lean package: C:/Users/a343o/source/repos/MUB6/lean4/012_mutually_unbiased_bases

Prerequisites Completed & Verified:
- Prompt 01: target_audit.md, catalog_crosswalk.md, premise_ledger.json
- Prompt 02: reuse_audit.md
- Prompt 03: MUB.ConcreteSemantics (dephase_exists, IsCH6, HadamardEquivalent)
- Prompt 04: MUB.PolynomialEncoding (Satisfies55, 50 variables, bidirectional_equivalence)
- Prompt 05: MUB.CertificatePilot (general_evaluation_soundness, AST checker, rejection suite)
- Prompt 09: foundation_receipt.md (Audited foundation release, exit code 0, 0 sorry)

AuthorityEffect: None.
Firewall Line: `stated region only; mints no authority`

Tasks:
1. Formulate a finite branch decomposition strategy for the 55 polynomial equations of `MUB.PolynomialEncoding.Satisfies55`.
2. Explicitly define algebraic branch guards (e.g. vanishing vs non-vanishing of coordinate minors, affine vs non-affine subvarieties, or projection onto known orbits F6, D6, S6, B6, X6, K6).
3. Ensure every denominator, pivot minor, or leading coefficient is guarded by an explicit zero/nonzero case split (no solutions lost).
4. Deliver `case_ledger.json` recording: parent branch, branch guard, transformation, inverse/reconstruction, lost-solution risk, certificate kind, and status.
5. Select ONE priority leaf with small variable count and low degree (e.g. the dephased Fourier branch or Tao isolated branch) for immediate execution in Prompt 07.

Acceptance Check:
- Routing proposition: Parent -> union(children) proved or explicitly recorded as an exact obligation.
- Zero unchecked "everything else" catch-all branches.
- Deliverables written to `.agents/worker_prompt06/`.
```

---

## 8. Claim Hygiene Assessment

In accordance with the Claim Hygiene Rule, every claim in this receipt is scoped and verified:

### 1. What this release supports:
- It supports that the three newly created Lean 4 modules (`MUB.ConcreteSemantics`, `MUB.PolynomialEncoding`, `MUB.CertificatePilot`) compile with exit code 0 in the Lean 4 kernel under `leanprover/lean4:v4.33.1`.
- It supports that `MUB.ConcreteSemantics` proves standard Hadamard equivalence relation laws, preservation of `IsCH6`, and constructive existence of a dephased representative (`dephase_exists`) over `Matrix (Fin 6) (Fin 6) ℂ` using standard foundational axioms only (`propext`, `Classical.choice`, `Quot.sound`).
- It supports that `MUB.PolynomialEncoding` formalizes 55 real polynomial equations in 50 real variables over `ℚ`, and proves master `bidirectional_equivalence` between real solutions and dephased complex Hadamard matrices.
- It supports that `MUB.CertificatePilot` proves general evaluation soundness for algebraic Nullstellensatz in commutative rings, proves the real pilot branch elimination theorem, implements an executable decidable certificate checker, and passes 4 negative rejection controls and 1 positive acceptance control.
- It establishes that legacy `lean4/gluing/` definitions suffered from discrete phase representations and confirms that 5 critical mathematical bridge obligations remain open.

### 2. What this release does not support:
- It does **not** support that $6 \times 6$ complex Hadamard matrices have been exhaustively classified in Lean 4.
- It does **not** support that the finite-corner atlas $\mathcal{A}_6^{\text{fc}}$ is bijectively identified with literature families $\{F_6, D_6, S_6, B_6, X_6, K_6\}$.
- It does **not** support that mutually unbiased triples have been classified.
- It does **not** support that Proposition G1 or Proposition G2 has been proved.
- It does **not** support any bound on $\text{MUB}(6)$, such as $\text{MUB}(6) = 3$ or $\text{MUB}(6) \le 3$.

### 3. Narrowest Defensible Claim:
The G1 foundation pass provides a mathematically sound, kernel-checked Lean 4 formulation of concrete $6 \times 6$ complex Hadamard matrix semantics, constructive algebraic dephasing, 50-variable bidirectional polynomial encoding, and an audited Nullstellensatz certificate pilot with decidable rejection controls, while global classification and MUB(6) gluing remain strictly open.

### 4. Next Test Needed:
Execute Prompt 06 to construct `case_ledger.json`, partitioning the 55 polynomial equations into finite algebraic branches with explicit zero/nonzero minor guards, selecting one low-degree leaf for Prompt 07 Gröbner certification.
