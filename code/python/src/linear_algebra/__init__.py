"""Exact linear algebra, scalar fields, polynomial algebra and exact solvers."""

from .scalars import GaussianRational, Q, q
from .matrix import ExactMatrix, MatrixError
from .smith_form import smith_normal_form
from .image_kernel import image_basis, kernel_basis

from . import bareiss_det
from . import basic_matrix
from . import char_poly
from . import commutant
from . import complex_tensor
from . import compositum_deg
from . import congruence
from . import cyclo_density
from . import elimination
from . import entropy_dichotomy
from . import field_factors
from . import field_squares
from . import image_kernel
from . import interpolation
from . import involution
from . import laws
from . import matrix
from . import ordered
from . import poly_roots
from . import pseudoinverse
from . import quintic_split
from . import rational_factors
from . import scalars
from . import second_jet
from . import smith_form
from . import spectral_factors
from . import splitting_deg
from . import tensor_proj
from . import test_support

__all__ = [
    "GaussianRational", "Q", "q", "ExactMatrix", "MatrixError", "smith_normal_form", "image_basis", "kernel_basis",
    "bareiss_det",
    "basic_matrix",
    "char_poly",
    "commutant",
    "complex_tensor",
    "compositum_deg",
    "congruence",
    "cyclo_density",
    "elimination",
    "entropy_dichotomy",
    "field_factors",
    "field_squares",
    "image_kernel",
    "interpolation",
    "involution",
    "laws",
    "matrix",
    "ordered",
    "poly_roots",
    "pseudoinverse",
    "quintic_split",
    "rational_factors",
    "scalars",
    "second_jet",
    "smith_form",
    "spectral_factors",
    "splitting_deg",
    "tensor_proj",
    "test_support",
]
