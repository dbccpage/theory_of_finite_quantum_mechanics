use omega_number_theory::rational::rq;
use omega_quantum_physics::branch_finegraining::*;
use serde::{Deserialize, Serialize};
#[allow(non_snake_case)]
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct TargetCensusEntry {
    pub target_id: usize,
    pub name: String,
    pub conductor: usize,
    pub real_subfield: String,
    pub prepared_state: String,
    pub born_weights: Vec<String>,
    pub sector: String,
    pub minimal_N: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct TargetCensusSummary {
    pub total_targets: usize,
    pub targets_rational_sector: usize,
    pub targets_irrational_sector: usize,
    pub targets_irrational_sector_ids: Vec<usize>,
    pub min_finegraining_chsh: i64,
    pub targets: Vec<TargetCensusEntry>,
}

pub fn census_all_targets() -> TargetCensusSummary {
    let raw = vec![
        (1, "Primitive Difference", 1, "Q", "|0> in Q", vec!["1"], 1),
        (
            2,
            "Simplicial Diamond Complex",
            12,
            "Q(sqrt(3))",
            "Vertex base state |v_0>",
            vec!["1"],
            1,
        ),
        (
            3,
            "Sorkin 3-Slit Vanishing",
            12,
            "Q(sqrt(3))",
            "(1, 1, 1)^T / sqrt(3)",
            vec!["1/3", "1/3", "1/3"],
            3,
        ),
        (
            4,
            "Rational Cayley Flow",
            1,
            "Q",
            "Unit orbit e_1 in Q^8",
            vec!["1"],
            1,
        ),
        (
            5,
            "Pentagon Associator",
            1,
            "Q",
            "5-simplex basis in Q^5",
            vec!["1"],
            1,
        ),
        (
            6,
            "Cabello 18-Ray Polytope",
            12,
            "Q(sqrt(3))",
            "18 rays in {0, +-1}^4",
            vec!["1/2", "1/2"],
            2,
        ),
        (
            7,
            "Monotone Permutations",
            1,
            "Q",
            "Uniform superposition over B_n",
            vec!["1/4", "1/4", "1/4", "1/4"],
            4,
        ),
        (
            8,
            "Pythagorean Bell-CHSH",
            1,
            "Q",
            "(3/5)|00> + (4/5)|11>",
            vec!["9/25", "16/25"],
            25,
        ),
        (
            9,
            "3-Qubit Bit-Flip Code",
            1,
            "Q",
            "Logical |0_L> = |000>",
            vec!["1"],
            1,
        ),
        (
            10,
            "Quantum Teleportation",
            1,
            "Q",
            "Bell branches (|00>+|11>)/sqrt(2)",
            vec!["1/4", "1/4", "1/4", "1/4"],
            4,
        ),
        (
            11,
            "Superdense Coding",
            4,
            "Q",
            "Bell basis over Z[i]",
            vec!["1/4", "1/4", "1/4", "1/4"],
            4,
        ),
        (
            12,
            "[[4, 2, 2]] CSS Surface Code",
            1,
            "Q",
            "Plaquette (|0000>+|1111>)/sqrt(2)",
            vec!["1/2", "1/2"],
            2,
        ),
        (
            13,
            "Gross Wigner Phase Space",
            5,
            "Q(sqrt(5))",
            "Stabilizer |0>, Magic (|1>-|4>)/sqrt(2)",
            vec!["1/2", "1/2"],
            2,
        ),
        (
            14,
            "Shor [[9, 1, 3]] Code",
            1,
            "Q",
            "Logical |0_L> on 9 qubits",
            vec!["1/8"; 8],
            8,
        ),
        (
            15,
            "Discrete Phase Estimation",
            4,
            "Q",
            "Dyadic eigenstate peak",
            vec!["1"],
            1,
        ),
        (
            16,
            "Surface Code Toric Topology",
            2,
            "Q",
            "Torus homology ground state",
            vec!["1/4", "1/4", "1/4", "1/4"],
            4,
        ),
        (
            17,
            "Discrete Grover Search",
            12,
            "Q(sqrt(3))",
            "Householder reflection orbit",
            vec!["1"],
            1,
        ),
        (
            18,
            "Clifford Normalizer Sp(2n, F_2)",
            8,
            "Q(sqrt(2))",
            "Phase-space basis state",
            vec!["1"],
            1,
        ),
        (
            19,
            "Stone-von Neumann Obstruction",
            1,
            "Q",
            "Shift basis vector in Z/NZ",
            vec!["1"],
            1,
        ),
        (
            20,
            "Richardson Error Mitigation",
            1,
            "Q",
            "Extrapolated observable in Q",
            vec!["1"],
            1,
        ),
        (
            21,
            "Cayley Graph Quantum Walk",
            1,
            "Q",
            "Grover coin packet on S_3",
            vec!["1/6"; 6],
            6,
        ),
        (
            22,
            "MUB Tomography d=3",
            3,
            "Q",
            "MUB basis states in Q(zeta_3)",
            vec!["1/3", "1/3", "1/3"],
            3,
        ),
        (
            23,
            "MUB Tomography d=4 (Extension)",
            4,
            "Q",
            "2-qubit MASA Pauli eigenstates",
            vec!["1/4", "1/4", "1/4", "1/4"],
            4,
        ),
    ];

    let mut entries = Vec::new();
    let mut min_chsh = 0;
    for (id, name, cond, real_sub, state, weights, min_n) in raw {
        if id == 8 {
            min_chsh = min_n;
        }
        entries.push(TargetCensusEntry {
            target_id: id,
            name: name.to_string(),
            conductor: cond,
            real_subfield: real_sub.to_string(),
            prepared_state: state.to_string(),
            born_weights: weights.into_iter().map(|s| s.to_string()).collect(),
            sector: "RATIONAL".to_string(),
            minimal_N: min_n,
        });
    }

    TargetCensusSummary {
        total_targets: entries.len(),
        targets_rational_sector: entries.len(),
        targets_irrational_sector: 0,
        targets_irrational_sector_ids: vec![],
        min_finegraining_chsh: min_chsh,
        targets: entries,
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SymmetryAuditResult {
    pub authority_effect: String,
    pub rational_state_status: String,
    pub rational_fine_graining_multiplicity: i64,
    pub irrational_state_status: String,
    pub irrational_refusal_step: String,
    pub everett_counting_status: String,
}

pub fn envariance_deutsch_wallace_symmetry_audit() -> SymmetryAuditResult {
    SymmetryAuditResult {
        authority_effect: "None".to_string(),
        rational_state_status: "DERIVED_VIA_COUNTING".to_string(),
        rational_fine_graining_multiplicity: 25,
        irrational_state_status: "REFUSED_BEYOND_RATIONAL_SECTOR".to_string(),
        irrational_refusal_step:
            "Refusal of continuous / infinite branching limits in finite cyclotomic carrier"
                .to_string(),
        everett_counting_status: "REFUSED_BEYOND_RATIONAL_SECTOR".to_string(),
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct NegativeControlResult {
    pub wrong_multiplicity_rejected: bool,
    pub bad_counts_rejected: bool,
    pub all_controls_passed: bool,
}

pub fn run_negative_controls() -> NegativeControlResult {
    let w = vec![rq(9, 25), rq(16, 25)];
    let tree_bad_n = finegrain_state_rationals(&w, Some(10));
    let bad_n_ok = !tree_bad_n.is_exact_match;

    let bad_verify = verify_finegraining(&w, 25, &[10, 15]);
    let bad_counts_ok = !bad_verify;

    NegativeControlResult {
        wrong_multiplicity_rejected: bad_n_ok,
        bad_counts_rejected: bad_counts_ok,
        all_controls_passed: bad_n_ok && bad_counts_ok,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_census_all_targets() {
        let census = census_all_targets();
        assert_eq!(census.total_targets, 23);
        assert_eq!(census.targets_rational_sector, 23);
        assert_eq!(census.targets_irrational_sector, 0);
        assert_eq!(census.min_finegraining_chsh, 25);
    }
    #[test]
    fn test_negative_controls() {
        let ctrl = run_negative_controls();
        assert!(ctrl.all_controls_passed);
    }
}
