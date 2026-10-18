
use crate::bicategory::Bicategory;
use crate::error::HigherCategoryError;

#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct CoherenceReport {
    pub pentagons_verified: usize,
    pub triangles_verified: usize,
}

pub fn check_pentagon_coherence<B: Bicategory>(
    bicat: &B,
    f: &B::OneCell,
    g: &B::OneCell,
    h: &B::OneCell,
    k: &B::OneCell,
) -> Result<(), HigherCategoryError> {
    let id_f_2 = bicat.id_2(f)?;
    let id_k_2 = bicat.id_2(k)?;

    let alpha_k_h_g = bicat.associator(g, h, k)?.forward;
    let alpha_h_g_f = bicat.associator(f, g, h)?.forward;

    let h_circ_g = bicat.compose_1(g, h)?;
    let g_circ_f = bicat.compose_1(f, g)?;
    let k_circ_h = bicat.compose_1(h, k)?;

    let alpha_k_hg_f = bicat.associator(f, &h_circ_g, k)?.forward;
    let alpha_kh_g_f = bicat.associator(f, g, &k_circ_h)?.forward;
    let alpha_k_h_gf = bicat.associator(&g_circ_f, h, k)?.forward;

    let step_a1 = bicat.compose_2_horizontal(&id_f_2, &alpha_k_h_g)?;
    let step_a2 = alpha_k_hg_f;
    let step_a3 = bicat.compose_2_horizontal(&alpha_h_g_f, &id_k_2)?;

    let path_a_12 = bicat.compose_2_vertical(&step_a1, &step_a2)?;
    let path_a = bicat.compose_2_vertical(&path_a_12, &step_a3)?;

    let step_b1 = alpha_kh_g_f;
    let step_b2 = alpha_k_h_gf;
    let path_b = bicat.compose_2_vertical(&step_b1, &step_b2)?;

    if path_a == path_b {
        Ok(())
    } else {
        Err(HigherCategoryError::PentagonCoherenceViolation {
            step: format!("Composable 4-chain ({f:?}, {g:?}, {h:?}, {k:?})"),
            path_a: format!("{path_a:?}"),
            path_b: format!("{path_b:?}"),
        })
    }
}

pub fn check_triangle_coherence<B: Bicategory>(
    bicat: &B,
    f: &B::OneCell,
    g: &B::OneCell,
) -> Result<(), HigherCategoryError> {
    let b_ob = bicat.target_0_of_1(f)?;
    let id_b_1 = bicat.id_1(&b_ob)?;
    let id_g_2 = bicat.id_2(g)?;
    let id_f_2 = bicat.id_2(f)?;

    let assoc = bicat.associator(f, &id_b_1, g)?.forward;
    let l_f = bicat.left_unitor(f)?.forward;
    let r_g = bicat.right_unitor(g)?.forward;

    let id_g_star_l_f = bicat.compose_2_horizontal(&l_f, &id_g_2)?;
    let lhs = bicat.compose_2_vertical(&assoc, &id_g_star_l_f)?;

    let rhs = bicat.compose_2_horizontal(&id_f_2, &r_g)?;

    if lhs == rhs {
        Ok(())
    } else {
        Err(HigherCategoryError::TriangleCoherenceViolation {
            left: format!("{lhs:?}"),
            right: format!("{rhs:?}"),
            details: format!("Triangle coherence failed for composable pair ({f:?}, {g:?})"),
        })
    }
}

pub fn verify_bicategory_coherence<B: Bicategory>(
    bicat: &B,
    one_cells: &[B::OneCell],
) -> Result<CoherenceReport, HigherCategoryError> {
    let mut triangles = 0usize;
    let mut pentagons = 0usize;

    for f in one_cells {
        for g in one_cells {
            if bicat.target_0_of_1(f)? == bicat.source_0_of_1(g)? {
                check_triangle_coherence(bicat, f, g)?;
                triangles = triangles.saturating_add(1);
            }
        }
    }

    for f in one_cells {
        for g in one_cells {
            if bicat.target_0_of_1(f)? != bicat.source_0_of_1(g)? {
                continue;
            }
            for h in one_cells {
                if bicat.target_0_of_1(g)? != bicat.source_0_of_1(h)? {
                    continue;
                }
                for k in one_cells {
                    if bicat.target_0_of_1(h)? != bicat.source_0_of_1(k)? {
                        continue;
                    }
                    check_pentagon_coherence(bicat, f, g, h, k)?;
                    pentagons = pentagons.saturating_add(1);
                }
            }
        }
    }

    Ok(CoherenceReport {
        pentagons_verified: pentagons,
        triangles_verified: triangles,
    })
}
