
use crate::complexes::ChainComplexGf2;
use crate::gf2_terminalizer::GF2Matrix;
use serde::{Deserialize, Serialize};

pub const DUAL_OBS_RECEIPT_TAG: &str = "omega.majorana-dual-observer-receipt.v1";

#[derive(Debug, Clone)]
pub struct ObservationMap {
    pub name: &'static str,
    pub matrix: GF2Matrix,
}

impl ObservationMap {
    pub fn apply(&self, omega: &[u8]) -> Result<Vec<u8>, String> {
        if omega.len() != self.matrix.cols {
            return Err("omega / observation matrix shape mismatch".into());
        }
        let mut r = vec![0u8; self.matrix.rows];
        for i in 0..self.matrix.rows {
            let mut acc = 0u8;
            for j in 0..self.matrix.cols {
                acc ^= self.matrix.data[i][j] & (omega[j] % 2);
            }
            r[i] = acc & 1;
        }
        Ok(r)
    }

    pub fn residual_weight(&self, omega: &[u8]) -> Result<usize, String> {
        Ok(self.apply(omega)?.iter().filter(|&&b| b == 1).count())
    }

    pub fn residual_zero(&self, omega: &[u8]) -> Result<bool, String> {
        Ok(self.apply(omega)?.iter().all(|&b| b == 0))
    }
}

pub fn observer_face_syndrome(complex: &ChainComplexGf2) -> ObservationMap {
    ObservationMap {
        name: "O_face_d1",
        matrix: complex.d1.clone(),
    }
}

pub fn observer_first_face_only(complex: &ChainComplexGf2) -> Result<ObservationMap, String> {
    if complex.d1.rows == 0 {
        return Err("no faces".into());
    }
    Ok(ObservationMap {
        name: "O_first_face",
        matrix: GF2Matrix::from_data(vec![complex.d1.data[0].clone()]),
    })
}

pub fn observer_even_edge_parity(num_edges: usize) -> ObservationMap {
    let mut row = vec![0u8; num_edges];
    for j in (0..num_edges).step_by(2) {
        row[j] = 1;
    }
    ObservationMap {
        name: "O_even_edge_xor",
        matrix: GF2Matrix::from_data(vec![row]),
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct DualObserverReceipt {
    pub certificate_tag: String,
    pub complex_name: String,
    pub omega: Vec<u8>,
    pub observer_a: String,
    pub observer_b: String,
    pub residual_a: Vec<u8>,
    pub residual_b: Vec<u8>,
    pub weight_a: usize,
    pub weight_b: usize,
    pub zero_a: bool,
    pub zero_b: bool,
    pub zero_disagreement: bool,
    pub weight_disagreement: bool,
    pub authority_effect: String,
    pub notes: String,
}

pub fn dual_observe(
    complex: &ChainComplexGf2,
    omega: &[u8],
    a: &ObservationMap,
    b: &ObservationMap,
) -> Result<DualObserverReceipt, String> {
    if omega.len() != complex.num_edges {
        return Err("omega length != num_edges".into());
    }
    let ra = a.apply(omega)?;
    let rb = b.apply(omega)?;
    let wa = ra.iter().filter(|&&x| x == 1).count();
    let wb = rb.iter().filter(|&&x| x == 1).count();
    let za = wa == 0;
    let zb = wb == 0;
    let zero_disagreement = za != zb;
    let weight_disagreement = wa != wb;
    let notes = if zero_disagreement {
        format!(
            "Relative residual disagreement: {} zero={} vs {} zero={} on same omega. \
             Same edge vector; two declared observation maps.",
            a.name, za, b.name, zb
        )
    } else if weight_disagreement {
        format!(
            "Weights differ ({} vs {}) but zero-ness agrees (both {}).",
            wa, wb, za
        )
    } else {
        "Observers agree on residual zero-ness and weight (on these maps).".into()
    };
    Ok(DualObserverReceipt {
        certificate_tag: DUAL_OBS_RECEIPT_TAG.into(),
        complex_name: complex.name.into(),
        omega: omega.iter().map(|x| x % 2).collect(),
        observer_a: a.name.into(),
        observer_b: b.name.into(),
        residual_a: ra,
        residual_b: rb,
        weight_a: wa,
        weight_b: wb,
        zero_a: za,
        zero_b: zb,
        zero_disagreement,
        weight_disagreement,
        authority_effect: "None".into(),
        notes,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::complexes::{plaquette, surface_grid_2x2_torus};
    use crate::gf2_terminalizer::GF2Matrix;

    #[test]
    fn edge_off_face_zero_disagrees_with_the_full_syndrome() {
        let c = surface_grid_2x2_torus();
        let o_all = observer_face_syndrome(&c);
        let o_one = observer_first_face_only(&c).unwrap();
        let omega = vec![0, 1, 0, 0, 0, 0, 0, 0];
        let r = dual_observe(&c, &omega, &o_all, &o_one).unwrap();
        assert_eq!(r.residual_a, vec![0, 1, 0, 1]);
        assert_eq!(r.residual_b, vec![0]);
        assert_eq!(r.weight_a, 2);
        assert_eq!(r.weight_b, 0);
        assert!(!r.zero_a);
        assert!(r.zero_b);
        assert!(r.zero_disagreement);
        assert!(r.weight_disagreement);
        assert_eq!(r.omega, omega);

        let err = dual_observe(&c, &[1, 0, 0], &o_all, &o_one).unwrap_err();
        assert!(err.contains("num_edges"), "{err}");
        let mut faceless = c.clone();
        faceless.d1 = GF2Matrix::zeros(0, c.num_edges);
        faceless.num_faces = 0;
        let err = observer_first_face_only(&faceless).unwrap_err();
        assert!(err.contains("no faces"), "{err}");
    }

    #[test]
    fn plaquette_face_vs_even_parity_disagreement() {
        let c = plaquette();
        let o_face = observer_face_syndrome(&c);
        let o_even = observer_even_edge_parity(c.num_edges);
        let omega = vec![1, 0, 0, 0];
        let r = dual_observe(&c, &omega, &o_face, &o_even).unwrap();
        assert_eq!(r.residual_a, vec![1]);
        assert_eq!(r.residual_b, vec![1]);
        assert!(!r.zero_disagreement);
        assert!(!r.weight_disagreement);
        let omega2 = vec![0, 1, 0, 0];
        let r2 = dual_observe(&c, &omega2, &o_face, &o_even).unwrap();
        assert_eq!(r2.residual_a, vec![1]);
        assert_eq!(r2.residual_b, vec![0]);
        assert_eq!(r2.weight_a, 1);
        assert_eq!(r2.weight_b, 0);
        assert!(r2.zero_disagreement);
        let wrong = observer_even_edge_parity(3);
        let err = dual_observe(&c, &omega2, &o_face, &wrong).unwrap_err();
        assert!(err.contains("shape"), "{err}");
    }

    #[test]
    fn zero_omega_agreement() {
        let c = plaquette();
        let r = dual_observe(
            &c,
            &[0, 0, 0, 0],
            &observer_face_syndrome(&c),
            &observer_even_edge_parity(4),
        )
        .unwrap();
        assert_eq!(r.residual_a, vec![0]);
        assert_eq!(r.residual_b, vec![0]);
        assert_eq!((r.weight_a, r.weight_b), (0, 0));
        assert!(r.zero_a && r.zero_b);
        assert!(!r.zero_disagreement);
        assert!(!r.weight_disagreement);
    }
}
