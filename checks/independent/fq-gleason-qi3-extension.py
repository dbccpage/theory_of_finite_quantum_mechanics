"""Exact finite obstruction to extending the prescribed Q^3 exotic to Q(i)^3.

AuthorityEffect: None. The independent-checking bounded context owns a closed
certificate schema and replays geometry and its integer linear contradiction.
At most 512 rays, 1024 frames, 512 prescriptions and 4096-bit intermediates.
No positivity, regularity, symmetry or classification of other functions follows.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from math import gcd
from pathlib import Path
import re
import sys
from typing import cast

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate, require
from checker_support.domains import Failure, integer, sequence
from checker_support.exact_json_document import ExactJsonDocument
from checker_support.outcome import Outcome

Vector = tuple[int, ...]
TARGET = 'FQ-GLEASON-QI3-FRAME-FUNCTIONS'
NORMALIZATION = 'g(v) = 3*f(v)-1'
KEYS = frozenset(('target', 'base_commit', 'normalization', 'contradiction_rhs',
                  'rays', 'frames', 'real_values'))
DEFAULT_SOURCE = Path(__file__).parent / 'data' / 'fq_gleason_qi3_extension.json'


def _bounded(value: object) -> int:
    result = integer(value, 'certificate integer')
    if result.bit_length() > 4096:
        raise Violation('resource', 'certificate integer exceeds 4096 bits')
    return result


def _row(value: object, length: int) -> Vector:
    return tuple(_bounded(x) for x in sequence(value, 'certificate row', length))


def _schema(value: object) -> dict[str, object]:
    if type(value) is not dict or len(value) != len(KEYS) or set(value) != KEYS:
        raise Violation('input', 'certificate must contain exactly the declared fields')
    data = cast(dict[str, object], value)
    if (type(data['target']) is not str or type(data['normalization']) is not str
            or data['target'] != TARGET or data['normalization'] != NORMALIZATION):
        raise Violation('input', 'wrong target or normalization')
    commit = data['base_commit']
    if type(commit) is not str or re.fullmatch('[0-9a-f]{40}', commit) is None:
        raise Violation('input', 'base_commit must be a lowercase forty-digit hexadecimal identifier')
    if _bounded(data['contradiction_rhs']) != 32:
        raise Violation('input', 'claimed contradiction must be 32')
    return data


def _rays(value: object) -> tuple[Vector, ...]:
    rays = tuple(_row(row, 6) for row in sequence(value, 'rays', maximum=512))
    if not rays:
        raise Violation('input', 'empty ray list')
    if len(set(rays)) != len(rays):
        raise Violation('duplicate', 'duplicate ray')
    for ray in rays:
        if gcd(*ray) != 1:
            raise Violation('input', 'ray must be nonzero with integer content one')
    return rays


def _records(value: object, width: int, indices: int, count: int,
             maximum: int) -> tuple[Vector, ...]:
    rows = tuple(_row(row, width) for row in sequence(value, 'constraints', maximum=maximum))
    if not rows:
        raise Violation('input', 'empty constraint list')
    for row in rows:
        if row[-1] == 0:
            raise Violation('input', 'zero constraint weight')
        if any(i < 0 or i >= count for i in row[:indices]):
            raise Violation('input', 'ray index out of range')
    return rows


def _inner(u: Vector, v: Vector) -> tuple[int, int]:
    real = imag = 0
    for k in (0, 2, 4):
        real_term = _bounded(_bounded(u[k]*v[k]) + _bounded(u[k+1]*v[k+1]))
        imag_term = _bounded(_bounded(u[k]*v[k+1]) - _bounded(u[k+1]*v[k]))
        real = _bounded(real + real_term)
        imag = _bounded(imag + imag_term)
    return real, imag


def _sign(ray: Vector) -> int:
    require(all(ray[k] == 0 for k in (1, 3, 5)), 'prescribed ray must be real')
    odd = tuple(x for x in ray[::2] if x % 2)
    if len(odd) != 2:
        return 0
    return -1 if (odd[0] % 4 - odd[1] % 4) % 4 == 0 else 1


@dataclass(frozen=True, slots=True, init=False)
class GaussianExtensionCertificate:
    """Owned literal vector constraints; a commit identifier is not authentication."""
    rays: tuple[Vector, ...]
    frames: tuple[Vector, ...]
    real_values: tuple[Vector, ...]
    base_commit: str

    def __init__(self, value: object) -> None:
        data = _schema(value)
        rays = _rays(data['rays'])
        frames = _records(data['frames'], 4, 3, len(rays), 1024)
        real_values = _records(data['real_values'], 3, 1, len(rays), 512)
        object.__setattr__(self, 'rays', rays)
        object.__setattr__(self, 'frames', frames)
        object.__setattr__(self, 'real_values', real_values)
        object.__setattr__(self, 'base_commit', data['base_commit'])

    def to_record(self) -> dict[str, object]:
        return {'target': TARGET, 'normalization': NORMALIZATION, 'base_commit': self.base_commit,
                'contradiction_rhs': 32, 'rays': [list(row) for row in self.rays],
                'frames': [list(row) for row in self.frames],
                'real_values': [list(row) for row in self.real_values]}

    def _frames(self, coefficients: list[int]) -> int:
        total = 0
        for a, b, c, weight in self.frames:
            u, v, w = self.rays[a], self.rays[b], self.rays[c]
            require(_inner(u, v) == _inner(u, w) == _inner(v, w) == (0, 0),
                    'frame is not pairwise Hermitian orthogonal')
            for i in (a, b, c):
                coefficients[i] = _bounded(coefficients[i] + weight)
            total = _bounded(total + weight)
        return total

    def _prescriptions(self, coefficients: list[int]) -> tuple[int, int]:
        total = rhs = 0
        signs: set[int] = set()
        for index, sign, weight in self.real_values:
            require(sign == _sign(self.rays[index]), 'wrong exotic real-ray value')
            coefficients[index] = _bounded(coefficients[index] + weight)
            rhs = _bounded(rhs + _bounded(weight * sign))
            total = _bounded(total + weight)
            signs.add(sign)
        require(signs == {-1, 0, 1}, 'missing prescribed exotic value')
        return total, rhs

    def _verify(self) -> dict[str, int]:
        coefficients = [0] * len(self.rays)
        frame_total = self._frames(coefficients)
        real_total, rhs = self._prescriptions(coefficients)
        require(not any(coefficients), 'linear combination leaves a variable')
        require(rhs == 32, 'wrong contradiction right side')
        require(_bounded(_bounded(3 * frame_total) + real_total) == 0,
                'constant terms fail to cancel')
        return {'rays': len(self.rays), 'frames': len(self.frames),
                'real_values': len(self.real_values), 'contradiction_rhs': rhs}

    def verify(self) -> Outcome[dict[str, int]]:
        return evaluate(self._verify)


def verify(data: object) -> Outcome[dict[str, int]]:
    return evaluate(GaussianExtensionCertificate, data).bind(lambda certificate: certificate.verify())


def read_certificate(path: object) -> Outcome[GaussianExtensionCertificate]:
    return ExactJsonDocument.read(path).bind(lambda doc: doc.parse()).bind(
        lambda data: evaluate(GaussianExtensionCertificate, data))


def _negative_controls(certificate: GaussianExtensionCertificate) -> tuple[tuple[str, object], ...]:
    records = [certificate.to_record() for _ in range(4)]
    frames = cast(list[list[int]], records[0]['frames'])
    frames[0][3] += 1
    a, b, _, _ = certificate.frames[0]
    rays = cast(list[list[int]], records[1]['rays'])
    rays[a] = [x+y for x, y in zip(certificate.rays[a], certificate.rays[b])]
    prescriptions = cast(list[list[int]], records[2]['real_values'])
    prescriptions[0][1] += 1
    cast(list[list[object]], records[3]['rays'])[0][0] = True
    return tuple(zip(('frame coefficient', 'nonorthogonal vector', 'exotic value',
                      'Boolean coordinate'), records))


def _self_test(certificate: GaussianExtensionCertificate) -> tuple[str, ...]:
    labels = []
    for label, changed in _negative_controls(certificate):
        require(not verify(changed).ok, label + ': corrupted certificate was accepted')
        labels.append(label)
    return tuple(labels)


def self_test(certificate: object) -> Outcome[tuple[str, ...]]:
    if not isinstance(certificate, GaussianExtensionCertificate):
        return Outcome(error=Failure('input', 'expected extension certificate'))
    return evaluate(_self_test, certificate)


def _main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    # The outer CLI boundary translates expected refusals and preserves cancellation.
    certificate_result = read_certificate(args.certificate)
    if certificate_result.error is not None:
        raise Violation(certificate_result.error.kind, certificate_result.error.message)
    certificate = cast(GaussianExtensionCertificate, certificate_result.value)
    result = certificate._verify()
    labels = _self_test(certificate) if args.self_test else ()
    print(json.dumps(result, sort_keys=True))
    print('Exact certificate: 0 = 32 for g=3*f-1. No signed extension of the prescribed exotic.')
    print('Not established by this certificate: classification or existence of other nonquadratic Q(i)^3 frame functions.')
    for label in labels:
        print('Negative control rejected: ' + label)


def main() -> int:
    return cli(_main)


if __name__ == '__main__':
    raise SystemExit(main())
