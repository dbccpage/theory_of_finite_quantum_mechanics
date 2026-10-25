Status: AI-drafted, awaiting human review.

# PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY

Node status stays CONDITIONAL. The standing text is an integer triangle slice. A general cost, a real or complex repair space, and weighted duality on an arbitrary complex stay outside that slice.

## Coboundary

For integers f0, f1, f2, write d0(f0, f1, f2) = (f1 - f0, f2 - f1, f2 - f0). Adding two vertex triples adds the three output entries, because subtraction distributes over addition. That is the componentwise sum of the two coboundaries.

## Residual identity

Let delta be an integer triple and let g be a vertex triple. The shifted edge triple is delta plus d0(g). Repairing that shift by f + g subtracts d0(f + g). Linearity replaces d0(f + g) by d0(f) + d0(g), and the two copies of d0(g) cancel. The residual equals delta minus d0(f). The sum of the absolute values of the three residual entries is therefore the same number.

## One edge triple

Take delta = (1, 1, 0). For an arbitrary integer repair f, the residual is (1, 1, 0) minus d0(f). The integer pairing of a triple (a, b, c) with the pattern (1, 1, -1) is a + b - c. On a coboundary that pairing is (f1 - f0) + (f2 - f1) - (f2 - f0) = 0. On the residual it is therefore 2. The absolute value of a + b - c is at most |a| + |b| + |c|, so the absolute residual sum is at least 2.

The repair (0, 1, 0) has coboundary (1, -1, 0) and residual (0, 2, 0). The absolute residual sum is 2.

## The same value after a shift

For every integer vertex triple g, the identity above sends the repair (g0, 1 + g1, g2) of delta + d0(g) to the residual of (0, 1, 0). The absolute residual sum is 2. Every other integer repair of the shifted triple has absolute residual sum at least 2, because it matches some integer repair of (1, 1, 0).

## What is proved

Coboundary linearity on integer triples; equality of residuals after adding a coboundary and shifting the repair by the same vertex triple; invariance of the absolute residual sum under that shift; the pairing of every coboundary with (1, 1, -1) is 0; the pairing of every residual of (1, 1, 0) is 2; every integer repair of (1, 1, 0) has absolute residual sum at least 2; the repair (0, 1, 0) attains 2; and both the lower bound and the attained value 2 survive every integer coboundary shift of (1, 1, 0).

## What is assumed

The ring of integers, with the usual addition and multiplication, and the absolute value on that ring. AuthorityEffect is None. The module imports no package.

## What is open

Representative independence for a general cost, attainment on a real or complex repair space, weighted duality on an arbitrary complex, rational repairs, a general coefficient field, and the weak direction named by the earlier bottleneck.
