//! Bounded finite-poset assignment census for the declared two-factor model.
//! AuthorityEffect: None.
use crate::qm::campaigns::causal_order::census_unlabeled;
use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::{
    involution::is_hermitian,
    matrix::{commutator, is_scalar_matrix, is_zero_matrix},
};
use omega_homology::finite_poset::FinitePoset;
use omega_homology::graph_coloring::{two_coloring, TwoColoring};
use omega_lie_theory::pauli_symplectic::{pauli, Pauli};
use omega_number_theory::cyclotomic::GaussianRat;
use omega_quantum_physics::commuting_obs::*;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeSet, HashMap};

/// Construct C1 witness assignment:
/// Event 0: sigma_x (x) I (factor 1)
/// Event 1: sigma_z (x) I (factor 1)
/// Event 2: I (x) sigma_z (factor 2)
pub fn construct_c1_assignment() -> Result<
    (
        HashMap<usize, BasicMatrix<GaussianRat>>,
        HashMap<usize, usize>,
    ),
    String,
> {
    let mut obs = HashMap::new();
    obs.insert(
        0,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );
    obs.insert(
        1,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );
    obs.insert(
        2,
        embed_factor_2(
            &pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );

    let mut factors = HashMap::new();
    factors.insert(0, 1);
    factors.insert(1, 1);
    factors.insert(2, 2);

    Ok((obs, factors))
}

/// Construct C2 witness assignment:
/// Event 0: sigma_x (x) I (factor 1)
/// Event 1: sigma_z (x) I (factor 1)
/// Event 2: I (x) sigma_z (factor 2)
/// Event 3: I (x) sigma_x (factor 2)
pub fn construct_c2_assignment() -> Result<
    (
        HashMap<usize, BasicMatrix<GaussianRat>>,
        HashMap<usize, usize>,
    ),
    String,
> {
    let mut obs = HashMap::new();
    obs.insert(
        0,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );
    obs.insert(
        1,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );
    obs.insert(
        2,
        embed_factor_2(
            &pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );
    obs.insert(
        3,
        embed_factor_2(
            &pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );

    let mut factors = HashMap::new();
    factors.insert(0, 1);
    factors.insert(1, 1);
    factors.insert(2, 2);
    factors.insert(3, 2);

    Ok((obs, factors))
}

/// Construct 3-element antichain (0 relations).
pub fn construct_c3_antichain() -> FinitePoset {
    FinitePoset::new(3, BTreeSet::new()).unwrap()
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PosetSearchResult {
    pub poset_n: usize,
    pub strict_relations_count: usize,
    pub spacelike_pairs_count: usize,
    pub has_odd_cycle: bool,
    pub odd_cycle_witness: Option<Vec<usize>>,
    pub admitted: bool,
    pub status: String,
    pub degenerate_assignments_rejected: usize,
}

/// Search for a commuting assignment on a single poset.
pub fn search_poset_assignment(
    poset: &FinitePoset,
    non_degeneracy_enforced: bool,
) -> Result<PosetSearchResult, String> {
    let edges = poset.incomparable_pairs();
    if poset.size() > 20 {
        return Err("DECLARED_SEARCH_BOUND_EXCEEDED".into());
    }
    let (has_odd, odd_cycle, coloring) =
        match two_coloring(poset.size(), &edges).map_err(|e| e.to_string())? {
            TwoColoring::OddCycle(cycle) => (true, Some(cycle), Vec::new()),
            TwoColoring::Bipartite { colors, .. } => (false, None, colors),
        };

    let mut degenerate_rejected = 0;

    if has_odd {
        // Every two-factor labelling violates an odd-cycle edge. Count only
        // when the bounded integer count is representable; refuse larger census inputs.
        let total_combos = 1usize << poset.size();
        for mask in 0..total_combos {
            let mut f_map = HashMap::new();
            for i in 0..poset.size() {
                f_map.insert(i, if (mask & (1 << i)) != 0 { 2 } else { 1 });
            }
            for &(u, v) in &edges {
                if f_map.get(&u) == f_map.get(&v) {
                    degenerate_rejected += 1;
                    break;
                }
            }
        }

        return Ok(PosetSearchResult {
            poset_n: poset.size(),
            strict_relations_count: poset.relation_count(),
            spacelike_pairs_count: edges.len(),
            has_odd_cycle: true,
            odd_cycle_witness: odd_cycle,
            admitted: false,
            status: "OBSTRUCTED_BY_ODD_CYCLE".to_string(),
            degenerate_assignments_rejected: degenerate_rejected,
        });
    }

    // Bipartite: construct assignment
    let f1_ops = [
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::Y).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    ];
    let f2_ops = [
        embed_factor_2(
            &pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
        embed_factor_2(
            &pauli::<GaussianRat>(Pauli::Y).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
        embed_factor_2(
            &pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    ];

    let mut assignment = HashMap::new();
    let mut factor_labels = HashMap::new();
    for i in 0..poset.size() {
        let c = usize::from(coloring[i]) + 1;
        factor_labels.insert(i, c);
        if c == 1 {
            assignment.insert(i, f1_ops[i % f1_ops.len()].clone());
        } else {
            assignment.insert(i, f2_ops[i % f2_ops.len()].clone());
        }
    }

    let (valid, reason, deg_rej) =
        validate_observable_assignment(poset, &assignment, &factor_labels, non_degeneracy_enforced);

    Ok(PosetSearchResult {
        poset_n: poset.size(),
        strict_relations_count: poset.relation_count(),
        spacelike_pairs_count: edges.len(),
        has_odd_cycle: false,
        odd_cycle_witness: None,
        admitted: valid,
        status: if valid {
            "COMMUTING_ASSIGNMENT_FOUND".into()
        } else {
            reason
        },
        degenerate_assignments_rejected: deg_rej,
    })
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CensusSearchResult {
    pub posets_searched: usize,
    pub n3_census_count: usize,
    pub n3_obstructed_count: usize,
    pub n3_admitted_count: usize,
    pub n4_census_count: usize,
    pub n4_obstructed_count: usize,
    pub n4_admitted_count: usize,
    pub total_obstructed_count: usize,
    pub total_admitted_count: usize,
    pub smallest_obstructed_poset_size: Option<usize>,
    pub obstructed_poset_found: bool,
    pub odd_cycle_analysed: bool,
    pub non_degeneracy_enforced: bool,
    pub degenerate_assignments_rejected: usize,
}

/// Exhaustive search over census of posets on 3 and 4 elements.
pub fn search_census_at_declared_bound(
    non_degeneracy_enforced: bool,
) -> Result<CensusSearchResult, String> {
    let c3 = census_unlabeled(3).expect("three-event census is bounded");
    let c4 = census_unlabeled(4).expect("four-event census is bounded");

    let mut total_degenerate_rejected = 0;
    let mut smallest_obstructed_size = None;
    let mut obstructed_poset_found = false;

    let mut n3_obstructed = 0;
    for posets in c3.values() {
        let p = &posets[0];
        let res = search_poset_assignment(p, non_degeneracy_enforced)?;
        total_degenerate_rejected += res.degenerate_assignments_rejected;
        if !res.admitted {
            n3_obstructed += 1;
            if !obstructed_poset_found {
                obstructed_poset_found = true;
                smallest_obstructed_size = Some(3);
            }
        }
    }

    let mut n4_obstructed = 0;
    for posets in c4.values() {
        let p = &posets[0];
        let res = search_poset_assignment(p, non_degeneracy_enforced)?;
        total_degenerate_rejected += res.degenerate_assignments_rejected;
        if !res.admitted {
            n4_obstructed += 1;
            if !obstructed_poset_found {
                obstructed_poset_found = true;
                smallest_obstructed_size = Some(4);
            }
        }
    }

    Ok(CensusSearchResult {
        posets_searched: c3.len() + c4.len(),
        n3_census_count: c3.len(),
        n3_obstructed_count: n3_obstructed,
        n3_admitted_count: c3.len() - n3_obstructed,
        n4_census_count: c4.len(),
        n4_obstructed_count: n4_obstructed,
        n4_admitted_count: c4.len() - n4_obstructed,
        total_obstructed_count: n3_obstructed + n4_obstructed,
        total_admitted_count: (c3.len() - n3_obstructed) + (c4.len() - n4_obstructed),
        smallest_obstructed_poset_size: smallest_obstructed_size,
        obstructed_poset_found,
        odd_cycle_analysed: true,
        non_degeneracy_enforced,
        degenerate_assignments_rejected: total_degenerate_rejected,
    })
}

/// Independent checker for C1 and C2 witness assignments.
pub fn verify_witness_independent(
    n: usize,
    strict_relations: &[(usize, usize)],
    observables: &HashMap<usize, BasicMatrix<GaussianRat>>,
    factor_labels: &HashMap<usize, usize>,
    non_degeneracy_enforced: bool,
) -> Result<bool, String> {
    if n == 0 || n > 20 {
        return Err("DECLARED_SEARCH_BOUND_EXCEEDED".into());
    }
    if (0..n).any(|i| !matches!(factor_labels.get(&i), Some(1 | 2))) {
        return Err("observable factor is outside the declared two-factor class".into());
    }
    let strict_set: BTreeSet<(usize, usize)> = strict_relations.iter().cloned().collect();
    FinitePoset::new(n, strict_set.clone()).map_err(|e| format!("invalid declared poset: {e}"))?;
    let mut spacelike = Vec::new();
    for i in 0..n {
        for j in (i + 1)..n {
            if !strict_set.contains(&(i, j)) && !strict_set.contains(&(j, i)) {
                spacelike.push((i, j));
            }
        }
    }

    // 1. Hermiticity
    for u in 0..n {
        let m = observables
            .get(&u)
            .ok_or_else(|| format!("Missing observable {}", u))?;
        if !is_hermitian(m).map_err(|e| e.to_string())? {
            return Err(format!("Observable {} is not Hermitian", u));
        }
    }

    // 2. Non-scalar
    if non_degeneracy_enforced {
        for u in 0..n {
            let m = observables.get(&u).unwrap();
            if is_scalar_matrix(m).map_err(|e| e.to_string())? {
                return Err(format!("Observable {} is scalar", u));
            }
        }
    }

    // 3. Commutation on spacelike pairs
    for &(u, v) in &spacelike {
        let m_u = observables.get(&u).unwrap();
        let m_v = observables.get(&v).unwrap();
        let comm = commutator(m_u, m_v).map_err(|e| e.to_string())?;
        if !is_zero_matrix(&comm) {
            return Err(format!("Spacelike pair ({}, {}) does not commute", u, v));
        }
        if non_degeneracy_enforced {
            let fu = factor_labels.get(&u).unwrap_or(&1);
            let fv = factor_labels.get(&v).unwrap_or(&2);
            if fu == fv {
                return Err(format!(
                    "Incomparable pair ({}, {}) shares factor and MASA",
                    u, v
                ));
            }
        }
    }

    Ok(true)
}
