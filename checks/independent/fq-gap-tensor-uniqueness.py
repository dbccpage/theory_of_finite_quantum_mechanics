"""Integer 2 by 2 outer-product determinants. No repository imports."""

def det(m00, m01, m10, m11):
    return m00 * m11 - m01 * m10


def main():
    failures = 0
    checks = 0
    for a0 in range(-3, 4):
        for a1 in range(-3, 4):
            for b0 in range(-3, 4):
                for b1 in range(-3, 4):
                    checks += 1
                    row = (a0 * b0, a0 * b1, a1 * b0, a1 * b1)
                    if det(*row) != 0:
                        failures += 1
                    if row == (1, 0, 0, 1):
                        failures += 1
    ident = det(1, 0, 0, 1)
    checks += 1
    if ident != 1:
        failures += 1
    sample = det(2 * 5, 2 * 7, 3 * 5, 3 * 7)
    checks += 1
    if sample != 0:
        failures += 1
    print(f"checks={checks} identity_det={ident} sample_det={sample} failures={failures}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
