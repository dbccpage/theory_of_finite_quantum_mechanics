# Fermionic Hamiltonians, Exact Normal Forms and Sign-Problem Boundaries

Research extension 2.4.0, 2026-09-22. **AuthorityEffect: None.**

The [manuscript](the_problem_of_the_fermion_sign.md) now develops actual normal-form laws, Hamiltonian source provenance, model-derived meron SQL cancellation, and Hubbard determinant constructions. [The claim ledger](the_problem_of_the_fermion_sign_claim_ledger.md) separates these results from withdrawn interpretations of historical fixtures.

| Result | Evidence and boundary |
|---|---|
| Rational quotient normal form | Exact RREF representative with soundness, idempotence and completeness modulo a supplied image; separate bounded exact L1 optimization. |
| Binary sign normal form | Fixed-labelled-graph representative modulo vertex sign changes, with returned gauge and odd sign-parity cycle witnesses. |
| Meron transfer reconstruction | Four-site interacting spinless model: normalized partition 912 before/after reduction; a nonconstant observable is preserved too. |
| Hubbard protected representations | Exact positivity under the stated half-filled bipartite or attractive spin-balanced conditions; independent full-Fock reconstruction. |
| Hubbard negative witnesses | Exact negative auxiliary fields outside those protections; negative exchange cycles even on a site-tree geometry. |
| Hamiltonian origin | Pinned sealed chain ingredients and post-seal signed hopping research; the Hamiltonian is explicitly admitted. |

These are finite constructions and conditional proofs. Exhaustive SQL enumeration is not a general polynomial-time FSP solver. Nonnegative determinant weights alone do not establish fast sampling.

See the detailed [normal-form audit](docs/normal_form_audit.md), [SQL derivation](docs/sql_meron_hubbard.md), and [Hamiltonian origin](docs/hamiltonian_origin.md). The catalog contains **2 executable canonicalizers, 12 relational predicates and 16 operational contracts**. A valid YAML contract does not by itself establish a normalizer.

Replay from this directory with Python, pytest, pytest-xdist, numpy, scipy and PyYAML installed:

```powershell
python code/sign_sql/exact_models.py --output code/sign_sql/exact_models_receipt.json
python -m pytest code/tests code/sign_sql/tests -n 8 --dist=loadfile --import-mode=importlib -q --basetemp "$env:TEMP\po023-replay"
```

Run `lake build` from `lean4/`. The new `MeronCharacter.lean` proves the finite character-sum identity for arbitrary flip lists. `NormalFormLaws.lean` proves specific integral and triangle normal-form laws; it does not mechanize the full Python normalizers or Hubbard determinant theorem.

`python verify_deposit.py` checks the package manifest, declared evidence references, Python suite and Lean build. It is a local package check, not publication approval or a mathematical audit. Exact run details are in [verification.md](verification.md); deterministic model results and parameters are in [exact_models_receipt.json](code/sign_sql/exact_models_receipt.json).

The frozen reference is [19L57G1 `sealed-derivation-v1`](https://github.com/dbccpage/19L57G1/tree/sealed-derivation-v1), commit `3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`. Post-seal exploratory references are pinned separately in the origin note. No sealed derivation sources or gates were imported.
