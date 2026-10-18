//! Geometric: E_n-Operads and Homology Operads.
//!
//! AuthorityEffect: None.

use crate::foundation::{OperadColour, Operation, OperationId, OperadSignature, PlanarColoredOperad, SymmetricColoredOperad};

pub fn build_associative_homology_operad() -> Result<PlanarColoredOperad, String> {
    let mut op = PlanarColoredOperad::new("Homology_E1_Ass", false);
    let c = op.add_colour(OperadColour::new("Object")?);
    let mu = Operation::new_generator(
        OperationId::new("mu_mult")?,
        OperadSignature::new(vec![c.clone(), c.clone()], c),
        "Associative multiplication m(x, y)",
    );
    op.add_operation(mu)?;
    op.ensure_identities();
    Ok(op)
}

pub fn build_gerstenhaber_homology_operad() -> Result<SymmetricColoredOperad, String> {
    let mut op = SymmetricColoredOperad::new("Homology_E2_Gerstenhaber", false);
    let c = op.add_colour(OperadColour::new("GradedVectorSpace")?);
    let mut dot = Operation::new_generator(
        OperationId::new("dot_comm")?,
        OperadSignature::new(vec![c.clone(), c.clone()], c.clone()),
        "Commutative multiplication dot(x, y)",
    );
    dot.is_equivariant = true;

    let mut bracket = Operation::new_generator(
        OperationId::new("gerst_bracket")?,
        OperadSignature::new(vec![c.clone(), c.clone()], c),
        "Lie bracket [x, y] of degree -1",
    );
    bracket.is_equivariant = true;

    op.add_operation(dot)?;
    op.add_operation(bracket)?;
    op.ensure_identities();
    Ok(op)
}

pub fn build_commutative_homology_operad() -> Result<SymmetricColoredOperad, String> {
    let mut op = SymmetricColoredOperad::new("Homology_E_infinity_Com", false);
    let c = op.add_colour(OperadColour::new("Object")?);
    let mut mu = Operation::new_generator(
        OperationId::new("mu_comm")?,
        OperadSignature::new(vec![c.clone(), c.clone()], c),
        "Commutative multiplication m(x, y) = m(y, x)",
    );
    mu.is_equivariant = true;
    op.add_operation(mu)?;
    op.ensure_identities();
    Ok(op)
}
