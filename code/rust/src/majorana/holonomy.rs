//! Discrete holonomy residual on a declared face (CODE_DEMO).
//!
//! # What this is (only this)
//!
//! Given a **declared** finite complex and a **declared** edge cochain (connection
//! data in a **declared** coefficient monoid), each face has a **holonomy** equal
//! to the ordered product of edge values around that face (for \(\mathbb{F}_2\),
//! the sum mod 2 of incident edges — same linear map as \(d_1\)).
//!
//! The **holonomy residual** on a face is the failure of that product/sum to equal
//! the monoid identity. On \(\mathbb{F}_2\) that residual **is** the face component
//! of \(d_1 A\).
//!
//! # Authority fence
//!
//! - AuthorityEffect: **None** on every receipt.
//! - Does not mint `CertifiedAuthority`, FOC ExactRepair, or continuum curvature.
//! - Does not assert ontology outside the declared carrier and monoid.
//! - Gauge-equivalent connections (differ by \(d_0\alpha\)) share the same face
//!   holonomy residual when \(d_1 d_0 = 0\) — a **declared** identity of the
//!   cochain complex, not a claim about anything outside the packet.

use crate::complexes::ChainComplexGf2;
use crate::gf2_terminalizer::{
    Cyclotomic16Element, GF2Matrix, GF2ScheduleStatus, Gf2CocycleClassifier,
};
use serde::{Deserialize, Serialize};

pub const HOLONOMY_RECEIPT_TAG: &str = "omega.majorana-holonomy-receipt.v1";

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; declared carrier + monoid only; diagnostic receipt.";

/// \(\mathbb{F}_2\) holonomy residual on each face: \(r = d_1 A\).
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct HolonomyReceiptGf2 {
    pub certificate_tag: String,
    pub complex_name: String,
    /// Edge cochain \(A \in C^1(\mathbb{F}_2)\).
    pub connection: Vec<u8>,
    /// Face residuals \(r = d_1 A\) (same length as number of faces).
    pub face_residuals: Vec<u8>,
    /// True iff every face residual is 0.
    pub flat: bool,
    /// Hamming weight of face residual vector.
    pub residual_weight: usize,
    pub boundary_valid: bool,
    /// Always `"None"`.
    pub authority_effect: String,
    pub notes: String,
}

/// Parallel-transport product around one face in \(\mathbb{Q}(\zeta_{16})\) (exact seed monoid).
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct HolonomyReceiptCyclotomic {
    pub certificate_tag: String,
    pub face_index: usize,
    /// Edge indices used on the face walk (as listed in `d1` support).
    pub edge_walk: Vec<usize>,
    /// Product of declared edge elements around the face (basis coeffs).
    pub holonomy_coeffs: [i64; 8],
    /// Residual = holonomy * inverse(identity) failure: true iff holonomy ≠ 1.
    pub residual_nontrivial: bool,
    pub authority_effect: String,
    pub notes: String,
}

/// Face residual vector \(r = d_1 A\) over \(\mathbb{F}_2\).
pub fn face_holonomy_residual_gf2(d1: &GF2Matrix, connection: &[u8]) -> Result<Vec<u8>, String> {
    if connection.len() != d1.cols {
        return Err(format!(
            "connection len {} != d1.cols {}",
            connection.len(),
            d1.cols
        ));
    }
    let mut r = vec![0u8; d1.rows];
    for i in 0..d1.rows {
        let mut acc = 0u8;
        for j in 0..d1.cols {
            acc ^= d1.data[i][j] & (connection[j] % 2);
        }
        r[i] = acc & 1;
    }
    Ok(r)
}

/// Holonomy residual receipt for a declared complex + \(\mathbb{F}_2\) connection.
pub fn holonomy_receipt_gf2(
    complex: &ChainComplexGf2,
    connection: &[u8],
) -> Result<HolonomyReceiptGf2, String> {
    if !complex.verify_boundary() {
        return Err("boundary invalid: d1 d0 != 0 on declared complex".into());
    }
    if connection.len() != complex.num_edges {
        return Err(format!(
            "connection len {} != num_edges {}",
            connection.len(),
            complex.num_edges
        ));
    }
    let face_residuals = face_holonomy_residual_gf2(&complex.d1, connection)?;
    let residual_weight = face_residuals.iter().filter(|&&b| b == 1).count();
    let flat = residual_weight == 0;
    let notes = if flat {
        "All face holonomies are identity in F2 (sum of edge values on each face = 0). \
         Residual weight 0 on the declared complex."
            .into()
    } else {
        format!(
            "Face holonomy residual weight {residual_weight}: at least one face has \
             d1 A = 1. This is a residual of the declared (complex, connection) pair. \
             Same data as OpenObstruction when residual is treated as a 1-cochain syndrome \
             on edges only after adapter choice; here residual lives on faces."
        )
    };
    Ok(HolonomyReceiptGf2 {
        certificate_tag: HOLONOMY_RECEIPT_TAG.into(),
        complex_name: complex.name.into(),
        connection: connection.iter().map(|x| x % 2).collect(),
        face_residuals,
        flat,
        residual_weight,
        boundary_valid: true,
        authority_effect: "None".into(),
        notes,
    })
}

/// Gauge transform: \(A' = A + d_0 \alpha\) (edge coboundary of a vertex 0-cochain).
pub fn gauge_transform_gf2(
    d0: &GF2Matrix,
    connection: &[u8],
    alpha: &[u8],
) -> Result<Vec<u8>, String> {
    if connection.len() != d0.rows || alpha.len() != d0.cols {
        return Err("gauge_transform shape mismatch".into());
    }
    let mut out = vec![0u8; d0.rows];
    for r in 0..d0.rows {
        let mut cob = 0u8;
        for c in 0..d0.cols {
            cob ^= d0.data[r][c] & (alpha[c] % 2);
        }
        out[r] = (connection[r] % 2) ^ cob;
    }
    Ok(out)
}

/// Edge indices with nonzero incidence on face `f` (walk support for products).
pub fn face_edge_support(d1: &GF2Matrix, face: usize) -> Result<Vec<usize>, String> {
    if face >= d1.rows {
        return Err("face index out of range".into());
    }
    Ok((0..d1.cols).filter(|&j| d1.data[face][j] == 1).collect())
}

/// Cyclotomic holonomy around face 0: product of declared edge elements.
///
/// Edge data must have length = number of edges; unused edges may be `one()`.
pub fn holonomy_receipt_cyclotomic_face0(
    complex: &ChainComplexGf2,
    edge_elements: &[Cyclotomic16Element],
) -> Result<HolonomyReceiptCyclotomic, String> {
    if complex.num_faces == 0 {
        return Err("no faces".into());
    }
    if edge_elements.len() != complex.num_edges {
        return Err("edge_elements length mismatch".into());
    }
    let walk = face_edge_support(&complex.d1, 0)?;
    let mut h = Cyclotomic16Element::one();
    for &e in &walk {
        h = h.checked_mul(&edge_elements[e]).ok_or("cyclotomic coefficient overflow")?;
    }
    let residual_nontrivial = h != Cyclotomic16Element::one();
    Ok(HolonomyReceiptCyclotomic {
        certificate_tag: HOLONOMY_RECEIPT_TAG.into(),
        face_index: 0,
        edge_walk: walk,
        holonomy_coeffs: h.coeffs,
        residual_nontrivial,
        authority_effect: "None".into(),
        notes: "Ordered product of declared Cyclotomic16Element on face-0 support. \
                residual_nontrivial iff product ≠ 1 in Z[ζ16]. \
                Declared representation data only."
            .into(),
    })
}

/// Bridge: treat face residual as open if any face has holonomy residual 1,
/// and compare to schedule class when connection is re-read as edge syndrome
/// against the same complex (optional diagnostic link, not an identification of layers).
pub fn connect_to_schedule_class(
    complex: &ChainComplexGf2,
    connection: &[u8],
) -> Result<(HolonomyReceiptGf2, GF2ScheduleStatus), String> {
    let hol = holonomy_receipt_gf2(complex, connection)?;
    let cert = Gf2CocycleClassifier::classify(&complex.d0, &complex.d1, connection)?;
    Ok((hol, cert.status))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::complexes::{plaquette, surface_grid_2x2_torus, torus_logical_x_example, triangle};
    use crate::gf2_terminalizer::GF2Matrix;

    #[test]
    fn plaquette_flat_connection() {
        let c = plaquette();
        // All-zero connection: flat
        let r = holonomy_receipt_gf2(&c, &[0, 0, 0, 0]).unwrap();
        assert!(r.flat);
        assert_eq!(r.residual_weight, 0);
        assert_eq!(r.authority_effect, "None");
        assert_eq!(r.certificate_tag, HOLONOMY_RECEIPT_TAG);
    }

    #[test]
    fn plaquette_single_edge_flux() {
        let c = plaquette();
        // One edge set → face residual 1
        let r = holonomy_receipt_gf2(&c, &[1, 0, 0, 0]).unwrap();
        assert!(!r.flat);
        assert_eq!(r.face_residuals, vec![1]);
        assert_eq!(r.residual_weight, 1);
        assert_eq!(r.authority_effect, "None");
    }

    #[test]
    fn plaquette_full_cycle_flat_in_f2() {
        let c = plaquette();
        // All four edges: sum mod 2 = 0 on the single face
        let r = holonomy_receipt_gf2(&c, &[1, 1, 1, 1]).unwrap();
        assert!(r.flat);
        assert_eq!(r.face_residuals, vec![0]);
    }

    #[test]
    fn gauge_invariance_of_face_residual() {
        // Kills: gauge_transform returning the input connection, which keeps the residual equal.
        let c = plaquette();
        let a = vec![1, 0, 0, 0];
        let a2 = gauge_transform_gf2(&c.d0, &a, &[1, 0, 0, 0]).unwrap();
        assert_eq!(a2, vec![0, 0, 0, 1]);
        let r0 = holonomy_receipt_gf2(&c, &a).unwrap();
        let r1 = holonomy_receipt_gf2(&c, &a2).unwrap();
        assert_eq!(r0.face_residuals, vec![1]);
        assert_eq!(r1.face_residuals, vec![1]);
        assert!(gauge_transform_gf2(&c.d0, &a, &[1, 0])
            .unwrap_err()
            .contains("shape mismatch"));
    }

    #[test]
    fn triangle_holonomy_matches_d1() {
        let c = triangle();
        let a = vec![1, 1, 0];
        let r = holonomy_receipt_gf2(&c, &a).unwrap();
        // d1 = [1,1,1], sum = 0
        assert!(r.flat);
        let a2 = vec![1, 0, 0];
        let r2 = holonomy_receipt_gf2(&c, &a2).unwrap();
        assert_eq!(r2.face_residuals, vec![1]);
    }

    #[test]
    fn torus_single_edge_lights_faces_zero_and_two() {
        // Kills: a length-4 residual that is nonzero but not the support of edge 0.
        let c = surface_grid_2x2_torus();
        let r = holonomy_receipt_gf2(&c, &[1, 0, 0, 0, 0, 0, 0, 0]).unwrap();
        assert_eq!(r.face_residuals, vec![1, 0, 1, 0]);
        assert_eq!(r.residual_weight, 2);
        assert!(!r.flat);
        assert_eq!(face_edge_support(&c.d1, 0).unwrap(), vec![0, 2, 4, 5]);
        assert!(face_edge_support(&c.d1, 4)
            .unwrap_err()
            .contains("out of range"));
    }

    #[test]
    fn refuses_a_short_connection_and_a_broken_boundary() {
        // Kills: skipping the length check or the d1*d0 check.
        let c = plaquette();
        assert!(holonomy_receipt_gf2(&c, &[1, 0, 0])
            .unwrap_err()
            .contains("len"));
        let mut broken = c.clone();
        broken.d1 = GF2Matrix::from_data(vec![vec![1, 0, 0, 0]]);
        assert!(holonomy_receipt_gf2(&broken, &[0, 0, 0, 0])
            .unwrap_err()
            .contains("d1 d0"));
    }

    #[test]
    fn cyclotomic_face0_product_one() {
        let c = plaquette();
        let ones: Vec<_> = (0..4).map(|_| Cyclotomic16Element::one()).collect();
        let r = holonomy_receipt_cyclotomic_face0(&c, &ones).unwrap();
        assert!(!r.residual_nontrivial);
        assert_eq!(r.authority_effect, "None");
        assert_eq!(r.edge_walk.len(), 4);
    }

    #[test]
    fn cyclotomic_face0_zeta_product() {
        let c = plaquette();
        // ζ on one edge: product = ζ ≠ 1
        let mut edges: Vec<_> = (0..4).map(|_| Cyclotomic16Element::one()).collect();
        let mut z = [0i64; 8];
        z[1] = 1; // ζ
        edges[0] = Cyclotomic16Element { coeffs: z };
        let r = holonomy_receipt_cyclotomic_face0(&c, &edges).unwrap();
        // Kills: setting residual_nontrivial without writing the product into the basis.
        assert_eq!(r.holonomy_coeffs, [0, 1, 0, 0, 0, 0, 0, 0]);
        assert!(r.residual_nontrivial);
        edges[1] = Cyclotomic16Element::zeta();
        let r2 = holonomy_receipt_cyclotomic_face0(&c, &edges).unwrap();
        assert_eq!(r2.holonomy_coeffs, [0, 0, 1, 0, 0, 0, 0, 0]);
        assert!(r2.residual_nontrivial);
    }

    #[test]
    fn schedule_bridge_separates_flat_logical_from_open_flux() {
        // Kills: deriving the schedule class from flatness (flat would become Exact).
        let c = plaquette();
        let (h, status) = connect_to_schedule_class(&c, &[1, 0, 0, 0]).unwrap();
        assert_eq!(h.face_residuals, vec![1]);
        assert_eq!(status, GF2ScheduleStatus::OpenObstruction);
        let torus = surface_grid_2x2_torus();
        let (flat, logical) =
            connect_to_schedule_class(&torus, &torus_logical_x_example()).unwrap();
        assert_eq!(flat.face_residuals, vec![0, 0, 0, 0]);
        assert!(flat.flat);
        assert_eq!(logical, GF2ScheduleStatus::ClosedResidual);
    }
}
