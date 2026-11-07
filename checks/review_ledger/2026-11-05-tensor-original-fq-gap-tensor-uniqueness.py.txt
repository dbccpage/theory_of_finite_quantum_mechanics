"""Exact integer determinant controls; no tensor-selection theorem or repository imports."""
from fractions import Fraction
from itertools import product
import json


def det(m):
    return m[0][0]*m[1][1]-m[0][1]*m[1][0]


def rank(m):
    """Independent rational elimination, without calling the determinant."""
    rows = [[Fraction(x) for x in row] for row in m]
    pivot_row = 0
    for col in range(2):
        candidate = next((r for r in range(pivot_row, 2) if rows[r][col]), None)
        if candidate is None:
            continue
        rows[candidate],rows[pivot_row] = rows[pivot_row],rows[candidate]
        pivot = rows[pivot_row][col]
        rows[pivot_row] = [x/pivot for x in rows[pivot_row]]
        for r in range(2):
            if r != pivot_row:
                factor = rows[r][col]
                rows[r] = [x-factor*y for x,y in zip(rows[r],rows[pivot_row])]
        pivot_row += 1
    return pivot_row


def main():
    checks = 0
    def check(ok, label):
        nonlocal checks
        checks += 1
        if not ok:
            raise RuntimeError(label)
    identity=((1,0),(0,1))
    inputs=list(product(range(-3,4), repeat=4))
    inputs.extend([(10**50,-17,10**40,23),(0,0,0,0)])
    for a0,a1,b0,b1 in inputs:
        matrix=((a0*b0,a0*b1),(a1*b0,a1*b1))
        check(det(matrix)==0,'outer determinant')
        check(rank(matrix)<=1,'independent elimination')
        check(matrix!=identity,'identity is not an outer product')
    check(det(identity)==1 and rank(identity)==2,'identity negative control')
    changed=((11,14),(15,21))
    check(det(changed)!=0 and rank(changed)==2,'altered outer-product entry')
    ones=((1,1),(1,1))
    wrong_sign=ones[0][0]*ones[1][1]+ones[0][1]*ones[1][0]
    check(wrong_sign!=det(ones),'wrong determinant sign rejected')
    print(json.dumps({'checks':checks,'failed':0,'input_vectors':len(inputs),'negative_controls':3,'identity_det':det(identity),'scope':'Exact finite census with independent elimination; the universal integer identity is separately Lean checked.'}))

if __name__ == '__main__':
    main()
