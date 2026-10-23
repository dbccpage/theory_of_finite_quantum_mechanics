# Example prompts: seven small finite nodes

**AuthorityEffect:** None. A prompt run produces a proposal that the host checks. It does not prove a node and never changes a status.

These are starting points for anyone who wants to run the project's prompt tooling on a small, exact, finite claim and submit the record. Each node below is in [`dag/derivation_dag.json`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/derivation_dag.json) with status `COMPUTATIONALLY_CHECKED` and **no Lean proof**: an exact finite computation exists, and a Lean statement or an independent check does not. Each has a staged prompt in `dag/prompts/` and has been run before, so the packet is grounded in real source declarations and the ladder will not skip it. All seven were checked with `--dry-run` (no provider call) before this page was written. Earlier ladder runs of nodes 1, 5, 6 and 7 ended `not_accepted`, and nodes 2, 3 and 4 were accepted at P0 (this says only that the host checks passed, as explained in [`CONTRIBUTING.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/CONTRIBUTING.md)). Your run may differ.

Why not the frontier targets? The fourteen finite frontier targets (constructor theory, causal QFT, AdS/CFT, loop quantum gravity) already have Lean modules, and their statements were narrowed to what those modules prove (3 full, 11 narrowed). They need review more than prompting. See [`REVIEWING.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/REVIEWING.md).

## Before you run any of them

1. Read [`CONTRIBUTING.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/CONTRIBUTING.md) once, in particular the honesty rules.
2. Install: Python 3.11 or later and `pip install pyyaml sympy` (add `anthropic` only for the Anthropic tiers). No Lean, Rust or Cargo is needed for anything on this page.
3. Fork, clone, and make a branch such as `community/alice/dfm-bphz-sector-kernel` (use your GitHub handle and the node you chose).
4. Put the key for **your own** provider in the environment or in a git-ignored `.env` file. The ladder reads `GROQ_API_KEY` and `OPENROUTER_API_KEY` (both have free models) and `ANTHROPIC_API_KEY` (paid). It never prints, writes or copies a key. If you have no key, use the by-hand route below.

### The cheap ladder, with your own key

The commands in this section use `DFM-BPHZ-SECTOR-KERNEL` as the worked example. **Replace it with the id of the node you chose.** Do not type angle brackets into a shell: `<` is redirection. Preview first. This needs no key, calls nothing and writes nothing:

```
python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node DFM-BPHZ-SECTOR-KERNEL --stage P0 --max-cost-usd 0.10 --max-tier 1 --dry-run
```

Then run it. `--max-tier 1` allows the free models and one paid OpenRouter model (`gpt-4o-mini`); it never reaches an Anthropic tier. `--ledger` points the budget ledger at a file outside the repository (here, the parent directory), so that the tracked ledger is not modified:

```
python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node DFM-BPHZ-SECTOR-KERNEL --stage P0 --max-cost-usd 0.10 --max-tier 1 --ledger ../tfqm-ledger.json
```

- Free models only: add `--max-tier 0` and use `--max-cost-usd 0`.
- Anthropic models: raise `--max-tier` (2 is Haiku, 3 is Sonnet, 4 is Opus). The pilot in [`DESIGN.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/pfp/llm_ladder/DESIGN.md) (section 13) measured about 0.002 USD for one Haiku call and about 0.02 USD for one Sonnet call on a comparable node. Keep the cap small.
- `--max-cost-usd` is a hard cap on paid calls in the run: the worst case of each call is reserved before it is sent. The ledger rates cost from provider usage and is not an invoice; check your provider's dashboard.
- The command prints a JSON summary and exits with 0 for `accepted`, 3 for `accepted_partial`, 4 for `skipped_ungroundable` and 1 otherwise.

### By hand, with any model

1. Open the prompt file named under the node. Copy the `system_prompt` block and the `user_prompt` block into the model of your choice, as a system and a user message.
2. Record the reply as a run folder in the same tree the ladder uses, named `<UTC date and time>_byhand_<your handle>`. For example, for the worked-example node, handle `alice` and 23 October 2026, 10:15 UTC: `dag/results/DFM-BPHZ-SECTOR-KERNEL/runs/20261023T101500Z_byhand_alice/`. Put the reply there, **unmodified**, as `reply.txt`.
3. Next to it, write `NOTES.md` with the model name and version, the date, any settings, and what you checked yourself.

Do not put replies under `docs/`: that directory is the source of the published site, and a model reply that contains <code>&#123;&#123;</code> or <code>&#123;%</code> (Liquid template markers) would break its build. A by-hand reply is not host-verified. It is recorded as an unverified proposal. Ladder tools ignore folders that do not end in `_ladder`, and the campaign queue does not count a `_byhand_` folder as an attempt.

### What the ladder writes

A ladder run writes `dag/results/DFM-BPHZ-SECTOR-KERNEL/runs/<UTC stamp>_ladder/` (for your node, its own id): `ladder_receipt.json` (every provider call, with tokens and rated cost), `p0/request.json`, `p0/raw_response.json`, `p0/candidate.json`, `p0/host_check.json`, `p0/operad_delta.yaml` and `p0/attempts/`. As side effects it also edits two shared files, the negative-entry index `dag/operads/_hallucination_index.json` and, unless you used `--ledger`, `dag/pfp/llm_ladder/budget_ledger.json`. **Do not submit those two.** Restore them before you commit; the maintainer integrates the index after review (the repository has a script that rebuilds it from the stored runs).

### How to verify a result locally

- Read `p0/host_check.json`: `status`, `predicate_results.verified_total`, `failed_total` and `failures_by_class`. These are the host's counts, not the model's. (A by-hand reply has no such file.)
- For every entry in `p0/operad_delta.yaml` that cites a declaration, open the cited file and confirm that the declaration is there and says what the entry claims. The host checks that a declaration exists; it cannot check that it means what the model says it means.
- Run the independent check under the node below. It does not use the repository or the model, and it should agree with the node statement.
- `python -I -X utf8 dag/validate_derivation_dag.py --no-files` must print `failures=0`. A prompt-result pull request changes no DAG data, so this guards against accidents.
- Optional and slow: `python -I -X utf8 dag/pfp/llm_ladder/replay.py --report` re-checks every stored attempt in the repository with the current verifier, without calling any provider. It reads the whole archive and takes minutes.

### How to open the pull request

Replace the node id, the folder name and the handle with your own:

```
git restore dag/operads/_hallucination_index.json dag/pfp/llm_ladder/budget_ledger.json
git add dag/results/DFM-BPHZ-SECTOR-KERNEL/runs/20261023T101500Z_ladder
git status
git commit -m "Prompt result: DFM-BPHZ-SECTOR-KERNEL (P0, free tier)"
git push -u origin community/alice/dfm-bphz-sector-kernel
```

`git status` must show only your run folder. If it shows `.env`, a ledger, the shared index or anything else, unstage it.
Open the pull request against `main` and fill in the template. The outcome class is **Prompt result**. In the statement-versus-theorem table, write "not proved" for every claim, because a P0 run proves nothing. Say what the run did not establish. If you would rather not use a pull request, open a *Prompt result* issue and attach the files.

---

## 1. `DFM-BPHZ-SECTOR-KERNEL`

- **Stage / status:** `DRESSING_FIELD`, `COMPUTATIONALLY_CHECKED`.
- **Statement.** For the kernel K(z; λ) = (1 + zλ) / (λ(1 + λ)) at z = 3/5, the four-term sum K₁(z)K₂(z) − K₁(z)K₂(0) − K₁(0)K₂(z) + K₁(0)K₂(0) equals (z/(1+λ₁))(z/(1+λ₂)) at nine rational pairs (λ₁, λ₂), with formal value z² = 9/25 at (0, 0).
- **Scope, from the node.** The identity is distributivity on one declared toy kernel. It is not Zimmermann's forest formula on a Feynman integrand and fixes no renormalization scheme.
- **Prompt file:** [`dag/prompts/dressing_field_dfm_bphz_sector_kernel_computationally_checked.yaml`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/prompts/dressing_field_dfm_bphz_sector_kernel_computationally_checked.yaml). Derivation note: [`tfq_1109_dfm_bphz_sector_kernel.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/derivations/24_dressing_field/tfq_1109_dfm_bphz_sector_kernel.md).
- **Command:** `python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node DFM-BPHZ-SECTOR-KERNEL --stage P0 --max-cost-usd 0.10 --max-tier 1 --ledger ../tfqm-ledger.json`
- **A valid result** names the kernel and the four-term combination as typed operations, states the identity K(z; λ) − K(0; λ) = z/(1 + λ) as a relation with its hypothesis (λ ≠ 0, λ ≠ −1), and lists in `open_obligations` that this is not a forest formula. Any numeric claim must recompute exactly. A reply that claims a renormalization result fails the scope check above.
- **Check it yourself:**

```python
from sympy import symbols, Rational, simplify
z, l1, l2 = symbols('z l1 l2')
K = lambda zz, l: (1 + zz * l) / (l * (1 + l))
lhs = K(z, l1) * K(z, l2) - K(z, l1) * K(0, l2) - K(0, l1) * K(z, l2) + K(0, l1) * K(0, l2)
assert simplify(lhs - z**2 / ((1 + l1) * (1 + l2))) == 0
print("identity holds for all z, l1, l2; value at z=3/5, formal (0,0):", Rational(3, 5) ** 2)
```

## 2. `PGW-PFP-C4-CERTIFICATE`

- **Stage / status:** `IMPLEMENTATION`, `COMPUTATIONALLY_CHECKED`.
- **Statement.** On the oriented 4-cycle with edges 01, 12, 23, 03, one face 01 + 12 + 23 − 03 and c = (2, −3, 5, 7): the potential a = (0, 2, −1, 4) leaves residual r = (0, 0, 0, 3) of L¹ norm 3 (an upper bound); the dual w = (−1, −1, −1, 1) is feasible and gives the lower bound w·c = 3; so φ₁ = 3. The face row d₁ = (1, 1, 1, −1) satisfies d₁d₀ = 0 and d₁c = −3, so γ₂ = 3.
- **Scope, from the node.** A finite certificate for one supplied complex. It does not hold on all complexes or norms, and it supplies no Hilbert space, Born rule or authorization.
- **Prompt file:** [`dag/prompts/implementation_pgw_pfp_c4_certificate_computationally_checked.yaml`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/prompts/implementation_pgw_pfp_c4_certificate_computationally_checked.yaml). Derivation note: [`tfq_0509_pfp_c4_certificate.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/derivations/04_authorization/tfq_0509_pfp_c4_certificate.md).
- **Command:** `python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node PGW-PFP-C4-CERTIFICATE --stage P0 --max-cost-usd 0.10 --max-tier 1 --ledger ../tfqm-ledger.json`
- **A valid result** separates the primal bound (residual) from the dual bound (feasible w), states weak duality as the relation that makes φ₁ = 3, and lists as open that nothing here generalises beyond this complex. Every number it quotes must recompute.
- **Check it yourself:**

```python
from sympy import Matrix
d0 = Matrix([[-1, 1, 0, 0], [0, -1, 1, 0], [0, 0, -1, 1], [-1, 0, 0, 1]])  # edges 01,12,23,03; (d0 a)_e = a_head - a_tail
d1 = Matrix([[1, 1, 1, -1]])
c = Matrix([2, -3, 5, 7]); a = Matrix([0, 2, -1, 4]); w = Matrix([-1, -1, -1, 1])
r = c - d0 * a
assert list(d0 * a) == [2, -3, 5, 4] and list(r) == [0, 0, 0, 3] and sum(abs(x) for x in r) == 3
assert max(abs(x) for x in w) == 1 and list(d0.T * w) == [0, 0, 0, 0] and (w.T * c)[0] == 3
assert list(d1 * d0) == [0, 0, 0, 0] and (d1 * c)[0] == -3
# weak duality: for every potential a, |c - d0 a|_1 >= w.(c - d0 a) = w.c - (d0^T w).a = 3
print("C4 certificate: upper bound 3 = dual lower bound 3; d1 d0 = 0; d1 c = -3")
```

## 3. `FSP-JORDAN-WIGNER-HOP-SIGN`

- **Stage / status:** `FERMION_SIGN`, `COMPUTATIONALLY_CHECKED`.
- **Statement.** In the increasing occupation ordering on 6 modes, the sign of the hop c†_target c_source on every occupation bitmask equals the product of the Jordan-Wigner parities of the annihilation step and the creation step, checked exhaustively over all 2⁶ states and ordered mode pairs.
- **Scope, from the node.** The general Jordan-Wigner bijection between spin chains and CAR operators is a standard result imported here, not derived or mechanized in this checkout.
- **Prompt file:** [`dag/prompts/fermion_sign_fsp_jordan_wigner_hop_sign_computationally_checked.yaml`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/prompts/fermion_sign_fsp_jordan_wigner_hop_sign_computationally_checked.yaml). Derivation note: [`tfq_1185_fsp_jordan_wigner_hop_sign.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/derivations/26_fsp/tfq_1185_fsp_jordan_wigner_hop_sign.md).
- **Command:** `python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node FSP-JORDAN-WIGNER-HOP-SIGN --stage P0 --max-cost-usd 0.10 --max-tier 1 --ledger ../tfqm-ledger.json`
- **A valid result** keeps the six-mode bound, states the sign rule on a bitmask (the parity of the occupied modes below the source, times the parity of those below the target after the source is removed), and lists the imported Jordan-Wigner bijection as an open obligation. A claim for general n is outside the node.
- **Check it yourself** (builds the 64 × 64 matrices of the six annihilation operators and compares every hop with the rule above; about two seconds):

```python
from sympy import Matrix, eye, zeros, diag, kronecker_product as kp
n = 6
Z, I2, lower = diag(1, -1), eye(2), Matrix([[0, 1], [0, 0]])      # basis (|0>, |1>); lower: |1> -> |0>
def annihilate(j):                                                 # Z x ... x Z x lower x I x ... x I
    m = Matrix([[1]])
    for k in range(n):
        m = kp(m, Z if k < j else (lower if k == j else I2))
    return m
c = [annihilate(j) for j in range(n)]
for i in range(n):
    for j in range(n):
        assert c[i] * c[j].T + c[j].T * c[i] == (eye(2**n) if i == j else zeros(2**n))
        assert c[i] * c[j] + c[j] * c[i] == zeros(2**n)
checked = 0
for s in range(n):
    for t in range(n):
        if s == t:
            continue
        hop = c[t].T * c[s]
        for state in range(2**n):
            bits = [(state >> (n - 1 - k)) & 1 for k in range(n)]    # mode 0 is the leftmost factor
            column = hop[:, state]
            if bits[s] == 0 or bits[t] == 1:
                assert column.is_zero_matrix
                continue
            after = bits.copy(); after[s] = 0
            sign = (-1) ** sum(bits[:s]) * (-1) ** sum(after[:t])
            after[t] = 1
            assert column[int(''.join(map(str, after)), 2)] == sign and sum(abs(x) for x in column) == 1
            checked += 1
print("CAR holds on 6 modes; hop sign = product of the two parities in", checked, "cases")
```

## 4. `MAJ-PARITY-SECTOR-SPLIT-EXACT`

- **Stage / status:** `MAJORANA`, `COMPUTATIONALLY_CHECKED`.
- **Statement.** On the exact 2-mode Fock carrier the parity operator restricts to 2-dimensional even and odd sectors, and restricting γ₁ to a sector is refused because it mixes the sectors.
- **Scope, from the node.** A fixed 2-mode instance. The paper code's own parity check is floating point; the Rust test is exact.
- **Prompt file:** [`dag/prompts/majorana_maj_parity_sector_split_exact_computationally_checked.yaml`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/prompts/majorana_maj_parity_sector_split_exact_computationally_checked.yaml). Rust test: `code/rust/src/majorana/majorana_fock_algebra.rs::test_sector_restriction_and_refusals`. Derivation note: [`tfq_1174_maj_parity_sector_split_exact.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/derivations/28_majorana/tfq_1174_maj_parity_sector_split_exact.md).
- **Command:** `python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node MAJ-PARITY-SECTOR-SPLIT-EXACT --stage P0 --max-cost-usd 0.10 --max-tier 1 --ledger ../tfqm-ledger.json`
- **A valid result** cites the repository's Rust declarations only where the host can find them, states that γ₁ anticommutes with parity (hence maps one sector to the other), and keeps the fixed-instance limit in `open_obligations`.
- **Check it yourself:**

```python
from sympy import Matrix, eye, diag, kronecker_product as kp
Z, I2, lower = diag(1, -1), eye(2), Matrix([[0, 1], [0, 0]])
c1, c2 = kp(lower, I2), kp(Z, lower)                 # two fermionic modes by Jordan-Wigner
P = kp(Z, Z)                                         # parity (-1)^N
gamma1 = c1 + c1.T                                   # Majorana operator
assert P * P == eye(4) and P * gamma1 == -gamma1 * P # gamma_1 anticommutes with parity
even = [k for k in range(4) if P[k, k] == 1]; odd = [k for k in range(4) if P[k, k] == -1]
assert len(even) == len(odd) == 2
assert all(gamma1[i, j] == 0 for i in even for j in even)   # no even-to-even block
assert any(gamma1[i, j] != 0 for i in odd for j in even)    # it maps even to odd
print("2-mode parity sectors have dimension 2 and 2; gamma_1 mixes them")
```

## 5. `MAJ-MAJORANA-BRAID-YB-EXACT`

- **Stage / status:** `MAJORANA`, `COMPUTATIONALLY_CHECKED`.
- **Statement.** For 3 to 10 Majoranas, the exact signed-permutation exchange action satisfies bᵢbᵢ₊₁bᵢ = bᵢ₊₁bᵢbᵢ₊₁, far commutativity, and composition with its inverse gives the identity.
- **Scope, from the node.** Fixed counts 3 to 10. This is the Majorana exchange action, not the Ising 2 × 2 representation.
- **Prompt file:** [`dag/prompts/majorana_maj_majorana_braid_yb_exact_computationally_checked.yaml`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/prompts/majorana_maj_majorana_braid_yb_exact_computationally_checked.yaml). Rust: `code/rust/src/majorana/braid_action.rs`. Derivation note: [`tfq_1172_maj_majorana_braid_yb_exact.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/derivations/28_majorana/tfq_1172_maj_majorana_braid_yb_exact.md).
- **Command:** `python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node MAJ-MAJORANA-BRAID-YB-EXACT --stage P0 --max-cost-usd 0.10 --max-tier 1 --ledger ../tfqm-ledger.json`
- **A valid result** types the exchange action as a signed permutation, states the three relations with their index ranges, and does not claim them for n > 10 or for any other representation.
- **Check it yourself** (the sign convention γᵢ → γᵢ₊₁, γᵢ₊₁ → −γᵢ is the standard one; compare it with `braid_action.rs`):

```python
from sympy import eye
for n in range(3, 11):
    def b(i):                                        # exchange of Majoranas i, i+1 (1-based)
        m = eye(n); m[i-1, i-1] = 0; m[i, i] = 0; m[i, i-1] = 1; m[i-1, i] = -1
        return m
    for i in range(1, n):
        assert b(i) * b(i).inv() == eye(n)
        if i < n - 1:
            assert b(i) * b(i+1) * b(i) == b(i+1) * b(i) * b(i+1)
        for j in range(i + 2, n):
            assert b(i) * b(j) == b(j) * b(i)
print("braid relations hold for 3..10 Majoranas")
```

## 6. `MAJ-TETRON-BETTI-COMPUTED`

- **Stage / status:** `MAJORANA`, `COMPUTATIONALLY_CHECKED`.
- **Statement.** For sizes 2×2, 2×3, 3×3, 3×4, 4×4, 5×5, 6×6, 6×8 and 8×8, F₂ row reduction gives dim H¹ = (E − rank d₁) − rank d₀ equal to 0 (disk), 1 (cylinder) or 2 (torus), agreeing with (2 if closed else 1) minus the Euler characteristic, with d₁d₀ = 0.
- **Scope, from the node.** Fixed sizes only. A closed-form proof for all rows and columns is absent.
- **Prompt file:** [`dag/prompts/majorana_maj_tetron_betti_computed_computationally_checked.yaml`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/prompts/majorana_maj_tetron_betti_computed_computationally_checked.yaml). Rust: `code/rust/src/majorana/tetron.rs`. Derivation note: [`tfq_1152_maj_tetron_betti_computed.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/derivations/28_majorana/tfq_1152_maj_tetron_betti_computed.md).
- **Command:** `python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node MAJ-TETRON-BETTI-COMPUTED --stage P0 --max-cost-usd 0.10 --max-tier 1 --ledger ../tfqm-ledger.json`
- **A valid result** keeps "fixed sizes" in its scope, separates the rank computation from the topological reading (Euler characteristic), and lists the all-sizes statement as an open obligation. A human-written proof for all sizes would be a campaign-style contribution, not a prompt result.
- **Check it yourself** (the periodic case only; this builds the torus complex with one 0-cell, two 1-cells and one 2-cell per site, and computes ranks over F₂ with bit masks):

```python
def gf2_rank(rows):
    rows, rank = list(rows), 0
    for bit in range(max((r.bit_length() for r in rows), default=0)):
        pivot = next((k for k in range(rank, len(rows)) if rows[k] >> bit & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for k in range(len(rows)):
            if k != rank and rows[k] >> bit & 1:
                rows[k] ^= rows[rank]
        rank += 1
    return rank

def torus(R, C):
    V = lambda i, j: (i % R) * C + (j % C)
    h = lambda i, j: (i % R) * C + (j % C)            # edge (i,j) -> (i,j+1)
    v = lambda i, j: R * C + (i % R) * C + (j % C)    # edge (i,j) -> (i+1,j)
    nV, nE = R * C, 2 * R * C
    d0 = [0] * nV                                     # column u of d0: the edges that touch vertex u
    for i in range(R):
        for j in range(C):
            for e, (a, b) in ((h(i, j), (V(i, j), V(i, j + 1))), (v(i, j), (V(i, j), V(i + 1, j)))):
                d0[a] ^= 1 << e
                d0[b] ^= 1 << e
    d1 = [(1 << h(i, j)) | (1 << v(i, j + 1)) | (1 << h(i + 1, j)) | (1 << v(i, j)) for i in range(R) for j in range(C)]
    return nV, nE, d0, d1, h, v

for R, C in [(2, 2), (2, 3), (3, 3), (3, 4), (4, 4), (5, 5), (6, 6), (6, 8), (8, 8)]:
    nV, nE, d0, d1, h, v = torus(R, C)
    assert all(bin(f & col).count('1') % 2 == 0 for f in d1 for col in d0)    # d1 d0 = 0
    assert (nE - gf2_rank(d1)) - gf2_rank(d0) == 2, (R, C)                    # dim H^1 of the torus
print("torus dim H1 = 2 over GF(2) for all listed sizes")
```

## 7. `MAJ-SYNDROME-READOUT-INADEQUATE`

- **Stage / status:** `MAJORANA`, `COMPUTATIONALLY_CHECKED`.
- **Statement.** On the 2 × 2 tetron torus, the column and row logical representatives are distinct cochains with equal zero syndrome d₁w, so the readout M(w) = d₁w is `DETECTOR_INADEQUATE` for them.
- **Scope, from the node.** A fixed instance. The adequacy of a syndrome-plus-class readout is asserted, not computed.
- **Prompt file:** [`dag/prompts/majorana_maj_syndrome_readout_inadequate_computationally_checked.yaml`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/prompts/majorana_maj_syndrome_readout_inadequate_computationally_checked.yaml). Derivation note: [`tfq_1164_maj_syndrome_readout_inadequate.md`](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/dag/derivations/28_majorana/tfq_1164_maj_syndrome_readout_inadequate.md).
- **Command:** `python -I -X utf8 dag/pfp/llm_ladder/ladder.py --node MAJ-SYNDROME-READOUT-INADEQUATE --stage P0 --max-cost-usd 0.10 --max-tier 1 --ledger ../tfqm-ledger.json`
- **A valid result** states which two cochains are meant, that both are cocycles (zero syndrome), that they are distinct and lie in different cohomology classes, and what "inadequate" means for this readout. It must not claim anything about decoders or error rates. An earlier ladder run of this node was not accepted; a clean negative result is a fair outcome here too.
- **Check it yourself** (run it after the snippet for node 6, which defines `gf2_rank` and `torus`; the cut representatives below are one natural choice, so compare them with the ones named in the node's source):

```python
R = C = 2
nV, nE, d0, d1, h, v = torus(R, C)
colcut = sum(1 << h(i, 0) for i in range(R))      # the horizontal edges crossing between column 0 and column 1
rowcut = sum(1 << v(0, j) for j in range(C))      # the vertical edges crossing between row 0 and row 1
syndrome = lambda w: [bin(f & w).count('1') % 2 for f in d1]
assert syndrome(colcut) == [0] * 4 and syndrome(rowcut) == [0] * 4 and colcut != rowcut
base = gf2_rank(d0)
bounds = lambda w: gf2_rank(d0 + [w]) == base     # is w in the image of d0?
assert not bounds(colcut) and not bounds(rowcut) and not bounds(colcut ^ rowcut)
print("two distinct non-bounding cocycles with zero syndrome on the 2x2 torus")
```

---

Found a mistake in one of these checks or in a node statement? Open a *Bug report* or a *Derivation review* issue. That is as useful as a run.
