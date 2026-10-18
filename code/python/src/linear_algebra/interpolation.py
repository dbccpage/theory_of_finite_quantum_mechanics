"""Exact field neville_aitken algebraic module matching Rust linear_algebra::exact_field::neville_aitken."""
from .scalars import GaussianRational, Q, q
from .matrix import ExactMatrix

__all__ = ["ExactMatrix", "GaussianRational", "Q", "q"]
