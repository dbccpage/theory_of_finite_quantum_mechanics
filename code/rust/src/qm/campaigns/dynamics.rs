//! Program Stone interface pricing. AuthorityEffect: None.
//!
//! A 4-cycle has characteristic polynomial `x^4 - 1`, computed by Laplace
//! expansion of `xI - P` and by the factorization `(x^2 - 1)(x^2 + 1)`.
//! The quadratic factor has no rational root, so a Stone generator is not
//! internal to `M_4(Q)`. Two integer lifts of the same root of unity witness
//! the branch ambiguity.
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct StoneCostingReport {
    pub gap_id: String,
    pub disposition: String,
    pub continuous_time_imported: bool,
    pub strong_continuity_imported: bool,
    pub infinite_branch_ambiguity: bool,
}

/// Returns the formal pricing report for Stone's theorem (GAP-F001-S000-008).
pub fn price_stone_theorem_interface() -> StoneCostingReport {
    let imported = cycle_obstruction().is_ok();
    let branched = distinct_lifts(4).is_ok();
    StoneCostingReport {
        gap_id: "GAP-F001-S000-008".to_string(),
        disposition: if imported {
            "PRICED_CONTINUUM_INTERFACE".to_string()
        } else {
            "RATIONAL_GENERATOR_INTERNAL".to_string()
        },
        continuous_time_imported: imported,
        strong_continuity_imported: imported,
        infinite_branch_ambiguity: branched,
    }
}

/// Laplace determinant of `xI - P` equals `(x^2 - 1)(x^2 + 1)`, and `x^2 + 1`
/// has no rational root.
pub fn cycle_obstruction() -> Result<Vec<i64>, &'static str> {
    let matrix = cycle_pencil(4)?;
    let expanded = poly_trim(&det_poly(&matrix)?);
    let factored = poly_trim(&poly_mul(&poly_mul(&[1, 0, 1], &[-1, 0, 1])?, &[1])?);
    // (x^2+1)(x^2-1) = x^4 - 1. The trailing `[1]` keeps the product total.
    let direct = poly_mul(&[1, 0, 1], &[-1, 0, 1])?;
    if expanded != poly_trim(&direct) || expanded != factored {
        return Err("cycle characteristic polynomial readings disagree");
    }
    if rational_root_exists(&[1, 0, 1])? {
        return Err("x^2+1 split over the rationals");
    }
    Ok(expanded)
}

/// `1` and `1 + order` are distinct integer lifts of the same root of unity.
pub fn distinct_lifts(order: i64) -> Result<(i64, i64), &'static str> {
    if order <= 1 {
        return Err("cycle order is not branching");
    }
    let low = 1i64;
    let high = low.checked_add(order).ok_or("lift overflow")?;
    if low == high || low.rem_euclid(order) != high.rem_euclid(order) {
        return Err("lifts are not a branch pair");
    }
    Ok((low, high))
}

fn cycle_pencil(n: usize) -> Result<Vec<Vec<Vec<i64>>>, &'static str> {
    if n == 0 {
        return Err("empty cycle");
    }
    let mut matrix = vec![vec![vec![0i64]; n]; n];
    for i in 0..n {
        matrix[i][i] = vec![0, 1];
        let next = (i + 1) % n;
        matrix[i][next] = vec![-1];
    }
    Ok(matrix)
}

fn rational_root_exists(poly: &[i64]) -> Result<bool, &'static str> {
    let leading = *poly.last().ok_or("empty polynomial")?;
    let constant = *poly.first().ok_or("empty polynomial")?;
    if leading == 0 || constant == 0 {
        return Err("root test needs nonzero ends");
    }
    // Any rational root in lowest terms divides the constant and the leading
    // coefficient. Both are ±1 here, so the only candidates are ±1.
    for candidate in [1i64, -1] {
        if poly_eval(poly, candidate)? == 0 {
            return Ok(true);
        }
    }
    Ok(false)
}

fn poly_eval(poly: &[i64], at: i64) -> Result<i64, &'static str> {
    let mut acc = 0i64;
    for coeff in poly.iter().rev() {
        acc = acc
            .checked_mul(at)
            .and_then(|v| v.checked_add(*coeff))
            .ok_or("evaluation overflow")?;
    }
    Ok(acc)
}

fn det_poly(matrix: &[Vec<Vec<i64>>]) -> Result<Vec<i64>, &'static str> {
    let n = matrix.len();
    if n == 0 || matrix.iter().any(|row| row.len() != n) {
        return Err("determinant shape");
    }
    if n == 1 {
        return Ok(matrix[0][0].clone());
    }
    let mut acc = vec![0i64];
    for col in 0..n {
        let mut minor = Vec::with_capacity(n - 1);
        for row in 1..n {
            let mut kept = Vec::with_capacity(n - 1);
            for (index, entry) in matrix[row].iter().enumerate() {
                if index != col {
                    kept.push(entry.clone());
                }
            }
            minor.push(kept);
        }
        let cofactor = det_poly(&minor)?;
        let signed = if col % 2 == 0 {
            cofactor
        } else {
            poly_neg(&cofactor)?
        };
        acc = poly_add(&acc, &poly_mul(&matrix[0][col], &signed)?)?;
    }
    Ok(acc)
}

fn poly_add(left: &[i64], right: &[i64]) -> Result<Vec<i64>, &'static str> {
    let n = left.len().max(right.len());
    let mut out = vec![0i64; n];
    for i in 0..n {
        let a = left.get(i).copied().unwrap_or(0);
        let b = right.get(i).copied().unwrap_or(0);
        out[i] = a.checked_add(b).ok_or("polynomial overflow")?;
    }
    Ok(out)
}

fn poly_neg(poly: &[i64]) -> Result<Vec<i64>, &'static str> {
    poly.iter().map(|c| c.checked_neg().ok_or("polynomial overflow")).collect()
}

fn poly_mul(left: &[i64], right: &[i64]) -> Result<Vec<i64>, &'static str> {
    if left.is_empty() || right.is_empty() {
        return Ok(vec![0]);
    }
    let mut out = vec![0i64; left.len() + right.len() - 1];
    for (i, a) in left.iter().enumerate() {
        for (j, b) in right.iter().enumerate() {
            let term = a.checked_mul(*b).ok_or("polynomial overflow")?;
            out[i + j] = out[i + j].checked_add(term).ok_or("polynomial overflow")?;
        }
    }
    Ok(out)
}

fn poly_trim(poly: &[i64]) -> Vec<i64> {
    let mut out = poly.to_vec();
    while out.len() > 1 && out.last() == Some(&0) {
        out.pop();
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stone_interface_costing() {
        let matrix = match cycle_pencil(4) {
            Ok(matrix) => matrix,
            Err(error) => {
                assert!(false, "{error}");
                return;
            }
        };
        let expanded = match det_poly(&matrix) {
            Ok(poly) => poly,
            Err(error) => {
                assert!(false, "{error}");
                return;
            }
        };
        let factored = match poly_mul(&[1, 0, 1], &[-1, 0, 1]) {
            Ok(poly) => poly,
            Err(error) => {
                assert!(false, "{error}");
                return;
            }
        };
        assert_eq!(poly_trim(&expanded), poly_trim(&factored));
        let at_one = match poly_eval(&[1, 0, 1], 1) {
            Ok(value) => value,
            Err(error) => {
                assert!(false, "{error}");
                return;
            }
        };
        let at_neg = match poly_eval(&[1, 0, 1], -1) {
            Ok(value) => value,
            Err(error) => {
                assert!(false, "{error}");
                return;
            }
        };
        assert_ne!(at_one, 0);
        assert_ne!(at_neg, 0);
        let rep = price_stone_theorem_interface();
        assert_eq!(rep.continuous_time_imported, cycle_obstruction().is_ok());
        assert_eq!(rep.infinite_branch_ambiguity, distinct_lifts(4).is_ok());
        assert!(rep.strong_continuity_imported);
        assert!(!rep.gap_id.is_empty());
    }
}
