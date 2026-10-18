"""Physics numeric constants (non-authority data).

This module is plain numeric reference data only. It does NOT constitute a
physical theory module: it performs no derivation, validation, or enforcement,
and carries no authority. Values are literature reference figures used by
diagnostic prototypes.
"""

# Mass scales (energy units as noted per variable).
M_P_GEV = 1.22e19  # Planck mass, GeV
M_EW_GEV = 246.0  # Electroweak (Higgs vev) scale, GeV
M_PROTON_GEV = 0.938  # Proton mass, GeV

M_Z = 91.1876  # Z boson mass, GeV
M_GUT = 2.0e16  # Grand-unification scale, GeV
M_SUSY = 1.0e3  # Assumed SUSY-breaking scale, GeV

# One-loop hypercharge beta-function coefficients b1 (dimensionless).
B1_SM = 41.0 / 10.0  # Standard Model
B1_MSSM = 33.0 / 5.0  # Minimal Supersymmetric Standard Model
B1_2LOOP_SM = 199.0 / 50.0  # SM two-loop b1 entry
