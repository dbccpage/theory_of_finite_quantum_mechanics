"""Independent Z/5Z circle table for L1-U1-SELECTOR-OTHER-SEGMENT.

No repository imports. Exact integer arithmetic only.
"""
failures = 0
checked = 0

def check(cond, msg):
    global failures, checked
    checked += 1
    if not cond:
        failures += 1
        print('FAIL', msg)

def norm(x, y):
    return (x * x + y * y) % 5

def mul(a, b, c, d):
    return ((a * c + 4 * b * d) % 5, (a * d + b * c) % 5)

def main():
    global checked, failures
    failures = 0
    checked = 0
    solutions = [(x, y) for x in range(5) for y in range(5) if norm(x, y) == 1]
    check(solutions == [(0, 1), (0, 4), (1, 0), (4, 0)], 'solution list')
    check(len(solutions) == 4, 'solution count')
    check(4 == 5 - 1, '4 = 5 - 1')
    check(5 + 1 == 6, '5 + 1 = 6')
    check(4 != 6, '4 != 6')
    check((4 + 1) % 5 == 0, '4 + 1 = 0 in Z/5Z')
    check(mul(0, 1, 0, 1) == (4, 0), 'square of (0, 1)')
    check((4, 0) != (1, 0), 'square differs from (1, 0)')
    check(mul(4, 0, 0, 1) == (0, 4), 'third power')
    check(mul(0, 4, 0, 1) == (1, 0), 'fourth power')
    check(norm(1, 1) == 2, '(1, 1) has norm 2')
    check(2 != 1, '2 != 1')
    check((2, 1) != (0, 0), '(2, 1) is nonzero')
    check(norm(2, 1) == 0, '(2, 1) has norm 0')
    fold = 0
    for x in range(5):
        for y in range(5):
            if (x * x + y * y) % 5 == 1:
                fold += 1
    check(fold == 4, 'range fold count')
    check(5 * 5 == 25, 'residue pairs')
    agree = True
    for a in range(5):
        for b in range(5):
            for c in range(5):
                for d in range(5):
                    if (a * c + 4 * b * d) % 5 != (a * c - b * d) % 5:
                        agree = False
    check(agree, 'coefficient 4 matches subtraction on all 625 products')
    check(5 ** 4 == 625, 'product tuples')
    print(f'checked {checked} claims, failures {failures}')
    raise SystemExit(failures)
if __name__ == '__main__':
    main()
