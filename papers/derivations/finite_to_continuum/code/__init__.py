"""
Finite to Continuum Bridging Package.

AuthorityEffect: None.

Implements the constructive bridge recovering continuum observables
from finite discrete rules without floating-point slop:
  - Step 1: Certified Rational Interval Calculus (RationalInterval)
  - Step 2: CS-Q Discretization Defect Operators (DiscretizationDefectCarrier, 2D Carrier)
  - Step 3: Wilsonian Finite-Size Scaling Extrapolation (WilsonianExtrapolator)
  - Pontryagin Duality: 1D Cyclic to Circle and 2D Torus Z_Lx x Z_Ly to T^2
  - Meron-Cluster Wilsonian Bridge: Thermodynamic limit of fermion chain transfer traces
"""

import sys
from pathlib import Path

_CODE_DIR = str(Path(__file__).resolve().parent)
if _CODE_DIR not in sys.path:
    sys.path.insert(0, _CODE_DIR)

from .interval_calculus import (
    RationalInterval,
    certified_ln_interval,
    certified_pi_enclosure,
    exp_interval,
    ln_interval_around_one,
    rational_heron_sqrt_bounds,
    sqrt_interval,
)
from .discretization_defect import (
    DiscretizationDefectCarrier,
    Discrete1DHamiltonianSolver,
    DiscreteTrapezoidalQuadratureSolver,
    MeshRefinementReceipt,
    verify_mesh_refinement,
)
from .coda_2d_discretization_defect import (
    DiscretizationDefect2DCarrier,
    Discrete2DCubatureSolver,
    Mesh2DRefinementReceipt,
    verify_2d_mesh_refinement,
)
from .wilsonian_extrapolator import (
    ChainObservation,
    WilsonianExtrapolator,
    WilsonianScalingReceipt,
)
from .pontryagin_duality import (
    DiscreteLatticeFourier,
    PontryaginProgrammeError,
    PontryaginStagedReceipt,
    ProgrammeStage,
    refuse_alpha_as_certified_exact,
    refuse_finite_zn_sold_as_free_u1,
    refuse_pi_from_exact_q,
    refuse_u1_derived_from_l1_mass_alone,
    run_pontryagin_staged_programme,
)
from .coda_2d_pontryagin import (
    Discrete2DTorusFourier,
    Pontryagin2DProgrammeError,
    Pontryagin2DStagedReceipt,
    Programme2DStage,
    refuse_alpha_2d_as_certified_exact,
    refuse_finite_z2_sold_as_t2,
    refuse_pi_from_exact_q_2d,
    refuse_t2_derived_from_l1_alone,
    run_pontryagin_2d_staged_programme,
)
from .meron_wilsonian_bridge import (
    MeronThermodynamicReceipt,
    MeronWilsonianBridge,
)
from .coda_inductive_presentation import (
    CharacterOrthogonalityReceipt,
    ContinuumEnclosure,
    CyclicPresentation,
    DomainContinuumElement,
    PontryaginCharacter,
    constructive_cauchy_completion,
    e_enclosure_sequence,
    generate_inductive_presentation_receipt,
    lift_mark_to_continuum,
    ln2_enclosure_sequence,
    pi_enclosure_sequence,
    sqrt2_enclosure_sequence,
    verify_character_orthogonality,
)
from .continuous_haar_limit import (
    HaarLimitCharacterPair,
    LipschitzContinuumEnclosure,
    TrigPolynomial,
    generate_continuous_haar_limit_receipt,
)

__all__ = [
    "RationalInterval",
    "certified_ln_interval",
    "certified_pi_enclosure",
    "exp_interval",
    "ln_interval_around_one",
    "rational_heron_sqrt_bounds",
    "sqrt_interval",
    "DiscretizationDefectCarrier",
    "Discrete1DHamiltonianSolver",
    "DiscreteTrapezoidalQuadratureSolver",
    "MeshRefinementReceipt",
    "verify_mesh_refinement",
    "DiscretizationDefect2DCarrier",
    "Discrete2DCubatureSolver",
    "Mesh2DRefinementReceipt",
    "verify_2d_mesh_refinement",
    "ChainObservation",
    "WilsonianExtrapolator",
    "WilsonianScalingReceipt",
    "DiscreteLatticeFourier",
    "PontryaginProgrammeError",
    "PontryaginStagedReceipt",
    "ProgrammeStage",
    "refuse_alpha_as_certified_exact",
    "refuse_finite_zn_sold_as_free_u1",
    "refuse_pi_from_exact_q",
    "refuse_u1_derived_from_l1_mass_alone",
    "run_pontryagin_staged_programme",
    "Discrete2DTorusFourier",
    "Pontryagin2DProgrammeError",
    "Pontryagin2DStagedReceipt",
    "Programme2DStage",
    "refuse_alpha_2d_as_certified_exact",
    "refuse_finite_z2_sold_as_t2",
    "refuse_pi_from_exact_q_2d",
    "refuse_t2_derived_from_l1_alone",
    "run_pontryagin_2d_staged_programme",
    "MeronThermodynamicReceipt",
    "MeronWilsonianBridge",
    "TargetSpec",
    "build_top_five_targets",
    "export_target_ladder_receipt",
    "verify_all_targets",
    "CyclicPresentation",
    "PontryaginCharacter",
    "CharacterOrthogonalityReceipt",
    "verify_character_orthogonality",
    "ContinuumEnclosure",
    "constructive_cauchy_completion",
    "pi_enclosure_sequence",
    "e_enclosure_sequence",
    "sqrt2_enclosure_sequence",
    "ln2_enclosure_sequence",
    "DomainContinuumElement",
    "lift_mark_to_continuum",
    "generate_inductive_presentation_receipt",
    "HaarLimitCharacterPair",
    "TrigPolynomial",
    "LipschitzContinuumEnclosure",
    "generate_continuous_haar_limit_receipt",
]
