//! Program branch-correlation fixtures. AuthorityEffect: None.
use num_traits::One;
use omega_number_theory::rational::{rq, Rational, Zero};
/// s_quantum = 14/5 = 2.8, max_classical = 2.
pub fn chsh_pythagorean_s() -> (Rational, i64, bool) {
    let a1 = (rq(0, 1), rq(1, 1));
    let a2 = (rq(1, 1), rq(0, 1));
    let b1 = (rq(-3, 5), rq(4, 5));
    let b2 = (rq(4, 5), rq(3, 5));

    // Check orthonormality
    let dot = |u: &(Rational, Rational), v: &(Rational, Rational)| {
        crate::linear_algebra::matrix::dot(
            &[u.0.clone(), u.1.clone()],
            &[v.0.clone(), v.1.clone()],
        )
        .expect("fixed two-vector shape")
    };
    assert!(dot(&a1, &a1) == Rational::one());
    assert!(dot(&a2, &a2) == Rational::one());
    assert!(dot(&b1, &b1) == Rational::one());
    assert!(dot(&b2, &b2) == Rational::one());
    assert!(dot(&a1, &a2) == Rational::zero());
    assert!(dot(&b1, &b2) == Rational::zero());

    // Correlations E(a, b) = - <a, b>
    let e11 = -dot(&a1, &b1); // -4/5
    let e12 = -dot(&a1, &b2); // -3/5
    let e21 = -dot(&a2, &b1); // +3/5
    let e22 = -dot(&a2, &b2); // -4/5

    let s_raw = &e11 + &e12 - &e21 + &e22;
    let s_quantum = if s_raw < Rational::zero() {
        -s_raw
    } else {
        s_raw
    };
    assert_eq!(s_quantum, rq(14, 5));

    let mut max_classical = 0i64;
    for &va1 in &[-1i64, 1i64] {
        for &va2 in &[-1i64, 1i64] {
            for &vb1 in &[-1i64, 1i64] {
                for &vb2 in &[-1i64, 1i64] {
                    let val = (va1 * vb1 + va1 * vb2 - va2 * vb1 + va2 * vb2).abs();
                    if val > max_classical {
                        max_classical = val;
                    }
                }
            }
        }
    }
    assert_eq!(max_classical, 2);

    let violates = s_quantum > rq(max_classical, 1);
    (s_quantum, max_classical, violates)
}

/// Evaluates Cabello 18-ray contextuality parity obstruction (Target 6 / H020).
///
/// 18 rays in {-1, 0, 1}^4, 9 tetrads, degree 2 for every ray.
/// Parity obstruction: 9 = 2k has no integer solution in Z.
pub fn cabello_18_ray_parity_obstruction() -> bool {
    let rays = &omega_quantum_physics::kochen_specker::CABELLO_18_VECTORS;
    let tetrads = &omega_quantum_physics::kochen_specker::CABELLO_9_CONTEXTS;

    // Verify orthogonality
    for tet in tetrads {
        for i in 0..4 {
            for j in (i + 1)..4 {
                let u = rays[tet[i]];
                let v = rays[tet[j]];
                let dot = u[0] * v[0] + u[1] * v[1] + u[2] * v[2] + u[3] * v[3];
                assert_eq!(dot, 0, "Non-orthogonal rays in tetrad");
            }
        }
    }

    // Check ray degrees
    let mut degrees = [0usize; 18];
    for tet in tetrads {
        for &r in tet {
            degrees[r] += 1;
        }
    }

    assert!(
        degrees.iter().all(|&d| d == 2),
        "Ray degree not identically 2"
    );
    let total_incidence: usize = degrees.iter().sum();
    assert_eq!(total_incidence, 36);

    // Every context selects one ray; every ray occurs twice. Odd contexts
    // therefore contradict the even number of selected incidences.
    tetrads.len() % 2 == 1 && degrees.iter().all(|d| *d == 2)
}

/// Demonstrates non-signaling across Everett measurement branches via vanishing cross-branch transitions.
pub fn verify_branch_non_signaling() -> bool {
    use omega_quantum_physics::exact_hermitian::{gi, partial_trace_first, partial_trace_second};
    use omega_quantum_physics::relative_state_branching::RelativeStatePacket;
    let packet = RelativeStatePacket::new(
        vec![gi(1, 0), gi(1, 0)],
        vec![vec![gi(1, 0), gi(0, 0)], vec![gi(0, 0), gi(1, 0)]],
    )
    .expect("fixed normalized records");
    let coherent = packet.global_state();
    let mixture = packet.branch_mixture();
    partial_trace_first(&coherent, 2, 2).expect("fixed bipartite shape")
        == partial_trace_first(&mixture, 2, 2).expect("fixed bipartite shape")
        && partial_trace_second(&coherent, 2, 2).expect("fixed bipartite shape")
            == partial_trace_second(&mixture, 2, 2).expect("fixed bipartite shape")
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_chsh_pythagorean_violation() {
        let (s, max_c, violates) = chsh_pythagorean_s();
        assert_eq!(s, rq(14, 5));
        assert_eq!(max_c, 2);
        assert!(violates);
    }
    #[test]
    fn test_cabello_18_ray_obstruction() {
        assert!(cabello_18_ray_parity_obstruction());
    }
    #[test]
    fn test_everett_branch_non_signaling() {
        assert!(verify_branch_non_signaling());
    }
}
