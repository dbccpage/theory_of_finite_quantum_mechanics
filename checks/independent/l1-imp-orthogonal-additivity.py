#!/usr/bin/env python3
"""Exact controls for one integer coefficient matrix; no arbitrary-frame theorem."""
from __future__ import annotations
import json


def expanded(matrix: tuple[tuple[int, int], tuple[int, int]], a: int, b: int) -> int:
    return matrix[0][0]*a*a + matrix[0][1]*a*b + matrix[1][0]*b*a + matrix[1][1]*b*b


def matrix_readout(matrix: tuple[tuple[int, int], tuple[int, int]], vector: tuple[int, int]) -> int:
    product = tuple(sum(entry*x for entry, x in zip(row, vector)) for row in matrix)
    return sum(x*y for x, y in zip(vector, product))


def main() -> None:
    checks = 0
    def check(condition: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            raise RuntimeError(label)
    matrix = ((1, 1), (-1, 1))
    check(matrix[0][1]+matrix[1][0] == 0, 'pair cancellation')
    check(matrix[0][1] != 0 and matrix[1][0] != 0, 'entrywise-zero inference rejected')
    check(matrix[0][1] != matrix[1][0], 'matrix is not symmetric')
    # Coefficients of a^2, ab, b^2, using integer commutativity.
    coefficients = (matrix[0][0], matrix[0][1]+matrix[1][0], matrix[1][1])
    check(coefficients == (1, 0, 1), 'polynomial coefficient identity')
    vectors = [(a,b) for a in range(-8,9) for b in range(-8,9)]
    for a,b in vectors:
        value=matrix_readout(matrix,(a,b))
        check(value == expanded(matrix,a,b), 'separate matrix multiplication')
        check(value == a*a+b*b, 'diagonal readout')
        check(value == matrix_readout(matrix,(a,0))+matrix_readout(matrix,(0,b)), 'axis additivity')
    symmetric = ((1,1),(1,1))
    check(matrix_readout(symmetric,(1,1)) != matrix_readout(symmetric,(1,0))+matrix_readout(symmetric,(0,1)), 'changed off-diagonal sign breaks additivity')
    check(matrix_readout(symmetric,(1,1)) != 2, 'changed coefficient breaks readout')
    check(matrix_readout(((1,0),(0,1)),(2,-3)) == 13, 'symmetric diagonal positive control')
    print(json.dumps({'checks':checks,'failed':0,'vectors':len(vectors),'coefficient_identity':coefficients,'negative_controls':2,'scope':'One nonsymmetric integer coefficient matrix and a finite input census; universal integer statements are separately Lean checked.'}))

if __name__ == '__main__':
    main()
