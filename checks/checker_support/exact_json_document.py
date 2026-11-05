"""Owned bounded UTF-8 JSON bytes for exact-arithmetic certificate admission.

AuthorityEffect: None. At most1 MiB,16 nested containers and4096-bit integers;
duplicate members, floats and nonstandard numeric constants are refused.
Each parse returns a new caller-owned tree; the document owns only bytes.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

from .boundary import Violation, evaluate
from .outcome import Outcome

MAX_BYTES=1024*1024


def _depth(raw: bytes) -> None:
    depth=0
    quoted=escaped=False
    for byte in raw:
        if escaped:
            escaped=False
            continue
        if quoted:
            if byte==92:
                escaped=True
            if byte==34:
                quoted=False
            continue
        if byte==34:
            quoted=True
        if byte in (91,123):
            depth+=1
        if byte in (93,125):
            depth-=1
        if depth>16:
            raise Violation('resource','exact JSON exceeds16 nested containers')


def _integer(text: str) -> int:
    if len(text.lstrip('-'))>1234:
        raise Violation('resource','JSON integer exceeds4096 bits')
    value=int(text)
    if value.bit_length()>4096:
        raise Violation('resource','JSON integer exceeds4096 bits')
    return value


def _inexact(text: str) -> object:
    raise Violation('input','exact JSON forbids floats and nonstandard numeric constants')


def _object(pairs: list[tuple[str,object]]) -> dict[str,object]:
    result: dict[str,object]={}
    for key,value in pairs:
        if key in result:
            raise Violation('duplicate','duplicate JSON object member: '+key)
        result[key]=value
    return result


@dataclass(frozen=True,slots=True,init=False)
class ExactJsonDocument:
    """Immutable byte custody; syntax/schema validation is an explicit query."""
    raw: bytes

    def __init__(self,raw: object) -> None:
        if type(raw) is not bytes:
            raise Violation('input','exact JSON document requires bytes')
        if len(raw)>MAX_BYTES:
            raise Violation('resource','exact JSON exceeds1 MiB')
        _depth(raw)
        object.__setattr__(self,'raw',raw)

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.raw).hexdigest()

    def _parse(self) -> object:
        try:
            value: object=json.loads(self.raw.decode('utf-8'),object_pairs_hook=_object,
                                     parse_int=_integer,parse_float=_inexact,parse_constant=_inexact)
        except RecursionError as error:
            raise Violation('resource','exact JSON parser recursion limit') from error
        return value

    def parse(self) -> Outcome[object]:
        return evaluate(self._parse)

    @staticmethod
    def _read(path: object) -> ExactJsonDocument:
        if not isinstance(path,Path):
            raise Violation('input','JSON source must be a filesystem Path')
        with path.open('rb') as stream:
            raw=stream.read(MAX_BYTES+1)
        return ExactJsonDocument(raw)

    @staticmethod
    def read(path: object) -> Outcome[ExactJsonDocument]:
        return evaluate(ExactJsonDocument._read,path)
