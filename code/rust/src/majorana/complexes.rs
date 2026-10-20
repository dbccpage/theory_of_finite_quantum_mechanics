
use crate::gf2_terminalizer::GF2Matrix;

#[derive(Debug, Clone)]
pub struct ChainComplexGf2 {
    pub name: &'static str,
    pub d0: GF2Matrix,
    pub d1: GF2Matrix,
    pub num_vertices: usize,
    pub num_edges: usize,
    pub num_faces: usize,
}

impl ChainComplexGf2 {
    pub fn verify_boundary(&self) -> bool {
        crate::gf2_terminalizer::Gf2CocycleClassifier::verify_boundary(&self.d0, &self.d1)
    }
}

pub fn triangle() -> ChainComplexGf2 {
    let d0 = GF2Matrix::from_data(vec![vec![1, 1, 0], vec![0, 1, 1], vec![1, 0, 1]]);
    let d1 = GF2Matrix::from_data(vec![vec![1, 1, 1]]);
    ChainComplexGf2 {
        name: "triangle",
        d0,
        d1,
        num_vertices: 3,
        num_edges: 3,
        num_faces: 1,
    }
}

pub fn plaquette() -> ChainComplexGf2 {
    let d0 = GF2Matrix::from_data(vec![
        vec![1, 1, 0, 0],
        vec![0, 1, 1, 0],
        vec![0, 0, 1, 1],
        vec![1, 0, 0, 1],
    ]);
    let d1 = GF2Matrix::from_data(vec![vec![1, 1, 1, 1]]);
    ChainComplexGf2 {
        name: "plaquette",
        d0,
        d1,
        num_vertices: 4,
        num_edges: 4,
        num_faces: 1,
    }
}

pub fn prism() -> ChainComplexGf2 {
    let d0 = GF2Matrix::from_data(vec![
        vec![1, 1, 0, 0, 0, 0],
        vec![0, 1, 1, 0, 0, 0],
        vec![1, 0, 1, 0, 0, 0],
        vec![0, 0, 0, 1, 1, 0],
        vec![0, 0, 0, 0, 1, 1],
        vec![0, 0, 0, 1, 0, 1],
        vec![1, 0, 0, 1, 0, 0],
        vec![0, 1, 0, 0, 1, 0],
        vec![0, 0, 1, 0, 0, 1],
    ]);
    let d1 = GF2Matrix::from_data(vec![
        vec![1, 1, 1, 0, 0, 0, 0, 0, 0],
        vec![0, 0, 0, 1, 1, 1, 0, 0, 0],
        vec![1, 0, 0, 1, 0, 0, 1, 1, 0],
        vec![0, 1, 0, 0, 1, 0, 0, 1, 1],
        vec![0, 0, 1, 0, 0, 1, 1, 0, 1],
    ]);
    ChainComplexGf2 {
        name: "prism",
        d0,
        d1,
        num_vertices: 6,
        num_edges: 9,
        num_faces: 5,
    }
}

pub fn exact_syndrome_example() -> Vec<u8> {
    vec![1, 1, 0]
}

pub fn open_syndrome_example() -> Vec<u8> {
    vec![1, 0, 0]
}

pub fn closed_residual_syndrome_example() -> Vec<u8> {
    vec![1, 1, 1, 1]
}


pub fn surface_grid_2x2_planar() -> ChainComplexGf2 {
    surface_grid(2, 2, false)
}

pub fn surface_grid_2x2_torus() -> ChainComplexGf2 {
    surface_grid(2, 2, true)
}

fn grid_vid(r: usize, c: usize, nrows: usize, ncols: usize, periodic: bool) -> usize {
    let rr = if periodic { r % nrows } else { r };
    let cc = if periodic { c % ncols } else { c };
    rr * ncols + cc
}

fn build_surface_edges(
    m: usize,
    n: usize,
    nrows: usize,
    ncols: usize,
    periodic: bool,
) -> (Vec<(usize, usize)>, Vec<(usize, usize)>) {
    let n_h_rows = if periodic { m } else { m + 1 };
    let mut h_edges: Vec<(usize, usize)> = Vec::new();
    for r in 0..n_h_rows {
        for c in 0..n {
            let u = grid_vid(r, c, nrows, ncols, periodic);
            let v = grid_vid(r, c + 1, nrows, ncols, periodic);
            h_edges.push((u, v));
        }
    }

    let n_v_cols = if periodic { n } else { n + 1 };
    let mut v_edges: Vec<(usize, usize)> = Vec::new();
    for r in 0..m {
        for c in 0..n_v_cols {
            let u = grid_vid(r, c, nrows, ncols, periodic);
            let v = grid_vid(r + 1, c, nrows, ncols, periodic);
            v_edges.push((u, v));
        }
    }
    (h_edges, v_edges)
}

fn build_surface_d0(
    num_vertices: usize,
    h_edges: &[(usize, usize)],
    v_edges: &[(usize, usize)],
) -> GF2Matrix {
    let num_h = h_edges.len();
    let num_edges = num_h + v_edges.len();
    let mut d0_data = vec![vec![0u8; num_vertices]; num_edges];
    for (ei, &(u, v)) in h_edges.iter().enumerate() {
        d0_data[ei][u] = 1;
        d0_data[ei][v] = 1;
    }
    for (ei, &(u, v)) in v_edges.iter().enumerate() {
        d0_data[num_h + ei][u] = 1;
        d0_data[num_h + ei][v] = 1;
    }
    GF2Matrix::from_data(d0_data)
}

fn h_edge_index(r: usize, c: usize, m: usize, n: usize, periodic: bool) -> usize {
    if periodic {
        (r % m) * n + (c % n)
    } else {
        r * n + c
    }
}

fn v_edge_index(r: usize, c: usize, m: usize, n: usize, num_h: usize, periodic: bool) -> usize {
    if periodic {
        num_h + (r % m) * n + (c % n)
    } else {
        num_h + r * (n + 1) + c
    }
}

fn build_surface_d1(
    m: usize,
    n: usize,
    num_h: usize,
    num_edges: usize,
    periodic: bool,
) -> GF2Matrix {
    let mut d1_data = vec![vec![0u8; num_edges]; m * n];
    for pr in 0..m {
        for pc in 0..n {
            let fi = pr * n + pc;
            let e_top = h_edge_index(pr, pc, m, n, periodic);
            let e_right = v_edge_index(pr, pc + 1, m, n, num_h, periodic);
            let e_bot = h_edge_index(pr + 1, pc, m, n, periodic);
            let e_left = v_edge_index(pr, pc, m, n, num_h, periodic);
            d1_data[fi][e_top] ^= 1;
            d1_data[fi][e_right] ^= 1;
            d1_data[fi][e_bot] ^= 1;
            d1_data[fi][e_left] ^= 1;
        }
    }
    GF2Matrix::from_data(d1_data)
}

pub fn try_surface_grid(
    m: usize,
    n: usize,
    periodic: bool,
) -> Result<ChainComplexGf2, &'static str> {
    if m == 0 || n == 0 {
        return Err("surface_grid requires m >= 1 and n >= 1");
    }
    let (nrows, ncols) = if periodic { (m, n) } else { (m + 1, n + 1) };
    let num_vertices = nrows * ncols;
    let (h_edges, v_edges) = build_surface_edges(m, n, nrows, ncols, periodic);
    let num_h = h_edges.len();
    let num_edges = num_h + v_edges.len();
    let d0 = build_surface_d0(num_vertices, &h_edges, &v_edges);
    let d1 = build_surface_d1(m, n, num_h, num_edges, periodic);
    let name: &'static str = if periodic {
        "surface_grid_2x2_torus"
    } else {
        "surface_grid_2x2_planar"
    };
    Ok(ChainComplexGf2 {
        name,
        d0,
        d1,
        num_vertices,
        num_edges,
        num_faces: m * n,
    })
}

pub fn surface_grid(m: usize, n: usize, periodic: bool) -> ChainComplexGf2 {
    try_surface_grid(m, n, periodic).expect("need at least one plaquette")
}

pub fn torus_logical_x_example() -> Vec<u8> {
    vec![0, 1, 0, 1, 0, 0, 0, 0]
}

pub fn torus_logical_z_example() -> Vec<u8> {
    vec![0, 0, 0, 0, 1, 1, 0, 0]
}

pub fn surface_open_single_edge_example(num_edges: usize) -> Vec<u8> {
    let mut w = vec![0u8; num_edges];
    if num_edges > 0 {
        w[0] = 1;
    }
    w
}

pub fn surface_exact_from_vertex0(d0: &GF2Matrix) -> Vec<u8> {
    (0..d0.rows).map(|r| d0.data[r][0]).collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::gf2_terminalizer::{GF2ScheduleStatus, Gf2CocycleClassifier};

    #[test]
    fn all_complexes_have_valid_boundary() {
        for c in [
            triangle(),
            plaquette(),
            prism(),
            surface_grid_2x2_planar(),
            surface_grid_2x2_torus(),
        ] {
            assert!(c.verify_boundary(), "{} fails d1 d0 = 0", c.name);
        }
        assert!(try_surface_grid(0, 2, false).is_err());
        assert!(try_surface_grid(2, 0, true).is_err());
    }

    #[test]
    fn play_triangle_exact_and_open() {
        let c = triangle();
        let exact =
            Gf2CocycleClassifier::classify(&c.d0, &c.d1, &exact_syndrome_example()).unwrap();
        assert_eq!(exact.status, GF2ScheduleStatus::Exact);
        assert_eq!(exact.authority_effect, "None");

        let open = Gf2CocycleClassifier::classify(&c.d0, &c.d1, &open_syndrome_example()).unwrap();
        assert_eq!(open.status, GF2ScheduleStatus::OpenObstruction);
    }

    #[test]
    fn play_plaquette_even_cycle_is_exact() {
        let c = plaquette();
        let cert =
            Gf2CocycleClassifier::classify(&c.d0, &c.d1, &closed_residual_syndrome_example())
                .unwrap();
        assert_eq!(cert.status, GF2ScheduleStatus::Exact);
        assert_eq!(cert.q1_dimension, 0);
        assert_ne!(cert.status, GF2ScheduleStatus::ClosedResidual);
    }

    #[test]
    fn play_surface_planar_exact_and_open() {
        let c = surface_grid_2x2_planar();
        assert_eq!(c.num_faces, 4);
        assert_eq!(c.num_vertices, 9);
        assert_eq!(c.num_edges, 12);

        let exact_syn = surface_exact_from_vertex0(&c.d0);
        let exact = Gf2CocycleClassifier::classify(&c.d0, &c.d1, &exact_syn).unwrap();
        assert_eq!(exact.status, GF2ScheduleStatus::Exact);
        assert_eq!(exact.authority_effect, "None");
        assert_eq!(exact.q1_dimension, 0);

        let open_syn = surface_open_single_edge_example(c.num_edges);
        let open = Gf2CocycleClassifier::classify(&c.d0, &c.d1, &open_syn).unwrap();
        assert_eq!(open.status, GF2ScheduleStatus::OpenObstruction);
    }

    #[test]
    fn play_surface_torus_logical_closed_residual() {
        let c = surface_grid_2x2_torus();
        assert_eq!(c.num_faces, 4);
        assert_eq!(c.num_vertices, 4);
        assert_eq!(c.num_edges, 8);
        assert!(c.verify_boundary());

        let lx = torus_logical_x_example();
        let cert_x = Gf2CocycleClassifier::classify(&c.d0, &c.d1, &lx).unwrap();
        assert_eq!(
            cert_x.status,
            GF2ScheduleStatus::ClosedResidual,
            "horizontal torus cycle should be ClosedResidual, got {:?}",
            cert_x.status
        );
        assert_eq!(cert_x.authority_effect, "None");
        assert!(
            cert_x.q1_dimension >= 1,
            "torus should have positive H1 dim, got {}",
            cert_x.q1_dimension
        );

        let lz = torus_logical_z_example();
        let cert_z = Gf2CocycleClassifier::classify(&c.d0, &c.d1, &lz).unwrap();
        assert_eq!(cert_z.status, GF2ScheduleStatus::ClosedResidual);
        assert_eq!(cert_z.authority_effect, "None");

        let open = Gf2CocycleClassifier::classify(
            &c.d0,
            &c.d1,
            &surface_open_single_edge_example(c.num_edges),
        )
        .unwrap();
        assert_eq!(open.status, GF2ScheduleStatus::OpenObstruction);
    }
}
