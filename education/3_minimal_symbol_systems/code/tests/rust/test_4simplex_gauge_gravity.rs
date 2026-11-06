//! Integration tests for 4-Simplex Regge Metric Nondegeneracy & Non-Abelian SU(2) Bianchi Verification.
//!
//! AuthorityEffect: None. GenesisEffect: None.

use mssn_stage_024::simplicial_gauge_gravity::{
    verify_4simplex_gauge_gravity, Simplex4GaugeBundle, Simplex4Geometry, SimplicialGaugeError,
    Su2Element,
};

#[test]
fn test_regular_4simplex_volume_reality_passes() {
    let geom = Simplex4Geometry::regular_unit();
    let (det, v4_sq) = geom.verify_volume_reality().expect("Regular 4-simplex must have positive volume");

    // In regular unit 4-simplex: det(C) = -5, V_4^2 = 5 / 9216
    assert!((det - (-5.0)).abs() < 1e-10, "Regular unit 4-simplex Cayley-Menger det must be -5, got {}", det);
    assert!((v4_sq - (5.0 / 9216.0)).abs() < 1e-12, "V_4^2 must be 5/9216");
}

#[test]
fn test_euclidean_orthogonal_4simplex_volume_reality_passes() {
    // Vertices at (0,0,0,0), (1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1)
    // d[0][i] = 1, d[i][j] = 2 for 1 <= i < j <= 4
    let mut d = [[0.0; 5]; 5];
    for i in 1..5 {
        d[0][i] = 1.0;
        d[i][0] = 1.0;
    }
    for i in 1..5 {
        for j in 1..5 {
            if i != j {
                d[i][j] = 2.0;
            }
        }
    }

    let geom = Simplex4Geometry::from_squared_lengths(d);
    let (det, v4_sq) = geom.verify_volume_reality().expect("Orthogonal 4-simplex must have positive volume");

    // V_4 = 1/24, V_4^2 = 1/576 = 16/9216. Det = -16.
    assert!((det - (-16.0)).abs() < 1e-10, "Det must be -16, got {}", det);
    assert!((v4_sq - (1.0 / 576.0)).abs() < 1e-12, "V_4^2 must be 1/576");
}

#[test]
fn test_degenerate_flattened_4simplex_fails_closed() {
    // Zero edge length between 0 and 1 (collapsed edge)
    let mut d = [[1.0; 5]; 5];
    for i in 0..5 {
        d[i][i] = 0.0;
    }
    d[0][1] = 0.0;
    d[1][0] = 0.0;

    let geom = Simplex4Geometry::from_squared_lengths(d);
    let err = geom.verify_volume_reality().expect_err("Collapsed edge must fail volume reality");
    match err {
        SimplicialGaugeError::ErrSimplicialMetricDefect(msg) => {
            assert!(msg.contains("Non-positive 4-volume squared"));
        }
        other => panic!("Expected ErrSimplicialMetricDefect, got: {:?}", other),
    }
}

#[test]
fn test_pure_gauge_su2_bianchi_identity_closes() {
    // Assign 5 distinct non-trivial frame elements at vertices
    let frames = [
        Su2Element::from_axis_angle(0.3, 1.0, 0.0, 0.0),
        Su2Element::from_axis_angle(0.7, 0.0, 1.0, 0.0),
        Su2Element::from_axis_angle(1.2, 0.0, 0.0, 1.0),
        Su2Element::from_axis_angle(0.5, 1.0, 1.0, 0.0),
        Su2Element::from_axis_angle(0.9, 0.0, 1.0, 1.0),
    ];

    let gauge = Simplex4GaugeBundle::pure_gauge(frames);
    let (passed, max_defect) = gauge.verify_tetrahedra_bianchi().expect("Pure gauge bundle must pass Bianchi");

    assert_eq!(passed, 5, "All 5 boundary tetrahedra must pass Bianchi test");
    assert!(max_defect < 1e-13, "Max defect must be numerical zero, got {:.6e}", max_defect);
}

#[test]
fn test_curved_non_abelian_su2_bianchi_identity_closes() {
    // Generate curved link variables: each edge has an arbitrary non-trivial SU(2) rotation
    // All 10 edges get independent elements, so face holonomies R_f != identity (curvature != 0)
    let edges = [
        ((0, 1), Su2Element::from_axis_angle(0.4, 1.0, 0.2, 0.1)),
        ((0, 2), Su2Element::from_axis_angle(0.8, 0.1, 1.0, 0.3)),
        ((0, 3), Su2Element::from_axis_angle(1.1, 0.2, 0.1, 1.0)),
        ((0, 4), Su2Element::from_axis_angle(0.6, 0.5, 0.5, 0.5)),
        ((1, 2), Su2Element::from_axis_angle(0.9, 0.7, 0.3, 0.1)),
        ((1, 3), Su2Element::from_axis_angle(0.3, 0.2, 0.8, 0.4)),
        ((1, 4), Su2Element::from_axis_angle(0.7, 0.4, 0.2, 0.8)),
        ((2, 3), Su2Element::from_axis_angle(1.3, 0.1, 0.9, 0.2)),
        ((2, 4), Su2Element::from_axis_angle(0.5, 0.6, 0.4, 0.5)),
        ((3, 4), Su2Element::from_axis_angle(1.0, 0.3, 0.3, 0.8)),
    ];

    let gauge = Simplex4GaugeBundle::from_links(edges.to_vec());

    // Verify face holonomies are genuinely curved (R_f != I)
    let r012 = gauge.face_holonomy(0, 1, 2);
    assert!(r012.distance_from_identity() > 0.05, "Face holonomy should be non-trivial (curved)");

    // Despite non-zero local curvature, the transported Bianchi loop around each tetrahedron boundary MUST close to identity
    let (passed, max_defect) = gauge.verify_tetrahedra_bianchi().expect("Curved SU(2) connection must satisfy Bianchi identity");

    assert_eq!(passed, 5, "All 5 boundary tetrahedra must satisfy Bianchi identity");
    assert!(max_defect < 1e-13, "Bianchi closure defect must be numerical zero, got {:.6e}", max_defect);
}

#[test]
fn test_full_4simplex_gauge_gravity_receipt() {
    let geom = Simplex4Geometry::regular_unit();
    let frames = [
        Su2Element::from_axis_angle(0.2, 1.0, 0.0, 0.0),
        Su2Element::from_axis_angle(0.4, 0.0, 1.0, 0.0),
        Su2Element::from_axis_angle(0.6, 0.0, 0.0, 1.0),
        Su2Element::from_axis_angle(0.8, 0.5, 0.5, 0.0),
        Su2Element::from_axis_angle(1.0, 0.0, 0.5, 0.5),
    ];
    let gauge = Simplex4GaugeBundle::pure_gauge(frames);

    let receipt = verify_4simplex_gauge_gravity(&geom, &gauge).expect("Full 4-simplex gauge gravity verification must PASS");

    assert_eq!(receipt.status, "PASS");
    assert_eq!(receipt.vertices_count, 5);
    assert_eq!(receipt.edges_count, 10);
    assert_eq!(receipt.triangles_count, 10);
    assert_eq!(receipt.tetrahedra_count, 5);
    assert!(receipt.metric_nondegeneracy_certified);
    assert_eq!(receipt.bianchi_identities_passed, 5);
    assert!(receipt.max_bianchi_closure_defect < 1e-13);
    assert!(receipt.gauge_covariance_certified);

    let json = serde_json::to_string_pretty(&receipt).expect("Receipt must serialize to JSON");
    assert!(json.contains("\"status\": \"PASS\""));
    assert!(json.contains("\"bianchi_identities_passed\": 5"));
}
