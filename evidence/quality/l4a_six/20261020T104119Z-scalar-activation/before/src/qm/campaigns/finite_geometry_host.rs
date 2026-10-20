use crate::qm::finite_witness::{field_q, qstr, qvec};
use crate::linear_algebra::{elimination, matrix as mx, ordered};
use num_traits::{Signed, Zero};
use omega_homology::finite_cliques::cliques;
use omega_lie_theory::cayley::{cayley_transform, is_orthogonal, so_basis};
use omega_lie_theory::finite_group::FiniteGroup;
use omega_number_theory::cyclotomic_integer::CyclotomicInteger as C;
use omega_number_theory::rational::{ri, rq, Rational as Q};
use omega_quantum_physics::finite_geometry::{
    adjacent, cabello, cabello_rays, coloring_count_small, config, d4_rays, e8, interface_defect,
    peres, sorkin, sorkin_coefficients,
};
use serde_json::{json, Value};

#[derive(Debug, thiserror::Error)]
enum GeometryHostError {
    #[error(transparent)]
    Geometry(#[from] omega_quantum_physics::finite_geometry::GeometryError),
    #[error(transparent)]
    Cliques(#[from] omega_homology::finite_cliques::CliqueError),
    #[error(transparent)]
    Group(#[from] omega_lie_theory::finite_group::GroupError),
    #[error(transparent)]
    Matrix(#[from] crate::linear_algebra::ExactFieldError),
    #[error(transparent)]
    Cayley(#[from] omega_lie_theory::cayley::CayleyError),
    #[error(transparent)]
    Ring(#[from] omega_number_theory::cyclotomic_integer::CyclotomicIntegerError),
    #[error("{0}")]
    Input(String),
}
impl From<String> for GeometryHostError {
    fn from(s: String) -> Self {
        Self::Input(s)
    }
}

fn check_cabello_projector(
    ray: &[i64],
) -> Result<(crate::linear_algebra::basic_matrix::BasicMatrix<Q>, bool), GeometryHostError> {
    let norm: i64 = ray.iter().map(|x| x * x).sum();
    let p = mx::from_fn(4, 4, |i, j| rq(ray[i] * ray[j], norm))?;
    let minors_ok = elimination::principal_minors(&p)?
        .iter()
        .all(|x| x >= &ri(0));
    let psd_ok = ordered::is_positive_semidefinite(&p)?;
    let defect_ok = interface_defect(&p, &[ri(1), ri(0), ri(0), ri(0)])?.is_zero();
    Ok((p, minors_ok && psd_ok && defect_ok))
}

fn projectors_pairwise_distinct(
    projectors: &[crate::linear_algebra::basic_matrix::BasicMatrix<Q>],
) -> bool {
    for i in 0..18 {
        for j in i + 1..18 {
            if projectors[i] == projectors[j] {
                return false;
            }
        }
    }
    true
}

fn check_negative_witness_sign(sign: i64) -> Result<bool, GeometryHostError> {
    let p = mx::from_rows(vec![
        vec![rq(-1, 2), ri(0), ri(0), ri(0)],
        vec![ri(0), rq(1, 2), rq(sign, 4), rq(1, 4)],
        vec![ri(0), rq(sign, 4), rq(1, 2), rq(sign, 4)],
        vec![ri(0), rq(1, 4), rq(sign, 4), rq(1, 2)],
    ])?;
    let has_neg_minor = elimination::principal_minors(&p)?
        .iter()
        .any(|x| x < &ri(0));
    let defect_half = interface_defect(&p, &[ri(1), ri(0), ri(0), ri(0)])? == rq(1, 2);
    Ok(has_neg_minor && defect_half)
}

fn interface_checks() -> Result<bool, GeometryHostError> {
    let mut valid = true;
    let mut projectors = vec![];
    for ray in cabello_rays() {
        let (p, ok) = check_cabello_projector(&ray)?;
        valid &= ok;
        projectors.push(p);
    }
    valid &= projectors_pairwise_distinct(&projectors);
    for sign in [-1, 1] {
        valid &= check_negative_witness_sign(sign)?;
    }
    Ok(valid)
}
fn diamond() -> Result<Value, GeometryHostError> {
    let edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)];
    let b1 = mx::from_fn(4, 5, |r, c| {
        ri(i64::from(edges[c].1 == r) - i64::from(edges[c].0 == r))
    })?;
    let b2 = mx::from_rows(vec![
        vec![ri(1), ri(0)],
        vec![ri(-1), ri(0)],
        vec![ri(1), ri(-1)],
        vec![ri(0), ri(1)],
        vec![ri(0), ri(-1)],
    ])?;
    omega_homology::chain_complex::ChainComplex::new(4, 5, 2, b1.clone(), b2.clone())
        .map_err(|e| e.to_string())?;
    let boundary = mx::multiply_vector(&b2, &[ri(1), ri(1)])?;
    let cochain = vec![ri(2), ri(3), ri(-1), ri(4), ri(5)];
    let lhs = mx::dot(&cochain, &boundary)?;
    let rhs = mx::dot(
        &mx::multiply_vector(&mx::transpose(&b2)?, &cochain)?,
        &[ri(1), ri(1)],
    )?;
    Ok(
        json!({"boundary":qvec(&boundary),"betti_0":4-elimination::rank(&b1)?,"betti_1":5-elimination::rank(&b1)?-elimination::rank(&b2)?,"stokes":lhs==rhs,"interior_edge_cancels":boundary[2].is_zero()}),
    )
}
fn lie_basis_checks() -> bool {
    let Ok(basis) = so_basis(8) else {
        return false;
    };
    let flat = mx::from_rows(basis.iter().map(|m| m.as_slice().to_vec()).collect())
        .expect("declared basis shape");
    if elimination::rank(&flat).ok() != Some(28) {
        return false;
    }
    basis.iter().all(|a| {
        basis.iter().all(|b| {
            mx::commutator(a, b)
                .and_then(|c| mx::add(&c, &mx::transpose(&c)?))
                .is_ok_and(|defect| mx::is_zero_matrix(&defect))
        })
    })
}

pub fn run(input: &Value) -> Result<Value, String> {
    evaluate(input).map_err(|e| e.to_string())
}
fn build_skew_matrix() -> Result<crate::linear_algebra::basic_matrix::BasicMatrix<Q>, GeometryHostError> {
    let mut skew = vec![vec![ri(0); 8]; 8];
    for i in 0..8 {
        for j in i + 1..8 {
            skew[i][j] = rq((i + j + 1) as i64, 17);
            skew[j][i] = -skew[i][j].clone();
        }
    }
    Ok(mx::from_rows(skew)?)
}

fn fourier_3_cell_ok(z3: &C, i: usize, j: usize) -> Result<bool, GeometryHostError> {
    let mut s = C::scalar(3, 0)?;
    for k in 0..3 {
        let term = z3.pow((i * k) % 3).conj().mul(&z3.pow((j * k) % 3))?;
        s = s.add(&term)?;
    }
    let expected = C::scalar(3, if i == j { 3 } else { 0 })?;
    Ok(s == expected)
}

fn verify_fourier_3_isometry() -> Result<bool, GeometryHostError> {
    let z3 = C::zeta(3)?;
    for i in 0..3 {
        for j in 0..3 {
            if !fourier_3_cell_ok(&z3, i, j)? {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

fn verify_braid_relation(
    s12: &crate::linear_algebra::basic_matrix::BasicMatrix<Q>,
    s23: &crate::linear_algebra::basic_matrix::BasicMatrix<Q>,
) -> Result<(bool, bool), GeometryHostError> {
    let recoupling_inv = mx::multiply(s23, s23)? == mx::identity(2)?;
    let braid =
        mx::multiply(s23, &mx::multiply(s12, s23)?)? == mx::multiply(s12, &mx::multiply(s23, s12)?)?;
    Ok((recoupling_inv, braid))
}

fn verify_braid_and_characters() -> Result<(bool, bool, bool), GeometryHostError> {
    let s12 = mx::from_rows(vec![vec![ri(1), ri(0)], vec![ri(0), ri(-1)]])?;
    let s23 = mx::from_rows(vec![vec![rq(-1, 2), ri(1)], vec![rq(3, 4), rq(1, 2)]])?;
    let (recoupling_inv, braid) = verify_braid_relation(&s12, &s23)?;
    let group = FiniteGroup::generated(
        &[s12, s23],
        mx::identity(2)?,
        |a, b| mx::multiply(a, b).expect("fixed rational symmetry carrier"),
        |m| m.as_slice().to_vec(),
        12,
    )?;
    let characters = group.character_table()?;
    let orth = characters.verify_row_orthogonality() && characters.verify_column_orthogonality();
    Ok((recoupling_inv, braid, orth))
}

fn apply_signed_perm(v: &[Q], p: &[usize], mask: usize) -> Vec<Q> {
    let mut out = Vec::with_capacity(3);
    for i in 0..3 {
        let sign = if mask & (1 << i) == 0 { 1 } else { -1 };
        out.push(v[p[i]].clone() * ri(sign));
    }
    out
}

fn check_signed_perm_mask(p: &[usize], mask: usize) -> Result<bool, GeometryHostError> {
    let x = vec![ri(2), ri(-3), ri(5)];
    let y = vec![ri(7), ri(1), ri(-2)];
    let a = apply_signed_perm(&x, p, mask);
    let b = apply_signed_perm(&y, p, mask);
    let l1_ok = a.iter().map(Q::abs).sum::<Q>() == x.iter().map(Q::abs).sum::<Q>();
    let dot_ok = mx::dot(&a, &b)? == mx::dot(&x, &y)?;
    Ok(l1_ok && dot_ok)
}

fn verify_signed_permutations() -> Result<bool, GeometryHostError> {
    let perms = omega_combinatorics::enumeration::permutations(3, 6).map_err(|e| e.to_string())?;
    let mut signed = true;
    for p in perms {
        for mask in 0..8 {
            signed &= check_signed_perm_mask(&p, mask)?;
        }
    }
    Ok(signed)
}

fn build_f4_rays() -> Vec<Vec<i64>> {
    let mut f4 = d4_rays();
    for i in 0..4 {
        let mut v = vec![0; 4];
        v[i] = 1;
        f4.push(v);
    }
    for m in 0..8 {
        f4.push(vec![
            1,
            if m & 1 == 0 { 1 } else { -1 },
            if m & 2 == 0 { 1 } else { -1 },
            if m & 4 == 0 { 1 } else { -1 },
        ]);
    }
    f4
}

fn verify_sorkin_pair(a: i64, b: i64) -> Result<bool, GeometryHostError> {
    for d in -3..=3 {
        if !sorkin(&ri(a), &ri(b), &ri(d), 2)?.is_zero() {
            return Ok(false);
        }
    }
    Ok(true)
}

fn verify_sorkin_quadratic_box() -> Result<bool, GeometryHostError> {
    for a in -3..=3 {
        for b in -3..=3 {
            if !verify_sorkin_pair(a, b)? {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

fn verify_hinge_orders() -> Result<bool, GeometryHostError> {
    let z12 = C::zeta(12)?;
    let one12 = C::scalar(12, 1)?;
    for k in [3usize, 4, 6, 12] {
        if z12.pow(12 / k).pow(k) != one12 {
            return Ok(false);
        }
    }
    Ok(true)
}

fn verify_sqrt2_and_sorkin() -> Result<(bool, bool, bool, bool), GeometryHostError> {
    let z8 = C::zeta(8)?;
    let sqrt2 = z8.sub(&z8.pow(3))?;
    let sqrt2_sq = sqrt2.mul(&sqrt2)? == C::scalar(8, 2)?;
    let sorkin_all = verify_sorkin_quadratic_box()?;
    let sorkin_poly = sorkin_coefficients(2)?.values().all(Q::is_zero);
    let sorkin_cubic = sorkin(&ri(1), &ri(1), &ri(1), 3)? == ri(6);
    Ok((sqrt2_sq, sorkin_all, sorkin_poly, sorkin_cubic))
}

fn build_checks_json(
    c: &crate::linear_algebra::basic_matrix::BasicMatrix<Q>,
) -> Result<Value, GeometryHostError> {
    let (sqrt2_sq, sorkin_all, sorkin_poly, sorkin_cubic) = verify_sqrt2_and_sorkin()?;
    let fourier = verify_fourier_3_isometry()?;
    let (recoupling_inv, braid, orth) = verify_braid_and_characters()?;
    let signed = verify_signed_permutations()?;
    let psd = interface_checks()?;
    let hinges = verify_hinge_orders()?;
    Ok(json!({
        "sqrt2_square": sqrt2_sq,
        "fourier_scaled_isometry": fourier,
        "cayley_isometry": is_orthogonal(c),
        "recoupling_involution": recoupling_inv,
        "braid_relation": braid,
        "character_orthogonality": orth,
        "signed_permutations": signed,
        "sorkin_quadratic_box": sorkin_all,
        "sorkin_quadratic_polynomial": sorkin_poly,
        "sorkin_cubic_obstruction": sorkin_cubic,
        "so8_rank_and_brackets": lie_basis_checks(),
        "psd_interface": psd,
        "hinge_orders": hinges
    }))
}

fn build_config_summary(
    rays: &[Vec<i64>],
) -> Result<
    (
        omega_quantum_physics::finite_geometry::Configuration,
        usize,
    ),
    GeometryHostError,
> {
    let adj = adjacent(rays)?;
    let clq = cliques(&adj, 4)?;
    let cfg = config(&adj, &clq)?;
    let col = coloring_count_small(&adj, &clq)?;
    Ok((cfg, col))
}

fn build_f4_config() -> Result<omega_quantum_physics::finite_geometry::Configuration, GeometryHostError> {
    let f4a = adjacent(&build_f4_rays())?;
    let f4_clq = cliques(&f4a, 4)?;
    Ok(config(&f4a, &f4_clq)?)
}

fn build_cayley_and_checks(
    input: &Value,
) -> Result<(Vec<Vec<String>>, Value, String), GeometryHostError> {
    let tau = field_q(input, "tau", rq(1, 3))?;
    let c = cayley_transform(&build_skew_matrix()?, &tau)?;
    let cayley_rows = mx::to_rows(&c)?.iter().map(|r| qvec(r)).collect::<Vec<_>>();
    let checks = build_checks_json(&c)?;
    let sorkin_cub = qstr(&sorkin(&ri(1), &ri(1), &ri(1), 3)?);
    Ok((cayley_rows, checks, sorkin_cub))
}

fn evaluate(input: &Value) -> Result<Value, GeometryHostError> {
    let (d4_cfg, d4_col) = build_config_summary(&d4_rays())?;
    let f4_cfg = build_f4_config()?;
    let (cayley_rows, checks, sorkin_cub) = build_cayley_and_checks(input)?;
    Ok(json!({
        "authority_effect": "None",
        "scope": "exact declared finite configurations; Lie continuum and measure-theoretic conclusions remain source-linked imports",
        "peres": peres(),
        "cabello": cabello(),
        "e8": e8(),
        "d4": d4_cfg,
        "d4_coloring_count": d4_col,
        "f4": f4_cfg,
        "diamond": diamond()?,
        "cayley": cayley_rows,
        "so8_dimension": 8 * 7 / 2,
        "checks": checks,
        "sorkin_cubic": sorkin_cub
    }))
}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exact_interface_and_stokes() {
        assert!(interface_checks().unwrap());
        assert_eq!(diamond().unwrap()["stokes"], true);
        assert!(
            elimination::principal_minors(&mx::from_rows(vec![vec![ri(1), ri(2)]]).unwrap())
                .is_err()
        );
    }

    #[test]
    fn character_orthogonality_is_computed_from_the_matrices() {
        let s12 = mx::from_rows(vec![vec![ri(-1), ri(0)], vec![ri(0), ri(1)]]).unwrap();
        let s23 = mx::from_rows(vec![vec![rq(1, 2), rq(3, 2)], vec![rq(1, 2), rq(-1, 2)]]).unwrap();
        for generators in [vec![s12.clone(), s23], vec![s12]] {
            let group = FiniteGroup::generated(
                &generators,
                mx::identity(2).unwrap(),
                |a, b| mx::multiply(a, b).unwrap(),
                |m| m.as_slice().to_vec(),
                12,
            )
            .unwrap();
            let table = group.character_table().unwrap();
            assert!(table.verify_row_orthogonality() && table.verify_column_orthogonality());
            assert_eq!(
                table.degrees().iter().map(|d| d * d).sum::<usize>(),
                group.order()
            );
        }
    }
}
