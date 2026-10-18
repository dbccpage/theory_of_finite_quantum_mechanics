//! JSON host of the exact finite configurations of the QM_122 paper.
//!
//! `run` assembles one report from the configurations computed in
//! `omega_quantum_physics::finite_geometry` (Peres, Cabello, the 24-cell and E8 as
//! orthogonality hypergraphs, the Sorkin polynomials, the Cayley transform and its
//! isometry check, the character orthogonality of a generated group) and from the
//! declared checks that are the paper's own: the two-triangle diamond complex, the
//! so(8) basis, the positive-semidefinite interface of the Cabello projectors, the
//! recoupling matrices and the signed permutations. Enumerations have explicit
//! finite bounds.
//!
//! AuthorityEffect: None.
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

fn interface_checks() -> Result<bool, GeometryHostError> {
    let mut valid = true;
    let mut projectors = vec![];
    for ray in cabello_rays() {
        let norm: i64 = ray.iter().map(|x| x * x).sum();
        let p = mx::from_fn(4, 4, |i, j| rq(ray[i] * ray[j], norm))?;
        valid &= elimination::principal_minors(&p)?
            .iter()
            .all(|x| x >= &ri(0))
            && ordered::is_positive_semidefinite(&p)?
            && interface_defect(&p, &[ri(1), ri(0), ri(0), ri(0)])?.is_zero();
        projectors.push(p);
    }
    for i in 0..18 {
        for j in i + 1..18 {
            valid &= projectors[i] != projectors[j];
        }
    }
    for sign in [-1, 1] {
        let p = mx::from_rows(vec![
            vec![rq(-1, 2), ri(0), ri(0), ri(0)],
            vec![ri(0), rq(1, 2), rq(sign, 4), rq(1, 4)],
            vec![ri(0), rq(sign, 4), rq(1, 2), rq(sign, 4)],
            vec![ri(0), rq(1, 4), rq(sign, 4), rq(1, 2)],
        ])?;
        valid &= elimination::principal_minors(&p)?
            .iter()
            .any(|x| x < &ri(0))
            && interface_defect(&p, &[ri(1), ri(0), ri(0), ri(0)])? == rq(1, 2);
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
fn evaluate(input: &Value) -> Result<Value, GeometryHostError> {
    let tau = field_q(input, "tau", rq(1, 3))?;
    let mut skew = vec![vec![ri(0); 8]; 8];
    for i in 0..8 {
        for j in i + 1..8 {
            skew[i][j] = rq((i + j + 1) as i64, 17);
            skew[j][i] = -skew[i][j].clone();
        }
    }
    let c = cayley_transform(&mx::from_rows(skew)?, &tau)?;
    let z8 = C::zeta(8)?;
    let sqrt2 = z8.sub(&z8.pow(3))?;
    let z3 = C::zeta(3)?;
    let fourier = (0..3).all(|i| {
        (0..3).all(|j| {
            let s = (0..3).fold(C::scalar(3, 0).expect("fixed conductor"), |s, k| {
                s.add(
                    &z3.pow((i * k) % 3)
                        .conj()
                        .mul(&z3.pow((j * k) % 3))
                        .unwrap(),
                )
                .unwrap()
            });
            s == C::scalar(3, if i == j { 3 } else { 0 }).expect("fixed conductor")
        })
    });
    let s12 = mx::from_rows(vec![vec![ri(1), ri(0)], vec![ri(0), ri(-1)]]).expect("fixed shape");
    let s23 =
        mx::from_rows(vec![vec![rq(-1, 2), ri(1)], vec![rq(3, 4), rq(1, 2)]]).expect("fixed shape");
    // The braid relation s23 s12 s23 = s12 s23 s12. The source calls it a
    // pentagon; no 6j symbols exist here, so no Biedenharn-Elliott identity is checked.
    let braid = mx::multiply(&s23, &mx::multiply(&s12, &s23)?)?
        == mx::multiply(&s12, &mx::multiply(&s23, &s12)?)?;
    let group = FiniteGroup::generated(
        &[s12.clone(), s23.clone()],
        mx::identity(2)?,
        |a, b| mx::multiply(a, b).expect("fixed rational symmetry carrier"),
        |m| m.as_slice().to_vec(),
        12,
    )?;
    let characters = group.character_table()?;
    let orth = characters.verify_row_orthogonality() && characters.verify_column_orthogonality();
    let mut signed = true;
    for p in omega_combinatorics::enumeration::permutations(3, 6).map_err(|e| e.to_string())? {
        for mask in 0..8 {
            let x = vec![ri(2), ri(-3), ri(5)];
            let y = vec![ri(7), ri(1), ri(-2)];
            let apply = |v: &Vec<Q>| {
                (0..3)
                    .map(|i| v[p[i]].clone() * ri(if mask & (1 << i) == 0 { 1 } else { -1 }))
                    .collect::<Vec<_>>()
            };
            let a = apply(&x);
            let b = apply(&y);
            signed &= a.iter().map(Q::abs).sum::<Q>() == x.iter().map(Q::abs).sum::<Q>()
                && mx::dot(&a, &b)? == mx::dot(&x, &y)?;
        }
    }
    let d4 = adjacent(&d4_rays())?;
    let mut f4 = d4_rays();
    for i in 0..4 {
        let mut v = vec![0; 4];
        v[i] = 1;
        f4.push(v)
    }
    for m in 0..8 {
        f4.push(vec![
            1,
            if m & 1 == 0 { 1 } else { -1 },
            if m & 2 == 0 { 1 } else { -1 },
            if m & 4 == 0 { 1 } else { -1 },
        ]);
    }
    let f4a = adjacent(&f4)?;
    let peres = peres();
    let cabello = cabello();
    let e8 = e8();
    let mut sorkin_all = true;
    for a in -3..=3 {
        for b in -3..=3 {
            for d in -3..=3 {
                sorkin_all &= sorkin(&ri(a), &ri(b), &ri(d), 2)?.is_zero();
            }
        }
    }
    Ok(
        json!({"authority_effect":"None","scope":"exact declared finite configurations; Lie continuum and measure-theoretic conclusions remain source-linked imports",
      "peres":peres,"cabello":cabello,"e8":e8,"d4":config(&d4,&cliques(&d4,4)?)?,"d4_coloring_count":coloring_count_small(&d4,&cliques(&d4,4)?)?,"f4":config(&f4a,&cliques(&f4a,4)?)?,"diamond":diamond()?,
      "cayley":mx::to_rows(&c)?.iter().map(|r|qvec(r)).collect::<Vec<_>>(),"so8_dimension":8*7/2,
      "checks":{"sqrt2_square":sqrt2.mul(&sqrt2)?==C::scalar(8,2)?,"fourier_scaled_isometry":fourier,"cayley_isometry":is_orthogonal(&c),"recoupling_involution":mx::multiply(&s23,&s23)?==mx::identity(2)?,"braid_relation":braid,"character_orthogonality":orth,"signed_permutations":signed,"sorkin_quadratic_box":sorkin_all,"sorkin_quadratic_polynomial":sorkin_coefficients(2)?.values().all(Q::is_zero),"sorkin_cubic_obstruction":sorkin(&ri(1),&ri(1),&ri(1),3)?==ri(6),"so8_rank_and_brackets":lie_basis_checks(),"psd_interface":interface_checks()?,"hinge_orders":([3usize,4,6,12].iter().all(|&k|C::zeta(12).unwrap().pow(12/k).pow(k)==C::scalar(12,1).expect("fixed conductor")))},"sorkin_cubic":qstr(&sorkin(&ri(1),&ri(1),&ri(1),3)?)}),
    )
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

    /// The characters are read off the generated group: the rational
    /// recoupling matrices give S3 and orthogonal rows; a single reflection
    /// generates a group of two classes, and three characters cannot then be
    /// orthogonal class functions.
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
