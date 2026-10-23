# Exact guarded-schedule experiment

This independent research experiment checks the finite complexes in
[`docs/guarded_schedule_topology.md`](../../docs/guarded_schedule_topology.md).
Event `2*i` removes one assertion count; event `2*i+1` adds one. Their
pair precedence is an explicitly supplied protocol. The native count guard
requires a positive count before a removal.

Every case with one through four pairs and every capacity `0..n` is included.
`K(n,c)` contains a permutohedral cell only when **every** ordering inside
each tied block obeys precedence and the guard. A separate baseline enumerates
complete words, runs the count guard, and admits coarsenings only after checking
all their vertex refinements. `T(n,c)` is the task permutohedron subcomplex
whose tied blocks have size at most `c`.

The oriented cellular boundaries use integer coefficients. Each boundary is
reduced by integral elementary operations with unit pivots. The certificate
records those pivots; the checker replays them without running pivot search.
It independently checks consecutive boundary compositions are zero. If all
residual matrices vanish, every nonzero Smith invariant is one. The boundary
images are therefore primitive subgroups, and the computed homology groups
are free abelian with the reported ranks. A nonunit residual gives an
unclassified result, with no inference that torsion exists.

All reported groups are ordinary integral `H_k` for `k >= 0`. The empty
capacity-zero complex is reported with no nonzero groups in those degrees;
the experiment does not compute augmented degree-minus-one homology.

| Case | Full native cell counts by dimension | Nonzero ordinary homology |
|---|---|---|
| `K(3,2)` | `54, 84, 30` | `H_0 = Z`, `H_1 = Z` |
| `K(4,2)` | `648, 1368, 876, 168, 6` | `H_0 = Z`, `H_1 = Z^7` |
| `K(4,3)` | `1944, 5400, 5340, 2184, 302` | `H_0 = Z`, `H_2 = Z` |
| `T(4,2)` | `24, 36, 6` | `H_0 = Z`, `H_1 = Z^7` |
| `T(4,3)` | `24, 36, 14` | `H_0 = Z`, `H_2 = Z` |

For `T(3,2)` and `T(4,3)`, the certificate also supplies the boundary of
the missing top permutohedral cell as an explicit cycle. A top cochain pairs
with it by `-1`. The checker verifies the cycle boundary and pairing against
the declared differential. This proves that the cochain is not exact. Higher
cells matter: truncating `K(4,3)` to its two-skeleton changes its second Betti
number from `1` to `1883`.

These calculations check finite instances. The general homotopy equivalence,
and the sphere conclusion for arbitrary `n`, are written proofs in the cited
derivation; they are not inferred from Euler characteristics or finite data.
The smaller task complex is a topological model, not an execution-state
quotient that retains native guards, prices, or raw states.

From the paper root, replay the retained matrix certificate with Python 3.11
or later and no additional runtime dependencies:

```sh
python scripts/verify_guarded_schedule_topology.py check \
  --certificate code/guarded_schedule_topology/evidence/certificate.json \
  --receipt /tmp/guarded-topology-recheck.json
```

To rebuild the certificate, change `check` to `build` and select a new output
path. To replay the actual Rust transitions as well, build the existing wire
adapter against an explicit repository root, then supply its executable,
build receipt, and source root:

```sh
python code/causal_certificates/native/build_native.py \
  --source-root /path/to/the_symbol_game \
  --build-dir /tmp/guarded-topology-native
python scripts/verify_guarded_schedule_topology.py check \
  --certificate code/guarded_schedule_topology/evidence/certificate.json \
  --native-bin /path/to/target/debug/wdp_causal_replay \
  --native-build-receipt /tmp/guarded-topology-native/native_build_receipt.json \
  --source-root /path/to/the_symbol_game \
  --receipt /tmp/guarded-topology-native-check.json
```

The builder prints the executable location. Native replay checks all `12,980`
causal tagged schedules for `n=1..4`, `c=0..n`, including refusals, intermediate
counts, and terminal addition counts. Its source-bound executable supplies
all native transition semantics. The retained build receipt records the
actual compiler, dependencies, source hashes, and executable hash. A run
without those three explicit native arguments reports that native replay
was not requested.

The package implements no production functional and grants no authority.
