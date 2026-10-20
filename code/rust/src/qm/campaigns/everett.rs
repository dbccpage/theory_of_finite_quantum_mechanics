use num_traits::One;
use omega_number_theory::rational::{rq, Rational, Zero};
fn dot_pair(u: &(Rational, Rational), v: &(Rational, Rational)) -> Rational {
    crate::linear_algebra::matrix::dot(
        &[u.0.clone(), u.1.clone()],
        &[v.0.clone(), v.1.clone()],
    )
    .expect("fixed two-vector shape")
}

fn classical_chsh_for_mask(mask: u8) -> i64 {
    let sign = |bit: u8| if (mask >> bit) & 1 == 0 { -1i64 } else { 1i64 };
    let va1 = sign(0);
    let va2 = sign(1);
    let vb1 = sign(2);
    let vb2 = sign(3);
    (va1 * vb1 + va1 * vb2 - va2 * vb1 + va2 * vb2).abs()
}

fn max_classical_chsh() -> i64 {
    let mut max_classical = 0i64;
    for mask in 0..16u8 {
        let val = classical_chsh_for_mask(mask);
        if val > max_classical {
            max_classical = val;
        }
    }
    max_classical
}

pub fn chsh_pythagorean_s() -> (Rational, i64, bool) {
    let a1 = (rq(0, 1), rq(1, 1));
    let a2 = (rq(1, 1), rq(0, 1));
    let b1 = (rq(-3, 5), rq(4, 5));
    let b2 = (rq(4, 5), rq(3, 5));

    assert!(dot_pair(&a1, &a1) == Rational::one());
    assert!(dot_pair(&a2, &a2) == Rational::one());
    assert!(dot_pair(&b1, &b1) == Rational::one());
    assert!(dot_pair(&b2, &b2) == Rational::one());
    assert!(dot_pair(&a1, &a2) == Rational::zero());
    assert!(dot_pair(&b1, &b2) == Rational::zero());

    let e11 = -dot_pair(&a1, &b1);
    let e12 = -dot_pair(&a1, &b2);
    let e21 = -dot_pair(&a2, &b1);
    let e22 = -dot_pair(&a2, &b2);

    let s_raw = &e11 + &e12 - &e21 + &e22;
    let s_quantum = if s_raw < Rational::zero() {
        -s_raw
    } else {
        s_raw
    };
    assert_eq!(s_quantum, rq(14, 5));

    let max_classical = max_classical_chsh();
    assert_eq!(max_classical, 2);

    let violates = s_quantum > rq(max_classical, 1);
    (s_quantum, max_classical, violates)
}

pub fn cabello_18_ray_parity_obstruction() -> bool {
    let rays = &omega_quantum_physics::kochen_specker::CABELLO_18_VECTORS;
    let tetrads = &omega_quantum_physics::kochen_specker::CABELLO_9_CONTEXTS;

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

    tetrads.len() % 2 == 1 && degrees.iter().all(|d| *d == 2)
}

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
