# Lean source inventory

AuthorityEffect: None. GenesisEffect: None.

These six modules have separate scopes. Compiling their declarations does not
prove equivalence with Python, Rust, SQL or the frozen Genesis source.

| Module | Content established by its actual statements |
| --- | --- |
| [MssnSyntax.lean](MssnSyntax.lean) | Unrestricted syntax sketches for 19 profiles. No grammar recognizer or parser-correspondence theorem. |
| [MssnObstructionDetector.lean](MssnObstructionDetector.lean) | Boolean four-gate factorization; a supplied collision fixture; integer cycle circulation vanishes on the stated coboundaries; unit circulation has no potential. Candidate metadata is not a verified lift. |
| [MssnFiniteAlgebra.lean](MssnFiniteAlgebra.lean) | Integer sign cancellation, 2×2 commutator trace and concrete matrix identities. |
| [MssnSimplicialGauge.lean](MssnSimplicialGauge.lean) | Pure-gauge triangle cancellation derived from group laws; sign checks on supplied determinant values. No curved Regge/Bianchi theorem or determinant algorithm. |
| [MssnSmithNormalForm.lean](MssnSmithNormalForm.lean) | Checks on supplied invariant-factor records and positive divisibility chains. No Smith reduction or homology computation. |
| [MssnQuantumTransfer.lean](MssnQuantumTransfer.lean) | Exact rational squared norms, a two-bit lookup table and comparisons of declared constants. No teleportation fidelity, anyon coherence or entanglement theorem. |

All six were directly compiled with Lean 4.33.1 for the October 9 review.
The package's `lean-toolchain` still requests 4.34.0; this direct compilation
is compatibility evidence for 4.33.1, not a claim that a Lake build under the
pinned version ran. For example, from the repository root:

```sh
lean -o /tmp/MssnSimplicialGauge.olean education/minimal_symbol_systems/lean4/MssnSimplicialGauge.lean
```

The [publication review](../publication_review.md) records scope and limitations.
Four domain core modules were also compiled after replacing falsely named
recovery-gap predicates by their exact singleton condition and a witnessed-pair
counterexample. Other domain proof files require their own validation.
