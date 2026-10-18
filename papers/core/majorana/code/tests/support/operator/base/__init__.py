"""Base Operator crate exposing pure Operators, Constructor base class, Lambda/Reducer/Transform base classes, and OperatorFactory."""

from omega_engine.crates.operator.base.ctor_base import (
    ConstructorBase,
    AdmittedResult,
    ConstructorRefusal,
)
from omega_engine.crates.operator.base.operator_base import (
    OperatorBase,
    OperatorFailure,
    OperatorResult,
)
from omega_engine.crates.operator.base.lambda_base import (
    LambdaOperator,
    LambdaWitness,
)
from omega_engine.crates.operator.base.reducer_base import (
    ReducerOperator,
)
from omega_engine.crates.operator.base.transform_base import (
    TransformOperator,
)
from omega_engine.crates.operator.base.operator_factory import (
    OperatorFactory,
    OperatorKey,
)

__all__ = [
    "ConstructorBase",
    "AdmittedResult",
    "ConstructorRefusal",
    "OperatorBase",
    "OperatorResult",
    "OperatorFailure",
    "LambdaOperator",
    "LambdaWitness",
    "ReducerOperator",
    "TransformOperator",
    "OperatorKey",
    "OperatorFactory",
]
