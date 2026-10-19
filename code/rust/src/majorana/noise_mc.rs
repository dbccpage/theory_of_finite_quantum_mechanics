
use crate::complexes::surface_grid;
use crate::gf2_terminalizer::{GF2ScheduleStatus, Gf2CocycleClassifier};
use serde::{Deserialize, Serialize};

pub const NOISE_MC_RECEIPT_TAG: &str = "omega.majorana-noise-mc-receipt.v1";

#[derive(Debug, Clone)]
pub struct Lcg {
    state: u64,
}

impl Lcg {
    pub fn new(seed: u64) -> Self {
        Self {
            state: seed | 1,
        }
    }

    pub fn next_u64(&mut self) -> u64 {
        self.state = self.state.wrapping_mul(1664525).wrapping_add(1013904223);
        self.state
    }

    pub fn bernoulli(&mut self, p: f64) -> bool {
        if p <= 0.0 {
            return false;
        }
        if p >= 1.0 {
            return true;
        }
        let thr = (p * (u32::MAX as f64)) as u32;
        (self.next_u64() as u32) < thr
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct NoiseMcReceipt {
    pub certificate_tag: String,
    pub grid_m: usize,
    pub num_edges: usize,
    pub num_faces: usize,
    pub p: f64,
    pub trials: usize,
    pub seed: u64,
    pub count_exact: usize,
    pub count_closed_residual: usize,
    pub count_open: usize,
    pub frac_exact: f64,
    pub frac_closed_residual: f64,
    pub frac_open: f64,
    pub mean_error_weight: f64,
    pub authority_effect: String,
    pub notes: String,
}

pub fn noise_mc_planar_grid(
    m: usize,
    p: f64,
    trials: usize,
    seed: u64,
) -> Result<NoiseMcReceipt, String> {
    if m == 0 {
        return Err("m >= 1".into());
    }
    if trials == 0 {
        return Err("trials >= 1".into());
    }
    let complex = surface_grid(m, m, false);
    let mut rng = Lcg::new(seed);
    let mut count_exact = 0usize;
    let mut count_closed = 0usize;
    let mut count_open = 0usize;
    let mut weight_sum = 0usize;

    for _ in 0..trials {
        let mut omega = vec![0u8; complex.num_edges];
        let mut w = 0usize;
        for e in 0..complex.num_edges {
            if rng.bernoulli(p) {
                omega[e] = 1;
                w += 1;
            }
        }
        weight_sum += w;
        let cert = Gf2CocycleClassifier::classify(&complex.d0, &complex.d1, &omega)?;
        match cert.status {
            GF2ScheduleStatus::Exact => count_exact += 1,
            GF2ScheduleStatus::ClosedResidual => count_closed += 1,
            GF2ScheduleStatus::OpenObstruction => count_open += 1,
        }
    }

    let t = trials as f64;
    Ok(NoiseMcReceipt {
        certificate_tag: NOISE_MC_RECEIPT_TAG.into(),
        grid_m: m,
        num_edges: complex.num_edges,
        num_faces: complex.num_faces,
        p,
        trials,
        seed,
        count_exact,
        count_closed_residual: count_closed,
        count_open,
        frac_exact: count_exact as f64 / t,
        frac_closed_residual: count_closed as f64 / t,
        frac_open: count_open as f64 / t,
        mean_error_weight: weight_sum as f64 / t,
        authority_effect: "None".into(),
        notes: format!(
            "IID Bernoulli(p) edge flips on planar {m}x{m} plaquette grid; \
             classes via face-syndrome classifier. Not a physical threshold. Auth=None."
        ),
    })
}

pub fn noise_mc_size_sweep(
    max_m: usize,
    p: f64,
    trials: usize,
    seed: u64,
) -> Result<Vec<NoiseMcReceipt>, String> {
    let mut out = Vec::new();
    for m in 1..=max_m {
        out.push(noise_mc_planar_grid(
            m,
            p,
            trials,
            seed.wrapping_add(m as u64),
        )?);
    }
    Ok(out)
}

pub fn noise_mc_torus_grid(
    m: usize,
    p: f64,
    trials: usize,
    seed: u64,
) -> Result<NoiseMcReceipt, String> {
    if m < 2 {
        return Err("torus grid requires m >= 2".into());
    }
    if trials == 0 {
        return Err("trials >= 1".into());
    }
    let complex = surface_grid(m, m, true);
    let mut rng = Lcg::new(seed);
    let mut count_exact = 0usize;
    let mut count_closed = 0usize;
    let mut count_open = 0usize;
    let mut weight_sum = 0usize;

    for _ in 0..trials {
        let mut omega = vec![0u8; complex.num_edges];
        let mut w = 0usize;
        for e in 0..complex.num_edges {
            if rng.bernoulli(p) {
                omega[e] = 1;
                w += 1;
            }
        }
        weight_sum += w;
        let cert = Gf2CocycleClassifier::classify(&complex.d0, &complex.d1, &omega)?;
        match cert.status {
            GF2ScheduleStatus::Exact => count_exact += 1,
            GF2ScheduleStatus::ClosedResidual => count_closed += 1,
            GF2ScheduleStatus::OpenObstruction => count_open += 1,
        }
    }

    let t = trials as f64;
    Ok(NoiseMcReceipt {
        certificate_tag: NOISE_MC_RECEIPT_TAG.into(),
        grid_m: m,
        num_edges: complex.num_edges,
        num_faces: complex.num_faces,
        p,
        trials,
        seed,
        count_exact,
        count_closed_residual: count_closed,
        count_open,
        frac_exact: count_exact as f64 / t,
        frac_closed_residual: count_closed as f64 / t,
        frac_open: count_open as f64 / t,
        mean_error_weight: weight_sum as f64 / t,
        authority_effect: "None".into(),
        notes: format!(
            "IID Bernoulli(p) edge flips on periodic torus {m}x{m} plaquette grid; \
             classes via face-syndrome classifier. Not a physical threshold. Auth=None."
        ),
    })
}

pub fn noise_mc_torus_size_sweep(
    max_m: usize,
    p: f64,
    trials: usize,
    seed: u64,
) -> Result<Vec<NoiseMcReceipt>, String> {
    if max_m < 2 {
        return Err("torus size sweep requires max_m >= 2".into());
    }
    let mut out = Vec::new();
    for m in 2..=max_m {
        out.push(noise_mc_torus_grid(
            m,
            p,
            trials,
            seed.wrapping_add(m as u64),
        )?);
    }
    Ok(out)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p_zero_all_exact() {
        let r = noise_mc_planar_grid(2, 0.0, 50, 7).unwrap();
        assert_eq!(r.num_edges, 12);
        assert_eq!(r.num_faces, 4);
        assert_eq!(r.count_exact, 50);
        assert_eq!(r.count_open, 0);
        assert_eq!(r.count_closed_residual, 0);
        assert_eq!(r.mean_error_weight, 0.0);
        assert_eq!(r.frac_exact, 1.0);
    }

    #[test]
    fn p_one_mostly_open_on_planar() {
        let r = noise_mc_planar_grid(2, 0.5, 200, 42).unwrap();
        assert_eq!(r.trials, 200);
        assert!(r.count_open + r.count_exact + r.count_closed_residual == 200);
        assert!(r.frac_open > 0.1, "expected open mass, got {}", r.frac_open);
        assert_eq!(r.authority_effect, "None");
    }

    #[test]
    fn open_fraction_rises_with_p() {
        let low = noise_mc_planar_grid(2, 0.05, 300, 1).unwrap();
        let high = noise_mc_planar_grid(2, 0.4, 300, 1).unwrap();
        assert!(
            high.frac_open > low.frac_open,
            "low open {} high open {}",
            low.frac_open,
            high.frac_open
        );
    }

    #[test]
    fn size_sweep_grows_the_planar_grids() {
        assert!(noise_mc_planar_grid(0, 0.0, 1, 1).unwrap_err().contains("m"));
        assert!(noise_mc_planar_grid(1, 0.0, 0, 1)
            .unwrap_err()
            .contains("trials"));
        let rows = noise_mc_size_sweep(3, 0.0, 4, 99).unwrap();
        assert_eq!(rows.len(), 3);
        let edges = [4usize, 12, 24];
        let faces = [1usize, 4, 9];
        for (i, r) in rows.iter().enumerate() {
            let m = i + 1;
            assert_eq!(r.grid_m, m);
            assert_eq!(r.num_edges, edges[i], "m={m}");
            assert_eq!(r.num_faces, faces[i], "m={m}");
            assert_eq!(r.seed, 99 + m as u64);
            assert_eq!(r.trials, 4);
            assert_eq!(r.p, 0.0);
            assert_eq!(r.count_exact, 4);
            assert_eq!(r.count_open, 0);
            assert_eq!(r.count_closed_residual, 0);
            assert_eq!(r.mean_error_weight, 0.0);
        }
    }

    #[test]
    fn p_one_flips_every_edge_and_stays_exact_on_the_disk() {
        let r = noise_mc_planar_grid(2, 1.0, 5, 7).unwrap();
        assert_eq!(r.num_edges, 12);
        assert_eq!(r.mean_error_weight, 12.0);
        assert_eq!(r.count_exact, 5);
        assert_eq!(r.count_open, 0);
        assert_eq!(r.count_closed_residual, 0);
    }

    #[test]
    fn planar_and_torus_size_sweeps_up_to_8x8() {
        let planar_rows = noise_mc_size_sweep(8, 0.15, 16, 1000).unwrap();
        assert_eq!(planar_rows.len(), 8);
        for (idx, r) in planar_rows.iter().enumerate() {
            let m = idx + 1;
            assert_eq!(r.grid_m, m);
            assert_eq!(r.num_faces, m * m);
            assert_eq!(r.num_edges, 2 * m * (m + 1));
            assert_eq!(r.count_exact + r.count_closed_residual + r.count_open, 16);
        }

        let torus_rows = noise_mc_torus_size_sweep(8, 0.15, 16, 2000).unwrap();
        assert_eq!(torus_rows.len(), 7); // m = 2..=8
        for (idx, r) in torus_rows.iter().enumerate() {
            let m = idx + 2;
            assert_eq!(r.grid_m, m);
            assert_eq!(r.num_faces, m * m);
            assert_eq!(r.num_edges, 2 * m * m);
            assert_eq!(r.count_exact + r.count_closed_residual + r.count_open, 16);
        }
    }
}
