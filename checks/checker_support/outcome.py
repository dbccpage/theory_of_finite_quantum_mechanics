"""Railway result for independent checker operations. AuthorityEffect: None."""
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, cast, overload
from .domains import Failure
from .boundary import Violation

T = TypeVar("T")
U = TypeVar("U")
_MISSING = object()


@dataclass(frozen=True, slots=True, init=False)
class Outcome(Generic[T]):
    """Success may contain None. Failure short-circuits bind without calling its function."""

    value: T | None = None
    error: Failure | None = None

    @overload
    def __init__(self, value: T) -> None: ...

    @overload
    def __init__(self, *, error: Failure) -> None: ...

    def __init__(self, value: object = _MISSING, error: Failure | None = None) -> None:
        if error is not None and type(error) is not Failure:
            raise Violation("input", "an Outcome error must be a Failure value")
        if error is not None and value is not _MISSING:
            raise Violation("input", "an Outcome cannot carry both a value and a failure")
        if value is _MISSING and error is None:
            raise Violation("input", "an Outcome must explicitly carry a value or a failure")
        object.__setattr__(self, "value", None if value is _MISSING else value)
        object.__setattr__(self, "error", error)

    @property
    def ok(self) -> bool:
        return self.error is None

    def bind(self, function: Callable[[T], "Outcome[U]"]) -> "Outcome[U]":
        if self.error is not None:
            return Outcome(error=self.error)
        if not callable(function):
            return Outcome(error=Failure("input", "bind requires a callable transition"))
        # The success variant admits T=None. Absence is identified by error,
        # rather than by using None as a second, ambiguous failure sentinel.
        try:
            result = function(cast(T, self.value))
        except Violation as error:
            return Outcome(error=error.failure)
        except OSError as error:
            return Outcome(error=Failure("resource", str(error) or type(error).__name__))
        except (ValueError, TypeError, ZeroDivisionError) as error:
            return Outcome(error=Failure("input", str(error) or type(error).__name__))
        if not isinstance(result, Outcome):
            return Outcome(error=Failure("input", "bind transition must return an Outcome"))
        return result

    def map(self, function: Callable[[T], U]) -> "Outcome[U]":
        """Transform only the success branch, retaining typed refusal semantics."""
        return self.bind(lambda value: Outcome(value=function(value)))

    def value_or(self, fallback: T) -> T:
        """A successful None stays None; the fallback is used only for failure."""
        return fallback if self.error is not None else cast(T, self.value)
