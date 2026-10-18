# Kill-criteria implementation + archive sample (2026-08-01)

**AuthorityEffect:** None

## 1. What Deutsch / Rovelli / Albert demanded → what shipped

| Kill criterion | Module / change | What it is (declared only) |
|---|---|---|
| Rename prestige | `Gf2CocycleClassifier::classify`, `Gf2ScheduleReceipt` | Primary API; old `MajoranaGF2Terminalizer::terminalize` kept as `#[deprecated]` alias |
| Dual observer | `dual_observer.rs` | Two linear maps \(M_A, M_B\) on same \(\omega\); receipt flags zero/weight disagreement |
| Noise + growing \(d\) | `noise_mc.rs` | IID Bernoulli edge flips on planar \(m\times m\) grids; class fractions; size sweep \(m=1..3\) |

```text
cd omega_engine
cargo test -j 1 -p omega_majorana
# 54 passed
cargo test -j 1 -p omega_majorana dual_observer noise_mc -- --nocapture
```

**Still not claimed:** physical threshold, continuum TQFT, device verdict, constructor impossibility.

## 2. Dual-observer fixed point

Same plaquette, \(\omega = e_1\) (odd edge):

- \(O_{\mathrm{face}} = d_1\): residual nonzero  
- \(O_{\mathrm{even}} =\) XOR of even edges: residual zero  
→ `zero_disagreement = true`

## 3. Noise MC fixed point

- \(p=0\): all Exact  
- \(p\)↑: open fraction rises (seedable LCG)  
- size sweep \(m=1,2,3\): Auth=None on every row  

## 4. Archive sample (unfinished notes 013 / 024 / 025)

### Paper 013 — Constructor Topos Theory v012
**Path:** `research_notes_000/013 - Constructor Topos Theory/v012/`

- Core **math**: \(\ell^1\) coboundary uniqueness extends to infinite posets via pro-finite exhaustion (Thms 1–2).  
- Constructor theory is **Section 5 dictionary only** (demoted from co-equal theme): tasks ↔ global sections; impossibility ↔ nontrivial obstruction; stable norm as construction cost lower bound.  
- Explicitly **not** a new topos beyond \(\mathbf{Sh}_\infty(\mathcal{P})\).  
- Open: Fermion Sign \(H^1\) conjecture for QMC graphs.

**Bridge to crate:** our GF(2) residual / packet refuse is the **finite** side of the same “task = section / obstruction = residual” dictionary — without claiming infinite poset uniqueness.

### Paper 024 — Speed of Light as Lieb–Robinson Velocity v004
**Path:** `research_notes_000/024 - Speed of Light as Lieb-Robinson Velocity/v004/`

- Conditional: if LR bounds exist for BD causal-set dynamics, \(v_{\mathrm{LR}} \ge c\).  
- Links Paper 000 short-time density + LR cone.  
- Softened: topological defects ≠ particles; LR saturation on BD nonlocality is **open**.

**Bridge to crate:** noise_mc has **no** LR cone — only IID edge flips. LR would be a *next* layer: restrict residual support to causal balls of radius \(v t\).

### Paper 025 — TQFT v003
**Path:** `research_notes_000/025 - Topological Quantum Field Theory/v003/`

- Review: 2D TQFT = commutative Frobenius algebra (classical classification).  
- Handle operator \(Z(\Sigma_g)\); dual-numbers non-semisimple example.  
- Softened “duality” language; Topological Wall compiler as consumer, not new theorem.

**Bridge to crate:** plaquette holonomy residual is **not** a TQFT functor. Frobenius / cobordism would require declared \(Z\) on cobordisms — still empty in `omega_majorana`.

## 5. Honest stack diagram (declared only)

```text
013 dictionary:  task ~ section, obstruction ~ residual class
024:             LR cone bounds residual *support* (not implemented here)
025:             TQFT Z: Cob → Vect (not implemented here)
crate now:       classify(ω), dual_observe(O1,O2,ω), noise_mc(m,p), holonomy r=d1 A
```

## 6. Still open vs trio

| Still open | Why |
|---|---|
| Real decoder + correlated noise | Only Bernoulli edges |
| Dual *physical* systems | Only dual **matrices** |
| Constructor impossibility theorem | Dictionary only in 013 |
| TQFT / LR in code | Notes unfinished; crate untouched |
