use crate::linear_algebra::{basic_matrix::BasicMatrix, matrix as mx};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::{r_zero, rq};
use omega_quantum_physics::mub::algebra::ProjectorAlgebraStatus;
use omega_quantum_physics::mub::MubSystem;
use serde::{Deserialize, Serialize};
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct CliftonKentDeficitReceipt {
    pub total_valuations: usize,
    pub non_psd_valuations: usize,
    pub non_psd_percentage: f64,
    pub purity_all_four: bool,
    pub trace_all_one: bool,
    pub sylvester_negative_minors_verified: bool,
    pub contextuality_persists_unconditionally: bool,
}

fn decode_base4_valuation(mut index: usize) -> [usize; 5] {
    let mut coords = [0usize; 5];
    for slot in &mut coords {
        *slot = index & 3;
        index >>= 2;
    }
    coords
}

fn build_valuation_pseudo_density(
    system: &MubSystem<Cyc24>,
    eye4: &BasicMatrix<Cyc24>,
    coords: &[usize; 5],
) -> Result<BasicMatrix<Cyc24>, String> {
    let mut sum = mx::zeros::<Cyc24>(4, 4).map_err(|e| e.to_string())?;
    for (basis_idx, &vec_idx) in coords.iter().enumerate() {
        let proj = system
            .try_projector(basis_idx, vec_idx)
            .map_err(|e| e.to_string())?;
        sum = mx::add(&sum, proj).map_err(|e| e.to_string())?;
    }
    mx::sub(&sum, eye4).map_err(|e| e.to_string())
}

fn minor_is_strictly_negative(
    rho: &BasicMatrix<Cyc24>,
    i: usize,
    j: usize,
) -> Result<bool, String> {
    let r_zero_val = r_zero();
    let diag_prod = rho
        .get_ref(i, i)
        .map_err(|e| e.to_string())?
        .mul(rho.get_ref(j, j).map_err(|e| e.to_string())?);
    let off_diag = rho.get_ref(i, j).map_err(|e| e.to_string())?;
    let off_diag_norm = off_diag.mul(&off_diag.conj());
    let minor = diag_prod.sub(&off_diag_norm);
    Ok(minor.as_rational().is_some_and(|r| r < r_zero_val))
}

fn has_negative_principal_2x2_minor(rho: &BasicMatrix<Cyc24>) -> Result<bool, String> {
    const PAIRS: [(usize, usize); 6] = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)];
    for (i, j) in PAIRS {
        if minor_is_strictly_negative(rho, i, j)? {
            return Ok(true);
        }
    }
    Ok(false)
}

fn validate_mub4_carrier(system: &MubSystem<Cyc24>) -> Result<(), String> {
    if system.dimension != 4
        || system.verify_projector_algebra().status != ProjectorAlgebraStatus::AlgebraVerified
        || !system.is_complete()
    {
        return Err("expected a checked complete dimension-four MUB carrier".into());
    }
    Ok(())
}

fn evaluate_single_valuation(
    system: &MubSystem<Cyc24>,
    eye4: &BasicMatrix<Cyc24>,
    valuation_idx: usize,
) -> Result<(bool, bool, bool), String> {
    let coords = decode_base4_valuation(valuation_idx);
    let rho = build_valuation_pseudo_density(system, eye4, &coords)?;
    let trace_one = mx::trace(&rho).map_err(|e| e.to_string())? == Cyc24::one();
    let rho_sq = mx::multiply(&rho, &rho).map_err(|e| e.to_string())?;
    let purity_four = mx::trace(&rho_sq).map_err(|e| e.to_string())? == Cyc24::rat(rq(4, 1));
    let neg_minor = has_negative_principal_2x2_minor(&rho)?;
    Ok((trace_one, purity_four, neg_minor))
}

pub fn evaluate_all_1024_clifton_kent_valuations(
    system: &MubSystem<Cyc24>,
) -> Result<CliftonKentDeficitReceipt, String> {
    validate_mub4_carrier(system)?;
    let eye4 = mx::identity::<Cyc24>(4).map_err(|e| e.to_string())?;

    let mut non_psd_count = 0usize;
    let mut purity_all_four = true;
    let mut trace_all_one = true;
    let mut sylvester_all_negative = true;

    let total = 1024usize;
    for valuation_idx in 0..total {
        let (tr_ok, pur_ok, neg_minor) = evaluate_single_valuation(system, &eye4, valuation_idx)?;
        trace_all_one &= tr_ok;
        purity_all_four &= pur_ok;
        if neg_minor {
            non_psd_count += 1;
        } else {
            sylvester_all_negative = false;
        }
    }

    let pct = (non_psd_count as f64 / total as f64) * 100.0;
    let persists = non_psd_count == total && purity_all_four && trace_all_one;

    Ok(CliftonKentDeficitReceipt {
        total_valuations: total,
        non_psd_valuations: non_psd_count,
        non_psd_percentage: pct,
        purity_all_four,
        trace_all_one,
        sylvester_negative_minors_verified: sylvester_all_negative,
        contextuality_persists_unconditionally: persists,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_all_1024_clifton_kent_valuations_certified() {
        let mub4 = MubSystem::mub_d4();
        let receipt = evaluate_all_1024_clifton_kent_valuations(&mub4).unwrap();
        assert_eq!(receipt.total_valuations, 1024);
        assert_eq!(receipt.non_psd_valuations, 1024);
        assert!(receipt.purity_all_four);
        assert!(receipt.trace_all_one);
        assert!(receipt.sylvester_negative_minors_verified);
        assert!(receipt.contextuality_persists_unconditionally);
    }

    #[test]
    fn test_incomplete_mub_system_refusal() {
        let mut mub4 = MubSystem::mub_d4();
        mub4.dimension = 3;
        assert!(evaluate_all_1024_clifton_kent_valuations(&mub4).is_err());
    }
}
