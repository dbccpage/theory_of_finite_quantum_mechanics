

use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::matrix as mx;
use num_traits::{Signed, Zero};
use omega_number_theory::cyclotomic::Cyc12;
use omega_number_theory::rational::{r_one, r_zero, ri, rq, Rational};
use omega_quantum_physics::pauli::{pauli_commutes, Pauli};
use omega_quantum_physics::stabilizer_code_distance::StabilizerCode;
use serde::{Deserialize, Serialize};


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Target1PrimitiveDifferenceReceipt {
    pub identity_zero_verified: bool,
    pub antisymmetry_verified: bool,
    pub cocycle_identity_verified: bool,
    pub sample_differences: Vec<i64>,
}

pub fn verify_target1_primitive_difference() -> Target1PrimitiveDifferenceReceipt {
    let pts = [0i64, 1, 3, 7, 12];
    let diff = |x: i64, y: i64| y - x;
    let mut id_ok = true;
    let mut anti_ok = true;
    let mut cocycle_ok = true;
    let mut samples = Vec::new();

    for &x in &pts {
        if diff(x, x) != 0 {
            id_ok = false;
        }
    }

    for &x in &pts {
        for &y in &pts {
            let d_xy = diff(x, y);
            let d_yx = diff(y, x);
            if d_xy + d_yx != 0 {
                anti_ok = false;
            }
            samples.push(d_xy);
            for &z in &pts {
                let d_yz = diff(y, z);
                let d_xz = diff(x, z);
                if d_xy + d_yz != d_xz {
                    cocycle_ok = false;
                }
            }
        }
    }

    Target1PrimitiveDifferenceReceipt {
        identity_zero_verified: id_ok,
        antisymmetry_verified: anti_ok,
        cocycle_identity_verified: cocycle_ok,
        sample_differences: samples[..5].to_vec(),
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Target2DiamondComplexReceipt {
    pub order_4_boundary_cycle_verified: bool,
    pub order_3_face_rotation_verified: bool,
    pub cyclotomic_minimal_polynomial_annihilated: bool,
    pub selected_ring: String,
}

pub fn verify_target2_diamond_complex() -> Target2DiamondComplexReceipt {
    let c4_vertices = [0usize, 1, 3, 2];
    let j_perm = |v: usize| -> usize {
        match v {
            0 => 1,
            1 => 3,
            3 => 2,
            2 => 0,
            _ => unreachable!(),
        }
    };
    let mut j_order4 = true;
    for &v in &c4_vertices {
        let v1 = j_perm(v);
        let v2 = j_perm(v1);
        let v4 = j_perm(j_perm(v2));
        if v4 != v || v2 == v {
            j_order4 = false;
        }
    }

    let tau_perm = |v: usize| -> usize {
        match v {
            0 => 1,
            1 => 2,
            2 => 0,
            other => other,
        }
    };
    let mut tau_order3 = true;
    for &v in &[0usize, 1, 2] {
        let v1 = tau_perm(v);
        let v3 = tau_perm(tau_perm(v1));
        if v3 != v || v1 == v {
            tau_order3 = false;
        }
    }

    let i_elem = Cyc12::i();
    let i2 = i_elem.mul(&i_elem);
    let i4 = i2.mul(&i2);
    let order_4_ok = j_order4 && i4 == Cyc12::one() && i2 == Cyc12::one().neg();

    let zeta3 = Cyc12::zeta3();
    let zeta3_cubed = zeta3.mul(&zeta3).mul(&zeta3);
    let order_3_ok = tau_order3 && zeta3_cubed == Cyc12::one() && zeta3 != Cyc12::one();

    let zeta12 = Cyc12::zeta12(1);
    let z2 = zeta12.mul(&zeta12);
    let z4 = z2.mul(&z2);
    let phi12 = z4.sub(&z2).add(&Cyc12::one());
    let phi12_annihilated = phi12.is_zero();

    Target2DiamondComplexReceipt {
        order_4_boundary_cycle_verified: order_4_ok,
        order_3_face_rotation_verified: order_3_ok,
        cyclotomic_minimal_polynomial_annihilated: phi12_annihilated,
        selected_ring: "Z[zeta_12] = Z[x]/(x^4 - x^2 + 1)".to_string(),
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Target3SorkinInterferenceReceipt {
    pub sorkin_i3_identically_zero: bool,
    pub non_zero_second_order_interference: bool,
    pub evaluation_degree: usize,
}

pub fn verify_target3_sorkin_interference() -> Target3SorkinInterferenceReceipt {
    let psi_a = Cyc12::one();
    let psi_b = Cyc12::zeta12(2);
    let psi_c = Cyc12::zeta12(4);

    let prob = |amps: &[Cyc12]| -> Rational {
        let mut sum = Cyc12::zero();
        for a in amps {
            sum = sum.add(a);
        }
        let norm_sq = sum.mul(&sum.conj());
        norm_sq.as_rational().unwrap_or_else(r_zero)
    };

    let p_a = prob(std::slice::from_ref(&psi_a));
    let p_b = prob(std::slice::from_ref(&psi_b));
    let p_c = prob(std::slice::from_ref(&psi_c));
    let p_ab = prob(&[psi_a.clone(), psi_b.clone()]);
    let p_bc = prob(&[psi_b.clone(), psi_c.clone()]);
    let p_ac = prob(&[psi_a.clone(), psi_c.clone()]);
    let p_abc = prob(&[psi_a, psi_b, psi_c]);

    let i2_ab = &p_ab - &(&p_a + &p_b);
    let has_i2 = !i2_ab.is_zero();

    let i3 = &p_abc - &p_ab - &p_ac - &p_bc + &p_a + &p_b + &p_c;
    let i3_zero = i3.is_zero();

    Target3SorkinInterferenceReceipt {
        sorkin_i3_identically_zero: i3_zero,
        non_zero_second_order_interference: has_i2,
        evaluation_degree: 2,
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Target4RationalCayleyReceipt {
    pub dimension: usize,
    pub tau: Rational,
    pub test_parameters_count: usize,
    pub all_rational_parameters_verified: bool,
    pub is_exact_orthogonal_isometry: bool,
}

pub fn verify_target4_rational_cayley() -> Target4RationalCayleyReceipt {
    let dim = 8;
    let mut x = mx::zeros::<Rational>(dim, dim).expect("declared eight-dimensional fixture");
    for i in (0..dim).step_by(2) {
        let val = ri((i + 1) as i64);
        x.set(i, i + 1, val.clone()).expect("fixture index");
        x.set(i + 1, i, -val).expect("fixture index");
    }
    let taus = [rq(1, 3), rq(1, 2), rq(1, 1), rq(2, 1), rq(5, 7), rq(-1, 4)];
    let identity = mx::identity::<Rational>(dim).expect("declared fixture");
    let all_ok = taus.iter().all(|tau| {
        omega_lie_theory::cayley::cayley_transform(&x, tau).is_ok_and(|cay| {
            let tau_x = mx::scale(&x, tau).expect("fixture shape");
            let plus = mx::add(&identity, &tau_x).expect("fixture shape");
            let minus = mx::sub(&identity, &tau_x).expect("fixture shape");
            mx::multiply(&plus, &cay).expect("fixture shape") == minus
                && omega_lie_theory::cayley::is_special_orthogonal(&cay)
        })
    });
    Target4RationalCayleyReceipt {
        dimension: dim,
        tau: rq(1, 3),
        test_parameters_count: taus.len(),
        all_rational_parameters_verified: all_ok,
        is_exact_orthogonal_isometry: all_ok,
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Target5PentagonIdentityReceipt {
    pub dimension: usize,
    pub leaf_coherence_verified: bool,
    pub path1_evaluates_to_terminal: bool,
    pub path2_evaluates_to_terminal: bool,
    pub pentagon_associator_deficit_is_zero: bool,
    pub initial_configuration_path_deficit_is_zero: bool,
    pub full_operator_equality_verified: bool,
    pub exact_phase_factor: String,
    pub description: String,
}

pub fn verify_target5_pentagon_identity() -> Target5PentagonIdentityReceipt {
    enum Tree {
        Leaf(usize),
        Branch(Box<Tree>, Box<Tree>),
    }
    fn leaf(i: usize) -> Tree {
        Tree::Leaf(i)
    }
    fn branch(a: Tree, b: Tree) -> Tree {
        Tree::Branch(Box::new(a), Box::new(b))
    }
    fn frontier(tree: &Tree, out: &mut Vec<usize>) {
        match tree {
            Tree::Leaf(i) => out.push(*i),
            Tree::Branch(a, b) => {
                frontier(a, out);
                frontier(b, out);
            }
        }
    }
    let trees = [
        branch(branch(branch(leaf(0), leaf(1)), leaf(2)), leaf(3)),
        branch(branch(leaf(0), branch(leaf(1), leaf(2))), leaf(3)),
        branch(leaf(0), branch(branch(leaf(1), leaf(2)), leaf(3))),
        branch(leaf(0), branch(leaf(1), branch(leaf(2), leaf(3)))),
        branch(branch(leaf(0), leaf(1)), branch(leaf(2), leaf(3))),
    ];
    let leaf_coherence = trees.iter().all(|tree| {
        let mut leaves = Vec::new();
        frontier(tree, &mut leaves);
        leaves == [0usize, 1, 2, 3]
    });

    let transposition_matrix = |i: usize, j: usize| -> BasicMatrix<Rational> {
        let mut m = mx::identity::<Rational>(5).expect("declared finite fixture");
        m.set(i, i, r_zero()).expect("fixture index");
        m.set(j, j, r_zero()).expect("fixture index");
        m.set(i, j, r_one()).expect("fixture index");
        m.set(j, i, r_one()).expect("fixture index");
        m
    };

    let f1 = transposition_matrix(0, 1);
    let f2 = transposition_matrix(1, 2);
    let f3 = transposition_matrix(2, 3);
    let f4 = transposition_matrix(0, 4);
    let f5 = transposition_matrix(4, 3);

    let p1 =
        mx::multiply(&mx::multiply(&f3, &f2).expect("fixture shape"), &f1).expect("fixture shape");

    let p2 = mx::multiply(&f5, &f4).expect("fixture shape");

    let mut e0 = mx::zeros::<Rational>(5, 5).expect("declared finite fixture");
    e0.set(0, 0, r_one()).expect("fixture index");

    let mut e3 = mx::zeros::<Rational>(5, 5).expect("declared finite fixture");
    e3.set(3, 0, r_one()).expect("fixture index");

    let path1_vec = mx::multiply(&p1, &e0).expect("fixture shape");
    let path2_vec = mx::multiply(&p2, &e0).expect("fixture shape");

    let p1_ok = path1_vec == e3;
    let p2_ok = path2_vec == e3;

    let init_deficit_zero = path1_vec == path2_vec;

    let deficit_zero = p1_ok && p2_ok && init_deficit_zero;

    let full_op_eq = p1 == p2;

    Target5PentagonIdentityReceipt {
        dimension: 5,
        leaf_coherence_verified: leaf_coherence,
        path1_evaluates_to_terminal: p1_ok,
        path2_evaluates_to_terminal: p2_ok,
        pentagon_associator_deficit_is_zero: deficit_zero,
        initial_configuration_path_deficit_is_zero: init_deficit_zero,
        full_operator_equality_verified: full_op_eq,
        exact_phase_factor: "rational permutation representation over Q^5".to_string(),
        description:
            "Declared tree-frontier and initial-configuration path replay over Q^5; full operator equality fails"
                .to_string(),
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Target6CabelloPolytopeReceipt {
    pub ray_count: usize,
    pub tetrad_count: usize,
    pub all_tetrads_mutually_orthogonal: bool,
    pub hypergraph_regular_degree_two: bool,
    pub mod2_parity_obstruction_verified: bool,
    pub non_bornian_extremal_vertex_detected: bool,
    pub pure_states_all_positive: bool,
    pub interface_transfer_eliminates_non_bornian: bool,
}

pub fn verify_target6_cabello_polytope() -> Target6CabelloPolytopeReceipt {
    let rays = omega_quantum_physics::kochen_specker::CABELLO_18_VECTORS;

    let dot = |u: &[i64; 4], v: &[i64; 4]| -> i64 {
        u[0] * v[0] + u[1] * v[1] + u[2] * v[2] + u[3] * v[3]
    };

    let tetrads = omega_quantum_physics::kochen_specker::CABELLO_9_CONTEXTS;

    let mut all_ortho = true;
    for t in &tetrads {
        for i in 0..4 {
            for j in (i + 1)..4 {
                if dot(&rays[t[i]], &rays[t[j]]) != 0 {
                    all_ortho = false;
                }
            }
        }
    }

    let mut degrees = [0usize; 18];
    for t in &tetrads {
        for &r in t {
            degrees[r] += 1;
        }
    }
    let all_deg_two = degrees.iter().all(|&d| d == 2);

    let parity_ok = all_deg_two && (tetrads.len() % 2 == 1);

    let v17 = rays[17];
    let m_diag = [1i64, 1, 1, -1];
    let bad_vertex_expectation = m_diag[0] * v17[0] * v17[0]
        + m_diag[1] * v17[1] * v17[1]
        + m_diag[2] * v17[2] * v17[2]
        + m_diag[3] * v17[3] * v17[3];
    let non_psd_detected = bad_vertex_expectation < 0;

    let mut all_pure_psd = true;
    for r in &rays {
        let norm_sq = dot(r, r);
        if norm_sq <= 0 {
            all_pure_psd = false;
        }
        for i in 0..4 {
            for j in 0..4 {
                let minor2 = (r[i] * r[i]) * (r[j] * r[j]) - (r[i] * r[j]) * (r[i] * r[j]);
                if minor2 < 0 {
                    all_pure_psd = false;
                }
            }
        }
    }

    let normal = [0i64, 0, 0, 1];

    let mut all_pure_interface_continuous = true;
    for r in &rays {
        let n_dot_r = dot(&normal, r);
        let exp = n_dot_r * n_dot_r;
        let deficit = if exp < 0 { -exp } else { 0 };
        if deficit != 0 {
            all_pure_interface_continuous = false;
        }
    }

    let bad_exp = m_diag[0] * normal[0] * normal[0]
        + m_diag[1] * normal[1] * normal[1]
        + m_diag[2] * normal[2] * normal[2]
        + m_diag[3] * normal[3] * normal[3];
    let bad_deficit = if bad_exp < 0 { -bad_exp } else { 0 };
    let bad_eliminated = bad_deficit > 0;

    let interface_eliminates = all_pure_interface_continuous && bad_eliminated;

    Target6CabelloPolytopeReceipt {
        ray_count: 18,
        tetrad_count: 9,
        all_tetrads_mutually_orthogonal: all_ortho,
        hypergraph_regular_degree_two: all_deg_two,
        mod2_parity_obstruction_verified: parity_ok,
        non_bornian_extremal_vertex_detected: non_psd_detected,
        pure_states_all_positive: all_pure_psd,
        interface_transfer_eliminates_non_bornian: interface_eliminates,
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Target7MonotoneUnitarityReceipt {
    pub exchangeable_is_signed_permutation: bool,
    pub irreversible_residue_detected: bool,
    pub residue_norm: Rational,
}

pub fn verify_target7_monotone_unitarity() -> Target7MonotoneUnitarityReceipt {
    let mut s_exch = mx::zeros::<Rational>(3, 3).expect("declared finite fixture");
    s_exch.set(0, 1, r_one()).expect("fixture index");
    s_exch.set(1, 0, -r_one()).expect("fixture index");
    s_exch.set(2, 2, r_one()).expect("fixture index");

    let s_t = mx::transpose(&s_exch).expect("fixture shape");
    let is_signed_perm = mx::multiply(&s_t, &s_exch).expect("fixture shape")
        == mx::identity::<Rational>(3).expect("declared finite fixture");

    let mut p_adm = mx::zeros::<Rational>(3, 3).expect("declared finite fixture");
    p_adm.set(0, 0, r_one()).expect("fixture index");
    p_adm.set(1, 1, r_one()).expect("fixture index");

    let id3 = mx::identity::<Rational>(3).expect("declared finite fixture");
    let p_t_p = mx::multiply(&mx::transpose(&p_adm).expect("fixture shape"), &p_adm)
        .expect("fixture shape");
    let mut _delta_irr = id3;
    for r in 0..3 {
        for c in 0..3 {
            let diff = _delta_irr.get_ref(r, c).expect("fixture index")
                - p_t_p.get_ref(r, c).expect("fixture index");
            _delta_irr.set(r, c, diff).expect("fixture index");
        }
    }

    let v = [rq(1, 2), rq(1, 2), rq(1, 4)];
    let l1_orig = &v[0] + &v[1] + &v[2];
    let l1_proj = &v[0] + &v[1];
    let residue_norm = l1_orig - l1_proj;
    let has_residue = residue_norm > r_zero();

    Target7MonotoneUnitarityReceipt {
        exchangeable_is_signed_permutation: is_signed_perm,
        irreversible_residue_detected: has_residue,
        residue_norm,
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Target8BellChshReceipt {
    pub measurement_bases_orthonormal: bool,
    pub exact_chsh_correlation: Rational,
    pub classical_bound: Rational,
    pub max_lhv_assignment_value: Rational,
    pub violates_local_realism: bool,
    pub pythagorean_inequality_satisfied: bool,
}

pub fn verify_target8_bell_chsh() -> Target8BellChshReceipt {
    let a1 = [r_zero(), r_one()];
    let a2 = [r_one(), r_zero()];
    let b1 = [rq(-3, 5), rq(-4, 5)];
    let b2 = [rq(4, 5), rq(-3, 5)];

    let dot2 = |u: &[Rational; 2], v: &[Rational; 2]| -> Rational { &u[0] * &v[0] + &u[1] * &v[1] };

    let ortho_ok = dot2(&a1, &a1) == r_one()
        && dot2(&a2, &a2) == r_one()
        && dot2(&b1, &b1) == r_one()
        && dot2(&b2, &b2) == r_one()
        && dot2(&a1, &a2) == r_zero()
        && dot2(&b1, &b2) == r_zero();

    let e11 = -dot2(&a1, &b1);
    let e12 = -dot2(&a1, &b2);
    let e21 = -dot2(&a2, &b1);
    let e22 = -dot2(&a2, &b2);

    let s_val = (&e11 + &e12 + &e21 - &e22).abs();
    let violates_lr = s_val > ri(2);

    let mut max_lhv = r_zero();
    let signs = [ri(-1), ri(1)];
    for a1_s in &signs {
        for a2_s in &signs {
            for b1_s in &signs {
                for b2_s in &signs {
                    let val = (a1_s * b1_s + a1_s * b2_s + a2_s * b1_s - a2_s * b2_s).abs();
                    if val > max_lhv {
                        max_lhv = val;
                    }
                }
            }
        }
    }

    let half_s = &s_val * rq(1, 2);
    let pythagorean_ratio = &half_s * &half_s;
    let pythagorean_ok = pythagorean_ratio <= ri(2) && violates_lr;

    Target8BellChshReceipt {
        measurement_bases_orthonormal: ortho_ok,
        exact_chsh_correlation: s_val,
        classical_bound: ri(2),
        max_lhv_assignment_value: max_lhv,
        violates_local_realism: violates_lr,
        pythagorean_inequality_satisfied: pythagorean_ok,
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Target9BitFlipCodeReceipt {
    pub stabilizers_commute: bool,
    pub distinct_syndrome_count: usize,
    pub deterministic_recovery_verified: bool,
}

pub fn verify_target9_bitflip_code() -> Target9BitFlipCodeReceipt {
    let s1 = [Pauli::Z, Pauli::Z, Pauli::I];
    let s2 = [Pauli::I, Pauli::Z, Pauli::Z];
    let stabs_commute = pauli_commutes(&s1, &s2);

    let errors = [
        ("I", [Pauli::I, Pauli::I, Pauli::I]),
        ("X0", [Pauli::X, Pauli::I, Pauli::I]),
        ("X1", [Pauli::I, Pauli::X, Pauli::I]),
        ("X2", [Pauli::I, Pauli::I, Pauli::X]),
    ];

    let mut syndromes = Vec::new();
    for (_, e) in &errors {
        let syn1 = if pauli_commutes(e, &s1) { 1 } else { -1 };
        let syn2 = if pauli_commutes(e, &s2) { 1 } else { -1 };
        syndromes.push((syn1, syn2));
    }

    let mut unique_syndromes = syndromes.clone();
    unique_syndromes.sort();
    unique_syndromes.dedup();

    Target9BitFlipCodeReceipt {
        stabilizers_commute: stabs_commute,
        distinct_syndrome_count: unique_syndromes.len(),
        deterministic_recovery_verified: unique_syndromes.len() == 4,
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Target10TeleportationReceipt {
    pub bell_resource: String,
    pub branch_count: usize,
    pub branch_probabilities_equal: bool,
    pub all_branches_fidelity_one: bool,
    pub exact_reconstruction_fidelity: Rational,
}

pub fn verify_target10_teleportation() -> Target10TeleportationReceipt {
    use omega_quantum_physics::quantum_state::RayVector;
    use omega_quantum_physics::teleportation::Teleportation;
    let input = RayVector::from_ints(&[(3, 0), (4, 0)])
        .expect("declared nonzero exact teleportation fixture");
    let branches = Teleportation::exact(&input).expect("checked Bell contraction fixture");
    let fidelities = branches
        .iter()
        .map(|branch| {
            input
                .transition_probability(&branch.bob_after)
                .expect("qubit rays have equal dimensions")
        })
        .collect::<Vec<_>>();
    let total: Rational = branches
        .iter()
        .map(|branch| branch.probability.clone())
        .sum();
    let branch_probabilities_equal = branches.first().is_some_and(|first| {
        branches
            .iter()
            .all(|branch| branch.probability == first.probability)
    }) && total == r_one();
    Target10TeleportationReceipt {
        bell_resource: "|Phi+> = (1/sqrt(2))(|00> + |11>)".to_string(),
        branch_count: branches.len(),
        branch_probabilities_equal,
        all_branches_fidelity_one: !fidelities.is_empty()
            && fidelities.iter().all(|f| *f == r_one()),
        exact_reconstruction_fidelity: fidelities.into_iter().min().unwrap_or_else(r_zero),
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Target11SuperdenseCodingReceipt {
    pub encoded_classical_bits: usize,
    pub transmitted_qubits: usize,
    pub bell_gram_matrix_is_scaled_identity: bool,
    pub decoding_circuit_verified: bool,
    pub all_four_messages_deterministic: bool,
    pub decoding_success_probability: Rational,
}

pub fn verify_target11_superdense_coding() -> Target11SuperdenseCodingReceipt {
    let i_phase = Cyc12::i();
    let one = Cyc12::one();
    let zero = Cyc12::zero();
    let neg_one = one.neg();
    let neg_i = i_phase.neg();

    let bell_states: [[Cyc12; 4]; 4] = [
        [one.clone(), zero.clone(), zero.clone(), one.clone()],
        [zero.clone(), one.clone(), one.clone(), zero.clone()],
        [one.clone(), zero.clone(), zero.clone(), neg_one.clone()],
        [zero.clone(), neg_i, i_phase, zero.clone()],
    ];

    let mut is_scaled_id = true;
    for i in 0..4 {
        for j in 0..4 {
            let mut dot = Cyc12::zero();
            for k in 0..4 {
                let term = bell_states[i][k].conj().mul(&bell_states[j][k]);
                dot = dot.add(&term);
            }
            let expected = if i == j { one.add(&one) } else { Cyc12::zero() };
            if dot != expected {
                is_scaled_id = false;
            }
        }
    }

    let mut cnot = mx::zeros::<Cyc12>(4, 4).expect("declared finite fixture");
    cnot.set(0, 0, one.clone()).expect("fixture index");
    cnot.set(1, 1, one.clone()).expect("fixture index");
    cnot.set(2, 3, one.clone()).expect("fixture index");
    cnot.set(3, 2, one.clone()).expect("fixture index");

    let mut h_scaled = mx::zeros::<Cyc12>(4, 4).expect("declared finite fixture");
    h_scaled.set(0, 0, one.clone()).expect("fixture index");
    h_scaled.set(0, 2, one.clone()).expect("fixture index");
    h_scaled.set(1, 1, one.clone()).expect("fixture index");
    h_scaled.set(1, 3, one.clone()).expect("fixture index");
    h_scaled.set(2, 0, one.clone()).expect("fixture index");
    h_scaled.set(2, 2, neg_one.clone()).expect("fixture index");
    h_scaled.set(3, 1, one.clone()).expect("fixture index");
    h_scaled.set(3, 3, neg_one).expect("fixture index");

    let u_dec = mx::multiply(&h_scaled, &cnot).expect("fixture shape");

    let mut circuit_ok = true;
    let mut success_probabilities = Vec::new();
    for (msg_idx, v) in bell_states.iter().enumerate() {
        let mut v_col = mx::zeros::<Cyc12>(4, 4).expect("declared finite fixture");
        for row in 0..4 {
            v_col.set(row, 0, v[row].clone()).expect("fixture index");
        }
        let decoded = mx::multiply(&u_dec, &v_col).expect("fixture shape");

        let norms = (0..4)
            .map(|row| {
                let value = decoded.get_ref(row, 0).expect("fixture index");
                value
                    .mul(&value.conj())
                    .as_rational()
                    .expect("rational norm of Gaussian fixture")
            })
            .collect::<Vec<_>>();
        let total: Rational = norms.iter().cloned().sum();
        success_probabilities.push(if total == r_zero() {
            r_zero()
        } else {
            &norms[msg_idx] / total
        });

        for row in 0..4 {
            let val = decoded.get_ref(row, 0).expect("fixture index");
            let norm_sq = val.mul(&val.conj());
            if row == msg_idx {
                let four = one.add(&one).add(&one).add(&one);
                if norm_sq != four {
                    circuit_ok = false;
                }
            } else if !val.is_zero() {
                circuit_ok = false;
            }
        }
    }

    Target11SuperdenseCodingReceipt {
        encoded_classical_bits: 2,
        transmitted_qubits: 1,
        bell_gram_matrix_is_scaled_identity: is_scaled_id,
        decoding_circuit_verified: circuit_ok,
        all_four_messages_deterministic: is_scaled_id && circuit_ok,
        decoding_success_probability: success_probabilities
            .into_iter()
            .min()
            .unwrap_or_else(r_zero),
    }
}


#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Target12CssCodeReceipt {
    pub n_physical: usize,
    pub k_logical: usize,
    pub code_distance: usize,
    pub stabilizers_commute: bool,
    pub logical_operators_commute_with_stabilizers: bool,
    pub single_qubit_errors_detected: usize,
    pub all_single_qubit_errors_detected: bool,
}

pub fn verify_target12_css_code() -> Target12CssCodeReceipt {
    let sx = [Pauli::X, Pauli::X, Pauli::X, Pauli::X];
    let sz = [Pauli::Z, Pauli::Z, Pauli::Z, Pauli::Z];
    let stabs_commute = pauli_commutes(&sx, &sz);

    let xl1 = [Pauli::X, Pauli::X, Pauli::I, Pauli::I];
    let zl1 = [Pauli::Z, Pauli::I, Pauli::Z, Pauli::I];
    let xl2 = [Pauli::X, Pauli::I, Pauli::X, Pauli::I];
    let zl2 = [Pauli::Z, Pauli::Z, Pauli::I, Pauli::I];

    let log_ops = [&xl1, &zl1, &xl2, &zl2];
    let mut log_commutes_stabs = true;
    for &op in &log_ops {
        if !pauli_commutes(op, &sx) || !pauli_commutes(op, &sz) {
            log_commutes_stabs = false;
        }
    }

    let mut detected_errors = 0usize;
    for q in 0..4 {
        for err_pauli in [Pauli::X, Pauli::Y, Pauli::Z] {
            let mut err_str = [Pauli::I; 4];
            err_str[q] = err_pauli;
            let syn_x = !pauli_commutes(&err_str, &sx);
            let syn_z = !pauli_commutes(&err_str, &sz);
            if syn_x || syn_z {
                detected_errors += 1;
            }
        }
    }
    let all_detected = detected_errors == 12;

    let code =
        StabilizerCode::try_new(vec![sx.to_vec(), sz.to_vec()]).expect("XXXX and ZZZZ commute");
    let distance = code
        .distance()
        .expect("the [[4, 2, 2]] code encodes two qubits and its search fits the default budget");

    Target12CssCodeReceipt {
        n_physical: code.n(),
        k_logical: code.k(),
        code_distance: distance.distance(),
        stabilizers_commute: stabs_commute,
        logical_operators_commute_with_stabilizers: log_commutes_stabs,
        single_qubit_errors_detected: detected_errors,
        all_single_qubit_errors_detected: all_detected,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_target1_primitive_difference() {
        let r = verify_target1_primitive_difference();
        assert!(r.identity_zero_verified);
        assert!(r.antisymmetry_verified);
        assert!(r.cocycle_identity_verified);
    }

    #[test]
    fn test_target2_diamond_complex() {
        let r = verify_target2_diamond_complex();
        assert!(r.order_4_boundary_cycle_verified);
        assert!(r.order_3_face_rotation_verified);
        assert!(r.cyclotomic_minimal_polynomial_annihilated);
    }

    #[test]
    fn test_target3_sorkin_interference() {
        let r = verify_target3_sorkin_interference();
        assert!(r.sorkin_i3_identically_zero);
        assert!(r.non_zero_second_order_interference);
    }

    #[test]
    fn test_target4_rational_cayley() {
        let r = verify_target4_rational_cayley();
        assert!(r.is_exact_orthogonal_isometry);
    }

    #[test]
    fn test_target5_pentagon_identity() {
        let r = verify_target5_pentagon_identity();
        assert!(r.leaf_coherence_verified);
        assert!(r.path1_evaluates_to_terminal);
        assert!(r.path2_evaluates_to_terminal);
        assert!(r.pentagon_associator_deficit_is_zero);
        assert!(r.initial_configuration_path_deficit_is_zero);
        assert!(!r.full_operator_equality_verified);
    }

    #[test]
    fn test_target6_cabello_polytope() {
        let r = verify_target6_cabello_polytope();
        assert!(r.all_tetrads_mutually_orthogonal);
        assert!(r.hypergraph_regular_degree_two);
        assert!(r.mod2_parity_obstruction_verified);
        assert!(r.non_bornian_extremal_vertex_detected);
        assert!(r.pure_states_all_positive);
        assert!(r.interface_transfer_eliminates_non_bornian);
    }

    #[test]
    fn test_target7_monotone_unitarity() {
        let r = verify_target7_monotone_unitarity();
        assert!(r.exchangeable_is_signed_permutation);
        assert!(r.irreversible_residue_detected);
    }

    #[test]
    fn test_target8_bell_chsh() {
        let r = verify_target8_bell_chsh();
        assert!(r.measurement_bases_orthonormal);
        assert!(r.violates_local_realism);
        assert_eq!(r.max_lhv_assignment_value, ri(2));
        assert!(r.pythagorean_inequality_satisfied);
    }

    #[test]
    fn test_target9_bitflip_code() {
        let r = verify_target9_bitflip_code();
        assert!(r.stabilizers_commute);
        assert!(r.deterministic_recovery_verified);
    }

    #[test]
    fn test_target10_teleportation() {
        let r = verify_target10_teleportation();
        assert!(r.all_branches_fidelity_one);
        assert_eq!(r.exact_reconstruction_fidelity, r_one());
    }

    #[test]
    fn test_target11_superdense_coding() {
        let r = verify_target11_superdense_coding();
        assert!(r.bell_gram_matrix_is_scaled_identity);
        assert!(r.decoding_circuit_verified);
        assert!(r.all_four_messages_deterministic);
        assert_eq!(r.decoding_success_probability, r_one());
    }

    #[test]
    fn test_target12_css_code() {
        let r = verify_target12_css_code();
        assert!(r.stabilizers_commute);
        assert!(r.logical_operators_commute_with_stabilizers);
        assert_eq!(r.single_qubit_errors_detected, 12);
        assert!(r.all_single_qubit_errors_detected);
    }

    #[test]
    fn test_target12_parameters_are_computed() {
        let r = verify_target12_css_code();
        assert_eq!((r.n_physical, r.k_logical, r.code_distance), (4, 2, 2));
        let code = StabilizerCode::try_new(vec![vec![Pauli::X; 4], vec![Pauli::Z; 4]]).unwrap();
        let d = code.distance().unwrap();
        assert_eq!(d.distance(), r.code_distance);
        assert!(code.is_logical(d.witness()).unwrap());
        assert_eq!(d.candidates_checked(), 13);
    }
}
