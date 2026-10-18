# A1 Deterministic Collar Partition Cover

**Grid**: 14 × 14 = 196 cells  
**Cell width**: 22/49  
**Domain**: [0, 44/7]² (rational 2π = 44/7)  

## Results

| Metric | Value |
|---|---|
| Certified cells | **114** |
| Refused cells | 82 |
| Coverage fraction | **57/98** = 0.5816 |
| Certified area | 55176/2401 |
| Total area | 1936/49 |

## Grid Map (✓ = certified, · = refused)

```
       0  1  2  3  4  5  6  7  8  9 10 11 12 13
  0    ·  ·  ✓  ✓  ✓  ✓  ✓  ✓  ·  ·  ·  ·  ·  ·
  1    ·  ·  ·  ✓  ✓  ✓  ✓  ✓  ✓  ·  ·  ·  ·  ·
  2    ✓  ·  ·  ·  ✓  ✓  ✓  ✓  ✓  ✓  ·  ·  ·  ·
  3    ✓  ✓  ·  ·  ·  ✓  ✓  ✓  ✓  ✓  ✓  ·  ·  ·
  4    ✓  ✓  ✓  ·  ·  ·  ✓  ✓  ✓  ✓  ✓  ✓  ·  ·
  5    ✓  ✓  ✓  ✓  ·  ·  ·  ✓  ✓  ✓  ✓  ✓  ✓  ·
  6    ✓  ✓  ✓  ✓  ✓  ·  ·  ·  ✓  ✓  ✓  ✓  ✓  ✓
  7    ✓  ✓  ✓  ✓  ✓  ✓  ·  ·  ·  ✓  ✓  ✓  ✓  ✓
  8    ·  ✓  ✓  ✓  ✓  ✓  ✓  ·  ·  ·  ✓  ✓  ✓  ✓
  9    ·  ·  ✓  ✓  ✓  ✓  ✓  ✓  ·  ·  ·  ✓  ✓  ✓
 10    ·  ·  ·  ✓  ✓  ✓  ✓  ✓  ✓  ·  ·  ·  ✓  ✓
 11    ·  ·  ·  ·  ✓  ✓  ✓  ✓  ✓  ✓  ·  ·  ·  ✓
 12    ·  ·  ·  ·  ·  ✓  ✓  ✓  ✓  ✓  ✓  ·  ·  ·
 13    ·  ·  ·  ·  ·  ·  ✓  ✓  ✓  ✓  ✓  ✓  ·  ·
```

The diagonal band (|i - j| small) is refused because the curvature
gap is too small relative to the cell radius. Off-diagonal cells are certified.

## Certified Cells by Separation |i - j|

| |i - j| | Count | Example margin |
|---|---|---|
| 2 | 24 | 0.151585 |
| 3 | 22 | 0.545487 |
| 4 | 20 | 0.954725 |
| 5 | 18 | 1.237076 |
| 6 | 16 | 1.209677 |
| 7 | 14 | 0.649035 |

## What This Demonstrates

1. The A1 collar partition is a **deterministic tiling** problem —
   no LLM proposer needed.
2. All certified cells have exact rational gap and margin values.
3. The uncovered diagonal band requires either finer grid resolution
   or a different verification model (beyond Taylor degree-4 cos).

## What This Does NOT Demonstrate

- Does not use the actual MUB6 curvature function (uses Taylor cos placeholder).
- Does not connect to the Lean 4 KernelReflectionBisection infrastructure.
- The uncovered diagonal band is the geometrically interesting region.
- Mints no authority regarding MUB(6) existence or non-existence.

---
*AuthorityEffect: None.*