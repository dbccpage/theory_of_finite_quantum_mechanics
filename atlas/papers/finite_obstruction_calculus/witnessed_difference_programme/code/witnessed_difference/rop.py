"""Railway result values owned by this package.

The deposit runs outside the monorepo, so it carries its own copy of the
``Ok`` / ``Err`` / ``Refusal`` shape instead of importing an engine package.
Field names and semantics match the engine's railway result, so a value built
here reads the same way there.

AuthorityEffect: None.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Any, Callable, Generic, NoReturn, TypeVar, Union, cast

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")

_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@-]*$")


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return unicodedata.normalize("NFC", value.strip())


@dataclass(frozen=True)
class Refusal:
    code: str
    message: str
    locus: str = ""
    details: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        code = _require_text(self.code, "code")
        if _IDENTIFIER.fullmatch(code) is None:
            raise ValueError("code must be a canonical identifier")
        object.__setattr__(self, "code", code)
        object.__setattr__(self, "message", _require_text(self.message, "message"))
        if self.locus:
            object.__setattr__(self, "locus", _require_text(self.locus, "locus"))
        normalized = tuple((_require_text(k, "detail key"), str(v)) for k, v in self.details)
        if len({key for key, _ in normalized}) != len(normalized):
            raise ValueError("refusal detail keys must be unique")
        object.__setattr__(self, "details", tuple(sorted(normalized)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "locus": self.locus,
            "details": dict(self.details),
        }


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T

    @property
    def is_ok(self) -> bool:
        return True

    @property
    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self.value

    def unwrap_err(self) -> NoReturn:
        raise ValueError("cannot unwrap_err from Ok")

    def map(self, function: Callable[[T], U]) -> Ok[U]:
        return Ok(function(self.value))

    def bind(self, function: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return function(self.value)


@dataclass(frozen=True)
class Err(Generic[E]):
    error: E

    @property
    def is_ok(self) -> bool:
        return False

    @property
    def is_err(self) -> bool:
        return True

    def unwrap(self) -> NoReturn:
        raise ValueError(f"cannot unwrap Err: {self.error}")

    def unwrap_err(self) -> E:
        return self.error

    def map(self, function: Callable[[Any], Any]) -> Err[E]:
        del function
        return self

    def bind(self, function: Callable[[Any], Result[U, E]]) -> Result[U, E]:
        del function
        return cast("Result[U, E]", self)


Result = Union[Ok[T], Err[E]]

__all__ = ["Err", "Ok", "Refusal", "Result"]
