//! C1000 rotation census, computed through the canonical exact Lie group API.
//! The conductor is the trace-field conductor; an axis choice may require
//! additional coefficients without changing that invariant.
// AuthorityEffect: None.
use omega_lie_theory::rotation::{self, RotationError};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

pub const REALISATION_CONVENTION: &str = "REAL_ORTHOGONAL";
pub const DIMENSION: usize = 3;
pub const GROUP_ORDER_BOUND: usize = 60;
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PriceTableRow {
    pub class_id: String,
    pub conductor_price_formula: String,
    pub computed_witness_orders: Vec<usize>,
}
pub fn build_classification_price_table() -> Result<Vec<PriceTableRow>, RotationError> {
    let cyclic = [1, 2, 3, 4, 6]
        .into_iter()
        .map(|m| rotation::cyclic_rotation_group(m).map(|g| g.order()))
        .collect::<Result<Vec<_>, _>>()?;
    let dihedral = [2, 3, 4, 6]
        .into_iter()
        .map(|m| rotation::dihedral_rotation_group(m).map(|g| g.order()))
        .collect::<Result<Vec<_>, _>>()?;
    Ok(vec![
        PriceTableRow {
            class_id: "CYCLIC".into(),
            conductor_price_formula: "conductor of Q(zeta_m + zeta_m^-1)".into(),
            computed_witness_orders: cyclic,
        },
        PriceTableRow {
            class_id: "DIHEDRAL".into(),
            conductor_price_formula: "conductor of Q(zeta_m + zeta_m^-1)".into(),
            computed_witness_orders: dihedral,
        },
        PriceTableRow {
            class_id: "TETRAHEDRAL".into(),
            conductor_price_formula: "1".into(),
            computed_witness_orders: vec![rotation::tetrahedral_group()?.order()],
        },
        PriceTableRow {
            class_id: "OCTAHEDRAL".into(),
            conductor_price_formula: "1".into(),
            computed_witness_orders: vec![rotation::octahedral_group()?.order()],
        },
        PriceTableRow {
            class_id: "ICOSAHEDRAL".into(),
            conductor_price_formula: "5".into(),
            computed_witness_orders: vec![rotation::icosahedral_group()?.order()],
        },
    ])
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RotationGroupsReceipt {
    pub realisation_convention: String,
    pub dimension: usize,
    pub tetrahedral_order: usize,
    pub octahedral_order: usize,
    pub icosahedral_order: usize,
    pub tetrahedral_price: usize,
    pub octahedral_price: usize,
    pub icosahedral_price: usize,
    pub order_census: BTreeMap<usize, usize>,
    pub nonrational_traces: usize,
    pub trace_polynomial_verified: bool,
    pub price_table: Vec<PriceTableRow>,
}
pub fn build_rotation_groups_receipt() -> Result<RotationGroupsReceipt, RotationError> {
    let t = rotation::tetrahedral_group()?;
    let o = rotation::octahedral_group()?;
    let i = rotation::icosahedral_group()?;
    let audit = rotation::icosahedral_trace_field()?;
    let t_orders = (0..t.order())
        .map(|j| t.element_order(j))
        .collect::<Result<Vec<_>, _>>()?;
    let o_orders = (0..o.order())
        .map(|j| o.element_order(j))
        .collect::<Result<Vec<_>, _>>()?;
    Ok(RotationGroupsReceipt {
        realisation_convention: REALISATION_CONVENTION.into(),
        dimension: DIMENSION,
        tetrahedral_order: t.order(),
        octahedral_order: o.order(),
        icosahedral_order: i.order(),
        tetrahedral_price: rotation::trace_field_conductor(t_orders),
        octahedral_price: rotation::trace_field_conductor(o_orders),
        icosahedral_price: audit.conductor,
        order_census: audit.order_census,
        nonrational_traces: audit.nonrational_traces,
        trace_polynomial_verified: audit.all_nonrational_traces_satisfy_minimal_polynomial,
        price_table: build_classification_price_table()?,
    })
}
