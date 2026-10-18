"""Exact field characteristic_polynomial algebraic module matching Rust linear_algebra::exact_field::characteristic_polynomial."""
from .scalars import GaussianRational, Q, q
from .matrix import ExactMatrix

__all__ = ["ExactMatrix", "GaussianRational", "Q", "q"]
