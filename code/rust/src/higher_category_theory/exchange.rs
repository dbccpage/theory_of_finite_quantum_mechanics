//! Middle-Four Interchange / Exchange Law verification.
//!
//! Evaluates the fundamental 2-categorical coherence:
//! (beta_2 ∘_v alpha_2) *_h (beta_1 ∘_v alpha_1) = (beta_2 *_h beta_1) ∘_v (alpha_2 *_h alpha_1)
//!
//! AuthorityEffect: None.

use crate::error::{reserve_exact, HigherCategoryError};
use crate::two_category::TwoCategory;

/// A 2x2 grid of 2-cells for evaluating the middle-four exchange law.
///
/// Col 1 (A -> B): alpha_1: f_0 => f_1, beta_1: f_1 => f_2
/// Col 2 (B -> C): alpha_2: g_0 => g_1, beta_2: g_1 => g_2
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct ExchangeQuadruple<T> {
    pub alpha_1: T,
    pub beta_1: T,
    pub alpha_2: T,
    pub beta_2: T,
}

impl<T> ExchangeQuadruple<T> {
    pub fn new(alpha_1: T, beta_1: T, alpha_2: T, beta_2: T) -> Self {
        Self {
            alpha_1,
            beta_1,
            alpha_2,
            beta_2,
        }
    }
}

/// Checks whether a quadruple of 2-cells forms a valid composable 2x2 grid.
pub fn check_exchange_composability<C: TwoCategory>(
    cat: &C,
    quad: &ExchangeQuadruple<C::TwoCell>,
) -> Result<(), HigherCategoryError> {
    // 1. Vertical composability in left column: alpha_1 then beta_1
    let a1_tgt = cat.target_1_of_2(&quad.alpha_1)?;
    let b1_src = cat.source_1_of_2(&quad.beta_1)?;
    if a1_tgt != b1_src {
        return Err(HigherCategoryError::VerticalNotComposable {
            alpha: format!("{:?}", quad.alpha_1),
            beta: format!("{:?}", quad.beta_1),
            tgt1: format!("{:?}", a1_tgt),
            src1: format!("{:?}", b1_src),
        });
    }

    // 2. Vertical composability in right column: alpha_2 then beta_2
    let a2_tgt = cat.target_1_of_2(&quad.alpha_2)?;
    let b2_src = cat.source_1_of_2(&quad.beta_2)?;
    if a2_tgt != b2_src {
        return Err(HigherCategoryError::VerticalNotComposable {
            alpha: format!("{:?}", quad.alpha_2),
            beta: format!("{:?}", quad.beta_2),
            tgt1: format!("{:?}", a2_tgt),
            src1: format!("{:?}", b2_src),
        });
    }

    // 3. Horizontal composability in top row: alpha_1 and alpha_2
    let a1_src1 = cat.source_1_of_2(&quad.alpha_1)?;
    let a2_src1 = cat.source_1_of_2(&quad.alpha_2)?;
    let a1_tgt0 = cat.target_0_of_1(&a1_src1)?;
    let a2_src0 = cat.source_0_of_1(&a2_src1)?;
    if a1_tgt0 != a2_src0 {
        return Err(HigherCategoryError::HorizontalNotComposable {
            alpha: format!("{:?}", quad.alpha_1),
            beta: format!("{:?}", quad.alpha_2),
            tgt0: format!("{:?}", a1_tgt0),
            src0: format!("{:?}", a2_src0),
        });
    }

    // 4. Horizontal composability in bottom row: beta_1 and beta_2
    let b1_tgt1 = cat.target_1_of_2(&quad.beta_1)?;
    let b2_tgt1 = cat.target_1_of_2(&quad.beta_2)?;
    let b1_tgt0 = cat.target_0_of_1(&b1_tgt1)?;
    let b2_src0 = cat.source_0_of_1(&b2_tgt1)?;
    if b1_tgt0 != b2_src0 {
        return Err(HigherCategoryError::HorizontalNotComposable {
            alpha: format!("{:?}", quad.beta_1),
            beta: format!("{:?}", quad.beta_2),
            tgt0: format!("{:?}", b1_tgt0),
            src0: format!("{:?}", b2_src0),
        });
    }

    Ok(())
}

/// Verifies that the middle-four interchange law holds for the given quadruple:
/// (beta_2 ∘_v alpha_2) *_h (beta_1 ∘_v alpha_1) == (beta_2 *_h beta_1) ∘_v (alpha_2 *_h alpha_1)
pub fn verify_exchange_law<C: TwoCategory>(
    cat: &C,
    quad: &ExchangeQuadruple<C::TwoCell>,
) -> Result<(), HigherCategoryError> {
    check_exchange_composability(cat, quad)?;

    // Path 1 (Vertical first, then horizontal):
    // v1 = beta_1 ∘_v alpha_1
    let v1 = cat.compose_2_vertical(&quad.alpha_1, &quad.beta_1)?;
    // v2 = beta_2 ∘_v alpha_2
    let v2 = cat.compose_2_vertical(&quad.alpha_2, &quad.beta_2)?;
    // lhs = v2 *_h v1
    let lhs = cat.compose_2_horizontal(&v1, &v2)?;

    // Path 2 (Horizontal first, then vertical):
    // h1 = alpha_2 *_h alpha_1
    let h1 = cat.compose_2_horizontal(&quad.alpha_1, &quad.alpha_2)?;
    // h2 = beta_2 *_h beta_1
    let h2 = cat.compose_2_horizontal(&quad.beta_1, &quad.beta_2)?;
    // rhs = h2 ∘_v h1
    let rhs = cat.compose_2_vertical(&h1, &h2)?;

    if lhs == rhs {
        Ok(())
    } else {
        Err(HigherCategoryError::ExchangeLawViolation {
            left: format!("{:?}", lhs),
            right: format!("{:?}", rhs),
            details: format!(
                "Exchange failure on quadruple: alpha_1={:?}, beta_1={:?}, alpha_2={:?}, beta_2={:?}",
                quad.alpha_1, quad.beta_1, quad.alpha_2, quad.beta_2
            ),
        })
    }
}

/// Validates the interchange law across all composable quadruples in a finite strict 2-category.
/// Employs Soviet Builder allocation discipline (`reserve_exact`).
pub fn verify_all_exchange_laws(
    cat: &crate::two_category::Strict2Category,
) -> Result<usize, HigherCategoryError> {
    let mut quadruples = Vec::new();
    let two_cell_ids: Vec<&String> = cat.two_cells.keys().collect();
    let mut verified_count = 0usize;

    for &a1 in &two_cell_ids {
        for &b1 in &two_cell_ids {
            // Check vertical composability (a1, b1)
            if cat.target_1_of_2(a1)? != cat.source_1_of_2(b1)? {
                continue;
            }
            for &a2 in &two_cell_ids {
                // Check horizontal composability (a1, a2)
                let a1_src1 = cat.source_1_of_2(a1)?;
                let a2_src1 = cat.source_1_of_2(a2)?;
                if cat.target_0_of_1(&a1_src1)? != cat.source_0_of_1(&a2_src1)? {
                    continue;
                }
                for &b2 in &two_cell_ids {
                    // Check vertical composability (a2, b2)
                    if cat.target_1_of_2(a2)? != cat.source_1_of_2(b2)? {
                        continue;
                    }
                    // Check horizontal composability (b1, b2)
                    let b1_tgt1 = cat.target_1_of_2(b1)?;
                    let b2_tgt1 = cat.target_1_of_2(b2)?;
                    if cat.target_0_of_1(&b1_tgt1)? != cat.source_0_of_1(&b2_tgt1)? {
                        continue;
                    }

                    let quad =
                        ExchangeQuadruple::new(a1.clone(), b1.clone(), a2.clone(), b2.clone());
                    reserve_exact(&mut quadruples, 1, &cat.limits)?;
                    quadruples.push(quad);
                }
            }
        }
    }

    for quad in &quadruples {
        verify_exchange_law(cat, quad)?;
        verified_count = verified_count.saturating_add(1);
    }

    Ok(verified_count)
}
