
#![forbid(unsafe_code)]

use linear_algebra::regge_exact::{cayley_menger, q_i64, q_ratio, signed_volume_4, So4};
use num_rational::BigRational;
use omega_general_relativity::exact_regge::{
    all_hinges_simple, all_tetra_closures_vanish, closed_s4_cube_boundary, defect_bound_holds,
    flat_einstein_hilbert, freudenthal_refine_16, hinge_holonomy, orthogonal_pentatope,
    pythagorean_so4, pythagorean_so4_inverse, rational_regge_proxy, try_transition, ManifoldError,
    SimplicialManifold4D,
};
use serde_json::{json, Value};

fn main() -> std::process::ExitCode {
    let (value, checks_pass) = build_receipt();
    println!("{value}");
    if checks_pass && persist_receipt(&value) {
        std::process::ExitCode::SUCCESS
    } else {
        std::process::ExitCode::from(1)
    }
}

fn build_receipt() -> (Value, bool) {
    let flat = flat_einstein_hilbert();
    let orthogonal = orthogonal_receipt();
    let refinement = refinement_receipt(&flat);
    let closed = closed_s4_receipt();
    let holonomy_ok = holonomy_identity();
    let bound_accepts = manufactured_bound_accepts();
    let bound_rejects = manufactured_bound_rejects();

    let checks_pass = orthogonal.nondegenerate
        && orthogonal.simple
        && orthogonal.closure
        && refinement.volume_conserved
        && refinement.defect_bound_holds
        && closed.nondegenerate
        && closed.simple
        && closed.closure
        && holonomy_ok
        && bound_accepts
        && bound_rejects
        && refinement.children == 16
        && closed.vertices == 32
        && closed.pentatopes == 240
        && orthogonal.euler_characteristic == 1
        && closed.euler_characteristic == 2
        && !orthogonal.signed_volume.is_empty();

    let value = json!({
        "authority_effect": "None",
        "scalar": "BigRational",
        "float_arithmetic": false,
        "classical_regge_action": "not_evaluated_transcendental_deficit",
        "flat_einstein_hilbert": flat.to_string(),
        "orthogonal_pentatope": {
            "signed_volume": orthogonal.signed_volume,
            "volume_squared": orthogonal.volume_squared,
            "nondegenerate": orthogonal.nondegenerate,
            "simple": orthogonal.simple,
            "closure": orthogonal.closure,
            "euler_characteristic": orthogonal.euler_characteristic,
        },
        "refinement": {
            "children": refinement.children,
            "volume_conserved": refinement.volume_conserved,
            "flat_proxy": refinement.flat_proxy,
            "defect_bound_holds": refinement.defect_bound_holds,
        },
        "closed_s4": {
            "vertices": closed.vertices,
            "pentatopes": closed.pentatopes,
            "euler_characteristic": closed.euler_characteristic,
            "nondegenerate": closed.nondegenerate,
            "simple": closed.simple,
            "closure": closed.closure,
        },
        "holonomy_identity": holonomy_ok,
        "manufactured_bound_accepts": bound_accepts,
        "manufactured_bound_rejects": bound_rejects,
    });
    (value, checks_pass)
}

struct OrthogonalReceipt {
    signed_volume: String,
    volume_squared: String,
    nondegenerate: bool,
    simple: bool,
    closure: bool,
    euler_characteristic: i64,
}

fn orthogonal_receipt() -> OrthogonalReceipt {
    let mut receipt = OrthogonalReceipt {
        signed_volume: String::new(),
        volume_squared: String::new(),
        nondegenerate: false,
        simple: false,
        closure: false,
        euler_characteristic: 0,
    };
    let Ok(manifold) = orthogonal_pentatope() else {
        return receipt;
    };
    receipt.nondegenerate = manifold.nondegeneracy().is_ok();
    receipt.simple = ok_true(all_hinges_simple(&manifold));
    receipt.closure = ok_true(all_tetra_closures_vanish(&manifold));
    receipt.euler_characteristic = manifold.euler_characteristic();
    let Ok(chart) = manifold.pentatope(0) else {
        return receipt;
    };
    if let Ok(volume) = signed_volume_4(&chart.coords) {
        receipt.signed_volume = volume.to_string();
    }
    let lengths = squared_edge_block(&chart.coords);
    if let Ok(cayley) = cayley_menger(4, &lengths) {
        receipt.volume_squared = cayley.volume_squared.to_string();
    }
    receipt
}

struct RefinementReceipt {
    children: usize,
    volume_conserved: bool,
    flat_proxy: String,
    defect_bound_holds: bool,
}

fn refinement_receipt(flat: &BigRational) -> RefinementReceipt {
    let mut receipt = RefinementReceipt {
        children: 0,
        volume_conserved: false,
        flat_proxy: String::new(),
        defect_bound_holds: false,
    };
    let Ok(manifold) = orthogonal_pentatope() else {
        return receipt;
    };
    let Ok(chart) = manifold.pentatope(0) else {
        return receipt;
    };
    let Ok(parent_volume) = signed_volume_4(&chart.coords) else {
        return receipt;
    };
    let Ok(children) = freudenthal_refine_16(&chart.coords) else {
        return receipt;
    };
    receipt.children = children.len();
    let mut sum = q_i64(0);
    let mut all_nonzero = !children.is_empty();
    for child in &children {
        match signed_volume_4(child) {
            Ok(volume) if volume != q_i64(0) => sum += volume,
            _ => {
                all_nonzero = false;
                break;
            }
        }
    }
    receipt.volume_conserved = all_nonzero && sum == parent_volume;

    let Ok(refined) = SimplicialManifold4D::from_ambient_pentatopes(&children) else {
        return receipt;
    };
    if refined.nondegeneracy().is_err() {
        return receipt;
    }
    let Ok(proxy) = rational_regge_proxy(&refined, &[]) else {
        return receipt;
    };
    receipt.flat_proxy = proxy.action.to_string();
    receipt.defect_bound_holds = match q_ratio(1, 4) {
        Ok(a_squared) => defect_bound_holds(&proxy.action, flat, &q_i64(1), &a_squared),
        Err(_) => false,
    };
    receipt
}

struct ClosedS4Receipt {
    vertices: u32,
    pentatopes: usize,
    euler_characteristic: i64,
    nondegenerate: bool,
    simple: bool,
    closure: bool,
}

fn closed_s4_receipt() -> ClosedS4Receipt {
    let mut receipt = ClosedS4Receipt {
        vertices: 0,
        pentatopes: 0,
        euler_characteristic: 0,
        nondegenerate: false,
        simple: false,
        closure: false,
    };
    let Ok(sphere) = closed_s4_cube_boundary() else {
        return receipt;
    };
    receipt.vertices = sphere.vertex_count();
    receipt.pentatopes = sphere.pentatope_count();
    receipt.euler_characteristic = sphere.euler_characteristic();
    receipt.nondegenerate = sphere.nondegeneracy().is_ok();
    receipt.simple = ok_true(all_hinges_simple(&sphere));
    receipt.closure = ok_true(all_tetra_closures_vanish(&sphere));
    receipt
}

fn holonomy_identity() -> bool {
    let holonomy: So4 = hinge_holonomy(&[pythagorean_so4(), pythagorean_so4_inverse()]);
    if !holonomy.is_identity() || holonomy.frobenius_defect_squared() != q_i64(0) {
        return false;
    }
    let zero = matrix4([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]);
    let reflection = matrix4([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]);
    try_transition(zero).is_err() && try_transition(reflection).is_err()
}

fn manufactured_bound_accepts() -> bool {
    let Ok(s_regge) = q_ratio(1, 3) else {
        return false;
    };
    let Ok(s_eh) = q_ratio(1, 4) else {
        return false;
    };
    let Ok(a_squared) = q_ratio(1, 16) else {
        return false;
    };
    defect_bound_holds(&s_regge, &s_eh, &q_i64(2), &a_squared)
}

fn manufactured_bound_rejects() -> bool {
    let Ok(a_squared) = q_ratio(1, 4) else {
        return false;
    };
    !defect_bound_holds(&q_i64(1), &q_i64(0), &q_i64(1), &a_squared)
}

fn ok_true(result: Result<bool, ManifoldError>) -> bool {
    matches!(result, Ok(true))
}

fn persist_receipt(value: &Value) -> bool {
    let path =
        std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../tests/omega_general_relativity/fixtures/regge_4d_receipt.json");
    let Some(parent) = path.parent() else {
        return false;
    };
    if std::fs::create_dir_all(parent).is_err() {
        return false;
    }
    let Ok(pretty) = serde_json::to_string_pretty(value) else {
        return false;
    };
    std::fs::write(path, pretty).is_ok()
}

fn squared_edge_block(points: &[[BigRational; 4]; 5]) -> [[BigRational; 5]; 5] {
    std::array::from_fn(|i| {
        std::array::from_fn(|j| {
            if i == j {
                q_i64(0)
            } else {
                squared_distance(&points[i], &points[j])
            }
        })
    })
}

fn squared_distance(left: &[BigRational; 4], right: &[BigRational; 4]) -> BigRational {
    let mut sum = q_i64(0);
    for (left_coord, right_coord) in left.iter().zip(right.iter()) {
        let delta = left_coord - right_coord;
        sum += &delta * &delta;
    }
    sum
}

fn matrix4(entries: [[i64; 4]; 4]) -> [[BigRational; 4]; 4] {
    std::array::from_fn(|row| std::array::from_fn(|col| q_i64(entries[row][col])))
}
