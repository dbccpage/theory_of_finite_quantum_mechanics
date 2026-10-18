//! Finite cell complexes for Majorana GF(2) play (triangle, plaquette, prism).
//!
//! Built so that \(d_1 \circ d_0 = 0 \pmod 2\) by construction (edge-vertex + face-edge).
//! AuthorityEffect: None.

use crate::gf2_terminalizer::GF2Matrix;

/// A 2-step GF(2) chain complex \(C_0 \xrightarrow{d_0} C_1 \xrightarrow{d_1} C_2\).
#[derive(Debug, Clone)]
pub struct ChainComplexGf2 {
    pub name: &'static str,
    /// \(d_0\): |E| × |V| (edge-vertex incidence mod 2).
    pub d0: GF2Matrix,
    /// \(d_1\): |F| × |E| (face-edge incidence mod 2).
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

/// Triangle: 3 vertices, 3 edges, 1 face.
///
/// Edges: e0=(0,1), e1=(1,2), e2=(0,2). Face: all three edges.
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

/// Square plaquette: 4 vertices, 4 edges, 1 face.
///
/// Edges: (0,1),(1,2),(2,3),(3,0). Face: cycle of four.
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

/// Triangular prism: 6 vertices, 9 edges, 5 faces (2 triangles + 3 quads).
///
/// Bottom triangle 0,1,2; top 3,4,5; vertical edges 0-3,1-4,2-5.
/// Faces: bottom, top, and three lateral quads (each as 4-edge incidence).
pub fn prism() -> ChainComplexGf2 {
    // Edge order:
    // 0:(0,1) 1:(1,2) 2:(0,2) bottom
    // 3:(3,4) 4:(4,5) 5:(3,5) top
    // 6:(0,3) 7:(1,4) 8:(2,5) vertical
    let d0 = GF2Matrix::from_data(vec![
        vec![1, 1, 0, 0, 0, 0], // e0
        vec![0, 1, 1, 0, 0, 0], // e1
        vec![1, 0, 1, 0, 0, 0], // e2
        vec![0, 0, 0, 1, 1, 0], // e3
        vec![0, 0, 0, 0, 1, 1], // e4
        vec![0, 0, 0, 1, 0, 1], // e5
        vec![1, 0, 0, 1, 0, 0], // e6
        vec![0, 1, 0, 0, 1, 0], // e7
        vec![0, 0, 1, 0, 0, 1], // e8
    ]);
    // Faces as edge sets (mod 2 incidence):
    // f0 bottom: e0,e1,e2
    // f1 top: e3,e4,e5
    // f2 side 01-34: e0,e7,e3,e6
    // f3 side 12-45: e1,e8,e4,e7
    // f4 side 02-35: e2,e8,e5,e6
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

/// Example syndromes for triangle play (edge-length 3).
pub fn exact_syndrome_example() -> Vec<u8> {
    // d0 * e_1 = edge incidence of vertex 1 = (1,1,0) on triangle edges
    vec![1, 1, 0]
}

pub fn open_syndrome_example() -> Vec<u8> {
    vec![1, 0, 0]
}

/// Closed but non-exact cycle on triangle: all edges (boundary of face) — in GF(2)
/// this is d1^T * face; for classification we need d1 ω = 0 and not in im d0.
/// On triangle, ω = (1,1,1) has d1 ω = 1+1+1 = 1 mod 2 → open.
/// For closed residual use a graph with H1 ≠ 0 — plaquette cycle ω = (1,1,1,1):
/// d1 ω = 0 mod 2, and not a vertex coboundary if consistent.
pub fn closed_residual_syndrome_example() -> Vec<u8> {
    // Plaquette full cycle (all four edges)
    vec![1, 1, 1, 1]
}

// ---------------------------------------------------------------------------
// Multi-plaquette surface-code toys (CODE_DEMO only; not device thresholds)
// ---------------------------------------------------------------------------

/// Planar \(2\times 2\) plaquette grid (disk topology): \(3\times 3\) vertices,
/// 12 edges, 4 faces. Disk fill ⇒ \(\dim H^1 = 0\) under \(d_1 d_0 = 0\).
///
/// Surface-code **shadow**: edge residual \(e\) with face syndrome \(s = d_1 e\).
/// Logical-like nontrivial classes require the torus toy below.
pub fn surface_grid_2x2_planar() -> ChainComplexGf2 {
    surface_grid(2, 2, false)
}

/// Periodic \(2\times 2\) plaquette torus: \(2\times 2\) vertices, 8 edges, 4 faces.
/// Expect \(\dim H^1 = 2\) (two independent non-contractible cycles over \(\mathbb{F}_2\)).
///
/// **Not** a Willow/Microsoft surface-code packet. CODE_DEMO only.
pub fn surface_grid_2x2_torus() -> ChainComplexGf2 {
    surface_grid(2, 2, true)
}

/// Build an \(m\times n\) plaquette grid over GF(2).
///
/// - `periodic = false`: planar \((m+1)\times(n+1)\) vertices (disk if all faces filled).
/// - `periodic = true`: \(m\times n\) vertices with wrap (torus).
///
/// Edge order: all horizontal edges first (row-major), then all vertical.
/// Face order: plaquette row-major; each face uses the four bounding edges.
pub fn surface_grid(m: usize, n: usize, periodic: bool) -> ChainComplexGf2 {
    assert!(m >= 1 && n >= 1, "need at least one plaquette");
    let (nrows, ncols) = if periodic { (m, n) } else { (m + 1, n + 1) };
    let num_vertices = nrows * ncols;

    let vid = |r: usize, c: usize| -> usize {
        let rr = if periodic { r % nrows } else { r };
        let cc = if periodic { c % ncols } else { c };
        rr * ncols + cc
    };

    // Horizontal edges: for each row r, each col c in 0..n_h
    let n_h_per_row = if periodic { n } else { n };
    let n_h_rows = if periodic { m } else { m + 1 };
    let mut h_edges: Vec<(usize, usize)> = Vec::new();
    for r in 0..n_h_rows {
        for c in 0..n_h_per_row {
            let u = vid(r, c);
            let v = if periodic {
                vid(r, c + 1)
            } else {
                vid(r, c + 1)
            };
            h_edges.push((u, v));
        }
    }

    // Vertical edges
    let n_v_per_col = if periodic { m } else { m };
    let n_v_cols = if periodic { n } else { n + 1 };
    let mut v_edges: Vec<(usize, usize)> = Vec::new();
    for r in 0..n_v_per_col {
        for c in 0..n_v_cols {
            let u = vid(r, c);
            let v = vid(r + 1, c);
            v_edges.push((u, v));
        }
    }

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

    // Face (r,c): lower-left vertex (r,c) in plaquette coords
    // edges: H(r,c), V(r,c+1), H(r+1,c), V(r,c)  (indices)
    let h_index = |r: usize, c: usize| -> usize {
        if periodic {
            (r % m) * n + (c % n)
        } else {
            r * n + c
        }
    };
    let v_index = |r: usize, c: usize| -> usize {
        if periodic {
            num_h + (r % m) * n + (c % n)
        } else {
            num_h + r * (n + 1) + c
        }
    };

    let mut d1_data = vec![vec![0u8; num_edges]; m * n];
    for pr in 0..m {
        for pc in 0..n {
            let fi = pr * n + pc;
            let e_top = h_index(pr, pc);
            let e_right = v_index(pr, pc + 1);
            let e_bot = h_index(pr + 1, pc);
            let e_left = v_index(pr, pc);
            for e in [e_top, e_right, e_bot, e_left] {
                d1_data[fi][e] ^= 1;
            }
        }
    }

    let name: &'static str = if periodic {
        "surface_grid_2x2_torus"
    } else {
        "surface_grid_2x2_planar"
    };
    // Only the 2x2 names are static for the two public constructors; rebuild name via leak only if needed.
    // For general m,n callers use the private builder only via the two pubs for now.
    let _ = (m, n);
    ChainComplexGf2 {
        name: if periodic && m == 2 && n == 2 {
            "surface_grid_2x2_torus"
        } else if !periodic && m == 2 && n == 2 {
            "surface_grid_2x2_planar"
        } else {
            // fallthrough label for future expansion
            name
        },
        d0: GF2Matrix::from_data(d0_data),
        d1: GF2Matrix::from_data(d1_data),
        num_vertices,
        num_edges,
        num_faces: m * n,
    }
}

/// Nontrivial \(H^1\) cocycle on the \(2\times 2\) torus (cochain class, not bare chain cycle).
///
/// Edge order: 4 horizontal then 4 vertical. Representative: alternating H edges
/// `e1 + e3` — lies in \(\ker d_1 \setminus \operatorname{im} d_0\) (CODE_DEMO).
pub fn torus_logical_x_example() -> Vec<u8> {
    vec![0, 1, 0, 1, 0, 0, 0, 0]
}

/// Independent nontrivial cocycle: both vertical edges of the first vertical “row”
/// (`e4 + e5`). Also \(\ker d_1 \setminus \operatorname{im} d_0\) on the \(2\times 2\) torus.
pub fn torus_logical_z_example() -> Vec<u8> {
    vec![0, 0, 0, 0, 1, 1, 0, 0]
}

/// One edge flip → open plaquette syndrome on torus/planar grids with faces.
pub fn surface_open_single_edge_example(num_edges: usize) -> Vec<u8> {
    let mut w = vec![0u8; num_edges];
    if num_edges > 0 {
        w[0] = 1;
    }
    w
}

/// Vertex coboundary of vertex 0 on a complex (Exact class when boundary-valid).
pub fn surface_exact_from_vertex0(d0: &GF2Matrix) -> Vec<u8> {
    // column 0 of d0 is the coboundary of vertex 0 (d0 is |E|×|V|)
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
        // Kills: labeling every even-weight closed vector ClosedResidual.
        // (1,1,1,1) = d0*(0,1,0,1) on C4, and the plaquette has q1 = 0.
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
        // Disk fill: homology trivial → q1_dimension 0
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

        // Non-contractible cycles: closed (all plaquette syndromes 0) and not Exact
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

        // Single edge remains open
        let open = Gf2CocycleClassifier::classify(
            &c.d0,
            &c.d1,
            &surface_open_single_edge_example(c.num_edges),
        )
        .unwrap();
        assert_eq!(open.status, GF2ScheduleStatus::OpenObstruction);
    }
}
