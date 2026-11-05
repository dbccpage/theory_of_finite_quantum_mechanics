"""CLI and Railway entry points; domain algorithms remain independent of production code."""
from __future__ import annotations
import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, ParamSpec, TypeVar
from .domains import Failure, FailureKind

if TYPE_CHECKING:
    from .outcome import Outcome


class Violation(ValueError):
    """Internal domain refusal; never a successful result or disabled assertion."""

    def __init__(self, kind: FailureKind, message: str) -> None:
        self.failure = Failure(kind, message)
        super().__init__(message)

P = ParamSpec("P")
T = TypeVar("T")


def evaluate(operation: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> Outcome[T]:
    """Catch declared synchronous domain failures, preserving unexpected programmer errors."""
    from .outcome import Outcome
    if not callable(operation):
        return Outcome(error=Failure("input", "evaluation requires a callable operation"))
    try:
        return Outcome(value=operation(*args, **kwargs))
    except Violation as error:
        return Outcome(error=error.failure)
    except OSError as error:
        return Outcome(error=Failure("resource", str(error) or type(error).__name__))
    except (ValueError, TypeError, ZeroDivisionError) as error:
        return Outcome(error=Failure("input", str(error) or type(error).__name__))


def require(condition: bool, message: str) -> None:
    """Internal verification guard: active under normal and optimized Python."""
    if type(condition) is not bool:
        raise Violation("input", "verification condition must be a bool")
    if type(message) is not str or not message.strip():
        raise Violation("input", "verification condition must have a nonempty description")
    if not condition:
        raise Violation("check", message)


def _write_failure(failure: Failure) -> None:
    try:
        print(json.dumps({"status": "failed", **failure.to_record()}), file=sys.stderr)
    except (OSError, ValueError):
        # A closed/broken diagnostic stream must not turn a refusal into success
        # or prevent the caller from returning the nonzero exit status.
        pass


def cli(operation: Callable[[], int | None]) -> int:
    result = evaluate(operation)
    if result.error is not None:
        _write_failure(result.error)
        return 1
    if result.value is None:
        return 0
    if type(result.value) is not int or not 0 <= result.value <= 255:
        _write_failure(Failure("input", "checker exit status must be None or an integer in [0,255]"))
        return 1
    return result.value
