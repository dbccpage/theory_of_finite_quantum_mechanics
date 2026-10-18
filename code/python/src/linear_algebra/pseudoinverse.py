"""Exact field pseudoinverse algebraic module matching Rust linear_algebra::exact_field::pseudoinverse."""
from .scalars import GaussianRational, Q, q
from .matrix import ExactMatrix

__all__ = ["ExactMatrix", "GaussianRational", "Q", "q"]
