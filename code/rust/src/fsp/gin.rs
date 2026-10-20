//! Generalized Inverted Index (GIN) Engine for Fermion Modes, Involution Doublet Cancellation,
//! and Kitaev Chain Majorana Zero Mode Decoupling.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct FermionConfiguration {
    pub cfg_id: u64,
    pub model_name: String,
    pub occupied_modes: BTreeSet<usize>,
    pub total_modes: usize,
    pub weight: BigRational,
    pub jw_sign: i64,
    pub parity_sector: i64,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct InvolutionCancellationReceipt {
    pub model_name: String,
    pub pairs_audited: usize,
    pub all_exact_cancellations: bool,
    pub max_weight_defect: BigRational,
    pub total_uncancelled_mass: BigRational,
    pub terminal_route: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MajoranaZeroModeReceipt {
    pub chain_length_l: usize,
    pub total_modes_audited: usize,
    pub unpaired_zero_modes: Vec<usize>,
    pub bulk_bonded_modes: Vec<usize>,
    pub is_boundary_isolated: bool,
    pub mzm_status: String,
}

/// Inverted posting list index mapping fermion orbital modes to many-body configuration IDs.
#[derive(Clone, Debug, Default)]
pub struct GinIndex {
    pub configurations: BTreeMap<u64, FermionConfiguration>,
    /// Posting lists: mode_id -> set of cfg_ids where mode is occupied
    pub posting_lists: BTreeMap<usize, BTreeSet<u64>>,
}

impl GinIndex {
    pub fn new() -> Self {
        Self::default()
    }

    /// Index a configuration and populate mode posting lists.
    pub fn index_configuration(
        &mut self,
        cfg_id: u64,
        model_name: impl Into<String>,
        occupied_modes: BTreeSet<usize>,
        total_modes: usize,
        weight: BigRational,
        jw_sign: i64,
        parity_sector: i64,
    ) {
        for &m in &occupied_modes {
            self.posting_lists.entry(m).or_default().insert(cfg_id);
        }
        self.configurations.insert(
            cfg_id,
            FermionConfiguration {
                cfg_id,
                model_name: model_name.into(),
                occupied_modes,
                total_modes,
                weight,
                jw_sign,
                parity_sector,
            },
        );
    }

    /// Fast inverted posting list query: intersection of required modes minus forbidden modes.
    pub fn query_by_modes(
        &self,
        required_modes: &BTreeSet<usize>,
        forbidden_modes: &BTreeSet<usize>,
    ) -> BTreeSet<u64> {
        let mut candidates: BTreeSet<u64> = if required_modes.is_empty() {
            self.configurations.keys().copied().collect()
        } else {
            let mut iter = required_modes.iter();
            let Some(first_mode) = iter.next() else {
                return BTreeSet::new();
            };
            let mut set = self
                .posting_lists
                .get(first_mode)
                .cloned()
                .unwrap_or_default();
            for m in iter {
                if let Some(posting) = self.posting_lists.get(m) {
                    set.retain(|id| posting.contains(id));
                } else {
                    return BTreeSet::new();
                }
            }
            set
        };

        for m in forbidden_modes {
            if let Some(posting) = self.posting_lists.get(m) {
                candidates.retain(|id| !posting.contains(id));
            }
        }
        candidates
    }

    /// Find unique involution partner differing exactly on flip_modes.
    pub fn find_involution_partner(
        &self,
        cfg_id: u64,
        flip_modes: &BTreeSet<usize>,
        total_modes: usize,
    ) -> Option<u64> {
        let current = self.configurations.get(&cfg_id)?;

        let mut required = BTreeSet::new();
        let mut forbidden = BTreeSet::new();

        for m in 1..=total_modes {
            let cur_occ = current.occupied_modes.contains(&m);
            let flipped = flip_modes.contains(&m);
            let target_occ = cur_occ ^ flipped;
            if target_occ {
                required.insert(m);
            } else {
                forbidden.insert(m);
            }
        }

        let mut candidates = self.query_by_modes(&required, &forbidden);
        candidates.remove(&cfg_id);
        candidates.into_iter().next()
    }

    /// Audit a collection of involution pairs for exact opposite-sign and identical-weight cancellation.
    pub fn audit_involution_cancellations(
        &self,
        model_name: &str,
        pairs: &[(u64, u64)],
    ) -> InvolutionCancellationReceipt {
        let mut max_defect = BigRational::zero();
        let mut total_uncancelled = BigRational::zero();
        let mut all_exact = !pairs.is_empty();

        for &(id_a, id_b) in pairs {
            let (cfg_a, cfg_b) = match (self.configurations.get(&id_a), self.configurations.get(&id_b)) {
                (Some(a), Some(b)) => (a, b),
                _ => {
                    all_exact = false;
                    continue;
                }
            };

            let opposite_sign = cfg_a.jw_sign == -cfg_b.jw_sign;
            let weight_diff = (&cfg_a.weight - &cfg_b.weight).abs();

            if weight_diff > max_defect {
                max_defect = weight_diff.clone();
            }

            if !opposite_sign || !weight_diff.is_zero() {
                all_exact = false;
                total_uncancelled = total_uncancelled + weight_diff;
            }
        }

        let terminal_route = if all_exact {
            "ExactRepair".to_string()
        } else {
            "OpenSignObstruction".to_string()
        };

        InvolutionCancellationReceipt {
            model_name: model_name.to_string(),
            pairs_audited: pairs.len(),
            all_exact_cancellations: all_exact,
            max_weight_defect: max_defect,
            total_uncancelled_mass: total_uncancelled,
            terminal_route,
        }
    }
}

/// Audit 1D Kitaev chain Majorana zero modes at sweet-spot chemical potential.
/// Chain length L has 2L Majorana operators \gamma_1, ..., \gamma_{2L}.
/// Bulk sweet-spot bonds are (\gamma_{2j}, \gamma_{2j+1}) for j = 1, ..., L-1.
/// Unpaired boundary modes are \gamma_1 and \gamma_{2L}.
pub fn audit_kitaev_chain_majorana(l: usize) -> Result<MajoranaZeroModeReceipt, &'static str> {
    if l < 2 {
        return Err("Kitaev chain requires at least 2 lattice sites (L >= 2)");
    }
    let Some(total_modes) = l.checked_mul(2) else {
        return Err("chain_length_l overflow");
    };
    let mut bulk_bonds = Vec::new();
    let mut bulk_modes_set = BTreeSet::new();

    for j in 1..l {
        let u = 2 * j;
        let v = 2 * j + 1;
        bulk_bonds.push((u, v));
        bulk_modes_set.insert(u);
        bulk_modes_set.insert(v);
    }

    let edge_modes = vec![1, total_modes];
    let mut is_boundary_isolated = true;

    for &edge in &edge_modes {
        if bulk_modes_set.contains(&edge) {
            is_boundary_isolated = false;
        }
    }

    let bulk_bonded_modes: Vec<usize> = bulk_modes_set.into_iter().collect();
    let mzm_status = if is_boundary_isolated && bulk_bonded_modes.len() == total_modes - 2 {
        "MZM_TOPOLOGICALLY_PROTECTED".to_string()
    } else {
        "MZM_BULK_POLLUTION".to_string()
    };

    Ok(MajoranaZeroModeReceipt {
        chain_length_l: l,
        total_modes_audited: total_modes,
        unpaired_zero_modes: edge_modes,
        bulk_bonded_modes,
        is_boundary_isolated,
        mzm_status,
    })
}

/// Finite lattice scaling benchmark for 1D Kitaev chain Majorana zero mode isolation
/// across arbitrary declared chain lengths `L` (`2L` Majorana modes).
pub fn benchmark_kitaev_chain_mzm_scaling(
    chain_lengths: &[usize],
) -> Result<Vec<MajoranaZeroModeReceipt>, &'static str> {
    if chain_lengths.is_empty() {
        return Err("chain_lengths must not be empty");
    }
    let mut receipts = Vec::with_capacity(chain_lengths.len());
    for &l in chain_lengths {
        receipts.push(audit_kitaev_chain_majorana(l)?);
    }
    Ok(receipts)
}

/// Finite lattice scaling benchmark for GIN inverted posting list lookup and involution
/// doublet cancellation across declared orbital mode counts `M`.
pub fn benchmark_gin_involution_scaling(
    mode_counts: &[usize],
) -> Result<Vec<InvolutionCancellationReceipt>, &'static str> {
    if mode_counts.is_empty() {
        return Err("mode_counts must not be empty");
    }
    let mut receipts = Vec::with_capacity(mode_counts.len());
    for &m in mode_counts {
        if m < 4 || m % 2 != 0 {
            return Err("each mode count must be an even integer >= 4");
        }
        let mut gin = GinIndex::new();
        let num_pairs = m / 2;
        let mut flip_modes = BTreeSet::new();
        flip_modes.insert(1);
        flip_modes.insert(m);

        let mut pairs = Vec::with_capacity(num_pairs);
        for p in 0..num_pairs {
            let id_a = (2 * p + 1) as u64;
            let id_b = (2 * p + 2) as u64;
            let mut occ_a = BTreeSet::new();
            occ_a.insert(1);
            if p + 2 < m {
                occ_a.insert(p + 2);
            }
            let mut occ_b = occ_a.clone();
            occ_b.remove(&1);
            occ_b.insert(m);

            let weight = BigRational::from(num_bigint::BigInt::from((p + 1) as i64));
            gin.index_configuration(id_a, format!("GIN_Scale_{m}"), occ_a, m, weight.clone(), 1, 1);
            gin.index_configuration(id_b, format!("GIN_Scale_{m}"), occ_b, m, weight, -1, 1);

            let partner = gin
                .find_involution_partner(id_a, &flip_modes, m)
                .ok_or("missing involution partner in GIN scaling benchmark")?;
            if partner != id_b {
                return Err("GIN partner mismatch in scaling benchmark");
            }
            pairs.push((id_a, id_b));
        }

        receipts.push(gin.audit_involution_cancellations(&format!("GIN_Scale_{m}"), &pairs));
    }
    Ok(receipts)
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigInt;

    #[test]
    fn gin_index_lookup_and_involution_partner_test() {
        let mut gin = GinIndex::new();
        // 4 sites, 2 particles
        let mut occ1 = BTreeSet::new();
        occ1.insert(1);
        occ1.insert(2);
        gin.index_configuration(1, "Bipartite", occ1, 4, BigRational::from(BigInt::from(5)), 1, 1);

        let mut occ2 = BTreeSet::new();
        occ2.insert(2);
        occ2.insert(3);
        gin.index_configuration(2, "Bipartite", occ2, 4, BigRational::from(BigInt::from(5)), -1, 1);

        // Query mode 2
        let mut req = BTreeSet::new();
        req.insert(2);
        let res = gin.query_by_modes(&req, &BTreeSet::new());
        assert_eq!(res.len(), 2);
        assert!(res.contains(&1) && res.contains(&2));

        // Audit involution pair (1, 2)
        let receipt = gin.audit_involution_cancellations("Bipartite", &[(1, 2)]);
        assert!(receipt.all_exact_cancellations);
        assert_eq!(receipt.terminal_route, "ExactRepair");
    }

    #[test]
    fn kitaev_chain_majorana_zero_mode_isolation_test() {
        let receipt = audit_kitaev_chain_majorana(4).unwrap();
        assert_eq!(receipt.total_modes_audited, 8);
        assert_eq!(receipt.unpaired_zero_modes, vec![1, 8]);
        assert_eq!(receipt.bulk_bonded_modes, vec![2, 3, 4, 5, 6, 7]);
        assert!(receipt.is_boundary_isolated);
        assert_eq!(receipt.mzm_status, "MZM_TOPOLOGICALLY_PROTECTED");
    }

    #[test]
    fn kitaev_chain_and_gin_involution_scaling_up_to_1024_modes() {
        let lengths = [4usize, 8, 16, 32, 64, 128, 256, 512];
        let mzm_receipts = benchmark_kitaev_chain_mzm_scaling(&lengths).unwrap();
        assert_eq!(mzm_receipts.len(), lengths.len());
        for (&l, r) in lengths.iter().zip(mzm_receipts.iter()) {
            assert_eq!(r.chain_length_l, l);
            assert_eq!(r.total_modes_audited, 2 * l);
            assert_eq!(r.unpaired_zero_modes, vec![1, 2 * l]);
            assert_eq!(r.bulk_bonded_modes.len(), 2 * l - 2);
            assert!(r.is_boundary_isolated);
            assert_eq!(r.mzm_status, "MZM_TOPOLOGICALLY_PROTECTED");
        }

        let mode_counts = [8usize, 16, 32, 64, 128];
        let gin_receipts = benchmark_gin_involution_scaling(&mode_counts).unwrap();
        assert_eq!(gin_receipts.len(), mode_counts.len());
        for (&m, r) in mode_counts.iter().zip(gin_receipts.iter()) {
            assert_eq!(r.pairs_audited, m / 2);
            assert!(r.all_exact_cancellations);
            assert_eq!(r.max_weight_defect, BigRational::zero());
            assert_eq!(r.total_uncancelled_mass, BigRational::zero());
            assert_eq!(r.terminal_route, "ExactRepair");
        }
    }
}
