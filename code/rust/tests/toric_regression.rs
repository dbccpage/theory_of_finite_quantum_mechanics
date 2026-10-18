// AuthorityEffect: None.

//! The 2×2 toric stabilizers commute, each edge meets two stars and two
//! plaquettes, and the logical pair `(W_X1, W_Z1)` anticommutes.

use omega_quantum_physics::pauli::Pauli;
use theory_of_finite_qm::qm::campaigns::toric::ToricCode2x2;

#[test]
fn toric_code_two_by_two_reproduces_the_regression_stabilizers() {
    let stars = ToricCode2x2::star_operators();
    let plaquettes = ToricCode2x2::plaquette_operators();
    let (wx1, wz1, wx2, wz2) = ToricCode2x2::logical_operators();

    let mut edge_stars = [0i64; 8];
    let mut edge_plaquettes = [0i64; 8];
    for star in &stars {
        for (qubit, letter) in star.iter().enumerate() {
            edge_stars[qubit] += i64::from(xz(letter).0);
        }
    }
    for plaquette in &plaquettes {
        for (qubit, letter) in plaquette.iter().enumerate() {
            edge_plaquettes[qubit] += i64::from(xz(letter).1);
        }
    }
    assert_eq!(edge_stars, [2; 8]);
    assert_eq!(edge_plaquettes, [2; 8]);

    let vertices = stars.len() as i64;
    let faces = plaquettes.len() as i64;
    let edges_from_stars: i64 = edge_stars.iter().sum::<i64>() / 2;
    let edges_from_plaquettes: i64 = edge_plaquettes.iter().sum::<i64>() / 2;
    assert_eq!(edges_from_stars, edges_from_plaquettes);
    assert_eq!(vertices - edges_from_stars + faces, 0);

    for star in &stars {
        for plaquette in &plaquettes {
            let form = symplectic(star, plaquette);
            let overlap = overlap_parity(star, plaquette);
            assert_eq!(form, overlap);
            assert_eq!(form, 0);
        }
    }

    assert_eq!(symplectic(&wx1, &wz1), 1);
    assert_eq!(symplectic(&wx1, &wz1), overlap_parity(&wx1, &wz1));
    assert_eq!(symplectic(&wx2, &wz2), 1);
    assert_eq!(symplectic(&wx1, &wz2), 0);
    assert_eq!(symplectic(&wx2, &wz1), 0);
}

fn xz(letter: &Pauli) -> (u8, u8) {
    match letter {
        Pauli::I => (0, 0),
        Pauli::X => (1, 0),
        Pauli::Y => (1, 1),
        Pauli::Z => (0, 1),
    }
}

fn symplectic(left: &[Pauli; 8], right: &[Pauli; 8]) -> u8 {
    let mut acc = 0u8;
    for qubit in 0..8 {
        let (x1, z1) = xz(&left[qubit]);
        let (x2, z2) = xz(&right[qubit]);
        acc ^= (x1 & z2) ^ (z1 & x2);
    }
    acc
}

/// Intersection count reduced modulo 2. Addition, not a running xor.
fn overlap_parity(left: &[Pauli; 8], right: &[Pauli; 8]) -> u8 {
    let mut hits = 0i64;
    for qubit in 0..8 {
        let (x1, z1) = xz(&left[qubit]);
        let (x2, z2) = xz(&right[qubit]);
        hits += i64::from(x1 & z2);
        hits += i64::from(z1 & x2);
    }
    (hits.rem_euclid(2)) as u8
}
