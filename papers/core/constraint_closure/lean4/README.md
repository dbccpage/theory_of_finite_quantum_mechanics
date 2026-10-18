# GR-002 Lean package

The root `GR002.lean` imports every module below, so `lake build` elaborates
the complete package. Mathlib is pinned to `v4.34.0-rc1`, matching
`lean-toolchain`.

| Module | What Lean proves | Explicit boundary |
|---|---|---|
| `GR002/HodgeSplitC3.lean` | $R_{\rm split}=7/3$ at the three positive basis fixtures (and hence their Python-checked signed variants); a nonzero equal-ratio identity | No global $7/3$ ceiling theorem |
| `GR002/HodgeDiracSUSY.lean` | $d_1d_0=0$ and the displayed coordinate Laplacian equals $3I_3$ | No formal spectrum, Witten-index, or physical-SUSY theorem |
| `GR002/ReggeDeficit.lean` | Hex-disk unit formula, strict growth, and its $\pi/3$-scaled real identity | The combinatorial family is supplied |
| `GR002/PonzanoRegge6j.lean` | The supplied two Racah terms and prefactor multiply to $1/6$ | No general Racah-formula derivation |
| `GR002/LinearEnergy.lean` | Scalar absolute-value homogeneity and its piecewise form | No quotient construction or Higgs theorem |
| `GR002/TopDimensionVanishing.lean` | A declared indicator is zero above its supplied dimension | Not a constructed simplicial cochain space |

The `#print axioms` commands in the source report the dependencies of every
theorem named by this inventory. `manifest.json` binds the source hashes and
records the same scoped statements; it is a receipt, not independent proof.

```powershell
lake update
lake exe cache get
lake build
python verify_manifest.py
```

On Windows, the package path can exceed legacy path limits while Mathlib is
unpacked. Build a byte-identical short scratch copy if that occurs.
