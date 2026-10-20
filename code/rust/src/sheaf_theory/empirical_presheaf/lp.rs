
use num_traits::{One, Signed, Zero};
use omega_solvers::solver_lp_standard_form::{StandardLp, StandardLpError, StandardLpSolution};

use super::{EmpiricalError, MAX_LP_ENTRIES, Q};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct L1DefectReceipt {
    pub defect: Q,
    pub coefficients: Vec<Q>,
    pub residual: Vec<Q>,
    pub dual_witness: Vec<Q>,
    pub dual_offset: Q,
    pub lp: StandardLpSolution,
}

pub(super) fn dot(a: &[Q], b: &[Q]) -> Q {
    a.iter().zip(b).map(|(x, y)| x * y).sum()
}

pub(super) fn too_large() -> EmpiricalError {
    EmpiricalError::LpSizeLimit {
        limit: MAX_LP_ENTRIES,
    }
}

pub(super) fn bound_dense(rows: usize, columns: usize) -> Result<(), EmpiricalError> {
    match rows.checked_mul(columns) {
        Some(entries) if entries <= MAX_LP_ENTRIES => Ok(()),
        _ => Err(too_large()),
    }
}

fn standard_form_l1(generators: &[Vec<Q>], target: &[Q]) -> Result<StandardLp, EmpiricalError> {
    let (k, m) = (generators.len(), target.len());
    let width = m
        .checked_mul(2)
        .and_then(|twice| twice.checked_add(k))
        .ok_or_else(too_large)?;
    bound_dense(m.checked_add(1).ok_or_else(too_large)?, width)?;
    let mut rows = Vec::with_capacity(m + 1);
    for i in 0..m {
        let mut row = vec![Q::zero(); width];
        for (j, column) in generators.iter().enumerate() {
            row[j] = column[i].clone();
        }
        row[k + i] = -Q::one();
        row[k + m + i] = Q::one();
        rows.push(row);
    }
    let mut rhs = target.to_vec();
    let mut row = vec![Q::zero(); width];
    for slot in row.iter_mut().take(k) {
        *slot = Q::one();
    }
    rows.push(row);
    rhs.push(Q::one());
    let costs = (0..width)
        .map(|j| if j >= k { Q::one() } else { Q::zero() })
        .collect();
    Ok(StandardLp::new(costs, rows, rhs)?)
}

pub fn l1_distance_to_convex_hull(
    generators: &[Vec<Q>],
    target: &[Q],
    pivots: usize,
) -> Result<L1DefectReceipt, EmpiricalError> {
    let (k, m) = (generators.len(), target.len());
    if k == 0 || generators.iter().any(|g| g.len() != m) {
        return Err(EmpiricalError::Shape);
    }
    let lp = standard_form_l1(generators, target)?;
    let solution = lp.solve(pivots)?;
    if !lp.verify(&solution) {
        return Err(EmpiricalError::Lp(StandardLpError::CertificateMismatch));
    }
    let coefficients: Vec<Q> = solution.primal[..k].to_vec();
    let residual: Vec<Q> = (0..m)
        .map(|i| {
            generators
                .iter()
                .zip(&coefficients)
                .map(|(g, c)| &g[i] * c)
                .sum::<Q>()
                - &target[i]
        })
        .collect();
    let receipt = L1DefectReceipt {
        defect: solution.value.clone(),
        coefficients,
        residual,
        dual_witness: solution.dual[..m].to_vec(),
        dual_offset: solution.dual[m].clone(),
        lp: solution,
    };
    if verify_l1_defect_receipt(generators, target, &receipt) {
        Ok(receipt)
    } else {
        Err(EmpiricalError::Lp(StandardLpError::CertificateMismatch))
    }
}

fn verify_l1_shapes_and_subrecords(
    generators: &[Vec<Q>],
    k: usize,
    m: usize,
    receipt: &L1DefectReceipt,
) -> bool {
    if receipt.coefficients.len() != k
        || receipt.residual.len() != m
        || receipt.dual_witness.len() != m
        || generators.iter().any(|g| g.len() != m)
    {
        return false;
    }
    receipt.lp.primal.len() == k + 2 * m
        && receipt.lp.dual.len() == m + 1
        && receipt.lp.primal[..k] == receipt.coefficients[..]
        && receipt.lp.dual[..m] == receipt.dual_witness[..]
        && receipt.lp.dual[m] == receipt.dual_offset
}

fn verify_l1_residuals_and_duality(
    generators: &[Vec<Q>],
    target: &[Q],
    receipt: &L1DefectReceipt,
) -> bool {
    let m = target.len();
    let residual_ok = (0..m).all(|i| {
        let combination: Q = generators
            .iter()
            .zip(&receipt.coefficients)
            .map(|(g, c)| &g[i] * c)
            .sum();
        combination - &target[i] == receipt.residual[i]
    });
    let coefficients_ok = receipt.coefficients.iter().all(|c| !c.is_negative())
        && receipt.coefficients.iter().sum::<Q>() == Q::one();
    let sup_norm_ok = receipt.dual_witness.iter().all(|y| y.abs() <= Q::one());
    let adjoint_ok = generators
        .iter()
        .all(|g| dot(g, &receipt.dual_witness) + &receipt.dual_offset <= Q::zero());
    let gap_zero = dot(target, &receipt.dual_witness) + &receipt.dual_offset == receipt.defect
        && omega_functional::Phi1Functional::unweighted_l1_rational(&receipt.residual).as_ref()
            == Some(&receipt.defect);
    residual_ok && coefficients_ok && sup_norm_ok && adjoint_ok && gap_zero
}

pub fn verify_l1_defect_receipt(
    generators: &[Vec<Q>],
    target: &[Q],
    receipt: &L1DefectReceipt,
) -> bool {
    let (k, m) = (generators.len(), target.len());
    if !verify_l1_shapes_and_subrecords(generators, k, m, receipt) {
        return false;
    }
    let Ok(lp) = standard_form_l1(generators, target) else {
        return false;
    };
    if !lp.verify(&receipt.lp) || receipt.lp.value != receipt.defect {
        return false;
    }
    verify_l1_residuals_and_duality(generators, target, receipt)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn q(n: i64, d: i64) -> Q {
        Q::new(n.into(), d.into())
    }

    #[test]
    fn l1_distance_certifies_zero_and_positive_defects_and_refuses_bad_shapes() {
        let gens = vec![vec![q(1, 1), q(0, 1)], vec![vec![q(0, 1), q(1, 1)]].pop().unwrap()];
        let inside = vec![q(1, 2), q(1, 2)];
        let r0 = l1_distance_to_convex_hull(&gens, &inside, 64).unwrap();
        assert_eq!(r0.defect, q(0, 1));
        assert!(verify_l1_defect_receipt(&gens, &inside, &r0));

        let outside = vec![q(1, 1), q(1, 1)];
        let r1 = l1_distance_to_convex_hull(&gens, &outside, 64).unwrap();
        assert_eq!(r1.defect, q(1, 1));
        assert!(verify_l1_defect_receipt(&gens, &outside, &r1));

        let mut tampered = r1.clone();
        tampered.defect = q(0, 1);
        assert!(!verify_l1_defect_receipt(&gens, &outside, &tampered));
        assert_eq!(
            l1_distance_to_convex_hull(&[], &inside, 64),
            Err(EmpiricalError::Shape)
        );
    }
}
