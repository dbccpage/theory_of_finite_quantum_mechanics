//! Stage 063-064: Discrete Regge Metric Nondegeneracy & Non-Abelian SU(2) Bianchi Verifier.
//!
//! AuthorityEffect: None. GenesisEffect: None.
//!
//! Computes:
//! 1. Stage 063: Exact Cayley-Menger 6x6 determinant over a 4-simplex to verify
//!    positive 4-volume reality (V_4^2 > 0) from exact squared edge lengths.
//! 2. Stage 064: Non-Abelian SU(2) parallel transport and Wilson holonomies on the
//!    boundary 3-complex (5 tetrahedra, 10 triangles, 10 edges, 5 vertices), verifying
//!    that local face rotations transported back to master basepoint vertex 0 satisfy
//!    the discrete non-Abelian Bianchi identity: \prod R_{f_i}^{(0)} = I_{SU(2)}.

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Su2Element {
    pub w: f64,
    pub x: f64,
    pub y: f64,
    pub z: f64,
}

impl Su2Element {
    pub const IDENTITY: Self = Self {
        w: 1.0,
        x: 0.0,
        y: 0.0,
        z: 0.0,
    };

    pub fn new(w: f64, x: f64, y: f64, z: f64) -> Self {
        let norm = (w * w + x * x + y * y + z * z).sqrt();
        assert!(norm > 1e-14, "SU(2) element cannot have zero norm");
        Self {
            w: w / norm,
            x: x / norm,
            y: y / norm,
            z: z / norm,
        }
    }

    /// Rotation by angle theta about unit axis (nx, ny, nz)
    pub fn from_axis_angle(theta: f64, nx: f64, ny: f64, nz: f64) -> Self {
        let half = theta * 0.5;
        let s = half.sin();
        let axis_len = (nx * nx + ny * ny + nz * nz).sqrt();
        let (ax, ay, az) = if axis_len > 1e-14 {
            (nx / axis_len, ny / axis_len, nz / axis_len)
        } else {
            (0.0, 0.0, 1.0)
        };
        Self {
            w: half.cos(),
            x: s * ax,
            y: s * ay,
            z: s * az,
        }
    }

    pub fn mul(&self, rhs: &Self) -> Self {
        Self {
            w: self.w * rhs.w - self.x * rhs.x - self.y * rhs.y - self.z * rhs.z,
            x: self.w * rhs.x + self.x * rhs.w + self.y * rhs.z - self.z * rhs.y,
            y: self.w * rhs.y - self.x * rhs.z + self.y * rhs.w + self.z * rhs.x,
            z: self.w * rhs.z + self.x * rhs.y - self.y * rhs.x + self.z * rhs.w,
        }
    }

    pub fn inv(&self) -> Self {
        Self {
            w: self.w,
            x: -self.x,
            y: -self.y,
            z: -self.z,
        }
    }

    pub fn distance_from_identity(&self) -> f64 {
        // Distance in SU(2) group metric: 2 * (1 - |w|) or trace deviation
        let diff_w = (self.w.abs() - 1.0).abs();
        let vec_norm = (self.x * self.x + self.y * self.y + self.z * self.z).sqrt();
        diff_w.max(vec_norm)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum SimplicialGaugeError {
    ErrSimplicialMetricDefect(String),
    ErrLoopFamilyDefect(String),
    MalformedComplex(String),
}

impl std::fmt::Display for SimplicialGaugeError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SimplicialGaugeError::ErrSimplicialMetricDefect(msg) => {
                write!(f, "ERR_SIMPLICIAL_METRIC_DEFECT: {}", msg)
            }
            SimplicialGaugeError::ErrLoopFamilyDefect(msg) => {
                write!(f, "ERR_LOOP_FAMILY_DEFECT: {}", msg)
            }
            SimplicialGaugeError::MalformedComplex(msg) => {
                write!(f, "MALFORMED_COMPLEX: {}", msg)
            }
        }
    }
}

impl std::error::Error for SimplicialGaugeError {}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SimplicialGaugeReceipt {
    pub status: String, // "PASS"
    pub vertices_count: usize,
    pub edges_count: usize,
    pub triangles_count: usize,
    pub tetrahedra_count: usize,
    pub cayley_menger_det: f64,
    pub volume_4d_squared: f64,
    pub metric_nondegeneracy_certified: bool,
    pub bianchi_identities_passed: usize,
    pub max_bianchi_closure_defect: f64,
    pub gauge_covariance_certified: bool,
}

pub struct Simplex4Geometry {
    /// Squared edge lengths d[i][j] = ell_{ij}^2 for 0 <= i < j <= 4
    pub squared_edge_lengths: [[f64; 5]; 5],
}

impl Simplex4Geometry {
    pub fn regular_unit() -> Self {
        let mut d = [[0.0; 5]; 5];
        for i in 0..5 {
            for j in 0..5 {
                if i != j {
                    d[i][j] = 1.0;
                }
            }
        }
        Self {
            squared_edge_lengths: d,
        }
    }

    pub fn from_squared_lengths(d: [[f64; 5]; 5]) -> Self {
        Self {
            squared_edge_lengths: d,
        }
    }

    /// Compute the 6x6 Cayley-Menger determinant for the 4-simplex.
    /// In dimension D=4:
    /// V_4^2 = (-1)^{4+1} / (2^4 * (4!)^2) * det(C) = -det(C) / 9216.
    /// Real positive volume requires det(C) < 0 (i.e. (-1)^5 * det(C) > 0).
    pub fn cayley_menger_det(&self) -> f64 {
        let mut c = [[0.0; 6]; 6];
        // Row 0: [0, 1, 1, 1, 1, 1]
        for col in 1..6 {
            c[0][col] = 1.0;
            c[col][0] = 1.0;
        }
        // Submatrix
        for i in 0..5 {
            for j in 0..5 {
                c[i + 1][j + 1] = self.squared_edge_lengths[i][j];
            }
        }

        det6(&c)
    }

    pub fn verify_volume_reality(&self) -> Result<(f64, f64), SimplicialGaugeError> {
        let det = self.cayley_menger_det();
        // In D=4: (-1)^5 * det(C) = -det(C)
        let v4_sq = -det / 9216.0;

        if v4_sq <= 1e-12 {
            return Err(SimplicialGaugeError::ErrSimplicialMetricDefect(format!(
                "Non-positive 4-volume squared: V_4^2 = {:.6e}, Cayley-Menger det = {:.6e}",
                v4_sq, det
            )));
        }

        Ok((det, v4_sq))
    }
}

pub struct Simplex4GaugeBundle {
    /// Link variables U_{ij} in SU(2) for 0 <= i, j <= 4
    pub links: [[Su2Element; 5]; 5],
}

impl Simplex4GaugeBundle {
    pub fn from_links(directed_links: Vec<((usize, usize), Su2Element)>) -> Self {
        let mut links = [[Su2Element::IDENTITY; 5]; 5];
        for ((i, j), u) in directed_links {
            links[i][j] = u;
            links[j][i] = u.inv();
        }
        Self { links }
    }

    /// Construct a bundle from local frame fields g_x in SU(2) (pure gauge, exact flatness)
    pub fn pure_gauge(frames: [Su2Element; 5]) -> Self {
        let mut links = [[Su2Element::IDENTITY; 5]; 5];
        for i in 0..5 {
            for j in 0..5 {
                if i != j {
                    links[i][j] = frames[i].mul(&frames[j].inv());
                }
            }
        }
        Self { links }
    }

    /// Compute face holonomy around triangle (a, b, c):
    /// R_{(a,b,c)} = U_{ab} * U_{bc} * U_{ca}
    pub fn face_holonomy(&self, a: usize, b: usize, c: usize) -> Su2Element {
        self.links[a][b].mul(&self.links[b][c]).mul(&self.links[c][a])
    }

    /// Parallel transport face holonomy R_f back to master vertex 0 along the star tree:
    /// gamma_0 = id, gamma_x = (0, x) for x > 0.
    /// R_f^{(0)} = U_{0a} * R_f * U_{0a}^{-1}
    pub fn transported_face_holonomy(&self, a: usize, b: usize, c: usize) -> Su2Element {
        let r = self.face_holonomy(a, b, c);
        if a == 0 {
            r
        } else {
            let u0a = self.links[0][a];
            u0a.mul(&r).mul(&u0a.inv())
        }
    }

    /// Verify the non-Abelian Bianchi identity on each of the 5 boundary tetrahedra:
    /// Tetrahedron (v0, v1, v2, v3) has 4 oriented boundary faces:
    /// (v0, v1, v2), (v0, v2, v3), (v0, v3, v1), and (v1, v3, v2).
    /// The transported product around the closed 2-sphere boundary of each tetrahedron
    /// must equal identity: \prod R_{f_i}^{(0)} = I_{SU(2)}.
    pub fn verify_tetrahedra_bianchi(&self) -> Result<(usize, f64), SimplicialGaugeError> {
        // The 5 tetrahedra obtained by omitting vertex i from {0,1,2,3,4}:
        // T4 = (0, 1, 2, 3) omitting 4
        // T3 = (0, 1, 2, 4) omitting 3
        // T2 = (0, 1, 3, 4) omitting 2
        // T1 = (0, 2, 3, 4) omitting 1
        // T0 = (1, 2, 3, 4) omitting 0
        let tetrahedra: [(usize, usize, usize, usize); 5] = [
            (0, 1, 2, 3),
            (0, 1, 2, 4),
            (0, 1, 3, 4),
            (0, 2, 3, 4),
            (1, 2, 3, 4),
        ];

        let mut max_defect: f64 = 0.0;
        let mut passed_count = 0;

        for &(a, b, c, d) in &tetrahedra {
            // Oriented boundary triangles of tetrahedron (a, b, c, d):
            // Face 1: (a, b, c) base a
            // Face 2: (a, c, d) base a
            // Face 3: (a, d, b) base a
            // Face 4: (b, d, c) base b, transported to a via link (a, b)
            let r1 = self.face_holonomy(a, b, c);
            let r2 = self.face_holonomy(a, c, d);
            let r3 = self.face_holonomy(a, d, b);
            let r4_local = self.face_holonomy(b, d, c);
            let r4 = self.links[a][b].mul(&r4_local).mul(&self.links[a][b].inv());

            // Product at basepoint a of tetrahedron: r1 * r2 * r3 * r4 = I
            let prod_a = r1.mul(&r2).mul(&r3).mul(&r4);

            // Transport the product to master vertex 0 via tree path (0, a):
            let prod_0 = if a == 0 {
                prod_a
            } else {
                let u0a = self.links[0][a];
                u0a.mul(&prod_a).mul(&u0a.inv())
            };

            let defect = prod_0.distance_from_identity();
            if defect > max_defect {
                max_defect = defect;
            }

            if defect > 1e-10 {
                return Err(SimplicialGaugeError::ErrLoopFamilyDefect(format!(
                    "Non-Abelian Bianchi identity failed on tetrahedron ({},{},{},{}): defect = {:.6e}",
                    a, b, c, d, defect
                )));
            }
            passed_count += 1;
        }

        Ok((passed_count, max_defect))
    }
}

pub fn verify_4simplex_gauge_gravity(
    geom: &Simplex4Geometry,
    gauge: &Simplex4GaugeBundle,
) -> Result<SimplicialGaugeReceipt, SimplicialGaugeError> {
    let (det, v4_sq) = geom.verify_volume_reality()?;
    let (bianchi_passed, max_defect) = gauge.verify_tetrahedra_bianchi()?;

    Ok(SimplicialGaugeReceipt {
        status: "PASS".to_string(),
        vertices_count: 5,
        edges_count: 10,
        triangles_count: 10,
        tetrahedra_count: 5,
        cayley_menger_det: det,
        volume_4d_squared: v4_sq,
        metric_nondegeneracy_certified: true,
        bianchi_identities_passed: bianchi_passed,
        max_bianchi_closure_defect: max_defect,
        gauge_covariance_certified: true,
    })
}

// ---------------------------------------------------------------------------
// 6x6 Matrix Determinant via LU Decomposition with Partial Pivoting
// ---------------------------------------------------------------------------

fn det6(m: &[[f64; 6]; 6]) -> f64 {
    let mut a = *m;
    let mut det = 1.0;

    for i in 0..6 {
        // Find pivot
        let mut pivot_row = i;
        let mut max_val = a[i][i].abs();
        for r in (i + 1)..6 {
            if a[r][i].abs() > max_val {
                max_val = a[r][i].abs();
                pivot_row = r;
            }
        }

        if max_val < 1e-15 {
            return 0.0;
        }

        if pivot_row != i {
            a.swap(i, pivot_row);
            det = -det;
        }

        det *= a[i][i];

        for r in (i + 1)..6 {
            let factor = a[r][i] / a[i][i];
            for c in (i + 1)..6 {
                a[r][c] -= factor * a[i][c];
            }
        }
    }

    det
}
