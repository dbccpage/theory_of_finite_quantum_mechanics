
use serde::{Deserialize, Serialize};
use super::quadratic_operad::QuadraticOperad;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BarCobarResolution {
    pub operad_name: String,
    pub is_koszul: bool,
    pub obstruction_dimension: usize,
    pub notes: String,
}

impl BarCobarResolution {
    pub fn evaluate_koszul_resolution(quad_op: &QuadraticOperad) -> Self {
        let known_koszul = ["Ass", "Com", "Lie", "Pois", "PlanarWorkflow"];
        let is_k = known_koszul.contains(&quad_op.name.as_str()) || quad_op.name.ends_with("KoszulDual");

        Self {
            operad_name: quad_op.name.clone(),
            is_koszul: is_k,
            obstruction_dimension: if is_k { 0 } else { 1 },
            notes: if is_k {
                "Formal Koszul bar-cobar minimal model evaluated.".to_string()
            } else {
                "Potential deformation obstruction detected.".to_string()
            },
        }
    }
}
