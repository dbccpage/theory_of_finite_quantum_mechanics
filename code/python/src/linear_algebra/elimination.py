"""Exact field elimination algebraic module matching Rust linear_algebra::exact_field::elimination."""
from .scalars import GaussianRational, Q, q
from .matrix import ExactMatrix

__all__ = ["ExactMatrix", "GaussianRational", "Q", "q"]
