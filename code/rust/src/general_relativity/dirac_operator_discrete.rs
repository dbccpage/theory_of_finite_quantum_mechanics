
use serde::{Deserialize, Serialize};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; discrete simplicial Dirac operator.";

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct Spinor2 {
    pub u: (f64, f64),
    pub d: (f64, f64),
}

impl Spinor2 {
    pub fn new(u: (f64, f64), d: (f64, f64)) -> Self {
        Self { u, d }
    }

    pub fn zero() -> Self {
        Self {
            u: (0.0, 0.0),
            d: (0.0, 0.0),
        }
    }

    pub fn add(&self, other: &Self) -> Self {
        Self {
            u: (self.u.0 + other.u.0, self.u.1 + other.u.1),
            d: (self.d.0 + other.d.0, self.d.1 + other.d.1),
        }
    }

    pub fn scale_complex(&self, c: (f64, f64)) -> Self {
        let (cr, ci) = c;
        Self {
            u: (cr * self.u.0 - ci * self.u.1, cr * self.u.1 + ci * self.u.0),
            d: (cr * self.d.0 - ci * self.d.1, cr * self.d.1 + ci * self.d.0),
        }
    }

    pub fn dot_dagger(&self, other: &Self) -> (f64, f64) {
        let re = (self.u.0 * other.u.0 + self.u.1 * other.u.1)
            + (self.d.0 * other.d.0 + self.d.1 * other.d.1);
        let im = (self.u.0 * other.u.1 - self.u.1 * other.u.0)
            + (self.d.0 * other.d.1 - self.d.1 * other.d.0);
        (re, im)
    }

    pub fn pauli_dot(&self, n: [f64; 3]) -> Self {
        let [nx, ny, nz] = n;
        let term1_u = (nz * self.u.0, nz * self.u.1);
        let term2_u = (
            nx * self.d.0 + ny * self.d.1,
            nx * self.d.1 - ny * self.d.0,
        );

        let term1_d = (
            nx * self.u.0 - ny * self.u.1,
            nx * self.u.1 + ny * self.u.0,
        );
        let term2_d = (-nz * self.d.0, -nz * self.d.1);

        Self {
            u: (term1_u.0 + term2_u.0, term1_u.1 + term2_u.1),
            d: (term1_d.0 + term2_d.0, term1_d.1 + term2_d.1),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct SpinConnectionSU2 {
    pub a: [f64; 4],
}

impl SpinConnectionSU2 {
    pub fn identity() -> Self {
        Self {
            a: [1.0, 0.0, 0.0, 0.0],
        }
    }

    pub fn new_normalized(a: [f64; 4]) -> Result<Self, String> {
        let norm_sq = a[0] * a[0] + a[1] * a[1] + a[2] * a[2] + a[3] * a[3];
        if norm_sq < 1e-12 || !norm_sq.is_finite() {
            return Err("Zero or non-finite SU(2) connection parameters".to_string());
        }
        let norm = norm_sq.sqrt();
        Ok(Self {
            a: [a[0] / norm, a[1] / norm, a[2] / norm, a[3] / norm],
        })
    }

    pub fn dagger(&self) -> Self {
        Self {
            a: [self.a[0], -self.a[1], -self.a[2], -self.a[3]],
        }
    }

    pub fn apply(&self, psi: &Spinor2) -> Spinor2 {
        let a0 = self.a[0];
        let term_id = Spinor2 {
            u: (a0 * psi.u.0, a0 * psi.u.1),
            d: (a0 * psi.d.0, a0 * psi.d.1),
        };
        let pauli = psi.pauli_dot([self.a[1], self.a[2], self.a[3]]);
        let i_pauli = pauli.scale_complex((0.0, 1.0));
        term_id.add(&i_pauli)
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct SimplicialDiracOperator {
    pub num_vertices: usize,
    pub vertex_volumes: Vec<f64>,
    pub directed_edges: Vec<(usize, usize, f64, [f64; 3], SpinConnectionSU2)>,
}

impl SimplicialDiracOperator {
    pub fn new(
        num_vertices: usize,
        vertex_volumes: Vec<f64>,
        directed_edges: Vec<(usize, usize, f64, [f64; 3], SpinConnectionSU2)>,
    ) -> Result<Self, String> {
        if vertex_volumes.len() != num_vertices {
            return Err("Vertex volumes count does not match num_vertices".to_string());
        }
        for (v, &vol) in vertex_volumes.iter().enumerate() {
            if vol <= 1e-12 || !vol.is_finite() {
                return Err(format!("Non-positive volume at vertex {v}: {vol}"));
            }
        }
        Ok(Self {
            num_vertices,
            vertex_volumes,
            directed_edges,
        })
    }

    pub fn apply(&self, psi: &[Spinor2]) -> Result<Vec<Spinor2>, String> {
        if psi.len() != self.num_vertices {
            return Err("Spinor field dimension does not match operator dimension".to_string());
        }

        let mut d_psi = vec![Spinor2::zero(); self.num_vertices];

        for &(u, v, weight, n_uv, conn) in &self.directed_edges {
            if u >= self.num_vertices || v >= self.num_vertices {
                continue;
            }

            let psi_trans = conn.apply(&psi[v]);

            let pauli_psi = psi_trans.pauli_dot(n_uv);

            let term = pauli_psi.scale_complex((0.0, -weight));

            d_psi[u] = d_psi[u].add(&term);
        }

        for (u, val) in d_psi.iter_mut().enumerate() {
            let inv_v = 1.0 / self.vertex_volumes[u];
            *val = val.scale_complex((inv_v, 0.0));
        }

        Ok(d_psi)
    }

    pub fn inner_product(&self, phi: &[Spinor2], psi: &[Spinor2]) -> Result<(f64, f64), String> {
        if phi.len() != self.num_vertices || psi.len() != self.num_vertices {
            return Err("Spinor field dimension mismatch in inner product".to_string());
        }

        let mut total_re = 0.0;
        let mut total_im = 0.0;

        for u in 0..self.num_vertices {
            let vol = self.vertex_volumes[u];
            let (dr, di) = phi[u].dot_dagger(&psi[u]);
            total_re += vol * dr;
            total_im += vol * di;
        }

        Ok((total_re, total_im))
    }

    pub fn check_hermiticity(
        &self,
        phi: &[Spinor2],
        psi: &[Spinor2],
        tolerance: f64,
    ) -> Result<bool, String> {
        let d_psi = self.apply(psi)?;
        let d_phi = self.apply(phi)?;

        let (re1, im1) = self.inner_product(phi, &d_psi)?;
        let (re2, im2) = self.inner_product(&d_phi, psi)?;

        let diff_sq = (re1 - re2).powi(2) + (im1 - im2).powi(2);
        Ok(diff_sq.sqrt() < tolerance)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_spinor_pauli_dot_involution() {
        let psi = Spinor2::new((1.5, 0.5), (-0.8, 1.2));
        let n = [1.0 / 3.0f64.sqrt(), 1.0 / 3.0f64.sqrt(), 1.0 / 3.0f64.sqrt()];

        let step1 = psi.pauli_dot(n);
        let step2 = step1.pauli_dot(n);

        assert!((step2.u.0 - psi.u.0).abs() < 1e-9);
        assert!((step2.u.1 - psi.u.1).abs() < 1e-9);
        assert!((step2.d.0 - psi.d.0).abs() < 1e-9);
        assert!((step2.d.1 - psi.d.1).abs() < 1e-9);
    }

    #[test]
    fn test_discrete_dirac_operator_hermiticity_on_simplicial_pair() {
        let v_vols = vec![1.0, 1.0];
        let n_01 = [1.0, 0.0, 0.0];
        let n_10 = [-1.0, 0.0, 0.0];
        let weight = 1.0;
        let conn_01 = SpinConnectionSU2::new_normalized([0.8, 0.6, 0.0, 0.0]).unwrap();
        let conn_10 = conn_01.dagger();

        let edges = vec![
            (0, 1, weight, n_01, conn_01),
            (1, 0, weight, n_10, conn_10),
        ];

        let dirac = SimplicialDiracOperator::new(2, v_vols, edges).unwrap();

        let phi = vec![
            Spinor2::new((1.0, 0.2), (-0.5, 0.3)),
            Spinor2::new((0.4, -0.6), (1.1, 0.7)),
        ];
        let psi = vec![
            Spinor2::new((0.3, 0.9), (0.2, -0.1)),
            Spinor2::new((-0.7, 0.5), (0.8, 0.4)),
        ];

        let is_hermitian = dirac.check_hermiticity(&phi, &psi, 1e-7).unwrap();
        assert!(is_hermitian, "Discrete Dirac operator must be Hermitian");
    }
}
