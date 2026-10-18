# Holonomy residual on a declared plaquette

**AuthorityEffect:** None  
**Receipt tag:** `omega.majorana-holonomy-receipt.v1`  
**Code:** `omega_majorana::holonomy`

## Declared data only

| Input | What it is |
|---|---|
| `ChainComplexGf2` | Finite \(d_0,d_1\) with \(d_1 d_0=0\) |
| Connection \(A\) | Edge cochain in a declared monoid (\(\mathbb{F}_2\) or \(\mathbb{Q}(\zeta_{16})\) seed) |
| Face holonomy residual | Failure of face product/sum to equal monoid identity |

On \(\mathbb{F}_2\): residual vector \(r = d_1 A\) (one bit per face).  
Gauge: \(A' = A + d_0\alpha\) leaves \(r\) unchanged when boundary holds.

No other object is introduced.

## Run

```text
cd omega_engine
cargo test -j 1 -p omega_majorana holonomy -- --nocapture
```

## Fixed checks

| Test | Assert |
|---|---|
| zero connection on plaquette | `flat`, residual weight 0 |
| single edge on plaquette | face residual `[1]` |
| all four edges | flat (sum 0 mod 2) |
| gauge transform | same face residuals |
| cyclotomic all-ones | product = 1, residual trivial |
| cyclotomic one \(\zeta\) | residual nontrivial |
| every receipt | `authority_effect == "None"` |

## Link to schedule classifier (declared bridge only)

`connect_to_schedule_class`: same \(A\) as edge residual for `terminalize` — face residual vs edge schedule class are two **declared readouts** of one cochain packet, not an identification of layers beyond the maps written in code.
