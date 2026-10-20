
use crate::complexes::{surface_grid_2x2_torus, torus_logical_x_example, ChainComplexGf2};
use crate::gf2_terminalizer::{GF2Matrix, GF2ScheduleStatus, Gf2CocycleClassifier};

const MAX_EXHAUSTIVE_EDGES: usize = 16;

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; finite homology distance bounds unique correction capacity; LGGR on declared torus only; not a no-go for quantum computing.";


pub fn hamming_weight(v: &[u8]) -> usize {
    v.iter().map(|&b| (b & 1) as usize).sum()
}


pub fn apply_d1(d1: &GF2Matrix, omega: &[u8]) -> Result<Vec<u8>, String> {
    if omega.len() != d1.cols {
        return Err(format!("vector len {} != d1.cols {}", omega.len(), d1.cols));
    }
    let mut out = vec![0u8; d1.rows];
    for i in 0..d1.rows {
        let mut sum = 0u8;
        for j in 0..d1.cols {
            sum ^= d1.data[i][j] & (omega[j] & 1);
        }
        out[i] = sum & 1;
    }
    Ok(out)
}

pub fn face_syndrome(d1: &GF2Matrix, omega: &[u8]) -> Result<Vec<u8>, String> {
    apply_d1(d1, omega)
}

pub fn syndrome_is_zero(s: &[u8]) -> bool {
    s.iter().all(|&v| v == 0)
}

pub fn apply_d0(d0: &GF2Matrix, x: &[u8]) -> Result<Vec<u8>, String> {
    if x.len() != d0.cols {
        return Err(format!("vector len {} != d0.cols {}", x.len(), d0.cols));
    }
    let mut out = vec![0u8; d0.rows];
    for i in 0..d0.rows {
        let mut sum = 0u8;
        for j in 0..d0.cols {
            sum ^= d0.data[i][j] & (x[j] & 1);
        }
        out[i] = sum & 1;
    }
    Ok(out)
}

pub fn is_closed(d1: &GF2Matrix, omega: &[u8]) -> Result<bool, String> {
    let s = apply_d1(d1, omega)?;
    Ok(syndrome_is_zero(&s))
}

pub fn in_image_d0(d0: &GF2Matrix, omega: &[u8]) -> Result<bool, String> {
    if omega.len() != d0.rows {
        return Err(format!("vector len {} != d0.rows {}", omega.len(), d0.rows));
    }
    let (rank_d0, _) = d0.rref();
    let mut augmented = vec![vec![0u8; d0.cols + 1]; d0.rows];
    for r in 0..d0.rows {
        for c in 0..d0.cols {
            augmented[r][c] = d0.data[r][c];
        }
        augmented[r][d0.cols] = omega[r] & 1;
    }
    let (aug_rank, _) = GF2Matrix::from_data(augmented).rref();
    Ok(aug_rank == rank_d0)
}

pub fn solve_d0(d0: &GF2Matrix, omega: &[u8]) -> Result<Option<Vec<u8>>, String> {
    if omega.len() != d0.rows {
        return Err(format!("vector len {} != d0.rows {}", omega.len(), d0.rows));
    }
    let mut augmented = vec![vec![0u8; d0.cols + 1]; d0.rows];
    for r in 0..d0.rows {
        for c in 0..d0.cols {
            augmented[r][c] = d0.data[r][c] & 1;
        }
        augmented[r][d0.cols] = omega[r] & 1;
    }
    let (_, reduced) = GF2Matrix::from_data(augmented).rref();

    let mut alpha = vec![0u8; d0.cols];
    for r in 0..reduced.rows {
        match (0..d0.cols).find(|&c| reduced.data[r][c] == 1) {
            Some(pivot) => alpha[pivot] = reduced.data[r][d0.cols],
            None => {
                if reduced.data[r][d0.cols] == 1 {
                    return Ok(None);
                }
            }
        }
    }
    Ok(Some(alpha))
}

pub fn gf2_add(a: &[u8], b: &[u8]) -> Result<Vec<u8>, String> {
    if a.len() != b.len() {
        return Err(format!("length mismatch {} vs {}", a.len(), b.len()));
    }
    Ok(a.iter().zip(b).map(|(&x, &y)| (x ^ y) & 1).collect())
}

fn enumerate_all(n: usize) -> Result<Vec<Vec<u8>>, String> {
    if n > MAX_EXHAUSTIVE_EDGES {
        return Err(format!(
            "exhaustive search refused for |E|={n} > {MAX_EXHAUSTIVE_EDGES} (CODE_DEMO fence)"
        ));
    }
    let count = 1usize << n;
    let mut out = Vec::with_capacity(count);
    for state in 0..count {
        let mut v = vec![0u8; n];
        for i in 0..n {
            v[i] = ((state >> i) & 1) as u8;
        }
        out.push(v);
    }
    Ok(out)
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct HomologyDistanceReport {
    pub complex_name: &'static str,
    pub d: Option<usize>,
    pub t: Option<usize>,
    pub min_weight_representative: Option<Vec<u8>>,
    pub q1_dimension: usize,
    pub authority_effect: &'static str,
}

pub type RepairCapacityReceipt = HomologyDistanceReport;

pub fn repair_capacity_bound(d: usize) -> usize {
    d.saturating_sub(1) / 2
}

pub fn repair_capacity_t(d: usize) -> usize {
    repair_capacity_bound(d)
}

fn is_nontrivial_cocycle(complex: &ChainComplexGf2, v: &[u8]) -> Result<bool, String> {
    if v.iter().all(|&b| b == 0) {
        return Ok(false);
    }
    if !is_closed(&complex.d1, v)? {
        return Ok(false);
    }
    Ok(!in_image_d0(&complex.d0, v)?)
}

pub fn homology_distance(complex: &ChainComplexGf2) -> Result<HomologyDistanceReport, String> {
    if !complex.verify_boundary() {
        return Err("boundary d1 d0 != 0".into());
    }
    let n = complex.num_edges;
    let all = enumerate_all(n)?;

    let mut min_d: Option<usize> = None;
    let mut rep: Option<Vec<u8>> = None;

    for v in &all {
        if !is_nontrivial_cocycle(complex, v)? {
            continue;
        }
        let w = hamming_weight(v);
        if min_d.map_or(true, |cur| w < cur) {
            min_d = Some(w);
            rep = Some(v.clone());
        }
    }

    let cert = Gf2CocycleClassifier::classify(&complex.d0, &complex.d1, &vec![0u8; n])?;
    let q1 = cert.q1_dimension;
    let t = min_d.map(repair_capacity_bound);
    Ok(HomologyDistanceReport {
        complex_name: complex.name,
        d: min_d,
        t,
        min_weight_representative: rep,
        q1_dimension: q1,
        authority_effect: "None",
    })
}

pub fn audit_repair_capacity(
    complex: &ChainComplexGf2,
    _max_weight: usize,
) -> Result<RepairCapacityReceipt, String> {
    let mut report = homology_distance(complex)?;
    let _ = &mut report;
    Ok(report)
}

impl HomologyDistanceReport {
    pub fn homology_distance_d(&self) -> Option<usize> {
        self.d
    }
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CosetDecodeDemo {
    pub error: Vec<u8>,
    pub error_weight: usize,
    pub syndrome: Vec<u8>,
    pub t: Option<usize>,
    pub d: Option<usize>,
    pub within_capacity: bool,
    pub closest_weight: usize,
    pub num_closest: usize,
    pub unique_closest: bool,
    pub a_closest: Vec<u8>,
    pub logical_same_syndrome: Option<bool>,
    pub logical_flips_unique_leader: Option<bool>,
    pub authority_effect: &'static str,
}

pub fn coset_decode_demo(
    complex: &ChainComplexGf2,
    error: &[u8],
    logical: Option<&[u8]>,
) -> Result<CosetDecodeDemo, String> {
    let report = homology_distance(complex)?;
    coset_decode_demo_inner(complex, error, report.d, report.t, logical)
}

fn find_closest_coset_leaders(
    d1: &GF2Matrix,
    all: &[Vec<u8>],
    syndrome: &[u8],
) -> Result<(usize, Vec<Vec<u8>>), String> {
    let mut closest_weight = usize::MAX;
    let mut closest: Vec<Vec<u8>> = Vec::new();
    for v in all {
        if apply_d1(d1, v)? != syndrome {
            continue;
        }
        let w = hamming_weight(v);
        if w < closest_weight {
            closest_weight = w;
            closest.clear();
            closest.push(v.clone());
        } else if w == closest_weight {
            closest.push(v.clone());
        }
    }
    if closest.is_empty() {
        return Err("empty coset (internal error)".into());
    }
    Ok((closest_weight, closest))
}

fn evaluate_logical_shift(
    complex: &ChainComplexGf2,
    error: &[u8],
    syndrome: &[u8],
    closest: &[Vec<u8>],
    d: Option<usize>,
    t: Option<usize>,
    log: &[u8],
) -> Result<(bool, bool), String> {
    let n = complex.num_edges;
    if log.len() != n {
        return Err(format!("logical len {} != |E|={}", log.len(), n));
    }
    if !is_closed(&complex.d1, log)? {
        return Err("logical must be closed (d1 L = 0)".into());
    }
    let e_plus_l = gf2_add(error, log)?;
    let syn_l = apply_d1(&complex.d1, &e_plus_l)?;
    let same_syndrome = syn_l == syndrome;
    let demo_l = coset_decode_demo_inner(complex, &e_plus_l, d, t, None)?;
    let leaders_differ =
        closest.len() != 1 || !demo_l.unique_closest || demo_l.a_closest != closest[0];
    Ok((same_syndrome, leaders_differ))
}

fn coset_decode_demo_inner(
    complex: &ChainComplexGf2,
    error: &[u8],
    d: Option<usize>,
    t: Option<usize>,
    logical: Option<&[u8]>,
) -> Result<CosetDecodeDemo, String> {
    let n = complex.num_edges;
    if error.len() != n {
        return Err(format!("error len {} != |E|={}", error.len(), n));
    }
    let syndrome = apply_d1(&complex.d1, error)?;
    let all = enumerate_all(n)?;
    let (closest_weight, closest) = find_closest_coset_leaders(&complex.d1, &all, &syndrome)?;

    let wt_e = hamming_weight(error);
    let within = t.map_or(true, |tv| wt_e <= tv);

    let (logical_same_syndrome, logical_flips_unique_leader) = match logical {
        Some(log) => {
            let (same, flips) =
                evaluate_logical_shift(complex, error, &syndrome, &closest, d, t, log)?;
            (Some(same), Some(flips))
        }
        None => (None, None),
    };

    Ok(CosetDecodeDemo {
        error: error.iter().map(|&b| b & 1).collect(),
        error_weight: wt_e,
        syndrome,
        t,
        d,
        within_capacity: within,
        closest_weight,
        num_closest: closest.len(),
        unique_closest: closest.len() == 1,
        a_closest: closest[0].clone(),
        logical_same_syndrome,
        logical_flips_unique_leader,
        authority_effect: "None",
    })
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LggrDemoReport {
    pub complex_name: &'static str,
    pub omega: Vec<u8>,
    pub syndrome_zero: bool,
    pub schedule_status: GF2ScheduleStatus,
    pub local_green: bool,
    pub global_red: bool,
    pub lggr: bool,
    pub authority_effect: &'static str,
}

pub fn lggr_demo_torus() -> Result<LggrDemoReport, String> {
    let complex = surface_grid_2x2_torus();
    let omega = torus_logical_x_example();
    lggr_demo_on(&complex, &omega)
}

pub fn lggr_demo_on(complex: &ChainComplexGf2, omega: &[u8]) -> Result<LggrDemoReport, String> {
    let cert = Gf2CocycleClassifier::classify(&complex.d0, &complex.d1, omega)?;
    let syndrome_zero = is_closed(&complex.d1, omega)?;
    let local_green = syndrome_zero;
    let global_red = cert.status == GF2ScheduleStatus::ClosedResidual;
    Ok(LggrDemoReport {
        complex_name: complex.name,
        omega: omega.iter().map(|&b| b & 1).collect(),
        syndrome_zero,
        schedule_status: cert.status,
        local_green,
        global_red,
        lggr: local_green && global_red,
        authority_effect: "None",
    })
}


#[cfg(test)]
mod tests {
    use super::*;
    use crate::complexes::{
        surface_exact_from_vertex0, surface_grid_2x2_planar, surface_open_single_edge_example,
        torus_logical_z_example, triangle,
    };

    #[test]
    fn hamming_weight_basic() {
        assert_eq!(hamming_weight(&[]), 0);
        assert_eq!(hamming_weight(&[0, 0, 0]), 0);
        assert_eq!(hamming_weight(&[1, 0, 1, 1]), 3);
        assert_eq!(hamming_weight(&[2, 3, 0]), hamming_weight(&[0, 1, 0]));
    }

    #[test]
    fn planar_disk_homology_distance_is_none() {
        let c = surface_grid_2x2_planar();
        let r = homology_distance(&c).unwrap();
        assert_eq!(r.authority_effect, "None");
        assert_eq!(r.q1_dimension, 0);
        assert_eq!(
            r.d, None,
            "disk fill ⇒ H1=0 ⇒ no nontrivial cocycle distance"
        );
        assert_eq!(r.t, None);
    }

    #[test]
    fn torus_2x2_homology_distance_and_capacity() {
        let c = surface_grid_2x2_torus();
        let r = homology_distance(&c).unwrap();
        assert_eq!(r.authority_effect, "None");
        assert!(r.q1_dimension >= 1);
        assert_eq!(r.d, Some(2), "torus_2x2 homology distance d must be 2");
        assert_eq!(r.t, Some(0), "t = floor((2-1)/2) = 0");
        let rep = r.min_weight_representative.as_ref().unwrap();
        assert_eq!(hamming_weight(rep), 2);
        assert!(is_closed(&c.d1, rep).unwrap());
        assert!(!in_image_d0(&c.d0, rep).unwrap());

        let audit = audit_repair_capacity(&c, 8).unwrap();
        assert_eq!(audit.homology_distance_d(), Some(2));
        assert_eq!(audit.t, Some(0));
    }

    #[test]
    fn repair_capacity_bound_formula() {
        assert_eq!(repair_capacity_bound(1), 0);
        assert_eq!(repair_capacity_bound(2), 0);
        assert_eq!(repair_capacity_bound(3), 1);
        assert_eq!(repair_capacity_bound(4), 1);
        assert_eq!(repair_capacity_bound(5), 2);
        assert_eq!(repair_capacity_t(2), 0);
    }

    #[test]
    fn coset_decode_within_capacity_zero_error_unique() {
        let c = surface_grid_2x2_torus();
        let e = vec![0u8; c.num_edges];
        let demo = coset_decode_demo(&c, &e, None).unwrap();
        assert_eq!(demo.authority_effect, "None");
        assert_eq!(demo.d, Some(2));
        assert_eq!(demo.t, Some(0));
        assert!(demo.within_capacity);
        assert_eq!(demo.error_weight, 0);
        assert!(demo.unique_closest);
        assert_eq!(demo.closest_weight, 0);
        assert_eq!(demo.a_closest, e);
    }

    #[test]
    fn coset_decode_weight_above_t_logical_preserves_syndrome() {
        let c = surface_grid_2x2_torus();
        let e = surface_open_single_edge_example(c.num_edges);
        assert_eq!(hamming_weight(&e), 1);
        let demo = coset_decode_demo(&c, &e, Some(&torus_logical_x_example())).unwrap();
        assert_eq!(demo.authority_effect, "None");
        assert!(!demo.within_capacity, "wt=1 > t=0");
        assert_eq!(demo.logical_same_syndrome, Some(true));
        assert!(demo.error_weight > demo.t.unwrap());
    }

    #[test]
    fn coset_decode_logical_on_zero_error_invisible_to_min_weight() {
        let c = surface_grid_2x2_torus();
        let e = vec![0u8; c.num_edges];
        let lx = torus_logical_x_example();
        let demo = coset_decode_demo(&c, &e, Some(&lx)).unwrap();
        assert_eq!(demo.logical_same_syndrome, Some(true));
        assert_eq!(demo.logical_flips_unique_leader, Some(false));
        assert!(demo.unique_closest);
        assert_eq!(demo.a_closest, e);
        let e_plus_l = gf2_add(&e, &lx).unwrap();
        assert_ne!(e_plus_l, demo.a_closest);
        assert_eq!(hamming_weight(&lx), 2);
        assert!(demo.t.unwrap() < hamming_weight(&lx));
    }

    #[test]
    fn lggr_torus_local_green_global_red() {
        let report = lggr_demo_torus().unwrap();
        assert_eq!(report.authority_effect, "None");
        assert!(report.syndrome_zero, "Local Green: d1 ω = 0");
        assert!(report.local_green);
        assert!(report.global_red, "Global Red: ClosedResidual");
        assert!(report.lggr);
        assert_eq!(report.schedule_status, GF2ScheduleStatus::ClosedResidual);

        let c = surface_grid_2x2_torus();
        for omega in [torus_logical_x_example(), torus_logical_z_example()] {
            let r = lggr_demo_on(&c, &omega).unwrap();
            assert!(r.lggr, "logical {:?} should be LGGR", omega);
        }
    }

    #[test]
    fn lggr_exact_is_not_global_red() {
        let c = surface_grid_2x2_torus();
        let exact = surface_exact_from_vertex0(&c.d0);
        let r = lggr_demo_on(&c, &exact).unwrap();
        assert!(r.local_green, "coboundaries are closed");
        assert!(!r.global_red);
        assert!(!r.lggr);
        assert_eq!(r.schedule_status, GF2ScheduleStatus::Exact);
    }

    #[test]
    fn planar_edge_has_no_distance_and_two_weight_one_leaders() {
        let c = surface_grid_2x2_planar();
        let e = surface_open_single_edge_example(c.num_edges);
        let demo = coset_decode_demo(&c, &e, None).unwrap();
        assert_eq!(demo.d, None);
        assert_eq!(demo.t, None);
        assert!(demo.within_capacity);
        assert_eq!(demo.error_weight, 1);
        assert_eq!(demo.syndrome, vec![1, 0, 0, 0]);
        assert_eq!(demo.closest_weight, 1);
        assert_eq!(demo.num_closest, 2);
        assert!(!demo.unique_closest);
        assert_eq!(demo.a_closest, e);
        assert_eq!(apply_d1(&c.d1, &demo.a_closest).unwrap(), demo.syndrome);
        assert!(coset_decode_demo(&c, &[1, 0], None)
            .unwrap_err()
            .contains("len"));

        assert_eq!(gf2_add(&[1, 0, 1], &[1, 1, 0]).unwrap(), vec![0, 1, 1]);
        assert!(gf2_add(&[1], &[1, 0]).unwrap_err().contains("length"));
        let tri = triangle();
        assert_eq!(apply_d1(&tri.d1, &[1, 0, 0]).unwrap(), vec![1]);
        assert_eq!(apply_d1(&tri.d1, &[1, 1, 0]).unwrap(), vec![0]);
        assert_eq!(apply_d1(&tri.d1, &[1, 1, 1]).unwrap(), vec![1]);
        assert!(apply_d1(&tri.d1, &[1])
            .unwrap_err()
            .contains("vector len 1 != d1.cols"));
    }
}
