
use crate::error::{reserve_exact, HigherCategoryError};
use crate::two_category::TwoCategory;

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

pub fn check_exchange_composability<C: TwoCategory>(
    cat: &C,
    quad: &ExchangeQuadruple<C::TwoCell>,
) -> Result<(), HigherCategoryError> {
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

pub fn verify_exchange_law<C: TwoCategory>(
    cat: &C,
    quad: &ExchangeQuadruple<C::TwoCell>,
) -> Result<(), HigherCategoryError> {
    check_exchange_composability(cat, quad)?;

    let v1 = cat.compose_2_vertical(&quad.alpha_1, &quad.beta_1)?;
    let v2 = cat.compose_2_vertical(&quad.alpha_2, &quad.beta_2)?;
    let lhs = cat.compose_2_horizontal(&v1, &v2)?;

    let h1 = cat.compose_2_horizontal(&quad.alpha_1, &quad.alpha_2)?;
    let h2 = cat.compose_2_horizontal(&quad.beta_1, &quad.beta_2)?;
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

pub fn verify_all_exchange_laws(
    cat: &crate::two_category::Strict2Category,
) -> Result<usize, HigherCategoryError> {
    let mut quadruples = Vec::new();
    let two_cell_ids: Vec<&String> = cat.two_cells.keys().collect();
    let mut verified_count = 0usize;

    for &a1 in &two_cell_ids {
        for &b1 in &two_cell_ids {
            if cat.target_1_of_2(a1)? != cat.source_1_of_2(b1)? {
                continue;
            }
            for &a2 in &two_cell_ids {
                let a1_src1 = cat.source_1_of_2(a1)?;
                let a2_src1 = cat.source_1_of_2(a2)?;
                if cat.target_0_of_1(&a1_src1)? != cat.source_0_of_1(&a2_src1)? {
                    continue;
                }
                for &b2 in &two_cell_ids {
                    if cat.target_1_of_2(a2)? != cat.source_1_of_2(b2)? {
                        continue;
                    }
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
